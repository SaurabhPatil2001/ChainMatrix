import tkinter as tk
import random

# ================= BACKEND =================

const_row, const_col = 6, 5
merge = [[0]*const_col for _ in range(const_row)]
display = [[0]*const_col for _ in range(const_row)]

def get_neighbours(r, c):
    n = []
    if r > 0: n.append((r-1, c))
    if r < const_row-1: n.append((r+1, c))
    if c > 0: n.append((r, c-1))
    if c < const_col-1: n.append((r, c+1))
    return n

def condition(player):
    count = 0
    for i in range(const_row):
        for j in range(const_col):
            if display[i][j] == player:
                return True
            if display[i][j] != 0:
                count += 1
    return count <= 2

def check_reaction(r, c):
    is_edge = r in (0, const_row-1) or c in (0, const_col-1)
    is_corner = (r, c) in [(0,0),(0,const_col-1),(const_row-1,0),(const_row-1,const_col-1)]
    limit = 2 if is_corner else 3 if is_edge else 4
    if merge[r][c] >= limit:
        merge[r][c] = 0
        display[r][c] = 0
        return get_neighbours(r, c)
    return []

def update_merge(r, c, player):
    merge[r][c] += 1
    display[r][c] = player

    if not condition(1): return 2
    if not condition(-1): return 1

    for nr, nc in check_reaction(r, c):
        res = update_merge(nr, nc, player)
        if res: return res

    return 0

# ================= GUI =================

current_player = 1

class ChainReactionGUI:
    def __init__(self, root):
        self.root = root
        root.title("ChainMatrix")

        title = tk.Label(root, text="ChainMatrix", font=("Arial", 24, "bold"))
        title.pack(pady=(10, 5)) 

        self.cells = [[None]*const_col for _ in range(const_row)]

        self.status = tk.Label(root, text="Player 1 (Red)", font=("Arial", 12))
        self.status.pack()

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        for i in range(const_row):
            for j in range(const_col):
                c = tk.Canvas(frame, width=60, height=60, bg="white", highlightthickness=1, highlightbackground="black")
                c.grid(row=i, column=j, padx=2, pady=2)
                c.bind("<Button-1>", lambda e, r=i, c=j: self.on_click(r, c))
                self.cells[i][j] = c

        self.animate()

    def draw_cell(self, canvas, owner, count):
        canvas.delete("all")
        if count == 0:
            return

        color = "red" if owner == 1 else "green"
        vib = min(count*2, 10)

        for _ in range(count):
            x = 30 + random.randint(-vib, vib)
            y = 30 + random.randint(-vib, vib)
            r = 6
            canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="")

    def refresh(self):
        for i in range(const_row):
            for j in range(const_col):
                self.draw_cell(self.cells[i][j], display[i][j], merge[i][j])

    def animate(self):
        self.refresh()
        self.root.after(120, self.animate)

    def on_click(self, r, c):
        global current_player

        if display[r][c] not in (0, current_player):
            return

        res = update_merge(r, c, current_player)
        self.refresh()

        if res:
            self.show_winner(f"Player {'1 (Red)' if res==1 else '2 (Green)'} wins!")
            return

        current_player *= -1
        self.status.config(text=f"Player {'1 (Red)' if current_player==1 else '2 (Green)'}")

    def show_winner(self, msg):
        win = tk.Toplevel(self.root)
        win.title("Game Over")
        tk.Label(win, text=msg, font=("Arial", 14)).pack(padx=20, pady=20)
        tk.Button(win, text="Exit", command=self.root.destroy).pack(pady=10)

# ================= RUN =================

if __name__ == "__main__":
    root = tk.Tk()
    ChainReactionGUI(root)
    root.mainloop()
