---
tag: Z897RY
kind: algorithm
slug: early-late-gate-synchronizer
name: Early-late gate synchronizer
aliases:
- early-late gate
- early-late timing detector
area: communications/synchronization
level: core
summary: "A timing loop that compares the energy of the matched filter output a little before and a little after the sampling instant, and moves the instant toward the side with more energy."
solves: [symbol-timing-recovery]
model: real-ram
complexity:
  vars: {N: the number of symbols}
  time: {worst: O(N)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, non_data_aided: true, carrier_phase_invariant: true, samples_per_symbol: "3 (early, on time and late)"}
history:
  year: 1970
  people: [Marvin K. Simon]
  note: "The early-late gate is older than this paper. 1970 is the year of Simon's analysis of the absolute-value early-late bit synchronizer, the earliest primary source checked for this page."
prereqs: [symbol-timing-recovery, phase-locked-loop]
see_also: [gardner-timing-error-detector, mueller-muller-timing-recovery, oerder-meyr-timing-estimation, delay-locked-loop, farrow-interpolator, raised-cosine-filter, modified-cramer-rao-bound, eye-diagram]
sources:
  - paper: doi:10.1109/TCOM.1970.1090410
    title: "M. K. Simon, Nonlinear analysis of an absolute value type of an early-late gate bit synchronizer, IEEE Transactions on Communication Technology 18(5), 1970, pages 589 to 596"
    locator: "the absolute-value early-late gate, its S-curve and its steady-state timing error by the Fokker-Planck method"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 5.3 (symbol timing estimation, with the early-late gate synchronizer as a non-decision-directed method)"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 7 (timing recovery in baseband transmission) and Chapter 8 (timing recovery with linear modulations)"
---

The early-late gate synchronizer is a feedback loop for [symbol timing recovery](/symbol-timing-recovery/). The output of the [matched filter](/matched-filter/) has its largest energy at the correct sampling instant, and the energy curve is symmetric around that point. So the loop takes two extra samples, one a time $d$ before the current instant (early) and one a time $d$ after it (late), and uses the difference of their squared magnitudes as the timing error. A loop filter and an accumulator, as in a [phase-locked loop](/phase-locked-loop/), move the instant until the two energies balance. The detector needs no decisions and no carrier phase. For [raised cosine](/raised-cosine-filter/) pulses its mean output is $\frac{\beta}{2}\sin(2\pi d)\sin(2\pi\Delta)$ for the timing error $\Delta$, so it works only with excess bandwidth $\beta > 0$, and it gives no error signal at all when $d = T/2$. The same early-late structure tracks a spreading code in the [delay-locked loop](/delay-locked-loop/). The [Gardner detector](/gardner-timing-error-detector/) uses fewer samples and has less self-noise, and the [Mueller and Muller detector](/mueller-muller-timing-recovery/) uses decisions at one sample per symbol.

## In plain words

Each received pulse rises to a peak and falls again, and the receiver should read it at the peak. The receiver does not know where the peak is, so it takes three readings: one at its current guess, one a little earlier and one a little later. If the later reading is stronger, the peak is later than the guess, and the guess moves forward a small step. If the earlier reading is stronger, the guess moves back. Since one pulse overlaps its neighbors and the data change from symbol to symbol, a single comparison can point the wrong way. The loop takes small steps, so these errors average out over many symbols. The comparison uses only the strength of the signal, so it works before the receiver knows the data or the phase of the carrier.

## The problem

Times are in symbol periods, $T = 1$. The receiver can sample the matched filter output
$$y(t) = e^{j\theta}\sum_m a_m\,g(t - m - \tau) + v(t)$$
at any time $t$: with an analog-to-digital converter whose clock it controls, or with an interpolator such as the [Farrow interpolator](/farrow-interpolator/) on a fixed sample grid. Here $g$ is the overall pulse (a raised cosine with roll-off $\beta$ in the analysis), $a_m$ are unknown independent symbols with $E a_m = 0$ and $E|a_m|^2 = 1$, $\theta$ is an unknown carrier phase, $v(t)$ is the filtered noise with $\mathrm{SNR} = E_s/N_0$, and $\tau$ is the unknown delay, which may drift slowly. The loop must output estimates $\tau_k$ such that the strobes $y(k + \tau_k)$ are taken at the pulse peaks.

## The algorithm

