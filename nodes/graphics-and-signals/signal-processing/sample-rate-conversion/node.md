---
tag: 7C279J
kind: problem
slug: sample-rate-conversion
name: Sample-rate conversion
aliases:
- decimation and interpolation
area: graphics-and-signals/signal-processing
level: core
summary: "Given a one-dimensional signal sampled at one rate, compute its samples at another rate as if the underlying band-limited signal had been sampled there, without aliasing or images."
prereqs: [sampling-theorem, aliasing, fir-filter]
see_also: [polyphase-resampling, polyphase-decomposition, sinc-interpolation, image-resampling, nyquist-rate, signal-reconstruction, digital-filter-design, filter-bank]
sources:
  - book: isbn:9780136051626
    title: Ronald E. Crochiere and Lawrence R. Rabiner, Multirate Digital Signal Processing, Prentice-Hall, 1983
    locator: Chapter 2, Basic Principles of Sampling and Sampling Rate Conversion (decimation by M, interpolation by L and conversion by L/M); chapter level locator
  - book: isbn:9780136057185
    title: P. P. Vaidyanathan, Multirate Systems and Filter Banks, Prentice Hall, 1993
    locator: Chapter 4, Multirate Systems Fundamentals (decimators, interpolators, fractional rate change and aliasing); chapter level locator
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 4.6, Changing the Sampling Rate Using Discrete-Time Processing (4.6.1 reduction by an integer factor, 4.6.2 increase by an integer factor, 4.6.4 change by a noninteger factor)
  - paper: "Ronald W. Schafer and Lawrence R. Rabiner, A Digital Signal Processing Approach to Interpolation, Proceedings of the IEEE 61(6), June 1973, pages 692 to 702"
    locator: interpolation with FIR filters, and rate change by a rational factor as an integer increase followed by an integer decrease
---

Sample-rate conversion is the problem to change the sampling rate of a discrete-time signal. The input is a sequence $x[n]$ taken at the rate $f_{in}$, and the output is the sequence at a new rate $f_{out}$ that sampling the same band-limited signal at $f_{out}$ would give. Reducing the rate by an integer factor is decimation, raising it is interpolation, and a general change combines the two. The hard part is not the arithmetic of the new sample times but the filtering: a lower rate needs a low-pass filter before the samples are dropped, or the high frequencies [alias](/aliasing/), and a higher rate needs a filter that removes the images of the spectrum. Typical cases are audio between 44.1 kHz and 48 kHz, speech between 8 kHz and 16 kHz, and channels in software radio. This page is about one-dimensional signals; the two-dimensional problem for pictures is [image resampling](/image-resampling/), which has other filters and other quality criteria. Frequencies on this page are $\omega$ in radians per sample, $\omega \in [-\pi, \pi]$, at the rate that the text names, and $f$ in hertz.

## In plain words

A recording is a list of numbers measured at a fixed pace, for example 44100 times per second. Another device wants 48000 numbers per second. You must invent the numbers at the new instants, which fall between the old ones.

The best answer is the value of the smooth signal that the old numbers describe. The sampling theorem says how to rebuild that signal from the numbers, as long as it has no tones that are too fast for the pace. Going to a slower pace has one more trap: tones that the slow pace cannot hold do not disappear, they come back as false low tones. So you must remove them before you take fewer numbers.

## Definition

**Input.** A sequence $x[n]$, $n \in \mathbb{Z}$, of samples $x[n] = x_c(n/f_{in})$ of a continuous signal $x_c$ whose spectrum is zero above $f_{in}/2$, as in the [sampling theorem](/sampling-theorem/). An output rate $f_{out} > 0$. Let $R = f_{out}/f_{in}$.

**Ideal output.** Let $\tilde x_c$ be $x_c$ after an ideal low-pass filter with cutoff $\min(f_{in}, f_{out})/2$. The ideal output is $y[m] = \tilde x_c(m/f_{out})$. With $\operatorname{sinc}(t) = \sin(\pi t)/(\pi t)$ and $\rho = \min(1, R)$, it is

$$y[m] = \sum_{n} x[n]\, \rho\, \operatorname{sinc}\!\big(\rho\,(m/R - n)\big).$$

For $R \ge 1$ this is the band-limited [sinc interpolation](/sinc-interpolation/) of $x$ at the times $m/R$. For $R < 1$ the kernel is wider and lower, which removes the band from $f_{out}/2$ to $f_{in}/2$ that the new rate cannot hold.

**Practical goal.** The ideal kernel has infinite length, so a real converter uses a filter of finite length and accepts a specification: a pass band up to some $f_p < \min(f_{in}, f_{out})/2$ with ripple $\delta_p$, a stop band from $\min(f_{in}, f_{out})/2$ (or a little above, if some aliasing into the transition band is allowed) with attenuation $\delta_s$, and a bound on the delay. Among the converters that meet it, the goal is the lowest cost per output sample.

## Variants

- **Decimation by an integer $M$.** $f_{out} = f_{in}/M$. Filter with cutoff $\pi/M$, then keep every $M$-th sample.
- **Interpolation by an integer $L$.** $f_{out} = L f_{in}$. Insert $L - 1$ zeros after each sample, then filter with cutoff $\pi/L$ and gain $L$ at the high rate.
- **Rational ratio $L/M$.** $f_{out}/f_{in} = L/M$ in lowest terms. Upsample by $L$, filter once with cutoff $\pi/\max(L, M)$ at the high rate, and downsample by $M$.
- **Arbitrary or varying ratio.** The ratio is irrational, very close to 1 with a large $L$ and $M$, or it drifts, as between two devices with separate clocks. Each output needs a delay that is a fraction of a sample, computed for each output.
- **Fractional delay.** The same rate, with all samples shifted by a fraction of a sample. It is the core of the arbitrary ratio case.
- **Offline or streaming.** A whole signal can be converted by a transform of its full length. A stream needs a causal method with a bounded delay and memory.

