import Constants as C
from ClientHolder import GetClient
import discord

async def entry(cmdArgs, message):
    if len(cmdArgs) == 0:
        await message.channel.send('Give a role name to leave')
    else:
        roleToLeave = (' '.join(cmdArgs)).lower()
        if roleToLeave not in C.joinableRolesAbv:
            await message.channel.send('Not a role (use >roles to see a list)')
        else:
            await removeRole(message.author, roleToLeave, message)
            
async def removeRole(user, role, message):
    roleTok = discord.utils.get(message.guild.roles, id = C.rolesToIdMap.get(C.joinableRolesAbvMap.get(role)))
    if roleTok in user.roles:
        try:
            await user.remove_roles(roleTok)
            await message.channel.send("{0}: You've been removed ```{1}```".format(message.author.mention, C.joinableRolesAbvMap.get(role)))
        except Exception as exc:
            print('{0}'.format(exc))
            await message.channel.send("{0}: Something went wrong, contact an admin".format(message.author.mention))
    else:
        await message.channel.send("You're not in that role")