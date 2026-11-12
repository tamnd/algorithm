---
title: Fisher's directions are the top generalized eigenvectors of the scatter pair, and there are at most k - 1 useful ones
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. The data are $x_1, \ldots, x_n \in \mathbb{R}^d$ with labels in $k$ classes, class $c$ has $n_c \ge 1$ points and mean $\mu_c$, and $\mu$ is the overall mean. $S_W$ and $S_B$ are the within-class and between-class scatter matrices of lines L2 and L3. We assume that $S_W$ is positive definite, so line L4 succeeds and $L$ is invertible.

**Lemma 1 (change of variables).** For $w \ne 0$ put $u = L^{\top} w$. Then $w^{\top} S_W w = u^{\top} u$ and $w^{\top} S_B w = u^{\top} M u$ with $M = L^{-1} S_B L^{-\top}$, so $J(w) = u^{\top} M u / u^{\top} u$. The map $w \mapsto L^{\top} w$ is a bijection of $\mathbb{R}^d \setminus \{0\}$.

*Proof.* $w^{\top} S_W w = w^{\top} L L^{\top} w = u^{\top} u$. Since $w = L^{-\top} u$, $w^{\top} S_B w = u^{\top} L^{-1} S_B L^{-\top} u = u^{\top} M u$. $L^{\top}$ is invertible, so the map is a bijection. $\square$

**Theorem 1 (optimality).** Let $\lambda_1 \ge \cdots \ge \lambda_d$ and $v_1, \ldots, v_d$ be the eigenvalues and orthonormal eigenvectors of $M$ from line L6, and $w_t = L^{-\top} v_t$ from line L7. Then:

1. $S_B w_t = \lambda_t S_W w_t$ and $w_s^{\top} S_W w_t = [s = t]$ for all $s, t$.
2. $J(w_t) = \lambda_t$, and $\lambda_t = \max \{ J(w) : w \ne 0,\ w^{\top} S_W w_s = 0 \text{ for } s < t \}$. In particular $\lambda_1 = \max_{w \ne 0} J(w)$.

*Proof.* $M$ is symmetric because $S_B$ is, and it is positive semidefinite because $u^{\top} M u = w^{\top} S_B w = \sum_c n_c \big((\mu_c - \mu)^{\top} w\big)^2 \ge 0$. By the [spectral theorem](/spectral-theorem/) it has real eigenvalues $\lambda_t \ge 0$ and an orthonormal basis of eigenvectors $v_t$.

(1) $M v_t = \lambda_t v_t$ means $L^{-1} S_B L^{-\top} v_t = \lambda_t v_t$. Multiply on the left by $L$ and use $L^{-\top} v_t = w_t$ and $v_t = L^{\top} w_t$: $S_B w_t = \lambda_t L L^{\top} w_t = \lambda_t S_W w_t$. Also $w_s^{\top} S_W w_t = v_s^{\top} v_t = [s = t]$.

(2) By Lemma 1, $J(w) = R(u) = u^{\top} M u / u^{\top} u$ with $u = L^{\top} w$, and the constraint $w^{\top} S_W w_s = 0$ is $u^{\top} v_s = 0$. Write $u = \sum_i \alpha_i v_i$. Then $R(u) = \sum_i \lambda_i \alpha_i^2 / \sum_i \alpha_i^2$. If $\alpha_s = 0$ for all $s < t$, every remaining $\lambda_i$ has $i \ge t$, so $\lambda_i \le \lambda_t$ and $R(u) \le \lambda_t$. The choice $u = v_t$ meets the constraints and gives $R(v_t) = \lambda_t$. So the maximum is $\lambda_t$ and $w_t$ attains it. $\square$

This is the [Courant-Fischer](/courant-fischer-theorem/) characterization applied to the [Rayleigh quotient](/rayleigh-quotient/) of $M$.

**Theorem 2 (at most $k - 1$ useful directions).** $\operatorname{rank} S_B \le k - 1$. Hence $\lambda_t = 0$ for every $t \ge k$, and for such $t$ the projections $w_t^{\top} \mu_c$ of all class means are equal.

*Proof.* Let $b_c = \mu_c - \mu$. Since $n \mu = \sum_i x_i = \sum_c n_c \mu_c$, we get $\sum_c n_c b_c = n\mu - n\mu = 0$. So the $k$ vectors $b_c$ are linearly dependent (all $n_c \ge 1$), and their span has dimension at most $k - 1$. The range of $S_B = \sum_c n_c b_c b_c^{\top}$ lies in that span, so $\operatorname{rank} S_B \le k - 1$. Since $L$ is invertible, $\operatorname{rank} M = \operatorname{rank} S_B \le k - 1$, and the positive semidefinite $M$ has at most $k - 1$ positive eigenvalues. So $\lambda_t = 0$ for $t \ge k$. Then $0 = \lambda_t = J(w_t) = \sum_c n_c (b_c^{\top} w_t)^2 / w_t^{\top} S_W w_t$, so $b_c^{\top} w_t = 0$ for every $c$, that is, $w_t^{\top} \mu_c = w_t^{\top} \mu$ for every class. $\square$

