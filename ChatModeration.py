from ContentControl import bannedWordList

CMOD_MSG_OK = 0
CMOD_MSG_ER = 1

async def moderateMessage(message):

    messageContent = message.clean_content.lower()

    for w in bannedWordList:
        if w in messageContent:
            await message.delete()
            return CMOD_MSG_ER
    
    return CMOD_MSG_OK
