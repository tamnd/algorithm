---
tag: WF9W5Z
kind: algorithm
slug: oerder-meyr-timing-estimation
name: Oerder and Meyr timing estimation
aliases:
- square-law timing recovery
- Oerder-Meyr estimator
area: communications/synchronization
level: advanced
summary: "A feedforward timing estimator. It squares the magnitude of a block of samples at four per symbol, takes the DFT bin at the symbol rate and reads the delay from the phase of that bin."
solves: [symbol-timing-recovery]
model: real-ram
complexity:
  vars: {N: the number of symbols in the block, S: the samples per symbol}
  time: {worst: O(N S)}
  space: {extra: O(S)}
properties: {deterministic: true, feedforward: true, non_data_aided: true, carrier_phase_invariant: true, samples_per_symbol: "at least 3, usually 4"}
history:
  year: 1988
  people: [Martin Oerder, Heinrich Meyr]
  note: "Oerder and Meyr published the digital filter and square estimator in 1988, for receivers that sample at a fixed rate and need the timing of a block without a loop."
prereqs: [symbol-timing-recovery, discrete-fourier-transform]
see_also: [gardner-timing-error-detector, early-late-gate-synchronizer, mueller-muller-timing-recovery, farrow-interpolator, goertzel-algorithm, modified-cramer-rao-bound, cyclostationary-feature-detection, raised-cosine-filter]
sources:
  - paper: doi:10.1109/26.1476
    title: "M. Oerder and H. Meyr, Digital filter and square timing recovery, IEEE Transactions on Communications 36(5), 1988, pages 605 to 612"
    locator: "the estimator from the spectral line at the symbol rate of the squared samples at four samples per symbol, and its variance"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Section 5.4 (feedforward timing estimation from the spectral line)"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 7 and Chapter 8 (feedforward non-data-aided timing estimation and its comparison with the modified Cramer-Rao bound)"
---

Oerder and Meyr timing estimation is a feedforward, non-data-aided method for [symbol timing recovery](/symbol-timing-recovery/). The power $|y(t)|^2$ of the matched filter output of a linearly modulated signal is, on average, a constant plus a sinusoid at the symbol rate, whose phase is the delay $\tau$. The estimator samples the output at $L_s = 4$ samples per symbol, squares the magnitudes, computes the one bin of the [discrete Fourier transform](/discrete-fourier-transform/) at the symbol rate, $X = \sum_n |x[n]|^2 e^{-j2\pi n/L_s}$, and returns $\hat\tau = -\arg(X)/(2\pi)$. There is no loop, so the estimate of a block is ready after the block, without acquisition time, which suits burst receivers. The squaring removes the data and the carrier phase. The estimate is then applied with an interpolator such as the [Farrow interpolator](/farrow-interpolator/). The sinusoid comes from the excess bandwidth: for a [raised cosine](/raised-cosine-filter/) pulse with roll-off $\beta$ its amplitude is $\beta/4$, so the method needs $\beta > 0$. The feedback detectors with the same idea are the [early-late gate](/early-late-gate-synchronizer/) and the [Gardner detector](/gardner-timing-error-detector/).

## In plain words

The strength of the received signal rises and falls once per symbol on average: it is strongest near the moments when the symbols should be read. The pattern of the data blurs this rhythm, but over many symbols the rhythm remains. The estimator measures the strength of the signal four times per symbol over a block. It then asks how well the measured strengths match a wave that repeats once per symbol, and at which shift of that wave the match is best. That shift is the timing. The method does not need the data or the phase of the carrier, and it gives an answer for the whole block at once instead of slowly moving toward it.

## The problem

Times are in symbol periods, $T = 1$. The input is a block of $N = L_0 L_s$ samples $x[n] = y(n/L_s)$ of the matched filter output
$$y(t) = e^{j\theta}\sum_m a_m\,g(t - m - \tau) + v(t),$$
taken by a free-running clock at $L_s \ge 3$ samples per symbol. The pulse $g$ is a raised cosine with roll-off $\beta > 0$, the symbols $a_m$ are unknown, independent and zero-mean with $E|a_m|^2 = 1$, $\theta$ is an unknown carrier phase, $v$ is filtered noise with $\mathrm{SNR} = E_s/N_0$, and $\tau$ is constant over the block. The output is an estimate $\hat\tau \in [-\frac12, \frac12)$ of $\tau$ modulo one symbol, so that the receiver can interpolate the strobes $y(k + \hat\tau)$.

