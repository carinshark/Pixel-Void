import numpy as np
import pygame

class AppSettings:
    
    def __init__(self):
        #colors
        self.background = np.array((0,0,0))
        self.blank= np.array((255,255,255),dtype="uint8")

        #adjustable parameters of canvas
        self.square_size=3
        self.line_width=1
        self.grid_size=20

        #in game settings
        self.color1=self.blank
        self.color2=self.background
        self.debug_mode=False

        #ui parameters
        self.window_background_color = np.array((150,200,200))
        self.window_size=(800,600)
        self.canvas_size=500
        self.margin=25
        self.pallete_box_size=(255,100)
        self.button_size=(75,25)

        self.main_font=pygame.font.Font("artAssets\GrapeSoda.ttf",size=30)
