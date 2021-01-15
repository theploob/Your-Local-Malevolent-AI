import sqlite3
import os
from pathlib import Path

dbConnectionList = []

# Init
def Initialize():
    global MasterConnectionFile
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

    connectedServerIds = [x for x in connectedServerIdList.split('\n') if x.strip()]
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

# Print a list of all servers with databases
#TODO
def listConnectedServers():
    global dbConnectionList
    for c in dbConnectionList:
        print('{}'.format(c.sqlConnectionId))
    


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
    
