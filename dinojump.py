# Tyler Vo  tkv9zd

import pygame
import gamebox
import random
camera = gamebox.Camera(800,270)

score = 0
dino_alive = False
game_on = False
# -----BACKGROUND-----
ground = gamebox.from_color(400,230,"black",800,3)

# -----DINO------
sheet = gamebox.load_sprite_sheet("dinosprite.png", 1, 4)
dino_dead = gamebox.from_image(100,200,"dinodead.png")
frame = 0
dino = gamebox.from_image(100, 200, sheet[frame])
# -----CACTUS------
cactus = [
    gamebox.from_image(1200,200,"bigcactus.png"),
    gamebox.from_image(2300,210,"small cactus.png"),
    gamebox.from_image(3600,200,"bigsmallcactus.png")
]

def tick(keys):
    camera.clear("white")
    global game_on
    global score
    global dino_alive

    dino.yspeed += 3
    dino.y = dino.y + dino.yspeed

    if game_on == False:
        camera.draw(gamebox.from_text(400, 130, "Press SPACE to Begin", 50, "gray"))

    if pygame.K_SPACE in keys and game_on == False:
        game_on = True
        dino_alive = True
    if game_on:
        camera.draw(ground)
        camera.draw(dino)
    if game_on == False and dino_alive== False:
        camera.draw(dino)



    # ----DINO JUMP------

    if dino.touches(ground):
        dino.move_to_stop_overlapping(ground)
    if dino.bottom_touches(ground):
        dino.yspeed = 0
        if pygame.K_UP in keys or pygame.K_SPACE in keys:
            dino.yspeed = -30
    if dino.touches(ground):
        dino.move_to_stop_overlapping(ground)

    # ------CACTUS-------
    if game_on and dino_alive:
        for each in cactus:
            each.speedx = -30
            each.move_speed()

    if game_on:
        for each in cactus:
            if each.x < 820:
                camera.draw(each)
            if each.x < -20:
                each.x = 3000
                each.x = random.randrange(3000,5000)

    # ------CACTUS COLLISION-------
    global score

    for each in cactus:
        if dino.touches(each):
            dino_alive = False
            dino_dead.move_to_stop_overlapping(ground)
            camera.draw(dino_dead)
            camera.draw(gamebox.from_text(400, 130, "GAME OVER", 50, "gray"))
            if pygame.K_SPACE in keys:
                cactus[0] =gamebox.from_image(1200,200,"bigcactus.png")
                cactus[1] =gamebox.from_image(2300,210,"small cactus.png")
                cactus[2] =gamebox.from_image(3600,200,"bigsmallcactus.png")
                dino_alive = True
                score = 0


    # -----SCORE-----------
    if game_on and dino_alive:
        score += 1
    camera.draw(gamebox.from_text(750, 20, "SCORE: " + str(score), 20, "gray"))



    global frame
    if game_on and dino_alive:
        frame += 1
        if frame == 4:
            frame = 0
        dino.image = sheet[frame]


    camera.display()


gamebox.timer_loop(30, tick)