---
tag: 8ZFGWM
kind: algorithm
slug: subspace-channel-identification
name: Subspace blind channel identification
aliases:
- Moulines subspace method
area: communications/channel-estimation-and-equalization
level: advanced
summary: "Identifies a multichannel FIR channel, up to one scalar, from the noise subspace of the covariance of an oversampled output. It needs subchannels with no common zero and a known channel length."
solves: [blind-equalization]
model: real-ram
complexity:
  vars: {P: the number of subchannels, L: the number of channel taps, N: the window length in symbols, K: the number of samples}
  time: {worst: O(K P^2 N^2 + P^3 N^4)}
  space: {extra: O(P^2 N^2)}
properties: {deterministic: true, online: false, blind: true, second_order_statistics: true, needs_known_order: true}
history:
  year: 1995
  people: [Eric Moulines, Pierre Duhamel, Jean-Francois Cardoso, Sylvie Mayrargue]
  note: "Moulines, Duhamel, Cardoso and Mayrargue published the subspace method in 1995, building on the result of Tong, Xu and Kailath that second-order statistics of an oversampled output determine the channel."
prereqs: [blind-equalization, eigenvalue, tong-xu-kailath-identification]
see_also: [music-algorithm, constant-modulus-algorithm, fractionally-spaced-equalizer, polynomial-gcd, sylvester-matrix, jacobi-eigenvalue-algorithm, covariance-matrix, channel-estimation]
sources:
  - paper: "Eric Moulines, Pierre Duhamel, Jean-Francois Cardoso and Sylvie Mayrargue, Subspace methods for the blind identification of multichannel FIR filters, IEEE Transactions on Signal Processing 43(2), 1995, pages 516 to 525"
    locator: "the block Toeplitz model, its full column rank for a window at least as long as the channel, and the identification of the channel from the noise subspace"
  - paper: doi:10.1109/18.312157
    title: "Lang Tong, Guanghan Xu and Thomas Kailath, Blind identification and equalization based on second-order statistics: a time domain approach, IEEE Transactions on Information Theory 40(2), 1994, pages 340 to 349"
    locator: "identifiability from second-order statistics when the subchannels have no common zero"
  - paper: "Guanghan Xu, Hui Liu, Lang Tong and Thomas Kailath, A least-squares approach to blind channel identification, IEEE Transactions on Signal Processing 43(12), 1995"
    locator: "the cross-relation method, which uses the same identity between pairs of subchannels"
---

Subspace blind channel identification estimates a channel with one input and $P \ge 2$ outputs, such as an oversampled or multi-antenna receiver, from the covariance of the received signal alone. It stacks $N$ consecutive output vectors into one long vector, whose covariance is $H_N H_N^H + \sigma^2 I$ for a block Toeplitz matrix $H_N$ built from the channel. The eigenvectors of the smallest eigenvalues, the noise subspace, are orthogonal to every column of $H_N$. That orthogonality is a set of linear equations in the channel taps, and the solution is the eigenvector of the smallest eigenvalue of a small matrix $Q$. The result is exact, up to one complex scalar, when the subchannels have no common zero and the covariance is exact. It solves the [blind equalization](/blind-equalization/) problem by identification, not by adapting an equalizer, and it uses only second-order statistics, unlike [CMA](/constant-modulus-algorithm/). It differs from [Tong-Xu-Kailath identification](/tong-xu-kailath-identification/), which uses the correlations at lags 0 and 1, whitens the signal part and assumes a white input. The subspace method uses only the lag-0 covariance of a stacked window, needs no whitening, and works for any input covariance of full rank. Both need the channel length.

## In plain words

When a receiver takes two or more samples per symbol, it sees the same symbols through two or more slightly different channels. The received vectors then lie close to a smaller set of directions that the channel fixes, and the directions left over contain only noise. The method finds these leftover directions from the measured correlations of the received signal. Every leftover direction must be at right angles to the channel's own directions, and this gives enough equations to find the channel, apart from one unknown factor. It fails when all the channels share a common zero, because then two different channels give the same correlations.

## The problem

The received vectors are
$$y[k] = \sum_{l=0}^{L-1} h(l)\, a[k-l] + w[k] \in \mathbb{C}^P,$$
with an unknown channel $h(0), \ldots, h(L-1) \in \mathbb{C}^P$, independent symbols $a[k]$ of unit power, and white noise of power $\sigma^2$ on each output. The stacked channel is $h = (h(0); \ldots; h(L-1)) \in \mathbb{C}^{PL}$. Subchannel $p$ has the transfer function $H_p(z) = \sum_l h_p(l) z^{-l}$. The input is the samples $y[0], \ldots, y[K-1]$, the number $P$ of subchannels, the channel length $L$ and a window length $N \ge L$. The output is $\hat h = \beta h$ for an unknown scalar $\beta$, with $\|\hat h\| = 1$.

