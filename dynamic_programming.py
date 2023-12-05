# Nama: Monica Oktaviona
# NPM: 2106701210
# Kode Asdos: 4
# Kelas: C
# Desain dan Analisis Algoritma
# Semester Ganjil 2023/2024

# The algorithm below is retrieved from: https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/

import sys

def unboundedKnapsack(W, wt, val, idx, dp):
    sys.setrecursionlimit(15000)  # Set recursion limit

    # Base Case 
    # if we are at idx 0. 
    if idx == 0: 
        return (W // wt[0]) * val[0] 
    # If the value is already calculated then we will 
    # previous calculated value 
    if dp[idx][W] != -1: 
        return dp[idx][W] 
    # There are two cases either take element or not take. 
    # If not take then 
    notTake = 0 + unboundedKnapsack(W, wt, val, idx - 1, dp) 
    # if take then weight = W-wt[idx] and index will remain 
    # same.
    take = float('-inf') 
    if wt[idx] <= W: 
        take = val[idx] + unboundedKnapsack(W - wt[idx], wt, val, idx, dp) 
    dp[idx][W] = max(take, notTake) 
    return dp[idx][W] 


if __name__ == '__main__':
    # Driver code 
    W = 100
    val = [10, 30, 20] 
    wt = [5, 10, 15] 
    n = len(val) 
    dp = [[-1 for _ in range(W+1)] for _ in range(n)] 
    print("Maximum value: ", unboundedKnapsack(W, wt, val, n-1, dp))

	