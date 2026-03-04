from rest_framework import serializers
from .models import Property, Unit, Member


class UnitSerializer(serializers.ModelSerializer):
    property_name = serializers.ReadOnlyField(source="property.name")

    class Meta:
        model = Unit
        fields = (
            "id",
            "property",
            "property_name",
            "unit_number",
            "monthly_rent",
            "status",
        )
        read_only_fields = ("property", "status")


class PropertySerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ("id", "name", "address", "units")


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id", "full_name", "email")
