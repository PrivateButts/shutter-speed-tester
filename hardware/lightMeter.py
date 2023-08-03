import asyncio
from time import sleep
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from analogio import AnalogIn

# Set up the light sensor
meter = AnalogIn(board.A1)

displayio.release_displays()

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(128, 32, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(118, 24, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
splash.append(inner_sprite)

# Draw a label
text = "Light Meter"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
splash.append(text_area)

sleep(2)


[splash.remove(x) for x in splash]

text = "Waiting for samples"
meter_display = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=15)
splash.append(meter_display)

sample_display = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=25)
splash.append(sample_display)


samples = []
async def sample():
    print("Starting average")
    while True:
        sample_display.text = "Samples: %d" % len(samples)
        samples.append(meter.value)
        await asyncio.sleep(0)


async def average():
    print("Starting average")
    while True:
        if len(samples) > 0:
            avg = sum(samples) / len(samples)
            meter_display.text = "Light: %d" % avg
            print("Light: %d" % avg)
            samples.clear()
        await asyncio.sleep(1)


async def main():
    while True:
        await asyncio.gather(sample(), average())

print("Starting Logger")
asyncio.run(main())
