#!/usr/bin/python
import math, json, sys

def out(manacurve):
    j = 0
    while j < 10:
        i = 0
        text_file.write(str(j)+':')
        if str(j) in manacurve.keys():
            units = manacurve[str(j)]
            while i < units:
                text_file.write('/')
                i += 1
            text_file.write(str(units)+'\n')
        else:
            text_file.write('0\n')
        j += 1

oc = 0 
text_file = open("Output.txt", "w")
while oc < 1:
    with open('best_deck.json', 'r') as f:
        read_data = f.read()
    ar = json.loads(read_data)
    for manacurve in ar:
        spell_count = 0
        minion_count = 0
        artefact_count = 0
        curve = {}
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
            if item['mana_cost'] not in curve:
                curve[item['mana_cost']] = 0
            curve[item['mana_cost']] += 1
        text_file.write('Average hand size: '+ str(avg_hand_size)+'\n')
        text_file.write('Average lost mana per game (coeff-ed): '+ str(mana_lost)+'\n')
        text_file.write('Minions : '+str(minion_count)+', Spells : '+str(spell_count)+', Artefacts : '+str(artefact_count)+'\n')
        text_file.write('Manacurve : '+str(mc)+'\n')
        out(curve)
        text_file.write('\n')
    oc += 1
text_file.close()