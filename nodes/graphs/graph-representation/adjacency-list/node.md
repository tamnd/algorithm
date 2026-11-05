---
tag: 3JK4BH
kind: data-structure
slug: adjacency-list
name: Adjacency list
aliases:
- adjacency lists
- incidence lists
area: graphs/graph-representation
level: intro
summary: Array indexed by vertex, each entry listing that vertex's neighbours; space Θ(V+E).
implements: [graph]
prereqs: [graph, directed-graph, dynamic-array]
see_also: [adjacency-matrix, edge-list, compressed-sparse-row, hash-based-adjacency, incidence-list, sparse-graph, transpose-graph, breadth-first-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), the adjacency-list representation, its Θ(V + E) memory and the sum of the list lengths
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the adjacency-lists data structure built from Bag objects, and Section 4.2 (Directed graphs)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 3, Section 3.3 (Implementing graph traversal using queues and stacks), the part on representing graphs
  - paper: doi:10.1137/0201010
    title: Robert Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 1972
    locator: pages 146 to 160, the linear-time algorithms on graphs given by adjacency lists
---

An adjacency list stores a [graph](/graph/) with vertices $0, \ldots, n-1$ as an array $\mathit{Adj}$ of $n$ lists, in which $\mathit{Adj}[u]$ holds the neighbours of $u$. It uses $\Theta(n + m)$ space for $m$ [edges](/edge/), lists the neighbours of $u$ in $\Theta(d(u))$ time, and adds an edge in $O(1)$ time. The [adjacency query](/adjacency-query/) "is $(u, v)$ an edge?" costs $O(d(u))$, because it scans a list. This is the standard representation for a [sparse graph](/sparse-graph/), and it is the one that makes [breadth-first search](/breadth-first-search/) and [depth-first search](/depth-first-search/) run in linear time $\Theta(n + m)$.

## In plain words

Give each vertex a list, and write in it the vertices it has an edge to. For a graph without arrows, each edge goes in two lists, one at each end. For a graph with arrows, the edge from $u$ to $v$ goes only in the list of $u$.

The memory you use is one list per vertex plus one entry per edge end, so a graph with few edges takes little room. To visit all neighbours of a vertex, you read its list, and you never look at the vertices that are not neighbours. The price is the yes-or-no question about one pair: to find out if $v$ is a neighbour of $u$, you must read through the list of $u$.

## The abstract type

The adjacency list implements the [graph](/graph/) type over the vertex set $V = \{0, \ldots, n-1\}$: `adjacent(G, u, v)`, `neighbors(G, u)`, `add-edge(G, u, v)`, `remove-edge(G, u, v)`, `add-vertex(G)`, `degree(G, u)` and `edges(G)`. It stores a [directed graph](/directed-graph/), with $E \subseteq V \times V$ and self-loops allowed, or a simple [undirected graph](/undirected-graph/), with edges $\{u, v\}$ and $u \ne v$. For a [multigraph](/multigraph/), the same layout with repeated entries works, as the variants below explain. For a [weighted graph](/weighted-graph/), each entry is a pair $(v, w(u, v))$.

## Representation

The structure has the number $n$, a flag that says whether the graph is directed, and an array $\mathit{Adj}[0 \ldots n-1]$ of lists. Here each list is a [dynamic array](/dynamic-array/), so the entries are contiguous; CLRS uses [linked lists](/linked-list/), which give the same bounds. The order of the entries in a list carries no meaning.

**Invariant (L).**

- (L1) No list holds the same vertex twice.
- (L2) If the graph is undirected, then $v \in \mathit{Adj}[u]$ if and only if $u \in \mathit{Adj}[v]$, and $u \notin \mathit{Adj}[u]$.

The graph it stands for has the edges $(u, v)$ with $v \in \mathit{Adj}[u]$ in the directed case, and the edges $\{u, v\}$ with $v \in \mathit{Adj}[u]$ in the undirected case. So the total length of the lists is $m$ for a directed graph and $2m$ for an undirected graph, by the [handshake lemma](/handshake-lemma/), and the space is $n + m$ or $n + 2m$ list entries and headers, which is $\Theta(n + m)$.

