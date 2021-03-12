import Constants as C
import discord
import re
import ClientHolder

async def entry(cmdArgs, message):
    if len(cmdArgs) == 0:
        await listAllRoles(message)
    else:
        await listAllRoles(message)

async def listAllRoles(message):
    msgStr = '```You can join the following roles with ">join <role>"\n\nJoinable roles:\n'
    for r in C.joinableRolesCapitalized:
        msgStr += '\t{0}\n'.format(r)
    msgStr += '```'
    await message.channel.send(msgStr)

async def modReactedRole(payload):
    userId = payload.user_id
    emoji = payload.emoji

    guild = await ClientHolder.heldClient.fetch_guild(payload.guild_id)
    channel = await ClientHolder.heldClient.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    roleName = getRoleFromEmoji(message, emoji)
    if roleName == None:
        return
    
    if payload.event_type == 'REACTION_ADD':
        addUserToRole(userId, roleName)
    elif payload.event_type == 'REACTION_REMOVE':
        removeUserFromRole(userId, roleName)
    else:
        raise Exception("Error in modReactedRole: Couldn't determine the event_type")

async def addUserToRole(userId, roleName):
    pass

async def removeUserFromRole(userId, roleName):
    pass    

def getRoleFromEmoji(message, emoji):
    try:
        cleanMessage = message.clean_content
        regStrip = re.search('========(.*)========', cleanMessage, re.S)
        res = regStrip.group(1)
        lines = [x for x in res.split('\n') if x.strip()]
        emojiMap = []
        for line in lines:
            parts = [j for j in line.split(' : ') if j.strip()]
            emojiMapPair = [parts[0], parts[1]]
            emojiMap.append(emojiMapPair)
        if emojiMap == []:
            raise Exception
        
        for p in emojiMap:
            if p[0] == emoji.name:
                return p[1]
            
        return None

    except Exception as e:
        print('Exception in getRoleFromEmoji: {}'.format(e))
    
    
