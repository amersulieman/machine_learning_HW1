'''
    Amer Sulieman
    Sep. 08 2019

    PART 1: Find the Mean Squared Error 
        When coefficients of linear model are computed
        Using exact solution B = inv(x' * x) * x' *y 
'''
import numpy as np

#load the data of each file
x = np.loadtxt("../HousingData/X.txt")
y = np.loadtxt("../HousingData/Y.txt")

#row, column numbers of dataframe x
num_rows,_ = np.shape(x)
x_transpose = x.conjugate().transpose()
#Assign beta to be the exact solution formula
#B = inv(x' * x) * x' *y 
B = np.linalg.inv(x_transpose @ x)  @ x_transpose @ y

#RSS = (Y - Y')^2 but since we can't do square, we use transpose multiplication
error = (y - x @ B ).conjugate().transpose() @ (y - x @ B)
MSE = error/num_rows
#Now we can take the root of our MSE since we squared it to avoid erros
root_MSE = MSE **0.5

file_data = '''Betas:\n\t{}
                \nRSS = {}
                \nMSE = {}
                \nROOT_MSE = {}'''.format(B, error, MSE, root_MSE)

with open("Output_MSE.txt","w") as my_file:
    my_file.write(file_data)

