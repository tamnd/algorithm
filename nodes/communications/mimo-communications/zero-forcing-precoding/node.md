---
tag: 3A1WH4
kind: algorithm
slug: zero-forcing-precoding
name: Zero-forcing precoding
aliases:
- channel inversion precoding
- zero-forcing beamforming
area: communications/mimo-communications
level: core
summary: Precodes with the pseudoinverse of the multiuser channel so that each user receives no interference from the others.
model: real-ram
complexity:
  vars: {M: the number of base station antennas, K: the number of single-antenna users}
  time: {worst: "O(K^2 M + K^3)"}
  space: {extra: O(M K)}
properties: {deterministic: true, linear: true, needs_channel_at_transmitter: true, zero_interference: true, needs_noise_level: false, diversity_order_iid_rayleigh: "M - K + 1"}
history:
  year: 2003
  people: [Giuseppe Caire, Shlomo Shamai]
  note: "Caire and Shamai used zero-forcing beamforming in 2003 as the simple linear benchmark for the capacity of the MIMO broadcast channel. Spencer, Swindlehurst and Haardt and Peel, Hochwald and Swindlehurst studied channel inversion in 2004 and 2005."
prereqs: [pseudoinverse, maximum-ratio-transmission, water-filling-power-allocation]
see_also: [regularized-zero-forcing-precoding, block-diagonalization, vector-perturbation-precoding, dirty-paper-coding, zero-forcing-mimo-detector, decorrelating-detector, zero-forcing-equalizer, truncated-channel-inversion]
sources:
  - paper: doi:10.1109/TIT.2003.813523
    title: "Giuseppe Caire and Shlomo Shamai, On the achievable throughput of a multiantenna Gaussian broadcast channel, IEEE Transactions on Information Theory 49(7), 1691-1706, 2003"
    locator: the zero-forcing beamforming scheme and its comparison with the dirty paper coding rate
  - paper: doi:10.1109/TSP.2003.821107
    title: "Quentin H. Spencer, A. Lee Swindlehurst and Martin Haardt, Zero-forcing methods for downlink spatial multiplexing in multiuser MIMO channels, IEEE Transactions on Signal Processing 52(2), 461-471, 2004"
    locator: the channel inversion precoder for single-antenna users and the power allocation over the users
  - paper: doi:10.1109/TCOMM.2004.840638
    title: "Christian B. Peel, Bertrand M. Hochwald and A. Lee Swindlehurst, A vector-perturbation technique for near-capacity multiantenna multiuser communication, Part I: channel inversion and regularization, IEEE Transactions on Communications 53(1), 195-202, 2005"
    locator: the channel inversion precoder and its poor performance when the number of users equals the number of antennas
  - paper: doi:10.1109/JSAC.2005.862421
    title: "Taesang Yoo and Andrea Goldsmith, On the optimality of multiantenna broadcast scheduling using zero-forcing beamforming, IEEE Journal on Selected Areas in Communications 24(3), 528-541, 2006"
    locator: zero-forcing beamforming with semi-orthogonal user selection and its sum rate scaling with many users
  - paper: doi:10.1109/TSP.2008.924638
    title: "Ami Wiesel, Yonina C. Eldar and Shlomo Shamai, Zero-forcing precoding and generalized inverses, IEEE Transactions on Signal Processing 56(9), 4409-4418, 2008"
    locator: the optimality of the pseudoinverse under a total power constraint and the other generalized inverses under per-antenna constraints
---

Zero-forcing (ZF) precoding is the linear multiuser precoder that removes all interference between users. A base station with $M$ antennas serves $K \le M$ single-antenna users and sends $x = W s$, where the columns of $W$ are the columns of the [pseudoinverse](/pseudoinverse/) $H^H (H H^H)^{-1}$ of the channel matrix, scaled to give each user a power $q_k$. Then $H W$ is diagonal: each user hears only its own symbol and noise. The price is power. A beam that must be orthogonal to every other user's channel points away from its own user, and the loss is the factor $[(H H^H)^{-1}]_{kk}$. This page is the transmit side of the same inverse that the [ZF MIMO detector](/zero-forcing-mimo-detector/) applies at a receiver, that the [decorrelating detector](/decorrelating-detector/) applies to CDMA users and that the [ZF equalizer](/zero-forcing-equalizer/) applies to a convolution. Compared with the other precoders: [maximum ratio transmission](/maximum-ratio-transmission/) maximizes each beam gain and ignores interference, [regularized zero-forcing precoding](/regularized-zero-forcing-precoding/) adds $(K N_0 / P) I$ to the inverse and balances the two, [block diagonalization](/block-diagonalization/) is the extension to users with several antennas, [SVD precoding](/svd-precoding/) is the single-user method where the receiver can cooperate, and [dirty paper coding](/dirty-paper-coding/) is the nonlinear scheme that reaches the capacity region. The name "channel inversion" on this page means inverting the matrix channel; the scalar power rule of [truncated channel inversion](/truncated-channel-inversion/) is a different method.

