from rest_framework import serializers

from chats.models import PrivateRoomChatMessage, PrivateChatRoom


class PrivateRoomSerializer(serializers.ModelSerializer):


    class Meta:
        model = PrivateChatRoom
        fields = [
            'room_id',
            'shop',
            'client',
        ]

class PrivateRoomChatMessageSerializer(serializers.ModelSerializer):
    room = PrivateRoomSerializer(many=False)

    class Meta:
        model = PrivateRoomChatMessage
        fields = ['id','room', 'message', 'timestamp', 'read' ]