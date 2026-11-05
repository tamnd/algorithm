---
tag: GW8EF8
kind: problem
slug: spanning-tree-enumeration
name: Spanning tree enumeration problem
aliases:
- listing spanning trees
area: graphs/spanning-trees
level: advanced
summary: List all spanning trees of a graph, with polynomial delay per tree.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, N: the number of spanning trees}
  time: {worst: O(n + m + N)}
prereqs: [spanning-tree, enumeration-problem, bridge, deletion-contraction]
see_also: [gabow-myers-enumeration, counting-spanning-trees, matrix-tree-theorem, cayley-formula, reverse-search, output-sensitive-enumeration, uniform-spanning-tree-sampling, second-best-mst]
sources:
  - paper: doi:10.1002/net.1975.5.3.237
    title: Ronald C. Read and Robert E. Tarjan, Bounds on backtrack algorithms for listing cycles, paths, and spanning trees, Networks 5(3) (1975), 237-252
    locator: the whole paper (backtracking with bridge tests, O(V + E + EN) time and O(V + E) space)
  - paper: doi:10.1137/0207024
    title: Harold N. Gabow and Eugene W. Myers, Finding all spanning trees of directed and undirected graphs, SIAM Journal on Computing 7(3) (1978), 280-287
    locator: the whole paper (O(V + E + VN) time for undirected graphs, O(V + E) space)
  - paper: doi:10.1137/S009753979225030X
    title: Sanjiv Kapoor and H. Ramesh, Algorithms for enumerating all spanning trees of undirected and weighted graphs, SIAM Journal on Computing 24(2) (1995), 247-265
    locator: the whole paper (O(N + V + E) time when only the change from one tree to the next is output)
---

The spanning tree enumeration problem asks for a list of all [spanning trees](/spanning-tree/) of a graph, each exactly once. The number $N$ of trees can be exponential, up to $n^{n-2}$ for the complete graph, so algorithms are judged by their time in terms of $n$, $m$ and $N$, and by the *delay* between two outputs. Backtracking with [bridge](/bridge/) tests lists all trees in $O(n + m + nN)$ time, which is optimal when each tree is written in full, and methods that output only the change from one tree to the next reach $O(n + m + N)$. The number $N$ itself is found without listing, by the [matrix-tree theorem](/matrix-tree-theorem/).

## In plain words

You want to write down every way to connect all towns of a road map with a tree of roads, each way once. There can be very many such ways, so the goal is to spend only a small amount of work for each way you write down.

Pick a road. Every tree either uses it or does not. So list the trees that use it, then list the trees that do not, and repeat this split inside each part. A part can be empty: if dropping the road cuts the map in two, no tree avoids it. Skip empty parts, and every split leads to at least one tree. Then the work is small for each tree found.

## Definition

**Input.** A finite undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges. Parallel edges are allowed and count as different edges; self-loops are never in a tree and can be removed first. Edge weights play no role in the basic problem.

**Output.** Each spanning tree of $G$, as a set of $n - 1$ edges, exactly once, in any order.

**Connectivity.** If $G$ is not [connected](/connected-graph/), it has no spanning tree and the list is empty. The natural question is then to list its spanning forests with one tree for each component, which is the product of the lists for the components.

**Measures.** Let $N$ be the number of spanning trees. The *total time* is the time for the whole list. The *delay* is the largest time between two outputs, or before the first or after the last. The output has size $(n - 1) N$ when each tree is written in full, so a total time of $O(n + m + nN)$ is then optimal. An algorithm can also write the first tree in full and then, for each next tree, only the edges that leave and enter; the output then has size $O(n + N)$ when each change is $O(1)$ edges.

**Ordered by weight.** In the weighted form, the trees are listed in increasing order of total weight. Weights may tie, and the order among trees of equal weight is then arbitrary. Listing only the first $k$ trees of this order is the *$k$ smallest spanning trees* problem.

## Variants

- **Counting.** Find $N$ only. This is in polynomial time by the matrix-tree theorem ([counting spanning trees](/counting-spanning-trees/)).
- **Sampling.** Output one tree chosen uniformly at random ([uniform spanning tree sampling](/uniform-spanning-tree-sampling/)).
- **Changes only.** Output the first tree and then the exchange $T \to T - f + e$ that gives each next tree. Such a list exists for every connected graph: Cummins (1966) showed that the *tree graph*, whose vertices are the spanning trees and whose edges join trees that differ by one exchange, has a Hamiltonian cycle when it has at least three vertices.
- **In order of weight.** The [second-best MST](/second-best-mst/) is the second tree of this list. Each next tree is one exchange away from a tree already listed, which the methods of Gabow (1977), Katoh, Ibaraki and Mine (1981) and Eppstein (1992) use.
- **Directed graphs.** List the spanning arborescences with a fixed root. Gabow and Myers do this in $O(n + m + mN)$ time.
- **Bases of a matroid.** Spanning trees are the bases of the [graphic matroid](/graphic-matroid/). [Reverse search](/reverse-search/) lists the bases of a matroid by moving along exchanges.

