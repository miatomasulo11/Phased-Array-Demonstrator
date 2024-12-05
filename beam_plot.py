import numpy as np
import adi
import matplotlib.pyplot as plt
import time

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

array = np.empty(50)
# Gather t samplesand display average power
for a in range(50):    # Clear buffer just to be safe
    for i in range (0, 10):
        raw_data = sdrx.rx()

    # Receive samples
    rx_samples = sdrx.rx()
    #print(rx_samples)

    # Stop transmitting
    #sdr.tx_destroy_buffer()

    #Calculate avegare power from received samples
    avg_power = np.mean(np.abs(rx_samples)**2)
    print("Average Power",avg_power)

    avg_power_db = 10.0*np.log10(avg_power)

    print("Average Power (dB)", avg_power_db)
    
    rssi = sdrx._ctrl.find_channel('voltage0').attrs['rssi'].value
    print("RSSI", rssi)
    print(a)
    array[a] = avg_power_db

    time.sleep(0.1)

plt.plot(range(50),array)
plt.show()