from rest_framework import serializers;
from myapp.models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room;
        fields='__all__'
