from rest_framework import serializers
from .models import (
    Customer,
    Profession,
    Datasheet,
    Document
)

# Serializers define the API representation.


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

    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'professions',
                  'data_sheet', 'is_active', 'status_message', 'num_professions')

    def get_num_professions(self, obj):
        return obj.num_professions()


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'dtype', 'doc_number', 'customer')
