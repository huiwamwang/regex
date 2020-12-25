def analyzer(reg, inp):
    #print('analyzer', reg, inp)
    if reg == '':
        return True
    elif inp == '' or reg[0] != inp[0] and reg[0] != '.':
        return False
    return analyzer(reg[1:], inp[1:])


def pre_analyzer(reg, inp):
    #print('pre_analyzer', reg, inp)
    try:
        if '?' == reg[1]:
            if reg[0] == inp[0]:
                #print('--? ==--', reg, inp)
                return analyzer(reg[2:], inp[1:])
            elif reg[0] == '.':
                if len(reg) == 2:
                    return True
                elif reg[2] != inp[0]:
                    return analyzer(reg[2:], inp[1:])
                elif reg[2] == inp[0]:
                    return analyzer(reg[2:], inp)
            elif reg[0] != inp[0]:
                #print('--? !=--', reg, inp)
                return analyzer(reg[2:], inp)
        elif '*' == reg[1]:
            if reg[0] == '.':
                if len(reg)-2 == len(inp):
                    return analyzer(reg[2:], inp)
                elif inp == '':
                    return True
                else:
                    return pre_analyzer(reg, inp[1:])
            elif reg[0] == inp[0]:
                #print("--*--", reg, inp)
                return pre_analyzer(reg, inp[1:])
            elif reg[0] != inp[0]:
                #print("--not *--", reg, inp)
                return pre_analyzer(reg[2:], inp)
        elif '+' == reg[1]:
            global counter
            #print('--+--', reg, inp, counter)
            if reg[0] == '.':
                if len(reg)-2 == len(inp):
                    return analyzer(reg[2:], inp)
                elif inp == '':
                    return True
                else:
                    return pre_analyzer(reg, inp[1:])
            elif reg[0] == inp[0]:
                counter += 1
                return pre_analyzer(reg, inp[1:])
            elif reg[0] != inp[0]:
                if counter == 0:
                    return False
                elif counter > 0:
                    return analyzer(reg[2:], inp)
    except IndexError:
        pass
    if '?' not in reg and '*' not in reg and '+' not in reg and len(reg) == len(inp):
        return analyzer(reg, inp)
    elif reg == '':
        return True
    elif inp == '':
        return False
    elif reg[0] == inp[0] or reg[0] == '.':
        return pre_analyzer(reg[1:], inp[1:])
    #print('end of pre_analyzer', reg, inp)
    return pre_analyzer(reg, inp[1:])


def checker(reg, inp):
    if reg == '':
        return True
    elif '\\' in reg:
        if reg[reg.index('\\')+1] in inp:
            return True
        else:
            return False
    elif reg[0] == '^' and reg[-1] == '$':
        if len(reg[1:-1]) == len(inp):
            return analyzer(reg[1:-1], inp)
        elif '?' in reg or '*' in reg or '+' in reg:
            return pre_analyzer(reg[1:-1], inp)
        else:
            return False
    elif reg[0] == '^':
        if '?' in reg or '*' in reg or '+' in reg:
            return pre_analyzer(reg[1:], inp)
        else:
            return analyzer(reg[1:], inp)
    elif reg[-1] == '$':
        return pre_analyzer(reg[0:-1], inp[-len(reg)+1:])
    return pre_analyzer(reg, inp)


counter = 0
#while True:
print(checker(*input().split('|')))
