from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Contract
from .serializers import ContractSerializer

from rest_framework import filters


class ContractListCreateView(generics.ListCreateAPIView):
    """
    GET /api/contracts (support ?active=true filtering)
    POST /api/contracts
    """

    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["member__full_name", "unit__unit_number"]
    ordering_fields = ["start_date", "end_date", "id"]
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Contract.objects.select_related("member", "unit").all()
        active = self.request.query_params.get("active", None)
        today = timezone.now().date()
        if active == "true":
            queryset = queryset.filter(start_date__lte=today, end_date__gte=today)
        elif active == "false":
            from django.db.models import Q

            queryset = queryset.filter(Q(start_date__gt=today) | Q(end_date__lt=today))
        return queryset
