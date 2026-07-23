
import pygame
from segmentCanvas import SegmentCanvas
from colorPickerWindow import ColorPickerWindow
from appSettings import AppSettings
from simpleUtility import in_range,subtract,limit
from colorPalette import ColorPalette
from button import Button
from incrementer import Incrementer
import numpy as np
from tkinter import Tk
from tkinter.messagebox import askyesno
from webbrowser import open as open_url



def save():
    draw_canvas.save_to_file()


def load():
    draw_canvas.load_from_file()


def download():
    draw_canvas.download_image()

def reset():
    root=Tk()
    root.withdraw()
    response=askyesno(title="Confirm Reset",
                        message="Are you sure you want reset everything?")


    if response:
        settings.grid_size=grid_inc.value
        settings.square_size=line_inc.value
        settings.calculate_parameters()
        draw_canvas.reset_image()
    root.destroy()


def open_help():
    open_url("https://github.com/carinshark/Pixel-Void/blob/main/README.md")
def undo():
    draw_canvas.undo()
def redo():
    draw_canvas.redo()
def debug_mode():
    settings.debug_mode=not settings.debug_mode

def leave_app():
    global exit
    root=Tk()
    root.withdraw()
    response=askyesno(title="Confirm Exit",
                        message="Are you sure you want to leave the app?")


    if response:
        exit=True
    root.destroy()


