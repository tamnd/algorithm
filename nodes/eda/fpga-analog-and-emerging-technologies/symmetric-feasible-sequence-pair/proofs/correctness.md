---
title: The key lemma of symmetric-feasible sequence pairs, and what SYM-PACK returns
proves: [correctness]
status: partial
---

Notation. The cells have widths $w$ and heights $h$. A sequence pair is two orders $\Gamma^+$ and $\Gamma^-$ of the cells, with positions $p^+(u)$ and $p^-(u)$. As on the [sequence pair](/sequence-pair/) page, $u$ is left of $v$ if $p^+(u) < p^+(v)$ and $p^-(u) < p^-(v)$, and $u$ is below $v$ if $p^+(u) > p^+(v)$ and $p^-(u) < p^-(v)$. Every two distinct cells are in exactly one of these four relations ($u$ left of $v$, $v$ left of $u$, $u$ below $v$, $v$ below $u$).

A symmetric set $G$ is a set of cells with an involution $\mathrm{sym} : G \to G$. A pair is $\{u, \mathrm{sym}(u)\}$ with $u \neq \mathrm{sym}(u)$, and the two cells have the same width and height. A self-symmetric cell has $\mathrm{sym}(s) = s$. The pair $(\Gamma^+, \Gamma^-)$ is symmetric-feasible for $G$ if

$$(C) \qquad p^+(x) < p^+(y) \iff p^-(\mathrm{sym}(y)) < p^-(\mathrm{sym}(x)) \quad \text{for all distinct } x, y \in G.$$

A placement is symmetric if there is a vertical axis $x = X$ such that the two cells of each pair have the same $y$ and centers mirrored about the axis, and each self-symmetric cell has its center on the axis.

**Lemma 1 (the key lemma).** Let $(C)$ hold, and let $u \neq v$ be in $G$.

1. If $u$ is left of $v$, then $\mathrm{sym}(v)$ is left of $\mathrm{sym}(u)$.
2. If $u$ is below $v$, then $\mathrm{sym}(u)$ is below $\mathrm{sym}(v)$.
3. The two cells of a pair are in a left-of relation, not a below relation.
4. Two self-symmetric cells are in a below relation, not a left-of relation.

*Proof.* (1) $p^+(u) < p^+(v)$, so $(C)$ with $x = u$, $y = v$ gives $p^-(\mathrm{sym}(v)) < p^-(\mathrm{sym}(u))$. Apply $(C)$ to $x = \mathrm{sym}(v)$, $y = \mathrm{sym}(u)$, which are distinct: $p^+(\mathrm{sym}(v)) < p^+(\mathrm{sym}(u))$ if and only if $p^-(u) < p^-(v)$, which holds. So $\mathrm{sym}(v)$ is before $\mathrm{sym}(u)$ in both orders.

(2) $p^+(v) < p^+(u)$, so $(C)$ with $x = v$, $y = u$ gives $p^-(\mathrm{sym}(u)) < p^-(\mathrm{sym}(v))$. Apply $(C)$ to $x = \mathrm{sym}(u)$, $y = \mathrm{sym}(v)$: $p^+(\mathrm{sym}(u)) < p^+(\mathrm{sym}(v))$ if and only if $p^-(v) < p^-(u)$, which is false. So $p^+(\mathrm{sym}(u)) > p^+(\mathrm{sym}(v))$ and $p^-(\mathrm{sym}(u)) < p^-(\mathrm{sym}(v))$.

(3) Take $x = u$, $y = \mathrm{sym}(u)$. Then $(C)$ reads $p^+(u) < p^+(\mathrm{sym}(u)) \iff p^-(u) < p^-(\mathrm{sym}(u))$. The two cells are in the same order in both sequences.

(4) For $s \neq t$ self-symmetric, $(C)$ reads $p^+(s) < p^+(t) \iff p^-(t) < p^-(s)$. The two cells are in opposite orders. $\square$

Lemma 1 is what makes symmetry possible. Part 3 says that the two cells of a pair are never asked to be one above the other, so they can share one $y$. Part 4 says that the self-symmetric cells, which all sit on the axis, are never asked to be side by side. Parts 1 and 2 say that the relations inside the group look the same in a mirror.

**Lemma 2 (the count).** Let $G$ have $g$ cells among $n$. For each $\Gamma^+$, exactly $n!/g!$ orders $\Gamma^-$ satisfy $(C)$. So there are $(n!)^2/g!$ symmetric-feasible pairs.

*Proof.* Condition $(C)$ says that the order of the group cells in $\Gamma^-$ is the list of the mirrors $\mathrm{sym}(x)$ of the group cells, taken in the reverse of their order in $\Gamma^+$. This fixes one of the $g!$ relative orders of $G$ in $\Gamma^-$, and leaves the rest of $\Gamma^-$ free. Each relative order is taken by $n!/g!$ permutations. $\square$

The same argument shows that REPAIR, which keeps the slots of $G$ in $\Gamma^-$ and refills them in this forced order, returns a symmetric-feasible pair, and returns $\Gamma^-$ itself when $(C)$ already holds.

**Lemma 3 (the merged vertical graph is acyclic).** Let $(C)$ hold. Merge the two cells of each pair into one node, and draw an arc from the node of $u$ to the node of $v$ when $u$ is below $v$. This graph has no cycle.

