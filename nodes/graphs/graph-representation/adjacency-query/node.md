---
tag: CM0Y9G
kind: problem
slug: adjacency-query
name: Adjacency query
aliases:
- edge query
- edge existence query
area: graphs/graph-representation
level: intro
summary: Given two vertices, decide whether an edge joins them.
prereqs: [graph, adjacency-matrix, adjacency-list]
see_also: [adjacency-matrix, adjacency-list, hash-based-adjacency, bitset-adjacency-matrix, dictionary, fks-perfect-hashing, degeneracy, implicit-graph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), the cost of deciding whether (u, v) is an edge with adjacency lists and with an adjacency matrix
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the table of the costs of checking whether w is adjacent to v for each representation
  - paper: "Marek Chrobak and David Eppstein, Planar orientations with low out-degree and compaction of adjacency matrices, Theoretical Computer Science 86(2), 1991"
    locator: pages 243 to 266, the orientation of a planar graph with out-degree at most 5 and the adjacency test in O(1) time from O(n) space
  - paper: "Sampath Kannan, Moni Naor and Steven Rudich, Implicit representation of graphs, SIAM Journal on Discrete Mathematics 5(4), 1992"
    locator: pages 596 to 603, adjacency labels of O(log n) bits for trees and for graphs of bounded arboricity
---

The adjacency query asks, for a [graph](/graph/) $G$ and two vertices $u$ and $v$, whether $G$ has an [edge](/edge/) from $u$ to $v$. It is the basic membership question about the edge set, and its cost is the main difference between the representations of a graph: one cell read on an [adjacency matrix](/adjacency-matrix/), a scan of $d(u)$ entries on an [adjacency list](/adjacency-list/), and $O(1)$ expected time with [hash-based adjacency](/hash-based-adjacency/). Viewed as a data-structure problem, it asks for the least space that answers each query fast, and the answer is that $O(n + m)$ words and $O(1)$ worst-case time are enough for a static graph, by [perfect hashing](/fks-perfect-hashing/).

## In plain words

You have a graph and you want to know if two given vertices are joined by an edge. You will ask this question many times, for many pairs, so you may first put the graph into a structure that makes the answers fast.

A table with one cell per pair answers in one look, but it is large. A list of neighbours per vertex is small, but you may have to read a whole list. A hash table gets both: small size and fast answers. For special graphs, such as maps drawn on a plane, there are simple tricks that also answer in a fixed small number of steps.

## Definition

**Input.** A graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and $m = |E|$, given once, and then a sequence of query pairs $(u, v) \in V \times V$.

**Output.** For each query, the bit $[(u, v) \in E]$ if $G$ is directed, or $[\{u, v\} \in E]$ if $G$ is a simple undirected graph. A loop query $(v, v)$ on a simple undirected graph has the answer "no".

**Measure.** A solution is a representation of $G$, built in a preprocessing step, together with a query procedure. It is measured by its space in bits or in words of the [word RAM](/word-ram/), by its preprocessing time, and by its query time, in the worst case or in expectation over the random choices of the structure. In the [cell probe model](/cell-probe-model/), the query cost is the number of memory words read.

So the problem is the static [dictionary](/dictionary/) membership problem for a set of $m$ keys, the edges, from a universe of $n^2$ keys, the pairs of vertices. This view gives the bounds below.

## Variants

- **Static or dynamic.** In the dynamic version, edges are added and removed between the queries, and each update has its own cost.
- **Directed or undirected.** For an undirected graph the query is symmetric, so a structure may answer it from either end, for example from the end of smaller degree.
- **Weighted.** The query returns $w(u, v)$ or "no edge". Each structure below extends to this by storing the weight next to the entry.
- **Multigraph.** The query returns the number of parallel edges between $u$ and $v$, or the list of them.
- **Labeling schemes.** Each vertex gets a short label, and the query must be answered from the labels of $u$ and $v$ alone, without access to the graph. This is the setting of [implicit graphs](/implicit-graph/) in the sense of Kannan, Naor and Rudich.
- **Approximate.** A [Bloom filter](/bloom-filter/) on the edge set answers "no" correctly and answers "yes" wrongly with a small chosen probability, in less space than any exact structure.
- **Batch.** All queries are known in advance. Then sorting the queries with the edges answers $q$ queries in $O(n + m + q)$ time by a [radix sort](/radix-sort/) of all pairs.

## Examples

Take the undirected graph on $\{0, \ldots, 5\}$ with the edges $01, 02, 12, 13, 23, 34, 45$, so the degrees are $2, 3, 3, 3, 2, 1$. Built in this order, its adjacency lists are $[1, 2]$, $[0, 2, 3]$, $[0, 1, 3]$, $[1, 2, 4]$, $[3, 5]$, $[4]$.

| query | answer | matrix | list of $u$ | shorter list, ties to $u$ | sorted list of $u$ |
|---|---|---|---|---|---|
| $(1, 3)$ | yes | 1 read | 3 reads | 3 reads | 2 reads |
| $(0, 3)$ | no | 1 read | 2 reads | 2 reads | 2 reads |
| $(3, 4)$ | yes | 1 read | 3 reads | 1 read, in $[3, 5]$ | 2 reads |
| $(5, 0)$ | no | 1 read | 1 read | 1 read | 1 read |

A list of length $d$ is read in full for a "no" answer, and binary search reads at most $\lfloor \log_2 d \rfloor + 1$ entries.

**A low out-degree orientation.** The same graph has [degeneracy](/degeneracy/) 2: removing a vertex of least degree again and again gives the order $5, 4, 0, 1, 2, 3$, and each vertex has at most 2 neighbours later in the order. Orient each edge from the earlier end to the later end and keep only the out-lists: $\mathrm{Out}[5] = [4]$, $\mathrm{Out}[4] = [3]$, $\mathrm{Out}[0] = [1, 2]$, $\mathrm{Out}[1] = [2, 3]$, $\mathrm{Out}[2] = [3]$, $\mathrm{Out}[3] = [\,]$. Each edge is stored once, in 7 entries, and the query $(u, v)$ reads $\mathrm{Out}[u]$ and $\mathrm{Out}[v]$, at most $2 + 2 = 4$ entries. For $(3, 4)$ it finds 3 in $\mathrm{Out}[4]$.

## Known algorithms

| structure | space | query time | update time |
|---|---|---|---|
| [adjacency matrix](/adjacency-matrix/) | $n^2$ bits | $O(1)$ | $O(1)$ |
| [bitset adjacency matrix](/bitset-adjacency-matrix/) | $n \lceil n/w \rceil$ words | $O(1)$ | $O(1)$ |
| [adjacency list](/adjacency-list/), unsorted | $\Theta(n + m)$ words | $O(d(u))$, or $O(\min(d(u), d(v)))$ undirected | $O(1)$ add, $O(d)$ remove |
| sorted lists or [CSR](/compressed-sparse-row/) | $\Theta(n + m)$ words | $O(\log d(u))$ by [binary search](/binary-search/) | $O(d)$, or a rebuild |
| [edge list](/edge-list/), unsorted | $\Theta(m)$ words | $O(m)$ | $O(1)$ add |
| [hash-based adjacency](/hash-based-adjacency/) | $\Theta(n + m)$ words | $O(1)$ expected | $O(1)$ expected amortized |
| one hash table of all pairs | $\Theta(m)$ words | $O(1)$ expected | $O(1)$ expected amortized |
| [FKS perfect hashing](/fks-perfect-hashing/) of all pairs, static | $\Theta(m)$ words | $O(1)$ worst case | rebuild, $O(m)$ expected |
| [cuckoo hashing](/cuckoo-hashing/) of all pairs | $\Theta(m)$ words | $O(1)$ worst case | $O(1)$ expected amortized |
| out-lists of a degeneracy-$k$ orientation | $\Theta(n + m)$ words | $O(k)$ | static |

The orientation in the last row exists for each graph of [degeneracy](/degeneracy/) $k$ and is found in $O(n + m)$ time by repeatedly removing a vertex of least degree. [Planar graphs](/planar-graph/) have degeneracy at most 5, so they answer queries in $O(1)$ worst-case time from $O(n)$ words without hashing; Chrobak and Eppstein gave this result. Graphs of [arboricity](/arboricity/) $a$ have degeneracy at most $2a - 1$.

## Bounds

**Space.** There are $\binom{N}{m}$ graphs with $m$ edges on $n$ labelled vertices, where $N = \binom{n}{2}$ for undirected graphs, so any exact structure for all of them needs at least $\log_2 \binom{N}{m}$ bits on some graph. For $m \le N/2$ this is $m \log_2(N/m) + \Theta(m)$ bits. For the example graph, $\binom{15}{7} = 6435$, so 13 bits are needed, against the 15 cells of the triangular matrix. The matrix is within a constant factor of the bound only when $m = \Theta(n^2)$; lists and hash tables use $\Theta(m \log n)$ bits, which is within a constant factor of the bound when $m \le n^{2 - \varepsilon}$ for a fixed $\varepsilon > 0$.

**Time from one unsorted list.** If the structure gives only the unsorted list of $u$, then a correct "no" answer must read all $d(u)$ entries: an adversary places $v$ in any entry that was not read. With lists at both ends of an undirected graph, the same argument gives $\Omega(\min(d(u), d(v)))$ reads. With sorted lists and comparisons only, the [decision tree](/decision-tree-model/) bound gives $\Omega(\log d(u))$ comparisons.

**Time with hashing.** Since the problem is static membership, the FKS scheme answers in $O(1)$ worst-case probes from $O(m)$ words, which matches the trivial lower bound of one probe up to a constant. So, unlike many data-structure problems, the adjacency query has no trade-off between linear space and constant time; the open questions are about bits, constants and cache behaviour.

**Whole-matrix questions.** Answering one query is cheap, but deciding a property of the whole graph by queries alone may need many of them: by an [adversary argument](/adversary-argument/), deciding whether a graph given only by an adjacency oracle has any edge needs all $\binom{n}{2}$ queries. The [graph](/graph/) page gives the proof.

## Reductions

- **To set membership.** The query on $G$ is a membership query in the set $\{u n + v : (u, v) \in E\}$ of integers below $n^2$, so each [dictionary](/dictionary/) structure solves it. For an undirected graph, store the key of $(\min(u, v), \max(u, v))$.
- **From set membership.** Conversely, a set $S$ of integers below $n^2$ is the edge set of a directed graph on $n$ vertices, so lower bounds for membership in a universe of size $n^2$ apply.
- **Neighbourhood marking.** When all queries share the first vertex $u$, mark the neighbours of $u$ in a Boolean array of size $n$ in $O(d(u))$ time, and each query $(u, v)$ is then one array read. Many algorithms, such as [triangle counting](/triangle-counting/), use this to answer all queries of a vertex in $O(d(u))$ time in total from plain adjacency lists.

## Applications

- **Checking cliques and triangles.** [Triangle counting](/triangle-counting/) asks, for each pair of neighbours of a vertex, whether they are adjacent; [Bron-Kerbosch](/bron-kerbosch/) and checks of a [clique](/clique/) do the same.
- **Building a simple graph.** An insertion that must not create a parallel edge first asks the query, so the cost of building depends on it.
- **Dense algorithms.** [Floyd-Warshall](/floyd-warshall/) and the matrix methods for [transitive closure](/transitive-closure/) read each pair once.
- **Search in implicit graphs.** In an [implicit graph](/implicit-graph/), such as the move graph of a puzzle, the query is computed from the rule that defines the edges.

## References
