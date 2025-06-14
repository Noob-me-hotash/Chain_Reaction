import screens
from screens import pygame, time, sys, keep_board_populated
from pygame.locals import *
from grid import *
from essentials import *
from heuristics import *

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()

displaysurf = pygame.display.set_mode((1200, 800))
displaysurf.fill(screens.BLACK)
pygame.display.set_caption("CHAIN REACTION")

time.sleep(0.5)

introSoundObj = pygame.mixer.Sound('game_utils/sounds/intro_1.mp3')
introSoundObj.play()


tapSoundObj = pygame.mixer.Sound('game_utils/sounds/click_button.mp3')
swipeSoundObj = pygame.mixer.Sound('game_utils/sounds/swipe_tiles.mp3')
mergeSoundObj = pygame.mixer.Sound('game_utils/sounds/merge_tiles.mp3')


current_screen = screens.start_screen
game_mode = "human_vs_human"


board = Board(9, 6)
current_player = player0
ai_thinking = False

last_ai_move_time = 0  
ai_move_interval = 1000  


def reset_game():
    global board, current_player, global_move_count
    board = Board(9, 6)
    current_player = player0
    global_move_count = 0
    screens.game_over_sound_played = False

def make_ai_move():
    global current_player, ai_thinking
    
    if current_player == player1 and game_mode in ["human_vs_ai", "ai_vs_ai"]:
        ai_thinking = True
        pygame.display.update()
        
        _, best_move = minimax_search(board, 3, True, player1, player0)
        
        if best_move:
            board.make_move(best_move[0], best_move[1], current_player)
            print(f"AI placed orb at ({best_move[0]}, {best_move[1]})")
            current_player = player0 if current_player == player1 else player1
        
        ai_thinking = False



def make_ai_move_auto():
    global current_player, ai_thinking
    
    ai_thinking = True
    pygame.display.update()
    
    if current_player == player1:
        _, best_move = minimax_search(board, 3, False, player1, player0)
    else:
        _, best_move = minimax_search(board, 3, True, player0, player1)
        
    if best_move:
        board.make_move(best_move[0], best_move[1], current_player)
        print(f"{current_player} placed orb at ({best_move[0]}, {best_move[1]})")
        current_player = player0 if current_player == player1 else player1    
    
    ai_thinking = False
    time.sleep(1.5)