## Operations

```pseudo id=main
NEW(n, directed)
L1  Adj[v] ← an empty list, for each v in 0 … n − 1

ADD-EDGE(G, u, v)                ▷ requires the edge absent; for undirected, u ≠ v
L2  append v to Adj[u]
L3  if not directed then append u to Adj[v]

REMOVE-EDGE(G, u, v)
L4  DELETE(Adj[u], v)
L5  if not directed then DELETE(Adj[v], u)

DELETE(L, x)                     ▷ removes x from the unordered list L
L6  find i with L[i] = x; if there is none, return
L7  L[i] ← L[last]
L8  remove the last entry of L

ADJACENT(G, u, v)
L9  return true if some entry of Adj[u] is v, else false

NEIGHBORS(G, u)
L10 for each v in Adj[u] do output v

DEGREE(G, u)                     ▷ out-degree for a directed graph
L11 return the length of Adj[u]

ADD-VERTEX(G)
L12 append an empty list to Adj
L13 n ← n + 1; return n − 1
```

**New** (line L1) makes $n$ empty lists in $\Theta(n)$ time.

**Add-edge** (lines L2 and L3) appends one entry, or two for an undirected graph, in $O(1)$ amortized time with dynamic arrays and $O(1)$ worst-case time with linked lists. It does not test whether the edge is already there, since that test costs $O(d(u))$. So the caller must know that the edge is absent, or (L1) breaks and the list holds a parallel edge. A builder that reads a list of distinct edges has this guarantee for free. To add an edge only when it is absent, call ADJACENT first, for a total of $O(d(u))$.

**Remove-edge** (lines L4 to L8) scans for $v$ in $\mathit{Adj}[u]$, moves the last entry into its place, and drops the last entry. This takes $O(d(u))$ time in the directed case and $O(d(u) + d(v))$ in the undirected case. The move in line L7 is why the order of a list carries no meaning.

**Adjacent** (line L9) scans $\mathit{Adj}[u]$ in $O(d(u))$ time. For an undirected graph, scanning the shorter of $\mathit{Adj}[u]$ and $\mathit{Adj}[v]$ gives $O(\min(d(u), d(v)))$.

**Neighbors and degree** (lines L10 and L11) take $\Theta(d(u))$ and $O(1)$ time. This is the main strength of the structure: the cost of a scan is the size of its output.

**Add-vertex** (lines L12 and L13) appends one empty list, in $O(1)$ amortized time. Removing a vertex $v$ must also remove $v$ from the lists of its neighbours, in $O(\sum_{u \in N(v)} d(u))$ time for an undirected graph; for a directed graph, the in-neighbours of $v$ are not known, and finding them takes $\Theta(n + m)$.

## Example

Take an undirected graph on $V = \{0, 1, 2, 3\}$ and the same operations as on the [adjacency matrix](/adjacency-matrix/) page. The table shows the lists $\mathit{Adj}[0], \ldots, \mathit{Adj}[3]$ after each step.

| step | operation | result | lists |
|---|---|---|---|
| 1 | NEW(4) | | [ ] [ ] [ ] [ ] |
| 2 | ADD-EDGE(0, 1) | | [1] [0] [ ] [ ] |
| 3 | ADD-EDGE(1, 2) | | [1] [0, 2] [1] [ ] |
| 4 | ADD-EDGE(2, 0) | | [1, 2] [0, 2] [1, 0] [ ] |
| 5 | ADD-EDGE(3, 1) | | [1, 2] [0, 2, 3] [1, 0] [1] |
| 6 | ADJACENT(0, 2) | true, after 2 reads | unchanged |
| 7 | ADJACENT(0, 3) | false, after 2 reads | unchanged |
| 8 | NEIGHBORS(1) | 0, 2, 3 | unchanged |
| 9 | DEGREE(1) | 3 | unchanged |
| 10 | REMOVE-EDGE(1, 0) | | [2] [3, 2] [1, 0] [1] |
| 11 | ADD-VERTEX | 4 | [2] [3, 2] [1, 0] [1] [ ] |

