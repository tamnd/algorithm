---
tag: 7KYG8D
kind: algorithm
slug: dulmage-mendelsohn-decomposition
name: Dulmage-Mendelsohn decomposition
aliases:
- DM decomposition
area: graphs/matching
level: advanced
summary: Canonical block decomposition of a bipartite graph from all of its maximum matchings.
solves: [bipartite-matching]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O((n + m) n^(1/2))}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1958
  people: [Andrew L. Dulmage, Nathan S. Mendelsohn]
  note: Dulmage and Mendelsohn introduced the coverings and the decomposition of bipartite graphs between 1958 and 1963; Pothen and Fan turned it into the standard tool for block triangular forms of sparse matrices in 1990.
prereqs: [bipartite-matching, alternating-path, strongly-connected-components]
see_also: [hopcroft-karp, tarjan-scc, gallai-edmonds-decomposition, konig-theorem, hall-theorem, condensation-graph, sparse-matrix, fill-reducing-ordering]
sources:
  - paper: doi:10.4153/CJM-1958-052-0
    title: Andrew L. Dulmage and Nathan S. Mendelsohn, Coverings of bipartite graphs, Canadian Journal of Mathematics 10, 517 to 534 (1958)
    locator: the whole paper (the coarse decomposition through minimum covers and the fine decomposition into irreducible parts)
  - paper: doi:10.1145/98267.98287
    title: Alex Pothen and Chin-Ju Fan, Computing the block triangular form of a sparse matrix, ACM Transactions on Mathematical Software 16(4), 303 to 324 (1990)
    locator: the whole paper (the algorithm by alternating searches and strongly connected components, and its use for sparse matrices)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing (2009 reprint of the 1986 edition)
    locator: Chapter 4, Bipartite graphs with perfect matchings (elementary bipartite graphs and the Dulmage-Mendelsohn decomposition)
---

The Dulmage-Mendelsohn decomposition splits a [bipartite graph](/bipartite-graph/) into a part with more left than right vertices, a part with more right than left vertices, and a square part that is cut into blocks with a natural order. The split does not depend on which maximum matching is used, and it tells exactly which edges lie in some maximum matching: those inside one part or one block. It is computed by one [maximum matching](/hopcroft-karp/), two [alternating path](/alternating-path/) searches, and one pass of [strongly connected components](/strongly-connected-components/). The graph is bipartite and unweighted; the general analogue is the [Gallai-Edmonds decomposition](/gallai-edmonds-decomposition/).

## In plain words

Workers on one side, jobs on the other, and links saying who can do what. Even when you know the largest number of worker-job pairs, many plans reach it, and you may want to know what all of them have in common.

The decomposition answers that. Some workers compete for too few jobs: whichever plan you pick, one of them is idle. Some jobs have too few workers: one of them is always left undone. The rest pair up exactly, and they fall into small teams that can trade jobs inside the team but never across teams. A link between two teams, or from a team to a crowded group, is never used by any best plan. The teams can be put in a line so that links between teams only point forward.

## The problem

The input is a bipartite graph $G = (X \cup Y, E)$ with the sides given, $n = |X| + |Y|$ vertices and $m$ edges, every edge joining $X$ to $Y$. A *maximum matching* has size $\nu(G)$. An edge is *allowed* if some maximum matching contains it.

The output is a maximum matching $M$ and a partition of $V$ into

- the *X-surplus part* $V_X$: the left vertices missed by some maximum matching, with their neighbours;
- the *Y-surplus part* $V_Y$: the right vertices missed by some maximum matching, with their neighbours;
- the *square part* $V_0$, the rest, split into blocks $B_1, \ldots, B_k$, each with as many left as right vertices,

such that the allowed edges are exactly the edges inside $V_X$, inside $V_Y$, or inside one block, and every other edge between blocks goes from the left side of a block $B_i$ to the right side of a block $B_j$ with $i < j$. The parts and blocks depend only on $G$; the order of the blocks is a [topological order](/topological-sort/) of a fixed partial order. In matrix terms, with rows $X$ and columns $Y$, ordering rows and columns as $V_Y$, $B_1, \ldots, B_k$, $V_X$ gives the *block upper triangular form* of a [sparse matrix](/sparse-matrix/): no edge goes from $V_X$ or a block to an earlier part.

**Assumptions.** The graph need not be connected; isolated vertices, an empty side and parallel edges are allowed. If $G$ has a perfect matching, $V_X = V_Y = \emptyset$ and only the blocks remain.

## The algorithm