while True:
    fpsClock.tick(FPS)
    
    if current_screen == screens.start_screen:
        screens.get_starting_surf()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if 520 < mouse_pos[0] < 680 and 450 < mouse_pos[1] < 490:
                    playGamefontObj = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 24)
                    playGameTextSurfaceObj = playGamefontObj.render('Human vs Human', True, Color(100, 100, 100)) 
                    playgameTextRectObj = playGameTextSurfaceObj.get_rect(center=(600, 470))
                    displaysurf.blit(playGameTextSurfaceObj, playgameTextRectObj)
                if 520 < mouse_pos[0] < 680 and 500 < mouse_pos[1] < 540:
                    playGamefontObj = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 24)
                    playGameTextSurfaceObj = playGamefontObj.render('Human vs AI', True, Color(100, 100, 100)) 
                    playgameTextRectObj = playGameTextSurfaceObj.get_rect(center=(600, 520))
                    displaysurf.blit(playGameTextSurfaceObj, playgameTextRectObj)
                elif 500 < mouse_pos[0] < 700 and 550 < mouse_pos[1] < 590:
                    creditsFontObj = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 24)
                    creditsTextSurf = creditsFontObj.render('AI vs AI', True, Color(100, 100, 100))
                    creditsTextRect = creditsTextSurf.get_rect(center=(600, 570))
                    displaysurf.blit(creditsTextSurf, creditsTextRect)
                elif 560 < mouse_pos[0] < 640 and 600 < mouse_pos[1] < 640:
                    quitTextSurf = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 24).render('Quit', True, Color(100, 100, 100))
                    quitTextRect = quitTextSurf.get_rect(center=(600, 620))
                    displaysurf.blit(quitTextSurf, quitTextRect)
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 520 < mouse_pos[0] < 680 and 450 < mouse_pos[1] < 490:
                    if tapSoundObj:
                        tapSoundObj.play()
                    game_mode = "human_vs_human"
                    reset_game()
                    current_screen = screens.game_screen
                elif 500 < mouse_pos[0] < 700 and 500 < mouse_pos[1] < 540:
                    if tapSoundObj:
                        tapSoundObj.play()
                    game_mode = "human_vs_ai"
                    # player1 = extra_AI_player
                    reset_game()
                    current_screen = screens.game_screen
                elif 500 < mouse_pos[0] < 700 and 550 < mouse_pos[1] < 590:
                    if tapSoundObj:
                        tapSoundObj.play()
                    game_mode = "ai_vs_ai"
                    reset_game()
                    current_screen = screens.ai_vs_ai_game_screen
                elif 560 < mouse_pos[0] < 640 and 600 < mouse_pos[1] < 640:
                    if tapSoundObj:
                        tapSoundObj.play()
                    pygame.quit()
                    sys.exit()
        pygame.display.update()



    elif current_screen == screens.game_screen:
        screens.get_main_game_surf()
        
        curr_color = RED if current_player == player0 else BLUE
        player_text = f"{current_player} move : "
        if ai_thinking:
            player_text = "AI thinking..."
        
        playerMoveSurf = pygame.font.Font('game_utils/font/LuckiestGuy-Regular.ttf', 32).render(player_text, True, curr_color)
        playerMoveRect = playerMoveSurf.get_rect(center=(600, 75))
        displaysurf.blit(playerMoveSurf, playerMoveRect)
        
        mode_text = f"Mode: {game_mode.replace('_', ' ').title()}"
        modeSurf = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 20).render(mode_text, True, WHITE)
        modeRect = modeSurf.get_rect(center=(600, 110))
        displaysurf.blit(modeSurf, modeRect)
        
        keep_board_populated(board)
        
        win_status = is_winning_state(board)
        if win_status[0]:
            winning_player = win_status[1]
            time.sleep(0.25)
            current_screen = screens.game_over_screen

        if not ai_thinking and current_player == player1 and game_mode in ["human_vs_ai", "ai_vs_ai"]:
            make_ai_move()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    current_screen = screens.start_screen
                elif event.key == K_r:
                    reset_game()
            elif event.type == MOUSEBUTTONDOWN and not ai_thinking:
                if (current_player == player0 or (current_player == player1 and game_mode == "human_vs_human")):
                    mouse_pos = pygame.mouse.get_pos()
                    cell_index = get_cell_index(mouse_pos)
                    if cell_index[0] >= 0 and cell_index[1] >= 0:
                        print(f"cell orb count = {board.grid[cell_index[0]][cell_index[1]].orb_count}, cell color = {board.grid[cell_index[0]][cell_index[1]].current_color};")
                        if board.is_valid_move(cell_index[0], cell_index[1], current_player):
                            if tapSoundObj:
                                tapSoundObj.play()
                            
                            board.make_move(cell_index[0], cell_index[1], current_player)
                            print(f"Player {current_player} placed orb at ({cell_index[0]}, {cell_index[1]})")
                            
                            current_player = player1 if current_player == player0 else player0
                        else:
                            print("Invalid move!")
        
        pygame.display.update()


    elif current_screen == screens.ai_vs_ai_game_screen:
        screens.get_ai_vs_ai_game_surf()
        
        curr_color = RED if current_player == player0 else BLUE
        player_text = f"{current_player} move : "
        if ai_thinking:
            player_text = "AI thinking..."

        playerMoveSurf = pygame.font.Font('game_utils/font/LuckiestGuy-Regular.ttf', 32).render(player_text, True, curr_color)
        playerMoveRect = playerMoveSurf.get_rect(center=(600, 75))
        displaysurf.blit(playerMoveSurf, playerMoveRect)
        
        mode_text = f"Mode: {game_mode.replace('_', ' ').title()}"
        modeSurf = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 20).render(mode_text, True, WHITE)
        modeRect = modeSurf.get_rect(center=(600, 110))
        displaysurf.blit(modeSurf, modeRect)

        keep_board_populated(board)

        win_status = is_winning_state(board)
        if win_status[0]:
            winning_player = win_status[1]
            current_screen = screens.game_over_screen

        current_time = pygame.time.get_ticks()
        if not ai_thinking and current_time - last_ai_move_time > ai_move_interval:
            make_ai_move_auto()
            last_ai_move_time = current_time



        # for event in pygame.event.get():
        #     if event.type == QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     elif event.type == KEYDOWN:
        #         if event.key == K_ESCAPE:
        #             current_screen = screens.start_screen
        #         elif event.key == K_r:
        #             reset_game()
        #     elif event.type == MOUSEBUTTONDOWN and not ai_thinking:
        #         if (current_player == player0 or (current_player == player1 and game_mode == "human_vs_human")):
        #             mouse_pos = pygame.mouse.get_pos()
        #             cell_index = get_cell_index(mouse_pos)
        #             if cell_index[0] >= 0 and cell_index[1] >= 0:
        #                 print(f"cell orb count = {board.grid[cell_index[0]][cell_index[1]].orb_count}, cell color = {board.grid[cell_index[0]][cell_index[1]].current_color};")
        #                 if board.is_valid_move(cell_index[0], cell_index[1], current_player):
        #                     if tapSoundObj:
        #                         tapSoundObj.play()
                            
        #                     board.make_move(cell_index[0], cell_index[1], current_player)
        #                     print(f"Player {current_player} placed orb at ({cell_index[0]}, {cell_index[1]})")
                            
        #                     current_player = player1 if current_player == player0 else player0
        #                 else:
        #                     print("Invalid move!")
        
        pygame.display.update()


    elif current_screen == screens.game_over_screen:
        screens.get_game_over_surf()
        winPlayerTextsurf = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 35).render(f"{winning_player} has won!", True, GREEN)
        winPlayerTextRect = winPlayerTextsurf.get_rect(center=(600, 375))
        displaysurf.blit(winPlayerTextsurf, winPlayerTextRect)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    reset_game()
                    current_screen = screens.game_screen
                elif event.key == K_ESCAPE:
                    current_screen = screens.start_screen
            elif event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if 500 < mouse_pos[0] < 540 and 530 < mouse_pos[1] < 570:
                    yesTextSurf = pygame.font.Font('game_utils/font/Arbutus-Regular.ttf', 25).render('Yes', True, Color(100, 100, 100))
                    yesTextRect = yesTextSurf.get_rect(center=(520, 550))
                    displaysurf.blit(yesTextSurf, yesTextRect)
                elif 640 < mouse_pos[0] < 720 and 530 < mouse_pos[1] < 570:
                    noTextSurf = pygame.font.Font('game_utils/font/Arbutus-Regular.ttf', 25).render('No, quit', True, Color(100, 100, 100))
                    noTextRect = noTextSurf.get_rect(center=(680, 550))
                    displaysurf.blit(noTextSurf, noTextRect)
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 500 < mouse_pos[0] < 540 and 530 < mouse_pos[1] < 570:
                    if tapSoundObj:
                        tapSoundObj.play()
                    reset_game()
                    current_screen = screens.game_screen
                elif 640 < mouse_pos[0] < 720 and 530 < mouse_pos[1] < 570:
                    if tapSoundObj:
                        tapSoundObj.play()
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()