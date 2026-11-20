---
tag: EVQ8KF
kind: algorithm
slug: decision-directed-carrier-recovery
name: Decision-directed carrier recovery
aliases:
- decision-directed phase tracking
area: communications/synchronization
level: core
summary: "Rotates each sample by the phase estimate, decides the nearest symbol and uses Im(z conj(a_hat)) as the phase error of a tracking loop. With correct decisions it has no squaring loss."
solves: [carrier-recovery]
model: real-ram
complexity:
  vars: {N: the number of symbols, M: the number of constellation points}
  time: {worst: O(N)}
  time_brute_force_decisions: {worst: O(N M)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, decision_directed: true, phase_ambiguity: "pi/2 for square QAM and QPSK"}
history:
  year: 1973
  people: [William C. Lindsey, Marvin K. Simon]
  note: "Decision-directed, or data-aided, carrier loops were analyzed next to the squaring and Costas loops in the early 1970s, among others by Lindsey and Simon. With QAM modems they became the usual way to track the carrier after acquisition."
prereqs: [phase-locked-loop, minimum-distance-detector, quadrature-amplitude-modulation]
see_also: [costas-loop, squaring-loop, viterbi-viterbi-phase-estimation, data-aided-synchronization, cycle-slip, per-survivor-processing, pilot-symbol-assisted-modulation, symbol-error-rate]
sources:
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Section 5.2 (clock-aided and data-aided phase recovery) and Section 5.3 (decision-directed phase recovery with non-offset modulation)"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 5.2-4 (decision-directed loops)"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Chapter 5 (synthesis of synchronization algorithms, the decision-directed approach) and Chapter 6 (performance analysis of synchronizers)"
---

Decision-directed (DD) carrier recovery tracks the carrier phase with the receiver's own symbol decisions. It rotates each sample $r_k$ by the current estimate, decides the nearest constellation point $\hat a_k$, and feeds the phase error $\operatorname{Im}(z_k \overline{\hat a_k})$ to the loop filter and the oscillator of a [phase-locked loop](/phase-locked-loop/). When the decisions are right, the detector output is $|a_k|^2 \sin\Delta$ plus noise, as if the data were known, so the loop has no squaring loss and works for any constellation, including QAM. This is the decision-directed member of the [carrier recovery](/carrier-recovery/) family, in the split described in [data-aided synchronization](/data-aided-synchronization/). The [Costas loop](/costas-loop/) and the [squaring loop](/squaring-loop/) remove the data without decisions, and the [Viterbi and Viterbi estimator](/viterbi-viterbi-phase-estimation/) does it in a block. For QPSK, the hard-limited Costas detector is $\sqrt2$ times the DD detector. The DD loop needs a phase error small enough for correct decisions, so it is usually started by a pilot, a preamble or one of those methods, and it shares their ambiguity: it locks modulo the rotation symmetry of the constellation, $\pi/2$ for QPSK and square QAM, and wrong decisions in noise can trigger a [cycle slip](/cycle-slip/).

## In plain words

The receiver must keep its picture of the constellation lined up with the received points. For each received point it asks: which symbol was this most likely? It then measures the angle between the received point and that symbol. If the points are turned a little to the left of the symbols they were decided as, the receiver turns its picture a little to the left, and the other way round. While the picture is close to right, almost all guesses are right, and the method works as well as if the receiver knew the data. If the picture is turned too far, the guesses go wrong, the measured angles point the wrong way, and the method can stick at a wrong angle.

## The problem

The input is $r_k = a_k e^{j\theta_k} + w_k$, $k = 0, \ldots, N - 1$, one sample per symbol after matched filtering and correct timing, with data $a_k$ uniform on a [signal constellation](/signal-constellation/) $\mathcal{A}$ of $M$ points normalized to $E_s = E|a|^2 = 1$, and $w_k \sim \mathcal{CN}(0, N_0)$ white, $\mathrm{SNR} = E_s/N_0$. The phase $\theta_k$ changes slowly. The loop must output an estimate $\phi_k$ from $r_0, \ldots, r_{k-1}$ and the decisions on them. If the symbols are known (a preamble or pilots), the same loop uses them in place of the decisions; that is the data-aided form.

## The algorithm

```pseudo id=main
DD-LOOP(r[0..N-1], A, Kp, Ki, known, phi0)
L1  phi <- phi0; s <- 0
L2  for k <- 0 to N - 1 do
L3      est[k] <- phi
L4      z <- r[k] * exp(-j * phi)                      ▷ derotate
L5      a_hat <- known[k] if known, else the point of A nearest to z
L6      e <- Im(z * conj(a_hat))                        ▷ |a|^2 sin(theta - phi) + noise
L7      s <- s + Ki * e
L8      phi <- phi + Kp * e + s
L9  return est, decisions
```

