import gamebox
import pygame
camera = gamebox.Camera(400,400)
box = gamebox.from_color(200,200,"white",50,50)
def steve(keys):
    camera.clear("black")
    box.x += 1
    camera.draw(box)
    camera.display()

gamebox.timer_loop(30, steve)

