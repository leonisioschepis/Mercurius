def build_file(readfile, matches, S):
    try:
        with open(readfile, 'r') as f:
            data = f.read()
    except FileNotFoundError:
        print(str(matches)[2:-1].replace('\\n','\n'), file = open(readfile, 'w'), end='')
        return
    if len(data) < S:
        print(str(matches)[2:-1].replace('\\n','\n'), file = open(readfile, 'w'), end='')
        return
    new_file = ""
    for element in matches:
        if type(element) is int:
            new_file += str(data[element*S:(element+1)*S])
        else:
            #that string need to be cleaned
            line = str(element)[2:-1].replace('\\n','\n')
            new_file += line
    print(new_file, file = open(readfile,'w'), end='')
