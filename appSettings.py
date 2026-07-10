import numpy as np

class AppSettings:
    
    def __init__(self):
        #colors
        self.background = np.array((0,0,0))
        self.blank= np.array((255,255,255),dtype="uint8")

        #adjustable parameters
        self.square_size=5
        self.line_width=1
        self.grid_size=20
        self.canvas_size=500