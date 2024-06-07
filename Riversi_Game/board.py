"""Module containing data models for the app"""

import json


class Board:
    """Class representing game board"""

    def __init__(self):
        self.ai = False
        self.player = 0
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.board[3][3] = "white"
        self.board[3][4] = "black"
        self.board[4][3] = "black"
        self.board[4][4] = "white"

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)

    def get_player_color(self) -> str:
        """Function to get current player's color

        Returns:
            str: black is player 0 and white is player 1
        """
        if self.player == 0:
            return "black"
        return "white"
