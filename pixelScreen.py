from PIL import Image
import pygame
import numpy as np
from math import ceil,floor
from simpleUtility import SimpleUtility


#colors
background = np.array((0,0,0))
blank= np.array((255,255,255),dtype="uint8")

#adjustable parameters
square_size=3
line_width=1
grid_size=10
canvas_size=500

step=line_width+square_size

resolution=(grid_size*step+line_width)

grid_scale=canvas_size/resolution

#returns 
def pixel_to_point(p):
    return (int((p[0]//grid_scale)),int((p[1]//grid_scale)))

#storing of line data
#odd values on the last row are irrelevant.
grid_data=np.full((grid_size*2+1,grid_size+1,3),blank,dtype="uint8")

#this converts it into visual pixels based on the parameters given
#THIS PART SPECIFICALLY IS COLUMN MAJOR RATHER THAN ROW MAJOR
image_data=np.full((resolution,
                    resolution
                    ,3),background,dtype="uint8")


#horizontal lines
for r in range(1,len(grid_data),2):
    for c in range(0,len(grid_data[0])):
        x=((r-1)//2)*(square_size+line_width)+line_width
        y=(square_size+line_width)*c
        for i in range(square_size):
            for j in range(line_width):
                image_data[y+j,x+i]=grid_data[r][c]

#vertical lines
for r in range(0,len(grid_data),2):
    for c in range(0,len(grid_data[0])-1):
        x=(r//2)*(square_size+line_width)
        y=c*(square_size+line_width)+line_width
        for i in range(line_width):
            for j in range(square_size):
                image_data[y+j,x+i]=grid_data[r][c]

#this replaces it with random colored pixels (for testing)
# image_data=(np.random.rand(9,9,3)*255).astype(np.uint8)


pygame.init()

canvas = pygame.display.set_mode((canvas_size,canvas_size))

pygame.display.set_caption("Pixel Void")
exit = False
is_drawing=False

draw_location = (0,0)
brush_size=1

while not exit:
    canvas.fill(background)

    img = Image.fromarray(image_data)

    img=img.resize((canvas_size,canvas_size),resample=Image.Resampling.NEAREST)

    imageTexture=pygame.image.frombytes(img.tobytes(),(canvas_size,canvas_size),"RGB")


    canvas.blit(imageTexture)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit=True
        elif event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit=True
        elif event.type==pygame.MOUSEBUTTONUP:
            if event.button==pygame.BUTTON_LEFT:
                is_drawing=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==pygame.BUTTON_LEFT:
                is_drawing=True

        elif event.type==pygame.MOUSEMOTION:
            draw_location=event.pos
        elif event.type==pygame.MOUSEWHEEL: 
            brush_size+=event.y/2
            brush_size=SimpleUtility.limit(brush_size,.5,grid_size*2+1)
            
    if is_drawing:
        point = pixel_to_point(draw_location)
        # point=(point[0]*2//step/2,point[1]*2//step/2)
        # print(point)

        brush_box=((point[0]-brush_size,point[0]+brush_size),(point[1]-brush_size,point[1]+brush_size))

        # if 0 in [point[0]%step,point[1]%step]:
        #     print("point!")
        
        

        #limit brush to edge of canvas
        brush_box= SimpleUtility.limit(brush_box,0,resolution)
        
        #align to grid
        brush_box = ((floor(brush_box[0][0]/step)*step,ceil(brush_box[0][1]/step)*step),
                     (floor(brush_box[1][0]/step)*step,ceil(brush_box[1][1]/step)*step))

        print(brush_box)


        #for testing purposes, it creates points at the furthest ones
        brush_points=[]
        for i in [(0,0),(0,1),(1,1),(1,0)]:
            pygame.draw.circle(canvas,(0,0,255),(brush_box[0][i[0]]*grid_scale,brush_box[1][i[1]]*grid_scale),10)
                




    pygame.draw.circle(canvas,(0,0,255),draw_location,brush_size*grid_scale,width=5)

        
    pygame.display.update()


