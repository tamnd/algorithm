---
title: Sphered projection pursuit searches every direction, and Gaussian projections score lowest
proves: [correctness]
status: full
---

We use the pseudocode and notation of the page. After line L1 the sphered points $z_t = V(x_t - \mu)$ have sample mean 0 and sample covariance $I$. An index $I$ maps a sample of real numbers to a real number and is invariant under affine maps $y \mapsto a y + b$ with $a \ne 0$; the three indices of the page standardize their input first, so they have this property.

**Lemma 1 (the sphere covers every projection).** For every nonzero $a \in \mathbb{R}^d$ there is a unit vector $w$ and a number $c > 0$ with $a^{\top}(x_t - \mu) = c\, w^{\top} z_t$ for all $t$. So the maximum of the index over unit $w$ in the sphered space equals its maximum over all linear projections of the data.

*Proof.* $V$ is invertible, so $x_t - \mu = V^{-1} z_t$ and $a^{\top}(x_t - \mu) = (V^{-\top} a)^{\top} z_t$. Put $c = \lVert V^{-\top} a \rVert$ and $w = V^{-\top} a / c$. By affine invariance the index of the two projections is the same. $\square$

For a unit $w$, the projection $w^{\top} z_t$ has sample mean 0 and sample variance $w^{\top} I w = 1$. So every candidate in line L5 is already standardized, and the index compares only the shapes of the projected distributions. Line L8 returns $w^{\top} V$, the functional $a$ of Lemma 1 for the direction found.

**Lemma 2 (the Gaussian is least interesting).** Let $y$ have a density $p$ with mean $m$ and variance $\sigma^2$, and let $\varphi$ be the Gaussian density with the same mean and variance. The negentropy $J(y) = h(\varphi) - h(p)$, with $h$ the differential entropy, satisfies
$$ J(y) = \int p \log \frac{p}{\varphi} \ge 0 , $$
with equality if and only if $y$ is Gaussian.

*Proof.* $\log \varphi(u) = -\frac12 \log(2\pi\sigma^2) - (u - m)^2 / (2\sigma^2)$ is a quadratic in $u$, so $\int p \log \varphi$ depends only on the mean and variance of $p$, and it equals $\int \varphi \log \varphi = -h(\varphi)$. Hence $\int p \log(p / \varphi) = -h(p) + h(\varphi) = J(y)$. This is a Kullback-Leibler divergence, which is nonnegative by Jensen's inequality and is 0 only when $p = \varphi$ almost everywhere. $\square$

The moment index $(\kappa_3^2 + \kappa_4^2/4)/12 = \kappa_3^2/12 + \kappa_4^2/48$ is the leading term of an expansion of $J$ about the Gaussian (Jones and Sibson 1987), and the logcosh index is another approximation of $J$ (Hyvärinen 1998). Both are 0 for a Gaussian, because its third and fourth cumulants are 0 and $E[\log\cosh u]$ then equals the Gaussian constant. Both are nonnegative by construction. The moment index can also be 0 for a non-Gaussian distribution with $\kappa_3 = \kappa_4 = 0$; this is a known blind spot of cumulant indices.

**Theorem 1 (ICA as projection pursuit).** Let $z = Q s$ with $Q$ orthogonal and $s$ a vector of independent sources with mean 0, variance 1, $\kappa_3(s_i) = 0$ and fourth cumulants $\kappa_i$, and let $m$ be the unique index with the largest $|\kappa_i|$. Then the population moment index of $w^{\top} z$ over unit $w$ is maximized exactly at $w = \pm Q e_m$, so the most interesting projection is one source.

*Proof.* Put $q = Q^{\top} w$, a unit vector, so $w^{\top} z = q^{\top} s$. Cumulants of independent variables add, and the third and fourth cumulants scale with the third and fourth powers, so $\kappa_3(q^{\top} s) = 0$ and $\kappa_4(q^{\top} s) = \sum_i q_i^4 \kappa_i$. Then
$$ \Bigl|\sum_i q_i^4 \kappa_i\Bigr| \le |\kappa_m| \sum_i q_i^4 \le |\kappa_m| \sum_i q_i^2 = |\kappa_m| . $$
The first inequality is an equality only if $q_i = 0$ whenever $|\kappa_i| < |\kappa_m|$, and the second only if $q$ has a single nonzero entry. So the index $\kappa_4^2/48$ reaches its maximum $\kappa_m^2/48$ only at $q = \pm e_m$. $\square$

If the search for the second direction is restricted to the orthogonal complement of $Q e_m$, the same argument applies to the other sources, so deflation as in lines L3 and L5 finds the sources in decreasing order of $|\kappa_i|$. With skewed sources the $\kappa_3^2$ term adds a similar term, and with the negentropy index the same picture holds approximately. This is why ICA by maximization of non-Gaussianity is a special case of projection pursuit.

**Theorem 2 (the search is monotone and stops).** In each restart, the index of the current direction never decreases, the current direction stays a unit vector orthogonal to $w_1, \ldots, w_{p-1}$, and the loop of lines L4 to L6 ends after at most $\lceil \log_2(h_0 / h_{\min}) \rceil (M + 1)$ passes, where $M$ is the cap on moves at one step size. At the end, no trial move of size $h_{\min}$ along a coordinate axis improves the index, unless the cap was reached.

*Proof.* Line L6 replaces $w$ only by a candidate with a strictly larger index. Each candidate is projected onto the orthogonal complement of the earlier directions and normalized, so the invariants hold. At one step size there are at most $M$ moves and then one halving, and the number of halvings before $h \le h_{\min}$ is $\lceil \log_2(h_0 / h_{\min}) \rceil$. The last statement is the stopping condition. $\square$

The directions found in different rounds are orthonormal in the sphered space, so the projections $w_p^{\top} z_t$ are uncorrelated with unit variance. The search finds a local maximum of a nonconvex function on the sphere; restarts in line L3 make it more likely that the best local maximum is a global one, but there is no guarantee for $d > 1$.

**Cost.** Line L1 takes $\Theta(n d^2 + d^3)$. One index evaluation takes $\Theta(n d)$ to project and $\Theta(n)$ for the moment and logcosh indices, or $\Theta(n^2)$ for the Friedman-Tukey density with all pairs. One pass of line L5 makes $2d$ evaluations. With $R$ restarts and $P$ passes per restart, finding $k$ directions costs $O(n d^2 + d^3 + k R P d\, n d)$ for the moment index. The extra memory is $\Theta(n d)$.
