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
    serializer_class = CustomerSerializer

    def get_queryset(self):
        active_customers = Customer.objects.filter(is_active=True)
        return active_customers

    def list(self, request, *args, **kwargs):
        customers = Customer.object.filter(id=1)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        return Response({'message': 'not allowed'})
        # instance = self.get_object()
        # serializer = self.get_serializer(instance)
        # return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = Datasheet.objects.all()
    serializer_class = DatasheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
