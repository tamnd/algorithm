---
tag: YMQQ6D
kind: algorithm
slug: moving-target-indication
name: Moving target indication
aliases:
- MTI
- MTI canceller
area: communications/radar-waveforms
level: core
summary: "Subtracts the returns of consecutive pulses at each range with the binomial filter (1 - 1/z)^(L-1), which removes stationary clutter and leaves blind speeds at multiples of lambda PRF / 2."
model: real-ram
complexity:
  vars: {P: the number of pulses, M: the number of range bins, L: the number of pulses in the canceller}
  time: {worst: Θ(L P M), average: Θ(L P M), best: Θ(L P M)}
  space: {extra: Θ(L)}
properties: {deterministic: true, linear: true, online: true, exact_for_integer_input: true, removes_zero_doppler: true}
prereqs: [fir-filter, binomial-coefficient]
see_also: [range-doppler-processing, space-time-adaptive-processing, cfar-detection, discrete-convolution, doppler-spread, autocorrelation, iir-filter, pulse-compression]
sources:
  - book: isbn:9780072881387
    title: "Merrill I. Skolnik, Introduction to Radar Systems, third edition, McGraw-Hill, 2001"
    locator: "Chapter 3, MTI and Pulse Doppler Radar (the delay-line canceller, blind speeds, staggered PRFs and the improvement factor)"
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 5, Section 5.2 (pulse cancellers, their frequency response and blind speeds in 5.2.1, and the improvement factor in 5.2.4 and 5.2.5)"
---

Moving target indication (MTI) removes the echo of stationary clutter, such as ground, buildings and sea, from the returns of a pulsed radar. At each range bin it takes the samples of $L$ consecutive pulses and forms the weighted difference with the binomial weights of $(1 - z^{-1})^{L-1}$: $x[p] - x[p-1]$ for the two-pulse canceller and $x[p] - 2x[p-1] + x[p-2]$ for the three-pulse canceller. Clutter that does not move gives the same sample from pulse to pulse and is removed exactly. A target with a Doppler shift $f_d$ changes phase from pulse to pulse and passes with the gain $(2|\sin(\pi f_d / \mathrm{PRF})|)^{L-1}$. Targets at the blind speeds $n \lambda\, \mathrm{PRF}/2$ are removed too. MTI does not measure the speed; [range-Doppler processing](/range-doppler-processing/) does that with a DFT over the pulses.

## In plain words

A radar sends the same pulse again and again. A building gives the same echo every time. A car moves a little between pulses, so its echo comes back with a different phase each time. If you subtract the echo of the previous pulse from the echo of this pulse, the building cancels and the car does not. Subtracting twice (the difference of differences) removes clutter whose echo changes slowly, as well, and gives a deeper notch at zero speed. The cost is one subtraction per pulse and range bin per stage. If the car moves exactly a half wavelength, or a multiple of it, between pulses, its echo has the same phase each time and it cancels too: that speed is blind.

## The problem

The input is a $P \times M$ array $x[p][r]$ of complex baseband samples, pulse $p = 0, \dots, P-1$ (slow time) and range bin $r = 0, \dots, M-1$ (fast time), and the canceller length $L \ge 1$. The output is the $(P - L + 1) \times M$ array

$$y[p][r] = \sum_{i=0}^{L-1} w[i]\, x[p - i][r], \qquad w[i] = (-1)^i \binom{L-1}{i},$$

for $p = L - 1, \dots, P - 1$. The weights are $(1, -1)$ for $L = 2$, $(1, -2, 1)$ for $L = 3$ and $(1, -3, 3, -1)$ for $L = 4$. The pulse repetition frequency is PRF and the wavelength is $\lambda$, and a target of radial speed $v$ has the Doppler shift $f_d = 2v/\lambda$ and the normalized Doppler $f = f_d/\mathrm{PRF}$.

## The algorithm

```pseudo id=main
MTI-CANCEL(x[0..P-1][0..M-1], L)
L1  w[i] <- (-1)^i * C(L - 1, i) for i = 0, ..., L - 1      ▷ binomial weights
L2  for p <- L - 1 to P - 1
L3      for r <- 0 to M - 1
L4          y[p - L + 1][r] <- sum over i = 0, ..., L - 1 of w[i] * x[p - i][r]
L5  return y
```

