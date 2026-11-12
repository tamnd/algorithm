---
title: The bandwidth search of SNE finds the unique precision for the target perplexity, and the SNE gradient is correct
proves: [correctness]
status: full
---

We use the notation of the page. Fix a point $i$ and write $D_j = \|x_i - x_j\|^2$ for $j \ne i$. For a precision $\beta = 1/(2\sigma_i^2) \ge 0$ let

$$p_j(\beta) = \frac{e^{-\beta D_j}}{Z(\beta)}, \qquad Z(\beta) = \sum_{k \ne i} e^{-\beta D_k},$$

and let $H(\beta) = -\sum_{j \ne i} p_j \ln p_j$ be the entropy in nats. The perplexity is $e^{H} = 2^{H/\ln 2}$, so a target perplexity $u$ is the same as the target entropy $\ln u$ in any base. Let $M$ be the set of indices $j$ with the smallest $D_j$, and let $|M|$ be its size.

## Part 1: the bandwidth search

**Lemma 1.** $H(\beta) = \ln Z(\beta) + \beta\, \mathbb{E}_\beta[D]$, where $\mathbb{E}_\beta$ is the mean under $p(\beta)$.

*Proof.* $\ln p_j = -\beta D_j - \ln Z$. Multiply by $-p_j$ and add over $j$. Since $\sum_j p_j = 1$, the sum is $\beta \sum_j p_j D_j + \ln Z$. $\square$

**Lemma 2.** $H'(\beta) = -\beta \operatorname{Var}_\beta(D)$.

*Proof.* $Z'(\beta) = -\sum_j D_j e^{-\beta D_j}$, so $(\ln Z)' = -\mathbb{E}_\beta[D]$. Also $p_j'(\beta) = p_j (\mathbb{E}_\beta[D] - D_j)$ by the quotient rule, so

$$\frac{d}{d\beta} \mathbb{E}_\beta[D] = \sum_j D_j p_j (\mathbb{E}_\beta[D] - D_j) = \mathbb{E}_\beta[D]^2 - \mathbb{E}_\beta[D^2] = -\operatorname{Var}_\beta(D).$$

By Lemma 1, $H' = -\mathbb{E}_\beta[D] + \mathbb{E}_\beta[D] + \beta \cdot (-\operatorname{Var}_\beta(D)) = -\beta \operatorname{Var}_\beta(D)$. $\square$

**Lemma 3.** If the $D_j$ are not all equal, $H$ is continuous and strictly decreasing on $[0, \infty)$, $H(0) = \ln(n-1)$ and $H(\beta) \to \ln |M|$ as $\beta \to \infty$.

*Proof.* Every $p_j(\beta)$ is positive. So $\operatorname{Var}_\beta(D) > 0$ when the $D_j$ are not all equal, and $H'(\beta) < 0$ for $\beta > 0$ by Lemma 2. At $\beta = 0$ all $p_j = 1/(n-1)$, so $H(0) = \ln(n-1)$. Let $D_{\min}$ be the smallest distance. Then $p_j = e^{-\beta(D_j - D_{\min})} / \sum_k e^{-\beta (D_k - D_{\min})}$. As $\beta \to \infty$, the terms with $D_j > D_{\min}$ tend to $0$ and the $|M|$ terms with $D_j = D_{\min}$ equal $1$. So $p$ tends to the uniform distribution on $M$, and $H \to \ln |M|$ because $H$ is a continuous function of $p$. $\square$

**Theorem 1.** If the $D_j$ are not all equal and $|M| < u < n - 1$, there is exactly one $\beta^* > 0$ with $H(\beta^*) = \ln u$. The search of the page brackets $\beta^*$ and halves the bracket in each step after the first upper end is found, so it reaches $|H(\beta) - \ln u| \le \tau$ for each tolerance $\tau > 0$ after finitely many steps.

*Proof.* Existence follows from Lemma 3 and the intermediate value theorem, since $H(0) > \ln u > \lim_{\beta\to\infty} H(\beta)$. Uniqueness follows from strict monotonicity.