## The algorithm

```pseudo id=main
OERDER-MEYR(x[0..N-1], Ls)
L1  rot[i] <- exp(-j 2 pi i / Ls) for i <- 0 to Ls - 1
L2  X <- 0
L3  for n <- 0 to N - 1 do
L4      X <- X + |x[n]|^2 * rot[n mod Ls]     ▷ symbol-rate DFT bin of |x|^2
L5  tau <- -arg(X) / (2 pi)                  ▷ wrapped to [-1/2, 1/2)
L6  return tau
```

Line L1 builds a table of the $L_s$ rotations. For $L_s = 4$ they are $1, -j, -1, j$, so with $P_r = \sum_{n \equiv r} |x[n]|^2$ for $r = 0, 1, 2, 3$, line L4 reduces to $X = (P_0 - P_2) + j(P_3 - P_1)$ and needs no multiplications. Line L4 is one bin of the DFT, which is what the [Goertzel algorithm](/goertzel-algorithm/) computes in general. Line L5 takes the argument with a two-argument arctangent. For a long stream, the receiver runs the estimator on consecutive blocks and unwraps the estimates, because each is known only modulo one symbol.

## Example

Take QPSK data (seed 7), $\beta = 0.5$, $\tau = 0.3$, no noise, $L_s = 4$ and a block of $L_0 = 100$ symbols in the middle of a longer stream, so $N = 400$. The four partial sums of line L4 are:

| $r$ | $P_r$ | rotation |
|---|---|---|
| 0 | $85.991$ | $1$ |
| 1 | $99.485$ | $-j$ |
| 2 | $92.528$ | $-1$ |
| 3 | $78.916$ | $j$ |

So $X = (85.991 - 92.528) + j(78.916 - 99.485) = -6.537 - 20.569j$. Its argument is $-1.8786$ rad, and line L5 gives $\hat\tau = 0.29897$, an error of $0.001$ symbol. The mean of $X$ is $\frac{\beta}{8}N e^{-j2\pi\tau} = 25e^{-j0.6\pi} = -7.725 - 23.776j$: the data pattern moved $X$ from its mean, which is self-noise. With alternating data $a_m = (-1)^m$ the power is exactly $\frac12 + \frac12\cos(2\pi(t - \tau))$, the sums are $34.548, 97.553, 65.450, 2.447$, and $X = -30.902 - 95.106j = 100e^{-j0.6\pi}$, which gives $\hat\tau = 0.3000003$.

Over 20 random QPSK blocks without noise, the rms error was $0.0056$ symbol and the largest $0.010$ (measurement). At $E_s/N_0 = 10$ dB, 30 blocks gave a mean square error of $1.92$ times the [MCRB](/modified-cramer-rao-bound/) $1/(8\pi^2\xi L_0\,\mathrm{SNR}) = 1.33 \times 10^{-4}$ (measurement). With alternating data and a delay that grows by $0.004$ symbol per symbol, from $0.3$ to $1.5$ over 300 symbols, blocks of 20 symbols with unwrapping followed the delay at each block centre within $0.01$ (measurement).

## Correctness

**Claim.** If $L_s \ge 3$ and $N$ is a multiple of $L_s$, then $E[X] = \frac{\beta}{8}N e^{-j2\pi\tau}$ for every carrier phase and every stationary noise, so the phase of the mean gives $\tau$ exactly. For $L_s = 2$, $X$ is real and the method fails. As $L_0 \to \infty$ the estimate converges to $\tau$ modulo one.

**Key steps.** By Poisson summation, the mean power of a raised cosine signal is $1 - \frac{\beta}{4} + \frac{\beta}{4}\cos(2\pi(t - \tau))$ plus the noise power. Over whole periods, the DFT bin removes the constant and the term at twice the symbol rate, and keeps $\frac{\beta}{8}e^{-j2\pi\tau}$ per sample. At $L_s = 2$ the term at $-1$ cycle per symbol aliases onto the one at $+1$. Also, $\operatorname{Re}\{Xe^{j2\pi\tau_c}\} = \sum_n |x[n]|^2\cos(2\pi(n/L_s - \tau_c))$, so $\hat\tau$ is the $\tau_c$ that maximizes the match between the measured power and a sinusoid at the symbol rate, and the tests check this against a grid search. The full proof is in the proofs file.

