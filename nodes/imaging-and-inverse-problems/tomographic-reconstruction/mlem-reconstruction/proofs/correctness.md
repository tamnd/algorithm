---
title: Monotone likelihood and fixed points of MLEM
proves: [correctness]
status: full
---

We use the notation of the page. $A$ is an $m \times N$ matrix with $a_{ij} \ge 0$, every column sum $s_j = \sum_i a_{ij}$ is positive (a pixel with $s_j = 0$ is removed; the code sets it to 0), $b \ge 0$ is the known background and $y \ge 0$ holds the counts. For $x \ge 0$ put $\bar y = A x + b$ and
$$L(x) = \sum_i \big[y_i \log \bar y_i - \bar y_i\big],$$
the Poisson log-likelihood without the constant $-\sum_i \log y_i!$. A term with $y_i = 0$ is $-\bar y_i$. We call $x \ge 0$ *admissible* if $\bar y_i > 0$ for each $i$ with $y_i > 0$; then $L(x)$ is finite. Lines L4 to L7 map an admissible $x$ to
$$x'_j = \frac{x_j}{s_j} \sum_i a_{ij} \frac{y_i}{\bar y_i}, \tag{1}$$
where the sum runs over the rays with $y_i > 0$ (line L5 sets the other ratios to 0). We work in exact arithmetic.

**Lemma 1 (admissible and positive).** If $x$ is admissible, then $x' \ge 0$, and $x'_j = 0$ if and only if $x_j = 0$ or no ray with $a_{ij} > 0$ has $y_i > 0$. If $x > 0$ and every ray with $y_i > 0$ has a positive entry or $b_i > 0$, then $x'$ is admissible.

*Proof.* Every factor in (1) is nonnegative, and the sum is positive exactly when some ray with $a_{ij} > 0$ has $y_i > 0$. For the second claim, let $y_i > 0$. If $b_i > 0$ then $\bar y'_i \ge b_i > 0$. Otherwise some $a_{ij} > 0$; for this $j$ the ray $i$ itself has $a_{ij} > 0$ and $y_i > 0$, so $x'_j > 0$ by the first claim, and $\bar y'_i \ge a_{ij} x'_j > 0$. $\square$

So from a positive start the iteration is well defined at every step, and a pixel can only reach 0 if no ray that sees it has counts.

**Lemma 2 (the surrogate).** Let $x$ be admissible, let $J = \{j : x_j > 0\}$, and for every $x' \ge 0$ define
$$Q(x'; x) = \sum_i y_i \Big[\log \bar y_i + \sum_{j \in J} \frac{a_{ij} x_j}{\bar y_i} \log \frac{x'_j}{x_j}\Big] - \sum_i \bar y'_i,$$
with the terms of rays with $y_i = 0$ left out of the first sum, and $\log 0 = -\infty$. Then $L(x') \ge Q(x'; x)$ and $L(x) = Q(x; x)$.

*Proof.* The second claim is clear, because $\log(x_j/x_j) = 0$. For the first, fix a ray with $y_i > 0$, so $\bar y_i > 0$. The weights $w_{ij} = a_{ij} x_j / \bar y_i$ for $j \in J$ and $w_{i0} = b_i / \bar y_i$ are nonnegative and sum to 1. Write
$$\bar y'_i \ge \sum_{j \in J} a_{ij} x'_j + b_i = \sum_{j \in J} w_{ij} \Big(\bar y_i \frac{x'_j}{x_j}\Big) + w_{i0}\, \bar y_i,$$
where the terms with $w_{ij} = 0$ are dropped. The logarithm is concave and increasing, so Jensen's inequality gives
$$\log \bar y'_i \ge \sum_{j \in J} w_{ij} \log\Big(\bar y_i \frac{x'_j}{x_j}\Big) + w_{i0} \log \bar y_i = \log \bar y_i + \sum_{j \in J} w_{ij} \log \frac{x'_j}{x_j}.$$
Multiply by $y_i > 0$, sum over these rays and subtract $\sum_i \bar y'_i$ on both sides. $\square$

**Theorem 1 (monotone likelihood).** Let $x$ be admissible and let $x'$ be given by (1). Then $L(x') \ge L(x)$, with equality only if $x' = x$.

