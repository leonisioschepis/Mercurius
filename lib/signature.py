import hashlib
M = 2**16                                                                       #they used 2^16 (because the result will be 32 bits)

def weak_cyclic_checksum(block, S):
    a = sum(block) % M                                                          #a = sum of all bytes in M modulus
    b = sum([(S-i)*x for i,x in enumerate(block)]) % M                          #b = sum of bytes times the position in the array in M modulus
    return a+M*b

def sign_file(f_read, S):
    md4_checksums = []
    weak_checksums = []
    blocks = []
    try:
        with open(f_read, 'rb') as f:
            data = f.read()
        for i in range(0, len(data), S):
            block = data[i:i+S]
            blocks.append(block)                                                #split it in blocks of size S
            block_digest = hashlib.new("md4", block).digest()
            md4_checksums.append(block_digest)                                  #md4 128 bits checksum for each block
            weak_checksums.append(weak_cyclic_checksum(block,S))
    except FileNotFoundError:
        pass
    return blocks, md4_checksums, weak_checksums
