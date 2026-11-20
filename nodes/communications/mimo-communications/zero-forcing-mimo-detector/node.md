---
tag: Q1ZTZN
kind: algorithm
slug: zero-forcing-mimo-detector
name: Zero-forcing MIMO detector
aliases:
- ZF detector
- ZF MIMO receiver
area: communications/mimo-communications
level: core
summary: Applies the pseudoinverse of the channel matrix to remove the interference between streams, then slices each stream to the nearest symbol. The price is noise enhancement.
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {n: the number of transmitted streams, m: the number of receive antennas, M: the constellation size}
  time: {worst: O(n^2 m + n^3 + n M)}
  time_per_vector_after_setup: {worst: O(n m + n M)}
  space: {extra: O(n m)}
properties: {deterministic: true, linear: true, exact_ml: false, exact_ml_if_columns_orthogonal: true, needs_noise_level: false, diversity_order_iid_rayleigh: "m - n + 1"}
history:
  year: 1998
  people: [Peter W. Wolniansky, Gerard J. Foschini, Glen D. Golden, Reinaldo A. Valenzuela]
  note: "The nulling step of the V-BLAST receiver of 1998 made the pseudoinverse the reference linear receiver for spatial multiplexing. The same inverse is the decorrelating detector of CDMA, from the late 1980s."
prereqs: [mimo-detection, pseudoinverse]
see_also: [mmse-mimo-detector, v-blast, lattice-reduction-aided-detection, zero-forcing-equalizer, zero-forcing-precoding, decorrelating-detector, diversity-order, spatial-multiplexing]
sources:
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: "Section 8.3.1, Linear decorrelator (the ZF receiver, the projection onto the orthogonal complement of the other columns and the diversity nr - nt + 1 in i.i.d. Rayleigh fading)"
  - book: isbn:9780521826150
    title: Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003
    locator: Chapter 7, Space-time receivers (the ZF receiver for spatial multiplexing and its comparison with ML and MMSE)
  - paper: doi:10.1109/MSP.2009.932126
    title: Erik G. Larsson, MIMO detection methods - how they work, IEEE Signal Processing Magazine 26(3), 91-95, 2009
    locator: the section on linear receivers (ZF as the least squares solution followed by a per-stream decision)
  - paper: doi:10.1109/ISSSE.1998.738086
    title: Peter W. Wolniansky, Gerard J. Foschini, Glen D. Golden and Reinaldo A. Valenzuela, V-BLAST - an architecture for realizing very high data rates over the rich-scattering wireless channel, Proc. URSI International Symposium on Signals, Systems and Electronics, Pisa, 1998, pages 295-300
    locator: the nulling vectors (the rows of the pseudoinverse) that the V-BLAST receiver uses at each step
---

The zero-forcing (ZF) MIMO detector is the simplest receiver for [spatial multiplexing](/spatial-multiplexing/). It multiplies the received vector by the [pseudoinverse](/pseudoinverse/) of the channel matrix, which removes the interference between the transmitted streams completely, and then slices each stream to the nearest constellation point on its own. So it solves the [MIMO detection](/mimo-detection/) problem in two cheap steps instead of a search over all $M^n$ symbol vectors. The price is noise enhancement: stream $k$ gets noise of variance $N_0 [(H^H H)^{-1}]_{kk}$, which is large when the columns of $H$ are nearly dependent. In i.i.d. Rayleigh fading this cuts the [diversity order](/diversity-order/) from $m$ for ML to $m - n + 1$. The [MMSE MIMO detector](/mmse-mimo-detector/) adds the noise level to the same inverse and loses less, [V-BLAST](/v-blast/) detects the streams one by one and cancels each decision, and [lattice reduction aided detection](/lattice-reduction-aided-detection/) applies ZF to a better basis of the same lattice. The same inverse appears three more times on this site, with a different meaning of the matrix: the [ZF equalizer](/zero-forcing-equalizer/) inverts a convolution in time, [ZF precoding](/zero-forcing-precoding/) applies the inverse at the transmitter, and the [decorrelating detector](/decorrelating-detector/) inverts the correlation matrix of CDMA users.

## In plain words

Several antennas send different symbols at the same time on the same frequency. Each receive antenna hears a mix of all of them. If the receiver knows how the channel mixes the symbols, it can undo the mix exactly, like solving a set of linear equations. After that, each symbol stands alone, and the receiver picks the nearest valid symbol for each one. The problem is the noise. Undoing the mix also changes the noise, and when two transmit antennas look alike to the receiver, the noise grows very large. The detector ignores this risk, so it is fast but loses much of the reliability that a full search would give.

## The problem

