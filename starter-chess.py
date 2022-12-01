# -*- coding: utf-8 -*-
import time
import os
import chess
import random
from random import choice

import sys
sys.setrecursionlimit(10000)


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
pst_pawn = [
  0, 0, 0, 0, 0, 0, 0, 0,
 50, 50, 50, 50, 50, 50, 50, 50,
 10, 10, 20, 30, 30, 20, 10, 10,
  5, 5, 10, 25, 25, 10, 5, 5,
  0, 0, 0, 20, 20, 0, 0, 0,
  5, -5, -10, 0, 0, -10, -5, 5,
  5, 10, 10,-20,-20, 10, 10, 5,
  0, 0, 0, 0, 0, 0, 0, 0
]

pst_knight = [
  -50,-40,-30,-30,-30,-30,-40,-50,
 -40,-20, 0, 0, 0, 0,-20,-40,
 -30, 0, 10, 15, 15, 10, 0, -30,
 -30, 5, 15, 20, 20, 15, 5, -30,
 -30, 0, 15, 20, 20, 15, 0, -30,
 -30, 5, 10, 15, 15, 10, 5, -30,
 -40,-20, 0, 5, 5, 0,-20,-40,
 -50,-40,-30,-30,-30,-30,-40,-50
]

pst_bishop = [
  -20,-10,-10,-10,-10,-10,-10,-20,
 -10, 0, 0, 0, 0, 0, 0,-10,
 -10, 0, 5, 10, 10, 5, 0, -10,
 -10, 5, 5, 10, 10, 5, 5, -10,
 -10, 0, 10, 10, 10, 10, 0, -10,
 -10, 10, 10, 10, 10, 10, 10, -10,
 -10, 5, 0, 0, 0, 0, 5, -10,
 -20,-10,-10,-10,-10,-10,-10,-20,
]

pst_rook = [
  0, 0, 0, 0, 0, 0, 0, 0,
   5, 10, 10, 10, 10, 10, 10, 5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
   0, 0, 0, 5, 5, 0, 0, 0
]

pst_queen = [
 -20,-10,-10, -5, -5,-10,-10,-20,
 -10, 0, 0, 0, 0, 0, 0,-10,
 -10, 0, 5, 5, 5, 5, 0, -10,
  -5, 0, 5, 5, 5, 5, 0, -5,
   0, 0, 5, 5, 5, 5, 0, -5,
 -10, 5, 5, 5, 5, 5, 0, -10,
 -10, 0, 5, 0, 0, 0, 0, -10,
 -20,-10,-10, -5, -5,-10,-10,-20
]

pst_king = [
  -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -20,-30,-30,-40,-40,-30,-30,-20,
 -10,-20,-20,-20,-20,-20,-20,-10,
  20, 20, 0, 0, 0, 0, 20, 20,
  20, 30, 10, 0, 0, 10, 30, 20
]

#[#Withe K,Q,R,B,N,P, #Black k,q,r,b,n,p]
#set the nb of each pieces
#first pos is the total nb
def count_pieces(board):
    count_tab = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    for k,p in board.piece_map().items():
        if p.symbol() == 'P':
            count_tab[0] += 1
            count_tab[6] += 1
        if p.symbol() == 'N':
            count_tab[0] += 1
            count_tab[5] += 1
        if p.symbol() == 'B':
            count_tab[0] += 1
            count_tab[4] += 1
        if p.symbol() == 'R':
            count_tab[0] += 1
            count_tab[3] += 1
        if p.symbol() == 'K':
            count_tab[0] += 1
            count_tab[2] += 1
        if p.symbol() == 'Q':
            count_tab[0] += 1
            count_tab[1] += 1
        if p.symbol() == 'p':
            count_tab[0] += 1
            count_tab[12] += 1
        if p.symbol() == 'n':
            count_tab[0] += 1
            count_tab[11] += 1
        if p.symbol() == 'b':
            count_tab[0] += 1
            count_tab[10] += 1
        if p.symbol() == 'r':
            count_tab[0] += 1
            count_tab[9] += 1
        if p.symbol() == 'K':
            count_tab[0] += 1
            count_tab[8] += 1
        if p.symbol() == 'q':
            count_tab[0] += 1
            count_tab[7] += 1
    return count_tab