```pseudo id=main
DULMAGE-MENDELSOHN(G = (X ∪ Y, E))
L1  M ← a maximum matching of G, by Hopcroft-Karp
L2  mark the free vertices of X as in V_X;  Q ← a queue of them
L3  while Q is not empty do x ← DEQUEUE(Q)
L4      for each edge xy with y not in V_X do mark y as in V_X
L5          x' ← mate[y];  if x' is not in V_X then mark x' as in V_X;  ENQUEUE(Q, x')
L6  compute V_Y by the same search from the free vertices of Y, with the sides swapped
L7  V_0 ← V \ (V_X ∪ V_Y)
L8  H ← the digraph on X ∩ V_0 with an arc x → mate[y] for each edge xy with y ∈ V_0, y ≠ mate[x]
L9  C_1, ..., C_k ← the strongly connected components of H, in topological order
L10 B_i ← C_i ∪ mate[C_i] for i = 1, ..., k
L11 return M, V_X, (B_1, ..., B_k), V_Y
```

Line L1 uses [Hopcroft-Karp](/hopcroft-karp/). Lines L2 to L5 are a [breadth-first search](/breadth-first-search/) over alternating paths from the free left vertices: from a left vertex it follows any edge, from a right vertex only the matching edge. The right vertex $y$ reached in line L5 is matched, since otherwise the search would have found an augmenting path and $M$ would not be maximum. Line L6 is the mirror search. In line L8, the arc $x \to x'$ says that $x$ can take the partner of $x'$: $x$ is adjacent to $\text{mate}[x']$. A directed cycle of $H$ is an alternating cycle of $G$, and flipping it gives another maximum matching, so the blocks are the groups of left vertices that can swap partners in a cycle. Line L9 uses [Tarjan's algorithm](/tarjan-scc/), which emits the components in reverse topological order. All searches use explicit queues and stacks, since an alternating path can have $\Theta(n)$ vertices.

## Example

Left vertices $1, \ldots, 6$, right vertices $a, \ldots, f$, and the edges $1a$, $2a$, $3a$, $3b$, $3c$, $4b$, $4c$, $3d$, $5d$, $6d$, $6e$, $6f$.

| step | result |
|---|---|
| L1 | $M = \{1a, 3b, 4c, 5d, 6e\}$, $\nu = 5$; left 2 and right $f$ are free |
| L2 to L5 | from 2: $2 \to a \Rightarrow 1$, and 1 has no other edge; $V_X = \{1, 2, a\}$ |
| L6 | from $f$: $f \to 6 \Rightarrow e$, and $e$ has no other edge; $V_Y = \{6, e, f\}$ |
| L7 | $V_0 = \{3, 4, 5, b, c, d\}$ |
| L8 | $3 \to 4$ (edge $3c$), $3 \to 5$ (edge $3d$), $4 \to 3$ (edge $4b$); the edge $3a$ leaves $V_0$ |
| L9, L10 | $C_1 = \{3, 4\}$, $C_2 = \{5\}$; $B_1 = \{3, 4, b, c\}$, $B_2 = \{5, d\}$ |

Here $\to$ is an edge outside $M$ and $\Rightarrow$ an edge of $M$. The X-surplus part has two left vertices and one right vertex, so one of 1 and 2 is always idle; the Y-surplus part has one left vertex and two right vertices. The allowed edges are $1a$, $2a$, $3b$, $3c$, $4b$, $4c$, $5d$, $6e$, $6f$. The other three are never used: $3a$ goes from the square part to $V_X$, $3d$ goes from $B_1$ to the later block $B_2$, and $6d$ goes from $V_Y$ to the square part. As a matrix with rows in the order $6, 3, 4, 5, 1, 2$ and columns in the order $e, f, b, c, d, a$, the nonzeros form a block upper triangular pattern with diagonal blocks $\{6\} \times \{e, f\}$, $\{3, 4\} \times \{b, c\}$, $\{5\} \times \{d\}$ and $\{1, 2\} \times \{a\}$; the three unused edges are the nonzeros above the diagonal blocks.

