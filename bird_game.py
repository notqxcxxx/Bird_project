import pygame
import pyganim
import sys
import os
import ast

pygame.init()

SAVE_FILE = 'bird_game/level0.txt'
SAVE_FILE_R = 'bird_game/level_r0.txt'
SAVE_FILE_B = 'bird_game/level_b0.txt'
SAVE_FILE_T = 'bird_game/level_t0.txt'
SAVE_FILE_S = 'bird_game/level_s0.txt'

WIDTH, HEIGHT = 640, 640 #320, 4256
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

WHITE = (255,255,255)
BLUE = (80,180,255)
GREEN = (70,200,70)
RED = (255, 0 ,0)
BROWN = (140,90,40)

plat_color = [RED, GREEN, BLUE]

firstx_coor = -1
firsty_coor = -1
secondx_coor = -1
secondy_coor = -1

GRAVITY = 0.8
PLAYER_SPEED = 6
JUMP_SPEED = -16
jumps = 2
jump = False
space_time = 0
setka = False

frame = 0
anim_timer = 0
anim_delay = 100

sky_images = []
#-----------------BIRD------------------------
bird = pygame.image.load("bird_game/bird/bird.png").convert_alpha()
bird = pygame.transform.scale(bird, (64, 64))
bird_f = pygame.transform.flip(bird,True, False)
bird_hit = pygame.image.load("bird_game/bird/bird_hit.png").convert_alpha()
bird_hit = pygame.transform.scale(bird_hit, (64, 64))
bird_hit_f = pygame.transform.flip(bird_hit,True, False)
bird_jump = pygame.image.load("bird_game/bird/bird_jump.png").convert_alpha()
bird_jump = pygame.transform.scale(bird_jump, (64, 64))
bird_jump_f = pygame.transform.flip(bird_jump,True, False)
bird_lay = pygame.image.load("bird_game/bird/bird_lay.png").convert_alpha()
bird_lay = pygame.transform.scale(bird_lay, (64, 64))
bird_lay_f = pygame.transform.flip(bird_lay,True, False)
bird_walk = pygame.image.load("bird_game/bird/bird_walk.png").convert_alpha()
bird_walk = pygame.transform.scale(bird_walk, (64, 64))
bird_walk_f = pygame.transform.flip(bird_walk,True, False)

bird_images = [bird, bird_hit, bird_jump, bird_lay, bird_walk]
bird_images_f = [bird_f, bird_hit_f, bird_jump_f, bird_lay_f, bird_walk_f]

bird_stay = [bird, bird_f]
bird_walks = [bird_walk, bird_walk_f]
bird_jumps = [bird_jump, bird_jump_f]
bird_hits = [bird_hit, bird_hit_f]
bird_lays = [bird_lay, bird_lay_f]

birds = [bird_stay, bird_walks, bird_jumps, bird_hits, bird_lays]

