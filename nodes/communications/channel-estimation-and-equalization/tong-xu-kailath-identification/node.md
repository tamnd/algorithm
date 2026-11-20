---
tag: WX9EA1
kind: algorithm
slug: tong-xu-kailath-identification
name: Tong-Xu-Kailath blind identification
aliases:
- second-order statistics blind identification
area: communications/channel-estimation-and-equalization
level: advanced
summary: "Estimates an oversampled FIR channel, up to a phase, from the output correlations at lags 0 and 1 by whitening and a shift. It is exact when the subchannels have no common zero."
solves: [blind-equalization]
model: real-ram
complexity:
  vars: {P: the number of subchannels, L: the number of channel taps, N: the window length in symbols, K: the number of samples}
  time: {worst: O(K P^2 N^2 + P^3 N^3)}
  space: {extra: O(P^2 N^2)}
properties: {deterministic: true, online: false, blind: true, second_order_statistics: true, needs_known_order: true, needs_white_input: true}
history:
  year: 1991
  people: [Lang Tong, Guanghan Xu, Thomas Kailath]
  note: "Tong, Xu and Kailath presented the method in 1991 and published the full time-domain version in IEEE Transactions on Information Theory in 1994. It was the first proof that second-order statistics of a fractionally sampled output identify a nonminimum-phase channel."
prereqs: [blind-equalization, eigenvalue, fractionally-spaced-equalizer]
see_also: [subspace-channel-identification, constant-modulus-algorithm, cyclostationary-feature-detection, polynomial-gcd, sylvester-matrix, jacobi-eigenvalue-algorithm, covariance-matrix, channel-estimation]
sources:
  - paper: doi:10.1109/18.312157
    title: "Lang Tong, Guanghan Xu and Thomas Kailath, Blind identification and equalization based on second-order statistics: a time domain approach, IEEE Transactions on Information Theory 40(2), 1994, pages 340 to 349"
    locator: "the identifiability condition (no common zero of the subchannels) and the identification algorithm from the correlations at lags 0 and 1"
  - paper: "Lang Tong, Guanghan Xu and Thomas Kailath, A new approach to blind identification and equalization of multipath channels, Conference Record of the 25th Asilomar Conference on Signals, Systems and Computers, Pacific Grove, 1991, volume 2, pages 856 to 860"
    locator: "the first, conference version of the method; this page relies on the 1994 journal version"
  - paper: "Eric Moulines, Pierre Duhamel, Jean-Francois Cardoso and Sylvie Mayrargue, Subspace methods for the blind identification of multichannel FIR filters, IEEE Transactions on Signal Processing 43(2), 1995, pages 516 to 525"
    locator: "the full column rank of the block Toeplitz channel matrix, used here as a lemma"
  - paper: doi:10.1109/5.720246
    title: "C. Richard Johnson, Jr., Philip Schniter, Thomas J. Endres, James D. Behm, Donald R. Brown and Raul A. Casas, Blind equalization using the constant modulus criterion: a review, Proceedings of the IEEE 86(10), 1998, starting at page 1927"
    locator: "the background on fractionally spaced blind equalization and the role of second-order methods"
---

Tong-Xu-Kailath identification estimates a channel with one input and $P \ge 2$ outputs, such as a receiver that takes $P$ samples per symbol, from two correlation matrices of the received signal: the lag-0 matrix $R(0)$ and the lag-1 matrix $R(1)$ of a stacked window. It removes the noise, whitens the signal part of $R(0)$, and uses $R(1)$, which is the whitened channel times a shift, to read off the channel one tap at a time. The result is exact, up to a phase, when the subchannels have no common zero, the input is white with known power, and the statistics are exact. This was the first proof that second-order statistics are enough for [blind equalization](/blind-equalization/) once the signal is oversampled, which is impossible at one sample per symbol. It differs from [subspace identification](/subspace-channel-identification/), which uses only the noise subspace of $R(0)$, needs no whitening and works for any input covariance of full rank. TXK uses the signal subspace and the lag-1 shift, and needs a white input. Both need the channel length and differ from [CMA](/constant-modulus-algorithm/), which uses fourth-order statistics and adapts online.

## In plain words

If a receiver takes two samples per symbol, it sees the same symbols through two different channels. The method measures how the received samples are correlated with each other, both within one window and between one window and the next. From the first measurement it builds a transform that makes the signal look like plain uncorrelated symbols. The second measurement, after the transform, shows how each symbol moves one step through the window. Following this step from the first symbol reveals the channel, one echo after another. It fails only if all the channels share a common zero, because then a different channel gives the same correlations.

## The problem

