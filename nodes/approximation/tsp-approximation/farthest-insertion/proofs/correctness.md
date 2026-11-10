---
title: Farthest insertion, and each insertion order with cheapest positions, costs at most (⌈lg n⌉ + 1) OPT
proves: [correctness]
status: full
---

This file proves the only general upper bound that is known for farthest insertion. The bound is not a constant, and it holds for each insertion method that puts each city at a cheapest position, whatever rule picks the city. The proof follows Rosenkrantz, Stearns and Lewis (1977). The lower bounds of Hurkens (1992) are quoted on the page, not proved here.

The costs $d$ on the city set $V$, with $|V| = n \ge 2$, are symmetric, non-negative and satisfy the triangle inequality. A cycle on one city costs 0 and a cycle on two cities $a, b$ costs $2\,d(a, b)$. The method starts with the city $s$ and adds the other cities in some order, each at a cheapest position. For a city $k \ne s$, let $c_k$ be the increase of the cost when $k$ is added, and let $c_s = 0$. The final cost is ALG $= \sum_{k} c_k$. Logarithms are to base 2.

**Lemma 1 (an earlier city bounds a later increase).** If $p$ is in the cycle when $q$ is added, then $c_q \le 2\,d(p, q)$.

*Proof.* If the cycle is $\{p\}$, then $c_q = 2\,d(p, q)$. Otherwise let $p'$ follow $p$ on the cycle. The position between $p$ and $p'$ costs $d(p, q) + d(q, p') - d(p, p') \le 2\,d(p, q)$, by the triangle inequality. The cheapest position costs at most this. $\square$

Let $\ell_k = c_k / 2$ for each city $k$.

**Lemma 2.** For two cities $p \ne q$, $d(p, q) \ge \min(\ell_p, \ell_q)$, and for each city $k$, $\ell_k \le \text{OPT}/2$.

*Proof.* One of the two cities is in the cycle when the other is added. If $p$ comes first, Lemma 1 gives $\ell_q \le d(p, q)$; the other case is the same. For the second claim, $\ell_s = 0$, and for $k \ne s$ the start city $s$ is in the cycle when $k$ is added, so $\ell_k \le d(s, k)$. An optimal tour holds two paths from $s$ to $k$ with no common edge, and each costs at least $d(s, k)$, so $d(s, k) \le \text{OPT}/2$. $\square$

**Lemma 3 (the charging bound).** Let $\ell$ be any non-negative function on $V$ that satisfies the two claims of Lemma 2. Then $\sum_k \ell_k \le \frac{1}{2}(\lceil \lg n \rceil + 1) \cdot \text{OPT}$.

*Proof.* Number the cities $u_1, \ldots, u_n$ so that $\ell_1 \ge \cdots \ge \ell_n$, where $\ell_i = \ell_{u_i}$. Fix $k$ with $1 \le k < n$, let $m = \min(2k, n)$ and $S = \{u_1, \ldots, u_m\}$. Walk along an optimal tour and skip the cities outside $S$. By the triangle inequality the result is a tour $H_S$ of $S$ with cost at most OPT. It has $m$ edges. Charge each edge $u_i u_j$ to the end with the larger index. By the first claim, the edge costs at least the $\ell$ value of that end. Each city is an end of two edges of $H_S$, so it takes at most two charges, and the charges add up to $m$. The values $\ell_{k+1}, \ldots, \ell_m$ are the $m - k$ smallest values in $S$, and $2(m - k) \le m$. So the least possible total of the charged values is at least $2 \sum_{i=k+1}^{m} \ell_i$, and

$$\text{OPT} \ge 2 \sum_{i=k+1}^{\min(2k, n)} \ell_i.$$

Use this for $k = 1, 2, 4, \ldots, 2^{L-1}$ with $L = \lceil \lg n \rceil$. The index ranges are disjoint and cover $2, \ldots, n$, so $L \cdot \text{OPT} \ge 2 \sum_{i \ge 2} \ell_i$. The second claim gives $\text{OPT} \ge 2 \ell_1$. The sum is $(L + 1) \cdot \text{OPT} \ge 2 \sum_i \ell_i$. $\square$

**Theorem (Rosenkrantz, Stearns and Lewis 1977).** Each insertion method that puts each city at a cheapest position returns a tour with ALG $\le (\lceil \lg n \rceil + 1) \cdot \text{OPT}$. In particular this holds for farthest insertion.

*Proof.* By Lemma 2 the values $\ell_k = c_k/2$ satisfy the conditions of Lemma 3. So ALG $= \sum_k c_k = 2 \sum_k \ell_k \le (\lceil \lg n \rceil + 1) \cdot \text{OPT}$. $\blacksquare$

**What the proof does not give.** The proof uses only the cheapest position. It does not use the rule that picks the farthest city, so it cannot give a better bound for farthest insertion than for the worst order. The bound 2 of [nearest insertion](/nearest-insertion/) and [cheapest insertion](/cheapest-insertion/) needs a step cost of at most $2\,d(S_t, V \setminus S_t)$. Farthest insertion picks the city with the largest distance to the cycle, so its step can cost up to $2 \max_{k \notin S_t} d(k, S_t)$, and the sum of these values is not bounded by a minimum spanning tree. Whether farthest insertion has a constant ratio is an open question; the best known lower bound for metric instances is 6.5 (Hurkens 1992).
