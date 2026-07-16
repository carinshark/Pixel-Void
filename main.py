
import pygame
from segmentCanvas import SegmentCanvas
from colorPickerWindow import ColorPickerWindow
from appSettings import AppSettings
from simpleUtility import in_range,subtract,limit





if __name__=="__main__":
    pygame.init()
    
    settings=AppSettings()
    canvas = pygame.display.set_mode(settings.window_size)
    canvas.fill(settings.window_background_color)
    pygame.display.set_caption("Pixel Void")

    

    

    color_picker1=ColorPickerWindow(settings.color1,name="Color 1",settings=settings)
    color_picker2=ColorPickerWindow(settings.color2,name="Color 2",settings=settings)
    color_pickerb=ColorPickerWindow(settings.canvas_background_color,
                                    name="Background",settings=settings)

    draw_canvas=SegmentCanvas(settings=settings)    

    #updater has to take in a position input in all of em
    window_inputs=[
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
    ]



    exit=False
    activeL=-1
    activeR=-1
    draw_location=(0,0)
    
    while not exit:
        canvas.fill(settings.window_background_color)
        draw_canvas.regular_update()

        for surf in window_inputs:
            canvas.blit(surf["surface"],surf["location"])


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit=True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    exit=True
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
                if event.button==pygame.BUTTON_LEFT:
                if event.button==pygame.BUTTON_LEFT and activeL!=-1:
                    window_inputs[activeL]["lclick"][1]()
                    activeL=-1
                            
                elif event.button==pygame.BUTTON_RIGHT:
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
                        subtract(event.pos,window_inputs[activeL]["location"]))
                        subtract(event.pos,window_inputs[activeR]["location"]))
            

            elif event.type==pygame.MOUSEWHEEL: 
                settings.brush_size+=event.y/2
                settings.brush_size=limit(settings.brush_size,.5,settings.grid_size*2+1)

        

        pygame.draw.circle(canvas,settings.color1,
                           draw_location,
                            settings.brush_size*settings.grid_scale,width=4,
                        draw_bottom_left=True,draw_top_left=True)
        pygame.draw.circle(canvas,settings.color2,draw_location,
                            settings.brush_size*settings.grid_scale,width=4,
                            draw_bottom_right=True,draw_top_right=True)
        

        pygame.display.update()
