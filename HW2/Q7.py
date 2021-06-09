#!/usr/bin/env python

import matplotlib.pyplot as plt # for plotting
import numpy as np # for sine function
import csv


def import_data(file):
    if file=="sigA.csv":
        sampling_rate = "10000Hz"
        f_L = "400Hz"
        b_L = "100Hz"

        # Configuration.
        fs = 10000  # Sampling rate.
        fL = 300  # Cutoff frequency.
        N = 311  # Filter length, must be odd.

    if file == "sigB.csv":
        sampling_rate = "3500Hz"
        f_L = "84Hz"
        b_L = "30Hz"

        # Configuration.
        fs = 3500  # Sampling rate.
        fL = 80  # Cutoff frequency.
        N = 311  # Filter length, must be odd.

    if file == "sigC.csv":
        sampling_rate = "2500Hz"
        f_L = "100Hz"
        b_L = "25Hz"

        # Configuration.
        fs = 2700  # Sampling rate.
        fL = 100  # Cutoff frequency.
        N = 311  # Filter length, must be odd.

    if file == "sigD.csv":
        sampling_rate = "400Hz"
        f_L = "30Hz"
        b_L = "34Hz"

        # Configuration.
        fs = 400  # Sampling rate.
        fL = 30  # Cutoff frequency.
        N = 34  # Filter length, must be odd. 


    h = np.sinc(2 * fL / fs * (np.arange(N) - (N - 1) / 2))

    # Apply window.
    h *= np.hamming(N)

    # Normalize to get unity gain.
    h /= np.sum(h)

    t = [] # column 0
    data = [] # column 1
    
    with open(file) as f:
        # open the csv file
        reader = csv.reader(f)
        for row in reader:
            # read the rows 1 one by one
            t.append(float(row[0])) # leftmost column
            data.append(float(row[1])) # second column

    return h ,t,data,fs,f_L, b_L


if __name__ == '__main__':
    h,t,data,fs,f_L, b_L =import_data('sigB.csv')
    ndata = []
    len_diff = len(data) - len(h)

    for i in range(len_diff):
        buffer = []
        for j in range(len(h)):
            buffer.append(data[i + j])
        ndata.append(np.average(buffer, weights=h))


    sample_rate = len(t)/t[-1]
    print(f"The sample rate is {sample_rate} Hz")

    dt = len(t)/t[-1]
    t = np.asarray(t)
    nt = t[0 : len_diff]

    Fs = dt 
    Ts = 1.0/Fs; # sampling interval
    ts = np.arange(0,t[-1],Ts) 
    y = data 
    n = len(y)
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(int(n/2))] # one side frequency range
    Y = np.fft.fft(y)/n # fft computing and normalization
    Y = Y[range(int(n/2))]

    nts = np.arange(0,nt[-1],Ts) # time vector
    ny = ndata # the data to make the fft from
    nn = len(ny) # length of the signal
    nk = np.arange(nn)
    nT = nn/Fs
    nfrq = k/nT # two sides frequency range
    nfrq = nfrq[range(int(nn/2))] # one side frequency range
    nY = np.fft.fft(ny)/nn # fft computing and normalization
    nY = nY[range(int(nn/2))]

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_title(f'sample_rate = {fs}, f_L = {f_L}, b_L = {b_L}')
    ax1.plot(t,data,'b')
    ax1.plot(nt, ndata,'r')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Signal')
    ax2.loglog(frq,abs(Y),'black') # plotting the fft
    ax2.loglog(nfrq,abs(nY),'r') # plotting the filtered fft
    ax2.set_xlabel('Freq (Hz)')
    ax2.set_ylabel('|Y(freq)|')
    fig.suptitle(f'Signal vs Time (for SignalB)')    
    
    plt.savefig('Q7_sigB.png')
