from django.db.models import Count  # Import Count for annotation
from rest_framework import viewsets  # Import viewsets from DRF
# Import custom exceptions
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response  # Import Response class
from .schema import server_list_docs
from .models import Server  # Import Server model
# Import Server serializer
from .serializers import ServerSerializer, ChannelSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing and filtering servers.
    """

    queryset = Server.objects.all()  # Define initial queryset

    @server_list_docs
    def list(self, request):
        """
        Handles GET requests to list and filter servers based on query parameters.

        Args:
        request (HttpRequest): The HTTP request object containing query parameters.

        Query Parameters:

        - `category` **(str)**: The category name to filter servers by.
        - `qty` **(str)**: The number of servers to return.
        - `by_user` **(str)**: If "true", filter servers by the authenticated user.
        - `by_serverid` **(str)**: The server ID to filter by.
        - `with_num_members` **(str)**: If "true", include the number of members in the response.

        Raises:

        - `AuthenticationFailed`: If the query contains 'by_user' or 'by_serverid'
            and the user is not authenticated.
        - `ValidationError`: If there is an error in validation or parsing whenhandling
            handling query parameters.

        Returns:
        A DRF Response object containing the serialized server data.

        Examples:

        Get all servers in the "gaming" category:

            GET /api/server/select/?category=gaming

        Get the latest 10 servers:

            GET /api/server/select/?qty=10

        Get servers for the authenticated user:

            GET /api/server/select/?by_user=true

        Get a specific server by its ID:

            GET /api/server/select/?by_serverid=123

        Get all servers with the number of members included:

            GET /api/server/select/?with_num_members=true
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
        # BUG: this wasn't working, hence the change in > if by_user condition
        # if by_user or (by_serverid and not request.user.is_authenticated):
        #    raise AuthenticationFailed(detail="User not authenticated")

        # Filter queryset by category if provided
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Filter queryset by user if by_user is true
        if by_user:
            if request.user.is_authenticated:
                user_id = request.user.id  # Get the ID of the authenticated user
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed(detail="User not authenticated")

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
