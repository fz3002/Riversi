"""Module containing controller class handling view and model/s
"""
#TODO: AI
#TODO: Save to file
#TODO: Read board state from save file

import copy


class Controller:
    """Controller class handling communications between model and view in mvc"""

    def __init__(self, model, view):
        self.board = model
        self.view = view
        self.passed = False
        self.end = False

    def validate(self, x, y):
        """Method validating moves given by user

        Arguments:
            x -- first coordinate of move
            y -- last coordinate of move

        Returns:
            True if move is valid, False otherwise
        """

        board = self.board.board
        if self.board.player == 0:
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

    def handle_user_input(self, x, y):
        """Method handling user input for given array coordinates

        Arguments:
            x -- first array coordinate
            y -- second array coordinate
        """
        print("Controller")
        print("validating")
        if self.validate(int(x), int(y)):
            print("moving")
            self.board.board = self.move(int(x), int(y))
            self.switch_turn()
            print("board:", *self.board.board, sep="\n")
            self.view.update_board(self.board.board)

        self.check_pass()
        self.check_if_board_is_full()
        print("passed : ", self.passed)
        if self.passed:
            print("Pass")
            self.switch_turn()
            self.view.pass_window()

        if self.end:
            score = self.get_score()
            print(score)
            self.view.end_game_message(score)

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
                if field[1] == '':
                    is_board_full =  False
                    break

        if is_board_full:
            self.end = True

    def switch_turn(self):
        """Function to switch whose turn it is"""
        if self.board.player == 0:
            self.board.player = 1
            self.view.set_current_player_label("white")
        else:
            self.board.player = 0
            self.view.set_current_player_label("black")

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
                if self.validate(row[0], field[0]) is True:
                    valid_moves.append((row[0], field[0]))

        return valid_moves
