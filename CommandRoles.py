import Constants as C
import discord
import re
import ClientHolder
import SQLiteInterface as SQI

async def entry(cmdArgs, message):
    pass

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
    
    user = await guild.fetch_member(userId)
    hasRoleAlready = await userHasRole(user, roleName, guild)
    
    if (payload.event_type == 'REACTION_ADD') and (hasRoleAlready == False):
        await addUserToRole(user, roleName, guild)
    elif (payload.event_type == 'REACTION_REMOVE') and (hasRoleAlready):
        await removeUserFromRole(user, roleName, guild)

async def roleMessageSync():
    try:
        for dbConnection in SQI.dbConnectionList:
            if (dbConnection.roleMsgId != 0) and (dbConnection.initialized == True):
                guild = await ClientHolder.heldClient.fetch_guild(dbConnection.getDbConnectionGuildId())
                channel = await ClientHolder.heldClient.fetch_channel(dbConnection.getDbConnectionRoleChannelId())
                message = await channel.fetch_message(dbConnection.getDbConnectionRoleMsgId())
                reactionsList = message.reactions
                
                #memberList = await guild.fetch_members(limit=None).flatten()
                #memberCount = len(memberList)
                #updatedMembers = 0
                print("Processing guild: {0}".format(guild.name))
                
                # iterate over each member in the guild, check their roles vs message roles
                users = await guild.fetch_members(limit=None).flatten()
                for user in users:
                    if user.id != 730947466983374900: # Remove self
                        #print("{:.0f}%".format(updatedMembers / memberCount * 100))
                        #print("Processing user {0} ({1})".format(user.name, guild.name))
                        for reaction in reactionsList:
                            roleFromEmoji = getRoleFromEmoji(message, reaction.emoji)
                            reactionUsers = await reaction.users().flatten()
    
                            uHasRole = await userHasRole(user, roleFromEmoji, guild)
                            mInMList = memberInMemberList(user, reactionUsers)                         
                            
                            if mInMList and not uHasRole:
                                await addUserToRole(user, roleFromEmoji, guild)
                                #print("Added user to role {0}".format(roleFromEmoji))
                            elif uHasRole and not mInMList:
                                await removeUserFromRole(user, roleFromEmoji, guild)
                                #print("Removed user from role {0}".format(roleFromEmoji))
                        #updatedMembers += 1
    
        print("Server finished roleMessageSync()")
    except Exception as e:
        print('Exception in roleMessageSync: {0}'.format(e))

async def addUserToRole(user, roleName, guild):
    try:
        guildRole= discord.utils.get(guild.roles, name = roleName)
        await user.add_roles(guildRole)
        print("Added {0} to {1}".format(user.name, roleName))
    except Exception as e:
        print('Exception in addUserToRole:\n\t{0}\n\t{1}\n\t{2}'.format(user.id, roleName, guild))

async def removeUserFromRole(user, roleName, guild):
    try:
        guildRole= discord.utils.get(guild.roles, name = roleName)
        await user.remove_roles(guildRole)
        print("Removed {0} from {1}".format(user.name, roleName))
    except Exception as e:
        print('Exception in removeUserFromRole:\n\t{0}\n\t{1}\n\t{2}'.format(user.id, roleName, guild))   

# Given the emoji name/PartialEmoji, return the name of the Role associated with it
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
            if type(emoji) == str:
                if p[0] == emoji:
                    return p[1]
            elif type(emoji) == discord.PartialEmoji:
                if p[0] == emoji.name:
                    return p[1]
            
        return None

    except Exception as e:
        print('Exception in getRoleFromEmoji: {}'.format(e))
    
async def isRoleNameValid(roleName, guild):
    guildRole = discord.utils.get(guild.roles, name=roleName)
    return guildRole != None
    
async def userHasRole(user, roleName, guild):
    role = discord.utils.get(user.roles, name=roleName)
    return role != None

def memberInMemberList(member, memberList):
    m = discord.utils.get(memberList, id=member.id)
    return m != None
