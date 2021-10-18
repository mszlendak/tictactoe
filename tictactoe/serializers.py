from django.contrib.auth.models import User
from rest_framework import serializers

import random
from tictactoe.models import Match


class UserSerializer(serializers.HyperlinkedModelSerializer):
    wins = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["url", "username", "email", "wins"]


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"


class NewMatchSerializer(serializers.Serializer):
    player1 = serializers.IntegerField(write_only=True)
    player2 = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        players = [self.validated_data["player1"], self.validated_data["player2"]]
        random.shuffle(players)
        return Match.objects.create(
            player_X=User.objects.get(id=players[0]),
            player_O=User.objects.get(id=players[1]),
        )


class PlaySerializer(serializers.Serializer):
    player = serializers.IntegerField(write_only=True)
    move = serializers.IntegerField(min_value=1, max_value=9, write_only=True)
