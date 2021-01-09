import discord

import GetToken
import CommandRemind as cRemind
import CommandRoll as cRoll
import CommandImplying as cImplying
import CommandJoin as cJoin
import CommandLeave as cLeave
import CommandRoles as cRoles
import CommandAccept as cAccept

import LogTools as LT
import Constants as C
import SQLiteInterface as SQI
import Debug
from ClientHolder import ClientHolderInit
import ChatModeration

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
        'implying': cImplying,
        'accept': cAccept
    }
    f = switch.get(cmdMain, lambda: 'None')
    if f != 'None':
        await f.entry(cmdArgs, message)

# Initial setup function for SQL, etc.
def init():
    err = False
    err |= ClientHolderInit(client)
    err |= SQI.Initialize()

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
    
    # Ignore self posts
    if message.author.id == client.user.id:
        return
    
    # Moderate message, return and don't continue if things don't check out
    if (await ChatModeration.moderateMessage(message) != ChatModeration.CMOD_MSG_OK):
        LT.Log(message.author.name, message.author.id, "System", "User's message was auto-filtered")
        return

    if message.content.startswith('>'):
        cmdStr = message.content[1:]
        if len(cmdStr) <= 0:
            return
        uNick = message.author.nick
        uName = message.author.name
        uId = message.author.id
        if uNick == None:
            print('{0} ({1}) gave command {2}'.format(uName, uId, str(cmdStr)))
        else:
            print('{3} ({0}) ({1}) gave command {2}'.format(uName, uId, str(cmdStr), uNick))            

        cmdTok = [x for x in cmdStr.split(' ') if x.strip()] # Tokenize
        cmdMain = cmdTok[0].lower()
        cmdArgs = cmdTok[1:]
        
        if cmdMain in C.commandList:
            await processCommand(cmdMain.lower(), cmdArgs, message)
       
       
@client.event
async def on_member_join(member):
    LT.Log(member.name, member.id, "System", "User joined the server")
    
    roleTok = discord.utils.get(member.guild.roles, id = C.rolesToIdMap.get('landlubber'))
    try:
        await member.add_roles(roleTok)
        print("Added {0} to the landlubber role".format(member.name))
    except Exception:
        print("Something went wrong adding {0} to the landlubbers!".format(member.name))

@client.event
async def on_member_remove(member):
    LT.Log(member.name, member.id, "System", "User left the server")

client.run(GetToken.get())