The mean is a closed form under assumptions: raised cosine pulses, independent data that extend beyond the block, stationary noise and a constant delay. The variance is not given in closed form here; the numbers above are measurements.

## Complexity

Each sample costs two real multiplications and one addition for $|x[n]|^2$, and one multiply-add by a table entry, or only an addition when $L_s = 4$. So a block costs $O(L_0 L_s)$ operations and one arctangent, in the [real RAM](/real-ram/), with $O(L_s)$ extra space for the table. The work per symbol is $O(L_s)$, a little more than a feedback loop at two samples per symbol, but the estimate has no acquisition time. The sum can be split over parallel hardware, since it has no feedback.

## Properties

- **Feedforward.** The estimate of a block depends only on that block. There is no hang-up and no acquisition time, which makes the method suitable for bursts.
- **Non-data-aided and phase-free.** The magnitude removes the carrier phase, and a frequency offset small enough not to distort the matched filter output does not matter.
- **Needs excess bandwidth.** The line amplitude is $\beta/4$ times the symbol power. For $\beta \to 0$ the line vanishes and the estimate becomes noise.
- **Modulo one symbol.** $\hat\tau$ is in $[-\frac12, \frac12)$. Which symbol the strobe belongs to must come from frame synchronization or from unwrapping.
- **Low-SNR maximum likelihood link.** At low SNR, the non-data-aided log-likelihood of the delay is about proportional to $\sum_k |y(k + \tau_c)|^2$, a periodic function of $\tau_c$. The estimator maximizes its first Fourier component (heuristic justification of the method).

## Variants and improvements

- **Other nonlinearities.** $|x|$, $|x|^4$ or $\ln(1 + |x|^2/\sigma^2)$ also produce a line at the symbol rate. They change the noise and the self-noise, but not the structure.
- **Other sample rates.** Any $L_s \ge 3$ works by the same proof; $L_s = 4$ is the cheapest. Variants at two samples per symbol interpolate a third sample or use a different nonlinearity to avoid the aliasing.
- **Block-wise tracking.** Running the estimator on consecutive blocks, with unwrapping, follows a slowly drifting delay, as in the example. A smoothing filter on the estimates reduces their variance.
- **Feedback form.** Using $\operatorname{Im}\{X e^{j2\pi\tau_k}\}$ as an error signal turns the estimator into a timing error detector for a loop.
- **Data-aided estimation.** With known symbols, the delay can be found by correlating with the known waveform, which reaches the MCRB at lower SNR; see [data-aided synchronization](/data-aided-synchronization/).

## When to use it

Use the Oerder and Meyr estimator when the receiver samples at a fixed rate of four samples per symbol, the data arrive in bursts or the timing must be found fast, the roll-off is not small, and the carrier is not yet recovered. It is a standard first stage in digital burst modems: estimate the timing, interpolate, then recover the carrier. For continuous links with tight jitter requirements, a narrow feedback loop averages over more symbols. For small roll-off, use a data-aided or decision-directed method.

## Pitfalls

- **Two samples per symbol.** At $L_s = 2$ the rotations are $\pm1$, $X$ is real, and the phase carries no timing information. The implementation raises an error for $L_s < 3$.
- **Block not a multiple of $L_s$.** Then the constant part of $|x|^2$ does not cancel in $X$ and biases the estimate. Use a whole number of symbols.
- **Edges of a burst.** If the block covers the ramp-up or the ramp-down of a burst, the power there does not follow the stationary model. Keep the block inside the data, or accept a larger error.
- **Wrap-around.** An estimate near $\pm\frac12$ can jump by one symbol from block to block. Unwrap before interpolating, and track which symbol each strobe belongs to.
- **Small roll-off.** With $\beta = 0.1$ the line is five times weaker than with $\beta = 0.5$, and self-noise dominates unless the block is long.

## Implementations

## History

Clock recovery by squaring the signal and filtering out the tone at the symbol rate is an old analog technique. Martin Oerder and Heinrich Meyr, at the RWTH Aachen, published a digital form in the IEEE Transactions on Communications in 1988: sample at a fixed rate of four samples per symbol, square, and take one DFT coefficient, so the phase of the tone is computed directly instead of filtered by a loop. Their paper gave the variance of the estimate and showed its use in all-digital receivers with interpolation. Meyr, Moeneclaey and Fechtel later placed it among the feedforward synchronizers derived from the likelihood function.

## References
