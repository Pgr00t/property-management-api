from rest_framework import serializers
from .models import Contract
from properties.models import Unit

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id', 'member', 'unit', 'start_date', 'end_date', 'monthly_rent', 'total_value')
        read_only_fields = ('total_value',)

    def validate(self, data):
        """
        Custom validation to handle default rent if not provided.
        """
        # If monthly_rent is not provided, use unit's monthly_rent.
        # Serializers often require the field if it's not nullable.
        # We can handle this by making it optional in the serializer.
        if not data.get('monthly_rent'):
            unit = data.get('unit')
            if unit:
                data['monthly_rent'] = unit.monthly_rent
            else:
                raise serializers.ValidationError({"monthly_rent": "This field is required."})
        
        # Model-level validation for overlaps is handled in models.py (clean/save).
        # We'll trigger it here to get validation errors in the response.
        contract = Contract(**data)
        try:
            contract.clean()
        except Exception as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else str(e))
        
        return data

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)
