from osc_send import *
from commandes import *
from list_repository import *
from oled.affichage import affIsLoading

#from main import *

	
def triCom(inventory,address, *args):
	
	#print("tricom: ",address,*args)
	inventaire={}
	inventaire=inventory
	idRack=inventaire["lastIdRack"]-1
	idInstru=inventaire["lastIdInstru"]-1
	idPas=inventaire["lastIdPas"]
	
	if(address=="/validSave"):
		inventaire=saveSet()
	if(address=="/validLoad"):
		affIsLoading()
		tempInventaire=loadSet()
		inventaire=setReload(tempInventaire)
	if(address=="/velo"):
		inventaire=tri_velo(idRack,idInstru,idPas,args)
	if(address=="/muteId"):
		inventaire=tri_mute(idRack,idInstru)
	if(address=="/muteRackId"):
		inventaire=tri_rackMute(idRack)
	if(address=="/clear"):
		inventaire=clear_velo(idRack,idInstru)
	if(address=="/clearRack"):
		inventaire=clear_rack_velo(idRack)
	if(address=="/idMenu"):
		if (round(args[0])==-2):
			analSaves()
		inventaire["lastIdMenu"]=round(args[0])
	if(address=="/idRack"):
		inventaire["lastIdRack"]=round(args[0])
	if(address=="/idInstru"):
		inventaire["lastIdInstru"]=round(args[0])
	if(address=="/idPas"):
		inventaire["lastIdPas"]=round(args[0])
	if(address=="/pas"):
		inventaire["lastPas"]=round(args[0])
	if(address=="/trackVol"):
		inventaire["list_vol"][idRack][idInstru]=round(args[0]*10)/10
	if(address=="/switchMode"):
		inventaire["mode"]=round(args[0])
	if(address=="/BPM"):
		inventaire["lastBpm"]=round(args[0])
	if(address=="/playPause"):
		inventaire["isPlaying"]=round(args[0])
	if(address=="/beginMesure"):
		inventaire["list_mesure"][idRack][idInstru][0]=round(args[0])
	if(address=="/endMesure"):
		inventaire["list_mesure"][idRack][idInstru][1]=round(args[0])
	if(address=="/masterVol"):
		inventaire["lastMasterVol"]=round(args[0]*100)
	if(address=="/masterRack"):
		inventaire["master_rack"][idRack]=round(args[0]*100)
	if(address=="/idLoad"):
		inventaire["lastLoadId"]=round(args[0])
	if(address=="/askFiles"):
		inventaire["lastKit"][idRack]=round(args[0])
		myRepo=listRepo()
		inventaire["lastKitName"][idRack]=myRepo[round(args[0])]
		print("lastKitName", inventaire["lastKitName"][idRack])
		analFiles(idRack+1,inventaire["lastKit"][idRack])
	if(address=="/initFiles"):
		initFiles()
	if(address=="/askFolders"):
		analFolders()
	if(address=="/askSaves"):
		analSaves()
	if(address=="/askRec"):
		inventaire["recIsOn"]=askRec()
		print(inventaire["recIsOn"])
	cmdReceiveInventory(inventaire)
	return(inventaire)
