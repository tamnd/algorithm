---
tag: WFJE4Y
kind: problem
slug: neighborhood-enumeration
name: Neighborhood enumeration
aliases:
- neighbour listing
- adjacency listing
area: graphs/graph-representation
level: intro
summary: Given a vertex, report all its neighbours efficiently.
prereqs: [neighborhood, adjacency-list, adjacency-matrix]
see_also: [neighborhood, adjacency-query, adjacency-list, adjacency-matrix, compressed-sparse-row, breadth-first-search, common-neighbors, transpose-graph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), the cost of listing the vertices adjacent to a vertex in each representation; Section 20.2, the aggregate analysis of the adjacency-list scans in breadth-first search
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the table of costs for iterating over the vertices adjacent to v in each representation
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox, Springer, 2008
    locator: Chapter 8 (Graph representation), the operations on edge sequences, adjacency arrays and adjacency matrices
---

Neighborhood enumeration is the problem of listing the [neighbours](/neighborhood/) of a given [vertex](/vertex/): given a graph $G$ and a vertex $v$, report each vertex of $N(v)$ once. It is the inner loop of almost every graph algorithm. [Breadth-first search](/breadth-first-search/), [depth-first search](/depth-first-search/), Dijkstra, Prim and the [Kahn](/kahns-algorithm/) topological sort all do "for each neighbour $u$ of $v$", and their running times are sums of the costs of these listings. The answer depends on the representation: $\Theta(1 + d(v))$ time with an [adjacency list](/adjacency-list/), which is optimal, and $\Theta(n)$ with an [adjacency matrix](/adjacency-matrix/).

## In plain words

You stand at one place on a map and want to know every place you can reach in one step. If you keep, for each place, a short list of its direct links, you read that list and are done: the work is the length of the list. If you keep instead a big table with one row and one column for every place, you must read the whole row, even when the place has only two links, because each cell could be a link.

Graph search repeats this step for every place it visits. With lists, the total work is the total length of all the lists, which is about the number of links. With the table, the total work is the size of the table.

## Definition

**Input.** A graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, stored in a fixed representation, and a vertex $v \in V$. $G$ is [directed](/directed-graph/) or [undirected](/undirected-graph/), simple or a [multigraph](/multigraph/).

**Output.** The elements of the [neighborhood](/neighborhood/) $N(v) = \{u : \{v, u\} \in E\}$ for an undirected graph, or of the out-neighborhood $N^+(v) = \{u : (v, u) \in E\}$ for a directed graph, each reported once, in any order. In a multigraph the usual output lists each incident edge, so a neighbour appears $\mu(v, u)$ times; a page must say which output it wants.

**The cost measure.** Time on the [word RAM](/word-ram/), as a function of $n$, $m$ and $d = |N(v)|$, plus the extra space. The output has size $d$, so the time is at least $\Omega(d)$ in every representation, and $\Omega(1)$ to decide that $d = 0$.

**As an iterator.** In code the problem is an iterator: `neighbors(v)` returns the elements one at a time. The cost of an iterator has two parts: the time to the first element (or to "none"), and the time between elements. An iterator with $O(1)$ time per step and $O(1)$ start-up gives $\Theta(1 + d)$ in total.

## Variants

- **Out- and in-neighbours.** For a directed graph, list $N^+(v)$ or $N^-(v)$. A representation built for one direction answers the other only by a full scan, unless both are stored or the [transpose](/transpose-graph/) is built.
- **Sorted output.** Report $N(v)$ in increasing order. Free if the lists are kept sorted, as in [compressed sparse row](/compressed-sparse-row/); otherwise it costs a sort of $d$ elements.
- **Weighted.** Report each neighbour with the weight of the edge; see [weighted graph](/weighted-graph/).
- **Edges, not vertices.** Report the incident edges, with names, as in an [incidence list](/incidence-list/). This is the right output for multigraphs and for algorithms that delete edges, such as Hierholzer's.
- **Filtered.** Report the neighbours with a property, such as the unvisited ones. With a plain list this costs $\Theta(1 + d)$; special structures, such as a list of unvisited vertices for BFS on the [complement graph](/complement-graph/), avoid scanning the visited ones.
- **Common neighbours.** Report $N(u) \cap N(v)$; see [common neighbors](/common-neighbors/). With sorted lists it costs $O(d(u) + d(v))$ by a merge.

## Examples

Let $G$ be undirected with $V = \{0, 1, 2, 3, 4\}$ and $E = \{01, 02, 12, 13\}$, and let $v = 1$, so $N(1) = \{0, 2, 3\}$ and $d = 3$.

| representation | stored data for vertex 1 | steps to list $N(1)$ |
|---|---|---|
| adjacency list | $\text{Adj}[1] = [0, 2, 3]$ | 3 reads |
| compressed sparse row | $\text{off} = [0, 2, 5, 7, 8, 8]$, $\text{adj}[2..4] = 0, 2, 3$ | 2 reads of $\text{off}$, then 3 reads |
| adjacency matrix | row 1 $= (1, 0, 1, 1, 0)$ | 5 reads, 3 hits |
| edge list | $(0,1), (0,2), (1,2), (1,3)$ | 4 reads, 3 hits |

For the isolated vertex 4, the adjacency list returns at once, the CSR form finds $\text{off}[4] = \text{off}[5] = 8$ in two reads, and the matrix still reads its whole row of 5 entries.

## Known algorithms

- **Scan the adjacency list.** Walk $\text{Adj}[v]$ from the head. $\Theta(1 + d)$ time, $O(1)$ extra space. Optimal.
- **Scan a CSR slice.** Read $\text{adj}[\text{off}[v] .. \text{off}[v+1] - 1]$. $\Theta(1 + d)$ time, and the slice is contiguous, so a scan costs $O(1 + d/B)$ transfers in the [external memory model](/external-memory-model/) with blocks of $B$ words.
- **Scan a matrix row.** Read $A[v, 0], \ldots, A[v, n-1]$ and report the columns with a 1. $\Theta(n)$ time. With a [bitset row](/bitset-adjacency-matrix/) of $w$-bit words, the time drops to $O(n/w + d)$: skip zero words, and in a nonzero word find each set bit by a count-trailing-zeros instruction.
- **Scan an edge list.** Read all $m$ edges and report the other end of each edge at $v$. $\Theta(m)$ time.
- **Hash-based adjacency.** Iterate the hash set of $v$. $\Theta(1 + d)$ time if the set iterates over its elements only, but $\Theta(\text{capacity})$ if it scans its empty slots; see [hash-based adjacency](/hash-based-adjacency/).

## Bounds

**Output lower bound.** Each algorithm reports $d$ items, so it takes $\Omega(d)$ time, and $\Omega(1 + d)$ in total. The adjacency list meets this bound.

**Matrix lower bound.** With only probes "is $A[v, u] = 1$?" to the adjacency matrix, every algorithm needs $n - 1$ probes in the worst case, even when $d = 0$. *Proof by adversary.* The adversary answers 0 to every probe. If the algorithm stops before it has probed some $A[v, u]$ with $u \ne v$, the adversary can set that entry to 1 or to 0, and the answer "$N(v) = \emptyset$" is wrong for one of the two graphs. So all $n - 1$ entries off the diagonal must be probed (and the diagonal too, if loops are allowed). This is why a [sparse graph](/sparse-graph/) should not be stored as a matrix.

**Total over a search.** In BFS or DFS each vertex's neighbourhood is listed at most once, so the total cost is

$$\sum_{v \in V} \Theta(1 + d(v)) = \Theta(n + m)$$

with adjacency lists, by the [handshake lemma](/handshake-lemma/) for undirected graphs ($\sum d(v) = 2m$) and by $\sum d^+(v) = m$ for directed ones. With a matrix the total is $\Theta(n^2)$. This aggregate argument is how CLRS bound BFS by $O(V + E)$.

## Reductions

- **From in-neighbours to out-neighbours.** Building the [transpose graph](/transpose-graph/) in $\Theta(n + m)$ time once turns every query for $N^-(v)$ into a query for $N^+(v)$ in the transpose, at $\Theta(1 + d^-(v))$ each.
- **From adjacency testing.** With only an oracle for the [adjacency query](/adjacency-query/) "is $uv \in E$?", enumeration costs $n - 1$ queries, as in the matrix bound above. So an adjacency oracle never replaces a neighbour list for sparse graphs.
- **To adjacency testing.** Enumeration answers "is $uv \in E$?" in $O(1 + d(u))$ time by a scan, or in $O(1 + \min(d(u), d(v)))$ for an undirected graph by scanning the shorter list.

## Applications

- **Graph search.** BFS, DFS and every algorithm built on them, such as [connected components](/connected-components/) and [strongly connected components](/strongly-connected-components/).
- **Shortest paths and spanning trees.** Dijkstra and Prim relax the edges of each vertex once, through its neighbour list.
- **Local counts.** [Triangle counting](/triangle-counting/) lists neighbourhoods and intersects them.
- **Message passing.** PageRank and graph neural networks update each vertex from the values on its neighbours, so each round is one enumeration per vertex, $\Theta(n + m)$ in total.

## References
