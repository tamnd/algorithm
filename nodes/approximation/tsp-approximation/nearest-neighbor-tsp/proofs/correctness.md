---
title: The nearest-neighbor tour costs at most (1/2)(⌈lg n⌉ + 1) OPT on metric instances
proves: [correctness]
status: full
---

The costs $d$ on the city set $V$, with $|V| = n \ge 2$, are symmetric, non-negative and satisfy the triangle inequality. OPT is the cost of an optimal tour. The nearest-neighbor tour is $v_1, v_2, \ldots, v_n$, and the tour closes with the edge $v_n v_1$. For a city $p = v_i$, let $\ell_p$ be the cost of the tour edge that leaves $p$: $\ell_{v_i} = d(v_i, v_{i+1})$ for $i < n$ and $\ell_{v_n} = d(v_n, v_1)$. So ALG $= \sum_{p \in V} \ell_p$. The proof follows Rosenkrantz, Stearns and Lewis (1977). Logarithms are to base 2.

**Lemma 1 (the greedy property).** For two cities $p \ne q$, $d(p, q) \ge \min(\ell_p, \ell_q)$.

*Proof.* Say $p = v_i$ and $q = v_j$ with $i < j$. When the algorithm stood at $v_i$ and chose $v_{i+1}$, the city $q$ was not yet visited. The algorithm takes a closest unvisited city, so $\ell_p = d(v_i, v_{i+1}) \le d(p, q)$. $\square$

**Lemma 2 (one edge).** For each city $p$, $\ell_p \le \text{OPT}/2$.

*Proof.* The edge that leaves $p$ goes to a city $q \ne p$. An optimal tour passes through $p$ and $q$, so it is the union of two paths from $p$ to $q$ that have no edge in common. By the triangle inequality each path costs at least $d(p, q)$. So $\text{OPT} \ge 2\,d(p, q) = 2\,\ell_p$. $\square$

**Lemma 3 (a subset).** For each set $S \subseteq V$ with $|S| \ge 2$, there is a tour of $S$ with cost at most OPT.

*Proof.* Walk along an optimal tour of $V$ and skip the cities that are not in $S$. Each skip replaces a path by one edge, and by the triangle inequality the edge costs at most the path. $\square$

Number the cities $u_1, \ldots, u_n$ so that $\ell_{u_1} \ge \ell_{u_2} \ge \cdots \ge \ell_{u_n}$, and write $\ell_i = \ell_{u_i}$.

**Lemma 4 (the charging bound).** For each $k$ with $1 \le k < n$,

$$\text{OPT} \ge 2 \sum_{i = k+1}^{\min(2k, n)} \ell_i.$$

*Proof.* Let $s = \min(2k, n)$ and $S = \{u_1, \ldots, u_s\}$, so $s \ge 2$. By Lemma 3, $S$ has a tour $H_S$ of cost at most OPT. The tour $H_S$ has $s$ edges (for $s = 2$, the same pair two times). Charge each edge $u_i u_j$ of $H_S$ to the end with the larger index, which is the end with the smaller value $\ell$. By Lemma 1 the edge costs at least $\min(\ell_i, \ell_j)$, which is the value of the charged end. Each city of $S$ is an end of exactly two edges of $H_S$, so it receives at most two charges. Let $\alpha_i \in \{0, 1, 2\}$ be the number of charges to $u_i$. Then $\sum_{i \le s} \alpha_i = s$ and

$$\text{OPT} \ge c(H_S) \ge \sum_{i=1}^{s} \alpha_i \ell_i.$$

The cities $u_{k+1}, \ldots, u_s$ are $s - k$ cities, and $2(s - k) \le s$ because $s \le 2k$. A sum $\sum \alpha_i \ell_i$ with $\alpha_i \le 2$ and $\sum \alpha_i = s$ is smallest when the charges go to the smallest values first. So it is at least $2 \sum_{i=k+1}^{s} \ell_i + (2k - s) \cdot \ell_k \ge 2 \sum_{i=k+1}^{s} \ell_i$, where the charges that remain after the $s - k$ smallest values have two each go to values at least $\ell_k \ge 0$. $\square$

**Theorem.** ALG $\le \frac{1}{2}(\lceil \lg n \rceil + 1) \cdot \text{OPT}$.

*Proof.* Let $L = \lceil \lg n \rceil$, so $2^{L} \ge n$. Apply Lemma 4 with $k = 2^j$ for $j = 0, 1, \ldots, L - 1$. The ranges $k + 1 \le i \le \min(2k, n)$ are $\{2\}$, $\{3, 4\}$, $\{5, \ldots, 8\}$, and so on. They have no index in common, and together they cover the indices $2, 3, \ldots, \min(2^L, n) = n$. The sum of the $L$ inequalities is

$$L \cdot \text{OPT} \ge 2 \sum_{i=2}^{n} \ell_i.$$

Lemma 2 gives $\text{OPT} \ge 2\,\ell_1$. Add the two inequalities: $(L + 1) \cdot \text{OPT} \ge 2 \sum_{i=1}^{n} \ell_i = 2 \cdot \text{ALG}$. $\blacksquare$

The proof uses only Lemmas 1 and 2. So the same bound holds for each tour whose leaving costs satisfy these two lemmas, whatever the start city and the tie rule. The lower bounds on OPT are of two kinds: the cost of one edge (Lemma 2) and the cost of a tour on a subset (Lemma 3).

**The lower-bound family.** The Hougardy and Wilde grid $G_k$ has $n = 16 \cdot 2^k - 6$ points in two rows, with the Manhattan metric. All costs are at least 1, and the boundary of the grid is a tour with $n$ unit edges, so OPT $= n$. The nearest-neighbor path $P_k$ of the implementation goes to a closest unvisited point at each step and has length $(12 + 4k) 2^k - 3$. It ends in the top row at the middle column $(W_k - 1)/2$, with $W_k = 8 \cdot 2^k - 3$, so the closing edge to the start $(0, 0)$ costs $(W_k + 1)/2 = 4 \cdot 2^k - 1$. So ALG $= (16 + 4k) 2^k - 4$, and

$$\frac{\text{ALG}}{\text{OPT}} = \frac{(16 + 4k) 2^k - 4}{16 \cdot 2^k - 6} \ge \frac{k + 4}{4} = \frac{\lg(n + 6)}{4},$$

because $\frac{k+4}{4}(16 \cdot 2^k - 6) = (16 + 4k) 2^k - \frac{3}{2}(k + 4)$ and $\frac{3}{2}(k + 4) \ge 4$. The length of $P_k$ follows from the recursion of the construction: $P_{k+1}$ is $P_k$ in the left copy, a jump of $(W_k + 1)/2$, four unit steps, $P_k$ in the right copy, a jump of $(W_k + 1)/2$ and one unit step, so $|P_{k+1}| = 2|P_k| + W_k + 6$. The test file checks each step of $P_k$ for $k \le 5$. So the upper bound of the theorem is tight up to a constant factor, and the ratio of the nearest-neighbor heuristic on metric instances is $\Theta(\log n)$.
