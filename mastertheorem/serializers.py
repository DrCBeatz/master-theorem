# mastertheorem/serializers.py

from rest_framework import serializers
from .models import Algorithm

class EvaluateMasterTheoremSerializer(serializers.Serializer):
    a = serializers.IntegerField(min_value=1)
    b = serializers.IntegerField(min_value=2)
    k = serializers.IntegerField(min_value=0)

class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = '__all__'