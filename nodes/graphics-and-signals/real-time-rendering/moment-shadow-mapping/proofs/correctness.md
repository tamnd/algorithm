---
title: The Hamburger 4MSM lookup returns the sharp lower bound on the occluded fraction given four power moments, so 1 - G is an upper bound on the lit fraction and is never above the VSM bound
proves: [correctness]
status: full
---

We use the notation of the page. A filter defines a probability distribution $\mu$ of depths on the real line. Its power moments are $b_k = \int z^k \, d\mu$ for $k = 0, \ldots, 4$, with $b_0 = 1$. The lit fraction for the depth $z_f$ is $\mu([z_f, \infty))$ and the occluded fraction is $\mu((-\infty, z_f))$, as in [variance shadow maps](/variance-shadow-maps/). Define the linear functional $L(p) = \sum_k p_k b_k$ on polynomials $p(x) = \sum_k p_k x^k$ of degree at most 4. Then $L(p) = \int p \, d\mu$ for every distribution with these moments. The Hankel matrix is $B = (b_{i + j})_{i, j = 0}^{2}$, and $c^T B c = L(p_c^2)$ for the polynomial $p_c(x) = c_1 + c_2 x + c_3 x^2$.

The standing hypothesis is that $B$ is positive definite: $L(p^2) > 0$ for every nonzero polynomial $p$ of degree at most 2. This holds when $\mu$ has at least three support points. The factorization in `solve_hankel` checks it: the pivots $d_1$ and $d_2$ of $B = L D L^T$ are positive exactly when $B$ is positive definite. We also assume that $c_3 \ne 0$ in line L4; the code stops otherwise. The arithmetic is exact real arithmetic.

## The kernel polynomial

Line L3 solves $B c = (1, z_f, z_f^2)^T$, and we write $K(x) = c_1 + c_2 x + c_3 x^2$.

**Lemma 1.** $L(K q) = q(z_f)$ for every polynomial $q$ of degree at most 2.

*Proof.* Row $k$ of $B c$ is $c_1 b_k + c_2 b_{k + 1} + c_3 b_{k + 2} = L(K x^k)$, and it equals $z_f^k$, for $k = 0, 1, 2$. Both sides are linear in $q$. $\square$

**Lemma 2.** $K(z_f) > 0$, and $K$ has two real roots $z_2 < z_3$, both different from $z_f$. These are the roots of line L4.

*Proof.* $c \ne 0$, because $B c \ne 0$. By Lemma 1 with $q = K$, $K(z_f) = L(K^2) = c^T B c > 0$. Suppose that $K$ does not change sign. Since $K(z_f) > 0$, then $K \ge 0$ on the real line, so $K(x)(x - z_f)^2$ is a nonnegative polynomial of degree at most 4. It is not the zero polynomial. A nonnegative polynomial in one variable is a sum of squares of polynomials of half its degree, so $L(K (x - z_f)^2) > 0$ by the hypothesis on $B$. But Lemma 1 with $q = (x - z_f)^2$ gives $L(K (x - z_f)^2) = 0$. So $K$ changes sign. As $c_3 \ne 0$, $K$ is a quadratic with two distinct real roots, and $K(z_f) > 0$ shows that $z_f$ is neither of them. $\square$

## The canonical representation

Let $x_1 = z_f$, $x_2 = z_2$, $x_3 = z_3$, and let $\ell_i$ be the Lagrange polynomials of degree 2 on these three nodes, with $\ell_i(x_j) = 1$ if $i = j$ and 0 otherwise.

**Lemma 3.** The weights $w_i = L(\ell_i)$ are positive, sum to 1, and the measure $\nu = \sum_i w_i \delta_{x_i}$ has the moments $b_0, \ldots, b_4$. So $L(p) = \sum_i w_i\, p(x_i)$ for every $p$ of degree at most 4.

