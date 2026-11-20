---
title: With exact statistics and two coprime subchannels, the null space of Q is the channel up to a scalar
proves: [correctness]
status: full
---

**Setting.** $P = 2$. The subchannels are $h_1, h_2$, each with taps $0, \ldots, L-1$, and $h(l) = (h_1(l), h_2(l))$. Assume $h(0) \ne 0$ and $h(L-1) \ne 0$, so the channel has exactly $L$ taps. For each $p$, let $\tilde p_p(x) = \sum_{l=0}^{L-1} h_p(l)\, x^{L-1-l}$. Its roots are the zeros of $H_p(z) = \sum_l h_p(l) z^{-l}$, so "no common zero" means that $\tilde p_1$ and $\tilde p_2$ are coprime. The window length is $N \ge L$. $H_N(h)$ is the $2N \times (N+L-1)$ block Toeplitz matrix with block $(i, m)$ equal to $h(m-i)$. The exact covariance is $R = H_N R_a H_N^H + \sigma^2 I$, with $R_a$ positive definite. The case $P > 2$ is the theorem of Moulines, Duhamel, Cardoso and Mayrargue (1995). It is cited and not proved here. The code tests only $P = 2$.

**Lemma 1 (full column rank).** If $N \ge L - 1$, then $H_N(h)$ has rank $N + L - 1$.

*Proof.* Let $H_N t = 0$ and $T(x) = \sum_{m=0}^{N+L-2} t_m x^m$. Row $(i, p)$ of $H_N t$ is $\sum_l h_p(l)\, t_{i+l}$, which is the coefficient of $x^{i+L-1}$ in $T(x)\, \tilde p_p(x)$. So, for each $p$, the coefficients of degrees $L-1, \ldots, N+L-2$ of $T \tilde p_p$ vanish. Since $\deg(T \tilde p_p) \le N + 2L - 3$, we can write $T \tilde p_p = A_p + x^{N+L-1} B_p$ with $\deg A_p \le L - 2$. Then
$$A_1 \tilde p_2 - A_2 \tilde p_1 = x^{N+L-1} (B_2 \tilde p_1 - B_1 \tilde p_2),$$
because both sides equal $T \tilde p_1 \tilde p_2$ minus the same terms. The left side has degree at most $2L - 3$. The right side is zero or has degree at least $N + L - 1 \ge 2L - 2$. So both sides are zero, and $A_1 \tilde p_2 = A_2 \tilde p_1$.

Because $h(0) \ne 0$, some $p$, say $p = 1$, has $h_1(0) \ne 0$, so $\deg \tilde p_1 = L - 1$. Since $\tilde p_1$ divides $A_1 \tilde p_2$ and is coprime to $\tilde p_2$, it divides $A_1$. But $\deg A_1 \le L - 2$, so $A_1 = 0$. Then $A_2 \tilde p_1 = 0$, so $A_2 = 0$. Now $T \tilde p_p = x^{N+L-1} B_p$ for both $p$. Because $h(L-1) \ne 0$, some $p$ has $\tilde p_p(0) = h_p(L-1) \ne 0$. Then $x^{N+L-1}$ divides $T$, but $\deg T \le N + L - 2$, so $T = 0$. $\square$

**Lemma 2 (the noise subspace).** The $2N - (N+L-1)$ smallest eigenvalues of $R$ equal $\sigma^2$, and their eigenvectors span the left null space $\{g : g^H H_N = 0\}$.

*Proof.* $S = H_N R_a H_N^H$ is positive semidefinite with range equal to the range of $H_N$, which has dimension $N + L - 1$ by Lemma 1. So $S$ has $N + L - 1$ positive eigenvalues, with eigenvectors spanning that range, and the eigenvalue $0$ on its orthogonal complement, which is the left null space of $H_N$. Adding $\sigma^2 I$ shifts every eigenvalue by $\sigma^2$ and keeps the eigenvectors. $\square$

So line L2, with the exact $R$, returns a basis of the left null space. The code takes $2k$ real eigenvectors of the real form, which give $2k$ complex vectors spanning the same $k$-dimensional complex space.

**Lemma 3 (what Q measures).** For any $h' \in \mathbb{C}^{2L}$, $h'^H Q h' = \sum_{g \in G} \|g^H H_N(h')\|^2$. So $Q h' = 0$ if and only if $g^H H_N(h') = 0$ for every $g$ in the span of $G$.

