---
title: The block-cut tree is a forest, and its queries are correct
proves: [correctness]
status: full
---

Let $G = (V, E)$ be an undirected graph. Parallel edges are allowed; loops are ignored, since they lie in no block with another edge and change no articulation point. Line L1 gives the vertex sets $B_1, \ldots, B_b$ of the blocks of the non-loop edges (correct by the proof on the [Hopcroft-Tarjan](/hopcroft-tarjan-biconnectivity/) page), plus a block $\{v\}$ for each vertex with no non-loop edge, and the set $A$ of articulation points. We use these facts from the [biconnected components](/biconnected-components/) page: two blocks share at most one vertex; a vertex lies in two or more blocks if and only if it is in $A$; and two edges at a vertex $x$ that lie in different blocks are not joined by a path that avoids $x$ (fact 3). We also use that $B_i \setminus \{x\}$ is connected in $G - x$ for every block $B_i$ and every vertex $x$: a block with two vertices becomes one vertex, and a block with three or more vertices is [biconnected](/biconnected-graph/).

Let $\mathcal{T}$ be the graph built by lines L2 and L3: a node $\beta_i$ for each block, a node $\gamma_x$ for each $x \in A$, and an edge $\{\beta_i, \gamma_x\}$ whenever $x \in B_i$.

**Lemma 1.** $\mathcal{T}$ is a forest, and its trees match the components of $G$.

*Proof.* Each node of $\mathcal{T}$ lies in one component of $G$, and two nodes are adjacent only if they share a vertex, so a tree of $\mathcal{T}$ stays in one component. Within a component, any two blocks are joined in $\mathcal{T}$: follow a path of $G$ from one to the other; each time it moves from one block to the next, it does so at a shared vertex, which is in $A$, so the two block nodes have a common neighbour.

We show that each edge $\{\beta, \gamma_x\}$ is a bridge of $\mathcal{T}$, so $\mathcal{T}$ has no cycle. Since $x \in A$, it lies in a second block $\beta' \neq \beta$. Suppose $\mathcal{T}$ minus the edge still has a path from $\beta$ to $\gamma_x$. Then it is $\beta = \beta_0, \gamma_{x_1}, \beta_1, \ldots, \gamma_{x_k}, \beta_k, \gamma_x$ with $\beta_k \neq \beta$ and all $x_j \neq x$. Each $\beta_j \setminus \{x\}$ is connected in $G - x$, and consecutive ones share $x_j \neq x$, so $G - x$ has a path from a neighbour $y$ of $x$ in $\beta$ to a neighbour $z$ of $x$ in $\beta_k$. The edges $xy$ and $xz$ lie in different blocks, and this path joins them without $x$, which contradicts fact 3. $\square$

Line L5 roots each tree of $\mathcal{T}$ at a block node, and one depth-first search of $\mathcal{T}$ gives each node $a$ an interval $[\mathrm{tin}[a], \mathrm{tout}[a]]$. The intervals of a node and of its descendants are nested, and those of two nodes that are not ancestor and descendant are disjoint. So line L6 is the ancestor test, and in line L7 the children of $a$ are sorted by $\mathrm{tin}$, so the last child whose $\mathrm{tin}$ is at most $\mathrm{tin}[c]$ is the one whose subtree holds $c$.

Line L4 sets $\mathrm{node}[v] = \gamma_v$ for $v \in A$, and otherwise the only block that holds $v$. Thus the blocks that hold $v$ are the tree neighbours of $\mathrm{node}[v]$ if $v \in A$, and $\{\mathrm{node}[v]\}$ if not.

**Lemma 2 (SEPARATES).** Let $u, v, x$ be distinct, with $u$ and $v$ in one component. Every $u$-$v$ path of $G$ passes through $x$ if and only if $x \in A$ and $\gamma_x$ lies on the tree path between $\mathrm{node}[u]$ and $\mathrm{node}[v]$.

*Proof.* Let $P$ be a $u$-$v$ path. Cut $P$ at each vertex where it passes from an edge of one block to an edge of another block. Each such vertex $y$ is in $A$, and the blocks of $P$ in order, with the nodes $\gamma_y$ between them, form a walk in $\mathcal{T}$ from a neighbour of (or the node) $\mathrm{node}[u]$ to the same for $\mathrm{node}[v]$. In a tree, every walk between two nodes visits each node of the path between them. So if $\gamma_x$ is on that path, $\gamma_x$ is on the walk, and $P$ passes through $x$.

Conversely, let $\gamma_x$ not be on the tree path $\mathrm{node}[u] = a_0, a_1, \ldots, a_k = \mathrm{node}[v]$. For each block $a_j$ on it, let $s_j$ and $t_j$ be the vertices where the path enters and leaves it: the vertex of the cut node before and after it, or $u$ at the start and $v$ at the end. None of these is $x$, since $\gamma_x$ is not on the path and $u, v \neq x$. Since $a_j \setminus \{x\}$ is connected in $G - x$, it has an $s_j$-$t_j$ path without $x$. Joining these paths gives a $u$-$v$ walk without $x$, so some $u$-$v$ path avoids $x$. If $x \notin A$, $G - x$ has as many components as $G$, and $u$, $v$ stay joined. $\square$

The tree path between $a$ and $b$ passes through $g$ if and only if $g$ is an ancestor of exactly one of them, or $g$ is an ancestor of both and they lie under different children of $g$ (or one of them is $g$; here $a, b \neq g$). Lines L9 to L12 compute this test, and line L8 handles $x \notin A$. So SEPARATES is correct.

**Lemma 3 (SAME-BLOCK).** For distinct $u$ and $v$, lines L13 to L16 return true if and only if some block holds both.

*Proof.* Let $N(u)$ be the set of blocks that hold $u$, as given above. A common block exists if and only if $N(u) \cap N(v) \neq \emptyset$. If neither vertex is in $A$, the sets are $\{a\}$ and $\{b\}$, so the test is $a = b$ (line L14). If only $u$ is in $A$, the block $b$ is in $N(u)$ if and only if $b$ is adjacent to $a = \gamma_u$, that is, $b$ is the parent or a child of $a$ (line L15). If both are in $A$, a common block $\beta$ is adjacent to both cut nodes. It cannot be a child of both. So it is the parent of both, or the parent of one and a child of the other, which makes the other the grandparent of the first (line L16). Cut nodes are never roots, so their parents exist. $\blacksquare$
