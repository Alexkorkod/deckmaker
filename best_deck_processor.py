#!/usr/bin/python
import math, json, sys

def out(manacurve):
    j = 0
    while j < 10:
        i = 0
        text_file.write(str(j)+':')
        if str(j) in manacurve.keys():
            units = manacurve[str(j)]['manacost']
            while i < units:
                text_file.write('/')
                i += 1
            text_file.write(str(units)+'\n')
        else:
            text_file.write('0\n')
        j += 1

def out_stats(manacurve):
    j = 0
    while j < 10:
        i = 0     
        if str(j) in manacurve.keys():
            text_file.write(str(j)+' mana: ')
            units = manacurve[str(j)]['manacost']
            avg_att = manacurve[str(j)]['attack']/float(units)
            avg_hp = manacurve[str(j)]['health']/float(units)
            avg_stats = (avg_att + avg_hp)/float(j)
            text_file.write('average attack: '+str(avg_att)+', average health: '+str(avg_hp)+', avg stats per mana point: '+str(avg_stats)+'\n')
        j += 1

text_file = open("Output.txt", "a")
with open('best_deck.json', 'r') as f:
    read_data = f.read()
ar = json.loads(read_data)
for manacurve in ar:
    spell_count = 0
    minion_count = 0
    artefact_count = 0
    curve = {}
    mana_lost = manacurve.pop()['lost_mana']
    avg_hand_size = manacurve.pop()['avg_hand_size']
    turns = manacurve.pop()['turns']
    avg_stats_per_mana = manacurve.pop()['stats_per_mana']
    for item in manacurve:
        if item['mana_cost'] not in curve:
            curve[item['mana_cost']] = {}
            curve[item['mana_cost']]['manacost'] = 0
            curve[item['mana_cost']]['attack'] = 0
            curve[item['mana_cost']]['health'] = 0
        curve[item['mana_cost']]['manacost'] += 1
        if item['type'] == 'Spell':
            spell_count += 1
        elif item['type'] == 'Artifact':
            artefact_count += 1
        else:
            curve[item['mana_cost']]['attack'] += int(item['attack'])
            curve[item['mana_cost']]['health'] += int(item['health'])
            minion_count += 1
    text_file.write('Average number of stat points per mana: '+ str(avg_stats_per_mana)+'\n')
    text_file.write('Average number of turns made: '+ str(turns)+'\n')
    text_file.write('Average hand size: '+ str(avg_hand_size)+'\n')
    text_file.write('Average lost mana per game (coeff-ed): '+ str(mana_lost)+'\n')
    text_file.write('Minions : '+str(minion_count)+', Spells : '+str(spell_count)+', Artifacts : '+str(artefact_count)+'\n')
    out(curve)
    #out_stats(curve)
    text_file.write('\n')
text_file.close()