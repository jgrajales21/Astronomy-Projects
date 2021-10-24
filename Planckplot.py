import matplotlib.pyplot as plt
import numpy as np
 
h = 6.626e-34 #m**2 * kg / s
c = 3.0e+8    #m / s
k = 1.38e-23  # m**2 kg / s**2 * K

def planck(wav, T):
    left = 2*h*c**2 / (wav **5)
    right = np.exp(h*c/(wav*k*T)) - 1
    intensity = left/ right
    
    return intensity

#numbers a through b evencly spaced by c
#wavelengths = np.arange(1e-6, 1000*1e-6, 1e-6) #i have no idea how to use this
log_wavelengths = np.arange(-6,-3,.01)
                           
out300 = planck(10**log_wavelengths, 300)
out1000 = planck(10**log_wavelengths, 1000)
out1500 = planck(10**log_wavelengths, 1500)
#so range is from micrometeres to millimeters 

plt.loglog(10**log_wavelengths*1e6 , out300, 'k-')
plt.loglog(10**log_wavelengths*1e6 , out1000, 'r-')
plt.loglog(10**log_wavelengths*1e6 , out1500, 'b-')

plt.xlabel(r'wavlength: ($\lambda$ nm) ')
plt.ylabel(r'I$_\lambda$ ($\lambda$,T)')

#latex --r'$\name of greek letter$'   underscore subscript and supperscore carot 
