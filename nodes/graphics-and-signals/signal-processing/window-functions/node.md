---
tag: YX4DES
kind: concept
slug: window-functions
name: Window functions
aliases:
- apodization
- tapering windows
- data windows
area: graphics-and-signals/signal-processing
level: core
summary: "Tapers (Hann, Hamming, Blackman, Kaiser) applied to a block before a DFT; they lower side lobes and leakage at the cost of a wider main lobe and some gain."
prereqs: [spectral-leakage]
see_also: [spectral-leakage, short-time-fourier-transform, fir-filter, digital-filter-design, welch-method, periodogram, time-frequency-uncertainty, gibbs-phenomenon]
sources:
  - paper: doi:10.1109/PROC.1978.10837
    title: Fredric J. Harris, On the Use of Windows for Harmonic Analysis with the Discrete Fourier Transform, Proceedings of the IEEE 66(1), 1978
    locator: pp. 51 to 83 (even and periodic windows, the figures of merit such as equivalent noise bandwidth, scalloping loss and highest side lobe, the classic windows, and the table that compares them)
  - paper: doi:10.1109/TASSP.1980.1163349
    title: James F. Kaiser and Ronald W. Schafer, On the Use of the I0-Sinh Window for Spectrum Analysis, IEEE Transactions on Acoustics, Speech, and Signal Processing 28(1), 1980
    locator: pp. 105 to 107 (the Kaiser window for spectrum analysis and the choice of its parameter for a required side lobe level)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 7, Filter Design Techniques (design of FIR filters by windowing, commonly used windows, the Kaiser window design method) and Chapter 10, Fourier Analysis of Signals Using the DFT (the effect of windowing)
---

A window function is a sequence $w[0], \ldots, w[N-1]$ that multiplies a block of samples before its [DFT](/discrete-fourier-transform/) is taken, or multiplies an ideal impulse response before it is used as a filter. Plain truncation is the rectangular window, which has the narrowest main lobe and the highest side lobes and so the worst [spectral leakage](/spectral-leakage/). Windows that taper smoothly to zero at both ends, such as Hann, Hamming, Blackman and Kaiser, push the side lobes far down and make them fall off faster, and pay with a wider main lobe, a smaller coherent gain and a larger noise bandwidth. No window wins on every figure, so the choice depends on whether the task needs resolution, dynamic range or amplitude accuracy.

## In plain words

Before we measure the notes in a short piece of sound, we can fade the piece in at the start and out at the end. A sharp cut makes false notes appear far from the real ones. A gentle fade removes most of them, so a quiet note next to a loud one can be heard. The price is that each real note looks a little blurred, so two notes very close together can merge. A window is the exact shape of that fade. Some shapes fade quickly and blur little but leave more false notes; others fade slowly and leave almost none but blur more. The art is picking the shape that fits the question being asked.

## The idea

**Why the shape matters.** Multiplying a block by $w$ convolves its [DTFT](/discrete-time-fourier-transform/) with the window's DTFT $W(e^{i\omega})$, so a pure tone appears as a copy of $W$ centred at its frequency. Everything about leakage is therefore a property of $W$: how wide its main lobe is, how high its side lobes are, and how fast they decay. Widths below are in DFT bins of $2\pi/N$ radians per sample.

**The cosine-sum family.** The classic windows are sums of a few cosines,

$$w[n] = \sum_{j=0}^{J} (-1)^j a_j \cos\frac{2\pi j n}{N}, \qquad n = 0, \ldots, N - 1,$$

with $a_0 = 1$ for rectangular, $(0.5, 0.5)$ for Hann, $(0.54, 0.46)$ for Hamming and $(0.42, 0.5, 0.08)$ for Blackman. Each cosine shifts the Dirichlet kernel of the rectangular window by $j$ bins, so $W$ is a short weighted sum of shifted kernels. For Hann,

$$W(e^{i\omega}) = \tfrac12 D(\omega) - \tfrac14 D\!\left(\omega - \tfrac{2\pi}{N}\right) - \tfrac14 D\!\left(\omega + \tfrac{2\pi}{N}\right),$$