*Proof.* Put $e_j = x_j \sum_i a_{ij} y_i / \bar y_i$, so that $x'_j = e_j / s_j$ and $e_j = 0$ for $j \notin J$. Since $\sum_i \bar y'_i = \sum_j s_j x'_j + \sum_i b_i$, the surrogate is
$$Q(x'; x) = C(x) + \sum_{j \in J} e_j \log x'_j - \sum_j s_j x'_j,$$
with $C(x)$ independent of $x'$. It is a sum of functions of one variable each. For $e_j > 0$ the function $t \mapsto e_j \log t - s_j t$ is strictly concave on $t > 0$ and has its unique maximum at $t = e_j / s_j$. For $e_j = 0$ the function $t \mapsto -s_j t$ has its unique maximum on $t \ge 0$ at $t = 0 = e_j / s_j$. So $x'$ of (1) is the unique maximizer of $Q(\cdot\,; x)$ over $x' \ge 0$, and by Lemma 2
$$L(x') \ge Q(x'; x) \ge Q(x; x) = L(x).$$
If $x' \ne x$, the middle inequality is strict, because the maximizer is unique. $\square$

**Theorem 2 (the total count).** If $b = 0$, then $\sum_j s_j x'_j = \sum_i y_i$ for every admissible $x$.

*Proof.* By (1), $\sum_j s_j x'_j = \sum_i \frac{y_i}{\bar y_i} \sum_j a_{ij} x_j = \sum_i y_i$, the sum over the rays with $y_i > 0$, because $\bar y_i = \sum_j a_{ij} x_j$ when $b = 0$. $\square$

So with $b = 0$ the expected total count $\sum_i \bar y_i$ equals the measured total count after the first iteration.

**Theorem 3 (fixed points).** An admissible $x$ is a fixed point of (1) if and only if $\partial L / \partial x_j = 0$ for every $j$ with $x_j > 0$. A maximizer of $L$ over $x \ge 0$ is a fixed point. A fixed point $x$ is a maximizer if and only if also $\partial L / \partial x_j \le 0$ for every $j$ with $x_j = 0$.

*Proof.* The gradient is $\partial L / \partial x_j = \sum_i a_{ij} y_i / \bar y_i - s_j$. For $x_j > 0$, (1) gives $x'_j = x_j$ if and only if $\sum_i a_{ij} y_i / \bar y_i = s_j$, that is $\partial L / \partial x_j = 0$. For $x_j = 0$, (1) gives $x'_j = 0$ always. The function $L$ is concave on the admissible set, because each $\log \bar y_i$ is the logarithm of an affine function and $-\bar y_i$ is affine. For a concave differentiable function on the orthant, $x$ is a maximizer if and only if the KKT conditions hold: $\partial L / \partial x_j \le 0$ for all $j$, with equality where $x_j > 0$. Both claims follow. $\square$

A fixed point with a zero pixel need not be a maximizer: a start with $x_j = 0$ keeps $x_j = 0$ for ever. This is why the start must be positive.

**Convergence (cited, not proved here).** For $b = 0$ and a positive start, the iterates converge to a maximizer of $L$ over $x \ge 0$. Vardi, Shepp and Kaufman (1985) gave the argument for emission tomography, and Csiszar and Tusnady (1984) proved it for the alternating minimization of the Kullback-Leibler divergence, of which MLEM with $b = 0$ is a special case. Theorem 1 alone does not give convergence of the iterates: it gives a nondecreasing sequence $L(x^k)$ that is bounded above, since $y_i \log t - t \le y_i \log y_i - y_i$ for every $t > 0$.
