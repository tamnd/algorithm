---
title: Nested dissection returns a permutation, and ordering a separator after the parts it separates creates no fill between those parts
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be the graph of a symmetric pattern with $|V| = n$. Line numbers refer to the pseudocode of the page. For an ordering, $f(v)$ is the position of $v$, and $L$ is the symbolic Cholesky factor: $l_{ij} \ne 0$ for $i > j$ exactly when the elimination graph model of the [fill-in](/fill-in/) page puts an edge between the vertices numbered $i$ and $j$ when $j$ is eliminated.

**Lemma 1 (the level separator).** Let $W$ induce a connected subgraph with a level structure $L_0, \ldots, L_h$ from a root, $h \ge 2$, and let $1 \le \mu \le h - 1$. Let $S$ be the set of vertices of $L_\mu$ with a neighbour in $L_{\mu+1}$. Then $S \ne \emptyset$, and $W \setminus S$ has no edge between $X = L_0 \cup \cdots \cup L_{\mu-1} \cup (L_\mu \setminus S)$ and $Y = L_{\mu+1} \cup \cdots \cup L_h$, both of which are nonempty.

*Proof.* Every vertex of $L_{\mu+1}$ has a neighbour in $L_\mu$ (its predecessor in the search), so $S \ne \emptyset$. Edges of a level structure join the same or adjacent levels. An edge from $Y$ to $X$ would join $L_{\mu+1}$ to $L_\mu \setminus S$, which contradicts the definition of $S$. $L_0 \subseteq X$ and $L_h \subseteq Y$. $\square$

The implementation picks $\mu$ at the level where the cumulative count first reaches $|W|/2$, clamped to $[1, h - 1]$. When $h < 2$ it orders the part by minimum degree instead.

**Termination and permutation.** Every task on the stack holds a vertex set, and the sets of the tasks on the stack together with the vertices already in the order always partition $V$. This holds initially with the single task $V$. Each step replaces a split task by one of three things:
- its components (line L5);
- its vertices appended to the order (line L6);
- an emit task for $S$ and split tasks for the components of $W \setminus S$ (lines L7 to L9).

An emit task appends its set. So each vertex is appended exactly once, and when the stack is empty, the order is a permutation. A split task on a disconnected set produces strictly smaller tasks. A split task on a connected set either ends at line L6 or, by Lemma 1, produces a nonempty $S$ and strictly smaller parts. So the multiset of task sizes decreases in the well-founded multiset order, and the loop ends. At most $2n$ split and emit tasks are created.

**Lemma 2 (dissection order).** When a split task for a set $W$ is processed with separator $S$ and parts $C_1, \ldots, C_t$, all vertices of $C_1, \ldots, C_t$ are appended before any vertex of $S$. Every neighbour of $W$ outside $W$ is appended after all of $W$.

*Proof.* The stack is last in, first out. The emit task for $S$ is pushed below the split tasks of the parts, so it is popped only after those tasks and everything they push have been processed. For the second claim, induct on the dissection tree. A neighbour of $W$ outside $W$ lies in no sibling part, because parts are components after removing the separators. So it lies in the separator of some ancestor task, which by the first claim is appended after all of that ancestor's parts, and $W$ is inside one of them. Component splits at line L5 have no edges between them. $\square$

**Theorem 1 (no fill between parts).** In the order produced, $l_{ij} = 0$ whenever the vertices numbered $i$ and $j$ lie in different parts $C_a \ne C_b$ of the same split.

*Proof.* By the path theorem of Rose, Tarjan and Lueker (1976), $l_{ij} \ne 0$ for $i > j$ if and only if $G$ has a path between the two vertices whose interior vertices are all numbered below $j$. Take $x \in C_a$ and $y \in C_b$, and any path between them in $G$. It cannot stay inside $C_a \cup C_b$, since these are different components of $G[W \setminus S]$. So it contains a vertex of $S$ or a vertex outside $W$. By Lemma 2 such a vertex is numbered after both $x$ and $y$. Hence no path qualifies, and $l_{ij} = 0$. $\square$

So $L$ restricted to a split has the block form
$$P A P^T = \begin{pmatrix} A_{11} & 0 & A_{1S} \\ 0 & A_{22} & A_{2S} \\ A_{S1} & A_{S2} & A_{SS} \end{pmatrix}, \qquad L = \begin{pmatrix} L_{11} & 0 & 0 \\ 0 & L_{22} & 0 \\ L_{S1} & L_{S2} & L_{SS} \end{pmatrix},$$
where the zero blocks stay zero. The two parts are factored independently, and only the separator block, a dense [Schur complement](/schur-complement/) in general, couples them. The tests check Theorem 1 on random geometric graphs.

**Theorem 2 (fill and work on the grid; cited).** For the $k \times k$ five-point grid, $n = k^2$, the cross-shaped nested dissection of George (1973) gives $|L| = \tfrac{31}{4} k^2 \log_2 k + O(k^2)$ and about $\tfrac{829}{84} k^3$ multiplications, and every ordering has $|L| = \Omega(k^2 \log k)$ and $\Omega(k^3)$ work (Hoffman, Martin and Rose, 1973). We do not reproduce these counts.

The recurrence behind the upper bounds is elementary. If $F(k)$ is the work of a square of side $k$ whose boundary is already numbered later, then $F(k) = 4F(k/2) + O(k^3)$. The $O(k^3)$ term is the dense factorization of a separator block of order $O(k)$. Hence $F(k) = O(k^3)$. The same count for storage gives $|L|(k) = 4|L|(k/2) + O(k^2)$, hence $O(k^2 \log k)$. The tests check both orders of growth with explicit constants for $k \le 32$.

**Floating point.** Theorem 1 is structural and holds for computed factors too, because exact zeros are never updated. Cholesky of $P A P^T$, when it runs to completion, satisfies $P A P^T + \Delta A = \hat L \hat L^T$ with $|\Delta A| \le \gamma_{n+1}|\hat L||\hat L^T|$ (Higham, Theorem 10.3) for every ordering. The tests verify this elementwise with exact rational residuals on grid matrices in nested dissection order.
