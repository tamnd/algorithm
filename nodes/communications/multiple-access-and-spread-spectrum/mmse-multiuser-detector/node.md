---
tag: 1NBA15
kind: algorithm
slug: mmse-multiuser-detector
name: MMSE multiuser detector
aliases:
- linear MMSE multiuser detector
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "A linear multiuser detector that applies (R + σ²A⁻²)⁻¹ to the matched filter outputs, which minimizes the mean square error and balances interference against noise."
solves: [multiuser-detection]
model: real-ram
complexity:
  vars: {K: the number of users, N: the number of chips per symbol}
  time: {worst: O(K^2 N + K^3)}
  space: {extra: O(K^2)}
properties: {deterministic: true, linear: true, needs_amplitudes: true, needs_noise_level: true, removes_interference: false, works_when_overloaded: true, near_far_resistant: true}
history:
  year: 1990
  people: [Zhenhua Xie, Robert T. Short, Craig K. Rushforth]
  note: "Xie, Short and Rushforth proposed the linear MMSE detector for synchronous multiuser channels in 1990; Madhow and Honig studied its adaptive form for CDMA in 1994."
prereqs: [multiuser-detection, decorrelating-detector]
see_also: [decorrelating-detector, matched-filter, wiener-filter, mmse-linear-equalizer, mmse-mimo-detector, successive-interference-cancellation, lms-algorithm, sherman-morrison-formula]
sources:
  - paper: doi:10.1109/26.339839
    title: "Upamanyu Madhow and Michael L. Honig, MMSE interference suppression for direct-sequence spread-spectrum CDMA, IEEE Transactions on Communications 42(12), 1994"
    locator: "pp. 3178 to 3188 (the MMSE detector, its SINR, and adaptive forms)"
  - book: isbn:9780521593731
    title: "Sergio Verdú, Multiuser Detection, Cambridge University Press, 1998"
    locator: "Chapter 6, Non-decorrelating linear multiuser detection"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 8.3.2, Linear MMSE receiver, and Discussion 8.1, Connections with CDMA multiuser detection"
---

The MMSE multiuser detector is the linear receiver for the [multiuser detection](/multiuser-detection/) problem that minimizes the mean square error between each output and the user's bit. A bank of [matched filters](/matched-filter/) gives $z = R A b + n$, where $R$ is the crosscorrelation matrix of the signatures and $A$ holds the amplitudes. The detector computes $x = (R + \sigma^2 A^{-2})^{-1} z$ and decides each bit by its sign. The term $\sigma^2 A^{-2}$ is what separates it from the [decorrelating detector](/decorrelating-detector/): the decorrelator removes all interference and lets the noise grow, while the MMSE detector leaves a little interference to keep the noise down. As $\sigma \to 0$ it becomes the decorrelator, and as $\sigma \to \infty$ its decisions become those of the matched filter. Among all linear detectors it has the largest signal to interference plus noise ratio (SINR) for every user, and the inverse always exists when $\sigma > 0$, even with more users than chips. It is the multiuser form of the [Wiener filter](/wiener-filter/), of the [MMSE equalizer](/mmse-linear-equalizer/) and of the [MMSE MIMO detector](/mmse-mimo-detector/).

## In plain words

A receiver tuned to one user also picks up part of every other user, plus noise. One way to fix this is to cancel the other users completely, but that also makes the noise count for more. Another way is to ignore the other users and only fight the noise. The MMSE detector finds the best balance between these two. When the noise is weak, it mostly cancels the other users. When the noise is strong, it mostly averages out the noise and accepts some leftover interference. To find the balance it must know how strong each user is and how strong the noise is. It still uses only a fixed linear mix of the tuned receivers, so it is fast.

## The problem

