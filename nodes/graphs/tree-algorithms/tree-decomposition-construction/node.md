---
tag: EC5HWV
kind: algorithm
slug: tree-decomposition-construction
name: Constructing a tree decomposition
area: graphs/tree-algorithms
level: advanced
summary: Builds a tree decomposition of small width for a graph, or reports that the width exceeds a given bound.
solves: [treewidth-computation]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the width bound}
  time: {worst: O(27^k k^2 n^2), best: O(n + m)}
  space: {extra: O(k n)}
properties: {deterministic: true, recursive: false}
prereqs: [tree-decomposition, treewidth, max-flow-min-cut-theorem]
see_also: [treewidth-computation, nice-tree-decomposition, dp-on-tree-decompositions, path-decomposition, fixed-parameter-tractable, menger-theorem, chordal-graph, courcelle-theorem]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 7 (Treewidth), the section on computing treewidth, the balanced separator lemma and the algorithm that outputs a tree decomposition of width at most 4k + 4 or reports that the treewidth exceeds k
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 10.5 (Constructing a tree decomposition), the recursive construction by balanced separators of a set of boundary vertices
  - paper: Neil Robertson and Paul D. Seymour, Graph minors. XIII. The disjoint paths problem, Journal of Combinatorial Theory, Series B 63(1), 65 to 110 (1995)
    locator: the approximation algorithm for tree decompositions by balanced separators, with running time quadratic in n for fixed k
  - paper: Hans L. Bodlaender, A linear-time algorithm for finding tree-decompositions of small treewidth, SIAM Journal on Computing 25(6), 1305 to 1317 (1996)
    locator: the exact algorithm that decides treewidth at most k and builds a decomposition in linear time for each fixed k
---

This algorithm takes a graph $G$ and a number $k$, and either builds a [tree decomposition](/tree-decomposition/) of $G$ of width at most $4k + 4$, or proves that the [treewidth](/treewidth/) of $G$ is larger than $k$. It grows the decomposition from the root down. Each bag is a boundary set $S$ plus a small set $Y$ that splits $S$ in a balanced way, and each part left over becomes a subproblem whose boundary is again small. The separators are found by trying the splits of $S$ and running a unit-capacity flow, so the running time is $O(27^k k^2 n^2)$: exponential only in $k$, which makes the method a [fixed-parameter](/fixed-parameter-tractable/) approximation. It is the usual first step before a [dynamic program over a tree decomposition](/dp-on-tree-decompositions/).

## In plain words

A tree decomposition covers a graph with small overlapping groups of vertices arranged as a tree. To build one, cut the graph again and again along small sets of vertices.

Take a part of the graph that is still open, and the vertices on its border. If the border is small, put it and one more vertex of the part into a new group. If the border has grown big, look for a few vertices whose removal splits the border into two halves that cannot reach each other. Put the border and these vertices into a new group. Each piece left touches only half of the old border plus the new vertices.

If the graph is close to a tree, a good split always exists. So if none is found, the algorithm can say that the graph is far from a tree.

## The problem

The input is a simple undirected graph $G = (V, E)$ with the vertices $0, \ldots, n-1$, given as an edge list, and an integer $k \ge 0$. It is not weighted, and the numbers of the vertices only fix the order of the choices. The output is either "treewidth larger than $k$", which must be true, or a tree decomposition: bags $B_0, B_1, \ldots$ joined in a forest that is one tree per component of $G$, such that every vertex and every edge lies in a bag, the bags that hold a vertex form a connected subtree, and every bag has at most $4k + 5$ vertices. If the treewidth is at most $k$, the second answer must be given. This is a 4-approximation of [treewidth computation](/treewidth-computation/), up to an additive constant.

## The algorithm

A *task* $(C, S)$ is a nonempty connected vertex set $C$ together with $S = N(C)$, the vertices outside $C$ with a neighbour in $C$. The task asks for a decomposition of $G[C \cup S]$ whose root bag contains $S$.

```pseudo id=main
DECOMPOSE(G, k)
L1  if |E| > k·n then return "treewidth > k"
L2  push the task (C, ∅, none) for each connected component C of G
L3  while the stack is not empty do
L4      pop a task (C, S, parent)
L5      if |S| < 3k + 4 then B ← S ∪ {one vertex of C}
L6      else find a split of S into S_A, S_X, S_B with |S_X| ≤ k + 1, |S_A| ≤ 2k + 2, |S_B| ≤ 2k + 2,
             and a set Y ⊆ C with |Y| ≤ k + 1 − |S_X| that meets every path from S_A to S_B in G[C ∪ S] − S_X
L7          if there is no such split then return "treewidth > k"
L8          B ← S ∪ Y
L9      add a node with the bag B, joined to parent
L10     for each connected component D of G[C \ B] do
L11         push the task (D, N(D), this node)
L12 return the bags and the tree edges
```

