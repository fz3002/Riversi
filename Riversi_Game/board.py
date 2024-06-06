class Board:
    def __init__(self):
        self.player = 0
        self.passed = 0
        self.won = False
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.board[3][3] = "white"
        self.board[3][4] = "black"
        self.board[4][3] = "black"
        self.board[4][4] = "white"
