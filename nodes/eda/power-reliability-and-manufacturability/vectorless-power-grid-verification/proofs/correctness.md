---
title: The worst drop under current bounds is a linear program, and with one total bound the greedy solves it
proves: [correctness]
status: full
---

**Setting.** $G$ is the $N \times N$ conductance matrix of a power grid in drop form, symmetric and nonsingular, with $G^{-1} \ge 0$ entrywise. The [power grid analysis](/power-grid-analysis/) page proves both facts when every connected part has a pad. There are $S$ sources at nodes $n_1, \ldots, n_S$, with currents $i \in \mathbb{R}^S$, and the load vector of the grid is $b(i) = \sum_s i_s e_{n_s}$. The feasible space is $\mathcal{F} = \{ i : 0 \le i \le u, \ U i \le w \}$ with $u \ge 0$, $w \ge 0$ and $U$ a 0-1 matrix.

**Lemma 1 (the drop is linear).** For each node $k$, $x_k(i) = r_k^T i$ with $(r_k)_s = (G^{-1})_{k n_s} \ge 0$. Line L2 computes $r_k$ correctly.

*Proof.* $x = G^{-1} b(i) = \sum_s i_s G^{-1} e_{n_s}$, so $x_k = \sum_s i_s (G^{-1})_{k n_s}$. Since $G$ is symmetric, so is $G^{-1}$, and row $k$ of $G^{-1}$ equals column $k$, which is the solution of $G r = e_k$. Its entries are nonnegative because $G^{-1} \ge 0$. $\square$

**Theorem 1 (exact worst case).** The maximum $z_k = \max_{i \in \mathcal{F}} x_k(i)$ exists, it equals the optimum of the linear program of line L3, it is attained at a vertex of $\mathcal{F}$, and for every $i \in \mathcal{F}$, $x_k(i) \le z_k$. No smaller number has this property.

*Proof.* By Lemma 1 the objective is the linear function $r_k^T i$. $\mathcal{F}$ is a polyhedron. It is not empty, since $i = 0$ meets every bound because $u, w \ge 0$. It is bounded, since $0 \le i \le u$. A linear function on a nonempty bounded polyhedron attains its maximum, and it attains it at a vertex. The bound property is the definition of the maximum, and since some $i^* \in \mathcal{F}$ gives $x_k(i^*) = z_k$, no smaller number bounds all feasible drops. $\square$

**Corollary 1 (local bounds only).** If there are no group bounds, $z_k = r_k^T u$, attained at $i = u$.

*Proof.* Every feasible $i$ has $i \le u$, and $r_k \ge 0$, so $r_k^T i \le r_k^T u$, and $u$ is feasible. $\square$

**Corollary 2 (monotone).** If $u \le u'$ and $w \le w'$, the worst drops for $(u', w')$ are at least those for $(u, w)$.

*Proof.* The feasible space only grows. $\square$

**Theorem 2 (the greedy with one total bound).** Let $r \ge 0$, $u \ge 0$ and $W \ge 0$, and let the only group bound be $\sum_s i_s \le W$. Then lines L5 to L8 return $\max \{ r^T i : 0 \le i \le u, \ \sum_s i_s \le W \}$.

*Proof.* The greedy output $g$ is feasible: each $g_s$ lies in $[0, u_s]$, since $rest$ never becomes negative, and the $g_s$ add up to at most $W$. Sort the sources so that $r_1 \ge r_2 \ge \cdots \ge r_S$, the order of line L5. Then $g = (u_1, \ldots, u_{j-1}, \theta, 0, \ldots, 0)$ with $0 \le \theta \le u_j$, where either all sources are full or the total is $W$.

Take an optimal $i^*$ that agrees with $g$ on the longest possible prefix, and suppose $i^* \ne g$. Let $t$ be the first index with $i^*_t \ne g_t$. If $i^*_t > g_t$, then $g_t < u_t$, so the greedy had $rest = g_t$ at step $t$, which means $\sum_{s \le t} g_s = W$. Then $\sum_{s \le t} i^*_s > W$, which is not feasible. So $i^*_t < g_t$. Let $\epsilon = g_t - i^*_t > 0$.

If $\sum_s i^*_s < W$, raise $i^*_t$ by $\min(\epsilon, W - \sum_s i^*_s)$. This stays feasible and does not lower $r^T i^*$, since $r_t \ge 0$. Otherwise $\sum_s i^*_s = W \ge \sum_s g_s$, and the first $t - 1$ entries agree, so some $s > t$ has $i^*_s > g_s \ge 0$. Move $\min(\epsilon, i^*_s)$ ampere from source $s$ to source $t$. This stays feasible and changes $r^T i^*$ by a multiple of $r_t - r_s \ge 0$. Repeating these moves raises $i^*_t$ to $g_t$ while keeping $i^*$ optimal, which gives an optimal vector that agrees with $g$ on a longer prefix, a contradiction. So $g$ is optimal. $\square$

This is the exchange argument of the [fractional knapsack](/fractional-knapsack/), with values $r_s$ per ampere, item sizes $u_s$ and the capacity $W$. For several group bounds that overlap, no such greedy is exact in general, and line L3 needs a full linear program.

The tests check the simplex of the code against an enumeration of all vertices of small feasible spaces, check that the worst vector is feasible and bounds random feasible currents, and check Theorem 2 against the simplex on random grids.
