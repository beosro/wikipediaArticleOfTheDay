#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in7b
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import feedparser, re, textwrap

fontSize = 13
lineWidth = 40

url = 'https://de.wikipedia.org/w/api.php?action=featuredfeed&feed=featured&feedformat=atom'
feed = feedparser.parse(url)

clean = re.compile('<.*?>|&.*?;')
summary = re.sub(clean, '', feed['entries'][-1]['summary_detail']['value']).strip()
print(feed['entries'][-1])

try:
    epd = epd2in7b.EPD()
    epd.init()
    print("Clear...")
    epd.Clear(0xFF)
    
    # Drawing on the Horizontal image
    HBlackimage = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 298*126
    HRedimage = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 298*126    
    
    # Horizontal
    print("Drawing")
    drawblack = ImageDraw.Draw(HBlackimage)
    drawred = ImageDraw.Draw(HRedimage)
    font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', fontSize)
    heading = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', fontSize + 4)
    drawred.rectangle((0,0,298, fontSize + 4), fill=0  )
    drawred.text((5, 0), feed['entries'][-1]['title'], font = font, fill = 255)

    lines = textwrap.wrap(summary, width=lineWidth)

    i = 1
    for line in lines:
        drawblack.text((0, (i * fontSize)+ 4), line, font = font, fill = 0)
        i+=1
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
    epd.sleep()
        
except :
    print ('traceback.format_exc():\n%s',traceback.format_exc())
    exit()
