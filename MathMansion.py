import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Mansion")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font_large = pygame.font.SysFont("ComicSans", 40)  # Changed font to ComicSans and size to 60
font_small = pygame.font.SysFont("ComicSans", 30)  # Changed font to ComicSans and size to 40

# Game variables
current_screen = "main_menu"
score = 0
problems_solved = 0
difficulty_level = 1
time_limit = 10  # Time limit for each question in seconds
reward_time = 2  # Time in seconds for displaying correct feedback

# Badges
badges = {
    "Beginner": {"score": 50, "earned": False},
    "Intermediate": {"score": 100, "earned": False},
    "Advanced": {"score": 200, "earned": False},
}

def draw_text(text, font, color, x, y):
    """Draws text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def generate_problem(category, difficulty):
    """Generates a math problem based on the category and difficulty."""
    if category == "addition":
        a = random.randint(1 * difficulty, 10 * difficulty)
        b = random.randint(1 * difficulty, 10 * difficulty)
        return f"{a} + {b}", a + b
    elif category == "subtraction":
        a = random.randint(1 * difficulty, 10 * difficulty)
        b = random.randint(1 * difficulty, a)  # Ensure no negative answers
        return f"{a} - {b}", a - b
    elif category == "multiplication":
        a = random.randint(1 * difficulty, 5 * difficulty)
        b = random.randint(1 * difficulty, 5 * difficulty)
        return f"{a} * {b}", a * b
    elif category == "division":
        a = random.randint(1 * difficulty, 10 * difficulty)
        b = random.randint(1, 10)
        a *= b  # Ensures that division is clean
        return f"{a} / {b}", a // b

def draw_main_menu():
    """Draws the main menu."""
    screen.fill(WHITE)
    draw_text("Math Mansion", font_large, BLUE, 150, 100)
    draw_text("Press ENTER to Start", font_small, BLACK, 150, 300)
    pygame.display.flip()

def draw_mansion_room():
    """Draws the mansion room where math categories are selected."""
    screen.fill(WHITE)
    draw_text("Choose a Math Room:", font_large, BLUE, 100, 100)
    draw_text("1. Addition", font_small, BLACK, 100, 200)
    draw_text("2. Subtraction", font_small, BLACK, 100, 250)
    draw_text("3. Multiplication", font_small, BLACK, 100, 300)
    draw_text("4. Division", font_small, BLACK, 100, 350)
    pygame.display.flip()

def draw_timer(time_left):
    """Displays a countdown timer on the screen."""
    draw_text(f"Time Left: {time_left} sec", font_small, RED, 550, 20)
    pygame.display.flip()

def draw_score_and_badges():
    """Displays the score and badges."""
    screen.fill(WHITE)
    draw_text(f"Score: {score}", font_large, BLUE, 20, 20)
    
    y_offset = 100
    for badge, info in badges.items():
        if info["earned"]:
            draw_text(f"{badge} Badge Earned!", font_small, GREEN, 20, y_offset)
        y_offset += 50
    
    pygame.display.flip()

def check_badges():
    """Check and update badges based on score."""
    global badges
    for badge, info in badges.items():
        if score >= info["score"] and not info["earned"]:
            info["earned"] = True
            # Show badge earned notification
            screen.fill(WHITE)
            draw_text(f"Congratulations! You earned the {badge} Badge!", font_large, GREEN, 100, 300)
            pygame.display.flip()
            pygame.time.wait(2000)  # Show for 2 seconds

def solve_problem(category):
    """Handles the math problem-solving process."""
    global problems_solved, score, difficulty_level, start_time
    problem, answer = generate_problem(category, difficulty_level)
    user_input = ""
    start_time = time.time()

    while True:
        screen.fill(WHITE)
        draw_text(f"Solve: {problem}", font_large, BLACK, 250, 100)
        draw_text(f"Your Answer: {user_input}", font_small, BLACK, 250, 200)
        
        time_left = max(0, time_limit - int(time.time() - start_time))
        draw_timer(time_left)
        
        if time_left == 0:
            return False
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        if int(user_input) == answer:
                            problems_solved += 1
                            score += 10 * difficulty_level
                            difficulty_level += 1
                            check_badges()  # Check for badge updates
                            return True
                        else:
                            return False
                    except ValueError:
                        return False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if event.unicode.isdigit():
                        user_input += event.unicode

def game_loop():
    """Main game loop."""
    global current_screen
    while True:
        if current_screen == "main_menu":
            draw_main_menu()
        elif current_screen == "mansion_room":
            draw_mansion_room()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if current_screen == "main_menu" and event.key == pygame.K_RETURN:
                    current_screen = "mansion_room"
                elif current_screen == "mansion_room":
                    if event.key == pygame.K_1:
                        correct = solve_problem("addition")
                    elif event.key == pygame.K_2:
                        correct = solve_problem("subtraction")
                    elif event.key == pygame.K_3:
                        correct = solve_problem("multiplication")
                    elif event.key == pygame.K_4:
                        correct = solve_problem("division")
                    if correct:
                        screen.fill(WHITE)
                        draw_text("Correct!", font_large, GREEN, 300, 400)
                        pygame.display.flip()
                        pygame.time.wait(reward_time * 1000)
                    else:
                        screen.fill(WHITE)
                        draw_text("Incorrect!", font_large, RED, 300, 400)
                        pygame.display.flip()
                        pygame.time.wait(2000)
                    
                    # Display score and badges after each problem
                    draw_score_and_badges()

# Start the game
game_loop()
