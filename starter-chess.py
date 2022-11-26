# -*- coding: utf-8 -*-
import time
import chess
from random import choice


#------ Random methode -------#

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.generate_legal_moves()])

def deroulementRandom(b):
    '''Déroulement d'une partie d'échecs au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues et sans gagnant. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement.'''
    print("----------")
    print(b)
    if b.is_game_over():
        print("Resultat : ", b.result())
        return
    b.push(randomMove(b))
    deroulementRandom(b)
    b.pop()

#------ Fin Random methode -------#

#------ Depth methode -------#

global nb_noeuds
noeuds = 1
    
def deroulementExhaustif(b,p, nb_noeud):
    
    if b.is_game_over() or p == 0:
        return nb_noeud
    for m in b.generate_legal_moves():
        b.push(m)
        nb_noeud = deroulementExhaustif(b,p - 1, nb_noeud + 1)
        b.pop()
    return nb_noeud

def maxProfondeur(b):
    p_max = 0
    for p in range (0, 12):
        time_start = time.time()
        nb_noeuds = deroulementExhaustif(b,p,0)
        print_str = "for profondeur " + str(p) + " have " + str(nb_noeuds) + " noeuds"
        print(print_str)
        time_after = time.time()
        if(time_after - time_start > 30):
            p_max = p -1
            break
    return p_max



#------ Fin Depth methode -------#





#------ Eval -------#
pion = { 56:0, 57:0, 58:0, 59:0, 60:0, 61:0, 62:0, 63:0,
 48:50, 49:50, 50:50, 51:50, 52:50, 53:50, 54:50, 55:50,
 40:10, 41:10, 42:20, 43:30, 44:30, 45:20, 46:10, 47:10,
  32:5, 33:5, 34:10, 35:25, 36:25, 37:10, 38:5, 39:5,
  24:0, 25:0, 26:0, 27:20, 28:20, 29:0, 30:0, 31:0,
  16:5, 17:-5, 18:-10, 19:0, 20:0, 21:-10, 22:-5, 23:5,
  8:5, 9:10, 10:10, 11:-20, 12:-20, 13:10, 14:10, 15:5,
  0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}

def eval(board):
    valeurs = {'K':20000, 
               'Q':900, 
               'R':500, 
               'B':330, 
               'N':320, 
               'P':100,
               '.':0}
    
    score = 0
    for k,p in board.piece_map().items():
        if(p.symbol() == p.symbol().upper()):
            score += valeurs[p.symbol()]
            
            score +=  (k//8) * 0.2
        else:
            score -= valeurs[p.symbol().upper()]
            if(p.symbol() == 'p'):
            score -= ((k//8) * 0.2)
    return score


#------ Fin Eval -------#





#------ MinMax methode -------#





def MaxMin(b,p):
    if b.is_game_over():
        if(b.result() == "1-0"):
            return 100000
        elif(b.result() == "0-1"):
            return -100000
        return 0
    if p == 0:
        return eval(b)
    max = -1000000
    for m in b.generate_legal_moves():
        b.push(m)
        global noeuds
        noeuds += 1
        v = MinMax(b,p-1)
        if(v > max):
            max = v
        b.pop()
    return max
        
def MinMax(b,p):
    if b.is_game_over():
        if(b.result() == "1-0"):
            return -100000
        elif(b.result() == "0-1"):
            return 100000
        return 0
    if p == 0:
        return eval(b)
    min = 1000000
    for m in b.generate_legal_moves():
        b.push(m)
        global noeuds
        noeuds += 1
        v = MaxMin(b,p-1)
        if(v < min):
            min = v
        b.pop()
    return min

def init(b,p,player):
    coup = 0
    global noeuds
    if(player):
        value = -10000000
        for m in b.generate_legal_moves():
            b.push(m)
            noeuds += 1
            v = MaxMin(b,p-1)
            if(v > value):
                value = v
                coup = m
            b.pop()
    else:
        value = 10000000
        for m in b.generate_legal_moves():
            b.push(m)
            noeuds += 1
            v = MinMax(b,p-1)
            if(v < value):
                value = v
                coup = m
            b.pop()
    return coup   

def playGame(b,p,player):
    if(player):
        b.push(init(b,p,player))
    else:
        b.push(init(b,p,player))

    if b.is_game_over():
        return b
    if(player):
        player = False
    else:
        player = True
    playGame(b,p,player)



#------ Fin MinMax methode -------#




#------ AlphaBeta methode -------#


def MaxValue(board, a, b, p):
    if board.is_game_over():
        if(board.result() == "1-0"):
            return 100000
        elif(board.result() == "0-1"):
            return -100000
        return 0
    if p == 0:
        return eval(board)
    for m in board.generate_legal_moves():
        board.push(m)
        global noeuds
        noeuds += 1
        a = max(MinValue(board, a, b, p-1), a)
        if(a >= b):
            board.pop()
            return b
        board.pop()
    return a



def MinValue(board, a, b, p):
    if board.is_game_over():
        if(board.result() == "1-0"):
            return -100000
        elif(board.result() == "0-1"):
            return 100000
        return 0
    if p == 0:
        return eval(board)
    for m in board.generate_legal_moves():
        board.push(m)
        global noeuds 
        noeuds += 1
        b = min(MaxValue(board, a, b, p-1), b)
        if(a >= b):
            board.pop()
            return a
        board.pop()
    return b

def initValue(board, p, player):
    coup = randomMove(board)

    if(player):
        value = -100000
    else:
        value = 100000
    for m in board.generate_legal_moves():
        board.push(m)
        global noeuds 
        noeuds += 1
        if(player):
            tmp = MaxValue(board, -1000000, 1000000, p-1)
            if(tmp >= value):
                value = tmp
                coup = m
        else:
            tmp = MinValue(board, -1000000, 1000000, p-1)
            if(tmp <= value):
                value = tmp
                coup = m
        board.pop()
    return coup


def playAB(b, p_a, p_e, player):
    #print("----------")
    #print(b)
    if(player):
        b.push(initValue(b,p_a,player))
    else:
        b.push(initValue(b,p_e,player))
    if b.is_game_over():
        return b
    if(player):
        player = False
    else:
        player = True
    playAB(b, p_a, p_e, player)

#------ Fin AlphaBeta methode -------#



#------ MinMax vs AlphaBeta -------#


def duel():
    return

#------ Fin MinMax vs AlphaBeta -------#



#------ Main -------#



board = chess.Board()
print(board)
#board.push(randomMove(board))
for k,p in board.piece_map().items():
    print(k)
print(board)
#deroulementRandom(board)
#print( maxProfondeur(board))
#deroulementExhaustif(board,2)
#playGame(board,3,True)
#playAB(board, 1, 3, False)
playAB(board, 3, 1, True)
print("Nb noeuds : " + str(noeuds) + "\n")
print("Resultat : " + board.result() + "\n")

#------ Fin Main -------#