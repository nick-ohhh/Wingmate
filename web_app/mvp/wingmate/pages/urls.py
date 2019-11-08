from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search/<location>/<date>/<time>', views.full_search, name="full_search"),
]
