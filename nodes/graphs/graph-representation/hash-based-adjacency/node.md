---
tag: NZ1XVJ
kind: data-structure
slug: hash-based-adjacency
name: Hash-based adjacency
aliases:
- adjacency hash table
area: graphs/graph-representation
level: core
summary: Neighbour sets stored in hash tables for expected constant-time adjacency tests.
implements: [graph]
prereqs: [adjacency-list, hash-table]
see_also: [adjacency-list, adjacency-matrix, hash-table, universal-hashing, adjacency-query, dynamic-graph, load-factor, compressed-sparse-row]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 11 (Hash tables), the expected O(1) time of search, insert and delete with chaining and universal hashing; Section 20.1 (Representations of graphs), the exercise that replaces each adjacency list by a hash table
  - paper: "Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, Exploring network structure, dynamics, and function using NetworkX, Proceedings of the 7th Python in Science Conference (SciPy 2008)"
    locator: pages 11 to 15, the dictionary-of-dictionaries representation of graphs with arbitrary hashable nodes
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox
    locator: Chapter 8 (Graph representation), the comparison of edge sequences, adjacency arrays, adjacency lists and the adjacency matrix for dynamic graphs and edge queries
---

Hash-based adjacency stores a [graph](/graph/) as a [hash table](/hash-table/) that maps each vertex to a hash set of its neighbours. It keeps the $\Theta(n + m)$ space and the $\Theta(d(u))$ neighbour scan of the [adjacency list](/adjacency-list/), and it answers the [adjacency query](/adjacency-query/), adds an edge with a duplicate test and removes an edge in $O(1)$ expected time, as the [adjacency matrix](/adjacency-matrix/) does in the worst case. Since the vertices are keys of a hash table, they can be any hashable names, and a vertex is removed in time proportional to its degree. It is the default representation of general-purpose graph libraries such as NetworkX, at the cost of a constant factor in memory and speed over packed arrays.

## In plain words

Give each vertex a set of its neighbours, but keep each set in a hash table instead of a plain list. A hash table answers "is this item in the set?" in a few steps on average, however large the set is.

So the yes-or-no question about one pair is as fast as with a table of all pairs, but the memory is only one entry per edge end, as with lists. Adding an edge that is already there does nothing, and removing an edge is just as quick. The vertices can be named by words or other objects, since the outer table maps each name to its set. The price is that hash tables use more memory than plain arrays and scatter the items around memory.

## The abstract type

The structure implements the full [graph](/graph/) type: `adjacent`, `neighbors`, `degree`, `add-edge`, `remove-edge`, `add-vertex`, `remove-vertex` and `edges`, over a vertex set of any hashable keys. It stores a simple [undirected graph](/undirected-graph/), or a [directed graph](/directed-graph/) with self-loops allowed, for which it also keeps the sets of in-neighbours. Since the edge sets are sets, adding an existing edge changes nothing. A [weighted graph](/weighted-graph/) maps each neighbour to its weight, a hash map in place of a hash set, which gives the dictionary of dictionaries of NetworkX.

## Representation

The structure has a flag that says whether the graph is directed and a hash map $S$ from vertices to hash sets: $S[u]$ is the set of out-neighbours of $u$, or of neighbours for an undirected graph. A directed graph also has a hash map $P$ with the same keys, where $P[v]$ is the set of in-neighbours of $v$. The vertex set is the key set of $S$.

**Invariant (H).**

- (H1) Each element of each set $S[u]$, or $P[v]$, is a key of $S$.
- (H2) If the graph is undirected, $v \in S[u]$ if and only if $u \in S[v]$, and $u \notin S[u]$.
- (H3) If the graph is directed, $P$ has the same keys as $S$, and $u \in P[v]$ if and only if $v \in S[u]$.

The edges are the pairs $(u, v)$, or sets $\{u, v\}$, with $v \in S[u]$. With tables that keep a bounded [load factor](/load-factor/) and shrink when they empty, the outer table has $\Theta(n)$ slots and $S[u]$ has $\Theta(d(u) + 1)$ slots, so the space is $\Theta(n + m)$ words.

## Operations

```pseudo id=main
NEW(directed)
L1  S ← an empty hash map; if directed then P ← an empty hash map

ADD-VERTEX(G, x)
L2  if x is not a key of S then S[x] ← ∅; if directed then P[x] ← ∅

ADD-EDGE(G, u, v)                        ▷ for an undirected graph, u ≠ v
L3  ADD-VERTEX(G, u); ADD-VERTEX(G, v)
L4  insert v into S[u]                   ▷ no change if already there
L5  if directed then insert u into P[v] else insert u into S[v]

REMOVE-EDGE(G, u, v)
L6  delete v from S[u] if it is there
L7  if directed then delete u from P[v] else delete u from S[v]

ADJACENT(G, u, v)
L8  return u is a key of S and v ∈ S[u]

NEIGHBORS(G, u)
L9  for each v in S[u] do output v

DEGREE(G, u)                             ▷ out-degree for a directed graph
L10 return |S[u]|

REMOVE-VERTEX(G, x)
L11 for each y in S[x] do delete x from (P[y] if directed else S[y])
L12 if directed then for each y in P[x] do delete x from S[y]
L13 delete the key x from S, and from P if directed
```

**Add-vertex** (line L2) is one lookup and maybe one insertion in the outer table, in $O(1)$ expected amortized time.

**Add-edge** (lines L3 to L5) is up to two lookups in the outer table and two set insertions, in $O(1)$ expected amortized time. The set insertion includes the duplicate test, so unlike the [adjacency list](/adjacency-list/) no precondition is needed: adding an edge twice leaves one edge.

**Remove-edge** (lines L6 and L7) is two set deletions, in $O(1)$ expected time.

**Adjacent** (line L8) is one lookup in the outer table and one in $S[u]$, in $O(1)$ expected time.

**Neighbors and degree** (lines L9 and L10) iterate over $S[u]$ in time proportional to its number of slots, which is $\Theta(d(u) + 1)$ when the table shrinks with its contents, and return the stored count in $O(1)$ time.

**Remove-vertex** (lines L11 to L13) deletes $x$ from the set of each neighbour, in $O(d(x) + 1)$ expected time for an undirected graph and $O(d^+(x) + d^-(x) + 1)$ for a directed graph. On a plain adjacency list, finding the in-neighbours of $x$ alone would take $\Theta(n + m)$.

The expected bounds hold for each fixed sequence of operations when the hash functions are drawn from a [universal family](/universal-hashing/), as for any [hash table](/hash-table/); the expectation is over the choice of the functions.

## Example

Take an undirected graph and the operations of the [adjacency matrix](/adjacency-matrix/) page, with two more at the end. Sets are shown sorted, but a hash set has no order.

| step | operation | result | $S$ after the step |
|---|---|---|---|
| 1 | NEW, then ADD-VERTEX of 0, 1, 2, 3 | | 0: { }, 1: { }, 2: { }, 3: { } |
| 2 | ADD-EDGE(0, 1) | | 0: {1}, 1: {0}, 2: { }, 3: { } |
| 3 | ADD-EDGE(1, 2) | | 0: {1}, 1: {0, 2}, 2: {1}, 3: { } |
| 4 | ADD-EDGE(2, 0) | | 0: {1, 2}, 1: {0, 2}, 2: {0, 1}, 3: { } |
| 5 | ADD-EDGE(3, 1) | | 0: {1, 2}, 1: {0, 2, 3}, 2: {0, 1}, 3: {1} |
| 6 | ADD-EDGE(1, 0) | | unchanged, the edge is already there |
| 7 | ADJACENT(0, 2) | true | unchanged |
| 8 | ADJACENT(0, 3) | false | unchanged |
| 9 | NEIGHBORS(1), DEGREE(1) | {0, 2, 3}, 3 | unchanged |
| 10 | REMOVE-EDGE(1, 0) | | 0: {2}, 1: {2, 3}, 2: {0, 1}, 3: {1} |
| 11 | REMOVE-VERTEX(2) | | 0: { }, 1: {3}, 3: {1} |

In step 6 the two set insertions find the elements already there. In step 11, line L11 visits the neighbours 0 and 1 of vertex 2 and deletes 2 from their sets, and line L13 deletes the key 2. On the matrix, removing a vertex renumbers another vertex; here the names 0, 1 and 3 stay.

For the directed graph on $\{0, \ldots, 4\}$ with the edges $(0,1), (0,2), (1,2), (2,3), (3,1), (3,4)$, the out-sets are $\{1, 2\}, \{2\}, \{3\}, \{1, 4\}, \{\,\}$ and the in-sets are $\{\,\}, \{0, 3\}, \{0, 1\}, \{2\}, \{3\}$. REMOVE-VERTEX$(3)$ deletes 3 from $P[1]$ and $P[4]$ by line L11 and from $S[2]$ by line L12.

## Correctness

The sets $S[u]$, and $P[v]$, behave as mathematical sets by the correctness of the [hash table](/hash-table/), so it suffices to check that each operation keeps (H) and changes the edge set as the graph type says. ADD-EDGE first makes both ends keys, which keeps (H1), and then inserts the two matching elements, $v$ into $S[u]$ and $u$ into $S[v]$ or $P[v]$, so the symmetry of (H2) or the mirror of (H3) still holds and the edge set gains exactly the edge. REMOVE-EDGE deletes the same two elements. ADJACENT, NEIGHBORS and DEGREE read $S[u]$, which by definition holds the neighbours of $u$. REMOVE-VERTEX deletes every element that names $x$, which by (H2) or (H3) are in the sets of the vertices listed in $S[x]$ and $P[x]$, and then deletes the key, so (H1) holds again and exactly the edges at $x$ are gone. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