Line L5 is the [minimum distance detector](/minimum-distance-detector/), a slicer in $O(1)$ for PSK and square QAM. Line L6 is the cross product of the sample and the decision. Its mean slope at $\Delta = 0$ is $E|a|^2 = 1$, so the gains come from the PLL design rule with detector gain 1. Some designs divide $e$ by $|\hat a|^2$, which gives $\sin\Delta$ for every symbol and a noise that is larger on the inner points. Lines L7 and L8 are the second-order loop filter and the oscillator.

## Example

Take 16-QAM (raw levels $\pm1, \pm3$, divided by $\sqrt{10}$), $\theta = 0.25$ rad ($14.3^\circ$), no noise, random data (seed 1), and the gains for $B_L T = 0.02$: $K_p = 0.053333$, $K_i = 0.0014222$. The columns $a_k$, $z$ and $\hat a_k$ are in raw units (times $\sqrt{10}$); $e$ and $\phi$ are for the unit-energy points:

| $k$ | $a_k$ | $z$ (line L4) | $\hat a_k$ | $e$ (line L6) | new $\phi$ (line L8) |
|---|---|---|---|---|---|
| 0 | $1 + 3j$ | $0.227 + 3.154j$ | $1 + 3j$ | $0.247404$ | $0.013547$ |
| 1 | $3 - 3j$ | $3.619 - 2.214j$ | $3 - 3j$ | $0.421661$ | $0.036987$ |
| 2 | $-3 + 3j$ | $-3.566 + 2.298j$ | $-3 + 3j$ | $0.380531$ | $0.058775$ |
| 3 | $3 - j$ | $3.135 - 0.412j$ | $3 - j$ | $0.190062$ | $0.070674$ |

The corner point at $k = 1$ has $|a|^2 = 1.8$, so it gives a larger error signal than the point at $k = 0$, with $|a|^2 = 1$. The error $0.25 - \phi_k$ is $0.1289$ at $k = 10$, $-0.0585$ at $50$, $0.00176$ at $200$ and $-8 \times 10^{-5}$ at $300$.

The starting error matters. For 16-QAM, every noise-free decision is right only while $|\Delta| < \arccos\bigl(\frac{2}{3\sqrt2}\bigr) - 45^\circ = 16.87^\circ$, where the corner points reach a decision boundary. Started at $\theta = 0.7$ rad ($40^\circ$), the loop does not reach $0.7$. It settles near a false lock point, with an error that swings between $0.417$ and $0.564$ rad around a mean of $0.487$ rad ($27.9^\circ$), and 75 percent of the decisions are wrong. The data-aided form on the same samples, with the known symbols, locks to $0.7$, and from $2.5$ rad as well. QPSK has no false lock: its S-curve is $\sin\Delta$ on all of $(-45^\circ, 45^\circ)$, and the loop locks from $0.7$ rad.

In noise, with $B_L T = 0.01$ (exact $0.010181$), the linear model gives the variance $B_L T/\mathrm{SNR}$. Simulations of 30000 symbols measured these ratios to it (measurements):

| case | symbol error rate | DD ratio | data-aided ratio |
|---|---|---|---|
| QPSK, 10 dB, seed 3 | $0.0019$ | $0.97$ | $0.95$ |
| 16-QAM, 20 dB, seed 4 | $0$ | $1.03$ | $1.03$ |
| 16-QAM, 15 dB, seed 5 | $0.0196$ | $1.27$ | $1.03$ |

At 15 dB, about 2 percent of the 16-QAM decisions are wrong, close to the exact value $0.017782$, and they raise the variance by about a quarter over the data-aided loop.

## Correctness

**Claim.** If the decisions are correct, line L6 outputs $|a_k|^2 \sin\Delta$ plus white noise of variance $|a_k|^2 N_0/2$. So the loop behaves like a PLL with detector gain $E|a|^2 = 1$, and in the linear model its phase error variance is $B_L T/\mathrm{SNR}$. Without noise, the decisions are correct for $|\Delta| < 45^\circ$ for QPSK and $|\Delta| < 16.874^\circ$ for 16-QAM, and the S-curve is $\sin\Delta$ there.

**Key steps.** With $\hat a = a$, $z\bar a = |a|^2 e^{j\Delta} + n\bar a$, where $n$ is the rotated noise, still circular Gaussian. The decision is correct as long as the rotated point stays in its own decision region. For 16-QAM the corner point $3 + 3j$ reaches the line $x = 2$ first, at $\arccos(2/(3\sqrt2)) - 45^\circ$. Beyond this angle the S-curve is a broken function of $\Delta$, and the full proof locates its sign changes and the false lock between $25^\circ$ and $30^\circ$. The variance claim is a closed form under assumptions (the linear model, correct decisions); the effect of wrong decisions and the false lock are measurements here.

