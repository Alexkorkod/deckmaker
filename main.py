#!/usr/bin/python
import math, json
import matplotlib.pyplot as plt
import sys
with open('bd.json', 'r') as f:
    read_data = f.read()
ar = json.loads(read_data)
f1 = open('values.txt', 'w')
value = {}
counter = 0
for card in ar:
    ka = 1
    kh = 1.2
    if card['attack'] != '' and card['mana_cost'] != '' and card['mana_cost'] != '0' and card['mana_cost'] != '1':
        data = {'m':int(card['mana_cost']),'a':int(card['attack']),'h':int(card['health']),'summab':0}
        if data['h'] < data['m']:
            kh = kh - 0.2
        if data['h'] == 2:
            kh = kh - 0.5
        if data['h'] == 1:
            kh = kh - 1
        if data['a'] <= math.ceil(data['m']/2.0):
            ka = ka - 0.2
        if card['description'] != '':
            data['summab'] = 1
        tmp = ((data['a']*ka+data['h']*kh)/data['m'])+data['summab']
        if counter < 40:
            tmp2 = {'value':tmp,'mana_cost':data['m']}
            value[card['label']] = tmp2
            counter = counter + 1
        else:
            min_value = 100
            min_label = ''
            for (key, item) in value.items():
                if item['value'] < min_value:
                    min_value = item['value']
                    min_label = key
            if tmp > min_value:
                value.pop(min_label)
                tmp2 = {'value':tmp,'mana_cost':data['m']}
                value[card['label']] = tmp2
        f1.write(card['label'] + ':' +str(tmp)+"\n")
json.dump(value,open('list.json','w'),indent=4)
manacurve = {}
for (key, item) in value.items():
    if item['mana_cost'] not in manacurve:
        manacurve[item['mana_cost']] = 0
    manacurve[item['mana_cost']] += 1
    
def out(manacurve):
    for (key, units) in manacurve.items():
        i = 0
        sys.stdout.write(str(key)+':')
        while i < units:
            sys.stdout.write('/')
            i += 1
        sys.stdout.write(str(units)+'\n')
    
out(manacurve)

def throughmanacurve(manacurve, lefover):
    maxm = 0
    for m in manacurve:
        if manacurve[m] > 0: 
            if m <= lefover and m > maxm:
                maxm = m
        else:
            continue
    if maxm in manacurve:
        manacurve[maxm] -= 1
        lefover = lefover - maxm 
        if lefover < min(manacurve.keys()):
            return manacurve
        else:
            return throughmanacurve(manacurve,lefover)
    else:
        return manacurve
            
def simulate(manacurve):
    manaperturn = [2,3,4,5,6,7,8,9,9,9,9,9]
    for mana in manaperturn:
        if mana in manacurve and manacurve[mana] != 0:
            manacurve[mana] -= 1
        else:
            manacurve = throughmanacurve(manacurve,mana)
        print(manacurve)
    return manacurve
    
out(simulate(manacurve))

