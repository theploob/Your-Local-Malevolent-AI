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

async def removeServerDatabase(guild):
    pass

# Print a list of all servers with databases
def listConnectedServers():
    global dbConnectionList
    for c in dbConnectionList:
        print('{}'.format(c.sqlConnectionId))
    
async def getRoleMessageForGuild(guildId):
    db = getDbConnection(guildId)
    if db == None:
        return 0
    else:
        return db.getRoleMessageId()

async def saveGuildRoleMessageId(guildId, messageId):
    
    # use the guild ID to get the right connection, then save the message ID there
    dbCon = getDbConnection(guildId)
    if dbCon == None:
        print("Error in saveGuildRileMessageId: getDbConnection returned Null")
    else:
        dbCon.saveRoleMessageId(messageId)
    pass

# Get the DbConnection based on the given guildId, returns None if none found
def getDbConnection(guildId):
    global dbConnectionList
    for db in dbConnectionList:
        if int(db.sqlConnectionId) == guildId:
            return db
    return None
      
# Instance of a running sqlite3 database connection
class DbConnection:
    def __init__(self, connectionId):
        self.sqlConnectionId = connectionId
        self.sqlConnection = None
        self.initialized = False
        self.roleMsgId = 0
        
    def initConnection(self):
        try:
            os.chdir('sqliteDatabases')
            self.sqlConnection = sqlite3.connect(self.sqlConnectionId + '.db')
            self.initialized = (self.sqlConnection != None)
            os.chdir('../')
            
            # Set up tables
            c = self.sqlConnection.cursor()
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='rolemessage' ''')
            count = c.fetchone()[0]
            if count == 1:
                pass
            elif count == 0:
                c.execute(''' CREATE TABLE rolemessage (messageid integer) ''')
            else:
                raise MultipleTable
            
            self.roleMsgId = self.getRoleMessageId()
        except Exception as exc:
            print('Exception in initConnection ({0}): {1}'.format(self.sqlConnectionId, exc))
    
        except MultipleTable as exc:
            print("Exception in initConnection: Multiple Tables exist, can't initialize")

    def saveRoleMessageId(self, messageId):
        try:
            c = self.sqlConnection.cursor()
            c.execute(''' DELETE FROM rolemessage ''')
            c.execute(''' INSERT INTO rolemessage VALUES (?) ''', [int(messageId)])
            self.sqlConnection.commit()
            self.roleMsgId = messageId
        except Exception as exc:
            print('Exception in saveRoleMessageId ({0}): {1}'.format(self.sqlConnectionId, exc))
            
    def getRoleMessageId(self):
        try:
            c = self.sqlConnection.cursor()
            c.execute(''' SELECT * FROM rolemessage ''')
            idRow = c.fetchone()
            if idRow == None:
                #raise Exception('Exception in getRoleMessageId ({0}): SELECT FROM returned NULL'.format(self.sqlConnectionId))
                return 0
            self.roleMsgId = idRow[0]
            return idRow[0]
        except Exception as exc:
            print('Exception in getRoleMessageId ({0}): {1}'.format(self.sqlConnectionId, exc))
            
    
    