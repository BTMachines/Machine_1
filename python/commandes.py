#from osc_send import sendRecDate,sendRecOff
from osc_send import *
import datetime
import pickle
from list_repository import *


inventaire={}

def cmdReceiveInventory(inventory):
    global inventaire
    inventaire=inventory
    


def initFiles():
    print("initFiles")
    global inventaire
    i=1
    while i< len(inventaire["lastKit"])+1:
        analFiles(i,0)
        i+=1

def saveSet():
    global inventaire
    date = datetime.datetime.now()
    saveName=inventaire["saveName"]=str(date.day)+"-"+str(date.month)+"_"+str(date.hour)+";"+str(date.minute)
    print(saveName)
    name=inventaire["chemin"]+saveName
    with open(name,'wb') as fichier:
        mon_pickler=pickle.Pickler(fichier)
        mon_pickler.dump(inventaire)
    inventaire["lastLoadId"]=0
    return inventaire
    
    
def loadSet():
    global inventaire
    myfilesSaves=listSaves();
    endname=myfilesSaves[inventaire["lastLoadId"]]
    name=inventaire["chemin"]+endname
    with open(name,'rb') as fichier:
        mon_depickler=pickle.Unpickler(fichier)
        recupSave=mon_depickler.load()
    myload =updateLoad(recupSave)
    return myload

    
def tri_load(arg):
    #print("trivelo",arguments)
    global inventaire
    inventaire["lastLoadId"]=arg
    return inventaire

def tri_mute(rack,instru):
    global inventaire
    if inventaire["list_mute"][rack][instru]==True:
        inventaire["list_mute"][rack][instru]=False
    elif inventaire["list_mute"][rack][instru]==False:
        inventaire["list_mute"][rack][instru]=True
    return inventaire

def tri_rackMute(rack):
    global inventaire
    if inventaire["list_rack_mute"][rack]==True:
        inventaire["list_rack_mute"][rack]=False
    elif inventaire["list_rack_mute"][rack]==False:
        inventaire["list_rack_mute"][rack]=True
    return inventaire

def tri_velo(rack,instru,pas,arguments):
    global inventaire
    inventaire["list_velos"][rack][instru][pas]=arguments[0]
    return inventaire 
    #print(list_velos[lastIdInstru])
    

def clear_velo(rack,instru):
    global inventaire
    inventaire["list_vol"][rack][instru]=0.5
    inventaire["list_mute"][rack][instru]=False
    inventaire["list_mesure"][rack][instru]=[0,16]
    i=0
    while i<64:
        inventaire["list_velos"][rack][instru][i]=0
        i+=1
    return inventaire
    
def clear_rack_velo(rack):
    global inventaire
    i=0
    j=0
    while j<inventaire["nbPlayers"]:
        inventaire["list_vol"][rack][j]=0.5
        inventaire["list_mute"][rack-1][j]=False
        inventaire["list_mesure"][rack-1][j]=[0,16]
        while i<64:
            inventaire["list_velos"][rack][j][i]=0
            i+=1
        j+=1
        i=0
    return inventaire


def askRec():
    global inventaire
    print("askRec")
    date = datetime.datetime.now()
    if inventaire["recIsOn"]==False:
        sendRecDate('/home/pi/Bureau/BTMachines_git/Records/'+str(date.day)+str(date.month)+str(date.year)[2:]+'-'+str(date.hour)+str(date.minute)+str(date.second)+'.wav')
        return True
    elif inventaire["recIsOn"]==True:
        sendRecOff()
        return False
        
    
def updateLoad(inventory):
    kitFolders=listRepo()
    updateInventory=inventory
    i=0
    while i<len(updateInventory["lastKit"]):
        j=0
        while j<len(kitFolders):
            if updateInventory["lastKitName"][i]==kitFolders[j]:
                updateInventory["lastKitName"][i]=j
            j+=1
        i+=1
    updateInventory["lastIdMenu"]=0
    updateInventory["lastIdInstru"]=1
    updateInventory["lastIdRack"]=1
    updateInventory["lastIdPas"]=0
    updateInventory["lastPas"]=0
    
    return(updateInventory)

