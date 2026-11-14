---
title: SDC scheduling is exact for timing rules and sound for resource limits
proves: [correctness]
status: full
---

We use the notation of the page. $C$ is the set of rows $s_v - s_u \ge w$ built by lines L2, L3 and L7, plus any user rows, with integer $w$. The bound rows of L8 are $s_v \le U_v$ with integer $U_v$. Write $P$ for the set of real vectors $s \ge 0$ that meet $C$ and the bound rows.

**Lemma 1 (total unimodularity).** Let $M$ be a matrix in which each row has either exactly one $+1$ and one $-1$ and zeros elsewhere, or exactly one nonzero entry, equal to $\pm 1$. Then every square submatrix of $M$ has determinant $0$, $1$ or $-1$.

*Proof.* By induction on the size $r$ of a square submatrix $Q$. For $r = 1$ the entries are $0$ and $\pm 1$. For $r > 1$: if a row of $Q$ is zero, $\det Q = 0$. If a row of $Q$ has exactly one nonzero entry, expand along it: $\det Q = \pm \det Q'$ for a square submatrix $Q'$ of size $r - 1$, and the claim holds by induction. Otherwise every row of $Q$ has two nonzero entries, which must be one $+1$ and one $-1$, so the sum of the columns of $Q$ is the zero vector and $\det Q = 0$. $\square$

The rows of $C$, written as $-s_u + s_v \ge w$, have the first form. The bound rows $s_v \le U_v$ and the sign rows $s_v \ge 0$ have the second form. So the full matrix of $P$ is totally unimodular. The same holds for the matrix $[A \mid I]$ of the standard form that the simplex method uses, because a square submatrix that uses some columns of $I$ can be expanded along them, each with at most one nonzero entry, down to a square submatrix of $A$.

**Theorem 1 (integral vertices).** Every vertex of $P$ is an integer vector. If $P$ is nonempty and bounded, a linear objective attains its minimum over $P$ at an integer vertex, and the simplex method returns one.

*Proof.* A vertex $\bar s$ of $P \subseteq \mathbb{R}^n$ is the unique solution of $n$ rows of the system that hold with equality at $\bar s$ and are linearly independent. Let $Q$ be their $n \times n$ matrix and $q$ their right-hand sides, which are integers. By Lemma 1, $\det Q = \pm 1$, and by Cramer's rule each entry of $\bar s = Q^{-1} q$ is a determinant with integer entries divided by $\pm 1$, an integer. A nonempty polytope is the convex hull of its vertices, so a linear function attains its minimum at a vertex. The simplex method ends at a basic feasible solution of the standard form, which is a vertex of $P$, and its basis matrix is a nonsingular square submatrix of $[A \mid I]$, so the same argument applies to it. $\square$

**Lemma 2 (closed under minimum).** If $s$ and $t$ meet $C$ and $s, t \ge 0$, then $m = \min(s, t)$, taken entry by entry, meets $C$ and $m \ge 0$.

*Proof.* Take a row $s_v - s_u \ge w$. Say $m_u = s_u$; the case $m_u = t_u$ is the same with $s$ and $t$ swapped. Then $s_v \ge s_u + w = m_u + w$ and $t_v \ge t_u + w \ge s_u + w = m_u + w$, so $m_v = \min(s_v, t_v) \ge m_u + w$. $\square$

**Theorem 2 (least solution).** Line L9 starts with $s = 0$ and, in each round, sets $s_v \leftarrow \max(s_v, s_u + w)$ for every row. If $C$ with $s \ge 0$ has a solution, then after at most $n + 1$ rounds no row changes $s$, and $s$ is the least solution: $s \le t$ entry by entry for every solution $t$. If some round $n + 1$ still changes $s$, there is no solution.

*Proof.* Invariant: $s \le t$ for every solution $t$. It holds at the start since $t \ge 0$. An update sets $s_v = s_u + w \le t_u + w \le t_v$. Now add a source $z$ with a row $s_v - s_z \ge 0$ for each $v$ and fix $s_z = 0$. After round $i$, $s_v$ is at least the largest weight of a path from $z$ to $v$ with at most $i$ edges, by induction on $i$, and $s_v$ is always the weight of some walk from $z$ to $v$. If a solution $t$ exists, then going around any cycle of rows gives $0 \ge$ its total weight, so no cycle is positive, the largest walk weight equals the largest path weight, and paths have at most $n$ edges. So after round $n$ the values equal the longest path weights and round $n + 1$ changes nothing. A vector that no row changes meets every row, so it is a solution, and by the invariant it is the least one. Conversely, if round $n + 1$ changes some value, a walk with more than $n$ edges is heavier than every path, so it holds a positive cycle, and no solution exists. $\square$

