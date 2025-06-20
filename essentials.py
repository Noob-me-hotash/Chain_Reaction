from colorama import Fore, Style, init
import pygame
from pygame.locals import *
from grid import Cell, Player, Board
init()


##########################################  Constants  ##########################################

global_move_count = 0
ai_thinking = False

last_ai_move_time = 0  
ai_move_interval = 800  

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(210, 40, 30)
GREEN = pygame.Color(50, 205, 100)
BLUE = pygame.Color(30, 60, 250) 
YELLOW = pygame.Color(255, 255, 0)
GRAY = pygame.Color(128, 128, 128)

grid_x = 150
grid_y = 150
grid_width = 900
grid_height = 600

cell_width = grid_width / 6    
cell_height = grid_height / 9

displaysurf = pygame.display.set_mode((1200, 800))
displaysurf.fill(BLACK)

player0 = Player("Human", "red")
player1 = Player("AI", "blue")

current_player = player0
winning_player = None

###################################################################################################################
##########################################  Functions  ##########################################

def draw_board(row, column):
    # Draw horizontal lines
    for i in range(row + 1):  
        y = grid_y + i * cell_height
        pygame.draw.line(displaysurf, GREEN, (grid_x, y), (grid_x + grid_width, y), width=3)

    # Draw vertical lines
    for i in range(column + 1):  
        x = grid_x + i * cell_width
        pygame.draw.line(displaysurf, GREEN, (x, grid_y), (x, grid_y + grid_height), width=3)


def get_cell_index(mouse_pos):
    if not(grid_x <= mouse_pos[0] <= grid_x + grid_width) or not(grid_y <= mouse_pos[1] <= grid_y + grid_height):
        return (-1, -1) 

    cell_x = int((mouse_pos[0] - grid_x) // cell_width)
    cell_y = int((mouse_pos[1] - grid_y) // cell_height)

    return (cell_y, cell_x)  


def get_orb_image(orb_color):
    if orb_color == "red":
        return "game_utils/images/red_ball.png"
    elif orb_color == "blue":
        return "game_utils/images/blue_ball.png"
    return ""


def read_state(filename):
    grid = []
    try:
        with open(filename, "r") as file:
            first_line = file.readline().strip() 
            for i in range(9):
                line = file.readline().strip()
                row = line.split()
                cell_row = []
                for j in range(6):
                    cell = Cell(i, j)
                    color = "null"
                    if row[j][0] == "0":
                        orb_count = 0
                    else:
                        orb_count = int(row[j][0])
                        if row[j][1] == 'R':
                            color = "red"
                        else:
                            color = "blue"
                    cell.orb_count = orb_count
                    cell.current_color = color
                    cell_row.append(cell)
                grid.append(cell_row)
        

        for i in range(9):
            for j in range(6):
                cell = grid[i][j]
                cell.adjacent_cells = set()
                for (di, dj) in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < 9 and 0 <= nj < 6:
                        cell.adjacent_cells.add(grid[ni][nj])
        # print("Reading complete!")
        return Board(9, 6, grid, global_move_count)
    except FileNotFoundError:
        print(f"File {filename} not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def write_state(filename, player: 'Player', state):
    try:
        with open(filename, "w") as file:
            file.write(str(player) + f" Move : \n")
            file.write(str(state))
        # print("Writing complete!")
    except Exception as e:
        print(f"Error writing file: {e}")

###################################################################################################################