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


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = Datasheet.objects.all()
    serializer_class = DatasheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
