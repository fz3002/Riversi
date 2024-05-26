import tkinter as tk

board = [[None]*10 for _ in range(10)]

counter = 0

root = tk.Tk()

root.title("Reversi")
root.geometry('100x100')

# TODO: click handler

for i, row in enumerate(board):
    for j, column in enumerate(row):
        L = tk.Label(root, text='    ', bg='green', width=int(100/len(board)), height=int(100/len(board)), borderwidth=1, relief="solid")
        L.grid(row=i, column=j)

root.mainloop()
