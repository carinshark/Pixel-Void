import pygame
import numpy as np
from appSettings import AppSettings
from simpleUtility import in_range

class ColorPalette(pygame.Surface):

    def __init__(self, settings:AppSettings):
        super().__init__((225,100))
        self.settings=settings

        self.background_img=pygame.image.load("artAssets/basicFrame.png")

        self.title_img=pygame.Surface((30,100),flags=pygame.SRCALPHA)

        t_color=(120,107,223)
        letter_add=settings.main_font.render
        name="Palette"
        
        for i in range(len(name)):
            x= 3 if i%2==0 else 14
            y=80/(len(name))*i
            self.title_img.blit(letter_add(name[i],False,t_color),dest=(x,y))

        self.palette_visual=pygame.Surface((196,88),flags=pygame.SRCALPHA)
        self.blank_palette_img=pygame.image.load("artAssets/emptyPallette.png")
        self.prompt_img=pygame.image.load("artAssets/palletteOverlay.png")

        self.open_prompt=-1

        self.current_palette=settings.saved_colors.copy()

        self.update()
    
    def regular_update(self):
        if len(self.settings.saved_colors)!=len(self.current_palette) or(
            not (self.settings.saved_colors==self.current_palette).all()):
            self.current_palette=self.settings.saved_colors.copy()
            self.update()

    
    def update(self):
        self.blit(self.background_img)
        self.blit(self.title_img,(190,0))

        

        for i in range(len(self.settings.saved_colors)):
            x=(i%10)*18
            y=(i//10)*18
            s = pygame.Surface((16,16))
            s.fill(self.settings.saved_colors[i])
            self.palette_visual.blit(s,(x,y))
        for i in range(len(self.settings.saved_colors),50):
            x=(i%10)*18
            y=(i//10)*18
            self.palette_visual.blit(self.blank_palette_img,(x,y))

        self.blit(self.palette_visual,dest=(6,6))

        if self.open_prompt!=-1:
            self.blit(self.prompt_img,(33,22))
        



    def check_input(self,pos:tuple):
        if self.open_prompt==-1:
            for i in range(len(self.settings.saved_colors)):
                x=(i%10)*18+6
                y=(i//10)*18+6
                if in_range(pos,(x,y),(16,16)):
                    self.open_prompt=i
                    self.update()
                    break
        else:
            button_pressed=True
            if in_range(pos,(165,22),(17,17)):
                #close out of it
                pass
            elif in_range(pos,(37,34),(32,32)):
                #set to 1
                for i in range(3):
                    self.settings.color1[i]=self.settings.saved_colors[self.open_prompt][i]
            elif in_range(pos,(71,34),(32,32)):
                #set to 2
                for i in range(3):
                    self.settings.color2[i]=self.settings.saved_colors[self.open_prompt][i]
            elif in_range(pos,(105,34),(32,32)):
                #set to background
                for i in range(3):
                    self.settings.canvas_background_color[i]=self.settings.saved_colors[self.open_prompt][i]
            elif in_range(pos,(139,34),(32,32)):
                #delete color
                self.settings.saved_colors=np.delete(self.settings.saved_colors,self.open_prompt,0)
            else:
                button_pressed=False
            if button_pressed:
                self.open_prompt=-1
                self.update()
            


    


    def no_input(self):
        pass



if __name__=="__main__":
    pygame.init()
    
    window = ColorPalette(AppSettings())
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
                    window.check_input(event.pos)
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    window.no_input()
                    active=False

            elif event.type==pygame.MOUSEMOTION:
                if active:
                    window.check_input(event.pos)

        canvas.blit(window) 

        pygame.display.update()
