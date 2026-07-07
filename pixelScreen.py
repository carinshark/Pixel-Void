from PIL import Image
import pygame
import numpy as np

from simpleUtility import SimpleUtility


#colors
background = np.array((0,0,0))
blank= np.array((255,255,255),dtype="uint8")

#adjustable parameters
square_size=3
line_width=1
grid_size=(20,20)

#storing of line data
#odd values on the last row are irrelevant.
grid_data=np.full((grid_size[0]*2+1,grid_size[1]+1,3),blank,dtype="uint8")

#this converts it into visual pixels based on the parameters given
#THIS PART SPECIFICALLY IS COLUMN MAJOR RATHER THAN ROW MAJOR
image_data=np.full((square_size*grid_size[1]+line_width*(grid_size[1]+1),
                    square_size*grid_size[0]+line_width*(grid_size[0]+1)
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

img = Image.fromarray(image_data)

img=img.resize((500,500),resample=Image.Resampling.NEAREST)

pygame.init()

canvas = pygame.display.set_mode((500,500))

pygame.display.set_caption("Pixel Void")
exit = False
is_drawing=False
imageTexture=pygame.image.frombytes(img.tobytes(),(500,500),"RGB")

draw_location = (0,0)
brush_size=10

while not exit:
    canvas.fill(background)
    
    

    canvas.blit(imageTexture)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit=True
        elif event.type==pygame.MOUSEBUTTONUP:
            is_drawing=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            is_drawing=True
        elif event.type==pygame.MOUSEMOTION:
            draw_location=event.pos
        elif event.type==pygame.MOUSEWHEEL:
            brush_size+=event.y
            brush_size=SimpleUtility.limit(brush_size,4,40)
            

    pygame.draw.circle(canvas,blank,draw_location,brush_size,width=2)

        
    pygame.display.update()