The received vectors are $y[k] = \sum_{l=0}^{L-1} h(l)\, a[k-l] + w[k] \in \mathbb{C}^P$, with independent symbols of unit power and white noise of power $\sigma^2$ on each output. The window $Y[k] = (y[k]; \ldots; y[k-N+1])$ has length $PN$ and equals $H_N s[k]$ plus noise, where $s[k] = (a[k], \ldots, a[k-N-L+2])$ and $H_N$ is the block Toeplitz matrix with block $(i, m)$ equal to $h(m-i)$. Let $d = N + L - 1$ and let $J$ be the $d \times d$ shift with ones just below the diagonal. Then
$$R(0) = E[Y[k] Y[k]^H] = H_N H_N^H + \sigma^2 I, \qquad R(1) = E[Y[k] Y[k-1]^H] = H_N J H_N^H + \sigma^2 (J_N \otimes I_P),$$
where $J_N$ is the $N \times N$ shift. The noise term in $R(1)$ appears because consecutive windows overlap in $N - 1$ samples. The input is estimates of $R(0)$ and $R(1)$, the noise power $\sigma^2$ (or an estimate), $P$, $L$ and $N \ge L$. The output is $\hat h = e^{j\theta} h$.

## The algorithm

```pseudo id=main
TXK-IDENTIFY(R(0), R(1), σ², P, L, N)
L1  A0 ← R(0) - σ² I;   A1 ← R(1) - σ² (J_N ⊗ I_P)
L2  (U, Λ) ← the d = N + L - 1 largest eigenpairs of A0
L3  F ← Λ^(-1/2) U^H                                ▷ whitening, d × PN
L4  M ← F A1 F^H                                     ▷ d × d, equals V J V^H
L5  v ← the unit eigenvector of M M^H for its smallest eigenvalue
L6  for l ← 0 to L - 1 do
L7      h(l) ← block 0 of U Λ^(1/2) v
L8      v ← M v
L9  return h
```

Line L1 removes the noise from both correlations. Line L2 keeps the signal subspace: $A_0 = H_N H_N^H$ has rank $d$. Line L3 builds a whitening matrix $F$, so that $V = F H_N$ is a $d \times d$ unitary matrix. Line L4 maps the lag-1 correlation through $F$, which gives $M = V J V^H$. Since $J^T$ has the null vector $e_0$, line L5 finds $v = e^{j\theta} V e_0$, the whitened first column of $H_N$. Lines L6 to L8 walk down the columns: $M^l v = e^{j\theta} V e_l$, and $U \Lambda^{1/2} V e_l$ is column $l$ of $H_N$, whose first block is $h(l)$. If $\sigma^2$ is unknown, the code estimates it as the mean of the $PN - d$ smallest eigenvalues of $R(0)$.

## Example

**A hand case.** Two subchannels $h_1 = (1, 0.5)$ and $h_2 = (0.5, 1)$, so $h(0) = (1, 0.5)$, $h(1) = (0.5, 1)$, $L = 2$, and $N = 2$, $d = 3$. Without noise,
$$A_0 = \begin{pmatrix} 1.25 & 1 & 0.5 & 0.25 \\ 1 & 1.25 & 1 & 0.5 \\ 0.5 & 1 & 1.25 & 1 \\ 0.25 & 0.5 & 1 & 1.25 \end{pmatrix}, \qquad A_1 = \begin{pmatrix} 0.5 & 0.25 & 0 & 0 \\ 1 & 0.5 & 0 & 0 \\ 1.25 & 1 & 0.5 & 0.25 \\ 1 & 1.25 & 1 & 0.5 \end{pmatrix}.$$
The eigenvalues of $A_0$ are $0, 0.329, 1.25, 3.421$, so line L2 keeps the last three. The rest of the run gives $\hat h = -(1, 0.5, 0.5, 1)$: the channel with the phase $\pi$. Because the input has unit power, the gain is exact; only the phase is unknown. The same output comes from $R(0)$ with $\sigma^2 = 0.3$ added on the diagonal and $R(1)$ with $0.3$ added on its block subdiagonal.

**From samples.** For $h_1 = (1, 0.5 + 0.2j, -0.3)$, $h_2 = (0.4j, 1, 0.6)$, $K = 3000$ QPSK symbols, noise of power $0.01$ per output and an estimated $\sigma^2$, the largest entry error after the best phase is $1.2$ percent of $\|h\|$ for $N = 3$ and $N = 4$ (seed 1, a measurement). With exact statistics it is below $10^{-14}$.

**A common zero.** Let both subchannels contain the factor $1 - 0.5 z^{-1}$: $h_p = (1 - 0.5 z^{-1})\, q_p(z)$ with $q_1 = (1, 0.3)$, $q_2 = (0.2, 1)$. Replace the factor by $-0.5 + z^{-1}$, which has the same magnitude on the unit circle. The two channels differ, but their $R(0)$ and $R(1)$ agree to $10^{-16}$, so no method that uses these statistics can tell them apart.

## Correctness

**Claim.** Assume that the subchannels have no common zero, $h(0) \ne 0$, $h(L-1) \ne 0$, $N \ge L$, the input is white with unit power, and the statistics are exact. Then lines L1 to L9 return $e^{j\theta} h$. This is a theorem.

