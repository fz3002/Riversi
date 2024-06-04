"""Module containing controller class handling view and model/s
"""

import copy
import view


class Controller:
    """Controller class handling communications between model and view in mvc"""

    def __init__(self, model, view):
        self.board = model
        self.view = view

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

        if board[x][y] is not None:
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
                if board[current_x][current_y] is None:
                    break
                if board[current_x][current_y] == color:
                    valid = True
                    break
                current_x += direction_vector[0]
                current_y += direction_vector[1]

        return valid

    def handle_user_input(self, x, y):
        """Method handling user input for given array coordinates

        Arguments:
            x -- first array coordinate
            y -- second array coordinate
        """
        print("Controller")
        if self.check_pass():
            print("Pass")
            # TODO: Inform user of a need to pass and automatically pass
        else:
            print("validating")
            if self.validate(int(x), int(y)):
                print("moving")
                self.board.board = self.move(int(x),int(y))
                print("board:", *self.board.board, sep="\n")
                self.view.update_board(self.board.board)
        if self.check_game_end():
            #TODO: handle game end
            score = self.get_score()
            print(score)
            #TODO: show end score and winner
        else:
            self.switch_turn()
                

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
            neighbor_x = neighbor[0]
            neighbor_y = neighbor[1]

            if work_array[neighbor_x][neighbor_y] == color:
                continue

            direction_vector = (neighbor_x - x, neighbor_y - y)
            current_x = neighbor_x
            current_y = neighbor_y
            while 0 <= current_x <= 7 and 0 <= current_y <= 7:
                if work_array[current_x][current_y] is None:
                    break
                if work_array[current_x][current_y] == color:
                    break
                disk_to_convert.append((current_x, current_y))
                current_x += direction_vector[0]
                current_y += direction_vector[1]

        for disk in disk_to_convert:
            work_array[disk[0]][disk[1]] = color

        return work_array

    def check_game_end(self):
        """checks if game has ended

        Returns:
            True if game has ended, False otherwise
        """
        return None in self.board.board

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
        for row in enumerate(self.board.board):
            for field in enumerate(row[1]):
                if self.validate(row[0], field[0]) is True:
                    return False

        return True

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
                if board[i][j] is not None:
                    neighbors.append((i,j))
        return neighbors
