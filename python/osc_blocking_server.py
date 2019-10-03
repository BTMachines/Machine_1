from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from oled.affichage import *

lastIdInstru=1
lastIdPas=0
lastPas=0
lastIdMenu=0
lastBpm=0
isPlaying=0

list_velos=[[],[],[],[]]
list_mute=[]
i=0
while i<12:
    list_mute.append(False)
    i+=1


i=0
j=0
while j<4:
    while i<64:
        list_velos[j].append(0)
        i+=1
    i=0
    j+=1


def tri_velo(arguments):
        #print("trivelo",arguments)
        global lastIdInstru, lastIdPas
        list_velos[lastIdInstru-1][lastIdPas]=arguments[0]
        #print(list_velos[lastIdInstru])


def tri_mute():
    global lastIdInstru
    if list_mute[lastIdInstru-1]==True:
        list_mute[lastIdInstru-1]=False
    elif list_mute[lastIdInstru-1]==False:
        list_mute[lastIdInstru-1]=True

def clear_velo():
    global lastIdInstru
    i=0
    while i<64:
        list_velos[lastIdInstru-1][i]=0
        i+=1



def default_handler(address, *args):
    print(address,args)
    global lastIdInstru, lastIdPas, lastPas, list_velos,lastIdMenu,list_mute,lastBpm,isPlaying
    if(address=="/idMenu"):
        lastIdMenu=round(args[0])
    if(address=="/idInstru"):
        lastIdInstru=round(args[0])
    if(address=="/idPas"):
        lastIdPas=round(args[0])
        #print("idPas:",lastIdPas)
    if(address=="/pas"):
        lastPas=round(args[0])
    if(address=="/velo"):
        tri_velo(args)
    if(address=="/muteId"):
        tri_mute()
    if(address=="/clear"):
        clear_velo()
    if(address=="/BPM"):
        lastBpm=round(args[0])
    if(address=="/playPause"):
        isPlaying=round(args[0])
    if lastIdMenu==2:
        affSeq(lastIdInstru,lastIdPas,lastPas,list_velos[lastIdInstru-1])
    if lastIdMenu==1:
        affMenu(lastIdInstru,list_mute)
    if lastIdMenu==0:
        affMainMenu(lastBpm,isPlaying)


dispatcher = Dispatcher()
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever

