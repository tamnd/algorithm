---
title: A set of parts can make a small translation exactly when no arc of the blocking graph leaves it, and the first strongly connected component that Tarjan's algorithm completes is such a set
proves: [correctness, termination]
status: full
---

We use the pseudocode and the model of the page. The parts are closed axis-aligned boxes with pairwise disjoint interiors. A box $a$ has corners $(a_1, a_2, a_3)$ and $(a'_1, a'_2, a'_3)$ with $a_k < a'_k$. A direction is a nonzero vector $d \in \mathbb{R}^3$, and its cell is its sign vector $s = \mathrm{sign}(d) \in \{-1, 0, 1\}^3 \setminus \{0\}$. A set $S$ of parts *can move along $d$* when there is $\varepsilon_0 > 0$ such that, for every $\varepsilon \in (0, \varepsilon_0]$, the boxes of $S$ moved by $\varepsilon d$ meet the interior of no part outside $S$. This is the infinitesimal translation model. The hand model is two-handed: one hand moves $S$ as one rigid body and the other holds the rest.

The predicate of line L3, $\mathrm{BLOCKED}(a, b, s)$, is true when, for each axis $k$, one of three conditions holds: $a_k < b'_k$ and $b_k < a'_k$; or $a'_k = b_k$ and $s_k > 0$; or $a_k = b'_k$ and $s_k < 0$. The graph $\mathrm{DBG}(s)$ has an arc $i \to j$ when $\mathrm{BLOCKED}(b_i, b_j, s)$.

**Lemma 1 (the axis test).** Let $a$ and $b$ be two boxes with disjoint interiors and let $d$ be a direction with cell $s$. Then $a + \varepsilon d$ meets the interior of $b$ for every small enough $\varepsilon > 0$ if $\mathrm{BLOCKED}(a, b, s)$, and for no small enough $\varepsilon > 0$ otherwise.

*Proof.* Two open boxes meet exactly when their open intervals meet on each of the three axes. On axis $k$, the moved interval is $(a_k + \varepsilon d_k, a'_k + \varepsilon d_k)$, and it meets $(b_k, b'_k)$ exactly when $a_k + \varepsilon d_k < b'_k$ and $b_k < a'_k + \varepsilon d_k$. Look at the cases.

- If $a_k < b'_k$ and $b_k < a'_k$, both strict inequalities stay true for small $\varepsilon$.
- If $a'_k = b_k$, the second inequality reads $0 < \varepsilon d_k$, which holds exactly when $s_k > 0$. The first holds, because $a_k < a'_k = b_k < b'_k$.
- If $a_k = b'_k$, the first inequality reads $\varepsilon d_k < 0$, which holds exactly when $s_k < 0$, and the second holds for the same reason.
- Otherwise $a'_k < b_k$ or $b'_k < a_k$, and a gap of positive length stays open for small $\varepsilon$.

In each case the answer is the same for all small $\varepsilon$, and it is the condition of BLOCKED on axis $k$. Take the smallest of the three thresholds. $\square$

**Corollary 1 (cells).** $\mathrm{DBG}(d)$ depends only on the cell of $d$. So the 26 graphs of line L1 are all the directional blocking graphs of the product.

**Lemma 2 (a set moves when no arc leaves it).** A set $S$ can move along $d$ if and only if $\mathrm{DBG}(s)$ has no arc from a part of $S$ to a part outside $S$.

*Proof.* The parts of $S$ move together, so two parts of $S$ never collide, and the parts outside $S$ do not move, so they never collide with each other. A collision is a pair $i \in S$, $j \notin S$ with $b_i + \varepsilon d$ meeting the interior of $b_j$. By Lemma 1, for each such pair there is a threshold below which this happens for all $\varepsilon$ when $i \to j$ is an arc, and for no $\varepsilon$ when it is not. There are finitely many pairs, so below the smallest threshold, $S$ collides exactly when an arc leaves $S$. $\square$

So line L5 is correct. A set with no arc out is a union of strongly connected components: if $i \in S$ and $j$ is in the component of $i$, there is a path from $i$ to $j$, and no arc of it can leave $S$.

**Lemma 3 (the first component is a sink).** In Tarjan's algorithm on a graph $G$, a component is completed only after every other component that it can reach. So the first completed component $C$ has no arc to a part outside $C$.

*Proof.* This is the standard property of Tarjan's algorithm: the components come out in reverse topological order of the condensation of $G$. If $C$ had an arc to a part $w$ of another component $C'$, then $C'$ is reachable from $C$ and would be completed before $C$, which contradicts that $C$ is first. $\square$

**Theorem 1 (the SCC test).** Let $A$ be a set of at least one part. REMOVABLE$(s, A)$ returns a nonempty proper subset of $A$ that can move along any $d$ of cell $s$, with the other parts of $A$ fixed, if one exists, and returns none otherwise.

*Proof.* Lines L6 and L7 run on the graph induced on $A$, which is $\mathrm{DBG}(s)$ of the subassembly $A$, because blocking is a relation between two parts. If line L9 returns $C$, then $C$ is a component, so it is nonempty, it is not $A$ by line L8, and no arc leaves it by Lemma 3. By Lemma 2 it can move. If line L8 returns none, then $A$ is one strongly connected component. Take any nonempty proper $S \subset A$ and parts $i \in S$, $j \in A \setminus S$. There is a path from $i$ to $j$ in the induced graph, and one of its arcs leaves $S$, so $S$ cannot move by Lemma 2. $\square$

**Theorem 2 (one translation in any direction).** SEPARATE$(A)$ returns a cell and a set that can move along it if some nonempty proper subset of $A$ can move along some direction, and none if $A$ is locked for every small translation.

*Proof.* Every direction lies in exactly one of the 26 cells, and by Corollary 1 the cell decides the graph. Line L10 tries every cell, and Theorem 1 answers each one. $\square$

**Lemma 4 (reverse cells).** $\mathrm{DBG}(-s)$ is $\mathrm{DBG}(s)$ with every arc reversed.

*Proof.* $a + \varepsilon d$ meets the interior of $b$ exactly when $b - \varepsilon d$ meets the interior of $a$, because both say that the open boxes overlap after a relative motion of $\varepsilon d$. Apply Lemma 1 on both sides. $\square$

**Lemma 5 (axis cells have no cycle).** For $s = \pm e_k$, $\mathrm{DBG}(s)$ has no cycle. So some single part of any product can move along each of the six axis directions.

*Proof.* Take $s = +e_1$. An arc $i \to j$ needs open overlap on axes 2 and 3, where $s$ is 0. The interiors are disjoint, so the intervals on axis 1 do not overlap, and the arc needs $b'_{i,1} = b_{j,1}$. Then $b_{j,1} > b_{i,1}$, and the lower $x$ coordinate grows strictly along each path. The other axis cells are the same. A graph with no cycle has only single parts as components, and the first one is a sink. $\square$

The off-axis cells can have cycles. Three boxes in a $2 \times 2 \times 2$ cube give a cycle of length 3 in the cell $(+, -, +)$, as the example of the page shows.

**Termination and cost.** Line L1 runs 26 times, and lines L2 to L4 test each ordered pair once, in $O(1)$ time, so BUILD costs $O(n^2)$. Tarjan's algorithm visits each part and each arc once, so line L6 costs $O(n + e)$ with $e \le n(n-1)$ arcs, and SEPARATE costs $O(n^2)$ for one subassembly.

**Scope.** The proofs are about small motions. A set that can make a small move may still collide later on its way out: in the frame of the page, the block can move up a little, but the top plate stops it before it leaves. The test for one translation to infinity uses other blocking graphs, and the same SCC argument holds for them, because Lemma 2 and Theorem 1 use only that a collision of a rigid set is a collision of one pair.
