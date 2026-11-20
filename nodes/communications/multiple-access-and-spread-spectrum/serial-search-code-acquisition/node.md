---
tag: 3AJ158
kind: algorithm
slug: serial-search-code-acquisition
name: Serial search code acquisition
aliases:
- serial search acquisition
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "Finds the code phase of a spread-spectrum signal by testing candidate phases one at a time: correlate, compare with a threshold, verify a crossing. It gives the coarse alignment before tracking."
solves: [signal-detection]
model: real-ram
complexity:
  vars: {q: the number of cells, N: the number of chips per dwell, K: the penalty of a false alarm in dwells, p: the detection probability per dwell, a: the false alarm probability per dwell}
  time: {per_dwell: Θ(N), expected: "Θ(N q (1 + K a) / p)"}
  space: {extra: Θ(1)}
properties: {deterministic: true, one_correlator: true, needs_verification: true, worst_case_unbounded: true}
history:
  year: 1984
  people: [Andreas Polydoros, Charles L. Weber]
  note: Serial search is the simplest acquisition method for spread-spectrum receivers. Holmes and Chen analyzed its acquisition time in 1977, and Polydoros and Weber gave a unified theory in 1984.
prereqs: [direct-sequence-spread-spectrum, maximal-length-sequence, autocorrelation, neyman-pearson-lemma]
see_also: [parallel-code-phase-search, delay-locked-loop, markov-chain, gaussian-q-function, preamble-correlation-detection, frame-synchronization, processing-gain, early-late-gate-synchronizer]
sources:
  - paper: doi:10.1109/TCOM.1984.1096109
    title: A. Polydoros and C. L. Weber, A unified approach to serial search spread-spectrum code acquisition, Part I, General theory, IEEE Transactions on Communications 32(5), 1984
    locator: pp. 542 to 549 (the general theory of serial search acquisition)
  - paper: doi:10.1109/TCOM.1977.1093913
    title: J. K. Holmes and C. C. Chen, Acquisition time performance of PN spread-spectrum systems, IEEE Transactions on Communications, 1977
    locator: The analysis of the acquisition time of a serial search
  - book: isbn:9780817643904
    title: Kai Borre, Dennis M. Akos, Nicolaj Bertelsen, Peter Rinder and Søren Holdt Jensen, A Software-Defined GPS and Galileo Receiver, Birkhäuser, 2007
    locator: Section 6.2, p. 76 (serial search acquisition over 41 frequency bins and 1023 code phases)
---

A direct-sequence receiver cannot despread a signal until it knows where the code starts. Serial search code acquisition finds this **code phase** by brute force, one candidate at a time. The receiver has $q$ **cells**, the candidate phases (and, in GPS, also candidate frequencies). It correlates the received chips with the local code at one cell, compares the energy with a threshold, and moves to the next cell if the energy is below it. A crossing is checked by a longer verification step, since noise alone can cross the threshold. When a crossing passes the check, the phase is known to within a fraction of a chip, and a [delay-locked loop](/delay-locked-loop/) takes over to track it. The method needs only one correlator, but its time grows with the number of cells. [Parallel code phase search](/parallel-code-phase-search/) tests all phases at once with FFTs.

## In plain words

Picture a long pattern of beeps arriving from a transmitter, and you have a copy of the pattern. You do not know where in the pattern the transmitter is, so you cannot line up your copy.

So you try one alignment and listen for a short time. If your copy matches, you hear a strong echo of agreement. If it does not, you hear only a little.

If the agreement is weak, you slide your copy by one step and try again. If it is strong, you listen longer to be sure, because noise sometimes sounds like agreement. A false alarm costs time. A miss costs more, because you must go around all the other alignments before you come back to the right one.

You stop at the first alignment that passes the longer test.

## The problem

The received chips in one dwell are $r[n] = \sqrt{E_s}\, c[(n - \tau) \bmod N] + w[n]$ for $n = 0, \ldots, N - 1$, with a known code $c$ of unit energy, an unknown phase $\tau$ and noise $w[n] \sim \mathcal{CN}(0, N_0)$. The task is to find $\tau$ among $q$ cells with a short mean time. Each dwell uses a new block of chips. This is a [signal detection](/signal-detection/) problem repeated over the cells: at each cell the receiver decides between "signal at this phase" and "noise only".

