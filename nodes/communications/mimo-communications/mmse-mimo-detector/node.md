---
tag: ZA2PHJ
kind: algorithm
slug: mmse-mimo-detector
name: MMSE MIMO detector
aliases:
- LMMSE detector
- linear MMSE MIMO receiver
area: communications/mimo-communications
level: core
summary: "Applies the linear filter (H^H H + (N0/Es) I)^-1 H^H, which minimizes the mean squared error of the symbol estimates, then removes its bias and slices each stream to the nearest symbol."
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {n: the number of transmitted streams, m: the number of receive antennas, M: the constellation size}
  time: {worst: O(n^2 m + n^3 + n M)}
  time_per_vector_after_setup: {worst: O(n m + n M)}
  space: {extra: O(n m)}
properties: {deterministic: true, linear: true, exact_ml: false, needs_noise_level: true, maximizes_sinr_among_linear_filters: true, works_when_n_exceeds_m: true}
history:
  year: 1984
  people: [Jack H. Winters]
  note: "Winters's optimum combining of 1984 weighted the antennas of a receiver to maximize the SINR against cochannel interference, which is the MMSE filter. It became a standard MIMO detector with the spatial multiplexing systems of the late 1990s."
prereqs: [mimo-detection, zero-forcing-mimo-detector, wiener-filter]
see_also: [v-blast, mmse-linear-equalizer, mmse-multiuser-detector, regularized-zero-forcing-precoding, expectation-propagation-detection, soft-interference-cancellation-equalizer, mimo-capacity, spatial-multiplexing]
sources:
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: "Section 8.3.3, Linear MMSE receiver (the SINR-maximizing filter and its MMSE form), and Section 8.3.4, Information theoretic optimality (MMSE-SIC achieves the capacity)"
  - book: isbn:9780521826150
    title: Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003
    locator: Chapter 7, Space-time receivers (the MMSE receiver and its comparison with ZF and ML)
  - paper: doi:10.1109/MSP.2009.932126
    title: Erik G. Larsson, MIMO detection methods - how they work, IEEE Signal Processing Magazine 26(3), 91-95, 2009
    locator: the section on linear receivers (the MMSE filter as a regularized ZF)
  - paper: "Ahmed Hesham Mehana and Aria Nosratinia, Diversity of MMSE MIMO receivers, IEEE Transactions on Information Theory 58(11), 6788-6805, 2012"
    locator: the main results (the diversity of the MMSE receiver depends on the rate, from the ML value at low rates to the ZF value at high rates)
---

The minimum mean square error (MMSE) MIMO detector is a linear receiver for [spatial multiplexing](/spatial-multiplexing/) that takes the noise level into account. It applies the filter $W = (H^H H + (N_0/E_s) I)^{-1} H^H$, which minimizes $E\|W y - x\|^2$ over all linear filters, divides each output by its gain $\beta_k$ to remove a bias, and slices each stream to the nearest constellation point. It differs from the [zero-forcing MIMO detector](/zero-forcing-mimo-detector/) only by the term $(N_0/E_s) I$: ZF removes all the interference and lets the noise grow, while MMSE leaves a little interference and much less noise. Among all linear filters, the MMSE filter gives each stream the largest SINR. As $N_0 \to 0$ it becomes ZF, and at low SNR it becomes the matched filter $H^H$ up to a scale. It is the [Wiener filter](/wiener-filter/) for the vector $x$. The same filter appears as the [MMSE linear equalizer](/mmse-linear-equalizer/) in time, as the [MMSE multiuser detector](/mmse-multiuser-detector/) in CDMA, and as [regularized ZF precoding](/regularized-zero-forcing-precoding/) at a transmitter. [V-BLAST](/v-blast/) with MMSE nulling and the [expectation propagation detector](/expectation-propagation-detection/) both start from this filter.

## In plain words

Several transmit antennas send different symbols at once, and each receive antenna hears a mix of them plus noise. A zero-forcing receiver undoes the mix exactly, but when the mix is hard to undo, it also makes the noise huge. The MMSE receiver asks a different question: which linear combination of the received signals is, on average, closest to the sent symbols? The answer undoes most of the mix but not all of it. Where undoing the mix would amplify the noise a lot, it holds back. When the noise is small, it acts like zero forcing. When the noise is large, it simply listens for each symbol in the direction where that symbol arrives strongest.

## The problem

The model is $y = H x + w$, with $H \in \mathbb{C}^{m \times n}$ known, $x \in \mathcal{S}^n$ for a constellation $\mathcal{S}$ of size $M$ with average energy $E_s$, and $w \sim \mathcal{CN}(0, N_0 I)$. The SNR is $E_s / N_0$ per complex symbol. The detector models the entries of $x$ as independent with mean 0 and variance $E_s$. It needs $N_0$, but unlike ZF it does not need $m \ge n$ or full column rank when $N_0 > 0$. The output is a decision $\hat x \in \mathcal{S}^n$.

