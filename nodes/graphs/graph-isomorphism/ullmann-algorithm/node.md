---
tag: GMKCZG
kind: algorithm
slug: ullmann-algorithm
name: Ullmann's algorithm
aliases:
- Ullmann subgraph isomorphism
- Ullmann's refinement procedure
area: graphs/graph-isomorphism
level: core
summary: Backtracking search that prunes a candidate-mapping matrix with refinement for subgraph isomorphism.
solves: [subgraph-isomorphism]
model: word-ram
complexity:
  vars: {k: the number of vertices of the pattern, n: the number of vertices of the host}
  time: {worst: O(n^k k^2 n^2)}
  space: {extra: O(k^2 n)}
properties: {deterministic: true, recursive: false, directed: false}
prereqs: [subgraph-isomorphism, generic-backtracking-algorithm, adjacency-matrix]
see_also: [vf2-algorithm, weisfeiler-leman, maximum-common-subgraph, clique-problem, graph-isomorphism-problem, partition-refinement]
sources:
  - paper: doi:10.1145/321921.321925
    title: J. R. Ullmann, An algorithm for subgraph isomorphism, Journal of the ACM 23(1), 31 to 42 (1976)
    locator: the whole paper (the enumeration over the matrix M, the refinement procedure, and the experiments)
  - paper: doi:10.1109/TPAMI.2004.75
    title: Luigi P. Cordella, Pasquale Foggia, Carlo Sansone and Mario Vento, A (sub)graph isomorphism algorithm for matching large graphs, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(10), 1367 to 1372 (2004)
    locator: Section 1 (Ullmann's algorithm as the reference method, and its memory use) and Section 4 (experimental comparison)
  - book: isbn:9783540435506
    title: Gabriel Valiente, Algorithms on Trees and Graphs, Springer, 2002
    locator: Chapter 7, Graph isomorphism (backtracking algorithms for subgraph isomorphism)
---

Ullmann's algorithm (1976) finds all embeddings of a pattern graph into a host graph. It keeps a 0-1 candidate matrix $M$ with one row per pattern vertex and one column per host vertex, where $M[i][j] = 1$ means that pattern vertex $i$ may still map to host vertex $j$. It assigns the rows one at a time by backtracking, and after each assignment it runs a refinement procedure that deletes candidates whose neighbors have no candidates next to them. The refinement makes the search far smaller than plain backtracking, and the matrix rows fit in bit vectors. It was the standard method for [subgraph isomorphism](/subgraph-isomorphism/) for decades and is still the baseline in comparisons.

## In plain words

Make a table with a row for each point of the small network and a column for each point of the large one. Put a mark where the small point could go: at first, wherever the large point has at least as many links. Then clean the table: if a small point is marked at a large point, but some neighbor of the small point has no mark at any neighbor of the large point, erase the mark. Repeat the cleaning until nothing changes. Now choose a place for the first small point, clean again, choose for the second, and so on. If a row loses all its marks, undo the last choice and try another.

## The problem

The input is a pattern $G_1 = (V_1, E_1)$ with $k$ vertices and a host $G_2 = (V_2, E_2)$ with $n$ vertices. Both are simple undirected graphs here, with optional vertex labels that an embedding must keep; Ullmann's paper states the method for adjacency matrices, and the same steps work for directed graphs with separate in-neighbor and out-neighbor checks. The output is every injective map $f : V_1 \to V_2$ with $\{a, b\} \in E_1 \implies \{f(a), f(b)\} \in E_2$ (a monomorphism). The induced variant also asks for $\{f(a), f(b)\} \in E_2 \implies \{a, b\} \in E_1$, and with $k = n$ and equal edge counts it decides [graph isomorphism](/graph-isomorphism-problem/).

## The algorithm

$M$ is a $k \times n$ 0-1 matrix; row $i$ is the candidate set of pattern vertex $i$. $N_1$ and $N_2$ are neighbor sets.

```pseudo id=main
ULLMANN(G1, G2)
L1  M[i][j] ← 1 when i and j have equal labels and deg1(i) ≤ deg2(j), else 0
L2  REFINE(M); if some row of M is all 0 then stop
L3  search the rows i = 0, 1, ..., k − 1 depth first, keeping one copy of M per level
L4      for each column j with M[i][j] = 1 do
L5          M' ← M with row i set to the single 1 at column j and column j set to 0 in the rows below i
L6          REFINE(M'); if some row of M' is all 0 then try the next j
L7          if i = k − 1 then output f(r) = the column of the 1 in row r, after checking the edges
            else continue with row i + 1 and matrix M'

REFINE(M)
L8  repeat
L9      for each i and j with M[i][j] = 1 do
L10         if some x in N1(i) has M[x][y] = 0 for every y in N2(j) then M[i][j] ← 0
L11 until no entry changed in a full pass
```

With bit vectors, the test in L10 is one AND of row $x$ with the neighbor mask of $j$. The implementation keeps rows as integers used as bit sets and runs the depth-first search with an explicit stack.

## Example

Let the pattern be the paw: the triangle $0, 1, 2$ with a pendant vertex 3 at 2 (degrees $2, 2, 3, 1$). Let the host have the edges $03, 12, 14, 15, 23, 45$: the triangle $1, 4, 5$, with $1 - 2 - 3 - 0$ hanging from vertex 1 (degrees $1, 3, 2, 2, 2, 2$). Rows list the candidate host vertices.

| step | row 0 | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| L1, by degree | 1, 2, 3, 4, 5 | 1, 2, 3, 4, 5 | 1 | 0, 1, 2, 3, 4, 5 |
| L2, after REFINE | 4, 5 | 4, 5 | 1 | 2, 4, 5 |
| row 0 ← 4, after REFINE | 4 | 5 | 1 | 2, 5 |
| row 1 ← 5, column 5 cleared below | 4 | 5 | 1 | 2 |
| output | | | | $f = (4, 5, 1, 2)$ |

REFINE at the root cuts the matrix from 17 marks to 8. Pattern vertex 2 can only go to host vertex 1, the only vertex of degree 3, so its neighbors 0 and 1 can only go to neighbors of 1 that have a neighbor among the candidates of 0 and 1, which leaves 4 and 5. The search then finds the second embedding $(5, 4, 1, 2)$ with row 0 set to 5, and no dead end occurs. Both embeddings are also induced.

Other counts from the implementation: the path on 3 vertices has 10 embeddings into $C_5$; $C_5$ has 120 embeddings into the Petersen graph and the triangle none; the $4 \times 4$ rook's graph has 1152 automorphisms and the Shrikhande graph 192, and the induced search between them finds no isomorphism.

## Correctness

The [full proof](proofs/correctness.md) rests on one invariant: for every embedding $f$ that agrees with the choices made so far, $M[i][f(i)] = 1$ for every row $i$.

- **L1 keeps the invariant**, because an embedding maps a vertex of degree $d$ to a vertex of degree at least $d$ with the same label.
- **REFINE keeps it.** If $M[i][j]$ is cleared, some neighbor $x$ of $i$ has no candidate adjacent to $j$; an embedding with $f(i) = j$ would need $f(x)$ adjacent to $j$ with $M[x][f(x)] = 1$, which does not exist.
- **L5 keeps it** for the embeddings with $f(i) = j$: they map no later row to $j$, by injectivity.
- **Soundness.** At a leaf every row has one 1; the rows above $i$ hold distinct columns because each fixed column was cleared below it, so $f$ is injective, and L7 checks the edges.
- **Completeness and uniqueness.** By the invariant, the branch $j = f(i)$ is never pruned at any level, so every embedding reaches a leaf, and distinct leaves differ in some row, so each embedding is output once.

## Complexity

| case | time | space |
|---|---|---|
| refinement at one node | $O(k n \cdot d_1)$ bit operations per pass, at most $k n$ passes | |
| whole search, worst case | $O(n^k)$ nodes, so $O(n^k \cdot k^2 n^2)$ word operations with $d_1 \le k$ and rows of $n / w$ words | $O(k^2 n)$ bits per path of the stack |
| best case | $O(k n)$ for L1 plus one refinement, when REFINE leaves a single candidate per row | $O(k n)$ |

The search tree has at most $n (n - 1) \cdots (n - k + 1) \le n^k$ leaves. Each node copies a $k \times n$ matrix and refines it. The depth-first stack holds one matrix per level, $k$ levels, so $O(k^2 n)$ bits; the implementation also keeps the untried columns of each level. Subgraph isomorphism is NP-complete, so no exact method avoids exponential worst cases unless P = NP; under the exponential time hypothesis no $f(k) n^{o(k)}$ algorithm exists for $k$-clique, a special case.

## Properties

- **Exact.** It lists every embedding.
- **Pruning by look-ahead.** REFINE is a form of arc consistency on the constraint network with one variable per pattern vertex; it finds many dead ends before the search reaches them.
- **Bit-parallel.** Rows and neighbor masks are bit vectors, so one machine word handles 64 host vertices at once.
- **Deterministic.** The running time depends on the row order and on the numbering of the host.
- **Memory hungry compared with [VF2](/vf2-algorithm/).** It stores a matrix per level instead of linear-size arrays.

## Variants and improvements

- **Row order.** Choosing the row with the fewest candidates first, or rows in a connected order, reduces the tree. Ullmann's paper uses the given order.
- **Induced embeddings and isomorphism.** Add the non-edge check, either at the leaves as here or inside REFINE with the complement graphs.
- **Ullmann (2010)** revisited the method with bit-vector domain filtering for binary constraint satisfaction, with stronger look-ahead than the 1976 refinement.
- **Constraint programming solvers** such as the Glasgow Subgraph Solver and LAD add all-different reasoning, neighborhood degree sequences and restarts; they descend from the same idea of filtering candidate domains.
- **[Color refinement](/weisfeiler-leman/)** before the search, for isomorphism, splits candidates by stable color, a stronger filter than degree.
- **[VF2](/vf2-algorithm/)** replaces the matrix by terminal sets and counts, trading pruning power for linear memory.

## When to use it

Use Ullmann's algorithm, or one of its bit-parallel descendants, for exact subgraph matching when patterns are small or medium and hosts have at most a few thousand vertices, so that the matrix fits in memory. It is easy to implement and to extend with labels. For very large sparse hosts use [VF2](/vf2-algorithm/) or VF3; for hard instances use a constraint solver; for isomorphism of whole unlabeled graphs use [nauty](/nauty/) or [bliss](/bliss/).

## Pitfalls

- **Forgetting injectivity.** Without clearing column $j$ in the rows below $i$ in L5, two pattern vertices can map to the same host vertex.
- **Refining only once.** One pass of L9 and L10 is not enough; clearing one entry can make others fail. Repeat until a full pass changes nothing.
- **Stale matrix after backtracking.** Each level must work on its own copy of $M$, or the changes of a failed branch leak into its siblings.
- **Treating REFINE as a complete test.** A matrix with a 1 in every row after REFINE can still have no embedding; only the search decides.
- **Recursion depth.** A recursive search has depth $k$, which can exceed default limits for large patterns; use an explicit stack.

## Implementations

## History

Julian R. Ullmann published the algorithm in the Journal of the ACM in 1976, with the refinement procedure as its main idea and experiments on random graphs. It was the reference method for subgraph isomorphism until [VF2](/vf2-algorithm/) (2001, journal 2004) reduced memory, and it still appears as the baseline in benchmarks of subgraph matching. Ullmann returned to the problem in 2010 with bit-vector algorithms for binary constraint satisfaction.

## References
