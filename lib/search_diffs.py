import hashlib

lookup_table = {}

def fill_lookup_table(sender_weak_checks, sender_md4_checks):
    for i,key in enumerate(sender_weak_checks):
        entry = key
        mask = 0b01111111111111111
        key = entry & mask
        if key in lookup_table:
            lookup_table[key].append((i,entry,sender_md4_checks[i]))
        else:
            lookup_table[key] = [(i,entry,sender_md4_checks[i])]

def sign_from_scratch(block, S, M):
    a = sum(block) % M
    b = sum([(S-i)*x for i,x in enumerate(block)]) % M
    return a,b

def find_diffs(readfile, len_blocks, weak_checksums, md4_checksums, S, M):
    with open(readfile, 'rb') as f:
        data = f.read()
        if len(data) <= S:
            return [data]
    fill_lookup_table(weak_checksums, md4_checksums)
    matches = []
    #FINDING THE DIFFERENCES
    last_match = 0
    from_scratch = True
    for i in range(0, len(data)):
        block = data[i:i+S]
        if from_scratch:
            a, b = sign_from_scratch(block, S, M)
            from_scratch = False
        else:
            try:
                a = (a - data[i-1] + data[i+S-1]) % M
                b = (b - (S)*data[i-1] + a) % M
            except IndexError:
                a = (a - data[i-1]) % M
                b = (b - (S)*data[i-1] + a) % M
        entry = a+M*b
        mask = 0b01111111111111111
        key = entry & mask
        #FIRST LEVEL SEARCH: find a "soft" match
        if key in lookup_table:
            #SECOND LEVEL SEARCH: find a "middle" match
            for tuple_ in lookup_table[key]:
                if tuple_[1] == entry:
                    #THIRD LEVEL SEARCH: find a "tough" match
                    block_digest = hashlib.new("md4", block).digest()
                    if tuple_[2] == block_digest:
                        current_match = i
                        if len(data[last_match:current_match]) > 0:
                            matches.append(data[last_match:current_match])
                        matches.append(tuple_[0])
                        try:
                            lookup_table[key].remove(tuple_)
                        except ValueError:
                            pass
                        last_match = current_match + S
                        i += S
                        from_scratch = True
        if len(block) <= len(data) % S:
            if len(len_blocks) > len(matches):
                matches.append(data[last_match:])
            break
    if len(matches) < 1:
        matches.append(data)
    return matches

def easy_diffs(readfile, data):
    with open(readfile, 'rb') as f:
        actual_state = f.read()
        #this check is done in this way just for the sake of the simulation
        if str(data)[2:-1] == str(actual_state)[2:-1]:
            return None
        else:
            return actual_state
