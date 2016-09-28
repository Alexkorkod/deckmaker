#!/usr/bin/python
import math, json, operator
import sys
import random
import time
sys.setrecursionlimit(10)
with open('bd.json', 'r') as f:
    read_data = f.read()
ar = json.loads(read_data)

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

def checkFieldForCards():
    global field
    if len(field) > 0:
        return True
    else:
        return False

def checkForTurn(hand,mana):
    turnexists = False
    for card in hand:
        if int(card['mana_cost']) <= mana:
            if card['type'] == 'Spell':
                if card['target'] == 'FRIENDLY' or card['target'] == 'ENEMY' or card['target'] == 'ANY':
                    turnexists = checkFieldForCards()
                else:
                    turnexists = True
                if turnexists:
                    break
            else:
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

def fishForMostExpensivePlay(hand,mana):
    max_index = 0
    max_cost = 0
    for (i,card) in enumerate(hand):
        if int(card['mana_cost']) <= mana and int(card['mana_cost']) >= max_cost:
            playable = True
            if card['type'] == 'Spell':
                if card['target'] == 'FRIENDLY' or card['target'] == 'ENEMY' or card['target'] == 'ANY':
                    playable = checkFieldForCards()
            if playable:
                max_cost = int(card['mana_cost'])
                max_index = i
    return max_index

def makeCollectionOfPlayables(hand,mana,playables):
    for (i,card) in enumerate(hand):
        if int(card['mana_cost']) <= mana:
            playable = True
            if card['type'] == 'Spell':
                if card['target'] == 'FRIENDLY' or card['target'] == 'ENEMY' or card['target'] == 'ANY':
                    playable = checkFieldForCards()
            if playable:
                playables.append(card)
    return playables

def choseCardForTurn(hand,mana):
    playables = []
    playables = makeCollectionOfPlayables(hand,mana,playables)
    playables = sorted(playables,key=operator.itemgetter('mana_cost'))
    sum_mana = 0
    card = {}
    cards_to_play = []
    while sum_mana < mana:
        if len(playables) > 0:
            top_card = playables.pop()
            if int(top_card['mana_cost']) == mana:
                card = top_card
            else:
                playables.append(top_card)
                card = playables.pop(0)
            sum_mana += int(card['mana_cost'])
            cards_to_play.append(card)
        else:
            break
    if sum_mana > mana:
        for card in cards_to_play:
            if sum_mana - int(card['mana_cost']) <= mana:
                odd_card = cards_to_play.pop(0)
                sum_mana -= int(odd_card['mana_cost'])
                break
    return cards_to_play
    
def findLeastExpensiveCardCost(hand):
    min_cost = 100
    for card in hand:
        if int(card['mana_cost']) < min_cost:
            playable = True
            if card['type'] == 'Spell':
                if card['target'] == 'FRIENDLY' or card['target'] == 'ENEMY' or card['target'] == 'ANY':
                    playable = checkFieldForCards()
            if playable:
                min_cost = int(card['mana_cost'])
    return min_cost

def makeTurn(deck,hand,mana,replace_count):
    global sum_lost_mana, cur_mana, field
    cards_to_play = choseCardForTurn(hand,mana)
    mana_left = mana
    if len(cards_to_play) > 0 :
        for played_card in cards_to_play:
            for (i,card) in enumerate(hand):
                if card == played_card:
                    hand.pop(i)
            field.append(played_card)
            mana_left = mana - int(played_card['mana_cost'])
    elif replace_count < 1:
        hand = replace(deck,hand)
        replace_count += 1
        makeTurn(deck,hand,mana_left,replace_count)
    sum_lost_mana += mana_left*(9-cur_mana)
    return hand
        
def endTurn(deck,hand):
    global sum_hand_size
    index = random.randint(0,len(deck)-1)
    card = deck.pop(index)
    if len(hand) < 6:
        hand.append(card)
    sum_hand_size += len(hand)
    return hand



c_limit = 1000
cc_limit = 1000
backup_ar = list(ar)
manacurves = [[2,3,4,5,6],[2,3,4,5,6,7,8,9],[2,3,4,5,6,7,8,9,9],[2,3,4,5,6,7,8,9,9,9,9]]
co = 0
for manacurve in manacurves:
    c = 0
    lost_mana = float('inf')
    hand_size = 0
    best_deck = []
    deck_info = []
    while c < c_limit:
        random.seed()
        i = 0
        backup_deck = []
        deck = []
        factions = ['Abyssian','Lyonar','Songhai','Vetruvian','Magmar','Vanar']
        faction = factions[random.randint(0,len(factions)-1)]
        ar = list(backup_ar)
        while i < 39:
            index = random.randint(0,len(ar)-1)
            card = ar.pop(index)
            if card['mana_cost'] != '' and card['faction'] == faction:
                k = 0
                limitk = random.randint(2,3)
                while k < limitk:
                    deck.append(card)
                    i += 1
                    k += 1
                    if i == 39:
                        break
    
        backup_deck = list(deck)
    
        cc = 0
        hand = []
        field = []
        sum_lost_mana = 0
        sum_hand_size = 0
        while cc < 1000:
            deck = list(backup_deck)
            simulateFirstDraw(deck,hand)
            mullForFirstTurn(deck,hand,2,0)
            for mana in manacurve:
                #outputHand(hand)
                cur_mana = mana
                makeTurn(deck,hand,mana,0)
                endTurn(deck,hand)
            cc += 1
            hand = []
            field = []
        c += 1
        sys.stdout.write(str((c*c_limit+co*1000000)/float(4*c_limit*cc_limit/100)) + '% done\r')
        sys.stdout.flush()
        if sum_lost_mana < lost_mana and sum_hand_size > hand_size:
            lost_mana = sum_lost_mana
            hand_size = sum_hand_size
            best_deck = list(backup_deck)
        best_deck.append({'avg_hand_size':hand_size/(11*1000.0)})
        best_deck.append({'lost_mana':lost_mana/1000.0})
        best_deck.append({'manacurve':manacurve})
    deck_info.append(best_deck)
    co += 1
json.dump(deck_info,open('best_deck.json','w'),indent=4)