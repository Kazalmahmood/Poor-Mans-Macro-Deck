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
        0: "Toggle Sidebar",
        1: "Split Editor",
        2: "Select Line",
        3: "Copy Line Up",
        4: "Copy Line Down",
        5: "New Line Up",
        6: "Move Line Up",
        7: "Move Line Down",
        8: "Delete Line",
        9: "Jump To Line Start",
        10: "Jump To Line End",
        11: "End Line",
        12: "Comment Line",
        13: "Block Comment",
        14: "Command Plaette",
        15: "Zen Mode",
        16: "New Window",
        17: "Volume UP",
        18: "Volume Down",
        19: "Mute/UnMute",
        # Add more macro names and their corresponding keys as needed
    }

    if event and event.pressed and event.key_number == 0:
        keyboard.send(Keycode.CONTROL, Keycode.B)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[0], display)

    if event and event.pressed and event.key_number == 1:
        keyboard.send(Keycode.CONTROL, Keycode.BACKSLASH)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[1], display)

    if event and event.pressed and event.key_number == 2:
        keyboard.send(Keycode.CONTROL, Keycode.L)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[2], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 3:
        keyboard.send(Keycode.HOME)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[9], display)

    if event and event.pressed and event.key_number == 4:
        keyboard.send(Keycode.END)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[10], display)
    if event and event.pressed and event.key_number == 5:
        keyboard.send(Keycode.SHIFT, Keycode.ENTER)
        led1_on()
        time.sleep(0.2)
        update_screen(splash, macro_names[11], display)

    if event and event.pressed and event.key_number == 6:
        keyboard.send(Keycode.CONTROL, Keycode.FORWARD_SLASH)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[12], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 7:
        keyboard.send(Keycode.SHIFT, Keycode.ALT, Keycode.A)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[13], display)

    if event and event.pressed and event.key_number == 8:
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.P)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[14], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 9:
        keyboard.send(Keycode.CONTROL, Keycode.K)
        time.sleep(0.05)
        keyboard.send(Keycode.Z)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[15], display)

    if event and event.pressed and event.key_number == 10:
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.N)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[16], display)

#    if rotary_position_2() == True:
#        print("Page Up")
#        keyboard.send(Keycode.ALT, Keycode.UP_ARROW)
#        led1_on()
#        time.sleep(0.5)
#        
##        update_screen(splash, macro_names[17], display)
#        
#    elif rotary_position_2() == False:
#        print("Page Down")
#        keyboard.send(Keycode.ALT, Keycode.DOWN_ARROW)
#        led1_on()
#        time.sleep(0.5)
        
#        update_screen(splash, macro_names[18], display)

    #Rotary encoder turned clockwise
    if rotary_position_1() == True:
        print("Up Arrow")
        keyboard.send(Keycode.SHIFT, Keycode.ALT, Keycode.UP_ARROW)
        led1_on()
        time.sleep(0.5)

#        update_screen(splash, macro_names[17], display)

        
    elif rotary_position_1() == False:
        print("Down Arrow")
        keyboard.send(Keycode.SHIFT, Keycode.ALT, Keycode.DOWN_ARROW)
        led1_on()
        time.sleep(0.5)

    #Rotary encoder turned clockwise
#    if rotary_changed_left() == True:
#        keyboard.send(Keycode.SHIFT, Keycode.ALT, Keycode.UP_ARROW)
#        led1_on()
#        time.sleep(0.2)
#        update_screen(splash, macro_names[3], display)
#        
#    elif rotary_changed_left() == False:
#        keyboard.send(Keycode.SHIFT, Keycode.ALT, Keycode.DOWN_ARROW)
#        led1_on()
#        time.sleep(0.2)
#        update_screen(splash, macro_names[4], display)
#    
#    #Rotary encoder turned clockwise
#    if rotary_changed_right() == True:
#        keyboard.send(Keycode.ALT, Keycode.UP_ARROW)
#        led1_on()
#        time.sleep(0.2)
#        update_screen(splash, macro_names[6], display)
#        
#    elif rotary_changed_right() == False:
#        keyboard.send(Keycode.ALT, Keycode.DOWN_ARROW)
#        led1_on()
#        time.sleep(0.2)
#        update_screen(splash, macro_names[7], display)

#    if rotary_changed_top() == True:
#        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
#        led1_on()
#        time.sleep(0.2)
#        update_screen(splash, macro_names[17], display)
#
#    elif rotary_changed_top() == False:
#        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
#        led1_on()
#        time.sleep(0.2)
#        update_screen(splash, macro_names[18], display)

    if not SW1.value:
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.ENTER)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[5], display)
        
    if not SW2.value:
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.K)
        led1_on()
#        time.sleep(0.2)
        update_screen(splash, macro_names[8], display)

#    if not SW3.value:
#        cc.send(ConsumerControlCode.MUTE)
#        led1_on()
#        time.sleep(0.2)
#        update_screen(splash, macro_names[19], display)

    time.sleep(0.0001)
