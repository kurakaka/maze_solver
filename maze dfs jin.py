import tkinter as tk
import random

# Configuration
WIDTH = 31
HEIGHT = 31
CELL_SIZE = 18 

class MazeDFS:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        
        self.root = tk.Tk()
        self.root.title("DFS Maze Solver")
        self.root.configure(bg="#1e1e1e")
        
        # --- UI Layout ---
        self.button_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.button_frame.pack(pady=10)

        self.dfs_button = tk.Button(
            self.button_frame, text="START SOLVER", command=self.dfs_bot,
            bg="#007ACC", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=10
        )
        self.dfs_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = tk.Button(
            self.button_frame, text="NEW MAZE", command=self.restart_maze,
            bg="#28a745", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=10
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(
            self.root, width=self.width * self.cell_size, height=self.height * self.cell_size,
            bg="black", highlightthickness=0
        )
        self.canvas.pack(pady=10, padx=20)

        self.restart_maze()
        self.root.mainloop()

    def create_maze(self):
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        stack = [(1, 1)]
        maze[1][1] = 0
        while stack:
            x, y = stack[-1]
            random.shuffle(dirs)
            neighbors = [(x+dx, y+dy) for dx, dy in dirs if 0 < x+dx < self.width-1 and 0 < y+dy < self.height-1 and maze[y+dy][x+dx] == 1]
            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[ny - (ny - y) // 2][nx - (nx - x) // 2] = 0
                maze[ny][nx] = 0
                stack.append((nx, ny))
            else: stack.pop()
        maze[1][0] = 0 
        maze[self.height - 2][self.width - 1] = 0 
        return maze

    def draw_maze(self):
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                color = "#ffffff" if self.maze[y][x] == 0 else "#252526"
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline="#333333"
                )
        # Goal markers
        self.canvas.create_rectangle(0, self.cell_size, self.cell_size, 2 * self.cell_size, fill="#4EC9B0") # Start
        self.canvas.create_rectangle((self.width-1)*self.cell_size, (self.height-2)*self.cell_size, 
                                     self.width*self.cell_size, (self.height-1)*self.cell_size, fill="#F44747") # End

    def restart_maze(self):
        self.maze = self.create_maze()
        self.draw_maze()

    def dfs_bot(self):
        self.draw_maze() 
        self.depth_first_search((1, 1), (self.width - 1, self.height - 2))
    def flash_colors(self, count):
        colors = ["#00CBA2", "#DC0000", "#D2D200", "#0077D8", "#CA3900"]
        current_color = colors[count % len(colors)]
        
        # Change the text color using the tag we created
        self.canvas.itemconfig("solved_text", fill=current_color)
        
        # Call itself again after 200ms to create the animation
        self.root.after(200, lambda: self.flash_colors(count + 1))

    def depth_first_search(self, start, end):
        stack = [(start, [start])]
        visited = set()
        move_dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        def step():
            if not stack: return
            current, path = stack.pop()
            
            # If we've already visited this, skip instantly to the next stack item
            if current in visited:
                self.root.after(1, step)
                return
            
            visited.add(current)

            # Draw the current step (Yellow)
            self.canvas.create_rectangle(
                current[0] * self.cell_size, current[1] * self.cell_size,
                (current[0] + 1) * self.cell_size, (current[1] + 1) * self.cell_size,
                fill="#DCDCAA", outline="#D7BA7D"
            )

            if current == end:
                # Create the text and give it a 'tag' so we can find it later
                self.canvas.create_text(
                    (self.width * self.cell_size) // 2, 
                    (self.height * self.cell_size) // 2,
                    text="SOLVED", fill="white", 
                    font=("Helvetica", 30, "bold"), 
                    tags="solved_text"
                )
                # Start the flashing loop
                self.flash_colors(0) 
                return

            # Check neighbors
            valid_neighbors = []
            for dx, dy in move_dirs:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.maze[ny][nx] == 0 and (nx, ny) not in visited:
                        valid_neighbors.append((nx, ny))

            delay = 25 # Default speed
            
            # If it's a junction, color it Blue and pause
            if len(valid_neighbors) > 1:
                delay = 250
                self.canvas.create_rectangle(
                    current[0] * self.cell_size, current[1] * self.cell_size,
                    (current[0] + 1) * self.cell_size, (current[1] + 1) * self.cell_size,
                    fill="#569CD6", outline="#333333"
                )

            for neighbor in valid_neighbors:
                stack.append((neighbor, path + [neighbor]))

            self.root.after(delay, step)

        step()

if __name__ == "__main__":
    app = MazeDFS(WIDTH, HEIGHT, CELL_SIZE)