```pseudo id=main
EARLY-LATE-GATE(y, N, Kp, Ki, tau0, d)
L1  tau <- tau0; s <- 0
L2  for k <- 0 to N - 1 do
L3      early <- |y(k + tau - d)|^2
L4      late <- |y(k + tau + d)|^2
L5      e <- late - early                       ▷ positive: the strobe is early
L6      est[k] <- tau; strobe[k] <- y(k + tau)
L7      s <- s + Ki * e                         ▷ loop filter
L8      tau <- tau + Kp * e + s                 ▷ timing accumulator
L9  return est, strobe
```

Lines L3 and L4 take the early and late samples at a distance $d$ from the strobe; $d = T/4$ gives the largest slope. Line L5 is the square-law detector. Line L6 is the on-time sample that goes to the detector of the data. Lines L7 and L8 are the loop of the PLL, with the phase replaced by the delay: $K_i = 0$ gives a first-order loop, which follows a constant delay, and $K_i > 0$ gives a second-order loop, which also follows a clock frequency offset (a delay that grows linearly). For a first-order loop with noise bandwidth $B_L T$, the gain is $K_p = 4B_LT/\bigl((1 + 2B_LT)K_D\bigr)$, with the detector slope $K_D = \pi\beta\sin(2\pi d)$ at unit symbol energy.

## Example

Take QPSK data (seed 1), $\beta = 0.5$, the true delay $\tau = 0.3$, no noise and no carrier phase. The gate half-width is $d = \frac14$, so $K_D = \pi/2$, and $B_LT = 0.01$ gives $K_p = 0.024965$ with $K_i = 0$. The loop starts at $\tau_0 = 0$:

| $k$ | $\tau_k$ | early (L3) | late (L4) | $e_k$ (L5) | $\tau_{k+1}$ (L8) |
|---|---|---|---|---|---|
| 0 | $0$ | $0.299949$ | $0.993528$ | $0.693579$ | $0.017316$ |
| 1 | $0.017316$ | $0.880789$ | $1.056403$ | $0.175615$ | $0.021700$ |
| 2 | $0.021700$ | $0.021493$ | $0.993303$ | $0.971810$ | $0.045962$ |

The mean error at $\Delta = 0.3$ is $\frac{0.5}{2}\sin(0.6\pi) = 0.2378$, but single values range from $0.18$ to $0.97$ in these three steps: the data pattern decides each one. The error $\tau - \tau_k$ is $0.217$ at $k = 10$, $0.161$ at $25$, $0.046$ at $50$, $-0.016$ at $100$ and $-0.011$ at $200$. After that the loop does not settle to a point. It jitters around the delay with an rms error of $0.016$ and peaks of $0.04$, without noise, because the detector has self-noise. For alternating data $a_m = (-1)^m$ the self-noise is zero, and the tests check that the loop then stays at $\tau$ to $10^{-9}$.

In noise at $E_s/N_0 = 10$ dB with $B_LT = 0.01$, the loop form of the [MCRB](/modified-cramer-rao-bound/) is $B_LT/(4\pi^2\xi\,\mathrm{SNR}) = 2.66 \times 10^{-4}$, with $\xi = 0.0951727$ for $\beta = 0.5$. Three runs of 2400 symbols (seeds 7, 8 and 9) measured a variance of $1.95$ to $2.79$ times this bound (measurement).

## Correctness

**Claim.** For raised cosine pulses and independent zero-mean data, the mean of $e_k$ with $\tau_k$ held fixed is $\frac{\beta}{2}\sin(2\pi d)\sin(2\pi\Delta)$ with $\Delta = \tau - \tau_k$, for every carrier phase and every stationary noise. So the loop has its stable points at $\Delta \in \mathbb{Z}$ and behaves near lock as a PLL with detector gain $K_D = \pi\beta\sin(2\pi d)$.

**Key steps.** The mean of $|y(t)|^2$ is $\sum_m g(t - m - \tau)^2$ plus the noise power, because the cross terms between symbols have mean zero. By Poisson summation, this folded energy of a raised cosine is $1 - \frac{\beta}{4} + \frac{\beta}{4}\cos(2\pi(t - \tau))$: only the spectral lines at $0$ and $\pm1$ survive, since $|g|^2$ has a band below 2 cycles per symbol. The late sample minus the early sample removes the constant and the noise power and leaves the sine. The full proof is in the proofs file.

The S-curve is a closed form under assumptions: raised cosine pulses, independent data, and $\tau_k$ constant while the mean is taken. The jitter of the example is a measurement.

## Complexity

Each symbol needs three samples of $y$ (lines L3, L4 and L6), two squared magnitudes of two real multiplications and one addition each, one subtraction, and the four operations of lines L7 and L8. With an interpolator of $K$ taps, each sample costs $K$ more multiply-adds, so a symbol costs $3K + O(1)$ operations. The loop is $O(1)$ per symbol and $O(N)$ for $N$ symbols in the [real RAM](/real-ram/), with $O(1)$ extra space besides the output. It is sequential, like every feedback loop.

