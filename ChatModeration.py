from ContentControl import bannedWordList
import Constants as C

CMOD_MSG_OK = 0
CMOD_MSG_ER = 1

async def moderateMessage(message):

    messageContent = message.clean_content_lower()

    for w in bannedWordList:
        if w in messageContent:
            await message.delete()
            return CMOD_MSG_ER
    
    return CMOD_MSG_OK