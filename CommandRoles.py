import Constants as C
import discord
import re
import ClientHolder
import SQLiteInterface as SQI

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
    
    if await isRoleNameValid(roleName, guild) == False:
        return
    
    hasRoleAlready = await userHasRole(userId, roleName, guild)
    
    if (payload.event_type == 'REACTION_ADD') and (hasRoleAlready == False):
        await addUserToRole(userId, roleName, guild)
    elif (payload.event_type == 'REACTION_REMOVE') and (hasRoleAlready):
        await removeUserFromRole(userId, roleName, guild)

async def allServerBootSetup():
    for dbConnection in SQI.dbConnectionList:
        if (dbConnection.roleMsgId != 0) and (dbConnection.initialized == True):
            guild = await ClientHolder.heldClient.fetch_guild(dbConnection.getDbConnectionGuildId())
            #channel = await 
            messageId = dbConnection.getDbConnectionRoleMsgId()
            pass #TODO save off channel of the message too
    

async def addUserToRole(userId, roleName, guild):
    try:
        user = await guild.fetch_member(userId)
        guildRole= discord.utils.get(guild.roles, name = roleName)
        await user.add_roles(guildRole)
        pass
    except Exception as e:
        print('Exception in \naddUserToRole(\n{0}\n{1}\n{2})'.format(userId, roleName, guild))

async def removeUserFromRole(userId, roleName, guild):
    try:
        user = await guild.fetch_member(userId)
        guildRole= discord.utils.get(guild.roles, name = roleName)
        await user.remove_roles(guildRole)
        pass
    except Exception as e:
        print('Exception in removeUserFromRole(\n{0}\n{1}\n{2})'.format(userId, roleName, guild))   

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
    
async def isRoleNameValid(roleName, guild):
    guildRoles = await guild.fetch_roles()
    for r in guildRoles:
        if r.name == roleName:
            return True
        
    return False
    
async def userHasRole(userId, roleName, guild):
    roleNameGuild = discord.utils.get(guild.roles, name = roleName).name
    user = await guild.fetch_member(userId)
    roleNameUserTok = discord.utils.get(user.roles, name = roleName)
    if roleNameUserTok == None:
        return False
    roleNameUser = roleNameUserTok.name
    return roleNameUser == roleNameGuild