User $k = 1, \ldots, K$ sends one bit $b_k \in \{-1, +1\}$ per symbol interval with amplitude $A_k > 0$ and a signature $s_k$ of $N$ chips with $\|s_k\| = 1$. The users are synchronous, so the received chips in one interval are $y = S A b + w$, with $S = [s_1, \ldots, s_K]$, $A = \mathrm{diag}(A_k)$ and $w \sim \mathcal{N}(0, \sigma^2 I)$, where $\sigma^2 = N_0/2$. The receiver knows the signatures, the amplitudes and $\sigma$. The output is a decision $\hat b_k$ for each user. The matched filter outputs are $z = S^\top y = R A b + n$ with $R = S^\top S$ and $n \sim \mathcal{N}(0, \sigma^2 R)$.

## The algorithm

```pseudo id=main
MMSE-MUD(y, S, A, σ)
L1  z ← Sᵀ y                     ▷ one matched filter per user
L2  R ← Sᵀ S                     ▷ the crosscorrelations
L3  G ← R + σ² A⁻²               ▷ add σ²/A_k² to the diagonal entry k
L4  x ← G⁻¹ z                    ▷ solve G x = z
L5  return b̂_k ← sgn(x_k) for every k
```

Lines L1 and L2 are the same as in the decorrelator. Line L3 adds $\sigma^2 / A_k^2$ to the diagonal entry $k$, so a weak user gets a large term and a strong user a small one. Line L4 solves the system; $G$ is symmetric positive definite for $\sigma > 0$, so a [Cholesky decomposition](/cholesky-decomposition/) works and never fails. Line L5 takes the signs, with $+1$ for a zero output. The filter for user $k$ on $z$ is row $k$ of $G^{-1}$ divided by $A_k$; that positive factor does not change the sign, so line L4 omits it.

## Example

Three users with $N = 8$ chips use $s_1 = (1,1,1,1,1,1,1,1)/\sqrt 8$, $s_2 = (1,1,1,1,1,1,-1,-1)/\sqrt 8$ and $s_3 = (1,-1,1,-1,1,-1,1,1)/\sqrt 8$, so

$$R = \begin{pmatrix} 1 & 0.5 & 0.25 \\ 0.5 & 1 & -0.25 \\ 0.25 & -0.25 & 1 \end{pmatrix}.$$

The amplitudes are $A = (1, 4, 2)$, the bits are $b = (+1, -1, +1)$ and $\sigma = 0.5$. Line L3 adds $(0.25, 0.0156, 0.0625)$ to the diagonal. The first row of $G^{-1}$ is $(1.156, -0.675, -0.431)$, against $(1.667, -1, -0.667)$ for $R^{-1}$: the weak user 1 relies less on cancelling the others. One noisy draw gave $z = (-0.47, -4.21, 2.18)$. The matched filter decides user 1 wrong. The MMSE detector gives $x = (1.36, -4.66, 0.64)$, and the decorrelator gives $(1.97, -5.09, 0.41)$; both have all three signs right. The exact error rates and output SINRs at $\sigma = 0.5$ are:

| user | matched filter | decorrelator | MMSE | MMSE SINR | decorrelator SINR |
|---|---|---|---|---|---|
| 1 | 0.460 | 0.0607 | 0.0584 | 2.46 | 2.40 |
| 2 | $2.5 \times 10^{-10}$ | $2.9 \times 10^{-10}$ | $1.2 \times 10^{-11}$ | 43.5 | 38.4 |
| 3 | 0.0183 | $2.7 \times 10^{-4}$ | $1.7 \times 10^{-4}$ | 12.8 | 12.0 |

The MMSE detector is best for every user here. The gain is largest for the strong user 2, for which the decorrelator was slightly worse than the matched filter. At $\sigma = 0.8$ the error rates of user 3 are 0.058, 0.015 and 0.011 for the matched filter, the decorrelator and the MMSE detector.

## Correctness

**Claim.** For each user $k$, the filter $w_k = G^{-1} e_k / A_k$ on $z$ minimizes $E[(b_k - w^\top z)^2]$ over all linear filters $w$, and it maximizes the output SINR, which equals $A_k^2\, s_k^\top C_k^{-1} s_k$ with $C_k = \sigma^2 I + \sum_{j \ne k} A_j^2 s_j s_j^\top$. The decision $\mathrm{sgn}(w_k^\top z)$ is $\mathrm{sgn}(x_k)$.

