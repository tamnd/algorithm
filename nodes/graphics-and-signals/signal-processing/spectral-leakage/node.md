---
tag: SQWQYP
kind: concept
slug: spectral-leakage
name: Spectral leakage
aliases:
- leakage
- DFT leakage
area: graphics-and-signals/signal-processing
level: core
summary: "A finite block of samples spreads a pure tone over all DFT bins unless it holds a whole number of cycles; the spread follows the spectrum of the window."
prereqs: [discrete-fourier-transform, discrete-time-fourier-transform]
see_also: [window-functions, gibbs-phenomenon, periodogram, welch-method, short-time-fourier-transform, power-spectral-density, spectral-estimation, aliasing]
sources:
  - paper: doi:10.1109/PROC.1978.10837
    title: Fredric J. Harris, On the Use of Windows for Harmonic Analysis with the Discrete Fourier Transform, Proceedings of the IEEE 66(1), 1978
    locator: pp. 51 to 83 (the DFT of finite-extent data, spectral leakage as the effect of the window's spectrum, the figures of merit, and the detection of a weak tone near a strong one)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 10, Fourier Analysis of Signals Using the DFT (the effect of windowing on the spectrum of sinusoidal signals, leakage and resolution)
  - book: isbn:9780138147570
    title: Alan V. Oppenheim, Alan S. Willsky and S. Hamid Nawab, Signals and Systems, second edition, Prentice Hall, 1997
    locator: Chapter 5, The Discrete-Time Fourier Transform (the multiplication property, which turns windowing into periodic convolution of spectra)
---

Spectral leakage is the spreading of a signal's energy from its true frequency into other frequencies, caused by analysing only a finite block of it. When the [DFT](/discrete-fourier-transform/) of $N$ samples of a pure tone is taken, the energy falls into a single bin only if the block holds a whole number of cycles; otherwise every bin receives some of it. The reason is that cutting out a block multiplies the signal by a window, and the spectrum of the product is the true spectrum smeared by the spectrum of the window. The rectangular window, plain truncation, has the narrowest main lobe and the highest side lobes; other [window functions](/window-functions/) trade a wider main lobe for much less leakage far from the tone.

## In plain words

To find the notes in a sound, we cut out a short piece and measure how much of each note it holds. The cut is the problem. If the piece holds a whole number of waves of a note, the measurement finds that note cleanly. If the piece stops in the middle of a wave, the cut leaves a sudden jump, and a jump is made of many notes. So the measurement shows the true note plus a spread of false ones nearby and far away. A loud note can then hide a quiet note beside it. Fading the piece in and out, instead of cutting it sharply, makes the spread much smaller.

## The idea

**Windowing is multiplication, so it smears the spectrum.** Let $x[n]$ be a sequence with [DTFT](/discrete-time-fourier-transform/) $X(e^{i\omega})$, $\omega$ in radians per sample, and let $w[n]$ be zero outside $0 \le n \le N - 1$. The block that is analysed is $x[n]w[n]$, and its DTFT is the periodic convolution

$$(xw)^\wedge(e^{i\omega}) = \frac{1}{2\pi}\int_{-\pi}^{\pi} X(e^{i\theta})\, W(e^{i(\omega - \theta)})\, d\theta.$$

For the tone $x[n] = e^{i\omega_0 n}$, $X$ is an impulse at $\omega_0$ and the result is $W(e^{i(\omega - \omega_0)})$: a copy of the window's spectrum centred at the tone. For the rectangular window $w[n] = 1$, $W$ is the Dirichlet kernel $e^{-i\omega(N-1)/2}\sin(N\omega/2)/\sin(\omega/2)$, with a main lobe of half-width $2\pi/N$ (one bin) and side lobes that fall off like $1/|\omega|$.

**The DFT samples the smeared spectrum.** The $N$-point DFT of the block is that DTFT at $\omega_k = 2\pi k/N$. The Dirichlet kernel is zero at every nonzero multiple of $2\pi/N$. So if $\omega_0 = 2\pi c/N$ with $c$ an integer, every bin except $k = c$ lands on a zero and no leakage is visible. If $c$ is not an integer, the bins sample the main lobe off its peak and the side lobes off their zeros, and every bin is nonzero. A real cosine is two complex tones at $\pm\omega_0$, so its DFT is the sum of two such kernels, centred at $c$ and $N - c$.

**The periodic view.** The DFT treats the block as one period of a periodic sequence. With a whole number of cycles the periodic extension is the same sinusoid. With a fractional number of cycles the extension has a jump at each block boundary, and a jump has a broad spectrum; the slow $1/|\omega|$ decay of the side lobes is the $1/k$ decay of the Fourier coefficients of a jump, the same fact behind the [Gibbs phenomenon](/gibbs-phenomenon/).

**Two separate costs.** The main lobe limits *resolution*: two tones closer than about one bin (for the rectangular window) merge into one peak. The side lobes limit *dynamic range*: a strong tone puts energy into far bins that can be larger than a weak tone there. A longer block narrows both lobes in proportion to $1/N$, but the level of the side lobes relative to the peak stays the same; for the rectangular window the highest side lobe is about $-13.26$ dB below the peak at every block length.

**Scalloping.** A tone halfway between two bins is measured at the bins next to it, below its main lobe peak. For the rectangular window the loss is $1/(N\sin(\pi/(2N)))$, which tends to $2/\pi$, or $-3.92$ dB. So the measured amplitude depends on where the tone falls relative to the bin grid, by up to almost $4$ dB.

**What leakage is not.** Leakage is not [aliasing](/aliasing/): aliasing comes from sampling too slowly and folds frequencies above $f_s/2$, while leakage comes from a finite record and happens at any sampling rate. Zero padding does not remove it: appending zeros only samples the same smeared DTFT on a finer grid, which shows the side lobes between the bins instead of hiding them. Leakage does not create or destroy energy: by [Parseval's theorem](/parsevals-theorem/) the sum of $|X_k|^2$ is always $N$ times the energy of the block, and leakage only moves it between bins.

**The remedies.**

- *A window that tapers to zero.* Hann, Hamming, Blackman and Kaiser windows remove the jump at the block boundary, so their side lobes are lower and fall off faster; the cost is a wider main lobe and a loss of amplitude, figures that are compared on [window functions](/window-functions/).
- *Synchronous sampling.* In test equipment the sampling clock is locked to the signal so that each block holds a whole number of cycles of the fundamental. Then the rectangular window has no leakage for the fundamental and its harmonics.
- *Longer records.* They improve resolution but not the relative side lobe level.
- *Averaging,* as in the [Welch method](/welch-method/), reduces the variance of a spectrum estimate, not its leakage, which comes from the window used in each segment.

## Examples

**A whole and a fractional number of cycles.** With $N = 16$, the cosine with $4$ cycles in the block has $|X_4| = |X_{12}| = 8$ and all other bins zero (below $10^{-9}$ in floating point). The cosine with $4.5$ cycles has, for $k = 0, \ldots, 8$, the magnitudes $1.0000$, $1.0569$, $1.2705$, $1.8860$, $5.2225$, $5.0254$, $1.7051$, $1.1295$, $1.0000$, computed by the direct DFT and equal to the two-kernel closed form to $10^{-9}$. No bin is below $1$, so even the bin farthest from the tone receives about $1/5$ of the peak.

**Far leakage with three windows.** For $N = 64$ and a cosine with $10.5$ cycles, the fraction of the DFT energy in bins more than $3$ bins away from the tone (counting its mirror image at $N - c$ as near) is $6.55 \times 10^{-2}$ with the rectangular window, $1.12 \times 10^{-4}$ with the Hann window and $3.85 \times 10^{-6}$ with the Blackman window. With $10$ whole cycles it is below $10^{-28}$ for all three, which is rounding error.

**A weak tone hidden by a strong one.** Let $N = 64$, a strong cosine of amplitude $1$ at $10.5$ cycles and a weak cosine of amplitude $10^{-3}$ ($-60$ dB) at $20$ cycles. With the rectangular window the DFT magnitudes at bins $19$, $20$, $21$ are $1.554$, $1.458$, $1.342$: a smooth slope of side lobes, with no peak at bin $20$. The weak tone alone would give $0.032$ there, about $33$ dB below the leakage of the strong one ($1.436$). With the Hann window the same bins read $0.0117$, $0.0171$, $0.0091$ and with the Blackman window $0.0085$, $0.0136$, $0.0081$: the weak tone now stands out as a local peak, because the leakage of the strong tone at bin $20$ falls to $0.0060$ (Hann) and $0.0020$ (Blackman), below the weak tone's own $0.0160$ and $0.0134$.

**Scalloping.** A complex tone at $5.5$ cycles in $N = 256$ samples gives a largest bin of $N \cdot 0.63662$, the $2/\pi$ loss to five digits; with $N = 16$ the loss is $1/(16\sin(\pi/32)) = 0.6376$.

**Zero padding.** Padding the $16$ samples of the $4.5$ cycle cosine to $64$ with zeros gives a DFT whose every fourth value is the original bin, and whose values in between follow the closed form of the Dirichlet kernels at quarter-bin spacing: the leakage is still there, only sampled more finely.

## Where it is used

- **Spectrum analysers and FFT measurement.** Instruments offer a choice of windows: flat-top windows for accurate amplitudes (small scalloping), Hann for general use, rectangular for transients and for signals that are synchronous with the block. Harmonic distortion tests use synchronous sampling to avoid leakage altogether.
- **Spectral estimation.** The [periodogram](/periodogram/), the [Welch method](/welch-method/) and other estimates of the [power spectral density](/power-spectral-density/) carry the bias of the window's spectrum; choosing it is part of [spectral estimation](/spectral-estimation/).
- **Spectrograms.** The [short-time Fourier transform](/short-time-fourier-transform/) analyses overlapping windowed blocks, and the window sets the time-frequency trade-off of the picture.
- **Radar, sonar and vibration analysis,** where small targets or faults appear as weak lines next to strong ones, and low side lobes decide whether they are seen.
- **Multicarrier communications.** OFDM subcarriers are orthogonal because each holds a whole number of cycles in a symbol; a frequency offset breaks this, and the resulting interference between carriers is leakage.
- **Filter design,** in the dual form: truncating an ideal impulse response is a rectangular window in time, and its side lobes appear as ripple in frequency.

## References
