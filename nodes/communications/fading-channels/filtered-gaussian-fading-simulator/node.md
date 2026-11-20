---
tag: K4JBF8
kind: algorithm
slug: filtered-gaussian-fading-simulator
name: Filtered Gaussian noise fading simulator
aliases:
- Smith fading simulator
- IFFT fading generator
area: communications/fading-channels
level: core
summary: "Weights N independent complex Gaussian samples by the square root of the Doppler spectrum of Clarke's model and takes one inverse DFT, which gives N samples of exactly Gaussian Rayleigh fading."
model: real-ram
complexity:
  vars: {N: the number of output samples}
  time: {worst: O(N log N)}
  space: {extra: O(N)}
properties: {randomized: true, exactly_gaussian: true, circularly_stationary: true, exact_clarke_autocorrelation: false}
history:
  year: 1975
  people: [J. I. Smith, David J. Young, Norman C. Beaulieu]
  note: "Smith (1975) shaped Gaussian noise in the frequency domain and used two inverse transforms, one for each quadrature. Young and Beaulieu (2000) used one inverse DFT of complex noise and gave a filter with a finite edge bin."
prereqs: [clarke-model, inverse-fft, rayleigh-fading-channel]
see_also: [clarke-model, jakes-fading-simulator, zheng-xiao-fading-simulator, inverse-fft, power-spectral-density, wiener-khinchin-theorem, autoregressive-model, fir-filter]
sources:
  - paper: doi:10.1109/T-VT.1975.23600
    title: "J. I. Smith, A computer generated multipath fading simulation for mobile radio, IEEE Transactions on Vehicular Technology 24(3), 1975, pages 39 to 40"
    locator: "the frequency-domain method with Gaussian noise shaped by the Doppler spectrum"
  - paper: doi:10.1109/26.855519
    title: "D. J. Young and N. C. Beaulieu, The generation of correlated Rayleigh random variates by inverse discrete Fourier transform, IEEE Transactions on Communications 48(7), 2000, pages 1114 to 1127"
    locator: "the IDFT method with one transform and the filter for Clarke's spectrum"
  - book: isbn:9780130422323
    title: "T. S. Rappaport, Wireless Communications: Principles and Practice, 2nd edition, Prentice Hall, 2002"
    locator: "Section 5.7.2, simulation of the Clarke and Gans fading model"
---

