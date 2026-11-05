---
tag: 4VK71J
kind: data-structure
slug: adjacency-matrix
name: Adjacency matrix
aliases:
- vertex matrix
area: graphs/graph-representation
level: intro
summary: V×V matrix whose entry (u,v) records the edge from u to v; space Θ(V^2).
implements: [graph]
prereqs: [graph, directed-graph]
see_also: [adjacency-list, bitset-adjacency-matrix, incidence-matrix, laplacian-matrix, dense-graph, universal-sink, graph-square, floyd-warshall]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), the adjacency-matrix representation, its symmetry for undirected graphs and its Θ(V^2) memory
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the representation alternatives and the table of their costs
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 3.1.1 (How is a graph represented?)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 7 (Graph Traversal), the section on data structures for graphs, the comparison of adjacency matrices and adjacency lists
---

An adjacency matrix stores a [graph](/graph/) with vertices $0, \ldots, n-1$ as an $n \times n$ array $A$ in which $A[u][v] = 1$ when there is an [edge](/edge/) from $u$ to $v$ and $A[u][v] = 0$ otherwise. It answers the [adjacency query](/adjacency-query/) "is $(u, v)$ an edge?" in $O(1)$ time and adds or removes an edge in $O(1)$ time. It costs $\Theta(n^2)$ space, whatever the number of edges, and listing the neighbours of a vertex takes $\Theta(n)$ time. So it is the representation of choice for a [dense graph](/dense-graph/) and for algorithms that are matrix computations, such as [Floyd-Warshall](/floyd-warshall/).

## In plain words

Make a table with one row and one column for each vertex. Put a 1 in the cell of row $u$ and column $v$ when $u$ has an edge to $v$, and a 0 when it has none. For a graph without arrows, the table is a mirror image of itself across its diagonal, because an edge between $u$ and $v$ is also an edge between $v$ and $u$.

To check one pair, you look at one cell. That is as fast as it gets. To find all the neighbours of a vertex, you read its whole row, even if it holds only one 1. And the table always has as many cells as the square of the number of vertices, so a big graph with few edges wastes a lot of memory on zeros.

## The abstract type

The adjacency matrix implements the [graph](/graph/) type over the vertex set $V = \{0, 1, \ldots, n-1\}$: `adjacent(G, u, v)`, `neighbors(G, u)`, `add-edge(G, u, v)`, `remove-edge(G, u, v)`, `add-vertex(G)`, `degree(G, u)` and `edges(G)`. It stores a [directed graph](/directed-graph/), where $E \subseteq V \times V$ and self-loops are allowed, or a simple [undirected graph](/undirected-graph/), where each edge is a pair $\{u, v\}$ with $u \ne v$. A [weighted graph](/weighted-graph/) stores $w(u, v)$ in the cell in place of the 1, as the variants below explain.

## Representation

The structure has the number $n$ of vertices, a flag that says whether the graph is directed, and an $n \times n$ array $A$ of bits. The graph it stands for is

$$E(A) = \{(u, v) : A[u][v] = 1\} \text{ (directed)}, \qquad E(A) = \{\{u, v\} : u < v,\ A[u][v] = 1\} \text{ (undirected)}.$$

**Invariant (M).** In the directed case, there is nothing more to keep: each 0-1 array is a directed graph with loops. In the undirected case:

- (M1) $A[u][v] = A[v][u]$ for each $u, v$ (the array is symmetric);
- (M2) $A[v][v] = 0$ for each $v$ (no self-loops).

So an undirected edge $\{u, v\}$ is stored twice, in cell $(u, v)$ and in cell $(v, u)$. The array uses $n^2$ cells. With one bit per cell it uses $n^2$ bits, and an undirected graph needs only the $\binom{n}{2}$ cells above the diagonal.

## Operations

