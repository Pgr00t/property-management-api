from rest_framework import serializers
from .models import Contract
from properties.models import Unit


class ContractSerializer(serializers.ModelSerializer):
    monthly_rent = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    member_name = serializers.ReadOnlyField(source="member.full_name")
    unit_number = serializers.ReadOnlyField(source="unit.unit_number")

    class Meta:
        model = Contract
        fields = (
            "id",
            "member",
            "member_name",
            "unit",
            "unit_number",
            "start_date",
            "end_date",
            "monthly_rent",
            "total_value",
        )
        read_only_fields = ("total_value",)

    def validate(self, data):
        """
        Custom validation to handle default rent if not provided.
        """
        if not data.get("monthly_rent"):
            unit = data.get("unit")
            if unit:
                data["monthly_rent"] = unit.monthly_rent
            else:
                raise serializers.ValidationError(
                    {"monthly_rent": "This field is required."}
                )

        contract = Contract(**data)
        try:
            contract.clean()
        except Exception as e:
            raise serializers.ValidationError(
                e.message_dict if hasattr(e, "message_dict") else str(e)
            )

        return data

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)
