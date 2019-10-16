from pythonosc import osc_message_builder
from pythonosc import udp_client
from list_repository import *

client = udp_client.UDPClient('localhost', 12000)

folders=listRepo();
finalFilesNames=[];

i=0
while i<12:
    finalFilesNames.append("x")
    i+=1

#print(folders)

def analFolders():
    addr="/folderLength"
    msg = osc_message_builder.OscMessageBuilder(address=addr)
    msg.add_arg(len(folders))
    print("lenFold:",len(folders))
    msg = msg.build()
    client.send(msg)


def analFiles(idFolder):
    name=folders[round(idFolder)]
    filesNames=listFiles(name)
    i=0
    print("name:",name)

    while i<len(filesNames):
        
        analyse= filesNames[i].split("_")
        numId=int(analyse[0])
        print("numid:",numId," name:",analyse[1])
        nakedName=analyse[1].split(".")
        finalFilesNames[numId-1]=nakedName[0]
        addr="/fileName"
        msg = osc_message_builder.OscMessageBuilder(address=addr)
        msg.add_arg(numId)
        msg.add_arg("open")
        msg.add_arg("/home/pi/Bureau/BTMachines_git/Samples/"+name+"/"+filesNames[i])
        msg = msg.build()
        client.send(msg)
        i+=1
    print("final:",finalFilesNames)
