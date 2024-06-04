import tkinter as tk
import tkinter.messagebox

class View(tk.Frame):
    def __init__(self, parent, board_size=400, column_count=8):
        super().__init__(parent, borderwidth=15, background="#6e3a00")
        self.current_player_label = tk.Label(parent, text="Player: black")
        self.current_player_label.pack()
        self.pack()
        self.board_size = board_size
        self.column_count = column_count
        self.field_size = self.board_size / self.column_count
        self.disk_size = int(0.8 * self.field_size)
        self.disk_list = [
            [None for _ in range(self.column_count)] for _ in range(self.column_count)
        ]
        self.field_list = [
            [None for _ in range(self.column_count)] for _ in range(self.column_count)
        ]
        self.fields = None
        self.border_size = 5

        self.root = parent

        self.controller = None

        self.draw_board()
        self.fields.bind("<Button-1>", self.mouse_click_handler)
        self.create_start_disks()

    def set_controller(self, controller):
        self.controller = controller

    def draw_board(self):

        self.fields = tk.Canvas(
            self,
            width=self.board_size,
            height=self.board_size,
            highlightbackground="#6e3a00",
        )
        self.fields.pack(fill="both")

        for row in range(self.column_count):
            for column in range(self.column_count):
                field = self.fields.create_rectangle(
                    row * self.field_size,
                    column * self.field_size,
                    (row * self.field_size) + self.field_size,
                    (column * self.field_size) + self.field_size,
                    fill="#026e00",
                    outline="black",
                )
                self.field_list[row][column] = field

    def update_board(self, board):
        self.fields.delete("tile")
        for x in range(self.column_count):
            for y in range(self.column_count):
                if board[x][y] is not None:
                    self.create_disk(x, y, board[x][y])
        self.fields.update()

    def mouse_click_handler(self, event):
        (x, y) = self.get_field_coordinates_after_mouse_click(event)
        self.controller.handle_user_input(x, y)

    def get_field_coordinates_after_mouse_click(self, event):
        col = event.y // self.field_size
        row = event.x // self.field_size
        print(col, row)
        return col, row

    def create_start_disks(self):
        self.create_disk(3, 3, "white")
        self.create_disk(4, 4, "white")
        self.create_disk(4, 3, "black")
        self.create_disk(3, 4, "black")

    def create_disk(self, row, column, color):
        padding = self.field_size - self.disk_size
        disk = self.fields.create_oval(
            (column * self.field_size) + padding,
            (row * self.field_size) + padding,
            (column * self.field_size) + self.disk_size,
            (row * self.field_size) + self.disk_size,
            fill=color,
            tags="tile",
        )
        self.disk_list[row][column] = disk
        return disk

    def set_current_player_label(self, player):
        self.current_player_label.config(text="Player: " + player)

    def end_game_message(self, score):
        win = tk.Toplevel()
        win.wm_title("Game Over")

        winner = max(score, key=lambda x: score[x])

        score_label = tk.Label(win, text=score)
        winner_label = tk.Label(win)
        score_label.pack()
        winner_label.pack()

        back_to_menu_button = tk.Button(win, text="Menu", command=win.destroy)
        back_to_menu_button.pack()

        if winner == 0:
            winner_label.config(text="Black player won!!!")
        else:
            winner_label.config(text="White player won!!!")

        score_label = tk.Label(win, text=score)
        winner_label = tk.Label(win)

    def pass_window(self):
        win = tk.Toplevel()
        l = tk.Label(win, text="Pass")
        win.wm_title("Pass")
        l.pack()
        win.after(1000, lambda x: win.destroy)