The filtered Gaussian noise simulator makes $N$ samples of a fading gain $h[n]$ for [Clarke's model](/clarke-model/): it multiplies $N$ independent complex Gaussian samples by a filter $F[k]$ whose square follows the Doppler spectrum, and takes one [inverse DFT](/inverse-fft/). Clarke's model is the target, the autocorrelation $\Omega J_0(2\pi f_D\tau)$; the [Jakes simulator](/jakes-fading-simulator/) and the [Zheng-Xiao simulator](/zheng-xiao-fading-simulator/) add sinusoids, so their output is Gaussian only approximately, while the output here is exactly Gaussian. Its autocorrelation is the inverse DFT of the sampled spectrum, which is close to $J_0$ but not equal to it.

## In plain words

Clarke's model says how strong each Doppler frequency is in the fading signal: a little at zero and most at the edges, near the largest Doppler shift. This simulator starts with pure random noise in the frequency domain, a separate random number for each frequency bin. It makes each number larger or smaller to match the strength that the model gives to that bin, and leaves the bins outside the Doppler band empty. One inverse Fourier transform then turns the shaped noise into a time signal. The result is random noise that changes at the speed of the Doppler, with the correct Rayleigh distribution at each time. The edge bin needs special care, because the model gives it an infinite peak.

## The problem

The input is the number of samples $N$, the normalized Doppler $f_m = f_D/f_s$ (the maximum Doppler shift over the sample rate), the mean power $\Omega$ and a source of random numbers. The output is $N$ samples $h[0], \ldots, h[N-1]$ spaced by $1/f_s$. The goal is a circular complex Gaussian sequence with $E|h[n]|^2 = \Omega$ and $E[h[n+d]\overline{h[n]}]$ close to $\Omega J_0(2\pi f_m d)$, so that the envelope is Rayleigh at each time and the time correlation is that of flat, time-correlated fading. The simulator gives the channel only; the receiver's CSIR or CSIT is set by the simulation that uses it.

## The algorithm

```pseudo id=main
FILTERED-GAUSSIAN(N, f_m, Ω, rng)
L1  k_m ← ⌊N f_m⌋                                   ▷ the last bin inside the Doppler band; need 2 ≤ k_m < N/2
L2  F[k] ← √(1 / (2√(1 - (k / (N f_m))²)))  for k = 1 .. k_m - 1
L3  F[k_m] ← √((k_m/2) (π/2 - arcsin((k_m - 1)/k_m)))   ▷ the area of the spectrum over the edge bin
L4  F[N - k] ← F[k]  for k = 1 .. k_m;  all other F[k] ← 0
L5  X[k] ← F[k] G[k], with G[k] independent CN(0, 1),  for k = 0 .. N-1
L6  y ← IDFT(X)                                      ▷ y[n] = (1/N) Σₖ X[k] e^{j2πkn/N}
L7  return h[n] = N √(Ω / Σₖ F[k]²) · y[n]  for n = 0 .. N-1
```

Lines L1 to L4 sample the Doppler spectrum $S(f) \propto 1/\sqrt{1 - (f/f_D)^2}$ at the bin frequencies $k f_s/N$, positive bins at $k$ and negative bins at $N - k$. The spectrum is infinite at $f = f_D$, so line L3 replaces the edge sample by the integral of the spectrum over the last bin, $\int_{k_m - 1}^{k_m} \frac{dk}{2\sqrt{1 - (k/k_m)^2}}$ with $N f_m$ replaced by $k_m$. Line L5 draws the random input; line L6 is one inverse DFT, computed by an FFT in practice. Line L7 scales the output to the mean power $\Omega$.

## Example

Take $N = 128$ and $f_m = 1/16$, so $k_m = 8$. The filter squares are $F[1]^2 = 0.5039$, rising to $F[7]^2 = 1/(2\sqrt{1 - 49/64}) = 1.0328$, and the edge bin has $F[8]^2 = 4(\pi/2 - \arcsin(7/8)) = 2.0214$. Bins 9 to 119 are 0, and bins 120 to 127 mirror bins 8 to 1.

The autocorrelation of the output, $r[d] = \Omega \sum_k F[k]^2\cos(2\pi k d/N) / \sum_k F[k]^2$, is exact and can be compared with Clarke's model. For $N = 256$ and $f_m = 1/8$, so $k_m = 32$, with $\Omega = 1$:

| $f_D\tau$ | 0.125 | 0.25 | 0.375 | 0.5 | 0.75 | 1.0 | 1.5 | 2.0 |
|---|---|---|---|---|---|---|---|---|
| $r$ | 0.8439 | 0.4464 | -0.0154 | -0.3459 | -0.2646 | 0.2454 | -0.2269 | 0.1848 |
| $J_0(2\pi f_D\tau)$ | 0.8516 | 0.4720 | 0.0255 | -0.3042 | -0.2659 | 0.2203 | -0.1812 | 0.1575 |

The difference is below 0.05 up to $f_D\tau = 1$. It shrinks slowly as the band gets more bins: at $f_D\tau = 0.375$ with $f_m = 1/16$, it is 0.105, 0.064, 0.041 and 0.027 for $k_m = 8$, 16, 32 and 64. In a Monte Carlo run of 60 blocks of $N = 128$ samples with $f_m = 1/8$, the sample autocorrelation agrees with $r[d]$ within $0.1\,\Omega$.

## Correctness

**Claim.** The output is a circular complex Gaussian vector. For every $n$ and $d$, with indices modulo $N$, $E[h[n+d]\overline{h[n]}] = r[d]$ as above, $E|h[n]|^2 = \Omega$, the quadratures each have the autocorrelation $r[d]/2$, and their cross-correlation is 0. This is a theorem. That $r[d]$ is close to $\Omega J_0(2\pi f_m d)$ for $d$ well below $N$ is a measurement, as in the table.

**Key step.** The output is a linear map of independent $CN(0, 1)$ inputs, so it is jointly circular Gaussian, and $E[h[n+d]\overline{h[n]}] = (c^2/N^2)\sum_k F[k]^2 e^{j2\pi kd/N}$ depends on $d$ only. Because $F[N - k] = F[k]$, this sum is real, which makes the quadratures uncorrelated. The full proof is in the proofs folder.

## Complexity

Lines L1 to L5 take $O(N)$ time and line L7 takes $O(N)$. The inverse DFT of line L6 takes $O(N \log N)$ with a [fast Fourier transform](/fast-fourier-transform/), so the total is $O(N \log N)$ in the [real RAM](/real-ram/), with $O(N)$ space. The direct sum of the reference code takes $O(N^2)$.

## Properties

- **Exactly Gaussian.** Each $h[n]$ is $CN(0, \Omega)$, so $|h[n]|$ is exactly Rayleigh, for any $N$. Sum-of-sinusoids generators are Gaussian only as their number of sinusoids grows.
- **Circular, not stationary over blocks.** The autocorrelation depends only on $d$ modulo $N$: $r[N - d] = r[d]$. Inside one block the process is periodic in its statistics, and separate blocks are independent.
- **Approximate $J_0$.** $r[d]$ is a sampled version of $J_0$, with the error set by $k_m$ and by the edge bin. It is not an approximation in the number of samples alone.
- **Block generation.** All $N$ samples come at once; the method does not run sample by sample.
- **Any spectrum.** Replacing $F$ with the square root of another spectrum gives a Gaussian process with that spectrum, through the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/).

