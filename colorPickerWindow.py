import pygame
import numpy as np

class ColorPickerWindow(pygame.Surface):
    
    def __init__(self,init_color:np.ndarray):
        super().__init__((255,100))
        super().fill()
        self.current_color=init_color


if __name__=="__main__":
    pygame.init()
    
    window = ColorPickerWindow(np.array((0,0,255),dtype="uint8"))
    canvas = pygame.display.set_mode(window.size)
    canvas.blit(window)
    pygame.display.update()
