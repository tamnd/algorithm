---
title: Cheapest insertion returns a tour of cost at most 2(1 − 1/n) OPT
proves: [correctness]
status: full
---

The costs $d$ on the city set $V$, with $|V| = n \ge 2$, are symmetric, non-negative and satisfy the triangle inequality. A cycle on one city costs 0, and a cycle on two cities $a, b$ costs $2\,d(a, b)$. Let $S_t$ be the set of the $t$ cities in the cycle after $t - 1$ insertions, so $S_1 = \{s\}$, $S_n = V$ and $S_1 \subset S_2 \subset \cdots \subset S_n$. Let $H_t$ be the cycle on $S_t$ and let

$$a_t = d(S_t, V \setminus S_t) = \min\{d(u, v) : u \in S_t,\ v \notin S_t\} \quad (1 \le t \le n - 1).$$

**Lemma 1 (one insertion).** The cheapest pair of a city and a position raises the cost of $H_t$ by at most $2 a_t$.

*Proof.* Let $u \in S_t$ and $k \notin S_t$ with $d(u, k) = a_t$. If $t = 1$, the cycle $u, k$ costs $2 a_t$. If $t \ge 2$, let $u'$ follow $u$ on $H_t$. To put $k$ between $u$ and $u'$ costs $d(u, k) + d(k, u') - d(u, u') \le 2\,d(u, k)$, by the triangle inequality $d(k, u') \le d(k, u) + d(u, u')$. The cheapest pair costs at most this pair. $\square$

**Lemma 2 (cuts of a nested chain).** For each chain $S_1 \subset S_2 \subset \cdots \subset S_n = V$ with $|S_t| = t$, and each minimum spanning tree $T$,

$$\sum_{t=1}^{n-1} a_t \le c(T).$$

*Proof.* Fix a number $x \ge 0$. Let $G_x$ be the graph on $V$ with the edges of cost at most $x$, and let $\kappa(x)$ be its number of connected components.

First, $\#\{t : a_t > x\} \le \kappa(x) - 1$. If $a_t > x$, no edge of $G_x$ joins $S_t$ to the rest, so $S_t$ is a union of components of $G_x$, and it is not empty and not all of $V$. The sets $S_t$ with $a_t > x$ are distinct and nested, and each one holds at least one more component than the one before it. A chain of such sets has at most $\kappa(x) - 1$ members.

Second, $T$ has exactly $\kappa(x) - 1$ edges of cost more than $x$. The edges of $T$ with cost at most $x$ form a forest in $G_x$. It is a spanning forest of $G_x$. If not, two cities of one component of $G_x$ are in two trees of this forest, and a path of $G_x$ between them has an edge $e$, of cost at most $x$, whose ends are in two trees of the forest. The path in $T$ between the ends of $e$ is then not inside the forest, so it has an edge $f$ of cost more than $x$. The tree $T - f + e$ is a spanning tree that costs less than $T$, which is not possible. A spanning forest of $G_x$ has $n - \kappa(x)$ edges, so $T$ has $(n - 1) - (n - \kappa(x)) = \kappa(x) - 1$ edges of cost more than $x$.

So for each $x \ge 0$, $\#\{t : a_t > x\} \le \#\{e \in T : c(e) > x\}$. For non-negative numbers $y_1, \ldots, y_m$, $\sum_i y_i = \int_0^\infty \#\{i : y_i > x\}\, dx$. Integrate the inequality over $x$ from 0 to $\infty$: $\sum_t a_t \le \sum_{e \in T} c(e) = c(T)$. $\square$

**Lemma 3 (the lower bound).** $c(T) \le (1 - 1/n) \cdot \text{OPT}$.

*Proof.* An optimal tour without its most costly edge is a spanning path, of cost at most $\text{OPT} - \text{OPT}/n$. $\square$

**Theorem.** Cheapest insertion returns a tour $H_n$ with $c(H_n) \le 2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$, for each start city and each tie rule.

*Proof.* $c(H_1) = 0$. By Lemma 1, $c(H_{t+1}) \le c(H_t) + 2 a_t$, so $c(H_n) \le 2 \sum_{t=1}^{n-1} a_t$. Lemma 2 bounds the sum by $c(T)$, and Lemma 3 bounds $c(T)$. $\blacksquare$

Lemma 2 holds for each nested chain, not only for the chain of this algorithm. So the proof gives the bound 2 for each insertion method whose step costs at most $2 a_t$. For [nearest insertion](/nearest-insertion/) the chain is Prim's order, and Lemma 2 holds with equality.

**Tightness.** On the cycle graph $C_n$ with unit edges and $n = 2h + 2 \ge 6$ even, OPT $= n$. Start at city 0 and add $1, 2, \ldots, n - 1$ in this order: city $k$ goes right after city 0 when $k \le h$ or $k = n - 1$, and right after city $h$ otherwise. The [nearest insertion](/nearest-insertion/) proof file shows two facts for each step: each pair of an outside city and a position raises the cost by an even number that is at least 2, and the chosen pair raises it by exactly 2. So each step is a cheapest pair, and ALG $= 2(n - 1) = 2(1 - 1/n) \cdot \text{OPT}$.
