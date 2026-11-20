---
tag: E77HBP
kind: algorithm
slug: regularized-zero-forcing-precoding
name: Regularized zero-forcing precoding
aliases:
- RZF precoding
- MMSE precoding
area: communications/mimo-communications
level: advanced
summary: Adds a regularization term to the channel inversion, which trades residual interference for less noise enhancement.
model: real-ram
complexity:
  vars: {M: the number of base station antennas, K: the number of single-antenna users}
  time: {worst: "O(K^2 M + K^3)"}
  space: {extra: O(M K)}
properties: {deterministic: true, linear: true, needs_channel_at_transmitter: true, needs_noise_level: true, zero_interference: false, minimizes_sum_mse: true}
history:
  year: 2005
  people: [Christian B. Peel, Bertrand M. Hochwald, A. Lee Swindlehurst]
  note: "Peel, Hochwald and Swindlehurst proposed the regularized channel inverse with the parameter K N0 / P in 2005, and Joham, Utschick and Nossek derived the same filter as the transmit Wiener filter in the same year."
prereqs: [zero-forcing-precoding, tikhonov-regularization]
see_also: [zero-forcing-precoding, maximum-ratio-transmission, vector-perturbation-precoding, mmse-mimo-detector, mmse-linear-equalizer, mmse-multiuser-detector, weighted-mmse-precoding, wiener-filter]
sources:
  - paper: doi:10.1109/TCOMM.2004.840638
    title: "Christian B. Peel, Bertrand M. Hochwald and A. Lee Swindlehurst, A vector-perturbation technique for near-capacity multiantenna multiuser communication, Part I: channel inversion and regularization, IEEE Transactions on Communications 53(1), 195-202, 2005"
    locator: the regularized inverse H^H (H H^H + alpha I)^(-1), the choice alpha = K / rho and its sum rate compared with channel inversion
  - paper: doi:10.1109/TSP.2005.850331
    title: "Michael Joham, Wolfgang Utschick and Josef A. Nossek, Linear transmit processing in MIMO communications systems, IEEE Transactions on Signal Processing 53(8), 2700-2712, 2005"
    locator: the transmit Wiener filter, which minimizes the MSE under a total power constraint with a common receive gain
  - paper: doi:10.1109/TCOMM.2004.841997
    title: "Bertrand M. Hochwald, Christian B. Peel and A. Lee Swindlehurst, A vector-perturbation technique for near-capacity multiantenna multiuser communication, Part II: perturbation, IEEE Transactions on Communications 53(3), 537-544, 2005"
    locator: the regularized form of vector perturbation, which applies the same inverse after the perturbation
---

Regularized zero-forcing (RZF) precoding is the linear multiuser precoder $W = \beta H^H (H H^H + \alpha I)^{-1}$ with $\alpha = K N_0 / P$ and a scalar $\beta$ that sets the transmit power to $P$. It sits between the two simple linear precoders. With $\alpha \to 0$ it is [zero-forcing precoding](/zero-forcing-precoding/), which removes all interference but can need much power when the channel matrix is badly conditioned. With $\alpha \to \infty$ it sends each user a beam along its own channel, as [maximum ratio transmission](/maximum-ratio-transmission/) does, and ignores interference. The choice $\alpha = K N_0 / P$ minimizes the sum mean squared error at the users, so RZF is the transmit form of the MMSE filter. The same regularized inverse $(\cdot + \text{noise} \cdot I)^{-1}$ appears at the receiver in the [MMSE linear equalizer](/mmse-linear-equalizer/), the [MMSE MIMO detector](/mmse-mimo-detector/) and the [MMSE multiuser detector](/mmse-multiuser-detector/); here it is applied before the channel, and the regularization is $K N_0 / P$ because the noise is at the receivers while the power limit is at the transmitter. [Vector perturbation precoding](/vector-perturbation-precoding/) adds an integer offset to the data before the same inverse, and [weighted MMSE precoding](/weighted-mmse-precoding/) tunes the beams to a weighted sum rate instead of the plain sum MSE.

## In plain words

A base station sends to several users at once. One simple method aims a beam at each user and ignores the others. Another method cancels every leak between users completely, but it may spend a lot of power to do this when two users are in similar directions. Regularized zero forcing takes a middle path. It cancels most of the leaks but stops when the cost in power gets too high. How far it goes depends on the noise: with much noise it cares more about signal strength, and with little noise it cares more about canceling the leaks. The result is a smaller total error at the users than either simple method.

