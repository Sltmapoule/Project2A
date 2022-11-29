import scipy
from scipy.signal import remez, freqz
from scipy.fft import fft, fftfreq
from scipy.signal import blackman
import matplotlib.pyplot as plt
import numpy as np


# b, a = signal.iirfilter(25, [2 * np.pi * 50, 2 * np.pi * 200], rs=60, btype='band', analog=True, ftype='cheby2')
# w, h = signal.freqs(b, a, 1000)
# fig = plt.figure()
# ax = fig.add_subplot(2, 1, 1)
# ax.semilogx(w / (2 * np.pi), 20 * np.log10(np.maximum(abs(h), 1e-5)))
# ax.set_title('Chebyshev Type II bandpass frequency response')
# ax.set_xlabel('Frequency [Hz]')
# ax.set_ylabel('Amplitude [dB]')
# ax.axis((10, 1000, -100, 10))
# ax.grid(which='both', axis='both')
#
# z, p, k = signal.iirfilter(25, [2 * np.pi * 50, 2 * np.pi * 200], rs=60, btype='band', analog=True, ftype='cheby2',
#                            output='zpk')
# bx = fig.add_subplot(2, 1, 2)
# bx.plot(np.real(z), np.imag(z), 'ob', markerfacecolor='none')
# bx.plot(np.real(p), np.imag(p), 'xr')
# bx.legend(['Zeros', 'Poles'], loc=2)
# bx.set_title('Pole / Zero Plot')
# bx.set_xlabel('Real')
# bx.set_ylabel('Imaginary')
# bx.grid()
# plt.show()


# # Number of sample points
# N = 10000
# # sample spacing
# T = 1.0 / 800.0
# x = np.linspace(0.0, N * T, N, endpoint=False)
# y = np.sin(50.0 * 2.0 * np.pi * x) + 0.5 * np.sin(80.0 * 2.0 * np.pi * x)
# yf = fft(y)
# w = blackman(N)
# ywf = fft(y * w)
# xf = fftfreq(N, T)[:N // 2]
# plt.semilogy(xf[1:N // 2], 2.0 / N * np.abs(yf[1:N // 2]), '-b')
# plt.semilogy(xf[1:N // 2], 2.0 / N * np.abs(ywf[1:N // 2]), '-r')
# plt.legend(['FFT', 'FFT w. window'])
# plt.grid()
# plt.show()

def plot_response(fs, w, h, title):
    "Utility function to plot response functions"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(0.5 * fs * w / np.pi, 20 * np.log10(np.abs(h)))
    ax.set_ylim(-40, 5)
    ax.set_xlim(0, 0.5 * fs)
    ax.grid(True)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Gain (dB)')
    ax.set_title(title)


fs = 96000.0  # Sample rate, Hz
band = [1000, 30000]  # Desired pass band, Hz
trans_width = 260  # Width of transition from pass band to stop band, Hz
numtaps = 50  # Size of the FIR filter.
edges = [0, band[0] - trans_width, band[0], band[1],
         band[1] + trans_width, 0.5 * fs]
taps = remez(numtaps, edges, [0, 1, 0], Hz=fs)
w, h = freqz(taps, [1], worN=2000)
plot_response(fs, w, h, "Band-pass Filter")
plt.show()
