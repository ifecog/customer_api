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
        fields = ('id', 'dtype', 'doc_number', 'customer')


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
    data_sheet = DatasheetSerializer(read_only=True)
    professions = ProfessionSerializer(many=True)
    document_set = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'professions',
                  'data_sheet', 'is_active', 'status_message', 'num_professions', 'document_set')
        
    def create(self, validated_data):
        professions = validated_data['professions']
        del validated_data['professions']
        
        customer = Customer.objects.create(**validated_data)
        
        for profession in professions:
            prof = Profession.objects.create(**profession)
            customer.professions.add(prof)
            
        customer.save()
        return customer

    def get_num_professions(self, obj):
        return obj.num_professions()
