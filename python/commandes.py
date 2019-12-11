from analyse import *

import datetime
import pickle

inventaire={}


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

def cmdReceiveInventory(inventory):
    global inventaire
    inventaire=inventory
    
def loadSet():
    global inventaire
    #name=filesSaves[loadId]
    name=inventaire["chemin"]+sendSaveName(inventaire["lastLoadId"])
    with open(name,'rb') as fichier:
        mon_depickler=pickle.Unpickler(fichier)
        recupSave=mon_depickler.load()
    return recupSave


def saveSet():
    global inventaire
    date = datetime.datetime.now()
    saveName=inventaire["saveName"]=str(date.day)+str(date.month)+str(date.year)[2:]+'-'+str(date.hour)+str(date.minute)+str(date.second)
    print(saveName)
    name=inventaire["chemin"]+saveName
    with open(name,'wb') as fichier:
        mon_pickler=pickle.Pickler(fichier)
        mon_pickler.dump(inventaire)
    
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


