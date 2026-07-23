import pygame
import numpy as np
from appSettings import AppSettings
from simpleUtility import limit,mix_colors
from PIL import Image
from math import floor,ceil,dist

from tkinter import Tk,filedialog

class SegmentCanvas(pygame.Surface):
    def __init__(self, settings:AppSettings):
        super().__init__((settings.canvas_size,settings.canvas_size))
        self.settings = settings

        #colors
        self.background = settings.background
        self.blank= settings.blank




        #storing of line data
        #odd values on the last row are irrelevant.
        self.grid_data=np.full((settings.grid_size*2+1,settings.grid_size+1,3),self.background,dtype="uint8")

        self.current_color=settings.canvas_background_color.copy()
        
        self.draw1=False
        self.draw2=False

        self.debug_overlay=pygame.Surface((settings.canvas_size,settings.canvas_size),flags=pygame.SRCALPHA)

        self.previous_states=[]
        self.current_state=0

        self.update_image()
        self.save_state()
    

    
    def load_from_file(self):
        root=Tk()
        root.withdraw()

        path = filedialog.askopenfile(mode="rb",defaultextension="npz",filetypes=[("Numpy File","npz")])

        try:
            if path:
                a=np.load(path,allow_pickle=False)
                


                self.settings.saved_colors=a["palette"]
                self.grid_data=a["grid"]

                for i in range(3):
                    self.settings.color1[i]=a["color1"][i]
                for i in range(3):
                    self.settings.color2[i]=a["color2"][i]
                for i in range(3):
                    self.settings.canvas_background_color[i]=a["colorb"][i]

                self.settings.grid_size=a["grid_size"]
                self.settings.square_size=a["square_size"]

                self.settings.calculate_parameters()

                self.update_image()
        except KeyError:
            pass

        finally:
            root.destroy()

    def save_to_file(self):
        root=Tk()
        root.withdraw()
        #prompt file
        path = filedialog.asksaveasfile(mode="wb",defaultextension="npz",filetypes=[("Numpy File","npz")])
        #save to location

        try:
            if path:
                np.savez(path,allow_pickle=False,
                         grid=self.grid_data,
                         palette=self.settings.saved_colors,
                         color1=self.settings.color1,
                         color2=self.settings.color2,
                         colorb=self.settings.canvas_background_color,
                         grid_size=self.settings.grid_size,
                         square_size=self.settings.square_size
                         )

        finally:
            root.destroy()
        

    def reset_image(self):
        
        self.grid_data=np.full((
            self.settings.grid_size*2+1,
            self.settings.grid_size+1,3),
            self.background,dtype="uint8")
        self.update_image()
        
   
    def download_image(self):

        root=Tk()
        root.withdraw()
        path = filedialog.asksaveasfile(
            mode="wb",defaultextension="jpg",
            filetypes=[("jpg Image","*.jpg"),("PNG Image","*.png")])

        #save to location
        try:
            if path:
                self.display_img.save(path)

        finally:
            root.destroy()
        



    def regular_update(self):
        if not (self.settings.canvas_background_color==self.current_color).all():
            self.update_image()
            self.current_color=self.settings.canvas_background_color.copy()
    
    def update_image(self):
        #horizontal lines
        square_size=self.settings.square_size
        line_width=self.settings.line_width
        canvas_size=self.settings.canvas_size

        #this converts it into visual pixels based on the parameters given
        #THIS PART SPECIFICALLY IS COLUMN MAJOR RATHER THAN ROW MAJOR
        self.image_data=np.full((self.settings.resolution,
                            self.settings.resolution
                            ,3),self.settings.canvas_background_color,dtype="uint8")
        
        for r in range(1,len(self.grid_data),2):
            for c in range(0,len(self.grid_data[0])):
                x=((r-1)//2)*(square_size+line_width)+line_width
                y=(square_size+line_width)*c
                for i in range(square_size):
                    for j in range(line_width):
                        self.image_data[y+j,x+i]=self.grid_data[r][c]

        #vertical lines
        for r in range(0,len(self.grid_data),2):
            for c in range(0,len(self.grid_data[0])-1):
                x=(r//2)*(square_size+line_width)
                y=c*(square_size+line_width)+line_width
                for i in range(line_width):
                    for j in range(square_size):
                        self.image_data[y+j,x+i]=self.grid_data[r][c]
        
        img = Image.fromarray(self.image_data)

        self.display_img=img.resize((canvas_size,canvas_size),resample=Image.Resampling.NEAREST)


        self.blit(pygame.image.frombytes(
            self.display_img.tobytes()
            ,(canvas_size,canvas_size),"RGB"))
        
        if self.settings.debug_mode:
            self.blit(self.debug_overlay)


    def check_input_left(self,pos):
        self.draw1=True
        self.draw(pos)
    
    def no_input_left(self):
        self.draw1=False
        self.save_state()
    def check_input_right(self,pos):
        self.draw2=True
        self.draw(pos)
    def no_input_right(self):
        self.draw2=False
        self.save_state()

    def save_state(self):
        if not (self.draw1 or self.draw2):
            self.previous_states=self.previous_states[:self.current_state+1]
            self.previous_states.append(self.grid_data.copy())
            self.current_state=len(self.previous_states)-1


    def undo(self):
        if self.current_state>0:
            self.current_state-=1
            self.grid_data=self.previous_states[self.current_state].copy()
            self.update_image()
    def redo(self):
        if self.current_state<len(self.previous_states)-1 and len(self.previous_states)>0:
            self.current_state+=1
            self.grid_data=self.previous_states[self.current_state].copy()
            self.update_image()


    def draw(self,draw_location):
        if self.settings.debug_mode:
                    self.debug_overlay.fill((0,0,0,0))
        
        if not (self.draw1 or self.draw2):
            return

        settings=self.settings
        brush_size=settings.brush_size
        step=self.settings.step
        
            
        point = self.pixel_to_point(draw_location)

        brush_box=((point[0]-brush_size,point[0]+brush_size),(point[1]-brush_size,point[1]+brush_size))
        
        #limit brush to edge of canvas
        brush_box= limit(brush_box,0,self.settings.resolution)
        
        #align to grid
        brush_box = ((floor(brush_box[0][0]/step)*step,ceil(brush_box[0][1]/step)*step),
                    (floor(brush_box[1][0]/step)*step,ceil(brush_box[1][1]/step)*step))

        #convert to index that grid_data uses
        brush_point_box=((brush_box[0][0]//step,brush_box[0][1]//step),
                        (brush_box[1][0]//step,brush_box[1][1]//step))

        
        
        for x in range(brush_point_box[0][0]*2,brush_point_box[0][1]*2):
            for y in range(brush_point_box[1][0],brush_point_box[1][1]):
                loc=self.line_to_pixel((x,y))
                if settings.debug_mode:
                    pygame.draw.circle(self.debug_overlay,(255,0,255),
                                    (loc[0]*self.settings.grid_scale,
                                        loc[1]*self.settings.grid_scale)
                                        ,3)

                if dist(loc,point)<=brush_size:
                    if settings.debug_mode:
                        pygame.draw.circle(self.debug_overlay,(255,0,0),
                                        (loc[0]*self.settings.grid_scale,
                                            loc[1]*self.settings.grid_scale),
                                            5)

                    if x>=0 and x<len(self.grid_data) and y>=0 and y<len(self.grid_data[0]):
                        if self.draw1 and self.draw2:
                            self.grid_data[x,y]=mix_colors(settings.color1,settings.color2)
                        elif self.draw1:
                            self.grid_data[x,y]=settings.color1
                        elif self.draw2:
                            self.grid_data[x,y]=settings.color2

                        



        if settings.debug_mode:
            pygame.draw.circle(self.debug_overlay,(0,255,0),
                            (point[0]*self.settings.grid_scale,
                                point[1]*self.settings.grid_scale),
                                8)
            for i in [(0,0),(0,1),(1,1),(1,0)]:
                pygame.draw.circle(self.debug_overlay,(0,0,255),
                                (brush_box[0][i[0]]*self.settings.grid_scale,
                                    brush_box[1][i[1]]*self.settings.grid_scale),
                                10)
        self.update_image()
    
    #returns the line at said point
    def pixel_to_point(self,p):
        grid_scale=self.settings.grid_scale
        return (int((p[0]//grid_scale)),int((p[1]//grid_scale)))

    def get_line_location(self,coordinate:tuple):
        step=self.settings.step
        if coordinate[0]%2==0:
            return (coordinate[0]*step,coordinate[1]*step+step/2)

    #returns the pixel coordinate at the middle of the line (for distance measuring)
    def line_to_pixel(self,p:tuple):
        step=self.settings.step
        line_width=self.settings.line_width
        square_size=self.settings.square_size
        if p[0]%2==0:
            #horizontal line
            return (p[0]/2*step+(line_width/2),
                    p[1]*step+(line_width)+(square_size/2))
        else:
            return ((p[0]-1)/2*step+(line_width)+(square_size/2),
                    p[1]*step+(line_width/2))



if __name__=="__main__":
    pygame.init()
    
    window = SegmentCanvas(settings=AppSettings())
    canvas = pygame.display.set_mode(window.size)
    exit=False
    activeL=False
    activeR=False

    while not exit:
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit=True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    exit=True
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    activeL=True
                elif event.button==pygame.BUTTON_RIGHT:
                    activeR=True
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    window.no_input_left()
                    activeL=False
                elif event.button==pygame.BUTTON_RIGHT:
                    window.no_input_right()
                    activeR=False

            elif event.type==pygame.MOUSEMOTION:
                if activeL:
                    window.check_input_left(event.pos)
                if activeR:
                    window.check_input_right(event.pos)

        canvas.blit(window) 

        pygame.display.update()
