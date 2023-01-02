from django.shortcuts import render
from .models import (
    Customer,
    Profession,
    Datasheet,
    Document
)
from rest_framework import viewsets
from .serializers import (
    CustomerSerializer,
    ProfessionSerializer,
    DatasheetSerializer,
    DocumentSerializer
)
from rest_framework.response import Response

# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
