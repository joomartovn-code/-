import pygame
import asyncio
from engine import RouletteGame


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
heart_img = pygame.image.load("assets/images/heart.png")
revolver_img = pygame.image.load("assets/images/revolver.png")


async def play_shot_animation():
    for i in range(10):
        screen.fill((255, 0, 0)) 
        pygame.display.flip()
        await asyncio.sleep(0.01)
    screen.fill((0, 0, 0))

async def main():
    game = RouletteGame(bullets=2) 
    running = True

    while running:
        screen.fill((30, 30, 30))
        
    
        for i in range(game.lives):
            screen.blit(heart_img, (20 + i * 50, 20))

        screen.blit(revolver_img, (250, 200))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    result = game.pull_trigger()
                    if result == 1:
                        shot_sound.play()
                        await play_shot_animation()
                        game.lives -= 1
                        print("БАХ! Минус жизнь.")
                    else:
                        print("Щелчок... повезло.")
        
        if game.lives <= 0:
            print("Игра окончена!")
            running = False

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

if __name__ == "__main__":
    asyncio.run(main())