import numpy as np
import pygame
from os import path

class AppSettings:
    
    def __init__(self):
        
        #colors
        self.background = np.array((0,0,0))
        self.blank= np.array((255,255,255),dtype="uint8")

        #adjustable parameters of canvas
        self.square_size=3
        self.line_width=1
        self.grid_size=20
        self.canvas_background_color=np.array((0,0,0),dtype="uint8")

        #in game settings
        self.color1=self.blank
        self.color2=self.background
        self.debug_mode=False

        #ui parameters
        self.window_background_color = np.array((8,14,32))
        self.window_size=(800,600)
        self.canvas_size=500
        self.margin=25
        self.pallete_box_size=(255,100)
        self.button_size=(75,25)
        self.brush_size=1
        

        #calculated parameters
        self.calculate_parameters()

        self.saved_colors=np.empty((0,3),dtype="uint8")
        

        self.main_text_color=np.array((125,192,255),dtype="uint8")

        self.file_path=path.abspath(path.dirname(__file__))+"/"

        self.main_font=pygame.font.Font(self.file_path+"artAssets/GrapeSoda.ttf",size=30)

        

    def calculate_parameters(self):
        self.step=self.line_width+self.square_size
        self.resolution=(self.grid_size*self.step+self.line_width)
        self.grid_scale=self.canvas_size/self.resolution