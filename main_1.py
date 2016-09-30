#!/usr/bin/python
import math, json, operator
import sys
import random
import time
sys.setrecursionlimit(10)
with open('bd.json', 'r') as f:
    read_data = f.read()
ar = json.loads(read_data)
      
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
    global sum_lost_mana, cur_mana, field, enemy_gen, game_stats_per_mana,played_cards,side
    cards_to_play = choseCardForTurn(hand,mana)
    mana_left = mana
    if len(cards_to_play) > 0 :
        for played_card in cards_to_play:
            for (i,card) in enumerate(hand):
                if card == played_card:
                    card_from_hand = hand.pop(i)
                    if card_from_hand['type'] != 'Spell' and card_from_hand['type'] != 'Artifact':
                        if card_from_hand['mana_cost'] == '0':
                            card_from_hand['mana_cost'] = '1'
                        game_stats_per_mana += (int(card_from_hand['attack'])+int(card_from_hand['health']))/float(card_from_hand['mana_cost'])
                        played_cards += 1
                        adj = getAdjForPlacement(side)
                        index = random.randint(0,len(adj)-1)
                        chosen_place = adj[index]
                        for tile in field:
                            if tile == chosen_place:
                                card_from_hand['side'] = side
                                tile['card'] = card_from_hand
                                break
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

def generateField():    
    global field
    i = 1
    while i <= 9:
        j = 1
        while j <= 5:
            pos = {'i':i,'j':j}
            card = {}
            field.append({'pos':pos,'card':card})
            j += 1
        i += 1

def initialPlacement():
    global field, general
    fp_gen_pos = {'i':1,'j':3}
    sp_gen_pos = {'i':9,'j':3}
    for tile in field:
        if tile['pos'] == fp_gen_pos:
            tile['card'] = general
        if tile['pos'] == sp_gen_pos:
            tile['card'] = enemy_general

def getAdjForMove(card):
    global field
    adj = []
    for tile in field:
        if tile['card'] == card:
            cur_adj = getAdj(tile)
            for place in cur_adj:
                adj.append(place)
    return adj

def getAdjForPlacement(side):
    global field
    adj = []
    for tile in field:
        if tile['card'] != {} and tile['card']['side'] == side:
            cur_adj = getAdj(tile)
            for place in cur_adj:
                adj.append(place)  
    return adj

def getAdj(cur_tile):
    global field
    adj = []
    cur_pos = cur_tile['pos']
    i = cur_pos['i'] 
    j = cur_pos['j']
    range_i = range(i-1,i+2)
    range_j = range(j-1,j+2)
    for tile in field:
        if tile['pos']['i'] in range_i and tile['pos']['j'] in range_j:
            adj.append(tile)
    tile = []
    adj = dict((i,el) for i,el in enumerate(adj))
    tiles_with_cards = []
    for i,tile in adj.items():
        if tile['card']:
            tiles_with_cards.append(i)
    for i in tiles_with_cards:
        adj.pop(i)
    adj = adj.values()
    return adj

def firstIterationTrade():
    #TODO trade with nearest THEN TODO trade with adj
    global field, side, other_side
    for tile in field:
        if tile['card'] != {} and tile['card']['side'] == side:
            for deep_tile in field:
                if deep_tile['card'] != {} and deep_tile['card']['side'] == other_side:
                    tile['card']['health'] = int(tile['card']['health']) - int(deep_tile['card']['attack'])
                    deep_tile['card']['health'] = int(deep_tile['card']['health']) - int(tile['card']['attack'])
                    if int(tile['card']['health']) <= 0:
                        tile['card'] = {}
                    if int(deep_tile['card']['health']) <= 0:
                        deep_tile['card'] = {}
                    break
            break

