from rest_framework import serializers

from apps.system.models import CustomerLevel
from apps.system.serializers.UserSerializer import UserSerializer


class CustomerLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerLevel
        fields = ["id", "level", "discount", "required_score"]

