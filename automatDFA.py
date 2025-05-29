def start_file(file, states):
    # Gaseste si returneaza starea initiala a automatului, specificata in sectiunea '[Start_point]' a fisierului.
    point = -1

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[Start_point]":
                break
        else:
            raise ValueError("Sectiunea [Start_point] nu a fost gasita! Te rog revizuieste inputul!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]":
                break
            point = line

    if point == -1 or point not in states:
        raise ValueError("Nu exista un punct de start valid sau acesta nu e in lista starilor!")

    return point


def states_file(file):
    # Extrage din fisier lista completa a starilor pe care le poate avea automatul.
    # Citeste din sectiunea '[States]' si valideaza ca exista cel putin o stare
    states_list = []

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[States]":
                break
        else:
            raise ValueError("Sectiunea [States] nu a fost gasita! Te rog revizuieste inputul!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]":
                break
            states_list.extend(line.split())
    if not states_list or len(set(states_list)) != len(states_list):
        raise ValueError("Lista starilor este goala sau contine duplicate! Te rog revizuieste inputul!")

    return states_list

def ending_file(file, states):
    # Identifica si returneaza starile finale (sau de acceptare) ale automatului.
    ending_list = []

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[Ending_points]":
                break
        else:
            raise ValueError("Sectiunea [Ending_points] nu a fost gasita! Te rog revizuieste inputul!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]":
                break
            ending_list.extend(line.split())
    if not ending_list or not set(ending_list).issubset(states): # Am simplificat putin conditia
        raise ValueError("Lista starilor finale este goala sau contine stari nedefinite! Te rog revizuieste inputul!")

    return ending_list


def alpha_file(file, states):
    # Citeste simbolurile acceptate de automat (alfabetul) din sectiunea '[Alpha]'.
    alpha_list = []

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[Alpha]":
                break
        else:
            raise ValueError("Sectiunea [Alpha] nu a fost gasita! Te rog revizuieste inputul!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]":
                break
            alpha_list.extend(line.split())
    if not alpha_list or len(set(alpha_list)) != len(alpha_list) or len(alpha_list) < len(states).bit_length():
        raise ValueError("Alfabetul lipseste, contine duplicate sau are prea putine simboluri! Te rog revizuieste inputul!")

    return alpha_list


def transitions_file(file, states, alpha):
    # Parseaza definitiile tranzitiilor din sectiunea '[Transitions]' a fisierului.
    # Pentru fiecare linie identifica starea curenta simbolurile de tranzitie si starea urmatoare
    # construind o structura de date (dictionar) ce mapeaza aceste reguli.
    # Valideaza ca toate starile si simbolurile folosite in tranzitii sunt corecte
    # si ca nu exista ambiguitati (o combinatie stare-simbol sa nu duca la mai multe stari).
    dtrans = {}

    with open(file, "r") as f:
        for line in f:
            if line.strip() == "[Transitions]":
                break
        else:
            raise ValueError("Sectiunea [Transitions] nu a fost gasita! Te rog revizuieste inputul!")

        for line in f:
            line = line.strip()
            if not line or line == "[End]": # Ignora liniile goale sau marcajul de final
                break

            parts = line.split(maxsplit=1)
            if len(parts) < 2: # Verifica daca linia are formatul asteptat
                raise ValueError(f"Format invalid pentru tranzitie: '{line}'. Lipsesc parti.")

            current_state = parts[0]
            # Extrage simbolurile si starea urmatoare
            try:
                end_of_symbols_marker_index = parts[1].index("]")
                symbols_part = parts[1][:end_of_symbols_marker_index]
                next_state_part = parts[1][end_of_symbols_marker_index+1:].strip()
                symbols_list = symbols_part.lstrip("[").split()

            except ValueError: # Daca ']' nu este gasit sau alte probleme de formatare
                 raise ValueError(f"Format invalid pentru simboluri/stare urmatoare in tranzitia: '{line}'")


            if not current_state or not next_state_part or not symbols_list:
                 raise ValueError(f"Elemente lipsa in definitia tranzitiei: '{line}'")


            if current_state not in states or next_state_part not in states or not set(symbols_list).issubset(alpha):
                raise ValueError(f"Tranzitie invalida: '{line}'. Stari sau simboluri necunoscute.")

            if current_state not in dtrans:
                dtrans[current_state] = {}

            for symbol in symbols_list:
                if symbol not in dtrans[current_state]:
                    dtrans[current_state][symbol] = next_state_part
                else:
                    raise ValueError(f"Tranzitie duplicata/nedeterminism: Starea '{current_state}' cu simbolul '{symbol}' are deja o tranzitie.")
    if not dtrans:
        raise ValueError("Nu au fost definite tranzitii! Te rog revizuieste inputul.")
    return dtrans

def verificare_input(number, start, ending, transitions):
    # Proceseaza un sir de intrare ('number') caracter cu caracter pentru a determina daca este acceptat de automat.
    current_state = start
    for symbol in number:
        # Verifica daca pentru starea curenta exista tranzitii definite
        if current_state not in transitions:
            return 0
        if symbol not in transitions[current_state]:
            # Daca nu exista tranzitie pentru acest simbol sirul nu este acceptat
            return 0
        current_state = transitions[current_state][symbol]

    if current_state in ending:
        return 1
    else:
         return 0


try:
     states = states_file("instructions.txt")
     start = start_file("instructions.txt", states)
     ending = ending_file("instructions.txt", states)
     alpha = alpha_file("instructions.txt", states)
     transitions = transitions_file("instructions.txt", states, alpha)

     number = input("Introduceti sirul de verificat: ")
     result = verificare_input(number, start, ending, transitions)

     if result == 1:
         print("Sirul este acceptat de automat.")
     else:
         print("Sirul NU este acceptat de automat.")

except ValueError as e:
    print(f"Eroare de configurare sau input: {e}")
except FileNotFoundError:
     print("Fisierul 'instructions.txt' nu a fost gasit.")
except Exception as e:
     print(f"A aparut o eroare neasteptata: {e}")