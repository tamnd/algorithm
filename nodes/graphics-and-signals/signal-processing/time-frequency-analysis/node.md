---
tag: 4QATN3
kind: problem
slug: time-frequency-analysis
name: Time-frequency analysis
aliases:
- joint time-frequency analysis
area: graphics-and-signals/signal-processing
level: core
summary: "Describe how the frequency content of a signal changes over time, as a map over time and frequency. The uncertainty principle limits how sharp the map can be in both at once."
model: real-ram
complexity:
  vars: {L: the length of the signal, N: the window length, R: the hop between frames}
  time: {worst: O((L + N) N log N / R)}
prereqs: [discrete-fourier-transform, discrete-time-fourier-transform]
see_also: [short-time-fourier-transform, time-frequency-uncertainty, continuous-wavelet-transform, discrete-wavelet-transform, empirical-mode-decomposition, analytic-signal, window-functions, pitch-detection]
sources:
  - book: isbn:9780135945322
    title: Leon Cohen, Time-Frequency Analysis, Theory and Applications, Prentice Hall, 1995
    locator: the chapters on the short-time Fourier transform, the Wigner distribution and the general class of quadratic distributions (general locator; chapter numbers not confirmed)
  - book: isbn:9780123743701
    title: Stéphane Mallat, A Wavelet Tour of Signal Processing, The Sparse Way, third edition, Academic Press, 2009
    locator: Chapter 4, Time Meets Frequency (windowed Fourier transform, wavelet transform, Wigner-Ville distribution)
  - paper: doi:10.1049/ji-3-2.1946.0074
    title: Dennis Gabor, Theory of communication, Part 1, The analysis of information, Journal of the Institution of Electrical Engineers, Part III 93(26), 1946, 429 to 441
    locator: the time-frequency plane divided into cells and the elementary signals with Gaussian envelopes
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 10.3, The Time-Dependent Fourier Transform
---

Time-frequency analysis is the problem of describing how the frequency content of a signal changes over time. The output is a map $T(t, \omega)$ over time and frequency that shows where the energy of the signal lies, such as the spectrogram of the [short-time Fourier transform](/short-time-fourier-transform/) or the scalogram of the [continuous wavelet transform](/continuous-wavelet-transform/). No map is sharp in both directions at once: the [time-frequency uncertainty principle](/time-frequency-uncertainty/) bounds the product of the spreads, so every method chooses a trade-off. The methods differ in that trade-off, in whether they are linear or quadratic, and in whether they can be inverted.

## In plain words

A plain Fourier transform lists the frequencies in a whole recording but hides when each one occurs. A bird call that rises in pitch and a chord that holds still can give similar lists. Time-frequency analysis draws a picture instead: time across, frequency up, brightness for strength.

The catch is that a short look at the signal tells exactly when something happens but only roughly which frequency it has, and a long look does the opposite. No method escapes this. Short windows suit clicks and drum hits, long windows suit sustained notes. Some methods change the window length with the frequency, and some build the pieces from the signal itself. The right choice depends on what you need to see.

## Definition

The input is a signal $x[0 \ldots L-1]$ sampled at $f_s$ Hz. Frequency is measured in radians per sample, $\omega \in [-\pi, \pi]$, or in Hz, $f = \omega f_s / (2\pi)$. The output is a representation $T_x(t, \omega)$ on a grid of times $t$ and frequencies $\omega$, or a set of components with a time-varying frequency each, such that:

- **Localization.** A sinusoid $\cos(\omega_0 n)$ gives a ridge near $\omega = \omega_0$, and an impulse $\delta[n - n_0]$ gives a ridge near $t = n_0$.
- **Energy.** The values are energy densities or amplitudes that can be compared across the map.

Further properties are asked for in some variants: linearity in $x$, invertibility, nonnegativity, and the marginals, that the sum over frequency is $|x[t]|^2$ and the sum over time is $|X(e^{i\omega})|^2$. No quadratic representation is both nonnegative everywhere and has both marginals for all signals, so each method gives up something.

## Variants

- **Linear, fixed window.** The [short-time Fourier transform](/short-time-fourier-transform/) $X_m[k]$, its squared magnitude the spectrogram, and the Gabor transform with a Gaussian window. The resolution is the same everywhere on the map.
- **Linear, scale-dependent window.** The [continuous wavelet transform](/continuous-wavelet-transform/) and its squared magnitude the scalogram, the [discrete wavelet transform](/discrete-wavelet-transform/) on a dyadic grid, and constant-Q transforms. Windows are short at high frequency and long at low frequency.
- **Quadratic.** The Wigner-Ville distribution $W_x(t, \omega) = \sum_\tau x[t + \tau]\, \overline{x[t - \tau]}\, e^{-2i\omega\tau}$ has the marginals and the best concentration for a linear chirp, but it takes negative values and creates cross terms between components. Smoothing it gives Cohen's class of distributions, which contains the spectrogram.
- **Instantaneous frequency.** For a signal with one component, the [analytic signal](/analytic-signal/) $z = a e^{i\varphi}$ gives the amplitude $a[n]$ and the frequency $\varphi[n+1] - \varphi[n]$ at each sample.
- **Adaptive decompositions.** [Empirical mode decomposition](/empirical-mode-decomposition/) splits the signal into oscillating modes from its own extrema, and the Hilbert spectrum plots their instantaneous frequencies. It is a heuristic without a convergence theory.
- **Sharpened maps.** Reassignment and synchrosqueezing move the energy of a spectrogram or scalogram towards the ridge it belongs to.

