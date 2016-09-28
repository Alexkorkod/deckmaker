#!/usr/bin/python
import math, json, sys

def out(manacurve):
    j = 0
    while j < 10:
        i = 0
        sys.stdout.write(str(j)+':')
        if str(j) in manacurve.keys():
            units = manacurve[str(j)]
            while i < units:
                sys.stdout.write('/')
                i += 1
            sys.stdout.write(str(units)+'\n')
        else:
            sys.stdout.write('0\n')
        j += 1

oc = 0        
while oc < 1:
    with open('best_deck.json', 'r') as f:
        read_data = f.read()
    ar = json.loads(read_data)
    spell_count = 0
    minion_count = 0
    artefact_count = 0
    curve = {}
    minioncurve = {}
    for manacurve in ar:
        mc = manacurve.pop()['manacurve']
        mana_lost = manacurve.pop()['lost_mana']
        avg_hand_size = manacurve.pop()['avg_hand_size']
        for item in manacurve:
            if item['type'] == 'Spell':
                spell_count += 1
            elif item['type'] == 'Artefact':
                artefact_count += 1
            else:
                minion_count += 1
            if item['mana_cost'] not in manacurve:
                curve[item['mana_cost']] = 0
            curve[item['mana_cost']] += 1
        sys.stdout.write('Average hand size: '+ str(avg_hand_size)+'\n')
        sys.stdout.write('Average lost mana per game (coeff-ed): '+ str(mana_lost)+'\n')
        sys.stdout.write('Minions : '+str(minion_count)+' Spells : '+str(spell_count)+' Artefacts : '+str(artefact_count)+'\n')
        sys.stdout.write('Manacurve : '+str(mc))
        out(curve)
    oc += 1