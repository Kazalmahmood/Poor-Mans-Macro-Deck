import board, busio, displayio, os, terminalio,  keypad
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import usb_hid
import digitalio
import time
import rotaryio

from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from rainbowio import colorwheel
import neopixel

from kicad_mode import handle_keypress as kicad_mode_handle_keypress
from windows_mody import handle_keypress as windows_mode_handle_keypress
from mc_mode import handle_keypress as mc_mode_handle_keypress
from vscode_mode import handle_keypress as vscode_mode_handle_keypress
from photoshop_mode import handle_keypress as photoshop_mode_handle_keypress

#________________________Neopixel____________________________________________________
pixel_pin = board.GP28
num_pixels = 8

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False)

RED = (255, 60, 60)
YELLOW = (255, 255, 50)
GREEN = (50, 255, 50)
CYAN = (80, 255, 255)
BLUE = (80, 80, 255)
PURPLE = (255, 50, 255)

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)
#----------------------------------------------------------------#

# Set up Consumer Control - Control Codes can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/consumer_control_code.html#ConsumerControlCode
cc = ConsumerControl(usb_hid.devices)

# Set up a keyboard device. - Keycode can be found here: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html#Keycode
keyboard = Keyboard(usb_hid.devices)

# Set up keyboard to write strings from macro
write_text = KeyboardLayoutUS(keyboard)

displayio.release_displays()

sda, scl = board.GP20, board.GP21  
i2c = busio.I2C(scl, sda)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
print(display_bus)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(128, 64, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(126, 62, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
splash.append(inner_sprite)

#Draw a label
text = "PoorMan's"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=38, y=28)
splash.append(text_area)
#Draw a label
text2 = "Macro___Deck"
text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFF00, x=30, y=40)
splash.append(text_area2)
#----------------------------------------------------------------------#

#Single color blue led
led1 = digitalio.DigitalInOut(board.GP27)
led1.direction = digitalio.Direction.OUTPUT

#Single color blue led for blink on key press
def led1_on():
  led1.value = True
  time.sleep(0.1)
  led1.value = False
  

#Dedicated mode button
modeChangeButton = digitalio.DigitalInOut(board.GP16)
modeChangeButton.direction = digitalio.Direction.INPUT
modeChangeButton.pull = digitalio.Pull.DOWN

modeChangeButton2 = digitalio.DigitalInOut(board.GP22)
modeChangeButton2.direction = digitalio.Direction.INPUT
modeChangeButton2.pull = digitalio.Pull.DOWN

modeChangeButton3 = digitalio.DigitalInOut(board.GP19)
modeChangeButton3.direction = digitalio.Direction.INPUT
modeChangeButton3.pull = digitalio.Pull.DOWN

modeChangeButton4 = digitalio.DigitalInOut(board.GP18)
modeChangeButton4.direction = digitalio.Direction.INPUT
modeChangeButton4.pull = digitalio.Pull.DOWN

modeChangeButton5 = digitalio.DigitalInOut(board.GP17)
modeChangeButton5.direction = digitalio.Direction.INPUT
modeChangeButton5.pull = digitalio.Pull.DOWN

# Set up the keypad 3*4 matrix
km = keypad.KeyMatrix(
    row_pins=(board.GP0, board.GP1, board.GP2),
    column_pins=(board.GP3, board.GP4, board.GP5, board.GP6),
)

##___________________Setup Rotary Encoder____________________________
SW1 = digitalio.DigitalInOut(board.GP9)
SW1.direction = digitalio.Direction.INPUT
SW1.pull = digitalio.Pull.DOWN

SW2 = digitalio.DigitalInOut(board.GP12)
SW2.direction = digitalio.Direction.INPUT
SW2.pull = digitalio.Pull.DOWN

SW3 = digitalio.DigitalInOut(board.GP15)
SW3.direction = digitalio.Direction.INPUT
SW3.pull = digitalio.Pull.DOWN

# Initialize the rotary encoder
encoder3 = rotaryio.IncrementalEncoder(board.GP13, board.GP14)
encoder2 = rotaryio.IncrementalEncoder(board.GP10, board.GP11)
encoder1 = rotaryio.IncrementalEncoder(board.GP7, board.GP8)

#Rotary encoder position function
#last_position3 = encoder3.position  # Initialize to the current position
#if last_position3 is None:
last_position3 = 0
last_position2 = 0
last_position1 = 0

def rotary_position_1():
    global last_position1
    #print(last_position)
    position = encoder1.position
    if position != last_position1:
        if position > last_position1:
            return(False)
        elif position < last_position1:
            return(True)
        last_position1 = position
    return(None)
#        
#def rotary_position_2():
#    global last_position2
#    #print(last_position)
#    position = encoder2.position
#    if position != last_position2:
#        if position > last_position2:
#            return(False)
#        elif position < last_position2:
#            return(True)
#        last_position2 = position
#    return(None)
#  
# __________________________________________________________________________________________


# _________________List of defind mode names, change the modes as you need_________________
    
