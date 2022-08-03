import pygame
import gamebox
import random

'' \
''
camera = gamebox.Camera(800, 600)
character = gamebox.from_color(50, 200, "green", 15, 40)
character.yspeed = 0
walls = [
    gamebox.from_color(50, 250, "black", 200, 10),
    gamebox.from_color(400, 150, "black", 200, 10),
    gamebox.from_color(600, 25, "black", 200, 10),
]

counter = 0


def tick(keys):
    # get access to the counter
    global counter
    if pygame.K_RIGHT in keys:
        character.x += 10
    if pygame.K_LEFT in keys:
        character.x -= 10
    character.yspeed += 1
    character.y = character.y + character.yspeed
    camera.clear("cyan")
    camera.draw(character)

    # makes the screen scroll
    camera.y -= 3

    # make random walls appear every time the counter hits a particular number
    # notice how I use the random.randint to vary the height of the platform
    # also I add in the camera.x to the x position because the screen keeps moving
    counter += 1
    if counter % 50 == 0:
        new_wall = gamebox.from_color(random.randint(200, 600), camera.y - 300, "black", random.randint(100, 250), 10)
        walls.append(new_wall)

    for wall in walls:
        if character.bottom_touches(wall):
            character.yspeed = 0
            if pygame.K_UP in keys or pygame.K_SPACE in keys:
                character.yspeed = -20
        if character.touches(wall):
            character.move_to_stop_overlapping(wall)
        camera.draw(wall)

    # Check gameover condition
    if character.y >= camera.y + 400:
        camera.draw(gamebox.from_text(400, camera.y + 250, "DEAD", 70, "red"))
        camera.display()
        # this line will end the game
        gamebox.pause()

    camera.display()


ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)