## In plain words

A base station talks to several phones at the same time and on the same frequency. If it simply aims a beam at each phone, each phone also hears the beams meant for the others. Zero forcing aims each beam so that it is exactly silent at every other phone. Because the base station knows all the channels, it can solve for such beams with a set of linear equations. Each phone then hears only its own data and some noise. The cost is that a beam squeezed away from the other phones is weaker at its own phone. When two phones have similar channels, the beams lose a lot, so the base station must pick users whose channels are different.

## The problem

User $k$ receives $y_k = h_k^H x + w_k$ with $w_k \sim \mathcal{CN}(0, N_0)$. The matrix $H = [h_1, \ldots, h_K]^H \in \mathbb{C}^{K \times M}$ is known at the base station and has full row rank, so $K \le M$. The base station sends $x = W s$ with independent unit-power symbols $s_k$ and the power constraint $\mathrm{tr}(W^H W) \le P$, and $\rho = P / N_0$. The goal is a $W$ with $h_k^H w_j = 0$ for every $j \ne k$, and among these the one with the largest sum rate $\sum_k \log_2(1 + \mathrm{SNR}_k)$, or with equal SNRs for all users.

## The algorithm

```pseudo id=main
ZF-PRECODE(H, P, N0, rule)
L1  G ← H Hᴴ                                       ▷ K × K Gram matrix
L2  B ← Hᴴ G⁻¹                                     ▷ the pseudoinverse, H B = I
L3  c_k ← ‖b_k‖² = [G⁻¹]_kk for each user k          ▷ the noise gain of user k
L4  q ← WATER-FILL(1/(c₁ N0), ..., 1/(c_K N0); P)  ▷ or q_k = P/K, or q_k ∝ c_k
L5  w_k ← √(q_k / c_k) b_k for each user k
L6  return W = [w₁, ..., w_K]
```

Line L2 solves $G X = H$ for $X = G^{-1} H$ and takes $B = X^H$, which avoids an explicit inverse. Line L3 gives the gain: user $k$ receives $\sqrt{q_k / c_k}\, s_k$, so its SNR is $q_k / (c_k N_0)$. Line L4 picks one of three power rules. Water-filling gives the best sum rate of any zero-interference linear precoder. Equal power is simple and close to it at high SNR. Channel inversion, $q_k = P c_k / \sum_j c_j$, gives every user the same SNR $P / (N_0\, \mathrm{tr}(G^{-1}))$ and the same receive amplitude, so the receivers need no gain control.

## Example

Take $M = K = 2$, $P = 10$, $N_0 = 1$ and the real channel

$$H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}, \qquad G = H H^H = \begin{pmatrix} 5 & 3 \\ 3 & 2 \end{pmatrix}, \qquad G^{-1} = \begin{pmatrix} 2 & -3 \\ -3 & 5 \end{pmatrix}.$$

Since $H$ is square, $B = H^{-1} = \begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}$, and line L3 gives $c = (2, 5)$. The two channels $(2, 1)$ and $(1, 1)$ make an angle $\theta$ with $\cos^2 \theta = 9/10$, and each user keeps only the part $\sin^2 \theta = 0.1$ of its channel gain that is orthogonal to the other user. So $1/c_k = 0.1\, \|h_k\|^2$, which gives the gains $1/c = (0.5, 0.2)$; user 2 pays more only because its channel is weaker. Water-filling with $P = 10$ gives the level $\mu = (10 + 2 + 5)/2 = 8.5$, above both $c_k$, so $q = (6.5, 3.5)$. The table compares the three rules and maximum ratio transmission with equal power:

| precoder | SINRs | sum rate (bits per channel use) |
|---|---|---|
| ZF, water-filling, $q = (6.5, 3.5)$ | 3.25, 0.70 | 2.853 |
| ZF, equal power, $q = (5, 5)$ | 2.50, 1.00 | 2.807 |
| ZF, channel inversion | 1.43, 1.43 | 2.560 |
| maximum ratio transmission, equal power | 1.06, 1.00 | 2.045 |

At $P = 10$ the interference makes maximum ratio transmission the worst choice. At $P = 1$ the order is reversed: ZF with water-filling gives 0.585 and maximum ratio transmission gives 1.433, because at low SNR the noise dominates and the beam gain matters more than the interference.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Lemma 1 and Theorem 1 show that $H B = I$, so $H W$ is diagonal, each user gets the SNR $q_k / (c_k N_0)$, and the power is $\sum_k q_k = P$. Theorem 2 shows that $b_k$ is the shortest vector that reaches user $k$ with amplitude 1 and is silent at the others, because every other such vector adds a component in the null space of $H$. Theorem 3 combines this with water-filling: no linear precoder with zero interference and power $P$ has a larger sum rate than ZF with the powers of line L4. Lemma 3 and Theorem 4 show that $1 / c_k$ is the squared distance from $h_k$ to the span of the other channels, which has the Gamma distribution with shape $M - K + 1$ in i.i.d. Rayleigh fading.