## Examples

**Decimation without a filter aliases.** Take $x[n] = \cos(0.75\pi n)$ and keep every second sample. Then $y[n] = x[2n] = \cos(1.5\pi n) = \cos(2\pi n - 0.5\pi n) = \cos(0.5\pi n)$ for every integer $n$. A tone at $0.75\pi$ at the input rate, which is $3/8$ of $f_{in}$, comes out as a tone at $0.5\pi$ at the output rate, that is $f_{in}/8$. It is a new tone that was not in the input. A low-pass filter with cutoff $\pi/2$ before the downsampler removes it.

**CD audio to 48 kHz.** The ratio is $48000/44100 = 160/147$, because $\gcd(48000, 44100) = 300$. So $L = 160$ and $M = 147$, and the three-stage method would filter at the rate $44100 \cdot 160 = 7.056$ MHz. The [polyphase resampler](/polyphase-resampling/) computes the same output with about $K/160$ multiplies per output sample for a filter of $K$ taps, about 20 for a filter with 10 zero crossings on each side.

**Speech from 48 kHz to 16 kHz.** This is decimation by 3. The filter must pass the speech band and reject everything above 8 kHz, that is $\omega \ge \pi/3$ at the input rate. With [polyphase decomposition](/polyphase-decomposition/) it runs at 16 kHz, at one third of the direct cost.

## Known algorithms

| method | ratio | cost per output sample | notes |
|---|---|---|---|
| decimator or interpolator in [polyphase](/polyphase-decomposition/) form | integer $M$ or $L$ | $K$ (decimator) or about $K/L$ (interpolator) | exactly equal to the direct form |
| [polyphase resampler](/polyphase-resampling/) | rational $L/M$ | about $K/L$ | the standard method for fixed ratios |
| multistage conversion | rational, with large $L$ or $M$ | often lower than one stage | each stage has a wide transition band and a short filter |
| cascaded integrator and comb (CIC) filters | integer, large | no multiplies | poor pass band; followed by a compensation filter |
| windowed [sinc interpolation](/sinc-interpolation/) with a table of phases | arbitrary, varying | about the number of zero crossings, plus the interpolation of the phases | used in audio software |
| polynomial fractional delay filters (often called the Farrow structure) | arbitrary, varying | a few short filters and a polynomial evaluation | taps are polynomials in the fractional delay |
| linear or cubic interpolation between samples | arbitrary | 2 or 4 | cheap; aliasing and loss at high frequencies |
| zero padding or truncation of the [DFT](/discrete-fourier-transform/) | rational | $O(\log N)$ per sample for $N$ samples | offline; treats the signal as periodic |

The filter in each of these methods is a problem of [digital filter design](/digital-filter-design/), usually a windowed sinc or a [Parks-McClellan](/parks-mcclellan-algorithm/) design.

## Bounds

- **Bandwidth.** The output can hold frequencies only up to $f_{out}/2$, the [Nyquist rate](/nyquist-rate/) limit of the new rate. When $f_{out} < f_{in}$, the band from $f_{out}/2$ to $f_{in}/2$ is lost, and no method can recover it.
- **No exact finite method.** The ideal kernel is a sinc of infinite length, so every converter with a finite filter has a transition band and a finite stop band attenuation.
- **Filter length.** For fixed ripples, the length of the filter at the high rate grows in proportion to $\max(L, M)$ divided by the relative width of the transition band. The work per output sample of a polyphase converter is then about the length of one phase, which does not grow with $L$ for $L \ge M$.
- **Delay.** A linear phase filter of $K$ taps at the high rate delays the signal by $(K - 1)/2$ high-rate samples. A shorter delay needs a filter that is not linear phase.

## Reductions

- **Rational conversion to filtering.** Conversion by $L/M$ is upsampling by $L$, one FIR filter at the high rate and downsampling by $M$. With the noble identities and [polyphase decomposition](/polyphase-decomposition/), it is a periodically time varying filter at the low rate.
- **Arbitrary conversion to fractional delay.** Each output $y[m]$ is the input delayed by the fractional part of $m/R$ and read at the integer part, so the problem reduces to fractional delay filtering with a delay that changes from sample to sample.
- **Conversion to reconstruction and sampling.** In theory, rebuild the continuous signal by [signal reconstruction](/signal-reconstruction/) and sample it again. The digital methods do the same in one step, without the continuous signal.
- **Images.** Separable [image resampling](/image-resampling/) applies a one-dimensional rate change to rows and then to columns, but with short kernels chosen for the look of edges rather than for a frequency specification.

## Applications

- Digital audio: mixing sources at 44.1, 48 and 96 kHz, and playback on hardware with a fixed rate.
- Telephony and speech coding: conversion between 8 kHz, 16 kHz and higher rates.
- Software radio: reducing a wide band to one channel, and matching the symbol rate of a receiver to its clock.
- Oversampling converters between analog and digital signals, whose output is decimated to the final rate.
- [Filter banks](/filter-bank/) and subband coding, which decimate each band.

## References