```pseudo id=main
NEW(n, directed)
L1  A ← an n × n array of 0

ADD-EDGE(G, u, v)                          ▷ for an undirected graph, u ≠ v
L2  A[u][v] ← 1
L3  if not directed then A[v][u] ← 1

REMOVE-EDGE(G, u, v)
L4  A[u][v] ← 0
L5  if not directed then A[v][u] ← 0

ADJACENT(G, u, v)
L6  return A[u][v] = 1

NEIGHBORS(G, u)                            ▷ out-neighbours, in increasing order
L7  for v ← 0 to n − 1 do
L8      if A[u][v] = 1 then output v

DEGREE(G, u)                               ▷ out-degree for a directed graph
L9  return the number of v with A[u][v] = 1

ADD-VERTEX(G)
L10 B ← an (n + 1) × (n + 1) array of 0
L11 B[i][j] ← A[i][j] for each 0 ≤ i, j < n
L12 A ← B, n ← n + 1
L13 return n − 1
```

**New** (line L1) makes the graph with $n$ vertices and no edges. It writes $n^2$ zeros, so it takes $\Theta(n^2)$ time. A system that hands out zeroed memory hides this cost but does not remove it.

**Add-edge and remove-edge** (lines L2 to L5) write one cell for a directed graph and two mirror cells for an undirected graph. Each takes $O(1)$ time. Adding an edge that is already there changes nothing, so the matrix stores a set of edges, as the [graph laws](/graph/) require. A self-loop in an undirected graph is refused by the caller, to keep (M2).

**Adjacent** (line L6) reads one cell, in $O(1)$ time. This is the main strength of the structure.

**Neighbors** (lines L7 and L8) reads the whole row of $u$. It takes $\Theta(n)$ time even when $u$ has no neighbours at all. The in-neighbours of $v$ are the 1s of column $v$, found in $\Theta(n)$ time too.

**Degree** (line L9) counts the 1s of row $u$ in $\Theta(n)$ time. With bit rows and a [population count](/population-count/) instruction this drops to $O(n/w)$ for $w$-bit words; see the [bitset adjacency matrix](/bitset-adjacency-matrix/). Keeping a count per row makes it $O(1)$, at the cost of an update in lines L2 to L5 that first tests whether the cell changes.

**Add-vertex** (lines L10 to L13) copies the array into a larger one, in $\Theta(n^2)$ time. With spare rows and columns allocated by doubling, as a [dynamic array](/dynamic-array/) does, a sequence of $k$ additions starting from $n_0 \ge 1$ vertices costs $O((n_0 + k)^2)$ in total, which is $O(n)$ amortized per addition when $k \ge n_0$, since each addition must clear a new row and column of $n$ cells anyway. Removing a vertex is done by swapping it with the last vertex: copy row and column $n - 1$ into row and column $v$, then drop the last row and column, in $\Theta(n)$ time. This renumbers vertex $n - 1$ as $v$.

## Example

Take an undirected graph on $V = \{0, 1, 2, 3\}$. Start with NEW$(4)$, then run these operations. The table shows the rows of $A$ after each step, written as bit strings with column 0 first.

| step | operation | result | rows 0, 1, 2, 3 |
|---|---|---|---|
| 1 | NEW(4) | | 0000 0000 0000 0000 |
| 2 | ADD-EDGE(0, 1) | | 0100 1000 0000 0000 |
| 3 | ADD-EDGE(1, 2) | | 0100 1010 0100 0000 |
| 4 | ADD-EDGE(2, 0) | | 0110 1010 1100 0000 |
| 5 | ADD-EDGE(3, 1) | | 0110 1011 1100 0100 |
| 6 | ADJACENT(0, 2) | true | unchanged |
| 7 | ADJACENT(0, 3) | false | unchanged |
| 8 | NEIGHBORS(1) | 0, 2, 3 | unchanged |
| 9 | DEGREE(1) | 3 | unchanged |
| 10 | REMOVE-EDGE(1, 0) | | 0010 0011 1100 0100 |
| 11 | ADD-VERTEX | 4 | 00100 00110 11000 01000 00000 |

After step 5 the matrix is

$$A = \begin{pmatrix} 0 & 1 & 1 & 0 \\ 1 & 0 & 1 & 1 \\ 1 & 1 & 0 & 0 \\ 0 & 1 & 0 & 0 \end{pmatrix},$$

