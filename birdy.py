import pygame
import sys
import random

class BirdyGame:
    def __init__(self):
        pygame.init()

        # Colors
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.BIRD_COLOR = (0, 0, 0)
        self.HURDLE_COLOR = (0, 0, 0)
        self.TEXT_COLOR = (0, 0, 0)
        self.SCORE_BACKGROUND_COLOR = (200, 200, 200)
        
        # Set up display
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Birdy")

        # Load background image
        self.background_image = pygame.image.load("media/background.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        # Load bird image
        self.bird_image = pygame.image.load("media/bird.png")
        self.bird_size = (50, 50)
        self.bird_image = pygame.transform.scale(self.bird_image, self.bird_size)

        # Bird attributes
        self.bird_rect = self.bird_image.get_rect()
        self.bird_rect.x = self.width // 4
        self.bird_rect.y = self.height // 2
        self.bird_speed = 50
        self.jump_height = 40
        self.gravity = 5

        # Hurdle attributes
        self.hurdle_width = 50
        self.hurdle_height = random.randint(100, self.height - 100)
        self.hurdle_x = self.width
        self.hurdle_speed = 1
        self.speed_increment = 0.01
        self.gap_height = 200

        # Game variables
        self.score = 0
        self.game_active = False

   # Font for score and title screen
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.title_screen = True
  
   # Lets activate music

        pygame.mixer.init()
        pygame.mixer.music.load("media/background_music.mp3")
        pygame.mixer.music.play(-1)  # -1 means play in an infinite loop
         # Load collision sound effect
        self.collision_sound = pygame.mixer.Sound("media/collision_sound.mp3")
        # Game loop
        self.clock = pygame.time.Clock()


    def draw_title_screen(self):
        # Draw background
        self.screen.blit(self.background_image, (0, 0))
        # Draw title
        title_text = self.title_font.render("Birdy Game", True, self.TEXT_COLOR)
        self.screen.blit(title_text, (self.width // 4, self.height // 3))
        # Draw instructions
        instructions_text = self.font.render("Press SPACE to start", True, self.TEXT_COLOR)
        self.screen.blit(instructions_text, (self.width // 4, self.height // 2))


    def draw_score(self):
        score_background_rect = pygame.Rect(10, 10, 150, 40)
        pygame.draw.rect(self.screen, self.SCORE_BACKGROUND_COLOR, score_background_rect)
        # Draw border around score display
        pygame.draw.rect(self.screen, self.BIRD_COLOR, score_background_rect, 3)
        # Draw score text
        text = self.font.render(f"Score: {int(self.score)}", True, self.TEXT_COLOR)
        self.screen.blit(text, (30, 20))  # Adjusted position for better alignment


    def draw_score_at_end(self):
        # Draw background for score
        score_background_rect = pygame.Rect(self.width // 2 - 75, self.height // 2 - 20, 150, 40)
        pygame.draw.rect(self.screen, self.SCORE_BACKGROUND_COLOR, score_background_rect)

        # Draw score text
        text = self.font.render(f"Score: {int(self.score)}", True, self.TEXT_COLOR)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect.topleft)
      
            
    def reset_game(self):
        # Reset game state
        self.bird_rect.x = self.width // 4
        self.bird_rect.y = self.height // 2
        self.hurdle_x = self.width
        self.hurdle_height = random.randint(100, self.height - 100)
        self.score = 0
        self.game_active = True
        self.hurdle_speed = 1
        self.jump_height = 40
        self.gravity = 5
        self.title_screen = True

    
    def handle_title_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.title_screen = False
   
    def handle_events(self):
        if self.title_screen:
            self.handle_title_screen_events()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_active:
                            self.bird_rect.y -= self.jump_height
                        else:
                            self.reset_game()


    def update_game_state(self):
        if self.game_active:
            # Simulate gravity and adjust gravity and jump_height based on hurdle speed
            self.gravity = 5 + self.hurdle_speed * 0.2
            self.jump_height = 40 + self.hurdle_speed * 0.5
            self.bird_rect.y += self.gravity

            # Move the hurdle
            self.hurdle_x -= self.hurdle_speed

            # Check for collision with hurdle
            if self.bird_rect.colliderect(pygame.Rect(self.hurdle_x, 0, self.hurdle_width, self.hurdle_height)) or \
                    self.bird_rect.colliderect(pygame.Rect(self.hurdle_x, self.hurdle_height + self.gap_height,
                    self.hurdle_width, self.height - (self.hurdle_height + self.gap_height))) or \
                    self.bird_rect.top < 0 or self.bird_rect.bottom > self.height:
                print("Game Over! Score:",self.draw_score)
                self.collision_sound.play()
                self.game_active = False


            # Score based on hurdle speed
            self.score += self.hurdle_speed

            # Increase hurdle speed progressively
            self.hurdle_speed += self.speed_increment

            # Spawn a new hurdle when the current one is off-screen
            if self.hurdle_x < 0:
                self.hurdle_x = self.width
                self.hurdle_height = random.randint(100, self.height - 100)


    def draw_elements(self):
        # Draw background
        self.screen.blit(self.background_image, (0, 0))
        if self.title_screen:
            self.draw_title_screen()
        elif self.game_active:
            # Draw bird
            self.screen.blit(self.bird_image, self.bird_rect)

            # Draw hurdle
            pygame.draw.rect(self.screen, self.HURDLE_COLOR, (self.hurdle_x, 0, self.hurdle_width, self.hurdle_height))
            pygame.draw.rect(self.screen, self.HURDLE_COLOR, (self.hurdle_x, self.hurdle_height + self.gap_height, self.hurdle_width, self.height - (self.hurdle_height + self.gap_height)))

            # Draw score
            font = pygame.font.Font(None, 36)
            text = font.render(f"Score: {self.score}", True, self.BIRD_COLOR)
            self.draw_score()

        else:
            # Draw game over message
            font = pygame.font.Font(None, 72)
            text = font.render("Game Over", True, self.BIRD_COLOR)
            self.screen.blit(text, (self.width // 4, self.height // 3))

            # Draw restart message
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Press SPACE to restart", True, self.BIRD_COLOR)
            self.screen.blit(restart_text, (self.width // 4, self.height // 2))
            self.draw_score_at_end()

            

            # Check for restart input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.reset_game()

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        self.clock.tick(30)