## Examples

**A triangle.** With edges $x, y, z$, the three trees are $\{x, y\}$, $\{x, z\}$ and $\{y, z\}$. The split on $x$ gives the trees with $x$, namely $\{x, y\}$ and $\{x, z\}$, and the trees without $x$. Without $x$, the edges $y$ and $z$ are bridges of what remains, so the only tree is $\{y, z\}$.

**Small counts.** The cycle $C_4$ has 4 spanning trees, one for each edge left out. The complete graph $K_4$ has $4^{4-2} = 16$, by [Cayley's formula](/cayley-formula/). The square with one diagonal has 8.

**A graph with six vertices.** The graph on $a$ to $f$ with the nine edges $ab, ac, bc, bd, cd, ce, de, df, ef$ has 55 spanning trees. With the weights $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$, their weights run from 13 to 25, with these numbers of trees for each weight:

| weight | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| trees | 1 | 2 | 3 | 5 | 7 | 9 | 7 | 7 | 3 | 5 | 3 | 2 | 1 |

A list in order of weight starts with the MST $\{ac, bc, bd, ce, ef\}$, then the two trees of weight 14 in either order, since they tie.

**A disconnected graph.** Two disjoint triangles have no spanning tree, and the list is empty. They have $3 \times 3 = 9$ spanning forests with one tree in each triangle.

## Known algorithms

| algorithm | year | time | notes |
|---|---|---|---|
| All $(n-1)$-subsets of edges | | $O\big(\binom{m}{n-1} n\big)$ | test each subset; most fail |
| Binary partition with a connectivity test | | $O(m^2)$ delay | flashlight search |
| Read and Tarjan | 1975 | $O(n + m + mN)$ | backtracking with bridge tests, $O(n + m)$ space |
| [Gabow and Myers](/gabow-myers-enumeration/) | 1978 | $O(n + m + nN)$ | depth-first growth, reuse of the last tree; optimal for full output |
| Kapoor and Ramesh | 1995 | $O(n + m + N)$ | outputs changes; also the weighted order |
| Shioura, Tamura and Uno | 1997 | $O(n + m + N)$ | outputs changes, $O(n + m)$ space, by reverse search |

**Binary partition.** Keep a set $I$ of edges that each tree must contain and a set $X$ of edges that no tree may contain. Start with $I = X = \emptyset$. At a node, pick an edge $e$ outside $I \cup X$ that does not close a cycle with $I$. Recurse on $I + e$; then, if $G - X - e$ is still connected, recurse on $X + e$. When $I$ has $n - 1$ edges, output it. Each node has at least one tree below it, because $I$ is a forest and $G - X$ is connected, so some spanning tree of $G - X$ contains $I$. The depth is at most $m$, so the delay is $O(m)$ connectivity tests, each in $O(n + m)$ time. Contracting the edges of $I$ and deleting the edges of $X$, as in [deletion-contraction](/deletion-contraction/), keeps the graph small.

**Bridge tests.** The test "is $G - X - e$ connected" asks whether $e$ is a bridge of $G - X$. Read and Tarjan and Gabow and Myers organize the search so that these tests share work, and Gabow and Myers bound the total cost by $O(n)$ for each tree.

## Bounds

**Lower bound.** Each algorithm must read the input and write the output, so it takes $\Omega(n + m + nN)$ time with full output and $\Omega(n + m + N)$ with output of changes. The algorithms of Gabow and Myers, Kapoor and Ramesh, and Shioura, Tamura and Uno meet these bounds.

**The size of $N$.** For a connected simple graph, $1 \le N \le n^{n-2}$, with $N = 1$ exactly for trees and $N = n^{n-2}$ exactly for $K_n$. With parallel edges, $N$ can be larger.

**Delay.** The binary partition gives polynomial delay, $O(m(n + m))$. The bounds of the table for the later algorithms are on the total time, which is a weaker guarantee than the same bound on the delay.

## Reductions

- **Counting from enumeration.** Count the output, in $O(n + m + N)$ time. The matrix-tree theorem is much faster when $N$ is large.
- **Spanning forests to spanning trees.** List the spanning trees of each component and output each combination, or add a new vertex joined to one vertex of each component and remove those edges from each tree.
- **Enumeration in order of weight to repeated second-best search.** Lawler's partition method splits the remaining trees into classes by fixed and forbidden edges and finds the best tree in each class with an MST algorithm.

## Applications

- **Network reliability.** The probability that a network with random edge failures stays connected is a sum over its connected spanning subgraphs; spanning trees give bounds and exact methods for small networks.
- **Electrical circuits.** Kirchhoff expressed the currents in a network as sums over its spanning trees, which is the origin of the matrix-tree theorem.
- **Search with side constraints.** When an extra condition, such as a degree bound, rules out most trees, listing the trees in order of weight finds the best one that meets the condition.
- **Testing.** Listing all trees of small graphs gives oracles for MST, counting and sampling algorithms.

## References
