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


font = pygame.font.SysFont(None, 40)

#Tekstbokser
show_dialogue = False
dialogue_text = "Broren din er borte. Du må finne han. Veien er blokkert av snø. Spade er til venstre"

show_dialogue2 = False
dialogue_text2 = "Du trenger en nøkkel til døra"

#Fikser fullscreen og sånnt
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Wow eventyr")

clock = pygame.time.Clock()


#Loader ting
player_img = pygame.image.load("assets/EvilBrotha.png").convert_alpha()
player = pygame.transform.scale_by(player_img, 7)


intro_img = pygame.image.load("assets/trollmannøye2.png").convert()
intro_img = pygame.transform.scale(intro_img, (WIDTH, HEIGHT))


bakgrunn = pygame.image.load("assets/Bakgrunnrom.png").convert()
bakgrunn = pygame.transform.scale(bakgrunn, (WIDTH, HEIGHT))

wizard = pygame.image.load("assets/Wizard.png").convert_alpha()
wizard = pygame.transform.scale(wizard, (300, 300))

wizard_rect = wizard.get_rect()
wizard_rect.midbottom = (WIDTH - 350, HEIGHT - 145)


key = pygame.image.load("assets/key.png").convert_alpha()
key = pygame.transform.scale(key, (200, 200))

key_rect = key.get_rect()
key_rect.midbottom = (WIDTH - 350, HEIGHT - 190)


spade = pygame.image.load("assets/Spade.png").convert_alpha()
spade = pygame.transform.scale(spade, (200, 200))

spade_rect = key.get_rect()
spade_rect.midbottom = (WIDTH - 650, HEIGHT - 190)

#Hitbox
player_rect = player.get_rect()
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 50

#Liste over rommene
areas = [
     scale_background(
        pygame.image.load("assets/Bakgrunnrom3.png").convert(),
        WIDTH,
        HEIGHT
    ),


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

#Random variabler
current_area = 1

WHITE = (240, 240, 240)
DARK = (30, 30, 30)

speed = 12
y_velocity = 0
gravity = 0.6
jump_strength = -15
on_ground = False

ground_y = HEIGHT - 135

keypickedup = False
spadepickedup = False

show_intro = True

INTRO_DURATION = 1500 
intro_start_time = pygame.time.get_ticks()


walk_frames = []
for i in range(1, 5):
    img = pygame.image.load(f"assets/Player{i}.png").convert_alpha()
    img = pygame.transform.scale_by(img, 7)
    walk_frames.append(img) 

frame_index = 0
animation_speed = 0.15
current_frame = walk_frames[0]

#Intro
while show_intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pygame.time.get_ticks() - intro_start_time >= INTRO_DURATION:
        show_intro = False

    screen.blit(intro_img, (0, 0))
    pygame.display.flip()
    clock.tick(60)



# Gameloop
while True:

    frame_index += animation_speed
    if frame_index >= len(walk_frames):
        frame_index = 0

    current_frame = walk_frames[int(frame_index)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # hopp
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                y_velocity = jump_strength
                on_ground = False

    # Snakke med trollmann
            if event.key == pygame.K_e:
                distance = abs(player_rect.centerx - wizard_rect.centerx)

                if distance < 150 and current_area == 1:
                    show_dialogue = True

            if event.key == pygame.K_ESCAPE:
                show_dialogue = False


            # Plukke opp nøkkel
            if event.key == pygame.K_e:
                distance = abs(player_rect.centerx - key_rect.centerx)

                if distance < 150 and current_area == 2:
                    keypickedup = True

             # Plukke opp spade
            if event.key == pygame.K_e:
                distance = abs(player_rect.centerx - spade_rect.centerx)

                if distance < 150 and current_area == 0:
                    spadepickedup = True



    #Bevegelse og physics
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_rect.x -= speed  
    if keys[pygame.K_d]:
        player_rect.x += speed

   
    y_velocity += gravity
    player_rect.y += y_velocity

    if player_rect.bottom >= ground_y:
        player_rect.bottom = ground_y
        y_velocity = 0
        on_ground = True

    

    
    # Move to next area if player reaches right edge
    if player_rect.right > WIDTH:
        if current_area < len(areas) - 1:  # Only move forward if there’s a next area
            current_area += 1
            player_rect.left = 0  # Start on left side of new area
            
# Move to previous area if player reaches left edge
    if player_rect.left < 0:
        if current_area > 1:  # Only move back if not in first area
            current_area -= 1
            player_rect.right = WIDTH
            
    # Keep player on screen
    if player_rect.left < 0:
        if current_area == 1 and keypickedup == True:  
            current_area -= 1
            player_rect.right = WIDTH
            

    if player_rect.left < 0:
        if current_area == 1 and keypickedup == False:
           show_dialogue2 = True

    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
                show_dialogue2 = False

 

    distance = abs(player_rect.centerx - wizard_rect.centerx)
    distance2 = abs(player_rect.centerx - spade_rect.centerx)
    
    player_rect.clamp_ip(screen.get_rect())
    # Draw

    # Player
    bg = areas[current_area]


    bg_x = (WIDTH - bg.get_width()) // 2
    bg_y = (HEIGHT - bg.get_height()) // 2

    screen.blit(bg, (bg_x, bg_y))
    


    if current_area == 1:
        screen.blit(wizard, wizard_rect)

    if current_area == 2 and keypickedup==False:
        screen.blit(key, key_rect)

    if current_area == 0 and spadepickedup==False:
        screen.blit(spade, spade_rect)

    screen.blit(current_frame, player_rect)

    # Draw dialogue box
    if show_dialogue:

    # Box background
        dialogue_rect = pygame.Rect(100, HEIGHT - 250, WIDTH - 200, 150)
        pygame.draw.rect(screen, (20, 20, 20), dialogue_rect)

    # Render text
        text_surface = font.render(dialogue_text, True, WHITE)


    # Draw text
        screen.blit(text_surface, (dialogue_rect.x + 20, dialogue_rect.y + 20))

    if distance < 150 and current_area == 1 and not show_dialogue:
        hint = font.render("Trykk E for å snakke", True, WHITE)
        hint_rect = hint.get_rect(center=(wizard_rect.centerx, wizard_rect.top - 40))
        screen.blit(hint, hint_rect)

    if distance < 150 and current_area == 1 and show_dialogue:
        hint = font.render("Trykk ESC for å lukke", True, WHITE)
        hint_rect = hint.get_rect(center=(wizard_rect.centerx, wizard_rect.top - 40))
        screen.blit(hint, hint_rect)

    if distance < 150 and current_area == 2 and keypickedup == False:
        hint = font.render("Trykk E for å plukke opp", True, 0)
        hint_rect = hint.get_rect(center=(key_rect.centerx, key_rect.top - 70))
        screen.blit(hint, hint_rect)

    if distance2 < 150 and current_area == 0 and spadepickedup == False:
        hint = font.render("Trykk E for å plukke opp", True, WHITE)
        hint_rect = hint.get_rect(center=(spade_rect.centerx, spade_rect.top - 70))
        screen.blit(hint, hint_rect)

    if show_dialogue2:

    # Box background
        dialogue_rect = pygame.Rect(100, HEIGHT - 250, WIDTH - 200, 150)
        pygame.draw.rect(screen, (20, 20, 20), dialogue_rect)

    # Render text
        text_surface = font.render(dialogue_text2, True, WHITE)


    # Draw text
        screen.blit(text_surface, (dialogue_rect.x + 20, dialogue_rect.y + 20))

    

    pygame.display.flip()
    clock.tick(60)

