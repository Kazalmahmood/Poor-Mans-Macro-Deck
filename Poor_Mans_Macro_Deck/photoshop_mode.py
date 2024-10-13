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
        0: "Show/Hide Extras",
        1: "Resize Image",
        2: "Free Transform",
        3: "Curves",
        4: "Deselect",
        5: "Select Inverse",
        6: "Color Range",
        7: "Trim",
        8: "Export As",
        9: "Quic Export as PNG",
        10: "Save for Web",
        11: "Brightness Up",
        12: "Brightness Down",
        13: "Monitor Off",
        14: "Play Next",
        15: "Play Previous",
        16: "Play/Pause",
        17: "Volume Up",
        18: "Volume Down",
        19: "Mute/Unmute",
        # Add more macro names and their corresponding keys as needed
    }

    if event and event.pressed and event.key_number == 0:
        keyboard.send(Keycode.CONTROL, Keycode.H)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[0], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 1:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.I)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[1], display)

    if event and event.pressed and event.key_number == 2:
        keyboard.send(Keycode.CONTROL, Keycode.T)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[2], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 3:
        keyboard.send(Keycode.CONTROL, Keycode.M)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[3], display)

    if event and event.pressed and event.key_number == 4:
        keyboard.send(Keycode.CONTROL, Keycode.D)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[4], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 5:
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.I)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[5], display)

    if event and event.pressed and event.key_number == 6:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.H)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[6], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 7:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.Q)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[7], display)

    if event and event.pressed and event.key_number == 8:
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.ALT, Keycode.W)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[8], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 9:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.Y)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[9], display)

    if event and event.pressed and event.key_number == 10:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.S)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[10], display)


    #Rotary encoder turned clockwise
#    if rotary_changed_top() == True:
#        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
#        led1_on()
#        #time.sleep(0.2)
#        update_screen(splash, macro_names[17], display)
#        
#    elif rotary_changed_top() == False:
#        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
#        led1_on()
#        #time.sleep(0.2)
#        update_screen(splash, macro_names[18], display)
    
    #Rotary encoder turned clockwise
    # if rotary_position_2() == True:
        # cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
        # led1_on()
        # time.sleep(0.5)
        # update_screen(splash, macro_names[14], display)
        # 
    # elif rotary_position_2() == False:
        # cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        # led1_on()
        # time.sleep(0.5)
        # update_screen(splash, macro_names[15], display)

    if rotary_position_1() == True:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.D)
        led1_on()
        time.sleep(0.5)
        update_screen(splash, macro_names[11], display)
        
    elif rotary_position_1() == False:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.I)
        led1_on()
        time.sleep(0.5)
        update_screen(splash, macro_names[12], display)
        
#    if not SW3.value:
#        cc.send(ConsumerControlCode.MUTE)
#        led1_on()
#        time.sleep(0.2)
#        update_screen(splash, macro_names[19], display)
        
    if not SW2.value:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[16], display)

    if not SW1.value:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.M)
        led1_on()
        #time.sleep(0.2)
        update_screen(splash, macro_names[13], display)

    time.sleep(0.0001)
