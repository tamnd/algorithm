---
tag: 7DQ56G
kind: data-structure
slug: incidence-matrix
name: Incidence matrix
aliases:
- vertex-edge incidence matrix
area: graphs/graph-representation
level: intro
summary: V×E matrix marking which vertices each edge touches.
implements: [graph]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n m)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [graph, edge, adjacency-matrix]
see_also: [adjacency-matrix, incidence-list, laplacian-matrix, line-graph, edge-list, compressed-sparse-column, hypergraph, matrix-tree-theorem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), Exercise 20.1-7, the signed incidence matrix of a directed graph and the product B B^T
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 1, Section 1.1, the incidence matrix and the adjacency matrix of a graph
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1, the adjacency matrix and the incidence matrix of a loopless graph
---

The incidence matrix of a [graph](/graph/) with $n$ vertices and $m$ edges is the $n \times m$ matrix $B$ with one row for each [vertex](/vertex/), one column for each [edge](/edge/), and a nonzero entry where the vertex is an end of the edge. For a [directed graph](/directed-graph/) the entries are signed, $-1$ at the tail and $+1$ at the head. As a data structure it is rarely the right choice, because it takes $\Theta(nm)$ space and most queries scan a whole row or column. Its value is algebraic: $BB^T$ is the [Laplacian matrix](/laplacian-matrix/), $B^TB$ gives the [line graph](/line-graph/), and the signed matrix is totally unimodular, which is why network flow problems have integer optimal solutions.

## In plain words

Make a table with one row for each town and one column for each road. In the column of a road, put a mark in the rows of the two towns that the road joins, and leave the rest blank. That table is the incidence matrix.

Each column has exactly two marks, whatever the size of the map. So the table is almost all blank, and it is large: the number of towns times the number of roads. To find the two ends of a road, you read down its column. To find the roads at a town, you read across its row. For one-way roads, you mark the start with a minus and the end with a plus. Then simple sums over the table count degrees and test connectivity.

## The abstract type

The incidence matrix stores a [graph](/graph/), possibly a [multigraph](/multigraph/), with named edges $e_0, \ldots, e_{m-1}$. It supports `add-edge(G, u, v) → e`, `ends(G, e)`, `incident(G, v)` (the edges at $v$), `adjacent(G, u, v)` and `degree(G, v)`. It also gives the matrix $B$ itself, for linear algebra.

## Representation

The graph has the vertices $0, \ldots, n - 1$ and the edges $e_0, \ldots, e_{m-1}$. The structure is the integer matrix $B \in \mathbb{Z}^{n \times m}$:

- **Undirected.** $B[v, e]$ is the number of times $v$ is an end of $e$. So $B[v, e] = 1$ when $v$ is one of two distinct ends of $e$, $B[v, e] = 2$ when $e$ is a [self-loop](/self-loop/) at $v$, and $B[v, e] = 0$ otherwise. Many books treat only loopless graphs and use entries 0 and 1.
- **Directed** (the convention of CLRS, Exercise 20.1-7). For an edge $e$ from $u$ to $v$ with $u \ne v$, $B[u, e] = -1$, $B[v, e] = +1$, and the other entries of the column are 0. A self-loop would need $-1$ and $+1$ in the same cell, so the signed matrix has no column for it; graphs with self-loops are not stored this way.

**Invariant.** Each column has exactly the two nonzero entries of the ends of its edge, as above. So each column of the undirected matrix sums to 2, each column of the signed matrix sums to 0, and the row sums are the degrees: $\sum_e B[v, e] = d(v)$ in the undirected case, and $\sum_e B[v, e] = d^-(v) - d^+(v)$ in the directed case, while the number of nonzeros in row $v$ is $d^+(v) + d^-(v)$.

Parallel edges are two equal columns, so a multigraph is stored without change. The order of the columns is the order of the edge names.

## Operations

```pseudo id=main
ADD-EDGE(B, u, v)                        ▷ a new column e = m
L1  append a zero column to B
L2  if directed then B[u, e] ← −1; B[v, e] ← +1
L3  else B[u, e] ← B[u, e] + 1; B[v, e] ← B[v, e] + 1    ▷ u = v gives 2
L4  return e

ENDS(B, e)
L5  for v ← 0 to n − 1 do
L6      if B[v, e] ≠ 0 then record v, |B[v, e]| times, with its sign
L7  return the two recorded vertices    ▷ the −1 entry is the tail

INCIDENT(B, v)
L8  return each e with B[v, e] ≠ 0, in increasing order

ADJACENT(B, u, v)                        ▷ directed: is there an edge from u to v?
L9  for e ← 0 to m − 1 do
L10     if B[u, e] = −1 and B[v, e] = +1 then return true
L11 return false
```

