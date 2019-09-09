import numpy as np
import random
#load the data of each file
x = np.loadtxt("../HousingData/X.txt")
y = np.loadtxt("../HousingData/Y.txt")

def generate_random_bits_vector():
    beta_bits = 19
    victor_bits = 19 *4
    random_number = []
    low = 0
    high = 2**20
    for x in range(4):
        rand_int = int((random.randint(low,high+1)-(2**19))/10)
        random_number.append(bin(rand_int))
    bin_arr = np.array(random_number)
    return bin_arr