## Complexity

Line L1 costs $K^2 M$ multiplications. Line L2 costs $O(K^3)$ for the factorization of $G$ and $O(K^2 M)$ for the $M$ right-hand sides. Lines L3 to L5 cost $O(M K + K \log K)$. The total is $O(K^2 M + K^3)$ per channel realization, with $O(M K)$ extra space. The precoding itself, $x = W s$, costs $M K$ multiplications per symbol vector.

## Properties

- **No interference.** $h_k^H w_j = 0$ for $j \ne k$, so the SINR of each user is its SNR (theorem).
- **Least power for zero interference.** Every zero-interference beam for user $k$ costs at least $c_k$ per unit received power, and ZF reaches this bound (theorem).
- **Noise level not needed for the beams.** The directions $b_k$ use only $H$. Only the water-filling powers use $N_0$.
- **Diversity.** In i.i.d. Rayleigh fading with equal power, each user has the SNR gain $\Gamma(M - K + 1, 1)$ and the diversity order $M - K + 1$ (theorem).
- **High SNR optimality.** The sum rate grows as $K \log_2 \rho$, the same slope as dirty paper coding. The gap to the capacity region stays bounded at high SNR for a fixed channel.
- **Low SNR loss.** At low SNR the beam gain matters more than interference, and maximum ratio transmission is better.

## Variants and improvements

- **Regularized ZF.** Use $H^H (H H^H + \alpha I)^{-1}$ with $\alpha = K N_0 / P$; see [regularized zero-forcing precoding](/regularized-zero-forcing-precoding/). It is never worse than ZF in the sum MSE sense and is much better when $K = M$.
- **User selection.** Serve a subset of users with nearly orthogonal channels. Yoo and Goldsmith (2006) showed that ZF with semi-orthogonal user selection reaches the same sum rate growth as dirty paper coding when the number of candidate users grows.
- **Per-antenna power constraints.** Under a power limit on each antenna, the pseudoinverse is no longer optimal, and other generalized inverses of $H$ do better (Wiesel, Eldar and Shamai, 2008).
- **Multi-antenna users.** Replace the null space of single vectors by the null space of whole channel matrices; see [block diagonalization](/block-diagonalization/).
- **Nonlinear.** Precode with successive interference presubtraction; see [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/) and [vector perturbation precoding](/vector-perturbation-precoding/), which perturbs the data before the same inverse.
- **Massive MIMO.** With $M \gg K$, $H H^H$ is close to $M I$ by [favorable propagation](/favorable-propagation/), and ZF approaches maximum ratio transmission in direction but keeps zero interference.

## When to use it

Use ZF in a multiuser downlink at moderate and high SNR when the base station has accurate channel estimates and $M$ is larger than $K$, for example in time division duplex [massive MIMO](/massive-mimo/). It is the standard linear benchmark for multiuser precoding. With $K = M$, or with users whose channels are nearly parallel, use regularized ZF or user selection instead. At low SNR, or when the channel estimates are poor, maximum ratio transmission is often better. When the base station cannot invert a $K \times K$ matrix fast enough, maximum ratio transmission avoids the inverse.

## Pitfalls

- **$K = M$ in Rayleigh fading.** The SNR gain $1/c_k$ is a single exponential, and $E[c_k]$ is infinite. Channel inversion with a fixed power then has a very low average SNR.
- **Channel estimation errors.** ZF sends nulls toward the other users. With an estimate $\hat H \ne H$, the nulls are in the wrong place, and the residual interference grows with $P$, so the SINR saturates at high SNR.
- **Wrong scaling.** Normalizing each column $b_k$ to unit norm before the power rule changes the gains. Keep $c_k = \|b_k\|^2$ and scale with $\sqrt{q_k / c_k}$, or the SNR formula is wrong.
- **Rank loss.** If two users have parallel channels, $G$ is singular and ZF does not exist. Select users or regularize.
- **Two meanings of "channel inversion".** In the precoding literature it means the pseudoinverse of $H$. In link adaptation it means a power rule that inverts a scalar fading gain. Do not confuse the two.

## Implementations

## History

Linear transmit processing that nulls interference toward other receivers is an old idea in array processing. For the multiuser MIMO downlink, Caire and Shamai (2003) used zero-forcing beamforming as a simple scheme and compared its throughput with the dirty paper coding rate. Spencer, Swindlehurst and Haardt (2004) treated channel inversion and its block form for users with several antennas, and Peel, Hochwald and Swindlehurst (2005) showed that plain channel inversion performs poorly when the number of users equals the number of antennas, which led them to regularization and vector perturbation. Yoo and Goldsmith (2006) showed that ZF with user selection keeps the sum rate growth of the optimal scheme when there are many users, and Wiesel, Eldar and Shamai (2008) clarified when the pseudoinverse is the optimal ZF matrix.

## References
