import time
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import math as m 
#the below should be added to download_eep.py
''' add interp 12/23/21'''

def selec_sort(array):
    '''
    selection sort algorithm to sort the EEP files
    '''
    MAX = len(array)
    curr = 0
    while curr < MAX:
        j = 0
        while j < MAX:
            if array[j] < array[curr]:
                temp = array[curr]
                array[curr] = array[j]
                array[j] = temp
                j = j + 1
            else:
                j = j + 1
        curr = curr + 1

    return array

def plt_iso(): 
    '''
    plot a single isochrone curve using the downloaded EEP files from 
    dowload_EEP.py
    '''
    # get directory where files will be operable files will be stored
    valid_cwd = False
    while valid_cwd != True:
        cwd = input("Enter absolute path to directory you want to store untared files: ")
        valid_cwd = os.path.exists(cwd)
        if valid_cwd != True:
            print("Not a valid directory.")

    # get location of downloaded untared files
    valid_eep = False
    while valid_eep != True:
        eep_file = input("Enter absolute path to the downloaded Isochrone files (must be .txz): ")
        valid_eep = os.path.exists(eep_file)
        if valid_eep != True:
            print("Not a valid directory.")
            eep_file = input("Enter absolute path to the downloaded Isochrone files (must be .txz): ")


    #untar the file
    os.system("cd " + cwd)
    os.system("tar -xvf " + eep_file)

    #difference between a tar and untar file is the .txz
    untar_eep_path = eep_file[:-4]

    # Extracting all the contents in the directory corresponding to path
    l_files = os.listdir(untar_eep_path)
    
    main = cwd + untar_eep_path[-44:] + '/' 
    #files are not ordered so perform sorting algorithm: selection sort
    arr_clean = []  
    j = 0
    #gets rid of of 3 docu files
    while j < (len(l_files)):
        if l_files[j] == 'README_tables.pdf' or l_files[j] == 'README_overview.pdf' or l_files[j] == "README_overview.pdf":
            j = j + 1
        else:
            arr_clean.append(l_files[j])
            j = j + 1

    user_dec = 'y'
    while user_dec != 'no':

        #loop through list of files and show user
        print("Select the mass file for the evolutionary track.")
        v_selec = selec_sort(arr_clean)
        sm_file = []
        for file in v_selec: 
            print(file + ' Solar Masses: ' + str(float(file[0:5])/100))
            sm_file.append(float(file[0:5])/100)
        
        file_ints_str = []
        for file in v_selec:
            file_ints_str.append(file[0:5])

        user_mass_input = input("Please enter the first four digits of the associated eep file : ")
        v_inp = False
        while v_inp == False:
            if user_mass_input not in file_ints_str:
                print("Not a valid input")
                user_mass_input = input("Please enter the first four digits of the associated eep file: ")
            else: 
                v_inp = True

        for file in v_selec:
            if file[0:5] == user_mass_input:
                file_selec = file
                print("The file selected is: " + file_selec + ", your input was " + user_mass_input +".")

        data1 = ascii.read(main + file_selec)

        logt1 = np.array(data1['col12'])
        logl1 = np.array(data1['col7'])
        age1 = np.array(data1['col1'])
        min_age = age1[0]
        max_age = age1[len(age1)-1]

        #ask user what age they want iso curve to cover
        user_age_min = float(input("Enter minimum age for isochrone curve (" + str(min_age) + " years - " + str(max_age) + " years): "))
        while user_age_min < min_age:
            print("Not a valid age selection, please select an age greater than" + str(min_age) + " years.")
            user_age_min = float(input("Enter minimum age for isochrone curve (" + str(min_age) + " years - " + str(max_age) + " years): "))

        user_age_max = float(input("Enter maximum age for isochrone curve (" + str(user_age_min) + " years - " + str(max_age) + " years): "))
        while user_age_max > max_age and user_age_max < user_age_min:
            print("Not a valid age selection, please select an age greater than" + str(min_age) + " years.")
            user_age_min = float(input("Enter maximum age for isochrone curve (" + str(user_age_min) + " years - " + str(max_age) + " years): "))

        # gather data that fit user criterion
        loc = np.where((age1>user_age_min)&(age1<user_age_max))

        # plot curve
        i1 = plt.plot(logt1[loc], logl1[loc], color = 'black', linestyle = 'dashed')
        
        # loop question
        user_dec = input("would you like to plot another evolutionary track? Please respond 'yes' or 'no': ")

    # begin interp loop
    interp_dec = input("Would you like to highlight an evolutionary track mass range. Please respond 'yes' or 'no': ")
    while interp_dec != 'no':
        
        # ask for min interp bound
        min_interp_dec = float(input("Please input the minimum eep mass curve you want to highlight (precision is up to 0.05 solar masses) (range is 0.1 - 300 solar masses): "))
        minstr = str(min_interp_dec)
        while min_interp_dec <= 0.1 or min_interp_dec >= 300.00 and (int(minstr[len(minstr)-3:len(minstr)-2]) != 0 or int(minstr[len(minstr)-3:len(minstr)-2]) != 5):
            print("Not a valid input please select a value that is both within the specified range and multiple of 0.05")
            min_interp_dec = float(input("Please input the minimum eep mass curve you want to highlight (precision is up to 0.05 solar masses) (range is 0.1 - 300 solar masses): "))
            minstr = str(min_interp_dec)

        # ask for max interp bound  
        max_interp_dec = float(input("Please input the maximum eep mass curve you want to highlight (precision is up to 0.05 solar masses) (range is " + str(min_interp_dec) + " - 300 solar masses): "))
        maxstr = str(max_interp_dec)
        while max_interp_dec <= min_interp_dec or max_interp_dec >= 300.00 and ((int(maxstr[len(maxstr)-3:len(maxstr)-2]) != 0 or int(maxstr[len(maxstr)-3:len(maxstr)-2]) != 5)):
            print("Not a valid input please select a value that is both within the specified range and multiple of 0.05.")
            max_interp_dec = float(input("Please input the maximum eep mass curve you want to highlight (precision is up to 0.05 solar masses) (range is " + str(min_interp_dec) + " - 300 solar masses): "))
            maxstr = str(max_interp_dec)

        # ask for age boundaries for interp region

    #plot
    title = input("Please input plot title: ")
    plt.title(title, fontsize = 20)
    plt.xlabel('Log(T)')
    plt.ylabel("Log(L)")
    plt.gca().invert_xaxis()
    plt.show()
    return 


plt_iso()