## The algorithm

```pseudo id=main
SERIAL-SEARCH(dwell, q, γ, verify, K, start)
L1  k ← start mod q
L2  while the time budget is not used up do
L3      z ← dwell(k)                     ▷ correlate a new block with the code at phase k
L4      if |z|² > γ then                 ▷ threshold test on the energy
L5          if verify(k) then return k   ▷ a rejected crossing costs K dwells
L6      k ← (k + 1) mod q
```

The dwell computes $z = \sum_n \overline{c[(n - k) \bmod N]}\, r[n]$. By the [autocorrelation](/autocorrelation/) of the code, $z$ is $\mathcal{CN}(\sqrt{E_s}\, R(\tau - k), N_0)$. For an [m-sequence](/maximal-length-sequence/) with unit energy, $R(0) = 1$ and $R(s) = -1/N$ elsewhere, so the right cell gives a large mean and the others a small one. The energy test is noncoherent, since the carrier phase is unknown. With $z \sim \mathcal{CN}(\mu, N_0)$,
$$P(|z|^2 > \gamma) = Q_1\big(\sqrt{2|\mu|^2/N_0},\ \sqrt{2\gamma/N_0}\big),$$
where $Q_1$ is the Marcum Q function. This gives the detection probability $P_d$ at the right cell and the false alarm probability $P_{fa}$ at the wrong cells. With no signal, $P_{fa} = e^{-\gamma/N_0}$, so $\gamma = N_0 \ln(1/P_{fa})$ sets the false alarm rate.

With perfect verification, a uniformly random start, and time counted in dwells, the mean acquisition time is
$$E[T] = \frac{2 + (2 - P_d)(q - 1)(1 + K P_{fa})}{2 P_d}.$$

## Example

**A small trace.** Take the m-sequence $1001011$ ($N = q = 7$), $E_s = 1$, no noise, the true phase $\tau = 4$, the start $0$ and $\gamma = 0.5$. The dwells at cells $0, 1, 2, 3$ give $|z|^2 = 1/49 = 0.0204$, below the threshold. The dwell at cell $4$ gives $|z|^2 = 1$, the verification accepts it, and the search returns $4$ after $5$ dwells.

**Mean time.** For the 1023 code phases of the GPS C/A code with $P_d = 0.9$, $P_{fa} = 0.01$ and $K = 10$, $E[T] = 688.1$ dwells, or $0.688$ s with 1 ms dwells. A perfect detector would need $(q + 1)/2 = 512$ dwells.

**From the signal level.** A 1 ms dwell on a signal at $C/N_0 = 45$ dB-Hz gives $E_s/N_0 = 10^{4.5} \cdot 10^{-3} = 31.62$ (15 dB). The threshold $\gamma = N_0 \ln 100$ gives $P_{fa} = 0.0100$.

| $C/N_0$ (dB-Hz) | $E_s/N_0$ | $P_d$ | $E[T]$, 1023 cells | $E[T]$, 41943 cells |
|---|---|---|---|---|
| 45 | 31.62 | 0.99999974 | 563.1 dwells | 23.07 s |
| 40 | 10.00 | 0.9423 | 632.1 dwells | 25.90 s |
| 38 | 6.31 | 0.7493 | 939.7 dwells | 38.51 s |
| 35 | 3.16 | 0.3688 | 2489.1 dwells | 102.04 s |

The last column uses $K = 10$ and the search grid of Borre and coauthors: 41 Doppler bins of 500 Hz times 1023 code phases, 41943 cells, with 1 ms dwells. A weak signal costs time in two ways: it is missed more often, and each miss costs a full pass over the other cells.

## Correctness