bird_img = bird_images[0]
bird_dir = 1
#-----------------HITBOX----------------------
road = pygame.image.load("bird_game/hitbox_textures/road.png").convert_alpha()
road = pygame.transform.scale(road, (640, 192))
roof1 = pygame.image.load("bird_game/hitbox_textures/roof1.png").convert_alpha()
roof1 = pygame.transform.scale(roof1, (64, 64))
roof1_f = pygame.transform.flip(roof1,True, False)
roof2 = pygame.image.load("bird_game/hitbox_textures/roof2.png").convert_alpha()
roof2 = pygame.transform.scale(roof2, (128, 64))
roof2_f = pygame.transform.flip(roof2,True, False) 
roof3 = pygame.image.load("bird_game/hitbox_textures/roof3.png").convert_alpha()
roof3 = pygame.transform.scale(roof3, (192, 64))
roof3_f = pygame.transform.flip(roof3,True, False)
sakura = pygame.image.load("bird_game/hitbox_textures/sakura.png").convert_alpha()
sakura = pygame.transform.scale(sakura, (320, 320))
sakura_f = pygame.transform.flip(sakura,True, False)
spike_up = pygame.image.load("bird_game/hitbox_textures/spike.png").convert_alpha()
spike_up = pygame.transform.scale(spike_up, (64, 64))
spike_right = pygame.transform.rotate(spike_up, -90)
spike_down = pygame.transform.rotate(spike_up, -180)
spike_left = pygame.transform.rotate(spike_up, 90)
windowsill = pygame.image.load("bird_game/hitbox_textures/windowsill.png").convert_alpha()
windowsill = pygame.transform.scale(windowsill, (192, 64))
roof_img = [roof1, roof2, roof3, roof3_f, roof2_f, roof1_f]
plat_img = [roof_img, windowsill]
spike_img = [spike_up, spike_right, spike_down, spike_left]
#-----------------HOUSE-----------------------
wall = pygame.image.load("bird_game/house_textures/wall.png").convert_alpha()
wall = pygame.transform.scale(wall, (64, 64))
wood_wall = pygame.image.load("bird_game/house_textures/wood_wall.png").convert_alpha()
wood_wall = pygame.transform.scale(wood_wall, (64, 64))
window = pygame.image.load("bird_game/house_textures/window.png").convert_alpha()
window = pygame.transform.scale(window, (64, 64))
back_img = [wall, window]
#-----------------SKY-------------------------
for i in range(12):
    sky_images.append(pygame.image.load(f"bird_game/sky_textures/sky{i+1}.png").convert_alpha())
    sky_images[i] = pygame.transform.scale(sky_images[i], (640, 640))
    #print(sky_images)

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(20,100,36,60)
        self.vel_y = 0
        self.double_jump = False
        self.jump_from_ground = False
        self.jumps = jumps
        self.bird_img = bird_img
        self.bird_dir = bird_dir
        self.jump = jump
        self.anim = pyganim.PygAnimation([
        ('bird_game/bird/anim/frame1.png', 300),
        ('bird_game/bird/anim/frame2.png', 300),
        ])
        self.anim_jump = pyganim.PygAnimation([
        ('bird_game/bird/anim/frame1.png', 100),
        ('bird_game/bird/anim/frame3.png', 100),
        ])
        self.anim.scale((64,64))
        self.anim_jump.scale((64,64))
        self.anim.play()
        self.how_many_pl = 0

    def update(self, platforms, editor_mode = 0):
        #global bird_dir, jump
        
        keys = pygame.key.get_pressed()

        dx = 0

        def jumpanim(spr):
            if abs(spr) == 5:
                #walk
                self.bird_img = bird_images[spr]
                return self.bird_img

        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
            self.bird_dir = 0
            #self.bird_img = jumpanim(5)
        if keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
            self.bird_dir = 1
            #self.bird_img = jumpanim(-5)
        if editor_mode != 0:
            self.vel_y = 0
            if keys[pygame.K_DOWN]:
                self.rect.y -= JUMP_SPEED
            if keys[pygame.K_UP]:
                self.rect.y += JUMP_SPEED



        # горизонтальний рух
        self.rect.x += dx

        for p in platforms:
            p = pygame.Rect(p[:4])
            if self.rect.colliderect(p):
                self.jump = False
                if dx > 0:
                    self.rect.right = p.left
                if dx < 0:
                    self.rect.left = p.right

        # гравітація
        if editor_mode == 0:
            self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        for p in platforms:
            p = pygame.Rect(p[:4])
            if self.rect.colliderect(p):
                if self.how_many_pl > 0:
                    self.how_many_pl =- 1
                else:    
                    #jumps = 2
                    self.jump = False
                    if self.vel_y >= 0:
                        player.jumps = 2
                        self.rect.bottom = p.top
                        self.vel_y = 0

                    elif self.vel_y < 0:
                        self.rect.top = p.bottom
                        self.vel_y = 0

        for p in roofs:
            p = pygame.Rect(p[:4])
            if self.rect.colliderect(p):
                #jumps = 2
                self.jump = False

                if self.vel_y >= 0:
                    player.jumps = 2
                    self.rect.bottom = p.top
                    self.vel_y = 0

                elif self.vel_y < 0:
                    self.rect.top = p.bottom
                    self.vel_y = 0  
                          


    def draw(self, surface, camera_x, camera_y):
        pygame.draw.rect(surface, BLUE,
                         (self.rect.x,#-camera_x,
                          self.rect.y-camera_y,
                          self.rect.width,
                          self.rect.height))
        if self.jump == True:
            self.anim.pause()
            self.anim_jump.play()
            self.anim_jump.blit(surface, (self.rect.x-20, self.rect.y-camera_y-4))
            #self.bird_img = bird_jumps[self.bird_dir]
        else:
            self.anim_jump.pause()
            self.anim.play()
            self.anim.blit(surface, (self.rect.x-8, self.rect.y-camera_y-4))

            #self.bird_img = birds[0][self.bird_dir]

        #if self.bird_dir == 0:
            #screen.blit(self.bird_img, (self.rect.x-20, self.rect.y-camera_y-4))
        #    self.anim.blit(surface, (self.rect.x-20, self.rect.y-camera_y-4))
        #else:
            #screen.blit(self.bird_img, (self.rect.x-8, self.rect.y-camera_y-4))
        #    self.anim.blit(surface, (self.rect.x-8, self.rect.y-camera_y-4))
        #self.anim.blit(surface, self.rect)


