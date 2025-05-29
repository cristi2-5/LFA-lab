def load_matrix(fn):
    m=[]
    with open(fn,"r") as fisier:
        for linie in fisier:
            linie=linie.split()
            if linie[0][0]!="/":
                for i in range(len(linie)):
                    linie[i]=int(linie[i])
                m.append(linie)
    if check(m)==True:
        return m
    else:
        print("nu")
        return 0
def save_matrix(m,fn):
    if check(m):
        with open(fn, "w") as file:
            for line in m:
                file.write(" ".join(map(str, line)) + "\n")
def check(m):
    size = len(m[0])
    ok = 1
    for i in range(len(m)):
        if len(m[i]) != size:
            ok = 0
    if ok == 1:
        return True
    else:
        return False
matrix=load_matrix("read.txt")
if matrix != 0:
    save_matrix(matrix,"write.txt")
else:
    with open("write.txt", "w") as file:
        file.write("no matrix\n")