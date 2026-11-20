---
title: V-BLAST is exact without noise, its order maximizes the smallest post-detection SNR, and MMSE nulling with correct cancellation adds up to the capacity
proves: [correctness]
status: full
---

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$, columns $h_1, \ldots, h_n$, $x \in \mathcal{S}^n$ with $E|x_k|^2 = E_s$, and $w \sim \mathcal{CN}(0, N_0 I_m)$. For a set $K$ of streams and $k \in K$, let $H_K$ be the matrix of the columns in $K$, let $H_{K \setminus k}$ be the same matrix without column $k$, and let $P^K = (H_K^H H_K + a I)^{-1}$, with $a = 0$ (ZF, which needs $H$ of full column rank) or $a = N_0 / E_s > 0$ (MMSE). The entry of $P^K$ that belongs to stream $k$ is written $P^K_{kk}$.

All SNR statements below assume that the earlier decisions are right. Then, before the step that detects $k$ from the set $K$, line L7 has left $r = H_K x_K + w$.

**Theorem 1 (exact without noise).** With ZF nulling and $w = 0$, V-BLAST returns $x$.

*Proof.* By induction over the steps, the invariant is $r = H_K x_K$. At the start $K = \{1, \ldots, n\}$ and $r = y = H x$. At a step with the set $K$, the nulling matrix is $W = P^K H_K^H = (H_K^H H_K)^{-1} H_K^H$, so $W H_K = I$ and $W r = x_K$. Row $k$ gives $z = x_k$, a point of $\mathcal{S}$, so line L6 returns $x_k$ at distance 0. Line L7 then gives $r = H_K x_K - h_k x_k = H_{K \setminus k} x_{K \setminus k}$, and line L8 gives the invariant for the new set. $\square$

**Lemma 2 (the SNR of one step).** Let $d(k, K)$ be the post-detection SNR (ZF) or the unbiased SINR (MMSE) of stream $k$ at the step with the set $K$. Then

$$d(k, K) = \frac{E_s}{N_0} \, \|\Pi_{K \setminus k}^{\perp} h_k\|^2 = \frac{E_s / N_0}{P^K_{kk}} \quad \text{(ZF)}, \qquad d(k, K) = h_k^H \left(H_{K \setminus k} H_{K \setminus k}^H + a I\right)^{-1} h_k = \frac{1}{a P^K_{kk}} - 1 \quad \text{(MMSE)},$$

where $\Pi_{K \setminus k}^{\perp}$ is the orthogonal projection onto the complement of the span of the columns in $K \setminus k$.

*Proof.* For ZF, the SNR $(E_s / N_0) / P^K_{kk}$ is Theorem 2 of the [ZF MIMO detector](/zero-forcing-mimo-detector/) applied to $H_K$, and $1 / P^K_{kk} = \|\Pi_{K \setminus k}^{\perp} h_k\|^2$ is Lemma 3 of the same page. For MMSE, write $r = h_k x_k + v$ with $v = H_{K \setminus k} x_{K \setminus k} + w$, whose covariance is $E_s H_{K \setminus k} H_{K \setminus k}^H + N_0 I = E_s (H_{K \setminus k} H_{K \setminus k}^H + a I)$. The largest SINR of a linear estimate of $x_k$ is $E_s h_k^H \mathrm{Cov}(v)^{-1} h_k$, which gives the first form, and the [MMSE MIMO detector](/mmse-mimo-detector/) reaches it with the unbiased SINR $1 / (a P^K_{kk}) - 1$ (its Theorem 3). $\square$

So for both kinds of nulling, $d(k, K)$ falls when $P^K_{kk}$ grows, and line L4 picks the stream with the largest $d(k, K)$ in $K$.

**Lemma 3 (fewer interferers never hurt).** If $k \in K' \subseteq K$, then $d(k, K') \ge d(k, K)$.

*Proof.* ZF: the span of the columns in $K' \setminus k$ is a subspace of the span of the columns in $K \setminus k$. The distance from $h_k$ to a subspace is at least the distance to a larger subspace, so $\|\Pi_{K' \setminus k}^{\perp} h_k\| \ge \|\Pi_{K \setminus k}^{\perp} h_k\|$.