def point_in_triangle(pt, v1, v2, v3):
    """Перевіряє, чи лежить точка pt (x, y) всередині трикутника (v1, v2, v3)."""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)


def save_map(list_rect, list_roofs, list_back, list_triangle, list_spikes):
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        for rect in list_rect:
            file.write(str([rect.x, rect.y, rect.width, rect.height]))
    with open(SAVE_FILE_R, "w", encoding="utf-8") as file:
        for rect in list_roofs:
            file.write(str(rect))
    with open(SAVE_FILE_B, "w", encoding="utf-8") as file:
        for rect in list_back:
            file.write(str(rect))
            #file.write(str([rect.x, rect.y, rect.width, rect.height]))
    with open(SAVE_FILE_T, "w", encoding="utf-8") as file:
        for tri in list_triangle:
            file.write(str(tri))
    with open(SAVE_FILE_S, "w", encoding="utf-8") as file:
            for tri in list_spikes:
                file.write(str(rect))


def load_map(level_file, level_file_r, level_file_b, level_file_t, level_file_s):
    '''
    level_file - platforms
    level_file_r - roof
    level_file_b - fon for lvl
    level_file_t - traangles
     

    '''
    platforms = []
    roofs = []
    l_back = []
    triangle = []
    spikes = []
    file_error = False
    if not os.path.exists(level_file):
        print("Файл збереження не знайдено")
        file_error = True
    if not os.path.exists(level_file_r):
        print("Файл збереження не знайдено")
        file_error = True
    if not os.path.exists(level_file_b):
        print("Файл збереження не знайдено")
        file_error = True
    if not os.path.exists(level_file_t):
        print("Файл збереження не знайдено")
        file_error = True
    if not os.path.exists(level_file_s):
            print("Файл збереження не знайдено")
            file_error = True
    if file_error:
        return platforms, roofs, l_back, triangle, spikes

    with open(level_file, "r", encoding="utf-8") as file:
        data = file.read()
        result = ast.literal_eval("[" + data.replace("][", "],[") + "]")
        for i in result:
            platforms.append(                
                    pygame.Rect(i)
                )
    with open(level_file_r, "r", encoding="utf-8") as file:
        data = file.read()
        result = ast.literal_eval("[" + data.replace("][", "],[") + "]")
        for i in result:
            roofs.append(i)
            
    with open(level_file_b, "r", encoding="utf-8") as file:
        data = file.read()
        result = ast.literal_eval("[" + data.replace("][", "],[") + "]")
        for i in result:
            l_back.append(i)
    with open(level_file_t, "r", encoding="utf-8") as file:
        data = file.read()
        result = ast.literal_eval("[" + data.replace("][", "],[") + "]")
        for i in result:
            triangle.append(i)
    with open(level_file_s, "r", encoding="utf-8") as file:
            data = file.read()
            result = ast.literal_eval("[" + data.replace("][", "],[") + "]")
            for i in result:
                spikes.append(i)

    return platforms, roofs, l_back, triangle, spikes

