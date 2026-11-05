---
tag: 2JVBPG
kind: problem
slug: maximum-independent-set-in-trees
name: Maximum independent set in trees
aliases:
- Independent sets in trees
area: graphs/tree-algorithms
level: core
summary: Finds the largest set of tree vertices with no two adjacent, solved by dynamic programming over rooted subtrees in linear time.
prereqs: [independent-set, tree, tree-dynamic-programming]
see_also: [independent-set-on-trees, company-party-planning, maximum-independent-set, vertex-cover, konig-theorem, maximum-matching, dp-on-tree-decompositions, treewidth]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 10.2, Solving NP-Hard Problems on Trees (the leaf lemma and the greedy algorithm for the unweighted case, and the dynamic program for the weighted case)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 6, Section 6.7, Independent sets in trees
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 14, Dynamic Programming, the end-of-chapter problem Planning a company party
---

The maximum independent set problem in trees asks for a largest set of vertices of a [tree](/tree/) such that no two of them are joined by an edge, or, with weights on the vertices, for an [independent set](/independent-set/) of largest total weight. On general graphs the problem is NP-hard, but on a tree it takes $\Theta(n)$ time, by a [dynamic program over the rooted subtrees](/independent-set-on-trees/) or, in the unweighted case, by a greedy rule that takes the leaves first. It is the standard first example of an NP-hard problem that becomes easy on a restricted class of graphs.

## In plain words

Some points are joined by lines in the shape of a tree: there is exactly one way to go from any point to any other point. You want to pick as many points as you can, but never two points that are joined by a line. In the second form of the problem, each point has a value and you want the biggest total value.

On a general network this is one of the hard problems with no known fast method. A tree is different. If you hang it from one point, each point and the part below it touch the rest only through that one point. So you can solve each part on its own, from the bottom up, and the answer for a part depends only on whether its top point is picked.

## Definition

**Input.** A tree $T = (V, E)$ with $V = \{0, \ldots, n-1\}$, $n \ge 1$, and $|E| = n - 1$. The tree is unrooted. In the weighted form, there is also a weight $w(v) \in \mathbb{Z}$ for each vertex (or a real number); the unweighted form is $w \equiv 1$.

**Output.** A set $S \subseteq V$ such that $\{u, v\} \not\subseteq S$ for each edge $\{u, v\} \in E$, that maximizes $w(S) = \sum_{v \in S} w(v)$. The maximum size in the unweighted form is the *independence number* $\alpha(T)$.

The empty set is always independent, so the optimum is at least 0, even with negative weights.

## Variants

- **Value only or set.** Return only $\alpha(T)$ or the optimal weight, or also a set that reaches it. The same dynamic program gives both.
- **Decision.** Given $k$, is there an independent set of weight at least $k$? On trees it is answered by computing the optimum.
- **Forest.** Solve each tree of the forest and add the results.
- **A vertex forced in or out.** For example the root must be in the set, as when the president must attend the [company party](/company-party-planning/). Then the answer is $A(r)$ of the dynamic program, not $\max(A(r), B(r))$.
- **Counting.** Count the independent sets of a tree. The same two-state recurrence works with sums and products in place of max and sum: $A(v) = \prod_c B(c)$ and $B(v) = \prod_c (A(c) + B(c))$. A path with $n$ vertices has $F_{n+2}$ independent sets, where $F$ is the Fibonacci sequence with $F_1 = F_2 = 1$.
- **Graphs that are almost trees.** On a graph of [treewidth](/treewidth/) $k$, the problem takes $2^k k^{O(1)} n$ time given a tree decomposition of width $k$, by [DP on tree decompositions](/dp-on-tree-decompositions/).

## Examples

The tree has 8 vertices with the parent array $[-, 0, 0, 1, 1, 2, 2, 4]$ when rooted at 0, so the edges are $01, 02, 13, 14, 25, 26, 47$. With weights $w = [6, 7, 2, 3, 4, 5, 1, 8]$, the optimum is 23, reached by $\{0, 3, 5, 6, 7\}$. With all weights 1, $\alpha = 5$, and the same set reaches it. The tree has 64 independent sets in all.

| tree | $n$ | $\alpha$ | a maximum set | number of independent sets |
|---|---|---|---|---|
| one vertex | 1 | 1 | $\{0\}$ | 2 |
| path $0 - 1 - \cdots - (n-1)$ | $n$ | $\lceil n/2 \rceil$ | the even vertices | $F_{n+2}$ |
| star with center 0 | $n \ge 2$ | $n - 1$ | all leaves | $2^{n-1} + 1$ |
| the 8-vertex tree above | 8 | 5 | $\{0, 3, 5, 6, 7\}$ | 64 |

For the path, $\lceil n/2 \rceil$ is also an upper bound: the $\lfloor n/2 \rfloor$ disjoint edges $\{0, 1\}, \{2, 3\}, \ldots$ each hold at most one chosen vertex, and for odd $n$ one vertex is left over. With weights, the star shows that the answer can be the center alone: with $w(0) = 100$ and nine leaves of weight 1 the optimum is 100.

A non-example of a greedy rule: picking the heaviest vertex and deleting its neighbors, over and over, gives $\{7, 1, 5, 6\}$ with weight 21 on the weighted example above, not 23.

## Known algorithms

- **[Dynamic programming on the rooted tree](/independent-set-on-trees/).** Two values per vertex, the best weight of its subtree with the vertex in and with it out. $\Theta(n)$ time and memory, for any integer or real weights. This is the general method.
- **Leaf greedy (unweighted).** Each tree with at least one edge has a leaf, and some maximum independent set contains a given leaf (Kleinberg and Tardos, Section 10.2). So: take a leaf, delete it and its neighbor, and repeat on the forest that is left. With a queue of current leaves this runs in $O(n)$ time.
- **Through matching (unweighted).** A tree is a [bipartite graph](/bipartite-graph/), so by [König's theorem](/konig-theorem/) the minimum vertex cover has the size $\nu$ of a [maximum matching](/maximum-matching/), and $\alpha = n - \nu$. A maximum matching of a tree is found greedily from the leaves in $O(n)$ time.

## Bounds

The problem takes $\Theta(n)$ time on a word RAM with $O(1)$-word weights: the dynamic program gives $O(n)$, and any algorithm must read each weight, since changing a single weight can change the answer. For general graphs the decision form is NP-complete, so the tree structure is what makes the problem easy.

## Reductions

- **Vertex cover.** $S$ is independent if and only if $V \setminus S$ is a [vertex cover](/vertex-cover/). So a maximum-weight independent set and a minimum-weight vertex cover are complements, on any graph; on trees both take $O(n)$ time.
- **Matching, unweighted.** As above, $\alpha(T) = n - \nu(T)$ on trees and on all bipartite graphs.
- **From the company party.** The [company party](/company-party-planning/) problem is this problem on the tree of the company, with the conviviality ratings as weights.
- **To treewidth DP.** A tree has treewidth 1, and the tree algorithm is the case $k = 1$ of the DP on a tree decomposition.

## Applications

- **Planning under a hierarchy.** Choose people, offices or tasks from a hierarchy so that no item is chosen with its direct parent; the [company party](/company-party-planning/) is the textbook case.
- **Placing facilities on a tree network.** Place stations at vertices of a tree-shaped network, such as a pipe or road network without loops, so that no two stations are adjacent and the total value is largest.
- **A subroutine for harder graphs.** Algorithms for graphs of small treewidth, and some heuristics for general graphs, solve tree-like pieces with this dynamic program.
- **A teaching example.** It shows how a problem that is NP-hard in general can be solved exactly on a class of inputs with a simple structure.

## References
