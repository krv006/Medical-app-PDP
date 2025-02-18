import re

from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField, HiddenField, CurrentUserDefault
from rest_framework.serializers import Serializer, ModelSerializer

from users.gen_code import generate_code
from users.models import User
from users.tasks import send_verification_email, send_verification_phone


class RegisterModelSerializer(ModelSerializer):
    password = CharField(max_length=255, write_only=True)
    phone_number = CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = 'email', 'phone_number', 'first_name', 'last_name', 'password'

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        if phone_number:
            phone: str = re.sub(r'[^\d]', '', phone_number)
            if len(phone) != 12 or not phone.startswith('998'):
                raise ValidationError('Incorrect phone number')
            validated_data['phone_number'] = phone[-9:]
        code = generate_code()
        cache.set(f"{email}_verification", code, timeout=120)
        send_verification_email(email, code)
        return validated_data


class VerifyCodeSerializer(Serializer):
    email = EmailField()
    code = CharField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get('email')
        code = attrs.pop('code')
        gen_code = cache.get(f'{email}_verification')
        if gen_code is None:
            raise ValidationError("Your verification already expired!")
        if code != gen_code:
            raise ValidationError("Code didn't matched")
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return user


class RessetVerifyCodeSerializer(Serializer):
    email = EmailField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get('email')
        if cache.get(f"{email}_verification"):
            raise ValidationError('Your old password is active still!')
        code = generate_code()
        cache.set(f"{email}_verification", code, timeout=120)
        send_verification_email(email, code)
        return attrs


class ResetPasswordSerializer(Serializer):
    email = EmailField(required=False, allow_blank=True, allow_null=True)
    phone = CharField(required=False, allow_blank=True, allow_null=True)
    user = HiddenField(default=CurrentUserDefault())

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get('email')
        phone_number = attrs.get('phone')
        if not email and not phone_number:
            raise ValidationError("Email or phone on of them are required")
        if email:
            if not User.objects.filter(email=email).exists():
                raise ValidationError(f"No such user with email: {email}")
            code = generate_code()
            cache.set(f"{email}_verification", code, timeout=120)
            send_verification_email(email, code)
        if phone_number:
            if not User.objects.filter(phone_number=phone_number).exists():
                raise ValidationError(f"No such user with phone number: {phone_number}")
            code = generate_code()
            cache.set(f"{phone_number}_verification", code, timeout=120)
            send_verification_phone(phone_number, code)
        return attrs


class ConfirmPasswordSerializer(Serializer):
    email = EmailField(required=False, allow_blank=True, allow_null=True)
    phone_number = CharField(required=False, allow_blank=True, allow_null=True)
    password = CharField()
    confirm_password = CharField()
    code = CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get("email")
        code = attrs.pop("code")
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password")
        gen_code_email = cache.get(f'{email}_verification')
        gen_code_phone = cache.get(f'{phone_number}_verification')
        if email:
            if gen_code_email is None:
                raise ValidationError("Your verification already expired!")
            if code != gen_code_email:
                raise ValidationError("Code didn't matched")
        if phone_number:
            if gen_code_phone is None:
                raise ValidationError("Your verification already expired!")
            if code != gen_code_phone:
                raise ValidationError("Code didn't matched")
        if password != confirm_password:
            raise ValidationError("Passwords didn't matched!")
        instance = User.objects.get(email=email) if email else User.objects.get(phone_number=phone_number)
        instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise ValidationError("Invalid email or password")
        return {"user": user}
