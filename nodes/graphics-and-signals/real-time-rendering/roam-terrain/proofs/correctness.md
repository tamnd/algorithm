---
title: The ROAM wedgies bound the surface, forced splits keep the mesh conforming, and with monotone priorities a frame ends at the unique smallest conforming triangulation whose leaves all meet the error bound
proves: [correctness]
status: full
---

We use the notation of the page. The domain is the square $[0, M]^2$ with $M = 2^k$, and $h$ gives a height to each grid point. A bintree triangle $T = (a, v_0, v_1)$ has the apex $a$ at its right angle and the base $v_0 v_1$. Its children are $T_0 = (c, a, v_0)$ and $T_1 = (c, v_1, a)$, where $c$ is the midpoint of the base. The two roots have level 0, and a child has the level of its parent plus 1. A triangle of level $\ell$ has legs of length $s_\ell = M / 2^{\ell/2}$ and a base of length $\sqrt2\, s_\ell$. The partner of $T$ is the triangle of the same level that shares its base, if the base is not on the border of the square. Heights and priorities are exact rationals.

A *mesh* is the set of leaves of a cut of the bintree: a set $S$ of split triangles that holds the parent of each of its members, and whose leaves are the triangles not in $S$ whose parent is in $S$ (or the roots, when they are not in $S$). The leaves tile the square. Two bintree triangles are either nested or have disjoint interiors. A mesh is *conforming* when no vertex of a leaf lies inside an edge of another leaf; then each edge of a leaf is an edge of exactly one other leaf, or lies on the border.

We use one fact of the construction. For each level $\ell$, the triangles of level $\ell$ form a conforming triangulation of the square, and its vertex set $V_\ell$ grows with $\ell$. (Even levels are square grids of spacing $M / 2^{\ell/2}$ cut by diagonals; odd levels are the grids of diamonds between them.) The midpoint of a base of a level $\ell$ triangle is in $V_{\ell + 1}$ but not in $V_\ell$.

## The wedgies

Let $H$ be the surface over the finest level: on each leaf of the full bintree, the plane through its three corners. Let $P_T$ be the plane over $T$ through its three corners. Lines L10 and L11 compute $e_T = 0$ for a leaf of the full bintree and $e_T = \max(e_{T_0}, e_{T_1}) + |h(c) - (h(v_0) + h(v_1))/2|$ otherwise. This is Equation (1) of Duchaineau et al., with the height written $h$ in place of their $z$.

**Lemma 1.** For every bintree triangle $T$ and every domain point $p \in T$, $|H(p) - P_T(p)| \le e_T$. Also $e_{T_0}, e_{T_1} \le e_T$.

*Proof.* The second claim holds because the gap term is nonnegative. The first is by induction from the finest level. On a leaf of the full bintree, $H = P_T$. For an inner $T$, let $p \in T_j$. Then $|H(p) - P_T(p)| \le |H(p) - P_{T_j}(p)| + |P_{T_j}(p) - P_T(p)|$. The first term is at most $e_{T_j}$ by induction. The difference $P_{T_j} - P_T$ is affine on $T_j$, so its largest absolute value on $T_j$ is at a corner. It is 0 at the corners $a$ and $v_j$, which $T_j$ shares with $T$. At $c$ it is $h(c) - P_T(c) = h(c) - (h(v_0) + h(v_1))/2$, because $c$ is the midpoint of the base and $P_T$ is affine. So the sum is at most $e_{T_j} + \mathrm{gap} \le e_T$. $\square$

**Lemma 2.** The priority of line L12, $p(T) = e_T^2 / \max(\mathrm{dist}(\mathrm{eye}, T)^2, d_0^2)$, is monotone: $p(T_j) \le p(T)$.

*Proof.* $e_{T_j} \le e_T$ by Lemma 1, and $T_j \subseteq T$, so the distance from the eye to $T_j$ is at least the distance to $T$. $\square$

The priority is the square of the bound of the page, so that it stays rational; the order is the same. It is a heuristic for the screen error: it bounds the error of the height as seen from the eye up to the factor of the projection, but not the error of the line of sight as in Section 6.2 of the paper.

## Forced splits

**Lemma 3.** In a conforming mesh, let $t$ be a leaf and $b$ the leaf that has the base of $t$ as an edge. Either $b$ is the partner of $t$ (the same level, the same base), or the base of $t$ is a leg of $b$ and $b$ has the level of $t$ minus 1.

*Proof.* The shared edge has the length $\sqrt2\, s_\ell$ for the level $\ell$ of $t$. If it is the base of $b$, then $b$ has level $\ell$ and shares its base with $t$, so $b$ is the partner. If it is a leg of $b$, then $s_{\ell(b)} = \sqrt2\, s_\ell = s_{\ell - 1}$. $\square$

**Lemma 4.** If the mesh is conforming and $t$ is a leaf with children, FORCE-SPLIT$(t)$ (lines L1 to L5) ends, $t$ is split at the end, the mesh is conforming after each split, and at most $2(\ell(t) + 1)$ triangles are split.

*Proof.* A split of a leaf $u$ with no base neighbor (base on the border) keeps the mesh conforming: the legs of $u$ become the bases of its children with the same neighbors, the new edge $a c$ is shared by the two children, and the two halves of the base are on the border. A split of a diamond, a leaf $u$ and its partner, also keeps it: the two halves of the common base are each shared by one child of $u$ and one child of the partner.

