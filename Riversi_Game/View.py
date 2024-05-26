import tkinter as tk
import Exceptions


class View:
    def __init__(self, board_size=400, column_count=8):
        self.board_size = board_size
        self.column_count = column_count
        self.field_size = self.board_size/self.column_count
        self.disk_size = int(0.8 * self.field_size)
        self.disk_list = [[None for _ in range(self.column_count)]
                          for _ in range(self.column_count)]
        self.field_list = [[None for _ in range(self.column_count)]
                           for _ in range(self.column_count)]
        self.board = None
        self.fields = None
        self.border_size = 5

        self.root = tk.Tk()

        self.root.title("Checkers")
        self.root.geometry(
            f'{self.board_size+30}x{self.board_size+30}+100+100')
        self.root.resizable(0, 0)

        self.draw_board()
        self.add_event_handlers()
        self.create_start_disks()
        self.start()

    def draw_board(self):

        self.board = tk.Frame(self.root, borderwidth=15, background='#6e3a00')
        self.board.pack()

        self.fields = tk.Canvas(self.board, width=self.board_size,
                                height=self.board_size, highlightbackground='#6e3a00')
        self.fields.pack(fill='both')

        for row in range(self.column_count):
            for column in range(self.column_count):
                field = self.fields.create_rectangle(row*self.field_size, column*self.field_size,
                                                     (row*self.field_size)+self.field_size, (column *
                                                                                             self.field_size)+self.field_size,
                                                     fill='#026e00', outline='black')
                self.field_list[row][column] = field

        # TODO: click handler

    def start(self):
        self.root.mainloop()

    def create_start_disks(self):
        self.create_disk(4, 4, "black")
        self.create_disk(5, 5, "black")
        self.create_disk(5, 4, "white")
        self.create_disk(4, 5, "white")

    def create_disk(self, row, column, color):
        if self.disk_list[row][column] == None:
            padding = self.field_size - self.disk_size
            disk = self.fields.create_oval(((column-1)*self.field_size)+padding, ((row-1)*self.field_size) +
                                           padding, ((column-1)*self.field_size) + self.disk_size, ((row-1)*self.field_size) + self.disk_size, fill=color)
            self.disk_list[row][column] = disk
            return disk
        else:
            raise Exceptions.FieldTakenException("Field Already Taken")

    def add_event_handlers(self):
        self.fields.tag_bind(
            self.field_list[0][0], '<Button-1>', lambda e: self.create_disk(1, 1, 'white'))
        self.fields.tag_bind(
            self.field_list[0][1], '<Button-1>', lambda e: self.create_disk(2, 1, 'white'))
        self.fields.tag_bind(
            self.field_list[1][0], '<Button-1>', lambda e: self.create_disk(1, 2, 'white'))
        self.fields.tag_bind(
            self.field_list[1][1], '<Button-1>', lambda e: self.create_disk(2, 2, 'white'))

    def __find_element(self, matrix, target):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == target:
                    return (i, j)
        return None


View()
