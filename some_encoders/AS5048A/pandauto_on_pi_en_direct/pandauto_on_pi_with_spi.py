
"""
De Arduino en debug:

Read (0x3FFF) with command: 0b1111111111111111
Read returned: 1101110100001010
Setting error bit
3433
Read (0x3FFF) with command: 0b1111111111111111
Read returned: 101110100000111
Setting error bit
3432

"""

from time import time, sleep
import pigpio

CE = 8

pi = pigpio.pi()
sensor = pi.spi_open(0, 1000000, 1)

dt = 0.00001

pi.set_mode(CE, pigpio.INPUT)

pi.write(CE, 1)
sleep(dt)

t0 = time()
n = -1
nbr = 1000
tempo = 0.03
while n < nbr:
    n += 1
    pi.write(CE, 0)
    sleep(dt)

    c, d = pi.spi_xfer(sensor, int.to_bytes(65535, 2, 'big'))
    if c == 2:
        val = (d[0] & 0b00111111) << 8 | d[1]
        angle = int(val/4)

    # #if n % 20 == 0:
        # #print(angle)

    pi.write(CE, 1)

    sleep(tempo)

pi.stop()

periode = (((time() - t0) / nbr) - tempo)*1000  # ms
print("periode =", round(periode, 2), "ms")
sleep(1)

"""
periode = 1.9 ms
il y a quelques incohérences dans les valeurs

sans print
periode = 1.3 ms
periode = 1.19 ms

"""