After step 5 the lists hold $8 = 2m$ entries for the $m = 4$ edges. In step 10, DELETE finds 0 at index 0 of $\mathit{Adj}[1]$ and moves the last entry 3 into its place, so $\mathit{Adj}[1]$ becomes [3, 2]; it does the same for 1 in $\mathit{Adj}[0]$, which becomes [2]. The matrix of the same graph has 16 cells; the lists have 4 headers and 8 entries.

For the directed graph on $\{0, \ldots, 4\}$ with the edges $(0,1), (0,2), (1,2), (2,3), (3,1), (3,4)$, the out-lists are [1, 2], [2], [3], [1, 4], [ ], with $6 = m$ entries. One pass over them builds the lists of the [transpose graph](/transpose-graph/), [ ], [0, 3], [0, 1], [2], [3], which are the in-lists, in $\Theta(n + m)$ time.

## Correctness

The structure is correct when, after each operation, the edge set stored by the lists is the edge set that the graph type prescribes and (L) holds. NEW gives empty lists, so no edges, and (L) holds trivially. ADD-EDGE on an absent edge adds $v$ to $\mathit{Adj}[u]$, and $u$ to $\mathit{Adj}[v]$ in the undirected case, so the stored set gains exactly that edge, and since the edge was absent, no list gets a repeated entry. DELETE removes the single copy of $x$ from $L$, which by (L1) is its only copy, and keeps the other entries as a set, so REMOVE-EDGE takes away exactly the edge and keeps (L2). The queries read the list that defines the neighbours of $u$, and DEGREE returns its length, which by (L1) is the number of distinct neighbours. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $d(u)$ be the degree of $u$, or its out-degree for a directed graph. Times for dynamic arrays are amortized where marked.

| operation | time | notes |
|---|---|---|
| new graph with $n$ vertices | $\Theta(n)$ | |
| build from $m$ distinct edges | $\Theta(n + m)$ | one ADD-EDGE per edge |
| adjacent$(u, v)$ | $O(d(u))$ | $O(\min(d(u), d(v)))$ when undirected |
| neighbors$(u)$ | $\Theta(d(u))$ | |
| degree$(u)$ | $O(1)$ | |
| in-neighbors$(v)$, directed | $\Theta(n + m)$ | or $\Theta(d^-(v))$ with in-lists as well |
| add-edge, edge known absent | $O(1)$ amortized | |
| add-edge if absent | $O(d(u))$ | |
| remove-edge | $O(d(u))$, or $O(d(u) + d(v))$ undirected | |
| add-vertex | $O(1)$ amortized | |
| list all edges | $\Theta(n + m)$ | |
| transpose | $\Theta(n + m)$ | |
| space | $n$ lists and $m$ or $2m$ entries | $\Theta(n + m)$ |

**Whole-graph algorithms.** An algorithm that calls neighbors once for each vertex reads $\sum_u d(u) = 2m$ entries (undirected) or $m$ entries (directed), plus $n$ list headers, so it takes $\Theta(n + m)$ time. This is the bound of [BFS](/breadth-first-search/), [DFS](/depth-first-search/), [topological sort](/topological-sort/), [strongly connected components](/strongly-connected-components/) and many others. On an [adjacency matrix](/adjacency-matrix/) the same algorithms take $\Theta(n^2)$, which is worse by a factor of $n$ when $m = O(n)$ and equal when $m = \Theta(n^2)$.

**Memory in words.** With 32-bit vertex numbers, the entries of an undirected graph take $8m$ bytes. Dynamic arrays add a header and spare capacity per vertex, which is at most a factor 2 on the entries. Linked lists add a pointer per entry, which doubles or triples the size and scatters the entries in memory. The [compressed sparse row](/compressed-sparse-row/) format packs all lists into one array of $m$ or $2m$ entries with $n + 1$ offsets, at the cost of making the graph static.

## Variants