mode_names = {1 : 'Windows', 2 : 'VS Code', 3 : 'Photoshop', 4 : 'Midnight Commander', 5 : 'KiCad',}

# Set Default Mode To 1
mode = 0
        
print(mode_names[1])    
    
# Function to update the macro label on the OLED screen
def update_macro_label(macro_name):
    macro_label = label.Label(terminalio.FONT, text=macro_name, color=0xFFFF00, x=0, y=55)
    splash.append(macro_label)
    display.refresh()
    time.sleep(0.05)
    splash.remove(macro_label)
    display.refresh()


while True:
    position = encoder3.position
    if position != last_position3:
        if position > last_position3:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
#            cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
            led1_on()

        elif position < last_position3:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
#            cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
            led1_on()
        last_position3 = position
        
    if not SW3.value:
        cc.send(ConsumerControlCode.MUTE)
        led1_on()
        time.sleep(0.2)

    position = encoder2.position
    if position != last_position2:
        if position > last_position2:
            cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
#            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            led1_on()

        elif position < last_position2:
            cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
#            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            led1_on()
        last_position2 = position

        
#        time.sleep(0.05)
#        update_screen(splash, macro_names[19], display)

    event = km.events.get()
    if event:
        if event and event.pressed and event.key_number == 11:
            mode = mode + 1
            if mode > 5:
                mode = 1
            # Checks if key_number 1 is pressed
            #print(f"Mode Change")
            # Make the display context
            splash = displayio.Group()
            display.show(splash)
            led1_on()

            color_bitmap = displayio.Bitmap(128, 64, 1)
            color_palette = displayio.Palette(1)
            color_palette[0] = 0xFFFFFF  # White

            bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
            splash.append(bg_sprite)

            # Draw a smaller inner rectangle
            inner_bitmap = displayio.Bitmap(118, 54, 1)
            inner_palette = displayio.Palette(1)
            inner_palette[0] = 0x000000  # Black
            inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
            splash.append(inner_sprite)

            # Draw a label
            text = mode_names[mode]
            center_x = (118 - len(text) * 6) // 2 + 5
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=center_x, y=28)
            splash.append(text_area)            
            
        else:
            print(event) 
        
        if mode == 0:
            time.sleep(0.05)

        
    if modeChangeButton.value:
        mode = 1
        splash = displayio.Group()
        display.show(splash)
        led1_on()  


        color_bitmap = displayio.Bitmap(128, 64, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(126, 62, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
        splash.append(inner_sprite)

        # Draw a label
        #text = mode_names[mode]
        #center_x = (118 - len(text) * 6) // 2 + 5
        #text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=center_x, y=28)
        #splash.append(text_area)
        
        text3 = "Windows"
        text_area3 = label.Label(terminalio.FONT, text=text3, color=0xFFFF00, x=43, y=7)
        splash.append(text_area3)

        text4 = "1:Explorer 2:VSCode"
        text_area4 = label.Label(terminalio.FONT, text=text4, color=0xFFFF00, x=2, y=17)
        splash.append(text_area4)

        text5 = "3:Edge 4:Firefox"
        text_area5 = label.Label(terminalio.FONT, text=text5, color=0xFFFF00, x=2, y=27)
        splash.append(text_area5)

        text6 = "5:Brave 6:Chrome"
        text_area6 = label.Label(terminalio.FONT, text=text6, color=0xFFFF00, x=2, y=37)
        splash.append(text_area6)

        text7 = "7:Spotify 8:SnipTool"
        text_area7 = label.Label(terminalio.FONT, text=text7, color=0xFFFF00, x=2, y=47)
        splash.append(text_area7)

        text8 = "9:Copy 10:Paste 11:WL"
        text_area8 = label.Label(terminalio.FONT, text=text8, color=0xFFFF00, x=2, y=57)
        splash.append(text_area8)


    elif modeChangeButton2.value:
        mode = 2
        # Make the display context
        splash = displayio.Group()
        display.show(splash)
        led1_on()  

        color_bitmap = displayio.Bitmap(128, 64, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(126, 62, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
        splash.append(inner_sprite)

        text9 = "VSCode"
        text_area9 = label.Label(terminalio.FONT, text=text9, color=0xFFFF00, x=50, y=7)
        splash.append(text_area9)

        text10 = "1:Sidbar 2:SpltEdtor"
        text_area10 = label.Label(terminalio.FONT, text=text10, color=0xFFFF00, x=2, y=17)
        splash.append(text_area10)

        text11 = "3:SelctLin 4:LinStat"
        text_area11 = label.Label(terminalio.FONT, text=text11, color=0xFFFF00, x=2, y=27)
        splash.append(text_area11)

        text12 = "5:LineEnd 6:EndLine"
        text_area12 = label.Label(terminalio.FONT, text=text12, color=0xFFFF00, x=2, y=37)
        splash.append(text_area12)

        text13 = "7:ComntLin 8:BlokComnt"
        text_area13 = label.Label(terminalio.FONT, text=text13, color=0xFFFF00, x=2, y=47)
        splash.append(text_area13)

        text14 = "9:ComndP 10:Zen 11:Windo"
        text_area14 = label.Label(terminalio.FONT, text=text14, color=0xFFFF00, x=2, y=57)
        splash.append(text_area14)
        
    elif modeChangeButton3.value:
        mode = 3
        # Make the display context
        splash = displayio.Group()
        display.show(splash)
        led1_on()  
        
        color_bitmap = displayio.Bitmap(128, 64, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)


        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(126, 62, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
        splash.append(inner_sprite)

        text15 = "Photoshop"
        text_area15 = label.Label(terminalio.FONT, text=text15, color=0xFFFF00, x=36, y=7)
        splash.append(text_area15)

        text16 = "1:Extra 2:ResizeImg"
        text_area16 = label.Label(terminalio.FONT, text=text16, color=0xFFFF00, x=2, y=17)
        splash.append(text_area16)

        text17 = "3:FreTrnsfrm 4:Curve"
        text_area17 = label.Label(terminalio.FONT, text=text17, color=0xFFFF00, x=2, y=27)
        splash.append(text_area17)

        text18 = "5:DSelect 6:InverseSl"
        text_area18 = label.Label(terminalio.FONT, text=text18, color=0xFFFF00, x=2, y=37)
        splash.append(text_area18)

        text19 = "7:ColorRange 8:Trim"
        text_area19 = label.Label(terminalio.FONT, text=text19, color=0xFFFF00, x=2, y=47)
        splash.append(text_area19)

        text20 = "9:ExAs 10:PNG 11:Web"
        text_area20 = label.Label(terminalio.FONT, text=text20, color=0xFFFF00, x=2, y=57)
        splash.append(text_area20)
        
    elif modeChangeButton4.value:
        mode = 4
        
        # Make the display context
        splash = displayio.Group()
        display.show(splash)
        led1_on()  

        color_bitmap = displayio.Bitmap(128, 64, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        inner_bitmap = displayio.Bitmap(126, 62, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
        splash.append(inner_sprite)

        text21 = "MidNightComander"
        text_area21 = label.Label(terminalio.FONT, text=text21, color=0xFFFF00, x=20, y=7)
        splash.append(text_area21)

        text22 = "1:Refresh 2:PrevDir"
        text_area22 = label.Label(terminalio.FONT, text=text22, color=0xFFFF00, x=2, y=17)
        splash.append(text_area22)

        text23 = "3:Copy 4:Move 5:Del"
        text_area23 = label.Label(terminalio.FONT, text=text23, color=0xFFFF00, x=2, y=27)
        splash.append(text_area23)

        text24 = "6:Selct 7:Dselect"
        text_area24 = label.Label(terminalio.FONT, text=text24, color=0xFFFF00, x=2, y=37)
        splash.append(text_area24)

        text25 = "8:Rename 9:SamPanel"
        text_area25 = label.Label(terminalio.FONT, text=text25, color=0xFFFF00, x=2, y=47)
        splash.append(text_area25)

        text26 = "10:DirCont 11:SwpPnel"
        text_area26 = label.Label(terminalio.FONT, text=text26, color=0xFFFF00, x=2, y=57)
        splash.append(text_area26)

    elif modeChangeButton5.value:
        mode = 5
        led1.value = True        
        
        # Make the display context
        splash = displayio.Group()
        display.show(splash)
        led1_on()  

        color_bitmap = displayio.Bitmap(128, 64, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(118, 54, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
        splash.append(inner_sprite)

        # Draw a label
        text = mode_names[mode]
        center_x = (118 - len(text) * 6) // 2 + 5
        text_area = label.Label(terminalio.FONT, text=text, color=0xffff00, x=center_x, y=28)
        splash.append(text_area)
    
# ----------------------------------------MODE 1--------------------------------------------------------------------------
    if mode == 0:
        rainbow_cycle(0)
        time.sleep(0.5)
    
    if mode == 1:
        windows_mode_handle_keypress(event, cc, led1_on, write_text, keyboard, SW1, SW2, SW3, rotary_position_1, splash, display)
        pixels.fill(GREEN)
        pixels.show()

    elif mode == 2:
        vscode_mode_handle_keypress(event, cc, led1_on, write_text, keyboard, SW1, SW2, SW3, rotary_position_1, splash, display)
        pixels.fill(RED)
        pixels.show()
        
    elif mode == 3:
        photoshop_mode_handle_keypress(event, cc, led1_on, write_text, keyboard, SW1, SW2, SW3, rotary_position_1, splash, display)
        pixels.fill(BLUE)
        pixels.show()

    elif mode == 4:
        mc_mode_handle_keypress(event, cc, led1_on, write_text, keyboard, SW1, SW2, SW3, rotary_position_1, splash, display)
        pixels.fill(PURPLE)
        pixels.show()
        
    elif mode == 5:
        kicad_mode_handle_keypress(event, cc, led1_on, write_text, keyboard, SW1, SW2, SW3, rotary_position_1, splash, display)
        pixels.fill(YELLOW)
        pixels.show()
        
    time.sleep(0.001)





  