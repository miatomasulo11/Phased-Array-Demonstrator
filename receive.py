import libiio
import numpy as np
import adi
import matplotlib.pyplot as plt
import time
from datetime import datetime

START_STRING = '1111100'
STOP_STRING = '10000011'
SLEEP_TIME = 50

sample_rate = 30e6 # Hz
center_freq = 1007e6 # Hz
num_samps = 1000 # number of samples per call to rx()

sdr = adi.Pluto("ip:192.168.2.1")
sdrx = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = 0 # Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx

sdrx.rx_lo = int(center_freq)
sdrx.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdrx.gain_control_mode_chan0 = 'manual'
sdrx.rx_hardwaregain_chan0 = 0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC

# Create transmit waveform (QPSK, 16 samples per symbol)
num_symbols = 1000
x_int = np.random.randint(0, 4, num_symbols) # Create an array of quality 'num_symbols' each element 0 to 3
x_degrees = x_int*360/4.0 + 45 # 45, 135, 225, 315 degrees
x_radians = x_degrees*np.pi/180.0 # sin() and cos() takes in radians
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) # this produces our QPSK complex symbols
#print("x_symbols: &",x_symbols)


samples = np.repeat(x_symbols, 16)  # 16 samples per symbol (rectangular pulses). 10K num_samp x 16 = 160000
                                    # Each symbol repeated 16 times
#print("samples= &",samples)


samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs

#plt.figure(0)
#plt.plot(samples)
#plt.show()

# Start the transmitter
# sdr.tx_cyclic_buffer = True # Enable cyclic buffers
# sdr.tx(samples) # start transmitting the samples continuelsy

array = np.empty(15)
test = ''
# Gather t samplesand display average power
while(1):    # Clear buffer just to be safe

    for i in range (0, 10):
        raw_data = sdrx.rx()

    # now = datetime.now()
    # # Extract hundredths of a second
    # hundredths = now.microsecond // 10000  # Convert microseconds to hundredths
    # while hundredths % SLEEP_TIME != 0:  # Check if the hundredth is even
    #     # Format time with hundredths of a second
    #     # Receive samples


    #     now = datetime.now()
    #     hundredths = now.microsecond // 10000

    rx_samples = sdrx.rx()

    #Calculate avegare power from received samples

    # current_time = now.strftime("%H:%M:%S.") + f"{hundredths:02}"
    # print(current_time)
    avg_power = np.mean(np.abs(rx_samples)**2)

    avg_power_db = 10.0*np.log10(avg_power)
    
    if avg_power_db > 10:
        bit = '1'
        
        
    elif avg_power_db <=10:
        bit= '0'

    print(bit)
    test += bit

    if  START_STRING in test:
        print('Start sequence detected.')
        test = ''
    elif STOP_STRING in test:
        print('End sequence detected.')
        test = test[:-len(STOP_STRING)]
        print('\n\n',test,'\n\n')
        test = ''
        while(1):
            pass

    time.sleep(SLEEP_TIME/100)

print(test)
