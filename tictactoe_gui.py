import tkinter as tk
from tkinter import messagebox
import math

# Global constants
HUMAN = 'X'
AI = 'O'
EMPTY = ' '

# Initialize board
board = [EMPTY] * 9

# Create main window
root = tk.Tk()
root.title("Tic Tac Toe - Minimax AI")

buttons = []

def is_winner(brd, player):
    win_combos = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # cols
        [0,4,8], [2,4,6]            # diags
    ]
    return any(all(brd[i] == player for i in combo) for combo in win_combos)

def is_board_full(brd):
    return all(cell != EMPTY for cell in brd)

def get_available_moves(brd):
    return [i for i in range(9) if brd[i] == EMPTY]

def minimax(brd, depth, is_maximizing):
    if is_winner(brd, AI):
        return 1
    elif is_winner(brd, HUMAN):
        return -1
    elif is_board_full(brd):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(brd):
            brd[move] = AI
            score = minimax(brd, depth + 1, False)
            brd[move] = EMPTY
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(brd):
            brd[move] = HUMAN
            score = minimax(brd, depth + 1, True)
            brd[move] = EMPTY
            best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -math.inf
    move = None
    for i in get_available_moves(board):
        board[i] = AI
        score = minimax(board, 0, False)
        board[i] = EMPTY
        if score > best_score:
            best_score = score
            move = i
    return move

def make_move(index, player):
    board[index] = player
    buttons[index].config(text=player, state="disabled")

def check_game_status():
    if is_winner(board, HUMAN):
        messagebox.showinfo("Game Over", "Congratulations! You win! 🎉")
        reset_board()
    elif is_winner(board, AI):
        messagebox.showinfo("Game Over", "AI wins! Better luck next time. 🤖")
        reset_board()
    elif is_board_full(board):
        messagebox.showinfo("Game Over", "It's a tie!")
        reset_board()

def player_click(index):
    if board[index] == EMPTY:
        make_move(index, HUMAN)
        check_game_status()
        if not is_board_full(board) and not is_winner(board, HUMAN):
            ai = ai_move()
            make_move(ai, AI)
            check_game_status()

def reset_board():
    global board
    board = [EMPTY] * 9
    for i in range(9):
        buttons[i].config(text=" ", state="normal")

# Create 3x3 buttons
for i in range(9):
    button = tk.Button(root, text=" ", font=('Arial', 40), width=5, height=2,
                       command=lambda i=i: player_click(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

# Start GUI loop
root.mainloop()