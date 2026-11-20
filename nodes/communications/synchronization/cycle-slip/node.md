---
tag: 4GQF6S
kind: concept
slug: cycle-slip
name: Cycle slip
aliases:
- PLL cycle slip
area: communications/synchronization
level: advanced
summary: A jump of a tracking loop by a full period of its phase ambiguity under noise, which shifts all later decisions.
prereqs: [phase-locked-loop, carrier-recovery]
see_also: [costas-loop, squaring-loop, decision-directed-carrier-recovery, viterbi-viterbi-phase-estimation, differential-phase-shift-keying, data-aided-synchronization, pilot-symbol-assisted-modulation, symbol-timing-recovery]
sources:
  - paper: doi:10.1109/PROC.1963.2686
    title: "A. J. Viterbi, Phase-locked loop dynamics in the presence of noise by Fokker-Planck techniques, Proceedings of the IEEE 51(12), 1963, pages 1737 to 1753"
    locator: "the stationary density of the phase error of the first-order loop and the mean time to the first slip"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Section 6.4 (cycle slipping, pages 385 to 399: effect on symbol detection, slips in feedback and feedforward synchronizers)"
---

A cycle slip is a jump of a phase tracking loop from one stable lock point to the next, caused by noise. A [phase-locked loop](/phase-locked-loop/) on a pure carrier has lock points $2\pi$ apart. A loop that removes the data, such as the [Costas loop](/costas-loop/), the [squaring loop](/squaring-loop/) or [decision-directed carrier recovery](/decision-directed-carrier-recovery/), has lock points $2\pi/M$ apart for an $M$-fold symmetric constellation, so it can slip by $2\pi/M$. After a slip, the loop is again locked and its phase error is small, but the phase reference is rotated by a symmetry of the constellation, so all later decisions are rotated until something resolves the ambiguity again. Slips are the main failure of [carrier recovery](/carrier-recovery/) at low SNR. Feedforward estimators such as [Viterbi and Viterbi phase estimation](/viterbi-viterbi-phase-estimation/) slip too, when the unwrapping of successive block estimates picks the wrong multiple of $2\pi/M$.

## In plain words

A tracking loop keeps its guess of the carrier near one of several correct-looking positions. Noise pushes the guess back and forth. Most pushes are small, and the loop pulls the guess back. Now and then, many pushes in the same direction carry the guess over the hill between two positions, and the loop then settles at the next position. Nothing looks wrong after that: the loop is locked again. But the receiver now reads every symbol turned by one step, so all later data is wrong until a known pattern or a special code puts it right.

## The idea

**Where slips come from.** The S-curve of a phase detector is periodic, with stable zeros (lock points) and unstable zeros between them. For the PLL, the S-curve is $\sin\Delta$, stable at $0$ and unstable at $\pm\pi$. In the linear model the error is Gaussian and never leaves the lock point, but the true error is a nonlinear random process. Noise can carry it over an unstable point, and the loop then pulls it on to the next stable point. A slip is this passage, from one lock point to a neighbor.

**The first-order loop (theorem).** For the continuous-time first-order PLL with a sinusoidal detector in white Gaussian noise, Viterbi solved the Fokker-Planck equation of the phase error in 1963. The density of the error modulo $2\pi$ is the Tikhonov density
$$p(\Delta) = \frac{e^{\rho\cos\Delta}}{2\pi I_0(\rho)},$$
where $\rho$ is the loop SNR, the inverse of the linear-model variance, and $I_0$ is the modified Bessel function. The mean time to the first slip is
$$T_{\mathrm{slip}} = \frac{\pi^2\rho\,I_0(\rho)^2}{2B_L},$$
where $B_L$ is the one-sided noise bandwidth of the loop. For large $\rho$, $I_0(\rho) \approx e^{\rho}/\sqrt{2\pi\rho}$, and $T_{\mathrm{slip}} \approx \frac{\pi e^{2\rho}}{4B_L}$. The mean time grows exponentially with the loop SNR: each 1 dB of loop SNR at high $\rho$ multiplies it by a large factor.

**Other loops (rules and measurements).** For second-order loops, loops with an $M$-fold ambiguity, and sampled loops, exact results are rare, and the first-order formula is used as an approximation, with these rules:

