---
title: The four lists of the adaptive FMM use each source leaf exactly once for each target leaf, and every far route is well separated
proves: [correctness]
status: full
---

We use exact complex arithmetic. The tree is the one of line L1: a box of side $w_l = 2^{-l}$ at level $l$ is split when it holds more than $s$ charges, and empty children are dropped. So every box holds at least one charge, and a box is a leaf exactly when it has no children. Two boxes are *adjacent* if their closed squares share at least one point; a box is adjacent to itself. *Colleagues* are adjacent boxes of the same level. For a box $b$ at level $l$ and $k \le l$, $b_k$ is the ancestor of $b$ at level $k$, with $b_l = b$. The lists are as in line L2:

- $U(b)$, for a leaf $b$: the leaves adjacent to $b$.
- $V(b)$, for a box $b$ at level $l \ge 2$: the children of the colleagues of $b_{l-1}$ that are not adjacent to $b$.
- $W(b)$, for a leaf $b$: the boxes $d$ that are descendants of a colleague of $b$, are not adjacent to $b$, and whose parent is adjacent to $b$.
- $X(d)$: the leaves $b$ with $d \in W(b)$.

**Lemma 1 (adjacency is inherited upward).** If boxes $a$ and $c$ are adjacent, so are their parents, and so are $a$ and the parent of $c$. Hence, along the ancestors of two leaves, the levels $k$ at which $t_k$ and $c_k$ are adjacent form an initial segment $\{0, \ldots, k^*\}$, and along the ancestors of $c$, the boxes adjacent to a fixed box $t$ form an initial segment too.

*Proof.* A box is contained in its parent, so a shared point of $a$ and $c$ is a shared point of the larger boxes. Level 0 is the root, which is adjacent to itself. $\square$

**Lemma 2 (the lists computed by the code are the lists defined above).** For a leaf $b$, the code puts into $U(b)$ the box $b$, the leaf colleagues of the proper ancestors of $b$ that are adjacent to $b$, and the leaves reached by a descent from the colleagues of $b$ through adjacent boxes; it puts into $W(b)$ the children met in this descent that are not adjacent to $b$.

*Proof.* Let $a \ne b$ be a leaf adjacent to $b$ at level $k$. If $k < l$, the ancestor $b_k$ contains $b$, so $a$ is adjacent to $b_k$ and is a colleague of it. If $k \ge l$, the ancestor $a_l$ is adjacent to $b$ by Lemma 1 and is a colleague of $b$, and $a_l \ne b$: if $k = l$ then $a_l = a \ne b$, and if $k > l$ then $a_l$ has children while the leaf $b$ has none. All the boxes between $a_l$ and $a$ are adjacent to $b$ by Lemma 1, so the descent, which follows every adjacent child, reaches $a$. Conversely, each box the code adds to $U(b)$ is a leaf adjacent to $b$, and each leaf is added once, at its own level. For $W(b)$: the descent visits exactly the descendants of colleagues of $b$ whose ancestors down to the colleague are all adjacent to $b$, and it records a child exactly when it is not adjacent; by Lemma 1 this is the set of descendants that are not adjacent to $b$ and have an adjacent parent. $\square$

**Lemma 3 (each pair of leaves is covered exactly once).** Let $t$ and $c$ be leaves at levels $l_t$ and $l_c$. Then exactly one of the following holds:

1. $c \in U(t)$;
2. $c_k \in V(t_k)$ for some $k$ (and then $k$ is unique);
3. $c_k \in W(t)$ for some $k$ (unique);
4. $c \in X(t_k)$ for some $k$ (unique).

*Proof.* Let $m = \min(l_t, l_c)$, and let $\{0, \ldots, k^*\}$ be the levels at which $t_k$ and $c_k$ are adjacent (Lemma 1), with $k^* \le m$.

*Case A: $k^* < m$.* At $k = k^* + 1 \le m$, the boxes $t_k$ and $c_k$ exist, are not adjacent, and have adjacent parents, which are colleagues. So $c_k \in V(t_k)$. A $V$ relation between an ancestor of $t$ and an ancestor of $c$ needs the same level, non-adjacency at that level and adjacency one level up, so $k = k^* + 1$ is the only one. Route 1 fails, because $t$ and $c$ are inside the non-adjacent boxes $t_k$ and $c_k$. Route 3 would need an ancestor $c_j$ with $j > l_t$ whose parent is adjacent to $t$; then $c_{l_t}$, which contains that parent, would be adjacent to $t = t_{l_t}$, but $l_t \ge k > k^*$. Route 4 fails in the same way with the roles exchanged.

*Case B: $k^* = m$ and $l_t = l_c$.* Then $t$ and $c$ are adjacent leaves, so route 1 holds. Route 2 needs non-adjacency at a level at most $m$. Routes 3 and 4 need a box of one leaf at a level finer than the other leaf, which is not an ancestor of a leaf of the same level.

