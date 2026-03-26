from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import LeadForm
from .models import City, Project


def landing_page(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thank you! Your message has been sent successfully."
            )
            return redirect("core:landing_page")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LeadForm()

    top_cities = City.objects.all()[:3]
    return render(request, "core/index.html", {"form": form, "top_cities": top_cities})


def all_cities(request):
    cities = City.objects.all()
    return render(request, "core/all_cities.html", {"cities": cities})


def city_detail(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    projects = city.projects.all()

    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thank you! Your message has been sent successfully."
            )
            return redirect("core:city_detail", city_id=city.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LeadForm()

    return render(
        request,
        "core/city_detail.html",
        {
            "city": city,
            "projects": projects,
            "form": form,
        },
    )


def about_page(request):
    return render(request, "core/about.html")


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thank you! Your message has been sent successfully."
            )
            return redirect("core:project_detail", project_id=project.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LeadForm()

    return render(
        request,
        "core/project_detail.html",
        {
            "project": project,
            "form": form,
        },
    )
