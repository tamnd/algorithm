---
title: Canonical difference bound matrices and the zone operations are correct
proves: [correctness, termination]
status: full
---

**Setting.** A bound is $(c, \prec)$ with $c \in \mathbb{R} \cup \{\infty\}$ and $\prec \in \{<, \le\}$. Bounds are ordered by $c$, with $(c, <) < (c, \le)$. They are added as on the page. A real number $t$ *satisfies* $(c, \prec)$ when $t \prec c$. Every $t$ satisfies $\infty$. A DBM $D$ over clocks $1, \ldots, n$ has the zone $[\![D]\!]$ of all $v \in \mathbb{R}_{\ge 0}^n$ with $v_i - v_j$ satisfying $D_{ij}$ for all $i, j \in \{0, \ldots, n\}$, where $v_0 = 0$. We assume $D_{0i} \le (0, \le)$ for every $i$. This says $x_i \ge 0$, and every operation keeps it. The *graph* of $D$ has nodes $0, \ldots, n$ and an edge from $i$ to $j$ of weight $D_{ij}$ when $D_{ij} \ne \infty$. The weight of a walk $i = k_0, k_1, \ldots, k_m = j$ is $D_{k_0 k_1} + \cdots + D_{k_{m-1} k_m}$, and it is $(0, \le)$ when $m = 0$. A *negative cycle* is a closed walk of weight below $(0, \le)$.

**Fact 1.** Addition of bounds is associative, commutative and monotone: if $a \le b$, then $a + e \le b + e$. If $t$ satisfies $a$ and $s$ satisfies $b$, then $t + s$ satisfies $a + b$.

*Proof.* The first part is direct from the definition. For the last part, $t + s \le c + d$, and the inequality is strict unless both are equalities, which needs both bounds to be $\le$. $\square$

**Lemma 1 (walks).** If $v \in [\![D]\!]$ and there is a walk from $i$ to $j$ of weight $w$, then $v_i - v_j$ satisfies $w$.

*Proof.* We have $v_i - v_j = \sum_t (v_{k_t} - v_{k_{t+1}})$, and each term satisfies its edge bound. Apply Fact 1. $\square$

**Lemma 2 (Floyd-Warshall).** Let $D$ be the input and $D^*$ the matrix after lines L1 to L5. Each $D^*_{ij}$ is the weight of some walk from $i$ to $j$ in the graph of $D$. Also $D^*_{ij} \le w$ for every path from $i$ to $j$ in that graph without repeated nodes, where the walk of length 0 counts as a path from $i$ to $i$.

*Proof.* After round $k$ of the outer loop, the following invariant holds. Each entry is the weight of some walk. Each entry is at most the weight of every simple path from $i$ to $j$ whose inner nodes are in $\{0, \ldots, k\}$. At the start, $D_{ij}$ is the weight of the one-edge walk, and it bounds the simple paths with no inner nodes, which are the edge itself and, for $i = j$, the empty path. Our inputs always have $D_{ii} \le (0, \le)$, so the empty path is covered. In round $k$, the new value $D[i][k] + D[k][j]$ is the weight of the walk made by joining two walks, so the first part is kept. A simple path from $i$ to $j$ with inner nodes in $\{0, \ldots, k\}$ either avoids $k$, or splits at $k$ into two simple paths with inner nodes in $\{0, \ldots, k-1\}$. In the second case its weight is at least $D[i][k] + D[k][j]$ by Fact 1. Updates in the same round only lower entries, so the bounds still hold. $\square$

**Lemma 3 (emptiness).** $[\![D]\!]$ is empty if and only if the graph of $D$ has a negative cycle, and this holds if and only if CANONICAL returns empty.

*Proof.* If there is a negative cycle through $i$, then Lemma 1 for that closed walk says $0 = v_i - v_i$ satisfies a bound below $(0, \le)$. That is false, so the zone is empty.

If CANONICAL returns empty, then some $D^*_{ii} < (0, \le)$ is the weight of a closed walk, by Lemma 2. That is a negative cycle. Conversely, a negative closed walk splits into simple cycles, and one of them is negative by Fact 1. Its weight is at least $D^*_{ii}$ for a node $i$ on it, by Lemma 2, so line L7 fires.