*Proof.* The below relation itself is a strict partial order: if $u$ is below $v$ and $v$ is below $t$, then $u$ is before $t$ in $\Gamma^-$ and after $t$ in $\Gamma^+$. Suppose the merged graph has a cycle. Write it as a closed walk of below relations $u_1$ below $v_1$, $u_2$ below $v_2$, ..., where $u_{i+1}$ is $v_i$ or its mirror. If $u_{i+1} = v_i$ at every step, transitivity gives $u_1$ below $u_1$, which is false. So the walk changes to the mirror at least once. Join the runs between two changes by transitivity. This gives group cells $a_1, b_1, \ldots, a_k, b_k$ with $a_i$ below $b_i$ and $a_{i+1} = \mathrm{sym}(b_i)$, indices mod $k$.

Let $f(x) = p^-(x) + p^-(\mathrm{sym}(x))$ for $x \in G$. If $a$ is below $b$, then $p^-(a) < p^-(b)$, and by Lemma 1 (2) $\mathrm{sym}(a)$ is below $\mathrm{sym}(b)$, so $p^-(\mathrm{sym}(a)) < p^-(\mathrm{sym}(b))$. So $f(a) < f(b)$. Also $f(\mathrm{sym}(b)) = f(b)$. Around the cycle, $f(a_1) < f(b_1) = f(a_2) < \cdots < f(b_k) = f(a_1)$, which is false. $\square$

**Theorem 4 (the $y$ coordinates).** Lines L3 to L5 give each cell the least $y$ such that every below relation holds and the two cells of each pair have the same $y$.

*Proof.* By Lemma 3, line L4 orders all nodes. The constraints $y_v \ge y_u + h_u$ for $u$ below $v$, with one variable per node, form a system of difference constraints on a DAG. The longest-path values of line L5 satisfy it, and every solution is at least these values, by induction along the order. $\square$

**Theorem 5 (the group alone).** Let $(C)$ hold, and let every cell be in $G$. Let $x^L$ be the least $x$ coordinates that keep the left-of relations (longest paths in the horizontal graph), and $T = \max_u (x^L_u + w_u)$ the least width. Then

$$a_u = \tfrac12 \big( x^L_u + T - w_u - x^L_{\mathrm{sym}(u)} \big)$$

keeps every left-of relation, fits in $[0, T]$, and is symmetric about $X = T/2$. So for a group alone, symmetry costs no width.

*Proof.* Let $m_u = T - w_u - x^L_{\mathrm{sym}(u)}$. As $w_{\mathrm{sym}(u)} = w_u$ and $0 \le x^L_{\mathrm{sym}(u)} \le T - w_u$, we have $0 \le m_u \le T - w_u$. If $u$ is left of $v$, then by Lemma 1 (1) $\mathrm{sym}(v)$ is left of $\mathrm{sym}(u)$, so $x^L_{\mathrm{sym}(v)} + w_v \le x^L_{\mathrm{sym}(u)}$, and so $m_u + w_u = T - x^L_{\mathrm{sym}(u)} \le T - w_v - x^L_{\mathrm{sym}(v)} = m_v$. So $m$ keeps the relations, and $x^L$ does too. The constraints are linear, so the mean $a = (x^L + m)/2$ keeps them and fits in $[0, T]$. Finally $a_u + a_{\mathrm{sym}(u)} = T - w_u$, so the centers $a_u + w_u/2$ and $a_{\mathrm{sym}(u)} + w_u/2$ add to $T$, and a self-symmetric cell has the center $T/2$. $\square$

**Free cells.** With cells outside $G$, the mirror $m$ above breaks the relations between free cells and group cells, and Theorem 5 does not apply. Balasa and Lampaert prove that every symmetric-feasible pair still has a symmetric placement that keeps all the relations of the pair (Balasa and Lampaert 2000, the section on symmetric-feasible sequence pairs). This page does not repeat that proof. Line L7 solves the linear program of line L6, so it finds such a placement when one exists. In the tests it found one for every symmetric-feasible pair that was tried, and line L7 raises an error if it ever does not.

**Theorem 6 (what SYM-PACK returns).** If line L7 succeeds, the placement keeps every relation of the pair, is symmetric, and has the least width and the least height among all such placements. So its area is the least among the symmetric placements that keep the relations of the pair.

*Proof.* Every left-of relation and the symmetry equations are rows of the program of line L6, and $W$ bounds every right edge. The program minimizes $W$, so the width is the least. The $y$ part is Theorem 4, and the symmetry of $y$ holds because each pair is one node. Two cells in a relation do not overlap, and every two cells are in a relation, so no two cells overlap. The $x$ and $y$ constraints share no variable, so the least width and the least height are reached together. $\square$

What is proved here: Lemmas 1 to 3 and Theorems 4 to 6, and the symmetric $x$ placement for a group with no free cells. What is cited: the existence of a symmetric placement when free cells are present. What is measured: the tests check the count of Lemma 2, Lemma 1 on all pairs of 4 cells, the placements of random instances, and, on two small instances, that the best area over all symmetric-feasible pairs equals the best area of a search over a half-unit grid.