Line L6 tries the splits: each $S_X \subseteq S$ of size at most $k + 1$, then each way to cut the rest into $S_A$ and $S_B$. For one split, $Y$ is a minimum vertex cut between $S_A$ and $S_B$ in $G[C \cup S] - S_X$ in which only vertices of $C$ may be cut. It is found by a maximum flow with capacity 1 on each vertex of $C$ and no limit on $S_A \cup S_B$, stopped after $k + 2 - |S_X|$ augmenting paths, as in [Menger's theorem](/menger-theorem/). Line L1 uses the fact that a graph of treewidth at most $k$ has at most $kn$ edges.

## Example

**Small boundaries only.** Take the strip of triangles with the edges $01, 02, 12, 13, 23, 24, 34, 35, 45$ and $k = 2$. The boundary never reaches $3k + 4 = 10$, so line L5 is used each time, and the order of the stack gives the bags $\{0\}$, $\{0, 1\}$, $\{0, 1, 2\}$, $\{1, 2, 3\}$, $\{2, 3, 4\}$, $\{3, 4, 5\}$ on a path. The width is $2$, which is the treewidth. With $k = 0$, line L1 stops at once, since there are $9 > 0$ edges.

**A balanced split.** Take $k = 1$ and the spider with the centre $16$, the middle vertices $8, \ldots, 15$, and the tips $0, \ldots, 7$, with the edges $\{i, 8 + i\}$ and $\{8 + i, 16\}$. The implementation takes the smallest vertex of $C$ at line L5.

| task | $S$ | line | new bag | tasks pushed |
|---|---|---|---|---|
| 1 | $\emptyset$ | L5 | $\{0\}$ | the rest, with $S = \{0\}$ |
| 2 to 7 | $\{0\}, \ldots, \{0, \ldots, 5\}$ | L5 | $S \cup \{1\}, \ldots, S \cup \{6\}$ | the rest, with $S = \{0, \ldots, 6\}$ |
| 8 | $\{0, \ldots, 6\}$, size $7 = 3k + 4$ | L6, L8 | $\{0, \ldots, 6, 16\}$ | the legs $\{8\}, \ldots, \{14\}$ and $\{7, 15\}$ |
| 9 to 15 | $\{i, 16\}$ for a leg $\{8 + i\}$ | L5 | $\{i, 8 + i, 16\}$ | none |
| 16, 17 | $\{16\}$, then $\{7, 16\}$ | L5 | $\{7, 16\}$, then $\{7, 15, 16\}$ | the leg $\{15\}$, then none |

At task 8, line L6 finds $S_X = \emptyset$, $S_A = \{0, 1, 2\}$, $S_B = \{3, 4, 5, 6\}$ and $Y = \{16\}$: every path from a tip in $S_A$ to a tip in $S_B$ passes through the centre. Each leg then sees only its own tip and the centre. The largest bag has $8 \le 4k + 5$ vertices. The tree has treewidth 1, so the algorithm must not fail, and it does not.

**The small cases.** A single vertex gives one bag $\{0\}$. A path with $k = 1$ and a star with $k = 1$ never reach a boundary of size 7, so only line L5 is used; the result is valid but can have bags larger than 2. The complete graph $K_5$ with $k = 1$ has $10 > 5$ edges and is rejected at line L1.

## Correctness

Every bag contains its task's boundary $S$, and each child task $(D, N(D))$ has $N(D) \subseteq B$, because the neighbours of $D$ outside $C \setminus B$ are in $B$ or in $S \subseteq B$. A vertex of $C$ appears first in exactly one bag, and later only in bags below that node, through boundaries, so the bags that hold it form a subtree. Every edge lies inside some $C \cup S$ and ends in a bag. When $|S| = 3k + 4$, each child boundary lies in $S_A \cup Y$ or in $S_B \cup Y$, so it has at most $2k + 2 + k + 1 = 3k + 3$ vertices, and the boundaries never exceed $3k + 4$; the bags never exceed $4k + 5$. If the treewidth is at most $k$, a set of $k + 1$ vertices splits any $S$ so that no part holds more than half of it, and the parts can be grouped into two sides of at most $2k + 2$ each, so line L7 never fires. Each task adds a vertex of $C$ to its bag, so the loop ends after at most $n$ tasks. The full proof is below.

## Complexity

- **Tasks.** Each task puts at least one vertex of $C$ into its bag, and that vertex is in no later $C$, so there are at most $n$ tasks.
- **One split.** Building the flow network on $G[C \cup S]$ costs $O(n + m)$, and at most $k + 2$ augmenting paths cost $O(k(n + m))$. After line L1, $m \le kn$, so this is $O(k^2 n)$.
- **Splits per task.** Each vertex of $S$, with $|S| = 3k + 4$, goes to $S_A$, $S_X$ or $S_B$, so there are at most $3^{3k+4} = 81 \cdot 27^k$ splits.

The worst case is $O(27^k k^2 n^2)$ time. When the boundaries stay small, as on paths and stars, no split is tried and each task costs $O(n + m)$, so the time is $O(n(n + m))$; the best case, a graph with no edges, is $O(n)$. The extra space is $O(n + m) = O(kn)$ for the graph, the flow network and the stack, plus the bags.

## Properties

- **Width.** At most $4k + 4$, so if $\mathrm{tw}(G) = k$ and the algorithm is run with $k, k+1, \ldots$ from $0$, the first success gives width at most $4\,\mathrm{tw}(G) + 4$.
- **One-sided answer.** "Treewidth $> k$" is always true. A decomposition can be returned even when the treewidth is larger than $k$, as long as the splits exist.
- **Size.** At most $n$ bags, joined in a forest with one tree per component of $G$.
- **Deterministic and not recursive.** The tasks are kept on an explicit stack, so a path of thousands of vertices does not overflow the call stack.
- **Root bag.** The first bag of each component holds one vertex. Any bag can be made the root, which a [nice tree decomposition](/nice-tree-decomposition/) needs.

## Variants and improvements

- **Better enumeration.** Choosing the split of $S$ into two sides first, and putting the vertices of $S$ into the separator through the flow, lowers the base of the exponent; Cygan and his coauthors state a running time of the form $O(8^k k^2 n^2)$.
- **Linear time in $n$.** Reed gave an $O(n \log n)$ algorithm for fixed $k$. Bodlaender's algorithm decides $\mathrm{tw}(G) \le k$ exactly and builds an optimal decomposition in time linear in $n$ for each fixed $k$, with a factor of the form $2^{O(k^3)}$. Bodlaender, Drange, Dregi, Fomin, Lokshtanov and Pilipczuk gave a 5-approximation in $2^{O(k)} n$ time, and Korhonen a 2-approximation in $2^{O(k)} n$ time.
- **Heuristics.** Greedy elimination orderings, such as minimum degree or minimum fill-in, build a decomposition of a [chordal](/chordal-graph/) supergraph quickly, with no guarantee on the width. They are the usual choice in practice.
- **Path decompositions.** The same separator idea, with the boundary split into a left and a right part, gives [path decompositions](/path-decomposition/).

## When to use it

Use it when a guaranteed bound is needed: to run a [dynamic program over a tree decomposition](/dp-on-tree-decompositions/) whose cost is exponential in the width, or to apply [Courcelle's theorem](/courcelle-theorem/), with a proof that the graph has small treewidth. It is simple enough to implement and test. For large graphs with a small width in practice, use a fast heuristic first and this method only to certify or to bound the width. When the exact width matters, use Bodlaender's algorithm or an exact search, since a factor of 4 in the width is a large factor in a cost that is exponential in it.

## Pitfalls

- **Forgetting the boundary in the child bag.** The root bag of each child task must contain all of $N(D)$, not only the vertices of $D$. Otherwise a vertex of the boundary has bags in two places that are not joined.
- **Cutting boundary vertices in the flow.** Only vertices of $C$ may be cut; the vertices of $S$ in the cut are chosen as $S_X$. If the flow can cut $S_A$ or $S_B$, the sides of the split change and the size bound on the child boundaries fails.
- **The threshold.** With $|S| = 3k + 3$ instead of $3k + 4$, a split can put all of $S \setminus Y$ on one side, $Y$ can avoid $C$, and the algorithm stops making progress.
- **Reading a success as a bound.** A decomposition of width $4k + 4$ does not show that the treewidth is at most $k$; only the failure answer is exact.
- **Recursion.** A recursive version goes as deep as the number of bags on a root path, which is $n$ on a path. Use an explicit stack.

## Implementations

## History

Robertson and Seymour introduced treewidth in their graph minors series and gave the first algorithm of this kind, which for a fixed $k$ either finds a decomposition of width $O(k)$ or shows that the treewidth exceeds $k$, in time quadratic in $n$. Kleinberg and Tardos present a version of it in their textbook, and Cygan and coauthors give the form with width $4k + 4$. Arnborg, Corneil and Proskurowski showed in 1987 that deciding treewidth is NP-complete when $k$ is part of the input. Reed lowered the time to $O(n \log n)$ for fixed $k$ in 1992, and Bodlaender in 1996 gave the exact linear-time algorithm for fixed $k$. Approximations with single-exponential dependence on $k$ and linear dependence on $n$ followed in 2016 and 2021.

## References
