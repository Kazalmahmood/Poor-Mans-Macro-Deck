import time
import board, busio, displayio, os, terminalio
import digitalio
import time
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_display_text import label
import adafruit_displayio_ssd1306

def update_screen(splash, macro_name, display):
    # Update the macro label
    center_x = (118 - len(macro_name) * 6) // 2 + 5
    macro_label = label.Label(terminalio.FONT, text=macro_name, color=0xFFFF00, x=center_x, y=50)
    splash.append(macro_label)
    display.refresh()
    # Wait for 1 seconds
    time.sleep(1)
    # Remove the macro label after 1 seconds
    splash.remove(macro_label)
    display.refresh()

def handle_keypress(event, cc, led1_on, write_text, keyboard, SW1, SW2, SW3, rotary_position_1, splash, display):

    # Macro names or actions
    # Change the macro names * 
    macro_names = {
        0: "Refresh",
        1: "PreviousDirectory",
        2: "Copy",
        3: "Move",
        4: "Delete",
        5: "Select",
        6: "Deselect",
        7: "Rename",
        8: "SamePanel",
        9: "DirectoryContent",
        10: "SwapPanel",
        11: "Page Up",
        12: "Page Down",
        13: "Directory Hotlist",
        14: "Up Arrow",
        15: "Down Arrow",
        16: "Enter",
        17: "Volume Up",
        18: "Volume Down",
        19: "Mute/Unmute",
        # Add more macro names and their corresponding keys as needed
    }

    if event and event.pressed and event.key_number == 0:
        keyboard.send(Keycode.CONTROL, Keycode.R)
        led1_on()
        update_screen(splash, macro_names[0], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 1:
        keyboard.send(Keycode.ALT, Keycode.Y)
        led1_on()
        update_screen(splash, macro_names[1], display)

    if event and event.pressed and event.key_number == 2:
        keyboard.send(Keycode.F5)
        led1_on()
        update_screen(splash, macro_names[2], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 3:
        keyboard.send(Keycode.F6)
        led1_on()
        update_screen(splash, macro_names[3], display)

    if event and event.pressed and event.key_number == 4:
        keyboard.send(Keycode.F8)
        led1_on()
        update_screen(splash, macro_names[4], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 5:
        keyboard.send(Keycode.INSERT)
        led1_on()
        
        update_screen(splash, macro_names[5], display)
    if event and event.pressed and event.key_number == 6:
        keyboard.send(Keycode.CONTROL, Keycode.T)
        led1_on()
        update_screen(splash, macro_names[6], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 7:
        keyboard.send(Keycode.SHIFT, Keycode.F6)
        led1_on()
        update_screen(splash, macro_names[7], display)

    if event and event.pressed and event.key_number == 8:
        keyboard.send(Keycode.ALT, Keycode.I)
        led1_on()
        update_screen(splash, macro_names[8], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 9:
        keyboard.send(Keycode.ALT, Keycode.O)
        led1_on()
        update_screen(splash, macro_names[9], display)

    if event and event.pressed and event.key_number == 10:
        keyboard.send(Keycode.CONTROL, Keycode.U)
        led1_on()
        update_screen(splash, macro_names[10], display)


    #Rotary encoder turned clockwise
#    if rotary_changed_top() == True:
#        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
#        #led1_on()
#        update_screen(splash, macro_names[17], display)
#        
#    elif rotary_changed_top() == False:
#        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
#        #led1_on()
#        update_screen(splash, macro_names[18], display)
    
    #Rotary encoder turned clockwise
#    if rotary_position_2() == True:
#        keyboard.send(Keycode.PAGE_DOWN)
#        led1_on()
#        time.sleep(0.5)
#        update_screen(splash, macro_names[14], display)
#        
#    elif rotary_position_2() == False:
#        keyboard.send(Keycode.PAGE_UP)
#        led1_on()
#        time.sleep(0.5)
#        update_screen(splash, macro_names[15], display)

    if rotary_position_1() == True:
        keyboard.send(Keycode.DOWN_ARROW)
        led1_on()
        time.sleep(0.5)
        update_screen(splash, macro_names[11], display)
        
    elif rotary_position_1() == False:
        keyboard.send(Keycode.UP_ARROW)
        led1_on()
        time.sleep(0.5)
        update_screen(splash, macro_names[12], display)
        
#    if not SW3.value:
#        cc.send(ConsumerControlCode.MUTE)
#        led1_on()
#        update_screen(splash, macro_names[19], display)
        
    if not SW2.value:
        keyboard.send(Keycode.CONTROL, Keycode.BACKSLASH)
        led1_on()
        update_screen(splash, macro_names[16], display)

    if not SW1.value:
        keyboard.send(Keycode.ENTER)
        led1_on()
        update_screen(splash, macro_names[13], display)

    time.sleep(0.0001)