*Case C: $k^* = m = l_t < l_c$.* The box $c_{l_t}$ is adjacent to $t$, and it is not $t$, since $t$ is a leaf and $c_{l_t}$ has the descendant $c$; so it is a colleague of $t$. Route 2 fails, since $k^* = m$. Route 4 fails, since $X(t_k) \ni c$ needs $t_k \in W(c)$, a box finer than $c$, but $l_t < l_c$. If $c$ is adjacent to $t$, route 1 holds and route 3 fails, since all ancestors of $c$ contain $c$ and are adjacent to $t$. If not, let $c_j$ be the coarsest ancestor of $c$ that is not adjacent to $t$. By Lemma 1, $j > l_t$, the parent $c_{j-1}$ is adjacent to $t$, and $c_j$ descends from the colleague $c_{l_t}$, so $c_j \in W(t)$, and by Lemma 1 it is the only ancestor of $c$ in $W(t)$. Route 1 fails because $c$ is not adjacent to $t$.

*Case D: $k^* = m = l_c < l_t$.* This is Case C with $t$ and $c$ exchanged: either $c \in U(t)$, or the coarsest ancestor $t_j$ of $t$ that is not adjacent to $c$ has $t_j \in W(c)$, that is $c \in X(t_j)$, and no other route holds. $\square$

**Lemma 4 (separation).** (a) If $c \in V(b)$, both of side $w$, the centers are at least $2w$ apart. (b) If $d \in W(b)$, the box $d$ has side $w_d$ smaller than the side of $b$, and every point of $b$ is at distance at least $\frac{3}{2} w_d$ from the center of $d$. So the charges of $d$, which lie within $r = w_d / \sqrt{2}$ of its center, and the points $x$ of $b$ satisfy $r / |x - c_d| \le \rho = \sqrt{2} / 3$. (c) The same ratio holds for $b \in X(d)$, with the charges in $b$ and the targets in $d$ and its descendants.

*Proof.* (a) Two boxes of one level that are not adjacent are at least one side apart in one coordinate, so their centers differ by at least $2w$ in it. (b) The box $d$ descends from a colleague of $b$, so its level is finer. The boundaries of $b$ lie on the grid of spacing $w_d$. The closed squares of $d$ and $b$ are disjoint, so in one coordinate they are separated by a gap of at least $w_d$, and each point of $b$ differs from the center of $d$ by at least $w_d / 2 + w_d$ in that coordinate. (c) The pairs are the same as in (b), and the descendants of $d$ lie in $d$. $\square$

**Theorem.** Let $u_j$ be the output for a charge $j$ in leaf $t$, $u(z_j)$ the exact potential without the self term, and $A = \sum_i |q_i|$. With $\gamma = 2\sqrt{2} - 1$ and $\rho = \sqrt{2} / 3$,

$$|u_j - u(z_j)| \le A \max\left( \frac{4e(p + \gamma)(\gamma + 1) + \gamma^2}{\gamma (\gamma - 1)} \left( \frac{1}{\gamma} \right)^{p+1}, \; \frac{\rho^{p+1}}{(p + 1)(1 - \rho)} \right).$$

The bound tends to $0$ as $p \to \infty$.

*Proof.* By Lemma 3 the charges other than $j$ are split into disjoint groups, one for each source leaf $c$, and each group reaches $t$ by exactly one route. Route 1 is the direct sum of line L7, which is exact and leaves out $i = j$. The multipole coefficients of each box are exact after line L3 (P2M at the leaves, then the exact M2M of Lemma 2 of the [fast multipole method](/fast-multipole-method/) proof). The L2L shifts of line L5 are exact (Lemma 3 of the same proof). So the only errors are the truncations of the far routes. Route 2: by Lemma 4(a), Lemma 4.7 of Beatson and Greengard bounds the error of the M2L step for the box $c_k$, at every point of $t_k$, by $A_{c_k}$ times the first factor, as in Lemma 4 of the FMM proof. Route 3: the box $c_k \in W(t)$ is evaluated at $z_j$ from its $p$-term multipole expansion; by Lemma 4(b) and the 2D [truncation bound](/multipole-truncation-error-bound/) the error is at most $A_{c_k}$ times the second factor. Route 4: the local expansion of the charges of $c$ about the center $x_0$ of $t_k$ is the series $q_i \log(w - z_i) = q_i \log(x_0 - z_i) - q_i \sum_{l \ge 1} \frac{1}{l} \left( \frac{w - x_0}{z_i - x_0} \right)^l$, and by Lemma 4(c) the tail after $l = p$ is at most $|q_i| \rho^{p+1} / ((p+1)(1 - \rho))$. The errors add, and the sums $A_c$ over the disjoint source groups add to at most $A$. $\square$

The same argument with the derivatives of the series gives the convergence of the field. Since $\rho < 1 / \gamma$, the $W$ and $X$ routes converge faster than the $V$ route, and the first factor is the larger one for every $p$; so the bound is the same as for the uniform FMM.