*Proof.* Let $N(x) = (x - z_f) K(x)$, a cubic whose roots are the three nodes. Divide a polynomial $p$ of degree at most 4 by $N$: $p = N s + r$ with $\deg s \le 1$ and $\deg r \le 2$. Then $L(N s) = L(K \cdot (x - z_f) s) = 0$ by Lemma 1, because $(x - z_f) s$ has degree at most 2 and is zero at $z_f$. So $L(p) = L(r)$. Since $r = \sum_i r(x_i) \ell_i$, we get $L(r) = \sum_i w_i r(x_i) = \sum_i w_i p(x_i)$, because $N(x_i) = 0$. With $p = 1$, the weights sum to $b_0 = 1$. With $p = \ell_i^2$, of degree 4, $w_i = \sum_j w_j \ell_i(x_j)^2 = L(\ell_i^2) > 0$ by the hypothesis on $B$. $\square$

The two weights that the code uses are, from $L((x - a)(x - b)) = b_2 - (a + b) b_1 + a b$,

$$w_{z_2} = \frac{z_f z_3 - b_1 (z_f + z_3) + b_2}{(z_3 - z_2)(z_f - z_2)}, \qquad w_{z_f} = \frac{z_2 z_3 - b_1 (z_2 + z_3) + b_2}{(z_f - z_2)(z_f - z_3)}.$$

The first is line L6. Line L7 returns $1 - w_{z_f}$.

## The bound

Let $G$ be the value of lines L5 to L7: $G = 0$ if $z_f < z_2$, $G = w_{z_2}$ if $z_2 < z_f < z_3$, and $G = 1 - w_{z_f} = w_{z_2} + w_{z_3}$ if $z_f > z_3$. In each case $G = \nu((-\infty, z_f))$, the weight of the nodes less than $z_f$. (By Lemma 2, $z_f$ is not a node of $K$, so the tests $z_f \le z_2$ and $z_f \le z_3$ of the code are strict.)

**Theorem 4.** Every distribution $\mu$ on the real line with the moments $b_1, \ldots, b_4$ has $\mu((-\infty, z_f)) \ge G$, and $\nu$ attains it. So $G$ is the sharp lower bound on the occluded fraction, and $1 - G$ is the sharp upper bound on the lit fraction.

*Proof.* We give in each case a polynomial $u$ of degree at most 4 with $u \ge \mathbf{1}_{[z_f, \infty)}$ on the real line and $u(x_i) = \mathbf{1}[x_i \ge z_f]$ at the three nodes. Then $\mu([z_f, \infty)) \le \int u \, d\mu = L(u) = \sum_i w_i u(x_i) = \nu([z_f, \infty)) = 1 - G$ by Lemma 3.

Case $z_f < z_2$. Take $u = 1$. Here $1 - G = 1$.

Case $z_f > z_3$. Take $u(x) = \kappa (x - z_2)^2 (x - z_3)^2$ with $\kappa = 1 / ((z_f - z_2)(z_f - z_3))^2$. Then $u \ge 0$, $u(z_2) = u(z_3) = 0$ and $u(z_f) = 1$. For $x > z_3$ the factor $(x - z_2)(x - z_3)$ is positive and increasing, so $u$ is increasing there and $u \ge 1$ on $[z_f, \infty)$.

Case $z_2 < z_f < z_3$. We want $u(z_2) = 0$ and $u(z_f) = u(z_3) = 1$. Take $u(x) = 1 + \kappa (x - z_f)(x - z_3)^2 (x - e)$ and choose $e$ and $\kappa$ so that $u(z_2) = 0$ and $u'(z_2) = 0$. At $z_2$ we have $u - 1 = -1 \ne 0$, so $u'(z_2) = 0$ is the condition that the logarithmic derivative of $u - 1$ is zero there:

$$\frac{1}{z_2 - e} = \frac{1}{z_f - z_2} + \frac{2}{z_3 - z_2} > 0.$$

