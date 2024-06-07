"""Main driving module of the application"""
import tkinter as tk
import controller
import board
import view



class App(tk.Tk):
    """Main driving class of the application

    Arguments:
        tk -- extended class
    """
    def __init__(self):
        super().__init__()

        self.title("Riversi Game")
        self.m = board.Board()
        self.v = view.Game(self)
        self.menu = view.Menu(self)
        self.leaderboard = view.Leaderboard(self)
        self.show_menu()
        self.resizable(True, True)
        self.cont = controller.Controller(self.m, self.v, self.menu, self.leaderboard)
        self.v.set_controller(self.cont)
        self.menu.set_controller(self.cont)

    def show_game(self):
        """Function hiding all windows apart from game window"""
        self.menu.pack_forget()
        self.leaderboard.pack_forget()
        self.v.pack(expand=True, fill="both")

    def show_menu(self):
        """Function hiding all windows apart from menu window"""
        self.v.pack_forget()
        self.leaderboard.pack_forget()
        self.menu.pack(expand=True, fill="both")

    def show_leaderboard(self):
        """Function hiding all windows apart from leaderboard window"""
        self.menu.pack_forget()
        self.v.pack_forget()
        self.leaderboard.pack(expand=True, fill="both")


app = App()
app.mainloop()
