---
title: Baker's scheme gives (1 - 1/k) OPT for independent set and (1 + 1/k) OPT for vertex cover
proves: [correctness, time.worst]
status: full
---

**Statement.** Let $G = (V, E)$ be a graph with $n$ vertices and $k \ge 1$ an integer. (a) The dynamic program MIS-DP returns a maximum independent set of the subgraph induced by its input set $U$, in time $O(|U|\, 2^{w} w^2)$, where $w = \max_v |S_v|$ is the width of the elimination order. (b) BAKER-IS returns an independent set of $G$ of size at least $(1 - 1/k)\,\mathrm{OPT}$. (c) The vertex cover version returns a vertex cover of size at most $(1 + 1/k)\,\mathrm{OPT}$. (d) If $G$ is planar and the bands are solved with tree decompositions of width $O(k)$, the total time is $2^{O(k)} n$.

The treewidth bound used in (d) is cited, not proved here: a $k$-outerplanar graph has treewidth at most $3k - 1$ (Bodlaender 1998), and a band of $k$ breadth-first levels of a planar graph has treewidth $O(k)$, because contracting the levels below it to one vertex gives a planar graph of radius at most $k$, and a planar graph of radius $r$ has treewidth at most $3r + 1$ (Robertson and Seymour).

**Setup.** Fix $U \subseteq V$ and let $H = G[U]$. The elimination order $v_1, \ldots, v_m$ of line L5 removes the vertices of $H$ one at a time; when $v$ is removed, $S_v$ is the set of its current neighbours, and these are made pairwise adjacent (*fill edges*) before the next step. Every vertex of $S_v$ is removed after $v$. If $S_v \ne \emptyset$, the *parent* $p(v)$ is the vertex of $S_v$ removed first. This gives a forest $F$; $D_v$ is the set of $v$ and its descendants in $F$.

**Lemma 1 (parents).** If $S_v \ne \emptyset$ and $p = p(v)$, then $S_v \setminus \{p\} \subseteq S_p$.

*Proof.* When $v$ is removed, $S_v$ becomes a clique. So each $u \in S_v \setminus \{p\}$ is a neighbour of $p$ from then on, until $p$ or $u$ is removed. The vertex $p$ is removed first among $S_v$, so $u$ is still present at that time and $u \in S_p$. $\square$

**Lemma 2 (later neighbours are ancestors).** If $u \in S_v$, then $u$ is a proper ancestor of $v$ in $F$.

*Proof.* By induction on the number of vertices removed between $v$ and $u$. Let $p = p(v)$. If $u = p$ we are done. Otherwise $u \in S_p$ by Lemma 1, $p$ is removed after $v$ and before $u$, and by induction $u$ is an ancestor of $p$, so of $v$. $\square$

**Lemma 3 (separation).** (i) Every edge of $H$ with one end in $D_v$ and the other end outside $D_v$ has its outside end in $S_v$. (ii) For two children $c \ne c'$ of $v$, no edge of $H$ joins $D_c$ and $D_{c'}$. (iii) For each child $c$ of $v$, $S_c \subseteq \{v\} \cup S_v$.

