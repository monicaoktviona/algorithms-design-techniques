# Nama: Monica Oktaviona
# NPM: 2106701210
# Kode Asdos: 4
# Kelas: C
# Desain dan Analisis Algoritma
# Semester Ganjil 2023/2024

# Reference: https://www.tandfonline.com/doi/pdf/10.1057/palgrave.jors.2601698?casa_token=EW35GGben2sAAAAA%3AVZt6DkysIcc7im289FIjHbV6Q3nZr2vYAH_HtWInlRnwryJnWsXKK87_g478Gof5mB_MDiz29IDO1eA 

import math
import sys

def eliminate_dominated(N):
    j = 0
    while j <= len(N)-2:
        k = j + 1
        while k <= len(N)-1:
            if (math.floor(N[k][0]/N[j][0]) * N[j][1] >= N[k][1]):
                N.pop(k)
            elif (math.floor(N[j][0]/N[k][0]) * N[k][1] >= N[j][1]):
                N.pop(j)
                k = len(N)-1
            else:
                k += 1
        j += 1
    return N

def initialization(N, W):
    # Sort non-dominated items according to decreasing v/w ratios
    N.sort(key=lambda x: x[1] / x[0], reverse=True)

    x_hat = 0   # current best solution
    z_hat = 0   # current best solution value
    i = 0       # index

    # Initialize empty sparse matrix M
    M = [[0] * len(N) for _ in range(len(N))]

    # Initialize empty list x
    x = [0] * len(N)      

    x[i] = math.floor(W/N[i][0])
    V = N[i][1] * x[i]
    W_prime = W - N[i][0] * x[i]

    # Calculate U
    U = calculate_u(N, W, V, i)

    # Find mi for all i and store it into m list
    m = []
    for p in range(0, len(N)):
        mi = sys.maxsize   
        for q in range(p+1, len(N)):
            mi = min(N[q][0], mi)
        m.append(mi)
    return N, W_prime, m, i, z_hat, V, x_hat, x, M, U

def develop(N, W_prime, m, i, z_hat, V, x_hat, x, M, U):
    if W_prime < m[i]:
        if z_hat < V:
            z_hat = V
            x_hat = x
            if z_hat == U:
                return(z_hat, x_hat)
        backtrack(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)
    else:
        # Find minimum j such that j > i and wj <= W'
        j = i + 1
        for idx in range(i+1, len(N)):
            if (N[idx][0] <= W_prime):
                j = idx
                break
        
        if V + calculate_u(N, W, V, j) <= z_hat:
            backtrack(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)
        
        if M[i, W_prime] >= V:
            backtrack(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)

        x[j] = math.floor(W_prime/N[j][0])
        V = V + N[j][1] * x[j]
        W_prime = W_prime - N[j][0] * x[j]
        M[i, W_prime] = V
        i = j
        develop(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)
    backtrack(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)

def backtrack(N, W_prime, m, i, z_hat, V, x_hat, x, M, U):
    j = i
    for idx in range (i, -1, -1):
        if x[j] > 0:
            j = idx
            break
    
    if j < 1:
        return z_hat, x_hat
    
    i = j
    x[i] = x[i]-1
    V = V - N[i][1]
    W_prime = W_prime + N[i][0]

    if W_prime < m[i]:
        backtrack(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)
    
    if V + math.floor((W_prime) * (N[i+1][1]/N[i+1][0])) <= z_hat:
        V = V - N[i][1] * x[i]
        W_prime = W_prime + N[i][0] * x[i]
        x[i] = 0
        backtrack(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)

    if W_prime - N[i][0] >= m[i]:
        develop(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)

    j = i
    h = j + 1
    replace(N, W_prime, m, j, h, i, z_hat, V, x_hat, x, M, U)

def replace(N, W_prime, m, j, h, i, z_hat, V, x_hat, x, M, U):
    if z_hat >= V + math.floor(W_prime * (N[h][1]/N[h][0])):
        backtrack(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)
    
    if N[h][0] >= N[j][0]:
        if N[h][0] == N[j][0] or N[h][0] > W_prime or z_hat >= V + N[h][1]:
            h = h + 1
            replace(N, W_prime, m, j, h, i, z_hat, V, x_hat, x, M, U)
    
        z_hat = V + N[h][1]
        x_hat = x
        x[h] = 1

        if z_hat == U:
            return z_hat, x_hat
        
        j = h
        h = h + 1
        replace(N, W_prime, m, j, h, i, z_hat, V, x_hat, x, M, U)
    else:
        if W_prime - N[h][0] < m[h-1]:
            h = h + 1
            replace(N, W_prime, m, j, h, i, z_hat, V, x_hat, x, M, U)
        
        i = h
        x[i] = math.floor(W_prime/N[i][0])
        V = V + N[i][1] * x[i]
        W_prime = W_prime - N[i][0] * x[i]
        develop(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)

    return z_hat, x_hat 

def calculate_u(N, W, V, i):
    if i + 2 >= len(N):
        return V
    else:
        w1, w2, w3 = N[i][0], N[i+1][0], N[i+2][0]
        v1, v2, v3 = N[i][1], N[i+1][1], N[i+2][1]

        W_prime = W - math.floor(W/w1) * w1
        z_prime = math.floor(W/w1) * v1 + math.floor(W_prime/w2) * w2
        W_double_prime = W_prime - math.floor(W_prime/w2) * w2
        U_prime = z_prime + math.floor(W_double_prime * (v3/w3))
        U_double_prime = z_prime + math.floor((W_double_prime + math.ceil((1/w1) * (w2 - W_double_prime)) * w1) * (v2/w2) - math.ceil((1/w1)*(w2-W_double_prime)) * v1)
        return max(U_prime, U_double_prime)


if __name__ == '__main__':
    sys.setrecursionlimit(15000)  # Set recursion limit

    W = 100     # capacity
    w_v = [(5, 10), (10, 30), (15, 20)]  # list of (weight, value)
    to_visit = eliminate_dominated(w_v)   # nodes to visit
    N, W_prime, m, i, z_hat, V, x_hat, x, M, U = initialization(to_visit, W)
    result = develop(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)
    print("Maximum value: ", result[0])


