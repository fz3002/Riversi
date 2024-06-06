"""Module containing controller class handling view and model/s
"""

# TODO: AI

import copy
import datetime
import json
import os
from types import SimpleNamespace

from attr import validate

from board import Board


class Controller:
    """Controller class handling communications between model and view in mvc"""

    def __init__(self, model, view, menu, leaderboard):
        self.board = model
        self.view = view
        self.menu = menu
        self.leaderboard = leaderboard
        self.passed = False
        self.end = False
        self.scoreboard: dict[str, int]
        self.read_scores()
        self.vs_ai = False

    def validate(self, player, x, y):
        """Method validating moves given by user

        Arguments:
            x -- first coordinate of move
            y -- last coordinate of move

        Returns:
            True if move is valid, False otherwise
        """

        board = self.board.board
        if player == 0:
            color = "black"
        else:
            color = "white"

        if board[x][y] != "":
            return False

        neighbors = self.__get_neighbors(board, x, y)

        if not neighbors:
            return False
        valid = False
        for neighbor in neighbors:
            neighbor_x = neighbor[0]
            neighbor_y = neighbor[1]

            if board[neighbor_x][neighbor_y] == color:
                continue

            direction_vector = (neighbor_x - x, neighbor_y - y)
            current_x = neighbor_x
            current_y = neighbor_y
            while 0 <= current_x <= 7 and 0 <= current_y <= 7:
                if board[current_x][current_y] == "":
                    break
                if board[current_x][current_y] == color:
                    valid = True
                    break
                current_x += direction_vector[0]
                current_y += direction_vector[1]

        return valid

    def move(self, x, y):
        """Function making a move

        Arguments:
            x -- first coordinate of move
            y -- last coordinate of move

        Returns:
            _description_
        """

        board = self.board.board
        if self.board.player == 0:
            color = "black"
        else:
            color = "white"

        work_array = copy.deepcopy(board)
        work_array[x][y] = color
        neighbors = self.__get_neighbors(board, x, y)

        disk_to_convert = []

        for neighbor in neighbors:
            line = []

            neighbor_x = neighbor[0]
            neighbor_y = neighbor[1]

            if work_array[neighbor_x][neighbor_y] == color:
                continue

            direction_vector = (neighbor_x - x, neighbor_y - y)
            current_x = neighbor_x
            current_y = neighbor_y
            while 0 <= current_x <= 7 and 0 <= current_y <= 7:
                line.append((current_x, current_y))
                if work_array[current_x][current_y] == "":
                    break
                if work_array[current_x][current_y] == color:
                    for disk in line:
                        disk_to_convert.append(disk)
                    break

                current_x += direction_vector[0]
                current_y += direction_vector[1]

        for disk in disk_to_convert:
            work_array[disk[0]][disk[1]] = color

        return work_array

    def alpha_beta_min_max(
        self, depth: int, node: list, maximizing_player, alpha, beta
    ):
        nodes = 1
        boards = []
        choices = []

        if depth == 0:
            return (self.move_score(node, maximizing_player), node)

        for x in range(8):
            for y in range(8):
                if self.validate(maximizing_player, x, y):
                    boards.append(self.move(x, y))
                    choices.append((x, y))

        if maximizing_player:
            best = -float("inf")
            best_board = []
            best_choice = []
            for board in boards:
                score = self.alpha_beta_min_max(depth - 1, board, False, alpha, beta)[0]
                if score > best:
                    best = score
                    best_board = board
                    best_choice = choices[boards.index(board)]
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return (best, best_board, best_choice)
        else:
            best = float("inf")
            best_board = []
            best_choice = []
            for board in boards:
                score = self.alpha_beta_min_max(depth - 1, board, True, alpha, beta)[0]
                if score < best:
                    best = score
                    best_board = board
                    best_choice = choices[boards.index(board)]
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return (best, best_board, best_choice)

    def move_score(self, board, maximizingPlayer):
        score = 0

        if maximizingPlayer == 0:
            player = "black"
            enemy = "white"
        else:
            player = "white"
            enemy = "black"

        for row in enumerate(self.board.board):
            for field in enumerate(row[1]):
                if board[row[0]][field[0]] == player:
                    score += 1
                elif board[row[0]][field[0]] == enemy:
                    score -= 1
        return score

    def handle_user_input(self, x, y):
        """Method handling user input for given array coordinates

        Arguments:
            x -- first array coordinate
            y -- second array coordinate
        """
        print("Controller")
        print("validating")
        if self.validate(self.board.player, int(x), int(y)):
            print("moving")
            self.board.board = self.move(int(x), int(y))
            self.switch_turn()
            print("board:", *self.board.board, sep="\n")
            self.view.update_board(self.board.board)
            if self.vs_ai:
                ai_move_result = self.alpha_beta_min_max(
                    3, self.board.board, 1, -float("inf"), float("inf")
                )
                self.board.board = ai_move_result[1]
                self.view.update_board(self.board.board)
                print(self.board.board)
                self.switch_turn()
        self.check_pass()
        self.check_if_board_is_full()
        print("passed : ", self.passed)

        if self.passed:
            print("Pass")
            self.switch_turn()
            self.view.pass_window()

        if self.end:
            score = self.get_score()
            self.view.end_game_message(score)
            (nickname_black, nickname_white) = self.view.leaderboard_window()
            self.add_to_scoreboard(score, nickname_black, nickname_white)
            self.save_scores()

    def get_score(self):
        """Function to get the score at the end of the game

        Returns:
            Dictionary of key:player and value:score
        """
        scores = {0: 0, 1: 0}
        for row in enumerate(self.board.board):
            for color in enumerate(row[1]):
                if color[1] == "black":
                    scores[0] += 1
                else:
                    scores[1] += 1
        return scores

    def check_pass(self):
        """Checks if player needs to pass as there is no valid move to be made

        Returns:
            True if player needs to pass, False otherwise
        """
        should_pass = True
        valid_moves = self.__find_valid_moves()
        print(valid_moves)
        if valid_moves:
            should_pass = False

        if should_pass:
            if self.passed:
                self.end = True
            else:
                self.passed = True
        else:
            self.passed = False

    def check_if_board_is_full(self):
        is_board_full: bool = True
        for row in enumerate(self.board.board):
            for field in enumerate(row[1]):
                if field[1] == "":
                    is_board_full = False
                    break

        if is_board_full:
            self.end = True

    def switch_turn(self):
        """Function to switch whose turn it is"""
        if self.board.player == 0:
            self.board.player = 1
            if not self.vs_ai:
                self.view.set_current_player_label("white")
        else:
            self.board.player = 0
            if not self.vs_ai:
                self.view.set_current_player_label("black")

    def save_to_file(self):
        filename = self.__generate_save_file_name()
        save_dir = "Saves"

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        filepath = os.path.join(save_dir, filename)

        with open(filepath, "w", encoding="UTF-8") as f:
            f.write(repr(self.board))

    def load_form_file(self, filepath):
        with open(filepath, "r", encoding="UTF-8") as f:
            read_json = f.readline()
            self.board = json.loads(
                read_json, object_hook=lambda x: SimpleNamespace(**x)
            )

        self.view.update_board(self.board.board)

    def save_scores(self):
        with open("scoreboard.txt", "w", encoding="UTF-8") as f:

            f.write(json.dumps(self.scoreboard))

    def read_scores(self):
        if os.path.exists("scoreboard.txt"):
            with open("scoreboard.txt", "r", encoding="UTF-8") as f:
                self.scoreboard = json.loads(f.readline())
        else:
            self.scoreboard = {}

        self.leaderboard.populate_leaderboard(self.scoreboard)

    def add_to_scoreboard(self, score, nickname_black, nickname_white):
        if nickname_black not in self.scoreboard.keys():
            self.scoreboard[nickname_black] = score[0]
        else:
            self.scoreboard[nickname_black] += score[0]
        if nickname_white not in self.scoreboard.keys():
            self.scoreboard[nickname_white] = score[1]
        else:
            self.scoreboard[nickname_white] += score[1]
        self.leaderboard.populate_leaderboard(self.scoreboard)

    def new_game(self):
        self.board = Board()
        self.vs_ai = False
        self.view.update_board(self.board.board)
        if self.board.player == 0:
            self.view.set_current_player_label("black")
        else:
            self.view.set_current_player_label("white")
            
            
    def new_game_vs_ai(self):
        self.board = Board()
        self.vs_ai = True
        self.view.update_board(self.board.board)
        if self.board.player == 0:
            self.view.set_current_player_label("black")
        else:
            self.view.set_current_player_label("white")
    
    def __generate_save_file_name(self) -> str:
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        return f"save_{date_str}.txt"

    def __get_neighbors(self, board, x, y):
        """Class getting neighbors of given coordinates on the board

        Arguments:
            board -- array representing game board
            x -- first coordinate
            y -- last coordinate

        Returns:
            list of neighbors of given coordinates
        """
        neighbors = []
        for i in range(max(0, x - 1), min(x + 2, 8)):
            for j in range(max(0, y - 1), min(y + 2, 8)):
                if board[i][j] != "":
                    neighbors.append((i, j))
        return neighbors

    def __find_valid_moves(self):
        print("player: ", self.board.player)
        valid_moves: list[tuple[int, int]] = []
        for row in enumerate(self.board.board):
            for field in enumerate(row[1]):
                if self.validate(self.board.player, row[0], field[0]) is True:
                    valid_moves.append((row[0], field[0]))

        return valid_moves