which is symmetric with a zero diagonal. Its row sums $2, 3, 2, 1$ are the degrees, and they sum to $8 = 2m$ for the $m = 4$ edges. Step 8 reads all four cells of row 1, and step 11 copies 16 cells into a $5 \times 5$ array.

For the directed graph on $\{0, \ldots, 4\}$ with the edges $(0,1), (0,2), (1,2), (2,3), (3,1), (3,4)$, the rows are 01100, 00100, 00010, 01001, 00000. Row sums give the out-degrees $2, 1, 1, 2, 0$ and column sums give the in-degrees $0, 2, 2, 1, 1$.

## Correctness

The structure is correct when, after each operation, $E(A)$ is the edge set that the graph type prescribes, and (M1) and (M2) hold for an undirected graph. NEW gives the zero array, so $E(A) = \emptyset$, and (M1) and (M2) hold. ADD-EDGE sets the cell $(u, v)$, and for an undirected graph also $(v, u)$, so $E(A)$ gains exactly the new edge, and the array stays symmetric. Since $u \ne v$, the diagonal stays zero. REMOVE-EDGE is the same with 0. The queries read the cells that define $E(A)$, so they answer for $E(A)$. ADD-VERTEX copies each old cell to the same place and adds a zero row and a zero column, so $E(A)$ is unchanged and the new vertex has no edges. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $n$ be the number of vertices and $m$ the number of edges. Each cell access costs $O(1)$ on the [word RAM](/word-ram/).

| operation | time | notes |
|---|---|---|
| new graph with $n$ vertices | $\Theta(n^2)$ | writes each cell |
| adjacent$(u, v)$ | $\Theta(1)$ | one read |
| add-edge, remove-edge | $\Theta(1)$ | one or two writes |
| neighbors$(u)$ | $\Theta(n)$ | the whole row, whatever $d(u)$ is |
| in-neighbors$(v)$ | $\Theta(n)$ | the whole column |
| degree$(u)$ | $\Theta(n)$, or $O(1)$ with stored counts | |
| add-vertex | $\Theta(n^2)$, or $O(n)$ amortized with doubling | |
| remove-vertex | $\Theta(n)$ with renumbering | |
| list all edges | $\Theta(n^2)$ | |
| transpose | $\Theta(n^2)$ | swap $A[u][v]$ and $A[v][u]$ |
| space | $\Theta(n^2)$ cells | $n^2$ bits with bit packing |

**The cost of whole-graph algorithms.** A [breadth-first search](/breadth-first-search/) or a [depth-first search](/depth-first-search/) calls neighbors once for each vertex it reaches, so it takes $\Theta(n^2)$ time on a matrix, against $\Theta(n + m)$ on an [adjacency list](/adjacency-list/). For a graph with $m = \Theta(n^2)$ the two are the same. For a graph with $m = O(n)$ the matrix is slower by a factor of $n$.

**A lower bound.** Many questions cannot be answered faster than $\Omega(n^2)$ on a matrix, because an algorithm may have to read each cell. For example, to decide whether an undirected graph has any edge, an algorithm must read all $\binom{n}{2}$ cells above the diagonal in the worst case: if it skips the cell $\{x, y\}$, it cannot tell the empty graph from the graph with only that edge. The [graph](/graph/) page gives the proof. Some questions are faster: a [universal sink](/universal-sink/) of a directed graph, a vertex with in-degree $n - 1$ and out-degree 0, is found in $O(n)$ time on a matrix.

**Matrix algebra.** With integer entries, $(A^k)[u][v]$ is the number of walks of length $k$ from $u$ to $v$. So the [square of a graph](/graph-square/) and the [transitive closure](/transitive-closure/) are matrix products, and fast matrix multiplication computes them in $O(n^\omega)$ time.

## Variants

