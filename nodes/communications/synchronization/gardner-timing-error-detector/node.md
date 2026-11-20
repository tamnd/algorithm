---
tag: 9K1C0E
kind: algorithm
slug: gardner-timing-error-detector
name: Gardner timing error detector
aliases:
- Gardner TED
- Gardner algorithm
area: communications/synchronization
level: core
summary: "A timing error detector at two samples per symbol. It multiplies the midpoint sample by the difference of the two strobes around it, needs no decisions and does not depend on the carrier phase."
solves: [symbol-timing-recovery]
model: real-ram
complexity:
  vars: {N: the number of symbols}
  time: {worst: O(N)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, non_data_aided: true, carrier_phase_invariant: true, samples_per_symbol: 2}
history:
  year: 1986
  people: [Floyd M. Gardner]
  note: "Floyd M. Gardner published the detector in 1986 for BPSK and QPSK receivers that sample at two samples per symbol."
prereqs: [symbol-timing-recovery, phase-locked-loop]
see_also: [early-late-gate-synchronizer, mueller-muller-timing-recovery, oerder-meyr-timing-estimation, farrow-interpolator, raised-cosine-filter, modified-cramer-rao-bound, phase-shift-keying, costas-loop]
sources:
  - paper: doi:10.1109/TCOM.1986.1096561
    title: "F. M. Gardner, A BPSK/QPSK timing-error detector for sampled receivers, IEEE Transactions on Communications 34(5), 1986, pages 423 to 429"
    locator: "the detector from the midpoint sample and the two strobes, its S-curve, and its independence of the carrier phase"
  - paper: doi:10.1109/26.221081
    title: "F. M. Gardner, Interpolation in digital modems, Part I: Fundamentals, IEEE Transactions on Communications 41(3), 1993, pages 501 to 507"
    locator: "timing loops with a free-running sampler, an interpolator and a numerically controlled oscillator"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 7 (timing recovery in baseband transmission) and Chapter 8 (timing recovery with linear modulations: the non-data-aided detectors)"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Chapter 9 (interpolation and the digital timing loop)"
---

The Gardner timing error detector is the most common non-data-aided detector for [symbol timing recovery](/symbol-timing-recovery/) in digital modems. It takes two samples per symbol: the strobe $y_k$, where the symbol should be read, and the midpoint $y_{k-1/2}$ halfway between two strobes. Its output is $e_k = \operatorname{Re}\{\overline{y_{k-1/2}}\,(y_{k-1} - y_k)\}$. When the data change sign between two symbols, the midpoint lies on the zero crossing of the transition if the timing is right, and it moves away from zero, with a sign that shows the direction of the error, if the timing is wrong. The product with $y_{k-1} - y_k$ removes the sign of the transition. The detector needs no decisions, and a carrier phase cancels in the product, so the loop can run before [carrier recovery](/carrier-recovery/). For [raised cosine](/raised-cosine-filter/) pulses its mean output is $A\sin(2\pi\Delta)$ with $A = \frac{4\sin(\pi\beta/2)}{\pi(4 - \beta^2)}$. It drives the loop filter and accumulator of a [phase-locked loop](/phase-locked-loop/), with a [Farrow interpolator](/farrow-interpolator/) when the sample clock is free-running. Against the [early-late gate](/early-late-gate-synchronizer/) it needs one sample fewer per symbol and has less self-noise; against the [Mueller and Muller detector](/mueller-muller-timing-recovery/) it needs twice the samples but no decisions and no carrier phase.

## In plain words

Picture the signal moving from one symbol value to the next. If the next symbol has the opposite sign, the signal crosses zero on the way, and with correct timing it crosses exactly halfway between the two reading points. The detector reads the signal at that halfway point too. If the halfway reading is not zero, the timing is off, and whether it lies above or below zero, compared with the direction of the change, tells whether the reading points are early or late. When two neighboring symbols are equal, the difference between them is near zero and the detector says almost nothing, which is correct because there is no crossing to measure. A turn of the whole signal by the carrier does not matter, since the detector compares the signal only with itself.

## The problem

Times are in symbol periods, $T = 1$. The receiver can sample the matched filter output
$$y(t) = e^{j\theta}\sum_m a_m\,g(t - m - \tau) + v(t)$$
at times it chooses, with a controlled clock or with an interpolator on a fixed grid of at least two samples per symbol. The pulse $g$ is real and even (a raised cosine with roll-off $\beta$ in the analysis), the symbols $a_m$ are unknown, independent and zero-mean with $E|a_m|^2 = 1$ (BPSK, QPSK or QAM), $\theta$ is an unknown carrier phase, $v$ is filtered noise with $\mathrm{SNR} = E_s/N_0$, and the delay $\tau$ is unknown and may drift. The loop must give estimates $\tau_k$ so that the strobes $y(k + \tau_k)$ fall on the symbol instants.

