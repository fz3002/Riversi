import copy

class Controller:
    def __init__(self, model, view):
        self.board = model
        self.view = view

    def validate(self, board, x, y, player):
        if player == 0:
            color = 'black'
        else:
            color = 'white'

        if board[x][y] is not None:
            return False

        neighbours = self.__get_neighbours(board, x, y)

        if not neighbours:
            return False
        valid = False
        for neighbour in neighbours:
            neighbour_x = neighbour[0]
            neighbour_y = neighbour[1]

            if board[neighbour_x][neighbour_y] == color:
                continue

            direction_vector = (neighbour_x-x, neighbour_y-y)
            current_x = neighbour_x
            current_y = neighbour_y
            while 0 <= current_x <= 7 and 0 <= current_y <= 7:
                if board[current_x][current_y] is not None:
                    break
                if board[current_x][current_y] == color:
                    valid = True
                    break
                current_x += direction_vector[0]
                current_y += direction_vector[1]

        return valid

    def move(self, array, x, y, player ):
        if player == 0:
            color = 'black'
        else:
            color = 'white'

        work_array = copy.deepcopy(array)
        neighbours = self.__get_neighbours(array, x, y)

        for neighbour in neighbours:
            neighbour_x = neighbour[0]
            neighbour_y = neighbour[1]

            if work_array[neighbour_x][neighbour_y] == color:
                continue

            direction_vector = (neighbour_x-x, neighbour_y-y)
            current_x = neighbour_x
            current_y = neighbour_y
            while 0 <= current_x <= 7 and 0 <= current_y <= 7:
                if work_array[current_x][current_y] is not None:
                    #TODO: Handle this if
                if work_array[current_x][current_y] == color:
                    #TODO: handle this if
                current_x += direction_vector[0]
                current_y += direction_vector[1]

    def __get_neighbours(self, board, x, y):
        neighbours = []
        for i in range(max(0, x-1), min(x+2, 8)):
            for j in range(max(0, y-1), min(y+2, 8)):
                if board[i][j] is not None:
                    neighbours.append(board[i][j])
        return neighbours
