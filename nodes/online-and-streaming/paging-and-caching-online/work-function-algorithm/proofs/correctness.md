---
title: The work function algorithm serves each request, its extended cost bound, and its ratio
proves: [correctness]
status: sketch
---

This file has three parts. Parts 1 and 2 are full proofs: the basic facts about work functions, the extended cost bound, and the ratio $k$ on metrics with $k + 1$ points. Part 3 is only a sketch of the bound $2k - 1$ of Koutsoupias and Papadimitriou for every metric; the full proof is in their 1995 paper and in Section 3.3 of the survey of Koutsoupias (2009).

**Setting.** $(M, d)$ is a metric space. A configuration is a multiset of $k$ points, and $D(X, Y)$ is the cost of a minimum perfect matching between $X$ and $Y$. $D$ is a metric on configurations. A schedule for $r_1, \ldots, r_t$ is a list $X_0 = C_0, X_1, \ldots, X_t$ with $r_i \in X_i$, of cost $\sum_i D(X_{i-1}, X_i)$. Define

$$w_0(X) = D(C_0, X), \qquad w_t(X) = \min_{Y \ni r_t} \bigl( w_{t-1}(Y) + D(Y, X) \bigr).$$

By induction on $t$, $w_t(X)$ is the least cost of a schedule for $r_1, \ldots, r_t$ followed by one more move to $X$. So $\mathrm{OPT}(\sigma) = \min_X w_m(X)$: a schedule ending in $X_m$ gives $w_m(X_m)$ at most its cost, and each $w_m(X)$ is at least the cost of some schedule.

## Part 1. Facts about work functions

**(F1) Lipschitz.** $w_t(X) \le w_t(Y) + D(Y, X)$. For $t = 0$ this is the triangle inequality of $D$. For $t \ge 1$, take $Z \ni r_t$ that attains $w_t(Y)$; then $w_t(X) \le w_{t-1}(Z) + D(Z, X) \le w_{t-1}(Z) + D(Z, Y) + D(Y, X)$.

**(F2) Recurrence.** $w_t(X) = \min_{x \in X} \bigl( w_{t-1}(X - x + r_t) + d(x, r_t) \bigr)$. The side $\le$ holds because $Y = X - x + r_t$ contains $r_t$ and $D(Y, X) \le d(r_t, x)$. For $\ge$, let $Y \ni r_t$ attain $w_t(X)$, and let $x$ be the partner of $r_t$ in a minimum matching of $Y$ and $X$. Then $D(Y, X) = d(r_t, x) + D(Y - r_t, X - x)$, and by (F1), $w_{t-1}(X - x + r_t) \le w_{t-1}(Y) + D(Y - r_t, X - x)$. Together, $w_{t-1}(Y) + D(Y, X) \ge w_{t-1}(X - x + r_t) + d(x, r_t)$.

**(F3) Monotone.** $w_t(X) \ge w_{t-1}(X)$, since $w_{t-1}(Y) + D(Y, X) \ge w_{t-1}(X)$ by (F1).

**(F4) Covered configurations.** If $r_t \in X$, then $w_t(X) = w_{t-1}(X)$. Take $Y = X$ for $\le$, and use (F3) for $\ge$.

Lines L2 and L4 of the algorithm compute exactly $w_0$ and the recurrence (F2), so the program holds $w_t$ after request $t$.

**Lemma (the move).** Let $C = C_{t-1}$, and let $r = r_t \notin C$. Let line L6 choose $s$, so $C_t = C - s + r$. Then $w_t(C) = w_t(C_t) + d(s, r)$.

*Proof.* By (F2), $w_t(C) = \min_{x \in C} \bigl( w_{t-1}(C - x + r) + d(x, r) \bigr)$. Each $C - x + r$ contains $r$, so by (F4) we can replace $w_{t-1}$ by $w_t$ there. Line L6 takes the $x$ that attains this minimum. $\square$

So line L8 gives a configuration that contains $r_t$, and WFA serves each request.

**Theorem 1 (extended cost).** Write $\mathrm{ext}_t = \max_X \bigl( w_t(X) - w_{t-1}(X) \bigr)$. Then

$$\mathrm{WFA}(\sigma) + w_m(C_m) = \sum_{t=1}^{m} \bigl( w_t(C_{t-1}) - w_{t-1}(C_{t-1}) \bigr), \qquad \mathrm{WFA}(\sigma) + \mathrm{OPT}(\sigma) \le \sum_{t=1}^{m} \mathrm{ext}_t .$$

*Proof.* Let $c_t$ be the cost of WFA for $r_t$. If $r_t \in C_{t-1}$, then $C_t = C_{t-1}$ and $c_t = 0 = w_t(C_{t-1}) - w_t(C_t)$. Otherwise the lemma gives $c_t = w_t(C_{t-1}) - w_t(C_t)$. So

