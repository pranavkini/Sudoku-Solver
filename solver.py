import tkinter as tk
from tkinter import messagebox
import numpy as np


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    # Check column
    for i in range(len(bo[0])):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = np.zeros((9, 9), dtype=int)
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        for row in range(9):
            for col in range(9):
                padx, pady = 1, 1
                if row % 3 == 0 and row != 0:
                    pady = (4, 1)
                if col % 3 == 0 and col != 0:
                    padx = (4, 1)
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), borderwidth=1, relief='solid',
                                 justify='center')
                entry.grid(row=row, column=col, padx=padx, pady=pady)
                self.entries[row][col] = entry

        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=3, pady=20)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        clear_button.grid(row=9, column=3, columnspan=3, pady=20)

    def get_board(self):
        for row in range(9):
            for col in range(9):
                value = self.entries[row][col].get()
                if value.isdigit():
                    self.board[row][col] = int(value)
                else:
                    self.board[row][col] = 0

    def set_board(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, str(self.board[row][col]))
                else:
                    self.entries[row][col].delete(0, tk.END)

    def solve(self):
        self.get_board()
        if solve(self.board):
            self.set_board()
        else:
            messagebox.showerror("Error", "No solution exists")

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
        self.board = np.zeros((9, 9), dtype=int)


if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()