The search keeps two ends $lo < hi$ (with $hi = \infty$ at the start) and the invariant $H(lo) \ge \ln u \ge H(hi)$, read as true when $hi = \infty$. At the start $lo = 0$, and $H(0) = \ln(n-1) > \ln u$. If $H(\beta) > \ln u$, then $\beta < \beta^*$ and the search sets $lo \leftarrow \beta$. If $H(\beta) < \ln u$, then $\beta > \beta^*$ and the search sets $hi \leftarrow \beta$. So $\beta^* \in [lo, hi]$ at all times.

While $hi = \infty$ the search doubles $\beta$. Since $H(\beta) \to \ln|M| < \ln u$, there is a finite $\beta_1$ with $H(\beta_1) < \ln u$, and the doubling passes $\beta_1$ after at most $\lceil \log_2 \beta_1 \rceil + 1$ steps from $\beta = 1$. From then on, each step sets $\beta$ to the midpoint of $[lo, hi]$ and replaces one end by it, so the length of the bracket drops by the factor $2$ in each step. After $s$ steps it is at most $L / 2^s$, where $L$ is the first finite length.

On the bracket, $|H'(\beta)| = \beta \operatorname{Var}_\beta(D) \le hi_0 \cdot D_{\max}^2 =: K$ by Lemma 2, where $hi_0$ is the first finite upper end. So $|H(\beta) - \ln u| = |H(\beta) - H(\beta^*)| \le K |\beta - \beta^*| \le K L / 2^s$, which is at most $\tau$ once $s \ge \log_2(K L / \tau)$. $\square$

When $u \le |M|$ the target is not reached at a finite $\beta$: for $u = |M|$ the entropy only tends to it. The page lists this as a pitfall.

## Part 2: the gradient

Let $d_{jk} = \|y_j - y_k\|^2$, $Z_i = \sum_{k \ne i} e^{-d_{ik}}$ and $q_{j|i} = e^{-d_{ij}} / Z_i$. The cost is

$$C = \sum_i \sum_{j \ne i} p_{j|i} \ln \frac{p_{j|i}}{q_{j|i}}.$$

**Theorem 2.** $\dfrac{\partial C}{\partial y_l} = 2 \sum_{j \ne l} \big(p_{j|l} - q_{j|l} + p_{l|j} - q_{l|j}\big)(y_l - y_j)$.

*Proof.* The $p_{j|i}$ do not depend on $y$. Since $\ln q_{j|i} = -d_{ij} - \ln Z_i$ and $\sum_{j \ne i} p_{j|i} = 1$,

$$C = \text{const} + \sum_i \sum_{j \ne i} p_{j|i} d_{ij} + \sum_i \ln Z_i.$$

We use $\partial d_{jk} / \partial y_j = 2(y_j - y_k)$.

*The first sum.* The terms that hold $y_l$ have $i = l$ or $j = l$. They give $\sum_{j} p_{j|l} \cdot 2(y_l - y_j) + \sum_{i} p_{l|i} \cdot 2(y_l - y_i)$. Rename $i$ as $j$ in the second part: the total is $2 \sum_{j \ne l} (p_{j|l} + p_{l|j})(y_l - y_j)$.

*The second sum.* For $i = l$, $\partial \ln Z_l / \partial y_l = \frac{1}{Z_l} \sum_k e^{-d_{lk}} \cdot (-2)(y_l - y_k) = -2 \sum_k q_{k|l} (y_l - y_k)$. For $i \ne l$, only the term $k = l$ of $Z_i$ holds $y_l$, so $\partial \ln Z_i / \partial y_l = \frac{1}{Z_i} e^{-d_{il}} \cdot (-2)(y_l - y_i) = -2 q_{l|i}(y_l - y_i)$. The total is $-2 \sum_{j \ne l} (q_{j|l} + q_{l|j})(y_l - y_j)$.

Add the two totals. $\square$

## What is not claimed

The cost $C$ is not convex in $y$, and gradient descent can stop at a local minimum or a saddle point. Theorem 2 only says that the update of the page moves along the exact negative gradient (with momentum), so for a small enough step size each plain gradient step without momentum and jitter does not increase $C$ when $C$ has a Lipschitz gradient near the current map.
