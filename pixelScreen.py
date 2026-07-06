from PIL import Image

import numpy as np

background = np.array((0,0,0))

blank= np.array((255,255,255),dtype="uint8")

square_size=4
line_width=2


grid_size=(3,4)

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
        print(x,y)
        for i in range(line_width):
            for j in range(square_size):
                image_data[y+j,x+i]=grid_data[r][c]


rsize=image_data.shape


canvas = Image.fromarray(image_data)
canvas.show()