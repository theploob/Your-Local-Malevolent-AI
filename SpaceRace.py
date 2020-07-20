import discord

import GetToken
import CommandRemind as cRemind
import CommandRoll as cRoll
import CommandImplying as cImplying

import LogTools as LT
import Constants as C
import SQLiteInterface as SQI
import Debug

client = discord.Client()

# Log tag
logtag = "SpaceRace Log: "
    


# Process the given command with parameters
async def processCommand(cmdMain, cmdArgs, message):
    # Switch to entry() function on each command
    switch = {
        # 'tag': cTag,
        # 'timeout': cTimeout,
        'remind': cRemind,
        'roll': cRoll,
        # 'shitpost': cShitpost,
        'implying': cImplying
    }
    f = switch.get(cmdMain, lambda: 'None')
    if f != 'None':
        await f.entry(cmdArgs, message)


# Initial setup function for SQL, etc.
def init():
    err = False
    err |= SQI.Initialize()
    return err

@client.event
async def on_ready():
    LT.Log('{0.user} logged in successfully'.format(client), logtag)
    if init():
        LT.Log('Error in beginning initialization, stopping server', logtag)
        await client.logout()
    else:
        LT.Log('Initialization complete', logtag)
    Debug.debug()
    

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    
    if message.content.startswith('>'):
        cmdStr = message.content[1:]
        if len(cmdStr) <= 0:
            return
        LT.Log(message.author.name + '(' + str(message.author.id) + ') gave command ' + str(cmdStr), logtag)
        cmdTok = [x for x in cmdStr.split(' ') if x.strip()] # Tokenize
        cmdMain = cmdTok[0].lower()
        cmdArgs = cmdTok[1:]
        
        if cmdMain in C.commandList:
            await processCommand(cmdMain.lower(), cmdArgs, message)
        
client.run(GetToken.get())

