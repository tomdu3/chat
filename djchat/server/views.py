from django.db.models import Count  # Import Count for annotation
from rest_framework import viewsets  # Import viewsets from DRF
# Import custom exceptions
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response  # Import Response class

from .models import Server  # Import Server model
from .serializers import ServerSerializer  # Import Server serializer


class ServerListViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing and filtering servers.
    """

    queryset = Server.objects.all()  # Define initial queryset

    def list(self, request):
        """
        Handles GET requests to list and filter servers based on query parameters.

        Args:
            request (HttpRequest): The HTTP request object containing query parameters.

        Query Parameters:
            category (str): The category name to filter servers by.
            qty (str): The number of servers to return.
            by_user (str): If "true", filter servers by the authenticated user.
            by_serverid (str): The server ID to filter by.
            with_num_members (str): If "true", include the number of members in the response.

        Raises:
            AuthenticationFailed: If the user is not authenticated when required.
            ValidationError: If the server ID is invalid or not found.

        Returns:
            Response: A DRF Response object containing the serialized server data.
        """

        category = request.query_params.get(
            "category")  # Get category from query params
        qty = request.query_params.get("qty")  # Get qty from query params
        by_user = request.query_params.get(
            "by_user") == "true"  # Check if by_user is true
        by_serverid = request.query_params.get(
            "by_serverid")  # Get server ID from query params
        with_num_members = request.query_params.get(
            "with_num_members") == "true"  # Check if with_num_members is true

        # Check if user authentication is required for by_user or by_serverid
        if by_user or (by_serverid and not request.user.is_authenticated):
            raise AuthenticationFailed(detail="User not authenticated")

        # Filter queryset by category if provided
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Filter queryset by user if by_user is true
        if by_user:
            user_id = request.user.id  # Get the ID of the authenticated user
            self.queryset = self.queryset.filter(member=user_id)

        # Annotate queryset with number of members if with_num_members is true
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Limit the queryset by quantity if qty is provided
        if qty:
            self.queryset = self.queryset.order_by("-id")[: int(qty)]

        # Filter queryset by server ID if by_serverid is provided
        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():  # Raise error if no server found
                    raise ValidationError(
                        detail=f"Server with id {by_serverid} not found"
                    )
            except ValueError:
                # Raise error if server ID is not an integer
                raise ValidationError(detail="Server value error")

        # Serialize the filtered queryset
        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )

        # Return the serialized data in the response
        return Response(serializer.data)

