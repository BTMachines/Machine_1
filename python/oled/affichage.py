
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from osc_send import *
from list_repository import *

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



def affSaveMenu(inventory):
    
    name=inventory["saveName"]
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((10,10),"SAVE",  font=font, fill=255)
    draw.text((10,25),"press edit to save",  font=font, fill=255)
    draw.text((10,40),"name:"+name,  font=font, fill=255)
    disp.image(image)
    disp.display()
    
def affLoadMenu(inventory):
    fileSaves=listSaves()
    print("affloadMenu/lastIdLoad:",inventory["lastLoadId"])
    print("filesSaves:",fileSaves)
    name=fileSaves[inventory["lastLoadId"]]
    print("name :",name)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((10,10),"lOAD",  font=font, fill=255)
    draw.text((10,25),"scroll and load set",  font=font, fill=255)
    draw.text((10,40),name,  font=font, fill=255)
    disp.image(image)
    disp.display()
    
def affIsLoading():
 
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=255)
    draw.text((10,28),"LOADING ...",  font=font, fill=0)
    disp.image(image)
    disp.display()
    

def affMainMenu(inventory):
    
    bpm=inventory["lastBpm"]
    play=inventory["isPlaying"]
    master=inventory["lastMasterVol"]
    recOn=inventory["recIsOn"]
    
    if play==1:
        playTitle="Playing"
    elif play==2:
        playTitle="Stoped"
    else:
        playTitle="Paused"
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.rectangle((0,0,34,12), outline=0, fill=255)
    
    if recOn==True:
        draw.ellipse((117,2,125,10), outline=0, fill=255)


    #font = ImageFont.load_default()
    draw.text((2,0),"BTM_1",  font=font, fill=0)
    draw.text((0,20),playTitle,  font=font, fill=255)
    draw.text((0,35),"master:"+(str(master))+"%",  font=font, fill=255)
    draw.text((0,50),"bpm:"+str(round(bpm)),  font=font, fill=255)

    disp.image(image)
    disp.display()
    
def affRackMenu(inventory):
    
    
    idRack=inventory["lastIdRack"]-1
    kitName=folders[inventory["lastKit"][idRack]]
    listMute=inventory["list_rack_mute"]
    mode=inventory["mode"]
    vol= inventory["master_rack"][idRack]
        
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)   
    draw.text((0,0),"Rack: "+str(idRack+1),  font=font, fill=255)
    draw.text((64,0),"vol: "+str(vol)+"%",  font=font, fill=255)
    draw.text((0,50),"kit: "+kitName,  font=font, fill=255)

    if mode==1:
        draw.rectangle((107,0,117,10), outline=0, fill=255)
        draw.text((110,0),"C",  font=font, fill=0)

    j=0
    i=0
    idCount=0
    while j<2:
        while i<4: 
            draw.text((i*carre2_width,marge_top+j*carre2_height-1),str(idCount+1),  font=font, fill=255)

            if idCount==idRack:
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
    

def affTrackMenu(inventory):
    
    idRack=inventory["lastIdRack"]-1
    idInstru=inventory["lastIdInstru"]-1 
    kitName=folders[inventory["lastKit"][idRack]]
    fileNames=finalFilesNames
    listMute=inventory["list_mute"][idRack]
    mode=inventory["mode"]
    vol= inventory["list_vol"][idRack][idInstru]
    beginEnd= inventory["list_mesure"][idRack][idInstru]


    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #font = ImageFont.load_default()
    draw.text((0,0),str(idRack+1)+":"+kitName+": "+fileNames[idRack][idInstru],  font=font, fill=255)
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

            if idCount==idInstru:
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

def affSeq(inventory):

    idRack= inventory["lastIdRack"]-1
    idInstru= inventory["lastIdInstru"]-1
    nameInstru= finalFilesNames[idRack]
    idPas= inventory["lastIdPas"]
    pas= inventory["lastPas"]
    listVelo= inventory["list_velos"][idRack][idInstru]
    vol= inventory["list_vol"][idRack][idInstru]
    beginEnd= inventory["list_mesure"][idRack][idInstru]

    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #font = ImageFont.load_default()
    draw.text((0,0),str(idInstru+1)+" / "+nameInstru[idInstru],  font=font, fill=255)
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
    
