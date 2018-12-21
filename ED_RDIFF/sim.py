from ed_diff import find_diffs
from random import randint,random, choice
from math import ceil
import string, _thread, queue, glob, os
from threading import Timer
from time import sleep, time
from sim_utils import Packet, Sensor, Buffer
import editdistance as ed

with open("backup", "rb") as f:
        old = f.read()

for filename in glob.glob("*.log"):
    os.remove(filename)

iteration = 3
num_threads = 3
print("Initial size:", len(old))

def sensor_task(sensor, iteration, old, queue, diffs_queue):
    item = queue.get()
    new = old
    with open(sensor.id+".log", "a+") as inputfile:
        for i in range(iteration):
            sleep(randint(5,15))
            if not sensor.queue.full():
                sensor.queue.put(None)
            ack = sensor.queue.get()
            if not ack is None:
                old = new
            old = new #to be removed
            print(sensor.id+" Iteration", i+1,file = inputfile)
            DEL_PROB = 0.5
            END_PROB = 0.8
            while True:
                event = random()
                if event > END_PROB:
                    break
                elif event > DEL_PROB:
                    size = randint(0, ceil(len(new)/2))
                    index = randint(0, len(new)-size)
                    print(size, "bytes removed from", index,file = inputfile)
                    new = new[:index]+new[index+size:]
                    DEL_PROB += 0.05
                else:
                    size = randint(0, ceil(len(old)/2))
                    index = randint(0, len(old)-size)
                    print(size, "bytes added at", index,file = inputfile)
                    chars = range(0,255)
                    #random_text = ''.join(choice(chars) for _ in range(size))
                    random_bytes = bytes([choice(chars) for _ in range(size)])
                    new = new[:index]+random_bytes+new[index:]
                    END_PROB -= 0.03

            block_size, cost, diffs = find_diffs(old, new)
            print("Estimated Block Size:", block_size,file = inputfile)
            print("Cost:", cost, "bytes",file = inputfile)
            print("New length:", len(new),file = inputfile)
            print("Edit Distance:", ed.eval(old,new),file = inputfile)
            print(diffs,file = inputfile)
            print("#############################################################",file = inputfile)
            packet = Packet(sensor.id, cost, block_size, diffs)
            diffs_queue.put(packet)
    queue.task_done()

def diffs_digester(target, sensors, queue, diffs_queue):
    token = queue.get()
    diffs_buffer = Buffer()
    t = 0
    def timer_event():
        if not diffs_buffer.empty():
            print(diffs_buffer.to_string())
            for item in diffs_buffer.container:
                sensors[int(list(item)[1]) - 1].queue.put("ACK")
            print(diffs_buffer.size, "bytes sent.")
            diffs_buffer.clean()
            t = 0
    while True:
        item = diffs_queue.get()                                                #blocking operation
        diffs_buffer.container[item.id] = item.diffs
        diffs_buffer.size += item.cost
        if diffs_buffer.size > diffs_buffer.max_size:
            print(diffs_buffer.to_string())
            for item in diffs_buffer.container:
                sensors[int(list(item)[1]) - 1].queue.put("ACK")
            print(diffs_buffer.size, "bytes sent.")
            diffs_buffer.clean()
            if not t == 0:
                t.cancel()
                t = 0
        else:
            if t == 0:
                t = Timer(10, timer_event)
                t.start()
        target -= 1
        print(target)
        if not target:
            if not diffs_buffer.empty():
                print(diffs_buffer.to_string())
                for item in diffs_buffer.container:
                    sensors[int(list(item)[1]) - 1].queue.put("ACK")
                print(diffs_buffer.size, "bytes sent.")
                diffs_buffer.clean()
                t = 0
            break
    queue.task_done()

diffs_q = queue.Queue()
sim_q = queue.Queue()
sensors = []
for i in range(num_threads):
    sim_q.put(None)
    sensor = Sensor("S"+str(i+1))
    try:
        t = _thread.start_new_thread(sensor_task, (sensor,iteration, old,sim_q,diffs_q))
    except:
       print ("Error: unable to start thread")
    sensors.append(sensor)
try:
    sim_q.put(None)
    _thread.start_new_thread(diffs_digester, (iteration*num_threads,sensors,sim_q, diffs_q,))
except:
    print ("Error: unable to start thread")
sim_q.join()
