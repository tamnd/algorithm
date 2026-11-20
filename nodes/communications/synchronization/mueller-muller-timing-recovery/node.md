---
tag: BY94Z6
kind: algorithm
slug: mueller-muller-timing-recovery
name: Mueller and Muller timing recovery
aliases:
- Mueller-Muller detector
- M and M timing detector
area: communications/synchronization
level: core
summary: "A decision-directed timing loop at one sample per symbol. Its error is the strobe times the previous decision minus the previous strobe times the current decision."
solves: [symbol-timing-recovery]
model: real-ram
complexity:
  vars: {N: the number of symbols, M: the number of constellation points}
  time: {worst: O(N M), qpsk_or_square_qam: O(N)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, decision_directed: true, carrier_phase_invariant: false, samples_per_symbol: 1}
history:
  year: 1976
  people: [Kurt H. Mueller, Markus Müller]
  note: "Mueller and Müller published a family of timing functions computed at the symbol rate from samples and decisions in 1976. The detector on this page is its simplest member."
prereqs: [symbol-timing-recovery, phase-locked-loop]
see_also: [gardner-timing-error-detector, early-late-gate-synchronizer, oerder-meyr-timing-estimation, data-aided-synchronization, nyquist-isi-criterion, fractionally-spaced-equalizer, modified-cramer-rao-bound, quadrature-amplitude-modulation]
sources:
  - paper: doi:10.1109/TCOM.1976.1093326
    title: "K. H. Mueller and M. Müller, Timing recovery in digital synchronous data receivers, IEEE Transactions on Communications 24(5), 1976, pages 516 to 531"
    locator: "the timing functions computed from one sample per symbol and the decisions, and the function that equalizes the pulse samples one symbol before and after the peak"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 7 (timing recovery in baseband transmission) and Chapter 8 (timing recovery with linear modulations: the decision-directed detectors)"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Section 5.7 (timing error detectors at the symbol rate)"
---

Mueller and Muller timing recovery is a decision-directed feedback loop for [symbol timing recovery](/symbol-timing-recovery/) that needs only one sample per symbol. At each strobe it makes a decision $\hat a_k$, or uses a known symbol, and forms the error $e_k = \operatorname{Re}\{\overline{\hat a_{k-1}}\,y_k - \overline{\hat a_k}\,y_{k-1}\}$. With correct decisions the mean of $e_k$ is $g(1 - \Delta) - g(1 + \Delta)$, the difference between the pulse sample one symbol after the strobe and the one one symbol before it. So the loop settles where these two samples are equal, which is the peak for a symmetric pulse. For a pulse that meets the [Nyquist criterion](/nyquist-isi-criterion/), the error at lock is exactly zero for every data sequence, so there is no self-noise, unlike the [Gardner detector](/gardner-timing-error-detector/) and the [early-late gate](/early-late-gate-synchronizer/). The price is that the loop needs the carrier phase and correct decisions. The loop filter and accumulator are those of a [phase-locked loop](/phase-locked-loop/). The detector is common in receivers that run at the symbol rate, such as those with a symbol-spaced equalizer and many wireline links.

## In plain words

Each received pulse spreads a little into the time slots of its neighbors. If the receiver reads at the right instant, the parts that leak one slot forward and one slot backward are equal and cancel out in a suitable comparison. If it reads too early, more leaks forward than backward. The detector cannot see the leak directly, so it uses its own decisions about the symbols to separate it from the data. It compares the current reading with the previous symbol, and the previous reading with the current symbol, and the difference shows which way the timing is off. Only one reading per symbol is needed. The decisions must be mostly right, and the receiver must already know the phase of the carrier.

## The problem

Times are in symbol periods, $T = 1$. After carrier phase correction, the receiver can sample the matched filter output
$$y(t) = \sum_m a_m\,g(t - m - \tau) + v(t)$$
once per symbol, at times it controls, with an adjustable clock or with an interpolator. The overall pulse $g$ is real and even, the symbols $a_m$ come from a constellation such as [QAM](/quadrature-amplitude-modulation/) or PSK, independent with $E a_m = 0$ and $E|a_m|^2 = 1$, $v$ is filtered noise with $\mathrm{SNR} = E_s/N_0$, and the delay $\tau$ is unknown and may drift. The loop must output $\tau_k$ such that the strobes $y_k = y(k + \tau_k)$ fall on the symbol instants.

## The algorithm

```pseudo id=main
MUELLER-MULLER(y, N, Kp, Ki, tau0, points, known)
L1  tau <- tau0; s <- 0
L2  for k <- 0 to N - 1 do
L3      yk <- y(k + tau); est[k] <- tau
L4      ak <- known[k] if known symbols are given, else the nearest point to yk
L5      if k > 0 then
L6          e <- Re(conj(a_prev) * yk - conj(ak) * y_prev)
L7          s <- s + Ki * e                     ▷ loop filter
L8          tau <- tau + Kp * e + s             ▷ timing accumulator
L9      y_prev <- yk; a_prev <- ak
L10 return est, strobes, decisions
```

Line L4 is the slicer of a [minimum distance detector](/minimum-distance-detector/); with a preamble the same loop is data-aided. Line L6 is the detector. It is positive when the strobe is early, so line L8 adds it. Lines L7 and L8 are the PLL loop with the delay in place of the phase. The detector slope at lock is $K_D = -2g'(1)$, which for a raised cosine with roll-off $\beta$ is $2\cos(\pi\beta)/(1 - 4\beta^2)$: $2$ at $\beta = 0$, $\pi/2$ at $\beta = \frac12$ and $\frac23$ at $\beta = 1$. A first-order loop with noise bandwidth $B_LT$ uses $K_p = 4B_LT/\bigl((1 + 2B_LT)K_D\bigr)$.

## Example

Take QPSK data (seed 1), a raised cosine with $\beta = 0.5$, the true delay $\tau = 0.3$, no noise, $B_LT = 0.01$ and $K_i = 0$, so $K_p = 0.024965$. The loop starts at $\tau_0 = 0$. At $k = 0$ there is no previous symbol, so the loop only stores $y_0 = -0.702 + 0.490j$ and its decision $\frac{1}{\sqrt2}(-1 + j)$:

| $k$ | $\tau_k$ | $y_k$ (L3) | $\hat a_k \sqrt2$ (L4) | $e_k$ (L6) | $\tau_{k+1}$ (L8) |
|---|---|---|---|---|---|
| 1 | $0$ | $0.471 + 0.934j$ | $1 + j$ | $0.477137$ | $0.011912$ |
| 2 | $0.011912$ | $-0.410 - 0.537j$ | $-1 - j$ | $0.324561$ | $0.020015$ |
| 3 | $0.020015$ | $0.272 + 0.426j$ | $1 + j$ | $0.175586$ | $0.024398$ |

At $\Delta = 0.3$ the mean error is $g(0.7) - g(1.3) = 0.457816$. Every decision of the run is correct, even at the start: a QPSK eye with this roll-off is still open at an offset of $0.3$. The error $\tau - \tau_k$ is $0.225$ at $k = 10$, $0.124$ at $25$, $0.038$ at $50$, $4.2 \times 10^{-3}$ at $100$, $7.8 \times 10^{-5}$ at $200$ and $2.7 \times 10^{-8}$ at $400$. It keeps falling geometrically, because the error at lock is exactly zero: the loop has no self-noise.

In noise at $E_s/N_0 = 10$ dB with $B_LT = 0.01$, three runs of 2400 symbols (seeds 7, 8 and 9) measured a variance of $2.76$ to $3.62$ times the loop form of the [MCRB](/modified-cramer-rao-bound/), $2.66 \times 10^{-4}$. The closed form below predicts $3.05$.

## Correctness

**Claim.** With correct decisions, independent zero-mean data and $\tau_k$ held fixed, the mean of $e_k$ is $g(1 - \Delta) - g(1 + \Delta)$, $\Delta = \tau - \tau_k$, so $\Delta = 0$ is a stable point with slope $K_D = -2g'(1)$. If $g$ is a Nyquist pulse, $e_k = 0$ at $\Delta = 0$ for every data sequence when there is no noise. For PSK with correct decisions, the linear model gives the loop variance $2B_LT\,N_0/K_D^2$, which is $32\xi = 3.05$ times the loop MCRB for $\beta = \frac12$.

**Key steps.** The mean of $\overline{a_{k-1}}\,y_k$ picks the coefficient of $a_{k-1}$ in $y_k$, which is $g(1 - \Delta)$; the mean of $\overline{a_k}\,y_{k-1}$ is $g(-1 - \Delta) = g(1 + \Delta)$. At lock a Nyquist pulse gives $y_k = a_k$, and then $\overline{a_{k-1}}a_k - \overline{a_k}a_{k-1}$ is purely imaginary, so its real part is zero. The noise samples at the symbol rate are white with variance $N_0$, and the two noise terms of $e_k$ add up to the variance $N_0$. The full proof is in the proofs file.

The S-curve and the zero self-noise are theorems under the stated assumptions. The variance is a closed form under assumptions: the linear model, correct decisions and white detector noise. The measured ratios are a measurement.

## Complexity

Each symbol needs one sample (line L3), one decision, the real parts of two complex products (four real multiplications and three additions) and the four operations of lines L7 and L8. A slicer that tries all $M$ points costs $O(M)$; for QPSK and square QAM, slicing each axis separately costs $O(1)$. So the loop costs $O(NM)$ in general and $O(N)$ for QPSK and square QAM, for $N$ symbols in the [real RAM](/real-ram/), with $O(1)$ extra space besides the output. With an interpolator of $K$ taps, add $K$ multiply-adds per symbol.

## Properties

- **One sample per symbol.** This is the lowest possible rate. It suits receivers whose analog-to-digital converter or equalizer runs at the symbol rate.
- **No self-noise at lock.** For a Nyquist pulse the detector output is exactly zero at the correct timing, whatever the data. The loop variance comes from the noise alone.
- **Works with small roll-off.** The slope is $2$ at $\beta = 0$ and $\pi/2$ at $\beta = 0.5$, so the detector keeps its gain when the excess bandwidth is small, where square-law detectors lose theirs.
- **Needs the carrier phase.** A phase error $\phi$ rotates $y_k$ against $\hat a_k$ and scales the useful part of the error by $\cos\phi$; at large $\phi$ the decisions fail. Timing and carrier loops must therefore run together, or a data-aided start must come first.
- **Lock point for unequal pulse sides.** If the channel makes the pulse asymmetric, the loop locks where $g(1 - \Delta) = g(1 + \Delta)$, which is not the peak. With an equalizer after the sampler this is often a good point, but it is a different criterion.

## Variants and improvements

- **Data-aided form.** With known symbols in line L4 the loop works at any SNR and from any start inside its pull-in range. The tests start it at $\tau_0 = -0.15$ with a delay of $0.3$, an error of $0.45$, and it locks exactly.
- **Real baseband form.** For PAM, $e_k = \hat a_{k-1}y_k - \hat a_k y_{k-1}$, which is the form in the paper.
- **Other timing functions.** Mueller and Müller derive a family of timing functions, each zero at a different combination of pulse samples. The one on this page is the symmetric member.
- **Second-order loop.** $K_i > 0$ follows a clock frequency offset with zero mean error, as in the PLL.
- **Baud-rate clock recovery in wireline links.** Serial links that sample once per bit use detectors of this kind, often with the decisions of an adaptive equalizer.

## When to use it

Use Mueller and Muller timing recovery when the receiver samples at the symbol rate, the carrier phase is known or tracked jointly, and the SNR is high enough that most decisions are correct. It is also a good tracking loop after a data-aided start from a preamble. When the timing must lock before the carrier, use the [Gardner detector](/gardner-timing-error-detector/) at two samples per symbol. When the SNR is low, decision errors bend the S-curve, and a non-data-aided detector or a [data-aided](/data-aided-synchronization/) detector on pilots is safer.

## Pitfalls

- **Wrong sign of the update.** With the convention here, $e_k > 0$ when the strobe is early. Some texts write the error with the opposite sign and subtract it.
- **Running it before the carrier loop has locked.** Without the carrier phase, the decisions are wrong for a large share of the symbols and the detector output has no useful mean. Start with a data-aided phase or a phase-free timing detector.
- **Decision errors at low SNR.** Each wrong decision gives a wrong error value, and at low SNR the slope shrinks. The variance then exceeds the closed form.
- **Hang-up at a bad start.** If the start is about half a symbol off, the eye is closed and the decisions are random, so the loop can stay there for a long time. Use a preamble or a non-data-aided detector for acquisition.
- **Gain not divided by $K_D$.** $K_D$ depends on the pulse and on the signal level; use the slope of the actual pulse.

## Implementations

## History

Kurt H. Mueller and Markus Müller published the method in the IEEE Transactions on Communications in May 1976. They looked for timing functions that a receiver at one sample per symbol can compute from its samples and its decisions, and that become zero at a chosen point of the sampled pulse. Their symmetric function, which equalizes the two pulse samples next to the peak, became the standard symbol-rate timing detector. It is the usual choice in receivers whose equalizer runs at the symbol rate, and its descendants are used for clock recovery in high-speed wireline links.

## References
