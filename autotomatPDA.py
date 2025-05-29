'''
Input file must follow this model:
[states]
state_1 value
state_2 value
(#! value refers to S for start_state, F for final_state or anything else for intermediary states;
there can only be one start state, but if there are more than one state signaled with S, the last one will be considered the start state;
there can only be one final state, but if there are more than one state signaled with F, the last one will be considered the start state;
if a start_state is also a final_state it will be set seperately, not on the same row)
...

[sigma]
letter_1
letter_2
...

[rules]
state_1 input_value pop_value push_value state_2 (#! first rule must have the start state on the first state position)
state_3 input_value pop_value push_value state_4
...
'''

# Incarca definitia automatului din fisier
def load_auto(name):
    auto = {}
    with open(name) as input:
        curr = None
        for line in input:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            if line.startswith('[') and line.endswith(']'):
                curr = line.strip('[]')
                auto[curr] = []
            elif curr == "sigma":
                if line.strip() not in auto[curr]:
                    auto[curr].append(line.strip())
            elif curr is not None:
                if line.split() not in auto[curr]:
                    auto[curr].append(line.split())
    return auto

# Verifica daca automatul are structura corecta
def is_valid_auto(dc):
    ls = ['states', 'sigma', 'rules']
    for key in ls:
        if key not in dc.keys():
            return False
    return True

# Verifica daca o regula este valida
def is_valid_rule(rule, dc):
    states = []
    for state in dc['states']:
        states.append(state[0])
    if len(rule) == 5 and rule[0] in states and rule[4] in states and rule[1] in dc['sigma'] and rule[2] in dc['sigma'] and rule[3] in dc['sigma']:
        return True
    return False

# Verifica daca toate regulile sunt valide
def all_valid_rules(dc):
    length = 0
    rules = dc['rules']
    for rule in rules:
        if is_valid_rule(rule, dc):
            length += 1
    if length == len(rules):
        return True
    return False

# Verifica daca prima regula incepe cu starea initiala
def is_valid_firstrule(rule, start_state):
    if rule[0] == start_state:
        return True
    return False

# Verifica daca sirul de intrare contine doar simboluri valide
def is_valid_input(ls, dc):
    for value in ls:
        if value not in dc['sigma']:
            return False
    return True

# Functia principala care ruleaza simularea PDA
def start_pda():
    auto = load_auto("auto_pda_input2.txt")
    if is_valid_auto(auto) and all_valid_rules(auto):
        input_string = list(input("Introdu sirul de intrare: ").split())
        stack = []
        ok = 0
        if is_valid_input(input_string, auto):
            curr_state = None
            final_states = []
            for state in auto['states']:
                if state[1] == 'S':
                    curr_state = state[0]
                elif state[1] == 'F':
                    final_states.append(state[0])
            if is_valid_firstrule(auto['rules'][0], curr_state):
                print(f'{curr_state} ->', end=' ')
                for value in input_string:
                    ok = 0
                    for rule in auto['rules']:
                        if curr_state == rule[0] and rule[1] == 'e':
                            if stack and stack[-1] == rule[2]:
                                stack.pop()
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end=" ")
                                print(stack)
                                ok = 1
                                break
                            elif 'e' == rule[2]:
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end=" ")
                                print(stack)
                                ok = 1
                                break
                    for rule in auto['rules']:
                        if curr_state == rule[0] and rule[1] == value:
                            if stack and stack[-1] == rule[2]:
                                stack.pop()
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end=" ")
                                print(stack)
                                ok = 1
                                break
                            elif 'e' == rule[2]:
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end=" ")
                                print(stack)
                                ok = 1
                                break
                    for rule in auto['rules']:
                        if curr_state == rule[0] and rule[1] == 'e':
                            if stack and stack[-1] == rule[2]:
                                stack.pop()
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end=" ")
                                print(stack)
                                ok = 1
                                break
                            elif 'e' == rule[2]:
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end=" ")
                                print(stack)
                                ok = 1
                                break
                    if ok == 0:
                        print('!!! Sir respins - tranzitie invalida !!!')
                        break
                if stack != []:
                    print('!!! Sir respins - stiva nu este goala !!!')
                print(f'Stiva finala: {stack}')
            else:
                print('Automat invalid - verifica prima regula!')
        else:
            print('Input invalid - simboluri nepermise!')
    else:
        print('Automat invalid - verifica definitia!')

start_pda()