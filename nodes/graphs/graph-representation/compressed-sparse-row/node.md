---
tag: J0260T
kind: data-structure
slug: compressed-sparse-row
name: Compressed sparse row
aliases:
- CSR
- Yale format
- packed adjacency array
area: graphs/graph-representation
level: core
summary: Adjacency lists packed into one edge array with an offset array; cache-friendly and compact.
implements: [graph]
prereqs: [adjacency-list, prefix-sums, counting-sort]
see_also: [compressed-sparse-column, adjacency-list, forward-star, edge-list, sparse-matrix, sparse-matrix-vector-multiplication, graph-compression, packed-memory-array]
sources:
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 3.4 (Storage schemes), the compressed sparse row format with its arrays of values, column indices and row pointers, and the compressed sparse column format
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox
    locator: Section 8.2 (Representation of graphs by adjacency arrays), the static adjacency array with its first-edge index and the remark on cache efficiency
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows
    locator: Section 2.3 (Network representations), the forward star representation with its point array and arc list sorted by tail
---

Compressed sparse row (CSR) stores a static [graph](/graph/) on vertices $0, \ldots, n-1$ in two arrays: an array $\mathit{adj}$ of length $m$ that holds the out-neighbours of vertex 0, then those of vertex 1, and so on, and an offset array $\mathit{off}$ of length $n + 1$ such that the neighbours of $u$ are $\mathit{adj}[\mathit{off}[u] \ldots \mathit{off}[u+1] - 1]$. It is an [adjacency list](/adjacency-list/) with all lists laid end to end, so it uses $n + 1 + m$ words, lists the neighbours of $u$ in $\Theta(d(u))$ time by reading consecutive memory, and gives the degree in $O(1)$ time. It is built from an [edge list](/edge-list/) by one [counting sort](/counting-sort/) in $\Theta(n + m)$ time, but adding or removing an edge requires a rebuild. It is the standard format of sparse matrices in numerical computing and of large static graphs in graph libraries.

## In plain words

Write the neighbour list of vertex 0, then right after it the list of vertex 1, then the list of vertex 2, and so on, all in one long array. Then keep a second, short array that says where the list of each vertex starts. The list of a vertex ends where the list of the next vertex starts.

This takes less memory than separate lists, because there is no list header, no pointer and no spare room per vertex. It is also fast to read, because the neighbours of a vertex sit next to each other in memory. The cost is that the graph is frozen: to add one edge, you must shift everything after it.

## The abstract type

CSR implements the query part of the [graph](/graph/) type over $V = \{0, \ldots, n-1\}$: `adjacent`, `neighbors`, `degree` and `edges`, together with a BUILD operation that makes the structure from $n$ and a list of edges. The updates `add-edge`, `remove-edge` and `add-vertex` are done by a rebuild. It stores a [directed graph](/directed-graph/), with self-loops allowed, in $m$ entries, or a simple [undirected graph](/undirected-graph/) with each edge $\{u, v\}$ stored in both rows, in $2m$ entries. A [weighted graph](/weighted-graph/) keeps a third array $\mathit{val}$ parallel to $\mathit{adj}$.

## Representation

The structure has $n$, the array $\mathit{off}[0 \ldots n]$ and the array $\mathit{adj}[0 \ldots M - 1]$, where $M = m$ for a directed graph and $M = 2m$ for an undirected graph. The *row* of $u$ is the segment $\mathit{adj}[\mathit{off}[u] \ldots \mathit{off}[u+1] - 1]$.

**Invariant (C).**

- (C1) $\mathit{off}[0] = 0$, $\mathit{off}[n] = M$, and $\mathit{off}[u] \le \mathit{off}[u+1]$ for each $u$.
- (C2) Each row is sorted in strictly increasing order, so no row holds a vertex twice.
- (C3) If the graph is undirected, $v$ is in the row of $u$ if and only if $u$ is in the row of $v$, and $u$ is not in its own row.

The graph it stands for has the edge $(u, v)$, or $\{u, v\}$, for each $v$ in the row of $u$. Rule (C2) is a choice: unsorted rows are also common, and then ADJACENT scans the row. The space is $n + 1 + M$ words, which is $\Theta(n + m)$; with 32-bit entries and offsets it is $4(n + 1 + M)$ bytes.

