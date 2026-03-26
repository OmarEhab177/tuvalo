from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("cities/", views.all_cities, name="all_cities"),
    path("cities/<int:city_id>/", views.city_detail, name="city_detail"),
    path("projects/<int:project_id>/", views.project_detail, name="project_detail"),
    path("about/", views.about_page, name="about_page"),
]
