import numpy as np
import random
import re as regex
import os.path as path


def generate_random_betas_vector(number_of_betas, bits_per_beta):
    '''
        Genrates 4 random beta values
    '''
    random_betas_vector = []
    for beta in range(number_of_betas):
        random_beta = random.randint(0, (2**bits_per_beta)-1)
        random_betas_vector.append(random_beta)
    return random_betas_vector


def calc_MSE(x, y, num_rows, beta_vector):
    '''reduce each beta to fall into a specified range
       -(2^19)/10 to (2^19)-1/10
       and calculate the mean squared error
    '''
    B = [(beta - 2**19)/10 for beta in beta_vector]
    B = np.array(B)
    # RSS = (Y - Y')^2 but since we can't do square, we use transpose multiplication
    error = (y - x @ B).conjugate().transpose() @ (y - x @ B)
    MSE = error/num_rows
    # Now we can take the root of our MSE since we squared it to avoid errors
    root_MSE = MSE ** 0.5
    return root_MSE


def get_neighbor(current_betas_vector):
    '''
        A function that finds all the neighbors of a vector
        If a vector size is 80 bits, then there are 80
        neighbors since at a time we can only change one bit
    '''
    for index in range(number_of_betas):
        for bit_index in range(bits_per_beta):
            old_beta = current_betas_vector[index]
            # shift 1 per bit so only one bit per neighbor changes
            bit_mask = 1 << bit_index
            new_beta = old_beta ^ bit_mask
            neighbor = current_betas_vector[:]
            neighbor[index] = new_beta
            yield neighbor


def input_files_read(exit_cond_files, x_file, y_file):
    # load the data of each file
    x = np.loadtxt(x_file)
    y = np.loadtxt(y_file)
    num_rows, num_columns = np.shape(x)
    exit_conditions = []
    try:
        with open(exit_cond_files, 'r') as myfile:
            file_content = myfile.read()
            filtered_content = re.split(r"\D+", file_content)
            exit_conditions[0] = file_content[1]
            exit_conditions[1] = file_content[2]
    except:
        print("problem opening your file.....")
    return x, y, num_rows, num_columns, exit_conditions


def hill_climbing(nums_of_betas, bits_per_beta, generations, restarts):
    entire_vector_size = number_of_betas * bits_per_beta
    for value in range(restarts):
        local_min = False
        current_beta_vector = generate_random_betas_vector()
        current_mse = calc_MSE(current_beta_vector)
        generation_count = 1
        while generation_count <= generations and local_min == False:
            found_better_neighbor = False
            # print("generation count --> ", generation_count, "\n")
            neighbor_generator = get_neighbor(current_beta_vector)
            for bit in range(entire_vector_size):
                neighbor = next(neighbor_generator)
                neighbor_fitness = calc_MSE(neighbor)
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


x_file = path.abspath("../HousingData/X.txt")
y_file = path.abspath("../HousingData/Y.txt")
exit_file = path.abspath("./EXIT_CONDITIONs.txt")
needed_data = input_files_read(exit_file, x_file, y_file)

x = needed_data[0]
y = needed_data[1]
num_rows = needed_data[2]
num_of_betas = needed_data[3]
exit_conditions = needed_data[4]
bits_per_beta = 20
entire_vector_size = num_of_betas * bits_per_beta
generations = 3000
restarts = 100

hill_climbing(nums_of_betas, entire_vector_size, generations, restarts)