## Properties

- **Non-data-aided and phase-free.** The detector uses only $|y|^2$, so a carrier phase or a slow frequency offset does not change it. Timing can be recovered before the carrier.
- **Needs excess bandwidth.** The slope $\pi\beta\sin(2\pi d)$ is proportional to the roll-off $\beta$. For $\beta \to 0$ the energy of the signal no longer varies with $t$ on average, and the detector has no mean output.
- **Self-noise.** At $\Delta = 0$ the mean is zero, but each $e_k$ depends on the neighboring symbols, so the loop jitters even without noise. The jitter falls with the loop bandwidth.
- **Mean offset in the loop (measurement).** In the runs of the tests and the example, the mean of $\tau_k - \tau$ was about $1.05\,B_LT$ without noise: $0.0105$ at $B_LT = 0.01$ and $0.0026$ at $B_LT = 0.0025$, over three seeds each. A likely cause is that $\tau_k$ depends on past symbols that also enter $e_k$ through the pulse tails (heuristic). The offset shrinks with the bandwidth.
- **Gain depends on amplitude.** $K_D$ scales with the square of the signal amplitude, so the loop bandwidth changes with the received level unless an automatic gain control keeps it fixed.

## Variants and improvements

- **Absolute-value gate.** $e = |y(t + d)| - |y(t - d)|$. Simon analyzed this form in 1970 and found it less noisy than two other bit synchronizers of that time.
- **Derivative form.** As $d \to 0$, $(|y(t + d)|^2 - |y(t - d)|^2)/(2d) \to 2\operatorname{Re}\{\overline{y(t)}\,y'(t)\}$. This is the non-data-aided maximum likelihood timing detector at low SNR. It needs a derivative filter instead of two extra samples.
- **Decision-directed gate.** $e = \operatorname{Re}\{\overline{\hat a_k}\,(y(t + d) - y(t - d))\}$ uses the decision $\hat a_k$. It removes most of the self-noise at high SNR, but it needs the carrier phase.
- **Integrate-and-dump gates.** For rectangular pulses, analog bit synchronizers integrate the signal over an early half and a late half of the symbol and compare the magnitudes. This is the classic form in telemetry receivers.
- **Delay-locked loop.** The same early-late structure on a known spreading code tracks the code phase; see [delay-locked loop](/delay-locked-loop/).
- **Fewer samples.** The [Gardner detector](/gardner-timing-error-detector/) needs two samples per symbol, and the [Mueller and Muller detector](/mueller-muller-timing-recovery/) needs one.

## When to use it

Use an early-late gate when the receiver has three samples per symbol or a continuous-time signal, the pulses have a clear excess bandwidth, and the timing must be found before the carrier. It is easy to build in analog hardware, which is why older bit synchronizers used it. In a digital modem at two samples per symbol, the Gardner detector does the same job with less self-noise. At high SNR with a known carrier phase, a decision-directed detector is more accurate.

## Pitfalls

- **Gate half-width $d = T/2$.** For raised cosine pulses, $\sin(2\pi d) = 0$ and the square-law gate has no restoring force. Use $d$ near $T/4$.
- **Wrong sign of the update.** The error is positive when the strobe is early. If the update subtracts it, the loop locks at the worst point, half a symbol from the peak.
- **Gain not divided by $K_D$.** The slope depends on $\beta$, $d$ and the signal power. Using a fixed $K_p$ for another roll-off or another level changes the loop bandwidth.
- **Too wide a loop.** The self-noise grows with $B_LT$. A loop that is fast enough for acquisition may be too noisy for tracking; switch to a narrower bandwidth after lock.
- **Small roll-off.** At $\beta = 0.1$ the slope is a fifth of that at $\beta = 0.5$, and the self-noise is relatively larger. Narrowband systems need a data-aided or decision-directed detector.

## Implementations

## History

Range trackers in radar keep a gate centered on an echo pulse by comparing the energy in an early half gate and a late half gate, and early bit synchronizers for digital telemetry used the same idea. Marvin K. Simon, at the Jet Propulsion Laboratory, published a nonlinear analysis of the absolute-value early-late gate bit synchronizer in 1970, with its S-curve and its steady-state timing error. With digital modems, the gate became a few lines of code on interpolated samples, as above, and later detectors such as Gardner's (1986) reduced the number of samples per symbol.

## References
