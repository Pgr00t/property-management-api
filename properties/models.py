from django.db import models


class Property(models.Model):
    """Model representing a real estate property."""

    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Unit(models.Model):
    """Model representing a rentable unit within a property."""

    STATUS_CHOICES = (
        ("available", "Available"),
        ("occupied", "Occupied"),
    )
    property = models.ForeignKey(
        Property, related_name="units", on_delete=models.CASCADE
    )
    unit_number = models.CharField(max_length=50)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )

    def update_status(self):
        """Automatically sync unit status based on active contracts."""
        from django.utils import timezone

        today = timezone.now().date()
        is_occupied = self.contracts.filter(
            start_date__lte=today, end_date__gte=today
        ).exists()
        self.status = "occupied" if is_occupied else "available"
        self.save(update_fields=["status"])

    def __str__(self):
        return f"{self.property.name} - {self.unit_number}"


class Member(models.Model):
    """Model representing a tenant/member."""

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.full_name
