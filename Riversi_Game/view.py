import tkinter as tk
from tkinter import messagebox
from controller import Controller
from tkinter import filedialog

class Game(tk.Frame):
    def __init__(self, parent, board_size=400, column_count=8):
        self.root = parent
        super().__init__(parent, borderwidth=15, background="#6e3a00")
        self.pack()
        self.button_frame = tk.Frame(self)
        self.button_to_main_window = tk.Button(
            self, text="Go Back To Menu", command=self.root.show_menu
        )
        self.button_to_main_window.pack()
        self.current_player_label = tk.Label(
            self,
            text="Player: black",
            background="#6e3a00",
            foreground="Black",
            font=("BigBlueTerm437 Nerd Font", 25),
            pady=10,
        )
        self.current_player_label.pack()
        self.board_size = board_size
        self.column_count = column_count
        self.field_size = self.board_size / self.column_count
        self.disk_size = int(0.8 * self.field_size)
        self.disk_list = [
            [None for _ in range(self.column_count)] for _ in range(self.column_count)
        ]
        self.fields = self.fields = tk.Canvas(
            self,
            width=self.board_size,
            height=self.board_size,
            highlightbackground="#6e3a00",
        )
        self.fields.pack(fill="both")

        self.border_size = 5

        self.controller: Controller

        self.draw_board()
        self.fields.bind("<Button-1>", self.mouse_click_handler)
        self.create_start_disks()

    def show(self):
        self.lift()

    def set_controller(self, controller):
        self.controller = controller

    def draw_board(self):
        for row in range(self.column_count):
            for column in range(self.column_count):
                self.fields.create_rectangle(
                    row * self.field_size,
                    column * self.field_size,
                    (row * self.field_size) + self.field_size,
                    (column * self.field_size) + self.field_size,
                    fill="#026e00",
                    outline="black",
                )

    def update_board(self, board):
        self.fields.delete("tile")
        for x in range(self.column_count):
            for y in range(self.column_count):
                if board[x][y] != "":
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
        self.current_player_label.config(text="Player: " + player, foreground=player)

    def end_game_message(self, score):
        score_text = "Black: " + str(score[0]) + "\nWhite: " + str(score[1])
        if score[0] > score[1]:
            score_text += "\nBlack Won !!!"
        elif score[0] < score[1]:
            score_text = "\nWhite Won !!!"
        else:
            score_text = "\nDRAW"
        messagebox.showinfo("End Game", score_text)

    def pass_window(self):
        messagebox.showinfo("Pass window", "Pass")


class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background="#6e3a00")
        self.root = parent
        self.controller: Controller
        self.pack(expand=True, fill="both")
        self.label = tk.Label(
            self,
            text="Menu",
            font=("BigBlueTerm437 Nerd Font", 25),
            background="#6e3a00",
            foreground="#ffe200",
            pady=10,
        )
        self.label.pack()
        self.button_play = tk.Button(
            self,
            text="Play",
            command=self.root.show_game,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=20,
            font=("BigBlueTerm437 Nerd Font", 20),
            pady=5,
        )
        self.button_play_vs_ai = tk.Button(
            self,
            text="Play vs AI",
            command=self.root.show_game,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=20,
            font=("BigBlueTerm437 Nerd Font", 20),
            pady=5,
        )
        self.button_save = tk.Button(
            self,
            text="Save",
            command=self.save_button_action,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=20,
            font=("BigBlueTerm437 Nerd Font", 20),
            pady=5,
        )
        self.button_load = tk.Button(
            self,
            text="Load",
            command=self.load_button_action,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=20,
            font=("BigBlueTerm437 Nerd Font", 20),
            pady=5,
        )
        self.button_exit = tk.Button(
            self,
            text="Exit",
            command=self.root.destroy,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=20,
            font=("BigBlueTerm437 Nerd Font", 20),
            pady=5,
        )
        self.button_play.pack()
        self.button_play_vs_ai.pack()
        self.button_save.pack()
        self.button_load.pack()
        self.button_exit.pack()

    def set_controller(self, controller):
        self.controller = controller

    def save_button_action(self):
        self.controller.save_to_file()
        
    def load_button_action(self):
        filepath = filedialog.askopenfilename()
        self.controller.load_form_file(filepath)