---
title: The sweep finds every contact liaison, and GROW lists every connected subassembly once
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The parts are closed axis-aligned boxes $b_1, \ldots, b_n$ whose interiors are pairwise disjoint. For a box $b$ and an axis $k \in \{x, y, z\}$, write $[lo_k(b), hi_k(b)]$ for its interval on that axis. For two boxes $a$ and $b$, the overlap width on axis $k$ is $w_k = \min(hi_k(a), hi_k(b)) - \max(lo_k(a), lo_k(b))$.

**Lemma 1 (contact test).** Let $a$ and $b$ be closed boxes with disjoint interiors. The set $a \cap b$ has positive area in a plane exactly when there is one axis $k$ with $hi_k(a) = lo_k(b)$ or $hi_k(b) = lo_k(a)$, and $w_m > 0$ for the two other axes $m$. In that case $a \cap b$ lies in the plane normal to $e_k$, its area is the product of the two widths $w_m$, and the outward normal of $a$ on it is $+e_k$ in the first case and $-e_k$ in the second. CONTACT on line L4 returns exactly this.

*Proof.* The intersection of two boxes is the product of the three intervals of length $\max(w_k, 0)$. The interiors meet exactly when $w_k > 0$ on all three axes, so by the hypothesis some $w_k \le 0$. If some $w_k < 0$, the intersection is empty. If two widths are 0, the intersection lies in a line and has no area. So $a \cap b$ has positive area in a plane exactly when one width is 0 and the two others are positive. A width of 0 on axis $k$, with $lo_k < hi_k$ for both boxes, means that one interval ends where the other starts, which is $hi_k(a) = lo_k(b)$ or $hi_k(b) = lo_k(a)$, and only one of the two can hold. In the first case $b$ lies on the side of $a$ where the $k$ coordinate grows, so the outward normal of $a$ on the patch is $+e_k$. The patch is a rectangle with sides $w_m$ for the two other axes. $\square$

**Lemma 2 (the sweep sees every contact pair).** Lines L1 to L6 call CONTACT on every pair $\{i, j\}$ for which CONTACT can return a contact.

*Proof.* If $b_i$ and $b_j$ are in contact, their intersection is not empty, so their closed $x$ intervals meet: $lo_x(b_i) \le hi_x(b_j)$ and $lo_x(b_j) \le hi_x(b_i)$. Say that $j$ comes before $i$ in the order of line L1, so $lo_x(b_j) \le lo_x(b_i)$. Line L6 puts $j$ in the active list when $j$ is processed. Line L3 removes $j$ only at a step $i'$ with $hi_x(b_j) < lo_x(b_{i'})$. Every step $i'$ from $j$ up to and including $i$ has $lo_x(b_{i'}) \le lo_x(b_i) \le hi_x(b_j)$, because the order is sorted. So $j$ is still active at step $i$, and line L4 tests the pair. $\square$

**Theorem 1 (BUILD).** BUILD returns the graph whose edges are exactly the pairs of parts that share a face patch of positive area, each labelled with its axis, the sign of the normal from the smaller index to the larger, and the area.

*Proof.* Line L4 calls CONTACT only on pairs of distinct parts, each pair at most once, because $j$ is active only for the steps after its own. By Lemma 1, an edge is added only for a real contact, with the stated label. By Lemma 2, no contact is missed. $\square$

**Lemma 3 (IS-CONNECTED).** IS-CONNECTED($S$) returns true exactly when $S$ is not empty and the subgraph induced by $S$ is connected. It does at most $|S|$ rounds.

*Proof.* Let $v$ be the lowest part of $S$. After round $r$, the set $R$ is the set of parts of $S$ that a path inside $S$ of at most $r$ edges joins to $v$: this holds for $r = 0$, and line L11 adds exactly the parts of $S$ one edge away from $R$. The loop stops when a round adds nothing, so $R$ is then closed under steps inside $S$, and $R$ is the component of $v$ in the induced subgraph. The answer $R = S$ is true exactly when this component is all of $S$. Each round that goes on adds a part, so there are at most $|S|$ rounds. $\square$

**Lemma 4 (one call of GROW).** Let $S$ be connected, let $B$ be a set disjoint from $S$, and call a set $T$ *reachable* from $(S, B)$ when $T$ is connected, $S \subseteq T$ and $T \cap B = \emptyset$. The call GROW($S$, $B$) outputs every reachable set exactly once, and nothing else.

*Proof.* By induction on the number of parts outside $S \cup B$. Line L14 outputs $S$, which is reachable. Let $w_1, \ldots, w_k$ be the candidates of line L15, which are the parts outside $S$ and $B$ with a neighbour in $S$. The call for $w_i$ on line L17 has the first set $S + w_i$, which is connected because $w_i$ has a neighbour in $S$, and the banned set $B_i = B \cup \{w_1, \ldots, w_{i-1}\}$, which is disjoint from $S + w_i$. It has one more part in its first set, so by induction it outputs exactly the sets reachable from $(S + w_i, B_i)$, each once.

Take a reachable $T \ne S$. A path inside $T$ joins a part of $T \setminus S$ to $S$, so some part of $T \setminus S$ has a neighbour in $S$. That part is not in $B$, so it is a candidate. Let $w_i$ be the first candidate in $T$. Then $T$ is reachable from $(S + w_i, B_i)$, and from no $(S + w_{i'}, B_{i'})$ with $i' \ne i$: if $i' < i$ then $w_{i'} \notin T$, and if $i' > i$ then $w_i \in B_{i'} \cap T$. So $T$ is output exactly once, in the call for $w_i$. The set $S$ itself is output only on line L14, because every set that a child call outputs contains a candidate. Every output set is reachable from $(S, B)$, because a set reachable from $(S + w_i, B_i)$ is reachable from $(S, B)$. $\square$

**Theorem 2 (CONNECTED-SUBSETS).** Lines L18 to L20 output every connected nonempty set of parts exactly once.

*Proof.* The loop calls GROW($\{v\}$, $\{u : u < v\}$) for each part $v$. By Lemma 4 this outputs exactly the connected sets whose lowest part is $v$. Each connected nonempty set has one lowest part. $\square$

**Termination and cost.** The sweep makes $n$ steps over a list of at most $n$ parts. In GROW, every call outputs one set, and by Theorem 2 there are exactly $N$ calls in total, where $N$ is the number of connected sets. One call does $O(|S|)$ word operations on bit masks to form its candidates on line L15, plus constant work for each child call. So the enumeration costs $O(N n)$ word operations when $n$ is at most the word length.
