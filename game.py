# Tyler Vo tkv9zd
# I used animataion, enemies, collectables, health bar, and a save point
import pygame
import gamebox
import random
camera = gamebox.Camera(800,600)

player_speed = 10  # speed of player
bat_velocity = 5  # speed of bat

game_on = False  # game off and player is not dead to start
player_dead = False
game_win = False

walls = [  # main outer walls stay on always
    gamebox.from_color(400, 50, "red", 800, 20),
    gamebox.from_color(0, 320, "red", 40, 560),
    gamebox.from_color(400, 590, "red", 800, 20),
    gamebox.from_color(800, 320, "red", 40, 560),
]
show_walls = [  # side of walls and background
    gamebox.from_color(400, 320, "indianred", 800, 560),
    gamebox.from_color(400, 70, "firebrick", 760, 20),
    gamebox.from_color(273, 210, "firebrick", 800, 20),
    gamebox.from_color(527, 340, "firebrick", 800, 20),
    gamebox.from_color(273, 470, "firebrick", 800, 20)
]
in_game_display = [  # Top of inside walls
    gamebox.from_color(273, 190, "red", 800, 20),
    gamebox.from_color(527, 320, "red", 800, 20),
    gamebox.from_color(273, 450, "red", 800, 20),
    gamebox.from_text(400,20,"Treasure Dungeon",25,"yellow",bold=True),

]
startscreen = [  # screen only shows up at the start of game
    gamebox.from_text(400,225,"Treasure Dungeon",75,"yellow",bold=True),
    gamebox.from_text(400, 290, "Find the key to open the chest and", 35, "yellow"),
    gamebox.from_text(400, 320, "unlock the dungeon's secrets", 35, "yellow"),
    gamebox.from_text(400, 375, "Press SPACE to start", 35, "yellow"),
    gamebox.from_text(400, 430, "Use the ARROW keys to evade the bats", 35, "yellow")
]
endscreen = [  # screen only shows up at the end of game
    gamebox.from_text(400, 225, "GAME OVER", 75, "red", bold=True),
    gamebox.from_text(400, 290, "Press SPACE to try again", 35, "yellow")
]
winscreen = [
    gamebox.from_text(400, 225, "YOU WIN", 75, "yellow", bold=True),
    gamebox.from_text(400, 290, "Press SPACE to play again", 35, "yellow")
]

key = gamebox.from_image(60,120,"Key.png")  # image of key
top_key = False  # no key collected


heart1 = gamebox.from_image(50,20,"heart.png")  # three hearts, gets taken away as player is hit
heart2 = gamebox.from_image(100,20, "heart.png")
heart3 = gamebox.from_image(150,20, "heart.png")

hearts = [ # list of hearts
    heart1,
    heart2,
    heart3
]

lives = 3  # lives counter

bat_sheet = gamebox.load_sprite_sheet("Bat_Sprite_Sheet.png", 1, 5)  # bat sheet
frame_bat = 0  # counter for bat

sheet_still = gamebox.load_sprite_sheet("Thief.png", 1, 4)  # standing still sheet
sheet_right = gamebox.load_sprite_sheet("Thief2.png", 2, 3)  # moving right sheet
sheet_left = gamebox.load_sprite_sheet("Thief3.png", 2, 3)  # moving left sheet

frame1 = 0  # frames for those sheets above
frame2 = 0
frame3 = 0
player = gamebox.from_image(60, 500, sheet_still[frame1])  # player box

bat1 = gamebox.from_image(random.randrange(60, 740), 100, bat_sheet[frame_bat])  # three bats with respective sheets
bat2 = gamebox.from_image(random.randrange(60, 740), 240, bat_sheet[frame_bat])
bat3 = gamebox.from_image(random.randrange(60, 740), 400, bat_sheet[frame_bat])

bats = [  # list of bats
    bat1,
    bat2,
    bat3
]
for bat in bats:  # sets movement speed of bat
    bat.xspeed = bat_velocity
    bat.yspeed = bat_velocity

chest_closed = gamebox.from_image(60,550,"treasure_chest_closed.png")
chest_open = gamebox.from_image(60,550,"treasure_chest_open.png")
chest_hit_box = gamebox.from_color(60, 565, "yellow", 50, 20)

##################################################
def tick(keys):
    global game_on
    global player_dead
    global game_win
    camera.clear("black")  # clears screen between frames

# ------- BACKGROUND AND DISPLAY ------------

    if not game_on:  # happens only at the beginning
        for text in startscreen:
            camera.draw(text)   # draws start-screen
    if game_on and not player_dead and not game_win:  # when game is running and player has not died
        for wall in show_walls:
            camera.draw(wall)  # draw side walls and background
        for item in in_game_display:
            camera.draw(item)  # draw main inside walls

        camera.draw(player)  # draws player

# ------- INPUT ---------
    global frame1
    global frame2
    global frame3
    if not game_on:     # while game is off (start-screen)
        if pygame.K_SPACE in keys:
            game_on = True  # starts game when SPACE is pressed

    if game_on and not player_dead and not game_win:  # while game is on and player is not dead
        if pygame.K_UP in keys:
            player.y -= player_speed  # player goes up when UP is pressed
        if pygame.K_DOWN in keys:
            player.y += player_speed  # player goes down when DOWN is pressed
        if pygame.K_RIGHT in keys:
            player.x += player_speed  # player goes right when RIGHT is pressed
            frame2 += 1
            if frame2 == 6:
                frame2 = 0
            player.image = sheet_right[frame2]  # cycles through sprite sheet
        elif pygame.K_LEFT in keys:
            player.x -= player_speed  # player goes left when LEFT is pressed
            frame3 += 1
            if frame3 == 6:
                frame3 = 0
            player.image = sheet_left[frame3]  # cycles through sprite sheet
        else:
            frame1 += 1  # if nothing is being pressed
            if frame1 == 4:
                frame1 = 0
            player.image = sheet_still[frame1]  # cycles through still sprite sheet

