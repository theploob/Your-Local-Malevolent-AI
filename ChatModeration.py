from ContentControl import bannedWordList
import Constants as C

CMOD_MSG_OK = 0
CMOD_MSG_ER = 1

async def moderateMessage(message):
    
    if message.channel.id == C.textChannelsToIdMap.get('initiation'):
        if (message.content.lower() != '>accept'):
            await message.delete()
            return CMOD_MSG_ER

    for w in bannedWordList:
        if w in message.content:
            await message.delete()
            return CMOD_MSG_ER
    
    return CMOD_MSG_OK