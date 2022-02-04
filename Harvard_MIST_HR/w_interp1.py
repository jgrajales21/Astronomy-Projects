import os
import math as m 
import numpy as np
import matplotlib.pyplot as plt
from fastnumbers import isfloat
from astropy.io import ascii

# has not been implemeted to fit general case as of now astrre dir hardcoded 

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
# dir hardecoded: /Users/joshuagrajales/Desktop/astrre/MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS
def test(): 
    # Insert the directory path in here
    path = input("Input abs path: ")
    
    # Extracting all the contents in the directory corresponding to path
    l_files = os.listdir(path)
    
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

    
    #loop through list of files and show user
    print("Please select the mass file for the evolutionary track.")
    v_selec = selec_sort(arr_clean)
    sm_file = []
    for file in v_selec: 
        print(file + ' Solar Masses: ' + str(float(file[0:5])/100))
        sm_file.append(float(file[0:5])/100)

    # file intergers in str
    file_ints_str = []
    for file in v_selec:
        file_ints_str.append(file[0:5])

    print(file_ints_str)
    # ensure user selects an existing file
    user_mass_input = input("Please enter the first four digits of the associated eep file : ")
    v_inp = False
    while v_inp == False:
        if user_mass_input not in file_ints_str:
            print("Not a valid input")
            user_mass_input = input("Please enter the first four digits of the associated eep file: ")
        else: 
            v_inp = True

    # tell the user which file the selected 
    for file in v_selec:
        if file[0:5] == user_mass_input:
            print("The file selected is: " + file + ", your input was " + user_mass_input +".")

    print("Input must be of the form ######. For example if you wish to input a 255.05 solar mass star then enter 25505. Likewise if you choose to enter a 1.10 solar mass star enter 00110.")
    # ask for LOW interp bound; this gives us the minimum mass we want to interpolate to 
    min_interp_dec = input("Please input the MINIMUM eep mass curve you want to highlight: ")
    while isfloat(min_interp_dec) != True or min_interp_dec < '00010' or min_interp_dec > '30000' or int(min_interp_dec[len(min_interp_dec)-1:])% 5 != 0 or len(min_interp_dec) >= 6 or len(min_interp_dec) < 5:
        print("Not a valid input please select a value that is both within the specified range.")
        min_interp_dec = input("Please input the MINIMUM eep mass curve you want to highlight (range is 00010 - 30000 solar masses): ")
       
    # if LOW interp is in the array of files then no need to interpolate just use existing data
    if min_interp_dec in file_ints_str:
        for file in v_selec:
            if file[0:5] == min_interp_dec:
                print("Min-Low file selected is: " + file + ", your input was " + min_interp_dec +".")
                break
        dataminlow = ascii.read('/Users/joshuagrajales/Desktop/astrre/MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS/' + file)

        logt1 = np.array(dataminlow['col12'])
        logl1 = np.array(dataminlow['col7'])
        age1 = np.array(dataminlow['col1'])
        min_age_minlow = age1[0]
        max_age_minlow = age1[len(age1)-1]

        user_age_min_i = float(input("Enter minimum age for lower bound of highlighted region (" + str(min_age_minlow) + " years - " + str(max_age_minlow) + " years): "))
        while user_age_min_i < min_age_minlow:
            print("Not a valid age selection, please select an age greater than" + str(min_age_minlow) + " years.")
            user_age_min_i = float(input("Enter minimum age for lower bound of highlighted region (" + str(min_age_minlow) + " years - " + str(max_age_minlow) + " years): "))

        user_age_max_i = float(input("Enter maximum age for lower bound of highlighted region (" + str(user_age_min_i) + " years - " + str(max_age_minlow) + " years): "))
        while user_age_max_i > max_age_minlow and user_age_max_i < user_age_min_i:
            print("Not a valid age selection, please select an age greater than" + str(min_age_minlow) + " years.")
            user_age_min_i = float(input("Enter maximum age for lower bound of highlighted region (" + str(user_age_min_i) + " years - " + str(max_age_minlow) + " years): "))
    
        locminlow = np.where((age1>user_age_min_i)&(age1<user_age_max_i))
        low_temp_arr = logt1[locminlow]
        low_lum_arr = logl1[locminlow]
         

    # low interp bound not an existing file so interpolate
    elif min_interp_dec not in file_ints_str:

        # find what existing files the min interp bound is between
        i = len(file_ints_str)-1
        while i >= 0 and file_ints_str[i] < min_interp_dec:
            i = i - 1
            
        min_max = file_ints_str[i]
        min_min = file_ints_str[i+1]
        
        # get the full name of the file that corresponds to min_min for low interp bound
        for file in v_selec:
            if file[0:5] == min_min:
                print("Min-Low file selected is: " + file + ", your input was " + min_interp_dec +".")
                break

        dataminlow = ascii.read('/Users/joshuagrajales/Desktop/astrre/MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS/' + file)

        logt1 = np.array(dataminlow['col12'])
        logl1 = np.array(dataminlow['col7'])
        age1 = np.array(dataminlow['col1'])
        min_age_minlow = age1[0]
        max_age_minlow = age1[len(age1)-1]

        # ask user what age they want interp curves to cover (note: the age range given for LOW INTERP will be the same as the one assigned for the HIGH INTERP range; we 
        # will then reduce the longer of the two arrays by array slicing until they are the same size)
        user_age_min_i = float(input("Enter minimum age for lower bound of highlighted region (" + str(min_age_minlow) + " years - " + str(max_age_minlow) + " years): "))
        while user_age_min_i < min_age_minlow and isfloat(user_age_min_i) == False:
            print("Not a valid age selection, please select an age greater than" + str(min_age_minlow) + " years.")
            user_age_min_i = float(input("Enter minimum age for lower bound of highlighted region (" + str(min_age_minlow) + " years - " + str(max_age_minlow) + " years): "))

        user_age_max_i = float(input("Enter maximum age for lower bound of highlighted region (" + str(user_age_min_i) + " years - " + str(max_age_minlow) + " years): "))
        while user_age_max_i > max_age_minlow and user_age_max_i < user_age_min_i and isfloat(user_age_max_i) == False:
            print("Not a valid age selection, please select an age greater than" + str(min_age_minlow) + " years.")
            user_age_min_i = float(input("Enter maximum age for lower bound of highlighted region (" + str(user_age_min_i) + " years - " + str(max_age_minlow) + " years): "))
        
        # gather data for minlow arrays; this restricts the range of values we are considering to the age range given by the user
        locminlow = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum array for minlow with range restrictions as given by user
        temp_minlow = logt1[locminlow]
        lum_minlow = logl1[locminlow]

        # This completes accessing the minimum low data points. We now need the minimum high values to then interpolate between both sets
        # of data. The below accomplishes the second portion of the interpolation routine for the LOW boundary.   

        # find the corresponding maximum low file as determined by min_interp_dec
        for file in v_selec:
            if file[0:5] == min_max:
                print("Max-low file selected is: " + file + ", your input was " + min_interp_dec +".")
                break

        print(file)
        datamaxlow = ascii.read('/Users/joshuagrajales/Desktop/astrre/MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS/' + file)

        logt1 = np.array(datamaxlow['col12'])
        logl1 = np.array(datamaxlow['col7'])
        age1 = np.array(datamaxlow['col1'])

        # gather data for maxlow arrays
        locmaxlow = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum for maxlow
        temp_maxlow = logt1[locmaxlow]
        lum_maxlow = logl1[locmaxlow]
        #check that there is some popping occuring 

        # ensure minlow and maxlow have arrays of the same size for all dimensions
        
        while len(temp_minlow) != len(temp_maxlow):
            if len(temp_maxlow) > len(temp_minlow):
                temp_maxlow = temp_maxlow[1:]
            else: 
                temp_minlow = temp_minlow[1:]

        while len(lum_minlow) != len(lum_maxlow):
            if len(lum_maxlow) > len(lum_minlow):
                lum_maxlow = lum_maxlow[1:]
            else:
                lum_minlow = lum_minlow[1:]

        print(242)
        # consider what hapens in the situation where this yields a decimal for tot steps -- int rounds down.
        # tot_steps tells us the number of steps of 0.05 we take to reach max_min from min_min 
        print(float(min_max)/100)
        print(float(min_min)/100)
        print(int(m.ceil((float(min_max)/100 - float(min_min)/100)*20)))
        tot_steps = int(m.ceil((float(min_max)/100 - float(min_min)/100)*20))
        float_user_dec_min = float(min_interp_dec)/100
        start = float(min_min)/100

        # arrays are now the same size so they are ready for interpolation. We add 0.05 to min_min until we reach min_interp_dec
        # (or the next best thing closest to it). 
        # Recall min_min and min_max are the largest mass file less than min_interp_dec and smallest mass file larger than min_interp_dec
        # respectively. Thus the below determines how many steps of 0.05 we need to take (from min_min) to get as close as possible
        # to the min_interp_dec. In doing so we know which index to consider when we perform interpolation for each ith index (see
        # next while loop with k < len(temp_maxlow) condition).
        i = 1 
        original = start
        while original != float_user_dec_min and original <= float_user_dec_min:
            original = start + 0.05*i
            i = i + 1
        #################################### MAKE SURE ABOVE LOOP WORKS


        print(252)
        # 'i' keeps track of how many steps we have to take from the base case (min_min) to get to the user input min_interp_dec.
        # The two while loops below complete the interpolation routine for the user input lower bound of the highlighted region, they 
        # do so by using linspace as a mock interpolation routine. The linspace is used to evenly divide the difference
        # of the ith index of the temp_minlow and temp_maxlow arrays. 
        print(str(tot_steps) + 'tot steps')
        print(i-1)
        i = i - 1
        k = 0
        low_temp_arr = []
        while k < len(temp_maxlow):
            x = np.linspace(temp_minlow[k], temp_maxlow[k], tot_steps+2)
            low_temp_arr.append(x[i])
            k  = k + 1

        y = 0
        low_lum_arr = []
        while y < len(temp_maxlow):
            x = np.linspace(lum_minlow[y], lum_maxlow[y], tot_steps+2)
            low_lum_arr.append(x[i])
            y = y + 1

    # ask for HIGH interp bound; this gives us the maximum mass we want to interpolate to 
    max_interp_dec = input("Please input the MAXIMUM eep mass curve you want to highlight: ")
    z = False
    while z != True:
        if max_interp_dec in file_ints_str:
            z = True
        elif isfloat(max_interp_dec) != True or max_interp_dec < min_interp_dec or max_interp_dec > '30000' or int(max_interp_dec[len(max_interp_dec)-1:])%5 != 0 or len(max_interp_dec) >= 6 or len(max_interp_dec) < 5:
        #while isfloat(max_interp_dec) != True or max_interp_dec < min_interp_dec or max_interp_dec > '30000' or int(max_interp_dec[len(max_interp_dec)-1:])%5 != 0 or len(max_interp_dec) >= 6 or len(max_interp_dec) < 5:
            print("Not a valid input please select a value that is both within the specified range.")
            max_interp_dec = input("Please input the MAXIMUM eep mass curve you want to highlight (range is " + str(min_interp_dec) + " - 30000 solar masses): ")
            z = False
        else:
            z = True
    ################################################### Begin Interp Routine ########################################################


    #begin interp routine for HIGH 

    # if High interp is in the array of files then no need to interpolate just use existing data
    if max_interp_dec in file_ints_str:
        for file in v_selec:
            if file[0:5] == max_interp_dec:
                print("Min-high file selected is: " + file + ", your input was " + max_interp_dec +".")
                break

        dataminhigh = ascii.read('/Users/joshuagrajales/Desktop/astrre/MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS/' + file)

        logt1 = np.array(dataminhigh['col12'])
        logl1 = np.array(dataminhigh['col7'])
        age1 = np.array(dataminhigh['col1'])
    
        # gather data for minhigh arrays. Note the age used is the same as given for the low interp.
        locminhigh = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum array for high interp
        high_temp_arr = logt1[locminhigh]
        high_lum_arr = logl1[locminhigh]


    elif max_interp_dec not in file_ints_str:

        # FOR HIGH INTERP: find the solar mass files the min interp is inbetween
        i = len(file_ints_str)-1
        while i >= 0 and file_ints_str[i] < max_interp_dec:
            i = i - 1
            
        max_max = file_ints_str[i]
        max_min = file_ints_str[i+1]
    
        # isolate min file for HIGH INTERP
        for file in v_selec:
            if file[0:5] == max_min:
                print("Min-high file selected is: " + file + ", your input was " + max_interp_dec +".")
                break

        dataminhigh = ascii.read('/Users/joshuagrajales/Desktop/astrre/MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS/' + file)

        logt1 = np.array(dataminhigh['col12'])
        logl1 = np.array(dataminhigh['col7'])
        age1 = np.array(dataminhigh['col1'])
    
        # gather data for minhigh arrays
        locminhigh = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum array for minhigh
        temp_minhigh = logt1[locminhigh]
        lum_minhigh = logl1[locminhigh]
        print(301)
        # This completes accessing the minimum high data points. We now need the maximum high values to then interpolate 
        # both sets of data. The below accomplishes the second portion of the interpolation routine for the HIGH boundary.

        # find the corresponding maximum high file as determined by max_interp_dec
        for file in v_selec:
            if file[0:5] == max_max:
                print("Max-high file selected is: " + file + ", yourr input was " + max_interp_dec +".")
                break

        print(306)
        print(file)
        datamaxhigh = ascii.read('/Users/joshuagrajales/Desktop/astrre/MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS/' + file)

        logt1 = np.array(datamaxhigh['col12'])
        logl1 = np.array(datamaxhigh['col7'])
        age1 = np.array(datamaxhigh['col1'])

        # gather data for maxhigh arrays
        locmaxhigh = np.where((age1>user_age_min_i)&(age1<user_age_max_i))

        # temp and lum for maxlow
        temp_maxhigh = logt1[locmaxhigh]
        lum_maxhigh = logl1[locmaxhigh]
        print(319)

        # ensure minhigh and maxhigh have arrays of the same size for all dimensions
        while len(temp_minhigh) != len(temp_maxhigh):
            if len(temp_maxhigh) > len(temp_minhigh):
                temp_maxhigh = temp_maxhigh[1:]
            else: 
                temp_minhigh = temp_minhigh[1:]
        print(327)
        while len(lum_minhigh) != len(lum_maxhigh):
            if len(lum_maxhigh) > len(lum_minhigh):
                lum_maxhigh = lum_maxhigh[1:]
            else:
                lum_minhigh = lum_minhigh[1:]

        print(335)
        tot_steps = int((float(max_max)/100 - float(max_min)/100)*20)
        float_user_dec_max = float(max_interp_dec)/100
        start = float(max_min)/100

        i = 1 
        print("star "+str(start))
        original = start
        while original != float_user_dec_max and original <= float(max_max)/100:
            original = start + 0.05*i
            i = i + 1
        print(351)
        i = i - 1
        k = 0
        high_temp_arr = []
        while k < len(temp_maxhigh):
            x = np.linspace(temp_minhigh[k], temp_maxhigh[k], tot_steps+2)
            high_temp_arr.append(x[i])
            k  = k + 1
        print(359)
        y = 0
        high_lum_arr = []
        while y < len(temp_maxhigh):
            x = np.linspace(lum_minhigh[y], lum_maxhigh[y], tot_steps+2)
            high_lum_arr.append(x[i])
            y = y + 1
        print(366)
    # ensure all arrays are of the same size
    while len(high_temp_arr) != len(low_temp_arr):
        if len(high_temp_arr) > len(low_temp_arr):
            high_temp_arr = high_temp_arr[1:]
        else: 
            low_temp_arr = low_temp_arr[1:]

    while len(high_lum_arr) != len(low_lum_arr):
        if len(high_lum_arr) > len(low_lum_arr):
            high_lum_arr = high_lum_arr[1:]
        else:
            low_lum_arr = low_lum_arr[1:]
    '''
    print(type(high_lum_arr))
    print(type(high_temp_arr))
    print(type(low_lum_arr))
    print(type(low_temp_arr))
    print(low_temp_arr)
    print(np.array(low_temp_arr))
    '''


    x1 = low_temp_arr
    y1 =  low_lum_arr
    x2 = high_temp_arr
    y2 = high_lum_arr


    plt.plot(x1, y1, 'o')
    plt.plot(x2, y2, 'x')

    plt.fill(np.append(x1, x2[::-1]), np.append(y1, y2[::-1]))
    '''
    print(len(high_lum_arr))
    fig, (ax, ax1, ax2) = plt.subplots(3,1)
    ax.plot(low_temp_arr,low_lum_arr, color = 'black')
    #ax.title(str(min_interp_dec))
    ax.invert_xaxis()
    ax1.plot(high_temp_arr, high_lum_arr, color = 'black')
    #ax1.title(str(max_interp_dec))
    ax1.invert_xaxis()
    ax2.fill_between(high_temp_arr, low_lum_arr, high_lum_arr, where = np.array(low_lum_arr) <= np.array(high_lum_arr), color = 'C0', alpha = 0.3)
    ax2.plot(low_temp_arr,low_lum_arr, color = 'black')
    ax2.plot(low_temp_arr,high_lum_arr, color = 'black')
    '''
    plt.gca().invert_xaxis()
    plt.show()

    # current issue is that i am using temperature array from low interp bound for both low and high lum;
    # in doing so the shape of the curves is altered

    return 
    
test()


