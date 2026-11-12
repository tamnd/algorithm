---
title: The Kabsch algorithm returns a proper rotation of least RMSD
proves: [correctness]
status: full
---

We use the notation of the page. The input is $x_1, \ldots, x_N$ and $y_1, \ldots, y_N$ in $\mathbb{R}^3$ with $N \ge 1$. We write $E(R, t) = \sum_i |R x_i + t - y_i|^2$, $\bar x$ and $\bar y$ for the centroids, $a_i = x_i - \bar x$, $b_i = y_i - \bar y$, $G_A = \sum_i |a_i|^2$, $G_B = \sum_i |b_i|^2$ and $H = \sum_i a_i b_i^{\mathsf T}$. $SO(3)$ is the set of real $3 \times 3$ matrices $R$ with $R^{\mathsf T} R = I$ and $\det R = +1$.

**Claim.** KABSCH$(X, Y)$ returns $R \in SO(3)$ and $t$ with $E(R, t) = \min_{R' \in SO(3), t'} E(R', t')$, and the value $r$ of line L11 is $\sqrt{E(R, t)/N}$.

**Lemma 1 (translation).** For a fixed $R$, $E(R, t)$ is smallest exactly at $t = \bar y - R \bar x$, and then $E = G_A + G_B - 2 \operatorname{tr}(R H)$.

*Proof.* Write $R x_i + t - y_i = (R a_i - b_i) + c$ with $c = R\bar x + t - \bar y$. Because $\sum_i a_i = \sum_i b_i = 0$, the cross term $2 c \cdot \sum_i (R a_i - b_i)$ is 0. So $E = \sum_i |R a_i - b_i|^2 + N |c|^2$, which is smallest exactly when $c = 0$. Next, $|R a_i - b_i|^2 = |a_i|^2 + |b_i|^2 - 2 b_i^{\mathsf T} R a_i$, because $R$ keeps lengths. Finally $\sum_i b_i^{\mathsf T} R a_i = \sum_i \operatorname{tr}(R a_i b_i^{\mathsf T}) = \operatorname{tr}(R H)$. $\square$

So the problem is to maximize $\operatorname{tr}(RH)$ over $R \in SO(3)$.

**Lemma 2 (the maximum of the trace).** Let $H = U S V^{\mathsf T}$ with $U, V$ orthogonal and $S = \operatorname{diag}(s_1, s_2, s_3)$, $s_1 \ge s_2 \ge s_3 \ge 0$. Let $d = \det U \det V \in \{+1, -1\}$. Then $\max_{R \in SO(3)} \operatorname{tr}(RH) = s_1 + s_2 + d\, s_3$, and $R = V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$ attains it.

*Proof.* Let $W = V^{\mathsf T} R U$. The map $R \mapsto W$ is a bijection from $SO(3)$ onto the orthogonal matrices with $\det W = \det V \det U = d$, and $\operatorname{tr}(RH) = \operatorname{tr}(R U S V^{\mathsf T}) = \operatorname{tr}(V^{\mathsf T} R U S) = \sum_k W_{kk} s_k$.

Case $d = +1$. Each entry of an orthogonal matrix has absolute value at most 1, so $\sum_k W_{kk} s_k \le s_1 + s_2 + s_3$, with equality at $W = I$.

Case $d = -1$. Let $D = \operatorname{diag}(1, 1, -1)$ and $W' = W D$. Then $W' \in SO(3)$, and $\sum_k W_{kk} s_k = W'_{11} s_1 + W'_{22} s_2 - W'_{33} s_3$. By Euler's rotation theorem, $W'$ is a rotation by an angle $\theta$ about a unit axis $n$, so $W'_{kk} = \cos\theta + (1 - \cos\theta) n_k^2$ and $1 - W'_{kk} \ge 0$. Then

$$ (s_1 + s_2 - s_3) - \sum_k W_{kk} s_k = (1 - W'_{11}) s_1 + (1 - W'_{22}) s_2 - (1 - W'_{33}) s_3 \ge s_3 \bigl(1 - W'_{11} - W'_{22} + W'_{33}\bigr), $$

