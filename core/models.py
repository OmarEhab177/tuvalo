from django.db import models


class Lead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class City(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="cities/")

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def project_count(self):
        return self.projects.count()


class Project(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="projects/")
    masterplan_image = models.ImageField(
        upload_to="projects/masterplans/", blank=True, null=True
    )
    location = models.TextField(help_text="Location description")
    area = models.CharField(max_length=255, help_text="Total area/space of the project")
    building_ratio = models.CharField(
        max_length=100, blank=True, null=True, help_text="e.g. 50%, 35%"
    )
    composition = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="e.g. residential/hotel, commercial/admin/residential",
    )
    floors = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="e.g. Basement + ground + 3 floors",
    )
    unit_sizes = models.CharField(
        max_length=255, blank=True, null=True, help_text="e.g. (45 : 127) m²"
    )
    payment_plan = models.TextField(
        blank=True, null=True, help_text="Payment plan details"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.city.name}"
