import time
import tkinter as tk
from tkinter import Scrollbar, messagebox
from controller import Controller
from tkinter import filedialog
from tkinter import simpledialog


class Game(tk.Frame):
    def __init__(self, parent, board_size=400, column_count=8):
        self.root = parent
        super().__init__(parent, borderwidth=15, background="#6e3a00")
        self.pack()
        self.button_frame = tk.Frame(self)
        self.button_to_main_window = tk.Button(
            self,
            text="Menu",
            command=self.root.show_menu,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=10,
            font=("BigBlueTerm437 Nerd Font", 20),
        )
        self.button_to_main_window.pack()
        self.current_player_label = tk.Label(
            self,
            text="Player: black",
            background="#6e3a00",
            foreground="Black",
            font=("BigBlueTerm437 Nerd Font", 25),
            pady=15,
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

    def draw_played_disk(self, x, y, color):
        
        self.create_disk(x, y, color)
        self.fields.update()
        time.sleep(0.5)
    
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

    def leaderboard_window(self):
        choice = messagebox.askquestion(
            title="LeaderBoard",
            message="BlackPlayer | Do you want to add your score to leaderboard",
            type=messagebox.YESNO,
        )
        if choice:
            nickname_black = simpledialog.askstring(
                "Nickname", "Enter Nickname: ", parent=self
            )
        choice = messagebox.askquestion(
            title="LeaderBoard",
            message="WhitePlayer | Do you want to add your score to leaderboard",
            type=messagebox.YESNO,
        )
        if choice:
            nickname_white = simpledialog.askstring(
                "Nickname", "Enter Nickname: ", parent=self
            )

        return (nickname_black, nickname_white)


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
        self.button_continue = tk.Button(
            self,
            text="Continue",
            command=self.root.show_game,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=20,
            font=("BigBlueTerm437 Nerd Font", 20),
            pady=5,
            state="disabled"
        )
        self.button_new_game = tk.Button(
            self,
            text="New Game",
            command=self.new_game_button_action,
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
            text="New Game vs AI",
            command=self.new_game_vs_ai_button_action,
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
        self.button_leaderBoard = tk.Button(
            self,
            text="Leaderboard",
            command=self.root.show_leaderboard,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=20,
            font=("BigBlueTerm437 Nerd Font", 20),
            pady=5,
        )
        self.button_continue.pack()
        self.button_new_game.pack()
        self.button_play_vs_ai.pack()
        self.button_save.pack()
        self.button_load.pack()
        self.button_leaderBoard.pack()
        self.button_exit.pack()

    def set_controller(self, controller):
        self.controller = controller

    def save_button_action(self):
        self.controller.save_to_file()

    def load_button_action(self):
        filepath = filedialog.askopenfilename(
            defaultextension="txt", initialdir="Saves"
        )
        self.controller.load_form_file(filepath)
        self.button_continue["state"] = "normal"

    def new_game_button_action(self):
        self.button_continue["state"] = "normal"
        self.controller.new_game()
        self.root.show_game()
        
    def new_game_vs_ai_button_action(self):
        self.button_continue["state"] = "normal"
        self.controller.new_game_vs_ai()
        self.root.show_game()

class Leaderboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, background="#6e3a00")
        self.root = parent
        self.controller: Controller
        self.pack(expand=True, fill="both")
        self.button_to_main_window = tk.Button(
            self,
            text="Menu",
            command=self.root.show_menu,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=10,
            font=("BigBlueTerm437 Nerd Font", 20),
        )
        self.button_to_main_window.pack()
        self.scroll_bar = Scrollbar(self)
        self.leaderboard = tk.Text(
            self,
            wrap="word",
            background="#6e3a00",
            foreground="#ffe200",
            yscrollcommand=self.scroll_bar.set,
            font=("BigBlueTerm437 Nerd Font", 20),
        )
        self.scroll_bar.pack(side="left", fill="y")
        self.leaderboard.pack(side="right", fill="both", expand=True)

        # TODO: add elements to the leaderboard

    def set_controller(self, controller):
        self.controller = controller

    def populate_leaderboard(self, dict):
        for key, value in dict.items():
            self.leaderboard.insert(tk.END, f"{key}: {value}\n")
