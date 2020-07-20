import CommandRoll

tokenArray = []
tokenOps = []
parseStack = []
unparsedOps = []
unparsedArray = []
OP_INT = 0
OP_ADD = 1
OP_MULT = 2
OP_DIE = 3
OP_KEEP = 4
OP_CONDITION = 5
OP_EXP = 6
OP_STPAR = 7
OP_ENPAR = 8
OP_BRIEF = 9

def debug():
    tstr = '2d20+3kl1'
    global tokenArray
    global tokenOps
    tokenArray = CommandRoll.createTokenArray(tstr)
    if tokenArray == None:
        print('Error in create token array')
    tokenOps = CommandRoll.tokenArrayToOpArray(tokenArray)
    if tokenOps == None:
        print('Error in token to op array')
    if CommandRoll.checkGrammar(tokenOps) == False: # Go back to school
        print('Bad grammar')
        
    # tokenArray
    # tokenOps
    
def lrParse():
    global parseStack
    global unparsedOps
    global unparsedArray
    parseStack = []
    unparsedOps = tokenOps.copy() # Remaining operator types, non-explicit
    unparsedArray = tokenArray.copy() # Remaining array, carries the explicit commands
    
    


