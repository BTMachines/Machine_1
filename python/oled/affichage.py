
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)


disp.begin()
disp.clear()
disp.display()

last=[0,0,0]


width = disp.width
height = disp.height
image = Image.new('1', (width, height))
carre_width=width/18
carre_size=4
carre2_width=width/4
carre2_size=8
marge_top=20
carre_height=(height-marge_top)/4
carre2_height=(height-marge_top)/3

lastpas=0
font = ImageFont.load_default()
playTitle="paused"




def affMainMenu(bpm, play):
    
    if play==1:
        playTitle="Play"
    elif play==2:
        playTitle="Stoped"
    else:
        playTitle="Paused"
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #font = ImageFont.load_default()
    draw.text((0,0),playTitle,  font=font, fill=255)
    draw.text((0,20),"bpm",  font=font, fill=255)
    draw.text((20,20),str(round(bpm)),  font=font, fill=255)


    disp.image(image)
    disp.display()

def affMenu(idInstru,listMute):
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #font = ImageFont.load_default()
    draw.text((0,0),"track",  font=font, fill=255)
    draw.text((40,0),str(idInstru),  font=font, fill=255)
    if listMute[idInstru-1]==True:
        draw.text((70,0),"mute",  font=font, fill=255)
    
    j=0
    i=0
    idCount=0
    while j<3:
        while i<4: 
            draw.text((i*carre2_width,marge_top+j*carre2_height),str(idCount+1),  font=font, fill=255)

            if idCount==idInstru-1:
                draw.rectangle((i*carre2_width+15,marge_top+j*carre2_height,i*carre2_width+12,marge_top+j*carre2_height+carre2_size), outline=255, fill=255) #center 

            if listMute[idCount]==False:
                draw.rectangle((i*carre2_width+15,marge_top+j*carre2_height,i*carre2_width+carre2_size+15,marge_top+j*carre2_height+carre2_size), outline=255, fill=0) #center 
            else:  
                draw.rectangle((i*carre2_width+18,marge_top+j*carre2_height+3,i*carre2_width+carre2_size+12,marge_top+j*carre2_height+carre2_size-3), outline=255, fill=255) #center 
            i+=1
            idCount+=1
        j+=1
        i=0
    disp.image(image)
    disp.display()

def affSeq(idInstru,idPas,pas,listVelo):


    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #font = ImageFont.load_default()
    draw.text((0,0),str(round(idInstru)),  font=font, fill=255)
    draw.text((30,0),str(round(idPas)),  font=font, fill=255)
    draw.text((60,0),str(listVelo[idPas]),  font=font, fill=255)
    #draw.text((20,0),str(round(idPas)),  font=font, fill=255)
    idPas=round(idPas);
    #print("idpas : ",idPas)
    i=0
    per_line=16
    pas_pos=[0,0,0]
    reste=idPas
    j=0
    i=0
    pas=pas*4
    
    
    
    while j<3:
        while i<4:
            if reste>=i*per_line:
                pas_pos[j]=i;
            i+=1
        #print("pos",j,":",pas_pos[j])
        i=0
        j+=1
        reste=reste-pas_pos[j-1]*per_line
        #print("reste",j,": ",reste)
        per_line=per_line/4
        
    j=0
    idCount=0
    col=0
    xInc=0
    margeInterval=4
    
    while j<4:
        while i<16: 
            if listVelo[idCount]!=0:
                col=255
            else:
                col=0
            draw.rectangle((i*carre_width+xInc,marge_top+j*carre_height,i*carre_width+carre_size+xInc,marge_top+j*carre_height+carre_size), outline=255, fill=col) #center 
            if pas==idCount:
                draw.rectangle((i*carre_width+xInc,marge_top+j*carre_height+carre_size,i*carre_width+carre_size+xInc,marge_top+j*carre_height+carre_size+1), outline=255, fill=255) #center 

            
            idCount+=1
            i+=1
            if i%4==0:
                xInc+=margeInterval
        j+=1
        i=0
        xInc=0

    pos_1=pas_pos[1]*carre_width*4+pas_pos[2]*carre_width+pas_pos[1]*margeInterval
    draw.rectangle((pos_1,marge_top+pas_pos[0]*carre_height,pos_1+carre_size,marge_top+pas_pos[0]*carre_height-3), outline=255, fill=255) #center 
    
    disp.image(image)
    disp.display()
    
