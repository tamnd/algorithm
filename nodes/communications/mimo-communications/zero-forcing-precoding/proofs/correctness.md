---
title: ZF precoding removes all interference with the least power, water-filling gives the best sum rate among zero-interference linear precoders, and the SNR gain is Gamma with shape M - K + 1
proves: [correctness]
status: full
---

The model is the multiuser downlink $y_k = h_k^H x + w_k$, $k = 1, \ldots, K$, with $w_k \sim \mathcal{CN}(0, N_0)$, the channel matrix $H = [h_1, \ldots, h_K]^H \in \mathbb{C}^{K \times M}$ of full row rank (so $K \le M$), and $x = W s$ with $E[s s^H] = I_K$ and the power $\mathrm{tr}(W^H W) \le P$. Let $G = H H^H$, $B = H^H G^{-1}$ (lines L1 and L2), $b_k$ column $k$ of $B$ and $c_k = [G^{-1}]_{kk}$.

**Lemma 1.** $G$ is Hermitian positive definite, $H B = I_K$, and $c_k = \|b_k\|^2$.

*Proof.* For $u \ne 0$, $u^H G u = \|H^H u\|^2 > 0$, because the rows of $H$ are independent. So $G$ is invertible, $H B = G G^{-1} = I$, and $B^H B = G^{-1} H H^H G^{-1} = G^{-1}$, whose diagonal entry $k$ is $\|b_k\|^2$. $\square$

**Theorem 1 (no interference).** With $w_k = \sqrt{q_k / c_k}\, b_k$ (line L5), user $k$ receives $y_k = \sqrt{q_k / c_k}\, s_k + w_k$. It sees no interference, its SNR is $q_k / (c_k N_0)$, and the total power is $\sum_k q_k$.

*Proof.* By Lemma 1, $h_k^H b_j = [H B]_{kj} = \delta_{kj}$, so $h_k^H x = \sum_j \sqrt{q_j / c_j}\, h_k^H b_j s_j = \sqrt{q_k / c_k}\, s_k$. The power is $\sum_k (q_k / c_k) \|b_k\|^2 = \sum_k q_k$. $\square$

**Theorem 2 (least power).** Every $w \in \mathbb{C}^M$ with $h_k^H w = a$ and $h_j^H w = 0$ for $j \ne k$ has the form $w = a b_k + n$ with $H n = 0$, and $\|w\|^2 = |a|^2 c_k + \|n\|^2 \ge |a|^2 c_k$. So $b_k$ is the shortest beam that gives user $k$ the amplitude 1 and the other users nothing.

*Proof.* $H w = a e_k = H (a b_k)$, so $n = w - a b_k$ lies in the null space of $H$. The vector $b_k = H^H (G^{-1} e_k)$ lies in the range of $H^H$, and that range is orthogonal to the null space of $H$: for $H n = 0$, $(H^H u)^H n = u^H H n = 0$. Pythagoras gives the norm. $\square$

**Lemma 2 (water-filling).** For gains $g_k > 0$, the powers $q_k = (\mu - 1/g_k)^+$ with $\sum_k q_k = P$ are the unique maximizer of $\sum_k \log_2(1 + g_k q_k)$ over $q \ge 0$, $\sum_k q_k \le P$. The function `water_fill` computes them.

*Proof.* This is the water-filling result; the KKT argument and the proof that the drop loop finds the right water level are on the page [water-filling power allocation](/water-filling-power-allocation/) and in the proof of [SVD precoding](/svd-precoding/), Lemma 1. The loop here tests the same condition $\mu_k > 1/g_k$ in the same order. The objective grows with each $q_k$, so the optimum uses the whole budget. $\square$

**Theorem 3 (best zero-interference linear precoder).** Among all $W$ with $h_k^H w_j = 0$ for $j \ne k$ and $\mathrm{tr}(W^H W) \le P$, ZF with water-filling over the gains $g_k = 1/(c_k N_0)$ (line L4) has the largest sum rate $\sum_k \log_2(1 + \mathrm{SNR}_k)$.

*Proof.* By Theorem 2, column $k$ of such a $W$ is $a_k b_k + n_k$ with $H n_k = 0$, so user $k$ has the SNR $|a_k|^2 / N_0$ and the power is at least $\sum_k |a_k|^2 c_k$. Put $q_k = |a_k|^2 c_k$. Then $\sum_k q_k \le P$ and the SNR of user $k$ is $q_k / (c_k N_0) = g_k q_k$. By Lemma 2, the sum rate is at most the water-filling value, and Theorem 1 shows that ZF with these powers reaches it. $\square$

The equal power rule $q_k = P/K$ and the channel inversion rule $q_k = P c_k / \sum_j c_j$, which gives every user the SNR $P / (N_0\, \mathrm{tr}(G^{-1}))$, also meet the power constraint by Theorem 1, but they do not maximize the sum rate in general.

**Lemma 3 (geometry of the noise gain).** Let $\Pi_k$ be the orthogonal projection onto the orthogonal complement of the span of $h_j$, $j \ne k$. Then $1 / c_k = \|\Pi_k h_k\|^2$.

*Proof.* Order the users so that $k$ is the last one, and write $H^H = [A\ h_k]$ with $A$ the matrix of the other channel vectors. Then $G = \begin{pmatrix} A^H A & A^H h_k \\ h_k^H A & h_k^H h_k \end{pmatrix}$, and the block inverse with the [Schur complement](/schur-complement/) of $A^H A$ gives $c_k = \bigl(h_k^H h_k - h_k^H A (A^H A)^{-1} A^H h_k\bigr)^{-1} = (h_k^H \Pi_k h_k)^{-1}$, with $\Pi_k = I - A (A^H A)^{-1} A^H$. This $\Pi_k$ is Hermitian and idempotent, so $h_k^H \Pi_k h_k = \|\Pi_k h_k\|^2$. $\square$

**Theorem 4 (SNR gain in Rayleigh fading).** If the entries of $H$ are i.i.d. $\mathcal{CN}(0, 1)$, then $1 / c_k$ has the Gamma distribution with shape $M - K + 1$ and scale 1. So with equal power, user $k$ has the SNR $(P / (K N_0)) \cdot \Gamma(M - K + 1, 1)$ and the diversity order $M - K + 1$.

*Proof.* Condition on $h_j$, $j \ne k$. With probability 1 they span a subspace of dimension $K - 1$, so $\Pi_k$ projects onto a fixed subspace of dimension $d = M - K + 1$. With an orthonormal basis $u_1, \ldots, u_d$ of that subspace, $\|\Pi_k h_k\|^2 = \sum_i |u_i^H h_k|^2$. The vector $h_k$ is independent of the others and its law is invariant under unitary maps, so the $u_i^H h_k$ are i.i.d. $\mathcal{CN}(0, 1)$, and the sum is Gamma with shape $d$. This law does not depend on the conditioning. Lemma 3 finishes the proof. $\square$

For $K = M$ the shape is 1, and $E[c_k] = E[1/\Gamma(1, 1)]$ is infinite. This is why channel inversion with $K = M$ has a poor average SNR.

The tests check Theorem 1 by $H W$ against a diagonal matrix within $10^{-9}$ and the power within $10^{-9}$ for all three power rules, Lemma 1 by $c_k$ against $[G^{-1}]_{kk}$, Theorem 2 with random null space vectors, Lemma 2 by its KKT conditions, Theorem 3 by a grid over the power splits of 2 and 3 users, Theorem 4 by the sample mean and variance of $1/c_k$, and the example values 2.853, 2.807 and 2.560 of the page.
