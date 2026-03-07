from django.contrib import admin
from .models import Lead, City, Project, SiteSettings


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "project_count")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "area", "created_at")
    search_fields = ("name", "city__name", "location")
    list_filter = ("city", "created_at")
    fieldsets = (
        (None, {"fields": ("city", "name", "image", "masterplan_image")}),
        (
            "Details",
            {
                "fields": (
                    "location",
                    "area",
                    "building_ratio",
                    "composition",
                    "floors",
                    "unit_sizes",
                )
            },
        ),
        ("Payment", {"fields": ("payment_plan",)}),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Google",
            {
                "fields": ("google_tag_id", "google_analytics_id"),
            },
        ),
        (
            "Social Pixels",
            {
                "fields": ("facebook_pixel_id", "tiktok_pixel_id"),
            },
        ),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