## Operations

```pseudo id=main
BUILD(n, E)                    ▷ E: a list of distinct (u, v); undirected edges in both orders
L1  cnt[0 … n] ← 0
L2  for each (u, v) in E do cnt[u + 1] ← cnt[u + 1] + 1
L3  off[0] ← 0; for u ← 1 to n do off[u] ← off[u − 1] + cnt[u]
L4  pos[u] ← off[u] for each u in 0 … n − 1
L5  for each (u, v) in E do
L6      adj[pos[u]] ← v; pos[u] ← pos[u] + 1
L7  sort each row adj[off[u] … off[u + 1] − 1]

NEIGHBORS(G, u)
L8  for i ← off[u] to off[u + 1] − 1 do output adj[i]

DEGREE(G, u)
L9  return off[u + 1] − off[u]

ADJACENT(G, u, v)              ▷ binary search in the sorted row of u
L10 lo ← off[u]; hi ← off[u + 1]
L11 while lo < hi do
L12     mid ← ⌊(lo + hi)/2⌋
L13     if adj[mid] < v then lo ← mid + 1 else hi ← mid
L14 return lo < off[u + 1] and adj[lo] = v
```

**Build** (lines L1 to L7) is a [counting sort](/counting-sort/) of the edges by their first end. Line L2 counts the out-degrees, line L3 turns the counts into [prefix sums](/prefix-sums/), which are the starts of the rows, and lines L5 and L6 drop each edge into the next free slot of its row. Lines L1 to L6 take $\Theta(n + M)$ time. Line L7 can sort each row by a comparison sort in $O(\sum_u d(u) \log d(u)) = O(M \log n)$ time. Or it can be done in $\Theta(n + M)$ time by running lines L1 to L6 twice: first by the second end $v$, then by the first end $u$. Since the counting sort is [stable](/stable-sort/), the second pass keeps each row in increasing order of $v$.

**Neighbors and degree** (lines L8 and L9) read one segment and two offsets. NEIGHBORS takes $\Theta(d(u))$ time and reads consecutive memory, which is the main speed advantage of CSR over linked or separately allocated lists, as each cache line brings in many neighbours.

**Adjacent** (lines L10 to L14) is a [binary search](/binary-search/) in the row of $u$, in $O(\log d(u))$ time. For an undirected graph, searching the shorter of the two rows gives $O(\log \min(d(u), d(v)))$.

**Updates.** Inserting $v$ into the row of $u$ shifts all later entries of $\mathit{adj}$ one place and increases $\mathit{off}[u+1], \ldots, \mathit{off}[n]$, which costs $\Theta(n + M)$ in the worst case. In practice, updates are collected in a batch and the structure is rebuilt once from the old rows and the batch, in $\Theta(n + M + b)$ time for $b$ updates.

## Example

Take the directed graph on $\{0, \ldots, 4\}$ with the edges $(0,1), (0,2), (1,2), (2,3), (3,1), (3,4)$, given to BUILD in the order

$$E = (3,4),\ (0,2),\ (2,3),\ (3,1),\ (0,1),\ (1,2).$$

Line L2 gives $\mathit{cnt} = [0, 2, 1, 1, 2, 0]$, so line L3 gives $\mathit{off} = [0, 2, 3, 4, 6, 6]$, and line L4 sets $\mathit{pos} = [0, 2, 3, 4, 6]$. Lines L5 and L6 then fill $\mathit{adj}$:

| edge | slot $\mathit{pos}[u]$ | $\mathit{adj}$ after the step |
|---|---|---|
| $(3, 4)$ | 4 | \_ \_ \_ \_ 4 \_ |
| $(0, 2)$ | 0 | 2 \_ \_ \_ 4 \_ |
| $(2, 3)$ | 3 | 2 \_ \_ 3 4 \_ |
| $(3, 1)$ | 5 | 2 \_ \_ 3 4 1 |
| $(0, 1)$ | 1 | 2 1 \_ 3 4 1 |
| $(1, 2)$ | 2 | 2 1 2 3 4 1 |

Line L7 sorts the rows $[2, 1]$ and $[4, 1]$, so the final arrays are

$$\mathit{off} = [0, 2, 3, 4, 6, 6], \qquad \mathit{adj} = [1, 2, \mid 2, \mid 3, \mid 1, 4, \mid\ ],$$

with bars between the rows. Then:

- NEIGHBORS$(3)$ reads $\mathit{adj}[4 \ldots 5] = 1, 4$.
- DEGREE$(3) = \mathit{off}[4] - \mathit{off}[3] = 6 - 4 = 2$, and DEGREE$(4) = 6 - 6 = 0$.
- ADJACENT$(3, 4)$: $\mathit{lo} = 4$, $\mathit{hi} = 6$, $\mathit{mid} = 5$, $\mathit{adj}[5] = 4$ is not less than 4, so $\mathit{hi} = 5$; $\mathit{mid} = 4$, $\mathit{adj}[4] = 1 < 4$, so $\mathit{lo} = 5$. The loop ends with $\mathit{adj}[5] = 4$, so the answer is yes.
- ADJACENT$(1, 0)$: the row of 1 is $[2]$; the search ends with $\mathit{lo} = 2$ and $\mathit{adj}[2] = 2 \ne 0$, so the answer is no.

The arrays take $6 + 6 = 12$ words. Separate lists for the same graph also need 6 entries, plus a header and spare capacity for each of the 5 lists.

For the undirected graph on $\{0, \ldots, 5\}$ with the edges $01, 02, 12, 13, 23, 34, 45$, each edge goes in both rows, so $M = 14$, $\mathit{off} = [0, 2, 5, 8, 11, 13, 14]$ and $\mathit{adj} = [1, 2 \mid 0, 2, 3 \mid 0, 1, 3 \mid 1, 2, 4 \mid 3, 5 \mid 4]$. The differences of the offsets are the degrees $2, 3, 3, 3, 2, 1$.

## Correctness

BUILD is a counting sort, so it places each edge in the row of its first end: by line L3, $\mathit{off}[u]$ is the number of edges whose first end is less than $u$, so the rows are disjoint segments that cover $\mathit{adj}$, and the segment of $u$ has exactly $d(u)$ slots. Lines L5 and L6 put each edge in the next free slot of its row, and after the loop $\mathit{pos}[u] = \mathit{off}[u+1]$, so each slot is filled exactly once. This gives (C1), and after line L7 rows are sorted, with no repeats since the edges are distinct, which gives (C2). NEIGHBORS and DEGREE read the row of $u$, so they answer for the stored graph. ADJACENT keeps the condition that the entries before $\mathit{lo}$ in the row are less than $v$ and the entries from $\mathit{hi}$ on are at least $v$, so at the end $\mathit{lo}$ is the first position of the row with an entry at least $v$, and $v$ is in the row exactly when that entry exists and equals $v$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $M$ be the number of entries, $m$ or $2m$.

| operation | time | notes |
|---|---|---|
| build from an edge list | $\Theta(n + M)$ | with two counting passes for sorted rows |
| neighbors$(u)$ | $\Theta(d(u))$ | consecutive memory |
| degree$(u)$ | $O(1)$ | two offsets |
| adjacent$(u, v)$ | $O(\log d(u))$ | $O(d(u))$ with unsorted rows |
| list all edges | $\Theta(n + M)$ | |
| transpose (build [CSC](/compressed-sparse-column/)) | $\Theta(n + M)$ | one counting sort by second end |
| add-edge, remove-edge, add-vertex | $\Theta(n + M)$ | rebuild |
| batch of $b$ updates | $\Theta(n + M + b)$, plus sorting the batch | one rebuild |
| space | $n + 1 + M$ words | $(n + 1) + 2M$ with weights |

**Whole-graph algorithms.** [BFS](/breadth-first-search/), [DFS](/depth-first-search/), [Dijkstra](/dijkstra/) and the other algorithms that read the neighbours of each vertex run in the same asymptotic time as on an [adjacency list](/adjacency-list/), $\Theta(n + m)$ plus the cost of their own structures. In practice they often run several times faster on CSR, because the scan of a row is a sequential read. [Sparse matrix-vector multiplication](/sparse-matrix-vector-multiplication/), the inner step of [PageRank](/pagerank/) and of iterative solvers, is one pass over $\mathit{off}$, $\mathit{adj}$ and $\mathit{val}$, in $\Theta(n + M)$ time.

**Space against an adjacency list.** Both need $\Theta(n + m)$ words, but CSR has no per-list overhead. With 32-bit numbers, an undirected graph with $n = 10^6$ and $m = 10^7$ takes $4(10^6 + 1 + 2 \cdot 10^7) \approx 84$ MB in CSR. In a language with one allocated dynamic array per vertex, the per-list headers and the spare capacity of up to a factor 2 add tens of MB or more.

## Variants

- **Weighted CSR.** A value array $\mathit{val}$ parallel to $\mathit{adj}$ holds $w(u, \mathit{adj}[i])$ at index $i$. In numerical computing these are the nonzero entries of a [sparse matrix](/sparse-matrix/), and the three arrays are its CSR or Yale format.
- **[Compressed sparse column](/compressed-sparse-column/).** The same layout for the columns, which gives the in-neighbours. Keeping both gives out- and in-neighbours in $\Theta(d)$ time.
- **[Forward star](/forward-star/).** The network flow name for the same idea, usually with the arcs stored as records that also carry the tail, the cost and the capacity, and with a reverse star for the in-arcs.
- **Unsorted rows.** Skipping line L7 saves its cost and keeps the input order, at the price of $O(d(u))$ queries.
- **Offsets of 64 bits.** When $M \ge 2^{32}$, the offsets need 64 bits even if vertex numbers fit in 32.
- **Dynamic CSR.** Leaving gaps in $\mathit{adj}$, as a [packed memory array](/packed-memory-array/) does, gives insertions in polylogarithmic amortized time while keeping rows almost contiguous.
- **Compressed rows.** Storing each sorted row as the gaps between consecutive entries, with [variable-byte](/variable-byte-encoding/) or [Elias-Fano](/elias-fano-encoding/) codes, cuts the space of large real graphs to a few bits per edge. See [graph compression](/graph-compression/).

## When to use it

Use CSR for a graph that is built once and read many times: road networks for route planning, web and social graphs for analytics, meshes and matrices for numerical methods, and the input of parallel graph algorithms, which split $\mathit{adj}$ among threads by the offsets. Use an [adjacency list](/adjacency-list/) or [hash-based adjacency](/hash-based-adjacency/) when edges are added and removed one at a time between the queries.

## Pitfalls

- **The last offset.** The offset array has $n + 1$ entries, not $n$. Code that allocates $n$ entries reads past the end when it computes the row of vertex $n - 1$.
- **Undirected edges once.** For an undirected graph, BUILD must get each edge in both orders. Given only $(u, v)$ with $u < v$, it builds a directed graph, and a search from $v$ misses $u$.
- **Duplicate input edges.** BUILD does not remove repeats. A file that lists an edge twice gives a row with a repeated entry, which breaks (C2) and doubles that edge in each scan. Remove repeats after line L7 by one pass over each sorted row, and recompute the offsets.
- **Offset overflow.** With 32-bit offsets, a graph with $2^{32}$ or more entries wraps around. Use 64-bit offsets for large graphs.
- **Updates one at a time.** A loop that adds $k$ edges one by one to a CSR rebuilds it $k$ times, for $\Theta(k(n + m))$ time. Collect the edges and rebuild once.
- **Vertex numbers.** CSR needs vertices numbered $0, \ldots, n - 1$ without gaps. Relabel the vertices first if their names are sparse or are strings.

## Implementations

The Python class `CompressedSparseRow` has the arrays `off` and `adj` as Python lists and follows the main block line by line. Its constructor is BUILD; it takes the edges of an undirected graph once each and adds both orders itself. Line L7 is the two-pass counting sort. `check_invariant` tests (C1) to (C3).

## History

The format comes from sparse matrix computation, where it is known as the Yale format after the Yale Sparse Matrix Package of the 1970s; Saad (Section 3.4) describes it with its column-major twin. In network optimization the same layout, with arcs sorted by tail and an array of first-arc positions, is the forward star, presented by Ahuja, Magnanti and Orlin (Section 2.3). Mehlhorn and Sanders (Section 8.2) present it as the adjacency array, the representation of choice for static graphs.

## References
