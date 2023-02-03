from rest_framework import serializers
from .models import (
    Customer,
    Profession,
    Datasheet,
    Document
)

# Serializers define the API representation.


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('dtype', 'doc_number', 'customer')
        read_only_fields = ['customer']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'description', 'status')


class DatasheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datasheet
        fields = ('id', 'description', 'historical_data')


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    data_sheet = DatasheetSerializer()
    professions = ProfessionSerializer(many=True)
    document_set = DocumentSerializer(many=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'professions',
                  'data_sheet', 'is_active', 'status_message', 'num_professions', 'document_set')

    def create(self, validated_data):
        professions = validated_data['professions']
        del validated_data['professions']

        document_set = validated_data['document_set']
        del validated_data['document_set']

        data_sheet = validated_data['data_sheet']
        del validated_data['data_sheet']

        d_sheet = Datasheet.objects.create(**data_sheet)
        customer = Customer.objects.create(**validated_data)
        customer.data_sheet = d_sheet

        for doc in document_set:
            Document.objects.create(
                dtype=doc['dtype'],
                doc_number=doc['doc_number'],
                customer_id=customer.id
            )

        for profession in professions:
            prof = Profession.objects.create(**profession)
            customer.professions.add(prof)

        customer.save()
        return customer

    def get_num_professions(self, obj):
        return obj.num_professions()
