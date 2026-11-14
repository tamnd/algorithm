---
title: The core step lists, for each of the six axis directions, exactly the subsets of a subassembly that can leave the rest by one translation
proves: [correctness, termination]
status: full
---

This proof covers the one step of the motion space approach that the page implements: lines L1 to L9, for the motion space of the six axis translations to infinity. The parts are closed axis-aligned boxes with disjoint interiors. A box $a$ has corners $(a_1, a_2, a_3)$ and $(a'_1, a'_2, a'_3)$. A subassembly is a set $A$ of parts. A nonempty proper subset $S \subset A$ *can leave along $d$* when, for every $t > 0$, no part of $S$ moved by $t d$ meets the interior of a part of $A \setminus S$. The hand model is two-handed: $S$ moves as one rigid body and $A \setminus S$ stays.

The graph $G_d$ of lines L2 and L3 has the parts of $A$ as nodes and an arc $i \to j$ when $\mathrm{blocks}(b_i, b_j, d)$. For $d = +e_k$ the predicate is: on both axes $m \ne k$ the open intervals of $b_i$ and $b_j$ overlap, and $b_{j,k} \ge b'_{i,k}$. For $d = -e_k$ the last condition is $b'_{j,k} \le b_{i,k}$.

**Lemma 1 (the pair test).** For two boxes $a$, $b$ with disjoint interiors and $d \in \{\pm e_1, \pm e_2, \pm e_3\}$, there is a $t > 0$ for which $a + t d$ meets the interior of $b$ if and only if $\mathrm{blocks}(a, b, d)$.

*Proof.* Take $d = +e_k$. The motion does not change the intervals on the axes $m \ne k$, so these must overlap, as the predicate asks. On axis $k$, the interval $(a_k + t, a'_k + t)$ meets $(b_k, b'_k)$ when $b_k - a'_k < t < b'_k - a_k$. Some $t > 0$ satisfies this exactly when $b'_k > a_k$, because $b'_k - a_k > b_k - a'_k$ always holds. The intervals on the other two axes overlap and the interiors are disjoint, so the intervals on axis $k$ do not overlap: either $b_k \ge a'_k$ or $b'_k \le a_k$. Of these, $b'_k > a_k$ holds exactly in the first case, which is the predicate. The case $d = -e_k$ is the mirror image. $\square$

**Lemma 2 (a set leaves when no arc leaves it).** $S$ can leave along $d$ if and only if $G_d$ has no arc from a part of $S$ to a part of $A \setminus S$.

*Proof.* The parts of $S$ keep their relative positions and the parts of $A \setminus S$ do not move, so a collision at some $t$ is a pair $i \in S$, $j \in A \setminus S$ with $b_i + t d$ meeting the interior of $b_j$. By Lemma 1 such a $t$ exists for the pair exactly when $i \to j$ is an arc. $\square$

Call a set *closed* when no arc of $G_d$ leaves it. A closed set is a union of strongly connected components: if $i \in S$ and $j$ is in the component of $i$, a path goes from $i$ to $j$, and none of its arcs leaves $S$.

**Lemma 3 (the order of the components).** Let $C_0, \ldots, C_{k-1}$ be the components in the order that Tarjan's algorithm completes them on line L4. If an arc goes from $C_t$ to $C_u$ with $u \ne t$, then $u < t$.

*Proof.* Tarjan's algorithm completes a component only after every other component that it can reach, which is the standard reverse topological order of the condensation. $\square$

**Lemma 4 (the enumeration).** The calls of lines L6 to L9 output every closed set other than $\emptyset$ and $A$ exactly once, and nothing else.

*Proof.* Line L5 sets $succ[t]$ to the parts of $A$ outside $C_t$ that an arc from $C_t$ reaches. By Lemma 3, $succ[t] \subseteq C_0 \cup \cdots \cup C_{t-1}$. A call $\mathrm{EXTEND}(t, chosen)$ has decided, for each $u < t$, whether $C_u \subseteq chosen$, and $chosen$ is the union of the chosen components. Line L8 leaves $C_t$ out, and line L9 puts it in when $succ[t] \subseteq chosen$.

*Only closed sets.* By induction on $t$, $chosen$ is closed at each call: a component put in at line L9 has all its targets in $chosen$ already, and the targets of earlier components do not change.

*All closed sets.* Let $S$ be closed. Then $S$ is a union of components, and for each $C_t \subseteq S$, $succ[t] \subseteq S \cap (C_0 \cup \cdots \cup C_{t-1})$. So the path of calls that puts in exactly the components of $S$ passes the test of line L9 at each step, and it reaches $t = k$ with $chosen = S$.

*Once.* Two different paths differ in the first component on which they decide differently. The components are disjoint and nonempty, so the two outputs differ.

Line L7 drops $\emptyset$ and $A$. $\square$

**Theorem 1 (the core step).** For each $d \in M$, removable_sets$(A)[d]$ is the list of the nonempty proper subsets of $A$ that can leave the rest of $A$ along $d$, each once.

*Proof.* Line L1 visits each direction. Lines L2 and L3 build $G_d$ on $A$, and by Lemma 2 the sets that can leave are the closed sets other than $\emptyset$ and $A$. Lemma 4 lists them. $\square$

**Corollary 1 (separations).** A split $\{S, A \setminus S\}$ of $A$ can be done by one axis translation of one side, under the motions $M$, exactly when $S$ or $A \setminus S$ is in one of the lists. So the splits that an [AND/OR graph](/and-or-graph-of-assembly-plans/) needs for the node $A$ are read from the lists, without a test of each of the $2^{|A| - 1} - 1$ splits.

**Lemma 5 (no cycles along an axis).** For boxes, $G_d$ has no cycle for each axis direction $d$. So every component is one part, and when $|A| \ge 2$, one part of $A$ can always leave along $d$.

*Proof.* An arc $i \to j$ along $+e_k$ needs $b_{j,k} \ge b'_{i,k} > b_{i,k}$, so the lower coordinate on axis $k$ grows strictly along a path. A graph with no cycle has a node with no arc out, and that node is a closed set. $\square$

So for the axis motion space and boxes, line L4 only orders the parts. The step is written with components because the same lines apply to every cell of a motion space, and in other motion spaces, such as oblique translations or small motions, the graph of a cell can have cycles.

**Termination and cost.** Let $k = |A|$ and let $R_d$ be the number of sets output for $d$. Lines L2 and L3 cost $O(k^2)$, and Tarjan's algorithm and line L5 cost $O(k^2)$. In the recursion of lines L6 to L9, each call has a child at line L8, so every path of calls goes down to a leaf at depth $k$. There are $R_d + 2$ leaves at most, so there are at most $k (R_d + 2) + 1$ calls. The step stops, and costs $O(k^2 + k R_d)$ for each direction.
