"""Module containing controller class handling view and model/s
"""

import copy
import datetime
import json
import os
from types import SimpleNamespace
from exceptions import SaveFormatException
from board import Board


class Controller:
    """Controller class handling communications between model and view in mvc"""

    def __init__(self, model, view, menu, leaderboard):
        self.board: Board = model
        self.view = view
        self.menu = menu
        self.leaderboard = leaderboard
        self.passed = False
        self.end = False
        self.scoreboard: dict[str, int]

        self.read_scores()

    def validate(self, player, x, y) -> bool:
        """Method validating moves given by user

        Args:
            player (int): 0 or 1 depending on color
            x (int): first coordinate of move
            y (int): last coordinate of move

        Returns:
            bool: True if move is valid, False otherwise
        """

        board = self.board.board

        if player == 0:
            color = "black"
        else:
            color = "white"

        if board[x][y] != "":
            return False

        if x < 0 and y < 0 and x > 7 and y > 7:
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

    def move(self, x, y) -> list:
        """Function making a move

        Args:
            x (int): first coordinate of move
            y (int): last coordinate of move

        Returns:
            list(list(str)): board after move
        """

        # Determine color of player
        color = self.board.get_player_color()

        work_board = copy.deepcopy(self.board.board)
        work_board[x][y] = color
        neighbors = self.__get_neighbors(work_board, x, y)

        disk_to_convert = []

        # loop checking every found neighbor for line to convert
        for neighbor in neighbors:
            line = []

            neighbor_x = neighbor[0]
            neighbor_y = neighbor[1]

            if work_board[neighbor_x][neighbor_y] == color:
                continue

            direction_vector = (
                neighbor_x - x,
                neighbor_y - y,
            )  # vector in which way the line will go

            current_x = neighbor_x
            current_y = neighbor_y

            while 0 <= current_x <= 7 and 0 <= current_y <= 7:
                line.append((current_x, current_y))
                if work_board[current_x][current_y] == "":
                    break
                if work_board[current_x][current_y] == color:
                    for disk in line:
                        disk_to_convert.append(disk)
                    break

                current_x += direction_vector[0]
                current_y += direction_vector[1]

        # convert disk to new colors
        for disk in disk_to_convert:
            work_board[disk[0]][disk[1]] = color

        return work_board

    def alpha_beta_min_max(
        self, depth: int, node: list, maximizing_player, alpha, beta
    ) -> tuple:
        """min max function using alpha beta pruning to find best move for ai

        Args:
            depth (int): depth of the decision tree
            node (list): starting board state
            maximizing_player (bool): True(or 1) if player is wants move with highest score
                                    else with the lowest (usually white player is maximizing)
            alpha (int): minimum score maximizing player is assured of
            beta (int): maximum score minimizing player is assured of


        Returns:
            tuple: Depending on depth of current recursion depth returns a tuple
            with score and board state with the best score,
            and when we are not considering leafs of the tree coordinates of move made.

        """
        boards = []
        choices = []

        # get every possible state from current board/node
        for x in range(8):
            for y in range(8):
                if self.validate(maximizing_player, x, y):
                    boards.append(self.move(x, y))
                    choices.append((x, y))

        # Condition to break recursion
        if depth == 0 or len(choices) == 0:
            return (self.__move_score(node, maximizing_player), node)

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

        best = float("inf")
        best_board = []
        best_choice = []
        for board in boards:
            score = self.alpha_beta_min_max(depth - 1, board, True, alpha, beta)[0]
            if score < best:
                best = score
                best_board = board
                best_choice = choices[boards.index(board)]
            beta = min(beta, best)
            if beta <= alpha:
                break
        return (best, best_board, best_choice)

    def __move_score(self, board, maximizing_player) -> int:
        """Simple algorithm evaluating score of given board state
        for maximizing or minimizing player

        Args:
            board (list(list(str))): array representing board state after move
            maximizing_player (bool): True(or 1) if player is wants move with highest score
                                    else with the lowest (usually white player is maximizing)

        Returns:
            int: Score of given board state
        """
        score = 0

        if maximizing_player == 0:
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

        Args:
            x (float): first array coordinate
            y (float): second array coordinate
        """

        if self.validate(self.board.player, int(x), int(y)) and (
            not self.board.ai or (self.board.ai and self.board.player == 0)
        ):
            self.board.board = self.move(int(x), int(y))
            self.view.draw_played_disk(int(x), int(y), self.board.get_player_color())
            self.view.update_board(self.board.board)
            self.switch_turn()

        # Loop for ai to continue making moves if player needs to pass without player clicking mouse
        while True:
            # Check if next player needs to pass
            self.check_pass()
            self.check_if_board_is_full()

            self.handle_pass()

            if self.board.ai and self.board.player == 1:

                self.ai_move()

                self.check_pass()
                self.check_if_board_is_full()
                self.handle_pass()
                if not self.passed:
                    break
            else:
                break  # when ai needs to pass or not ai

    def handle_pass(self):
        """Handle pass and end"""
        if self.passed:
            self.switch_turn()
            if not self.end:
                self.view.pass_window()

        if self.end:
            score = self.get_score()
            self.view.end_game_message(score)

            (nickname_black, nickname_white) = self.view.leaderboard_window()
            self.add_to_scoreboard(score, nickname_black, nickname_white)
            self.save_scores()

            # clearing board after game ends
            self.end = False
            self.passed = False
            self.menu.button_continue["state"] = "disabled"
            self.board = Board()
            self.view.update_board(self.board.board)
            self.menu.root.show_menu()

    def ai_move(self):
        """Computer move"""
        ai_move_result: tuple = self.alpha_beta_min_max(
            3, self.board.board, 1, -float("inf"), float("inf")
        )
        self.board.board = ai_move_result[1]
        if len(ai_move_result) == 3:
            x_ai = ai_move_result[2][0]
            y_ai = ai_move_result[2][1]
            self.view.draw_played_disk(x_ai, y_ai, self.board.get_player_color())

        self.view.update_board(self.board.board)
        self.switch_turn()

    def get_score(self) -> dict:
        """Function to get the score at the end of the game

        Returns:
            dict(int, int): Dictionary of key:player and value:score
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
        """Checks if player needs to pass as there is no valid move to be made"""
        should_pass = True
        valid_moves = self.__find_valid_moves()
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
        """Function ending game if board is full"""
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
            if not self.board.ai:
                self.view.set_current_player_label("white")
        else:
            self.board.player = 0
            if not self.board.ai:
                self.view.set_current_player_label("black")

    def save_to_file(self):
        """Function current game state to file"""
        filename = self.__generate_save_file_name()
        save_dir = "Saves"

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        filepath = os.path.join(save_dir, filename)

        with open(filepath, "w", encoding="UTF-8") as f:
            f.write(repr(self.board))

    def load_form_file(self, filepath: str):
        """Function loading game state from file

        Args:
            filepath (str): file path taken from user
        """
        with open(filepath, "r", encoding="UTF-8") as f:
            read_json = f.readline()
            if self.__validate_data(json.loads(read_json)):
                self.board = json.loads(
                    read_json, object_hook=lambda x: SimpleNamespace(**x)
                )
                self.view.update_board(self.board.board)
            else:
                raise SaveFormatException(f"Invalid save file: {filepath}")

    def save_scores(self):
        """Function saving scoreboard to file"""
        with open("scoreboard.txt", "w", encoding="UTF-8") as f:

            f.write(json.dumps(self.scoreboard))

    def read_scores(self):
        """Function reading scores from file"""
        if os.path.exists("scoreboard.txt"):
            with open("scoreboard.txt", "r", encoding="UTF-8") as f:
                self.scoreboard = json.loads(f.readline())
        else:
            self.scoreboard = {}

        self.leaderboard.populate_leaderboard(self.scoreboard)

    def add_to_scoreboard(self, score: dict, nickname_black: str, nickname_white: str):
        """Function adding score to scoreboard

        Args:
            score (dict): dictionary of scores gotten from get score function
                    with players as keys and scores of played game as values
            nickname_black (str): nickname given by black player
            nickname_white (str): nickname given by white player
        """
        if nickname_black != "null":
            if nickname_black not in self.scoreboard.keys():
                self.scoreboard[nickname_black] = score[0]
            else:
                self.scoreboard[nickname_black] += score[0]
        if nickname_white != "null":
            if nickname_white not in self.scoreboard.keys():
                self.scoreboard[nickname_white] = score[1]
            else:
                self.scoreboard[nickname_white] += score[1]
        self.leaderboard.populate_leaderboard(self.scoreboard)

    def new_game(self):
        """Function starting new game with clean board"""
        self.board = Board()
        self.board.ai = False
        self.view.update_board(self.board.board)
        if self.board.player == 0:
            self.view.set_current_player_label("black")
        else:
            self.view.set_current_player_label("white")

    def new_game_vs_ai(self):
        """Function starting new game vs ai"""
        self.board = Board()
        self.board.ai = True
        self.view.update_board(self.board.board)
        if self.board.player == 0:
            self.view.set_current_player_label("black")
        else:
            self.view.set_current_player_label("white")

    def is_game_vs_ai(self):
        """Is game vs ai

        Returns:
            bool: true if is
        """
        return self.board.ai

    def __generate_save_file_name(self) -> str:
        """Generates game save file name

        Returns:
            str: File name as save+{current date}

        """
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        return f"save_{date_str}.txt"

    def __get_neighbors(self, board: list, x: int, y: int) -> list:
        """Class getting neighbors of given coordinates on the board

        Args:
            board (list): array representing game board
            x (int): first coordinate
            y (int): last coordinate

        Returns:
            list: neighbors of given coordinates
        """
        neighbors = []
        for i in range(max(0, x - 1), min(x + 2, 8)):
            for j in range(max(0, y - 1), min(y + 2, 8)):
                if board[i][j] != "":
                    neighbors.append((i, j))
        return neighbors

    def __find_valid_moves(self) -> list:
        """Function finding all valid moves on the board


        Returns:
            list: List of tuples with coordinates of valid moves
        """
        valid_moves: list[tuple[int, int]] = []
        for row in enumerate(self.board.board):
            for field in enumerate(row[1]):
                if self.validate(self.board.player, row[0], field[0]) is True:
                    valid_moves.append((row[0], field[0]))

        return valid_moves

    def __validate_data(self, data) -> bool:
        """Validate if data in save file conforms to json save format

        Args:
            data (json_data): json data read of file

        Returns:
            bool: True if data in save file conforms to json save format
        """
        required_keys = {
            "ai": bool,
            "player": int,
            "passed": int,
            "won": bool,
            "board": list,
        }

        for key, value_type in required_keys.items():
            if key not in data or not isinstance(data[key], value_type):
                return False

        board = data["board"]
        if len(board) != 8:
            return False

        for row in board:
            if not isinstance(row, list) or len(row) != 8:
                return False
            for cell in row:
                if cell not in {"", "white", "black"}:
                    return False

        return True
