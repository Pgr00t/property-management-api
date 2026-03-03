from rest_framework import serializers
from .models import Property, Unit, Member

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'property', 'unit_number', 'monthly_rent', 'status')
        read_only_fields = ('property', 'status') # Status handled logically, Property via URL

class PropertySerializer(serializers.ModelSerializer):
    # Could embed units if needed, but requirements just mention properties
    class Meta:
        model = Property
        fields = ('id', 'name', 'address')

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'full_name', 'email')
