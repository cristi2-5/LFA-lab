def start_file(file,states):
    point = -1

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[Start_point]":
                break
        else:
            raise ValueError("Section [Start_point] not found! Please review input!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]":
                break
            point = line

    if point == -1 or point not in states:
        raise ValueError("There is no starting point!")

    return point

def states_file(file):
    states_list = []

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[States]":
                break
        else:
            raise ValueError("Section [States] not found! Please review input!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]":
                break
            states_list.extend(line.split())
    if not states_list or len(set(states_list)) != len(states_list):
        raise ValueError("There are no states! Please review input!")

    return states_list

def ending_file(file,states):
    ending_list = []

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[Ending_points]":
                break
        else:
            raise ValueError("Section [Ending_points] not found! Please review input!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]":
                break
            ending_list.extend(line.split())
    if not ending_list:
        raise ValueError("There are no ending states! Please review input!")

    return ending_list

def alpha_file(file, states):
    alpha_list = []

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[Alpha]":
                break
        else:
            raise ValueError("Section [Alpha] not found! Please review input!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]":
                break
            alpha_list.extend(line.split())
    if not alpha_list or len(set(alpha_list))!=len(alpha_list) or len(alpha_list)<len(states).bit_length():
        raise ValueError("You need more symbols! Please review input!")

    return alpha_list

def transitions_file(file, states, alpha):
    dtrans={}

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[Transitions]":
                break
        else:
            raise ValueError("Section [Transitions] not found! Please review input!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]":
                break

            line=line.split(maxsplit=1)
            line1=line[1].split("] ")
            alp_list=line1[0].split()
            alp_list[0]=alp_list[0].lstrip("[")
            first=line[0]
            second=line1[1]
            if first not in states or second not in states :
                raise ValueError("Please review input!You have duplicates!")

            if first not in dtrans:
                dtrans[first] = {}

            for i in alp_list:
                if i in alpha:
                    if i not in dtrans[first]:
                        dtrans[first][i]=[]
                        dtrans[first][i].append(second)
                    else:
                        dtrans[first][i].append(second)
                else:
                    raise ValueError("not in alpha")
    return dtrans

def verificare_input(number,start,ending,transitions):
    state_list = []
    state_list.append(start)
    for i in number:
        aux=[]
        for j in state_list:
            if i in  transitions[j]:
                for k in range(len(transitions[j][i])):
                        if "E" in transitions[transitions[j][i][k]]:
                            aux.append(transitions[j][i][k])
                            for l in range(len(transitions[transitions[j][i][k]]['E'])):
                                aux.append(transitions[transitions[j][i][k]]['E'][l])
                        else:
                            aux.append(transitions[j][i][k])
            else:
                aux.append(j)
        state_list=aux
    for i in aux:
        if i in ending:
            return  True
    return False



states = states_file("instructions.txt")
start = start_file("instructions.txt",states)
ending = ending_file("instructions.txt",states)
alpha = alpha_file("instructions.txt",states)
transitions = transitions_file("instructions.txt",states,alpha)
number=input()
print(verificare_input(number,start,ending,transitions))
