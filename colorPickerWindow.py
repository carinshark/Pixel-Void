import pygame
import numpy as np
from appSettings import AppSettings
from simpleUtility import SimpleUtility

class ColorPickerWindow(pygame.Surface):
    
    def __init__(self,init_color:np.ndarray,name:str,settings:AppSettings):
        super().__init__((225,100))
        self.current_color=init_color
        self.settings=settings

        self.background_image=pygame.image.load("artAssets/colorPickerBackground.png")
        self.color_display=pygame.Surface((38,38))

        self.title=self.settings.main_font.render(name,False,(120,107,223))

        self.sliders=[
            pygame.image.load("artAssets/sliderRed.png"),
            pygame.image.load("artAssets/sliderGreen.png"),
            pygame.image.load("artAssets/sliderBlue.png")
        ]
        self.is_pressed=False
        self.item_pressed=-1

        self.update()
    
    def __create_slider(self,c:int):
        s=pygame.Surface((128,4))
        for x in range(128):
            color = [x*2 if i==c else self.current_color[i] for i in range(len(self.current_color))]
            s.fill(color,((x,0),(1,4)))
        return s


    def update(self):
        self.blit(self.background_image)
        self.color_display.fill(self.current_color)
        self.blit(self.color_display,dest=(24,39))
        
        self.blit(self.__create_slider(0),dest=(74,39))
        self.blit(self.__create_slider(1),dest=(74,53))
        self.blit(self.__create_slider(2),dest=(74,67))

        self.blits(
            [(self.sliders[i],(72+self.current_color[i]//2,43+(i*14))) for i in range(3)]
        )

        self.blit(self.title,dest=(14,3))

    def check_input(self,pos):
        if not self.is_pressed:
            self.is_pressed=True
            if SimpleUtility.in_range(pos,(74,39),(128,10)):
                self.item_pressed=0
            elif SimpleUtility.in_range(pos,(74,53),(128,10)):
                self.item_pressed=1
            elif SimpleUtility.in_range(pos,(74,67),(128,10)):
                self.item_pressed=2

        if self.is_pressed and self.item_pressed>=0:
            print(SimpleUtility.limit((pos[0]-74)*2,0,255))
            self.current_color[self.item_pressed] = SimpleUtility.limit((pos[0]-74)*2,0,255)

            self.update()
            print(self.current_color)



    def no_input(self):
        self.is_pressed=False
        self.item_pressed=-1
        

        
        
        


if __name__=="__main__":
    pygame.init()
    
    window = ColorPickerWindow(np.array((100,0,0),dtype="uint8"),
                               name="background",
                               settings=AppSettings())
    canvas = pygame.display.set_mode(window.size)
    exit=False
    active=False

    while not exit:
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit=True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    exit=True
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    active=True
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    window.no_input()
                    active=False

            elif event.type==pygame.MOUSEMOTION:
                if active:
                    window.check_input(event.pos)
                    
        canvas.blit(window)

        pygame.display.update()
