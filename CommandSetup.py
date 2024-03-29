import re
from SQLiteInterface import saveGuildRoleMessageId

async def entry(cmdArgs, message):
    
    #checkPerms = message.author.permissions_in(message.guild)
    #TODO
    # if message.author.id != 263515295019171861:
    #     return
    
    if message.author.top_role.permissions == False:
        return
    
    numArgs = len(cmdArgs)
    if len(cmdArgs) == 0:
        pass
    else:
        # Role setup should be >setup roles [channel with reaction message]
        if (cmdArgs[0] == 'roles') and (numArgs == 2):
            
            roleChannels = message.channel_mentions
            if len(roleChannels) <= 0:
                return
            else:
                roleChannel = roleChannels[0]
                
            channelMessages = await roleChannel.history(limit=100).flatten()
            reRes = None
            reactionMessageId = None
            reacionMessageChannel = None
            for cMsg in channelMessages:
                cCMsg = cMsg.clean_content
                reRes = re.search('========(.*)========', cCMsg, re.S)
                if reRes != None:
                    reactionMessageId = cMsg.id
                    reacionMessageChannel = cMsg.channel.id
                    break
            if reRes == None:
                return
            
            await saveGuildRoleMessageId(message.guild.id, reactionMessageId, reacionMessageChannel)