This fixes $e < z_2$. Then $u(z_2) = 0$ gives $\kappa = 1 / ((z_f - z_2)(z_3 - z_2)^2 (z_2 - e)) > 0$. For $x \ge z_f$, the factors $x - z_f$, $(x - z_3)^2$ and $x - e$ are all nonnegative, so $u \ge 1$. For $x < z_f$ we need $u \ge 0$. The roots of $u - 1$ are $e < z_f < z_3$, with $z_3$ double, so by Rolle's theorem $u' = (u - 1)'$ has a root in $(e, z_f)$, a root in $(z_f, z_3)$ and the root $z_3$. These are its three roots. Since $u'(z_2) = 0$ and $z_2 \in (e, z_f)$, $z_2$ is the only root of $u'$ below $z_f$. The leading coefficient $\kappa$ is positive, so $u$ decreases on $(-\infty, z_2)$ and increases on $(z_2, z_f)$. So $u \ge u(z_2) = 0$ on $(-\infty, z_f)$.

The measure $\nu$ has the moments $b$ by Lemma 3 and $\nu((-\infty, z_f)) = G$, so no larger lower bound holds for all $\mu$. $\square$

This is the Markov-Krein type result that Peters and Klein use (Krein and Nudel'man, Theorem IV.3.1). The bound is sharp over distributions on the whole real line (the Hamburger problem). The depths of a map lie in $[0, 1]$, and the nodes $z_2, z_3$ can lie outside it; then the bound is still valid, but a distribution on $[0, 1]$ may not attain it.

**Corollary 5.** $1 - G$ is never larger than the VSM value $p_{\max}(z_f)$ of the same distribution.

*Proof.* If $z_f \le b_1$, the VSM value is 1. Otherwise, the set of distributions with the moments $b_1, \ldots, b_4$ is a subset of the set with the moments $b_1, b_2$. The largest lit fraction over the smaller set is $1 - G$ (Theorem 4), and over the larger set it is $p_{\max}$ (Cantelli's inequality, which is sharp). $\square$

## The moment bias

**Proposition 6.** Line L1 with $\alpha \in [0, 1]$ and $b^\ast = (\tfrac12, \tfrac12, \tfrac12, \tfrac12)$ replaces $\mu$ by the mixture $\mu' = (1 - \alpha) \mu + \tfrac{\alpha}{2} (\delta_0 + \delta_1)$. For $0 < z_f \le 1$ the result $1 - G'$ satisfies $1 - G' \ge \mu([z_f, \infty)) - \alpha / 2$. If $\alpha > 0$ and $\mu$ has a depth outside $\{0, 1\}$, the biased Hankel matrix is positive definite.

*Proof.* The point masses at 0 and 1 have $z^k$ equal to 0 and 1 for $k \ge 1$, so their moments are all $\tfrac12$, and the moments of $\mu'$ are $(1 - \alpha) b + \alpha b^\ast$. With $0 < z_f \le 1$, $\mu'([z_f, \infty)) = (1 - \alpha) \mu([z_f, \infty)) + \alpha / 2$. By Theorem 4 applied to $\mu'$, $1 - G' \ge (1 - \alpha) \mu([z_f, \infty)) + \alpha / 2 \ge \mu([z_f, \infty)) - \alpha / 2$, because $\mu([z_f, \infty)) \le 1$. For the last claim, $B' = (1 - \alpha) B + \alpha B^\ast$, and $c^T B' c = (1 - \alpha) \int p_c^2 \, d\mu + \tfrac{\alpha}{2} (p_c(0)^2 + p_c(1)^2)$. If this is 0, then $p_c$ is zero at 0, at 1 and at a depth of $\mu$ outside $\{0, 1\}$, so $p_c = 0$ and $c = 0$. $\square$

So the bias trades an upper bound for an estimate that is at most $\alpha/2$ below the true lit fraction, and it makes maps with one or two distinct depths usable, as a plane under a plane is. Peters and Klein use $\alpha = 3 \cdot 10^{-5}$ for their quantized formats; this value is a tuning, not a derived constant. The clamp of line L8 does nothing in exact arithmetic, because $0 \le G \le 1$; it guards against rounding.