Last, suppose there is no negative cycle. We build a point of the zone. There are finitely many simple cycles. Each has weight $(s, \prec)$ with $s > 0$, or with $s = 0$ and all its bounds $\le$. Let $\sigma$ be the least positive $s$ among them, or 1 if there is none. Let $\varepsilon = \sigma / (2(n+1))$. Give each edge the real weight $c$ if $D_{ij} = (c, \le)$, and $c - \varepsilon$ if $D_{ij} = (c, <)$. A simple cycle has at most $n + 1$ edges, so its real weight is at least $s - (n+1)\varepsilon > 0$ if $s > 0$, and exactly 0 if $s = 0$. So the real-weighted graph has no negative cycle. Add a new node $z$ with an edge of weight 0 to every node, and let $\pi_i$ be the shortest real distance from $z$ to $i$. This is finite and well defined. The triangle inequality $\pi_j \le \pi_i + \mathrm{weight}(i, j)$ holds for each edge from $i$ to $j$. Set $v_i = \pi_0 - \pi_i$. Then

$$v_i - v_j = \pi_j - \pi_i \le \mathrm{weight}(i, j),$$

which satisfies $D_{ij}$: when the bound is strict, the real weight is $c - \varepsilon < c$. Also $v_0 = 0$, and $0 - v_i = v_0 - v_i$ satisfies $D_{0i} \le (0, \le)$, so $v_i \ge 0$. So $v \in [\![D]\!]$. $\square$

**Theorem 1 (canonical form).** If CANONICAL$(D)$ returns $D^*$, then $[\![D^*]\!] = [\![D]\!]$, and $D^*$ is canonical: $D^*_{ij} \le D^*_{ik} + D^*_{kj}$ for all $i, j, k$. Each $D^*_{ij}$ is the least weight of a walk from $i$ to $j$, or $\infty$ if there is none.

*Proof.* Entries only go down, so $[\![D^*]\!] \subseteq [\![D]\!]$. Each $D^*_{ij}$ is the weight of a walk of $D$, so every $v \in [\![D]\!]$ satisfies it by Lemma 1. So the zones are equal. With no negative cycle, a least-weight walk can be taken simple, because removing a cycle does not raise the weight. So by Lemma 2, $D^*_{ij}$ is the least weight of a walk. The triangle inequality follows, because joining a walk from $i$ to $k$ with a walk from $k$ to $j$ gives a walk from $i$ to $j$. $\square$

**Lemma 4 (tightness).** Let $D$ be canonical with a nonempty zone, and let $D_{ij} = (c, \prec)$ with $i \ne j$. If $\prec$ is $\le$, some $v \in [\![D]\!]$ has $v_i - v_j = c$. If $\prec$ is $<$, then for every $\eta > 0$ some $v \in [\![D]\!]$ has $v_i - v_j > c - \eta$. If $c = \infty$, then for every $M$ some $v \in [\![D]\!]$ has $v_i - v_j > M$.

*Proof.* Add the constraint $x_j - x_i \le -c'$, which is a new bound $(-c', \le)$ on the entry $(j, i)$. Here $c' = c$ in the first case, $c' = c - \eta$ in the second, and $c' = M$ in the third. Any new cycle uses the new edge from $j$ to $i$ once, after a walk from $i$ to $j$. By Theorem 1 that walk weighs at least $D_{ij}$. So the cycle weighs at least $(c, \prec) + (-c', \le)$, which is $(0, \le)$ in the first case and $(\eta, <)$ in the second. In the third case there is no walk from $i$ to $j$, so there is no new cycle. Cycles that do not use the new edge were already nonnegative. By Lemma 3 the new zone is nonempty, and its points satisfy $v_i - v_j \ge c'$. $\square$

**Theorem 2 (inclusion).** For canonical $D$ and $E$ with nonempty zones, $[\![E]\!] \subseteq [\![D]\!]$ if and only if $E_{ij} \le D_{ij}$ for all $i, j$.