## The algorithm

```pseudo id=main
MMSE-DETECT(y, H, S, N0, Es)
L1  P ← (Hᴴ H + (N0/Es) I)⁻¹                     ▷ N0 P is the error covariance
L2  W ← P Hᴴ
L3  z ← W y
L4  for k ← 1 to n
L5      β_k ← 1 - (N0/Es) P_kk                    ▷ β_k = (W H)_kk, the bias
L6      x̂_k ← the point of S nearest to z_k / β_k
L7  return x̂
```

Lines L1 and L2 depend only on the channel and on $N_0$, so a receiver computes them once per block. Line L1 is a Cholesky factorization of a positive definite matrix when $N_0 > 0$. With the push-through identity, $W = H^H (H H^H + (N_0/E_s) I)^{-1}$, which is cheaper when $m < n$. Line L5 computes the gain of stream $k$ in its own output: $E[z_k \mid x_k] = \beta_k x_k$ with $0 < \beta_k < 1$. For PSK and 4-QAM the division in line L6 does not change the decision, because the decision regions are cones. For 16-QAM and larger it does: without it, the outer points are pulled toward the origin and land in the wrong ring.

## Example

Take the channel and the received vector of the [ZF example](/zero-forcing-mimo-detector/): BPSK, $H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$, $x = (+1, -1)$, $w = (-0.5, 0.6)$ and $y = (0.5, 0.6)$. Let $N_0 = 0.5$, so $E_s / N_0 = 2$ (3.0 dB). Then $H^H H + 0.5 I = \begin{pmatrix} 5.5 & 3 \\ 3 & 2.5 \end{pmatrix}$ has determinant 4.75, and

$$P = \frac{1}{4.75}\begin{pmatrix} 2.5 & -3 \\ -3 & 5.5 \end{pmatrix}, \qquad W = P H^H = \frac{1}{4.75}\begin{pmatrix} 2 & -0.5 \\ -0.5 & 2.5 \end{pmatrix}.$$

| quantity | stream 1 | stream 2 |
|---|---|---|
| $z = W y$ | 0.7 / 4.75 = 0.147 | 1.25 / 4.75 = 0.263 |
| $\beta_k = 1 - 0.5\, P_{kk}$ | 3.5 / 4.75 = 0.737 | 2 / 4.75 = 0.421 |
| $z_k / \beta_k$ | 0.200 | 0.625 |
| decision | +1 (right) | +1 (wrong) |
| SINR $= 1/(0.5\, P_{kk}) - 1$ | 2.8 (4.5 dB) | 0.727 (-1.4 dB) |
| ZF SNR $= 2 / [(H^H H)^{-1}]_{kk}$ | 1 (0.0 dB) | 0.4 (-4.0 dB) |

ZF decided $(-1, +1)$ on this vector, with two errors. MMSE gets the first stream right and still misses the second, while the ML detector finds $(+1, -1)$. The last two rows show why: at the same SNR, MMSE gives the two streams 4.5 dB and 2.6 dB more SINR than ZF on this channel.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that $W$ minimizes $E\|W y - x\|^2$ over all $n \times m$ matrices, by the orthogonality principle, and that the minimum error covariance is $N_0 P$ (a theorem). It shows that row $k$ of $W$ is proportional to $h_k^H R_k^{-1}$, where $R_k$ is the covariance of the interference and the noise seen by stream $k$, so that this row maximizes the output SINR over all linear filters, and that this SINR is $1/((N_0/E_s) P_{kk}) - 1$ (a theorem). The same computation gives the bias $\beta_k = 1 - (N_0/E_s) P_{kk}$. Without noise and with full column rank, $W \to (H^H H)^{-1} H^H$ as $N_0 \to 0$, so the decisions become the ZF decisions, which are exact.

## Complexity

Forming $H^H H$ costs $n^2 m$ multiplications, the inverse in line L1 costs $O(n^3)$, and line L2 costs $n^2 m$. Per received vector, line L3 costs $n m$ multiplications and lines L4 to L6 cost $O(n M)$ by a linear scan, or $O(n)$ for square QAM by rounding. In the [real RAM](/real-ram/), a block of $T$ vectors on one channel costs $O(n^2 m + n^3 + T n (m + M))$, with $O(n m)$ extra space. This is the same order as ZF.

## Properties