MMSE: let $A = H_{K \setminus k} H_{K \setminus k}^H + a I$ and $A' = H_{K' \setminus k} H_{K' \setminus k}^H + a I$. Then $A - A' = \sum_{j \in K \setminus K'} h_j h_j^H$ is positive semidefinite, and $A' \succeq a I$ is positive definite. For positive definite matrices, $A \succeq A'$ implies $A'^{-1} \succeq A^{-1}$. So $h_k^H A'^{-1} h_k \ge h_k^H A^{-1} h_k$. $\square$

**Theorem 4 (the order is optimal in the max-min sense).** For an order $\pi = (\pi_1, \ldots, \pi_n)$ of the streams, let $K_t(\pi) = \{\pi_t, \ldots, \pi_n\}$ and $v(\pi) = \min_t d(\pi_t, K_t(\pi))$, the smallest post-detection SNR or SINR along the order. Let $g$ be the order chosen by line L4, with any rule for ties. Then $v(g) \ge v(\pi)$ for every order $\pi$.

*Proof.* By induction on $n$. For $n = 1$ there is only one order. Let $n \ge 2$, let $\pi$ be any order, let $N = \{1, \ldots, n\}$, and let $k_1 = g_1$, a stream with the largest $d(k, N)$. Suppose $k_1 = \pi_j$.

Exchange step. Let $\pi'$ be the order that puts $k_1$ first and keeps the other streams in the order of $\pi$. Compare the terms of $v(\pi')$ with those of $v(\pi)$:

- The stream $k_1$ gets $d(k_1, N) \ge d(\pi_1, N) \ge v(\pi)$, by the choice of $k_1$ and because the first term of $\pi$ is one of the terms of the minimum.
- A stream $\pi_t$ with $t < j$ is detected from the set $K_t(\pi) \setminus \{k_1\}$ in $\pi'$, a subset of $K_t(\pi)$, so by Lemma 3 its term does not fall.
- A stream $\pi_t$ with $t > j$ has the same set $K_t(\pi)$ in both orders, so its term is the same.

So $v(\pi') \ge v(\pi)$.

Reduction. After $k_1$, both $g$ and $\pi'$ detect the streams $N' = N \setminus \{k_1\}$, and the terms depend only on the sets of remaining streams. This is the same problem for the channel $H_{N'}$ with $n - 1$ columns, and the remaining part of $g$ is the order that line L4 chooses for it. By the induction hypothesis, the smallest term of the rest of $g$ is at least the smallest term of the rest of $\pi'$. So

$$v(g) = \min\left(d(k_1, N), v_{N'}(g)\right) \ge \min\left(d(k_1, N), v_{N'}(\pi')\right) = v(\pi') \ge v(\pi). \qquad \square$$

**Corollary 5 (no stream is worse than with linear detection).** In the order $g$, each stream $k$ has $d(k, K) \ge d(k, N)$, the SNR or SINR of the linear ZF or MMSE detector. With ZF nulling in i.i.d. $\mathcal{CN}(0, 1)$ fading, the first detected stream has an error probability that decays at least as fast as $\mathrm{SNR}^{-(m - n + 1)}$.

*Proof.* The first part is Lemma 3 with $K \subseteq N$. For the second part, the first stream has the SNR $\max_k d(k, N) \ge d(1, N)$. By Theorem 4 of the ZF page, $(N_0 / E_s) \, d(1, N)$ is a sum of $m - n + 1$ independent unit exponentials, so $P(d(1, N) < \epsilon) \le (\epsilon N_0 / E_s)^{m - n + 1}$. The same bound then holds for the maximum. Write $D = m - n + 1$ and $X = (N_0 / E_s) \max_k d(k, N)$, so $P(X < \epsilon) \le \epsilon^D$. The error probability of a slicer at SNR $s$ is at most $C e^{-c s}$ for constants $C, c > 0$ of the constellation. Averaged over the fading, with $\rho = E_s / N_0$,

$$E\left[C e^{-c \rho X}\right] = C \int_0^\infty P\left(X < \frac{u}{c \rho}\right) e^{-u} \, du \le C \int_0^\infty \left(\frac{u}{c \rho}\right)^D e^{-u} \, du = \frac{C \, D!}{(c \rho)^D}. \qquad \square$$

**Theorem 6 (MMSE-SIC adds up to the capacity).** With MMSE nulling and correct cancellation, for every order $\pi$,

$$\sum_{t = 1}^{n} \log_2\left(1 + d(\pi_t, K_t(\pi))\right) = \log_2 \det\left(I + \frac{E_s}{N_0} H^H H\right).$$

*Proof.* Let $K = K_t(\pi)$, $k = \pi_t$ and $D(K) = \det(H_K^H H_K + a I)$, with $D(\emptyset) = 1$. By the cofactor formula for the inverse, $P^K_{kk} = D(K \setminus k) / D(K)$, because the cofactor of the diagonal entry $k$ of $H_K^H H_K + a I$ is the determinant of the matrix without row and column $k$, which is $H_{K \setminus k}^H H_{K \setminus k} + a I$. By Lemma 2,

$$1 + d(k, K) = \frac{1}{a P^K_{kk}} = \frac{D(K)}{a \, D(K \setminus k)}.$$

The sets $K_1(\pi) = N \supset K_2(\pi) \supset \cdots \supset K_n(\pi) \supset \emptyset$ lose one stream at each step, so the product over $t$ telescopes:

$$\prod_{t = 1}^{n} \left(1 + d(\pi_t, K_t(\pi))\right) = \frac{D(N)}{a^n D(\emptyset)} = \det\left(\frac{H^H H}{a} + I\right).$$

Since $1 / a = E_s / N_0$, the base 2 logarithm gives the claim. $\square$

The right side is the capacity of the channel $H$ with equal power $E_s$ per transmit antenna and no channel knowledge at the transmitter. So if each stream carries a capacity-achieving code of rate $\log_2(1 + d(\pi_t, K_t(\pi)))$ and the receiver decodes each stream before it cancels it, the sum rate equals this capacity, which is the statement of Tse and Viswanath, Section 8.3.4. Theorem 6 holds for every order; the order of Theorem 4 matters for uncoded detection, where the weakest step limits the error rate.
