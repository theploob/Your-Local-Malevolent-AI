import discord
import asyncio

heldClient = None
client_asyncio_event_loop = None

def ClientHolderInit(client):
    global heldClient
    global client_asyncio_event_loop
    heldClient = client
    client_asyncio_event_loop = asyncio.get_running_loop()
    
    return False


def GetClient():
    global heldClient
    return heldClient


def getGuildList():
    global heldClient
    return heldClient.guilds


def get_client_asyncio_event_loop():
    global client_asyncio_event_loop
    return client_asyncio_event_loop
