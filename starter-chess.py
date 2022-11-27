# -*- coding: utf-8 -*-
import time
import chess
import random
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
pst_pawn = {
  0, 0, 0, 0, 0, 0, 0, 0,
 50, 50, 50, 50, 50, 50, 50, 50,
 10, 10, 20, 30, 30, 20, 10, 10,
  5, 5, 10, 25, 25, 10, 5, 5,
  0, 0, 0, 20, 20, 0, 0, 0,
  5, -5, -10, 0, 0, -10, -5, 5,
  5, 10, 10,-20,-20, 10, 10, 5,
  0, 0, 0, 0, 0, 0, 0, 0
}

pst_knight = {
  -50,-40,-30,-30,-30,-30,-40,-50,
 -40,-20, 0, 0, 0, 0,-20,-40,
 -30, 0, 10, 15, 15, 10, 0, -30,
 -30, 5, 15, 20, 20, 15, 5, -30,
 -30, 0, 15, 20, 20, 15, 0, -30,
 -30, 5, 10, 15, 15, 10, 5, -30,
 -40,-20, 0, 5, 5, 0,-20,-40,
 -50,-40,-30,-30,-30,-30,-40,-50
}

pst_bishop = {
  -20,-10,-10,-10,-10,-10,-10,-20,
 -10, 0, 0, 0, 0, 0, 0,-10,
 -10, 0, 5, 10, 10, 5, 0, -10,
 -10, 5, 5, 10, 10, 5, 5, -10,
 -10, 0, 10, 10, 10, 10, 0, -10,
 -10, 10, 10, 10, 10, 10, 10, -10,
 -10, 5, 0, 0, 0, 0, 5, -10,
 -20,-10,-10,-10,-10,-10,-10,-20,
}

pst_rook = {
  0, 0, 0, 0, 0, 0, 0, 0,
   5, 10, 10, 10, 10, 10, 10, 5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
   0, 0, 0, 5, 5, 0, 0, 0
}

pst_queen = {
 -20,-10,-10, -5, -5,-10,-10,-20,
 -10, 0, 0, 0, 0, 0, 0,-10,
 -10, 0, 5, 5, 5, 5, 0, -10,
  -5, 0, 5, 5, 5, 5, 0, -5,
   0, 0, 5, 5, 5, 5, 0, -5,
 -10, 5, 5, 5, 5, 5, 0, -10,
 -10, 0, 5, 0, 0, 0, 0, -10,
 -20,-10,-10, -5, -5,-10,-10,-20
}

pst_king = {
  -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -20,-30,-30,-40,-40,-30,-30,-20,
 -10,-20,-20,-20,-20,-20,-20,-10,
  20, 20, 0, 0, 0, 0, 20, 20,
  20, 30, 10, 0, 0, 10, 30, 20
}

def eval(board, player):
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
            if p == 'P':
                score += pst_pawn[i]
            if p == 'N':
                score += pst_knight[i]
            if p == 'B':
                score += pst_bishop[i]
            if p == 'R':
                score += pst_rook[i]
            if p == 'K':
                score += pst_king[i]
            if p == 'Q':
                score += pst_queen[i] 
        else:
            score += valeurs[p.symbol().upper()]
            if p == 'p':
                score += pst_pawn[i]
            if p == 'n':
                score += pst_knight[i]
            if p == 'b':
                score += pst_bishop[i]
            if p == 'r':
                score += pst_rook[i]
            if p == 'q':
                score += pst_queen[i]
    if(player):
        return score
    return -score


#------ Fin Eval -------#



#------ MinMax methode -------#


def MaxMin(b,p,player):
    if b.is_game_over():
        if(b.result() == "1-0"):
            return 100000
        elif(b.result() == "0-1"):
            return -100000
        return 0
    if p == 0:
        return eval(b,player)
    maxm = -1000000
    for m in b.generate_legal_moves():
        b.push(m)
        global noeuds
        noeuds += 1
        v = MinMax(b,p-1,player)
        if(v > maxm):
            maxm = v
        b.pop()
    return maxm
        
def MinMax(b,p,player):
    if b.is_game_over():
        if(b.result() == "1-0"):
            return -100000
        elif(b.result() == "0-1"):
            return 100000
        return 0
    if p == 0:
        return eval(b,player)
    minm = 1000000
    for m in b.generate_legal_moves():
        b.push(m)
        global noeuds
        noeuds += 1
        v = MaxMin(b,p-1,player)
        if(v < minm):
            minm = v
        b.pop()
    return minm

def init(b,p,player):
    if b.is_game_over():
        if(b.result() == "1-0"):
            return -100000
        elif(b.result() == "0-1"):
            return 100000
        return 0
    if p == 0:
        return eval(b,player)
    coup = 0
    global noeuds
    list_best_coup = []
    if(player):
        value = -10000000

        for m in b.generate_legal_moves():
            b.push(m)
            noeuds += 1
            v = MaxMin(b,p-1,player)
            if(v > value):
                list_best_coup = [m]
                value = v
                coup = m
            elif(v == value):
                list_best_coup.append(m)
            b.pop()
    else:
        value = 10000000
        for m in b.generate_legal_moves():
            b.push(m)
            noeuds += 1
            v = MinMax(b,p-1,player)
            if(v < value):
                list_best_coup = [m]
                value = v
                coup = m
            elif(v == value):
                list_best_coup.append(m)
            b.pop()
    if(len(list_best_coup) > 1):
        return list_best_coup[random.randint(0, len(list_best_coup) - 1)]
    return coup   

