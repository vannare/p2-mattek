from scipy.signal import boxcar
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftshift

def windowplot(window, windowlength):
    """
    Parameters
    ----------
    window : chosen window function. Possible options is 'hanning', 'rectangular' or 'hamming'
        TYPE OF INPUT: string
        DESCRIPTION: Plot of chosen window function in time domain and in frequency domain
    length : 
        TYPE: int
        DESCRIPTION: Length M-1, of time window 

    """
    if window == 'hanning':
        window = window.capitalize()
        timewindow=np.hanning(windowlength)
    elif window=='hamming':
        window = window.capitalize()
        timewindow=np.hamming(windowlength)
    elif window== 'rectangular':
        window = window.capitalize()
        timewindow=boxcar(windowlength)
    
    textsize = 14
    
    
    plt.figure()
    plt.plot(timewindow)
    plt.title(f"{window} window in time domain",fontsize=textsize)
    plt.ylabel("Amplitude",fontsize=textsize)
    plt.xlabel("Sample",fontsize=textsize)
    plt.savefig(f'{window}Time.pdf')
    

    A = fft(timewindow, 2048) / (windowlength/2)
    mag = np.abs(fftshift(A))
    #freq = np.linspace(-3,3, len(A)) # Værdierne på denne er der tvivl om.
    response = 20 * np.log10(mag)
    response = np.clip(response, -100, 100)
    
    plt.figure()
    plt.plot(response)
    plt.title(f"Frequency response of {window} window",fontsize=textsize)
    plt.ylabel("Magnitude [dB]",fontsize=textsize)
    plt.xlabel("Normalized frequency [cycles per sample]",fontsize=textsize)
    plt.savefig(f'{window}Fourier.pdf')

# for i in [window[0]]:
#       windowplot(i,21)

# 1 Hz
def f1(t):
    return np.sin(2*np.pi*t)

#5 Hz
def f2(t):
    return np.sin(5*2*np.pi*t)



def recwindow(timeStart,timeEnd, windowStart, windowlength):
    time=np.linspace(timeStart,timeEnd,20001)
    timewindow=[]
    for i in time:
        if windowStart<=i<=windowStart+windowlength:
            timewindow.append(1)
        else:
            timewindow.append(0)
    return timewindow

t = np.linspace(0,20,20001)
def overlapplot (amount, overlap, windowStart, windowLength):
    """
    Note: Overlap angive i decimaltal: 0,50 = 50%. 
    Dog skal overlap stadig kunne være af typen int.
    """
    overlap=int(windowLength*overlap)
    f1end=8000
    f2start=8000
    #Whole signal
    fig, axs = plt.subplots(amount+1, sharex=True,sharey=True,figsize=(10,6))
    axs[0].plot(t[:f1end],f1(t[:f1end]),'b')
    axs[0].plot(t[f2start:],f2(t[f2start:]),'b')
    for i in range(0,amount):    
       axs[i+1].plot(t[windowStart*1000:min(f1end,(windowStart+windowLength)*1000)],f1(t[windowStart*1000:min(f1end,(windowStart+windowLength)*1000)]),'b')
       axs[i+1].plot(t[max(f2start,windowStart*1000):(windowStart+windowLength)*1000],f2(t[max(f2start,windowStart*1000):(windowStart+windowLength)*1000]),'b') 
       axs[i+1].plot(t,recwindow(0,20,windowStart,windowLength),'r')
       windowStart=windowStart+overlap  
    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel('time[s]', fontsize=16)
    plt.ylabel('Amplitude', fontsize=16, )
    plt.savefig('overlapfigure.pdf')
    
#overlapplot(2,0.5,3,4)