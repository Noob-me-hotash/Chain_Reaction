import pygame, sys, time
from pygame.locals import *
from essentials import *
from grid import *

FPS = 100
fpsClock = pygame.time.Clock()

start_screen = 'start'
game_screen = 'game'
credits_screen = 'credits'
game_over_screen = 'game_over'
restart_screen = 'restart'
quit_to_menu_screen = 'quit_to_menu'
win_screen = 'win'
ai_vs_ai_game_screen = "ai_vs_ai"

displaysurf = pygame.display.set_mode((1200, 800))
displaysurf.fill(BLACK)

game_over_sound_played = False

time.sleep(0.2)

print("Hello!")

def keep_board_populated(board: 'Board'):
    for i in range(board.row_count):
        for j in range(board.col_count):
            cell_midpoint = (grid_x + cell_width*j + cell_width//2, grid_y + cell_height*i + cell_height//2)
            blit_x = int(cell_midpoint[0] - 30)
            blit_y = int(cell_midpoint[1] - 30)
            curr_cell = board.grid[i][j]
            orb_count = curr_cell.orb_count
            
            if curr_cell.current_color != "null" and orb_count > 0: 
                orb_image = get_orb_image(curr_cell.current_color)
                orb_image_surf = pygame.image.load(orb_image)
                orb_image_surf = pygame.transform.scale(orb_image_surf, (60, 60))
                    
                if orb_count == 1:
                    displaysurf.blit(orb_image_surf, (blit_x, blit_y))
                elif orb_count == 2:
                    displaysurf.blit(orb_image_surf, (blit_x - 15, blit_y))
                    displaysurf.blit(orb_image_surf, (blit_x + 15, blit_y))
                elif orb_count == 3:
                    displaysurf.blit(orb_image_surf, (blit_x - 15, blit_y + 15))
                    displaysurf.blit(orb_image_surf, (blit_x + 15, blit_y + 15))
                    displaysurf.blit(orb_image_surf, (blit_x, blit_y - 15))
                elif orb_count >= 4:
                    displaysurf.blit(orb_image_surf, (blit_x - 15, blit_y - 15))
                    displaysurf.blit(orb_image_surf, (blit_x + 15, blit_y - 15))
                    displaysurf.blit(orb_image_surf, (blit_x - 15, blit_y + 15))
                    displaysurf.blit(orb_image_surf, (blit_x + 15, blit_y + 15))
                        
                    if orb_count > 4:
                        count_surf = pygame.font.Font(None, 24).render(str(orb_count), True, WHITE)
                        count_rect = count_surf.get_rect(center=(blit_x + 30, blit_y + 30))
                        displaysurf.blit(count_surf, count_rect)
                            
                        


def get_starting_surf():
    displaysurf.fill(BLACK)
    
    titleFont = pygame.font.Font('game_utils/font/LuckiestGuy-Regular.ttf', 48)
    titleSurf = titleFont.render('CHAIN REACTION', True, GREEN) 
    titleRect = titleSurf.get_rect(center=(600, 100))
    displaysurf.blit(titleSurf, titleRect)

    menuFont = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 24)
    
    playGameSurf = menuFont.render('Human vs Human', True, BLACK) 
    playGameRect = playGameSurf.get_rect(center=(600, 470))
    pygame.draw.rect(displaysurf, YELLOW, playGameRect.inflate(20, 10))
    displaysurf.blit(playGameSurf, playGameRect)
    
    humanAIGameSurf = menuFont.render('Human vs AI', True, BLACK)
    humanAIGameRect = humanAIGameSurf.get_rect(center=(600, 520))
    pygame.draw.rect(displaysurf, YELLOW, humanAIGameRect.inflate(20, 10))
    displaysurf.blit(humanAIGameSurf, humanAIGameRect)

    aiGameSurf = menuFont.render('AI vs AI', True, BLACK)
    aiGameRect = aiGameSurf.get_rect(center=(600, 570))
    pygame.draw.rect(displaysurf, YELLOW, aiGameRect.inflate(20, 10))
    displaysurf.blit(aiGameSurf, aiGameRect)

    quitSurf = menuFont.render('Quit', True, BLACK)
    quitRect = quitSurf.get_rect(center=(600, 620))
    pygame.draw.rect(displaysurf, YELLOW, quitRect.inflate(20, 10))
    displaysurf.blit(quitSurf, quitRect)

   

