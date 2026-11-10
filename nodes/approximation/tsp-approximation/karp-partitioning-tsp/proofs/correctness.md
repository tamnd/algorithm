---
title: The grid form of Karp's scheme is within an additive O(kL) of OPT
proves: [correctness]
status: full
---

The input is a set $S$ of $n$ points in the plane with the Euclidean distance, and an integer $k \ge 1$. Let $Q$ be the bounding square of $S$, with side $L$. The algorithm cuts $Q$ into $k \times k$ cells of side $a = L/k$, half-open so that each point of $Q$ is in exactly one cell. It computes an optimal tour $T_C$ of $S \cap C$ for each nonempty cell $C$, takes the nonempty cells $C_1, \ldots, C_m$ in snake order (row by row, the direction changes in each row), and joins the cell tours as described below. The deterministic bound is a full proof. The statement about random points at the end is quoted from Karp (1977) and Beardwood, Halton and Hammersley (1959), with a short argument that is a sketch.

**Lemma 1 (Karp's cell lemma).** For each cell $C$, let $\lambda(C)$ be the length of the part of an optimal tour $T^*$ that lies in $C$. Then

$$\text{OPT}(S \cap C) \le \lambda(C) + \tfrac{3}{2} \operatorname{per}(C),$$

where $\operatorname{per}(C) = 4a$ is the perimeter of $C$.

*Proof.* If $S \cap C$ has at most one point, the left side is 0. If $T^*$ lies in the closure $\bar C$, then $\text{OPT}(S \cap C) \le \text{OPT} = \lambda(C)$, because shortcuts of $T^*$ give a tour of $S \cap C$. Otherwise the closure of $T^* \cap C$ is a finite set of polygonal paths in $\bar C$, each with both ends on the boundary $\partial C$, and together they pass through all points of $S \cap C$. Let $x_1, \ldots, x_{2j}$ be their ends, in the order around $\partial C$; there is an even number of ends, since each path has two. These points cut $\partial C$ into $2j$ arcs. Number the arcs alternately odd and even. One of the two classes has total length at most $\operatorname{per}(C)/2$; call it $A$.

Build the multigraph $G$ from the paths, the whole boundary $\partial C$, and a second copy of each arc of $A$. Each end $x_i$ has degree 1 from its path, 2 from $\partial C$, and 1 from $A$, because exactly one of the two arcs at $x_i$ is in $A$. So all degrees are even. $G$ is connected, because each path meets $\partial C$. So $G$ has an [Eulerian circuit](/eulerian-circuit/), of length at most $\lambda(C) + \operatorname{per}(C) + \operatorname{per}(C)/2$. The circuit passes through all points of $S \cap C$. Shortcuts in the plane, by the triangle inequality, give a tour of $S \cap C$ that is not longer. $\square$

**Lemma 2 (the cell tours).** $\sum_{C} \text{OPT}(S \cap C) \le \text{OPT} + \tfrac{3}{2} \cdot m \cdot 4a \le \text{OPT} + 6kL$.

*Proof.* The cells are disjoint and cover $Q$, so $\sum_C \lambda(C) = \text{OPT}$. Add Lemma 1 over the $m \le k^2$ nonempty cells, and use $k^2 \cdot 4a = 4kL$. $\square$

**The join.** Let $p_i$ be the first point of the path added for $C_i$, and let $q_i$ be its last point. The path is the cycle $T_{C_i}$ with its edge $q_i p_i$ removed, so its length is $|T_{C_i}| - d(q_i, p_i)$. (If $C_i$ has one point, $p_i = q_i$ and the path has length 0.) The tour is the path of $C_1$, the edge $q_1 p_2$, the path of $C_2$, and so on, and the closing edge $q_m p_1$. With $p_{m+1} = p_1$, the triangle inequality gives $d(q_i, p_{i+1}) \le d(q_i, p_i) + d(p_i, p_{i+1})$, so

$$\text{ALG} \le \sum_{i=1}^{m} |T_{C_i}| + \sum_{i=1}^{m} d(p_i, p_{i+1}). \tag{1}$$

The choice of $p_i$ in each cell does not matter for (1). The implementation takes the point that is nearest to $q_{i-1}$.

**Lemma 3 (the snake).** $\sum_{i=1}^{m} d(p_i, p_{i+1}) \le (1 + \sqrt{2})\, kL + \sqrt{2}\, L$.

*Proof.* Let $c_i$ be the center of $C_i$. A point of a cell is at distance at most $a/\sqrt{2}$ from its center. Two cells that are consecutive in the snake order of all $k^2$ cells are side neighbors, so their centers are at distance $a$. For $i < m$, walk from $c_i$ to $c_{i+1}$ through the cells between them in snake order; so $d(p_i, p_{i+1}) \le \sqrt{2}\,a + a \cdot s_i$, where $s_i$ is the number of snake steps from $C_i$ to $C_{i+1}$. The steps for different $i$ are different, so $\sum_{i < m} s_i \le k^2 - 1$. The last term $d(p_m, p_1)$ is at most the diameter $\sqrt{2}\,L$ of $Q$. So the sum is at most $\sqrt{2}\, a \cdot m + a (k^2 - 1) + \sqrt{2}\, L \le \sqrt{2}\, kL + kL + \sqrt{2}\, L$, with $m \le k^2$ and $a k^2 = kL$. $\square$

**Theorem.** For every point set and every $k \ge 1$,

$$\text{OPT} \le \text{ALG} \le \text{OPT} + \left((7 + \sqrt{2})\, k + \sqrt{2}\right) L.$$

For $k = 1$ the algorithm returns an optimal tour.

*Proof.* The lower bound holds because ALG is the length of a tour. For the upper bound, put Lemma 2 and Lemma 3 into (1). For $k = 1$ there is one cell, and its tour is an optimal tour of $S$. $\blacksquare$

**Random points (quoted, with a sketch).** Let the $n$ points be uniform and independent in the unit square, so $L \le 1$. Beardwood, Halton and Hammersley (1959) proved that $\text{OPT}/\sqrt{n} \to \beta$ almost surely, for a constant $\beta > 0$; numerical estimates put $\beta$ near 0.7124. Choose $k = \lceil \sqrt{n / t} \, \rceil$, so that a cell holds about $t$ points on average. Then the additive error of the theorem is about $(7 + \sqrt{2}) \sqrt{n/t}$, and its ratio to OPT is about $(7 + \sqrt{2}) / (\beta \sqrt{t})$, which goes to 0 as $t$ grows. This is the idea of Karp's result: for each $\varepsilon > 0$ there is a $t$ such that the tour is at most $(1 + \varepsilon) \cdot \text{OPT}$ almost surely as $n \to \infty$. For the grid form on this page the argument is a sketch: the cells of a fixed grid do not all hold at most $t$ points, and the time of the dynamic program depends on the largest cell. Karp's own scheme cuts at medians, so that each cell holds at most $t$ points, and his proof handles the boundary lengths of these cells.