and the side lobes of the three kernels largely cancel. The same identity says that windowing with Hann can be done after the DFT, as $X^{w}_k = \tfrac12 X_k - \tfrac14 X_{k-1} - \tfrac14 X_{k+1}$ with indices mod $N$.

**How each window is built.**

- *Hann* goes to zero with zero slope at both ends; its periodic extension is continuous with a continuous first derivative, so its side lobes fall like $1/\omega^3$, or $18$ dB per octave.
- *Hamming* picks $0.54/0.46$ so that the first side lobe nearly cancels. It does not reach zero at the ends, so its far side lobes fall only like $1/\omega$, as for the rectangular window, but its highest side lobe is nearly the lowest of the two-term windows: $a_0 = 0.53836$ gives $-42.94$ dB against $-42.45$ dB at $N = 64$.
- *Blackman* adds a third cosine and gets both low and fast-falling side lobes, with a main lobe $3$ bins wide on each side.
- *Kaiser* is $w[n] = I_0\!\left(\beta\sqrt{1 - r_n^2}\right)/I_0(\beta)$ with $r_n = 2n/(N-1) - 1$ and $I_0$ the modified Bessel function. The single parameter $\beta$ moves continuously along the trade-off: $\beta = 0$ is rectangular, and larger $\beta$ means lower side lobes and a wider main lobe. The half-width of its main lobe is about $\sqrt{1 + (\beta/\pi)^2}$ bins.

**The figures of merit.** For a window $w$ of length $N$:

- *First null:* the half-width of the main lobe, the distance from the peak to the first zero of $|W|$.
- *Half-power (−3 dB) and −6 dB widths:* the full width of the main lobe at those levels. Two equal tones closer than about the −6 dB width merge into one peak.
- *Peak side lobe level:* the highest side lobe relative to the peak, which sets how weak a tone can be seen next to a strong one.
- *Coherent gain:* $\frac{1}{N}\sum w[n]$, the factor by which the window scales the amplitude of a tone on a bin. For a cosine sum it is $a_0$.
- *Equivalent noise bandwidth:* $N\sum w[n]^2 / \left(\sum w[n]\right)^2$ bins, the width of a rectangular filter that passes the same white-noise power. For a cosine sum it is $\left(a_0^2 + \tfrac12\sum_{j \ge 1} a_j^2\right)/a_0^2$.
- *Scalloping loss:* $|W(e^{i\pi/N})|/|W(1)|$, the drop in amplitude for a tone halfway between two bins.

**The trade-off is forced.** A window that is short in time cannot have a spectrum concentrated in a narrow band, by the [time-frequency uncertainty](/time-frequency-uncertainty/) principle. Tapering the ends makes the window effectively shorter, which widens the main lobe. In return, the smoother the periodic extension of $w$, the faster its spectrum decays: a jump gives $1/\omega$, a jump in the first derivative gives $1/\omega^2$, a jump in the second gives $1/\omega^3$.

**Periodic and symmetric forms.** The formula above with period $N$ gives the *periodic* or DFT-even window, whose $N$-point DFT has only $J + 1$ nonzero entries on each side; it is the right form for spectral analysis. Replacing $N$ by $N - 1$ gives the *symmetric* window, with $w[n] = w[N-1-n]$, which is the right form for designing [FIR filters](/fir-filter/) with linear phase. The periodic Hann window of length $N$ is the symmetric Hann window of length $N + 1$ with its last sample, a zero, dropped. Mixing them up changes the figures slightly and destroys the exact three-bin structure of the Hann DFT.

## Examples

**The comparison table.** The figures below are measured for $N = 64$ periodic windows (Kaiser symmetric) from a direct DTFT evaluated at $64$ points per bin over $[0, \pi]$, with the −3 dB and −6 dB points refined by bisection on the same direct sum. The coherent gain and noise bandwidth are computed by the sums and agree with the closed forms to $10^{-12}$.

