from django.urls import path
from rest_framework.routers import DefaultRouter

from medical.views import MainCategoriesListAPIView, DoctorCategoryListAPIView, DoctorsListAPIView, \
    TopDoctorsListAPIView, ClientRecentDoctors, DoctoDetailAPIView, CreateAppointmentAPIView

router = DefaultRouter()
urlpatterns = [
    path('main-categories', MainCategoriesListAPIView.as_view(), name="main_categories"),
    path('doctor-categories', DoctorCategoryListAPIView.as_view(), name="doctor_categories"),
    path('doctors-list', DoctorsListAPIView.as_view(), name="doctors_list"),
    path('doctor/<int:pk>', DoctoDetailAPIView.as_view(), name="doctor_detail"),
    path('top-doctors-list', TopDoctorsListAPIView.as_view(), name="top_doctors_list"),
    path('client-recent-doctors-list', ClientRecentDoctors.as_view(), name="client_recent_doctors_list"),
    path('doctor/book', CreateAppointmentAPIView.as_view(), name="client_book_doctor"),
]