## Variants and improvements

- **Smith's form with two transforms.** Smith (1975) shaped two independent noise sequences and used one inverse transform for each quadrature. Young and Beaulieu (2000) showed that one IDFT of complex noise gives the same statistics with half the work.
- **Time-domain filters.** White Gaussian noise passed through an [FIR filter](/fir-filter/) or an [IIR filter](/iir-filter/) that approximates the Doppler spectrum gives samples one at a time, at the cost of a filter design error.
- **Autoregressive models.** An [autoregressive model](/autoregressive-model/) fitted to $J_0$ gives fading sample by sample, with a recursion that suits [Kalman channel tracking](/kalman-channel-tracking/).
- **Sum of sinusoids.** The [Jakes simulator](/jakes-fading-simulator/) and the [Zheng-Xiao simulator](/zheng-xiao-fading-simulator/) give $h(t)$ at any time $t$, but are Gaussian only approximately.

## When to use it

Use it when a simulation needs long blocks of time-correlated Rayleigh fading on a fixed sample grid, with an exactly Gaussian distribution, for example for error rates, outage or level crossings at high $\bar\gamma$. Make $N$ much larger than the longest lag of interest and take $k_m$ of 30 or more. Use a sum-of-sinusoids generator when the channel is needed at arbitrary times or sample by sample, and an independent draw per block when the fading is block fading.

## Pitfalls

- **Wrap-around.** The output is periodic in its statistics: the end of a block is correlated with its start. Do not join blocks and expect a smooth process, and do not use lags near $N/2$.
- **Too few bins in the band.** With small $k_m$ the spectrum is coarse and the autocorrelation differs from $J_0$ by 0.1 or more. The test $2 \le k_m < N/2$ is only a minimum.
- **The edge bin.** Using the spectrum value at $k = k_m$ gives infinity when $N f_m$ is an integer. Setting it to 0 removes the strongest part of the spectrum and changes the fade rate.
- **Scaling.** The inverse DFT convention changes the output power by $N$ or $\sqrt N$. Scale by the sum of $F[k]^2$, as in line L7.
- **Sample rate.** $f_m$ is $f_D/f_s$. A sample rate far above $f_D$ needs a very large $N$ for a few fade cycles; generate at a low rate and interpolate.

## Implementations

## History

Smith (1975) described a computer simulation of mobile radio fading in which Gaussian noise is shaped in the frequency domain by the Doppler spectrum and transformed to the time domain, with one transform for each quadrature. The method became a standard tool, and Rappaport's textbook presents it for the Clarke and Gans fading model. Young and Beaulieu (2000) analyzed the IDFT method, showed that a single inverse transform of complex noise is enough, and gave a filter that handles the infinite spectrum at the Doppler edge by the area of the last bin.

## References
