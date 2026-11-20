---
tag: VA0M3B
kind: algorithm
slug: viterbi-viterbi-phase-estimation
name: Viterbi and Viterbi phase estimation
aliases:
- Viterbi-Viterbi algorithm
- Mth-power phase estimator
area: communications/synchronization
level: core
summary: Estimates the carrier phase of M-PSK in feedforward form by raising samples to the Mth power and averaging over a block.
solves: [carrier-recovery]
model: real-ram
complexity:
  vars: {N: the number of symbols in the block}
  time: {worst: O(N)}
  space: {extra: O(1)}
properties: {deterministic: true, feedforward: true, non_data_aided: true, phase_ambiguity: "2 pi/M for M-PSK"}
history:
  year: 1983
  people: [Andrew J. Viterbi, Audrey M. Viterbi]
  note: "Andrew J. Viterbi and Audrey M. Viterbi published the estimator in 1983 for burst transmission, where a loop has no time to acquire. They used a general nonlinearity of the sample modulus times the Mth power of its phase."
prereqs: [phase-shift-keying, carrier-recovery, additive-white-gaussian-noise-channel]
see_also: [costas-loop, squaring-loop, decision-directed-carrier-recovery, modified-cramer-rao-bound, cycle-slip, data-aided-synchronization, differential-phase-shift-keying, phase-locked-loop]
sources:
  - paper: doi:10.1109/TIT.1983.1056713
    title: "A. J. Viterbi and A. M. Viterbi, Nonlinear estimation of PSK-modulated carrier phase with application to burst digital transmission, IEEE Transactions on Information Theory 29(4), 1983, pages 543 to 551"
    locator: "the feedforward estimator with the nonlinearity F(rho) e^(j M psi) of each sample, and its variance against the nonlinearity"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 5 (carrier phase recovery with linear modulations, the non-data-aided feedforward estimator for M-PSK)"
  - book: isbn:9780471502753
    title: "Heinrich Meyr, Marc Moeneclaey and Stefan A. Fechtel, Digital Communication Receivers, Wiley, 1998"
    locator: "Chapter 5 (feedforward carrier phase estimation for M-PSK, the Viterbi and Viterbi algorithm)"
---

Viterbi and Viterbi (VV) phase estimation finds the carrier phase of an M-PSK signal from one block of $N$ samples, with no feedback and no knowledge of the data. It writes each sample as $r_k = \rho_k e^{j\psi_k}$, removes the data by multiplying the angle by $M$, weights each sample by a power $\rho_k^p$ of its modulus, sums, and divides the angle of the sum by $M$. It is the block, or feedforward, member of the [carrier recovery](/carrier-recovery/) family. The [Costas loop](/costas-loop/) and the [squaring loop](/squaring-loop/) remove the data in the same way but in a feedback loop that runs symbol by symbol, and [decision-directed carrier recovery](/decision-directed-carrier-recovery/) uses decisions instead of a power. The estimate has an $M$-fold ambiguity, and at high SNR its variance approaches the [modified Cramer-Rao bound](/modified-cramer-rao-bound/) $1/(2N\,\mathrm{SNR})$. Because it needs no acquisition time, it suits burst transmission, and at low SNR the unwrapping of successive block estimates can fail, which is the block form of a [cycle slip](/cycle-slip/).

## In plain words

In QPSK each symbol turns the carrier by one of four angles. If you multiply every angle by four, the four data angles all fall on the same angle, and only four times the carrier phase is left. So the receiver takes each sample, multiplies its angle by four, adds all of them up as arrows, and reads the angle of the total. Dividing by four gives the carrier phase, but only up to a quarter turn, because a quarter turn of the carrier also looks the same after the multiplication. Long arrows count more than short ones, but not too much, because the strong samples are not always the reliable ones.

## The problem

The input is a block $r_k = a_k e^{j\theta} + w_k$, $k = 0, \ldots, N - 1$, one sample per symbol after matched filtering and correct timing. The data $a_k = e^{j(2\pi i_k/M + \varphi_0)}$ are unknown and uniform on M-PSK with a known offset $\varphi_0$ (for example $\varphi_0 = \pi/4$ for QPSK with points on the diagonals), and $w_k \sim \mathcal{CN}(0, N_0)$ is white, $\mathrm{SNR} = E_s/N_0 = 1/N_0$. The phase $\theta$ is constant over the block. Output an estimate $\hat\theta$ of $\theta$ modulo $2\pi/M$, in $[-\pi/M, \pi/M)$.

