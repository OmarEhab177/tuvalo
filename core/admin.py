from django.contrib import admin
from django.utils.html import format_html
from .models import Lead, City, Project, SiteSettings


# ── Helpers ──────────────────────────────────────────────────────────────────

def image_preview(obj, field_name="image", width=60):
    img = getattr(obj, field_name, None)
    if img:
        return format_html(
            '<img src="{}" width="{}" height="{}" '
            'style="object-fit:cover; border-radius:6px; box-shadow:0 1px 4px rgba(0,0,0,.2);" />',
            img.url, width, width,
        )
    return "—"


# ── Inline: Projects inside City ──────────────────────────────────────────────

class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0
    show_change_link = True
    fields = (
        "name", "image", "masterplan_image",
        "location", "area", "building_ratio",
        "composition", "floors", "unit_sizes", "payment_plan",
    )
    classes = ("collapse",)
    verbose_name = "Project"
    verbose_name_plural = "➕ Add / Edit Projects"


# ── City ─────────────────────────────────────────────────────────────────────

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display  = ("city_image_thumb", "name", "project_count")
    search_fields = ("name",)
    inlines       = [ProjectInline]
    save_on_top   = True

    @admin.display(description="Image")
    def city_image_thumb(self, obj):
        return image_preview(obj, "image", 55)


# ── Project ───────────────────────────────────────────────────────────────────

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display   = ("project_image_thumb", "name", "city", "area", "created_at")
    list_filter    = ("city", "created_at")
    search_fields  = ("name", "city__name", "location")
    readonly_fields = ("created_at", "image_preview_full", "masterplan_preview_full")
    list_per_page  = 20
    save_on_top    = True
    date_hierarchy = "created_at"

    fieldsets = (
        ("🏙️ Basic Info", {
            "fields": ("city", "name"),
        }),
        ("🖼️ Images", {
            "fields": (
                "image", "image_preview_full",
                "masterplan_image", "masterplan_preview_full",
            ),
        }),
        ("📋 Project Details", {
            "fields": (
                "location", "area", "building_ratio",
                "composition", "floors", "unit_sizes",
            ),
        }),
        ("💳 Payment", {
            "fields": ("payment_plan",),
        }),
        ("🕒 Meta", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Image")
    def project_image_thumb(self, obj):
        return image_preview(obj, "image", 55)

    @admin.display(description="Main Image Preview")
    def image_preview_full(self, obj):
        return image_preview(obj, "image", 200)

    @admin.display(description="Masterplan Preview")
    def masterplan_preview_full(self, obj):
        return image_preview(obj, "masterplan_image", 200)


# ── Lead ──────────────────────────────────────────────────────────────────────

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display   = ("name", "email_link", "phone", "created_at")
    search_fields  = ("name", "email", "phone")
    list_filter    = ("created_at",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    list_per_page  = 25
    save_on_top    = True

    fieldsets = (
        ("👤 Contact Info", {
            "fields": ("name", "email", "phone"),
        }),
        ("💬 Message", {
            "fields": ("message",),
        }),
        ("🕒 Meta", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Email")
    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)


# ── Site Settings ─────────────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    save_on_top = True

    fieldsets = (
        ("📊 Google", {
            "description": "Add your Google Tag Manager and Analytics IDs here.",
            "fields": ("google_tag_id", "google_analytics_id"),
        }),
        ("📱 Social Pixels", {
            "description": "Add your Facebook and TikTok pixel IDs here.",
            "fields": ("facebook_pixel_id", "tiktok_pixel_id"),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
