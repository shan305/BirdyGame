import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Birdy")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
# Load background image
background_image = pygame.image.load("background.jpg")  # Replace "background.jpg" with the actual filename or path
background_image = pygame.transform.scale(background_image, (width, height))


# Load bird image
bird_image = pygame.image.load("bird.png")  # Replace "bird.png" with the actual filename or path
bird_rect = bird_image.get_rect()


# Resize bird image
bird_size = (50, 50)  # Replace with your desired size
bird_image = pygame.transform.scale(bird_image, bird_size)


# Bird attributes
bird_rect = bird_image.get_rect()
bird_rect.x = width // 4
bird_rect.y = height // 2
bird_speed = 50
jump_height = 40
gravity = 5

# Hurdle attributes
hurdle_width = 50
hurdle_height = random.randint(100, height - 100)
hurdle_x = width
hurdle_speed = 1  # Initial hurdle speed
speed_increment = 0.01  # Speed increment per frame
gap_height = 150

# Game variables
score = 0
game_active = False  # Flag to check if the game is active

# Function to reset the game state
def reset_game():
    global bird_rect, hurdle_x, hurdle_height, score, game_active, hurdle_speed, jump_height, gravity
    bird_rect.x = width // 4
    bird_rect.y = height // 2
    hurdle_x = width
    hurdle_height = random.randint(100, height - 100)
    score = 0
    game_active = True
    hurdle_speed = 1  # Reset hurdle speed
    jump_height = 40  # Reset jump height
    gravity = 5  # Reset gravity


# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_rect.y -= jump_height

    if game_active:
        # Simulate gravity and adjust gravity and jump_height based on hurdle speed
        gravity = 5 + hurdle_speed * 0.2
        jump_height = 40 + hurdle_speed * 0.5
        bird_rect.y += gravity

        # Move the hurdle
        hurdle_x -= hurdle_speed

        # Check for collision with hurdle
        if bird_rect.colliderect(pygame.Rect(hurdle_x, 0, hurdle_width, hurdle_height)) or \
            bird_rect.colliderect(pygame.Rect(hurdle_x, hurdle_height + gap_height, hurdle_width, height - (hurdle_height + gap_height))) or \
            bird_rect.top < 0 or bird_rect.bottom > height:
                print("Game Over! Score:", score)
                game_active = False

        # Score based on hurdle speed
        score += hurdle_speed

        # Increase hurdle speed progressively
        hurdle_speed += speed_increment

        # Spawn a new hurdle when the current one is off-screen
        if hurdle_x < 0:
            hurdle_x = width
            hurdle_height = random.randint(100, height - 100)

        # Draw background
        screen.blit(background_image, (0, 0))

        # Draw bird
        screen.blit(bird_image, bird_rect)

        # Draw hurdle
        pygame.draw.rect(screen, black, (hurdle_x, 0, hurdle_width, hurdle_height))
        pygame.draw.rect(screen, black, (hurdle_x, hurdle_height + gap_height, hurdle_width, height - (hurdle_height + gap_height)))

        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, black)
        screen.blit(text, (10, 10))

    else:
        # Draw game over message
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, black)
        screen.blit(text, (width // 4, height // 3))

        # Draw restart message
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press SPACE to restart", True, black)
        screen.blit(restart_text, (width // 4, height // 2))

        # Check for restart input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)