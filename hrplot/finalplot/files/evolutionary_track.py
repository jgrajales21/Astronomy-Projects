import os
import math as m 
import numpy as np
import matplotlib.pyplot as plt
from fastnumbers import isfloat
from astropy.io import ascii
    
def plot_eep(i): 
        
    ls = ['dashed', 'dotted','dashdot']
    path = input("Input name of untarred evolutionary track file: ")

    # Extracting all the contents in the directory corresponding to path
    l_files = os.listdir(path)
    
    arr_clean = []  
    j = 0
    # gets rid of of 3 doc files
    while j < (len(l_files)):
        if l_files[j] == 'README_tables.pdf' or l_files[j] == 'README_overview.pdf' or l_files[j] == "README_overview.pdf":
            j = j + 1
        else:
            arr_clean.append(l_files[j])
            j = j + 1

    # sort the mass files in increasing order and show user
    # Each file is named according to the star mass its data corresponds to. The following makes an array composed of only 
    # the mass digits associated with each file -- this is needed to determine which file the user wants to interact with  
    v_selec = sorted(arr_clean)
    file_ints_str = []
    for file in v_selec: 
        print(file + ' Solar Masses: ' + str(float(file[0:5])/100))
        file_ints_str.append(file[0:5])

    print()
    print("INSTRUCTIONS: Input must be of the form #####. For example if you wish to input a 255.05 solar mass star then enter 25505. Likewise if you choose to enter a 1.10 solar mass star enter 00110.")
    print()

    # ask for LOW interp bound; this gives us the minimum mass we want to graph (and posssibly interpolate for)
    min_interp_dec = input("Please input the MINIMUM eep mass curve you want to highlight: ")
    print("Check that the below can be used as inputs for the following print")
    print("MIN MASS", min(file_ints_str))
    print("MAX MASS", max(file_ints_str))

    while isfloat(min_interp_dec) != True or min_interp_dec < '00010' or min_interp_dec > '30000' or len(min_interp_dec) >= 6 or len(min_interp_dec) < 5:
        min_interp_dec = input("Not a valid input. Please input the MINIMUM eep mass curve you want to highlight (range is 00010 - 30000 solar masses): ")
       
    # if min_interp_dec is in the array of files then no need to interpolate just use existing data
    if min_interp_dec in file_ints_str:
        print("No interpolation needed for specified mass file.")
        print("Min-low file: "+min_interp_dec+"M.track.eep")
        dataminlow = ascii.read(path+'/'+min_interp_dec+"M.track.eep")

        logt1 = np.array(dataminlow['col12']) # temps for lower bound evolutionary track
        logl1 = np.array(dataminlow['col7']) # lums for lower bound evolutionary track 
        age1 = np.array(dataminlow['col1']) # age for lower bound evolutionary track 
        min_age_minlow = age1[0] # minimum age in lower bound evolutionary track (think of this as the starting age for the evo track)
        max_age_minlow = age1[len(age1)-1] # maximum age in lower bound evolutionary track (think of this as the final age for the evo track)

        # now that we have the file that corresponds to the queried mass, we need to subset this data based on the user-provided age ranges
        # we get the age bounds below 
        user_age_min_i = float(input("Enter minimum age for lower bound of highlighted region (" + str(min_age_minlow) + " years - " + str(max_age_minlow) + " years): "))
        while user_age_min_i < float(min_age_minlow) or isfloat(user_age_min_i) == False:
            user_age_min_i = float(input("Not a valid age selection. Enter minimum age for lower bound of highlighted region (" + str(min_age_minlow) + " years - " + str(max_age_minlow) + " years): "))

        user_age_max_i = float(input("Enter maximum age for lower bound of highlighted region (" + str(user_age_min_i) + " years - " + str(max_age_minlow) + " years): "))
        while user_age_max_i > max_age_minlow or user_age_max_i < user_age_min_i or isfloat(user_age_max_i) == False:
            user_age_max_i = float(input("Not a valid age selection. Enter maximum age for lower bound of highlighted region (" + str(user_age_min_i) + " years - " + str(max_age_minlow) + " years): "))
    
        # subset the data according to the age ranges; make the boolean array 
        locminlow = np.where((age1>user_age_min_i)&(age1<user_age_max_i))
        low_temp_arr = logt1[locminlow] # subset the temps 
        low_lum_arr = logl1[locminlow]  # subset the lums
         

    # min_interp_dec not an existing file so we need to interpolate the data points for the user queired mass
    elif min_interp_dec not in file_ints_str:
        print()
        print('Mass selected has no existing data file. Begin interpolation routine for low-bound curve.')
        print()

        # find what existing files the min interp bound is between, we loop over all of the mass files (i.e the pre-existing mass files from the MESA database)
        # we do this by finding the maximum mass file that is less than the user specified mass (min_min)
        # AND the minimum mass file that is greater than the user specified mass (min_max)
        i = 0
        while i < len(file_ints_str) and file_ints_str[i] < min_interp_dec:
            i = i + 1
            
        min_max = file_ints_str[i]
        min_min = file_ints_str[i-1]
        
        print("Min-Low file selected is: " + min_min + "M.track.eep, your input was " + min_interp_dec +".")

        dataminlow = ascii.read(path+'/'+min_min+"M.track.eep")

        # load the min_min data 
        logt1 = np.array(dataminlow['col12'])
        logl1 = np.array(dataminlow['col7'])
        age1 = np.array(dataminlow['col1'])
        min_age_minlow = age1[0]
        max_age_minlow = age1[len(age1)-1]

        # ask user what age they want interp curves to cover (note: the age range given for LOW INTERP will be the same as the one assigned for the HIGH INTERP range; 
        # we do this because we want to maximize the number of data points availble in each evolutionary track, as we know stars with larger mass have shorter lifetimes
        # than stars with lower mass so we use the age bounds for the lower bound (corresponding to lower mass star data))
        user_age_min_i = float(input("Enter minimum age for lower bound of highlighted region (" + str(min_age_minlow) + " years - " + str(max_age_minlow) + " years): "))
        while user_age_min_i < min_age_minlow or isfloat(user_age_min_i) == False:
            user_age_min_i = float(input("Not a valid age selection. Enter minimum age for lower bound of highlighted region (" + str(min_age_minlow) + " years - " + str(max_age_minlow) + " years): "))

        user_age_max_i = float(input("Enter maximum age for lower bound of highlighted region (" + str(user_age_min_i) + " years - " + str(max_age_minlow) + " years): "))
        while user_age_max_i > max_age_minlow or user_age_max_i < user_age_min_i or isfloat(user_age_max_i) == False:
            user_age_max_i = float(input("Not a valid age selection. Enter maximum age for lower bound of highlighted region (" + str(user_age_min_i) + " years - " + str(max_age_minlow) + " years): "))
        
        # gather data for minlow arrays; this restricts the range of values we are considering to the age range given by the user
        locminlow = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum array for minlow with range restrictions as given by user
        temp_minlow = logt1[locminlow]
        lum_minlow = logl1[locminlow]

        #  This completes accessing the minimum interp data points for low bound. We now need the minimum high values to then interpolate between 
        #  both sets of data.
        #  The below accomplishes the second portion of the interpolation routine for the MAX LOW boundary.
               
        print("Max-low file selected is: " + min_max + "M.track.eep, your input was " + min_interp_dec +".")

        datamaxlow = ascii.read(path+'/'+min_max + "M.track.eep")

        logt1 = np.array(datamaxlow['col12'])
        logl1 = np.array(datamaxlow['col7'])
        age1 = np.array(datamaxlow['col1'])

        # gather data for maxlow arrays; recall we use the same age as that given for the min_low array
        locmaxlow = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum for maxlow
        temp_maxlow = logt1[locmaxlow]
        lum_maxlow = logl1[locmaxlow]

        # slice arrays so that they have the same size; we need to do this so that there is a one to one interpolation 
        # betwen points in the array          
        # we will truncate only the larger of the two arrays

        # begin by determining which of the two is larger
        if len(temp_minlow) > len(temp_minhigh):
            temp_minlow = temp_minlow[:-abs(len(temp_minlow)-len(temp_maxlow))]
        elif len(temp_minlow) < len(temp_minhigh):
            temp_maxlow = temp_maxlow[:-abs(len(temp_minlow)-len(temp_maxlow))]

        if len(lum_minlow) > len(lum_maxlow):
            lum_minlow = lum_minlow[:-abs(len(lum_minlow)-len(lum_maxlow))]
        elif len(lum_minlow) < len(lum_maxlow):
            lum_maxlow = lum_maxlow[:-abs(len(lum_minlow)-len(lum_maxlow))]

 
        tot_steps = int(m.ceil((float(min_max)/100 - float(min_min)/100)/0.01))
        float_user_dec_min = float(min_interp_dec)/100 # the mass we need to interpolate to 
        start = float(min_min)/100 # the mass we are starting from 

        # arrays are now the same size so they are ready for interpolation. 

        # we want to linearly interpolate with steps of 0.01. In this case, the steps of 0.01 correspond to increments in (solar) mass
        nsteps = (float_user_dec_min - min_min)/0.01 
        
       # we have temp and lum arrays of the same length for stars of different mass. Truncating the arrays to the same length is our way of 'forcing'
       # data points to correspond to the same age. B/c each index corresponds to a temp and lum measurement of a given age (for diff star of diff mass), 
       # we interpolate in between each pair of temp and lum data points nsteps, to the mass specified by the user e
        k = 0
        low_temp_arr = []
        while k < len(temp_maxlow):
            x = np.linspace(temp_minlow[k], temp_maxlow[k], tot_steps+2)
            low_temp_arr.append(x[nsteps])
            k  = k + 1

        y = 0
        low_lum_arr = []
        while y < len(temp_maxlow):
            x = np.linspace(lum_minlow[y], lum_maxlow[y], tot_steps+2)
            low_lum_arr.append(x[nsteps])
            y = y + 1

    # ask for HIGH interp bound; this gives us the maximum mass we want to interpolate to 
    max_interp_dec = input("Please input the MAXIMUM eep mass curve you want to highlight: ")
    while isfloat(max_interp_dec) != True or max_interp_dec < min_interp_dec or len(max_interp_dec) >= 6 or len(max_interp_dec) < 5:
        max_interp_dec = input("Not a valid input. Please input the MAXIMUM eep mass curve you want to highlight (range is "+str(min_interp_dec)+" - 30000 solar masses): ")
     

    # if High interp is in the array of files then no need to interpolate just use existing data
    if max_interp_dec in file_ints_str:
        
        print("Min-high file selected is: " + max_interp_dec + "M.track.eep, your input was " + max_interp_dec +".")

        dataminhigh = ascii.read(path+'/' + max_interp_dec+"M.track.eep")

        logt1 = np.array(dataminhigh['col12'])
        logl1 = np.array(dataminhigh['col7'])
        age1 = np.array(dataminhigh['col1'])
    
        # gather data for minhigh arrays. Note the age used is the same as given for the low interp.
        locminhigh = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum array for high interp
        high_temp_arr = logt1[locminhigh]
        high_lum_arr = logl1[locminhigh]


    elif max_interp_dec not in file_ints_str:
        print()
        print('Mass selected has no existing data file. Begin interpolation routine for high-bound curve.')
        print()

        # FOR HIGH INTERP: find the solar mass files the min interp is inbetween
        i = 0
        while i < len(file_ints_str) and file_ints_str[i] < max_interp_dec:
            i = i + 1
            
        max_max = file_ints_str[i]
        max_min = file_ints_str[i-1]
    
        # isolate min file for HIGH INTERP
        print("Min-high file selected is: " + max_min + "M.track.eep, your input was " + max_interp_dec +".")

        dataminhigh = ascii.read(path+'/' + max_min+"M.track.eep")

        logt1 = np.array(dataminhigh['col12'])
        logl1 = np.array(dataminhigh['col7'])
        age1 = np.array(dataminhigh['col1'])
    
        # gather data for minhigh arrays
        locminhigh = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum array for minhigh
        temp_minhigh = logt1[locminhigh]
        lum_minhigh = logl1[locminhigh]

        # This completes accessing the minimum high data points. We now need the maximum high values to then interpolate 
        # both sets of data. The below accomplishes the second portion of the interpolation routine for the HIGH boundary.

        print("Max-high file selected is: " + max_max + "M.track.eep, yourr input was " + max_interp_dec +".")

        datamaxhigh = ascii.read(path+'/' + max_max+"M.track.eep")

        logt1 = np.array(datamaxhigh['col12'])
        logl1 = np.array(datamaxhigh['col7'])
        age1 = np.array(datamaxhigh['col1'])

        # gather data for maxhigh arrays
        locmaxhigh = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum for maxlow
        temp_maxhigh = logt1[locmaxhigh]
        lum_maxhigh = logl1[locmaxhigh]

        # ensure minhigh and maxhigh have arrays of the same size for all dimensions
        if len(temp_minhigh) > len(temp_maxhigh):
            temp_minhigh = temp_minhigh[:-abs(len(temp_minhigh)-len(temp_maxhigh))]
        elif len(temp_minhigh) < len(temp_maxhigh):
            temp_maxhigh = temp_maxhigh[:-abs(len(temp_minhigh)-len(temp_maxhigh))]

        if len(lum_minhigh) > len(lum_maxhigh):
            lum_minhigh = lum_minhigh[:-abs(len(lum_minhigh)-len(lum_maxhigh))]
        elif len(lum_minhigh) < len(lum_maxhigh):
            lum_maxhigh = lum_maxhigh[:-abs(len(lum_minhigh)-len(lum_maxhigh))]
        
        tot_steps = int((float(max_max)/100 - float(max_min)/100)/0.01)
        float_user_dec_max = float(max_interp_dec)/100
        start = float(max_min)/100

        nsteps = (float_user_dec_max-start)/0.01
        
        k = 0
        high_temp_arr = []
        while k < len(temp_maxhigh):
            x = np.linspace(temp_minhigh[k], temp_maxhigh[k], tot_steps+2)
            high_temp_arr.append(x[nsteps])
            k  = k + 1

        y = 0
        high_lum_arr = []
        while y < len(temp_maxhigh):
            x = np.linspace(lum_minhigh[y], lum_maxhigh[y], tot_steps+2)
            high_lum_arr.append(x[nsteps])
            y = y + 1


    x1 = low_temp_arr
    y1 = low_lum_arr
    x2 = high_temp_arr
    y2 = high_lum_arr

    print([len(x1),len(x2),len(y1),len(y2)])
    plt.plot(x1, y1, 'x', label = input("Input label for lower bound: "))
    plt.plot(x2, y2, 'x', label = input("Input label for upper bound: "))

    fill_dec = input("Would you light to highlight the region between these curves? (yes or no) ")
    if fill_dec == 'yes':
        plt.fill(np.append(x1, x2[::-1]), np.append(y1, y2[::-1]), color='black', linestyle=ls[i])
        
        
    return 
    

