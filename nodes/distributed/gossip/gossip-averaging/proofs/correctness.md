---
title: Randomized gossip averaging converges to the average, with the upper bound of Theorem 3
proves: [correctness]
status: full
---

**Claim.** Let $G$ be a graph on $n$ nodes and $P$ a stochastic matrix with $P_{ij} > 0$ only on edges. Run the algorithm from any $x(0) \in \mathbb{R}^n$ and let $\bar x = \frac1n \mathbf 1^T x(0)$ and $e(k) = x(k) - \bar x \mathbf 1$. Then (1) $\mathbf 1^T x(k) = n\bar x$ for all $k$; (2) $\lVert e(k+1) \rVert \le \lVert e(k) \rVert$ in every run; (3) $\mathbb{E} \lVert e(k) \rVert^2 \le \lambda_2(\bar W)^k \lVert e(0) \rVert^2$; (4) $\Pr(\lVert e(k) \rVert \ge \varepsilon \lVert x(0) \rVert) \le \varepsilon$ for all $k \ge 3 \log \varepsilon^{-1} / \log \lambda_2(\bar W)^{-1}$ and $0 < \varepsilon < 1$; (5) $x(k) \to \bar x \mathbf 1$ with probability 1 for every input if and only if $\lambda_2(\bar W) < 1$.

**Setup.** At tick $k$ the node $i$ is uniform, and $j$ is chosen with probability $P_{ij}$, independently of the past. So $x(k+1) = W(k) x(k)$, where $W(k) = W_{ij}$ with probability $P_{ij}/n$, and

$$W_{ij} = I - \tfrac12 v v^T, \qquad v = e_i - e_j.$$

Lines L5 and L6 of the pseudocode compute exactly $W_{ij} x$: the entries $i$ and $j$ become $(x_i + x_j)/2$ and the others stay.

**Step 1 (projection).** $v^T v = 2$, so $(vv^T)^2 = v (v^T v) v^T = 2 vv^T$. Hence $W_{ij}^2 = I - vv^T + \frac14 \cdot 2 vv^T = W_{ij}$, and $W_{ij}^T = W_{ij}$. So $W_{ij}$ is an orthogonal projection. Also $W_{ij} \mathbf 1 = \mathbf 1$ and $\mathbf 1^T W_{ij} = \mathbf 1^T$, because $v^T \mathbf 1 = 0$.

**Proof of (1).** $\mathbf 1^T x(k+1) = \mathbf 1^T W(k) x(k) = \mathbf 1^T x(k)$, and induction on $k$ gives the claim.

**Proof of (2).** By (1), $\bar x$ is the mean of $x(k)$ for every $k$. Then $e(k+1) = W(k) x(k) - \bar x W(k) \mathbf 1 = W(k) e(k)$. An orthogonal projection $Q$ satisfies $\lVert Qy \rVert^2 = y^T Q^T Q y = y^T Q y \le \lVert y \rVert^2$, since the eigenvalues of $Q$ are 0 and 1. So $\lVert e(k+1) \rVert \le \lVert e(k) \rVert$.

**Proof of (3).** Condition on $e(k)$. By Step 1, $\lVert e(k+1) \rVert^2 = e(k)^T W(k)^T W(k) e(k) = e(k)^T W(k) e(k)$. The choice at tick $k$ is independent of $e(k)$, so

$$\mathbb{E}\big[\lVert e(k+1) \rVert^2 \mid e(k)\big] = e(k)^T \bar W e(k), \qquad \bar W = \sum_{i,j} \frac{P_{ij}}{n} W_{ij}.$$

$\bar W$ is symmetric, and it is a convex combination of projections, so it is positive semidefinite with eigenvalues in $[0, 1]$. It has $\bar W \mathbf 1 = \mathbf 1$, so $\mathbf 1$ is an eigenvector of $\lambda_1 = 1$, and the other eigenvectors can be chosen orthogonal to $\mathbf 1$. Since $\mathbf 1^T e(k) = 0$, the vector $e(k)$ lies in their span, and $e(k)^T \bar W e(k) \le \lambda_2(\bar W) \lVert e(k) \rVert^2$. Taking expectations and using induction on $k$ gives $\mathbb{E}\lVert e(k) \rVert^2 \le \lambda_2(\bar W)^k \lVert e(0) \rVert^2$.

**Proof of (4).** $\lVert e(0) \rVert \le \lVert x(0) \rVert$, because $e(0)$ is the orthogonal projection of $x(0)$ onto $\mathbf 1^\perp$. By Markov's inequality applied to $\lVert e(k) \rVert^2$ and by (3),

$$\Pr\big(\lVert e(k) \rVert \ge \varepsilon \lVert x(0) \rVert\big) \le \frac{\mathbb{E}\lVert e(k) \rVert^2}{\varepsilon^2 \lVert x(0) \rVert^2} \le \frac{\lambda_2(\bar W)^k}{\varepsilon^2}.$$

If $\lambda_2(\bar W) = 0$, the right side is 0 for $k \ge 1$. Otherwise, for $k \ge 3 \log \varepsilon^{-1} / \log \lambda_2(\bar W)^{-1}$ we have $\lambda_2(\bar W)^k \le \varepsilon^3$, so the probability is at most $\varepsilon$. This is the upper bound of Theorem 3 of Boyd et al.

**Proof of (5).** First let $\lambda = \lambda_2(\bar W) < 1$ and fix $\delta > 0$. By Markov's inequality and (3), $\Pr(\lVert e(k) \rVert > \delta) \le \lambda^k \lVert e(0) \rVert^2 / \delta^2$, and these bounds have a finite sum over $k$. By the Borel-Cantelli lemma, with probability 1 only finitely many $k$ have $\lVert e(k) \rVert > \delta$. Taking $\delta = 1/r$ for $r = 1, 2, \ldots$ and a countable union of null events, $e(k) \to 0$ with probability 1.

Now let $\lambda_2(\bar W) = 1$. Expand $\bar W = I - \frac{1}{2n} \sum_{i,j} P_{ij} (e_i - e_j)(e_i - e_j)^T$, so $y^T (I - \bar W) y = \frac{1}{2n} \sum_{i,j} P_{ij} (y_i - y_j)^2$. A unit vector $y \perp \mathbf 1$ with $y^T \bar W y = 1$ has $y_i = y_j$ whenever $P_{ij} + P_{ji} > 0$. If the graph $H$ of these pairs were connected, $y$ would be constant, which contradicts $y \perp \mathbf 1$ and $y \ne 0$. So $H$ has at least two components. An exchange uses only pairs of $H$, so the sum of each component is kept, by the argument of (1). Take an input whose components have different averages: no run converges to $\bar x \mathbf 1$. $\square$
