---
title: The list sphere decoder returns the L best vectors, and its LLRs are exact for the full list
proves: [correctness]
status: full
---

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$ of full column rank and $x \in \mathcal{S}^n$, $|\mathcal{S}| = M$. Let $H^H H = R^H R$ with $R$ upper triangular with a positive diagonal (line L1), let $\bar y$ solve $R^H \bar y = H^H y$, and let $c = \|y\|^2 - \|\bar y\|^2$. Write $f(x) = \|y - H x\|^2$ for the metric of $x \in \mathcal{S}^n$.

**Theorem 1 (the triangular metric).** For every $x \in \mathbb{C}^n$, $f(x) = \|\bar y - R x\|^2 + c$.

*Proof.* $f(x) = \|y\|^2 - 2 \,\mathrm{Re}(x^H H^H y) + x^H H^H H x$ and $\|\bar y - R x\|^2 = \|\bar y\|^2 - 2 \,\mathrm{Re}(x^H R^H \bar y) + x^H R^H R x$. Since $R^H \bar y = H^H y$ and $R^H R = H^H H$, the two differ by $\|y\|^2 - \|\bar y\|^2 = c$. $\square$

For $1 \le i \le n$ let $t_i(x_i, \ldots, x_n) = |\bar y_i - \sum_{j > i} R_{ij} x_j - R_{ii} x_i|^2 \ge 0$ and let $D_i = \sum_{l = i}^{n} t_l$, with $D_{n+1} = 0$. Row $i$ of $\bar y - R x$ is the expression inside $t_i$, so $\|\bar y - R x\|^2 = D_1$.

**Lemma 2 (monotone partial metrics).** $D_i$ depends only on $(x_i, \ldots, x_n)$, and $D_i = D_{i+1} + t_i \ge D_{i+1}$. So for every completion $x$ of a partial vector $(x_i, \ldots, x_n)$, $D_1(x) \ge D_i(x_i, \ldots, x_n)$.

*Proof.* Immediate from the definition and $t_l \ge 0$. $\square$

**Lemma 3 (the call invariant).** When SEARCH$(i, D)$ is called, $x_{i+1}, \ldots, x_n$ hold the symbols of the current path and $D = D_{i+1}(x_{i+1}, \ldots, x_n)$. Each $D'$ of line L7 is $D_i$ of the child $(s, x_{i+1}, \ldots, x_n)$, and each list entry inserted by line L9 is a pair $(D_1(x), x)$.

*Proof.* By induction on the depth of the call. The first call is SEARCH$(n, 0)$, and $D_{n+1} = 0$. In a call, line L5 computes $u = \bar y_i - \sum_{j > i} R_{ij} x_j$, so $|u - R_{ii} s|^2 = t_i(s, x_{i+1}, \ldots, x_n)$ and $D' = D_{i+1} + t_i = D_i$. Line L9 sets $x_i = s$ before line L10 calls SEARCH$(i - 1, D')$, so the invariant holds for the child call. At $i = 1$ the inserted value is $D_1(x)$. $\square$

By Lemma 3 and Theorem 1, every metric returned by line L4 is $D_1(x) + c = f(x)$.

Let $\rho$ denote the value of radius. It is $\infty$ until the list holds $L$ entries, and after that it is the largest metric $D_1$ in the list. An insertion into a full list either does not change the list (the new metric is the largest and is dropped) or replaces the largest entry by a smaller one, so $\rho$ never grows.

**Lemma 4 (the break is safe).** Line L8 never prevents the insertion of a vector $x$ with $D_1(x) < \rho_{\mathrm{end}}$, where $\rho_{\mathrm{end}}$ is the final radius.

*Proof.* Line L6 orders the children by $t_i$, and $D$ is common to all children, so the values $D'$ increase along the loop. When line L8 breaks at a child with $D' \ge \rho$, every later child of the same node has an even larger $D'$. Every completion $x$ of any of these children has $D_1(x) \ge D' \ge \rho \ge \rho_{\mathrm{end}}$ by Lemma 2 and the fact that $\rho$ never grows. So no vector with $D_1(x) < \rho_{\mathrm{end}}$ is lost. $\square$

