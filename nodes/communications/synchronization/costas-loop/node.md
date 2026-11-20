---
tag: J5XYD4
kind: algorithm
slug: costas-loop
name: Costas loop
aliases:
- Costas phase-locked loop
area: communications/synchronization
level: core
summary: "A carrier loop for BPSK and QPSK. It splits each sample into in-phase and quadrature arms and drives a PLL with their product, so it locks modulo pi for BPSK and modulo pi/2 for QPSK."
solves: [carrier-recovery]
model: real-ram
complexity:
  vars: {N: the number of symbols}
  time: {worst: O(N)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, non_data_aided: true, phase_ambiguity: "pi for BPSK, pi/2 for QPSK"}
history:
  year: 1956
  people: [John P. Costas]
  note: "John P. Costas of General Electric proposed the loop in 1956 to receive double-sideband suppressed-carrier signals, which have no carrier tone for an ordinary PLL to lock to."
prereqs: [phase-locked-loop, phase-shift-keying]
see_also: [squaring-loop, decision-directed-carrier-recovery, viterbi-viterbi-phase-estimation, cycle-slip, data-aided-synchronization, differential-phase-shift-keying, quadrature-amplitude-modulation, symbol-timing-recovery]
sources:
  - paper: doi:10.1109/JRPROC.1956.275063
    title: "J. P. Costas, Synchronous communications, Proceedings of the IRE 44(12), 1956, pages 1713 to 1718"
    locator: "the receiver with an in-phase and a quadrature arm whose product controls the local oscillator, for suppressed-carrier transmission"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 5.2-5 (non-decision-directed loops: the squaring loop and the Costas loop)"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 5 (carrier phase recovery with linear modulations, the feedback and non-data-aided schemes)"
---

The Costas loop recovers the carrier phase of a BPSK or QPSK signal, whose spectrum has no carrier tone. It rotates each sample by the current phase estimate and splits it into an in-phase arm $I$ and a quadrature arm $Q$. For BPSK, the product $IQ$ is $\frac12 \sin 2\Delta$ for the phase error $\Delta$ whatever the data symbol is, so it can drive the loop filter and the oscillator of a [phase-locked loop](/phase-locked-loop/). It is one of the classic solutions of [carrier recovery](/carrier-recovery/). For BPSK it gives exactly the same phase as the [squaring loop](/squaring-loop/) with the same gains, and for QPSK the hard-limited Costas detector is $\sqrt2$ times the detector of [decision-directed carrier recovery](/decision-directed-carrier-recovery/). The feedforward [Viterbi and Viterbi estimator](/viterbi-viterbi-phase-estimation/) removes the data in the same way, but over a block and without feedback. Like every estimator that does not know the data, the loop locks only modulo $\pi$ for BPSK and modulo $\pi/2$ for QPSK, and in noise it can jump between these points; see [cycle slip](/cycle-slip/).

## In plain words

A BPSK signal flips its sign with each data bit. An ordinary phase-locked loop sees the flips as phase jumps of half a turn and cannot follow them. The Costas loop looks at the signal along two directions at once, the direction it thinks is right and the one at a right angle to it. If its guess is a little off, part of the signal leaks into the second direction. The product of the two parts tells which way the guess is off, and the sign of the data cancels in the product. The loop corrects its guess with this product, as a normal loop does. It cannot tell the right phase from the opposite one, because a flipped signal with flipped data looks the same.

## The problem

The input is $r_k = a_k e^{j\theta_k} + w_k$, $k = 0, \ldots, N - 1$, at one sample per symbol after matched filtering and correct symbol timing. The data $a_k$ are unknown, independent and uniform on BPSK $\{+1, -1\}$ or on QPSK $\{e^{j(\pi/4 + m\pi/2)}\}$, so $E_s = 1$. The noise is $w_k \sim \mathcal{CN}(0, N_0)$, white, and $\mathrm{SNR} = E_s/N_0$. The carrier phase $\theta_k$ is unknown and changes slowly, for example $\theta_k = \theta_0 + \omega k$. The loop must output a phase estimate $\phi_k$ from $r_0, \ldots, r_{k-1}$. Because of the symmetry of the constellation, the goal is $\phi_k \to \theta_k$ modulo $\pi$ (BPSK) or $\pi/2$ (QPSK).

## The algorithm

