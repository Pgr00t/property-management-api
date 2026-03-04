from django.db import models
from django.core.exceptions import ValidationError
from properties.models import Unit, Member
from django.utils import timezone
from decimal import Decimal

class Contract(models.Model):
    """
    Model representing a rental contract between a Member and a Unit.
    """
    member = models.ForeignKey(Member, related_name='contracts', on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, related_name='contracts', on_delete=models.CASCADE)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, editable=False)

    def clean(self):
        """
        Validate overlapping dates for the same unit.
        """
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError("Start date must be before end date.")

            overlapping_contracts = Contract.objects.filter(
                unit=self.unit,
                start_date__lt=self.end_date,
                end_date__gt=self.start_date
            )
            if self.pk:
                overlapping_contracts = overlapping_contracts.exclude(pk=self.pk)
            
            if overlapping_contracts.exists():
                raise ValidationError("This unit is already booked for the selected dates.")

    def calculate_total_value(self):
        """
        Calculate total contract value based on months.
        Calculation: (Months + partial months) * monthly_rent
        For simplicity, we'll calculate the number of days and convert to approximate months,
        or just use the difference in months if requirements imply calendar months.
        Let's use a more precise daily calculation:
        Total Value = (end_date - start_date).days * (monthly_rent / 30)
        Actually, typical property systems use: 
        Value = Monthly Rent * Number of full months + prorated days.
        Let's stick to a simple: total_days * (monthly_rent * 12 / 365) or similar.
        Requirement says: "The system should automatically calculate total contract value".
        Let's use (end - start) in days / 30.44 * monthly_rent.
        """
        delta = self.end_date - self.start_date
        months = Decimal(delta.days) / Decimal('30.44')
        return (months * self.monthly_rent).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        self.full_clean()
        self.total_value = self.calculate_total_value()
        super().save(*args, **kwargs)
        self.unit.update_status()

    def delete(self, *args, **kwargs):
        unit = self.unit
        super().delete(*args, **kwargs)
        unit.update_status()

    def __str__(self):
        return f"Contract: {self.member.full_name} -> {self.unit.unit_number}"