*Proof.* If $E \le D$ entrywise, every bound of $D$ is implied by the matching bound of $E$. For the other direction, suppose $E_{ij} > D_{ij} = (d, \prec)$. Then $d < \infty$ and $i \ne j$, since diagonal entries of a nonempty canonical DBM are $(0, \le)$. If $E_{ij} = (e, \le)$ with $e \ge d$, Lemma 4 gives $v \in [\![E]\!]$ with $v_i - v_j = e$, which breaks $D_{ij}$. If $E_{ij} = (e, <)$, then $e > d$ because $E_{ij} > D_{ij}$, and Lemma 4 gives a point with $v_i - v_j > d$. If $E_{ij} = \infty$, Lemma 4 gives a point with $v_i - v_j > d$. In all cases $[\![E]\!] \not\subseteq [\![D]\!]$. $\square$

**Theorem 3 (up).** If $D$ is canonical, then UP$(D)$ is canonical and $[\![\mathrm{UP}(D)]\!] = \{v + t : v \in [\![D]\!], t \ge 0\}$.

*Proof.* Let $U = \mathrm{UP}(D)$. If $v \in [\![D]\!]$ and $t \ge 0$, then $v + t$ keeps all differences $v_i - v_j$ with $i, j \ge 1$. Also $0 - (v_j + t) \le 0 - v_j$ satisfies $D_{0j}$. The entries $U_{i0}$ are $\infty$. So $v + t \in [\![U]\!]$.

Conversely, let $w \in [\![U]\!]$. We need $t \ge 0$ with $w - t \in [\![D]\!]$. The conditions on $t$ are lower bounds $t \ge 0$ and $w_i - t$ satisfies $D_{i0}$, which says $t$ is above $w_i - D_{i0}$. They are also upper bounds: $t - w_j$ satisfies $D_{0j}$, which says $t$ is below $w_j + D_{0j}$. Differences with $i, j \ge 1$ do not depend on $t$, and $w$ satisfies them. A finite set of lower and upper bounds on one real number has a solution if and only if each lower bound is compatible with each upper bound. Take the pair $w_i - D_{i0}$ and $w_j + D_{0j}$. It is compatible because $w_i - w_j$ satisfies $D_{ij} \le D_{i0} + D_{0j}$. Here we use canonicity, and for $i = j$ the facts that $D_{ii} = (0, \le)$ and $(0, \le) \le D_{i0} + D_{0i}$. The pair $0$ and $w_j + D_{0j}$ is compatible because $-w_j$ satisfies $U_{0j} = D_{0j}$. The case $t = 0$ also gives $w - t \ge 0$ through $D_{0j} \le (0, \le)$.

For canonicity, the only changed entries are $U_{i0} = \infty$ for $i \ge 1$. The triangle inequality $U_{i0} \le U_{ik} + U_{k0}$ holds trivially. Every inequality $U_{ij} \le U_{ik} + U_{kj}$ with $j \ne 0$ uses only unchanged entries on the left. On the right, $U \ge D$ entrywise, so it follows from the same inequality for $D$. $\square$

**Theorem 4 (reset).** If $D$ is canonical, then RESET$(D, x)$ is canonical and its zone is $\{v[x := 0] : v \in [\![D]\!]\}$.

*Proof.* Let $R = \mathrm{RESET}(D, x)$. Row $x$ of $R$ is row 0 of $D$, and column $x$ is column 0, except that $R_{xx} = R_{x0} = R_{0x} = (0, \le)$. If $v \in [\![D]\!]$, then $u = v[x := 0]$ has $u_x = u_0$, so the bounds of row and column $x$ are those of row and column 0, which $v$ satisfies. The other entries are unchanged. So $u \in [\![R]\!]$.

Conversely, let $w \in [\![R]\!]$. Then $w_x = 0$, because $R_{x0} = R_{0x} = (0, \le)$. We need a value $t$ for clock $x$ with $w[x := t] \in [\![D]\!]$. The conditions are that $t - w_j$ satisfies $D_{xj}$ and $w_i - t$ satisfies $D_{ix}$, for $i, j \ne x$, including the index 0. As in Theorem 3, each lower bound $w_i - D_{ix}$ is compatible with each upper bound $w_j + D_{xj}$, because $w_i - w_j$ satisfies $R_{ij} = D_{ij} \le D_{ix} + D_{xj}$. So such a $t$ exists. It is at least 0, because $-t$ satisfies $D_{0x} \le (0, \le)$.

