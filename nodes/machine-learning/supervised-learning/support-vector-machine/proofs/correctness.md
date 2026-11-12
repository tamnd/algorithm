---
title: The SVM dual gives the maximum margin classifier, and the KKT conditions certify it
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $(x_i, y_i)$, $i = 1, \ldots, n$, be the data with $y_i \in \{-1, +1\}$, let $k(x, z) = \varphi(x) \cdot \varphi(z)$ be a positive semidefinite kernel, and let $C > 0$. Write $f(x) = w \cdot \varphi(x) + b$. The primal problem is

$$(P) \quad \min_{w, b, \xi} \; \tfrac12 \lVert w \rVert^2 + C \sum_i \xi_i \quad \text{subject to } y_i f(x_i) \ge 1 - \xi_i, \; \xi_i \ge 0.$$

**Lemma 1 (the primal has a solution, and $w$ is unique).** The point $w = 0$, $b = 0$, $\xi_i = 1$ is feasible, so the optimal value $p^*$ is finite and at most $Cn$. On the feasible set we can restrict to $\tfrac12 \lVert w \rVert^2 \le Cn$ and $\xi_i \le n$ without loss. The constraints also bound $|b|$: if both classes occur, a positive point gives $b \ge 1 - \xi_i - w \cdot \varphi(x_i)$, a negative point gives $b \le -1 + \xi_j - w \cdot \varphi(x_j)$, and both right sides are bounded on the restricted set. Projecting $w$ onto the span of the $\varphi(x_i)$ does not change any $w \cdot \varphi(x_i)$ and does not increase $\lVert w \rVert$, so we can also restrict $w$ to this finite dimensional span. So we minimize a continuous function on a compact set, and a minimizer exists. (If only one class occurs, $b$ can grow without bound, and $w = 0$, $\xi = 0$ with $b = \pm 1$ is optimal.) If two minimizers had different $w$, their midpoint would be feasible, have the same $\sum \xi_i$ part or less (it is linear), and a strictly smaller $\tfrac12 \lVert w \rVert^2$ by strict convexity. This contradicts optimality, so $w$ is unique.

**Lemma 2 (the dual).** The Lagrangian with multipliers $\alpha_i \ge 0$ and $\mu_i \ge 0$ is

$$L = \tfrac12 \lVert w \rVert^2 + C \sum_i \xi_i - \sum_i \alpha_i \bigl(y_i (w \cdot \varphi(x_i) + b) - 1 + \xi_i\bigr) - \sum_i \mu_i \xi_i.$$

Minimizing over $w$, $b$ and $\xi$: the gradient in $w$ is zero at $w = \sum_i \alpha_i y_i \varphi(x_i)$. The term in $b$ is $-b \sum_i \alpha_i y_i$, which is bounded below only if $\sum_i \alpha_i y_i = 0$. The term in $\xi_i$ is $\xi_i (C - \alpha_i - \mu_i)$, bounded below only if $\alpha_i + \mu_i = C$, so $0 \le \alpha_i \le C$. Substituting gives the dual function

$$D(\alpha) = \sum_i \alpha_i - \tfrac12 \sum_{i,j} \alpha_i \alpha_j y_i y_j k(x_i, x_j),$$

to be maximized subject to $0 \le \alpha_i \le C$ and $\sum_i \alpha_i y_i = 0$. Line L3 minimizes $-D(\alpha) = \tfrac12 \alpha^\top Q \alpha - \sum_i \alpha_i$ with $Q$ from lines L1 and L2, so it solves this dual.

**Lemma 3 (weak duality and the gap).** For any primal feasible $(w, b, \xi)$ and dual feasible $\alpha$, with $w_\alpha = \sum_i \alpha_i y_i \varphi(x_i)$,

$$P(w, b, \xi) - D(\alpha) = \tfrac12 \lVert w - w_\alpha \rVert^2 + \sum_i \alpha_i \bigl(y_i f(x_i) - 1 + \xi_i\bigr) + \sum_i (C - \alpha_i) \xi_i \ge 0.$$

*Proof.* Expand: $\tfrac12 \lVert w - w_\alpha \rVert^2 = \tfrac12 \lVert w \rVert^2 - w \cdot w_\alpha + \tfrac12 \lVert w_\alpha \rVert^2$ and $w \cdot w_\alpha = \sum_i \alpha_i y_i w \cdot \varphi(x_i)$. The middle sum equals $\sum_i \alpha_i y_i w \cdot \varphi(x_i) + b \sum_i \alpha_i y_i - \sum_i \alpha_i + \sum_i \alpha_i \xi_i$, and $b \sum_i \alpha_i y_i = 0$. Adding the three terms gives $\tfrac12 \lVert w \rVert^2 + C \sum_i \xi_i - \sum_i \alpha_i + \tfrac12 \lVert w_\alpha \rVert^2 = P - D$, since $\lVert w_\alpha \rVert^2 = \alpha^\top Q \alpha$. Each of the three terms is nonnegative by feasibility. $\square$

