import copy

class Controller:
    def __init__(self, model, view):
        self.board = model
        self.view = view

    def validate(self, board, x, y):
        if self.board.player == 0:
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
                if board[current_x][current_y] is None:
                    break
                if board[current_x][current_y] == color:
                    valid = True
                    break
                current_x += direction_vector[0]
                current_y += direction_vector[1]

        return valid

    def move(self, array, x, y ):
        if self.board.player == 0:
            color = 'black'
        else:
            color = 'white'

        work_array = copy.deepcopy(array)
        neighbours = self.__get_neighbours(array, x, y)

        disk_to_convert = []

        for neighbour in neighbours:
            neighbour_x = neighbour[0]
            neighbour_y = neighbour[1]

            if work_array[neighbour_x][neighbour_y] == color:
                continue

            direction_vector = (neighbour_x-x, neighbour_y-y)
            current_x = neighbour_x
            current_y = neighbour_y
            while 0 <= current_x <= 7 and 0 <= current_y <= 7:
                if work_array[current_x][current_y] is None:
                    break
                if work_array[current_x][current_y] == color:
                    disk_to_convert.append(current_x, current_y)
                    break
                current_x += direction_vector[0]
                current_y += direction_vector[1]
        
        for disk in disk_to_convert:
            work_array[disk[0]][disk[1]] = color

        self.board.switch_players()
        return work_array

    def __get_neighbours(self, board, x, y):
        neighbours = []
        for i in range(max(0, x-1), min(x+2, 8)):
            for j in range(max(0, y-1), min(y+2, 8)):
                if board[i][j] is not None:
                    neighbours.append(board[i][j])
        return neighbours
