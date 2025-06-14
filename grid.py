class Player:
    def __init__(self, player_name, color):
        self.color = color
        self.player_name = player_name
    
    def __str__(self):
        return self.player_name

class Cell:
    def __init__(self, row_index, col_index):
        self.row_index = row_index
        self.col_index = col_index
        self.adjacent_cells = set()
        self.orb_count = 0
        self.current_color = "null"
        self.critical_mass = 0

    def __hash__(self):
        return hash((self.row_index, self.col_index))
    
    def __eq__(self, other: 'Cell'):
        return self.row_index == other.row_index and self.col_index == other.col_index
    
    def __str__(self):
        return f"Cell({self.row_index}, {self.col_index})"
    
    def copy_cell(self):
        new_cell = Cell(self.row_index, self.col_index)
        new_cell.orb_count = self.orb_count
        new_cell.current_color = self.current_color
        new_cell.critical_mass = self.critical_mass
        return new_cell

    def burst(self):
        if self.orb_count >= self.critical_mass and self.orb_count > 0:
            burst_color = self.current_color
            # orbs_to_distribute = self.orb_count
            
            self.orb_count = 0
            self.current_color = "null"
            
            cells_to_burst = []
            for neighbor_cell in self.adjacent_cells:
                neighbor_cell.current_color = burst_color
                neighbor_cell.orb_count += 1
                
                if neighbor_cell.orb_count >= neighbor_cell.critical_mass:
                    cells_to_burst.append(neighbor_cell)
            
            # Handle chain reactions
            for cell in cells_to_burst:
                cell.burst()


    def put_orb(self, orb_color):
        if self.orb_count < self.critical_mass:
            self.orb_count += 1
            self.current_color = orb_color
            
            if self.orb_count >= self.critical_mass:
                self.burst()


class Board:
    def __init__(self, rows, cols, grid=None, move_count=0):
        self.row_count = rows
        self.col_count = cols
        self.move_count = move_count
        
        if grid:
            self.grid = grid
        else:
            self.grid = [[Cell(i, j) for j in range(self.col_count)] for i in range(self.row_count)]
            self.setup_board()


    def setup_board(self):
        for i in range(self.row_count):
            for j in range(self.col_count):
                cell = self.grid[i][j]
                
                if self.is_corner(i, j):
                    cell.critical_mass = 2
                elif self.is_edge(i, j):
                    cell.critical_mass = 3
                else:
                    cell.critical_mass = 4
                
                self.setup_adjacencies(i, j)


    def is_corner(self, i, j):
        return ((i == 0 or i == self.row_count - 1) and (j == 0 or j == self.col_count - 1))


    def is_edge(self, i, j):
        return (i == 0 or i == self.row_count - 1 or j == 0 or j == self.col_count - 1) and not self.is_corner(i, j)


    def setup_adjacencies(self, i, j):
        cell = self.grid[i][j]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.row_count and 0 <= nj < self.col_count:
                cell.adjacent_cells.add(self.grid[ni][nj])

    def __str__(self):
        board_string = ""
        for i in range(self.row_count):
            row_string = ""
            for j in range(self.col_count):
                curr_cell = self.grid[i][j]
                if curr_cell.current_color == "null":
                    row_string += "0\t"
                elif curr_cell.current_color == "red":
                    row_string += str(curr_cell.orb_count) + "R\t"
                elif curr_cell.current_color == "blue":
                    row_string += str(curr_cell.orb_count) + "B\t"
            board_string += row_string + "\n"
        return board_string


    def make_copy(self):
        new_board = Board(self.row_count, self.col_count)
        new_board.move_count = self.move_count
        
        for i in range(self.row_count):
            for j in range(self.col_count):
                old_cell = self.grid[i][j]
                new_cell = new_board.grid[i][j]
                new_cell.orb_count = old_cell.orb_count
                new_cell.current_color = old_cell.current_color
                new_cell.critical_mass = old_cell.critical_mass
        
        return new_board


    def is_valid_move(self, row, col, player):
        if not (0 <= row < self.row_count and 0 <= col < self.col_count):
            return False
        
        cell = self.grid[row][col]
        return (cell.current_color == "null" or (cell.current_color == player.color and cell.orb_count < cell.critical_mass))


    def make_move(self, row, col, player):
        if self.is_valid_move(row, col, player):
            self.grid[row][col].put_orb(player.color)
            self.move_count += 1
            return True
        return False