---
tag: PVGB8C
kind: algorithm
slug: squaring-loop
name: Squaring loop
aliases:
- squaring carrier recovery
- Mth-power loop
area: communications/synchronization
level: core
summary: "Raises each M-PSK sample to the power M, which removes the data and leaves a tone at M times the carrier phase. A PLL locks to the tone, and the phase divided by M is correct modulo 2 pi/M."
solves: [carrier-recovery]
model: real-ram
complexity:
  vars: {N: the number of symbols, M: the number of PSK phases}
  time: {worst: O(N log M)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, non_data_aided: true, phase_ambiguity: 2 pi/M}
history:
  year: 1973
  people: [William C. Lindsey, Marvin K. Simon]
  note: "Squaring loops came into use with suppressed-carrier links next to the Costas loop. Lindsey and Simon described the loss of both loops against a loop with a carrier by one factor, the squaring loss, in 1973."
prereqs: [phase-locked-loop, phase-shift-keying]
see_also: [costas-loop, viterbi-viterbi-phase-estimation, decision-directed-carrier-recovery, cycle-slip, data-aided-synchronization, differential-phase-shift-keying, noncoherent-detection, modified-cramer-rao-bound]
sources:
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 5.2-5 (non-decision-directed loops: the squaring loop, the Mth-power loop and the Costas loop, with their squaring losses)"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 5 (carrier phase recovery with linear modulations, the non-data-aided schemes for PSK)"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Chapter 6 (performance analysis of synchronizers, the tracking performance of feedback loops)"
---

The squaring loop recovers the carrier of a suppressed-carrier signal by removing the modulation with a power law. For BPSK, squaring the sample turns both symbols $\pm1$ into $1$, so $r^2$ has a tone at twice the carrier phase. For M-PSK, the power $M$ does the same: every symbol $a$ satisfies $a^M = e^{jM\phi_c}$. A [phase-locked loop](/phase-locked-loop/) then locks to the tone, and its phase divided by $M$ estimates the carrier phase modulo $2\pi/M$. It is a classic algorithm of [carrier recovery](/carrier-recovery/). For BPSK it gives exactly the same phase as the [Costas loop](/costas-loop/) with the same gains. The [Viterbi and Viterbi estimator](/viterbi-viterbi-phase-estimation/) uses the same power, but averages over a block instead of feeding a loop. Compared with [decision-directed carrier recovery](/decision-directed-carrier-recovery/), the squaring loop needs no decisions, but the power multiplies noise with noise, which raises the phase variance by the *squaring loss*. Under strong noise, the loop jumps between its $M$ lock points; see [cycle slip](/cycle-slip/).

## In plain words

A PSK signal moves its phase between a few fixed positions to carry data. The receiver does not know the data, so it cannot simply follow the phase. If you multiply each phase by the number of positions, all the positions fall on top of each other. The data disappear, and what is left is one steady signal whose phase is a multiple of the carrier phase. An ordinary loop can lock onto that. Divide its phase by the same number and you have the carrier phase. The price is twofold. You cannot tell which of the positions is the true one, and the multiplication makes the noise stronger.

## The problem

The input is $r_k = a_k e^{j\theta_k} + w_k$, $k = 0, \ldots, N - 1$, one sample per symbol, where $a_k = e^{j(\phi_c + 2\pi m_k/M)}$ is an M-PSK symbol with unknown index $m_k$ and known constellation phase $\phi_c$ ($\phi_c = 0$ for BPSK, $\phi_c = \pi/4$ for QPSK), so $E_s = 1$. The noise is $w_k \sim \mathcal{CN}(0, N_0)$, white, and $\mathrm{SNR} = E_s/N_0$. The loop must output phase estimates $\phi_k$ from the past samples, with $\phi_k \to \theta_k$ modulo $2\pi/M$.

## The algorithm

```pseudo id=main
SQUARING-LOOP(r[0..N-1], M, Kp, Ki, phase0, phi0)
L1  psi <- M * phi0; s <- 0                    ▷ psi tracks M times the carrier phase
L2  for k <- 0 to N - 1 do
L3      est[k] <- psi / M
L4      y <- r[k]^M * exp(-j * M * phase0)      ▷ the data are gone: a^M = exp(j M phase0)
L5      e <- Im(y * exp(-j * psi))              ▷ PLL phase detector: sin(M theta - psi)
L6      s <- s + Ki * e
L7      psi <- psi + Kp * e + s
L8  return est
```

