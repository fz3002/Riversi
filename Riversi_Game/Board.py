import tkinter as tk

BOARD_SIZE = 400

WIDTH = 8
FIELD_SIZE = BOARD_SIZE/WIDTH

DISK_SIZE = int(0.8 * FIELD_SIZE)
BORDER_SIZE = 5

root = tk.Tk()

root.title("Checkers")
root.geometry(f'{BOARD_SIZE}x{BOARD_SIZE}+100+100')
root.resizable(0,0)

board = tk.Frame(root)
board.pack()

draughts = tk.Canvas(board, width = BOARD_SIZE, height = BOARD_SIZE, borderwidth=15, background='#6e3a00')
draughts.pack(fill = 'both')


for row in range(WIDTH + 1):
    for column in range(WIDTH + 1):
        
        draught = draughts.create_rectangle(row*FIELD_SIZE,column*FIELD_SIZE,\
                                            (row*FIELD_SIZE)+FIELD_SIZE,(column*FIELD_SIZE)+FIELD_SIZE,\
                                            fill = '#026e00', outline = 'black')


# TODO: click handler


root.mainloop()
