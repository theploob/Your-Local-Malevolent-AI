import discord
import threading
import GetToken
import CommandImplying as cImplying
import CommandRoles as cRoles
import CommandSetup as cSetup
import Gregorian
import LogTools as LT
import Constants as C
import ServerTimer
import SQLiteInterface as SQI
from ClientHolder import ClientHolderInit
import ChatModeration
import Debug

serverInitialized = False
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)


# Process the given command with parameters
async def processCommand(cmdMain, cmdArgs, message):
    # Switch to entry() function on each command
    switch = {
        # 'tag': cTag,
        # 'timeout': cTimeout,
        # 'remind': cRemind,
        # 'roll': cRoll,
        # 'shitpost': cShitpost,
        'implying': cImplying,
        'setup': cSetup
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
    global serverInitialized
    print('{0.user} logged in successfully'.format(client))
    if init():
        print('Error in beginning initialization, stopping server')
        await client.logout()
    else:

        await cRoles.roleMessageSync()
        serverInitialized = True
        print('Initialization complete')
        await Gregorian.update() # Update Revol's name to Greg or Ian, day-dependant
        # await Debug.debug()

@client.event
async def on_message(message):
    if serverInitialized == False:
        return
    
    # Ignore self posts
    if message.author.id == client.user.id:
        return
    
    # Moderate message, return and don't continue if things don't check out
    if await ChatModeration.moderateMessage(message) != ChatModeration.CMOD_MSG_OK:
        LT.Log(message.author.name, message.author.id, "System", "User's message was auto-filtered")
        return

    if message.content.startswith('>'):
        cmdStr = message.content[1:]
        if len(cmdStr) <= 0:
            return
        uNick = message.author.nick
        uName = message.author.name
        uId = message.author.id


        cmdTok = [x for x in cmdStr.split(' ') if x.strip()] # Tokenize
        cmdMain = cmdTok[0].lower()
        cmdArgs = cmdTok[1:]
        
        if cmdMain in C.commandList:
            if uNick is None:
                print('{0} ({1}) gave command {2}'.format(uName, uId, str(cmdStr)))
            else:
                print('{3} ({0}) ({1}) gave command {2}'.format(uName, uId, str(cmdStr), uNick))
            await processCommand(cmdMain.lower(), cmdArgs, message)


@client.event
async def on_raw_reaction_add(payload):
    if serverInitialized == False:
        return
    storedMsgId = SQI.getDbConnection(payload.guild_id).roleMsgId
    if payload.message_id == storedMsgId:
        await cRoles.modReactedRole(payload)

@client.event
async def on_raw_reaction_remove(payload):
    if serverInitialized == False:
        return
    storedMsgId = SQI.getDbConnection(payload.guild_id).roleMsgId
    if payload.message_id == storedMsgId:
        await cRoles.modReactedRole(payload)

       
@client.event
async def on_member_join(member):
    if not serverInitialized:
        return
    LT.Log(member.name, member.id, "System", "User joined the server")
    
@client.event
async def on_member_remove(member):
    if not serverInitialized:
        return
    LT.Log(member.name, member.id, "System", "User left the server")

@client.event
async def on_guild_join(guild):
    if not serverInitialized:
        return
    await SQI.addNewServerDatabase(guild)
    LT.Log(guild.name, guild.id, "System", "Guild joined the botnet")

@client.event
async def on_guild_remove(guild):
    if not serverInitialized:
        return
    await SQI.removeServerDatabase(guild)
    LT.Log(guild.name, guild.id, "System", "Guild left the botnet")


class aThread (threading.Thread):
    def __init__(self, threadID, name, function):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.function = function

    def run(self):
        global client
        print("Starting {} Thread".format(self.name))
        self.function(self.name)


def run_server(thread_name):
    client.run(serverToken)


serverToken = GetToken.get()
# client.run(GetToken.get())

thread1 = aThread(1, "Client", run_server)
thread2 = aThread(2, "Timer", ServerTimer.start_timer)

# Start new Threads
thread1.start()
thread2.start()
