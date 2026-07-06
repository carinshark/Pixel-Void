from PIL import Image

import numpy as np

background = np.array((0,0,0))

blank= np.array((255,255,255),dtype="uint8")

square_size=3
line_width=1


grid_size=(3,4)

#storing of line data
#odd values on the last row are irrelevant.
grid_data=np.full((grid_size[0]*2+1,grid_size[1]+1,3),blank,dtype="uint8")


#this converts it into visual pixels based on the parameters given
image_data=np.full((square_size*grid_size[0]+line_width*(grid_size[0]),
                    square_size*grid_size[1]+line_width*(grid_size[1])
                    ,3),background,dtype="uint8")


#horizontal lines
for r in range(1,len(grid_data),2):
    for c in range(0,len(grid_data[0])-1):
        x=((r-1)//2)*square_size+line_width
        y=0
        for i in range(square_size):
            for j in range(line_width):
                image_data[x+i,y+j]=grid_data[r][c]

rsize=image_data.shape


canvas = Image.fromarray(image_data)
canvas.show()