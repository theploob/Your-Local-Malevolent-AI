

# ADD_OP       + -
# MULT_OP      * /
# DIE_OP       d
# KEEP_OP      k kl
# BRIEF_OP     b
# CONDITION_OP < > = <= >=
# EXP_OP       !
# START_PAREN  (
# END_PAREN    )
# INT          you know this one
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
operators = {                               # OP Code:
    'ADD':       ['+','-'],                 # 1
    'MULT':      ['*','/'],                 # 2
    'DIE':       ['d'],                     # 3
    'KEEP':      ['k','kl'],                # 4
    'CONDITION': ['<','>','<=','>=','='],   # 5
    'EXP':       ['!'],                     # 6
    'STPAR':     ['('],                     # 7
    'ENPAR':     [')'],                     # 8
    'BRIEF':     ['b']                      # 9
    # 'INT':       [0,1,2,...]              # 0
}

allowable_characters = {
    '+','-','*','/','d','k','b','<','>','!','(',')','=',
    'l' # Not used alone, must be with k,<,>
    # multi character inputs: kl, <=, >=
}

# Returns op code # of the given operation token
def getOpCode(token):
    if isNumStr(token):
        return 0
    ops = {
        '+': 1,'-': 1,
        '*': 2, '/': 2,
        'd': 3,
        'k': 4, 'kl': 4,
        '<': 5, '>': 5, '<=': 5, '>=': 5, '=': 5,
        '!': 6,
        '(': 7,
        ')': 8,
        'b': 9
    }
    return ops.get(token, -1)

# Turns the given array of string operators into numeric, generic ones
def tokenArrayToOpArray(tokenArray):
    toksOps = []
    for t in tokenArray:
        opCode = getOpCode(t)
        if opCode != -1:
            toksOps.append(opCode)
        else:
            return None
    return toksOps

# Returns boolean if the given string is of a number
def isNumStr(instr):
    try:
        int(instr)
        return True
    except Exception:
        return False

# Turn the token string into an array of each token piece
# Format is a list of tokens, such as ['4', 'd', '20', '+', etc...]
# Doesn't check grammer, only forms the tokens for later grammar processing
def createTokenArray(tokenString):
    tString = tokenString
    tArray = [] # Array of tokens to build upon
    for n,c in enumerate(tString): # Iterate over tokenString
        if c in allowable_characters or isNumStr(c): # Ensure it is a valid character
            if c == 'l':
                if n != 0:
                    if tArray[-1] == 'k': # Starts with l, incorrect, previous character must be 'k'
                        tArray = tArray[:-1] # Remove the k, make it a 'kl'
                        tArray.append('kl')
                    else:
                        return None
                else:
                    return None
                         
            elif c == '=':
                if n != 0: # Not starting character, could be preceeding < or >
                    if tArray[-1] == '<':
                        tArray = tArray[:-1] # Remove the k, make it a 'kl'
                        tArray.append('<=')
                    elif tArray[-1] == '>':
                        tArray = tArray[:-1] # Remove the k, make it a 'kl'
                        tArray.append('>=')
                    else:
                        tArray.append('=')
                else: # Starts with '='
                    tArray.append('=')
                              
            # Form a number out of possibly multiple individual ints
            elif isNumStr(c):
                if n != 0:
                    if isNumStr(tArray[-1]): # Preceeded by another number, combine
                        prevNum = int(tArray[-1])
                        tArray = tArray[:-1]
                        tArray.append(str(prevNum * 10 + int(c)))     
                    else: # not preceeded by another number, append
                        tArray.append(c)
                else: # Starts with int, just add and move on
                    tArray.append(c)
      
            else:
                tArray.append(c)
        else: # Not an allowable character, return None since string  is unusable TODO just ignore?
            return None
            
    return tArray
    
# Returns true on correct grammar, false otherwise
def checkGrammar(tokenOps):
    # Have toksOps array, ensure no unusable statements occur
    # OP_INT = 0
    # OP_ADD = 1
    # OP_MULT = 2
    # OP_DIE = 3
    # OP_KEEP = 4
    # OP_CONDITION = 5
    # OP_EXP = 6
    # OP_STPAR = 7
    # OP_ENPAR = 8
    # OP_BRIEF = 9
    stparen = 0
    enparen = 0
    # TODO finish grammar checker, find more break cases
    for n,t in enumerate(tokenOps): # Turn into function array switch
        if t == OP_STPAR:
            stparen += 1
        elif t == OP_ENPAR:
            enparen += 1
        elif n == 0: # Things that can't start a statement
            if t in [OP_ADD, OP_MULT, OP_KEEP, OP_CONDITION, OP_EXP, OP_ENPAR]:
                return False
        elif n == len(tokenOps)-1: # Things that can't end a statement
            if t in [OP_ADD, OP_MULT, OP_DIE, OP_CONDITION, OP_STPAR]:
                return False

    if stparen != enparen: # Unequal parenthesis
        return False
    
    return True
    
def parseRoll(inTokenArray, inTokenOps):
    tokenOps = inTokenOps.copy()
    tokenArray = inTokenArray.copy()
    
    briefText = False
    while OP_BRIEF in tokenOps: # Get brief flag, remove otherwise since it doesn't affect the rest of the expression
        briefText = True
        tokenOps.remove(OP_BRIEF)
        tokenArray.remove('b')

    
    

async def entry(cmdArgs, message):
    if cmdArgs == []:
        return
    
    tokenString = ''.join(cmdArgs) # Rejoin args, no spaces left between parts
    tokenArray = createTokenArray(tokenString)
    if tokenArray == None:
        return # Error found in createTokenArray TODO
    tokenOps = tokenArrayToOpArray(tokenArray)
    if tokenOps == None:
        return
    if checkGrammar(tokenOps) == False: # Go back to school
        return
    parseRoll(tokenArray, tokenOps)
    

    
    
    