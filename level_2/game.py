import copy

VIC = 10 ** 20  # The value of a winning board (for max)
LOSS = -VIC  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # The length of a winning sequence
COMPUTER = SIZE + 1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board
ROWS = 6
COLUMN = 7

'''
The state of the game is represented by a list of 4 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
   the comp's cells = COMPUTER and the human's = HUMAN
1. The heuristic value of the state.
2. Who's turn is it: HUMAN or COMPUTER
3. number of empty cells
4. list of how many cells full in each column
'''


def create():
    # Returns an empty board. The human plays first.
    board = []
    for i in range(ROWS):
        board = board + [COLUMN * [0]]
    return [board, 0.00001, HUMAN, ROWS * COLUMN, [5, 5, 5, 5, 5, 5, 5]]


def value(s):
    # Returns the heuristic value of s
    return s[1]


def printState(s):
    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prins who won.
    for r in range(ROWS):
        print("\n -- -- -- -- -- -- -- \n|", end="")
        for c in range(COLUMN):
            if s[0][r][c] == COMPUTER:
                print("X |", end="")
            elif s[0][r][c] == HUMAN:
                print("O |", end="")
            else:
                print(" ", "|", end="")
    print("\n -- -- -- -- -- -- -- \n ", end="")
    print("1  2  3  4  5  6  7 \n")
    if value(s) == VIC:
        print("Ha ha ha I won!")
    elif value(s) == LOSS:
        print("You did it!")
    elif value(s) == TIE:
        print("It's a TIE")


def isFinished(s):
    # Seturns True if the game ended
    return s[1] in [LOSS, VIC, TIE]


def isHumTurn(s):
    # Returns True if it the human's turn to play
    return s[2] == HUMAN


def whoIsFirst(s):
    # The user decides who plays first
    # if int(input("Who plays first? 1-me / anything else-you. : ")) == 1:
    s[2] = COMPUTER


# else:
#   s[2] == HUMAN


def checkSeq(s, r1, c1, r2, c2):
    # r1, c1 are in the board. if r2,c2 not on board returns 0.
    # Checks the seq. from r1,c1 to r2,c2. If all X returns VIC. If all O returns LOSS.
    # If no Os returns 1. If no Xs returns -1, Otherwise returns 0.
    if r2 < 0 or c2 < 0 or r2 >= ROWS or c2 >= COLUMN or s[0][r2][c2] != 0:
        return 0  # r2, c2 are illegal
    dr = (r2 - r1) // (SIZE - 1)  # the horizontal step from cell to cell
    dc = (c2 - c1) // (SIZE - 1)  # the vertical step from cell to cell
    sum = 0
    for i in range(SIZE):  # summing the values in the seq.
        sum += s[0][r1 + i * dr][c1 + i * dc]
    if sum == COMPUTER * SIZE:
        return VIC
    if sum == HUMAN * SIZE:
        return LOSS
    if sum > 0 and sum < COMPUTER:
        return -1
    if sum > 0 and sum % COMPUTER == 0:
        return 1
    return 0


def makeMove(s, c):
    # Puts mark (for huma. or comp.) in r,c
    # switches turns
    # and re-evaluates the heuristic value.
    # Assumes the move is legal.
    r = s[4][c] # finde the next row of the column
    s[0][r][c] = s[2]  # marks the board
    s[3] -= 1  # one less empty cell
    s[2] = COMPUTER + HUMAN - s[2]  # switches turns
    dr = [-SIZE + 1, -SIZE + 1, 0, SIZE - 1]  # the next lines compute the heuristic val.
    dc = [0, SIZE - 1, SIZE - 1, SIZE - 1]
    s[1] = 0.00001
    for row in range(len(s[0])):
        for col in range(len(s[0][0])):
            for i in range(len(dr)):
                 t = checkSeq(s, row , col, row + dr[i], col + dc[i])
                 if t in [LOSS, VIC]:
                     s[1] = t
                     return
                 else:
                    s[1] += t
    s[4][c] -= 1  # one less empty cell in the column
    if s[3] == 0:
        s[1] = TIE


def inputMove(s):
    # Reads, enforces legality and executes the user's move.
    printState(s)
    flag = True
    while flag:
        move = int(input("Enter your next place: "))
        if move <= 0 or move > COLUMN:
            print("Illegal place.")
        elif s[4][move - 1] == -1:
            print("Illegal place, the column is full.")
        else:
            flag = False
            makeMove(s, move-1)


def getNext(s):
    # returns a list of the next states of s
    ns = []
    if s[3]==42:
         tmp = copy.deepcopy(s)
         makeMove(tmp, 3)
         ns += [tmp]
    else:
          for c in range(COLUMN):
              columnPlace = s[4][c]
              if s[0][columnPlace][c] == 0:
                  tmp = copy.deepcopy(s)
                  makeMove(tmp, c)
                  ns += [tmp]
    return ns
