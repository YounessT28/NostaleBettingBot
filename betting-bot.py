import socket
import time
import threading
import re
import win32gui
from enum import Enum
import discord
import random

class Options(Enum):
    ENHANCEDDAMAGE = '.1.' # WEAPON
    SRELA = '.2.'
    MINORBLEEDING = '.3.'
    OPENWOUND = '.4.'
    HEAVYBLESSING = '.5.'
    STUN = '.6.'
    FREEZE = '.7.'
    STUNBADLY = '.8.'
    INCREASEDAMAGETOPLANT = '.9.'
    INCREASEDAMAGETOANIMAL = '.10.'
    INCREASEDAMAGETOMONSTER = '.11.'
    INCREASEDAMAGETOUNDEAD = '.12.'
    SOCIETYMONSTER = '.13.'
    INCREASEDAMAGETOMAPBOSSES = '.14.'
    INCREASECHANCEOFCRITICALHIT = '.15.'
    INCREASECRITICALDAMAGE = '.16.'
    ANTIINCANTATIONMAGE = '.17.'
    INCREASEFIREPROPERTY = '.18.'
    INCREASEWATERPROPERTY = '.19.'
    INCREASELIGHTPROPERTY = '.20.'
    INCREASESHADOWENERGY = '.21.'
    INCREASEELEMENTALPROPERTY = '.22.'
    REDUCECONSOMP = '.23.'
    HPRECOVERYPERKILL = '.24.'
    MPRECOVERYPERKILL = '.25.'
    SLDAMAGE = '.26.'
    SLDEFENCE = '.27.'
    SLPROPERTY = '.28.'
    SLENERGY = '.29.'
    SLOVERALL = '.30.'
    GAINMOREGOLD = '.31.'
    INCREASECOMBATEXP = '.32.'
    GAINMORECXP = '.33.'
    TODAMAGEPVP = '.34.'
    REDUCDEFPVP = '.35.'
    REDUCRESFIREPVP = '.36.'
    REDUCRESWATERPVP = '.37.'
    REDUCRESLIGHTPVP = '.38.'
    REDUCRESSHADOWPVP = '.39.'
    REDUCALLRESPVP = '.40.'
    ANTIMISS100HIT = '.41.'
    TODAMAGEAT15INPVP = '.42.'
    DRAINOPPENENTMANAPVP = '.43.'
    IGNORERESFIRE = '.44.'
    IGNORERESWATER = '.45.'
    IGNORERESLIGHT = '.46.'
    IGNORERESSHADOW = '.47.'
    SPRECOVERYPERKILL = '.48.'
    INCREASEACCURACY = '.49.'
    INCREASECONCENTRATION = '.50.'
    ENHANCEDMELEEDEF = '.1.' # ARMOR
    ENHANCEDLONGRANGEDEF = '.2.'
    ENHANCEDMAGICDEF = '.3.'
    OVERALLDEF = '.4.'
    REDUCECHANCECRITIALHIT = '.23.'
    OVERALLDEFPVP = '.33.'
    DODGEMELEEATTACKPVP = '.34.'
    DODGELONGRANGEPVP = '.35.'
    IGNOREMAGICPVP = '.36.'
    DODGEALLATTACKPVP = '.37.'

# Create TCP/IP socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get PacketLogger port function
def enum_windows_callback(hwnd, port):
    if re.search(r"BladeTiger", win32gui.GetWindowText(hwnd)):
        title = win32gui.GetWindowText(hwnd)
        port[0] = int(title[-5:])


port = [None]
win32gui.EnumWindows(enum_windows_callback, port) # Get PacketLogger port
 
# Connection to socket
server_address = ('127.0.0.1', port[0])
print('Connexion à {} port {}'.format(*server_address))
sock.connect(server_address)

shell = [Options.ENHANCEDDAMAGE.value, Options.SRELA.value, Options.STUN.value, Options.TODAMAGEPVP.value]

stop = 0
stop_thread = False


def send_data(): # Betting function
    global stop_thread
    while not stop_thread:
            sock.sendall('1 up_gr 7 0 0'.encode()) # Betting (item must be in the first slot)
            time.sleep(1)
            sock.sendall('1 eqinfo 1 0'.encode())
            print("Betting")
            time.sleep(round(random.uniform(6, 8), 1)) # Betting every 6-8 seconds

send_thread = threading.Thread(target=send_data, daemon=True)
send_thread.start()

while stop == 0:
    data = sock.recv(1024)
    packet = data.decode("windows-1252") 

    state = 1 
    if "Speaker" not in packet and "e_info" in packet:
        for opt in shell:
            if opt not in packet:
                state = 0
        if state == 0:
            print("There are not all the options")
        else:
            print("Shell found")
            stop_thread = True
            send_thread.join()
            break

print('Closing socket')
sock.close()

#--------------------SEND DISCORD MESSAGE--------------------#
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# Bot access token
TOKEN = 'PUT_YOUR_BOT_TOKEN_HERE'

# Discord user ID
user_id = 'PUT_YOUR_DISCORD_ID_HERE'

# Message to send
message = 'Shell found'

@client.event
async def on_ready():
    user = await client.fetch_user(user_id)
    await user.send(message)
    await client.close()

# Run discord bot
client.run(TOKEN)
#------------------------------------------------------------#