**The stacked model.** The window $Y[k] = (y[k]; y[k-1]; \ldots; y[k-N+1]) \in \mathbb{C}^{PN}$ equals $H_N\, (a[k], \ldots, a[k-N-L+2])^T$ plus noise, where $H_N$ is the $PN \times (N+L-1)$ block Toeplitz matrix whose block $(i, m)$ is $h(m - i)$, and zero outside $0 \le m - i \le L - 1$. So $R = E[Y Y^H] = H_N H_N^H + \sigma^2 I$.

## The algorithm

```pseudo id=main
SUBSPACE-IDENTIFY(y, P, L, N)
L1  R ← (1/K') Σ_k Y[k] Y[k]^H                      ▷ sample covariance of the windows
L2  G ← eigenvectors of R for its PN - (N+L-1) smallest eigenvalues
L3  Q ← the PL × PL zero matrix
L4  for each g in G do
L5      build 𝒢(g): row m, for m = 0..N+L-2, is (g_m^H, g_{m-1}^H, ..., g_{m-L+1}^H), with g_i = 0 outside 0..N-1
L6      Q ← Q + 𝒢(g)^H 𝒢(g)
L7  ĥ ← the unit eigenvector of Q for its smallest eigenvalue
L8  return ĥ
```

Line L1 estimates $R$ from the $K' = K - N + 1$ windows. Line L2 takes the noise subspace: $H_N$ has rank $N + L - 1$, so $R$ has $PN - (N+L-1)$ eigenvalues equal to $\sigma^2$, and their eigenvectors are orthogonal to the columns of $H_N$. Here $g_i$ is block $i$ of $g$, a vector of length $P$. Line L5 rewrites the condition $g^H H_N = 0$ as $\mathcal{G}(g)\, h = 0$: entry $m$ of $g^H H_N$ is $\sum_l g_{m-l}^H h(l)$. Lines L3 to L6 sum the squared residuals over the noise subspace, so $h^H Q h = \sum_g \|g^H H_N\|^2$, and line L7 minimizes it on the unit sphere. The code solves the two Hermitian eigenproblems with the [Jacobi method](/jacobi-eigenvalue-algorithm/) on the real form $\begin{pmatrix} B & -C \\ C & B \end{pmatrix}$ of $A = B + jC$, which has every eigenvalue twice.

## Example

**A hand case.** Two subchannels $h_1 = (1, 0.5)$ and $h_2 = (0.5, 1)$, so $L = 2$, $h(0) = (1, 0.5)$ and $h(1) = (0.5, 1)$. Their zeros are $-0.5$ and $-2$: no common zero. With $N = 2$, the window has length 4 and
$$H_2 = \begin{pmatrix} 1 & 0.5 & 0 \\ 0.5 & 1 & 0 \\ 0 & 1 & 0.5 \\ 0 & 0.5 & 1 \end{pmatrix},$$
of rank 3. The noise subspace has dimension $4 - 3 = 1$, spanned by $g = (-1, 2, -2, 1)$: check $g^H H_2 = (-1 + 1,\ -0.5 + 2 - 2 + 0.5,\ -1 + 1) = 0$. So $g_0 = (-1, 2)$ and $g_1 = (-2, 1)$. With $h = (x_0, x_1, x_2, x_3)$, the three rows of line L5 give
$$-x_0 + 2x_1 = 0, \qquad -2x_0 + x_1 - x_2 + 2x_3 = 0, \qquad -2x_2 + x_3 = 0.$$
So $x_1 = x_0/2$, $x_3 = 2x_2$, and the middle equation gives $x_2 = x_0/2$: $h = x_0 (1, 0.5, 0.5, 1)$, the channel up to a scalar. The vector $g$ is the cross relation $h_2 * y_1 - h_1 * y_2 = 0$ between the two outputs, scaled by $-2$.

**From samples.** For the complex channel $h_1 = (1, 0.5 + 0.2j, -0.3)$, $h_2 = (0.4j, 1, 0.6)$, with $K = 2000$ QPSK symbols and noise of power $0.01$ per output, the misalignment $1 - |\hat h^H h|^2 / \|h\|^2$ is $2.7 \times 10^{-4}$ for $N = 3$ and $2.9 \times 10^{-4}$ for $N = 4$ (seed 1, a measurement). With the exact covariance, it is zero to rounding.

**A common zero.** If both subchannels contain the factor $(1 - 0.5 z^{-1})$, for example $h_1 = (1, -0.2, -0.15)$ and $h_2 = (0.2, 0.9, -0.5)$, then $Q$ has a null space of dimension 2, and line L7 can return any vector in it.

## Correctness

**Claim.** Let $P = 2$, $N \ge L$, $h(0) \ne 0$, $h(L-1) \ne 0$, and let the two subchannels have no common zero. With the exact covariance $R = H_N R_a H_N^H + \sigma^2 I$ for any input covariance $R_a$ of full rank, the null space of $Q$ is exactly $\{\beta h\}$, so line L7 returns $h / \|h\|$ up to a unit scalar. This is a theorem. For $P > 2$ the same holds under the condition that the $P$ subchannels have no zero common to all of them; that case is the theorem of Moulines and others (1995) and is cited, not proved here.

