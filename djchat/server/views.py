from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Server
from .serializers import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing and filtering servers.
    """

    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if qty:
            self.queryset = self.queryset.order_by("-id")[: int(qty)]

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)