## The problem

User $k$ receives $y_k = h_k^H x + w_k$, with $H = [h_1, \ldots, h_K]^H \in \mathbb{C}^{K \times M}$ known at the base station, $w_k \sim \mathcal{CN}(0, N_0)$, $x = W s$, $E[s s^H] = I_K$ and the power $\mathrm{tr}(W^H W) = P$. Each user scales its sample by the same real factor $1/\beta$. The goal is the linear precoder that minimizes the sum MSE $E\|s - \beta^{-1} y\|^2$, as a cheap and robust stand-in for the sum rate. Unlike zero forcing, RZF also works when $K = M$ with a badly conditioned $H$, and even when $K > M$, because $H H^H + \alpha I$ is always invertible.

## The algorithm

```pseudo id=main
RZF-PRECODE(H, P, N0)
L1  α ← K N0 / P                                ▷ the regularization
L2  A ← H Hᴴ                                    ▷ K × K
L3  A ← A + α I
L4  F ← Hᴴ A⁻¹                                  ▷ solve A X = H, F = Xᴴ
L5  β ← √(P / ‖F‖²_F)                            ▷ meet the power exactly
L6  return W = β F
```

Line L4 needs one factorization of a $K \times K$ Hermitian positive definite matrix, for example a [Cholesky decomposition](/cholesky-decomposition/), and $M$ solves. By the push-through identity, $H^H (H H^H + \alpha I)^{-1} = (H^H H + \alpha I)^{-1} H^H$, so a base station with $M < K$ can invert the smaller $M \times M$ matrix instead. Line L5 does not change the directions of the beams, only the common power.

## Example

Take the same channel as on the zero-forcing page: $M = K = 2$, $P = 10$, $N_0 = 1$ and

$$H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}, \qquad H H^H = \begin{pmatrix} 5 & 3 \\ 3 & 2 \end{pmatrix}.$$

Line L1 gives $\alpha = 2 \cdot 1 / 10 = 0.2$. Then $A = \begin{pmatrix} 5.2 & 3 \\ 3 & 2.2 \end{pmatrix}$ with $\det A = 2.44$, and

$$F = H^H A^{-1} = \frac{1}{2.44} \begin{pmatrix} 1.4 & -0.8 \\ -0.8 & 2.2 \end{pmatrix}, \qquad H F = \frac{1}{2.44} \begin{pmatrix} 2.0 & 0.6 \\ 0.6 & 1.4 \end{pmatrix}.$$

So each user still hears some interference ($0.6 / 2.44$ against the signals $2.0 / 2.44$ and $1.4 / 2.44$). Line L5 gives $\|F\|_F^2 = 8.08 / 2.44^2 = 1.357$ and $\beta = 2.714$. The SINRs are 3.425 and 1.678, and the sum rate is 3.567 bits per channel use. The table compares RZF with the other linear precoders on this channel; the zero-forcing rows are from the [zero-forcing page](/zero-forcing-precoding/):

| precoder | $P = 1$ | $P = 10$ | $P = 100$ |
|---|---|---|---|
| RZF, $\alpha = K N_0 / P$ | 1.737 | 3.567 | 8.066 |
| zero forcing, channel inversion | 0.385 | 2.560 | 7.868 |
| zero forcing, water-filling | 0.585 | 2.853 | |
| maximum ratio transmission, equal power | 1.433 | 2.045 | |

At $P = 10$ the sum MSE of RZF is $\alpha\, \mathrm{tr}(A^{-1}) = 0.2 \cdot 7.4 / 2.44 = 0.607$, against 1.4 for the plain inverse. At high power RZF and zero forcing come close, because $\alpha$ goes to 0.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem 1 shows that the scaling of line L5 meets the power constraint exactly. Lemma 2 writes the sum MSE of any scaled precoder as $\|I - H F\|_F^2 + (K N_0 / P) \|F\|_F^2$, which does not depend on the scale of $F$. Theorem 2 shows that this is a [Tikhonov regularization](/tikhonov-regularization/) problem whose unique minimizer is the $F$ of line L4, with the minimum $\alpha\, \mathrm{tr}((H H^H + \alpha I)^{-1})$; this is the transmit Wiener filter of Joham, Utschick and Nossek. Theorem 3 shows that the limits $\alpha \to 0$ and $\alpha \to \infty$ give zero forcing with channel inversion and matched beams $h_k$.

