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
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
)
from django.http.response import HttpResponseNotAllowed

# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'data_sheet__description']
    filterset_fields = ['name', ]
    ordering_fields = ['name', ]
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        address = self.request.query_params.get('address', None)

        if self.request.query_params.get('is_active') == 'False':
            status = False
        else:
            status = True

        if address:
            customers = Customer.objects.filter(
                address__icontains=address, is_active=status)
        else:
            customers = Customer.objects.filter(is_active=status)

        return customers

    # def list(self, request, *args, **kwargs):
    #     customers = self.get_queryset()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # return HttpResponseNotAllowed('not allowed')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     customer = Customer.objects.create(
    #         name=data['name'], address=data['address'], data_sheet_id=data['data_sheet']
    #     )
    #     profession = Profession.objects.get(id=data['profession'])

    #     customer.professions.add(profession)
    #     customer.save()

    #     serializer = CustomerSerializer(customer)
    #     return Response(serializer.data)

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

    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = self.get_queryset()
        customers.update(is_active=True)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_status(self, request, **kwargs):
        status = True if request.data['is_active'] == 'True' else False

        customers = self.get_queryset()
        customers.update(is_active=status)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = Datasheet.objects.all()
    serializer_class = DatasheetSerializer
    permission_classes = [AllowAny, ]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]
