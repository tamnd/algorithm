---
tag: SX5BWH
kind: data-structure
slug: edge-list
name: Edge list
aliases:
- edge array
- edge set
area: graphs/graph-representation
level: intro
summary: Array of all edges as vertex pairs (with weights if any); space Θ(E).
implements: [graph]
prereqs: [graph, edge, dynamic-array]
see_also: [adjacency-list, adjacency-matrix, compressed-sparse-row, forward-star, kruskal, bellman-ford, incidence-list, counting-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 21.2 (The algorithms of Kruskal and Prim), Kruskal's algorithm that sorts the edges by weight; Section 22.1 (The Bellman-Ford algorithm), the passes over all edges
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the representation alternatives, with the list of edges and its costs
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows
    locator: Section 2.3 (Network representations), the arc list and the forward and reverse star built from it
---

An edge list stores a [graph](/graph/) as its number of vertices $n$ and one array of its $m$ [edges](/edge/), each a pair $(u, v)$ of vertex numbers, with a weight when the graph is weighted. It uses $\Theta(m)$ space beyond the number $n$ and adds an edge in $O(1)$ time, but each question about one vertex or one pair needs a scan of all $m$ edges. It is the usual format of graph files and the natural input of algorithms that treat the edges as a set, such as [Kruskal's algorithm](/kruskal/), which sorts them, and [Bellman-Ford](/bellman-ford/), which relaxes each of them in turn. One [counting sort](/counting-sort/) by the first end turns it into an [adjacency list](/adjacency-list/) or a [compressed sparse row](/compressed-sparse-row/) array in $\Theta(n + m)$ time.

## In plain words

Write down every edge of the graph as a pair of vertex numbers, one pair per line, and keep the number of vertices. That is all. A road map stored like this is a list of roads, each with its two end towns and its length.

The list is as small as a graph can be stored without compression, and it is easy to read, write, sort and split. Adding a road is one more line. But to find the roads at one town, or to check whether two towns have a road between them, you must read the whole list. So most programs read an edge list from a file and then build a better structure from it.

## The abstract type

The edge list implements the [graph](/graph/) type over $V = \{0, \ldots, n-1\}$: `adjacent(G, u, v)`, `neighbors(G, u)`, `add-edge(G, u, v)`, `remove-edge(G, u, v)`, `add-vertex(G)`, `degree(G, u)` and `edges(G)`. It stores a [directed graph](/directed-graph/), where the pair $(u, v)$ is the edge from $u$ to $v$ and a loop $(v, v)$ is allowed, or a simple [undirected graph](/undirected-graph/), where the pair $(u, v)$ with $u \ne v$ stands for the edge $\{u, v\}$ and is stored once, in either order. With a third field $w$ per entry it stores a [weighted graph](/weighted-graph/). With repeated entries, which the structure does not forbid, it stores a [multigraph](/multigraph/), and each entry is then one edge with its own identity, its index in the array.

## Representation

The structure has the number $n$, a flag that says whether the graph is directed, and a [dynamic array](/dynamic-array/) $L[0 \ldots m-1]$ of pairs. Two pairs *match* when they stand for the same edge: $(x, y)$ matches $(u, v)$ when $(x, y) = (u, v)$, or, for an undirected graph, when $(x, y) = (v, u)$.

**Invariant (E).**

- (E1) Each entry $(x, y)$ has $0 \le x, y < n$, and $x \ne y$ if the graph is undirected.
- (E2) No two entries of $L$ match.

The graph it stands for has the edges $(x, y)$, or $\{x, y\}$, of the entries of $L$, so $|L| = m$. The space is $2m$ vertex numbers, or $3m$ fields with weights, plus a constant.

## Operations

```pseudo id=main
NEW(n, directed)
L1  L ← an empty list

ADD-EDGE(G, u, v)                ▷ requires the edge absent; for undirected, u ≠ v
L2  append (u, v) to L

REMOVE-EDGE(G, u, v)
L3  find i with MATCH(L[i], u, v); if there is none, return
L4  L[i] ← L[last]
L5  remove the last entry of L

MATCH((x, y), u, v)
L6  return (x, y) = (u, v) or (not directed and (x, y) = (v, u))

ADJACENT(G, u, v)
L7  return true if MATCH(L[i], u, v) for some i, else false

NEIGHBORS(G, u)                  ▷ out-neighbours for a directed graph
L8  for each (x, y) in L do
L9      if x = u then output y
L10     else if not directed and y = u then output x

DEGREE(G, u)
L11 return the number of outputs of NEIGHBORS(G, u)

ADD-VERTEX(G)
L12 n ← n + 1; return n − 1
```

**Add-edge** (line L2) appends one pair in $O(1)$ amortized time. Like the [adjacency list](/adjacency-list/), it does not test for a duplicate, which would cost $O(m)$, so the caller must know that the edge is absent.

**Remove-edge** (lines L3 to L5) scans for a matching entry, moves the last entry into its place, and drops the last entry. The scan takes $O(m)$ time. If the caller holds the index $i$ of the edge, for example because it got the edge from a scan, lines L4 and L5 alone remove it in $O(1)$ time.

**Adjacent, neighbors and degree** (lines L7 to L11) scan all of $L$, in $\Theta(m)$ time for neighbors and degree and $O(m)$ for adjacent. A loop $(u, u)$ in a directed graph is output once by line L9, and line L10 is not reached for it.

**Add-vertex** (line L12) only increases $n$, in $O(1)$ time, since vertices that have no edges take no space in $L$. Removing a vertex must remove its edges, in $\Theta(m)$ time.

**Building other representations.** Sorting $L$ by the first end, with ties in any order, groups the out-edges of each vertex together. A [counting sort](/counting-sort/) on keys $0, \ldots, n-1$ does it in $\Theta(n + m)$ time, and the counts are the degrees, whose [prefix sums](/prefix-sums/) are the offsets of the [compressed sparse row](/compressed-sparse-row/) format and of the [forward star](/forward-star/). For an undirected graph, put each edge in both orders first. Appending each pair to the lists of its ends builds an [adjacency list](/adjacency-list/) in the same time bound.

## Example

Take an undirected graph on $V = \{0, 1, 2, 3\}$ and the same operations as on the [adjacency matrix](/adjacency-matrix/) page.

| step | operation | result | $L$ |
|---|---|---|---|
| 1 | NEW(4) | | [ ] |
| 2 | ADD-EDGE(0, 1) | | [(0,1)] |
| 3 | ADD-EDGE(1, 2) | | [(0,1), (1,2)] |
| 4 | ADD-EDGE(2, 0) | | [(0,1), (1,2), (2,0)] |
| 5 | ADD-EDGE(3, 1) | | [(0,1), (1,2), (2,0), (3,1)] |
| 6 | ADJACENT(0, 2) | true, after 3 reads | unchanged |
| 7 | ADJACENT(0, 3) | false, after 4 reads | unchanged |
| 8 | NEIGHBORS(1) | 0, 2, 3 | unchanged |
| 9 | DEGREE(1) | 3 | unchanged |
| 10 | REMOVE-EDGE(1, 0) | | [(3,1), (1,2), (2,0)] |
| 11 | ADD-VERTEX | 4 | unchanged, with $n = 5$ |

In step 6 the third entry $(2, 0)$ matches $(0, 2)$ because the graph is undirected. In step 8 the scan reads all four entries and outputs 0 from $(0,1)$ by line L10, 2 from $(1,2)$ by line L9, and 3 from $(3,1)$ by line L10. In step 10 the entry $(0,1)$ at index 0 matches $(1, 0)$, and the last entry $(3,1)$ takes its place.

The directed graph on $\{0, \ldots, 4\}$ with the edges $(0,1), (0,2), (1,2), (2,3), (3,1), (3,4)$ is the edge list itself. Counting the first ends gives the out-degrees $2, 1, 1, 2, 0$, their prefix sums give the offsets $0, 2, 3, 4, 6, 6$, and the list is already sorted by first end, so it is the edge array of the [compressed sparse row](/compressed-sparse-row/) form with the heads $1, 2, 2, 3, 1, 4$.

## Correctness

The structure is correct when, after each operation, the edges of the entries of $L$ form the edge set that the graph type prescribes and (E) holds. NEW gives the empty list. ADD-EDGE on an absent edge appends an entry that matches no other entry, so the set gains exactly that edge and (E2) holds. REMOVE-EDGE finds the one matching entry, which is unique by (E2), and the move of the last entry keeps all other entries, so the set loses exactly that edge. MATCH holds exactly when two entries stand for the same edge, so ADJACENT answers for the stored set, and NEIGHBORS outputs the other end of each entry at $u$, once per entry, which by (E2) is once per neighbour. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| new graph with $n$ vertices | $O(1)$ | $n$ is a number only |
| adjacent$(u, v)$ | $O(m)$ | one scan |
| neighbors$(u)$, degree$(u)$ | $\Theta(m)$ | one scan |
| add-edge, edge known absent | $O(1)$ amortized | |
| add-edge if absent | $O(m)$ | |
| remove-edge | $O(m)$, or $O(1)$ given the index | |
| add-vertex | $O(1)$ | |
| list all edges | $\Theta(m)$ | the structure itself |
| sort by weight | $O(m \log m)$ | for Kruskal |
| convert to adjacency list or CSR | $\Theta(n + m)$ | counting sort by first end |
| space | $2m$ vertex numbers, $3m$ fields with weights | $\Theta(m)$ beyond $n$ |

**Whole-graph algorithms.** An algorithm that only needs to see each edge, in any order, runs as fast on an edge list as on any other structure. [Bellman-Ford](/bellman-ford/) makes $n - 1$ passes over $L$, in $\Theta(nm)$ time; [Kruskal](/kruskal/) sorts $L$ and then scans it once with a [disjoint-set](/disjoint-set/) structure, in $O(m \log m)$ time; [Karger's minimum cut](/karger-min-cut/) picks random entries of $L$. An algorithm that walks from a vertex to its neighbours, such as [BFS](/breadth-first-search/), would take $\Theta(nm)$ time on an edge list, so it first builds an adjacency list in $\Theta(n + m)$.

## Variants

- **Weighted edge list.** Each entry is a triple $(u, v, w)$. This is the input of [Kruskal](/kruskal/) and of [Bellman-Ford](/bellman-ford/).
- **Two parallel arrays.** Store the first ends in one array and the second ends in another, the *structure of arrays* layout. Sparse matrix libraries call this the coordinate format of a [sparse matrix](/sparse-matrix/), with a third array of values.
- **Sorted edge list.** Sorted by $(u, v)$, the list answers ADJACENT in $O(\log m)$ time by binary search, and the out-edges of $u$ form one block that binary search finds in $O(\log m)$ time. Adding the block starts as an array of $n + 1$ offsets gives the [forward star](/forward-star/) and the [compressed sparse row](/compressed-sparse-row/) format.
- **Edge array with incidence lists.** Keep the edge array as the home of each edge, and give each vertex a list of indices into it. This is the [incidence list](/incidence-list/), which stores [multigraphs](/multigraph/) and edges with many attributes.
- **Streams.** A graph too large for memory is read as a stream of edges in one or a few passes, and each pass sees the edges in the order of the file.

## When to use it

Use an edge list to read and write graphs, to move them between programs, and as the input of algorithms that process all edges without regard to their ends, such as [Kruskal](/kruskal/), [Bellman-Ford](/bellman-ford/) and random edge sampling. It is also the right structure when edges have many attributes and the graph is small. For each algorithm that asks about the neighbours of a vertex, convert it to an [adjacency list](/adjacency-list/) or a [compressed sparse row](/compressed-sparse-row/) array first.

## Pitfalls

- **Both orders of an undirected edge.** Many files list each undirected edge twice, as $u\,v$ and $v\,u$. Read as an edge list of an undirected graph, this breaks (E2), doubles the degrees, and makes Kruskal see each edge twice. Keep the pairs with $u < v$, or keep the file's form and treat it as a directed graph.
- **Isolated vertices.** A vertex with no edges does not appear in $L$. If $n$ is taken as one more than the largest vertex number in the file, the last isolated vertices are lost. Store $n$ explicitly.
- **Neighbour scans in a loop.** Calling NEIGHBORS for each vertex costs $\Theta(nm)$ in total. Build an adjacency list first.
- **Indices after removal.** REMOVE-EDGE moves the last entry into the hole, so the index of that entry changes. Code that keeps edge indices, as incidence lists do, must update the moved one.
- **Vertex names.** Files often name vertices by strings or by large sparse numbers. Map them to $0, \ldots, n-1$ with a [hash table](/hash-table/) before building any array-based structure.

## Implementations

The Python class keeps a Python list of tuples and a flag for directed graphs, and follows the main block line by line. `to_adjacency_lists` builds the lists of an [adjacency list](/adjacency-list/) in one pass, and `check_invariant` tests (E1) and (E2).

## History

The list of edges is the oldest and simplest way to write a graph down, since a graph is by definition a set of vertices and a set of edges. Network flow texts such as Ahuja, Magnanti and Orlin (Section 2.3) call it the arc list and build the forward and reverse star from it by sorting. Kruskal's 1956 minimum spanning tree algorithm and the Bellman-Ford algorithm of the 1950s use the edges in exactly this form, as CLRS (Sections 21.2 and 22.1) presents them.

## References
