import Constants as C
from ClientHolder import GetClient
import discord

async def entry(cmdArgs, message):
    if len(cmdArgs) == 0:
        await message.channel.send('Give a role name to join (use >roles to a see a list)')
    else:
        roleToJoin = (' '.join(cmdArgs)).lower()
        if roleToJoin not in C.joinableRolesAbv:
            await message.channel.send('Not a role (use >roles to see a list)')
        else:
            theUserId = message.author.id
            m = discord.utils.get(message.guild.members, id = theUserId)
            mr = m.roles
            
            await giveRole(message.author, roleToJoin, message)
            

async def giveRole(user, role, message):
    roleTok = discord.utils.get(message.guild.roles, id = C.rolesToIdMap.get(C.joinableRolesAbvMap.get(role)))
    if roleTok in user.roles:
        await message.channel.send("You've already joined that role")
    else:
        try:
            await user.add_roles(roleTok)
            await message.channel.send("{0}: You've been added to ```{1}```".format(message.author.mention, C.joinableRolesAbvMap.get(role)))
        except Exception as exc:
            print('{0}'.format(exc))
            await message.channel.send("{0}: Something went wrong, contact an admin".format(message.author.mention))