def add_platform(platforms, firstx_coor, y_draw, plat_size):
    platforms.append(pygame.Rect(firstx_coor*64,y_draw*64,plat_size*64,32))

def destroy_obj(x, y):
    y = y - 32
    for p in roofs:
        if pygame.Rect(p[:4]).collidepoint(x, y):
            roofs.remove(p)
    for p in platforms:
        if p.collidepoint(x, y):
            platforms.remove(p)
    for p in platforms_back:
        if pygame.Rect(p[:4]).collidepoint(x, y):
            platforms_back.remove(p)
    '''
    for p in triangle:
        pt = (x, y)
        v1, v2, v3 = p
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        d1 = sign(pt, v1, v2)
        d2 = sign(pt, v2, v3)
        d3 = sign(pt, v3, v1)
        has_neg = d1 < 0 or d2 < 0 or d3 < 0
        has_pos = d1 > 0 or d2 > 0 or d3 > 0
        return not (has_neg and has_pos)
    '''


player = Player()

# Карта
platforms, roofs, platforms_back, triangle, spikes = load_map(SAVE_FILE, SAVE_FILE_R, SAVE_FILE_B, SAVE_FILE_T, SAVE_FILE_S)

if len(platforms) ==0:
    # Земля
    for i in range(50):
        platforms.append(
            pygame.Rect(i*100,540,100,60)
        )
    # Платформи
    platforms.extend([
        pygame.Rect(300,450,200,20),
        pygame.Rect(650,370,180,20),
        pygame.Rect(1000,300,200,20),
        pygame.Rect(1450,430,200,20),
        pygame.Rect(1900,340,180,20),
        pygame.Rect(2300,250,220,20),
    ])

camera_x = 0

running = True
editor_mode = 0