def get_main_game_surf():
    displaysurf.fill(BLACK)
    pygame.draw.rect(displaysurf, BLACK, Rect(0, 0, 1200, 800))

    draw_board(9, 6)
    
    for i in range(9):
        for j in range(6):
            cell_center = (int(grid_x + cell_width*j + cell_width//2), int(grid_y + cell_height*i + cell_height//2))
            
            if ((i == 0 or i == 8) and (j == 0 or j == 5)):
                critical_mass = 2
            elif (i == 0 or i == 8 or j == 0 or j == 5):
                critical_mass = 3
            else:
                critical_mass = 4
            
            try:
                font = pygame.font.Font(None, 16)
                mass_surf = font.render(str(critical_mass), True, GRAY)
                mass_rect = mass_surf.get_rect()
                mass_rect.topleft = (cell_center[0] - 60, cell_center[1] - 40)
                displaysurf.blit(mass_surf, mass_rect)
            except:
                pass

    return displaysurf


def get_ai_vs_ai_game_surf():
    displaysurf.fill(BLACK)
    pygame.draw.rect(displaysurf, BLACK, Rect(0, 0, 1200, 800))
    
    draw_board(9, 6)
    
    for i in range(9):
        for j in range(6):
            cell_center = (int(grid_x + cell_width*j + cell_width//2), int(grid_y + cell_height*i + cell_height//2))
            
            if ((i == 0 or i == 8) and (j == 0 or j == 5)):
                critical_mass = 2
            elif (i == 0 or i == 8 or j == 0 or j == 5):
                critical_mass = 3
            else:
                critical_mass = 4
            
            try:
                font = pygame.font.Font(None, 16)
                mass_surf = font.render(str(critical_mass), True, GRAY)
                mass_rect = mass_surf.get_rect()
                mass_rect.topleft = (cell_center[0] - 60, cell_center[1] - 40)
                displaysurf.blit(mass_surf, mass_rect)
            except:
                pass

    return displaysurf


def get_game_over_surf():
    global game_over_sound_played

    pygame.draw.rect(displaysurf, GRAY, Rect(300, 200, 600, 400))
    
    if not game_over_sound_played:
        gameOverSoundObj = pygame.mixer.Sound('game_utils/sounds/game_over.mp3')
        gameOverSoundObj.play()  
        game_over_sound_played = True

    gameOverFont = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 50)    
    gameOverSurf = gameOverFont.render('Game Over!', True, BLACK)
    gameOverRect = gameOverSurf.get_rect(center=(600, 300))
    displaysurf.blit(gameOverSurf, gameOverRect)

    
    playAgainFont = pygame.font.Font('game_utils/font/Fresh Salmon.otf', 25)
    playAgainSurf = playAgainFont.render('Want to play again?', True, BLACK)
    playAgainRect = playAgainSurf.get_rect(center=(600, 450))
    displaysurf.blit(playAgainSurf, playAgainRect)

    
    buttonFont = pygame.font.Font('game_utils/font/Arbutus-Regular.ttf', 25)
    yesSurf = buttonFont.render('Yes', True, BLACK)
    yesRect = yesSurf.get_rect(center=(520, 550))
    noSurf = buttonFont.render('No, quit', True, BLACK)
    noRect = noSurf.get_rect(center=(680, 550))
    
    pygame.draw.rect(displaysurf, YELLOW, yesRect.inflate(20, 10))
    pygame.draw.rect(displaysurf, YELLOW, noRect.inflate(20, 10))
    displaysurf.blit(yesSurf, yesRect)
    displaysurf.blit(noSurf, noRect)