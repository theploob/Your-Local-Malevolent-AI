import discord
from ClientHolder import GetClient
import LogTools as LT
import Constants as C

async def entry(cmdArgs, message):
    usr = message.author
    roleTok = discord.utils.get(message.guild.roles, id = C.rolesToIdMap.get('landlubber'))
    if roleTok in usr.roles:
        try:
            await usr.remove_roles(roleTok)
            LT.Log(usr.name, usr.id, "System", "User accepted the rules")
        except Exception:
            print("Something went wrong with {0} accepting the rules".format(usr.name))