```pseudo id=main
COSTAS(r[0..N-1], Kp, Ki, mod, phi0)
L1  phi <- phi0; s <- 0
L2  for k <- 0 to N - 1 do
L3      est[k] <- phi
L4      z <- r[k] * exp(-j * phi); I <- Re z; Q <- Im z     ▷ the two arms
L5      if mod = BPSK then e <- I * Q
            else e <- sgn(I) * Q - sgn(Q) * I               ▷ QPSK
L6      s <- s + Ki * e                                      ▷ loop filter
L7      phi <- phi + Kp * e + s                              ▷ oscillator
L8  return est
```

Line L4 is the derotation. In an analog receiver it is two mixers, one with the cosine and one with the sine of the oscillator, each followed by a low-pass filter; at one sample per symbol after the matched filter the two arms are the real and imaginary parts of one complex product. Line L5 is the Costas phase detector. For BPSK, $IQ = \frac12 \operatorname{Im}(z^2)$, which shows how the data are removed: the square of $\pm1$ is $1$. For QPSK, each arm is hard-limited to its sign and multiplied by the other arm; this detector has gain $K_d = \sqrt2$ near lock, against $K_d = 1$ for BPSK. Lines L6 and L7 are the second-order loop of the PLL. The gains come from the PLL design rule for a noise bandwidth $B_L T$ and damping $\zeta$, divided by $K_d$.

## Example

Take BPSK, $B_L T = 0.02$ and $\zeta = 1/\sqrt2$, so $K_p = 0.053333$ and $K_i = 0.0014222$. The carrier phase is $\theta = 0.7$ rad, there is no noise, and the data are random (seed 1). Since $IQ = \frac12 \sin 2\Delta$ for both symbols, the first steps do not depend on the data:

| $k$ | $\phi$ (line L3) | $e$ (line L5) | $s$ (line L6) | new $\phi$ (line L7) |
|---|---|---|---|---|
| 0 | $0$ | $0.492725$ | $0.000701$ | $0.026979$ |
| 1 | $0.026979$ | $0.487424$ | $0.001394$ | $0.054369$ |
| 2 | $0.054369$ | $0.480592$ | $0.002077$ | $0.082078$ |

The phase error $0.7 - \phi_k$ is $0.42297$ at $k = 10$, $0.08816$ at $25$, $-0.13253$ at $50$ (the overshoot reaches $-0.1461$), $-0.06821$ at $100$, $0.00449$ at $200$ and $-0.00023$ at $300$. From $k = 300$ on it stays below $10^{-3}$ rad.

The ambiguity is visible with $\theta = 2.0$. The initial error $2.0$ is beyond $\pi/2$, so the loop moves to the stable point $\pi$ away and settles at $\phi = 2.0 - \pi = -1.1416$. In this lock, every decision is inverted. For QPSK with $\theta = 1.0$, the loop settles at $1.0 - \pi/2 = -0.5708$. A receiver resolves this with a known preamble or with [differential encoding](/differential-phase-shift-keying/).

In noise at $\mathrm{SNR} = 10$ (10 dB) and $B_L T = 0.01$ (exact digital value $0.010181$), the linear model gives $1.069 \times 10^{-3}$ rad$^2$ for BPSK, which includes the squaring loss $1 + 1/(2 \cdot 10) = 1.05$, and $1.018 \times 10^{-3}$ for QPSK. A simulation of 40000 symbols (seeds 3 and 4) measured $1.019 \times 10^{-3}$ and $9.74 \times 10^{-4}$, ratios of $0.95$ and $0.96$.

## Correctness

**Claim.** Without noise, the BPSK detector of line L5 outputs $\frac12 \sin 2\Delta$ and the QPSK detector outputs $\sqrt2 \sin\Delta$ for $|\Delta| < \pi/4$, with period $\pi/2$, for every data symbol. So the loop locks to $\theta$ modulo $\pi$ (BPSK) or $\pi/2$ (QPSK), with the steady-state behavior of the PLL. For BPSK in the linear model, the phase error variance is $\frac{B_L T}{\mathrm{SNR}}\bigl(1 + \frac{1}{2\,\mathrm{SNR}}\bigr)$.

**Key steps.** For BPSK, $z = a e^{j\Delta}$ with $a^2 = 1$ gives $IQ = \frac12 \sin 2\Delta$, and with $\psi = 2\phi$ the loop is a PLL on $r^2$, which is the squaring loop. For QPSK, the detector does not change when $z$ is multiplied by $j$, so one symbol suffices. Near lock, $e = \Delta + a n_Q + n_I n_Q$ for BPSK, and the term $n_I n_Q$, noise times noise, adds the factor $1 + N_0/2$ to the variance. The full proof is in the proofs file.

The variance formula is a closed form under assumptions: the linear model, white Gaussian noise, correct timing and a constant amplitude. The equality between the BPSK Costas loop and the squaring loop is exact.