The stack holds triangles whose levels decrease by 1 from each entry to the next one above it. This holds at the start. Line L4 pushes $b$ only when the base of the top $u$ is a leg of $b$, and then $b$ has the level of $u$ minus 1 by Lemma 3. Line L5 splits the top $u$ and its partner, or $u$ alone on the border, and these are the two cases that keep the mesh conforming. A split removes only the top entry and its partner, which have the level of the top. All entries below are finer, so they stay leaves. After the split of $b$, its child whose base is the old leg is a leaf, and it is the new base neighbor of the entry below, with the same base. So the next pass splits that entry with it as a diamond.

The stack has at most $\ell(t) + 1$ entries. Each pass pops, pushes, or splits and pops. Each push puts a strictly coarser triangle on top, so there are at most $\ell(t)$ pushes in a row, and each split pops one entry. So the loop ends. The bottom entry $t$ is popped only after it is split, because it stays a leaf until line L5 splits it. Each level gives at most one diamond, so at most $2(\ell(t) + 1)$ splits happen. $\square$

## A conforming mesh is closed under partners

**Lemma 5.** If a mesh with split set $S$ is conforming, then $S$ holds the partner of each of its members.

*Proof.* Let $T \in S$ with partner $T'$, and suppose $T' \notin S$. Then $T'$ lies in a leaf $L$: $L = T'$ or a proper ancestor of $T'$. The midpoint $c$ of the common base is a vertex of a child of $T$, so of a leaf inside $T$. The leaf $L$ is not an ancestor of $T$ (it is not split) and not inside $T$ (it holds $T'$), so it does not overlap the interior of $T$, and $c$, which lies on the boundary of $T$, is not in the interior of $L$. So $c$ is on the boundary of $L$. The level of $L$ is at most $\ell(T)$, so the vertices of $L$ are in $V_{\ell(T)}$, and $c$ is not. So $c$ is inside an edge of $L$, and the mesh is not conforming. $\square$

## One frame

Let $\varepsilon \ge 0$, let $P = \{T : p(T) > \varepsilon^2\}$, and let $C$ be the smallest set that holds $P$ and the parent and the partner of each of its members. This is the set that `target` builds. A triangle in $P$ has $e_T > 0$, so it has children.

**Theorem 6.** Start from any conforming mesh. After UPDATE (lines L6 to L9), the split set is exactly $C$. So the mesh is the set of leaves of $C$, whatever mesh the frame started from.

*Proof.* *The split phase (lines L6 and L7).* The heap holds an entry for each leaf: all leaves at the start, and each leaf that a split adds. The phase pops entries in the order of priority, skips those that are no longer leaves, and force-splits a leaf with $p > \varepsilon^2$. It stops at a leaf with $p \le \varepsilon^2$, and all remaining entries have a priority no larger. Each force split adds new leaves, so the phase ends after a finite number of splits (the bintree is finite). At its end every leaf has $p \le \varepsilon^2$, and the mesh is conforming by Lemma 4. Now let $T \in P$. If $T$ were not split, then a leaf $L$ would be $T$ or an ancestor of $T$, and $p(L) \ge p(T) > \varepsilon^2$ by Lemma 2. So $S \supseteq P$. By Lemma 5 and the parent rule, $S \supseteq C$.

*The merge phase (line L8).* A diamond $T$ (with its partner $T'$, or alone on the border) is mergeable when $T$ is split and all children of $T$ and of $T'$ are leaves. A merge removes $T$ and $T'$ from $S$. The new leaves $T$ and $T'$ have as legs the bases of the old children, with the same neighbors, and the common base is shared by $T$ and $T'$, so the mesh stays conforming. The phase merges only diamonds with $\max(p(T), p(T')) \le \varepsilon^2$, so it never removes a member of $P$, and $S \supseteq C$ stays true. A diamond becomes mergeable only when a merge makes the last of its children a leaf, and then its parent diamond is pushed. So when the phase stops, every mergeable diamond has a priority above $\varepsilon^2$.

*No extra split remains.* Suppose $S \setminus C$ is not empty, and let $T$ be a member of the greatest level. A child of $T$ in $S$ would be in $C$ by the choice of $T$, and then its parent $T$ would be in $C$. So both children of $T$ are leaves. The partner $T'$, if any, is in $S$ by Lemma 5, and not in $C$, because $C$ holds the partners of its members and the partner of $T'$ is $T$. So the children of $T'$ are leaves too. The diamond of $T$ is mergeable, and its priority is at most $\varepsilon^2$, because $T, T' \notin C \supseteq P$. This contradicts the end of the merge phase. So $S = C$. $\square$

**Corollary 7.** Among the conforming meshes whose leaves all have $p \le \varepsilon^2$, the mesh of Theorem 6 has the fewest triangles, and it is the only one with that number.

*Proof.* Such a mesh has a split set that holds $P$ (the argument of the split phase) and is closed under parents and partners (Lemma 5), so it holds $C$. A mesh with the split set $S$ has $2 + |S|$ leaves, because each split adds one leaf. So it has at least $2 + |C|$ leaves, with equality only when its split set is $C$. $\square$

This is the optimality statement of Section 5.1 of the paper in a precise form, and it needs the monotone priority of Lemma 2: with a priority that can grow from a parent to a child, the split phase can keep a leaf with a priority of at most $\varepsilon^2$ that hides a descendant above $\varepsilon^2$, and the result is then not accurate. The test checks Theorem 6 against `target` and Corollary 7 by enumeration of all 5489 conforming meshes of the $4 \times 4$ grid.
