'''
This method represents the task that will be executed by each device during
the simulation. You can change it as you wish. for the correct execution of the
simulation it must return an array of INTEGER values which represents the amount of
information that will be sent as a BLACK BOX to lower levels of the TCP/IP stack.
'''

from lib.signature import *
from lib.search_diffs import *
import ED_RDIFF.ed_rsync as ed_diff
import matplotlib.pyplot as plt
import numpy as np
from random import choice,randint, random
import editdistance as ed
import os, json
from math import ceil

SYNC = 1
S = 512
doc_size = 3000

def task(rnm):
    chars = range(0,255)
    old = bytes([choice(chars) for _ in range(doc_size)])
    open('start'+str(rnm)+'.file', 'wb+').write(old)
    DEL_PROB = 0.4
    END_PROB = 0.7
    new = old
    while True:
        event = random()
        if event > END_PROB:
            if ed.eval(old,new) > 0:
                break
            else:
                continue
        elif event > DEL_PROB:
            size = randint(0, ceil(len(new)/4))
            index = randint(0, len(new)-size)
            new = new[:index]+new[index+size:]
            DEL_PROB += 0.03
        else:
            size = randint(0, ceil(len(old)/3))
            index = randint(0, len(old)-size)
            chars = range(0,255)
            random_bytes = bytes([choice(chars) for _ in range(size)])
            new = new[:index]+random_bytes+new[index:]
            END_PROB -= 0.02
    open('new'+str(rnm)+'.file', 'wb+').write(new)
    if SYNC == 1:
        blocks, sender_md4_checks, sender_weak_checks = sign_file('start'+str(rnm)+'.file', S)
        diffs = find_diffs('new'+str(rnm)+'.file', blocks, sender_weak_checks, sender_md4_checks, S, M)
        bytes_count_orig = 0
        for e in diffs:
            if type(e) is bytes:
                bytes_count_orig += len(e)
            elif type(e) is int:
                bytes_count_orig += 2
        os.system('rm start'+str(rnm)+'.file')
        os.system('rm new'+str(rnm)+'.file')
        return [20*ceil(20*len(new)/S), bytes_count_orig]
    else:
        diffs = ed_diff.find_diffs(old,new)
        bytes_count_ed = 0
        for e in diffs[2]:
            if type(e) is bytes:
                bytes_count_ed += len(e)
            elif type(e) is int:
                bytes_count_ed += 2
            elif type(e) is tuple:
                bytes_count_ed += 4
        os.system('rm start'+str(rnm)+'.file')
        os.system('rm new'+str(rnm)+'.file')
        return [bytes_count_ed]
