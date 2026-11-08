---
title: Shepard's interpolant interpolates, stays within the data range, and has flat spots for p > 1
proves: [correctness, termination]
status: full
---

**Setting.** Sites $x_1, \ldots, x_N \in \mathbb{R}^d$, values $y_1, \ldots, y_N$, a power $p > 0$, and $r_i(x) = \|x - x_i\|$. Let $D = \{x_1, \ldots, x_N\}$. For $x \notin D$ the algorithm returns $s(x) = \sum_i w_i y_i / \sum_i w_i$ with $w_i = r_i^{-p}$ (lines L1, L3, L4); for $x \in D$ it returns the mean of the $y_i$ with $x_i = x$ (line L2). We assume the sites are distinct for Lemmas 2 and 3 (a repeated site with several values has no continuous interpolant).

**Lemma 1 (convex combination).** For $x \notin D$, $s(x) = \sum_i u_i(x) y_i$ with $u_i = w_i / \sum_j w_j$, $u_i > 0$ and $\sum_i u_i = 1$. Hence $\min_i y_i \le s(x) \le \max_i y_i$, and if all $y_i = c$ then $s(x) = c$.

*Proof.* Each $r_i(x) > 0$, so $w_i > 0$ and the denominator is positive. The $u_i$ are positive and sum to 1 by construction, so $s(x)$ is a convex combination of the $y_i$, which lies between their minimum and maximum and equals $c$ when they all equal $c$. For $x \in D$, the returned mean of some $y_i$ also lies in that range. $\square$

**Lemma 2 (interpolation and continuity).** $s(x_k) = y_k$, and $s(x) \to y_k$ as $x \to x_k$. More precisely, with $\delta = \min_{i \ne k} r_i(x_k) > 0$ and $r_k(x) < \delta / 2$,
$$|s(x) - y_k| \le \Big(\frac{2}{\delta}\Big)^{p} \Big(\sum_{i \ne k} |y_i - y_k|\Big)\, r_k(x)^{p}.$$

*Proof.* $s(x_k) = y_k$ by line L2, since $x_k$ is the only site at $x_k$. For $x \ne x_k$ near $x_k$, $s(x) - y_k = \sum_{i \ne k} u_i(x) (y_i - y_k)$ because the $u_i$ sum to 1. For $i \ne k$, $u_i = w_i / \sum_j w_j \le w_i / w_k = r_k^p / r_i^p$. When $r_k(x) < \delta/2$ the triangle inequality gives $r_i(x) \ge \delta - r_k(x) > \delta/2$, so $u_i(x) \le (2/\delta)^p r_k(x)^p$. Summing gives the bound, which tends to 0 with $r_k(x)$. $\square$

**Lemma 3 (flat spots).** If $p > 1$, then $s$ is differentiable at each site $x_k$ with gradient $0$.

*Proof.* By Lemma 2, $|s(x) - s(x_k)| \le C\, \|x - x_k\|^p$ near $x_k$ for a constant $C$. Since $p > 1$, $|s(x) - s(x_k) - 0 \cdot (x - x_k)| / \|x - x_k\| \le C \|x - x_k\|^{p-1} \to 0$, which is the definition of differentiability with zero derivative. $\square$

**Theorem (correctness).** For distinct sites, SHEPARD returns $s(x)$, where $s$ is a continuous function on $\mathbb{R}^d$ with $s(x_i) = y_i$ for every $i$, $\min y \le s \le \max y$, and $s \equiv c$ when all data equal $c$. For $p > 1$ its gradient vanishes at every site.

*Proof.* Lines L1 to L4 compute exactly the formula above. Away from $D$, $s$ is a quotient of continuous functions with positive denominator, hence continuous; at the sites it is continuous by Lemma 2. The remaining claims are Lemmas 1 to 3. For the local version (weights $((R - r_i)_+ / (R r_i))^2$), the same arguments apply wherever at least one site lies within distance $R$, since the weights are then nonnegative, not all zero, and the weight of $x_k$ still tends to infinity as $x \to x_k$ while the others stay bounded. $\square$

**Termination.** Line L1 is a loop over $N$ sites with $d$ coordinates each; lines L2 to L4 are single passes over the $N$ sites. There is no recursion, so the algorithm stops after $\Theta(N d)$ operations. $\square$
