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
state_1 letter state_2 letter direction (#! first rule must have the start state on the first state position)
state_3 letter state_4 letter direction (#! direction MUST be R or L)
...
'''


# Incarca definitia automatului din fisier
def load_auto(name):
    auto = {}
    with open(name, encoding='utf-8') as input_file:
        curr = None
        for line in input_file: # Folosim input_file aici
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
    if len(rule) == 5 and rule[0] in states and rule[2] in states and rule[1] in dc["sigma"] and rule[3] in dc[
        "sigma"] and (rule[4] == "R" or rule[4] == "L"):
        return True
    return False


# Verifica daca toate regulile sunt valide
def all_valid_rules(dc):
    return all(is_valid_rule(rule, dc) for rule in dc['rules'])


# Verifica daca prima regula incepe cu starea initiala
def is_valid_firstrule(rule, start_state):
    return rule[0] == start_state


# Verifica daca sirul de intrare contine doar simboluri valide
def is_valid_input(ls, dc):
    return all(value in dc['sigma'] for value in ls)


# Functia principala care ruleaza simularea masinii Turing
def start_turing():
    auto = load_auto("turinginput4.txt")

    if not is_valid_auto(auto):
        print('Automat invalid - verifica definitia!')
        return

    if not all_valid_rules(auto):
        print('Automat invalid - verifica regulile!')
        return

    input_string = list(input("Introdu sirul de intrare: ").split())
    index = 0
    banda = input_string.copy()
    banda.extend(['_'] * 100)  # Extinde banda cu spatii libere

    if not is_valid_input(input_string, auto):
        print('Input invalid - simboluri nepermise!')
        return

    curr_state = None
    final_state = None

    # Identifica starea initiala si cea finala
    for state in auto['states']:
        if len(state) > 1 and state[1] == 'S':
            curr_state = state[0]
        elif len(state) > 1 and state[1] == 'F':
            final_state = state[0]

    if not curr_state:
        print('Nu s-a gasit starea initiala!')
        return

    if not final_state:
        print('Nu s-a gasit starea finala!')
        return

    if not is_valid_firstrule(auto['rules'][0], curr_state):
        print('Prima regula nu incepe cu starea initiala!')
        return

    print(f'Stare initiala: {curr_state}')
    print(f'Continut banda: {banda}')

    # Simularea masinii Turing
    while curr_state != final_state:
        if index < 0 or index >= len(banda):
            print("Eroare: Indicatorul a iesit din banda!")
            break

        rule_found = False
        for rule in auto['rules']:
            if rule[0] == curr_state and rule[1] == banda[index]:
                curr_state = rule[2]
                banda[index] = rule[3]

                if rule[4] == "R":
                    index += 1
                else:
                    index -= 1

                print(f'Stare curenta: {curr_state}')
                print(f'Pozitie indicator: {index}')
                print(f'Banda actualizata: {banda}')
                rule_found = True
                break

        if not rule_found:
            print("Eroare: Nu exista tranzitie valida!")
            break

    if curr_state == final_state:
        print("Sir acceptat!")

    # Afiseaza banda fara spatii libere
    print(f'Continut final banda: {[x for x in banda if x != "_"]}')


start_turing()