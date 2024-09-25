import pygame
import tensorflow as tf
from tensorflow import keras
import numpy as np

pygame.font.init()

WIDTH, HEIGHT, GRID_WIDTH = 560, 560, 20
NUMBER_OF_ROWS = int(HEIGHT//GRID_WIDTH)
NUMBER_OF_COLS = int(WIDTH//GRID_WIDTH)

BOTTOM_RECT_HEIGHT = 200
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
BUTTON_POS_X, BUTTON_POS_Y = WIDTH * 0.1, HEIGHT + BOTTOM_RECT_HEIGHT/2 - BUTTON_HEIGHT/2 - 50
BUTTON_FONT = pygame.font.SysFont('Arial', 40)
WIN = pygame.display.set_mode((WIDTH, HEIGHT + BOTTOM_RECT_HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)

def clear_button(grid):
    rect = pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y + 70), (BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(WIN, WHITE, rect)
    draw_text = BUTTON_FONT.render("Clear", 1, BLACK)
    WIN.blit(draw_text, (BUTTON_POS_X, BUTTON_POS_Y + 70))
    if pygame.mouse.get_pressed()[0]:
        position = pygame.mouse.get_pos()
        if rect.collidepoint(position):
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    grid[row][col] = 0
                    draw_background()


    pygame.display.update()
    pass

def draw_background():
    WIN.fill(BLACK)
    out_of_canvas = pygame.Rect((0,HEIGHT), (WIDTH, BOTTOM_RECT_HEIGHT))
    pygame.draw.rect(WIN, YELLOW, out_of_canvas)


def predict(grid):
    number_list = [0,1,2,3,4,5,6,7,8,9]
    grid = np.array([grid])
    model = keras.models.load_model('num_reader.keras')
    prediction = model.predict(grid)
    number = number_list[np.argmax(prediction)]
    return number

def button(grid):
    draw_text = BUTTON_FONT.render("Guess Number", 1, BLACK)
    button = pygame.Rect(BUTTON_POS_X, BUTTON_POS_Y, draw_text.get_width(), BUTTON_HEIGHT)
    pygame.draw.rect(WIN, WHITE, button)
    WIN.blit(draw_text, (BUTTON_POS_X, BUTTON_POS_Y))

    if pygame.mouse.get_pressed()[0]:
        position = pygame.mouse.get_pos()
        if button.collidepoint(position):
            number = predict(grid)
            draw_number = BUTTON_FONT.render(str(number), 1, BLACK)
            WIN.blit(draw_number, (WIDTH * 0.7, BUTTON_POS_Y))



    pygame.display.update()



def create_grid():
    #create grid and draws rectangles
    grid = []
    for rows in range(NUMBER_OF_ROWS):
        row = []
        for cols in range(NUMBER_OF_COLS):
            row.append(0)
        grid.append(row)

    return grid

def draw(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            rect = pygame.Rect((col*GRID_WIDTH, row*GRID_WIDTH), (GRID_WIDTH, GRID_WIDTH))
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                if rect.collidepoint(position):
                    if grid[row][col] == 0:
                        grid[row][col] = 1
                        pygame.draw.rect(WIN, WHITE, rect)
    pygame.display.update()
    return grid        
            
def main():
    run = True
    grid = create_grid()
    draw_background()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        grid = draw(grid)
        button(grid)
        clear_button(grid)


if __name__ == "__main__":
    main()