- **Weighted matrix.** Store $w(u, v)$ in the cell, and a special value such as $\infty$ for "no edge". [Floyd-Warshall](/floyd-warshall/) and the matrix forms of [all-pairs shortest paths](/all-pairs-shortest-paths/) use this form, with $A[v][v] = 0$.
- **Bit matrix.** Pack each row into $\lceil n/w \rceil$ words of $w$ bits. Then the space is $n \lceil n/w \rceil$ words, and set operations on rows run $w$ bits at a time. See [bitset adjacency matrix](/bitset-adjacency-matrix/).
- **Triangular storage.** For an undirected graph, store only the cells with $u < v$, in an array of $\binom{n}{2}$ bits. The cell of $\{u, v\}$ with $u < v$ is at index $\binom{v}{2} + u$ in the order $(0,1), (0,2), (1,2), (0,3), \ldots$.
- **Multigraph counts.** Store the number of parallel edges in the cell. For an undirected multigraph a loop is often stored as 2 on the diagonal, so that the row sum is the degree.
- **[Incidence matrix](/incidence-matrix/).** An $n \times m$ matrix with one column per edge. It is a different structure.
- **[Laplacian matrix](/laplacian-matrix/).** $L = D - A$, where $D$ is the diagonal matrix of degrees. It is the base of spectral graph methods and of the [matrix-tree theorem](/matrix-tree-theorem/).
- **Sparse matrix formats.** A [sparse matrix](/sparse-matrix/) stores only the nonzero cells. The [compressed sparse row](/compressed-sparse-row/) format of the adjacency matrix is the same thing as a packed adjacency list.

## When to use it

Use an adjacency matrix when the graph is dense, when the algorithm makes many adjacency queries on arbitrary pairs, or when the algorithm is a matrix computation. Examples are [Floyd-Warshall](/floyd-warshall/), [transitive closure](/transitive-closure/) by matrix products, exhaustive searches for a [clique](/clique/) on small graphs and spectral methods. It is also the simplest structure to write, and it is a good choice when $n$ is at most a few thousand. Use an [adjacency list](/adjacency-list/) when the graph is sparse or when the algorithm walks the neighbours of each vertex, as most traversals do. Use [hash-based adjacency](/hash-based-adjacency/) to get fast queries and $\Theta(n + m)$ space together.

## Pitfalls

- **One cell for an undirected edge.** Setting only $A[u][v]$ in line L2 and forgetting line L3 breaks (M1). Then ADJACENT$(v, u)$ is false while ADJACENT$(u, v)$ is true, and a search from $v$ misses the edge.
- **Zero as "no edge" in a weighted matrix.** If a weight can be 0, a cell value of 0 cannot also mean "no edge". Use $\infty$, a separate bit matrix, or `None`.
- **Memory for a sparse graph.** A graph with $n = 10^6$ vertices needs $10^{12}$ cells, which is 125 GB even with one bit per cell, while an adjacency list of a graph with $10^7$ edges fits in about 100 MB. Check $n^2$ before you choose the matrix.
- **Quadratic traversals.** Running BFS on a matrix costs $\Theta(n^2)$, because line L7 scans each full row. On a sparse graph, convert to an adjacency list first, in $\Theta(n^2)$ time once, if many traversals follow.
- **Column scans and the cache.** In row-major storage, a row is contiguous and a column is not. A loop that scans column $v$ for the in-neighbours touches $n$ different cache lines. Scan the transpose by rows instead.
- **Self-loops in an undirected matrix.** If a loop at $v$ is stored as $A[v][v] = 1$, the row sum no longer equals the degree in the multigraph sense, where a loop counts 2. Fix the convention before you count.

## Implementations

The Python class keeps a list of $n$ rows, each a list of $n$ booleans, and a flag for directed graphs. It follows the main block line by line. `add_edge` refuses a self-loop in an undirected graph, to keep (M2). `neighbors` returns the out-neighbours in increasing order.

## History

The matrix of a graph is as old as the algebraic study of graphs, and the textbooks of this page present it as one of the two standard representations, together with the [adjacency list](/adjacency-list/). CLRS (Section 20.1) and Sedgewick and Wayne (Section 4.1) give the trade-off of this page: constant-time queries against quadratic space and quadratic traversals.

## References
