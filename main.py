import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def display_game_over(screen, font, player_score):
    # Main "GAME OVER" text
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))  # Red text
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))  # Centered vertically with some offset

    # Smaller score text below
    score_font = pygame.font.Font(None, 28)
    score_text = score_font.render(f"Final Score: {player_score}", True, (255, 255, 255))  # White text
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))  # Centered and slightly below "GAME OVER"

    # Flashing effect variables
    flashing = True
    flashing_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Fill the screen black
        screen.fill((0, 0, 0))

        # Flash "GAME OVER" text every 500ms
        flashing_timer += pygame.time.get_ticks() % 1000
        if flashing_timer > 500:
            flashing = not flashing
            flashing_timer = 0
        
        if flashing:
            screen.blit(game_over_text, game_over_rect)

        # Display the final score
        screen.blit(score_text, score_rect)

        pygame.display.flip()
        pygame.time.delay(100)


def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

    pygame.font.init()
    font = pygame.font.Font(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    _ = AsteroidField()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill((0, 0, 0))
        
        for sprite in updatable:
            sprite.update(dt)
            
        for sprite in drawable:
            sprite.draw(screen)
        
        for asteroid in asteroids:
            if asteroid.check_collision(player):
                player.die()
                if player.lives == 0:
                    display_game_over(screen, font, player.score)
                else:
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, player.lives, player.score)

            for shot in shots:
                if asteroid.check_collision(shot):
                    score = asteroid.split()
                    player.increment_score(score)
                    shot.kill()
        
        # draw the score
        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # draw remaining lives
        lives_text = font.render(f"Remaining lives: {player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))
        
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()