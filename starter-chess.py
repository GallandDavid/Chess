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
nb_noeuds = 1
noeuds = 1
    
#Déroule tous les jeux possibles pour un état du jeux jusqu'à une profondeur donnée "p"
def deroulementExhaustif(b,p):
    #print(b)
    global nb_noeuds
    if b.is_game_over() or p == 0:
        return
    for m in b.generate_legal_moves():
        b.push(m)
        nb_noeuds += 1
        deroulementExhaustif(b,p - 1)
        b.pop()
    return

#Retourne la profondeur là plus loin pour un état du jeux qui met moins de 30s à s'éxécuter
def maxProfondeur(b):
    global nb_noeuds
    p_max = 0
    for p in range (0, 12):
        time_start = time.time()
        deroulementExhaustif(b,p)
        print_str = "Pour une profondeur p = " + str(p) + " il y a " + str(nb_noeuds) + " noeuds"
        print(print_str)
        time_after = time.time()
        print("Temps écoulé : " + str(time_after - time_start))
        if(time_after - time_start > 30):
            p_max = p -1
            break
    return p_max



#------ Fin Depth methode -------#




#pst_x sont des tableaux de valeur 
#------ Eval -------#

pst_pawn_white = [
  0, 0, 0, 0, 0, 0, 0, 0,
 50, 50, 50, 50, 50, 50, 50, 50,
 10, 10, 20, 30, 30, 20, 10, 10,
  5, 5, 10, 25, 25, 10, 5, 5,
  0, 0, 0, 20, 20, 0, 0, 0,
  5, -5, -10, 0, 0, -10, -5, 5,
  5, 10, 10,-20,-20, 10, 10, 5,
  0, 0, 0, 0, 0, 0, 0, 0
]

pst_pawn_black = [
  0, 0, 0, 0, 0, 0, 0, 0,
  -5, -10, -10,20,20, -10, -10, -5,
  -5, 5, 10, 0, 0, 10, 5, -5,
  0, 0, 0, -20, -20, 0, 0, 0,
  -5, -5, -10, -25, -25, -10, -5, -5,
 -10, -10, -20, -30, -30, -20, -10, -10,
 -50, -50, -50, -50, -50, -50, -50, -50,
  0, 0, 0, 0, 0, 0, 0, 0
]

pst_knight_white = [
  -50,-40,-30,-30,-30,-30,-40,-50,
 -40,-20, 0, 0, 0, 0,-20,-40,
 -30, 0, 10, 15, 15, 10, 0, -30,
 -30, 5, 15, 20, 20, 15, 5, -30,
 -30, 0, 15, 20, 20, 15, 0, -30,
 -30, 5, 10, 15, 15, 10, 5, -30,
 -40,-20, 0, 5, 5, 0,-20,-40,
 -50,-40,-30,-30,-30,-30,-40,-50
]

pst_knight_black = [
  50,40,30,30,30,30,40,50,
 40,20, 0, -5, -5, 0,20,40,
 -30, -5, -10, -15, -15, -10, -5, 30,
 30, 0, -15, -20, -20, -15, 0, 30,
 30, -5, -15, -20, -20, -15, -5, 30,
 30, 0, -10, -15, -15, -10, 0, 30,
 40,20, 0, 0, 0, 0,20,40,
 50,40,30,30,30,30,40,50
]

pst_bishop_white = [
  -20,-10,-10,-10,-10,-10,-10,-20,
 -10, 0, 0, 0, 0, 0, 0,-10,
 -10, 0, 5, 10, 10, 5, 0, -10,
 -10, 5, 5, 10, 10, 5, 5, -10,
 -10, 0, 10, 10, 10, 10, 0, -10,
 -10, 10, 10, 10, 10, 10, 10, -10,
 -10, 5, 0, 0, 0, 0, 5, -10,
 -20,-10,-10,-10,-10,-10,-10,-20,
]

pst_bishop_black = [
  20,10,10,10,10,10,10,20,
 10, -5, 0, 0, 0, 0, -5, 10,
 10, -10, -10, -10, -10, -10, -10, 10,
 10, 0, -10, -10, -10, -10, 0, 10,
 10, -5, -5, -10, -10, -5, -5, 10,
 10, 0, -5, -10, -10, -5, 0, 10,
 10, 0, 0, 0, 0, 0, 0,10,
 20,10,10,10,10,10,10,20,
]

