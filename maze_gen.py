from mazelib import Maze
from mazelib.generate.Kruskal import Kruskal
import matplotlib.pyplot as plt

def show_maze(grid):
    """Generates an image of the maze"""
    start_place = (1,1)
    end_place = (41,41)
    plt.figure(figsize=(10,10))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')

    ax = plt.gca()
    ax.add_patch(plt.Rectangle((start_place[1]-0.5, start_place[0]-0.5), 1, 1,
                                color='green', alpha=1.0, linewidth=0.1))
    ax.add_patch(plt.Rectangle((end_place[1]-0.5, end_place[0]-0.5), 1, 1,
                                color='red', alpha=1.0, linewidth=0.1))

    plt.xticks([]), plt.yticks([])
    plt.savefig('maze.png', dpi=600)
    plt.show()

def generate_maze(randomizer:int):
    """Generating a Kruskal Maze"""
    m = Maze(randomizer)
    m.generator = Kruskal(21,21)
    m.start = (1,1)
    m.end = (41,41)
    m.generate()

    return m


def create_maze_file(m):
    """Outputs the generated maze to a text file"""
    with open("maze_output.txt", "w") as f:
        print(m, file=f)
        f.close()
    return "maze_output.txt"


def get_maze_grid(file_location):
    """Gets the row and columns of the maze"""
    grid = []
    with open(file_location, 'r') as file:
        for line in file:
            line = line.rstrip()
            row = []
            for char in line:
                if char == " ":
                    row.append(0)
                else:
                    row.append(1)
            grid.append(row)
    return grid

if __name__ == '__main__':
    m = generate_maze(randomizer=123)
    maze_file = create_maze_file(m)
    grid = get_maze_grid(maze_file)
    maze_output = show_maze(grid)