**Theorem 5 (the list is the L best).** Assume $L \le M^n$. At the end, the list holds $L$ distinct vectors, and no vector of $\mathcal{S}^n$ outside the list has a smaller metric than a vector inside it. That is, the list is a set of $L$ vectors with the smallest metrics (with an arbitrary choice among equal metrics at the boundary).

*Proof.* First, the list becomes full. While $\rho = \infty$, the test of line L8 never succeeds, so the search visits leaves until $L$ of them have been inserted. There are $M^n \ge L$ distinct leaves, and each leaf is visited at most once, because each path of symbols is visited at most once by the depth-first loop.

Now let $x$ be a vector outside the final list and $z$ a vector inside it. Suppose $D_1(x) < D_1(z)$. Then $D_1(x) < \rho_{\mathrm{end}}$, because $\rho_{\mathrm{end}}$ is the largest metric in the final list. By Lemma 4, no break removed $x$, so the search reached the leaf $x$, and line L9 inserted it. At that time $\rho \ge \rho_{\mathrm{end}} > D_1(x)$, so $x$ stayed in the list: if the list was not full, nothing was dropped, and if it was full, the dropped entry had the largest metric, at least $\rho > D_1(x)$. A later insertion drops one entry with the largest metric of $L + 1$ entries. That metric is at least the new radius, which is at least $\rho_{\mathrm{end}} > D_1(x)$, so it is never $x$. So $x$ is in the final list, a contradiction. $\square$

**Corollary 6 (the two limits).** With $L = 1$, the only vector in the list minimizes $f$ over $\mathcal{S}^n$, so it is an ML decision. With $L = M^n$, the list holds all of $\mathcal{S}^n$ with their metrics.

For stream $k$ and bit $j$, let $b_{k,j}(x)$ be bit $j$ of the label of $x_k$. With equal priors, the posterior probability of $x$ is proportional to $e^{-f(x) / N_0}$, so the exact LLR is

$$\Lambda_{k,j} = \ln \sum_{x : b_{k,j}(x) = 0} e^{-f(x) / N_0} - \ln \sum_{x : b_{k,j}(x) = 1} e^{-f(x) / N_0}.$$

**Theorem 7 (exact LLRs for the full list).** With $L = M^n$, the log-sum-exp LLRs computed from the list equal $\Lambda_{k,j}$, and the max-log LLRs from the list equal $(\min_{b = 1} f - \min_{b = 0} f) / N_0$ over all of $\mathcal{S}^n$.

*Proof.* By Corollary 6 the list is $\mathcal{S}^n$ with the true metrics $f(x)$. Both bit values occur in $\mathcal{S}^n$, so no clipping applies, and the two sums of the list are the two sums of $\Lambda_{k,j}$. For max-log, $\max(-f / N_0) = -\min f / N_0$ in each part. $\square$

**Theorem 8 (max-log from a shorter list).** For any $L$, if both values of bit $b_{k,j}$ occur in the list, the max-log LLR from the list equals the max-log LLR over all of $\mathcal{S}^n$.

*Proof.* Let $\hat x$ be the first vector of the list, an ML vector by Theorem 5, and let $v = b_{k,j}(\hat x)$. Then $\min_{b = v} f = f(\hat x)$, and it is in the list. Let $x^\ast$ minimize $f$ over the vectors with $b_{k,j} = 1 - v$. Some vector $z$ of the list has $b_{k,j}(z) = 1 - v$, so $f(z) \ge f(x^\ast)$. If $x^\ast$ were not in the list, then by Theorem 5, $f(x^\ast) \ge f(z')$ for every $z'$ in the list, and so $f(x^\ast) \ge f(z)$. Then $f(z) = f(x^\ast)$ and $z$ is also a minimizer with bit value $1 - v$. In both cases the list holds a vector with bit value $1 - v$ and metric $\min_{b = 1 - v} f$. So both minimums of the max-log formula are attained in the list. $\square$

When only one value of a bit occurs in the list, the true minimum metric of the other value is at least the largest metric in the list, by Theorem 5. So the true max-log LLR has the sign of the clipped value and a magnitude of at least $(\rho_{\mathrm{end}} - f(\hat x)) / N_0$. The clipping level $\Lambda_{\max}$ replaces this unknown magnitude.
