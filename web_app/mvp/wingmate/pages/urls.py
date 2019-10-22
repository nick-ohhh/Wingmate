from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search/<location>/', views.search, name="search"),
    path('search/', views.bad_search, name="bad_search")
]
