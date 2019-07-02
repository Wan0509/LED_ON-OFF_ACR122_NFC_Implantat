#!/usr/bin/python
from smartcard.scard import *
from smartcard.util import     toHexString

import RPi.GPIO as GPIO
# import MFRC522
import signal
import time
import lcddriver

lcd = lcddriver.lcd()
lcd.lcd_clear()

#lcd.lcd_display_string("Bitte Chip", 1)
#lcd.lcd_display_string("auflegen", 2)

def s():
    while 1:
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        assert hresult==SCARD_S_SUCCESS
        hresult, readers = SCardListReaders(hcontext, [])
        assert len(readers)>0
        reader = readers[0]
        hresult, hcard, dwActiveProtocol = SCardConnect(
            hcontext,
            reader,
            SCARD_SHARE_SHARED,
            SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
        time.sleep(1)
        try:
            hresult, response = SCardTransmit(hcard,dwActiveProtocol,[0xFF,0xCA,0x00,0x00,0x04])
            uid = toHexString(response, format=0)
            print (uid)

            if uid == "04 4A CE 12 90 00":
                # how to count the Pins
                GPIO.setmode(GPIO.BOARD)
                # get Pin 12  as output
                GPIO.setup(12, GPIO.OUT)
        
                # ask if output is low
                if GPIO.input(12) == GPIO.LOW:
                    # if output is low print this message
                    print ("Licht wird angeschalten")
                    lcd.lcd_clear()
                    lcd.lcd_display_string ("Licht wird ", 1)
                    lcd.lcd_display_string ("angeschaltet", 2)
                    time.sleep(1.5)
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Bitte Chip", 1)
                    lcd.lcd_display_string("auflegen", 2)
                    print ("Bitte Chip auflegen")
                    # and set output to high (switch the light on)
                    GPIO.output(12, GPIO.HIGH)
            
                # outherwise is output is high
                elif GPIO.input(12) == GPIO.HIGH:
                    # printthis message
                    print ("Licht wird ausgeschaltet")
                    lcd.lcd_clear()
                    lcd.lcd_display_string ("Licht wird", 1)
                    lcd.lcd_display_string ("ausgeschaltet", 2)
                    time.sleep(1.5)
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Bitte Chip", 1)
                    lcd.lcd_display_string("auflegen", 2)
                    print ("Bitte Chip auflegen")
                    #and set the output to low (switch the light off)
                    GPIO.output(12, GPIO.LOW)
                    GPIO.cleanup()
            else:
                #if the RFID Card isn't the one we are looking for
                print ("Unknown/Wrong RFID Modul")
                lcd.lcd_clear()
                lcd.lcd_display_string("Falscher Chip", 1)
                time.sleep(1.5)
                lcd.lcd_clear()
                lcd.lcd_display_string("Bitte Chip", 1)
                lcd.lcd_display_string("auflegen", 2)
                #print ("Bitte Chip auflegen")
            
        except SystemError:
            print ("no card found")

s()

