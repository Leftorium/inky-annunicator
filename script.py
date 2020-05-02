import requests
import json
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
# Get the current message on the annunciator
response = requests.get('https://dm-devci-annunciator-services.azurewebsites.net/api/Message/message/0/current')
data = response.json()
message = data['slides'][0]['lines'][0]['content']
# Inky section shamelessly stolen from their guide https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat
inkyphat = InkyPHAT('red')
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FredokaOne, 22)
w, h = font.getsize(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2)
draw.text((x, y), message, inky_display.RED, font)
inky_display.set_image(img)
inky_display.show()
