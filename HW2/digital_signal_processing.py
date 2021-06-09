#!/usr/bin/env python

import matplotlib.pyplot as plt # for plotting
import numpy as np # for sine function
import csv


def import_data(file):

    t = [] # column 0
    data1 = [] # column 1
    data2 = [] # column 2

    with open(file) as f:
        # open the csv file
        reader = csv.reader(f)
        for row in reader:
            # read the rows 1 one by one
            t.append(float(row[0])) # leftmost column
            data1.append(float(row[1])) # second column
        # data2.append(float(row[2])) # third column

    return t,data1

def plot_data(x,y,name):
    plt.plot(x,y,'b-*')
    plt.xlabel('Time [s]')
    plt.ylabel('Signal')
    plt.title(name+' vs Time')
    plt.savefig(name+'.png')
    # plt.show()

def generate_fft(x,y,name):
    
    Fs = 10000 # sample rate
    Ts = 1.0/Fs; # sampling interval
    ts = np.arange(0,x[-1],Ts) # time vector
    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(int(n/2))] # one side frequency range
    Y = np.fft.fft(y)/n # fft computing and normalization
    Y = Y[range(int(n/2))]

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(x,y,'b')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax1.set_title(name+' vs Time')
    ax2.loglog(frq,abs(Y),'r') # plotting the fft
    ax2.set_xlabel('Freq (Hz)')
    ax2.set_ylabel('|Y(freq)|')
    ax2.set_title('fft for '+name)
    plt.savefig(name+'.png')
    plt.show()


# def IIR_filter(x,y,a,b):

def moving_average_filter(data,n) :
    new_list = []
    for i in range(len(data)-n):
        sum=0
        for j in range(n):
           sum+=data[i+j]

        new_list.append(sum/n)
    
    return new_list

    # for i in range(len(data)):
    #     if i<n:
    #         new_list.append(0)
    #     else:
    #         this_window = data[i : i + n]
    #         window_average = sum(this_window) / n
    #         new_list.append(window_average)

    # return new_list

  
def plot_moving_filter(dt,data,nt,ndata,name):
    Fs = dt # sample rate
    Ts = 1.0/Fs; # sampling interval
    ts = np.arange(0,t[-1],Ts) # time vector
    y = data # the data to make the fft from
    n = len(y) # length of the signal
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
    ax1.set_title(f'Signal vs Time')
    ax1.plot(t,data,'black')
    ax1.plot(nt, ndata, 'r')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Signal')
    ax2.loglog(frq,abs(Y),'b') # plotting the fft
    ax2.loglog(nfrq,abs(nY),'r') # plotting the filtered fft
    ax2.set_xlabel('Freq (Hz)')
    ax2.set_ylabel('|Y(freq)|')
    plt.savefig('iir_filter_'+name+'.png')
    plt.show()

def plot_iir_filter(dt,data,nt,ndata,name,A,B):
    Fs = dt # sample rate
    Ts = 1.0/Fs; # sampling interval
    ts = np.arange(0,t[-1],Ts) # time vector
    y = data # the data to make the fft from
    n = len(y) # length of the signal
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
    ax1.set_title(f'Signal vs Time with A='+A+'and B='+B)
    ax1.plot(t,data,'black')
    ax1.plot(nt, ndata, 'r')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Signal')
    ax2.loglog(frq,abs(Y),'b') # plotting the fft
    ax2.loglog(nfrq,abs(nY),'r') # plotting the filtered fft
    ax2.set_xlabel('Freq (Hz)')
    ax2.set_ylabel('|Y(freq)|')
    plt.savefig('iir_filter_'+name+'.png')
    plt.show()

def IIR_filter(data,n):
    new_list = []
    A = 0.99
    B = 1 - A
    new_average = data[0]
    for i in range(len(data)):
        new_average = A * new_average + B*data[i]
        new_list.append(new_average)
    return new_list,A,B


if __name__ == '__main__':
    '''replace sigA.csv with each signal's .csv file here to visualize the signal'''
    t,data=import_data('sigD.csv')
    # plot_data(x,y,'sigD')
    # plt.plot(x,y,'b')
    n=500
    # new_data=moving_average_filter(data,n)
    # generate_fft(x,y,'sigD')
    # # print(new_x)

    # dt = len(t)/t[-1]
    # t = np.asarray(t)
    # new_t=t[0:-n]

    # plot_moving_filter(dt,data,new_t,new_data,'sigD')
    new_data,A,B= IIR_filter(data,n)
    dt = len(t)/t[-1]
    t = np.asarray(t)
    new_t=t[0:]

    
    plot_iir_filter(dt,data,new_t,new_data,'sigD',str(A),str(B))




   