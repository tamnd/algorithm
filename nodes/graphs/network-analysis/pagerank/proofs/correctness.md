---
title: Power iteration converges to the unique PageRank vector
proves: [correctness, termination]
status: full
---

We use the notation of the page. Vectors are row vectors, $\|z\|_1 = \sum_v |z_v|$, and $\Delta = \{x \in \mathbb{R}^n : x \ge 0, \sum_v x_v = 1\}$ is the set of probability vectors. Let $0 \le \alpha < 1$.

**The matrices.** Let $S$ be the $n \times n$ matrix with $S_{uv} = c_{uv}/d^+(u)$ when $d^+(u) > 0$, and $S_{uv} = 1/n$ when $u$ is dangling. Each row of $S$ is non-negative and sums to 1, so $S$ is stochastic. Let $J = \tfrac{1}{n}\mathbf{1}\mathbf{1}^T$. The Google matrix is $P = \alpha S + (1 - \alpha) J$, which is the matrix of the page: for a dangling $u$, $\alpha/n + (1 - \alpha)/n = 1/n$.

**Lemma 1 (one round computes $xP$).** If $x \in \Delta$ at the start of a round, then at the end of line L6, $y = xP$, and $y \in \Delta$.

*Proof.* After line L5, $y_v = \sum_{(u, v) \in E} x_u / d^+(u) = \sum_{u : d^+(u) > 0} x_u S_{uv}$, because the $c_{uv}$ copies of an arc from $u$ to $v$ each add $x_u/d^+(u)$. Line L4 sets $d = \sum_{u \text{ dangling}} x_u$, and $\sum_{u \text{ dangling}} x_u S_{uv} = d/n$. So after line L6,

$$y_v = \alpha \sum_u x_u S_{uv} + \frac{1 - \alpha}{n} = \alpha (xS)_v + (1 - \alpha)(xJ)_v = (xP)_v,$$

where $(xJ)_v = \tfrac1n \sum_u x_u = \tfrac1n$ because $x \in \Delta$. Every entry of $P$ is non-negative and each row sums to 1, so $xP \ge 0$ and $\sum_v (xP)_v = \sum_u x_u = 1$. $\square$

**Lemma 2 ($S$ does not expand the $L_1$ norm).** For every $z \in \mathbb{R}^n$, $\|zS\|_1 \le \|z\|_1$.

*Proof.* $\|zS\|_1 = \sum_v |\sum_u z_u S_{uv}| \le \sum_v \sum_u |z_u| S_{uv} = \sum_u |z_u| \sum_v S_{uv} = \|z\|_1$. $\square$

**Lemma 3 (contraction).** For $x, x' \in \Delta$, $\|xP - x'P\|_1 \le \alpha \|x - x'\|_1$.

*Proof.* Let $z = x - x'$. Then $\sum_u z_u = 0$, so $zJ = 0$, and $zP = \alpha zS$. By Lemma 2, $\|zP\|_1 \le \alpha \|z\|_1$. $\square$

**Theorem.** (a) There is exactly one $\pi \in \Delta$ with $\pi = \pi P$. (b) Let $x^{(0)}$ be the uniform vector of line L1 and $x^{(k)}$ the vector after $k$ rounds. Then $\|x^{(k)} - \pi\|_1 \le 2\alpha^k$. (c) The loop stops after a finite number of rounds, and the returned vector $x$ satisfies $\|x - \pi\|_1 \le \alpha\varepsilon/(1 - \alpha)$.

*Proof.* By Lemma 1 and induction on $k$, every $x^{(k)}$ lies in $\Delta$ and $x^{(k+1)} = x^{(k)}P$.

(a) The set $\Delta$ is a closed subset of $\mathbb{R}^n$, so it is complete under $\|\cdot\|_1$. By Lemma 1 the map $f(x) = xP$ sends $\Delta$ into $\Delta$, and by Lemma 3 it is a contraction with factor $\alpha < 1$. The Banach fixed-point theorem gives exactly one fixed point $\pi \in \Delta$. For a direct proof of uniqueness: if $\pi$ and $\pi'$ are both fixed, then $\|\pi - \pi'\|_1 = \|\pi P - \pi' P\|_1 \le \alpha \|\pi - \pi'\|_1$, so $\|\pi - \pi'\|_1 = 0$.

(b) Since $\pi = \pi P$, Lemma 3 gives $\|x^{(k+1)} - \pi\|_1 = \|x^{(k)}P - \pi P\|_1 \le \alpha \|x^{(k)} - \pi\|_1$. By induction, $\|x^{(k)} - \pi\|_1 \le \alpha^k \|x^{(0)} - \pi\|_1$. Two probability vectors are at $L_1$ distance at most $\|x^{(0)}\|_1 + \|\pi\|_1 = 2$.

(c) Termination. The value of $\delta$ computed in round $k \ge 1$ is $\delta^{(k)} = \|x^{(k)} - x^{(k-1)}\|_1$. By Lemma 3 applied $k - 1$ times, $\delta^{(k)} \le \alpha^{k-1} \delta^{(1)} \le 2\alpha^{k-1}$. If $\alpha = 0$, then $x^{(1)} = x^{(0)}P = $ the uniform vector, so $\delta^{(1)} = 0 < \varepsilon$ and the loop stops after one round. If $0 < \alpha < 1$, then $2\alpha^{k-1} < \varepsilon$ as soon as $k - 1 > \log(\varepsilon/2)/\log\alpha$, so the loop stops after at most $\lceil \log(\varepsilon/2)/\log \alpha \rceil + 1$ rounds.

Error at the stop. Let the loop stop after round $k$, so $\delta^{(k)} < \varepsilon$ and the result is $x = x^{(k)}$. By the triangle inequality and (b),

$$\|x^{(k-1)} - \pi\|_1 \le \|x^{(k-1)} - x^{(k)}\|_1 + \|x^{(k)} - \pi\|_1 \le \delta^{(k)} + \alpha \|x^{(k-1)} - \pi\|_1,$$

so $\|x^{(k-1)} - \pi\|_1 \le \delta^{(k)}/(1 - \alpha)$. Then $\|x^{(k)} - \pi\|_1 \le \alpha \|x^{(k-1)} - \pi\|_1 \le \alpha \delta^{(k)}/(1 - \alpha) < \alpha \varepsilon/(1 - \alpha)$. $\blacksquare$

**The fixed point is the PageRank vector.** The equation $\pi = \pi P$, read entry by entry with $\sum_u \pi_u = 1$, is the formula of the page: $\pi_v = \alpha \sum_{(u,v) \in E} \pi_u/d^+(u) + \tfrac{\alpha}{n}\sum_{u \text{ dangling}} \pi_u + \tfrac{1 - \alpha}{n}$. Since every entry of $P$ is at least $(1 - \alpha)/n$, the chain is irreducible and aperiodic for $\alpha < 1$, and $\pi$ is its stationary distribution.
