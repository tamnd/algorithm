---
tag: X81J9E
kind: algorithm
slug: decorrelating-detector
name: Decorrelating detector
aliases:
- decorrelator
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "A linear multiuser detector that applies the inverse of the users' crosscorrelation matrix to the matched filter outputs, which removes all multiple access interference at the cost of more noise."
solves: [multiuser-detection]
model: real-ram
complexity:
  vars: {K: the number of users, N: the number of chips per symbol}
  time: {worst: O(K^2 N + K^3)}
  space: {extra: O(K^2)}
properties: {deterministic: true, linear: true, needs_amplitudes: false, needs_noise_level: false, removes_interference: true, enhances_noise: true, near_far_resistant: true}
history:
  year: 1989
  people: [Ruxandra Lupas, Sergio Verdú]
  note: "Lupas and Verdú analyzed the decorrelating detector for synchronous CDMA and showed that its near-far resistance equals that of the optimum multiuser detector."
prereqs: [multiuser-detection, least-squares-problem]
see_also: [mmse-multiuser-detector, optimum-multiuser-detector, near-far-problem, zero-forcing-mimo-detector, zero-forcing-equalizer, parallel-interference-cancellation, pseudoinverse, schur-complement]
sources:
  - paper: doi:10.1109/18.42183
    title: "Ruxandra Lupas and Sergio Verdú, Linear multiuser detectors for synchronous code-division multiple-access channels, IEEE Transactions on Information Theory 35(1), 1989"
    locator: "pp. 123 to 136 (the decorrelating detector, its error probability, and its near-far resistance, equal to that of the optimum detector)"
  - book: isbn:9780521593731
    title: "Sergio Verdú, Multiuser Detection, Cambridge University Press, 1998"
    locator: "Chapter 5, Decorrelating detector"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 8.3.1, Linear decorrelator, and Discussion 8.1, Connections with CDMA multiuser detection"
---

The decorrelating detector, or decorrelator, is the simplest receiver for the [multiuser detection](/multiuser-detection/) problem that removes all multiple access interference. A bank of [matched filters](/matched-filter/) gives $z = R A b + n$, where $R$ is the crosscorrelation matrix of the users' signatures. The decorrelator multiplies by $R^{-1}$ and decides each bit by its sign. Each output is then the user's own amplitude and bit plus noise, whatever the other users send and however strong they are. So it solves the [near-far problem](/near-far-problem/) without power control and without knowing any amplitude. The price is that the noise grows by the factor $(R^{-1})_{kk} \ge 1$. Lupas and Verdú showed in 1989 that its near-far resistance equals that of the [optimum detector](/optimum-multiuser-detector/), at a cost that is polynomial in the number of users $K$. It is the CDMA form of the [zero-forcing equalizer](/zero-forcing-equalizer/) and of the [zero-forcing MIMO detector](/zero-forcing-mimo-detector/). The [MMSE detector](/mmse-multiuser-detector/) adds the noise level to the same design and trades a little interference for less noise.

## In plain words

Each user's code looks a little like the codes of the others, so a receiver tuned to one user also picks up a bit of every other user. When another user is much stronger, that bit can be larger than the wanted signal. The decorrelator knows how much each code looks like each other code. It combines the outputs of all the tuned receivers in exactly the way that cancels every other user. What remains for each user is its own signal and some noise. The strength of the other users no longer matters. The cost is that cancelling the others also removes the part of the wanted signal that looks like them, so the noise counts for more. If two codes are almost the same, that cost becomes very large.

## The problem

User $k = 1, \ldots, K$ sends one bit $b_k \in \{-1, +1\}$ per symbol interval with amplitude $A_k > 0$ and a signature $s_k$ of $N$ chips with $\|s_k\| = 1$. The users are synchronous, so the received chips in one interval are $y = S A b + w$, where $S = [s_1, \ldots, s_K]$, $A = \mathrm{diag}(A_k)$ and $w \sim \mathcal{N}(0, \sigma^2 I)$. This is the in-phase part of the complex model for coherent BPSK, with $\sigma^2 = N_0/2$. The receiver knows the signatures but not the amplitudes or $\sigma$. The output is a decision $\hat b_k$ for each user. The matched filter outputs are $z = S^\top y = R A b + n$ with $R = S^\top S$ and $n \sim \mathcal{N}(0, \sigma^2 R)$.

