---
tag: QBTGMJ
kind: definition
slug: nyquist-rate
name: Nyquist rate
aliases:
- Nyquist frequency
area: graphics-and-signals/signal-processing
level: core
summary: "The Nyquist rate of a signal band-limited to B Hz is 2B samples per second; the related Nyquist frequency fs/2 is half the rate of a given sampler."
prereqs: [sampling-theorem]
see_also: [aliasing, sinc-interpolation, signal-reconstruction, sample-rate-conversion, antialiasing, discrete-time-fourier-transform, compressed-sensing]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 4, Sampling of Continuous-Time Signals (the Nyquist frequency and the Nyquist rate in the statement of the sampling theorem, and changing the sampling rate)
  - paper: doi:10.1109/JRPROC.1949.232969
    title: Claude E. Shannon, Communication in the Presence of Noise, Proceedings of the IRE 37(1), 1949
    locator: Section II, The Sampling Theorem (the interval 1/(2W) between samples, which Shannon calls the Nyquist interval)
  - paper: doi:10.1109/T-AIEE.1928.5055024
    title: Harry Nyquist, Certain Topics in Telegraph Transmission Theory, Transactions of the AIEE 47(2), 1928
    locator: pp. 617 to 644 (the result that 2W independent signal elements per second fit in a band of W cycles per second, the origin of the name)
---

The Nyquist rate of a band-limited signal is twice its highest frequency: if the spectrum is zero for $|f| \ge B$ Hz, the Nyquist rate is $2B$ samples per second. By the [sampling theorem](/sampling-theorem/), sampling faster than this rate keeps all the information in the signal, and sampling slower causes [aliasing](/aliasing/). The *Nyquist frequency* is a different quantity with a similar name: it belongs to the sampler, not to the signal, and is half the sampling rate, $f_s/2$.

## Definition

**Units.** Frequencies are in Hz and sampling rates in samples per second. The spectrum of $x$ is $X(f) = \int x(t) e^{-2\pi i f t} dt$.

**Definition (Nyquist rate).** Let $x$ be band-limited, and let $B = \inf\{b > 0 : X(f) = 0 \text{ for almost every } |f| > b\}$ be its *bandwidth*, the highest frequency present. The Nyquist rate of $x$ is

$$f_N = 2B.$$

The *Nyquist interval* is $1/(2B)$, the largest sample spacing that the theorem allows.

**Definition (Nyquist frequency).** For a sampler with rate $f_s$, the Nyquist frequency is $f_s/2$. It is the edge of the baseband $[-f_s/2, f_s/2)$: every frequency above it has an alias below it. In the normalized frequency of the [DTFT](/discrete-time-fourier-transform/), $\omega = 2\pi f/f_s$ rad per sample, the Nyquist frequency is $\omega = \pi$, or $0.5$ cycles per sample. Some filter design software normalizes frequencies so that the Nyquist frequency is $1$.

**The two notions together.** Sampling at $f_s$ preserves $x$ when its band lies below the Nyquist frequency, $B < f_s/2$, or, equivalently, when $f_s$ is above the Nyquist rate, $f_s > 2B$. The *oversampling ratio* is $f_s/(2B)$. The inequality must be strict for a signal that may contain a sinusoid at $B$: $\sin(2\pi B t)$ sampled at exactly its Nyquist rate gives only zeros. For signals of finite energy, sampling at exactly $2B$ also suffices, as explained on the [sampling theorem](/sampling-theorem/) page.

**In telegraphy.** In data transmission, the *Nyquist rate* of a channel of bandwidth $W$ Hz is $2W$ symbols per second, the highest rate at which independent pulses can be sent without intersymbol interference. This is the result of Nyquist's 1928 paper, and the sampling rate later took its name from it.

## Examples and non-examples

**Telephone speech.** Classic telephony keeps the band $300$ to $3400$ Hz. The highest frequency is $3400$ Hz, so the Nyquist rate is $6800$ samples per second. The standard rate $8000$ samples per second gives the Nyquist frequency $4000$ Hz and the margin $3400$ to $4000$ Hz for the analog anti-aliasing filter.

**Compact disc audio.** Human hearing reaches about $20$ kHz, so the Nyquist rate of audio limited to $20$ kHz is $40$ kHz. The compact disc rate is $44.1$ kHz, with Nyquist frequency $22.05$ kHz and oversampling ratio $1.1025$.

**A tone at the Nyquist frequency.** At $f_s = 48$ kHz the Nyquist frequency is $24$ kHz. A $24$ kHz cosine gives the samples $(-1)^n \cos\varphi$, which lose its phase, and a $24$ kHz sine gives zeros. A $25$ kHz tone appears at $48 - 25 = 23$ kHz.

**A band-pass signal.** A radio signal occupying $f_L = 10.0$ MHz to $f_H = 10.2$ MHz has the Nyquist rate $2 f_H = 20.4$ MHz. Because the band is narrow, it can also be sampled at much lower rates without overlap of the shifted bands (see bandpass sampling on [aliasing](/aliasing/)); the lowest is $2(f_H - f_L) = 0.4$ MHz, possible here because $f_H/(f_H - f_L) = 51$ is an integer. So the Nyquist rate in the sense of the definition, $2f_H$, is an upper bound on the rate needed, not the least rate, for signals whose spectrum has gaps. For such signals H. J. Landau showed that the least average rate is the total measure of the spectral support, here $2 \times 0.2$ MHz.

**Non-example: a square wave.** A square wave has harmonics at every odd multiple of its fundamental, with amplitudes falling like $1/k$. Its spectrum is not zero above any frequency, so it has no Nyquist rate, and every sampling rate aliases some of its harmonics.

**Non-example: a pulse of finite duration.** A signal that is zero outside a finite time interval and not identically zero is never band-limited, because a band-limited signal of finite energy is an entire function of time. It has no Nyquist rate, and in practice one chooses the rate above which the remaining spectrum is below the noise.

**Non-example: the sampler's rate.** The Nyquist rate is not a property of the converter. A converter running at $96$ kHz has the Nyquist frequency $48$ kHz; the Nyquist rate of the signal it records depends on what is fed to it.

## Related definitions

- **Sampling rate.** The rate $f_s$ at which samples are taken; the period is $T = 1/f_s$. The [sampling theorem](/sampling-theorem/) compares $f_s$ with the Nyquist rate.
- **Baseband.** The interval $[-f_s/2, f_s/2)$, which contains one representative of each class of aliases.
- **Undersampling and oversampling.** Sampling below the Nyquist rate (on purpose in bandpass sampling, by mistake otherwise) and above it. Oversampling relaxes the anti-aliasing filter and allows short reconstruction kernels; [sample-rate conversion](/sample-rate-conversion/) moves between rates.
- **Anti-aliasing filter.** The low-pass filter before a sampler that removes content above the Nyquist frequency; in rendering the same role is played by the methods on [antialiasing](/antialiasing/).
- **Cardinal series.** The sinc series that rebuilds a signal from samples taken at or above its Nyquist rate, computed by [sinc interpolation](/sinc-interpolation/).
- **Sub-Nyquist sampling.** Recovery from fewer samples than the Nyquist rate, using structure such as sparsity, as in [compressed sensing](/compressed-sensing/).

## References
