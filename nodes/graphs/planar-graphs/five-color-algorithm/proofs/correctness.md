---
title: The five-color algorithm returns a proper 5-coloring of every planar graph
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $G = (V, E)$ is a simple graph with $n$ vertices. A *coloring* is a partial map $c$ from $V$ to $\{0, \ldots, 4\}$; it is *proper* if no edge has two colored ends of the same color.

**Lemma 1 (peeling).** Lines L1 to L4 remove each vertex at most once. When a vertex $v$ is removed, it has at most 5 neighbours that are not yet removed. If $G$ is planar, every vertex is removed, so line L5 does not fail.

*Proof.* Let $deg[u]$ be the number of neighbours of $u$ that are not removed; line L4 keeps this true, since it decreases $deg[u]$ exactly when a neighbour of $u$ is removed. A vertex is pushed on $Q$ at line L1 if $deg \le 5$ at the start, or at line L4 when $deg$ drops from 6 to 5. Since $deg$ only decreases, and by exactly 1 at a time, each vertex is pushed at most once, so it is popped and removed at most once, and $deg[v] \le 5$ when $v$ is popped: a vertex in $Q$ has $deg \le 5$, and it stays so. So the loop of line L2 runs at most $n$ times.

Now let $G$ be planar, and suppose the loop ends with a nonempty set $R$ of vertices that are not removed. Then $Q$ is empty, so each $u \in R$ has $deg[u] \ge 6$ (a vertex with $deg[u] \le 5$ was pushed when its degree first became at most 5, at line L1 or line L4, and is therefore removed). So the induced subgraph $G[R]$ has minimum degree at least 6. But $G[R]$ is a simple planar graph, and if $|R| \ge 3$ it has at most $3|R| - 6$ edges by [Euler's formula](/euler-formula/), so its average degree is less than 6, a contradiction; if $|R| \le 2$ every degree is at most 1. $\square$

Let $S = s_1, \ldots, s_n$ be the removal order. By Lemma 1, each $s_k$ has at most 5 neighbours among $s_{k+1}, \ldots, s_n$.

**Lemma 2 (Kempe swap).** Let $c$ be a proper coloring, $i \ne j$ two colors, $x$ a vertex of color $i$, and $K$ the set of line L11. After swapping $i$ and $j$ on $K$, the coloring is proper and has the same colored vertices.

*Proof.* $K$ is the vertex set of the connected component of $x$ in the subgraph $H$ induced by the colored vertices of color $i$ or $j$; line L11 finds it by breadth-first search on $H$. Consider an edge $ab$ with both ends colored. If neither end is in $K$, nothing changes. If both are in $K$, both colors are swapped by the same bijection, so they stay different. If $a \in K$ and $b \notin K$, then $b$ is not in $H$, since $b$ is adjacent to $a \in K$ and $K$ is a component of $H$. So $c(b) \notin \{i, j\}$, while the new color of $a$ is in $\{i, j\}$. $\square$

**Lemma 3 (some pair works).** Let $G$ be planar, $c$ a proper coloring, and $v$ an uncolored vertex with exactly five colored neighbours of five different colors. Then for some pair of colors $i < j$, the vertex $y$ of color $j$ among them is not in the chain $K$ of the vertex $x$ of color $i$.

*Proof.* Fix a drawing of $G$ in the plane. Let $x_1, \ldots, x_5$ be the five colored neighbours of $v$ in the cyclic order of their edges around $v$, with colors $c_1, \ldots, c_5$. Suppose that the $\{c_1, c_3\}$-chain of $x_1$ contains $x_3$. Then there is a path $P$ from $x_1$ to $x_3$ whose vertices have colors $c_1$ or $c_3$. The path $P$ with the edges $v x_1$ and $v x_3$ is a cycle $C$ of $G$, drawn as a simple closed curve. By the [Jordan curve theorem](/jordan-curve-theorem/), the plane minus $C$ has two regions. Near $v$, a small disk around $v$ is cut by the two arcs of $vx_1$ and $vx_3$ into two sectors, one in each region; since the edges at $v$ come in the cyclic order $x_1, x_2, x_3, x_4, x_5$, the edge $v x_2$ starts in one sector and $v x_4$ in the other. These edges do not meet $C$ except at $v$, because $x_2, x_4 \notin C$ (their colors are $c_2, c_4 \notin \{c_1, c_3\}$, and they differ from $v$). So $x_2$ and $x_4$ lie in different regions of the plane minus $C$.

Now suppose also that the $\{c_2, c_4\}$-chain of $x_2$ contains $x_4$, by a path $P'$ whose vertices have colors $c_2$ or $c_4$. No vertex of $P'$ is on $C$: the vertices of $C$ are $v$, which is uncolored, and the vertices of $P$, of colors $c_1$ or $c_3$. Edges of a plane drawing meet only at common ends, so the drawing of $P'$ does not meet $C$. It is a connected set from $x_2$ to $x_4$ in the plane minus $C$, which contradicts the previous paragraph. So one of the two pairs $\{c_1, c_3\}$ or $\{c_2, c_4\}$ has the property of the lemma, for the vertex of the smaller color as $x$ (the chain of $x$ contains $y$ exactly when the chain of $y$ contains $x$, since both are the component of $H$ containing $x$). $\square$

**Theorem.** If $G$ is planar, FIVE-COLOR stops and returns a proper coloring of all vertices with colors $0$ to $4$.

*Proof.* By Lemma 1 line L5 does not fail, and $S$ holds every vertex once. We show by induction on the number of vertices processed by line L6 that before each iteration the coloring is proper and the colored vertices are exactly those after $v$ in $S$. At the start nothing is colored. At an iteration for $v = s_k$, the colored neighbours of $v$ are its neighbours among $s_{k+1}, \ldots, s_n$, at most 5 of them by Lemma 1. Line L7 records one neighbour for each color used.

If fewer than 5 colors are used, line L8 gives $v$ a color that no colored neighbour has, so the coloring stays proper.

Otherwise $v$ has exactly 5 colored neighbours, of 5 different colors, and $owner[k]$ is the unique neighbour of color $k$. The loop of line L9 tries the 10 pairs. By Lemma 3, some pair has $y \notin K$, so line L13 is not reached. At the first such pair, line L12 swaps $i$ and $j$ on $K$; by Lemma 2 the coloring stays proper. After the swap, $x \in K$ has color $j$. The other neighbours of $v$ keep their colors: $y \notin K$, and the other three have colors outside $\{i, j\}$, so they are not in $K$. So no colored neighbour of $v$ has color $i$, and $c(v) = i$ keeps the coloring proper.

Every loop is finite: lines L2 to L4 run at most $n$ times by Lemma 1, line L6 runs $n$ times, line L9 at most 10 times for each $v$, and the search of line L11 adds each vertex to $K$ at most once. After the last iteration all vertices are colored, and line L14 returns a proper 5-coloring. $\blacksquare$

**Non-planar inputs.** Lemmas 1 and 2 and the induction hold for every simple graph; only Lemma 3 uses planarity. So on any input the algorithm either fails at line L5 or line L13, or returns a proper 5-coloring.