def playGame(b,p_a,p_e,player):
    #print("----------")
    #print(b)
    if(player):
        b.push(init(b,p_a,player))
    else:
        b.push(init(b,p_e,player))
    if b.is_game_over():
        return b
    if(player):
        player = False
    else:
        player = True
    playGame(b,p_a,p_e,player)

def roundMatch(b,rounde,p_a,p_e,player):
    times = []
    score = [0,0]
    noeud = []
    global noeuds
    r = rounde
    while(r >= 0):
        noeuds = 1
        b.reset()
        time_start = time.time()
        playGame(b,p_a,p_e,player)
        time_end = time.time()
        print("time : " + str(time_end - time_start))
        times.append(time_end - time_start)
        if(b.result() == "1-0"):
            score[0] += 1
        elif(b.result() == "0-1"):
            score[1] += 1
        else:
            score[0] += 0.5
            score[1] += 0.5
        print("score : " + str(score[0]) + "-" + str(score[1]))
        noeud.append(noeuds)
        print("Nb noeuds : " + str(noeuds))
        r -= 1
    temps = 0
    node = 0
    for time_e in times:
        temps += time_e
    temps = temps / len(times)
    for ne in noeud:
        node += ne
    node = node / len(noeud)
    print("temps moyen : " + str(temps))
    print("nombre de noeuds moyen : " + str(node))
    print("pourcentage de chance de victoire : " + str(score[0] / (rounde + 1) *100))





#------ Fin MinMax methode -------#




#------ AlphaBeta methode -------#


def MaxValue(board, a, b, p, player):
    if board.is_game_over():
        if(board.result() == "1-0"):
            return 100000
        elif(board.result() == "0-1"):
            return -100000
        return 0
    if p == 0:
        return eval(board, player)
    for m in board.generate_legal_moves():
        board.push(m)
        global noeuds
        noeuds += 1
        a = max(MinValue(board, a, b, p-1,not player), a)
        if(a >= b):
            board.pop()
            return b
        board.pop()
    return a



def MinValue(board, a, b, p, player):
    if board.is_game_over():
        if(board.result() == "1-0"):
            return -100000
        elif(board.result() == "0-1"):
            return 100000
        return 0
    if p == 0:
        return eval(board, player)
    for m in board.generate_legal_moves():
        board.push(m)
        global noeuds 
        noeuds += 1
        b = min(MaxValue(board, a, b, p-1, not player), b)
        if(a >= b):
            board.pop()
            return a
        board.pop()
    return b

def initValue(board, p, player):
    coup = randomMove(board)
    if board.is_game_over():
        if(board.result() == "1-0"):
            return -100000
        elif(board.result() == "0-1"):
            return 100000
        return 0
    if p == 0:
        return coup
    if(player):
        value = -1000000
    else:
        value = 1000000
    for m in board.generate_legal_moves():
        board.push(m)
        global noeuds 
        noeuds += 1
        tmp = 0
        if(player):
            tmp = MinValue(board, -1000000, 1000000, p-1, not player)
            if(tmp >= value):
                value = tmp
                coup = m
        else:
            tmp = MaxValue(board, -1000000, 1000000, p-1, not player)
            if(tmp >= value):
                value = tmp
                coup = m
        board.pop()
    return coup


def playAB(b, p_a, p_e, player):
    print("----------")
    print(b)
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


def makeRound(b,p_a,p_e,player):
    times = []
    score = [0,0]
    noeud = []
    global noeuds
    r = rounde
    while(r >= 0):
        noeuds = 1
        b.reset()
        time_start = time.time()
        playAB(b,p_a,p_e,player)
        time_end = time.time()
        print("time : " + str(time_end - time_start))
        times.append(time_end - time_start)
        if(b.result() == "1-0"):
            score[0] += 1
        elif(b.result() == "0-1"):
            score[1] += 1
        else:
            score[0] += 0.5
            score[1] += 0.5
        print("score : " + str(score[0]) + "-" + str(score[1]))
        noeud.append(noeuds)
        print("Nb noeuds : " + str(noeuds))
        r -= 1
    temps = 0
    node = 0
    for time_e in times:
        temps += time_e
    temps = temps / len(times)
    for ne in noeud:
        node += ne
    node = node / len(noeud)
    print("temps moyen : " + str(temps))
    print("nombre de noeuds moyen : " + str(node))
    print("pourcentage de chance de victoire : " + str(score[0] / (rounde + 1) *100))




#------ Fin AlphaBeta methode -------#



#------ MinMax vs AlphaBeta -------#


def duel():
    return

#------ Fin MinMax vs AlphaBeta -------#



#------ Main -------#



board = chess.Board()
#print(board)
#board.push(randomMove(board))
#for k,p in board.piece_map().items():
#    print(k)
#print(board)
#deroulementRandom(board)
#print( maxProfondeur(board))
#deroulementExhaustif(board,2)
#playGame(board,2,1,True)
roundMatch(board,10,3,2,True)
#playAB(board, 1, 3, False)
#playAB(board, 3, 1, True)
print("Nb noeuds : " + str(noeuds) + "\n")
print("Resultat : " + board.result() + "\n")

#------ Fin Main -------#