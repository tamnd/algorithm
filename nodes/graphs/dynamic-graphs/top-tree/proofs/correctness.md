---
title: Expose builds a top tree whose root holds the path from u to v
proves: [correctness]
status: full
---

Let $T$ be the tree of $u$ and $v$ (if $u$ and $v$ are in different trees, expose returns nil, which is correct). Let $X = \{u, v\}$ be the exposed set. For a cluster $C$, let $E(C)$ be its set of edges and $V(C)$ the ends of those edges. During the loop, call a cluster **top** if it has no parent yet. Write $\pi(a, b)$ for the tree path from $a$ to $b$.

We assume the user's functions satisfy the following: the information of a base cluster describes its edge; compress$(A, B)$ describes the concatenation of the cluster paths of $A$ and $B$ and the union of their edges; rake$(A, B)$ describes the cluster path of $B$ and the union of the edges. For path sum, path max and total weight, these are the functions of the implementation. So it suffices to show that the clusters have the claimed boundaries and cluster paths.

**Lemma 1 (no conflicts).** In one round, no two adjacent vertices are both removed, and no removed vertex receives a rake.

*Proof.* Exposed vertices are never removed. If a leaf $x$ rakes into $y$ and $y$ is also removed, $y$ is not exposed. A compressing vertex has no unexposed leaf neighbor, so $y$ is not compressed; so $y$ rakes and is a leaf whose only neighbor is $x$, and then only the smaller of the two rakes. Two adjacent vertices cannot both compress, since each needs heads for itself and tails for the other. The forced compress of line L4 happens only when no other vertex was chosen. $\square$

**Invariant (I).** After every round, with $L$ the live vertices:

1. the top clusters partition $E(T)$, and each is the edge set of a subtree of $T$;
2. for each live edge $\{a, b\}$ of the live tree there is a top path cluster $K_{ab}$ with boundary $\{a, b\}$, and its cluster path is $\pi(a, b)$;
3. every other top cluster is a point cluster at a live vertex $y$, the only vertex it shares with other top clusters; there is at most one per live vertex;
4. every vertex of $V(K) \setminus \mathrm{bound}(K)$ for a top cluster $K$ is removed and not exposed, and it touches only edges of $K$;
5. the live tree is a tree on $L$ that contains $X$.

*Proof.* At the start, the top clusters are the edges, $L = V(T)$, and the live tree is $T$. Assume (I) before a round; by Lemma 1, apply the removals one at a time.

*Rake of a leaf $x$ into $y$.* The live edge is $K_{xy}$, and $x$ may have a point cluster $P$. By item 4 and since $x$ is a leaf of the live tree, every edge at $x$ lies in $K_{xy}$ or $P$. If there is no $P$, then by item 2, $K_{xy}$ is a subtree whose only vertex touching outside edges is $y$ (the vertex $x$ is not exposed and has no edge outside), so it is a point cluster at $y$. If there is $P$, the rake of $P$ onto $K_{xy}$ is a subtree with the same property. The new point cluster at $y$ is then raked onto the point cluster already at $y$, if there is one; the result is a subtree, and its only vertex touching other top clusters is $y$, because both parts had $y$ as their only shared vertex. The live tree loses the leaf $x$.

*Compress of $x$ with live edges to $a$ and $b$.* By item 4, every edge at $x$ lies in $K_{ax}$, $K_{xb}$ or the point cluster $P$ at $x$. Raking $P$ onto $K_{ax}$ gives a cluster with boundary $\{a, x\}$ and the same path $\pi(a, x)$. Its edges and those of $K_{xb}$ share only the vertex $x$, which is not exposed and has no other edges, so the compress gives a subtree with boundary $\{a, b\}$; its cluster path is $\pi(a, x)$ followed by $\pi(x, b)$, and these two paths share only $x$, so in a tree their concatenation is $\pi(a, b)$. The live tree replaces the path $a, x, b$ by the edge $ab$.

In every case, the vertex removed is not exposed and becomes interior to a cluster that holds all its edges, which gives item 4; the clusters replaced are removed from the top level, which keeps item 1; item 5 holds because removing a leaf or contracting a vertex of degree two keeps a tree that still contains $X$. $\square$

**Termination.** If a live vertex outside $X$ exists, either some unexposed vertex is a leaf of the live tree, which rakes or whose leaf neighbor rakes, or every leaf is exposed. In the second case the live tree has at most two leaves, both in $X$, so it is the path from $u$ to $v$ and every unexposed live vertex has degree two with no unexposed leaf neighbor; line L4 compresses at least one of them. So every round removes a vertex, and the loop ends with $L = X$.

**Lemma 2 (binary).** Every cluster above the edges has exactly two children, and the root contains every edge of $T$ once.

*Proof.* Every merge in lines L5 to L7 is a rake or a compress of two clusters, and a leaf edge with no point cluster is reused, not merged. By item 1 the top clusters always partition $E(T)$, and line L7 merges all remaining top clusters into one. $\square$

**Theorem.** If $u \neq v$, the root returned by expose$(u, v)$ is a cluster with $E = E(T)$, boundary $\{u, v\}$ and cluster path $\pi(u, v)$. If $u = v$, the root has $E = E(T)$ and boundary $\{u\}$. In both cases the root information is that of the path from $u$ to $v$ and of the whole tree.

*Proof.* When the loop ends, $L = \{u, v\}$. If $u \neq v$, the live tree is the single edge $\{u, v\}$, so by item 2 the top path cluster $K_{uv}$ has path $\pi(u, v)$, and by item 3 the other top clusters are point clusters at $u$ or $v$. Line L7 rakes each of them onto the path cluster, which keeps the boundary $\{u, v\}$ (both vertices are exposed) and the path $\pi(u, v)$. If $u = v$, the live tree is the single vertex $u$, there is no path cluster, and line L7 joins the point cluster at $u$; if $T$ has no edges, the root is the empty cluster. By item 1 and Lemma 2 the root has all edges of $T$. The information follows from the assumption on the user's functions, by induction over the merges. $\blacksquare$