Line L4 is the power law. For QPSK, $r^4$ alone gives $-e^{j4\theta}$, because $(e^{j\pi/4})^4 = -1$; the factor $e^{-jM\phi_c}$ removes this sign. Lines L5 to L7 are the second-order PLL acting on $\psi$, with detector gain $1$, so its gains come from the PLL design rule for the noise bandwidth $B_L T$ of the loop on $\psi$. Line L3 divides by $M$. In an analog receiver, line L4 is a squarer or an Mth-law device followed by a band-pass filter at $M$ times the carrier frequency, and the PLL output is passed through a frequency divider by $M$.

## Example

Take QPSK, $\phi_c = \pi/4$, a carrier phase $\theta = 0.7$ rad, no noise and random data (seed 1), with the loop gains for $B_L T = 0.02$: $K_p = 0.053333$ and $K_i = 0.0014222$. Line L4 gives $y = e^{j2.8}$ for every symbol, so line L5 outputs $\sin(2.8 - \psi)$:

| $k$ | $\psi$ | est (line L3) | $e$ (line L5) | $s$ (line L6) | new $\psi$ (line L7) |
|---|---|---|---|---|---|
| 0 | $0$ | $0$ | $0.334988$ | $0.000476$ | $0.018342$ |
| 1 | $0.018342$ | $0.004586$ | $0.352214$ | $0.000977$ | $0.038105$ |
| 2 | $0.038105$ | $0.009526$ | $0.370639$ | $0.001504$ | $0.059376$ |

The start is near the edge of the S-curve, where $\sin(2.8 - \psi)$ is small, so the loop moves slowly at first. The error $0.7 - \mathrm{est}_k$ is $0.63527$ at $k = 10$, $0.42495$ at $25$, $-0.01135$ at $50$, $-0.1098$ at $100$, $0.00589$ at $200$ and $-0.00021$ at $300$. It stays below $10^{-3}$ from $k = 257$ on. For 8-PSK and the same $\theta = 0.7$, the start is beyond $\pi/8$, and the loop settles at $0.7 - \pi/4 = -0.0854$ instead.

The noise is amplified by the power. With $B_L T = 0.01$ (exact digital value $0.010181$), the linear model gives the variance $B_L T\, N_0 \cdot L$, where the squaring loss $L$ is $1 + N_0/2$ for $M = 2$ and $1 + 4.5N_0 + 6N_0^2 + 1.5N_0^3$ for $M = 4$:

| case | squaring loss | predicted variance | measured (40000 symbols) | ratio |
|---|---|---|---|---|
| $M = 2$, 10 dB, seed 1 | $1.050$ | $1.069 \times 10^{-3}$ | $1.073 \times 10^{-3}$ | $1.00$ |
| $M = 4$, 10 dB, seed 2 | $1.512$ | $1.539 \times 10^{-3}$ | $1.534 \times 10^{-3}$ | $1.00$ |
| $M = 4$, 6 dB, seed 3 | $2.533$ | $6.48 \times 10^{-3}$ | $6.78 \times 10^{-3}$ | $1.05$ |

At 3 dB the linear model breaks down. In the same setup with seed 5, the QPSK loop moved between lock points 52 times in 40000 symbols and ended 8 quarter turns away from where it started; at 4 dB it moved 12 times, and at 5 dB not once. These counts are measurements of one simulated run each.

## Correctness

**Claim.** Without noise, line L4 outputs $e^{jM\theta_k}$ for every M-PSK symbol, so the loop locks $\psi$ to $M\theta$ and the estimate $\psi/M$ to $\theta$ modulo $2\pi/M$, with the steady-state behavior of the PLL. In the linear model, the variance of the estimate is $\frac{B_L T}{M^2}\sum_{n=1}^{M} \binom{M}{n}^2 n!\, N_0^n$. For $M = 2$ the loop gives the same phase as the BPSK Costas loop.

**Key steps.** The power maps every symbol to $e^{jM\phi_c}$. The noise after the power is a sum of terms $\binom{M}{n} (a e^{j\theta})^{M-n} w^n$, which are uncorrelated, with $E|w|^{2n} = n!\, N_0^n$ for circular Gaussian $w$; the PLL turns a white detector noise of variance $\sigma^2$ into a phase variance $2B_L T\,\sigma^2$, and the division by $M$ divides the variance by $M^2$. For $M = 2$, $\operatorname{Im}(z^2) = 2IQ$, the Costas detector. The full proof is in the proofs file.

The variance formula is a closed form under assumptions: the linear model, white Gaussian noise, a constant amplitude and correct symbol timing. The cycle slip counts are measurements.

## Complexity