**Key step.** The normal equations of the mean square error are $(R A^2 R + \sigma^2 R) w = A_k R e_k$, and $R A^2 R + \sigma^2 R = R A^2 G$, so $w_k$ solves them. The SINR bound follows from the Cauchy-Schwarz inequality, and the [Sherman-Morrison formula](/sherman-morrison-formula/) shows that $w_k$ reaches it. The full proof, with the two limits and the exact error rate, is in the proofs folder.

## Complexity

Line L1 costs $O(K N)$, line L2 costs $O(K^2 N)$ and line L4 costs $O(K^3)$ in the [real RAM](/real-ram/), the same as the decorrelator. When the signatures, the amplitudes and $\sigma$ stay the same, the factor of $G$ is computed once and each interval costs $O(K N + K^2)$. When the amplitudes change, $G$ must be factored again, which the decorrelator never needs.

## Properties

- **Minimum mean square error and maximum SINR** among linear detectors, for every user at the same time.
- **Between two known detectors.** It tends to the decorrelator as $\sigma \to 0$, and its decisions tend to those of the matched filter as $\sigma \to \infty$.
- **Always defined for $\sigma > 0$.** $G$ is positive definite even when $R$ is singular, so the detector works with more users than chips.
- **Needs amplitudes and the noise level.** Errors in these estimates move the detector away from the optimum.
- **Residual interference.** The outputs still hold some interference, so the error rate depends on the other users' amplitudes. The near-far resistance equals that of the decorrelator, because the two detectors agree as $\sigma \to 0$.
- **Not minimum error probability.** The residual interference is not Gaussian, so maximum SINR does not always give the lowest bit error rate, although it is close in practice.

## Variants and improvements

- **Adaptive MMSE.** For one user, the filter can be learned from training bits with the [LMS algorithm](/lms-algorithm/) or recursive least squares, without knowing the other signatures or amplitudes. Madhow and Honig studied this form.
- **Blind MMSE.** With only the wanted user's signature, minimizing the output energy under a constraint on the response to that signature gives the same filter up to scale.
- **Large systems.** With random signatures and $K$ and $N$ both large at a fixed ratio, the SINR of each user tends to a fixed value that solves a simple equation in the load $K/N$ and the other users' powers.
- **MMSE with cancellation.** Factoring $G$ by Cholesky gives an MMSE decision feedback detector, which cancels the decided users one at a time, as in [successive interference cancellation](/successive-interference-cancellation/).
- **Asynchronous and multipath channels.** Use the block matrices of a whole frame, or a finite window of chips, and the same formula.

## When to use it

Use the MMSE detector when the receiver can estimate the amplitudes and the noise level, when the system may be loaded with more users than chips, or when some signatures are highly correlated. It is the usual choice of linear detector in practice, and an adaptive form needs only training bits for the wanted user. When the amplitudes are unknown and change fast, the decorrelator is simpler.

## Pitfalls

- **Wrong noise level.** Using $\sigma = 0$ gives the decorrelator, and a very large $\sigma$ gives the matched filter. A badly wrong estimate loses the gain.
- **Forgetting the amplitude scaling.** The diagonal term is $\sigma^2 / A_k^2$, not $\sigma^2$. Using $\sigma^2 I$ is right only when all users have unit amplitude.
- **Expecting zero interference.** The output still holds interference. Analyses that treat it as Gaussian noise are approximations.
- **Recomputing per symbol.** Factor $G$ once while the signatures, amplitudes and $\sigma$ stay the same.

## Implementations

## History

Xie, Short and Rushforth proposed the linear MMSE detector for synchronous multiuser channels in 1990, as one of a family of suboptimum detectors. Madhow and Honig analyzed MMSE interference suppression for direct-sequence CDMA in 1994 and gave adaptive forms that need only the wanted user's signature and training data. These adaptive and blind forms made the MMSE detector the practical linear multiuser receiver. Its analysis for large random CDMA systems in the late 1990s gave simple formulas for the SINR as a function of the system load.

## References
