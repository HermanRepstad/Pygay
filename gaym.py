import pygame
import sys

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/ELMCM.mp3")
pygame.mixer.music.play(-1)

def scale_background(image, screen_width, screen_height):
    img_width, img_height = image.get_size()

    scale = max(
        screen_width / img_width,
        screen_height / img_height
    )

    new_size = (
        int(img_width * scale),
        int(img_height * scale)
    )

    scaled = pygame.transform.smoothscale(image, new_size)

    return scaled

# Font
font = pygame.font.SysFont(None, 40)

# Dialogue
show_dialogue = False
dialogue_text = "Velkommen til livet! Du er øyet mitt cuh. Broren din har forsvunnet! -Trykk ESC for å lukke"


# Screen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Wow eventyr")

clock = pygame.time.Clock()

# Load & scale player image
player_img = pygame.image.load("assets/EvilBrotha.png").convert_alpha()
player = pygame.transform.scale_by(player_img, 7)

# Load intro image
intro_img = pygame.image.load("assets/trollmannøye2.png").convert()
intro_img = pygame.transform.scale(intro_img, (WIDTH, HEIGHT))

# Load background
bakgrunn = pygame.image.load("assets/Bakgrunnrom.png").convert()
bakgrunn = pygame.transform.scale(bakgrunn, (WIDTH, HEIGHT))

wizard = pygame.image.load("assets/Wizard.png").convert_alpha()
wizard = pygame.transform.scale(wizard, (300, 300))

wizard_rect = wizard.get_rect()
wizard_rect.midbottom = (WIDTH - 350, HEIGHT - 145)

# Player rect (HITBOX = IMAGE SIZE)
player_rect = player.get_rect()
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 50

areas = [
    scale_background(
        pygame.image.load("assets/Bakgrunnrom.png").convert(),
        WIDTH,
        HEIGHT
    ),

    scale_background(
        pygame.image.load("assets/Bakgrunnrom2.png").convert(),
        WIDTH,
        HEIGHT
    )
]

current_area = 0

# Colors
WHITE = (240, 240, 240)
DARK = (30, 30, 30)

# Movement & physics
speed = 7
y_velocity = 0
gravity = 0.6
jump_strength = -15
on_ground = False

# Ground
ground_y = HEIGHT - 135


show_intro = True

INTRO_DURATION = 1500  # milliseconds (5 seconds)
intro_start_time = pygame.time.get_ticks()


walk_frames = []
for i in range(1, 5):
    img = pygame.image.load(f"assets/Player{i}.png").convert_alpha()
    img = pygame.transform.scale_by(img, 7)
    walk_frames.append(img) 

frame_index = 0
animation_speed = 0.15
current_frame = walk_frames[0]

while show_intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check if 5 seconds passed
    if pygame.time.get_ticks() - intro_start_time >= INTRO_DURATION:
        show_intro = False

    screen.blit(intro_img, (0, 0))
    pygame.display.flip()
    clock.tick(60)



# Game loop
while True:

    frame_index += animation_speed
    if frame_index >= len(walk_frames):
        frame_index = 0

    current_frame = walk_frames[int(frame_index)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                y_velocity = jump_strength
                on_ground = False

    # Interact with wizard
            if event.key == pygame.K_e:
                distance = abs(player_rect.centerx - wizard_rect.centerx)

                if distance < 150 and current_area == 0:
                    show_dialogue = True

            if event.key == pygame.K_ESCAPE:
                show_dialogue = False

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_rect.x -= speed  
    if keys[pygame.K_d]:
        player_rect.x += speed

    # Gravity
    y_velocity += gravity
    player_rect.y += y_velocity

    # Ground collision
    if player_rect.bottom >= ground_y:
        player_rect.bottom = ground_y
        y_velocity = 0
        on_ground = True

    

    
    # Move to next area if player reaches right edge
    if player_rect.right > WIDTH:
        if current_area < len(areas) - 1:  # Only move forward if there’s a next area
            current_area += 1
            player_rect.left = 0  # Start on left side of new area
            ground_y = HEIGHT - 170
# Move to previous area if player reaches left edge
    if player_rect.left < 0:
        if current_area > 0:  # Only move back if not in first area
            current_area -= 1
            player_rect.right = WIDTH
            ground_y = HEIGHT - 135
    # Keep player on screen
    

    distance = abs(player_rect.centerx - wizard_rect.centerx)
    
    player_rect.clamp_ip(screen.get_rect())
    # Draw

    # Player
    bg = areas[current_area]


    bg_x = (WIDTH - bg.get_width()) // 2
    bg_y = (HEIGHT - bg.get_height()) // 2

    screen.blit(bg, (bg_x, bg_y))
    


    if current_area == 0:
        screen.blit(wizard, wizard_rect)

    screen.blit(current_frame, player_rect)

    # Draw dialogue box
    if show_dialogue:

    # Box background
        dialogue_rect = pygame.Rect(100, HEIGHT - 250, WIDTH - 200, 150)
        pygame.draw.rect(screen, (20, 20, 20), dialogue_rect)

    # Border
        pygame.draw.rect(screen, WHITE, dialogue_rect, 2)

    # Render text
        text_surface = font.render(dialogue_text, True, WHITE)

    # Draw text
        screen.blit(text_surface, (dialogue_rect.x + 20, dialogue_rect.y + 20))

    if distance < 150 and current_area == 0 and not show_dialogue:
        hint = font.render("Press E to talk", True, WHITE)
        hint_rect = hint.get_rect(center=(wizard_rect.centerx, wizard_rect.top - 40))
        screen.blit(hint, hint_rect)

    if distance < 150 and current_area == 0 and show_dialogue:
        hint = font.render("Press ESC to close", True, WHITE)
        hint_rect = hint.get_rect(center=(wizard_rect.centerx, wizard_rect.top - 40))
        screen.blit(hint, hint_rect)

    pygame.display.flip()
    clock.tick(60)

