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

nb_noeuds = 0
    
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


def eval(board):
    valeurs = {'K':200, 
               'Q':9, 
               'R':5, 
               'B':3, 
               'N':3, 
               'P':1,
               '.':0}
    
    score = 0
    for k,p in board.piece_map().items():
        if(p.symbol() == p.symbol().upper()):
            score += valeurs[p.symbol()]
            score +=  (k//8) * 0.2
        else:
            score -= valeurs[p.symbol().upper()]
            score -= 1 - ((k//8) * 0.2)
    return score


#------ Fin Eval -------#





#------ MinMax methode -------#





def MaxMin(b,p):
    if b.is_game_over():
        if(b.result() == "1-0"):
            return 1000
        elif(b.result() == "0-1"):
            return -1000
        return 0
    if p == 0:
        return eval(b)
    max = -10000
    for m in b.generate_legal_moves():
        b.push(m)
        v = MinMax(b,p-1)
        if(v > max):
            max = v
        b.pop()
    return max
        
def MinMax(b,p):
    if b.is_game_over():
        if(b.result() == "1-0"):
            return 1000
        elif(b.result() == "0-1"):
            return -1000
        return 0
    if p == 0:
        return eval(b)
    min = 10000
    for m in b.generate_legal_moves():
        b.push(m)
        v = MaxMin(b,p-1)
        if(v < min):
            min = v
        b.pop()
    return min

def init(b,p,player):
    coup = 0
    if(player):
        value = -100000
        for m in b.generate_legal_moves():
            b.push(m)
            v = MaxMin(b,p-1)
            if(v > value):
                value = v
                coup = m
            b.pop()
    else:
        value = 100000
        for m in b.generate_legal_moves():
            b.push(m)
            v = MinMax(b,p-1)
            if(v < value):
                value = v
                coup = m
            b.pop()
    return coup   

def playGame(b,p,player):
    print("----------")
    print(b)
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
            return 1000
        elif(board.result() == "0-1"):
            return -1000
        return 0
    if p == 0:
        return eval(board)
    for m in board.generate_legal_moves():
        board.push(m)
        a = max(MinValue(board, a, b, p-1), a)
        if(a >= b):
            board.pop()
            return b
        board.pop()
    return a



def MinValue(board, a, b, p):
    if board.is_game_over():
        if(board.result() == "1-0"):
            return 1000
        elif(board.result() == "0-1"):
            return -1000
        return 0
    if p == 0:
        return eval(board)
    for m in board.generate_legal_moves():
        board.push(m)
        b = min(MaxValue(board, a, b, p-1), b)
        if(a >= b):
            board.pop()
            return a
        board.pop()
    return b

def initValue(board, p):
    coup = 0

    if(player):
        value = -100000
    else:
        value = 100000
    for m in board.generate_legal_moves():
        board.push(m)
        if(player):
            tmp = MinValue(board, -100000, 100000, p-1)
            if(tmp > value):
                value = tmp
                coup = m
        else:
            tmp = MaxValue(board, -100000, 100000, p-1)
            if(tmp > value):
                value = tmp
                coup = m
        board.pop()
    return coup


def playAB(b, p, player):
    print("----------")
    print(b)
    if(player):
        b.push(init(b,p,player))
    else:
        b.push(init(b,p - 1,player))
    if b.is_game_over():
        return b
    if(player):
        player = False
    else:
        player = True
    playGame(b,p,player)

#------ Fin AlphaBeta methode -------#




#------ Main -------#



board = chess.Board()

#deroulementRandom(board)
#print( maxProfondeur(board))
#deroulementExhaustif(board,2)
#playGame(board,3,True)
playAB(board, 3, True)
print("Resultat : " + board.result())

#------ Fin Main -------#