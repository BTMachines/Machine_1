from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from analyse import *
from commandes import *
from tri_com import *
from oled.affichage import *
import datetime


chemin="/home/pi/Bureau/BTMachines_git/Machine_1/saves/"
saveName="default"

lastIdInstru=1
lastIdRack=1
lastIdPas=0
lastPas=0
lastIdMenu=0
lastBpm=0
isPlaying=0
nbPlayers=12
nbRack=4
lastMasterVol=0
lastKit=[]
lastLoadId=0
mode=0
list_vol=[]
list_mesure=[]

list_velos=[]
list_mute=[]
list_rack_mute=[]
master_rack=[]
j=0
i=0
h=0
while j<nbRack:
    list_vol.append([])
    list_mute.append([])
    list_velos.append([])
    list_mesure.append([])
    lastKit.append(0)
    analFiles(j+1,lastKit[j])
    list_rack_mute.append(False)
    master_rack.append(50)
    while i<nbPlayers:
        list_vol[j].append(0.5)
        list_mute[j].append(False)
        list_velos[j].append([])
        list_mesure[j].append([0,16])

        while h<64:
            list_velos[j][i].append(0)
            h+=1
        i+=1
        h=0
    j+=1
    i=0


def default_handler(address, *args):
    print("default_handler: ",address,*args)
    toto()
    triCom(address,*args)

    if lastIdMenu==3:
        affSeq(lastIdRack,lastIdInstru,finalFilesNames[lastIdRack-1],lastIdPas,lastPas,list_velos[lastIdRack-1][lastIdInstru-1],list_vol[lastIdRack-1][lastIdInstru-1],list_mesure[lastIdRack-1][lastIdInstru-1])
    if lastIdMenu==2:
        affTrackMenu(folders[lastKit[lastIdRack-1]],lastIdRack,finalFilesNames,lastIdInstru,list_mute[lastIdRack-1],mode,list_vol[lastIdRack-1][lastIdInstru-1],list_mesure[lastIdRack-1][lastIdInstru-1])
    if lastIdMenu==1:
        affRackMenu(lastIdRack,list_rack_mute,folders[lastKit[lastIdRack-1]],mode,master_rack[lastIdRack-1])
    if lastIdMenu==0:
        affMainMenu(lastBpm,isPlaying,lastMasterVol)
    if lastIdMenu==-1:
        affSaveMenu(saveName)
    if lastIdMenu==-2:
        affLoadMenu(filesSaves[lastLoadId])

dispatcher = Dispatcher()
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
port = 1337


server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever

