---
tag: YWG207
kind: algorithm
slug: phase-locked-loop
name: Phase-locked loop
aliases:
- PLL
- digital phase-locked loop
area: communications/synchronization
level: intro
summary: "A feedback loop that makes a local oscillator follow the phase of an input. With a phase detector, a PI loop filter and an NCO, it tracks phase and frequency steps with zero steady-state error."
solves: [carrier-recovery]
model: real-ram
complexity:
  vars: {N: the number of samples}
  time: {worst: O(N)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, feedback: true, exact: false}
history:
  year: 1932
  people: [Henri de Bellescize, Andrew J. Viterbi]
  note: "Henri de Bellescize described synchronous reception with a phase-locked oscillator in 1932. Andrew Viterbi gave the nonlinear analysis of the loop in noise with Fokker-Planck methods in 1963."
prereqs: [z-transform, linear-time-invariant-system, additive-white-gaussian-noise-channel]
see_also: [costas-loop, squaring-loop, decision-directed-carrier-recovery, cycle-slip, delay-locked-loop, symbol-timing-recovery, kalman-filter, iir-filter]
sources:
  - book: isbn:9780471430636
    title: "Floyd M. Gardner, Phaselock Techniques, third edition, Wiley, 2005"
    locator: "Chapters 2 and 4 (transfer functions of analog and digital loops), Chapter 6 (effects of additive noise, the noise bandwidth), Chapter 8 (acquisition) and Chapter 13 (digital sampled loops)"
  - paper: doi:10.1109/PROC.1963.2686
    title: "A. J. Viterbi, Phase-locked loop dynamics in the presence of noise by Fokker-Planck techniques, Proceedings of the IEEE 51(12), 1963, pages 1737 to 1753"
    locator: "the nonlinear model of the loop in noise, the stationary distribution of the phase error and the time to loss of lock"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 5.2-2 (the phase-locked loop) and Section 5.2-3 (effect of additive noise on the phase estimate)"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Chapter 6 (performance analysis of synchronizers, the tracking performance of feedback loops)"
---

A phase-locked loop (PLL) makes a local oscillator follow the phase of an input signal. It measures the phase difference between the input and the oscillator with a *phase detector*, smooths it with a *loop filter*, and uses the result to advance the oscillator. This page is the digital loop at one complex sample per symbol, with a proportional-plus-integral filter and a numerically controlled oscillator (NCO). It is the basic tool of [carrier recovery](/carrier-recovery/). The [Costas loop](/costas-loop/), the [squaring loop](/squaring-loop/) and [decision-directed carrier recovery](/decision-directed-carrier-recovery/) are this loop with a different phase detector, which removes the data modulation first. The feedforward [Viterbi and Viterbi estimator](/viterbi-viterbi-phase-estimation/) solves the same problem without feedback, and a [cycle slip](/cycle-slip/) is the main failure of a loop in noise. The second-order loop on this page has two integrators, so in its linear model it follows both a phase step and a frequency step with zero error in the steady state. Its phase error variance in white noise is $B_L T/\mathrm{SNR}$, where $B_L T$ is the noise bandwidth of the loop.

## In plain words

Think of a clock that must keep time with a reference clock it can only glance at. At each tick you compare the two hands and see how far yours is ahead or behind. You do not jump to the reference at once, because each glance is a little noisy. You move your hand by a small part of the difference. You also keep a running memory of the differences. If your clock is always behind, the memory grows and you start to run your clock faster, until it runs at the same speed as the reference. Small corrections give a steady clock that reacts slowly. Large corrections react fast but carry more of the noise into your clock.

## The problem

The input is a sequence of complex samples $r_k = A e^{j\theta_k} + w_k$, $k = 0, \ldots, N-1$, with an unknown phase $\theta_k$ that changes slowly, and noise $w_k \sim \mathcal{CN}(0, N_0)$ that is white and circular, as on the [AWGN channel](/additive-white-gaussian-noise-channel/). Here the data modulation is already removed, or the input is an unmodulated pilot tone, and $A = 1$, so $E_s = 1$ and the signal-to-noise ratio is $\mathrm{SNR} = E_s/N_0 = 1/N_0$. The loop must output, for each $k$, an estimate $\phi_k$ of $\theta_k$ that uses only $r_0, \ldots, r_{k-1}$. Typical inputs are a phase offset $\theta_k = \theta_0$ and a frequency offset $\theta_k = \theta_0 + \omega k$, where $\omega$ is in radians per symbol.

## The algorithm

```pseudo id=main
PLL(r[0..N-1], Kp, Ki, phi0)
L1  phi <- phi0; s <- 0
L2  for k <- 0 to N - 1 do
L3      est[k] <- phi                       ▷ the estimate used on r[k]
L4      e <- Im(r[k] * exp(-j * phi))       ▷ phase detector: sin(theta - phi) + noise
L5      s <- s + Ki * e                      ▷ integral path of the loop filter
L6      phi <- phi + Kp * e + s              ▷ NCO: add the filter output to the phase
L7  return est
```

Line L4 rotates the sample back by the current estimate. Without noise, the imaginary part of $e^{j(\theta - \phi)}$ is $\sin(\theta - \phi)$, which is close to the phase error $\theta - \phi$ when the error is small, so the detector gain is $K_d = 1$. Lines L5 and L6 together are the loop filter $F(z) = K_p + K_i/(1 - z^{-1})$ followed by the oscillator, an accumulator. The integrator $s$ of line L5 learns the frequency offset: when the loop is locked to a frequency $\omega$, $s = \omega$ and $e = 0$. The phase $\phi$ is not reduced modulo $2\pi$, so it follows a frequency offset without jumps.

The gains come from two design values, the noise bandwidth $B_L T$ (normalized to the symbol rate) and the damping $\zeta$. The usual rule, taken from the analog loop and accurate for small $B_L T$, is

$$\omega_n T = \frac{2 B_L T}{\zeta + 1/(4\zeta)}, \qquad K_d K_p = 2\zeta\,\omega_n T, \qquad K_d K_i = (\omega_n T)^2.$$

For $\zeta = 1/\sqrt2$ this is $K_p = \frac83 B_L T$ and $K_i = \frac{32}{9} (B_L T)^2$. The exact noise bandwidth of the digital loop is $B_L T = \frac12 \sum_k h_k^2$, with $h$ the impulse response of the closed loop, and the proof gives it in closed form.

## Example

Take $B_L T = 0.02$ and $\zeta = 1/\sqrt2$. The rule gives $K_p = 0.053333$ and $K_i = 0.0014222$, and the exact noise bandwidth of this digital loop is $0.020738$. The input has the constant phase $\theta = 0.7$ rad, with no noise, and the loop starts at $\phi = 0$.

| $k$ | $\phi$ (line L3) | $e$ (line L4) | $s$ (line L5) | new $\phi$ (line L6) |
|---|---|---|---|---|
| 0 | $0$ | $0.644218$ | $0.000916$ | $0.035274$ |
| 1 | $0.035274$ | $0.616843$ | $0.001794$ | $0.069966$ |
| 2 | $0.069966$ | $0.589172$ | $0.002631$ | $0.104020$ |

The phase error $\theta - \phi_k$ then evolves as follows. It overshoots to $-0.1470$ at $k = 58$, as a loop with this damping does, and it stays below $10^{-3}$ from $k = 300$ on.

| $k$ | 0 | 10 | 25 | 50 | 100 | 150 | 200 | 300 |
|---|---|---|---|---|---|---|---|---|
| error (rad) | $0.7$ | $0.3789$ | $0.0560$ | $-0.1389$ | $-0.0634$ | $0.00146$ | $0.00427$ | $-0.00023$ |

With a frequency offset of $0.002$ cycles per symbol added, $\theta_k = 0.7 + 0.012566\,k$, the errors at $k = 100$, $200$, $300$ and $400$ are $-0.0494$, $0.00262$, $-9.5 \times 10^{-5}$ and $-5.3 \times 10^{-8}$, and the error at $k = 2999$ is $0$ to double precision. The integrator $s$ has learned $\omega = 0.012566$.

In noise, the linear model predicts the variance $B_L T/\mathrm{SNR}$. For $B_L T = 0.01$ (exact value $0.010181$) and $\mathrm{SNR} = 10$ (10 dB), that is $1.018 \times 10^{-3}$ rad$^2$, a standard deviation of 1.83 degrees. A simulation of 60000 samples with seed 5, after 2000 samples of settling, measured $9.60 \times 10^{-4}$, a ratio of $0.94$.

## Correctness

**Claim.** If $0 < K_p < 2$, $K_i > 0$ and $2K_p + K_i < 4$, then in the linear model the loop is stable, it follows $\theta_k = \theta_0 + \omega k$ with an error that tends to zero, and in noise its phase error has variance $N_0 B_L T = B_L T/\mathrm{SNR}$ with $B_L T = \frac12 \sum_k h_k^2$.

**Key steps.** Line L4 outputs $\sin(\theta_k - \phi_k)$ plus a noise term $n_k$ of variance $N_0/2$, white, because a rotation does not change the law of circular Gaussian noise. With $\sin x \approx x$, the closed loop from $\theta$ to $\phi$ is

$$H(z) = \frac{(K_p + K_i) z - K_p}{z^2 + (K_p + K_i - 2) z + (1 - K_p)},$$

and the Jury test on the denominator gives the three conditions. The error transfer $1 - H(z)$ has the factor $(z - 1)^2$, which cancels the double pole of a phase ramp, so the error tends to zero. The noise enters at the same point as $\theta$, so its contribution has variance $\frac{N_0}{2} \sum h_k^2$. The full proof is in the proofs file, together with the closed form of $\sum h_k^2$.

The linear model is a closed form under assumptions: small phase errors, white Gaussian noise and a constant input amplitude. For large errors, the sine of line L4 matters. Its slope is negative near $\pm\pi$, so the error point $\pi$ is an unstable equilibrium, and in noise the loop can leave the stable point and slip by $2\pi$; see [cycle slip](/cycle-slip/).

## Complexity

Each sample costs one complex exponential (a cosine and a sine, or a table lookup in an NCO), two real multiplications for the imaginary part of line L4, and three multiplications and four additions in lines L5 and L6. That is $O(1)$ per sample and $O(N)$ for $N$ samples in the [real RAM](/real-ram/), with $O(1)$ extra space for $\phi$ and $s$. The loop is sequential: each step needs the phase from the step before, so it does not split over parallel hardware without a change of structure.

## Properties

- **Steady-state errors.** In the linear model, a phase step and a frequency step give zero error in the steady state (Theorem 1 of the proof). A frequency ramp $\theta_k = \alpha k^2/2$, such as the Doppler of an accelerating receiver, gives the constant error $\alpha/K_i$.
- **Noise and speed are traded by one number.** The variance $B_L T/\mathrm{SNR}$ grows with the bandwidth, and the settling time falls like $1/B_L T$. In the example, the error falls below $10^{-3}$ rad in about $6/B_L T$ symbols.
- **Design rule against exact bandwidth.** The analog formula is a rule for small $B_L T$. For $\zeta = 1/\sqrt2$ the exact values are $0.0050449$, $0.010181$, $0.020738$, $0.054893$ and $0.12176$ for the design values $0.005$, $0.01$, $0.02$, $0.05$ and $0.1$.
- **Lock-in range.** The loop locks without a slip only if the initial frequency error is small. The usual rule, from Gardner (Chapter 8), puts the lock-in range at about $2\zeta\omega_n$ radians per symbol. Beyond it, the loop pulls in slowly, with slips, or not at all.
- **Hang-up.** If the initial error is near $\pi$, the detector output is near zero and the restoring force is weak, so the loop can stay near the wrong point for a long time before it locks.
- **Dependence on amplitude.** The detector gain is the amplitude $A$ of the input. If $A$ changes, the gains $K_d K_p$ and $K_d K_i$ change and the bandwidth and damping move. Real receivers put an automatic gain control before the loop or normalize the detector output.

## Variants and improvements

- **First-order loop.** Set $K_i = 0$. The loop is simpler and always stable for $0 < K_p < 2$, but a frequency offset $\omega$ leaves the steady-state error $\arcsin(\omega/K_p)$, and the loop cannot lock if $|\omega| > K_p$.
- **Third-order loop.** Add a second integrator to the filter to follow a frequency ramp with zero error. It needs more care for stability.
- **Other phase detectors.** For a modulated input, the detector must remove the data. The [Costas loop](/costas-loop/) multiplies the in-phase and quadrature arms, the [squaring loop](/squaring-loop/) raises the sample to the power $M$, and the [decision-directed loop](/decision-directed-carrier-recovery/) compares the sample with the decided symbol. Each gives a phase ambiguity of $2\pi/M$.
- **Frequency-aided loops.** A frequency-locked loop, or a coarse estimate from a [frequency offset estimator](/frequency-offset-estimation/), removes most of the frequency error before the PLL starts, which avoids slow pull-in.
- **Kalman form.** For a phase that is a random walk with a random-walk frequency, the steady-state [Kalman filter](/kalman-filter/) has the same structure as this second-order loop, with gains set by the noise variances.
- **Delay and timing loops.** The same loop with a timing error detector tracks the symbol clock in [symbol timing recovery](/symbol-timing-recovery/), and with a code correlator it is the [delay-locked loop](/delay-locked-loop/).

## When to use it

Use a PLL to track a carrier phase that drifts during a long or continuous transmission, when the signal has a pilot tone or the data can be removed by a detector. A loop is cheap, works sample by sample and follows slow changes of frequency. For short bursts, a feedforward estimator such as [Viterbi and Viterbi](/viterbi-viterbi-phase-estimation/) or a data-aided estimate over a preamble needs no acquisition time and has no cycle slips, so it is the better choice. At low SNR, a loop with a narrow bandwidth keeps the variance small but acquires slowly; use a frequency estimate first.

## Pitfalls

- **Wrapping the phase.** If line L6 reduces $\phi$ modulo $2\pi$ and a later step compares phases, the jump at the wrap looks like a large error. Keep $\phi$ unwrapped, or wrap only where the phase is used in line L4, where the exponential does not care.
- **The analog formula at large bandwidth.** The rule gives $B_L T = 0.12176$ for a design value of $0.1$. Check the exact bandwidth with the closed form when $B_L T$ is above about $0.02$.
- **Delay in the loop.** A hardware loop often has a pipeline delay between line L4 and the use of the new $\phi$. One extra symbol of delay changes the characteristic polynomial to third order and shrinks the stable region. Design with the delay in the model.
- **Unstable gains.** Gains outside the Jury region do not make the phase grow without limit, because the sine of line L4 saturates. The loop swings instead: the tests show $K_p = 1.9$ and $K_i = 0.5$ held in an oscillation of about $\pm0.65$ rad. This can look like a noisy lock.
- **Forgetting the detector gain.** For a signal with amplitude $A \ne 1$, or for a Costas detector with $K_d = \sqrt2$, the same $K_p$ and $K_i$ give a different loop. Divide the gains by $K_d$.
- **Sign of the detector.** With $e = \operatorname{Im}(r^\ast e^{j\phi})$, the sign of the error is reversed and the loop moves away from lock. The rotation of line L4 must be by $-\phi$.

## Implementations

## History

Henri de Bellescize described synchronous reception of radio signals with a phase-locked local oscillator in 1932. In the 1940s, phase-locked circuits kept the horizontal scan of television receivers in step with the transmitter. In the 1950s, the space program used loops to track the weak carriers of satellites, and Jaffe and Rechtin gave a design of loop filters for such signals in 1955. Andrew Viterbi analyzed the nonlinear loop in noise in 1963 with Fokker-Planck methods, and found the distribution of the phase error and the rate of loss of lock. Floyd Gardner's book Phaselock Techniques (first edition 1966) made the loop a standard tool of engineers. With digital receivers, the loop became an all-digital recursion such as the one on this page.

## References
