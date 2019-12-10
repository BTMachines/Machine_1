from analyse import *
from commandes import *

def toto():
	print("coucou toto")
	global lastBpm
	lastBpm=120
	
def triCom(address, *args):
	
	    
	print("tricom: ",address,*args)

	global lastIdRack,lastIdInstru,lastIdRack, lastIdPas, lastPas, list_velos,lastIdMenu,list_mute,lastBpm,isPlaying,lastNbMesures,lastMasterVol,lastKit, mode,lastLoadId
	
	if(address=="/validSave"):
		saveSet()
	if(address=="/validLoad"):
		loadSet(lastLoadId)
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
		lastKit[lastIdRack-1]=round(*args)
		analFiles(lastIdRack,lastKit[lastIdRack-1])
	if(address=="/askFolders"):
		analFolders()
	if(address=="/askSaves"):
		analSaves()
	if(address=="/idLoad"):
		lastLoadId=round(args[0])