Line L1 builds the weights from one row of Pascal's triangle with alternating signs. Lines L2 and L3 visit each output pulse and range bin. Line L4 is a short [FIR filter](/fir-filter/) along slow time: each range bin is filtered on its own, and the filter reads only the current pulse and the $L - 1$ pulses before it. Line L2 starts at $p = L - 1$, because the first $L - 1$ pulses do not have enough earlier pulses. In a real radar the loop over $p$ runs as the pulses arrive, and $L - 1$ earlier pulses are kept in memory.

## Example

Take $P = 5$ pulses and $M = 3$ range bins. Bin 0 holds clutter of amplitude 5, bin 2 holds clutter of amplitude 3, and bin 1 holds clutter of amplitude 5 plus a target $2 j^p$, which has $f = 1/4$ (the target turns a quarter cycle from pulse to pulse). So $x[p] = (5, 5 + 2j^p, 3)$.

| $p$ | $x[p][1]$ | two-pulse $y$ | three-pulse $y$ |
|---|---|---|---|
| 0 | $7$ | | |
| 1 | $5 + 2j$ | $-2 + 2j$ | |
| 2 | $3$ | $-2 - 2j$ | $3 - 2(5 + 2j) + 7 = -4j$ |
| 3 | $5 - 2j$ | $2 - 2j$ | $4$ |
| 4 | $7$ | $2 + 2j$ | $4j$ |

In bins 0 and 2 every output is 0: the clutter is removed exactly. In bin 1 the two-pulse output has magnitude $2\sqrt{2} = 2 \cdot 2\sin(\pi/4)$ and the three-pulse output has magnitude $4 = 2 \cdot (2\sin(\pi/4))^2$, as the response formula says. The clutter of amplitude 5 in bin 1 is gone in both.

## Correctness

By the binomial theorem, $\sum_i w[i] z^{-i} = (1 - z^{-1})^{L-1}$, so line L4 applies the two-pulse difference $L - 1$ times. For an input $c\, e^{j 2\pi f p}$ the output is the input times $H(f) = (1 - e^{-j 2\pi f})^{L-1}$, and $|1 - e^{-j 2\pi f}| = 2|\sin(\pi f)|$. So the gain is $(2|\sin(\pi f)|)^{L-1}$, which is 0 exactly at integer $f$: the blind speeds $v_n = n\lambda\,\mathrm{PRF}/2$. A difference lowers the degree of a polynomial by one, so $L - 1$ differences remove any clutter sequence that is a polynomial in $p$ of degree at most $L - 2$. For wide-sense stationary clutter with normalized autocorrelation $\rho_k$, the improvement factor (the gain in signal to clutter ratio averaged over the target Doppler) is $\sum_i w[i]^2 / \sum_{i,m} w[i] w[m] \rho_{|i-m|}$. The [correctness proof](proofs/correctness.md) gives the full arguments.

## Complexity

**Time.** Line L4 does $L$ multiplications and additions for each of the $(P - L + 1) M$ outputs, so the time is $\Theta(L P M)$ for $L \le P/2$, in every case. With the cascade form ($L - 1$ passes of the two-pulse difference) only additions are needed. $L$ is 2 or 3 in practice, so the cost is a few operations per sample.

**Space.** $\Theta(L)$ for the weights, beyond the input and the output. A real-time canceller stores $L - 1$ earlier pulses, $\Theta(L M)$ samples.

## Properties