## Examples

**Grid sizes.** At $f_s = 8000$ Hz with a window of $N = 256$ samples, a frame lasts $256 / 8000 = 32$ ms and the DFT bins are $8000 / 256 = 31.25$ Hz apart. A hop of $R = 64$ samples gives a new frame every 8 ms. A signal of one second has $\lfloor 7999/64 \rfloor + \lfloor 255/64 \rfloor + 1 = 124 + 3 + 1 = 128$ frames, each with 129 bins from 0 to 4000 Hz for real input.

**Two tones and a click.** Let the signal hold tones at 1000 Hz and 1020 Hz, and a click at 0.5 s. With the 32 ms window, the tones are $20 / 31.25 = 0.64$ bins apart, inside one main lobe of a Hann window, which is 4 bins wide, so they merge into one ridge; the click is a vertical line about 32 ms wide. With a window of 200 ms ($N = 1600$), the bins are 5 Hz apart, the tones are 4 bins apart and appear as two ridges, and the click is smeared over 200 ms. No single window shows both well, which is the trade-off that the uncertainty principle makes precise.

**A chirp.** A signal whose frequency rises linearly with time gives a straight diagonal ridge on a spectrogram. A wavelet scalogram shows it as a curve, because its frequency axis is logarithmic. The Wigner-Ville distribution of a single linear chirp is concentrated exactly on the line, but the sum of two chirps adds an oscillating cross term halfway between them.

## Known algorithms

| Method | Cost | Output |
|---|---|---|
| [Short-time Fourier transform](/short-time-fourier-transform/) | about $\frac{N}{R}(1 + \frac{1}{2}\log_2 N)$ multiplications per sample | linear, invertible by overlap-add; spectrogram $\lvert X \rvert^2$ |
| [Continuous wavelet transform](/continuous-wavelet-transform/) | $O(J \log L)$ per sample by FFT, for $J$ scales | linear, redundant, logarithmic frequency axis |
| [Discrete wavelet transform](/discrete-wavelet-transform/) | $O(K)$ per sample for filters of length $K$ | linear, not redundant, dyadic grid |
| Wigner-Ville distribution | $O(N \log N)$ per time point with a lag window of length $N$ | quadratic, sharp for chirps, cross terms |
| [Analytic signal](/analytic-signal/) | $O(\log L)$ per sample with an FFT of the whole signal | amplitude and instantaneous frequency of one component |
| [Empirical mode decomposition](/empirical-mode-decomposition/) | about $O(L)$ per sifting step, number of steps not bounded by theory | adaptive modes and their Hilbert spectrum |

## Bounds

- **Uncertainty.** For any window, the product of its spread in time and its spread in frequency has a positive lower bound, reached only by Gaussians; see the [time-frequency uncertainty principle](/time-frequency-uncertainty/). This is a worst case bound that holds for every signal and every linear method with that window.
- **Bin spacing.** An $N$-point DFT has bins $2\pi / N$ radians per sample apart, $f_s / N$ in Hz. Two tones closer than about the main lobe width of the window, which is 4 bins for the Hann window, are not separated, whatever the hop.
- **Redundancy.** A linear map that is invertible must produce at least $L$ numbers for $L$ samples. The STFT produces $N/R$ times as many; the discrete wavelet transform and the [modified discrete cosine transform](/modified-discrete-cosine-transform/) reach exactly $L$. For Gabor systems at exactly $L$ numbers, the Balian-Low theorem rules out windows that are well localized in both time and frequency.
- **Cost.** Any method that looks at every sample costs $\Omega(L)$. The STFT costs $O(\log N)$ per sample per unit of redundancy.

## Reductions

- The spectrogram is the squared magnitude of the STFT. It equals the Wigner-Ville distribution of the signal smoothed by the Wigner-Ville distribution of the window, which places it in Cohen's class.
- The [Welch method](/welch-method/) estimate of the [power spectral density](/power-spectral-density/) is the time average of a spectrogram.
- The STFT at a fixed bin is a bandpass [filter bank](/filter-bank/) output, sampled every hop.
- Inverting a modified spectrogram without phases is [phase retrieval](/phase-retrieval/), solved in practice by the [Griffin-Lim algorithm](/griffin-lim-algorithm/).

## Applications

- **Speech.** Spectrograms show formants, voicing and pitch; [pitch detection](/pitch-detection/) and speech recognizers work on frames of 20 to 40 ms.
- **Music.** Note onsets, pitch tracks and chord changes; constant-Q maps match the semitone spacing of musical scales.
- **Noise reduction.** [Spectral subtraction](/spectral-subtraction/) and Wiener filtering act on each time-frequency cell and then invert the STFT.
- **Radar and sonar.** Doppler shifts that change over time, such as the micro-Doppler of rotating parts.
- **Biomedicine and geophysics.** EEG rhythms, heart rate variability, and seismic signals with changing frequency.
- **Machine monitoring.** Faults in gears and bearings show as frequency components that come and go.

## References
