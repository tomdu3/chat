from rest_framework import serializers

from .models import Category, Channel, Server


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"  # ["id", "name", "owner", "topic", "server"]


class ServerSerializer(serializers.ModelSerializer):
    # using channel_server to get all the channels in the server
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        # fields = (
        #     "__all__"  # ["id", "name", "owner", "category", "description", "member"]
        # )
        exclude = [
            "member",
        ]

    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members

        return None

    # remove num_members from representation if not requested as filter
    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")

        if not num_members:
            data.pop("num_members", None)

        return data
