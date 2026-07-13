from PIL import Image
import pygame
import numpy as np
from math import ceil,floor,dist
from simpleUtility import SimpleUtility
from appSettings import AppSettings


settings = AppSettings()

#colors
background = settings.background
blank= settings.blank

#adjustable parameters
square_size=settings.square_size
line_width=settings.line_width
grid_size=settings.grid_size
canvas_size=settings.canvas_size


#calculated variables (not for changing)
step=line_width+square_size
resolution=(grid_size*step+line_width)
grid_scale=canvas_size/resolution

canvas_offset=(settings.margin,settings.margin)




#storing of line data
#odd values on the last row are irrelevant.
grid_data=np.full((grid_size*2+1,grid_size+1,3),background,dtype="uint8")

#this converts it into visual pixels based on the parameters given
#THIS PART SPECIFICALLY IS COLUMN MAJOR RATHER THAN ROW MAJOR
image_data=np.full((resolution,
                    resolution
                    ,3),background,dtype="uint8")



def update_image():
    #horizontal lines
    global image_data
    global imageTexture
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

    img=img.resize((canvas_size,canvas_size),resample=Image.Resampling.NEAREST)

    imageTexture=pygame.image.frombytes(img.tobytes(),(canvas_size,canvas_size),"RGB")

#returns the line at said point
def pixel_to_point(p):
    return (int((p[0]//grid_scale)),int((p[1]//grid_scale)))

def get_line_location(coordinate:tuple):
    if coordinate[0]%2==0:
        return (coordinate[0]*step,coordinate[1]*step+step/2)

#returns the pixel coordinate at the middle of the line (for distance measuring)
def line_to_pixel(p:tuple):
    if p[0]%2==0:
        #horizontal line
        return (p[0]/2*step+(line_width/2),
                p[1]*step+(line_width)+(square_size/2))
    else:
        return ((p[0]-1)/2*step+(line_width)+(square_size/2),
                p[1]*step+(line_width/2))


pygame.init()
canvas = pygame.display.set_mode(settings.window_size)
pygame.display.set_caption("Pixel Void")


#this replaces it with random colored pixels (for testing)
# image_data=(np.random.rand(9,9,3)*255).astype(np.uint8)




#gameplay variables

exit = False
draw1=False
draw2=False

draw_location = (0,0)
brush_size=1

while not exit:
    canvas.fill(settings.window_background_color)

    update_image()


    canvas.blit(imageTexture,dest=canvas_offset)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit=True
        elif event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit=True
        elif event.type==pygame.MOUSEBUTTONUP:
            if event.button==pygame.BUTTON_LEFT:
                draw1=False
                
            elif event.button==pygame.BUTTON_RIGHT:
                draw2=False
                
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==pygame.BUTTON_LEFT:
                draw1=True
            elif event.button==pygame.BUTTON_RIGHT:
                draw2=True

        elif event.type==pygame.MOUSEMOTION:
            draw_location=event.pos
            draw_location=(draw_location[0]-canvas_offset[0],draw_location[1]-canvas_offset[1])
        elif event.type==pygame.MOUSEWHEEL: 
            brush_size+=event.y/2
            brush_size=SimpleUtility.limit(brush_size,.5,grid_size*2+1)
            
    if draw1 or draw2:
        
        point = pixel_to_point(draw_location)

        brush_box=((point[0]-brush_size,point[0]+brush_size),(point[1]-brush_size,point[1]+brush_size))
        
        #limit brush to edge of canvas
        brush_box= SimpleUtility.limit(brush_box,0,resolution)
        
        #align to grid
        brush_box = ((floor(brush_box[0][0]/step)*step,ceil(brush_box[0][1]/step)*step),
                     (floor(brush_box[1][0]/step)*step,ceil(brush_box[1][1]/step)*step))

        #convert to index that grid_data uses
        brush_point_box=((brush_box[0][0]//step,brush_box[0][1]//step),
                         (brush_box[1][0]//step,brush_box[1][1]//step))

        
        
        for x in range(brush_point_box[0][0]*2,brush_point_box[0][1]*2):
            for y in range(brush_point_box[1][0],brush_point_box[1][1]):
                # print(x,y)
                loc=line_to_pixel((x,y))
                if settings.debug_mode:
                    pygame.draw.circle(canvas,(255,0,255),
                                       (loc[0]*grid_scale+canvas_offset[0],
                                        loc[1]*grid_scale+canvas_offset[1])
                                        ,3)

                if dist(loc,point)<=brush_size:
                    if settings.debug_mode:
                        pygame.draw.circle(canvas,(255,0,0),
                                           (loc[0]*grid_scale+canvas_offset[0],
                                            loc[1]*grid_scale+canvas_offset[1]),
                                            5)

                    if x>=0 and x<len(grid_data) and y>=0 and y<len(grid_data[0]):
                        # print(len(grid_data))
                        if draw1 and draw2:
                            grid_data[x,y]=SimpleUtility.mix_colors(settings.color1,settings.color2)
                        elif draw1:
                            grid_data[x,y]=settings.color1
                        elif draw2:
                            grid_data[x,y]=settings.color2

                        



        if settings.debug_mode:
            pygame.draw.circle(canvas,(0,255,0),
                               (point[0]*grid_scale+canvas_offset[0],
                                point[1]*grid_scale+canvas_offset[1]),
                                8)
            for i in [(0,0),(0,1),(1,1),(1,0)]:
                pygame.draw.circle(canvas,(0,0,255),
                                   (brush_box[0][i[0]]*grid_scale+canvas_offset[0],
                                    brush_box[1][i[1]]*grid_scale+canvas_offset[1]),
                                   10)
        
        





    pygame.draw.circle(canvas,(0,0,255),
                       (draw_location[0]+canvas_offset[0],
                        draw_location[1]+canvas_offset[1]),
                       brush_size*grid_scale,width=5)
    
        
    pygame.display.update()