**Edge cases.** With no edges, every left vertex is in $V_X$, every right vertex in $V_Y$, and there are no blocks. An even cycle $C_6$ is one block. A perfect matching alone, $\{1a, 2b, 3c\}$, gives three blocks of one edge each. The upper triangular pattern, edges $ij$ for $i \le j$, gives $n$ blocks of size one in the order $1, \ldots, n$. Three left vertices that share two right vertices form an X-surplus part, a set that violates [Hall's condition](/hall-theorem/).

## Correctness

The proof in the correctness file shows four facts. First, the left vertices of $V_X$ are exactly the left vertices missed by some maximum matching, and the right vertices of $V_X$ are their neighbours; symmetrically for $V_Y$; and the two searches never meet, since a common vertex would join a free left vertex to a free right vertex by an augmenting path. So $V_X$ and $V_Y$ do not depend on $M$. Second, $(X \setminus V_X) \cup (Y \cap V_X)$ is a minimum vertex cover, as in [Kőnig's theorem](/konig-theorem/), and so is its mirror; an edge with both ends in one minimum cover is in no maximum matching, which rules out every edge from the square part to $V_X$, from $V_Y$ to the square part, and from $V_Y$ to $V_X$. Third, every edge inside $V_X$ or $V_Y$ is allowed, by flipping an even alternating path or cycle. Fourth, an edge $xy \notin M$ of the square part is allowed if and only if $x$ and $\text{mate}[y]$ lie on a common directed cycle of $H$, that is, in the same strongly connected component. So the blocks are the connected components of the allowed edges inside $V_0$, which do not depend on $M$, and every edge between blocks follows an arc of $H$ between components, which goes forward in a topological order.

## Complexity

- **Matching.** Line L1 costs $O((n + m)\sqrt n)$ with Hopcroft-Karp.
- **Searches.** Each vertex enters a queue at most once per search and each edge is scanned at most twice: $O(n + m)$.
- **Components.** $H$ has at most $|X|$ nodes and $m$ arcs, built in $O(n + m)$; Tarjan's algorithm takes $O(n + m)$, and line L10 $O(n)$.
- **Total.** $O((n + m)\sqrt n)$ time, dominated by the matching, and $\Theta(n + m)$ space. Given a maximum matching, the rest is linear.

## Properties

- **Canonical.** The parts and the blocks are the same for every maximum matching; only $M$ itself and, among blocks that are not comparable, their order depend on the choices.
- **Allowed edges.** An edge is in some maximum matching if and only if it lies inside $V_X$, inside $V_Y$ or inside one block. In particular a block with $k$ left vertices is an *elementary* bipartite graph: it has a perfect matching and every one of its edges is in some perfect matching of the block.
- **Counting.** $|X \cap V_X| - |Y \cap V_X|$ equals the number of free left vertices, and $\nu(G) = |Y \cap V_X| + |V_0|/2 + |X \cap V_Y|$.
- **Gallai-Edmonds.** In a bipartite graph the [Gallai-Edmonds decomposition](/gallai-edmonds-decomposition/) has $D = (X \cap V_X) \cup (Y \cap V_Y)$, $A = (Y \cap V_X) \cup (X \cap V_Y)$ and $C = V_0$; the DM decomposition adds the blocks and their order.
- **Deterministic.** For a fixed order of the adjacency lists the output is fixed.

## Variants and improvements

- **Coarse only.** Stopping after line L7 gives the coarse decomposition, enough to find the vertices covered by every maximum matching or a minimum vertex cover.
- **Splitting the surplus parts.** The connected components of $G[V_X]$ and of $G[V_Y]$ are independent of each other, and sparse matrix codes such as Pothen and Fan's report them as separate diagonal blocks.
- **Strongly connected components by other methods.** Any linear SCC algorithm works, such as [Kosaraju-Sharir](/kosaraju-sharir/) or the path-based method of Gabow.
- **Faster matching.** The matching dominates; with an [almost-linear max flow](/almost-linear-max-flow/) the whole decomposition takes $m^{1 + o(1)}$ time.
- **Generalizations.** Murota extended the decomposition to matroids and to mixed matrices, and the Gallai-Edmonds theorem plays its role for general graphs.

## When to use it

Use it when one maximum matching is not enough: to list all allowed edges, to find the vertices that every maximum matching covers, to decide whether a sparse square system is structurally singular, or to permute a sparse matrix to block triangular form before a direct solver, so that only the diagonal blocks need factoring. It is also the standard test, in constraint programming, for pruning the values of an all-different constraint that can take part in no solution.

## Pitfalls

- **Searching in the wrong direction.** From the free left vertices the search must follow non-matching edges from left to right and matching edges from right to left; the mirror search reverses both. Mixing them produces sets that are not canonical.
- **Arc direction and order.** Tarjan's algorithm returns the components in reverse topological order. Forgetting to reverse them, or building the arcs as $\text{mate}[y] \to x$, gives a lower triangular form instead of an upper one, which is fine only if the convention is stated.
- **Using a non-maximum matching.** With a matching that is not maximum, the searches can meet and the parts overlap; L1 must produce a maximum matching.
- **Recursion depth.** Recursive Tarjan or recursive searches can go $\Theta(n)$ deep on long alternating paths; use explicit stacks.

## Implementations

The Python version takes the sizes of both sides and a list of edges $(x, y)$ and returns the matching size, the two mate arrays with $-1$ for a free vertex, the X-surplus and Y-surplus parts, and the blocks in topological order, each part given by its sorted left and right vertices. It includes an iterative Hopcroft-Karp for line L1 and an iterative Tarjan for line L9.

## History

Andrew Dulmage and Nathan Mendelsohn studied minimum coverings of bipartite graphs in 1958 and showed that they lead to a canonical decomposition; papers of 1959 and 1963 refined it and applied it to the block triangular form of matrices. The decomposition became a standard tool of sparse linear algebra, where Pothen and Fan's 1990 implementation, based on maximum matching, alternating searches and strongly connected components, is widely used. Lovász and Plummer placed it in matching theory as the bipartite companion of the Gallai-Edmonds structure theorem.

## References