- A loop with lock points $2\pi/M$ apart behaves, for slips, like a PLL with the error $M\Delta$, so the relevant loop SNR is about $\rho/M^2$. A QPSK loop slips at a far higher SNR than a BPSK loop of the same bandwidth.
- The squaring loss of non-data-aided loops lowers the effective $\rho$ further at low SNR.
- A narrower loop bandwidth raises $\rho = \mathrm{SNR}/(B_L T)$ and lowers the slip rate exponentially, but it tracks phase noise and frequency changes less well.
- A residual frequency offset makes the error sit off zero, closer to one unstable point, so slips become more frequent and go mainly in one direction.

**Effect on the data.** After a slip by $2\pi/M$, every symbol is decided rotated by $2\pi/M$. With absolute (coherent) encoding, all bits that depend on the rotation are wrong from the slip on, until a known word or a pilot detects it. [Differential encoding](/differential-phase-shift-keying/) turns this into a short burst of errors at the slip, at the price of about twice the symbol error rate. In coded systems, a slip inside a codeword can make the decoder fail for the whole block, so slip-resilient receivers use pilot symbols, rotation-invariant codes or per-block ambiguity resolution.

**Counting slips.** Counting every crossing of an unstable point counts too many, because the error can cross and come back. A practical counter uses hysteresis: it counts a slip only when the error has gone well past the unstable point, for example $3\pi/2$ away from the current lock point for a PLL, and then moves its reference to the new lock point.

## Examples

**A first-order sampled PLL (measurement).** The loop $\phi \leftarrow \phi + K \operatorname{Im}(r_k e^{-j\phi})$ on an unmodulated carrier has the noise bandwidth $B_L T = \frac{K}{2(2-K)}$ and the linear variance $B_L T/\mathrm{SNR} = 1/\rho$. Simulations of 150000 samples (seed 7), with the counter above, gave these mean numbers of samples between slips, against $\frac{\pi^2\rho I_0(\rho)^2}{2B_L T}$:

| $K$ | $\rho$ | slips | measured | formula |
|---|---|---|---|---|
| 0.05 | 1.5 | 89 | 1685 | 1566 |
| 0.05 | 2.0 | 33 | 4545 | 4000 |
| 0.10 | 2.0 | 58 | 2586 | 1949 |
| 0.02 | 1.5 | 37 | 4054 | 3974 |
| 0.05 | 3.0 | 5 | 30000 | 27508 |

The continuous-time formula fits the sampled loop well for small $K$, and less well for $K = 0.1$, where the sampling matters. From $\rho = 1.5$ to $\rho = 3$, the slip rate falls by a factor of about 18. The measured mean of $\cos\Delta$ was $0.613$ at $\rho = 1.5$, against the Tikhonov value $I_1(1.5)/I_0(1.5) = 0.596$.

**A QPSK squaring loop.** On the [squaring loop](/squaring-loop/) page, a fourth-power loop with $B_L T = 0.01$ ran over 40000 QPSK symbols (seed 5). At $E_s/N_0 = 3$ dB the error crossed between quarter-turn lock points 52 times with a net drift of $-8$ quarter turns; at 4 dB there were 12 crossings, and at 5 dB none (measurements). A change this steep over 2 dB is what the exponential growth of $T_{\mathrm{slip}}$ with the loop SNR leads one to expect.

**Feedforward unwrapping.** A Viterbi and Viterbi estimator on blocks of 32 QPSK symbols, followed by unwrapping, slips when two consecutive block estimates differ by more than $\pi/4$ because of noise. At 10 dB per symbol this is rare; at low SNR, or with long blocks and a fast phase drift, it becomes common.

## Where it is used

- **Receiver design.** The loop bandwidth of a carrier loop is chosen so that the mean time between slips is long compared with a frame, for example hours at the operating SNR, while it still tracks the phase noise of the oscillators.
- **Code and frame design.** Pilot symbols, unique words, differential encoding and rotation-invariant trellis codes are chosen to detect or tolerate slips. Deep space and satellite links count slips as a key measure.
- **Coherent optical receivers.** Carrier phase estimation of QPSK and QAM in optical links uses feedforward estimators with unwrapping, and cycle slips there cause long error bursts; differential coding or pilots are used against them.
- **GNSS.** In carrier-phase positioning, a slip of the carrier tracking loop changes the integer ambiguity of the phase measurement, and receivers detect and repair such slips.
- **Timing recovery.** A [symbol timing recovery](/symbol-timing-recovery/) loop can slip by one symbol period, which drops or repeats a symbol.

## References