**Corollary (lines L9 and L10).** With the bound rows, $P$ is nonempty exactly when the least solution $s^*$ of $C$ exists and $s^* \le U$: any point of $P$ is a solution of $C$, so it is at least $s^*$, and $s^* \le U$ then follows; the converse is clear. If $w_v \ge 0$ for all $v$, then $\sum_v w_v s^*_v \le \sum_v w_v t_v$ for every $t \in P$, so $s^*$ is optimal. With an integer $C$, $s^*$ is an integer vector, since every update adds integers.

**Theorem 3 (exact chaining).** Let $s$ meet $s_v \ge s_u + \ell(u)$ for every edge. Then $s$ meets the rows of L3 exactly when every path of combinational operations whose operations all start in one step has total delay at most $T$.

*Proof.* Suppose the rows of L3 hold, and let $p$ be a path of combinational operations from $u$ to $v$ that all start in step $j$. Its delay is at most $D(u, v)$. If $D(u, v) > T$, the row $s_v - s_u \ge \lceil D(u, v)/T \rceil - 1 \ge 1$ contradicts $s_u = s_v = j$. So $D(u, v) \le T$ and the delay of $p$ fits. Conversely, suppose every in-step path fits, and take $u, v$ with $D(u, v) > T$ and a path $p$ from $u$ to $v$ of delay $D(u, v)$. Along $p$ each edge leaves a combinational operation, so the starts do not decrease, and they take the values $s_u = j_0 < j_1 < \cdots < j_r = s_v$ with $r \le s_v - s_u$. The operations of $p$ with start $j_i$ form a contiguous piece of $p$ in one step, so its delay is at most $T$. The $r + 1$ pieces cover $p$, so $D(u, v) \le (r + 1) T \le (s_v - s_u + 1) T$, which gives $s_v - s_u \ge \lceil D(u, v)/T \rceil - 1$. $\square$

**Theorem 4 (sound resources).** Every $s$ that meets the rows of L7 for type $k$ has at most $a_k$ busy operations of type $k$ in each step.

*Proof.* Let $o_1, \ldots, o_r$ be the order of L6 and $c = a_k$. For a residue $i \in \{1, \ldots, c\}$, the operations $o_i, o_{i + c}, o_{i + 2c}, \ldots$ meet $s_{o_{i + (q+1)c}} \ge s_{o_{i + qc}} + o(o_{i + qc})$, so each one starts after the previous one is no longer busy. By induction along the chain, their busy intervals $[s, s + o)$ are pairwise disjoint, so in any step at most one of them is busy. The $c$ residues cover all operations of type $k$, so at most $c$ of them are busy in a step. $\square$

**Theorem 5 (feasible without a bound).** If there is no latency bound and no user row, then $C$ has a solution.

*Proof.* Let $\kappa(v) = (\mathrm{ALAP}(v), \mathrm{ASAP}(v), \mathrm{topo}(v))$, compared in lexicographic order, where ASAP and ALAP come from the rows of L2 and L3 and topo is the index in a topological order of $G$. The ASAP values are the least solution of those rows, and the ALAP values are computed by $\mathrm{ALAP}(u) = \min(\mathrm{ALAP}(u), \mathrm{ALAP}(v) - w)$ over the same rows. Every row of L2 and L3 has $w \ge 0$ and joins $u$ to $v$ along a path of $G$. So for such a row $\mathrm{ASAP}(v) \ge \mathrm{ASAP}(u) + w \ge \mathrm{ASAP}(u)$, $\mathrm{ALAP}(u) \le \mathrm{ALAP}(v) - w \le \mathrm{ALAP}(v)$ and $\mathrm{topo}(u) < \mathrm{topo}(v)$, which gives $\kappa(u) < \kappa(v)$. Every row of L7 joins $o_i$ to $o_{i + c}$ with $\kappa(o_i) < \kappa(o_{i + c})$ by the sort. So every row of $C$ goes from a smaller key to a larger one, the graph of the rows has no cycle at all, and by Theorem 2 the least solution exists. $\square$

**What is not claimed.** Theorem 4 shows that the rows of L7 are sufficient for the resource limits. They are not necessary: a valid schedule may break them. So the least solution of $C$ can have a larger latency than the best valid schedule. The page gives an instance with three operations where it loses one step.