because $1 - W'_{11} \ge 0$, $1 - W'_{22} \ge 0$ and $s_1, s_2 \ge s_3$. With the formula for $W'_{kk}$ and $n_1^2 + n_2^2 + n_3^2 = 1$, the bracket is $(1 - \cos\theta)(1 + n_3^2 - n_1^2 - n_2^2) = 2 (1 - \cos\theta) n_3^2 \ge 0$. So $\sum_k W_{kk} s_k \le s_1 + s_2 - s_3$, with equality at $W' = I$, that is $W = D$.

In both cases the best $W$ is $\operatorname{diag}(1, 1, d)$, so $R = V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$. $\square$

**Lemma 3 (what lines L4 to L8 compute).** After line L8, $R = \sum_k v_k u_k^{\mathsf T}$ is in $SO(3)$ and $\operatorname{tr}(RH)$ is the maximum of Lemma 2.

*Proof.* $H^{\mathsf T} H$ is symmetric and positive semidefinite. Line L4 gives orthonormal eigenvectors $v_1, v_2, v_3$ with eigenvalues $s_1^2 \ge s_2^2 \ge s_3^2 \ge 0$, and line L5 makes $V = [v_1\, v_2\, v_3]$ proper, which keeps each $v_k$ an eigenvector. For all $j, k$, $(H v_j)^{\mathsf T}(H v_k) = v_j^{\mathsf T} H^{\mathsf T} H v_k = s_k^2 [j = k]$. So $|H v_k| = s_k$, and the vectors $H v_k$ are pairwise orthogonal.

Case $s_2 > 0$. Line L6 sets $u_k = H v_k / s_k$ for $k = 1, 2$, an orthonormal pair, and line L7 sets $u_3 = u_1 \times u_2$, so $U = [u_1\, u_2\, u_3]$ is in $SO(3)$. The vector $H v_3$ is orthogonal to $u_1$ and $u_2$, so $H v_3 = \sigma u_3$ with $|\sigma| = s_3$. Hence $H = H V V^{\mathsf T} = \sum_k (H v_k) v_k^{\mathsf T} = U \operatorname{diag}(s_1, s_2, \sigma) V^{\mathsf T}$. If $\sigma \ge 0$, this is a decomposition as in Lemma 2 with $d = +1$, and the optimal rotation is $V U^{\mathsf T}$. If $\sigma < 0$, then $H = U' \operatorname{diag}(s_1, s_2, s_3) V^{\mathsf T}$ with $U' = [u_1\, u_2\, {-u_3}]$, $\det U' = -1$, so $d = -1$ and the optimal rotation is $V \operatorname{diag}(1, 1, -1)\, U'^{\mathsf T} = V U^{\mathsf T}$. In both cases line L8 returns the optimal rotation.

Case $s_2 = 0 < s_1$. Then $H v_2 = H v_3 = 0$, so $H = s_1 u_1 v_1^{\mathsf T}$, and for each $R' \in SO(3)$, $\operatorname{tr}(R' H) = s_1 v_1^{\mathsf T} R' u_1 \le s_1$. The code picks any unit $u_2 \perp u_1$ and $u_3 = u_1 \times u_2$, so $R = V U^{\mathsf T}$ is in $SO(3)$ with $R u_1 = v_1$, and $\operatorname{tr}(RH) = s_1$, the maximum.

Case $s_1 = 0$. Then $H = 0$, each rotation gives $\operatorname{tr}(RH) = 0$, and the code returns $R = I$. $\square$

**Proof of the claim.** By Lemma 3, $R \in SO(3)$ maximizes $\operatorname{tr}(RH)$. By Lemma 1, $E(R', t')$ is at least $G_A + G_B - 2\operatorname{tr}(R' H) \ge G_A + G_B - 2 \operatorname{tr}(RH)$ for each $R' \in SO(3)$ and each $t'$. Line L9 sets $t = \bar y - R \bar x$, so by Lemma 1 again $E(R, t) = G_A + G_B - 2\operatorname{tr}(RH)$, which is the value $E$ of line L10. So $(R, t)$ is optimal, and line L11 returns $\sqrt{E/N}$, the least RMSD. $\blacksquare$

**Remark on the value.** By Lemma 2, $E_{\min} = G_A + G_B - 2(s_1 + s_2 + d\, s_3)$, and $d = \operatorname{sign}(\det H)$ when $\det H \neq 0$, because $\det H = \det U \det V\, s_1 s_2 s_3$.
