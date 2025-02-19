from django_filters import FilterSet, NumberFilter

from medical.models import Doctor


class TopDoctorFilterSet(FilterSet):
    limit = NumberFilter(method="filter_limit", label='Limit')

    class Meta:
        model = Doctor
        fields = 'full_name', 'specialty', 'distance', 'arrival_time', 'leave_time'

    def filter_limit(self, queryset, name, value):
        return queryset.order_by("-stars")[:int(value)] if value else queryset