## The algorithm

```pseudo id=main
DECORRELATOR(y, S)
L1  z ← Sᵀ y                     ▷ one matched filter per user
L2  R ← Sᵀ S                     ▷ the crosscorrelations, 1 on the diagonal
L3  x ← R⁻¹ z                    ▷ solve R x = z by Gaussian elimination
L4  return b̂_k ← sgn(x_k) for every k
```

Line L1 correlates the received chips with each signature. Line L2 needs only the signatures, so for a fixed set of users it is computed once. Line L3 solves the linear system; it fails when $R$ is singular, which happens exactly when the signatures are linearly dependent, and in particular when $K > N$. Line L4 takes the sign of each output, with $+1$ for a zero output. Since $R^{-1} S^\top$ is the [pseudoinverse](/pseudoinverse/) of $S$, the vector $x$ is also the [least squares](/least-squares-problem/) fit of $y$ by the signatures.

## Example

Three users with $N = 8$ chips use $s_1 = (1,1,1,1,1,1,1,1)/\sqrt 8$, $s_2 = (1,1,1,1,1,1,-1,-1)/\sqrt 8$ and $s_3 = (1,-1,1,-1,1,-1,1,1)/\sqrt 8$. Then

$$R = \begin{pmatrix} 1 & 0.5 & 0.25 \\ 0.5 & 1 & -0.25 \\ 0.25 & -0.25 & 1 \end{pmatrix}, \qquad R^{-1} = \frac{1}{3}\begin{pmatrix} 5 & -3 & -2 \\ -3 & 5 & 2 \\ -2 & 2 & 4 \end{pmatrix}.$$

The amplitudes are $A = (1, 4, 2)$, so user 2 is 12 dB stronger than user 1, and the bits are $b = (+1, -1, +1)$. Without noise, $z = (-0.5, -4, 3.25)$; the matched filter decides user 1 wrong, and $R^{-1} z = (1, -4, 2) = A b$ exactly. With $\sigma = 0.5$, one noisy draw gave $z = (-0.47, -4.21, 2.18)$ and $x = R^{-1} z = (1.97, -5.09, 0.41)$, all three signs right. The exact error rates at $\sigma = 0.5$ are:

| user | single-user bound $Q(A_k/\sigma)$ | matched filter | decorrelator | $1/(R^{-1})_{kk}$ |
|---|---|---|---|---|
| 1 | 0.0228 | 0.460 | 0.0607 | 0.60 |
| 2 | $6.2 \times 10^{-16}$ | $2.5 \times 10^{-10}$ | $2.9 \times 10^{-10}$ | 0.60 |
| 3 | $3.2 \times 10^{-5}$ | 0.0183 | $2.7 \times 10^{-4}$ | 0.75 |

The weak user 1 goes from an error rate near one half to 0.061. The decorrelator pays $1/0.6$, or 2.2 dB, of energy for users 1 and 2, and 1.2 dB for user 3. For the strong user 2 the matched filter is slightly better: the interference it sees is small compared with its own signal, and the decorrelator's noise penalty costs more than it saves.

## Correctness

**Claim.** If the signatures are linearly independent, then $x = A b + \tilde n$ with $\tilde n \sim \mathcal{N}(0, \sigma^2 R^{-1})$, so user $k$ errs with probability $Q(A_k / (\sigma \sqrt{(R^{-1})_{kk}}))$, which depends on neither the bits nor the amplitudes of the other users. Without noise every decision is right.

**Key step.** $R^{-1} z = R^{-1} R A b + R^{-1} n$, and the covariance of $R^{-1} n$ is $\sigma^2 R^{-1} R R^{-1} = \sigma^2 R^{-1}$. The penalty $1/(R^{-1})_{kk}$ is the squared length of the part of $s_k$ orthogonal to the other signatures, by the [Schur complement](/schur-complement/). The full proof is in the proofs folder.

## Complexity

