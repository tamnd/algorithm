---
tag: RG5BXY
kind: data-structure
slug: compressed-sparse-column
name: Compressed sparse column
aliases:
- CSC
area: graphs/graph-representation
level: core
summary: Column-major analogue of CSR, storing in-neighbours of each vertex.
implements: [graph]
prereqs: [compressed-sparse-row]
see_also: [compressed-sparse-row, transpose-graph, sparse-matrix, sparse-matrix-vector-multiplication, pagerank, breadth-first-search, forward-star, counting-sort]
sources:
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 3.4 (Storage schemes), the compressed sparse column format as the CSR format of the transpose
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 2 (Basic algorithms), the compressed-column data structure of CSparse and the transpose of a matrix in that format
  - paper: doi:10.1109/SC.2012.50
    title: Scott Beamer, Krste Asanovic and David Patterson, Direction-optimizing breadth-first search, SC 2012
    locator: the bottom-up step, in which each unvisited vertex scans its in-neighbours, and the switch between top-down and bottom-up steps
---

Compressed sparse column (CSC) stores a static directed [graph](/graph/) on vertices $0, \ldots, n-1$ by its *in*-neighbours: an array $\mathit{src}$ of length $m$ holds the in-neighbours of vertex 0, then those of vertex 1, and so on, and an offset array $\mathit{coff}$ of length $n + 1$ marks where each column starts. It is the [compressed sparse row](/compressed-sparse-row/) format of the [transpose graph](/transpose-graph/), and in matrix terms it stores the [adjacency matrix](/adjacency-matrix/) column by column. It uses $n + 1 + m$ words, lists the in-neighbours of $v$ in $\Theta(d^-(v))$ time, and is built from a CSR array in $\Theta(n + m)$ time with columns already sorted. Algorithms that *pull* values from in-neighbours, such as [PageRank](/pagerank/) and the bottom-up step of [breadth-first search](/breadth-first-search/), read it in place of CSR.

## In plain words

In CSR, each vertex has a block listing the vertices it points to. In CSC, each vertex has a block listing the vertices that point to it. Everything else is the same: one long array of these blocks, laid end to end, and a short array saying where each block starts.

You need it because the arrows of a directed graph go one way. CSR answers "where can I go from here?" fast, but "who can reach me in one step?" would need a scan of the whole graph. CSC answers the second question fast. Many programs keep both. For a graph without arrows the two are the same thing.

## The abstract type

CSC implements the query part of the [graph](/graph/) type for a [directed graph](/directed-graph/), with self-loops allowed, seen from the heads of the edges: `in-neighbors(G, v)`, `in-degree(G, v)`, `adjacent(G, u, v)` and `edges(G)`, together with BUILD. Updates are done by a rebuild, as for CSR. For a simple undirected graph the adjacency matrix is symmetric, so CSC and CSR are the same arrays. A [weighted graph](/weighted-graph/) keeps a value array $\mathit{val}$ parallel to $\mathit{src}$, which in numerical computing holds the nonzero entries of a [sparse matrix](/sparse-matrix/) column by column.

## Representation

The structure has $n$, the array $\mathit{coff}[0 \ldots n]$ and the array $\mathit{src}[0 \ldots m-1]$. The *column* of $v$ is the segment $\mathit{src}[\mathit{coff}[v] \ldots \mathit{coff}[v+1] - 1]$, and it holds the tails $u$ of the edges $(u, v)$.

**Invariant (K).**

- (K1) $\mathit{coff}[0] = 0$, $\mathit{coff}[n] = m$, and $\mathit{coff}[v] \le \mathit{coff}[v+1]$ for each $v$.
- (K2) Each column is sorted in strictly increasing order.

The graph it stands for has the edge $(u, v)$ for each $u$ in the column of $v$. So column $v$ of the adjacency matrix $A$ has its 1s at the rows listed in the column of $v$, which is why the format has its name. The space is $n + 1 + m$ words.

## Operations

```pseudo id=main
BUILD-FROM-CSR(n, off, adj)              ▷ CSR of the same graph, rows of length d⁺(u)
L1  cnt[0 … n] ← 0
L2  for i ← 0 to m − 1 do cnt[adj[i] + 1] ← cnt[adj[i] + 1] + 1
L3  coff[0] ← 0; for v ← 1 to n do coff[v] ← coff[v − 1] + cnt[v]
L4  pos[v] ← coff[v] for each v in 0 … n − 1
L5  for u ← 0 to n − 1 do
L6      for i ← off[u] to off[u + 1] − 1 do
L7          v ← adj[i]; src[pos[v]] ← u; pos[v] ← pos[v] + 1

IN-NEIGHBORS(G, v)
L8  for i ← coff[v] to coff[v + 1] − 1 do output src[i]

IN-DEGREE(G, v)
L9  return coff[v + 1] − coff[v]

ADJACENT(G, u, v)                        ▷ binary search for u in the column of v
L10 lo ← coff[v]; hi ← coff[v + 1]
L11 while lo < hi do
L12     mid ← ⌊(lo + hi)/2⌋
L13     if src[mid] < u then lo ← mid + 1 else hi ← mid
L14 return lo < coff[v + 1] and src[lo] = u
```

**Build** (lines L1 to L7) is a [counting sort](/counting-sort/) of the edges by their head. Line L2 counts the in-degrees, line L3 turns them into [prefix sums](/prefix-sums/), and lines L5 to L7 walk the CSR rows in increasing order of $u$ and drop each tail into the next free slot of its column. Since the tails arrive in increasing order, each column comes out sorted, with no extra sort. The time is $\Theta(n + m)$. Building CSC from an [edge list](/edge-list/) is BUILD of the CSR page with the roles of the two ends swapped.

**In-neighbors and in-degree** (lines L8 and L9) read one column and two offsets, in $\Theta(d^-(v))$ and $O(1)$ time.

**Adjacent** (lines L10 to L14) is a [binary search](/binary-search/) for $u$ in the sorted column of $v$, in $O(\log d^-(v))$ time. With both CSR and CSC at hand, the query can search the shorter of the row of $u$ and the column of $v$.

**Matrix view.** For the adjacency matrix $A$, the CSC arrays of $A$ are the CSR arrays of $A^{\mathsf T}$. So the product $y = A^{\mathsf T} x$, with $y[v] = \sum_{u : (u, v) \in E} x[u]$, is one pass over the columns, and each $y[v]$ is computed by one thread without writes to shared entries. This is the *pull* form of an update; the *push* form over CSR adds $x[u]$ into $y[v]$ for each out-neighbour $v$ and needs atomic writes when run in parallel.

## Example

Take the directed graph on $\{0, \ldots, 4\}$ with the edges $(0,1), (0,2), (1,2), (2,3), (3,1), (3,4)$. Its CSR arrays, from the [compressed sparse row](/compressed-sparse-row/) page, are $\mathit{off} = [0, 2, 3, 4, 6, 6]$ and $\mathit{adj} = [1, 2 \mid 2 \mid 3 \mid 1, 4 \mid\ ]$.

Line L2 counts the heads: $\mathit{cnt} = [0, 0, 2, 2, 1, 1]$, so the in-degrees are $0, 2, 2, 1, 1$, and line L3 gives $\mathit{coff} = [0, 0, 2, 4, 5, 6]$. Line L4 sets $\mathit{pos} = [0, 0, 2, 4, 5]$. Lines L5 to L7 then read the CSR rows:

| CSR entry | edge | slot $\mathit{pos}[v]$ | $\mathit{src}$ after the step |
|---|---|---|---|
| row 0, entry 1 | $(0, 1)$ | 0 | 0 \_ \_ \_ \_ \_ |
| row 0, entry 2 | $(0, 2)$ | 2 | 0 \_ 0 \_ \_ \_ |
| row 1, entry 2 | $(1, 2)$ | 3 | 0 \_ 0 1 \_ \_ |
| row 2, entry 3 | $(2, 3)$ | 4 | 0 \_ 0 1 2 \_ |
| row 3, entry 1 | $(3, 1)$ | 1 | 0 3 0 1 2 \_ |
| row 3, entry 4 | $(3, 4)$ | 5 | 0 3 0 1 2 3 |

So $\mathit{coff} = [0, 0, 2, 4, 5, 6]$ and $\mathit{src} = [\ \mid 0, 3 \mid 0, 1 \mid 2 \mid 3]$. Then:

- IN-NEIGHBORS$(1)$ reads $\mathit{src}[0 \ldots 1] = 0, 3$: the edges $(0, 1)$ and $(3, 1)$.
- IN-DEGREE$(0) = \mathit{coff}[1] - \mathit{coff}[0] = 0$, so 0 is a source.
- ADJACENT$(1, 2)$ searches the column $[0, 1]$ of vertex 2 and finds 1, so the answer is yes. ADJACENT$(2, 1)$ searches the column $[0, 3]$ of vertex 1 and does not find 2, so the answer is no.

**A pull step.** With $x = [1, 1, 1, 1, 1]$, the product $y = A^{\mathsf T} x$ has $y[v] = $ the in-degree of $v$, so $y = [0, 2, 2, 1, 1]$, computed column by column.

## Correctness

BUILD-FROM-CSR is the counting sort of the CSR page applied with the head as the key. By the same argument as Lemma 1 there, $\mathit{coff}[v]$ is the number of edges with head less than $v$, which gives (K1) and makes the columns disjoint segments of the right lengths $d^-(v)$. Each edge $(u, v)$ is read once from the CSR row of $u$, and its tail $u$ goes into the next free slot of column $v$, so each column ends up holding exactly the tails of the edges into $v$. Lines L5 and L6 visit the tails in increasing order, and the edges of the graph are distinct, so each column is strictly increasing, which is (K2). IN-NEIGHBORS and IN-DEGREE read one column, and ADJACENT is a binary search in a sorted column, with the same proof as on the CSR page. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| build from CSR | $\Theta(n + m)$ | columns come out sorted |
| build from an edge list | $\Theta(n + m)$ | two counting passes for sorted columns |
| in-neighbors$(v)$ | $\Theta(d^-(v))$ | consecutive memory |
| in-degree$(v)$ | $O(1)$ | |
| out-neighbors$(u)$ from CSC alone | $\Theta(n + m)$ | scan all columns |
| adjacent$(u, v)$ | $O(\log d^-(v))$ | |
| $y = A^{\mathsf T} x$ (pull) | $\Theta(n + m)$ | no write conflicts in parallel |
| updates | $\Theta(n + m)$ | rebuild |
| space | $n + 1 + m$ words | $2(n + 1 + m)$ for CSR and CSC together |

**Direction-optimizing BFS.** In a breadth-first search, a *top-down* step scans the out-neighbours of each frontier vertex in CSR. A *bottom-up* step instead lets each unvisited vertex scan its in-neighbours in CSC and stop at the first one in the frontier. When the frontier is large, as in the middle levels of a search on a social network, the bottom-up step reads far fewer edges. Beamer, Asanovic and Patterson switch between the two steps by comparing the sizes of the frontier and of the unvisited set, and so keep both arrays.

## Variants

- **CSR and CSC together.** A directed graph that needs both directions keeps both, for twice the space. This is the common layout in graph analytics libraries.
- **Weighted CSC.** A value array parallel to $\mathit{src}$. In direct sparse solvers, compressed column is the main format, since many factorization algorithms work column by column.
- **Unsorted columns.** Building from an unsorted edge list in one counting pass gives columns in input order, with $O(d^-(v))$ queries.
- **Undirected graphs.** The matrix is symmetric, so CSC and CSR coincide, and in-neighbours are neighbours.
- **Bipartite and rectangular forms.** For an $r \times c$ matrix, such as the biadjacency matrix of a [bipartite graph](/bipartite-graph/), CSC has $c + 1$ offsets and lists for each column the rows with a nonzero entry.

## When to use it

Use CSC for a static directed graph when the algorithm asks for the in-neighbours of a vertex: pull-style iterations such as [PageRank](/pagerank/) and other fixed-point computations over in-edges, bottom-up BFS steps, the backward search of a bidirectional search, and the second pass of Kosaraju's [strongly connected components](/strongly-connected-components/) algorithm, which searches the [transpose graph](/transpose-graph/). In numerical work, use it when the solver accesses the matrix by columns. Use [CSR](/compressed-sparse-row/) for out-neighbours; for a graph that changes, use an [adjacency list](/adjacency-list/) with in-lists.

## Pitfalls

- **Rows and columns.** Cell $(u, v)$ of the adjacency matrix is the edge from $u$ to $v$, so the column of $v$ holds the tails. Some libraries use the opposite convention, with $A[v][u]$ for the edge $(u, v)$, which swaps the meaning of CSR and CSC. Check the convention before you pass arrays between libraries.
- **CSC of an undirected graph.** Building a separate CSC for an undirected graph doubles the space for no gain.
- **The last offset.** As for CSR, $\mathit{coff}$ has $n + 1$ entries.
- **Keeping two copies consistent.** When a graph is stored in both CSR and CSC, a rebuild of one must be followed by a rebuild of the other, or the two describe different graphs.
- **Isolated sources.** A vertex with in-degree 0 has an empty column, so $\mathit{coff}[v] = \mathit{coff}[v+1]$. Code that assumes each column has an entry reads the column of the next vertex.

## Implementations

The Python class `CompressedSparseColumn` builds from the arrays of a CSR, as in the main block, and has a class method that builds from an edge list by first building the CSR. It keeps `coff` and `src` as Python lists. `check_invariant` tests (K1) and (K2).

## History

The compressed column format is as old as the CSR or Yale format of sparse matrix computation, and Saad (Section 3.4) presents it as the CSR format of the transpose. It is the main format of direct sparse solvers, as in Davis's CSparse library (Chapter 2). In graph algorithms, its use for the in-edges of a graph became common with parallel graph frameworks and with the direction-optimizing BFS of Beamer, Asanovic and Patterson in 2012.

## References