if __name__=="__main__":
    pygame.init()
    
    settings=AppSettings()
    canvas = pygame.display.set_mode(settings.window_size)
    canvas.fill(settings.window_background_color)
    pygame.display.set_caption("Pixel Void")

    pygame.display.set_icon(pygame.image.load(
        settings.file_path+"artAssets/PixelVoidIcon.png"
    ))

    background_img=pygame.image.load(settings.file_path+"artAssets/backgroundLines.png")

    color_picker1=ColorPickerWindow(settings.color1,name="Color 1",settings=settings)
    color_picker2=ColorPickerWindow(settings.color2,name="Color 2",settings=settings)
    color_pickerb=ColorPickerWindow(settings.canvas_background_color,
                                    name="Background",settings=settings)
    color_palette=ColorPalette(settings)
    draw_canvas=SegmentCanvas(settings=settings)
    load_button=Button(settings.file_path+"artAssets/loadImage.png",settings,load)
    save_button=Button(settings.file_path+"artAssets/saveImage.png",settings,save)
    download_button=Button(settings.file_path+"artAssets/downloadImage.png",settings,download)
    reset_button=Button(settings.file_path+"artAssets/resetCanvas.png",settings,reset)
    grid_inc=Incrementer(4,30,settings.grid_size,"grids",settings)
    line_inc=Incrementer(2,6,settings.square_size,"length",settings)

    
    help_button=Button(settings.file_path+"artAssets/helpButton.png",settings,open_help)

    carinshark_decal=pygame.image.load(settings.file_path+"artAssets/carinsharkDecal.png")

    undo_button=Button(settings.file_path+"artAssets/undoButton.png",settings,undo)


    #updater has to take in a position input in all of em
    window_inputs=[
        {"surface":background_img,
         "location":(0,0)},
        {"surface":color_picker1,
         "location":(550,25),
        "lclick":[color_picker1.check_input,color_picker1.no_input]},
        {"surface":color_picker2,
         "location":(550,150),
        "lclick":[color_picker2.check_input,color_picker2.no_input]},
        {"surface":color_pickerb,
         "location":(550,275),
        "lclick":[color_pickerb.check_input,color_pickerb.no_input]},
        {"surface":draw_canvas,
         "location":(25,25),
         "lclick":[draw_canvas.check_input_left,draw_canvas.no_input_left],
         "rclick":[draw_canvas.check_input_right,draw_canvas.no_input_right]
         },
         {
             "surface":color_palette,
             "location":(550,400),
             "lclick":[color_palette.check_input,color_palette.no_input]
         },
         {"surface":load_button,
          "location":(25,550),
          "lclick":[load_button.check_input,load_button.no_input]
          },
          {"surface":save_button,
          "location":(125,550),
          "lclick":[save_button.check_input,save_button.no_input]
          },
          {"surface":download_button,
          "location":(225,550),
          "lclick":[download_button.check_input,download_button.no_input]
          },
          {"surface":reset_button,
          "location":(625,525),
          "lclick":[reset_button.check_input,reset_button.no_input]
          },
          {"surface":line_inc,
          "location":(550,525),
          "lclick":[line_inc.check_input,line_inc.no_input]
          },
          {"surface":grid_inc,
          "location":(700,525),
          "lclick":[grid_inc.check_input,grid_inc.no_input]
          },
             {"surface":help_button,
             "location":(375,550),
             "lclick":[help_button.check_input,help_button.no_input]},
             {"surface":undo_button,
              "location":(325,550),
              "lclick":[undo_button.check_input,undo_button.no_input]},
              {"surface":carinshark_decal,
               "location":(425,550)}
        
    ]


    exit=False
    activeL=-1
    activeR=-1
    draw_location=(0,0)
    
    while not exit:
        canvas.fill(settings.window_background_color)

        for surf in window_inputs:
            if "regular_update" in dir(surf["surface"]):
                
                surf["surface"].regular_update()






        for surf in window_inputs:
            canvas.blit(surf["surface"],surf["location"])

        keys=set()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                leave_app()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    leave_app()
                else:
                    keys.add(event.key)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==pygame.BUTTON_LEFT:
                    for surf in window_inputs:
                        if "lclick" in surf.keys() and(
                            in_range(event.pos,surf["location"],surf["surface"].size)):
                            activeL=window_inputs.index(surf)

                            window_inputs[activeL]["lclick"][0](
                                subtract(event.pos,window_inputs[activeL]["location"]))
                            
                            break

                elif event.button==pygame.BUTTON_RIGHT:
                    for surf in window_inputs:
                        if "rclick" in surf.keys() and(
                            in_range(event.pos,surf["location"],surf["surface"].size)):
                            activeR=window_inputs.index(surf)
                            window_inputs[activeR]["rclick"][0](
                                subtract(event.pos,window_inputs[activeR]["location"]))

                            break
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button==pygame.BUTTON_LEFT and activeL!=-1:
                    window_inputs[activeL]["lclick"][1]()
                    activeL=-1
                            
                elif event.button==pygame.BUTTON_RIGHT and activeR!=-1:
                    window_inputs[activeR]["rclick"][1]()
                    activeR=-1

            elif event.type==pygame.MOUSEMOTION:
                draw_location=event.pos
                if activeL>=0:
                    window_inputs[activeL]["lclick"][0](
                        subtract(event.pos,window_inputs[activeL]["location"]))
                if activeR>=0:
                    window_inputs[activeR]["rclick"][0](
                        subtract(event.pos,window_inputs[activeR]["location"]))
            

            elif event.type==pygame.MOUSEWHEEL: 
                settings.brush_size+=event.y/2
                settings.brush_size=limit(settings.brush_size,.5,settings.step*settings.grid_size/2)

        gestures=[
            [{pygame.KMOD_LCTRL,pygame.KMOD_LSHIFT},{pygame.K_z},redo],
            [{pygame.KMOD_LCTRL},{pygame.K_z},undo],
            [{pygame.KMOD_LCTRL},{pygame.K_d},debug_mode],
        ]

        
        
        mod_keys=pygame.key.get_mods()
        for g in gestures:
            mods=0
            for m in g[0]:
                mods |= m
            
            if g[1]<=keys and mods&mod_keys==mods:
                g[2]()
                break

        pygame.draw.circle(canvas,settings.color1,
                           draw_location,
                            settings.brush_size*settings.grid_scale,width=4,
                        draw_bottom_left=True,draw_top_left=True)
        pygame.draw.circle(canvas,settings.color2,draw_location,
                            settings.brush_size*settings.grid_scale,width=4,
                            draw_bottom_right=True,draw_top_right=True)
        

        pygame.display.update()
