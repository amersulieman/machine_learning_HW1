import numpy as np
import random
import time


def generate_random_bits_vector():
    betas_vector = []
    for beta in range(number_of_betas):
        random_number = np.random.choice([0, 1], size=(20))
        betas_vector.append(list(random_number))
    return betas_vector


def convert_binary_betas_to_numbers(betas_vector):
    # holds the final betas
    betas = []
    for binary_beta in betas_vector:
        # concatenate the binaries to be treated as one binary number
        string_betas = "".join(map(str, binary_beta))
        # convert the base 2 binary number to integer
        beta = int(string_betas, 2)
        # subtract by 2^19 and divide by 10 to set the range i decided for my betas
        beta -= (2**19)
        beta /= 10
        betas.append(beta)
    return betas


def calc_MSE(x, y, betas, num_rows):
    B = convert_binary_betas_to_numbers(betas)
    B = np.array(B)  # convert it to numpy array
    # RSS = (Y - Y')^2 but since we can't do square, we use transpose multiplication
    error = (y - x @ B).conjugate().transpose() @ (y - x @ B)
    MSE = error/num_rows
    # Now we can take the root of our MSE since we squared it to avoid erros
    root_MSE = MSE ** 0.5
    return root_MSE


def get_neighbor_and_its_fitness(betas_vector):
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
            neighbor_fitness = calc_MSE(x, y, neighbor, num_rows)
            yield neighbor, neighbor_fitness


# load the data of each file
x = np.loadtxt("../HousingData/X.txt")
y = np.loadtxt("../HousingData/Y.txt")
number_of_betas = 4
bits_per_beta = 20
entire_vector_size = number_of_betas * bits_per_beta
num_rows, _ = np.shape(x)


iterations = 10
begin = time.time()
generation = 30000
restart = 100
all_mses = []
for value in range(restart):
    local_min = False
    current_beta_vector = generate_random_bits_vector()
    current_mse = calc_MSE(x, y, current_beta_vector, num_rows)
    generation_count = 1
    while generation_count <= generation and local_min == False:
        found_better_neighbor = False
        # print("generation count --> ", generation_count, "\n")
        neighbor_generator = get_neighbor_and_its_fitness(
            current_beta_vector)
        for bit in range(entire_vector_size):
            neighbor, neighbor_fitness = next(neighbor_generator)
            if neighbor_fitness < current_mse:
                current_beta_vector = neighbor
                current_mse = neighbor_fitness
                found_better_neighbor = True
        if not found_better_neighbor:
            # print("Reached local min")
            # print("Betas --> ", convert_binary_betas_to_numbers(current_beta_vector))
            # print("Local MSE--> ", current_mse)
            local_min = True
        generation_count += 1
        all_mses.append(current_mse)
end = time.time()
print("speed -> ", end-begin)
