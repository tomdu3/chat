from rest_framework import serializers

from .models import Category, Channel, Server


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"  # ["id", "name", "owner", "topic", "server"]


class ServerSerializer(serializers.ModelSerializer):
    # using channel_server to get all the channels in the server
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        fields = (
            "__all__"  # ["id", "name", "owner", "category", "description", "member"]
        )
