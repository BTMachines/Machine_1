from pythonosc import osc_message_builder
from pythonosc import udp_client
from list_repository import *

client = udp_client.UDPClient('localhost', 12000)

def anal(name):
    line=listRepo(name)
    i=0
    myNum=0
    print("name:",name)

    while i<len(line):
        
        nombre=True
        try:
            float(line[i][1])>=0
        except ValueError:
            nombre=False
        
        if nombre==True:    
            myNum=int(line[i][:2])
        else:
            myNum=int(line[i][0])
                
        #print(myNum)

        numId= line[myNum-1].split("_")
        addr="/fileName"
        msg = osc_message_builder.OscMessageBuilder(address=addr)
        msg.add_arg(int(numId[0]))
        msg.add_arg("open")
        msg.add_arg("/home/pi/Bureau/BTMachines_git/Samples/"+name+"/"+line[myNum-1])
        msg = msg.build()
        client.send(msg)
        i+=1
