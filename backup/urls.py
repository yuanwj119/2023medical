from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.show_student_info, name='student_info'),
]