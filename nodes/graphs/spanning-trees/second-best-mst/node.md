---
tag: 3Q5221
kind: problem
slug: second-best-mst
name: Second-best minimum spanning tree problem
aliases:
- second-minimum spanning tree
area: graphs/spanning-trees
level: advanced
summary: Find the spanning tree with the smallest weight strictly above the minimum.
model: comparison-model
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: "O(m log n)"}
prereqs: [minimum-spanning-tree, mst-optimality-conditions, fundamental-cycle, exchange-argument]
see_also: [mst-sensitivity-analysis, mst-verification, mst-uniqueness, binary-lifting, kruskal, prim, k-shortest-paths, matroid]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Problem 21-1, Second-best minimum spanning tree
  - paper: doi:10.1137/0221070
    title: Brandon Dixon, Monika Rauch and Robert E. Tarjan, Verification and sensitivity analysis of minimum spanning trees in linear time, SIAM Journal on Computing 21(6) (1992), 1184-1192
    locator: the path-maximum values for the non-tree edges, from which the best single exchange follows
---

The second-best minimum spanning tree problem asks for a spanning tree whose weight is the least value strictly above the weight of a [minimum spanning tree](/minimum-spanning-tree/). The key fact is that one exchange is enough: for each MST $T$, some second-best tree has the form $T - f + e$, where $e$ is a non-tree edge and $f$ is an edge on the tree path between the ends of $e$. So the problem reduces to path-maximum queries on $T$, and it takes $O(m \log n)$ time with [binary lifting](/binary-lifting/), or $O(n^2)$ time by a search from each vertex. A second form of the problem asks only for a tree different from a given MST, which can have the same weight when weights tie.

## In plain words

You have found the cheapest network of cables. Now you want the next cheapest one, with a strictly higher price, for example as a backup plan.

You do not need to search all networks. Take the cheapest one, add one cable that it does not use, and remove one cable from the loop that this creates. Among all such swaps, pick the one that raises the price by the least amount above zero. That gives a next cheapest network. The work is to find, for each unused cable, the best cable to remove from its loop, which a good table of the tree makes fast.

## Definition

**Input.** A finite, [connected](/connected-graph/), undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, and a weight $w(e) \in \mathbb{R}$ on each edge. Weights may tie. Parallel edges and self-loops are allowed.

**Output.** Let $w^*$ be the weight of an MST, and let $w_2$ be the least weight of a spanning tree with weight greater than $w^*$. The output is a spanning tree of weight $w_2$, or NONE if every spanning tree has weight $w^*$. A **second-best MST** is such a tree.

**The other form.** CLRS (Problem 21-1) fixes an MST $T$ and asks for a spanning tree $T' \ne T$ of least weight. When the MST is unique the two forms agree. With ties, the other form may return another MST, of weight $w^*$, while the form above skips all MSTs.

**Disconnected graphs.** A disconnected graph has no spanning tree. For spanning forests, the same question has the same answer in each component, and the second-best forest changes only the component with the cheapest exchange.

**The exchange theorem.** Let $T$ be any MST. For $e = uv \notin T$, let $P_T(e)$ be the path from $u$ to $v$ in $T$. Then

$$w_2 = w^* + \min \{\, w(e) - w(f) : e \notin T,\ f \in P_T(e),\ w(e) > w(f) \,\},$$

and NONE is the answer when the set is empty.

*Proof.* Each $T - f + e$ with $f \in P_T(e)$ is a spanning tree, so the right side is at least $w_2$ when the set is not empty. For the other direction, let $T'$ be a tree of weight $w_2$ that has the most edges in common with $T$. Since $w(T') > w^*$, $T' \ne T$, so some $f \in T \setminus T'$ exists. Removing $f$ from $T$ leaves two trees with vertex sets $S$ and $V \setminus S$. The cycle that $f$ closes in $T'$ crosses this cut at $f$, and a cycle crosses a cut an even number of times, so it has another edge $e \in T'$ that crosses it. The only edge of $T$ across the cut is $f$, so $e \notin T$, and $f \in P_T(e)$. Both $T - f + e$ and $T' - e + f$ are spanning trees, and with $d = w(e) - w(f)$,

