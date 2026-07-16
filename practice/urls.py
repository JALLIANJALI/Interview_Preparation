from django.urls import path
from . import views

urlpatterns = [
    path('section/<slug:category_slug>/', views.start_section, name='practice_section'),
    path('<int:question_id>/', views.practice, name='practice'),
    path('end/', views.end_interview, name='end_interview'),
]