## Complexity

Each symbol costs one rotation, one decision and $O(1)$ arithmetic. With a slicer, the decision is $O(1)$, so $N$ symbols cost $O(N)$ in the [real RAM](/real-ram/), with $O(1)$ extra space. The implementation decides by brute force over the $M$ points, $O(NM)$, so that it is easy to check against the shared brute-force ML detector; the tests do this on 64-QAM and 8-PSK as well.

## Properties

- **No squaring loss.** With correct decisions, the noise is that of the data-aided loop. This is the main advantage over the Costas and squaring loops, and it holds for any constellation.
- **Needs a good start.** The linear range ends where decisions go wrong: $45^\circ$ for QPSK, $16.87^\circ$ for 16-QAM, and less for larger QAM. Outside it, the loop can false-lock, as in the example.
- **Ambiguity.** The decided symbols are rotated with the constellation, so the loop locks modulo the symmetry of $\mathcal{A}$: $\pi$ for BPSK, $\pi/2$ for QPSK and square QAM, $2\pi/M$ for M-PSK. The data-aided form has no ambiguity.
- **Threshold.** As the symbol error rate grows, wrong decisions reduce the detector gain and add noise. In the example at 15 dB, 2 percent wrong 16-QAM decisions raised the variance by 27 percent; at lower SNR the loop slips.
- **Decision delay.** The decision must be ready before the loop update. If decisions come from a decoder, they arrive late, and the delay in the loop reduces its stability margin.

## Variants and improvements

- **Data-aided mode.** Use known symbols during a preamble or on pilot symbols, as in [pilot-symbol-assisted modulation](/pilot-symbol-assisted-modulation/), then switch to decisions. This avoids false lock and the ambiguity.
- **Normalized detector.** $e = \operatorname{Im}(z \overline{\hat a})/|\hat a|^2 = \operatorname{Im}(z/\hat a)$ gives the same restoring force on every point.
- **Reduced constellation.** For large QAM, use only the corner points or the points of largest modulus during acquisition, because they give the largest and most reliable phase information; switch to all points after lock.
- **Feedforward DD.** Estimate the phase over a block by $\arg \sum_k z_k \overline{\hat a_k}$ and iterate. This is the decision-directed form of the block ML estimator.
- **Per-survivor processing.** In a Viterbi receiver, each survivor path keeps its own phase estimate, updated with its own tentative decisions; see [per-survivor processing](/per-survivor-processing/).

## When to use it

Use a DD loop to track the carrier of QAM or high-order PSK after acquisition, or in steady state on a continuous link, when the symbol error rate is low (below about 1 percent). Start it with a preamble, pilots, a [Viterbi and Viterbi](/viterbi-viterbi-phase-estimation/) estimate or a Costas loop. At low SNR, or when decisions are unreliable, use a non-data-aided method or pilots.

## Pitfalls

- **Acquiring with decisions.** Starting a 16-QAM DD loop at a phase error above about $17^\circ$ can end in a false lock with most decisions wrong, as in the example. Nothing in the loop shows it except a high error rate.
- **Forgetting the ambiguity.** After lock, the decisions may be rotated by a multiple of $\pi/2$. Use differential encoding of the quadrant bits or a known word.
- **Wrong scaling of the constellation.** Line L5 assumes that the received points have the scale of $\mathcal{A}$. If an automatic gain control leaves the samples 20 percent too large, outer QAM points are decided wrong even at zero phase error. Fix the gain first.
- **Using decisions from a different phase.** Line L5 must decide on the derotated $z$, not on $r$. Deciding on $r$ makes every decision depend on the raw carrier phase.
- **Ignoring decision errors in the noise budget.** The variance $B_L T/\mathrm{SNR}$ assumes correct decisions. At a symbol error rate of a few percent the measured variance is noticeably higher.

## Implementations

## History

Decision-directed ideas came with adaptive data modems in the 1960s, where the receiver's own decisions also drove adaptive equalizers. In the early 1970s, data-aided carrier loops were analyzed next to the squaring loop and the Costas loop, among others by Lindsey and Simon, and they were shown to avoid the squaring loss when decisions are reliable. With high-order QAM in telephone line modems, microwave radio and later cable and satellite systems, decision-directed tracking after a training or blind start became the common design. Mengali and D'Andrea's book of 1997 derives it as the decision-directed form of the maximum likelihood phase estimator.

## References