All bounds are expected over the choice of universal hash functions, and amortized where the tables grow or shrink.

| operation | time |
|---|---|
| adjacent$(u, v)$ | $O(1)$ |
| add-edge, with the duplicate test | $O(1)$ amortized |
| remove-edge | $O(1)$ amortized |
| neighbors$(u)$ | $\Theta(d(u) + 1)$ |
| degree$(u)$ | $O(1)$ |
| in-neighbors$(v)$, directed | $\Theta(d^-(v) + 1)$ |
| add-vertex | $O(1)$ amortized |
| remove-vertex | $O(d(x) + 1)$, or $O(d^+(x) + d^-(x) + 1)$ directed |
| list all edges | $\Theta(n + m)$ |
| space | $\Theta(n + m)$ words |

**Against the other representations.** For a dynamic sparse graph with many pair queries, hash-based adjacency is the only one of the basic representations with $\Theta(n + m)$ space and $O(1)$ time for all of `adjacent`, `add-edge` and `remove-edge`. The [adjacency list](/adjacency-list/) pays $O(d)$ for the query and for removal, and the [adjacency matrix](/adjacency-matrix/) pays $\Theta(n^2)$ space. The cost is in the constants: a hash set uses several words per element for the slots it keeps free and for the stored hashes, and a scan of $S[u]$ jumps through memory. A [compressed sparse row](/compressed-sparse-row/) array of the same graph is often five to ten times smaller and faster to scan.

**Worst cases.** The $O(1)$ bounds are expected. A fixed hash function can be attacked with keys that all collide, which makes each operation take time linear in the set size. Universal or randomly seeded hashing prevents this for inputs that do not depend on the random choices. [Cuckoo hashing](/cuckoo-hashing/) gives $O(1)$ worst-case queries.

## Variants

- **Dictionary of dictionaries.** Map each neighbour to its edge data, such as a weight, in place of a set. This is the representation of NetworkX, in which `G[u][v]` returns the data of the edge.
- **One hash set of pairs.** Store all edges as keys $(u, v)$ in one table, together with plain adjacency lists for the scans. The query costs one lookup, and the space is about one table entry per edge.
- **Hybrid sets.** Keep a small set as a sorted array, and switch to a hash set when its size passes a threshold. Most vertices of real graphs have small degree, so this saves memory with little loss in query time.
- **Integer vertices.** When the vertices are $0, \ldots, n-1$, replace the outer hash map by an array of sets, which saves one lookup per operation.
- **Multigraphs.** Map each neighbour to a count, or to a set of edge keys, as NetworkX does in its multigraph classes.

## When to use it

Use hash-based adjacency for a graph that changes by single edges and vertices, that is queried for pairs, or whose vertices are named by strings or objects: graph libraries, prototypes, [dynamic graph](/dynamic-graph/) algorithms, and graphs built while reading data. Use an [adjacency list](/adjacency-list/) when no pair queries are needed and memory matters, a [compressed sparse row](/compressed-sparse-row/) array for large static graphs, and an [adjacency matrix](/adjacency-matrix/) or a [bitset matrix](/bitset-adjacency-matrix/) for dense graphs.

## Pitfalls

- **Iteration order.** A hash set has no fixed order, and in some languages the order changes from run to run because of seeded hashing. Algorithms that must give the same output each time, such as tie-breaking in a search, must sort the neighbours or use insertion-ordered maps.
- **Changing a set during iteration.** Removing an edge at $u$ while iterating over $S[u]$ is an error in many languages, and in others it gives undefined results. Copy the set first, as line L11 does in the implementation.
- **Memory.** A hash set per vertex costs tens to hundreds of bytes even when empty. A graph with $10^7$ vertices of degree 1 or 2 spends most of its memory on empty slots. Use the hybrid sets or a packed structure for such graphs.
- **Mutable or unhashable vertex names.** Vertices are hash keys, so their hash must not change while they are in the graph. In Python, a list cannot be a vertex; a tuple can.
- **Forgetting the in-sets.** Without $P$, removing a vertex of a directed graph must scan all sets for $x$, in $\Theta(n + m)$ time, and the in-neighbours of a vertex are not available.

## Implementations

The Python class `HashAdjacency` uses a `dict` from vertices to `set` objects, and a second `dict` of in-sets for directed graphs. Python's `dict` and `set` are hash tables with open addressing and randomized string hashing. The methods follow the main block line by line, and `check_invariant` tests (H1) to (H3).

## History

Replacing each adjacency list by a hash table, to get constant expected time pair queries in linear space, is a standard exercise in CLRS (Section 20.1), built on the hash tables of Chapter 11. The dictionary-of-dictionaries form became widespread with the NetworkX library, described by Hagberg, Schult and Swart in 2008, which stores each graph as nested Python dictionaries keyed by arbitrary hashable nodes.

## References
