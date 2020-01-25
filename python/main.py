from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from analyse import *
from commandes import *
from tricom import *
from oled.affichage import *


inventaire={
    "chemin":"/home/pi/Bureau/BTMachines_git/Machine_1/saves/python/",
    "saveName":"default",
    "lastIdInstru":1,
    "lastIdRack":1,
    "lastIdPas":0,
    "lastPas":0,
    "lastIdMenu":0,
    "lastBpm":0,
    "isPlaying":0,
    "nbPlayers":12,
    "nbRack":4,
    "lastMasterVol":0,
    "lastKit":[],
    "lastLoadId":0,
    "mode":0,
    "list_vol":[],
    "list_mesure":[],
    "list_velos":[],
    "list_mute":[],
    "list_rack_mute":[],
    "master_rack":[],
    "recIsOn":False
    }
    
def updateInventaire(inventory):
    global inventaire
    inventaire=inventory
    


def initParams():
    global inventaire
    j=0
    i=0
    h=0

    for cle, valeur in inventaire.items():

        while j<inventaire["nbRack"]:
            analFiles(j+1,0)
            inventaire["list_vol"].append([])
            inventaire["list_mute"].append([])
            inventaire["list_velos"].append([])
            inventaire["list_mesure"].append([])
            inventaire["lastKit"].append(0)
            inventaire["list_rack_mute"].append(False)
            inventaire["master_rack"].append(50)
            while i<inventaire["nbPlayers"]:
                inventaire["list_vol"][j].append(0.5)
                inventaire["list_mute"][j].append(False)
                inventaire["list_velos"][j].append([])
                inventaire["list_mesure"][j].append([0,16])

                while h<64:
                    inventaire["list_velos"][j][i].append(0)
                    h+=1
                i+=1
                h=0
            j+=1
            i=0



def default_handler(address, *args):
    global inventaire
    #print("default_handler: ",address,*args)
    inventaire=triCom(inventaire,address,*args)

    if inventaire["lastIdMenu"]==3:
        affSeq(inventaire)
    if inventaire["lastIdMenu"]==2:
        affTrackMenu(inventaire)
    if inventaire["lastIdMenu"]==1:
        affRackMenu(inventaire)
    if inventaire["lastIdMenu"]==0:
        affMainMenu(inventaire)
    if inventaire["lastIdMenu"]==-1:
        affSaveMenu(inventaire)
    if inventaire["lastIdMenu"]==-2:
        affLoadMenu(inventaire)
        

initParams()

dispatcher = Dispatcher()
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
port = 1337


server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever

