import CommandRoll

tokenArray = []
tokenOps = []

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
    tokenArray = CommandRoll.createTokenArray(tstr)
    if tokenArray == None:
        print('Error in create token array')
    tokenOps = tokenArrayToOpArray(tokenArray)
    if tokenOps == None:
        print('Error in token to op array')
    if checkGrammar(tokenOps) == False: # Go back to school
        print('Bad grammar')
        
    # tokenArray
    # tokenOps
    
# Recursive processing
# given total tokenArray, total tokenOps make global?
# current set of tokens to process
def process(curSet):
	for n,op in enumerate(curSet):
		if op == OP_STPAR:
            while (curSet[index] != OP_ENPAR) and (curSet[index] != OP_STPAR): # Get position of
                index += 1
