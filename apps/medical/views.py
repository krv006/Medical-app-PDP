import datetime

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.custom_searchfilter import CustomSearchFilter
from base.pagination import CustomPageNumberPagination
from medical.filters import TopDoctorFilterSet, DoctorFilterSet
from medical.models import MainCategory, Category, Doctor, BookAppointment
from medical.serializers import MainCategoriesModelSerializer, CategoryModelSerializer, DoctorsModelSerializer, \
    RecentDoctorsModelSerializer, DoctorDetailModelSerializer, CreateAppointmentModelSerializer


@extend_schema(tags=['Home-page'], description="""
API for get list or detail of main categories
""")
class MainCategoriesListAPIView(ListAPIView):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategoriesModelSerializer
    filter_backends = SearchFilter, DjangoFilterBackend
    search_fields = "name",


@extend_schema(tags=['Home-page'], description="""
API for get list or detail of doctors categories
""")
class DoctorCategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


@extend_schema(tags=['Home-page'], description="""
API for get list of doctors
""")
class DoctorsListAPIView(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorsModelSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = CustomSearchFilter, DjangoFilterBackend
    search_fields = 'full_name', 'specialty', 'distance', 'arrival_time', 'stars'
    filterset_class = DoctorFilterSet


@extend_schema(tags=['Home-page'], description="""
API for get list of top doctors
""")
class TopDoctorsListAPIView(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorsModelSerializer
    filter_backends = DjangoFilterBackend,
    filterset_class = TopDoctorFilterSet
    pagination_class = CustomPageNumberPagination


@extend_schema(tags=['Home-page'], description="""
API for get list of client recent doctors
""")
class ClientRecentDoctors(ListAPIView):
    queryset = BookAppointment.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = IsAuthenticated,

    def list(self, request, *args, **kwargs):
        client = self.request.user
        client_booked_apps = BookAppointment.objects.filter(user=client)
        doctors = Doctor.objects.filter(book_appointments__in=client_booked_apps).distinct()
        page = self.paginate_queryset(doctors)
        if page is not None:
            serializer = RecentDoctorsModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RecentDoctorsModelSerializer(doctors, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Home-page'], description="""
API for doctor detail
""")
class DoctoDetailAPIView(RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailModelSerializer
    permission_classes = IsAuthenticated,

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        doctor = self.get_object()
        doctors_todays_appointments = BookAppointment.objects.filter(
            doctor=doctor,
            created_at__date=datetime.datetime.now().date()
        ).values_list('appointment_date', flat=True)
        arrive_time = doctor.arrival_time.hour
        leave_time = doctor.leave_time.hour
        lunch_time = [doctor.lunch_time.hour, doctor.lunch_time.hour + 1]
        busy_hours = [d.hour for d in doctors_todays_appointments] + lunch_time
        ctx['empty_hours'] = [time for time in range(arrive_time, leave_time + 1) if time not in busy_hours]
        return ctx


@extend_schema(tags=['Home-page'], description="""
API for booking doctor
""")
class CreateAppointmentAPIView(CreateAPIView):
    queryset = BookAppointment.objects.all()
    serializer_class = CreateAppointmentModelSerializer
    permission_classes = IsAuthenticated,
