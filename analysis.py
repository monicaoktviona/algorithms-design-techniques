# Nama: Monica Oktaviona
# NPM: 2106701210
# Kode Asdos: 4
# Kelas: C
# Desain dan Analisis Algoritma
# Semester Ganjil 2023/2024

import time
import os
import dynamic_programming
import branch_and_bound
import sys
import psutil

def run(algorithm, caller, W, *args):
    """
    Fungsi untuk menjalankan algoritma (yang ditentukan pada parameter)
    untuk menghitung maximum value dari 0/1 Knapsack Problem (Repetition
    of items allowed). 
    
    Fungsi ini juga melakukan perhitungan waktu dan memory.
    """
    dataset_path = "./dataset/"
    
    for dataset in os.scandir(dataset_path):
        with open(dataset, "r") as current_dataset:
            lines = current_dataset.readlines()[1:]

            print("=" * 30)
            print(algorithm)
            print("=" * 30)
            print(f"File: {dataset.name}")
            print("-" * 30)

            start_time = time.time()
            memory = psutil.Process().memory_info().rss


            max_value = caller(lines, W, *args)

            end_time = time.time()
            psutil.Process().memory_info().rss

            print("Maximum value: ", max_value)
            print("-" * 30)
            print(f"Time taken: {((end_time-start_time)*1000):.10f} ms")
            print(f"Memory used: {memory} Bytes")
            print("=" * 30)
            print()


def dynamic_programming_caller(lines, W, *args):
    sys.setrecursionlimit(15000)  # Set recursion limit

    weights = []
    values = []		

    for line in lines:
        weight, value = map(int, line.split())
        weights.append(weight)
        values.append(value)

    n = len(weights)

    dp = [[-1 for _ in range(W+1)] for _ in range(n)] 

    result = dynamic_programming.unboundedKnapsack(W, weights, values, n-1, dp, *args)

    return result


def branch_and_bound_caller(lines, W, *args):
    sys.setrecursionlimit(100000000)  # Set recursion limit

    data = []
    for line in lines:
        weight, value = map(int, line.split())
        data.append((weight, value))
    
    to_visit = branch_and_bound.eliminate_dominated(data)
    N, W_prime, m, i, z_hat, V, x_hat, x, M, U = branch_and_bound.initialization(to_visit, W)
    result = branch_and_bound.develop(N, W_prime, m, i, z_hat, V, x_hat, x, M, U)
    return(result[0])


if __name__ == '__main__':
    W = 500     # capacity

    # dynamic programming
    run("Dynamic Programming", dynamic_programming_caller, W)

    # branch and bound
    run("Branch and Bound", branch_and_bound_caller, W)