The model is $y = H x + w$. Here $H \in \mathbb{C}^{m \times n}$ is the known channel matrix, with $m$ receive antennas (rows) and $n$ transmitted streams (columns), $x = (x_1, \ldots, x_n)$ holds one point of a unit-energy constellation $\mathcal{S}$ of size $M$ per stream, and $w \sim \mathcal{CN}(0, N_0 I)$. The SNR is $E_s / N_0$ per complex symbol, with $E_s = 1$. The detector needs $m \ge n$ and $H$ of full column rank, so that $H^H H$ is invertible. The output is a decision $\hat x \in \mathcal{S}^n$. ZF does not have to be the ML decision, and in general it is not.

## The algorithm

```pseudo id=main
ZF-DETECT(y, H, S)
L1  G ← Hᴴ H                                      ▷ n × n Gram matrix
L2  W ← G⁻¹ Hᴴ                                    ▷ the pseudoinverse H⁺
L3  z ← W y                                       ▷ z = x + W w
L4  for k ← 1 to n
L5      x̂_k ← the point of S nearest to z_k
L6  return x̂
```

Lines L1 and L2 depend only on the channel, so a receiver computes $W$ once per channel use of a block fading channel and then reuses it for every received vector of the block. Line L2 solves $G W = H^H$ by [Gaussian elimination](/gaussian-elimination/) or a [Cholesky decomposition](/cholesky-decomposition/), or it uses the [QR decomposition](/qr-decomposition/) $H = Q R$, where $W = R^{-1} Q^H$ is better conditioned because it does not square the condition number of $H$. Line L3 is the unconstrained [least squares](/least-squares-problem/) solution: it minimizes $\|y - H z\|^2$ over all $z \in \mathbb{C}^n$, not only over $\mathcal{S}^n$. Line L5 is the [minimum distance detector](/minimum-distance-detector/) for one symbol; for square QAM it is a rounding of the real and imaginary parts.

## Example

Take $m = n = 2$, BPSK with $\mathcal{S} = \{+1, -1\}$, and the real channel

$$H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}, \qquad H^{-1} = \begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}.$$

The transmitter sends $x = (+1, -1)$, so $H x = (1, 0)$. The noise is $w = (-0.5, 0.6)$, with $\|w\|^2 = 0.61$, and the receiver gets $y = (0.5, 0.6)$. Because $H$ is square, line L2 gives $W = H^{-1}$, and line L3 gives

$$z = H^{-1} y = (0.5 - 0.6,\; -0.5 + 1.2) = (-0.1,\; 0.7).$$

Line L5 decides $\hat x = (-1, +1)$. Both decisions are wrong. The ML detector compares the four candidates:

| candidate $x$ | $H x$ | $\|y - H x\|^2$ |
|---|---|---|
| $(+1, +1)$ | $(3, 2)$ | 8.21 |
| $(+1, -1)$ | $(1, 0)$ | 0.61 |
| $(-1, +1)$ | $(-1, 0)$ | 2.61 |
| $(-1, -1)$ | $(-3, -2)$ | 19.01 |

So ML finds the sent vector, and the ZF decision has the second best metric. The reason is the noise gain. The rows of $H^{-1}$ have the squared norms 2 and 5, so the two streams see noise of variance $2 N_0$ and $5 N_0$, losses of 3.0 dB and 7.0 dB. The noise $W w = (-1.1, 1.7)$ is much larger than $w$, and it moves both outputs across the decision boundary at 0. Without noise, line L3 gives $z = x$ exactly.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows four things. First, $W H = I$, so $z = x + W w$ with no interference from the other streams, and without noise ZF recovers $x$ exactly (a theorem). Second, the noise $W w$ is $\mathcal{CN}(0, N_0 (H^H H)^{-1})$, so stream $k$ has the post-detection SNR $(E_s / N_0) / [(H^H H)^{-1}]_{kk}$ (a closed form). Third, if the columns of $H$ are orthogonal, the ML metric separates into one term per stream, and ZF is exactly ML (a theorem). Fourth, $1 / [(H^H H)^{-1}]_{kk}$ is the squared distance from column $h_k$ to the span of the other $n - 1$ columns. In i.i.d. $\mathcal{CN}(0, 1)$ fading this is a sum of $m - n + 1$ independent unit exponentials, so the error probability of each stream decays as $\mathrm{SNR}^{-(m - n + 1)}$ (a theorem, Tse and Viswanath, Section 8.3.1).

## Complexity

