import sqlite3
import os
from pathlib import Path
from ClientHolder import getGuildList

# Master list of all DbConnections, one for each SQLite database/server

dbConnectionList = []

# Init
def Initialize():
    global dbConnectionList
    err = False
    
    try:
        # Create db directory if it doesn't exist
        if os.path.isdir('sqliteDatabases') == False:
            os.mkdir('sqliteDatabases')
            
        if os.path.isfile('ConnectedServerIdList.txt') == False:
            f = open('ConnectedServerIdList.txt', 'w')
            f.close()
            
        connFile = open('ConnectedServerIdList.txt', 'r+')
        connectedServerIdList = connFile.read()
        connFile.close()
    except Exception as exc:
        print('{}'.format(exc))
        return True

    # Grab list of currently connected guilds
    currentConnectedGuilds = [str(x.id) for x in getGuildList() if str(x.id).strip()]

    # Grab list of tracked guilds
    connectedServerIds = [x for x in connectedServerIdList.split('\n') if x.strip()]
    
    # Get servers that joined while offline and add them
    guildDiff = list(set(currentConnectedGuilds) - set(connectedServerIds))
    if len(guildDiff) > 0:
        connFile = open('ConnectedServerIdList.txt', 'w')
        for gd in guildDiff:
            connFile.write('{}\n'.format(gd))
        connectedServerIds += guildDiff
    
    
    
    if len(connectedServerIds) == 0:
        return False
        
    for cId in connectedServerIds:
        dbConnectionList.append(DbConnection(cId))
        
    for dCL in dbConnectionList:
        dCL.initConnection()
        
    for dCL in dbConnectionList:
        if dCL.initialized == False:
            print("Connection {} wasn't initialized".format(dCL.sqlConnectionId))

    return err

async def addNewServerDatabase(guild):
    global dbConnectionList
    
    connFile = open('ConnectedServerIdList.txt', 'r+')
    connectedServerIdList = connFile.read()
    
    serverIdsTok = [x for x in connectedServerIdList.split('\n') if x.strip()] # Tokenize
    
    foundServer = False
    
    for tok in serverIdsTok:
        if (int(tok) == guild.id):
            foundServer = True
            break
    
    if foundServer == False:
        connFile.write('{}\n'.format(str(guild.id)))
    
    connFile.close()
    
    newDbConnection = DbConnection(guild.id)
    newDbConnection.initConnection()
    if(newDbConnection.initialized):
        dbConnectionList.append(newDbConnection)
    else:
        print("Error adding DbConnection for guild {0} (id {1})".format(guild.name, guild.id))

# Print a list of all servers with databases
def listConnectedServers():
    global dbConnectionList
    for c in dbConnectionList:
        print('{}'.format(c.sqlConnectionId))
    
async def getRoleMessageForGuild(guildId):
    return 0

async def saveGuildRoleMessageId(guildId, messageId):
    pass

# Get the DbConnection based on the given guildId, returns None if none found
def getDbConnection(guildId):
    global dbConnectionList
    for db in dbConnectionList:
        if db.sqlConnectionId == guildId:
            return db
    return None
      
# Instance of a running sqlite3 database connection
class DbConnection:
    def __init__(self, connectionId):
        self.sqlConnectionId = connectionId
        self.sqlConnection = None
        self.initialized = False
        
    def initConnection(self):
        try:
            os.chdir('sqliteDatabases')
            self.sqlConnection = sqlite3.connect(self.sqlConnectionId + '.db')
            self.initialized = (self.sqlConnection != None)
            os.chdir('../')
        except Exception as exc:
            print('Exception in initConnection ({0}): {1}'.format(self.sqlConnectionId, exc))
    