- **Linked lists.** CLRS uses one [linked list](/linked-list/) per vertex. Inserting at the head is $O(1)$ in the worst case, not only amortized, and a pointer to the entry deletes it in $O(1)$.
- **Sorted lists.** With each list sorted, ADJACENT takes $O(\log d(u))$ by binary search, and the neighbour sets of two vertices are intersected by a merge in $O(d(u) + d(v))$ time, as in [triangle counting](/triangle-counting/). ADD-EDGE then costs $O(d(u))$ to keep the order.
- **Weighted lists.** Each entry is a pair $(v, w)$. [Dijkstra's algorithm](/dijkstra/) and [Prim's algorithm](/prim/) read the weight together with the neighbour.
- **Out-lists and in-lists.** A directed graph often keeps both $\mathit{Adj}$ and the lists of its [transpose](/transpose-graph/). This doubles the space and makes in-neighbours cost $\Theta(d^-(v))$.
- **Incidence lists.** Each entry holds an edge number $e$ in place of a neighbour, and an edge array gives the two ends and the weight of $e$. This stores [multigraphs](/multigraph/) with parallel edges and loops, lets each undirected edge find its twin entry, and so removes an edge in $O(1)$ time with stored positions. See [incidence list](/incidence-list/).
- **Hash sets.** Replacing each list by a [hash table](/hash-table/) gives $O(1)$ expected ADJACENT, ADD-EDGE with a duplicate test, and REMOVE-EDGE. See [hash-based adjacency](/hash-based-adjacency/).
- **Packed arrays.** [Compressed sparse row](/compressed-sparse-row/) and the [forward star](/forward-star/) store the lists of a static graph in one array.

## When to use it

Use an adjacency list for a sparse graph, and for each algorithm that works by walking from vertices to their neighbours: traversals, shortest paths, spanning trees, flows and connectivity. It is the default representation in most textbooks and libraries. Use an [adjacency matrix](/adjacency-matrix/) when the graph is dense or when the algorithm asks about arbitrary pairs in its inner loop. Use [hash-based adjacency](/hash-based-adjacency/) when you need both fast pair queries and $\Theta(n + m)$ space. Use [compressed sparse row](/compressed-sparse-row/) when the graph does not change and speed or memory matters.

## Pitfalls

- **Duplicate entries.** ADD-EDGE does not check for the edge. Reading an input that lists an undirected edge as both $u\,v$ and $v\,u$ adds each edge twice, so degrees double and a later REMOVE-EDGE removes only one copy. Remove repeats in the input, or test before adding.
- **One end only.** For an undirected graph, forgetting line L3 gives a directed graph, and a search from $v$ misses the edge.
- **Pair queries in an inner loop.** An algorithm that calls ADJACENT for each pair of neighbours of each vertex costs $\sum_u d(u)^3$ on lists. Mark the neighbours of $u$ in a Boolean array first, then each query is $O(1)$, or use sorted lists or hash sets.
- **Changing a list while scanning it.** REMOVE-EDGE moves the last entry into the hole (line L7). A loop over $\mathit{Adj}[u]$ that removes edges at $u$ will then skip the moved entry. Collect the edges first, then remove them.
- **Directed in-neighbours.** The out-lists alone do not give the in-neighbours of a vertex. An algorithm such as Kosaraju's [strongly connected components](/strongly-connected-components/) needs the transpose, which must be built.
- **Object overhead.** In languages with boxed integers, such as Python, a list of lists costs tens of bytes per entry. For a large graph use arrays of machine integers or the [compressed sparse row](/compressed-sparse-row/) format.

## Implementations

The Python class keeps a list of $n$ Python lists and a flag for directed graphs. It follows the main block line by line; `add_edge` assumes that the edge is absent, and `add_edge_if_absent` tests first. `check_invariant` tests (L1) and (L2).

## History

Adjacency lists became the standard representation of graphs for algorithms through the work of Hopcroft and Tarjan in the early 1970s. Tarjan's 1972 paper on depth-first search shows that, with the graph given by adjacency lists, depth-first search and the algorithms built on it, such as strongly connected components and biconnected components, run in time linear in $n + m$. CLRS (Section 20.1) and Sedgewick and Wayne (Section 4.1) present the list and the matrix as the two standard choices.

## References
