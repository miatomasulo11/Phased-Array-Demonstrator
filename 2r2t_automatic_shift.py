import adi
import time
import numpy as np

# Create radio
sdr = adi.ad9361(uri='ip:192.168.2.1')

# Configure Tx properties
sdr.tx_rf_bandwidth = int(30.72e6)
sdr.tx_lo = int(1e9)
sdr.tx_cyclic_buffer = True
sdr.tx_hardwaregain_chan0 = int(0)
sdr.tx_hardwaregain_chan1 = int(0)
sdr.tx_buffer_size = int(2**18)

# Program the Tx with some data
fs = int(30.72e6)
fc0 = int(500e6)
fc1 = int(500e6)
N = 2**16
ts = 1 / float(fs)
t = np.arange(0, N * ts, ts)

shift = 0

for i in range(8):
    # Generate the IQ data
    i0 = np.cos(2 * np.pi * t * fc0 + np.pi/6  + shift) * 2 ** 14
    q0 = np.sin(2 * np.pi * t * fc0 + np.pi/6 + shift) * 2 ** 14
    i1 = 1.27 * np.cos(2 * np.pi * t * fc1) * 2 ** 14
    q1 = 1.27 * np.sin(2 * np.pi * t * fc1) * 2 ** 14

    # Combine to form complex IQ data
    iq0 = i0 + 1j * q0
    iq1 = i1 + 1j * q1

    # Transmit the data
    sdr.tx([iq0, iq1])
    shift += np.pi/2
    time.sleep(1)
    sdr.tx_destroy_buffer()

print('Transmitting')

# Infinite loop to keep the program running
while True:
    pass