Line L1 costs $n^2 m$ complex multiplications, or half of that with the symmetry of $G$. Line L2 costs $O(n^3 + n^2 m)$. Line L3 costs $n m$ multiplications per received vector, and line L5 costs $O(M)$ per stream by a linear scan, or $O(1)$ per stream for square QAM by rounding. So a block of $T$ vectors on one channel costs $O(n^2 m + n^3 + T n (m + M))$ in the [real RAM](/real-ram/), with $O(n m)$ extra space for $W$. Exhaustive ML costs $M^n$ metrics of $O(n m)$ each per vector.

## Properties

- **No interference.** $W H = I$, so each output depends on its own symbol and on noise only.
- **Noise enhancement.** Stream $k$ gets the noise variance $N_0 [(H^H H)^{-1}]_{kk} \ge N_0 / \|h_k\|^2$, with equality when $h_k$ is orthogonal to the other columns. The right side is the noise of a receiver that sees stream $k$ alone, the [maximal ratio combining](/maximal-ratio-combining/) bound.
- **Diversity.** In i.i.d. Rayleigh fading each stream has diversity order $m - n + 1$ (theorem). With $m = n$ this is 1, the diversity of a single antenna link, while ML has diversity $m$.
- **No noise level needed.** The filter uses only $H$. This is useful when $N_0$ is unknown, but it is also why ZF loses to MMSE at low SNR.
- **Exact on orthogonal channels.** When $H^H H$ is diagonal, the decision is the ML decision.
- **Same decision for every constellation size.** The filter does not depend on $\mathcal{S}$. Only line L5 does.

## Variants and improvements

- **ZF with QR.** Compute $H = Q R$ and solve $R z = Q^H y$ by back substitution. This avoids forming $H^H H$, whose condition number is the square of that of $H$.
- **ZF with successive cancellation.** Detect one stream, subtract it, and solve the smaller problem. With a fixed order this is the ZF decision feedback receiver, the [Babai nearest plane](/babai-nearest-plane/) rule of lattice theory. With the order chosen by the best post-detection SNR it is [V-BLAST](/v-blast/).
- **MMSE.** Replace $H^H H$ by $H^H H + (N_0 / E_s) I$; see the [MMSE MIMO detector](/mmse-mimo-detector/).
- **Lattice reduction.** Apply ZF to the channel $H T$ for a unimodular $T$ from the [LLL algorithm](/lll-algorithm/). With i.i.d. Rayleigh fading this reaches the receive diversity $m$; see [lattice reduction aided detection](/lattice-reduction-aided-detection/).
- **Soft output.** For a coded system, compute bit LLRs from $z_k$ with the noise variance $N_0 [(H^H H)^{-1}]_{kk}$, as for a scalar channel; see [soft demapping](/soft-demapping/).

## When to use it

Use ZF when $m$ is much larger than $n$, as in [massive MIMO](/massive-mimo/) uplinks, where $H^H H$ is close to a scaled identity and the noise gain is small, or when the receiver does not know $N_0$. It is also the reference that every other detector on this site must beat. On square channels ($m = n$) at moderate SNR, the loss is large: use MMSE, V-BLAST or a lattice reduction aided detector instead, and use a sphere search such as [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) when the ML decision is needed.

## Pitfalls

- **Square channels.** With $m = n$ and i.i.d. Rayleigh fading, the diversity is 1. The error rate falls by only a factor of 10 for each 10 dB of SNR.
- **Ill-conditioned channels.** A channel with nearly dependent columns, for example from antenna correlation or a line-of-sight path, can give noise gains of 20 dB or more. Check the [condition number](/condition-number/) of $H$.
- **Forming $H^H H$ in floating point.** This squares the condition number. Use a QR decomposition when $H$ is ill conditioned.
- **Bias assumptions.** ZF is unbiased: $E[z \mid x] = x$. Do not apply the bias correction of the MMSE detector to it.
- **Wide channels.** With $n > m$, $H^H H$ is singular and ZF is not defined. The streams cannot be separated by any linear filter.
- **Noise variance for soft output.** The output noise of stream $k$ has variance $N_0 [(H^H H)^{-1}]_{kk}$, not $N_0$. A demapper that uses $N_0$ gives LLRs that are too large.

## Implementations

## History

Linear receivers that null interfering signals with an antenna array were studied for adaptive arrays long before MIMO. The same inverse was the decorrelating detector for synchronous CDMA in the late 1980s. When Foschini and his colleagues at Bell Labs built the first spatial multiplexing systems, the V-BLAST receiver of Wolniansky, Foschini, Golden and Valenzuela in 1998 used the rows of the pseudoinverse as nulling vectors, and ZF became the reference linear MIMO detector. The diversity result $m - n + 1$ for i.i.d. Rayleigh fading is part of the standard analysis of linear MIMO receivers, as in Tse and Viswanath (2005).

## References