# ------ LIVES-------
    global lives
    global top_key
    if game_on and not player_dead and not game_win:  # while game is on and player is not dead
        if lives == 3:  # if there are three lives, draws all three
            camera.draw(heart1)
            camera.draw(heart2)
            camera.draw(heart3)
        elif lives == 2:  # if player loses life, draws only two
            camera.draw(heart1)
            camera.draw(heart2)
        elif lives == 1:    # if player loses another life, draws only one
            camera.draw(heart1)
        else:   # if no lives left, player is dead
            player_dead = True
            lives = 3  # resets lives back to 3
            top_key = False
            player.x = 60  # respawns player at start
            player.y = 540
            bat1.x = random.randrange(60, 740)
            bat1.y = 100
            bat2.x = random.randrange(60, 740)
            bat2.y = 240
            bat3.x = random.randrange(60, 740)
            bat3.y = 400

# ------ KEY --------
    if game_on and not player_dead and not top_key and not game_win:  # while game is on and player is not dead AND key has not been
        if player.touches(key):                      # grabbed
            top_key = True  # if player grabs key, key appears on top bar
        else:
            camera.draw(key)    # if player has yet to grab key, key is on map
    if top_key and not player_dead:  # if key is grabbed, key appears on top bar
        camera.draw(gamebox.from_image(200,20,"Key.png"))

# ------- CHEST ------------
    if game_on and not player_dead and not game_win:  # while game is on and player is not dead
        if player.touches(chest_closed) and top_key:
            game_win = True
    if not game_win and game_on:  # and not player_dead:  # while game is on and player is not dead AND game is not won
        camera.draw(chest_closed)
    elif game_win and game_on and not player_dead:
        camera.draw(chest_open)

# ------- ENEMIES -------------
    global frame_bat
    global bat_velocity
    if game_on and not player_dead and not game_win:  # while game is on and player is not dead
        for bat in bats:  # each bat moves
            bat.move_speed()
        for bat in bats:  # cycles through bat sprite sheets for each bat
            frame_bat += 1
            if frame_bat == 5:
                frame_bat = 0
            bat.image = bat_sheet[frame_bat]

        for bat in bats:  # if any bat touches outer walls, it bounces off
            if bat.touches(walls[0]):
                bat.yspeed = bat_velocity
            if bat.touches(walls[1]):
                bat.xspeed = bat_velocity
            if bat.touches(walls[2]):
                bat.yspeed = -bat_velocity
            if bat.touches(walls[3]):
                bat.xspeed = -bat_velocity

        for bat in bats:  # if any bat hits the side walls, it bounces off
            if bat.touches(show_walls[1]):
                bat.yspeed = bat_velocity
            if bat.touches(show_walls[2]):
                bat.yspeed = bat_velocity
            if bat.touches(show_walls[3]):
                bat.yspeed = bat_velocity
            if bat.touches(show_walls[4]):
                bat.yspeed = bat_velocity


        for bat in bats:  # if any bat touches the inside walls, it bounces off
            if bat.touches(in_game_display[0]):
                bat.yspeed = -bat_velocity
            if bat.touches(in_game_display[1]):
                bat.yspeed = -bat_velocity
            if bat.touches(in_game_display[2]):
                bat.yspeed = -bat_velocity

        for bat in bats:  # draws each bat
            camera.draw(bat)

        for bat in bats:  # for each bat
            if player.touches(bat) and not top_key:  # if player is alive and key is not picked up
                player.x = 60   # takes away a life and respawns player at start
                player.y = 500
                lives -= 1
                bat1.x = random.randrange(60,740)
                bat1.y = 100
                bat2.x = random.randrange(60,740)
                bat2.y = 240
                bat3.x = random.randrange(60,740)
                bat3.y = 400

            if player.touches(bat) and top_key:  # if player is alive and key is not picked up
                player.x = 60   # takes away a life and respawns player at start
                player.y = 120
                lives -= 1
                bat1.x = random.randrange(60, 740)
                bat1.y = 520
                bat2.x = random.randrange(60, 740)
                bat2.y = 240
                bat3.x = random.randrange(60, 740)
                bat3.y = 400

# ------- PLAYER COLLISION ---------

    for each in in_game_display:  # prevents player from going through walls
        if player.touches(each):
            player.move_to_stop_overlapping(each)
    for each in walls:
        if player.touches(each):
            player.move_to_stop_overlapping(each)
    if player.touches(chest_hit_box):
        player.move_to_stop_overlapping(chest_hit_box)

# -------- RESTART --------------

    if game_on and player_dead or game_on and game_win:  # while game is on but player is dead
        if pygame.K_SPACE in keys:  # pressing SPACE restarts game
            player_dead = False
            game_win = False

    if player_dead:  # when at 0 lives, player dies and game over screen shows
        for text in endscreen:
            camera.draw(text)

# -------- WIN --------------
    if game_win:
        for text in winscreen:
            camera.draw(text)
        lives = 3
        player.x = 60  # respawns player at start
        player.y = 540
        top_key = False

# ----- ALWAYS DRAW METHODS --------
    for wall in walls:  # draws each wall the entire time
        camera.draw(wall)
    camera.draw(gamebox.from_text(730,20,"Tyler Vo - tkv9zd",20,"yellow"))
    camera.display()

gamebox.timer_loop(30, tick)