pst_rook_white = [
  0, 0, 0, 0, 0, 0, 0, 0,
   5, 10, 10, 10, 10, 10, 10, 5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
   0, 0, 0, 5, 5, 0, 0, 0
]

pst_rook_black = [
  0, 0, 0, -5, -5, 0, 0, 0,
   5, 0, 0, 0, 0, 0, 0, 5,
  5, 0, 0, 0, 0, 0, 0, 5,
  5, 0, 0, 0, 0, 0, 0, 5,
  5, 0, 0, 0, 0, 0, 0, 5,
  5, 0, 0, 0, 0, 0, 0, 5,
  -5, -10, -10, -10, -10, -10, -10, -5,
   0, 0, 0, 0, 0, 0, 0, 0
]

pst_queen_white = [
 -20,-10,-10, -5, -5,-10,-10,-20,
 -10, 0, 0, 0, 0, 0, 0,-10,
 -10, 0, 5, 5, 5, 5, 0, -10,
  -5, 0, 5, 5, 5, 5, 0, -5,
   0, 0, 5, 5, 5, 5, 0, -5,
 -10, 5, 5, 5, 5, 5, 0, -10,
 -10, 0, 5, 0, 0, 0, 0, -10,
 -20,-10,-10, -5, -5,-10,-10,-20
]

pst_queen_black = [
 20,10,10, 5, 5,10,10,20,
 10, 0, -5, -0, -0, 0, -0,10,
 10, -5, -5, -5, -5, -5, -0, -10,
 0, -0, -5, -5, -5, -5, -0, 5,
 5, -0, -5, -5, -5, -5, -0, 5,
 10, -5, -5, -5, -5, -5, -0, 10,
 10, -0, -5, -0, -0, -0, -0, 10,
 20,10,10, 5, 5,10,10,20
]

pst_king_white = [
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -20,-30,-30,-40,-40,-30,-30,-20,
 -10,-20,-20,-20,-20,-20,-20,-10,
  20, 20, 0, 0, 0, 0, 20, 20,
  20, 30, 10, 0, 0, 10, 30, 20
]

pst_king_black = [
  -20,-30,-10,-0,-0,-10,-30,-20,
 -20,-20,-0,-0,-0,-0,-20,-20,
 10,20,20,20,20,20,20,10,
 20,30,30,40,40,30,30,20,
 30,40,40,50,50,40,40,30,
 30,40,40,50,50,40,40,30,
  30,40,40,50,50,40,40,30,
  30,40,40,50,50,40,40,30,
]


#[#Blanc K,Q,R,B,N,P, #Noire k,q,r,b,n,p]
#compte le nombre de pièces pour chacune
#première position du tableau est le nombre total de pièce
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
        if p.symbol() == 'Q':
            count_tab[0] += 1
            count_tab[2] += 1
        if p.symbol() == 'K':
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
        if p.symbol() == 'q':
            count_tab[0] += 1
            count_tab[8] += 1
        if p.symbol() == 'k':
            count_tab[0] += 1
            count_tab[7] += 1
    return count_tab

#fonction servant à donner un malus aux tour possédent des axes bloqué directement par une pièce allié
#non mis en oeuvre dans l'évaluation car le rajoue de condition similaire pour chaque pièce aurais pris trop de temps
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

#valeur de chaque pièces
valeurs = {'K':200, 
               'Q':9, 
               'R':5, 
               'B':3, 
               'N':3, 
               'P':1,
               '.':0}


