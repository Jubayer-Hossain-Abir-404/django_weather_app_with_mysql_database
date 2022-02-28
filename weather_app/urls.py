from django.urls import path
from . import views

urlpatterns = [
    path('', views.CityWeatherView, name="City_Weather"),
    path('remove/<city_name>/', views.City_delete, name="City_remove"),  
    path('update/<city_name>/', views.City_update, name="City_update"),  
]