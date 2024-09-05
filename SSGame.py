import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simon Says")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Button dimensions and positions
BUTTON_SIZE = 200
button_rects = {
    "green": pygame.Rect(50, 100, BUTTON_SIZE, BUTTON_SIZE),
    "red": pygame.Rect(300, 100, BUTTON_SIZE, BUTTON_SIZE),
    "blue": pygame.Rect(50, 350, BUTTON_SIZE, BUTTON_SIZE),
    "yellow": pygame.Rect(300, 350, BUTTON_SIZE, BUTTON_SIZE)
}

# List of button colors
button_colors = ["green", "red", "blue", "yellow"]

# Maximum level
max_level = 10

# Fonts
font_large = pygame.font.SysFont("Arial", 60)
font_medium = pygame.font.SysFont("Arial", 40)
font_small = pygame.font.SysFont("Arial", 30)

# Badge system
badges = {
    "Beginner": 50,
    "Intermediate": 150,
    "Expert": 300
}

def draw_text(text, font, color, x, y):
    """Draws text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_buttons(highlighted_color=None):
    """Draws the buttons on the screen, optionally highlighting one."""
    screen.fill(WHITE)
    for color, rect in button_rects.items():
        pygame.draw.rect(screen, globals()[color.upper()] if color != highlighted_color else GRAY, rect)
    pygame.display.flip()

def show_sequence(sequence):
    """Shows the sequence of button presses to the player."""
    for color in sequence:
        draw_buttons(color)
        pygame.time.wait(500)
        draw_buttons()
        pygame.time.wait(250)

def check_input():
    """Checks if the user input matches the sequence."""
    return user_input == sequence

def get_badge(score):
    """Determines the badge based on the score."""
    if score >= badges["Expert"]:
        return "Expert"
    elif score >= badges["Intermediate"]:
        return "Intermediate"
    elif score >= badges["Beginner"]:
        return "Beginner"
    return None

def main_menu():
    """Displays the main menu."""
    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Simon Says", font_large, BLACK, 200, 100)
        draw_text("Press ENTER to Start", font_medium, BLACK, 200, 300)
        draw_text("Press ESC to Quit", font_small, BLACK, 300, 400)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    global sequence, user_input, level, score
                    sequence = []
                    user_input = []
                    level = 1
                    score = 0
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def instruction_screen():
    """Displays the instructions for the game."""
    running = True
    while running:
        screen.fill(WHITE)
        draw_text("How to Play", font_large, BLACK, 200, 50)
        draw_text("1. Follow the sequence of colors shown.", font_medium, BLACK, 50, 150)
        draw_text("2. Click the colored buttons in the same order.", font_medium, BLACK, 50, 200)
        draw_text("3. The sequence gets longer with each level.", font_medium, BLACK, 50, 250)
        draw_text("4. Score points by matching the sequence.", font_medium, BLACK, 50, 300)
        draw_text("Press ENTER to Start", font_medium, BLACK, 200, 400)
        draw_text("Press ESC to Quit", font_small, BLACK, 300, 500)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def game_loop():
    """Main game loop."""
    global sequence, user_input, score, level
    while True:
        screen.fill(WHITE)
        draw_text(f"Level: {level}", font_medium, BLACK, 50, 20)
        draw_text(f"Score: {score}", font_medium, BLACK, 650, 20)
        pygame.display.flip()

        # Generate sequence for current level
        sequence = [random.choice(button_colors) for _ in range(level)]
        
        # Show sequence to player
        show_sequence(sequence)
        
        # Get user input
        user_input = []
        while len(user_input) < len(sequence):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for color, rect in button_rects.items():
                        if rect.collidepoint(pos):
                            user_input.append(color)
                            draw_buttons(color)
                            pygame.time.wait(500)
                            draw_buttons()
                            break
            pygame.time.wait(100)
        
        # Check if user input matches sequence
        if check_input():
            score += level * 10
            level += 1
            if level > max_level:
                badge = get_badge(score)
                screen.fill(WHITE)
                draw_text("Congratulations! You Win!", font_large, BLACK, 100, 150)
                if badge:
                    draw_text(f"You earned the {badge} Badge!", font_medium, BLACK, 100, 250)
                pygame.display.flip()
                pygame.time.wait(3000)
                return
        else:
            screen.fill(WHITE)
            draw_text("Incorrect! Game Over!", font_large, RED, 100, 250)
            pygame.display.flip()
            pygame.time.wait(3000)
            return

# Start the game
instruction_screen()
main_menu()
game_loop()