- **Minimum mean square error.** Among linear filters, $W$ gives the smallest $E\|W y - x\|^2$, equal to $N_0\, \mathrm{tr}(P)$ (theorem).
- **Maximum SINR.** Each row of $W$ maximizes the SINR of its stream among all linear filters (theorem). After the bias removal, the SINR is $1/((N_0/E_s) P_{kk}) - 1$, which is never smaller than the ZF post-detection SNR.
- **Biased output.** $E[z_k \mid x_k] = \beta_k x_k$ with $\beta_k = \mathrm{SINR}_k / (1 + \mathrm{SINR}_k)$.
- **Limits.** As $N_0 \to 0$ with full column rank, MMSE becomes ZF. As $N_0 \to \infty$, $W$ tends to $(E_s/N_0) H^H$, the matched filter.
- **Diversity.** Tse and Viswanath (Section 8.3.1 and its exercises) give the MMSE receiver the same diversity as ZF, $m - n + 1$ in i.i.d. Rayleigh fading. Mehana and Nosratinia (2012) refined this: the diversity of the MMSE receiver depends on the rate, and at low rates it is larger, up to the ML value. So the MMSE gain over ZF is large at low and moderate SNR and shrinks to a fixed SNR offset at high SNR.
- **Capacity with cancellation.** With Gaussian codes and successive cancellation of decoded streams, MMSE nulling at each step reaches $\log_2 \det(I + (E_s/N_0) H H^H)$, the capacity with equal power (theorem, Tse and Viswanath, Section 8.3.4). The [D-BLAST](/d-blast/) page uses this.
- **Not ML.** For a fixed vector, the decision can differ from the ML decision, as in the example.

## Variants and improvements

- **MMSE with successive cancellation.** Detect the stream with the largest SINR, cancel it, and recompute the filter for the rest. This is [V-BLAST](/v-blast/) with MMSE nulling.
- **MMSE with soft output.** Treat $z_k / \beta_k$ as $x_k$ plus Gaussian noise of variance $E_s (1 - \beta_k) / \beta_k$ and compute bit LLRs as in [soft demapping](/soft-demapping/). This is the first stage of many coded receivers.
- **Soft interference cancellation.** With prior means and variances of the symbols from a decoder, replace $E_s I$ by the diagonal of the prior variances and subtract the prior means. This is the [soft interference cancellation equalizer](/soft-interference-cancellation-equalizer/) of turbo receivers.
- **Expectation propagation.** Run the MMSE filter again and again, each time with a Gaussian prior on each symbol that is fitted to the constellation; see the [expectation propagation detector](/expectation-propagation-detection/).
- **Lattice reduction with MMSE.** Apply lattice reduction to the extended matrix $\begin{pmatrix} H \\ \sqrt{N_0/E_s}\, I \end{pmatrix}$. ZF on this matrix is the MMSE filter, so MMSE inherits the gains of [lattice reduction aided detection](/lattice-reduction-aided-detection/).

## When to use it

Use MMSE when a linear detector is enough and the receiver has an estimate of $N_0$. It is never worse than ZF in SINR, it costs the same, and it works when the channel is ill conditioned or when $n > m$. In [massive MIMO](/massive-mimo/) uplinks with $m \gg n$, MMSE is close to optimal and is the default. On square channels at high SNR, its error rate is far from ML; use V-BLAST, a lattice reduction aided detector or a sphere search such as [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) instead.

## Pitfalls

- **Forgetting the bias.** For 16-QAM and larger, slicing $z_k$ without dividing by $\beta_k$ adds errors on the outer points. The tests on this page measure this effect.
- **The wrong $N_0$.** An $N_0$ that is much too small turns MMSE into ZF, and one that is much too large shrinks the outputs toward 0. Check the noise estimate.
- **Mixing up $N_0$ and $N_0/E_s$.** The regularization is the ratio $N_0 / E_s$. With a unit-energy constellation it is $N_0$; with a constellation of energy $E_s \ne 1$ it is not.
- **Treating the residual interference as white Gaussian noise.** The error $z_k - \beta_k x_k$ holds interference from discrete symbols, so it is not exactly Gaussian. Using a Gaussian model for LLRs is an approximation (a rule).
- **Calling it ML.** The MMSE detector minimizes the mean squared error of a linear estimate. It does not minimize the error probability of the vector.

## Implementations

## History

Jack Winters introduced optimum combining for antenna arrays with cochannel interference in 1984: weights that maximize the SINR at the output of the array, which is the MMSE filter of a single stream. The same linear MMSE idea appeared for CDMA multiuser detection in the early 1990s. With the Bell Labs layered space-time systems of Foschini and his colleagues in the late 1990s, the MMSE filter, with or without successive cancellation, became a standard MIMO detector. Tse and Viswanath (2005) showed how the MMSE filter with successive cancellation reaches the capacity of the MIMO channel, which links the simple receiver to the information theory.

## References