*Proof.* Entry $m$ of $g^H H_N(h')$ is $\sum_i g_i^H h'(m - i) = \sum_l g_{m-l}^H h'(l)$, which is row $m$ of $\mathcal{G}(g)$ (line L5) times $h'$. So $\|g^H H_N(h')\|^2 = \|\mathcal{G}(g) h'\|^2 = h'^H \mathcal{G}(g)^H \mathcal{G}(g) h'$, and line L6 sums these. $Q$ is positive semidefinite, so $h'^H Q h' = 0$ if and only if $Q h' = 0$. The map $g \mapsto g^H H_N(h')$ is conjugate linear, so it vanishes on a spanning set if and only if it vanishes on the span. $\square$

**Theorem.** Under the setting above, the null space of $Q$ is $\{\beta h : \beta \in \mathbb{C}\}$. So line L7 returns $h / \|h\|$ times a unit scalar.

*Proof.* If $h' = \beta h$, then $g^H H_N(h') = \beta\, g^H H_N(h) = 0$ for every $g$ in the left null space, so $Q h' = 0$ by Lemmas 2 and 3.

Conversely, let $Q h' = 0$. Define the cross-relation vector $c$ by its blocks $c_i^H = (h_2(i), -h_1(i))$ for $0 \le i \le L - 1$ and $c_i = 0$ for $L \le i \le N - 1$. This fits because $N \ge L$. Entry $m$ of $c^H H_N(h)$ is
$$\sum_i \left( h_2(i)\, h_1(m-i) - h_1(i)\, h_2(m-i) \right),$$
which is coefficient $m$ of $h_2 * h_1 - h_1 * h_2 = 0$. So $c$ is in the left null space, and by Lemmas 2 and 3, $c^H H_N(h') = 0$. The same computation shows that entry $m$ of $c^H H_N(h')$ is coefficient $m$ of $h_2 * h'_1 - h_1 * h'_2$. The column index $m$ runs over $0, \ldots, N + L - 2 \supseteq \{0, \ldots, 2L - 2\}$, which covers every coefficient. So $h_2 * h'_1 = h_1 * h'_2$. In terms of the reversed polynomials, $\tilde p_2 \tilde p'_1 = \tilde p_1 \tilde p'_2$, where $\tilde p'_p$ is formed from $h'_p$ in the same way and has degree at most $L - 1$.

Take $p$ with $\deg \tilde p_p = L - 1$, say $p = 1$. Then $\tilde p_1$ divides $\tilde p_2 \tilde p'_1$, and since it is coprime to $\tilde p_2$, it divides $\tilde p'_1$. Because $\deg \tilde p'_1 \le L - 1 = \deg \tilde p_1$, we get $\tilde p'_1 = \beta \tilde p_1$ for a constant $\beta$. Then $\tilde p_1 \tilde p'_2 = \beta \tilde p_1 \tilde p_2$, so $\tilde p'_2 = \beta \tilde p_2$. So $h' = \beta h$. $\square$

**Remark (a common zero).** If $\tilde p_1$ and $\tilde p_2$ share a root $z_0$, write $\tilde p_p = (x - z_0)\, q_p$ and let $h'$ be the channel with $\tilde p'_p = (x - z_1)\, q_p$ for another $z_1 \ne z_0$. Then $\tilde p_2 \tilde p'_1 = \tilde p_1 \tilde p'_2$, so the cross relation no longer separates $h$ from $h'$. In fact no second-order method can separate them when $z_1 = 1/\bar z_0$ and the input is white, since the two channels then differ by an allpass factor, up to a scale, and give the same covariance at every lag. The test `test_a_common_zero_makes_the_channel_unidentifiable` shows that $Q$ then has a null space of dimension 2.

**Remark (sample covariance).** With the sample covariance $\hat R$ from line L1, $\hat R \to R$ as $K \to \infty$ for an ergodic input. The noise subspace is a continuous function of $R$ while the gap between $\sigma^2$ and the next eigenvalue is positive, and the null vector of $Q$ is a continuous function of $Q$ while the null space has dimension 1. So $\hat h$ converges to $h$ up to the scalar. The rate is not derived here.
