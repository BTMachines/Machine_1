
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
carre2_size=6
marge_top=20
marge_top2=15

carre_height=(height-marge_top)/4
carre2_height=(height-marge_top)/4

lastpas=0
font = ImageFont.load_default()
playTitle="paused"



def affSaveMenu(name):
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=255)
    draw.text((10,10),"save menu",  font=font, fill=0)
    draw.text((10,30),"name:"+name,  font=font, fill=0)
    disp.image(image)
    disp.display()
    
def affLoadMenu(name):
    nakedname=name[:-4]
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=255)
    draw.text((10,10),"load menu",  font=font, fill=0)
    draw.text((10,30),"name:"+nakedname,  font=font, fill=0)
    disp.image(image)
    disp.display()
    

def affMainMenu(bpm, play,master):
    
    if play==1:
        playTitle="Playing"
    elif play==2:
        playTitle="Stoped"
    else:
        playTitle="Paused"
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.rectangle((0,0,34,12), outline=0, fill=255)

    #font = ImageFont.load_default()
    draw.text((2,0),"BTM_1",  font=font, fill=0)
    draw.text((0,20),playTitle,  font=font, fill=255)
    draw.text((0,35),"bpm:"+str(round(bpm)),  font=font, fill=255)
    draw.text((0,50),"master:"+(str(master))+"%",  font=font, fill=255)

    disp.image(image)
    disp.display()
    
def affRackMenu(idRack,listMute,kitName,mode,vol):
    
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)   
    draw.text((0,0),"Racks: "+str(idRack),  font=font, fill=255)
    draw.text((0,37),"kit: "+kitName,  font=font, fill=255)
    draw.text((0,55),"vol: "+str(vol)+"%",  font=font, fill=255)

    if mode==1:
        draw.rectangle((107,0,117,10), outline=0, fill=255)
        draw.text((110,0),"C",  font=font, fill=0)

    j=0
    i=0
    idCount=0
    while j<1:
        while i<4: 
            draw.text((i*carre2_width,marge_top+j*carre2_height-1),str(idCount+1),  font=font, fill=255)

            if idCount==idRack-1:
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
    

def affTrackMenu(kitName,idRack,fileNames,idInstru,listMute,mode,vol,beginEnd):
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #font = ImageFont.load_default()
    draw.text((0,0),str(idRack)+":"+kitName+": "+fileNames[idRack-1][idInstru-1],  font=font, fill=255)
    draw.text((0,55),"vol:"+str(round(vol*100))+"%",  font=font, fill=255)
    draw.text((64,55),"mesure:"+str(round(beginEnd[1]/4)),  font=font, fill=255)
    if mode==1:
        draw.rectangle((107,0,117,10), outline=0, fill=255)
        draw.text((110,0),"C",  font=font, fill=0)

        
    #draw.text((40,0),str(idInstru),  font=font, fill=255)
    #if listMute[idInstru-1]==True:
    #    draw.text((70,0),"mute",  font=font, fill=255)
    
    j=0
    i=0
    idCount=0
    while j<3:
        while i<4: 
            draw.text((i*carre2_width,marge_top+j*carre2_height-1),str(idCount+1),  font=font, fill=255)

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

def affSeq(idRack,idInstru,nameInstru,idPas,pas,listVelo,vol,beginEnd):


    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #font = ImageFont.load_default()
    draw.text((0,0),str(idInstru)+" / "+nameInstru[idInstru-1],  font=font, fill=255)
    #draw.text((30,0),str(round(idPas)),  font=font, fill=255)
    draw.rectangle((96,0,123,10), outline=0, fill=255)
    draw.text((98,0),str(round(listVelo[idPas]*100))+"%",  font=font, fill=0)
    draw.text((0,55),"vol:"+str(round(vol*100))+"%",  font=font, fill=255)
    idPas=round(idPas);
    
    
    i=0
    j=0
    idCount=0
    col=0
    xInc=0
    margeInterval=3
    end=beginEnd[0]+beginEnd[1]-1
    if end>=64:
        end-=64
    
    while j<4:
        while i<16: 
            x=3+i*carre_width+xInc
            y=marge_top+j*(carre_height-3)
            if listVelo[idCount]!=0:
                col=255
            else:
                col=0
            draw.rectangle((x,y,x+carre_size,y+carre_size), outline=255, fill=col) #center 
            if (pas)==idCount:
                draw.rectangle((x,y+carre_size,x+carre_size,y+carre_size+1), outline=255, fill=255) #center 
            if idPas==idCount:
                draw.rectangle((x,y,x+carre_size,y-1), outline=255, fill=255) #center 
            if beginEnd[0]==idCount:
                draw.rectangle((x-3,y,x-2,y+carre_size), outline=255, fill=255) #center 
            if end==idCount:
                draw.rectangle((x+carre2_size+1,y,x+carre_size+2,y+carre_size), outline=255, fill=255) #center 
            idCount+=1
            i+=1
            if i%4==0:
                xInc+=margeInterval
        j+=1
        i=0
        xInc=0

    disp.image(image)
    disp.display()
    
