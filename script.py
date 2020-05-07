import requests
import json
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
# Get the current message on the annunciator
response = requests.get('https://dm-devci-annunciator-services.azurewebsites.net/api/Message/message/0/current')
data = response.json()
currentCommons = data['slides'][0]['lines']
totalMess = len(currentCommons)
messagePayload = totalMess - 1
i = 0
holder = []
while messagePayload > i:
    holder.append(data['slides'][0]['lines'][i]['content'])
    i += 1
message = ' '.join(holder).title()

# Inky section shamelessly stolen from their guide https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FredokaOne, 16)
w, h = font.getsize(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2)

# Reflow function from https://www.adambowie.com/blog/2019/09/news-twitter-feeds-and-inky-what-e-ink-display/

def reflow_text(quote, width, font):
    words = quote.split(" ")
    reflowed = ' '
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n " + word

    # reflowed = reflowed.rstrip() + '"'

    return reflowed
reflowed_message = reflow_text(message, inky_display.WIDTH, font)
draw.text((0, 0), reflowed_message, inky_display.BLACK, font)
inky_display.set_image(img)
inky_display.show()
