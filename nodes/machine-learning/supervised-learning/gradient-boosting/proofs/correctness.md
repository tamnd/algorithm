---
title: The steps of gradient tree boosting, and when the training loss cannot increase
proves: [correctness]
status: full
---

We use the pseudocode of the page and its two losses. For squared loss, $\ell(y, F) = \frac12 (y - F)^2$. For log loss, $y \in \{0, 1\}$, $p(F) = 1/(1 + e^{-F})$ and $\ell(y, F) = \log(1 + e^{F}) - yF$. Write $F_i = F_{t-1}(x_i)$ for the scores before round $t$, and let $R_1, \ldots, R_J$ be the leaves of the tree of round $t$, as sets of training indices. Gradient boosting has no global optimality guarantee, since each tree is grown greedily. The claims below are what does hold.

### Claim 1: the pseudo-residuals are the negative gradient

For squared loss, $\partial \ell / \partial F = -(y - F)$, so $r_i = y_i - F_i$, the ordinary residual. For log loss, $\partial \ell / \partial F = e^{F}/(1 + e^{F}) - y = p(F) - y$, so $r_i = y_i - p(F_i)$. The vector $r = (r_1, \ldots, r_n)$ is the negative gradient of $L(F_1, \ldots, F_n) = \sum_i \ell(y_i, F_i)$ with respect to the scores. $\square$

### Claim 2: the initial constant

$F_0 = \arg\min_c \sum_i \ell(y_i, c)$. For squared loss, $\sum_i \frac12 (y_i - c)^2$ is a strictly convex quadratic with derivative $\sum_i (c - y_i)$, which is zero at $c = \bar y$. For log loss, the derivative is $\sum_i (p(c) - y_i) = n p(c) - \sum_i y_i$, zero at $p(c) = \bar y$, that is, $c = \ln(\bar y / (1 - \bar y))$ when $0 < \bar y < 1$. The second derivative $n p(c)(1 - p(c))$ is positive, so this is the minimum. $\square$

### Claim 3: the leaf values

The tree assigns one value $v_j$ to all examples in leaf $R_j$, so the line search splits into one problem per leaf: minimize $\phi_j(v) = \sum_{i \in R_j} \ell(y_i, F_i + v)$.

- *Squared loss.* $\phi_j(v) = \sum_{i \in R_j} \frac12 (r_i - v)^2$ has derivative $\sum_{i \in R_j} (v - r_i)$ and is strictly convex, so the exact minimizer is $v_j = \frac{1}{|R_j|}\sum_{i \in R_j} r_i$, the mean residual of the leaf. This is also the value that the least squares tree fit of line L5 gives to the leaf, so for squared loss line L6 changes nothing.
- *Log loss.* Here $\phi_j'(0) = -\sum_{i \in R_j} r_i = -G_j$ and $\phi_j''(0) = \sum_{i \in R_j} p(F_i)(1 - p(F_i)) = H_j$. The second-order Taylor polynomial $\phi_j(0) - G_j v + \frac12 H_j v^2$ is minimized at $v_j = G_j / H_j$. This is one Newton step from $v = 0$ for the equation $\phi_j'(v) = 0$. $\square$

### Claim 4: with squared loss, a round never increases the training loss when $0 < \nu \le 2$

Assume no subsampling, so the leaves partition $\{1, \ldots, n\}$. Fix a leaf $R_j$ with $m_j = |R_j|$ and mean residual $v_j$. After line L7 the residual of $i \in R_j$ is $r_i - \nu v_j$, and

$$\sum_{i \in R_j} \tfrac12 (r_i - \nu v_j)^2 = \sum_{i \in R_j} \tfrac12 r_i^2 - \nu v_j \sum_{i \in R_j} r_i + \tfrac12 \nu^2 m_j v_j^2 = \sum_{i \in R_j} \tfrac12 r_i^2 - \left(\nu - \tfrac{\nu^2}{2}\right) m_j v_j^2,$$

since $\sum_{i \in R_j} r_i = m_j v_j$. For $0 < \nu \le 2$, $\nu - \nu^2/2 = \nu(2 - \nu)/2 \ge 0$, so the loss of the leaf does not increase. Summing over the leaves gives the claim. The decrease is strict when $\nu < 2$ and some leaf has $v_j \ne 0$. $\square$

### Claim 5: with log loss, a round does not increase the loss of leaf $R_j$ when $\nu \le 8 H_j / |R_j|$

For each $i$, $\partial^2 \ell / \partial F^2 = p(1 - p) \le \frac14$. So $\phi_j''(v) \le |R_j|/4$ for every $v$, and Taylor's theorem with the Lagrange remainder gives, for each real $s$,

$$\phi_j(s) \le \phi_j(0) - G_j s + \frac{|R_j|}{8} s^2.$$

Take $s = \nu v_j = \nu G_j / H_j$. Then

$$\phi_j(\nu v_j) - \phi_j(0) \le -\nu \frac{G_j^2}{H_j} + \nu^2 \frac{|R_j| G_j^2}{8 H_j^2} = -\nu \frac{G_j^2}{H_j}\left(1 - \frac{\nu |R_j|}{8 H_j}\right),$$

which is at most 0 when $\nu \le 8H_j / |R_j|$. The ratio $H_j / |R_j|$ is the mean of $p(1 - p)$ over the leaf. It is small when the leaf is already confident, so no fixed $\nu$ works for all data; this is why the page calls the monotone decrease for log loss an observed fact for a given $\nu$, with this sufficient condition. $\square$

### Claim 6: a deep enough first tree with $\nu = 1$ fits squared loss exactly

Assume the inputs $x_i$ are distinct and there is no depth limit. A node is split while some threshold split has a positive decrease of the squared error. If the residuals in a node are not all equal, such a split exists: sort the node by a feature on which two of its points differ; if every threshold split had equal means on both sides, every prefix of the sorted residuals would have the same mean as the node, and then all residuals would be equal. A threshold split with unequal means $a \ne b$ on parts of sizes $k$ and $m - k$ decreases the error by $k(m - k)(a - b)^2/m > 0$. So each leaf has equal residuals, its value $v_j$ is that residual, and with $\nu = 1$ line L7 gives $F_1(x_i) = F_0 + r_i = y_i$ for every $i$. $\square$

### Termination and cost

The loop of line L2 runs $T$ times. Each tree split strictly reduces the size of both children, so each tree has at most $n$ leaves and its growth stops. Line L3 and line L7 take $O(n)$ time plus the tree evaluations, and the cost of line L5 is derived on the page.