def showField():
    #TODO make this shit beatyfull
    global field
    local_field = {'row1':{},'row2':{},'row3':{},'row4':{},'row5':{}}
    for tile in field:
        if tile['pos']['j'] == 1:
            if tile['card'] != {}:
                local_field['row1'][tile['pos']['i']] = '|%2s:%2s|' % (tile['card']['attack'],tile['card']['health'])
            else:
                local_field['row1'][tile['pos']['i']] = '|  :  |'
        elif tile['pos']['j'] == 2:
            if tile['card'] != {}:
                local_field['row2'][tile['pos']['i']] = '|%2s:%2s|' % (tile['card']['attack'],tile['card']['health'])
            else:
                local_field['row2'][tile['pos']['i']] = '|  :  |'
        elif tile['pos']['j'] == 3:
            if tile['card'] != {}:
                local_field['row3'][tile['pos']['i']] = '|%2s:%2s|' % (tile['card']['attack'],tile['card']['health'])
            else:
                local_field['row3'][tile['pos']['i']] = '|  :  |'
        elif tile['pos']['j'] == 4:
            if tile['card'] != {}:
                local_field['row4'][tile['pos']['i']] = '|%2s:%2s|' % (tile['card']['attack'],tile['card']['health'])         
            else:
                local_field['row4'][tile['pos']['i']] = '|  :  |'
        elif tile['pos']['j'] == 5:
            if tile['card'] != {}:
                local_field['row5'][tile['pos']['i']] = '|%2s:%2s|' % (tile['card']['attack'],tile['card']['health'])
            else:
                local_field['row5'][tile['pos']['i']] = '|  :  |'
    for key, row in local_field.items():
        l = row.keys()
        l = list(l)
        l.sort()
        for i in l:
            sys.stdout.write(row[i])
        sys.stdout.write('\n')
    sys.stdout.write('---------------------------------\n')

def placeCard(card):
    global field
    
def moveGeneral(side):
    if side == 'first':
        cur_gen = general
    else:
        cur_gen = enemy_general
    adj = getAdjForMove(cur_gen)
    if len(adj) > 0:
        index = random.randint(0,len(adj)-1)
        chosen_place = adj[index]
        for tile in field:
            if tile == chosen_place:
                tile['card'] = cur_gen
            elif tile['card'] != {} and tile['card']['type'] == 'GENERAL' and tile['card']['side'] == side:
                tile['card'] = {}   

c_limit = 1000
cc_limit = 1000
show_field = False
if len(sys.argv) > 1:
    c_limit = int(sys.argv[1])
if len(sys.argv) > 2:
    cc_limit = int(sys.argv[2])
if len(sys.argv) > 3:
    show_field = True
backup_ar = list(ar)
deck_info = []
c = 0
lost_mana = float('inf')
hand_size = 0
best_deck = []
made_turns = 0
stats_per_mana = 0
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
                card['side'] = 'first'
                deck.append(card.copy())
                i += 1
                k += 1
                if i == 39:
                    break

    backup_deck = list(deck)

    cc = 0
    sum_lost_mana = 0
    sum_hand_size = 0
    sum_stats_per_mana = 0
    hand = []
    field = []
    turns = 0
    while cc < cc_limit:
        side = 'first'
        other_side = 'second'
    	enemy_general = {'attack':2,'health':25,'type':'GENERAL','side':other_side}
        for card in backup_deck:
            deck.append(card.copy())
        if deck == backup_deck:
            for card in deck:
                sys.stdout.write(str(card['label'])+':'+str(card['health']))
                sys.stdout.write('\n')
            sys.stdout.write('-----------------------\n')
        simulateFirstDraw(deck,hand)
        mullForFirstTurn(deck,hand,2,0)
        general = {'attack':2,'health':25,'type':'GENERAL','side':side}
        generateField()
        initialPlacement()
        played_cards = 0
        game_stats_per_mana = 0
        mana = 2
        while enemy_general['health'] > 0: 
            turns += 1
            cur_mana = mana
            moveGeneral(side)
            makeTurn(deck,hand,mana,0)
            moveGeneral(other_side)
            firstIterationTrade()
            endTurn(deck,hand)
            if mana < 9:
            	mana += 1
            if show_field:
                showField()
        if played_cards > 0:
            sum_stats_per_mana += game_stats_per_mana/float(played_cards)
        cc += 1
        hand = []
        field = []
    c += 1
    if len(sys.argv) <= 2:
        sys.stdout.write('%(progress)2.2f%% done\r' % {'progress': (c*c_limit)/float(c_limit*c_limit/100)})
        sys.stdout.flush()
        if sum_lost_mana < lost_mana and sum_hand_size > hand_size and sum_stats_per_mana > stats_per_mana:
            stats_per_mana = sum_stats_per_mana
            lost_mana = sum_lost_mana
            hand_size = sum_hand_size
            best_deck = list(backup_deck)
            made_turns = turns/float(cc_limit)
if len(sys.argv) <= 2:
    best_deck.append({'stats_per_mana':stats_per_mana/cc_limit})
    best_deck.append({'turns':made_turns})
    best_deck.append({'avg_hand_size':hand_size/(made_turns*cc_limit)})
    best_deck.append({'lost_mana':lost_mana/cc_limit})
    deck_info.append(best_deck)
    json.dump(deck_info,open('best_deck.json','w'),indent=4)
