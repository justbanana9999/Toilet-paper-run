#handle exceptions
import sys
from sys import exit

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyError):
        print('Need to load',exc_value)
        return
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
    # print(f"Unhandled exception: {exc_type.__name__}: {exc_value},{exc_traceback}")

sys.excepthook = handle_exception

#measure load time
from time import time as t

time1 = t()

import pygame

from random import randint

try:
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
except:
    print('DPI not supported')

res = (1000,700)
mid = [res[0]/2,res[1]/2]

screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()

def checkExit():
    global focus
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            #save progress
            with open('Info','w') as file:
                file.write(f'total_money = {total_money}\n')
                file.write(f'score = {score}\n')
                file.write(f'high_score = {high_score}\n')
                file.write(f'global_volume = {global_volume}\n')
                file.write(f'theme = {theme}\n')
                file.write(f'bought = {bought}\n')
                file.write(f'hitboxes = {hitboxes}\n')
                file.write(f'fancy = {fancy}\n')
            
            pygame.quit()
            exit()
        
        #check window focus
        elif event.type == pygame.ACTIVEEVENT:
            if event.gain == 1 or event.state == 1:
                focus = True
            else:
                focus = False

global_scale = 10

hitboxes = True

fancy = True

import math

mouse_clicked = False

def button(num,pos,size=global_scale):
    global mouse_clicked
    global b_sizes,b_time
    global mouse_pos,mouse_click
    sprite = sprites['button'][num]
    
    rect = scale(sprite,b_sizes[num]).get_rect()
    rect.center = [pos[0]+mid[0],pos[1]+mid[1]]
    
    press = False
    if rect.collidepoint(mouse_pos):
        size *= 1.2
        b_time[num] += 1
        
        if mouse_click[0] and not mouse_clicked:
            press = True
    else:
        b_time[num] = 0
    
    b_sizes[num] = smooth(b_sizes[num],size,2)
    
    angle = math.sin(math.radians(b_time[num]*25))*2
    
    if hitboxes:
        pygame.draw.rect(screen,(0,0,255),rect,2)
    
    if fancy:
        display_image(sprite,pos,b_sizes[num],angle)
    else:
        display_image(sprite,pos)
    
    if press:
        play_sound('click')
        return True
    else:
        return False

def display_image(image,pos=(0,0),size=global_scale,angle=0,anchor=False):
    '''
    Returns the transformed image rect
    '''
    
    if size != 1:
        image = scale(image,size)
    if angle != 0:
        image,rect = rot_center(image,angle,pos[0]+mid[0],pos[1]+mid[1])
    else:
        rect = image.get_rect()
        rect.center = (pos[0]+mid[0],pos[1]+mid[1])
    
    if anchor != False:
        if anchor == 'top':
            rect.top = rect.centery
        elif anchor == 'bottom':
            rect.bottom = rect.centery
        elif anchor == 'left':
            rect.left = rect.centerx
        elif anchor == 'right':
            rect.right = rect.centerx
        elif anchor == 'br':
            rect.bottom = rect.centery
            rect.right = rect.centerx
            
    if hitboxes:
        pygame.draw.rect(screen,(255,0,0),rect,2)
    
    screen.blit(image,rect)
    
    return rect

def rot_center(image,angle,x,y):
    if angle != 0:
        rotated_image = pygame.transform.rotate(image,-angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x,y)).center)
    return rotated_image,new_rect

def scale(image,size):
    image = pygame.transform.scale(image,(image.get_width()*size,image.get_height()*size))
    return image

def smooth(value,target,easing):
    value += (target-value)/easing
    if abs(target-value) <= 0.01*easing:
        value = target
    return value

def update_keys():
    global key
    key = pygame.key.get_pressed()

def update_key_pressed():
    global key,key_pressed
    if any(key):
        key_pressed = True
    else:
        key_pressed = False

def update_mouse():
    global mouse_pos,mouse_click
    mouse_pos = list(pygame.mouse.get_pos())
    mouse_click = pygame.mouse.get_pressed()

def update_clicked():
    global mouse_click,mouse_clicked
    if mouse_click[0]:
        mouse_clicked = True
    else:
        mouse_clicked = False

def check_click(rect):
    global mouse_pos,mouse_click,mouse_clicked
    
    if rect.collidepoint(mouse_pos) and mouse_click[0] and not mouse_clicked:
        return True
    else:
        return False

def show_fps():
    text = font.render(f'{round(fps)}',True,(0,0,0))
    display_image(text,(-480,300),0.6,anchor='left')
    
    count = 0
    for i in sprites.keys():
        count += len(i)
    
    pixels = 0
    for i in sprites.keys():
        for image in sprites[i]:
            pixels += image.get_width()*image.get_height()
    
    text = font.render(f'{count} IMAGES IN MEMORY ({pixels} PIXELS)',True,(0,0,0))
    
    display_image(text,(-400,300),0.6,anchor='left')

def play_sound(name):
    global sounds
    pygame.mixer.Sound.play(sounds[name])