**Add.** A dense matrix stored row by row gets one new cell in each row, so ADD-EDGE takes $\Theta(n)$ time, amortized over the growth of the rows. Line L3 adds rather than sets, so that a self-loop gets the entry 2.

**Ends.** Lines L5 to L7 scan the column of $e$. This is $\Theta(n)$, against $O(1)$ for an [edge list](/edge-list/) or an [incidence list](/incidence-list/).

**Incident.** Line L8 scans the row of $v$, in $\Theta(m)$ time, even when $v$ has few edges.

**Adjacent.** Lines L9 to L11 scan the rows of $u$ and $v$ together. In the undirected case the test of line L10 is $B[u, e] \ne 0$ and $B[v, e] \ne 0$ for $u \ne v$, and $B[u, e] = 2$ for $u = v$. The time is $\Theta(m)$ in the worst case, against $O(1)$ for an [adjacency matrix](/adjacency-matrix/).

## Example

Take the vertices $0, 1, 2, 3$ and the edges $e_0 = \{0,1\}$, $e_1 = \{0,2\}$, $e_2 = \{1,2\}$, $e_3 = \{2,3\}$. The undirected matrix $B$ and the signed matrix $B_{\to}$ for the orientation $0 \to 1$, $0 \to 2$, $1 \to 2$, $2 \to 3$ are

$$B = \begin{pmatrix} 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 \\ 0 & 1 & 1 & 1 \\ 0 & 0 & 0 & 1 \end{pmatrix}, \qquad B_{\to} = \begin{pmatrix} -1 & -1 & 0 & 0 \\ 1 & 0 & -1 & 0 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & 0 & 1 \end{pmatrix}.$$

The row sums of $B$ are the degrees $2, 2, 3, 1$. ENDS$(B_{\to}, e_3)$ reads the column $(0, 0, -1, 1)$ and returns the tail 2 and the head 3. INCIDENT$(B, 2)$ reads the row $(0, 1, 1, 1)$ and returns $e_1, e_2, e_3$. The products are

$$B_{\to} B_{\to}^T = \begin{pmatrix} 2 & -1 & -1 & 0 \\ -1 & 2 & -1 & 0 \\ -1 & -1 & 3 & -1 \\ 0 & 0 & -1 & 1 \end{pmatrix}, \qquad B^T B = \begin{pmatrix} 2 & 1 & 1 & 0 \\ 1 & 2 & 1 & 1 \\ 1 & 1 & 2 & 1 \\ 0 & 1 & 1 & 2 \end{pmatrix}.$$

The first is $D - A$, the degree matrix minus the adjacency matrix, which is the [Laplacian](/laplacian-matrix/). The second is $2I$ plus the adjacency matrix of the line graph: $e_0, e_1, e_2$ share ends pairwise, and $e_3$ shares an end with $e_1$ and $e_2$ only.

## Correctness

The invariant holds after each ADD-EDGE: line L1 adds a column of zeros, and lines L2 and L3 put the entries of the two ends into it and change no other column. ENDS, INCIDENT and ADJACENT are then correct because, by the invariant, the nonzero entries of a column are exactly the ends of its edge, with the sign of the tail and the head. The algebraic facts follow from the same invariant:

- **$BB^T$.** The entry $(u, v)$ of $B_{\to}B_{\to}^T$ is $\sum_e B[u, e] B[v, e]$. For $u = v$ each edge at $u$ adds $(\pm 1)^2 = 1$, so the diagonal is $d^+(u) + d^-(u)$. For $u \ne v$ only edges with both ends $u$ and $v$ contribute, each with $(-1)(+1) = -1$. So $B_{\to}B_{\to}^T = D - A$ for the underlying undirected multigraph, whatever the orientation. For the unsigned matrix of a loopless graph the same computation gives $BB^T = D + A$.
- **$B^TB$.** For a loopless undirected graph, the entry $(e, f)$ is the number of common ends of $e$ and $f$. So the diagonal is 2, and for a simple graph the entry is 1 when $e$ and $f$ share an end and 0 otherwise: $B^TB = 2I + A(L(G))$.
- **Rank.** Let $G$ have $c$ connected components. A row vector $x$ with $x B_{\to} = 0$ has $x_v - x_u = 0$ for each edge $(u, v)$, so $x$ is constant on each component, and each such $x$ works. The left null space has dimension $c$, so $\operatorname{rank} B_{\to} = n - c$. A connected graph has rank $n - 1$, and a set of columns is linearly independent exactly when its edges form a forest.
- **Total unimodularity.** Each square submatrix $S$ of $B_{\to}$ has $\det S \in \{-1, 0, 1\}$. *Proof*, by induction on the size $k$ of $S$. For $k = 1$ the entries are in $\{-1, 0, 1\}$. For $k > 1$: if a column of $S$ is zero, $\det S = 0$. If a column has one nonzero entry, expand along it, and $\det S = \pm \det S'$ for a $(k-1) \times (k-1)$ submatrix $S'$. Otherwise each column of $S$ holds both nonzeros of its edge, $-1$ and $+1$, so the rows of $S$ sum to zero and $\det S = 0$. $\square$

