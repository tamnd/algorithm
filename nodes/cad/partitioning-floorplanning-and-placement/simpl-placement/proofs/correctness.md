---
title: The B2B cost is twice the span at its build point, the anchored system is positive definite, and every placement that SimPL returns is legal
proves: [correctness, termination, running time]
status: full
---

**Lemma 1 (B2B at the build point).** Let a net of weight $w$ have $p \ge 2$ pins with coordinates $c$, no two of them closer than $\varepsilon$, extreme pins $\ell$ and $u$, and span $L = c_u - c_\ell$. The B2B edges built at $c$ have the quadratic cost $2 w L$ at $c$.

*Proof.* An edge $(a, b)$ has weight $\frac{2 w}{(p - 1) |c_a - c_b|}$, so its cost at $c$ is $\frac{2 w}{p - 1} |c_a - c_b|$. The edge $(\ell, u)$ gives $\frac{2w}{p - 1} L$. An inner pin $q$ lies between $c_\ell$ and $c_u$, so its two edges give $\frac{2w}{p - 1} \bigl( (c_q - c_\ell) + (c_u - c_q) \bigr) = \frac{2w}{p - 1} L$. There are $p - 2$ inner pins, so the total is $\frac{2w}{p - 1} (1 + p - 2) L = 2 w L$. $\square$

**Lemma 2 (the anchored system).** For $\alpha > 0$, the matrix of line L7 is symmetric positive definite. For $\alpha = 0$ it is positive definite if every cell has a path of edges to a pad.

*Proof.* The cost is $\sum_{\text{edges}} w_{ab} (x_a - x_b)^2 + \alpha \sum_i (x_i - \hat x_i)^2$ with all $w_{ab} > 0$. Its quadratic part in the cell coordinates is $v^\top A v = \sum_{\text{cell edges}} w_{ab} (v_a - v_b)^2 + \sum_i \omega_i v_i^2 + \alpha \sum_i v_i^2$, where $\omega_i \ge 0$ is the weight of the edges from cell $i$ to pads. With $\alpha > 0$ the last sum is positive for $v \ne 0$. With $\alpha = 0$, $v^\top A v = 0$ forces $v$ constant along cell edges and zero at cells with a pad edge, so $v = 0$ when every cell reaches a pad. $\square$

So each solve has a unique minimum, the solution of $A x = b$, which the conjugate gradient method finds in at most $n$ steps in exact arithmetic.

**Lemma 3 (packing a row segment).** Let cells with integer widths and total width at most $s_1 - s_0$ be packed by the procedure of the page: in order of their targets, each goes to the site nearest its target, clamped to $[s_0, s_1 - W_i]$, but not left of the end of the previous cell; then, from the right, each cell is moved left to end at or before the start of the next cell, with the first limit $s_1$. The result has every cell inside $[s_0, s_1)$ and no two cells overlapping.

*Proof.* Number the cells $1, \ldots, m$ in the order. After the first pass, $p_j \ge p_{j-1} + W_{j-1}$, so $p_j \ge s_0 + \sum_{l < j} W_l$. The second pass sets $p'_m = \min(p_m, s_1 - W_m)$ and $p'_j = \min(p_j, p'_{j+1} - W_j)$. By induction from $j = m$ down, $p'_j \ge s_0 + \sum_{l < j} W_l$: the first term of the minimum satisfies it, and $p'_{j+1} - W_j \ge s_0 + \sum_{l \le j} W_l - W_j$ for $j < m$, while $s_1 - W_m \ge s_0 + \sum_{l < m} W_l$ because the total width fits. So every $p'_j \ge s_0$. The second pass gives $p'_j + W_j \le p'_{j+1}$ and $p'_m + W_m \le s_1$, so no two cells overlap and all end by $s_1$. All values are integers, so the cells are on sites. $\square$

**Theorem 1 (lookahead legalization is legal).** If lookahead legalization returns, every cell is on a site of a row, inside it, and no two cells overlap.

*Proof.* By induction on the recursion, every call gets a region of whole rows and sites and a set of cells whose total width is at most the room of the region. This holds at the top only if the cells fit the chip; otherwise a later check fails. A cut of the rows passes on only a split where both halves fit, or stops with an error. A cut of a single row does the same, or packs the whole segment, whose cells fit. A leaf is a single row segment whose cells fit, so Lemma 3 places them legally inside it. Different calls get disjoint regions, so cells from different leaves do not overlap. $\blacksquare$

**Theorem 2 (the result).** If SimPL returns, its result is legal, and its HPWL is the least HPWL among the UB placements computed, so it is at least the optimum of the placement problem on the same rows.

*Proof.* Line L5 keeps the UB placement of least HPWL, and each is legal by Theorem 1. A legal placement is a feasible point of the placement problem, so its HPWL is at least the least HPWL of all legal placements. $\blacksquare$

**Theorem 3 (termination and running time).** SimPL stops after at most the given number $k$ of iterations, in $O(k (t (n + P) + n \log n \log(K S)))$ time with $t$ conjugate gradient steps per solve.

*Proof.* The loop of line L3 has a bound. A net of $p$ pins has at most $2p - 3$ B2B edges, so the matrix has $O(n + P)$ entries and is built in that time; each conjugate gradient step multiplies by it once. The recursion of lookahead legalization halves the rows or the sites at each level, so it has $O(\log K + \log S)$ levels; the cells of the regions of one level are disjoint, so the sorts of one level cost $O(n \log n)$. Line L5 and line L8 cost $O(P)$. $\blacksquare$