#fonction renvoyant le score d'évaluation pour un état du plateau.
#Rajout d'un bonus en cas de pièces mangait ou malus si la pièce est dans son camps
#rajou d'un bonus de positionnement adapté à chaque pièce en fonction de sa couleur
#old_pieces contage des pièces présentent avant dernier coup tous juste jouer
def eval(board, player, old_pieces):
    score = 0
    pieces = count_pieces(board)
    if(pieces[0] < old_pieces[0]):
        ratio = 2
        for i in range(1,13,1):
            if(pieces[i] != old_pieces[i]):
                if(i%6 == 1):
                    score -= valeurs['K'] * ratio
                if(i%6 == 2):
                    score -= valeurs['Q'] * ratio
                if(i%6 == 3):
                    score -= valeurs['R'] * ratio
                if(i%6 == 4):
                    score -= valeurs['B'] * ratio
                if(i%6 == 5):
                    score -= valeurs['N'] * ratio
                if(i%6 == 0):
                    score -= valeurs['P'] * ratio
                if(i <= 6):
                    score = -score
                break
    for k,p in board.piece_map().items():
        if(p.symbol() == p.symbol().upper()):
            score += valeurs[p.symbol()]
            if p.symbol() == 'P':
                score += pst_pawn_white[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'N':
                score += pst_knight_white[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'B':
                score += pst_bishop_white[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'R':
                score += pst_rook_white[((7 - (k//8)) * 8) + (k%8)]
                #score -= psb_rook(board,k)
            if p.symbol() == 'K':
                score += pst_king_white[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'Q':
                score += pst_queen_white[((7 - (k//8)) * 8) + (k%8)]
        else:
            score -= valeurs[p.symbol().upper()]
            if p.symbol() == 'p':
                score += pst_pawn_black[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'n':
                score += pst_knight_black[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'b':
                score += pst_bishop_black[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'r':
                score += pst_rook_black[((7 - (k//8)) * 8) + (k%8)]
                #score += psb_rook(board,k)
            if p.symbol() == 'k':
                score += pst_king_black[((7 - (k//8)) * 8) + (k%8)]
            if p.symbol() == 'q':
                score += pst_queen_black[((7 - (k//8)) * 8) + (k%8)]
    return score


#------ Fin Eval -------#



#------ MinMax methode -------#

#old_pieces contage des pièces présentent avant dernier coup tous juste jouer
#p profondeur 
def MaxMin(b,p,player,old_pieces):
    if b.is_game_over():
        if(b.result() == "1-0"):
            return 100000
        elif(b.result() == "0-1"):
            return -100000
        return 0
    if p == 0:
        return eval(b,player,old_pieces)
    maxm = -1000000
    pieces = count_pieces(board)
    for m in b.generate_legal_moves():
        b.push(m)
        global noeuds
        noeuds += 1
        v = MinMax(b,p-1,not player,pieces)
        if(v > maxm):
            maxm = v
        b.pop()
    return maxm
        


#old_pieces contage des pièces présentent avant dernier coup tous juste jouer
#p profondeur  
def MinMax(b,p,player,old_pieces):
    if b.is_game_over():
        if(b.result() == "1-0"):
            return 100000
        elif(b.result() == "0-1"):
            return -100000
        return 0
    if p == 0:
        return eval(b,player,old_pieces)
    minm = 1000000
    pieces = count_pieces(board)
    for m in b.generate_legal_moves():
        b.push(m)
        global noeuds
        noeuds += 1
        v = MaxMin(b,p-1,not player,pieces)
        if(v < minm):
            minm = v
        b.pop()
    return minm


#Fonction servant d'initialisation à MinMax
#Elle permet de renvoyer un coup à partir des valeurs d'heuristique remonté par MaxMin et MinMax
#p profondeur 
def init(b,p,player):
    coup = randomMove(board)
    if p == 0:
        return coup
    global noeuds
    list_best_coup = []
    pieces = count_pieces(board)
    if(player):
        value = -10000000
        for m in b.generate_legal_moves():
            b.push(m)
            noeuds += 1
            v = MaxMin(b,p-1,player,pieces)
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
            v = MinMax(b,p-1,player,pieces)
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

#Simule un tournois entre 2 MinMax
#p_a profondeur minmax Blanc
#p_e profondeur minmax Noir
def playGame(b,p_a,p_e):
    #print("----------")
    #print(b)
    player = True
    while(1):
        if(player):
            b.push(init(b,p_a,player))
        else:
            b.push(init(b,p_e,player))
        if b.is_game_over():
            return b
        player = not player


#Simule un tournois entre 2 MinMax
#rounde est le nombre de partie
#p_a profondeur minmax Blanc
#p_e profondeur minmax Noir
def roundMatch(b,rounde,p_a,p_e):
    times = []
    score = [0,0]
    noeud = []
    global noeuds
    r = rounde
    player = True
    while(r >= 0):
        noeuds = 1
        b.reset()
        time_start = time.time()
        playGame(b,p_a,p_e)
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
    print("pourcentage de chance de victoire joueur Blanc : " + str(score[0] / (rounde + 1) *100))
    print("pourcentage de chance de victoire joueur Noir : " + str(score[1] / (rounde + 1) *100))





#------ Fin MinMax methode -------#




#------ AlphaBeta methode -------#


#a valeur alpha
#b valeur beta
#old_pieces contage des pièces présentent avant dernier coup tous juste jouer
#p profondeur  
def MaxValue(board, a, b, p, player,old_pieces):
    if board.is_game_over():
        if(board.result() == "1-0"):
            return 100000
        elif(board.result() == "0-1"):
            return -100000
        return 0
    if p == 0:
        return eval(board, player,old_pieces)
    pieces = count_pieces(board)
    for m in board.generate_legal_moves():
        board.push(m)
        global noeuds
        noeuds += 1
        a = max(MinValue(board, a, b, p-1,not player, pieces), a)
        if(a >= b):
            board.pop()
            return b
        board.pop()
    return a



#a valeur alpha
#b valeur beta
#old_pieces contage des pièces présentent avant dernier coup tous juste jouer
#p profondeur  
def MinValue(board, a, b, p, player,old_pieces):
    if board.is_game_over():
        if(board.result() == "1-0"):
            return 100000
        elif(board.result() == "0-1"):
            return -100000
        return 0
    if p == 0:
        return eval(board, player,old_pieces)
    pieces = count_pieces(board)
    for m in board.generate_legal_moves():
        board.push(m)
        global noeuds 
        noeuds += 1
        b = min(MaxValue(board, a, b, p-1, not player, pieces), b)
        if(a >= b):
            board.pop()
            return a
        board.pop()
    return b


#Fonction servant d'initialisation à AlphaBeta
#Elle permet de renvoyer un coup à partir des valeurs d'heuristique remonté par MaxValue et MinValue
#p profondeur 
def initValue(board, p, player):
    coup = randomMove(board)
    list_best_coup = []
    if p == 0:
        return coup
    if(player):
        value = -1000000
    else:
        value = 1000000
        pieces = count_pieces(board)
    for m in board.generate_legal_moves():
        board.push(m)
        global noeuds 
        noeuds += 1
        tmp = 0
        if(player):
            tmp = MinValue(board, -1000000, 1000000, p-1, not player, pieces)
            if(tmp >= value):
                list_best_coup = [m]
                value = tmp
                coup = m
            elif(v == value):
                list_best_coup.append(m)
        else:
            tmp = MaxValue(board, -1000000, 1000000, p-1, not player, pieces)
            if(tmp >= value):
                list_best_coup = [m]
                value = tmp
                coup = m
            elif(tmp == value):
                list_best_coup.append(m)
        board.pop()
    if(len(list_best_coup) > 1):
        return list_best_coup[random.randint(0, len(list_best_coup) - 1)]
    return coup

#Simule un match entre 2 AlphaBeta
#p_a profondeur alphabeta Blanc
#p_e profondeur alphabeta Noir
def playAB(b, p_a, p_e):
    #print("----------")
    #print(b)
    player = True
    while(1):
        if(player):
            b.push(initValue(b,p_a,player))
        else:
            b.push(initValue(b,p_e,player))
        if b.is_game_over():
            return 
        player = not player

#Simule un tournois entre 2 AlphaBeta
#rounde est le nombre de partie
#p_a profondeur alphabeta Blanc
#p_e profondeur alphabeta Noir
def makeRound(b,rounde,p_a,p_e):
    times = []
    score = [0,0]
    noeud = []
    global noeuds
    r = rounde
    while(r >= 0):
        noeuds = 1
        b.reset()
        time_start = time.time()
        playAB(b,p_a,p_e)
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
    print("pourcentage de chance de victoire joeur Blanc: " + str(score[0] / (rounde + 1) *100))
    print("pourcentage de chance de victoire joeur Noire: " + str(score[1] / (rounde + 1) *100))




#------ Fin AlphaBeta methode -------#



#------ MinMax vs AlphaBeta -------#

#Simule un match entre les 2 IA
#p_a profondeur minmax
#p_e profondeur alphabeta
def playDuel(b,p_a,p_e):
    player = True
    while(1):
        #print("----------")
        #print(b)
        if(player):
            b.push(init(b,p_a,player))
        else:
            b.push(initValue(b,p_e,player))
        if b.is_game_over():
            return b
        player = not player

#fonction simulant une certain nombre de partie entre MinMax(Blanc) et AlphaBeta(Noir)
#rounde est le nombre de partie
#p_a profondeur minmax
#p_e profondeur alphabeta
def duel(b,rounde,p_a,p_e):
    times = []
    score = [0,0]
    noeud = []
    global noeuds
    r = rounde
    while(r > 0):
        noeuds = 1
        b.reset()
        time_start = time.time()
        playDuel(b,p_a,p_e)
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
    print("pourcentage de chance de victoire : " + str(score[0] / rounde *100))


#------ Fin MinMax vs AlphaBeta -------#



#------ Simulation Joueur VS Machine -------#

#Les information afficher pour aider à jouer
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

#Affiche le jeux avec un curseur de selection de pieces et un curseur de selection de position pour le coup de la pieces
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


#Permet via une inteface textuel de selectionner l'IA contre qui jouer
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
        
#Permet via une inteface textuel de selectionner la profondeur de l'IA sélectionné
def select_p():
    running = True
    while(running):
        os.system('clear')
        print("Pour jouer aux échecs contre contre une IA, vous devez choissir quel doit être la profondeur pour l'algorithme choisit")
        tmp = input("Choisir un chiffre entre 1 et 4 :\n")
        if( int(tmp) >= 1 and int(tmp) <= 4):
            return int(tmp)

#Initialise les parametres necessaire à la jouabilité humain contre machine
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
    loop(board, f, p)

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


#Simule une partie d'échecs entre un joueur et une ia choisit
#Comprends aussi la possibilité de jouer
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

#------ Fin Simulation Joueur VS Machine -------#



#------ TEST -------#

board = chess.Board()

#------ Jeux aléatoire -------#

#deroulementRandom(board)

#------ Fin Jeux aléatoire -------#


#------ Recherche exhaustif -------#

#nb_noeuds = 1
#deroulementExhaustif(board,2)
#print(nb_noeuds)
#nb_noeuds = 1
#print("La profondeur la plus profonde qui met moins de 30s est : " + str(maxProfondeur(board)))

#------ Fin Recherche exhaustif -------#


#------ MinMax  -------#
#2eme parametre : nombre de partie
#3eme parametre : profondeur Blanc
#4eme parametre : profondeur Noir

#roundMatch(board,10,1,1)
#roundMatch(board,10,2,1)
#roundMatch(board,10,3,1)
#roundMatch(board,10,3,3)
#roundMatch(board,10,2,2)
#roundMatch(board,10,1,3)
#roundMatch(board,10,1,2)

#------ Fin MinMax  -------#


#------ AlphaBeta  -------#

#2eme parametre : nombre de partie
#3eme parametre : profondeur Blanc
#4eme parametre : profondeur Noir

#makeRound(board,10,1,1)
#makeRound(board,10,2,1)
#makeRound(board,10,3,1)
#makeRound(board,10,3,3)
#makeRound(board,10,2,2)
#makeRound(board,10,1,3)
#makeRound(board,10,1,2)

#------ Fin AlphaBeta  -------#


#------ MinMax Vs AlphaBeta  -------#

#duel(board,10,1,1)
#duel(board,10,2,1)
#duel(board,10,3,1)
#duel(board,10,3,3)
#duel(board,10,2,2)
duel(board,10,1,3)
#duel(board,10,1,2)

#------ Fin MinMax Vs AlphaBeta  -------#


#------ Joueur Vs IA -------#

#init_game(board)

#------ Fin Joueur Vs IA -------#


#------ Fin Main -------#