$R$ is canonical: index $x$ is a copy of index 0 joined to it by $(0, \le)$ in both directions. So each triangle inequality that involves $x$ is a triangle inequality of $D$ with $x$ replaced by 0, or it is trivial. $\square$

**Theorem 5 (tighten).** Let $D$ be canonical with a nonempty zone, and let $b$ be a bound. If $D_{ji} + b < (0, \le)$, the zone of $D$ together with $x_i - x_j$ satisfying $b$ is empty. Otherwise TIGHTEN returns the canonical form of $D$ with $D_{ij}$ replaced by $\min(D_{ij}, b)$.

*Proof.* If $D_{ji} + b < (0, \le)$, there is a negative cycle, and Lemma 3 applies. Otherwise, any cycle that uses the new edge once weighs at least $b + D_{ji} \ge (0, \le)$, by Theorem 1. A cycle that uses it several times splits into such cycles. So there is no negative cycle. A least-weight walk from $p$ to $q$ in the new graph either avoids the new edge, and then weighs $D_{pq}$ by Theorem 1, or uses it. It can be taken to use it once, because removing a nonnegative cycle does not raise the weight. Then it weighs at least $D_{pi} + b + D_{jq}$. Line T5 takes the minimum of these two values. In line T5, the entries $D[p][i]$ and $D[j][q]$ may already be updated in the same loop. Their new values are still weights of walks and are at most the old ones, so the result is the same minimum. By Theorem 1 the result is the canonical form. $\square$

Constraining by $x \sim c$ is one or two calls of TIGHTEN, with $(i, j) = (x, 0)$ for upper bounds and $(0, x)$ for lower bounds.

**Theorem 6 (extrapolation is sound and finite).** For canonical $D$ with a nonempty zone, $[\![D]\!] \subseteq [\![\mathrm{EXTRAPOLATE}(D, k)]\!]$. The set of canonical DBMs that EXTRAPOLATE can return, for a fixed $k$ and integer constants, is finite.

*Proof.* Lines E2 and E3 only raise entries, so the zone can only grow, and line E4 does not change the zone by Theorem 1. For finiteness, after lines E1 to E3 each entry with $i \ne j$ is $\infty$ or lies between $(-k_j, <)$ and $(k_i, \le)$, which is a finite set of bounds. Closure only lowers entries, and the result is the least walk weight. A walk of the graph after E3 has at most $n + 1$ edges, so its weight is a sum of at most $n + 1$ such bounds, and it is not below the bound $(-(n+1)K, <)$, where $K = \max_x k_x$. So every entry of the result lies in a finite set, and there are finitely many results. $\square$

**Corollary 1 (termination and soundness of the zone search).** The forward search over zones with EXTRAPOLATE stores finitely many zones, so it terminates. Every location that some run of the automaton reaches is reported.

*Proof.* Every stored zone is an output of EXTRAPOLATE, so by Theorem 6 there are finitely many. A zone enters the waiting list only if no stored zone of its location includes it, and then it is stored. So each zone enters the list at most once. For soundness, we show by induction on runs that each reachable state $(\ell, v)$ lies in some zone that the search stores for $\ell$, or in a zone that includes a stored one. By Theorems 3 to 5, the successor computation gives a zone that contains all successors of the states in the source zone. Extrapolation and the inclusion test only enlarge what is kept. $\square$

**Exactness for diagonal-free automata (cited).** The converse needs one more fact, proved by Bouyer (2004). Let $A$ be diagonal-free, and let $M$ give for each clock its largest constant. For each zone $Z$ that the search builds, every valuation of $\mathrm{Extra}_M(Z)$ is region equivalent, for the constants $M$, to a valuation of $Z$. Given this fact, the [region graph](/region-graph/) argument applies. Region equivalence is a time-abstract bisimulation, so any location reached from a valuation of $\mathrm{Extra}_M(Z)$ is also reached from a valuation of $Z$. By induction on the search, every reported location is reachable. The fact needs that guards compare single clocks with constants. Bouyer also gives an automaton with diagonal guards $x - y \sim c$ where the search with $\mathrm{Extra}_M$ reports a location that is not reachable. The tests on this page check the conclusion against the region graph and against integer-step runs on random diagonal-free automata. With Theorems 1 to 6 and Corollary 1, this completes the argument, and only the exactness step is taken from Bouyer. $\blacksquare$