| window | first null (bins) | −3 dB width | −6 dB width | peak side lobe | scalloping | coherent gain | noise bandwidth |
|---|---|---|---|---|---|---|---|
| rectangular | 1 | 0.886 | 1.207 | −13.26 dB | −3.92 dB | 1 | 1.000 |
| Hann | 2 | 1.441 | 2.000 | −31.47 dB | −1.42 dB | 0.5 | 1.500 |
| Hamming | 2 | 1.303 | 1.815 | −42.45 dB | −1.75 dB | 0.54 | 1.363 |
| Blackman | 3 | 1.644 | 2.299 | −58.11 dB | −1.10 dB | 0.42 | 1.727 |
| Kaiser, $\beta = 6$ | 2.20 | 1.423 | 1.984 | −43.97 dB | −1.47 dB | 0.492 | 1.489 |
| Kaiser, $\beta = 8.6$ | 2.95 | 1.663 | 2.328 | −62.78 dB | −1.07 dB | 0.414 | 1.749 |

Sorting by −3 dB width gives rectangular, Hamming, Hann, Blackman; sorting by side lobe level from highest to lowest gives rectangular, Hann, Hamming, Blackman. The rectangular window is first in both lists: narrowest main lobe and highest side lobes. Harris's table, rounded to two digits, gives the same side lobe levels ($-13$, $-32$, $-43$, $-58$ dB), the same noise bandwidths ($1.00$, $1.50$, $1.36$, $1.73$) and −3 dB widths of $0.89$, $1.44$, $1.30$ and $1.68$; the measured Blackman width of $1.64$ is a little below the tabulated $1.68$.

**Dependence on length.** The widths in bins hardly change with $N$, and neither do most side lobe levels. Hamming's peak side lobe measures $-42.45$ dB at $N = 64$, $-42.66$ dB at $N = 256$ and $-42.67$ dB at $N = 1024$, approaching the familiar $-43$ dB; Blackman's is $-58.11$ dB at all three lengths.

**Kaiser main lobe.** For $\beta = 6$ the formula $\sqrt{1 + (\beta/\pi)^2}$ gives $2.156$ bins, which becomes $2.190$ when scaled by $N/(N-1)$ for a symmetric window spread over $N - 1$ sample intervals; the measured first null is $2.20$ at the $1/64$-bin grid. For $\beta = 8.6$ the same steps give $2.961$ against a measured $2.95$.

**Periodic against symmetric.** The symmetric Hann window of length $64$ has a −3 dB width of $1.463$ bins and a noise bandwidth of $1.524$, against $1.441$ and $1.500$ for the periodic form: it is a Hann window of length $63$ intervals measured on a grid of $64$.

**A weak tone next to a strong one.** On [spectral leakage](/spectral-leakage/) a tone $60$ dB down and $9.5$ bins from a strong off-bin tone is invisible with the rectangular window and shows as a clear peak with Hann and Blackman. The window spectra explain why: measured by the direct DTFT at $9.5$ bins from the peak, $|W|$ is $-29.18$ dB for the rectangular window, $-68.54$ dB for Hann and $-76.45$ dB for Blackman, so only the tapered windows push the strong tone's leakage below the weak tone.

## Where it is used

- **Spectrum analysis.** FFT analysers and the [periodogram](/periodogram/) apply a window to every block; the [Welch method](/welch-method/) windows overlapping segments, and Hann with $50\%$ overlap is the common default. The coherent gain is divided out to report amplitudes, and the noise bandwidth to report noise densities.
- **Spectrograms.** The [short-time Fourier transform](/short-time-fourier-transform/) slides a window along the signal; its length and shape fix the time and frequency resolution of the picture.
- **FIR filter design.** The window method multiplies the impulse response of an ideal filter by a symmetric window; the side lobes of the window become the stop-band ripple and the main lobe the transition width. The Kaiser formulas choose $\beta$ and $N$ for a required attenuation and transition band, a standard step in [digital filter design](/digital-filter-design/). Without a window the truncated ideal filter shows the [Gibbs phenomenon](/gibbs-phenomenon/).
- **Apodization in optics and spectroscopy.** In Fourier transform infrared and NMR spectroscopy the recorded interferogram or free induction decay is tapered before the transform to suppress ringing around sharp lines; in optics an aperture with a tapered transmission lowers the side rings of a diffraction pattern.
- **Antenna and sonar arrays,** where tapering the weights of the elements lowers the side lobes of the beam pattern by the same mathematics, with the element index in place of time.

## References
