from rest_framework.filters import SearchFilter


class CustomSearchFilter(SearchFilter):
    search_description = "Qidiruv bo'limi ➡ : full_name, specialty, distance, arrival_time, stars"
