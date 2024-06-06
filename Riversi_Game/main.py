import controller
import board
import view
import tkinter as tk



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.wm_geometry("600x600")
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
        self.menu.pack_forget()
        self.leaderboard.pack_forget()
        self.v.pack(expand=True, fill="both")

    def show_menu(self):
        self.v.pack_forget()
        self.leaderboard.pack_forget()
        self.menu.pack(expand=True, fill="both")

    def show_leaderboard(self):
        self.menu.pack_forget()
        self.v.pack_forget()
        self.leaderboard.pack(expand=True, fill="both")


app = App()
app.mainloop()
