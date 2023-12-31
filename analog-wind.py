#!/usr/bin/env python3

import sys
import time

import automationhat
time.sleep(0.1) # Short pause after ads1015 class creation recommended

try:
    from PIL import Image, ImageFont, ImageDraw
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

import ST7735 as ST7735

try:
    from fonts.ttf import RobotoBlackItalic as UserFont
except ImportError:
    print("""This example requires the Roboto font.
Install with: sudo pip{v} install fonts font-roboto
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

# Create ST7735 LCD display class.
disp = ST7735.ST7735(
    port=0,
    cs=ST7735.BG_SPI_CS_FRONT,
    dc=9,
    backlight=25,
    rotation=270,
    spi_speed_hz=4000000
)

# Initialise display.
disp.begin()

colour = (255, 181, 86)
font = ImageFont.truetype(UserFont, 12)

# Values to keep everything aligned nicely.
text_x = 110
text_y = 34

bar_x = 25
bar_y = 37
bar_height = 8
bar_width = 73

while True:
    # Value to increment for spacing text and bars vertically.
    offset = 0

    # Open our background image.
    image = Image.open("images/analog-inputs-blank.jpg")
    draw = ImageDraw.Draw(image)

    # Draw the text and bar for each channel in turn.
    reading = automationhat.analog.one.read()
        #ms = reading * 1000 * 0.003
        #mph = ms * 2.23694
    mph = reading * 6.704082
    print ("{0:.2f} mph".format(mph))
    draw.text((text_x, text_y + offset), "{reading:.2f}".format(reading=reading), font=font, fill=colour)

    # Scale bar dependent on channel reading.
    width = int(bar_width * (reading / 24.0))

    draw.rectangle((bar_x, bar_y + offset, bar_x + width, bar_y + bar_height + offset), colour)

    offset += 14

    # Draw the image to the display.
    disp.display(image)

    time.sleep(1.5)
