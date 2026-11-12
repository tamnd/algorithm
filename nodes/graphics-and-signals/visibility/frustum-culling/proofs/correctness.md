---
title: Frustum culling never drops a box that meets the frustum
proves: [correctness, termination]
status: full
---

We use the model and the pseudocode of the page. The frustum is $V = \bigcap_j H_j$ with $H_j = \{x : n_j \cdot x + d_j \ge 0\}$. A box is $\beta = \prod_k [lo_k, hi_k]$. Write $f_j(x) = n_j \cdot x + d_j$. Each node $v$ of the hierarchy has a box $\beta(v)$ that contains the box of each child and the box of each object of $v$.

**Termination.** Each node is pushed at most once, by its parent at line L11, and the hierarchy is finite. Each step of the loop does $O(1)$ work per active plane and per object of a leaf, plus the walk of line L8 over a finite subtree. So FRUSTUM-CULL stops.

**Lemma 1.** For each box $\beta$ and each plane $j$, $\max_{x \in \beta} f_j(x) = f_j(p)$ and $\min_{x \in \beta} f_j(x) = f_j(q)$, where $p$ is the p-vertex and $q$ the n-vertex of $\beta$ for $n_j$.

*Proof.* $f_j(x) = d_j + \sum_k n_{j,k} x_k$, and the coordinates $x_k \in [lo_k, hi_k]$ can be chosen independently. The term $n_{j,k} x_k$ is largest at $x_k = hi_k$ if $n_{j,k} \ge 0$ and at $x_k = lo_k$ otherwise, which is $p_k$. The minimum is the same with the roles swapped, which is $q_k$. $\square$

**Lemma 2.** If line L5 holds for a box and a plane $j$, then the box does not meet $V$. If line L7 fails for a box and a plane $j$, then the box is inside $H_j$.

*Proof.* If $f_j(p) < 0$, then $f_j(x) \le f_j(p) < 0$ for each $x \in \beta$ by Lemma 1, so $\beta \cap H_j = \emptyset$ and $\beta \cap V = \emptyset$. If $f_j(q) \ge 0$, then $f_j(x) \ge f_j(q) \ge 0$ for each $x \in \beta$. $\square$

**Lemma 3 (invariant).** Each entry $(v, A)$ on the stack satisfies $\beta(v) \subseteq H_j$ for each plane $j \notin A$.

*Proof.* The first entry has $A$ = all planes. An entry $(c, \text{left})$ is pushed at line L11 for a child $c$ of a node $v$ popped with the set $A$. A plane $j \notin \text{left}$ is either not in $A$, and then $\beta(c) \subseteq \beta(v) \subseteq H_j$ by the invariant for $v$; or it is in $A$ and line L7 failed for it, and then $\beta(c) \subseteq \beta(v) \subseteq H_j$ by Lemma 2. $\square$

**Theorem 1.** If the box of object $i$ meets $V$, then $i$ is in the output.

*Proof.* Let $v_0 = R, v_1, \ldots, v_m$ be the path from the root to the leaf that holds $i$. Each box $\beta(v_t)$ contains $\beta(i)$, so it meets $V$, and by Lemma 2 line L5 never holds for it; the same is true for $\beta(i)$ at line L10. So no node of the path is skipped at line L6. Follow the path from the root. If some $v_t$ reaches line L8 with an empty set, then $i$ is added there, because $i$ is below $v_t$. Otherwise each $v_t$ with $t < m$ pushes $v_{t+1}$ at line L11, and $v_m$ reaches line L10, where $\beta(i)$ is not outside any plane of left, so $i$ is added. $\square$

**Theorem 2.** The output is the set of objects $i$ such that no plane $j$ has $f_j(p) < 0$ at the p-vertex $p$ of $\beta(i)$. So the hierarchy gives the same answer as the flat test of each box against all six planes.

*Proof.* If the flat test drops $i$ at a plane $j$, then $\beta(i)$ is outside $H_j$, so each node box on the path is not inside $H_j$. By Lemma 3, $j$ is still active at each node of the path, so line L8 does not accept $i$ at a node of the path, and line L10 tests $i$ against $j$ and drops it, unless a node of the path is skipped earlier. If the flat test keeps $i$, then $\beta(i)$ meets each $H_j$, and the argument of Theorem 1 with "meets $H_j$ for each active $j$" in place of "meets $V$" shows that $i$ is added: no node of the path fails at line L5, because each node box contains $\beta(i)$ and Lemma 1 gives $f_j(p(v)) \ge f_j(p(i)) \ge 0$; at line L10, the planes not in left hold all of $\beta(i)$ by Lemma 3. $\square$

**Remark.** The converse of Theorem 1 is false. The box D of the example is inside each closed half-space $H_j$ at some point, but no point of D is in all six, so it is kept although it does not meet $V$. Theorem 2 shows that this is the only kind of error. $\blacksquare$