def play_music(name,pos=0):
    global music,music_pos
    music_pos = pos
    pygame.mixer.music.load(music[name])
    pygame.mixer.music.play(start=pos)

def stop_music():
    pygame.mixer.music.stop()

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()

def update_volume(value=-1):
    global global_volume,music_volume
    
    if value >= 0:
        music_volume = value
    pygame.mixer.music.set_volume(music_volume*global_volume)

#play other version of music with same position
def replace_music(name,offset=0):
    global music,music_pos
    pos = pygame.mixer.music.get_pos()/1000+music_pos+offset
    play_music(name,pos)

def load_sprites(folders):
    global sprites
    for folder in folders:
        sprites[folder] = []
        names = os.listdir(f'Sprites/{folder}')
        for name in names:
            sprites[folder].append(pygame.image.load(f'Sprites/{folder}/{name}').convert_alpha())

def unload_sprites(folders):
    global sprites
    for name in folders:
        del sprites[name]

music_pos = 0

global_volume = 1
music_volume = 1

import os

#sprites
sprite_folders = os.listdir('Sprites')

sprites = {}

load_sprites(['intro','button'])

#sounds
pygame.mixer.init()

pygame.mixer.set_num_channels(20)

sounds = {}

for file in os.listdir('Sounds'):
    sounds[file[:-4]] = pygame.mixer.Sound(f'Sounds/{file}')

for key in sounds.keys():
    sounds[key].set_volume(0.6)

sounds['click'].set_volume(0.4)
sounds['switch'].set_volume(0.3)
sounds['clang'].set_volume(0.3)
sounds['pop2'].set_volume(0.8)
sounds['pop2'].set_volume(0.8)
sounds['bonk'].set_volume(0.3)

#music
music = {}

for file in os.listdir('Music'):
    music[file[:-4]] = f'Music/{file}'

b = (107,255,175)

b_sizes = [global_scale for i in sprites['button']]
b_time = [0 for i in sprites['button']]

#scripts
scripts = {}
for i in os.listdir('Scripts'):
    scripts[i] = compile(open(f'Scripts/{i}').read(),f'Scripts/{i}','exec')

mode = 'intro'

theme_music = ['snap along','jazz in paris','the duel','elevator','crazy daze','christmas jazz']
theme_names = ['ORIGINAL','PARIS','WILD WEST','LSD','OFFICE','CHRISTMAS']

#keyframes
keyframes = []
for k in range(3):
    for i in range(10):
        keyframes.append(k)
for i in range(10):
    keyframes.append(2)

for k in range(6):
    for i in range(10):
        if k%2 == 0:
            keyframes.append(3)
        else:
            keyframes.append(4)

for k in range(6):
    for i in range(10):
        keyframes.append(k+5)

#font
pygame.font.init()
font = pygame.font.Font('zepto.ttf',80)

#initialize variables
menu_pos = [0,0]
menu_size = global_scale+2 
mouse_pos = [0,0]
mouse_click = [0,0]
frame = 0
frame2 = 0
time = 0
opacity = 0

kill_effects = [0,5,6,9,11,20]
kill_effect_length = [5,1,3,2,9,1]
kill_loop = [0,0,1,0,0,0]
kill_time = [10,30,10,20,8,30]
kill_sound = ['chirp','error',False,'pop','oof','skull']

bought = [1,0,0,0,0,0]
cost = [0,20,30,100,200,500]

total_money = 0
score = 0
high_score = 0

theme = 0

option_button_size = 6

skin_pos = [(0,0),(25,15),(0,-55),(10,5),(0,0),(-5,-40)]

#transparent surface
transparent_surf = pygame.Surface(res,pygame.SRCALPHA,32)
transparent_surf.fill((0,0,0))

focus = True

key_pressed = False

#load progress
with open('Info','rb') as file:
    info = file.read()

exec(info)

print()
info = str(info).split('\n')
for i in info:
    print(i)

time2 = t()

print('load time:',time2-time1)

update_volume(0.3)
play_music('elevator muffled')

while True:
    checkExit()
    
    fps = clock.get_fps()
    
    update_mouse()
    update_keys()
    
    if mode in scripts:
        exec(scripts[mode])
    else:
        screen.fill((200,100,100))
        text = font.render('SCRIPT NOT FOUND',True,(150,50,50))
        display_image(text,(0,0),1)

    if hitboxes:
        show_fps()
    
    if key[pygame.K_r] and not key_pressed:
        time1 = t()
        #scripts
        scripts = {}
        for i in os.listdir('Scripts'):
            scripts[i] = compile(open(f'Scripts/{i}').read(),f'Scripts/{i}','exec')
        time2 = t()
        print('script load time:',time2-time1)
    
    if key[pygame.K_i] and not key_pressed:
        time1 = t()
        #sprites
        sprite_folders = os.listdir('Sprites')

        sprites = {}

        load_sprites(sprite_folders)
        
        time2 = t()
        print('image load time:',time2-time1)
    
    
    update_clicked()
    update_key_pressed()
    
    pygame.display.update()
    clock.tick(60)