The search returns only from L5, so with a perfect verification it returns only the true cell. Each visit to the true cell is a new dwell that crosses the threshold with probability $P_d$, and L6 visits the true cell once in every $q$ dwells, so the search stops with probability 1 if $P_d > 0$. For the mean time, let $M$ be the number of misses at the true cell, a geometric variable with mean $(1 - P_d)/P_d$. A start at position $j$ before the true cell costs $j - 1$ wrong dwells, and each miss costs one more dwell at the true cell and $q - 1$ wrong dwells. A wrong dwell costs $1 + K P_{fa}$ on average, and its false alarms are independent of $M$. Averaging over a uniform $j$ gives the formula. The full proof, with the Marcum Q series, is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/) model, each dwell costs $\Theta(N)$ multiply-adds (L3). The expected number of dwells is $E[T]$, which is $\Theta(q (1 + K P_{fa}) / P_d)$, so the expected cost is $\Theta(N q (1 + K P_{fa}) / P_d)$, with $\Theta(1)$ extra space. There is no worst-case bound, because noise can cause misses at the true cell any number of times; a real receiver stops after a time budget (L2).

## Properties

- **One correlator.** The hardware is one correlator and one comparator, the reason serial search was used in early receivers.
- **Linear in the number of cells.** The mean time grows with $q$. Doubling the cells to 2046 half-chip cells raises the mean time at 45 dB-Hz from 563.1 to 1125.8 dwells.
- **Misses are expensive.** A miss costs about $q (1 + K P_{fa})$ dwells, a false alarm costs $K$. So the threshold is usually set low enough to keep $P_d$ high.
- **False alarm penalty.** At 45 dB-Hz, $K = 0$ gives 512.0 dwells and $K = 100$ gives 1023.1 dwells, with the same $P_{fa} = 0.01$.
- **Independent dwells.** The formula assumes a new block for each dwell. Reusing the same block in all cells makes the outcomes dependent.

## Variants and improvements

- **Multiple dwell.** Use a short first dwell and a longer second dwell only on crossings. The verification in L5 is a simple form of this.
- **Search strategies.** Start at the most likely cell and expand to both sides (a Z search or expanding window), when prior information gives a likely phase.
- **Several correlators.** Test several adjacent cells per dwell to divide the time by the number of correlators.
- **Matched filter acquisition.** A matched filter tests one new phase per chip. Polydoros and Weber treat it in Part II of their paper.
- **FFT search.** [Parallel code phase search](/parallel-code-phase-search/) computes all $N$ correlations of one block in $O(N \log N)$ operations.
- **Sequential tests.** Let the dwell time depend on the data, stopping early at cells where the energy is clearly low.

## When to use it

Use serial search when the hardware can afford only one correlator, or when the number of cells is small. When a processor with an FFT is available, as in software GNSS receivers, the parallel search over all code phases is faster per block. Serial search also works for long codes whose period is too large for one FFT, where the receiver searches a window of phases around a prior estimate.

## Pitfalls

- **Cell spacing.** The autocorrelation of a rectangular chip is a triangle of width two chips. With cells one chip apart, the true phase can be half a chip from the nearest cell, and the amplitude drops to $1/2$, a loss of 6.02 dB. With half-chip cells the worst loss is 2.50 dB.
- **Frequency offset.** A residual carrier offset rotates the chips during the dwell and lowers the peak. Long dwells need fine frequency bins.
- **Data bit changes.** A data bit transition inside a dwell can cancel part of the correlation.
- **Wrong noise level.** The threshold $\gamma = N_0 \ln(1/P_{fa})$ needs the noise level. An error in $N_0$ changes $P_{fa}$ exponentially, so receivers estimate it from cells with no signal.
- **Formula without verification.** The formula assumes a verification that never accepts a wrong cell. If it can, the search can lock on a wrong phase, and the tracking loop must detect this and restart the search.

## Implementations

## History

Serial search is the simplest acquisition method for spread-spectrum receivers, because it needs only one correlator. J. K. Holmes and C. C. Chen analyzed its acquisition time in 1977. In 1984 Andreas Polydoros and Charles Weber gave a unified theory of serial search acquisition in two parts, the second for receivers with a matched filter. With fast processors, FFT-based searches replaced serial search in many software GNSS receivers.

## References
