---
tag: VCA1WD
kind: algorithm
slug: block-diagonalization
name: Block diagonalization precoding
aliases:
- BD precoding
area: communications/mimo-communications
level: advanced
summary: Precodes each multi-antenna user in the null space of the other users' channels, making the channel block diagonal.
model: real-ram
complexity:
  vars: {M: the number of base station antennas, K: the number of users, N: the total number of user antennas}
  time: {worst: O(K N M^2)}
  space: {extra: O(M^2 + M N)}
properties: {deterministic: true, linear: true, needs_channel_at_transmitter: true, zero_interference: true, best_zero_interference_sum_rate: true}
history:
  year: 2004
  people: [Quentin H. Spencer, A. Lee Swindlehurst, Martin Haardt, Lai-U Choi, Ross D. Murch]
  note: "Spencer, Swindlehurst and Haardt published block diagonalization in 2004, and Choi and Murch described the same null space decomposition in the same year."
prereqs: [zero-forcing-precoding, svd-precoding, singular-value-decomposition]
see_also: [zero-forcing-precoding, regularized-zero-forcing-precoding, dirty-paper-coding, weighted-mmse-precoding, water-filling-power-allocation, mimo-capacity, spatial-multiplexing]
sources:
  - paper: doi:10.1109/TSP.2003.821107
    title: "Quentin H. Spencer, A. Lee Swindlehurst and Martin Haardt, Zero-forcing methods for downlink spatial multiplexing in multiuser MIMO channels, IEEE Transactions on Signal Processing 52(2), 461-471, 2004"
    locator: block diagonalization with the null space of the other users, the power allocation by water-filling, the antenna condition, and successive optimization
  - paper: doi:10.1109/TWC.2003.821148
    title: "Lai-U Choi and Ross D. Murch, A transmit preprocessing technique for multiuser MIMO systems using a decomposition approach, IEEE Transactions on Wireless Communications 3(1), 20-24, 2004"
    locator: the decomposition of the multiuser channel into parallel single-user channels by null space precoding
---

Block diagonalization (BD) precoding serves several users that each have more than one antenna. It puts the precoder of each user in the null space of the channels of all the other users, so that $H_j W_k = 0$ for $j \ne k$ and the overall channel $H W$ becomes block diagonal. Inside its own null space, each user then gets [SVD precoding](/svd-precoding/), and one water-filling over all users splits the power. BD is the multi-antenna form of [zero-forcing precoding](/zero-forcing-precoding/). Zero forcing removes the interference between every pair of receive antennas, even two antennas of the same user. BD removes only the interference between different users, and lets each user handle the rest itself. With one antenna per user the two are the same. Among all precoders with zero interference between users, BD has the largest sum rate.

## In plain words

A base station sends to several phones at once, and each phone has a few antennas. The base station wants no phone to hear the signals meant for the others. For each phone, it finds the directions that the other phones cannot hear at all, and sends that phone's signal only in those directions. After this, each phone sees a private link, as if it were alone. The base station then shapes each private link for the best rate, and gives more power to the strong links. Because the signals for different antennas of the same phone may mix, this wastes less power than canceling every leak between all antennas.

## The problem

User $k$ has $N_k$ antennas and receives $y_k = H_k x + w_k$, with $H_k \in \mathbb{C}^{N_k \times M}$ known at the base station and $w_k \sim \mathcal{CN}(0, N_0 I)$. The base station sends $x = \sum_k W_k d_k$ with unit-energy symbols $d_k$ and total power $\sum_k \|W_k\|_F^2 = P$. Let $\tilde H_k$ stack the channels of all users except $k$. The goal is to choose the $W_k$ with $\tilde H_k W_k = 0$ that maximize the sum rate $\sum_k \log_2 \det(I + H_k W_k W_k^H H_k^H / N_0)$. A solution exists only if $\mathrm{rank}(\tilde H_k) < M$ for every $k$; for generic channels this means that $M$ is larger than the number of antennas of all the other users together.

## The algorithm

```pseudo id=main
BD-PRECODE(H₁, ..., H_K, P, N0)
    for each user k:
L1      H̃_k ← the channels H_j of all users j ≠ k, stacked
L2      V⁽⁰⁾_k ← orthonormal basis of the null space of H̃_k   ▷ from the SVD of H̃_k
L3      U_k Σ_k V⁽¹⁾_kᴴ ← SVD of H_k V⁽⁰⁾_k
L4  g ← all values σ² / N0 of all users
L5  p ← WATER-FILL(g, P)                                    ▷ one water level for all streams
    for each user k:
L6      W_k ← V⁽⁰⁾_k V⁽¹⁾_k diag(√p_k)                       ▷ the first r_k columns
L7  return W₁, ..., W_K and the receive filters U₁ᴴ, ..., U_Kᴴ
```

Line L2 takes the right singular vectors of $\tilde H_k$ that belong to the zero singular values. Line L3 is the [singular value decomposition](/singular-value-decomposition/) of the effective single-user channel. Line L5 is [water-filling](/water-filling-power-allocation/) over the gains of all streams of all users together. User $k$ applies $U_k^H$ and sees parallel scalar channels.

## Example

Take $M = 3$, $P = 3$, $N_0 = 1$ and two users: user 1 has two antennas and user 2 has one.

$$H_1 = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}, \qquad H_2 = \begin{pmatrix} 1 & 1 & 1 \end{pmatrix}.$$

For user 1, $\tilde H_1 = H_2$, whose null space has the basis $(1, -1, 0)/\sqrt 2$ and $(1, 1, -2)/\sqrt 6$. Then

