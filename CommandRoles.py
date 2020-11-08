import Constants as C

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