**Lemma 4 (strong duality and KKT).** The constraints of (P) are affine and (P) has a solution, so by the linear constraint form of Slater's condition there is a dual optimum $\alpha^*$ with $D(\alpha^*) = p^*$. By Lemma 3, a feasible pair $(w, b, \xi)$ and $\alpha$ are both optimal if and only if all three terms vanish:

1. $w = \sum_i \alpha_i y_i \varphi(x_i)$;
2. $\alpha_i (y_i f(x_i) - 1 + \xi_i) = 0$ for each $i$;
3. $(C - \alpha_i) \xi_i = 0$ for each $i$.

These are the KKT conditions. With $\xi_i = \max(0, 1 - y_i f(x_i))$, they give the three cases of the page. If $\alpha_i = 0$, then (3) gives $\xi_i = 0$, so $y_i f(x_i) \ge 1$. If $0 < \alpha_i < C$, then (3) gives $\xi_i = 0$ and (2) gives $y_i f(x_i) = 1$. If $\alpha_i = C$, then (2) gives $y_i f(x_i) = 1 - \xi_i \le 1$. Conversely, if $\alpha$ is dual feasible, $w$ is given by (1), and $b$ makes the three cases hold, then $\xi_i = \max(0, 1 - y_i f(x_i))$ makes all three terms of Lemma 3 zero, so the gap is zero and both are optimal.

**Lemma 5 (the bias of line L5).** Let $\alpha$ be dual optimal. If some $i$ has $0 < \alpha_i < C$, the KKT conditions force $y_i f(x_i) = 1$, that is $b = y_i - \sum_j \alpha_j y_j K_{ji}$ (using $y_i^2 = 1$). By Lemma 4, an optimal $b$ exists, and every free $i$ gives the same value, so the mean of line L5 is that value. If no $\alpha_i$ is free, the cases of Lemma 4 are a set of inequalities $b \ge \ell_i$ and $b \le u_i$, one per point, and a $b$ satisfying all of them exists by Lemma 4. The feasible set is the interval $[\max \ell_i, \min u_i]$, and its middle is in it. In both cases the returned $(\alpha, b)$ satisfies the KKT conditions, so by Lemma 4 the classifier $f(x) = \sum_i \alpha_i y_i k(x_i, x) + b$ of line L7 is the primal optimum. Line L7 sums only over $i \in SV$, which drops the terms with $\alpha_i = 0$ and does not change $f$.

**Lemma 6 (hard margin is maximum margin).** Suppose the data is linearly separable in feature space and consider the hard margin problem $\min \tfrac12 \lVert w \rVert^2$ subject to $y_i f(x_i) \ge 1$. For a hyperplane $(w, b)$ that separates the data, its geometric margin is $\gamma(w, b) = \min_i y_i f(x_i) / \lVert w \rVert$, and this is invariant under scaling $(w, b)$ by a positive number. Scale so that $\min_i y_i f(x_i) = 1$; then $\gamma = 1/\lVert w \rVert$, and $(w, b)$ is feasible. Conversely, a feasible $(w, b)$ has $\gamma \ge 1/\lVert w \rVert$. So maximizing $\gamma$ over separating hyperplanes is the same as minimizing $\lVert w \rVert$ over the feasible set, and the optimal street between $w \cdot \varphi(x) + b = -1$ and $w \cdot \varphi(x) + b = +1$ has width $2/\lVert w \rVert$. If $C \ge \max_i \alpha_i^{\text{hard}}$ for some hard margin dual optimum, then that $\alpha$ is also feasible for the soft dual, and it satisfies the soft KKT conditions with $\xi = 0$, so the soft and hard margin solutions coincide.

**Theorem.** If line L3 returns an exact dual optimum, SVM-TRAIN returns $(\alpha, b)$ such that the function $f$ of line L7 is $w \cdot \varphi(x) + b$ for the unique optimal $w$ of (P) and an optimal $b$, and SVM-PREDICT returns the sign of this optimal classifier. If line L3 stops when the largest KKT violation is at most $\tau$, the returned point satisfies the KKT conditions within $\tau$, and the gap of Lemma 3 is $O(\tau)$ times $\sum_i \alpha_i + C n$.

*Proof.* The exact case is Lemmas 2, 4 and 5. For the approximate case, the stopping rule bounds every violation of the three cases of Lemma 4 by $\tau$ with the $b$ of line L5, so each term $\alpha_i (y_i f(x_i) - 1 + \xi_i)$ is at most $\alpha_i \tau$ and each $(C - \alpha_i) \xi_i$ is at most $(C - \alpha_i)\tau$, while the first term of Lemma 3 is zero because $w = w_\alpha$. $\square$
