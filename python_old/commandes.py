

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
        
def tri_load(arg):
    #print("trivelo",arguments)
    global lastLoadId
    lastLoadId=arg
        

def saveSet():
    global saveName
    date = datetime.datetime.now()
    saveName=str(date.day)+str(date.month)+str(date.year)[2:]+'-'+str(date.hour)+str(date.minute)+str(date.second)
    print(saveName)
    name=chemin+saveName+".txt"
    file = open(name,'w')
    file.write(str(lastBpm)+'\n')
    file.write(str(lastMasterVol)+'\n')
    for i in range(0,nbRack):
        file.write(folders[lastKit[i]]+',')
    file.write('\n')
    file.close() #to change file access modes

def loadSet(loadId):
    global lastIdRack,lastIdInstru, lastIdPas, lastPas, list_velos,lastIdMenu,list_mute,lastBpm,isPlaying,lastNbMesures,lastMasterVol, lastKit, mode,lastLoadId
    name=filesSaves[loadId]
    file = open(chemin+name,'r')
    params=file.readlines()
    print(params[0])

