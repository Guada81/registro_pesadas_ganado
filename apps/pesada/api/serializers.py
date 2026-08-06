from rest_framework import serializers
from apps.pesada.models import Pesada
from apps.pesada.services import registrar_pesada, RegistroPesadaError

class PesadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesada
        fields = [
            'id',
            'animal',
            'usuario',
            'fecha_hora',
            'peso',
            'unidad_medida',
            'peso_kg',
            'valida',
        ]
        read_only_fields = ['id', 'peso_kg', 'valida', 'usuario']

    def create(self, validated_data):
        """
        En lugar de usar Pesada.objects.create(), 
        delegamos la creación al servicio de la capa de dominio.
        """
        animal = validated_data['animal']
        usuario = validated_data['usuario']
        peso = validated_data['peso']
        unidad_medida = validated_data['unidad_medida']
        fecha_hora = validated_data.get('fecha_hora')

        try:
            pesada = registrar_pesada(
                animal_id=animal.id,
                usuario=usuario,
                peso=peso,
                unidad_medida=unidad_medida,
                fecha_hora=fecha_hora,
            )
            return pesada
        except RegistroPesadaError as e:
            # Captura excepciones del servicio y las lanza como error 400 de la API
            raise serializers.ValidationError({"detail": str(e)})