**Theorem 3 (two classes).** If $k = 2$, let $\delta = \mu_1 - \mu_0$. Then $S_B = \frac{n_0 n_1}{n} \delta \delta^{\top}$, the direction $w_1$ is a multiple of $S_W^{-1} \delta$, and $\lambda_1 = \frac{n_0 n_1}{n} \delta^{\top} S_W^{-1} \delta$.

*Proof.* $\mu = (n_0 \mu_0 + n_1 \mu_1)/n$ gives $b_0 = -\frac{n_1}{n} \delta$ and $b_1 = \frac{n_0}{n} \delta$. So $S_B = n_0 \frac{n_1^2}{n^2} \delta\delta^{\top} + n_1 \frac{n_0^2}{n^2} \delta\delta^{\top} = \frac{n_0 n_1}{n} \delta \delta^{\top}$. If $\delta = 0$ then $\lambda_1 = 0$, $J \equiv 0$ and every direction is optimal, which agrees with the claim. Else $\lambda_1 > 0$: take $w = S_W^{-1}\delta$, then $J(w) = \frac{n_0 n_1}{n} \delta^{\top} S_W^{-1} \delta > 0$. By Theorem 1, $S_B w_1 = \lambda_1 S_W w_1$, that is, $\frac{n_0 n_1}{n} (\delta^{\top} w_1) \delta = \lambda_1 S_W w_1$. The right side is not zero, so $\delta^{\top} w_1 \ne 0$ and $w_1 = \frac{n_0 n_1 (\delta^{\top} w_1)}{n \lambda_1} S_W^{-1} \delta$. Then $J(w_1) = J(S_W^{-1}\delta)$, because $J$ does not change when $w$ is scaled. $\square$

**Theorem 4 (link to the Gaussian classifier).** Fit the model $x \mid c \sim \mathcal{N}(\mu_c, \Sigma)$ with priors $\pi_c$ by maximum likelihood, so $\Sigma = S_W / n$ and $\pi_c = n_c / n$. (a) The Bayes rule for the fitted model maximizes $\delta_c(x) = x^{\top} \Sigma^{-1} \mu_c - \frac12 \mu_c^{\top} \Sigma^{-1} \mu_c + \log \pi_c$, a linear function of $x$. (b) For $k = 2$ its boundary is a level set of $w_1^{\top} x$. (c) If $\operatorname{rank} S_B = k - 1$ and $W = [w_1, \ldots, w_{k-1}]$, the Bayes rule equals $\arg\max_c \big( -\frac n2 \lVert W^{\top}(x - \mu_c) \rVert^2 + \log \pi_c \big)$.

*Proof.* (a) $\log(\pi_c\, p(x \mid c)) = -\frac12 (x - \mu_c)^{\top} \Sigma^{-1} (x - \mu_c) + \log \pi_c + C$, where $C$ does not depend on $c$ because $\Sigma$ is shared. Expand the quadratic form: the term $-\frac12 x^{\top} \Sigma^{-1} x$ is also the same for all classes. Drop both to get $\delta_c$. (b) $\delta_1(x) - \delta_0(x) = x^{\top} \Sigma^{-1} \delta + \text{const} = n\, x^{\top} S_W^{-1} \delta + \text{const}$, and $S_W^{-1} \delta$ is a multiple of $w_1$ by Theorem 3. (c) Put $z = L^{-1} x$ and $\nu_c = L^{-1} \mu_c$, $\nu = L^{-1} \mu$. Then $(x - \mu_c)^{\top} \Sigma^{-1} (x - \mu_c) = n \lVert z - \nu_c \rVert^2$. Let $P = \sum_{t < k} v_t v_t^{\top}$. The range of $M = \sum_c n_c (\nu_c - \nu)(\nu_c - \nu)^{\top}$ is the span of the $\nu_c - \nu$, of dimension $k - 1$, and it is spanned by $v_1, \ldots, v_{k-1}$, the eigenvectors with positive eigenvalues. So $P(\nu_c - \nu) = \nu_c - \nu$, and $(I - P)\nu_c = (I - P)\nu$ for every $c$. By Pythagoras, $\lVert z - \nu_c \rVert^2 = \lVert P(z - \nu_c) \rVert^2 + \lVert (I - P)(z - \nu) \rVert^2$, and the second term is the same for all classes. Finally $\lVert P(z - \nu_c) \rVert^2 = \sum_{t<k} \big(v_t^{\top} L^{-1}(x - \mu_c)\big)^2 = \lVert W^{\top}(x - \mu_c) \rVert^2$, because $v_t^{\top} L^{-1} = (L^{-\top} v_t)^{\top} = w_t^{\top}$. $\square$

**Cost.** Lines L1 to L3 take $\Theta(n d^2)$ operations: one outer product of size $d \times d$ per point for $S_W$, and $k$ of them for $S_B$. Line L4 takes about $d^3/3$ operations and line L5 $\Theta(d^3)$ by triangular solves. Line L6 takes $\Theta(d^3)$ operations with a symmetric QR eigensolver; the Jacobi method of the implementation takes $\Theta(d^3)$ per sweep and a number of sweeps that is small in practice but not bounded by a constant in theory. Line L7 takes $\Theta(r d^2)$. The memory is $\Theta(d^2)$ beyond the data.
