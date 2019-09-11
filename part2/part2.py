import numpy as np
import random
#load the data of each file
x = np.loadtxt("../HousingData/X.txt")
y = np.loadtxt("../HousingData/Y.txt")
number_of_betas = 4
bits_per_beta = 20
entire_vector_size = number_of_betas * bits_per_beta
num_rows,_ = np.shape(x)

def generate_random_bits_vector():
    betas_vector = []
    for beta in range(number_of_betas):
        random_number = np.random.choice([0,1], size =(20))
        betas_vector.append(list(random_number))
    return betas_vector

def convert_binary_betas_to_numbers(betas_vector):
    # holds the final betas
    betas = []
    for binary_beta in betas_vector:
        #concatenate the binaries to be treated as one binary number
        string_betas= "".join(map(str, binary_beta))
        #convert the base 2 binary number to integer
        beta = int(string_betas, 2)
        #subtract by 2^19 and divide by 10 to set the range i decided for my betas 
        beta -= (2**19)
        beta/=10
        betas.append(beta)
    return betas

def calc_MSE(x, y, betas, num_rows):
    B = convert_binary_betas_to_numbers(betas)
    B = np.array(B) #convert it to numpy array
    #RSS = (Y - Y')^2 but since we can't do square, we use transpose multiplication
    error = (y - x @ B ).conjugate().transpose() @ (y - x @ B)
    MSE = error/num_rows
    #Now we can take the root of our MSE since we squared it to avoid erros
    root_MSE = MSE **0.5 
    return root_MSE

def neighbor_producer(betas_vector):
    '''
        A function that finds all the neighbors of a vector
        If a vector size is 80 bits, then there are 80 
        neighbors since at a time we can only change one bit
    '''
    for beta in range(number_of_betas):
        for bit in range(bits_per_beta):
            new_beta = betas_vector[beta][:]
            new_beta[bit] ^= 1
            neighbor = betas_vector[:]
            neighbor[beta] = new_beta
            MSE = calc_MSE(x, y, neighbor, num_rows)
            yield neighbor 
        


generation = 3000
local_min = False
restart = 100
for value in range(restart):
    binary_beta_vector = generate_random_bits_vector()
    start_generation = 1
    neighbor = neighbor_producer(binary_beta_vectora)
    while start_generation <= 3000 or local_min == False:


# neighbor = neighbor_producer(vector)
# for x in range(80):
#    print(next(neighbor),"\n\n")
