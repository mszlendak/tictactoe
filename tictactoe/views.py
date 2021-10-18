from tictactoe.models import Match
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import (
    UserSerializer,
    NewMatchSerializer,
    MatchSerializer,
    PlaySerializer,
)
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.db.models import Count


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.annotate(wins=Count("games_won")).order_by("-wins")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class MatchViewSet(viewsets.ModelViewSet):
    """ "
    API endpoint for creating/viewing/updating matches.
    """

    queryset = Match.objects.all()
    http_method_names = ["get", "post", "put"]
    serializer_class = PlaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.serializer_class = MatchSerializer
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = NewMatchSerializer
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return Response("Not Implemented", status=501)

    @action(detail=True, methods=["put"])
    def move(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                match = Match.objects.get(id=pk)
                response = match.make_a_move(
                    serializer.validated_data["player"],
                    serializer.validated_data["move"],
                )
                match.save()
                return Response({"Response": response}, status=200)
        except Match.DoesNotExist:

            return Response({"Response": "Match does not exist"}, status=400)
