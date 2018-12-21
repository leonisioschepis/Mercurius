import matplotlib.pyplot as plt
import numpy as np
from math import log,ceil,floor,e
from random import randint
from statistics import median
from time import time
import editdistance as ed
start_time = time()
MINIMUM_BLOCK_SIZE = 8

'''with open("ossimetria/nonin-memory-playback.nmp (1)", "rb") as f:
        old = f.read()

with open("ossimetria/nonin-memory-playback.nmp (2)", "rb") as f:
        new = f.read()'''

def find_diffs(old, new):
    old_size = len(old)
    new_size = len(new)
    #################################################
    #################################################
    ################# Computing EST #################
    #################################################
    #################################################
    ED = ed.eval(old,new)
    val = ED - abs(new_size - old_size)
    check = 1
    if val > 1:
        check = log(val,2)**2
    EST = max((ceil(val/check), MINIMUM_BLOCK_SIZE))
    #################################################
    #################################################
    ############## Finding differences ##############
    #################################################
    #################################################
    to_send = []
    old_sign = [old[i:i+EST] for i in range(0,len(old),EST)]
    i = 0
    last_match = 0
    while True:
        block = new[i:i+EST]
        if block in old_sign:
            if not i == last_match:
                to_send.append(new[last_match:i])
            last_match = i+EST
            indice = old_sign.index(block)
            #la funzione index ritorna la prima occorrenza del blocco, ma se ho più
            #occorrenze magari vado a spezzare un intervallo inutilmente. Il controllo
            #sottostante serve ad evitare questo: in pratica controlla se il blocco
            #successivo all'ultimo match trovato (solo se è un potenziale intervallo
            #quindi un intero) sia uguale al blocco e in quel caso salva l'indice
            #successivo al precedente in modo da non spezzare inutilmente l'intervallo
            if len(to_send) > 1 and type(to_send[-1]) is int:
                if old_sign[to_send[-1] + 1] == block:
                    to_send.append(to_send[-1] + 1)
                else:
                    to_send.append(indice)
            else:
                to_send.append(indice)
            i += EST
        else:
            i += 1
        if i > new_size:
            if len(new[last_match:]) > 0:
                to_send.append(new[last_match:])
            #if not i == last_match:
            #    to_send.append(new[last_match:])
            break
    #################################################
    #################################################
    ############## Shrinking intervals ##############
    #################################################
    #################################################
    filtered = []
    for entry in to_send:
        if len(filtered) == 0:
            filtered.append(entry)
        elif type(filtered[-1]) is bytes:
            filtered.append(entry)
        elif type(filtered[-1]) is int:
            if type(entry) is int:
                if filtered[-1] + 1 == entry:
                    filtered[-1] = (filtered[-1], entry)
                else:
                    filtered.append(entry)
            else:
                filtered.append(entry)
        else:
            if type(entry) is bytes:
                filtered.append(entry)
            else:
                if filtered[-1][1] + 1 == entry:
                    filtered[-1] = (filtered[-1][0], entry)
                else:
                    filtered.append(entry)
    cost = 0
    for entry in filtered:
        if type(entry) is bytes:
            cost += len(entry)
        if type(entry) is int:
            cost += 1
        if type(entry) is tuple:
            cost += 2
    #print("The cost is",cost,"bytes over an edit distance of", ED)
    #print("Time elapsed:", time() - start_time)
    return EST,cost, filtered
'''block_size,cost,diffs = find_diffs(old,new)
print("Block_size:", block_size)
print("Cost:", cost)
print("Diffs:", diffs)'''
