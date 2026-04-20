import tkinter as tk
import math

class TicTacToe:
    def __init__(self, root):
        self.root = root
        root.title("Tic Tac Toe")
        root.geometry("400x400")  # Initial size to make boxes roughly square
        root.minsize(300, 300)    # Minimum size
        self.current = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.mode = None  # No mode selected initially

        self.font = ("Arial", 20)  # Initial font size
        self.status = tk.Label(root, text="Choose mode", font=self.font)
        self.status.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        # Configure grid weights for dynamic scaling
        root.rowconfigure(0, weight=0)
        for i in range(1, 4):
            root.rowconfigure(i, weight=1)
        root.rowconfigure(4, weight=0)
        root.rowconfigure(5, weight=0)  # For choice buttons
        for j in range(3):
            root.columnconfigure(j, weight=1)

        for r in range(3):
            for c in range(3):
                button = tk.Button(
                    root,
                    text="",
                    font=self.font,
                    command=lambda r=r, c=c: self.click(r, c),
                )
                button.grid(row=r + 1, column=c, padx=5, pady=5, sticky="nsew")
                self.buttons[r][c] = button

        restart_button = tk.Button(root, text="Restart", command=self.reset)
        restart_button.grid(row=4, column=0, columnspan=3, sticky="we", pady=(5, 10))

        # Choice buttons
        self.ai_button = tk.Button(root, text="Play vs AI", command=self.set_ai)
        self.human_button = tk.Button(root, text="Play vs Human", command=self.set_human)

        # Bind resize event
        root.bind('<Configure>', self.on_resize)

        # Initially disable board and show choice
        self.disable_all()
        self.show_choice()

    def on_resize(self, event):
        if event.widget == self.root:
            height = event.height
            font_size = max(10, height // 20)  # Scale font with window height
            self.font = ("Arial", font_size)
            self.status.config(font=self.font)
            for row in self.buttons:
                for button in row:
                    button.config(font=self.font)

    def click(self, row, col):
        if self.check_winner():
            return

        if self.board[row][col]:
            self.status.config(text=f"Illegal move. Turn: {self.current}")
            return

        self.board[row][col] = self.current
        self.buttons[row][col].config(text=self.current, state="disabled")

        winner = self.check_winner()
        if winner:
            self.status.config(text=f"{winner} wins!")
            self.disable_all()
        elif all(self.board[r][c] for r in range(3) for c in range(3)):
            self.status.config(text="Draw")
        else:
            self.current = "O" if self.current == "X" else "X"
            self.status.config(text=f"Turn: {self.current}")
            if self.current == "O" and self.mode == "AI":
                self.ai_move()

    def ai_move(self):
        move = self.get_best_move(self.board)
        if move:
            self.click(move[0], move[1])

    def get_best_move(self, board):
        best_score = -math.inf
        best_move = None
        for move in self.get_available_moves(board):
            board[move[0]][move[1]] = "O"
            score = self.minimax(board, "X")
            board[move[0]][move[1]] = ""
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, board, player):
        winner = self.check_winner()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif not self.get_available_moves(board):
            return 0

        if player == "O":
            max_eval = -math.inf
            for move in self.get_available_moves(board):
                board[move[0]][move[1]] = "O"
                eval = self.minimax(board, "X")
                board[move[0]][move[1]] = ""
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_available_moves(board):
                board[move[0]][move[1]] = "X"
                eval = self.minimax(board, "O")
                board[move[0]][move[1]] = ""
                min_eval = min(min_eval, eval)
            return min_eval

    def get_available_moves(self, board):
        return [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]

    def check_winner(self):
        lines = []
        lines.extend(self.board)
        lines.extend([[self.board[r][c] for r in range(3)] for c in range(3)])
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] and line[0] == line[1] == line[2]:
                return line[0]
        return None

    def disable_all(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")

    def enable_all(self):
        for row in self.buttons:
            for button in row:
                button.config(state="normal")

    def reset(self):
        self.current = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.mode = None
        self.status.config(text="Choose mode")
        for row in self.buttons:
            for button in row:
                button.config(text="", state="disabled")
        self.show_choice()

    def show_choice(self):
        self.ai_button.grid(row=5, column=0, columnspan=1, sticky="we", pady=(5, 10))
        self.human_button.grid(row=5, column=1, columnspan=2, sticky="we", pady=(5, 10))

    def hide_choice(self):
        self.ai_button.grid_forget()
        self.human_button.grid_forget()

    def set_ai(self):
        self.mode = "AI"
        self.status.config(text="Turn: X")
        self.enable_all()
        self.hide_choice()

    def set_human(self):
        self.mode = "Human"
        self.status.config(text="Turn: X")
        self.enable_all()
        self.hide_choice()

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()