$$c_t = \bigl( w_t(C_{t-1}) - w_{t-1}(C_{t-1}) \bigr) - \bigl( w_t(C_t) - w_{t-1}(C_{t-1}) \bigr).$$

The second brackets telescope over $t$ to $w_m(C_m) - w_0(C_0) = w_m(C_m)$. This is the equation. For the inequality, each term is at most $\mathrm{ext}_t$, and $w_m(C_m) \ge \min_X w_m(X) = \mathrm{OPT}(\sigma)$. $\square$

So WFA is $c$-competitive if the sum of the extended costs is at most $(c + 1) \cdot \mathrm{OPT}$ plus a constant.

## Part 2. Metrics with $k + 1$ points

**Theorem 2.** Let $|M| = k + 1$, and let $C_0$ have $k$ distinct points. Let $\Delta$ be the diameter of $M$. Then $\mathrm{WFA}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + k \Delta$.

*Proof.* WFA is lazy and moves a server only to an uncovered point, so each $C_t$ has $k$ distinct points. There are exactly $k + 1$ such sets, one for each missing point; call their family $\mathcal{F}$. By (F3), each difference $w_t(X) - w_{t-1}(X)$ is at least $0$, so

$$w_t(C_{t-1}) - w_{t-1}(C_{t-1}) \le \sum_{X \in \mathcal{F}} \bigl( w_t(X) - w_{t-1}(X) \bigr).$$

Sum over $t$ and use the equation of Theorem 1:

$$\mathrm{WFA}(\sigma) + w_m(C_m) \le \sum_{X \in \mathcal{F}} \bigl( w_m(X) - w_0(X) \bigr) \le \sum_{X \in \mathcal{F}} w_m(X).$$

An optimal schedule can be taken lazy: delay each move of a server until that server must serve a request, and then move it straight there; by the triangle inequality this does not cost more. A lazy schedule from $C_0$ stays in $\mathcal{F}$, so $\mathrm{OPT}(\sigma) = w_m(X^*)$ for some $X^* \in \mathcal{F}$. Any other $X \in \mathcal{F}$ differs from $X^*$ in one point, so $D(X^*, X) \le \Delta$, and by (F1), $w_m(X) \le \mathrm{OPT}(\sigma) + \Delta$. Hence

$$\sum_{X \in \mathcal{F}} w_m(X) \le \mathrm{OPT}(\sigma) + k \bigl( \mathrm{OPT}(\sigma) + \Delta \bigr).$$

With $w_m(C_m) \ge \mathrm{OPT}(\sigma)$, this gives $\mathrm{WFA}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + k \Delta$. $\square$

By the lower bound of Manasse, McGeoch and Sleator, no deterministic algorithm has a ratio below $k$ on such a metric, so WFA is optimal on $k + 1$ points.

## Part 3. Sketch of the bound $2k - 1$ on every metric

This part is a sketch. It names the steps of the proof of Koutsoupias and Papadimitriou, but it does not prove them.

1. By Theorem 1, it is enough to show $\sum_t \mathrm{ext}_t \le 2k \cdot \mathrm{OPT}(\sigma) + b$ for a constant $b$ that depends only on $C_0$ and the metric.
2. **Quasiconvexity.** For each work function $w$ and configurations $A$ and $B$, there is a bijection $h : A \to B$ such that for each $A' \subseteq A$, $w(A) + w(B) \ge w(A - A' + h(A')) + w(B - h(A') + A')$. The proof is by induction on $t$, with the recurrence (F2).
3. **Duality.** Let $w'$ be the work function after the request $r$. A configuration $A$ that minimizes $w(X) - \sum_{x \in X} d(r, x)$ also minimizes $w'(X) - \sum_{x \in X} d(r, x)$, and it maximizes $w'(X) - w(X)$. So the extended cost is attained at such a minimizer. This follows from quasiconvexity.
4. **A potential.** Define $\Psi(w)$ as a minimum, over a configuration $U = \{u_1, \ldots, u_k\}$ and configurations $B_1, \ldots, B_k$, of $k \cdot w(U) + \sum_i \bigl( w(B_i) - \sum_{b \in B_i} d(u_i, b) \bigr)$. With duality, one shows that $\Psi(w_t) - \Psi(w_{t-1}) \ge \mathrm{ext}_t$ for each $t$. Taking all these configurations equal to a minimizer of $w_m$ bounds $\Psi(w_m)$ by $2k \cdot \mathrm{OPT}(\sigma)$ plus a constant, and $\Psi(w_0)$ is at least a constant.
5. Summing step 4 over $t$ gives step 1, and Theorem 1 then gives $\mathrm{WFA}(\sigma) \le (2k - 1) \cdot \mathrm{OPT}(\sigma) + b$.

The tests check Theorem 1, Theorem 2 and the bound $2k - 1$ with a generous constant on many random small metrics, with the optimum from an independent brute force. $\blacksquare$