## The algorithm

```pseudo id=main
VV(r[0..N-1], M, p, phase0)
L1  S <- 0
L2  for k <- 0 to N - 1 do
L3      rho <- |r[k]|; psi <- arg r[k]
L4      S <- S + rho^p * exp(j * M * psi)          ▷ the data angle is removed
L5  theta <- (arg S - M * phase0) / M
L6  return theta reduced to [-pi/M, pi/M)
```

Line L4 is the nonlinearity $F(\rho) e^{jM\psi}$ with $F(\rho) = \rho^p$. With $p = M$ it is $r_k^M$, the plain Mth power, and the estimator is $\frac1M \arg \sum_k r_k^M$ up to the offset; with $p = 0$ only the angles are used. Line L5 removes the angle $M\varphi_0$ that the offset adds; for QPSK on the diagonals $M\varphi_0 = \pi$, and the estimate is $\frac14 \arg\bigl(-\sum_k r_k^4\bigr)$. For a long signal, the receiver runs VV on successive blocks, or on a sliding window, and unwraps: it moves each new estimate by a multiple of $2\pi/M$ to the value nearest to the previous one.

## Example

QPSK on the diagonals, $\theta = 0.3$ rad, $\mathrm{SNR} = 10$ dB, $N = 4$, $p = 2$ (random data and noise, seed 6):

| $k$ | $r_k$ | $\rho_k$ | $\psi_k$ | $\rho_k^2 e^{j4\psi_k}$ |
|---|---|---|---|---|
| 0 | $0.293 + 0.901j$ | $0.947$ | $1.2562$ | $0.276 - 0.854j$ |
| 1 | $0.648 + 1.120j$ | $1.294$ | $1.0464$ | $-0.842 - 1.447j$ |
| 2 | $-0.486 - 0.842j$ | $0.972$ | $-2.0947$ | $-0.474 - 0.818j$ |
| 3 | $1.000 - 0.809j$ | $1.287$ | $-0.6802$ | $-1.511 - 0.677j$ |

The sum is $S = -2.5510 - 3.7957j$, with $\arg S = -2.1625$. Line L5 gives $(-2.1625 - \pi)/4 = -1.3260$, and line L6 adds $\pi/2$ to reach $0.2448$ in $[-\pi/4, \pi/4)$. The error is $-0.055$ rad. The four sample angles differ by about $\pi/2$ multiples plus noise, but after multiplication by 4 the terms point in roughly the same direction.

With $N = 32$ and 600 random blocks per point (seed 4), the mean square error over the MCRB $1/(2N\,\mathrm{SNR})$ was (measurements):

| $E_s/N_0$ | $p = 0$ | $p = 1$ | $p = 2$ | $p = 4$ |
|---|---|---|---|---|
| 0 dB | $8.42$ | $7.51$ | $7.31$ | $7.63$ |
| 5 dB | $3.37$ | $2.65$ | $2.70$ | $3.97$ |
| 10 dB | $1.17$ | $1.13$ | $1.16$ | $1.42$ |

At 10 dB the error is close to the bound. At lower SNR the nonlinearity enhances the noise, and the powers $p = 1$ and $p = 2$ do better than the plain fourth power.

## Correctness

**Claim.** $\hat\theta$ maximizes $J(\phi) = \sum_k \rho_k^p \cos\bigl(M(\psi_k - \phi - \varphi_0)\bigr)$, and its maximizers are $\hat\theta + \frac{2\pi}{M}\mathbb{Z}$. Without noise $\hat\theta \equiv \theta$ modulo $2\pi/M$. In circular Gaussian noise, the error modulo $2\pi/M$ is symmetric about zero, so the estimator is unbiased. At high SNR its variance is $\frac{1}{2N\,\mathrm{SNR}}(1 + o(1))$, the MCRB.

**Key steps.** $M(2\pi i/M + \varphi_0) = 2\pi i + M\varphi_0$, so the data drops out of $e^{jM\psi}$. Then $J(\phi) = |S|\cos(\arg S - M(\phi + \varphi_0))$, which is largest where line L5 puts $\phi$. Complex conjugation maps M-PSK and circular noise onto themselves, which gives the symmetry. A first-order expansion of the angle in the noise gives $\hat\theta - \theta \approx \frac1N \sum_k y_k$ with $y_k \sim \mathcal{N}(0, N_0/2)$. The first three claims are theorems; the high-SNR variance is a closed form under assumptions, and the table above is a measurement.