## Complexity

Each symbol costs one complex rotation, one real multiplication (BPSK) or two multiplications and two sign tests (QPSK) for the detector, and the five operations of the loop filter and the oscillator. That is $O(1)$ per symbol, $O(N)$ for $N$ symbols in the [real RAM](/real-ram/), and $O(1)$ extra space. The loop is sequential, like every feedback loop.

## Properties

- **Non-data-aided.** The loop needs no known symbols and no decisions for BPSK. The QPSK detector uses the signs of the arms, which are hard decisions, so at low SNR it behaves like a decision-directed loop with wrong decisions; see [data-aided synchronization](/data-aided-synchronization/).
- **Squaring loss.** For BPSK, the noise times noise term raises the variance by $1 + 1/(2\,\mathrm{SNR})$ over that of a loop that knows the data: by 1.05 at 10 dB and by 1.5 at 0 dB.
- **Phase ambiguity.** The stable points are spaced by $\pi$ (BPSK) or $\pi/2$ (QPSK). Which point the loop picks depends on the start. Cycle slips move the loop between them.
- **Detector gain depends on amplitude.** The BPSK S-curve scales with $A^2$, the square of the signal amplitude, and the QPSK detector scales with $A$. An automatic gain control keeps the loop bandwidth fixed.
- **Steady state.** The second-order filter tracks a frequency offset with zero error, as in the PLL; the tests check this for $0.001$ cycles per symbol.

## Variants and improvements

- **Analog Costas loop.** The original loop multiplies the received passband signal with the cosine and the sine of a voltage-controlled oscillator, filters both products and multiplies the two arms. The arm filters must pass the data, and they add delay to the loop.
- **Soft QPSK detector.** $e = IQ(I^2 - Q^2)$, which is $\frac14 \operatorname{Im}(z^4)$, is the fourth-power detector of the [squaring loop](/squaring-loop/) with $M = 4$. The hard-limited form of line L5 has less noise at moderate and high SNR.
- **Decision-directed loop.** Replacing $\operatorname{sgn}(I)$ and $\operatorname{sgn}(Q)$ by the nearest constellation point extends the idea to QAM; see [decision-directed carrier recovery](/decision-directed-carrier-recovery/).
- **Hyperbolic tangent detector.** For BPSK, the maximum likelihood detector averaged over the data uses $\tanh(2I/N_0)\, Q$. It becomes $IQ$ at low SNR, up to a constant, and $\operatorname{sgn}(I)\, Q$ at high SNR.
- **Feedforward estimation.** For short bursts, the [Viterbi and Viterbi estimator](/viterbi-viterbi-phase-estimation/) uses the same power law on a block and has no acquisition time.

## When to use it

Use a Costas loop for continuous BPSK or QPSK transmission when no pilot tone is sent and the SNR is moderate. It is simple, it needs no decisions for BPSK, and it was the standard carrier loop for suppressed-carrier links, including deep-space links. Use the decision-directed loop for QAM, a data-aided estimate when a preamble or pilots are present, and a feedforward block estimator for short bursts.

## Pitfalls

- **Gains not divided by the detector gain.** The QPSK detector of line L5 has $K_d = \sqrt2$. Using the BPSK gains for QPSK makes the loop $\sqrt2$ times wider than designed.
- **Ignoring the ambiguity.** A Costas loop can lock with an error of $\pi$ (BPSK) or a multiple of $\pi/2$ (QPSK), and nothing in the loop shows it. Every decision is then wrong or rotated. Use a unique word, a preamble or differential encoding.
- **Too large a frequency offset.** The S-curve of BPSK has period $\pi$, half that of a PLL, and that of QPSK has period $\pi/2$. A large initial frequency error makes the loop slip between ambiguity points instead of locking. Remove the coarse offset first.
- **Wrong timing.** The detector assumes samples at the symbol centers. With a timing error, intersymbol interference adds self noise to $I$ and $Q$, and the loop variance grows even without channel noise.
- **Using BPSK on a QPSK signal.** For QPSK, $IQ$ averages to zero over the data, so the BPSK detector gives no restoring force.

## Implementations

## History

John P. Costas, at General Electric, published the loop in 1956 in a paper that argued for double-sideband suppressed-carrier transmission instead of single-sideband. Such a signal has no carrier for an ordinary phase-locked loop, and his receiver recovered the carrier from the product of the in-phase and the quadrature channels. The loop became the standard carrier recovery circuit for BPSK and QPSK in satellite and deep-space links. In digital receivers it is a few lines of code, as above. The same J. P. Costas later described the Costas arrays used in radar, which are a different subject.

## References
