from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search/<location>/<date>/<time>', views.full_search, name="full_search"),
    path('search/<location>/', views.location_search_only, name="location_search_only"),
    path('search/', views.bad_search, name="bad_search")
]