Line L4 costs $O(\log M)$ complex multiplications by repeated squaring, or one table lookup on the phase if the amplitude is not needed, and lines L5 to L7 cost $O(1)$. So $N$ symbols cost $O(N \log M)$ in the [real RAM](/real-ram/), with $O(1)$ extra space. For BPSK and QPSK this is one or two complex squarings per symbol.

## Properties

- **Non-data-aided.** The loop needs no decisions and no known symbols, so it acquires before the receiver can make reliable decisions.
- **Squaring loss.** The variance is $L$ times that of a loop that knows the data. At 10 dB, $L = 1.05$ for BPSK and $1.51$ for QPSK; at 6 dB it is $1.13$ and $2.53$. It grows fast with $M$ and $N_0$, which limits the method to small $M$ or high SNR.
- **Ambiguity of $2\pi/M$.** The estimate is correct only modulo $2\pi/M$, and the loop picks the lock point nearest its start.
- **Smaller pull range.** The tone $y$ has $M$ times the frequency offset of the carrier. A frequency offset $\omega$ appears to the PLL as $M\omega$, so the loop must be wider, or the offset smaller, than for an unmodulated carrier.
- **Equivalence with Costas for BPSK.** With the same gains, the squaring loop and the Costas loop give the same phase for BPSK. Their hardware differs: the squaring loop works at $2f_c$ and divides by 2.

## Variants and improvements

- **Amplitude nonlinearity.** Replace $r^M$ by $F(|r|)\, e^{jM\arg r}$, as in the [Viterbi and Viterbi estimator](/viterbi-viterbi-phase-estimation/). A smaller weight on the amplitude, for example $F(\rho) = \rho^2$ or $1$ for QPSK, reduces the noise times noise terms and lowers the squaring loss at moderate SNR.
- **Feedforward form.** Average $y_k$ over a block of $N$ symbols and take $\frac1M \arg$. This is the Viterbi and Viterbi estimator; it needs no acquisition and has no hang-up.
- **Costas form.** For BPSK, the [Costas loop](/costas-loop/) computes the same detector as $IQ$ at the carrier frequency, without a squarer and a divider.
- **Decision-directed tracking.** After the squaring loop has locked, a [decision-directed loop](/decision-directed-carrier-recovery/) can take over. It has no squaring loss when the decisions are correct.
- **QAM.** For square QAM, the fourth power does not remove the data, but $E[a^4]$ is a negative real number for square QAM, so the fourth power of QAM samples still has a tone at $4\theta$ in the mean. The self noise from the data is large, and the method works only with long averages.

## When to use it

Use the squaring loop for continuous BPSK or QPSK when no pilot is present and the SNR is moderate to high, especially in analog or mixed hardware where a squarer and a divider are simple. For 8-PSK and above, the squaring loss is high, and a decision-directed loop is better once lock is reached. For bursts, use the feedforward Viterbi and Viterbi estimator.

## Pitfalls

- **Forgetting the constellation phase.** For QPSK with $\phi_c = \pi/4$, $r^4$ points to $4\theta + \pi$. Without the factor of line L4, the estimate is off by $\pi/4$, a quarter of the ambiguity period, which is the worst place for decisions.
- **Dividing the gains by M.** The gains of lines L6 and L7 act on $\psi$, not on the carrier phase. The noise bandwidth $B_L T$ of the loop on $\psi$ is also the noise bandwidth of the estimate $\psi/M$; do not scale it by $M$.
- **Using the formula at low SNR.** The variance formula holds only in the linear model. In the example at 3 dB, slips made the error drift by many quarter turns, and the measured variance was hundreds of times the formula.
- **Large frequency offsets.** The power multiplies the frequency offset by $M$. A QPSK signal with an offset of 0.05 cycles per symbol gives a tone at 0.2 cycles per symbol, too fast for a narrow loop.
- **Unresolved ambiguity.** As with every non-data-aided method, the receiver must resolve the $2\pi/M$ ambiguity with a preamble, a unique word or differential encoding.

## Implementations

## History

Squaring loops appeared with suppressed-carrier transmission in the 1950s and 1960s, as an alternative to the Costas loop of 1956. Both regenerate a carrier from a double-sideband suppressed-carrier signal, and the analyses of the time treated them as equivalent. William Lindsey and Marvin Simon, in their book Telecommunication Systems Engineering (1973) and in papers on suppressed-carrier tracking, expressed the extra phase noise of these loops against a loop with a carrier by one factor, the squaring loss. The Mth-power loop for M-PSK followed with the use of QPSK and 8-PSK on satellite links. In 1983, A. J. Viterbi and A. M. Viterbi turned the same power law into a feedforward block estimator with a nonlinearity on the amplitude.

## References
