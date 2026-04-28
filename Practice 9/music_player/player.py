import pygame

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("iPod Style Player")

# (типо айподко)
BG = (245, 245, 245)      
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)
BLUE = (0, 120, 255)

font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 28)

sounds = [
    "sounds/Eminem Mockingbird.mp3",
    "sounds/2Pac All Eyez On Me.mp3",
    "sounds/The Neighbourhood Sweater Weather.mp3"
]

names = [
    "Eminem - Mockingbird",
    "2Pac - All Eyez On Me",
    "The Neighbourhood - Sweater Weather"
]

index = 0
isPaused = False

def play_music():
    pygame.mixer.music.load(sounds[index])
    pygame.mixer.music.play()

running = True
while running:
    screen.fill(BG)

    
    title = big_font.render("Now Playing", True, BLACK)
    screen.blit(title, (180, 30))

    
    song = font.render(names[index], True, BLACK)
    screen.blit(song, (80, 80))

    
    pygame.draw.rect(screen, GRAY, (80, 140, 340, 6), border_radius=5)

    
    pos = pygame.mixer.music.get_pos()  
    progress = max(0, min(pos / 1000, 100))  

    pygame.draw.rect(screen, BLUE, (80, 140, progress * 3.4, 6), border_radius=5)

    
    controls = font.render("P Play | S Stop | N Next | B Prev | SPACE Pause", True, BLACK)
    screen.blit(controls, (50, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                play_music()

            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()

            elif event.key == pygame.K_n:
                index = (index + 1) % len(sounds)
                play_music()

            elif event.key == pygame.K_b:
                index = (index - 1) % len(sounds)
                play_music()

            elif event.key == pygame.K_SPACE:
                if isPaused:
                    pygame.mixer.music.unpause()
                    isPaused = False
                else:
                    pygame.mixer.music.pause()
                    isPaused = True

    pygame.display.flip()

pygame.quit()
