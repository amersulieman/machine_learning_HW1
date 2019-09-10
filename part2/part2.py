import numpy as np
import random
#load the data of each file
x = np.loadtxt("../HousingData/X.txt")
y = np.loadtxt("../HousingData/Y.txt")

def generate_random_bits_vector():

    number_of_betas = 4
    bits_per_beta = 20
    entire_vector_size = number_of_betas * bits_per_beta
    random_betas= []
    low = 0
    high = 2**bits_per_beta
    for beta in range(number_of_betas):
        # the following provides a range for rang between (-2^19 - 2^19)
        # Because my entire beta vector size is 2^20 bits combos
        random_number = random.randint(low, high+1) - (2**19)
        random_betas.append(format(random_number,"021b"))
    #format the binary with w1 bits, one will be used for negative sign
    # if there is no negative, anyway i will be only using 20 bits and ignoring 
    #first one example-> -1011 - > i will use 1011 for neighbors finding
    #                    01110 -> i will use 1110 for neighbors finding
    bin_arr = np.array(random_betas)
    return bin_arr

vector = generate_random_bits_vector()
print(vector)
# def calculate_MSE():

def calc_MSE(x, y, B, num_rows):
    #RSS = (Y - Y')^2 but since we can't do square, we use transpose multiplication
    error = (y - x @ B ).conjugate().transpose() @ (y - x @ B)
    MSE = error/num_rows
    #Now we can take the root of our MSE since we squared it to avoid erros
    root_MSE = MSE **0.5 
    return root_MSE


