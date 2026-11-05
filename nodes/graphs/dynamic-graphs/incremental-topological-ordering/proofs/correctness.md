---
title: Local reordering keeps a valid topological order and detects every cycle
proves: [correctness]
status: full
---

The invariant is:

**(V)** The graph is acyclic, $\mathrm{pos}$ is a bijection from $V$ to $\{0, \ldots, n - 1\}$, and $\mathrm{pos}(x) < \mathrm{pos}(y)$ for every edge $(x, y)$.

It holds for the empty graph with any bijection. Assume (V) before ADD-EDGE$(u, v)$, and write $\mathrm{pos}$ for the order before the call and $\mathrm{pos}'$ for the order after it. The case $u = v$ is a loop, which is a cycle and is refused. Line L1 is correct: if $\mathrm{pos}(u) < \mathrm{pos}(v)$, the new edge goes forward, the order stays valid, and the graph stays acyclic, since a cycle through $(u, v)$ would need a path from $v$ to $u$, along which positions increase, so $\mathrm{pos}(v) < \mathrm{pos}(u)$.

From now on $\mathrm{pos}(v) < \mathrm{pos}(u)$. Write $W$ for the window of positions from $\mathrm{pos}(v)$ to $\mathrm{pos}(u)$.

**Lemma 1 (cycle test).** Line L3 returns "cycle" if and only if the graph has a path from $v$ to $u$, that is, if and only if the new edge closes a cycle.

*Proof.* If the search of line L2 finds an edge into $u$, it found a path from $v$ to $u$. Conversely, let $v = x_0, x_1, \ldots, x_k = u$ be a path. Positions increase along it, so $\mathrm{pos}(x_t) < \mathrm{pos}(u)$ for $t < k$. The search starts at $v$ and follows every edge out of a visited vertex to a vertex with position below $\mathrm{pos}(u)$, so by induction it visits $x_0, \ldots, x_{k-1}$, and at $x_{k-1}$ it examines the edge into $u$. $\square$

So if line L3 does not return, the new graph is acyclic. Let $F$ be the set found by line L2 and $B$ the set found by line L4. Then:

- (F1) $F$ is the set of vertices $y$ with a path from $v$ to $y$ all of whose vertices have positions below $\mathrm{pos}(u)$. In particular, if $f \in F$ and $(f, y)$ is an edge with $y \notin F$, then $\mathrm{pos}(y) \ge \mathrm{pos}(u)$, and $y \ne u$ by Lemma 1, so $\mathrm{pos}(y) > \mathrm{pos}(u)$.
- (B1) Symmetrically, if $b \in B$ and $(x, b)$ is an edge with $x \notin B$, then $\mathrm{pos}(x) < \mathrm{pos}(v)$.
- (D) $B \cap F = \emptyset$, and there is no edge from $F$ to $B$: a vertex in both, or such an edge, would give a path from $v$ to $u$, which Lemma 1 rules out.
- (W) All positions of $B \cup F$ lie in $W$: positions increase along paths from $v$, so $F$ has positions in $W$, and positions decrease backward from $u$, so $B$ has positions in $W$.

**Lemma 2 (monotone moves).** After line L6, $\mathrm{pos}'(b) \le \mathrm{pos}(b)$ for every $b \in B$ and $\mathrm{pos}'(f) \ge \mathrm{pos}(f)$ for every $f \in F$. All new positions of $B \cup F$ lie in $W$, every other vertex keeps its position, and $\mathrm{pos}'$ is a bijection.

*Proof.* Line L6 gives the positions $P$, which are exactly the old positions of $B \cup F$, back to the same vertices in a new arrangement, so $\mathrm{pos}'$ is a bijection, other vertices are untouched, and new positions lie in $W$ by (W). Let $f$ be the $k$-th smallest vertex of $F$ by old position, at old position $a$. It gets the $(|B| + k)$-th smallest element of $P$. Fewer than $k$ elements of $P$ that belong to $F$ are below $a$, and at most $|B|$ that belong to $B$, so $a$ is at most the $(|B| + k)$-th smallest element of $P$, and $\mathrm{pos}'(f) \ge a$. The claim for $B$ is symmetric: the $k$-th smallest vertex of $B$ gets the $k$-th smallest element of $P$, and its old position is at least that. $\square$

**Lemma 3.** After line L6, every edge $(x, y)$ of the new graph has $\mathrm{pos}'(x) < \mathrm{pos}'(y)$.

*Proof.* We go through the cases by the groups of $x$ and $y$. Let $O = V \setminus (B \cup F)$.

- $x, y \in O$: both positions are unchanged.
- $x, y \in F$, or $x, y \in B$: line L6 keeps the relative order inside each group.
- $x \in B$, $y \in F$: all of $B$ gets smaller positions than all of $F$. This includes the new edge, since $u \in B$ and $v \in F$.
- $x \in F$, $y \in B$: impossible by (D).
- $x \in F$, $y \in O$: by (F1), $\mathrm{pos}(y) > \mathrm{pos}(u)$, which is above every position of $W$, and $\mathrm{pos}'(x) \in W$.
- $x \in O$, $y \in B$: by (B1), $\mathrm{pos}(x) < \mathrm{pos}(v)$, below every position of $W$, and $\mathrm{pos}'(y) \in W$.
- $x \in O$, $y \in F$: $\mathrm{pos}'(x) = \mathrm{pos}(x) < \mathrm{pos}(y) \le \mathrm{pos}'(y)$ by Lemma 2.
- $x \in B$, $y \in O$: $\mathrm{pos}'(x) \le \mathrm{pos}(x) < \mathrm{pos}(y) = \mathrm{pos}'(y)$ by Lemma 2. $\square$

**Theorem.** After every call of ADD-EDGE, (V) holds; the call refuses the edge exactly when it would close a cycle; and ORDER returns a topological order of the current graph.

*Proof.* By induction on the calls. A refused edge leaves the graph and the order unchanged, and by Lemma 1 it is refused exactly when it closes a cycle. An accepted edge in line L1 keeps (V) as shown above. Otherwise, by Lemma 1 the new graph is acyclic, and by Lemmas 2 and 3 $\mathrm{pos}'$ is a bijection under which every edge goes forward. So (V) holds, and line L7 lists the vertices by $\mathrm{pos}$, which is a topological order. $\blacksquare$
