from rest_framework import serializers

from apps.system.models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
