import pygame
from appSettings import AppSettings
from simpleUtility import in_range,limit

class Incrementer(pygame.Surface):
    def __init__(self,min:int,max:int,current_val:int,title:str,settings:AppSettings):
        super().__init__((75,50))
        self.settings=settings
        
        self.background_img=pygame.image.load("artAssets/IncrementUI.png")
        self.min=min
        self.max=max
        self.value=current_val

        self.title_img=settings.main_font.render(title,False,settings.main_text_color)
        self.pressed=False

        self.update()

    def update(self):
        num=self.settings.main_font.render(str(self.value),False,self.settings.main_text_color)

        
        self.blit(self.background_img)

        self.blit(self.title_img,((self.size[0]-self.title_img.size[0])/2,-3))
        self.blit(num,((75-num.size[0])/2,22))

    def check_input(self,pos):
        if self.pressed:return

        updated=False
        if in_range(pos,(0,25),(25,25)):
            self.value=limit(self.value-1,
                               self.min,self.max)
            updated=True
        elif in_range(pos,(50,25),(25,25)):
            self.value=limit(self.value+1,
                               self.min,self.max)
            updated=True
        
        if updated:
            self.update()
            self.pressed=True


    def no_input(self):
        self.pressed=False


if __name__=="__main__":
    pygame.init()
    
    window = Incrementer(4,10,4,"length",AppSettings())
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