Line L1 costs $O(K N)$, line L2 costs $O(K^2 N)$ and line L3 costs $O(K^3)$ in the [real RAM](/real-ram/). When the signatures stay the same over many intervals, $R^{-1}$ or a [Cholesky](/cholesky-decomposition/) factor of $R$ is computed once, and each interval then costs $O(K N + K^2)$. In an asynchronous system with $M$ symbols per user, $R$ is a block Toeplitz matrix of size $K M$ with bandwidth about $2K$, and a banded solver costs $O(M K^3)$.

## Properties

- **No interference.** Each output is $A_k b_k$ plus Gaussian noise. The detector is the zero-forcing solution of the multiuser problem.
- **Near-far resistant.** The asymptotic efficiency $1/(R^{-1})_{kk}$ does not depend on the amplitudes, so it is also the near-far resistance. No detector, linear or not, has a larger near-far resistance (Lupas and Verdú).
- **Needs no amplitudes and no noise level.** It uses only the signatures, unlike the optimum and the MMSE detectors.
- **Noise enhancement.** $(R^{-1})_{kk} \ge 1$, with equality only when $s_k$ is orthogonal to all the others. For two users with correlation $\rho$, the loss is $1/(1 - \rho^2)$.
- **Least squares and maximum likelihood.** $x$ minimizes $\|y - S x\|^2$, so it is the maximum likelihood estimate of $A b$ when that vector is treated as an unknown real vector.

## Variants and improvements

- **Asynchronous decorrelator.** Apply the inverse of the block Toeplitz crosscorrelation matrix of a whole frame, or a one-shot decorrelator that treats each partial overlap as an extra virtual user.
- **Decorrelating decision feedback.** Factor $R = F^\top F$ by Cholesky, whiten with $F^{-\top}$, and cancel the users one at a time with decisions, as in a [decision feedback equalizer](/decision-feedback-equalizer/).
- **Decorrelator as a first stage.** Use its decisions to start [parallel interference cancellation](/parallel-interference-cancellation/), as in the multistage detector of Varanasi and Aazhang.
- **Adaptive and blind forms.** For the user $k$ alone, the decorrelating filter is the projection of $s_k$ orthogonal to the other signatures. It can be learned from the received data without knowing the other signatures, which led to blind adaptive multiuser detection.
- **Regularized form.** Adding $\sigma^2 A^{-2}$ to $R$ gives the [MMSE detector](/mmse-multiuser-detector/).

## When to use it

Use the decorrelator when the users have very different powers and the receiver does not know the amplitudes or the noise level, and when $K \le N$ with signatures that are not nearly dependent. It is also a good first stage for cancellation methods. At low SNR, or when two signatures are highly correlated, the MMSE detector has a lower error rate.

## Pitfalls

- **More users than chips.** With $K > N$, $R$ is singular and the decorrelator does not exist. Use the MMSE detector, which is defined for any $K$ when $\sigma > 0$.
- **Nearly dependent signatures.** When $R$ is ill conditioned, $(R^{-1})_{kk}$ is large and the noise swamps the signal. Check the [condition number](/condition-number/) of $R$ or the penalties $1/(R^{-1})_{kk}$.
- **Using it for the strongest user.** A strong user loses energy to the noise penalty and gains little from the removed interference. The table above shows a case where its matched filter is slightly better.
- **Signature mismatch.** The exact cancellation relies on the exact $R$. Errors in the chip timing or the channel change $R$ and leave residual interference, which is again near-far sensitive.
- **Forming $R^{-1}$ in each interval.** Solve the system once per set of signatures and reuse the factor; do not invert $R$ for every symbol.

## Implementations

## History

Earlier work on code division multiplexing had already used the inverse of the crosscorrelations to remove the interference between users. Lupas and Verdú gave the full analysis of the decorrelating detector for synchronous CDMA in 1989. They showed that its error probability does not depend on the energies of the other users, defined the near-far resistance of a detector, and proved that the decorrelator reaches the near-far resistance of the optimum detector at polynomial cost. A paper of 1990 extended the analysis to asynchronous users. The decorrelator became the baseline linear multiuser detector, and the MMSE detector followed it a few years later.

## References