- **Exact cancellation of fixed clutter (theorem).** A constant at a range bin gives 0 for every $L \ge 2$, and a polynomial of degree at most $L - 2$ gives 0. With integer input the output is exact.
- **The response (theorem).** $|H(f)| = (2|\sin(\pi f)|)^{L-1}$, with $|H(f)|^2 = 4\sin^2(\pi f)$ for two pulses and $16\sin^4(\pi f)$ for three. The largest gain, $2^{L-1}$, is at $f = 1/2$.
- **Blind speeds (theorem).** $v_n = n\lambda\,\mathrm{PRF}/2$. At 3 GHz ($\lambda = 0.0999$ m) with a PRF of 1 kHz, the first blind speed is 49.97 m/s.
- **The improvement factor (closed form).** $I = 1/(1 - \rho_1)$ for two pulses and $I = 6/(6 - 8\rho_1 + 2\rho_2)$ for three. For a Gaussian clutter spectrum, $\rho_k = e^{-2\pi^2 \sigma_c^2 k^2/\mathrm{PRF}^2}$. With $\sigma_c = 10$ Hz and a PRF of 1 kHz, $I$ is 27.05 dB for two pulses and 51.10 dB for three; with $\sigma_c = 20$ Hz, 21.04 dB and 39.10 dB. A wider clutter spectrum, from wind or from the motion of the radar, lowers $I$ quickly. For AR(1) clutter with $\rho_k = 0.9^k$, $I$ is 10 and 14.29, and the tests measure these values by simulation within 6 percent.
- **Linear and time-invariant along slow time.** MTI commutes with [pulse compression](/pulse-compression/), so the two can run in either order.

## Variants and improvements

- **Staggered PRF.** Change the interval between pulses in a fixed pattern. The blind speeds of the different intervals do not coincide, so the first common blind speed moves far above the target speeds. The filter weights then change from pulse to pulse.
- **Recursive cancellers.** An [IIR filter](/iir-filter/) with feedback gives a sharper notch and a flatter passband than the binomial FIR, at the cost of a long transient.
- **Clutter-matched weights.** Choose $w$ to maximize the improvement factor for a known $\rho_k$. With the target Doppler averaged as above, it is an eigenvector problem: the best $w$ is the eigenvector of the clutter correlation matrix with the smallest eigenvalue.
- **Moving target detection (MTD).** Follow a short canceller with a bank of Doppler filters (a short DFT over the pulses) and a CFAR in each filter. This is between MTI and full [range-Doppler processing](/range-doppler-processing/).
- **Airborne MTI.** For a moving radar, the clutter Doppler depends on the angle. A fixed notch at zero Doppler no longer fits, and [space-time adaptive processing](/space-time-adaptive-processing/) filters jointly in angle and Doppler.

## When to use it

Use MTI in a ground-based radar that must see moving targets against strong fixed clutter, when only a few pulses fall on each target, or when the hardware must be simple. Use [range-Doppler processing](/range-doppler-processing/) when you have many pulses per dwell and want the speed of the target as well, and STAP when the radar moves. MTI is usually followed by a [CFAR detector](/cfar-detection/) on the canceller output.

## Pitfalls

- **Weights that are not binomial in line L1.** The weights $(1, -1, 1)$ look like a three-pulse canceller but sum to 1, so they pass fixed clutter with gain 1. The weights must sum to 0 to null zero Doppler, and the binomial weights also null the first $L - 2$ derivatives.
- **Starting the loop of line L2 at $p = 0$.** Then line L4 reads $x[-1]$, $x[-2]$, and so on. In C this reads outside the array. In Python a negative index silently reads the last pulses, and the first outputs mix the start and the end of the dwell. The first $L - 1$ outputs are not valid and must not reach the detector.
- **Filtering across range in line L4.** The difference is along the pulse index $p$ at a fixed range bin $r$. Subtracting adjacent range bins of one pulse is a high-pass filter in range, and it does not remove clutter.
- **Blind speeds.** A target at a blind speed disappears. With one PRF, a 3 GHz radar at 1 kHz is blind at 49.97 m/s, 99.93 m/s and so on, which are common aircraft speeds. Use staggered or multiple PRFs.
- **Amplitude and phase instability.** The cancellation is exact only if the transmitter phase, the timing and the receiver gain are the same for every pulse. A phase jitter of $\epsilon$ radians leaves a residue of about $\epsilon^2$ of the clutter power, which limits $I$ in practice to the stability of the radar.
- **Clutter spectral width.** The improvement factor falls fast as the clutter spreads in Doppler. Going from $\sigma_c = 10$ Hz to 20 Hz costs 6 dB for two pulses and 12 dB for three.

## Implementations

## History

Pulse cancellers are among the oldest radar signal processing methods. Early MTI radars used analog delay lines, for example mercury or quartz lines, to hold the echo of one pulse until the next one arrived, so that the two could be subtracted. Digital memories later replaced the delay lines and made higher order and staggered cancellers easy to build. Skolnik and Richards describe the canceller, its blind speeds and its improvement factor in their textbooks.

## References
