from rest_framework import serializers
from apps.animal.models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'nro_identificacion', 'activo', 'raza', 'sexo']
        read_only_fields = fields