The full proof of the operations is in `proofs/correctness.md`.

## Complexity

The model is the [word RAM](/word-ram/). For the dense matrix:

| operation | time | compare: adjacency list |
|---|---|---|
| ends$(e)$ | $\Theta(n)$ | not supported without edge names |
| incident$(v)$, degree$(v)$ | $\Theta(m)$ | $\Theta(1 + d(v))$ |
| adjacent$(u, v)$ | $\Theta(m)$ worst case | $O(1 + d(u))$ |
| add-edge | $\Theta(n)$ amortized | $O(1)$ amortized |
| add-vertex | $\Theta(m)$ | $O(1)$ amortized |
| remove-edge$(e)$ | $\Theta(nm)$ to shift the columns, or $\Theta(n)$ to zero a column | $O(d(u) + d(v))$ |
| space | $\Theta(nm)$ entries | $\Theta(n + m)$ |

A traversal such as [breadth-first search](/breadth-first-search/) on the dense matrix takes $\Theta(nm)$ time: for each vertex it scans its row, $\Theta(m)$, and for each edge found it scans a column, $\Theta(n)$. For a connected graph $nm \ge n(n-1)$, so this is at least as slow as on an adjacency matrix.

**Sparse storage.** The matrix has exactly $2m$ nonzeros. Stored by columns, in [compressed sparse column](/compressed-sparse-column/) form, it is an [edge list](/edge-list/) with $O(1)$ `ends`. Stored by rows, in [compressed sparse row](/compressed-sparse-row/) form, it is a static [incidence list](/incidence-list/) with $\Theta(1 + d(v))$ `incident`. Both use $\Theta(n + m)$ space. This is how solvers store it.

## Variants

- **Unsigned and signed.** The unsigned matrix of an undirected graph gives $BB^T = D + A$, the signless Laplacian. Orienting each edge arbitrarily and using the signed matrix gives $BB^T = D - A$, the Laplacian, for any choice of the orientation.
- **Weighted.** Scaling the column of $e$ by $\sqrt{w(e)}$ gives $BB^T = L_w$, the weighted Laplacian, with $w(e)$ in place of 1.
- **Hypergraphs.** A [hypergraph](/hypergraph/) edge may have any number of ends. Its incidence matrix has a 1 in each of them, and it is the standard way to store a hypergraph. The column sums are the sizes of the edges.
- **Bipartite graphs.** The unsigned incidence matrix of a [bipartite graph](/bipartite-graph/) is totally unimodular too: multiply the rows of one side by $-1$ and it becomes a signed incidence matrix.

## When to use it

Use the incidence matrix as a mathematical object: to write the flow conservation constraints $B_{\to} f = b$ of a [flow network](/flow-network/) as a linear program, to build the [Laplacian](/laplacian-matrix/), to prove the [matrix-tree theorem](/matrix-tree-theorem/) by the Cauchy-Binet formula, or to store a [hypergraph](/hypergraph/). Store it sparse, by rows or columns. Do not use the dense matrix to run graph algorithms: an [adjacency list](/adjacency-list/) or an [incidence list](/incidence-list/) does each operation faster in less space.

## Pitfalls

- **Self-loops in the signed matrix.** A self-loop would put $-1$ and $+1$ in one cell, which sums to 0 and loses the edge. Remove self-loops first, or use the unsigned matrix with the entry 2.
- **The sign convention.** CLRS put $-1$ at the tail and $+1$ at the head; other books do the opposite. Both give the same $BB^T$, but the sign of the flow balance $B f$ flips. State the convention in the code.
- **Dense storage.** A graph with $10^6$ vertices and $10^7$ edges has $10^{13}$ cells, of which $2 \cdot 10^7$ are nonzero. Use sparse storage.
- **Confusing $BB^T$ and $B^TB$.** The first is $n \times n$ and is about vertices; the second is $m \times m$ and is about edges.

## Implementations

The Python class stores the dense matrix row by row, with the signed convention of CLRS for directed graphs and the entry 2 for undirected self-loops. It also computes $BB^T$ and $B^TB$, to check the identities.

## History

The incidence matrix is one of the two classic matrices of a graph, with the adjacency matrix; Bondy and Murty and West define both at the start of their texts. CLRS give the signed incidence matrix as an exercise in their section on graph representations and ask what $BB^T$ represents.

## References
