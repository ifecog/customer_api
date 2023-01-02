from django.shortcuts import render
from .models import (
    Customer,
    Profession,
    Datasheet,
    Document
)
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import (
    CustomerSerializer,
    ProfessionSerializer,
    DatasheetSerializer,
    DocumentSerializer
)
from rest_framework.response import Response
from django.http.response import HttpResponseNotAllowed

# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        active_customers = Customer.objects.all()
        # active_customers = Customer.objects.filter(is_active=True)
        return active_customers

    # def list(self, request, *args, **kwargs):
    #     customers = Customer.objects.filter(id=1)
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # return HttpResponseNotAllowed('not allowed')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(
            name=data['name'], address=data['address'], data_sheet_id=data['data_sheet']
        )
        profession = Profession.objects.get(id=data['profession'])

        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']

        profession = Profession.objects.get(id=data['profession'])

        for p in customer.professions.all():
            customer.professions.remove(p)

        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get(
            'data_sheet', customer.data_sheet_id)

        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()

        return Response('Object removed')

    @action(detail=True)
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.is_active = False
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=True)
    def deactivate_all(self, request, **kwargs):
        customers = Customer.objects.all()
        customers.update(is_active=False)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_status(self, request, **kwargs):
        status = True if request.data['is_active'] == 'True' else False

        customers = Customer.objects.all()
        customers.update(is_active=status)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = Datasheet.objects.all()
    serializer_class = DatasheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
