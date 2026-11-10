---
title: Nearest insertion returns a tour of cost at most 2(1 − 1/n) OPT, and the bound is tight
proves: [correctness]
status: full
---

The costs $d$ on the city set $V$, with $|V| = n \ge 2$, are symmetric, non-negative and satisfy the triangle inequality. A cycle $H$ on a set $S$ visits each city of $S$ one time; a cycle on one city costs 0, and a cycle on two cities $a, b$ costs $2\,d(a, b)$. For a set $S$ and a city $v \notin S$, $d(v, S) = \min_{u \in S} d(v, u)$. Let $S_t$ be the set of the $t$ cities in the cycle after $t - 1$ insertions, so $S_1 = \{s\}$ and $S_n = V$, and let $H_t$ be the cycle on $S_t$.

**Lemma 1 (the cost of one insertion).** Let $k \notin S_t$ and let $j \in S_t$ be a city with $d(k, j) = d(k, S_t)$. Then the cheapest position for $k$ in $H_t$ raises the cost by at most $2\,d(k, S_t)$.

*Proof.* If $t = 1$, the new cycle is $j, k$, and its cost is $2\,d(j, k)$. If $t \ge 2$, let $j'$ be the city after $j$ in $H_t$. To put $k$ between $j$ and $j'$ costs $d(j, k) + d(k, j') - d(j, j')$. By the triangle inequality $d(k, j') \le d(k, j) + d(j, j')$, so the increase is at most $2\,d(j, k)$. The cheapest position costs at most this position. $\square$

**Lemma 2 (Prim's order).** Let $k_t$ be the city that nearest insertion adds to $S_t$, and let $a_t = d(k_t, S_t)$. Then $\sum_{t=1}^{n-1} a_t$ is the cost of a minimum spanning tree.

*Proof.* At each step the algorithm adds a city outside $S_t$ at the least distance from $S_t$, and it joins the city to $S_t$ by an edge of cost $a_t$. This is the rule of [Prim's algorithm](/prim/) started at $s$. The $n - 1$ edges form a spanning tree, and by the cut property each edge is a cheapest edge across the cut $(S_t, V \setminus S_t)$, so the tree has minimum cost. Its cost is $\sum_t a_t$. $\square$

**Lemma 3 (the lower bound).** A minimum spanning tree $T$ has $c(T) \le (1 - 1/n) \cdot \text{OPT}$.

*Proof.* Delete the most costly edge of an optimal tour. It costs at least OPT$/n$, and the rest is a spanning path. $\square$

**Theorem.** Nearest insertion returns a tour $H_n$ with $c(H_n) \le 2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$, for each start city and each tie rule.

*Proof.* $c(H_1) = 0$. By Lemma 1 with $k = k_t$, $c(H_{t+1}) \le c(H_t) + 2 a_t$. So $c(H_n) \le 2 \sum_{t=1}^{n-1} a_t$. By Lemma 2 this is $2\,c(T)$, and by Lemma 3 it is at most $2(1 - 1/n) \cdot \text{OPT}$. $\blacksquare$

## The bound is tight

Let $n = 2h + 2$ be even with $h \ge 2$, and let $d(i, j) = \min(|i - j|, n - |i - j|)$ on the cities $0, 1, \ldots, n - 1$. This is the shortest path metric of the cycle graph $C_n$ with unit edges. Each tour has $n$ edges of cost at least 1, and the tour $0, 1, \ldots, n - 1$ costs $n$, so OPT $= n$. Start at city 0 and add the cities $1, 2, \ldots, n - 1$ in this order:

- city $k$ with $1 \le k \le h$ goes right after city 0, so the cycle becomes $0, k, k - 1, \ldots, 1$;
- city $k$ with $h + 1 \le k \le n - 2$ goes right after city $h$, so the cycle becomes $0, h, k, k - 1, \ldots, h + 1, h - 1, \ldots, 1$;
- city $n - 1$ goes right after city 0.

**Claim.** Each step is a legal step of nearest insertion, and each step raises the cost by exactly 2. So ALG $= 2(n - 1)$ and ALG/OPT $= 2(1 - 1/n)$.

*Proof.* Before city $k$ is added, the cycle holds the arc $S = \{0, 1, \ldots, k - 1\}$.

1. *The city.* City $k$ is at distance 1 from $k - 1 \in S$, and each city outside $S$ is at distance at least 1 from $S$. So $k$ is a closest city.
2. *Each increase is even and at least 2.* $C_n$ is bipartite because $n$ is even, so $d(a, v) + d(v, b) - d(a, b)$ is even for all cities $a, v, b$. The value is 0 only if $v$ lies on a shortest path from $a$ to $b$. The edges of the cycle are of four kinds: unit edges; $\{0, k'\}$ with $k' \le h$; $\{0, h\}$ and $\{h, k - 1\}$ with $k - 1 - h \le h$; and $\{h + 1, h - 1\}$. In each case the length is at most $h < n/2$, so the shortest path is unique, and it runs along the arc between the two ends, which is inside $S$. So no city outside $S$ lies on a shortest path between two neighbors of the cycle, and each increase for each city outside $S$ is at least 2.
3. *The chosen position costs 2.* For $k \le h$, the position between 0 and $k - 1$ costs $k + 1 - (k - 1) = 2$ (for $k = 1$ the cycle $0, 1$ costs 2). For $h + 1 \le k \le n - 2$, the position between $h$ and the next city, which is $k - 1$ (or $h - 1$ when $k = h + 1$), costs $(k - h) + 1 - (k - 1 - h) = 2$ (or $1 + 2 - 1 = 2$). For $k = n - 1$, the position between 0 and $h$ costs $d(0, n - 1) + d(n - 1, h) - d(0, h) = 1 + (h + 1) - h = 2$.

By steps 2 and 3 the chosen position is a cheapest position for $k$, so with steps 1 the run is legal. The $n - 1$ steps each add 2. $\square$

Step 2 shows more: at each step, each pair of a city outside the cycle and a position costs at least 2. So the same run is also a legal run of [cheapest insertion](/cheapest-insertion/), and the bound $2(1 - 1/n)$ is tight for both rules. The ties in this family go against the algorithm; the factor 2 in Lemma 1 is reached when $k$, $j$ and $j'$ lie on a line with $j$ in the middle.
