from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Contract
from .serializers import ContractSerializer

class ContractListCreateView(generics.ListCreateAPIView):
    """
    GET /api/contracts (support ?active=true filtering)
    POST /api/contracts
    """
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contract.objects.all()
        active = self.request.query_params.get('active', None)
        if active == 'true':
            today = timezone.now().date()
            queryset = queryset.filter(start_date__lte=today, end_date__gte=today)
        return queryset
