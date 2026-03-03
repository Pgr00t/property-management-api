from django.urls import path
from .views import ContractListCreateView

urlpatterns = [
    path('contracts/', ContractListCreateView.as_view(), name='contract-list-create'),
]