## The algorithm

```pseudo id=main
GARDNER(y, N, Kp, Ki, tau0)
L1  tau <- tau0; s <- 0
L2  prev <- y(-1 + tau)
L3  for k <- 0 to N - 1 do
L4      mid <- y(k - 1/2 + tau)                 ▷ midpoint sample
L5      cur <- y(k + tau)                       ▷ strobe; est[k] <- tau
L6      e <- Re(conj(mid) * (prev - cur))       ▷ Gardner detector
L7      s <- s + Ki * e                         ▷ loop filter
L8      tau <- tau + Kp * e + s                 ▷ timing accumulator
L9      prev <- cur
L10 return est, strobes
```

Line L6 is the detector. With this sign it is positive when the strobes are early ($\tau_k < \tau$), so line L8 adds it. Gardner's paper writes the difference the other way and subtracts. Line L9 keeps the strobe for the next symbol, so each symbol costs two new samples. Lines L7 and L8 are the PLL loop with the delay in place of the phase. For a first-order loop with noise bandwidth $B_LT$, $K_p = 4B_LT/\bigl((1 + 2B_LT)K_D\bigr)$ with the detector slope $K_D = 2\pi A$ at unit symbol energy, which is $1.508494$ for $\beta = 0.5$.

## Example

Take QPSK data (seed 1), $\beta = 0.5$, the true delay $\tau = 0.3$, no noise, $B_LT = 0.01$ and $K_i = 0$, so $K_p = 0.025997$. The loop starts at $\tau_0 = 0$, and the samples are rounded to three decimals:

| $k$ | $\tau_k$ | prev | mid (L4) | cur (L5) | $e_k$ (L6) | $\tau_{k+1}$ (L8) |
|---|---|---|---|---|---|---|
| 0 | $0$ | $0.104 - 0.080j$ | $-0.173 + 0.112j$ | $-0.702 + 0.490j$ | $-0.203510$ | $-0.005291$ |
| 1 | $-0.005291$ | $-0.702 + 0.490j$ | $-0.487 + 0.826j$ | $0.463 + 0.935j$ | $0.198966$ | $-0.000118$ |
| 2 | $-0.000118$ | $0.463 + 0.935j$ | $0.563 + 0.402j$ | $-0.389 - 0.520j$ | $1.064807$ | $0.027563$ |

The mean error at $\Delta = 0.3$ is $A\sin(0.6\pi) = 0.2283$, but the first output is negative: at $k = 0$ the data pattern pulls the wrong way. The large output at $k = 2$ comes from a full sign change in both the real and the imaginary parts, the case that carries the most timing information. The error $\tau - \tau_k$ is $0.238$ at $k = 10$, $0.177$ at $25$, $0.052$ at $50$ and below $10^{-3}$ at $100$ and $200$. After that the loop jitters around the delay with an rms error of $0.005$ and peaks of $0.011$, without noise. With alternating data $a_m = (-1)^m$, the output is $\sin(2\pi\Delta)$ exactly and the loop stays at $\tau$.

In noise at $E_s/N_0 = 10$ dB with $B_LT = 0.01$, the loop form of the [MCRB](/modified-cramer-rao-bound/) is $2.66 \times 10^{-4}$. Three runs of 2400 symbols (seeds 7, 8 and 9) measured a variance of $1.36$ to $2.08$ times this bound (measurement).

## Correctness

**Claim.** For raised cosine pulses, independent zero-mean data and stationary noise, the mean of $e_k$ with $\tau_k$ held fixed is $A\sin(2\pi\Delta)$, $\Delta = \tau - \tau_k$, for every carrier phase. So the loop has stable points at $\Delta \in \mathbb{Z}$ and behaves near lock as a PLL with detector gain $2\pi A$.

**Key steps.** A phase $e^{j\theta}$ cancels between $\overline{y_{k-1/2}}$ and $y_{k-1} - y_k$. The cross terms between different symbols have mean zero, so the mean is a sum over all integer shifts of $p(t) = g(t - \frac12)\bigl(g(t - 1) - g(t)\bigr)$. By Poisson summation only the Fourier coefficients at $0$ and $\pm1$ remain. The one at $0$ is zero, because both products have the same integral, the autocorrelation of $g$ at lag $\frac12$. The one at $1$ is $\frac{jA}{2}$, an integral over the roll-off band. The full proof is in the proofs file.

