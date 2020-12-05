#!/usr/bin/env python3
"""
Usage: cappi <something> [--foo=<bar>]

Options: 
--foo=<bar>  my flag [default: bardefault]
"""
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd


#from docopt import docopt

def main():
 #   args = docopt(__doc__)
    print("Cap Pi :hello")

def testScreen(self):
    lcd_columns = 16
    lcd_rows = 2
    i2c = busio.I2C(board.SCL, board.SDA)
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
    lcd.color = [100, 0, 0]
    lcd.message = "Hello\nCircuitPython"


if __name__ == '__main__':
    main()
