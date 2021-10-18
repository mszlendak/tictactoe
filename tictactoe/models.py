from django.db import models
from django.contrib.auth.models import User

WINNING_POSITIONS = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    (3, 5, 7),
    (1, 5, 9),
)

MAX_MOVES = 9


class Match(models.Model):
    players_mapping = {1: "X", 2: "O"}

    tic_tac_toe = [
        ("X", "X"),
        ("O", "O"),
        ("", "Blank"),
    ]

    field_1 = models.CharField(max_length=1, choices=tic_tac_toe, default="")
    field_2 = models.CharField(max_length=1, choices=tic_tac_toe, default="")
    field_3 = models.CharField(max_length=1, choices=tic_tac_toe, default="")
    field_4 = models.CharField(max_length=1, choices=tic_tac_toe, default="")
    field_5 = models.CharField(max_length=1, choices=tic_tac_toe, default="")
    field_6 = models.CharField(max_length=1, choices=tic_tac_toe, default="")
    field_7 = models.CharField(max_length=1, choices=tic_tac_toe, default="")
    field_8 = models.CharField(max_length=1, choices=tic_tac_toe, default="")
    field_9 = models.CharField(max_length=1, choices=tic_tac_toe, default="")

    move = models.IntegerField(default=0)
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="games_won", null=True
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    player_X = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="player_x"
    )
    player_O = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="player_o"
    )

    def make_a_move(self, player: int, move: int) -> str:
        """
        Function to move on the board
        :param player: id of a player
        :param move: number of field 1-9
        :return:
        """
        if (
            self.winner is None
            and self._is_your_turn(player)
            and self._is_move_possible(move)
        ):
            setattr(self, f"field_{move}", self._determine_symbol(player))
            self.move += 1
            if self._check_for_win(player):
                self.winner = User.objects.get(id=player)
                return f"Congratulations You WON, {self._determine_symbol(player)}"
            elif self.move == MAX_MOVES:
                return "It's a tie!"
            return "Correct Move!"
        else:
            if self.winner:
                return "Already finished"
            if self.move == MAX_MOVES:
                return "It's a tie!"
            return "Invalid Move or Player"

    def _is_your_turn(self, player: int) -> bool:
        """
        Check if good player is making move
        :param player: id of a player
        :return:
        """
        player_turn = (self.move % 2) + 1
        player_id = getattr(self, f"player_{self.players_mapping[player_turn]}").id

        return player == player_id

    def _is_move_possible(self, move: int) -> bool:
        """
        Check if field is empty
        :param move: number of field 1-9
        :return:
        """
        return getattr(self, f"field_{move}") == ""

    def _check_for_win(self, player: int) -> bool:
        """
        Check if one of the players won
        :param player: id of the player
        :return:
        """
        positions = []
        for x in range(1, 10):
            attr = getattr(self, f"field_{x}")
            if attr == self._determine_symbol(player):
                positions.append(x)
        return any(
            set(winning_position).issubset(positions)
            for winning_position in WINNING_POSITIONS
        )

    def _determine_symbol(self, player: int) -> str:
        """
        Determine the symbol X or O of current player
        :param player: id of the player
        :return:
        """
        if self.player_X.id == player:
            return "X"
        if self.player_O.id == player:
            return "O"