The S-curve is a closed form under assumptions: raised cosine pulses, independent data, stationary noise, and $\tau_k$ constant while the mean is taken. The jitter and the noise ratios are measurements.

## Complexity

Each symbol needs two new samples (lines L4 and L5), one complex subtraction, the real part of one complex product (two real multiplications and one addition), and the four operations of lines L7 and L8. With an interpolator of $K$ taps, a symbol costs $2K + O(1)$ operations. The loop is $O(1)$ per symbol and $O(N)$ for $N$ symbols in the [real RAM](/real-ram/), with $O(1)$ extra space besides the output.

## Properties

- **Non-data-aided and phase-free.** It needs no decisions and no carrier phase, so it works from the first symbol, before the carrier loop has locked. A residual frequency offset that turns the phase slowly does not disturb it.
- **Two samples per symbol.** The strobe of one symbol is reused as the previous strobe of the next, so the sample rate is $2/T$, as in many modems that sample at twice the symbol rate anyway.
- **Needs excess bandwidth.** $A \to 0$ as $\beta \to 0$: $A = 0.240$ at $\beta = 0.5$ and $0.050$ at $\beta = 0.1$. With little excess bandwidth the S-curve is small and the self-noise dominates.
- **Self-noise and loop offset (measurement).** Without noise the rms jitter was $0.0053$ at $B_LT = 0.01$ and $0.0013$ at $B_LT = 0.0025$, and the mean of $\tau_k - \tau$ was about $0.32\,B_LT$, over three seeds each. The jitter is a third of that of the square-law early-late gate with the same bandwidth.
- **Gain depends on amplitude.** $K_D$ scales with the signal power, so an automatic gain control should come first.

## Variants and improvements

- **Real-valued form.** For BPSK, or for the real and imaginary parts of QPSK separately, $e = y^I_{k-1/2}(y^I_{k-1} - y^I_k) + y^Q_{k-1/2}(y^Q_{k-1} - y^Q_k)$, which is the same value written without complex arithmetic.
- **Decision-directed form.** Replacing $y_{k-1} - y_k$ by $\hat a_{k-1} - \hat a_k$ removes much of the self-noise at high SNR, but it needs decisions and the carrier phase.
- **Feedforward use.** The same products can be averaged over a block to estimate a fixed delay, but the [Oerder and Meyr estimator](/oerder-meyr-timing-estimation/) is the usual feedforward choice.
- **Interpolated loop.** In Gardner's 1993 structure, the sampler runs from a fixed clock, a numerically controlled oscillator gives the basepoint and the fractional interval, and a [Farrow interpolator](/farrow-interpolator/) computes the samples of lines L4 and L5.

## When to use it

Use the Gardner detector when the receiver has two samples per symbol, the modulation is BPSK, QPSK or a QAM with moderate roll-off, and the timing must lock before the carrier. It is the default choice in many software and hardware modems. With a small roll-off, or when decisions are reliable and the carrier phase is known, the [Mueller and Muller detector](/mueller-muller-timing-recovery/) or a data-aided detector gives less jitter. For short bursts, a feedforward estimate avoids the acquisition time of the loop.

## Pitfalls

- **Wrong midpoint.** The midpoint must be half a symbol before the current strobe, between the two strobes in the product. Taking it after the current strobe reverses the sign of the S-curve, and the loop locks half a symbol off.
- **Sign convention.** Gardner's paper uses $y_k - y_{k-1}$ and subtracts the error from the timing. Mixing one convention for the detector with the other for the update makes the loop diverge from the right point.
- **Long runs of equal symbols.** A run of equal symbols has no transitions and gives no timing information. Scrambling the data keeps transitions frequent.
- **Small roll-off.** At $\beta = 0.1$ the slope is a fifth of that at $\beta = 0.5$. Use a narrow loop or another detector.
- **Offset QPSK.** In OQPSK the quadrature data are delayed by half a symbol, so the detector must use the matching midpoint for each arm, or it sees no S-curve.

## Implementations

## History

Floyd M. Gardner published the detector in the IEEE Transactions on Communications in 1986, for receivers that sample at two samples per symbol with a clock that is not tied to the symbol rate. Its independence of the carrier phase allowed timing recovery to come first in a digital receiver. In 1993 Gardner, with Lars Erup and Robert A. Harris, described how such a loop drives an interpolator from a free-running sample clock, and the pair of the Gardner detector and a Farrow interpolator became a standard structure in digital modems.

## References
