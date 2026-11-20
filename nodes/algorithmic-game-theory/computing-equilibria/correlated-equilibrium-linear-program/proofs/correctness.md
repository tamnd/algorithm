---
title: The feasible set of the correlated equilibrium LP is the set of correlated equilibria, it is a nonempty polytope, and the LP returns an optimal correlated equilibrium
proves: [correctness]
status: full
---

Let $G$ be a finite game with players $1, \ldots, n$, pure strategy sets $S_i$, profiles $S = S_1 \times \cdots \times S_n$ and utilities $u_i$ (maximized). Let $w : S \to \mathbb{Q}$ be the objective. Let $P$ be the feasible set of the LP built in lines L1 to L4: the vectors $p \in \mathbb{R}^S$ with $p(s) \ge 0$ for all $s$, $\sum_s p(s) = 1$, and, for every player $i$ and every ordered pair $j \ne l$ in $S_i$,

$$g_i(j, l; p) = \sum_{s \in S : s_i = j} p(s)\,\big[u_i(l, s_{-i}) - u_i(s)\big] \le 0 .$$

**Claim 1 (the feasible set).** $P$ is exactly the set of correlated equilibria of $G$.

*Proof.* A distribution $p$ on $S$ is a correlated equilibrium if, for every player $i$ and every map $\delta : S_i \to S_i$, $\sum_s p(s)\,[u_i(\delta(s_i), s_{-i}) - u_i(s)] \le 0$. Group the sum by the value $j = s_i$: it equals $\sum_{j \in S_i} g_i(j, \delta(j); p)$, where $g_i(j, j; p) = 0$. If $p \in P$, every term is at most 0, so $p$ is a correlated equilibrium. Conversely, if $p$ is a correlated equilibrium, fix $i$ and $j \ne l$ and take $\delta(j) = l$ and $\delta(m) = m$ for $m \ne j$; then the sum is $g_i(j, l; p)$, so $g_i(j, l; p) \le 0$. Lines L1 and L4 say that $p$ is a distribution, and line L3 adds exactly the constraints $g_i(j, l; p) \le 0$, one for each $i$ (line L2) and each ordered pair. $\square$

**Claim 2 (nonempty).** $P$ is not empty.

*Proof.* By Nash's theorem, $G$ has a mixed Nash equilibrium $\sigma$. Let $p(s) = \prod_m \sigma_m(s_m)$. Then $p$ is a distribution, and

$$g_i(j, l; p) = \sigma_i(j)\,\big[u_i(l, \sigma_{-i}) - u_i(j, \sigma_{-i})\big].$$

If $\sigma_i(j) = 0$ this is 0. If $\sigma_i(j) > 0$, then $j$ is in the support of $\sigma_i$, so $j$ is a pure best response to $\sigma_{-i}$ (a mixed strategy is a best response exactly when its support consists of pure best responses), and the bracket is at most 0. So $p \in P$. Hart and Schmeidler (1989) give a second proof that uses only linear programming duality and no fixed point theorem. $\square$

**Claim 3 (the LP has an optimum).** $P$ is a bounded polyhedron, so the LP of line L5 has an optimal solution, and the optimum is attained at a vertex of $P$.

*Proof.* $P$ is the intersection of finitely many closed half spaces and one hyperplane, so it is a polyhedron. It lies in the simplex $\{p \ge 0, \sum_s p(s) = 1\}$, so $0 \le p(s) \le 1$ for all $s$, and $P$ is bounded. A bounded nonempty polyhedron is a polytope, the convex hull of its finitely many vertices, and a linear function on it attains its maximum, at a vertex. $\square$

**Claim 4 (the method returns it).** The two-phase simplex method with Bland's rule, run on the LP of lines L1 to L5, stops after finitely many pivots and returns a vertex $p^*$ of $P$ with $\sum_s w(s) p^*(s) = \max_{p \in P} \sum_s w(s) p(s)$.

*Proof.* With Bland's rule, the simplex method does not cycle, so each phase stops after finitely many pivots. Phase 1 maximizes minus the sum of the artificial variables; by Claim 2 the original constraints are feasible, so the phase ends with value 0 and a basic feasible solution of the original LP. Phase 2 cannot report that the LP is unbounded, because by Claim 3 the objective is bounded on $P$. So it stops with all reduced costs at most 0, which is the optimality condition, and the basic solution is a vertex of $P$. In exact rational arithmetic, as in the code, no rounding error enters. $\square$

**Conclusion.** By Claims 1 and 4, line L6 returns a correlated equilibrium of $G$ that maximizes $\sum_s w(s) p(s)$ over all correlated equilibria. With $w = 0$ it returns some correlated equilibrium. $\blacksquare$
