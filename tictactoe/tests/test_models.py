from django.test import TestCase
from django.contrib.auth.models import User

from tictactoe.models import Match


class MatchModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="test1", email="test1@gmail.com")
        self.user2 = User.objects.create(username="test2", email="test2@gmail.com")

    def test_create_object(self):
        match = Match(self.user1, self.user2)
        assert match

    def test_make_a_correct_move(self):
        match = Match(player_X=self.user1, player_O=self.user2)

        assert match.make_a_move(match.player_X.id, 1) == "Correct Move!"

    def test_move_not_on_your_turn(self):
        match = Match(player_X=self.user1, player_O=self.user2)

        assert match.make_a_move(match.player_O.id, 1) == "Invalid Move or Player"

    def test_invalid_move(self):
        match = Match(player_X=self.user1, player_O=self.user2)

        assert match.make_a_move(match.player_O.id, 12) == "Invalid Move or Player"

    def test_check_for_win(self):
        match = Match(
            player_X=self.user1,
            player_O=self.user2,
            field_1="X",
            field_2="O",
            field_4="X",
            field_5="O",
        )
        assert match.make_a_move(match.player_X.id, 7) == "Congratulations You WON"

    def test_check_for_tie(self):
        match = Match(
            player_X=self.user1,
            player_O=self.user2,
            field_1="O",
            field_2="O",
            field_3="X",
            field_4="X",
            field_5="X",
            field_6="O",
            field_7="O",
            field_8="X",
            move=8,
        )
        assert match == "It's a tie!"
