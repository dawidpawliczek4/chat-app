from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from .models import Server
from .serializers import ServerSerializer, CategorySerializer
from .schema import server_list_docs

# Create your views here.


class ServerMembershipViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, server_id):
        server = get_object_or_404(Server, id=server_id)
        user = request.user
        if user in server.members.all():
            return Response({"message": "User is already a member of this server"}, status=400)
        server.members.add(user)
        return Response({"message": "User has been added to the server"}, status=200)

    @action(detail=False, methods=['DELETE'])
    def remove_member(self, request, server_id):
        server = get_object_or_404(Server, id=server_id)
        user = request.user

        if user not in server.members.all():
            return Response({"message": "User is not a member of this server"}, status=400)

        if server.owner == user:
            return Response({"message": "Owner cannot remove themselves from the server"}, status=400)

        server.members.remove(user)
        return Response({"message": "User has been removed from the server"}, status=200)

    @action(detail=False, methods=['GET'])
    def is_member(self, request, server_id):
        server = get_object_or_404(Server, id=server_id)
        user = request.user
        is_member = user in server.members.all()
        return Response({"is_member": is_member})


class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return []

    def create(self, request):
        serializer = ServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, members=[request.user])
            return Response(serializer.data, status=201)        
        return Response(serializer.errors, status=400)

    @ server_list_docs
    def list(self, request):
        """
        Retrieves a list of servers based on the provided query parameters.

        Handles the following query parameters for filtering and pagination:
            - category (str, optional): Filters servers by the specified category name (case-insensitive). If not provided, all categories are included.
            - qty (int, optional): Limits the number of servers returned to the specified quantity. If not provided, all matching servers are returned.
            - by_user (bool, optional): If set to "true", filters servers to include only those that the authenticated user is a member of. Requires the user to be authenticated.
            - by_serverid (int, optional): Filters servers by the specified server ID. If the server ID does not exist or is invalid, a ValidationError is raised.
            - with_num_members (bool, optional): If set to "true", includes the number of members in each server in the response.

        Query Parameter Details:
            - 'category': Example usage: ?category=gaming
            - 'qty': Example usage: ?qty=10
            - 'by_user': Example usage: ?by_user=true
            - 'by_serverid': Example usage: ?by_serverid=123
            - 'with_num_members': Example usage: ?with_num_members=true

        Raises:
            AuthenticationFailed: If 'by_user' or 'by_serverid' is specified and the user is not authenticated.
            ValidationError: If 'by_serverid' is specified and is invalid or does not exist.

        Returns:
            Response: A DRF Response object containing serialized server data, which includes:
                - Server details based on the filtering criteria.
                - Number of members in each server if 'with_num_members' is set to "true".

        Example Response:
            [
                {
                    "id": 1,
                    "name": "Server A",
                    "category": "Gaming",
                    "num_members": 25
                },
                {
                    "id": 2,
                    "name": "Server B",
                    "category": "Music",
                    "num_members": 10
                }
            ]

        """
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == "true"
        by_serverid = request.query_params.get('by_serverid')
        with_num_members = request.query_params.get(
            'with_num_members') == "true"

        # if (by_user or by_serverid) and not request.user.is_authenticated:
        #     raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(
                category__name__iexact=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(members=user_id)

        if with_num_members:
            self.queryset = self.queryset.annotate(
                num_members=Count('members'))

        if qty:
            self.queryset = self.queryset[:int(qty)]

        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset:
                    raise ValidationError(detail=f"Server with id {
                                          by_serverid} not found")
            except ValueError:
                raise ValidationError(detail=f"Server with id {
                                      by_serverid} not found")

        serializer = ServerSerializer(self.queryset, many=True, context={
            "num_members": with_num_members})
        return Response(serializer.data)


class CategoryListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    @ extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)
