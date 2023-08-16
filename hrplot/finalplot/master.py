
from files.evolutionary_track import plot_eep 
from fastnumbers import isint, isfloat
import matplotlib.pyplot as plt
import numpy as np 
import os


# /Users/joshuagrajales/Downloads/MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS.txz
# /Users/joshuagrajales/Desktop/astrre/final_plot
def run():

    # colors for the data points plotted in the hr-diagram 
    c = ['blue', 'purple', 'green', 'red', 'brown'] # preset colors for data points in the hr diagram 
    i = 0 # used to index colors in the c array above
    j = 0 # used to demarcate different line styles in the event that multilple pairs of evolutionary tracks are plotted 

    # display the menu options
    print("1. Input data for evolutionary track curves ")
    print("2. Plot all")

    # intialize the decision 
    decision = input("Enter a digit with the task associated above. ")
    while True:
        # check if is not integer or if is not in range of valid choices 
        if isint(decision) != True or int(decision) > 6 or int(decision) < 1:
            print("Not a valid input.")
        # subset evolutionary tracks 
        elif int(decision) == 1:
            plot_eep(j)
            j+=1
        # add data points to hr diagram and plot tracks
        elif int(decision) == 2:
            point = input("Would you like to plot a point? (yes or no) ")
            while point == 'yes':

                # ask for x point 
                x_point = input("Please provide the effective temperature in Kelvin: Log(T_eff) =  ")
                # check that the input is an int or float
                while isint(x_point) == False and isfloat(x_point) == False:
                    x_point = input("Invalid input. Please provide the effective temperature in Kelvin: Log(T_eff) =  ")
                x_point = [float(x_point)]
                # check that the input is an int or float
                x_point_err = input("Please provide the error for effective temperature in Kelvin: Log(T_eff) =  ")
                while isint(x_point_err) == False and isfloat(x_point_err) == False:
                    x_point_err = input("Invalid input. Please provide the effective temperature in Kelvin: Log(T_eff) =  ")
                x_point_err = [float(x_point_err)]

                # ask for y point 
                y_point = input("Please provide the bolometric luminosity of the star in: Log(L) = ")
                while isint(y_point) == False and isfloat(y_point) == False:
                    y_point = input("Invalid input. Please provide the effective temperature in Kelvin: Log(T_eff) =  ")
                y_point = [float(y_point)]
                y_point_err = input("Please provide the error for bolometric luminsity in Log(L) =  ")
                while isint(y_point_err) == False and isfloat(y_point_err) == False:
                    y_point_err = input("Invalid input. Please provide the error for bolometric luminsity in Log(L) =  ")
                y_point_err = [float(y_point_err)]

                # name for graph 
                co = c[i]
                i += 1
                name = input("Please provide a name for this point: ")
                plt.scatter(x_point, y_point, color = co)
                plt.xticks(fontsize=10)
                plt.yticks(fontsize=10)
                plt.errorbar(x_point, y_point, yerr= y_point_err, xerr=x_point_err, label = name, color = co, fmt='o')
                point = input("Would you like to plot another point? (yes or no): ")
            
            title = input("Please input the title to the graph: ")
            plt.title(title, fontsize = 20)
            plt.xlabel(r'log($T_{eff}$)', fontsize = 20)
            plt.ylabel(r'log($L_{\odot}$)', fontsize = 20)
            plt.legend()
            plt.gca().invert_xaxis()
            plt.grid()
            plt.show()
            return 
        
        # display the menu 
        print("1. Input data for evolutionary track curves ")
        print("2. Plot all")
        decision = input("Enter a digit with the task associated above. ") 

run()