*Proof.* Each edge $xy$ of $H$, with $x$ removed first, has $y \in S_x$, so $y$ is an ancestor of $x$ by Lemma 2. (ii) Vertices of $D_c$ and $D_{c'}$ are not ancestors of each other, so no edge joins them. (iii) Is Lemma 1 with $p(c) = v$. (i) Let $x \in D_v$ and $y \notin D_v$ be adjacent. If $y$ were removed first, $x$ would be an ancestor of $y$, and $y$ would be in $D_v$. So $x$ is removed first, and $y \in S_x$. We show by induction along the path from $v$ down to $x$ that $S_x \subseteq D_v \cup S_v$. For $x = v$ it is trivial. For $x \ne v$ with parent $q \in D_v$, Lemma 1 gives $S_x \subseteq \{q\} \cup S_q \subseteq D_v \cup S_v$. As $y \notin D_v$, $y \in S_v$. $\square$

**Proof of (a).** For $v \in U$ and an independent set $T \subseteq S_v$, let $f_v(T)$ be the largest size of a set $I \subseteq D_v$ such that $I \cup T$ is independent in $H$. We show that line L6 computes $\mathit{table}[v][T] = f_v(T)$, by induction along the order (children are removed before their parents). Take an optimal $I$ for $(v, T)$, and let $x = 1$ if $v \in I$. If $x = 1$, then $v$ has no neighbour in $T$, so this option is tried. For each child $c$, the set $I \cap D_c$ is independent together with $T_c = (T \cup \{v\}^{x}) \cap S_c$, so $|I \cap D_c| \le f_c(T_c)$, and $|I| \le x + \sum_c f_c(T_c)$. Conversely, pick for each child an optimal set $I_c$ for $(c, T_c)$, and add $v$ if $x = 1$. Edges from $D_c$ leave only to $S_c \subseteq \{v\} \cup S_v$ (Lemma 3), where the chosen vertices are exactly $T_c$; there are no edges between different $D_c$; and $v$ has no neighbour in $T$ when $x = 1$. So the union is a valid set for $(v, T)$ and its size is $x + \sum_c f_c(T_c)$. The maximum over $x$ is therefore $f_v(T)$.

The roots of $F$ are the vertices with $S_v = \emptyset$, and their sets $D_v$ partition $U$ with no edges between them (Lemma 3 (i) with $S_v = \emptyset$). Line L7 walks the order backwards. When it reaches $v$, all of $S_v$ is decided, and it applies the choice stored for $(v, T)$ with $T$ the chosen part of $S_v$. By the recurrence, the vertices chosen in $D_v$ then form an optimal set for $(v, T)$, so each root contributes $f_v(\emptyset)$ and the union is a maximum independent set of $H$.

*Time.* Each $v$ has at most $2^{|S_v|}$ sets $T$. For each, the independence test costs $O(w^2)$ and the recurrence $O(|\text{children}(v)| \cdot w)$. Each vertex is a child at most once, so the total is $O(m\, 2^{w} w^2)$. The order itself costs $O(m^2 w)$ in the simple form of the code, or less with buckets. $\square$

**Proof of (b).** *Edges are local.* Breadth-first search reaches vertices in order of level, and when $u$ is processed every unvisited neighbour gets level $\ell(u) + 1$. So each edge $uv$ has $|\ell(u) - \ell(v)| \le 1$.

Fix $r$. Line L4 groups the kept vertices by $\lfloor (\ell(v) - r)/k \rfloor$. Two kept vertices in different groups have a level $\ell \equiv r$ strictly between their levels, so their levels differ by at least 2 and they are not adjacent. By (a) each band gets an independent set, so their union $S_r$ is independent in $G$.

Let $I^*$ be a maximum independent set of $G$ and $I^*_r = \{v \in I^* : \ell(v) \equiv r \pmod k\}$. The $k$ sets $I^*_r$ partition $I^*$, so some $r$ has $|I^*_r| \le \mathrm{OPT}/k$. The set $I^* \setminus I^*_r$ uses only kept vertices, and its part in each band is independent, so by (a) the band optimum is at least as large. Summing over bands, $|S_r| \ge \mathrm{OPT} - |I^*_r| \ge (1 - 1/k)\,\mathrm{OPT}$, and line L9 keeps a set at least this large. $\square$

**Proof of (c).** Fix $r$ and let $P_j$ be the set of vertices with level in $\{r + jk, \ldots, r + (j+1)k\}$, for all integers $j$ with $P_j \ne \emptyset$. An edge $uv$ has levels $\ell$ and $\ell$ or $\ell + 1$, and both lie in the piece $j = \lfloor (\ell - r)/k \rfloor$, since $r + jk \le \ell < r + (j+1)k$. For a piece $P$, the set $P \setminus I_P$, with $I_P$ a maximum independent set of $G[P]$ from (a), is a minimum vertex cover of $G[P]$. So the union $C_r$ covers every edge of $G$.

Let $C^*$ be a minimum vertex cover of $G$. Its restriction to a piece $P_j$ covers $G[P_j]$, so $|P_j \setminus I_{P_j}| \le |C^* \cap P_j|$. A vertex lies in two pieces if its level is $\equiv r \pmod k$, and in one piece otherwise. So
$$|C_r| \le \sum_j |C^* \cap P_j| = \mathrm{OPT} + |C^*_r|, \qquad C^*_r = \{v \in C^* : \ell(v) \equiv r \pmod k\}.$$
Some $r$ has $|C^*_r| \le \mathrm{OPT}/k$, and the best $r$ gives at most $(1 + 1/k)\,\mathrm{OPT}$. $\square$

**Proof of (d).** Breadth-first search costs $O(n)$ for a planar graph, which has $O(n)$ edges. There are $k$ offsets, and for each one the bands are disjoint (for (b)) or cover each vertex at most twice (for (c)). A band of at most $k + 1$ levels of a planar graph has treewidth $O(k)$ by the cited bounds, and for each fixed width a tree decomposition of that width can be found in linear time (Bodlaender 1996). A tree decomposition of width $w$ gives an elimination order with $|S_v| \le w$ for all $v$: repeatedly remove a vertex that occurs only in a leaf bag. The dynamic program of (a), run on such an order with $w = O(k)$, costs $O(|U|\, 2^{w} w^2)$ per band. Summed over bands and offsets, the time is $k \cdot 2^{O(k)} n = 2^{O(k)} n$. $\blacksquare$
