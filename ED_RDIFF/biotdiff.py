import editdistance as ed
import matplotlib.pyplot as plt
import numpy as np
from math import log,ceil,floor,e
from random import randint
from statistics import median
from time import time

start_time = time()
MINIMUM_BLOCK_SIZE = 8
'''
def random_way(backup, data,n = 10, g = 4):
    size = log(len(backup), 2)
    size = ceil(size) if size >= ceil(size) - 0.5 else floor(size)
    original_splitted = [backup[i:i+size] for i in range(0, len(backup),size)]
    results = []
    for _ in range(0, g):
        band = []
        for _ in range(0, n):
            index = randint(0, len(backup)-size)
            random_block = data[index:index+size]
            if not random_block in original_splitted:
                a = []
                for block in original_splitted:
                    score = ed.eval(block, random_block)
                    if score < size:
                        a.append(score)
                band.append(min(a))
        results.append(sum(band)/n)
    EST = median(results)
    return ceil(EST) if EST >= ceil(EST) - 0.5 else floor(EST)

def deterministic_way(present, previous):
    edit_distance = ed.eval(previous,present) - abs(len(present)-len(previous))
    block_size = round(log(len(present),2)) + 1
    prec = []
    candidate = -1
    candidate_score = 30000
    #if edit_distance < MINIMUM_BLOCK_SIZE:
    #    return MINIMUM_BLOCK_SIZE
    for i in range(block_size - MINIMUM_BLOCK_SIZE):
        block_size -= 1
        #Phase 1
        present_blocks = [present[i:i+block_size] for i in range(0, len(present),block_size)]
        previous_window = [previous[i:i+block_size] for i in range(0, len(previous))]
        count = 0
        for entry in previous_window:
            if count == 0:
                if entry in present_blocks:
                    present_blocks.remove(entry)
                    count = block_size - 1
            else:
                count -= 1
        #Phase 2
        present_window = [present[i:i+block_size] for i in range(0, len(present))]
        previous_blocks = [previous[i:i+block_size] for i in range(0, len(previous),block_size)]
        count = 0
        for entry in present_window:
            if count == 0:
                if entry in previous_blocks:
                    previous_blocks.remove(entry)
                    count = block_size - 1
            else:
                count-=1
        p1 = len(previous_blocks)
        p2 = len(present_blocks)
        faulted_blocks = min(p1,p2)
        score = faulted_blocks - edit_distance/block_size
        if score >= 0 and score <= candidate_score:
            candidate = block_size
            candidate_score = score
        prec.append(score)
    plt.plot(prec, label = "Leonisio Coefficient")
    plt.legend(loc="best")
    block_size = round(log(len(present),2))
    plt.xticks(np.arange(len(prec)), [round(log(len(present),2)) - i for i in range(block_size)])
    plt.show()
    plt.clf()
    print("The candidate is:", candidate)
    return candidate
'''
#################################################
#################################################
################# Loading input #################
#################################################
#################################################


def find_diffs(backup, data):
    data_size = len(data)
    backup_size = len(backup)
    ED = ed.eval(backup, data)
    #print("Original size:", data_size)
    #print("The edit distance between the two docs is",ED)
    #print("and therefore the portion of modified document is", ED/data_size)
    # Rounds the log value to the nearest integer

    #################################################
    #################################################
    ################# Computing EST #################
    #################################################
    #################################################
    val = ED - abs(data_size - backup_size)
    check = log(val,2) if val > 0 else 1
    EST = max((ceil(val/check), MINIMUM_BLOCK_SIZE))
    #print("Block size estimation:", EST)
    to_send = []
    #################################################
    #################################################
    ############## Finding differences ##############
    #################################################
    #################################################
    backup_sign = [backup[i:i+EST] for i in range(0,len(backup),EST)]
    i = 0
    last_match = 0
    while True:
        block = data[i:i+EST]
        if block in backup_sign:
            if not i == last_match:
                to_send.append(data[last_match:i])
            last_match = i+EST
            indice = backup_sign.index(block)
            #la funzione index ritorna la prima occorrenza del blocco, ma se ho più
            #occorrenze magari vado a spezzare un intervallo inutilmente. Il controllo
            #sottostante serve ad evitare questo: in pratica controlla se il blocco
            #successivo all'ultimo match trovato (solo se è un potenziale intervallo
            #quindi un intero) sia uguale al blocco e in quel caso salva l'indice
            #successivo al precedente in modo da non spezzare inutilmente l'intervallo
            if len(to_send) > 1 and type(to_send[-1]) is int:
                if backup_sign[to_send[-1] + 1] == block:
                    to_send.append(to_send[-1] + 1)
                else:
                    to_send.append(indice)
            else:
                to_send.append(indice)
            i += EST
        else:
            i += 1
        if i > data_size:
            if len(data[last_match:]) > 0:
                to_send.append(data[last_match:])
            #if not i == last_match:
            #    to_send.append(data[last_match:])
            break
    #################################################
    #################################################
    ############## Shrinking intervals ##############
    #################################################
    #################################################
    filtered = []
    i = 0
    found = False
    begin = -1
    tuple_ = -1
    while True:
        if i > len(to_send) - 1:
            if found:
                if tuple_[0] == tuple_[1]:
                    filtered.append(tuple_[0])
                else:
                    filtered.append(tuple_)
            break
        if type(to_send[i]) is str:
            if not found:
                filtered.append(to_send[i])
            else:
                if tuple_[0] == tuple_[1]:
                    filtered.append(tuple_[0])
                else:
                    filtered.append(tuple_)
                found = False
                filtered.append(to_send[i])

        if type(to_send[i]) is int:
            if not found:
                tuple_ = (to_send[i], to_send[i])
                found = True
            else:
                if to_send[i] == to_send[i - 1] +1:
                    tuple_ = (tuple_[0], to_send[i])
                else:
                    if tuple_[0] == tuple_[1]:
                        filtered.append(tuple_[0])
                    else:
                        filtered.append(tuple_)
                    tuple_ = (to_send[i], to_send[i])
                    found = False
        i +=1
    cost = 0
    for entry in filtered:
        if type(entry) is str:
            cost += len(entry)
        if type(entry) is int:
            cost += 1
        if type(entry) is tuple:
            cost += 2
    #print("The cost is",cost,"bytes over an edit distance of", ED)
    #print("Time elapsed:", time() - start_time)
    return EST,cost, filtered
