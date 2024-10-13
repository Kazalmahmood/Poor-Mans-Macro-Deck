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
    macro_label = label.Label(terminalio.FONT, text=macro_name, color=0x000000, x=center_x, y=50)
    splash.append(macro_label)
    display.refresh()
    # Wait for 1 seconds
    time.sleep(0.05)
    # Remove the macro label after 1 seconds
    splash.remove(macro_label)
    display.refresh()


def handle_keypress(event, cc, led1_on, write_text, keyboard, SW1, SW2, SW3, rotary_position_1, splash, display):

    # Macro names or actions
    # Change the macro names * 
    macro_names = {
        0: "File Explorer",
        1: "VS Code",
        2: "Microsoft Edge",
        3: "Firefox",
        4: "Brave",
        5: "Chrome",
        6: "Spotify",
        7: "Snipping Tool",
        8: "Copy",
        9: "Paste",
        10: "Windows Lock",
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
        keyboard.send(Keycode.GUI, Keycode.E)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[0], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 1:
        keyboard.send(Keycode.CONTROL, Keycode.F2)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[1], display)

    if event and event.pressed and event.key_number == 2:
        keyboard.send(Keycode.CONTROL, Keycode.F3)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[2], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 3:
        keyboard.send(Keycode.CONTROL, Keycode.F4)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[3], display)

    if event and event.pressed and event.key_number == 4:
        keyboard.send(Keycode.CONTROL, Keycode.F5)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[4], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 5:
        keyboard.send(Keycode.CONTROL, Keycode.F6)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[5], display)

    if event and event.pressed and event.key_number == 6:
        keyboard.send(Keycode.CONTROL, Keycode.F8)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[6], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 7:
        keyboard.send(Keycode.CONTROL, Keycode.F9)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[7], display)

    if event and event.pressed and event.key_number == 8:
        keyboard.send(Keycode.CONTROL, Keycode.C)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[8], display)

        #update_screen(splash, macro_names[0], display)
    if event and event.pressed and event.key_number == 9:
        keyboard.send(Keycode.CONTROL, Keycode.V)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[9], display)

    if event and event.pressed and event.key_number == 10:
        keyboard.send(Keycode.GUI, Keycode.L)
        led1_on()
        # time.sleep(0.05)
        update_screen(splash, macro_names[10], display)

    #Rotary encoder turned clockwise
#    if rotary_position_2() == True:
#        print("SCAN_NEXT_TRACK")
#        cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
#        led1_on()
#        time.sleep(0.5)
#        update_screen(splash, macro_names[17], display)
#        
#    elif rotary_position_2() == False:
#        print("SCAN_PREVIOUS_TRACK")
#        cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
#        led1_on()
#        time.sleep(0.5)        
#        update_screen(splash, macro_names[18], display)

    #Rotary encoder turned clockwise
    if rotary_position_1() == True:
        print("Brightness Down")
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.D)
        led1_on()
        time.sleep(0.5)
        update_screen(splash, macro_names[17], display)

        
    elif rotary_position_1() == False:
        print("Brightness Up")
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.I)
        led1_on()
        time.sleep(0.5)
        update_screen(splash, macro_names[18], display)
    
        
    if not SW2.value:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[16], display)

    if not SW1.value:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.M)
        led1_on()
        #time.sleep(0.05)
        update_screen(splash, macro_names[13], display)

    time.sleep(0.0001)
