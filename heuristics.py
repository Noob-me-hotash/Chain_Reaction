from grid import *
from essentials import *

def get_orb_counts(state: 'Board'):
    red_count = 0
    blue_count = 0
    for i in range(state.row_count):
        for j in range(state.col_count):
            curr_cell = state.grid[i][j]
            if curr_cell.current_color == "red":
                red_count += curr_cell.orb_count
            elif curr_cell.current_color == "blue":
                blue_count += curr_cell.orb_count
    return red_count, blue_count


def get_cell_counts(state: 'Board'):
    red_cells = 0
    blue_cells = 0
    for i in range(state.row_count):
        for j in range(state.col_count):
            curr_cell = state.grid[i][j]
            if curr_cell.current_color == "red":
                red_cells += 1
            elif curr_cell.current_color == "blue":
                blue_cells += 1
    return red_cells, blue_cells


def orb_diff_heuristic(state: 'Board'):
    red_count, blue_count = get_orb_counts(state)
    return (red_count - blue_count) if current_player.color == "red" else (blue_count - red_count)


def territory_heuristic(state: 'Board'):
    red_cells, blue_cells = get_cell_counts(state)
    return (red_cells - blue_cells) if current_player.color == "red" else (blue_cells - red_cells)


def mobility_heuristic(state: 'Board'):
    red_mobility = 0
    blue_mobility = 0
    
    for i in range(state.row_count):
        for j in range(state.col_count):
            curr_cell = state.grid[i][j]
            if curr_cell.current_color == "red":
                red_mobility += curr_cell.critical_mass - curr_cell.orb_count
            elif curr_cell.current_color == "blue":
                blue_mobility += curr_cell.critical_mass - curr_cell.orb_count
            else:
                red_mobility += 1
                blue_mobility += 1
    
    return (red_mobility - blue_mobility) if current_player.color == "red" else (blue_mobility - red_mobility) 



def critical_mass_proximity_heuristic(state: 'Board'):
    critical_asset_red = 0
    critical_asset_blue = 0

    for i in range(state.row_count):
        for j in range(state.col_count):
            curr_cell = state.grid[i][j]
            if curr_cell.orb_count == curr_cell.critical_mass - 1:
                if curr_cell.current_color == "red":
                    critical_asset_red += 1
                elif curr_cell.current_color == "blue":
                    critical_asset_blue += 1
    
    return (critical_asset_red - critical_asset_blue) if current_player.color == "red" else (critical_asset_blue - critical_asset_red)


def combined_heuristic(state: 'Board'):
    piece_score = orb_diff_heuristic(state)
    territory_score = territory_heuristic(state)
    mobility_score = mobility_heuristic(state)
    critical_prox_score = critical_mass_proximity_heuristic(state)
    
    total_score = (piece_score * 0.2 + territory_score * 0.3 + mobility_score * 0.2 + critical_prox_score * 0.3)
    
    return total_score if current_player.color == "red" else -total_score


def is_winning_state(board: 'Board'):
    if board.move_count <= 2:
        return False, None
    
    red_count, blue_count = get_orb_counts(board)
    
    if red_count == 0 and blue_count > 0:
        return True, player1
    elif blue_count == 0 and red_count > 0:
        return True, player0
    
    return False, None


def get_possible_moves(player: 'Player', state: 'Board'):
    moves = []
    for i in range(state.row_count):
        for j in range(state.col_count):
            if state.is_valid_move(i, j, player):
                moves.append((i, j))
    return moves


def minimax_search(state: 'Board', heuristic, depth_limit, is_maximizing: bool, max_player: 'Player', min_player: 'Player', alpha=float('-inf'), beta=float('inf')):
    win_happened, won_player = is_winning_state(state)
    if win_happened:
        if won_player == max_player:
            return 1000 + depth_limit, None  
        else:
            return -1000 - depth_limit, None  
    
    if depth_limit == 0:
        return heuristic(state), None
    
    current_player = max_player if is_maximizing else min_player
    possible_moves = get_possible_moves(current_player, state)
    
    if not possible_moves:
        return heuristic(state), None
    
    best_move = possible_moves[0]
    
    if is_maximizing:
        max_eval = float('-inf')
        for move in possible_moves:
            next_state = state.make_copy()
            next_state.make_move(move[0], move[1], current_player)
            
            eval_score, _ = minimax_search(next_state, heuristic, depth_limit - 1, False, max_player, min_player, alpha, beta)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  
        
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        for move in possible_moves:
            next_state = state.make_copy()
            next_state.make_move(move[0], move[1], current_player)
            
            eval_score, _ = minimax_search(next_state, heuristic, depth_limit - 1, True, max_player, min_player, alpha, beta)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            
            beta = min(beta, eval_score)
            if beta <= alpha:
                break 
        
        return min_eval, best_move
    

# test_state = read_state("gamestate.txt")
# print(test_state)
# print(f"Orb diff heuristic value = {orb_diff_heuristic(test_state)}\n")
# print(f"Mobility heuristic value = {mobility_heuristic(test_state)}\n")
# print(f"Territory heuristic value = {territory_heuristic(test_state)}\n")
# print(f"Piece diff heuristic value = {piece_diff_heuristic(test_state)}\n")
# print(f"Piece diff heuristic value = {piece_diff_heuristic(test_state)}\n")