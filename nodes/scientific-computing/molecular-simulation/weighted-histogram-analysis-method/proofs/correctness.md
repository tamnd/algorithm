---
title: The WHAM equations as maximum likelihood and as the minimum of a convex function, and the uniqueness of the solution
proves: [correctness]
status: full
---

Fix $K$ windows and $B$ bins, counts $n_k(b) \ge 0$ with $N_k = \sum_b n_k(b) > 0$ for every $k$, finite biases $w_k(b)$, and $\beta > 0$. Let $n(b) = \sum_k n_k(b)$ and $N = \sum_k N_k = \sum_b n(b)$. Let $\mathcal B = \{b : n(b) > 0\}$, which is not empty. For $f \in \mathbb R^K$ write
$$D_b(f) = \sum_k N_k\, e^{\beta (f_k - w_k(b))}, \qquad L(f) = \sum_{b \in \mathcal B} n(b) \ln D_b(f) - \beta \sum_k N_k f_k.$$

**Claim 1 (maximum likelihood).** Model the counts of window $k$ as $N_k$ independent draws from the bin probabilities $q_k(b) = p(b) e^{-\beta w_k(b)} / c_k(p)$ with $c_k(p) = \sum_{b'} p(b') e^{-\beta w_k(b')}$, for an unknown $p$ in the simplex. At any maximizer of the likelihood with $p(b) > 0$ on $\mathcal B$, the WHAM equations hold:
$$p(b) = \frac{n(b)}{\sum_k N_k\, e^{\beta (f_k - w_k(b))}}, \qquad e^{-\beta f_k} = \sum_b p(b)\, e^{-\beta w_k(b)}.$$

*Proof.* Up to a constant, the log-likelihood is $\ell(p) = \sum_k \sum_b n_k(b) \ln q_k(b) = \sum_b n(b) \ln p(b) - \sum_k N_k \ln c_k(p) + \text{const}$. If a bin $b_0$ with $n(b_0) = 0$ has mass $\epsilon > 0$, set it to 0 and divide the rest by $1 - \epsilon$. The first term grows by $-N \ln(1 - \epsilon)$, and each $\ln c_k$ changes by $\ln(1 - \epsilon e^{-\beta w_k(b_0)} / c_k) - \ln(1 - \epsilon)$, so $\ell$ changes by $-\sum_k N_k \ln(1 - \epsilon e^{-\beta w_k(b_0)} / c_k) > 0$. So a maximizer puts $p(b) = 0$ on bins outside $\mathcal B$, which agrees with the first equation. On $\mathcal B$, with a Lagrange multiplier $\mu$ for $\sum_b p(b) = 1$, the stationarity condition is
$$\frac{n(b)}{p(b)} - \sum_k N_k \frac{e^{-\beta w_k(b)}}{c_k(p)} = \mu.$$
Multiply by $p(b)$ and sum over $b$: the left side gives $N - \sum_k N_k = 0$, so $\mu = 0$. Define $f_k$ by $e^{-\beta f_k} = c_k(p)$, which is the second equation. Then the condition reads $n(b) / p(b) = \sum_k N_k e^{\beta f_k} e^{-\beta w_k(b)}$, the first equation. $\square$

**Claim 2 (fixed points and the convex function).** $f$ is a fixed point of lines L3 to L5 if and only if $\nabla L(f) = 0$ and the $p$ of line L3 already sums to 1. Every stationary point is mapped in one step to a fixed point on the same line $f + c\mathbf 1$.

*Proof.* $\partial L / \partial f_k = \beta N_k e^{\beta f_k} \sum_{b} r(b) e^{-\beta w_k(b)} - \beta N_k$, where $r(b) = n(b) / D_b(f)$ is the unnormalized $p$ of line L3. For every $f$,
$$\sum_k N_k e^{\beta f_k} \sum_b r(b) e^{-\beta w_k(b)} = \sum_b r(b) D_b(f) = \sum_b n(b) = N. \qquad (*)$$
Let $z = \sum_b r(b)$. Lines L4 and L5 map $f$ to $f'$ with $e^{-\beta f'_k} = z^{-1} \sum_b r(b) e^{-\beta w_k(b)}$.

If $\nabla L(f) = 0$, then $e^{\beta f_k} \sum_b r(b) e^{-\beta w_k(b)} = 1$ for every $k$, so $e^{-\beta f'_k} = z^{-1} e^{-\beta f_k}$ and $f' = f + \beta^{-1} (\ln z)\, \mathbf 1$. Moving every $f_k$ by $c$ multiplies every $D_b$ by $e^{\beta c}$ and so $r$ and $z$ by $e^{-\beta c}$; hence $f'$ has $z = 1$, and $\nabla L(f') = 0$ by the invariance of Claim 3. So a stationary point is a fixed point exactly when $z = 1$, and one step maps any stationary point to the point of its line with $z = 1$. This proves the direction "stationary implies fixed" in that normalized sense: the stationary points with $z = 1$ are fixed points.

Conversely, let $f' = f$. Then $e^{\beta f_k} \sum_b r(b) e^{-\beta w_k(b)} = z$ for every $k$. Put this in $(*)$: $\sum_k N_k z = N$, so $z = 1$, and then $\partial L / \partial f_k = \beta N_k (z - 1) = 0$. $\square$

**Claim 3 (uniqueness).** $L$ is convex and $L(f + c \mathbf 1) = L(f)$ for every $c$. For every $v$ that is not a multiple of $\mathbf 1$, $t \mapsto L(f + t v)$ is strictly convex and tends to $+\infty$ as $t \to \pm\infty$. Hence $L$ has a minimizer, the set of minimizers is exactly one line $\{f^* + c \mathbf 1\}$, and the normalized $p$ of the WHAM equations is unique.

*Proof.* Invariance: $D_b(f + c\mathbf 1) = e^{\beta c} D_b(f)$, so the first term grows by $\beta c \sum_b n(b) = \beta c N$ and the second falls by $\beta c \sum_k N_k = \beta c N$.

Convexity: $\ln D_b(f)$ is a log-sum-exp of affine functions of $f$. With $\pi_k(b) = N_k e^{\beta(f_k - w_k(b))} / D_b(f)$, so that $\sum_k \pi_k(b) = 1$, its Hessian is $\beta^2 (\mathrm{diag}(\pi(b)) - \pi(b) \pi(b)^T)$, so
$$v^T \nabla^2 L(f)\, v = \beta^2 \sum_{b \in \mathcal B} n(b)\, \mathrm{var}_{\pi(b)}(v) \ge 0,$$
where $\mathrm{var}_{\pi(b)}(v) = \sum_k \pi_k(b) v_k^2 - (\sum_k \pi_k(b) v_k)^2$. All $\pi_k(b) > 0$ because $N_k > 0$ and the biases are finite, so this variance is 0 only if $v$ is constant. Since $\mathcal B$ is not empty, the second derivative along $v$ is positive when $v$ is not a multiple of $\mathbf 1$, which gives strict convexity along such lines.

Growth: as $t \to +\infty$, $\ln D_b(f + tv) = \beta t \max_k v_k + O(1)$, so $L(f + tv) = \beta t\,(N \max_k v_k - \sum_k N_k v_k) + O(1)$. The bracket is positive when $v$ is not constant, because $\sum_k N_k v_k$ is an average of the $v_k$ with positive weights $N_k / N$, times $N$. The case $t \to -\infty$ is the same with $-v$.

Existence and uniqueness: restrict $L$ to the subspace $H = \{f : \sum_k f_k = 0\}$, which meets each line $f + c \mathbf 1$ once. On $H$, $L$ is continuous, strictly convex, and tends to $+\infty$ along every ray, so (a convex function that grows along every ray of a finite-dimensional space is coercive) it has exactly one minimizer $f^*$ on $H$. By the invariance, the minimizers in $\mathbb R^K$ are $f^* + c \mathbf 1$. By Claim 2, exactly one of them has $z = 1$, and its $p(b) = n(b) / D_b(f^*)$ normalized is the same for every point of the line, since the scaling of $r$ cancels in the normalization. $\square$

**Claim 4 (exact data).** Let $p^\circ$ be a probability vector with $p^\circ(b) > 0$ on every bin, $e^{-\beta f^\circ_k} = \sum_b p^\circ(b) e^{-\beta w_k(b)}$, and suppose $n_k(b) = N_k\, p^\circ(b) e^{-\beta (w_k(b) - f^\circ_k)}$ exactly. Then $(p^\circ, f^\circ)$ solves the WHAM equations, so by Claim 3 WHAM returns $p^\circ$.

*Proof.* $n(b) = p^\circ(b) \sum_k N_k e^{\beta (f^\circ_k - w_k(b))} = p^\circ(b) D_b(f^\circ)$, which is the first equation. The second holds by the definition of $f^\circ$. $\square$

The counts in Claim 4 need not be integers: the equations and $L$ are defined for real nonnegative counts, which is how the code checks the equations on exact data.

**Remark (no claim about the iteration).** Claims 2 and 3 show that the iteration can only stop at the right answer. They do not show that it converges, or how fast. The iteration counts on the page are measurements. A safe solver minimizes $L$ directly, for example with Newton's method and a line search, which converges for a strictly convex coercive function.
