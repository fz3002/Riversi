"""Module containing views for application"""

from json import JSONDecodeError
from tkinter import filedialog
from tkinter import simpledialog
import time
import tkinter as tk
from tkinter import Scrollbar, messagebox
from exceptions import SaveFormatException
from controller import Controller


class Game(tk.Frame):
    """Class representing game windows"""

    def __init__(self, parent, board_size=400, column_count=8):
        self.root = parent
        super().__init__(
            parent, borderwidth=15, background="#6e3a00", width=500, height=500
        )
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
            font=("Impact", 20),
        )
        self.button_to_main_window.pack()
        self.current_player_label = tk.Label(
            self,
            text="Player: black",
            background="#6e3a00",
            foreground="Black",
            font=("Impact", 25),
            pady=15,
        )
        self.current_player_label.pack()
        self.board_size = board_size
        self.column_count = column_count
        self.field_size = self.board_size / self.column_count
        self.disk_size = int(0.8 * self.field_size)
        self.disk_list = [
            [0 for _ in range(self.column_count)] for _ in range(self.column_count)
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

    def set_controller(self, controller: Controller):
        """Controller setter

        Args:
            controller (Controller): instance of Controller
        """
        self.controller = controller

    def draw_board(self):
        """Function drawing initial board"""
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
        """Function draws played disk before updating whole board

        Args:
            x (int): first disk coordinate
            y (int): second disk coordinate
            color (string): disk color
        """
        self.create_disk(x, y, color)
        self.fields.update()
        time.sleep(0.5)

    def update_board(self, board):
        """Function updating whole board with flipped disk

        Args:
            board (list[list[string]]): Board state to be reflected in ui
        """
        self.fields.delete("tile")
        for x in range(self.column_count):
            for y in range(self.column_count):
                if board[x][y] != "":
                    self.create_disk(x, y, board[x][y])
        self.fields.update()

    def mouse_click_handler(self, event):
        """Function handling mouse click

        Args:
            event (event): mouse event
        """
        (x, y) = self.get_field_coordinates_after_mouse_click(event)
        self.controller.handle_user_input(x, y)

    def get_field_coordinates_after_mouse_click(self, event) -> tuple[float, float]:
        """Function translating mouse position to board coordinates

        Args:
            event (event): mouse click event

        Returns:
            tuple[float, float]: mouse click coordinates on board
        """
        col = event.y // self.field_size
        row = event.x // self.field_size
        print(col, row)
        return col, row

    def create_start_disks(self):
        """Creates starting disk"""
        self.create_disk(3, 3, "white")
        self.create_disk(4, 4, "white")
        self.create_disk(4, 3, "black")
        self.create_disk(3, 4, "black")

    def create_disk(self, row: int, column: int, color: str) -> int:
        """Function creating oval (disk) on canvas

        Args:
            row (int): row of board
            column (int): column of board
            color (str): color of disk

        Returns:
            int: id of disk
        """
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

    def set_current_player_label(self, player: str):
        """Sets label telling which player's turn is it

        Args:
            player (str): Current player color
        """
        self.current_player_label.config(text="Player: " + player, foreground=player)

    def end_game_message(self, score: dict):
        """Show popup message after game end

        Args:
            score (dict): dictionary containing score information
        """

        score_text = "Black: " + str(score[0]) + "\nWhite: " + str(score[1])
        if score[0] > score[1]:
            score_text += "\nBlack Won !!!"
        elif score[0] < score[1]:
            score_text = "\nWhite Won !!!"
        else:
            score_text = "\nDRAW"
        messagebox.showinfo("End Game", score_text)

    def pass_window(self, player_passed = False):
        """Show popup message informing user of passing

        Args:
            player (bool): if player or ai passed in ai game
        """
        messagebox.showinfo("Pass window", "Pass")
        if player_passed:
            self.controller.ai_move()

    def leaderboard_window(self) -> tuple:
        #TODO: don't ask for nickname of white if playing vs ai
        #TODO: handle one of the users not wanting to add nickname
        """Ask user for nicknames of players

        Returns:
            tuple: nicknames
        """
        choice = messagebox.askquestion(
            title="LeaderBoard",
            message="BlackPlayer | Do you want to add your score to leaderboard",
            type=messagebox.YESNO,
        )
        if choice == "yes":
            nickname_black = simpledialog.askstring(
                "Nickname", "Enter Nickname: ", parent=self
            )
        else: nickname_black = "null"
        nickname_white = "null"
        if not self.controller.is_game_vs_ai():
            choice = messagebox.askquestion(
                title="LeaderBoard",
                message="WhitePlayer | Do you want to add your score to leaderboard",
                type=messagebox.YESNO,
            )
            if choice == "yes":
                nickname_white = simpledialog.askstring(
                    "Nickname", "Enter Nickname: ", parent=self
                )
        return (nickname_black, nickname_white)


class Menu(tk.Frame):
    """Menu window class

    Args:
        tk (Frame): Extending
    """
    def __init__(self, parent):
        super().__init__(
            parent, borderwidth=15, background="#6e3a00", width=500, height=500
        )
        self.root = parent
        self.controller: Controller
        self.pack(expand=True, fill="both")
        self.label = tk.Label(
            self,
            text="Menu",
            font=("Impact", 25),
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
            font=("Impact", 20),
            pady=5,
            state="disabled",
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
            font=("Impact", 20),
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
            font=("Impact", 20),
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
            font=("Impact", 20),
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
            font=("Impact", 20),
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
            font=("Impact", 20),
            pady=5,
        )
        self.button_leaderboard = tk.Button(
            self,
            text="Leaderboard",
            command=self.root.show_leaderboard,
            bg="#026e00",
            fg="#ffe200",
            activebackground="#015400",
            activeforeground="#ffe200",
            height=2,
            width=20,
            font=("Impact", 20),
            pady=5,
        )
        self.button_continue.pack()
        self.button_new_game.pack()
        self.button_play_vs_ai.pack()
        self.button_save.pack()
        self.button_load.pack()
        self.button_leaderboard.pack()
        self.button_exit.pack()

    def set_controller(self, controller: Controller):
        """Sets controller

        Args:
            controller (Controller): Controller instance
        """
        self.controller = controller

    def save_button_action(self):
        """Action after pressing button_save_game
        """
        self.controller.save_to_file()

    def load_button_action(self):
        """Action after pressing button_load_game
        """
        filepath = filedialog.askopenfilename(
            defaultextension="txt", initialdir="Saves"
        )
        try:
            self.controller.load_form_file(filepath)
            self.button_continue["state"] = "normal"
        except SaveFormatException as e:
            messagebox.showinfo("Error", str(e))
        except JSONDecodeError as e:
            messagebox.showinfo("Error", str(e))
        

    def new_game_button_action(self):
        """Action after pressing new game button
        """
        self.button_continue["state"] = "normal"
        self.controller.new_game()
        self.root.show_game()

    def new_game_vs_ai_button_action(self):
        """action after pressing new game vs ai button
        """
        self.button_continue["state"] = "normal"
        self.controller.new_game_vs_ai()
        self.root.show_game()


class Leaderboard(tk.Frame):
    """Leaderboard window class

    Args:
        tk (Frame): Extends
    """
    def __init__(self, parent):
        super().__init__(
            parent, borderwidth=15, background="#6e3a00", width=500, height=500
        )
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
            font=("Impact", 20),
        )
        self.button_to_main_window.pack()
        self.scroll_bar = Scrollbar(self)
        self.leaderboard = tk.Text(
            self,
            wrap="word",
            background="#6e3a00",
            foreground="#ffe200",
            yscrollcommand=self.scroll_bar.set,
            font=("Impact", 20),
        )
        self.scroll_bar.pack(side="left", fill="y")
        self.leaderboard.pack(side="right", fill="both", expand=True)

    def set_controller(self, controller: Controller):
        """Set controller

        Args:
            controller (Controller): Controller instance
        """
        self.controller = controller

    def populate_leaderboard(self, score:dict):
        """Add score board from controller to leaderboard text field

        Args:
            score (dict): scoreboard
        """
        for key, value in score.items():
            self.leaderboard.insert(tk.END, f"{key}: {value}\n")
