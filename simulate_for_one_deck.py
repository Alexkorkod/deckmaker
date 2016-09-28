#!/usr/bin/python
import math, json
import matplotlib.pyplot as plt
import sys
import random
import time

def outputHand(hand):
        sys.stdout.write('HAND: ')
        for card in hand:
            sys.stdout.write(card['label']+', ')
        sys.stdout.write('\n')
      
def findMostExpensiveCardInHand(hand):
    meindex = 0
    max_cost = 0
    for (i,card) in enumerate(hand):
        if card['mana_cost'] > max_cost:
            meindex = i
            max_cost = card['mana_cost']
    return meindex
    
def checkForTurn(hand,mana):
    turnexists = False
    for card in hand:
        if int(card['mana_cost']) <= mana and (card['type'] != 'Spell' or card['type'] != 'Artifact'):
            turnexists = True
            break
    return turnexists
    
def replace(deck,hand):
    tmp = hand.pop(findMostExpensiveCardInHand(hand))
    index = random.randint(0,len(deck)-1)
    card = deck.pop(index)
    hand.append(card)
    deck.append(tmp)
    return hand
        
def mullForFirstTurn(deck,hand,mana,replace_count):
    turnexists = checkForTurn(hand,mana)
    if not turnexists and replace_count < 2:
        hand = replace(deck,hand)
        replace_count += 1
        mullForFirstTurn(deck,hand,mana,replace_count)
    else:
        return hand
            
def simulateFirstDraw(deck, hand):
    j = 0
    while j < 5:
        index = random.randint(0,len(deck)-1)
        card = deck.pop(index)
        hand.append(card)
        j += 1
    return hand
    
def choseCardForTurn(hand,mana):
    index = 0
    max_cost = 0
    for (i,card) in enumerate(hand):
        if int(card['mana_cost']) <= mana and int(card['mana_cost']) >= max_cost:
            max_cost = int(card['mana_cost'])
            index = i
    return index
    
def findLeastExpensiveCardCost(hand):
    min_cost = 100
    for card in hand:
        if int(card['mana_cost']) < min_cost:
            min_cost = int(card['mana_cost'])
    return min_cost

def makeTurn(deck,hand,mana,replace_count):
    global sum_lost_mana
    turnexists = checkForTurn(hand,mana)
    mana_left = mana
    if turnexists :
        played_card = hand.pop(choseCardForTurn(hand,mana))
        mana_left = mana - int(played_card['mana_cost'])
        sys.stdout.write(played_card['label'] +
        ' was played at ' + str(mana) + ' mana, mana left: ' +
        str(mana_left)+'\n')
    elif replace_count < 1:
        hand = replace(deck,hand)
        replace_count += 1
        makeTurn(deck,hand,mana,replace_count)
    if mana_left >= findLeastExpensiveCardCost(hand) and len(hand) > 0:
        makeTurn(deck,hand,mana_left,replace_count)
    else:
        sum_lost_mana += mana_left
    return hand
        
def endTurn(deck,hand):
    index = random.randint(0,len(deck)-1)
    card = deck.pop(index)
    if len(hand) < 6:
        hand.append(card)
    return hand

hand = []
deck = json.load(open('best_deck0.json','r'))
simulateFirstDraw(deck,hand)
mullForFirstTurn(deck,hand,2,0)
manacurve = [2,3,4,5,6,7,8,9,9,9,9]
sum_lost_mana = 0 #stud
for mana in manacurve:
    outputHand(hand)
    makeTurn(deck,hand,mana,0)
    endTurn(deck,hand)