**Key steps.** First, $H_N$ has full column rank $d$; this needs the no-common-zero condition, and for $P = 2$ it is Lemma 1 of the subspace page's proof. So $A_0 = U \Lambda U^H$ with $d$ positive eigenvalues, and $V = F H_N$ satisfies $V V^H = \Lambda^{-1/2} U^H A_0 U \Lambda^{-1/2} = I$, so $V$ is unitary. Second, the input correlation at lag 1 is $J$, so $M = V J V^H$, and $M^H x = 0$ exactly when $V^H x$ is a multiple of $e_0$. Third, $M^l V e_0 = V J^l e_0 = V e_l$, and $U \Lambda^{1/2} V e_l = U U^H H_N e_l = H_N e_l$, whose block 0 is $h(l)$. The proofs folder has the details.

**The condition is also necessary.** If the subchannels share a zero, flipping it to its reciprocal conjugate in every subchannel changes $h$ but, with a white input, keeps $R(m)$ for every lag $m$. The example above shows this. So no method can identify such a channel from second-order statistics.

**What it needs.** The white input with known power is part of the model: with a colored input, $R(1)$ has $H_N R_a(1) H_N^H$ in place of $H_N J H_N^H$, and the shift structure breaks. The channel length $L$ must be right, for the rank $d$ in line L2.

## Complexity

Estimating $R(0)$ and $R(1)$ from $K$ samples costs $O(K P^2 N^2)$. The eigenproblem of line L2 costs $O(P^3 N^3)$. Lines L3 to L5 multiply matrices of size at most $PN$, which costs $O(P^3 N^3)$, and line L5 is an eigenproblem of size $d \le PN$. Lines L6 to L8 cost $O(L d^2)$. The extra space is $O(P^2 N^2)$. All counts are in the [real RAM](/real-ram/).

## Properties

- **Blind and second order.** It needs only $R(0)$, $R(1)$ and the input power, not the alphabet.
- **Only a phase is unknown.** With a white input of known power, the gain of $h$ is found exactly; only $e^{j\theta}$ remains.
- **Batch.** It needs enough samples to estimate the correlations.
- **Needs a white input.** The shift structure in line L4 depends on it.
- **Works for nonminimum-phase channels.** The oversampling breaks the phase ambiguity of symbol-rate second-order statistics.

## Variants and improvements

- **The subspace method.** [Subspace identification](/subspace-channel-identification/) uses the noise subspace of $R(0)$ alone. It does not need a white input or $R(1)$.
- **Frequency-domain form.** The cyclostationary correlation of the oversampled signal gives the same information in the frequency domain; see [cyclostationary feature detection](/cyclostationary-feature-detection/) for the property used.
- **Using more lags.** Using $R(m)$ for several lags $m$, or a least squares fit of the shift structure, reduces the variance.
- **Cross-relation method.** The identity $h_q * y_p = h_p * y_q$ between pairs of outputs gives a least squares estimate directly from the data.
- **Equalization from the estimate.** With $\hat h$, an FIR zero-forcing or MMSE [fractionally spaced equalizer](/fractionally-spaced-equalizer/) can be designed directly; with no common zero, an exact FIR zero-forcing equalizer exists.

## When to use it

Use it as a direct, closed form way to identify an oversampled channel from short blocks when the input is white and its power is known. It is also the cleanest demonstration that oversampling makes second-order blind identification possible. The subspace method avoids the whitening and the walk of line L8, whose errors grow along the taps, so it is often preferred. CMA is used when the receiver must adapt online.

## Pitfalls

- **Leaving out the noise term of R(1) in line L1.** Consecutive windows share $N - 1$ samples, so the noise contributes $\sigma^2 (J_N \otimes I_P)$ to $R(1)$, not zero. Without this term, the estimate is biased.
- **A wrong rank in line L2.** If $L$ is wrong, $d$ is wrong, and the whitening keeps a noise direction or drops a signal direction.
- **Nearly common zeros.** If the subchannels nearly share a zero, the smallest kept eigenvalue in line L2 is small, $\Lambda^{-1/2}$ amplifies the estimation error, and the result is poor.
- **Errors that grow along the walk in line L8.** Each step multiplies by $M$, so an error in $v$ or $M$ grows over the taps. Late taps are less accurate than early ones.
- **A colored or unknown-power input.** The method assumes $E[s s^H] = I$. Scale the data first if the power is known; use the subspace method if the input is colored.

## Implementations

## History

Lang Tong, Guanghan Xu and Thomas Kailath presented the method in 1991 and published the full time-domain version in 1994. It showed that, unlike at the symbol rate, second-order statistics of a fractionally sampled output identify the channel, including its phase, if the subchannels have no common zero. It started a line of second-order blind methods, among them the subspace method of Moulines, Duhamel, Cardoso and Mayrargue (1995) and the cross-relation method of Xu, Liu, Tong and Kailath (1995).

## References