## Complexity

Each sample costs one modulus, one angle, one power and one complex exponential, so the block costs $O(N)$ time in the [real RAM](/real-ram/), with $O(1)$ extra space. For $p = M$, $r_k^M$ needs only $\log_2 M$ complex squarings and no trigonometric function. A sliding window of length $N$ updates $S$ in $O(1)$ per sample by adding the new term and subtracting the old one.

## Properties

- **Feedforward.** There is no loop, so there is no acquisition time and no hang-up. Every block gives an estimate of the same quality.
- **Non-data-aided.** The data need not be known or decided. The estimator works at SNRs where decisions are poor.
- **Ambiguity $2\pi/M$.** The estimate is modulo $2\pi/M$: $\pi$ for BPSK, $\pi/2$ for QPSK. A known word or differential encoding must resolve it.
- **Self noise and noise enhancement.** At low SNR, the power multiplies the noise: terms of the type noise times noise appear in $S$. The variance is then several times the MCRB, as the table shows.
- **Choice of $p$.** Viterbi and Viterbi studied the nonlinearity $F(\rho)$; low powers ($p = 1$ or $2$) are a good choice for QPSK at moderate SNR, and $p = M$ is the low-SNR maximum likelihood form.
- **Only for constant phase.** The block length is a tradeoff: longer blocks lower the noise, but the phase must stay constant over the block, and a residual frequency offset $\nu$ adds a phase change $2\pi\nu N$ over it.

## Variants and improvements

- **Sliding window with unwrapping.** A running sum of the last $N$ terms gives an estimate per symbol, and unwrapping follows a phase that moves beyond $\pm\pi/M$.
- **Plain Mth power.** $p = M$: $\hat\theta = \frac1M \arg \sum_k r_k^M$, the low-SNR approximation of the non-data-aided ML estimator for M-PSK.
- **QAM.** For square QAM, the fourth power still keeps a nonzero mean, $E a^4 \neq 0$, so $\frac14 \arg(-\sum r_k^4)$ works, with much more self noise. Selecting only the corner points or the points of a given ring reduces it.
- **Decision-directed refinement.** Use the VV estimate to start a [decision-directed loop](/decision-directed-carrier-recovery/), or recompute the block estimate with decisions.
- **Joint frequency and phase.** With a residual frequency offset, apply a frequency estimator to $r_k^M$ first, for example the [Kay estimator](/kay-frequency-estimator/), then VV on the derotated block.

## When to use it

Use VV for M-PSK in burst mode, in satellite modems, or after a coarse frequency correction in coherent optical receivers, where a block estimate is wanted at once and the SNR is moderate. For QPSK at a few dB SNR, choose $p = 1$ or $2$. For QAM, or at high SNR with a continuous signal, a decision-directed loop is simpler and has no self noise.

## Pitfalls

- **Forgetting the offset.** For QPSK on the diagonals, $\arg \sum r^4$ is off by $\pi$ before the division. Omitting $M\varphi_0$ shifts every estimate by $\pi/4$.
- **Not unwrapping.** Block estimates are in $[-\pi/M, \pi/M)$. A phase that drifts past $\pi/M$ jumps by $2\pi/M$ unless the blocks are unwrapped.
- **Wrong unwrapping at low SNR.** If two consecutive estimates differ by more than $\pi/M$ because of noise, the unwrapping adds a wrong multiple of $2\pi/M$, and all later symbols are rotated. This is a cycle slip of the block estimator.
- **Too long a block with a frequency offset.** The term $e^{jM 2\pi\nu k}$ turns inside the sum. If $M\nu N$ is not small, the sum cancels and the estimate is meaningless.
- **Using $p = M$ at low SNR.** The plain Mth power enhances the noise most. At 5 dB for QPSK it had about 50 percent more error than $p = 2$ in the table.

## Implementations

## History

Andrew J. Viterbi and Audrey M. Viterbi published the estimator in the IEEE Transactions on Information Theory in 1983. They designed it for burst digital transmission, such as time-division multiple access satellite links, where a carrier loop has no time to acquire at the start of each burst. Their paper considered a general nonlinearity of the modulus and computed the variance for several choices. The Mth power idea itself is older: the squaring and Mth power loops of the 1960s and 1970s used it in feedback form. The VV estimator later became the standard feedforward phase recovery for QPSK in digital coherent optical receivers.

## References