while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
            editor_mode = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            setka = not setka
        if event.type == pygame.KEYDOWN and pygame.K_1 <= event.key <= pygame.K_9:
            editor_mode = event.key - pygame.K_0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            print(pygame.mouse.get_pos() ,camera_y)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and editor_mode != 0:
            xx, yy = pygame.mouse.get_pos()
            destroy_obj(xx, yy+camera_y)
            firstx_coor = -1
            firsty_coor = -1
            secondx_coor = -1
            secondy_coor = -1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if player.jumps != 0:
                player.jump = True
                player.vel_y = 0 
                player.vel_y += JUMP_SPEED
                player.jumps = player.jumps-1
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if player.vel_y < 0:
                player.vel_y = -4
            #if not player.jump_from_ground:
            #    if not player.double_jump:
            #        player.vel_y += JUMP_SPEED
            #    if player.vel_y == 0:
            #       player.jump_from_ground = True
            #else:
                #player.jump_from_ground = False
                #if not player.double_jump:
                #    player.double_jump = True
                #    player.vel_y += JUMP_SPEED
                #else:    
                #    player.double_jump = False


        #if editor_mode and event.type == pygame.MOUSEBUTTONUP:
        #    x, y = pygame.mouse.get_pos()
        #    x_draw = x // 64
        #    y_draw = (y+player.rect.centery - HEIGHT//2) // 64
            #print(x_draw*64,y_draw*64)
        if editor_mode != 0 and event.type == pygame.MOUSEBUTTONDOWN:
            if firstx_coor == -1:
                x, y = pygame.mouse.get_pos()
                firstx_coor = x // 64
                firsty_coor = (y+player.rect.centery - HEIGHT//2) // 64
            else:
                x, y = pygame.mouse.get_pos()
                secondx_coor = x // 64
                secondy_coor = (y+player.rect.centery - HEIGHT//2) // 64

                x_size = secondx_coor - firstx_coor + 1
                if x_size > 3:
                    x_size = 3
                plat_dir = x_size-1
                if x_size < 1 and editor_mode == 1:
                    plat_dir = x_size-1
                    x_size = abs(x_size)+1
                if x_size > 3:
                    x_size = 3

                y_size = secondy_coor - firsty_coor + 1
        
            if editor_mode == 1 and secondx_coor != -1:
                """Намалювати платформу"""
                if event.button == 1:
                    minus = 0
                    if plat_dir < 0:
                        minus = x_size*64
                    roofs.append([firstx_coor*64-minus, firsty_coor*64, x_size*64, 32, plat_dir, 32])
                    if plat_dir > -1:
                        platforms.append(pygame.Rect(firstx_coor*64,firsty_coor*64,x_size*64,32))
                    else:
                        platforms.append(pygame.Rect(firstx_coor*64-x_size*64,firsty_coor*64,x_size*64,32))
                    firstx_coor = -1
                    firsty_coor = -1
                    secondx_coor = -1
                    secondy_coor = -1

                elif event.button == 2:
                    print(len(platforms))
                    for i in platforms:
                        if i.x == firstx_coor*64 and i.y == firsty_coor*64:
                            print(i)
                            platforms.remove(i)
                            firstx_coor = -1
                            firsty_coor = -1
                            secondx_coor = -1
                            secondy_coor = -1

            elif editor_mode == 2 and secondx_coor != -1:
                firstx_coor *= 64
                firsty_coor *= 64

                if abs(firstx_coor - secondx_coor*64)<64:
                    """up or down"""
                    if firsty_coor > secondy_coor*64:
                        coor1 = [firstx_coor+32,firsty_coor-32]
                        coor2 = [firstx_coor,firsty_coor+32]
                        coor3 = [firstx_coor+64,firsty_coor+32]
                        spikes.append([firstx_coor, firsty_coor, 1, 1, 0])
                    else:
                        coor1 = [firstx_coor+32,firsty_coor+32]
                        coor2 = [firstx_coor,firsty_coor-32]
                        coor3 = [firstx_coor+64,firsty_coor-32]
                        spikes.append([firstx_coor, firsty_coor, 1, 1, 2])
                else:
                    """left or right"""
                    if firstx_coor > secondx_coor*64:
                        coor1 = [firstx_coor,firsty_coor]
                        coor2 = [firstx_coor+64,firsty_coor-32]
                        coor3 = [firstx_coor+64,firsty_coor+32]
                        spikes.append([firstx_coor, firsty_coor, 1, 1, 3])
                    else:
                        coor1 = [firstx_coor+64,firsty_coor]
                        coor2 = [firstx_coor,firsty_coor-32]
                        coor3 = [firstx_coor,firsty_coor+32]
                        spikes.append([firstx_coor, firsty_coor, 1, 1, 1])
                    
                triangle.append([coor1, coor2, coor3])
                firstx_coor = -1
                firsty_coor = -1
                secondx_coor = -1
                secondy_coor = -1
        
        
                
            elif editor_mode == 3:
                if event.button == 1:
                    platforms_back.append([firstx_coor*64,firsty_coor*64, 64, 64, 0])
                    #platforms_back.append(pygame.Rect(firstx_coor*64,firsty_coor*64, 64, 64))
                    firstx_coor = -1
                    firsty_coor = -1
                    secondx_coor = -1
                    secondy_coor = -1

                elif event.button == 2:
                    for i in platforms_back:
                        if i.x == firstx_coor*64 and i.y == firsty_coor*64:
                            print(i)
                            platforms_back.remove(i)
                            firstx_coor = -1
                            firsty_coor = -1
                            secondx_coor = -1
                            secondy_coor = -1
            elif editor_mode == 4:
                if event.button == 1:
                    platforms_back.append([firstx_coor*64,firsty_coor*64, 64, 64, 1])
                    #platforms_back.append(pygame.Rect(firstx_coor*64,firsty_coor*64, 64, 64))
                    firstx_coor = -1
                    firsty_coor = -1
                    secondx_coor = -1
                    secondy_coor = -1

                elif event.button == 2:
                    for i in platforms_back:
                        if i.x == firstx_coor*64 and i.y == firsty_coor*64:
                            print(i)
                            platforms_back.remove(i)
                            firstx_coor = -1
                            firsty_coor = -1
                            secondx_coor = -1
                            secondy_coor = -1

            elif editor_mode == 5:
                if event.button == 1:
                    roofs.append([firstx_coor*64-64,firsty_coor*64-32, 192, 32, 0, 0])
                    platforms.append(pygame.Rect(firstx_coor*64-64,firsty_coor*64-32, 192, 32))
                    firstx_coor = -1
                    firsty_coor = -1
                    secondx_coor = -1
                    secondy_coor = -1

                elif event.button == 2:
                    for i in platforms:
                        if i.x == firstx_coor*64-64 and i.y == firsty_coor*64-32:
                            print(i)
                            platforms.remove(i)
                            firstx_coor = -1
                            firsty_coor = -1
                            secondx_coor = -1
                            secondy_coor = -1
            elif editor_mode == 6:
                if event.button == 1:
                    platforms.append(pygame.Rect(firstx_coor*64, firsty_coor*64-32, 64, 32))
                    firstx_coor = -1
                    firsty_coor = -1
                    secondx_coor = -1
                    secondy_coor = -1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
            editor_mode = False
            save_map(platforms, roofs, platforms_back, triangle, spikes)
        
            

    player.update(platforms,editor_mode)

    # ---------------------------
    # КАМЕРА
    # ---------------------------
    camera_x = player.rect.centerx - WIDTH//2
    camera_y = player.rect.centery - HEIGHT//2

    if camera_x < 0:
        camera_x = 0
    if camera_y > 320:
        camera_y = 320
    #print(camera_y)

    screen.fill(WHITE)
    # Малюємо платформи

    a = []
    for x in range(10):
        for y in range(200):
    
            a.append(pygame.Rect(
                    x * 64,
                    y * -64+960-camera_y,
                    64,
                    64
                ))

    screen.blit(road, (0, 448+320-camera_y))
    
    for p in range(12):

        b = p*640+320
            
        screen.blit(sky_images[p], (0,#camera_x-20, 
                                448-b-camera_y))
    
    if setka:
        for p in a:
            pygame.draw.rect(screen, BLUE, p, 1)
    
    for p in platforms:
        pygame.draw.rect(
            screen,
            GREEN,
            (p[0],
            p[1]-camera_y+32,
            p[2],
            p[3])
        )
    for p in roofs:    
        if len(p) > 4:
            if p[5] == 32:
                screen.blit(roof_img[p[4]], (p[0],#camera_x-20, 
                                        p[1]-camera_y))
            else:
                screen.blit(windowsill, (p[0],#camera_x-20, 
                                        p[1]-camera_y+32))
                                        
    for p in platforms_back:
            
        screen.blit(back_img[p[4]], (p[0],#camera_x-20, 
                                p[1]-camera_y))
            
    for tria in triangle:
        cam_tria = [[tria[0][0], tria[0][1] -camera_y+32],
        [tria[1][0], tria[1][1] -camera_y+32],
        [tria[2][0], tria[2][1] -camera_y+32]]
        pygame.draw.polygon(screen, RED, cam_tria)

    for p in spikes:
                
        screen.blit(spike_img[p[4]], (p[0],#camera_x-20, 
                                    p[1]-camera_y))


    player.draw(screen, camera_x, camera_y-32)

    pygame.display.flip()
    

pygame.quit()
sys.exit()

