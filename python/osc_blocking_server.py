from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from analyse import *
from oled.affichage import *

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



def tri_velo(arguments):
        #print("trivelo",arguments)
        global lastIdRack, lastIdInstru, lastIdPas
        list_velos[lastIdRack-1][lastIdInstru-1][lastIdPas]=arguments[0]
        #print(list_velos[lastIdInstru])


def tri_mute():
    global lastIdRack,lastIdInstru
    if list_mute[lastIdRack-1][lastIdInstru-1]==True:
        list_mute[lastIdRack-1][lastIdInstru-1]=False
    elif list_mute[lastIdRack-1][lastIdInstru-1]==False:
        list_mute[lastIdRack-1][lastIdInstru-1]=True

def tri_rackMute():
    global lastIdRack
    if list_rack_mute[lastIdRack-1]==True:
        list_rack_mute[lastIdRack-1]=False
    elif list_rack_mute[lastIdRack-1]==False:
        list_rack_mute[lastIdRack-1]=True


def clear_velo():
    global lastIdInstru, lastIdRack
    list_vol[lastIdRack-1][lastIdInstru-1]=0.5
    list_mute[lastIdRack-1][lastIdInstru-1]=False
    list_mesure[lastIdRack-1][lastIdInstru-1]=[0,16]
    i=0
    while i<64:
        list_velos[lastIdRack-1][lastIdInstru-1][i]=0
        i+=1

def clear_rack_velo():
    global lastIdRack
    i=0
    j=0
    while j<nbPlayers:
        list_vol[lastIdRack-1][j]=0.5
        list_mute[lastIdRack-1][j]=False
        list_mesure[lastIdRack-1][j]=[0,16]
        while i<64:
            list_velos[lastIdRack-1][j][i]=0
            i+=1
        j+=1
        i=0

def saveSet():
    name=chemin+saveName+".txt"
    file = open(name,'w')
    file.write(str(lastBpm)+'\n')
    file.write(str(lastMasterVol)+'\n')
    for i in range(0,nbRack):
        file.write(folders[lastKit[i]]+',')
    file.write('\n')
    file.close() #to change file access modes


def default_handler(address, *args):
    print(address,args)
    global lastIdRack,lastIdInstru, lastIdPas, lastPas, list_velos,lastIdMenu,list_mute,lastBpm,isPlaying,lastNbMesures,lastMasterVol, lastKit, mode
    if(address=="/validSave"):
        saveSet();
    if(address=="/idMenu"):
        lastIdMenu=round(args[0])
    if(address=="/idRack"):
        lastIdRack=round(args[0])
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
    if(address=="/muteRackId"):
        tri_rackMute()
    if(address=="/clear"):
        clear_velo()
    if(address=="/clearRack"):
        clear_rack_velo()
    if(address=="/trackVol"):
        list_vol[lastIdRack-1][lastIdInstru-1]=round(args[0]*10)/10
    if(address=="/switchMode"):
        mode=round(args[0])
    if(address=="/BPM"):
        lastBpm=round(args[0])
    if(address=="/playPause"):
        isPlaying=round(args[0])
    if(address=="/beginMesure"):
        list_mesure[lastIdRack-1][lastIdInstru-1][0]=round(args[0])
    if(address=="/endMesure"):
        list_mesure[lastIdRack-1][lastIdInstru-1][1]=round(args[0])
    if(address=="/masterVol"):
        lastMasterVol=round(args[0]*100)
    if(address=="/masterRack"):
        master_rack[lastIdRack-1]=round(args[0]*100)
    if(address=="/askFiles"):
        lastKit[lastIdRack-1]=round(args[0])
        analFiles(lastIdRack,lastKit[lastIdRack-1])
    if(address=="/askFolders"):
        analFolders()
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

dispatcher = Dispatcher()
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever
