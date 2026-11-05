---
tag: Q90FNQ
kind: problem
slug: transpose-graph
name: Graph transposition
aliases:
- graph reversal
- transpose
area: graphs/graph-representation
level: intro
summary: Build the graph with every edge reversed, in O(V+E) time.
prereqs: [directed-graph, adjacency-list, adjacency-matrix]
see_also: [graph-transpose, kosaraju-sharir, strongly-connected-components, compressed-sparse-row, compressed-sparse-column, counting-sort, direction-optimizing-bfs, bidirectional-dijkstra]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1, Exercise 20.1-3 (computing the transpose from adjacency lists and from an adjacency matrix); Section 20.5 (Strongly connected components), the transpose G^T and its use
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2 (Directed graphs), the reverse() method of the Digraph API and its use in the Kosaraju-Sharir algorithm
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox, Springer, 2008
    locator: Chapter 8 (Graph representation), adjacency arrays and the construction of the reverse edges
---

Graph transposition is the problem of building, from a [directed graph](/directed-graph/) $G$, the graph $G^T$ that has the same [vertices](/vertex/) and every [edge](/edge/) reversed. The out-neighbours of $v$ in $G^T$ are the in-neighbours of $v$ in $G$, so transposing once makes "who points to $v$?" as cheap as "where does $v$ point?". It is a step of the [Kosaraju-Sharir](/kosaraju-sharir/) algorithm for [strongly connected components](/strongly-connected-components/), of backward search and of pull-style graph processing. From [adjacency lists](/adjacency-list/) it takes $\Theta(n + m)$ time, which is optimal; from an [adjacency matrix](/adjacency-matrix/) it is the matrix transpose, $\Theta(n^2)$. The object $G^T$ itself is described on the [graph transpose](/graph-transpose/) page.

## In plain words

A one-way street map tells you, for each crossing, where you can drive next. Sometimes you need the other question: from which crossings can you drive here? To answer it fast, make a second map with every arrow turned around.

To make that map, go through the first map once. For each arrow from A to B, write "A" in the list of B. Every arrow is read once and written once, so the work is the number of arrows plus the number of crossings.

## Definition

**Input.** A directed graph $G = (V, E)$, $E \subseteq V \times V$, with $V = \{0, \ldots, n - 1\}$ and $m = |E|$, in a given representation. [Self-loops](/self-loop/) are allowed. For a multigraph, $E$ is a list in which an edge may repeat.

**Output.** The **transpose** $G^T = (V, E^T)$ with

$$E^T = \{(v, u) : (u, v) \in E\},$$

in the same representation. In matrix terms, the adjacency matrix of $G^T$ is $A^T$, which gives the name. Each self-loop stays where it is, and an edge weight moves with its edge.

**Facts.** $(G^T)^T = G$. $d^+_{G^T}(v) = d^-_G(v)$ and $d^-_{G^T}(v) = d^+_G(v)$. A path $u \to \cdots \to v$ in $G$ is a path $v \to \cdots \to u$ in $G^T$, so $G$ and $G^T$ have the same strongly connected components. For an [undirected graph](/undirected-graph/), stored as the directed version, $G^T = G$.

## Variants

- **In place for a matrix.** Swap $A[u, v]$ and $A[v, u]$ for $u < v$; $\binom{n}{2}$ swaps and $O(1)$ extra space.
- **Static CSR.** Building the [compressed sparse column](/compressed-sparse-column/) form of a matrix stored as [CSR](/compressed-sparse-row/) is the same problem, and it is solved by [counting sort](/counting-sort/) on the heads.
- **Sorted lists.** Produce each list of $G^T$ in increasing order. The scan below gives this for free if it visits the tails in increasing order.
- **Keep both.** Store $G$ and $G^T$ together, so each edge is in an out-list and in an in-list. This doubles the space and makes each edge insertion touch two lists; see [incidence list](/incidence-list/).
- **Implicit transpose.** For a graph given by a successor function, no transpose can be built without enumerating the graph; a backward search needs a predecessor function.

## Examples

Let $V = \{0, 1, 2, 3\}$ and $E = \{(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)\}$.

| vertex | $\text{Adj}_G$ | $\text{Adj}_{G^T}$ |
|---|---|---|
| 0 | $[1, 2]$ | $[2]$ |
| 1 | $[2]$ | $[0]$ |
| 2 | $[0, 3]$ | $[0, 1]$ |
| 3 | $[3]$ | $[2, 3]$ |

Both have 6 entries. The lists of $G^T$ come out sorted because the scan visits $u = 0, 1, 2, 3$ in order: from $u = 0$ it appends 0 to the lists of 1 and 2, from $u = 1$ it appends 1 to the list of 2, from $u = 2$ it appends 2 to the lists of 0 and 3, and from $u = 3$ it appends 3 to the list of 3. The loop $(3, 3)$ is unchanged. The strongly connected components $\{0, 1, 2\}$ and $\{3\}$ are the same in both graphs.

**In CSR form.** $G$ has $\text{off} = [0, 2, 3, 5, 6]$ and $\text{adj} = [1, 2, 2, 0, 3, 3]$. The in-degrees are $1, 1, 2, 2$, so the prefix sums give $\text{off}^T = [0, 1, 2, 4, 6]$, and placing each tail at the next free slot of its head gives $\text{adj}^T = [2, 0, 0, 1, 2, 3]$.

## Known algorithms

- **List scan.** Make $n$ empty lists. For each $u$ in order and each $v \in \text{Adj}[u]$, append $u$ to $\text{Adj}^T[v]$. Each of the $m$ entries costs $O(1)$, and creating the lists costs $\Theta(n)$, so the time is $\Theta(n + m)$, and the output takes $\Theta(n + m)$ space. This is the answer to CLRS Exercise 20.1-3.
- **Counting sort into CSR.** (1) Count the in-degree of each vertex in one pass. (2) Take [prefix sums](/prefix-sums/) to get $\text{off}^T$. (3) In a second pass, put each tail $u$ at position $\text{next}[v]$ and increment it. The time is $\Theta(n + m)$ and the output is two flat arrays of $n + 1$ and $m$ integers, with no per-list overhead. It is a stable [counting sort](/counting-sort/) of the edges by head.
- **Matrix transpose.** $\Theta(n^2)$ time, in place. A blocked or cache-oblivious order of the swaps cuts the number of cache misses, but not the time.
- **Edge list.** Swap the two ends of each pair: $\Theta(m)$ time, in place.

## Bounds

**Lower bound.** Any algorithm must write the $m$ entries of the output and initialise its $n$ lists, so it needs $\Omega(n + m)$ time for list forms. The list scan and the counting sort match it. For a matrix, the output has $n^2$ entries, and the $n(n-1)$ entries off the diagonal may each change, so $\Omega(n^2)$ writes are needed in the worst case.

**Space.** The list forms need $\Theta(n + m)$ extra words for the new graph, because the in-degrees differ from the out-degrees and every list can change size. The usual practice is to build the new graph next to the old one.

**Cost table.**

| input form | time | extra space |
|---|---|---|
| adjacency list | $\Theta(n + m)$ | $\Theta(n + m)$ |
| CSR | $\Theta(n + m)$ | $\Theta(n + m)$ |
| adjacency matrix | $\Theta(n^2)$ | $O(1)$, in place |
| edge list | $\Theta(m)$ | $O(1)$, in place |

## Reductions

- **In-neighbour enumeration to out-neighbour enumeration.** One transposition, $\Theta(n + m)$, then each [neighborhood enumeration](/neighborhood-enumeration/) of $N^-(v)$ costs $\Theta(1 + d^-(v))$ instead of a $\Theta(n + m)$ scan.
- **Reachability to $v$ to reachability from $v$.** The set of vertices that can reach $v$ in $G$ is the set reachable from $v$ in $G^T$, so one BFS on $G^T$ finds it.
- **Sparse matrix transpose.** Transposing a sparse matrix in CSR form is the same problem, with values carried along.

## Applications

- **Strongly connected components.** [Kosaraju-Sharir](/kosaraju-sharir/) runs DFS on $G$, then DFS on $G^T$ in decreasing order of finishing times. See [strongly connected components](/strongly-connected-components/).
- **Bidirectional search.** The backward half of [bidirectional Dijkstra](/bidirectional-dijkstra/) searches $G^T$ from the target.
- **Pull-style BFS.** [Direction-optimizing BFS](/direction-optimizing-bfs/) switches to the bottom-up step, in which each unvisited vertex scans its in-neighbours, so it keeps the transpose.
- **PageRank.** Each step sums over the in-neighbours of each vertex, which is a scan of $G^T$.

## References