def psb_rook(board,k):
    malus = 0
    ratio = 2 / 24
    if k//8 != 0:
        if(board.piece_at(((k//8) - 1) + k%8) != None):
            malus += valeurs['R'] * ratio
    else:
        malus += valeurs['R'] * ratio
    
    if k//8 != 7:
        if(board.piece_at(((k//8) + 1) + k%8) != None):
            malus += valeurs['R'] * ratio
    else:
        malus += valeurs['R'] * ratio
    
    if k%8 != 0:
        if(board.piece_at(((k%8) - 1) + ((k//8) * 8)) != None):
            malus += valeurs['R'] * ratio
    else:
        malus += valeurs['R'] * ratio
    
    if k%8 != 7:
        if(board.piece_at(((k%8) + 1) + ((k//8) * 8)) != None):
            malus += valeurs['R'] * ratio
    else:
        malus += valeurs['R'] * ratio
    return malus

valeurs = {'K':20000, 
               'Q':900, 
               'R':500, 
               'B':330, 
               'N':320, 
               'P':100,
               '.':0}

def eval(board, player, old_pieces):
    score = 0
    new_withe = 0
    new_black = 0
    pieces = count_pieces(board)
    #print("piece[0] = " + str(pieces[0]) + "   old_pieces[0] = " + str(old_pieces[0]))
    if(pieces[0] != old_pieces[0]):
        ratio = 2
        for i in range(1,13,1):
            if(pieces[i] != old_pieces[i]):
                if(i%6 == 1):
                    score -= valeur['K'] * ratio
                if(i%6 == 2):
                    score -= valeur['Q'] * ratio
                if(i%6 == 3):
                    score -= valeur['R'] * ratio
                if(i%6 == 4):
                    score -= valeur['B'] * ratio
                if(i%6 == 5):
                    score -= valeur['N'] * ratio
                if(i%6 == 0):
                    score -= valeur['P'] * ratio
                if(i <= 6):
                    score = -score
                break
    for k,p in board.piece_map().items():
        if(p.symbol() == p.symbol().upper()):
            score += valeurs[p.symbol()]
            if p.symbol() == 'P':
                score += pst_pawn[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'N':
                score += pst_knight[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'B':
                score += pst_bishop[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'R':
                score += pst_rook[((7 - (k//8)) * 8) + (k%8)]
                #score -= psb_rook(board,k)
            if p.symbol() == 'K':
                score += pst_king[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'Q':
                score += pst_queen[((7 - (k//8)) * 8) + (k%8)]
        else:
            score -= valeurs[p.symbol().upper()]
            if p.symbol() == 'p':
                score -= pst_pawn[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'n':
                score -= pst_knight[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'b':
                score -= pst_bishop[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'r':
                score -= pst_rook[((7 - (k//8)) * 8) + (k%8)]
                #score += psb_rook(board,k)
            if p.symbol() == 'K':
                score -= pst_king[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'q':
                score -= pst_queen[((7 - (k//8)) * 8) + (k%8)]
    return score


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
        return eval(b,player,count_pieces(board))
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
        return eval(b,player,count_pieces(board))
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
        return eval(b,player,count_pieces(board))
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
        return eval(board, player,count_pieces(board))
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
        return eval(board, player,count_pieces(board))
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


def playDuel(b,p_a,p_e,player):
    #print("----------")
    #print(b)
    if(player):
        b.push(init(b,p_a,player))
    else:
        b.push(initValue(b,p_e,player))
    if b.is_game_over():
        return b
    if(player):
        player = False
    else:
        player = True
    playDuel(b, p_a, p_e, player)

def duel(b,p_a,p_e,player,rounde):
    times = []
    score = [0,0]
    noeud = []
    global noeuds
    r = rounde
    while(r > 0):
        noeuds = 1
        b.reset()
        time_start = time.time()
        playDuel(b,p_a,p_e,player)
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
        player = not player
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
    print("pourcentage de chance de victoire : " + str(score[0] / rounde *100))


#------ Fin MinMax vs AlphaBeta -------#



#------ Simulation Joueur VS Machine -------#

def printinfo():
    print("Règles d'utilisation :")
    print(" -\"i\" pour afficher / ne plus afficher les règles d'utilisation")
    print(" -\"entrer\" pour valider la selection")
    print(" -\"z, q, s, d\" pour vous déplacer")
    print(" -\"espace\" pour selectionner une pièce ({ }) ou pour placer la pièce sélectionnée (| |)")
    print(" -\"r\" pour déselectionner une pièce")
    print(" -\"e \" pour quitter le jeu")

def reverse(s):
    str = ""
    for i in s:
        str = i + str
    return str

def printgame(board,cursor,selected,area):
    print("------------------------")
    ligne = ""
    prev_k = 64
    tmp = ""
    for k,p in board.piece_map().items():
        if(k < (prev_k - 1)):
            for i in range ( prev_k-1,k, -1):
                if(selected):
                    if((i+1) % 8 == 0):
                        ligne = ligne + reverse(tmp) + '\n'
                        tmp = ""
                        if( area // 8 == (i // 8) + 1):
                            for j in range (0, 8):
                                if(j == (area % 8)):
                                    tmp += ' ' + '-' + ' '
                                else:
                                    tmp += ' ' + ' ' + ' '
                        if( area // 8 ==  i // 8):
                            for j in range (0, 8):
                                if(j == (area % 8)):
                                    tmp += ' ' + '-' + ' '
                                else:
                                    tmp += ' ' + ' ' + ' '
                        ligne = ligne + tmp + '\n'
                        tmp = ""
                else:
                    if((i+1) % 8 == 0):
                        ligne = ligne + reverse(tmp) + '\n' + '\n'
                        tmp = ""
                if(i == cursor):
                    tmp = tmp +  '}'
                    tmp = tmp + '.'
                    tmp = tmp + '{'
                elif(i == area):
                    tmp = tmp +  '|'
                    tmp = tmp + '.'
                    tmp = tmp + '|'
                else:
                    tmp = tmp + ' '
                    tmp = tmp + '.'
                    tmp = tmp + ' '
        if((k+1) % 8 == 0):
            if(selected):
                if((k+1) % 8 == 0):
                    ligne = ligne + reverse(tmp) + '\n'
                    tmp = ""
                    if( area // 8 == (k // 8) + 1):
                            for j in range (0, 8):
                                if(j == (area % 8)):
                                    tmp += ' ' + '-' + ' '
                                else:
                                    tmp += ' ' + ' ' + ' '
                    if( area // 8 ==  k // 8):
                        for j in range (0, 8):
                            if(j == (area % 8)):
                                tmp += ' ' + '-' + ' '
                            else:
                                tmp += ' ' + ' ' + ' '
                    ligne = ligne + tmp + '\n'
                    tmp = ""
            else:
                if((k+1) % 8 == 0):
                    ligne = ligne + reverse(tmp) + '\n' + '\n'
                    tmp = ""
        if(k == cursor):
            tmp = tmp +  '}'
            tmp = tmp + p.symbol()
            tmp = tmp + '{'
        elif(k == area):
            tmp = tmp +  '|'
            tmp = tmp + p.symbol()
            tmp = tmp + '|'
        else:
            tmp = tmp + ' '
            tmp = tmp + p.symbol()
            tmp = tmp + ' '
        prev_k = k
    if(prev_k != 0):
        for i in range ( prev_k-1,-1, -1):
            if(selected):
                if((i+1) % 8 == 0):
                    if( area // 8 == (i // 8) + 1):
                        for j in range (0, 8):
                            if(j == (area % 8)):
                                tmp += ' ' + '-' + ' '
                            else:
                                tmp += ' ' + ' ' + ' '
                    if( area // 8 ==  i // 8):
                        for j in range (0, 8):
                            if(j == (area % 8)):
                                tmp += ' ' + '-' + ' '
                            else:
                                tmp += ' ' + ' ' + ' '
                    ligne = ligne + tmp + '\n'
                    tmp = ""
            else:
                if((i+1) % 8 == 0):
                    ligne = ligne + reverse(tmp) + '\n'
                    tmp = ""
            if(i == cursor):
                tmp = tmp +  '}'
                tmp = tmp + '.'
                tmp = tmp + '{'
            elif(i == area):
                tmp = tmp +  '|'
                tmp = tmp + '.'
                tmp = tmp + '|'
            else:
                tmp = tmp + ' '
                tmp = tmp + '.'
                tmp = tmp + ' '
    ligne = ligne + reverse(tmp) + '\n'
    tmp = ""
    print(k)
    if(selected):
        if( area // 8 == (k // 8)):
                for j in range (0, 8):
                    if(j == (area % 8)):
                        tmp += ' ' + '-' + ' '
                    else:
                        tmp += ' ' + ' ' + ' '
        ligne = ligne + tmp 
        tmp = ""
    print(ligne)
    print("------------------------")
    return

global cursor
global selected
global area
global board
global print_info

def selectf():
    running = True
    select = 1
    while(running):
        os.system('clear')
        print("Pour jouer aux échecs contre contre une IA, vous devez choissir quel doit être l'algorithme contre lequel vous allez vous battre")
        print("Choisir entre :")
        if(select == 1):
            print("1) *- MaxMin")
            print("2)  - AlphaBeta")
        else:
            print("1)  - MaxMin")
            print("2) *- AlphaBeta")
        tmp = input("Choisir 1 ou 2 :\n")
        if(tmp == ''):
            if(select == 1):
                return init
            else:
                return initValue
        if( tmp[0] == '1'):
            print("ok1")
            select = 1
        if(tmp[0] == '2'):
            print("ok2")
            select = 2
        

def select_p():
    running = True
    while(running):
        os.system('clear')
        print("Pour jouer aux échecs contre contre une IA, vous devez choissir quel doit être la profondeur pour l'algorithme choisit")
        tmp = input("Choisir un chiffre entre 1 et 4 :\n")
        if( int(tmp) >= 1 and int(tmp) <= 4):
            return int(tmp)

def init_game(board):
    f = selectf()
    p = select_p()
    global selected
    global cursor
    global area 
    global print_info
    print_info = True
    area = -1
    selected = False
    if(selected):
        area = cursor
    cursor = 27
    main(f, p, board)

def main(f, p, board):
    loop(board, f, p)
    return
def restart(board):
    again_re = True
    running = True
    while(running):
        os.system('clear')
        if(board.result() == "1-0"):
            print("Bravo ! Tu as gagnée !")
        elif(board.result() == "0-1"):
            print("C'est pas grave ! Tu y arriveras la prochaine fois !")
        else:
            print("Dommage ! C'était pas loin !")
        print()
        print("Voulez vous rejouer ?")
        tmp = input("Choisir \"oui\" ou \"non\" :\n")
        if tmp == "oui":
            again_re = True
            running = False
        if tmp == "non":
            again_re = False
            running = False
    if(again_re):
        f = selectf()
        p = select_p()
        board.reset()
        return f,p
    return -1
    
def loop(board, f, p):
    while(1):
        os.system('clear')
        global cursor
        global selected
        global area
        global print_info
        printgame(board, cursor, selected, area)
        if(print_info):
            printinfo()
        string = input("Choose action :\n")
        if len(string) > 0:
            if(string[0] == 'z'):
                if(selected):
                    if((area // 8) == 7):
                        area = area % 8
                    else:
                        area += 8   
                else:
                    if((cursor // 8) == 7):
                        cursor = cursor % 8
                    else:
                        cursor += 8 
                
            if(string[0] == 'q'):
                if(selected):
                    if((area) % 8 == 0):
                        area += 7
                    else:
                        area -= 1 
                else: 
                    if((cursor) % 8 == 0):
                        cursor += 7
                    else:
                        cursor -= 1 

            if(string[0] == 's'):
                if(selected):
                    if((area // 8) == 0):
                        area = 56 + (area % 8)
                    else:
                        area -= 8 

                else:
                    if((cursor // 8) == 0):
                        cursor = 56 + (cursor % 8)
                    else:
                        cursor -= 8 

            if(string[0] == 'd'):
                if(selected):
                    if(area % 8 == 7):
                        area -= 7
                    else:
                        area += 1 
                else:    
                    if(cursor % 8 == 7):
                        cursor -= 7
                    else:
                        cursor += 1 
            if(string[0] == 'r'):
                if(selected):
                    area = -1
                    selected = not selected
            if(string[0] == ' '):
                if(selected):
                    find = False
                    for m in board.generate_legal_moves():
                        cursor_pos = m.from_square
                        dest_pos = m.to_square
                        if cursor_pos == cursor and dest_pos == area:
                            board.push(m)
                            if(board.is_game_over()):
                                
                                tmp = restart(board)
                                if(tmp == -1):
                                    return
                                else:
                                    f = tmp[0]
                                    p = tmp[1]
                                    area = -1
                                    selected = False
                                break
                            os.system('clear')
                            printgame(board,cursor, selected, area)
                            selected = not selected
                            board.push(f(board, p, False))
                            area = -1
                    
                else:
                    area = cursor
                    selected = not selected
            
            if(string[0] == 'e'):
                return
            if(string[0] == 'i'):
                print_info = not print_info
    return

#------ Fin MinMax vs SimAlphaBetaulation Joueur VS Machine -------#



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
roundMatch(board,10,2,1,True)
#playAB(board, 1, 3, False)
#playAB(board, , 1, True)

#duel(board,1,1,True,100)

#print("Nb noeuds : " + str(noeuds) + "\n")
#print("Resultat : " + board.result() + "\n")

#init_game(board)

#------ Fin Main -------#