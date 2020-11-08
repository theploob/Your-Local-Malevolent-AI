import discord

heldClient = None


def ClientHolderInit(client):
    global heldClient
    heldClient = client
    
    return False

def GetClient():
    global heldClient
    return heldClient

def getGuildList():
    global heldClient
    return heldClients.guilds

