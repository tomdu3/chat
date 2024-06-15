from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
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
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")

        if by_user or by_serverid and not request.user.is_authenticated:
            raise AuthenticationFailed(detail="User not authenticated")

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if qty:
            self.queryset = self.queryset.order_by("-id")[: int(qty)]

        if by_serverid:
            try:  # it can break if by_serverid is not an int
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_serverid} not found"
                    )
            except ValueError:
                raise ValidationError(detail=f"Server value error")

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)  # channel details included in serializer