$$w(T - f + e) = w^* + d, \qquad w(T' - e + f) = w_2 - d.$$

The first is at least $w^*$, so $d \ge 0$. If $d = 0$, then $T' - e + f$ has weight $w_2$ and one more edge in common with $T$, which contradicts the choice of $T'$. So $d > 0$. Then $w_2 - d < w_2$, and no tree has weight strictly between $w^*$ and $w_2$, so $w_2 - d = w^*$, that is, $d = w_2 - w^*$. So the pair $(e, f)$ is in the set and attains $w_2$. If no tree is heavier than $w^*$, the set is empty, because each pair in it would give one. $\square$

The proof works for any MST $T$, so the algorithm may start from the MST that any MST algorithm returns.

## Variants

- **Different from a given MST.** Allow $d = 0$ in the minimum. Then the answer is $w^* + \min_{e \notin T} (w(e) - \operatorname{max}_T(e))$, where $\operatorname{max}_T(e)$ is the largest weight on $P_T(e)$. This is exactly the data of [MST sensitivity analysis](/mst-sensitivity-analysis/).
- **Distinct weights.** All values $w(e) - \operatorname{max}_T(e)$ are then positive, the MST is unique, and both forms coincide.
- **The $k$ smallest spanning trees.** List the spanning trees in increasing order of weight. The exchange idea extends: each next tree is one exchange away from some tree already listed, as in the methods of Gabow (1977) and Eppstein (1992). This parallels the [$k$ shortest paths](/k-shortest-paths/) problem.
- **Matroids.** The exchange theorem holds for bases of every [matroid](/matroid/), with the same proof by the symmetric exchange property.

## Examples

**A graph with six vertices.** Take the vertices $a$ to $f$ and these nine edges.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

The MST $T = \{ac, bc, bd, ce, ef\}$ has weight 13. The best exchange for each non-tree edge:

| non-tree edge $e$ | path $P_T(e)$ | best $f$ | $d = w(e) - w(f)$ | tree |
|---|---|---|---|---|
| $ab$ (4) | $ac, bc$ | $ac$ (3) | 1 | $\{ab, bc, bd, ce, ef\}$ |
| $cd$ (4) | $bc, bd$ | $bd$ (2) | 2 | $\{ac, bc, cd, ce, ef\}$ |
| $de$ (7) | $bd, bc, ce$ | $ce$ (5) | 2 | $\{ac, bc, bd, de, ef\}$ |
| $df$ (6) | $bd, bc, ce, ef$ | $ce$ (5) | 1 | $\{ac, bc, bd, df, ef\}$ |

So $w_2 = 14$, and two second-best trees exist. A full count confirms it: of the 55 spanning trees, one has weight 13 and two have weight 14, the two in the table.

**Ties.** In the triangle with weights $1, 2, 2$, the MSTs are the two trees that hold the edge of weight 1, both of weight 3. Take $T$ as one of them. The non-tree edge of weight 2 has the path with weights $1$ and $2$. The exchange with the edge of weight 2 gives $d = 0$ and another MST, which the other form returns. The exchange with the edge of weight 1 gives $d = 1$ and the tree of the two edges of weight 2, of weight 4, which is the second-best MST.

**All weights equal.** In the cycle $C_4$ with four edges of weight 1, each spanning tree has weight 3, so the answer is NONE. The other form returns another tree of weight 3.

**A tree.** If $G$ is itself a tree, it has one spanning tree and the answer is NONE.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| Brute force over all trees | exponential | the oracle for tests |
| Exchange over all pairs, path by path | $O(n m)$ | after an MST |
| Tables of path maxima by a search from each vertex | $O(n^2)$ | after an MST; CLRS Problem 21-1 |
| [Binary lifting](/binary-lifting/) with the two largest distinct weights | $O(m \log n)$ | handles ties |
| Path maxima by MST verification | $O(m)$ | after an MST; for the other form or for distinct weights |

**Search from each vertex.** For each vertex $u$, a [graph traversal](/graph-traversal/) of $T$ from $u$ fills $\operatorname{max}[u][v]$, the heaviest weight on the path from $u$ to $v$, for all $v$ in $O(n)$ time. Then each non-tree edge is checked in $O(1)$ time.

**Binary lifting with ties.** When $w(e) = \operatorname{max}_T(e)$, the heaviest edge of the path gives $d = 0$, and the strict form needs the largest weight on the path that is less than $w(e)$. So for each jump of length $2^i$, store the largest weight and the largest weight different from it. A query combines $O(\log n)$ such pairs, and for each non-tree edge it uses the largest stored value below $w(e)$.

The whole problem takes the time of one MST computation plus the time of the queries.

## Bounds

**Lower bound.** An algorithm must examine every edge that is not a [bridge](/bridge/) or a self-loop, by the adversary argument of the [MST lower bound](/mst-lower-bound/), so $\Omega(m)$ time is needed.

**Upper bound.** With distinct weights, or in the other form, the second-best MST takes one MST computation plus $O(m)$, since the path maxima come from linear-time [MST verification](/mst-verification/). In the strict form with ties, the binary lifting method gives $O(m \log n)$.

**Many second-best trees.** The number of second-best trees can be large, but one of them is always a single exchange from any fixed MST, so the output is found without listing them.

## Reductions

- **Second-best MST to path-maximum queries.** One query for each non-tree edge, by the exchange theorem.
- **Second-best MST to sensitivity analysis.** In the other form, the minimum over tree edges $f$ of $\operatorname{cov}_T(f) - w(f)$ is the least increase.
- **Uniqueness to the other form.** The MST is unique if and only if the other form returns a tree heavier than $w^*$, which is the strict test of [MST uniqueness](/mst-uniqueness/).

## Applications

- **Backup networks.** A second network, nearly as cheap, for use when the first is not possible.
- **Ranking solutions.** The first step of listing spanning trees in increasing order of weight, used when side constraints rule out the best tree.
- **Uniqueness tests.** A gap $w_2 - w^*$ that is small shows that the optimum is fragile under small changes of the weights.

## References
