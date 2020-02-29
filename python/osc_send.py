from pythonosc import osc_message_builder
from pythonosc import udp_client
from list_repository import *

client = udp_client.UDPClient('localhost', 12000)

folders=listRepo();
filesSaves=listSaves();
finalFilesNames=[];

i=0
j=0
while j<4:
    finalFilesNames.append([])
    while i<12:
        finalFilesNames[j].append("x")
        i+=1
    i=0
    j+=1

#print(folders)
def sendSaveName(idSave):
    print("idSave : =>",idSave)
    global filesSaves
    filesSaves=listSaves();
    return(filesSaves[idSave])
    
def sendRecDate(myDate):
    addr="/currentDate"
    msg = osc_message_builder.OscMessageBuilder(address=addr)
    msg.add_arg("open")
    msg.add_arg(myDate)
    print("myDate:",myDate)
    msg = msg.build()
    client.send(msg)
    
def sendRecOff():
    addr="/recOff"
    msg = osc_message_builder.OscMessageBuilder(address=addr)
    msg.add_arg("isOff")
    print("recOff")
    msg = msg.build()
    client.send(msg)


def analSaves():
    filesSaves=listSaves(); 
    addr="/folderSaveLength"
    msg = osc_message_builder.OscMessageBuilder(address=addr)
    msg.add_arg(len(filesSaves))
    print("SavelenFold:",len(filesSaves))
    msg = msg.build()
    client.send(msg)


def analFolders():
    addr="/folderLength"
    msg = osc_message_builder.OscMessageBuilder(address=addr)
    msg.add_arg(len(folders))
    print("lenFold:",len(folders))
    msg = msg.build()
    client.send(msg)


def analFiles(idRack,idFolder):
    folderName=folders[idFolder]
    filesNames=listFiles(folderName)
    i=0
    print("folderName:",folderName)

    while i<len(filesNames):
        
        analyse= filesNames[i].split("_")
        numId=int(analyse[0])
        #print("numid:",numId," name:",analyse[1])
        nakedName=analyse[1].split(".")
        finalFilesNames[idRack-1][numId-1]=nakedName[0]
        addr="/fileName"
        msg = osc_message_builder.OscMessageBuilder(address=addr)
        msg.add_arg(idRack)
        msg.add_arg(numId)
        #msg.add_arg("open")
        msg.add_arg("/home/pi/Bureau/BTMachines_git/Samples/"+folderName+"/"+filesNames[i])
        msg = msg.build()
        client.send(msg)
        i+=1
    #print("final:",finalFilesNames)
    
def setReload(inventory):
    addr="/myload"
    loadInventaire=inventory
    for cle,valeur in inventory.items():
        #print(cle,type(valeur))
        if cle == "lastKit":
            i=0
            while i< len(valeur):
                analFiles(i+1,valeur[i])
                i+=1
        if type(valeur)==int or type(valeur)==float:
            #print (cle, valeur)
            msg = osc_message_builder.OscMessageBuilder(address=addr)
            msg.add_arg(cle)
            msg.add_arg(valeur)
            msg = msg.build()
            client.send(msg)
        elif type(valeur)==bool:
            msg = osc_message_builder.OscMessageBuilder(address=addr)
            msg.add_arg(cle)
            if valeur==True:
                msg.add_arg(0)
            else:
                msg.add_arg(1)
            msg = msg.build()
            client.send(msg)
        elif type(valeur)==list:
            print(cle,type(valeur))
            i=0
            while i<len(valeur):
                print (cle,i,type(valeur[i]))
                    
                if type(valeur[i])==int or type(valeur[i])==float:
                    msg = osc_message_builder.OscMessageBuilder(address=addr)
                    msg.add_arg(cle)
                    msg.add_arg(i)
                    msg.add_arg(valeur[i])
                    msg = msg.build()
                    client.send(msg)
                elif type(valeur[i])==bool:
                    msg = osc_message_builder.OscMessageBuilder(address=addr)
                    msg.add_arg(cle)
                    msg.add_arg(i)
                    if valeur[i]==True:
                        msg.add_arg(0)
                    else:
                        msg.add_arg(1)
                    msg = msg.build()
                    client.send(msg)
                elif type(valeur[i])==list:
                    j=0
                    while j<len(valeur[i]):
                        #print (cle,i,j,valeur[i][j])

                        if type(valeur[i][j])==int or type(valeur[i][j])==float:
                            msg = osc_message_builder.OscMessageBuilder(address=addr)
                            msg.add_arg(cle)
                            msg.add_arg(i)
                            msg.add_arg(j)
                            msg.add_arg(valeur[i][j])
                            #print (cle,i,j,valeur[i][j])
                            msg = msg.build()
                            client.send(msg)
                        elif type(valeur[i][j])==bool:
                            msg = osc_message_builder.OscMessageBuilder(address=addr)
                            msg.add_arg(cle)
                            msg.add_arg(i)
                            msg.add_arg(j)
                            if valeur[i][j]==True:
                                msg.add_arg(0)
                            else:
                                msg.add_arg(1)
                            msg = msg.build()
                            client.send(msg)
                        elif type(valeur[i][j])==list:
                            k=0
                            while k<len(valeur[i][j]):
                                #print (cle,i,j,k,valeur[i][j][k])
                                msg = osc_message_builder.OscMessageBuilder(address=addr)
                                msg.add_arg(cle)
                                msg.add_arg(i)
                                msg.add_arg(j)
                                msg.add_arg(k)
                                msg.add_arg(valeur[i][j][k])
                                msg = msg.build()
                                client.send(msg)
                                k+=1
                        j+=1
                i+=1
    
    return loadInventaire

