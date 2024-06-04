import controller
import board
import view
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title = "Riversi Game"

        m = board.Board()
        v = view.View(self)
        self.geometry(f"{400+30}x{400+30}+100+100")
        self.resizable(0, 0)
        cont = controller.Controller(m, v)
        v.set_controller(cont)


app = App()
app.mainloop()