**Key steps.** First, $H_N$ has full column rank: a vector in its null space gives polynomial identities that, by the coprimality of the subchannels, force it to be zero. So the noise subspace is the whole left null space of $H_N$. Second, the cross-relation vector $g$ with blocks $g_i^H = (h_2(i), -h_1(i))$ lies in that null space. For any candidate $h'$, the condition $g^H H_N(h') = 0$ says $h_2 * h'_1 = h_1 * h'_2$ as sequences. Since the subchannels are coprime, $h_1$ divides $h'_1$, and the degree bound forces $h' = \beta h$. The proofs folder has the details.

**What it needs.** The channel length $L$ must be right. If $L$ is too large, the zero padding gives extra solutions, and $Q$ has a null space of dimension more than 1. The noise must be white with equal power on all outputs, or prewhitened. With a sample covariance, the estimate is consistent as $K \to \infty$, because the noise subspace depends continuously on $R$ when the eigenvalue gap is positive; the error at finite $K$ is a measurement.

## Complexity

Line L1 costs $O(K P^2 N^2)$. The eigenproblem of line L2 costs $O(P^3 N^3)$ with a standard Hermitian solver (the Jacobi method in the code costs that per sweep). Lines L3 to L6 handle at most $PN$ vectors, each with $N + L - 1$ rows and a rank-one update of $O(P^2 L^2)$, so $O(P^3 N^2 L^2) \le O(P^3 N^4)$. Line L7 is an eigenproblem of size $PL$. The extra space is $O(P^2 N^2)$ for $R$. All counts are in the [real RAM](/real-ram/).

## Properties

- **Blind and second order.** It needs only the covariance, not the alphabet, so it works for any input with a full-rank covariance.
- **One scalar ambiguity.** It returns $h$ up to a complex scalar, the least possible ambiguity for second-order statistics.
- **Batch.** It needs a block of samples long enough for a good covariance estimate.
- **Exact with exact statistics.** With the true covariance, it returns the true channel up to the scalar.
- **Order sensitive.** It needs the exact channel length $L$.

## Variants and improvements

- **Cross-relation method.** Xu, Liu, Tong and Kailath (1995) used the identities $h_q * y_p = h_p * y_q$ between every pair of outputs directly on the data, which avoids the eigenvectors of $R$.
- **Weighted subspace fitting.** Weighting the noise vectors by their eigenvalues gives a smaller variance from finite samples.
- **Order estimation.** The number of eigenvalues of $R$ near $\sigma^2$ gives $PN - (N + L - 1)$, from which $L$ can be estimated before line L2.
- **Equalization from the estimate.** With $\hat h$, a zero-forcing or MMSE [fractionally spaced equalizer](/fractionally-spaced-equalizer/) can be designed directly; for $P \ge 2$ and no common zero, an FIR zero-forcing equalizer exists.
- **Related subspace methods.** The idea of splitting the covariance into a signal subspace and a noise subspace is the same as in the [MUSIC algorithm](/music-algorithm/) for direction finding.

## When to use it

Use the subspace method when the receiver has $P \ge 2$ samples or antennas per symbol, the channel is fixed over a block, and its length is known or can be estimated. In the example, 2000 symbols already give a small error, and there is no local minimum to get stuck in, as there is for CMA. Do not use it at one sample per symbol, where second-order statistics cannot identify the channel, or when the subchannels are nearly coprime only, such as with little excess bandwidth, where the estimate is poor.

## Pitfalls

- **The wrong channel length in lines L2 and L5.** Overestimating $L$ leaves a null space of $Q$ of dimension more than 1, and line L7 returns a mixture. Underestimating it leaves no exact solution.
- **A small eigenvalue gap in line L2.** If the subchannels nearly share a zero, the smallest signal eigenvalue is close to $\sigma^2$, and the noise subspace is badly estimated.
- **Colored noise.** The noise eigenvalues are equal only for white noise of equal power. Prewhiten with the known noise covariance first.
- **Taking each eigenvalue once from the real form.** The real form of a complex Hermitian matrix has each eigenvalue twice. Line L2 must take $2(PN - N - L + 1)$ real eigenvectors, not $PN - N - L + 1$.
- **Expecting the scalar.** The phase and gain of $\hat h$ are arbitrary. A pilot, a decision-directed step or a carrier recovery stage must fix them.

## Implementations

## History

Tong, Xu and Kailath showed in 1991 that the second-order statistics of a fractionally sampled output identify the channel, which started the second-order blind methods. Moulines, Duhamel, Cardoso and Mayrargue (1995) gave the subspace method, which uses the noise subspace of the stacked covariance, and Xu, Liu, Tong and Kailath (1995) gave the closely related cross-relation method.

## References