## Complexity

Lines L2 and L3 cost $K^2 M$ multiplications. Line L4 costs $O(K^3)$ for the factorization and $O(K^2 M)$ for the solves, or $O(M^3 + M^2 K)$ with the push-through form. Line L5 costs $O(M K)$. The total is $O(K^2 M + K^3)$ per channel realization, with $O(M K)$ extra space, the same as zero forcing.

## Properties

- **Minimum sum MSE.** Among linear precoders with power $P$ and a common receive scale, RZF has the smallest sum MSE (theorem).
- **Always defined.** $H H^H + \alpha I$ is invertible for every $H$ when $\alpha > 0$, including $K > M$.
- **Between two extremes.** $\alpha \to 0$ gives zero forcing, and $\alpha \to \infty$ gives beams along each user's channel (theorem).
- **Needs the noise level.** Unlike zero forcing, RZF uses $N_0 / P$. A wrong value moves it toward one of the two extremes.
- **Residual interference.** $H W$ is not diagonal. If $\alpha$ stays fixed while $P$ grows, the SINR of each user stops at a finite value. With $\alpha = K N_0 / P$, $\alpha$ falls with $P$, and for $K \le M$ and a channel of full row rank the sum rate grows like $K \log_2 P$.
- **Large $K = M$.** Peel, Hochwald and Swindlehurst showed that the sum rate of RZF grows linearly with $K = M$, while plain channel inversion does not.

## Variants and improvements

- **Per-user regularization.** With unequal path losses or noise levels, use $H^H (H H^H + \mathrm{diag}(\alpha_k))^{-1}$ or the general MMSE form with a weight per user.
- **Imperfect channel knowledge.** Add the estimation error variance to $\alpha$. The large-system analysis of RZF gives the best $\alpha$ for a given error level.
- **Regularized vector perturbation.** Perturb the data by an integer vector before the regularized inverse; see [vector perturbation precoding](/vector-perturbation-precoding/).
- **Weighted MMSE.** Replace the sum MSE by a weighted sum of MSEs with weights updated from the rates; this gives a local optimum of the weighted sum rate; see [weighted MMSE precoding](/weighted-mmse-precoding/).
- **Multi-antenna users.** Regularized block diagonalization applies the same idea to [block diagonalization](/block-diagonalization/).

## When to use it

Use RZF as the default linear precoder in a multiuser downlink when the base station knows the channel and the noise level, especially when $K$ is close to $M$ or when the SNR is low or moderate. It costs the same as zero forcing and is never worse than it in sum MSE. At very high SNR with $K \ll M$, zero forcing and RZF are nearly the same. When the sum rate itself must be maximized with user weights, start from RZF and refine it with [weighted MMSE precoding](/weighted-mmse-precoding/).

## Pitfalls

- **The name "MMSE precoding".** It is used for RZF, for the transmit Wiener filter with a common scale (the same thing), and for other designs with per-user receive gains or with power constraints per antenna. Check the cost function before comparing results.
- **Not the sum rate optimum.** $\alpha = K N_0 / P$ minimizes the sum MSE, not the sum rate. On the example channel at $P = 1$, $\alpha = 3$ gives a sum rate of 1.741, a little more than the 1.737 of $\alpha = 2$.
- **Wrong regularization.** Using $N_0$ instead of $K N_0 / P$, or the SNR in dB, gives a precoder that is close to one of the extremes.
- **Normalization.** Normalizing each column of $F$ separately changes the precoder. Line L5 uses one common scale.
- **Stale channel.** As for zero forcing, an old channel estimate leaves interference that grows with $P$.

## Implementations

## History

Linear transmit filters that minimize an MSE were studied for multiuser and MIMO systems in the early 2000s. Peel, Hochwald and Swindlehurst (2005) showed that plain channel inversion has a poor sum rate when the number of users equals the number of antennas, and proposed the regularized inverse with $\alpha = K / \rho$, which they found to maximize the SINR in a large system. In the same year Joham, Utschick and Nossek gave a unified treatment of linear transmit processing and derived the same filter as the transmit Wiener filter. Later work by many groups analyzed RZF with random matrix theory for large arrays and imperfect channel knowledge.

## References
