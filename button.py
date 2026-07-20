import pygame
from appSettings import AppSettings

class Button(pygame.Surface):
    def __init__(self,icon:str,settings:AppSettings,
                 function1,function2:function=None,icon2:str=None):
        self.bkg_img=pygame.image.load(icon)
        super().__init__(self.bkg_img.size)
        self.settings=settings
        self.function1:function=function1
        self.function2:function=function2

        

        self.pressed=False
        self.is_active=False
        
        self.toggle=True if self.function2 else False

        self.bkg_img2=pygame.image.load(icon2) if icon2 else None

        self.update()

    def update(self):
        if self.bkg_img2 and self.is_active:
            self.blit(self.bkg_img2)
        else:
            self.blit(self.bkg_img)
        

    def check_input(self,pos):
        if self.pressed:
            return
        self.pressed=True
        if not self.is_active:
            self.function1()
            if self.toggle:
                self.is_active=True
            self.update()
        else:
            self.function2()
            self.is_active=False
            self.update()
            

    def no_input(self):
        self.pressed=False

if __name__=="__main__":
    pygame.init()

    def testCommand():
        print("pressed!")
    def command2():
        print("unclick")
    
    window = Button("artAssets/downloadImage.png",AppSettings(),testCommand,command2,"artAssets/saveImage.png")
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