$$H_1 V^{(0)}_1 = \begin{pmatrix} 1/\sqrt 2 & 1/\sqrt 6 \\ -1/\sqrt 2 & 1/\sqrt 6 \end{pmatrix},$$

whose columns are orthogonal with norms 1 and $1/\sqrt 3$, so the gains are 1 and $1/3$. For user 2, $\tilde H_2 = H_1$, whose null space is spanned by $e_3 = (0, 0, 1)$, and $H_2 e_3 = 1$, so the gain is 1. Water-filling over the gains $(1, 1/3, 1)$ with $P = 3$ first tries all three streams, with the water level $(3 + 1 + 3 + 1)/3 = 8/3 < 3$, so the weak stream gets no power. With two streams the level is $(3 + 1 + 1)/2 = 2.5$, and the powers are 1.5, 0 and 1.5. The sum rate is $2 \log_2 2.5 = 2.644$ bits per channel use.

| precoder | $P = 3$ | $P = 10$ |
|---|---|---|
| BD | 2.644 | 5.381 |
| zero forcing with water-filling over the 3 antennas as 3 users | 2.245 | 4.966 |

Zero forcing over the three antennas has the gains $1/2$, $1/2$ and 1, because it also cancels the interference between the two antennas of user 1. BD does not, and it loses less power.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Lemma 1 shows that line L2 gives an orthonormal basis of the null space. Theorem 1 shows that $H_j W_k = 0$ for $j \ne k$, and Theorem 2 that the power is exactly $P$. Lemma 2 shows that each user sees parallel channels with the gains of line L3. Theorem 3 shows that BD maximizes the sum rate over all precoders with zero inter-user interference: every such precoder has the form $W_k = V^{(0)}_k X_k$, the sum rate is then a log det of a block diagonal channel, and the [MIMO capacity](/mimo-capacity/) result for that channel is reached by SVD and one water-filling. A corollary shows that with one antenna per user BD is zero forcing with water-filling.

## Complexity

Line L2 needs the SVD of a matrix with at most $N$ rows and $M$ columns, which costs $O(M N \min(M, N)) \subseteq O(N M^2)$, once for each of the $K$ users. Line L3 costs less, because $H_k V^{(0)}_k$ has only $N_k$ rows. Lines L4 and L5 cost $O(N \log N)$ for the sort in water-filling. The total is $O(K N M^2)$. The extra space is $O(M^2)$ for one null space basis at a time and $O(M N)$ for the precoders.

## Properties

- **Zero inter-user interference.** $H_j W_k = 0$ for $j \ne k$ (theorem).
- **Best with that constraint.** No precoder with zero inter-user interference has a larger sum rate (theorem).
- **Generalizes zero forcing.** With $N_k = 1$ for every user, BD is zero-forcing precoding with water-filling (corollary).
- **Antenna condition.** User $k$ has a null space of dimension $M - \mathrm{rank}(\tilde H_k)$; for generic channels BD needs $M > \sum_{j \ne k} N_j$ for every $k$, and full multiplexing needs $M \ge \sum_k N_k$.
- **Linear.** The precoder is a matrix, so the cost per symbol is $O(M N)$.
- **Noise enhancement.** Like zero forcing, BD loses power when the null spaces are small or nearly orthogonal to the user's own channel.

## Variants and improvements

- **Regularized BD.** Replace the exact null space by a regularized inverse, which allows a little interference and loses less power at low SNR, as [regularized zero-forcing precoding](/regularized-zero-forcing-precoding/) does for single-antenna users.
- **Successive optimization.** Spencer, Swindlehurst and Haardt also proposed to null the interference only toward users that are served earlier, which relaxes the antenna condition.
- **Per-user power or rate targets.** Replace the joint water-filling by a weighted water-filling or by fixed powers for each user.
- **User and stream selection.** When $\sum_k N_k > M$, serve a subset of users or fewer streams per user so that the null spaces exist.
- **Weighted MMSE.** Allow interference and optimize the weighted sum rate directly; see [weighted MMSE precoding](/weighted-mmse-precoding/).
- **Dirty paper coding.** The capacity of the broadcast channel needs nonlinear coding; see [dirty paper coding](/dirty-paper-coding/).

## When to use it

Use BD in a multiuser MIMO downlink when the users have several antennas, the base station has accurate channel knowledge, and it has more antennas than the users together. It is a good choice at high SNR, where removing interference matters most. When the users have one antenna each, it is the same as [zero-forcing precoding](/zero-forcing-precoding/). At low SNR, or when the antenna condition is close to its limit, regularized or weighted MMSE designs do better.

## Pitfalls

- **Rank threshold.** Line L2 decides which singular values are zero. With noisy channel estimates, a fixed relative threshold such as $10^{-10}$ times the largest singular value is needed; a wrong threshold gives a null space that is too large (with interference) or too small.
- **Too many user antennas.** If $\tilde H_k$ has full column rank, user $k$ cannot be served. Check the antenna condition before calling the algorithm.
- **The receivers must apply $U_k^H$.** Each user needs its own receive filter, so it must know its effective channel, for example from precoded pilots.
- **Stale channel.** An old estimate of $H_j$ leaves interference that grows with $P$, as for zero forcing.

## Implementations

## History

Spencer, Swindlehurst and Haardt (2004) studied zero-forcing methods for the multiuser MIMO downlink with multi-antenna users. They described block diagonalization with the null space of the other users, the power allocation, and the condition on the number of antennas, and they also proposed successive optimization. In the same year, Choi and Murch published a transmit preprocessing technique that decomposes the multiuser channel into parallel single-user channels by null space projection, which is the same idea. Later work added regularization, user selection and comparisons with the capacity of the broadcast channel.

## References
