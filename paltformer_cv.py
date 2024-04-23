import pygame
import cv2
import numpy as np
import mediapipe as mp
import random

#human pose
mpPose=mp.solutions.pose
pose=mpPose.Pose()
mpDraw=mp.solutions.drawing_utils

#initialize
pygame.init()

#create window/display
width,height=1000,1000
window=pygame.display.set_mode((width,height))
pygame.display.set_caption("PLATFORMER")

#split
p1_camera = pygame.Rect(0,0,500,1000)
p2_camera = pygame.Rect(500,0,500,1000)


run = True

#Load Images
ghost_img = pygame.image.load('ghost.png')
bee_img = pygame.image.load("bee_fly.png")
bat_img = pygame.image.load("bat.png")
fly_img = pygame.image.load("fly.png")
barnacle_img = pygame.image.load("barnacle.png")
slime_img = pygame.image.load("slimeBlock.png")
bg_img = pygame.image.load('sky.png')

rect_ghost = ghost_img.get_rect()
rect_bee = bee_img.get_rect()
rect_bat = bat_img.get_rect()
rect_fly = fly_img.get_rect()
rect_barnacle = barnacle_img.get_rect()
rect_slime = slime_img.get_rect()



enemy = [bee_img,bat_img,fly_img,barnacle_img,slime_img]
enemy_rects = [rect_bee,rect_bat,rect_fly,rect_barnacle,rect_slime]


#camera
cap=cv2.VideoCapture(0)
cap.set(3,1000)
cap.set(4,1000)

def resetEnemy():
    global enemy , enemy_chosing , enemy_rects , path_chosing

    enemy_chosing = random.randint(0,4)
    enemy_chosing = int(enemy_chosing)

    path_chosing = random.randint(0,2)
    path_chosing = int(path_chosing)

    if path_chosing == 0:
        enemy_rects[enemy_chosing].x = 70
        enemy_rects[enemy_chosing].y = 0

    elif path_chosing == 1:
        enemy_rects[enemy_chosing].x = 240
        enemy_rects[enemy_chosing].y = 0
    
    elif path_chosing == 2:
        enemy_rects[enemy_chosing].x = 400
        enemy_rects[enemy_chosing].y = 0





lmList1=[]

#main loop
start=True
temp=0
a=True
b=True



while start:

    t=False

    lmList=[]

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            start=False
            pygame.quit()
    
    _,img=cap.read()

    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=pose.process(imgRGB)

    if a == True:
        enemy_chosing = random.randint(0,4)
        enemy_chosing = int(enemy_chosing)

        path_chosing = random.randint(0,2)
        path_chosing = int(path_chosing)

        a=False

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        for id,lm in enumerate(results.pose_landmarks.landmark):
            
            h , w , c = img.shape
            cx , cy = int(lm.x*w) , int(lm.y*h)
            lmList.append([id,cx,cy])
    

    if len(lmList) != 0:
        x , y = lmList[0][1] , lmList[0][2]
        x = np.interp(x,[0,1240],[1280,0])
        x = int(x)
        y = np.interp(y,[0,720],[-20,640])
        y = int(y)
        rect_ghost.x , rect_ghost.y = x-500 , y+200

       
        if enemy_rects[enemy_chosing].collidepoint(x-500,y+200):
            resetEnemy() 

        enemy_rects[enemy_chosing].y = enemy_rects[enemy_chosing].y + 5

        
    

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()

    
    window.blit(bg_img,(0, 0), p1_camera)
    window.blit(ghost_img,rect_ghost,p1_camera)
    window.blit(enemy[enemy_chosing],enemy_rects[enemy_chosing],p1_camera)

    window.blit(frame, (500, 0), p2_camera)
    #Update Display
    pygame.display.update()