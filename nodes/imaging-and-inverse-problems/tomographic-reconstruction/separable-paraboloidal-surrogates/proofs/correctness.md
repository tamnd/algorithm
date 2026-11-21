---
title: The SPS surrogate lies above the cost, so SPS does not increase it
proves: [correctness]
status: full
---

We use the notation of the page. $A$ is an $m \times N$ matrix with $a_{ij} \ge 0$ and row sums $a_i = \sum_j a_{ij} > 0$. The data are $y_i \ge 0$, the background is $b_i \ge 0$ with $b_i > 0$ wherever $y_i > 0$, and $\beta \ge 0$. The cost is
$$\Phi(x) = \sum_i h_i([A x]_i) + \beta R(x), \qquad h_i(l) = (l + b_i) - y_i \log(l + b_i), \qquad R(x) = \tfrac12 \sum_{\{j,k\} \in E} w_{jk} (x_j - x_k)^2,$$
with $w_{jk} \ge 0$. Each $h_i$ is convex and finite on $[0, \infty)$. Fix the current image $x \ge 0$ and write $l_i = [A x]_i$. All statements are in exact arithmetic.

**Lemma 1 (the one-dimensional parabola).** Let $h(t) = (t + b) - y \log(t + b)$ with $y > 0$ and $b > 0$, let $l \ge 0$, and let
$$c = \frac{2\,[h(0) - h(l) + h'(l)\, l]}{l^2} \text{ if } l > 0, \qquad c = h''(0) = \frac{y}{b^2} \text{ if } l = 0.$$
Then $c \ge 0$, and $q(t) = h(l) + h'(l)(t - l) + \frac{c}{2}(t - l)^2$ satisfies $q(t) \ge h(t)$ for all $t \ge 0$, with equality at $t = l$. For $y = 0$, $h$ is linear and $c = 0$ gives $q = h$.

*Proof.* $c \ge 0$ because $h$ is convex: $h(0) \ge h(l) + h'(l)(0 - l)$. Let $g = q - h$ on $[0, \infty)$. Then $g(l) = 0$ and $g'(l) = 0$, and $g''(t) = c - h''(t) = c - y/(t + b)^2$. Since $h''$ is decreasing, $g''$ is increasing, so $g'$ is convex.

If $l = 0$, then $g''(t) = h''(0) - h''(t) \ge 0$, so $g$ is convex with $g(0) = g'(0) = 0$, and $g \ge 0$.

If $l > 0$, the choice of $c$ gives $g(0) = 0$. Since $g(0) = g(l) = 0$, Rolle's theorem gives a $\xi \in (0, l)$ with $g'(\xi) = 0$. The convex function $g'$ is 0 at $\xi$ and at $l$, so $g' \le 0$ on $[\xi, l]$ and $g' \ge 0$ on $[0, \xi]$ and on $[l, \infty)$. So $g$ rises from $g(0) = 0$ on $[0, \xi]$, falls to $g(l) = 0$ on $[\xi, l]$, and rises again after $l$. Each piece starts or ends at the value 0 from above, so $g \ge 0$ on $[0, \infty)$. $\square$

The curvature is the smallest one with this property for $l > 0$: a parabola with the same value and slope at $l$ and a smaller curvature is below $h(0)$ at $t = 0$.

**Lemma 2 (the separable surrogate).** For $z \ge 0$ let
$$S(z) = \sum_i \sum_j \frac{a_{ij}}{a_i}\, q_i\big(a_i (z_j - x_j) + l_i\big) + \beta \sum_{\{j,k\} \in E} \frac{w_{jk}}{4} \Big[(2 z_j - x_j - x_k)^2 + (2 z_k - x_j - x_k)^2\Big],$$
with $q_i$ the parabola of Lemma 1 for $h_i$ at $l_i$. Then $S(x) = \Phi(x)$ and $S(z) \ge \Phi(z)$ for every $z \ge 0$.

*Proof.* The weights $a_{ij}/a_i$ are nonnegative and sum to 1 over $j$, and $\sum_j (a_{ij}/a_i)(a_i (z_j - x_j) + l_i) = [A z]_i - l_i + l_i = [A z]_i$. The parabola $q_i$ is convex on all of $\mathbb{R}$, so Jensen's inequality gives $\sum_j (a_{ij}/a_i) q_i(a_i(z_j - x_j) + l_i) \ge q_i([A z]_i)$. Since $[A z]_i \ge 0$, Lemma 1 gives $q_i([A z]_i) \ge h_i([A z]_i)$. Note that the arguments $a_i(z_j - x_j) + l_i$ can be negative; this is no problem, because only the convexity of $q_i$ is used there, and $q_i$ is defined everywhere.

For the penalty, $z_j - z_k = \frac12 (2 z_j - x_j - x_k) - \frac12 (2 z_k - x_j - x_k)$, and $(\frac12 u - \frac12 v)^2 \le \frac12 u^2 + \frac12 v^2$ by the convexity of the square. Multiplying by $\beta w_{jk} / 2$ gives the penalty terms of $S$. At $z = x$ every inequality is an equality: all arguments of $q_i$ equal $l_i$, $q_i(l_i) = h_i(l_i)$, and $u = -v = x_j - x_k$. $\square$

**Theorem 1 (the update minimizes the surrogate).** $S$ is a sum of one-pixel quadratics $S(z) = \sum_j S_j(z_j)$ with
$$S_j'(x_j) = \partial \Phi / \partial x_j(x), \qquad S_j'' = d_j + \beta p_j, \qquad d_j = \sum_i a_{ij}\, a_i\, c_i, \qquad p_j = 2 \sum_{k \sim j} w_{jk}.$$
If $d_j + \beta p_j > 0$, the minimizer of $S_j$ over $z_j \ge 0$ is $[x_j - \partial_j \Phi(x) / (d_j + \beta p_j)]_+$, which is line L10.

*Proof.* The derivative of the $i$-th data term with respect to $z_j$ at $z = x$ is $(a_{ij}/a_i) \cdot a_i\, q_i'(l_i) = a_{ij} h_i'(l_i)$, and its second derivative is $(a_{ij}/a_i) a_i^2 c_i = a_{ij} a_i c_i$. Each edge $\{j, k\}$ adds $\beta (w_{jk}/4) \cdot 4 (2 z_j - x_j - x_k)$ to $S_j'$, which is $\beta w_{jk} (x_j - x_k)$ at $z_j = x_j$, and $\beta (w_{jk}/4) \cdot 8 = 2 \beta w_{jk}$ to $S_j''$. Summing gives the formulas, and the gradient of $\Phi$ at $x$ is $A^T h'(A x) + \beta \nabla R(x)$, which matches. A one-variable quadratic with positive curvature has its minimizer over $[0, \infty)$ at the clipped Newton point. If $d_j + \beta p_j = 0$, then every ray through $j$ has $y_i = 0$ (so $c_i = 0$ and $h_i' = 1$) and $j$ has no penalty edge with $w_{jk} > 0$; $S_j$ is linear with slope $\sum_i a_{ij} \ge 0$, and the code takes $z_j = 0$ if the slope is positive. $\square$

**Theorem 2 (monotone decrease).** Let $x'$ be the SPS update of $x$. Then $x' \ge 0$ and $\Phi(x') \le \Phi(x)$.

*Proof.* $x' \ge 0$ by the clipping. By Lemma 2 and Theorem 1, $\Phi(x') \le S(x') \le S(x) = \Phi(x)$. $\square$

**Theorem 3 (fixed points).** If every $d_j + \beta p_j > 0$, then $x \ge 0$ is a fixed point of the update if and only if it satisfies the KKT conditions $\partial_j \Phi(x) = 0$ where $x_j > 0$ and $\partial_j \Phi(x) \ge 0$ where $x_j = 0$. Since $\Phi$ is convex, these are exactly the minimizers of $\Phi$ over $x \ge 0$.

*Proof.* With $D_j = d_j + \beta p_j > 0$, $x_j = [x_j - \partial_j \Phi / D_j]_+$ holds if and only if $\partial_j \Phi = 0$ (when $x_j > 0$) or $-\partial_j \Phi / D_j \le 0$ (when $x_j = 0$). For a convex function on the nonnegative orthant, the KKT conditions are necessary and sufficient for a minimum. $\square$

**Convergence (cited, not proved here).** Theorem 2 makes $\Phi(x^k)$ a nonincreasing sequence that is bounded below when $\Phi$ is bounded below on $x \ge 0$, so it converges. That the iterates themselves converge to a minimizer needs more: a lower bound on the curvatures and a strictly convex cost are typical conditions. The papers of Erdogan and Fessler discuss this; this page does not prove it. The tests check the KKT conditions at the limit for a small problem.
