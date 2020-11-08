import discord

import GetToken
import CommandRemind as cRemind
import CommandRoll as cRoll
import CommandImplying as cImplying
import CommandJoin as cJoin
import CommandLeave as cLeave
import CommandRoles as cRoles

import LogTools as LT
import Constants as C
import SQLiteInterface as SQI
import Debug
from ClientHolder import ClientHolderInit

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

# Process the given command with parameters
async def processCommand(cmdMain, cmdArgs, message):
    # Switch to entry() function on each command
    switch = {
        # 'tag': cTag,
        # 'timeout': cTimeout,
        #'remind': cRemind,
        #'roll': cRoll,
        # 'shitpost': cShitpost,
        'join': cJoin,
        'leave': cLeave,
        'roles': cRoles,
        'implying': cImplying
    }
    f = switch.get(cmdMain, lambda: 'None')
    if f != 'None':
        await f.entry(cmdArgs, message)


# Initial setup function for SQL, etc.
def init():
    err = False
    err |= ClientHolderInit(client)
    #err |= SQI.Initialize()
    return err

@client.event
async def on_ready():
    print('{0.user} logged in successfully'.format(client))
    if init():
        print('Error in beginning initialization, stopping server')
        await client.logout()
    else:
        print('Initialization complete')   

@client.event
async def on_message(message):
    
    LT.Log(message.author.nick, message.author.id, message.channel.name, message.content)
    
    if message.author.id == client.user.id:
        return
    
    if message.content.startswith('>'):
        cmdStr = message.content[1:]
        if len(cmdStr) <= 0:
            return
        print('{0} ({1}) gave command {2}'.format(message.author.nick, message.author.id, str(cmdStr)))
        #print(message.author.name + '(' + str(message.author.id) + ') gave command ' + str(cmdStr))
        cmdTok = [x for x in cmdStr.split(' ') if x.strip()] # Tokenize
        cmdMain = cmdTok[0].lower()
        cmdArgs = cmdTok[1:]
        
        if cmdMain in C.commandList:
            await processCommand(cmdMain.lower(), cmdArgs, message)
        
client.run(GetToken.get())

