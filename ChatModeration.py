from ContentControl import bannedWordList
import Constants as C

CMOD_MSG_OK = 0
CMOD_MSG_ER = 1

async def moderateMessage(message):

    for w in bannedWordList:
        if w in message.content:
            await message.delete()
            return CMOD_MSG_ER
    
    return CMOD_MSG_OK