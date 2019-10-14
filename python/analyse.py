from pythonosc import osc_message_builder
from pythonosc import udp_client

def anal():
    client = udp_client.UDPClient('localhost', 1338)
    msg = osc_message_builder.OscMessageBuilder(address="/debug")
    msg = msg.build()
    print('Sending')
    client.send(msg)
