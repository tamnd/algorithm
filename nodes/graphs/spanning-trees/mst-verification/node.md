---
tag: SVQ0EP
kind: problem
slug: mst-verification
name: MST verification
aliases:
- minimum spanning tree verification
area: graphs/spanning-trees
level: advanced
summary: Decide whether a given spanning tree is a minimum spanning tree; linear time is possible.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(m)}
prereqs: [minimum-spanning-tree, mst-optimality-conditions, fundamental-cycle, lowest-common-ancestor]
see_also: [mst-sensitivity-analysis, karger-klein-tarjan-mst, mst-lower-bound, second-best-mst, binary-lifting, cycle-property, tarjan-offline-lca, mst-uniqueness]
sources:
  - paper: doi:10.1007/BF02579443
    title: János Komlós, Linear verification for spanning trees, Combinatorica 5(1) (1985), 57-65
    locator: the whole paper (O(m) comparisons for the path-maximum queries)
  - paper: doi:10.1137/0221070
    title: Brandon Dixon, Monika Rauch and Robert E. Tarjan, Verification and sensitivity analysis of minimum spanning trees in linear time, SIAM Journal on Computing 21(6) (1992), 1184-1192
    locator: the whole paper (the first linear-time algorithm)
  - paper: doi:10.1007/BF02526037
    title: Valerie King, A simpler minimum spanning tree verification algorithm, Algorithmica 18(2) (1997), 263-270
    locator: the whole paper (reduction to a full branching tree by Borůvka steps, then Komlós's method with table lookups)
  - paper: doi:10.1145/322154.322161
    title: Robert E. Tarjan, Applications of path compression on balanced trees, Journal of the ACM 26(4) (1979), 690-715
    locator: the application to verification of minimum spanning trees, O(m α(m, n)) time
---

MST verification asks whether a given spanning tree of a weighted graph is a [minimum spanning tree](/minimum-spanning-tree/). By the [optimality conditions](/mst-optimality-conditions/), the answer is yes exactly when each edge outside the tree is at least as heavy as every edge on the tree path between its ends, so the problem reduces to one path-maximum query on the tree for each non-tree edge. Komlós showed that $O(m)$ comparisons suffice, and Dixon, Rauch and Tarjan, and later King, gave $O(m)$-time algorithms on the [word RAM](/word-ram/). Verification is thus provably linear, while the deterministic complexity of finding an MST is still open, and the [Karger-Klein-Tarjan algorithm](/karger-klein-tarjan-mst/) uses it as a filter.

## In plain words

Someone hands you a network of cables and claims that it is the cheapest one that connects all houses. You want to check the claim without building your own network.

Take each cable that the network does not use. In the network, its two ends are joined by a route. If some cable on that route costs more than the unused cable, swap them: the network stays connected and gets cheaper, so the claim was false. If no unused cable allows such a swap, the claim is true. So the check is: for each unused cable, find the most expensive cable on the route between its ends. Done with care, all these checks together take time proportional to the number of cables.

## Definition

**Input.** A finite, [connected](/connected-graph/), undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, a weight $w(e) \in \mathbb{R}$ on each edge, and a set $T \subseteq E$. Weights may tie. Parallel edges and self-loops are allowed.

**Output.** Yes if $(V, T)$ is a [spanning tree](/spanning-tree/) of minimum total weight, and no otherwise.

**The test.** First check that $T$ has $n - 1$ edges and no cycle, which takes $O(n)$ time. For a non-tree edge $e = uv$, let $P_T(e)$ be the path from $u$ to $v$ in $T$, and let

$$\operatorname{max}_T(e) = \max \{ w(f) : f \in P_T(e) \}.$$

Then $T$ is an MST if and only if $w(e) \ge \operatorname{max}_T(e)$ for each edge $e \notin T$. This is the path optimality condition. A self-loop has an empty path and always passes. The inequality is not strict: with ties, a non-tree edge may weigh exactly as much as an edge on its path, and $T$ is still an MST. The strict form, $w(e) > \operatorname{max}_T(e)$ for each $e \notin T$, holds exactly when $T$ is the only MST ([MST uniqueness](/mst-uniqueness/)).

**Graphs that are not connected.** A disconnected graph has no spanning tree, so the answer is no for each $T$. The natural question is then whether a forest $F$ is a minimum spanning forest. It is when $F$ is a spanning forest, with one tree for each component, and the same test holds for each non-forest edge, whose ends then lie in one tree of $F$.

## Variants

- **Heavy edges of a forest.** Given any forest $F$ in $G$, not necessarily spanning, list the *$F$-heavy* edges: the edges $uv$ with $u$ and $v$ in the same tree of $F$ and $w(uv) > \operatorname{max}_F(uv)$. By the [cycle property](/cycle-property/), no $F$-heavy edge is in any MST of $G$, even with ties, since it is strictly heaviest on a cycle. The Karger-Klein-Tarjan algorithm needs this form.
- **Path-maximum queries.** The core problem: given a tree with weighted edges and $m$ pairs of vertices, find the heaviest edge on each path. Verification is the case where the pairs are the ends of the non-tree edges.
- **Sensitivity analysis.** Find, for each edge, how far its weight can change before $T$ stops being an MST ([MST sensitivity analysis](/mst-sensitivity-analysis/)). This answers the verification question as a side result.
- **Uniqueness test.** Decide whether $T$ is the only MST, by the strict test.

## Examples

**A graph with six vertices.** Take the vertices $a$ to $f$ and these nine edges.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

Let $T = \{ac, bc, bd, ce, ef\}$, of weight 13. The non-tree edges and their paths in $T$:

| non-tree edge $e$ | $w(e)$ | path in $T$ | $\operatorname{max}_T(e)$ | test |
|---|---|---|---|---|
| $ab$ | 4 | $a, c, b$ | 3 | $4 \ge 3$ |
| $cd$ | 4 | $c, b, d$ | 2 | $4 \ge 2$ |
| $de$ | 7 | $d, b, c, e$ | 5 | $7 \ge 5$ |
| $df$ | 6 | $d, b, c, e, f$ | 5 | $6 \ge 5$ |

All four tests pass, and all are strict, so $T$ is the unique MST.

**A tree that fails.** Let $T' = \{ab, bc, bd, ce, ef\}$, of weight 14. The non-tree edge $ac$ of weight 3 has the path $a, b, c$ in $T'$, with maximum $w(ab) = 4 > 3$. So $T'$ is not an MST, and the swap $T' - ab + ac$ gives a lighter tree.

**Ties.** In the triangle with weights $1, 2, 2$, the tree of the edge of weight 1 and one edge of weight 2 is an MST. The other edge of weight 2 has a path of maximum 2, the test $2 \ge 2$ passes, and the strict test fails, which shows that the MST is not unique.

**Not a tree.** In the same triangle, the set of all three edges fails the first check, since it has 3 edges and $n - 1 = 2$.

## Known algorithms

| algorithm | year | time | notes |
|---|---|---|---|
| Walk each path | | $O(n m)$ | for each non-tree edge, follow its tree path |
| Compute an MST and compare weights | | the time of an MST algorithm | all MSTs have the same weight |
| [Binary lifting](/binary-lifting/) | | $O((n + m) \log n)$ | store the maximum on each jump of length $2^i$ |
| Tarjan | 1979 | $O(m\,\alpha(m, n))$ | offline queries with path compression on balanced trees |
| Komlós | 1985 | $O(m)$ comparisons | the time to choose the comparisons is larger |
| Dixon, Rauch and Tarjan | 1992 | $O(m)$ | first linear-time algorithm, on a RAM |
| King | 1997 | $O(m)$ | simpler: Borůvka tree, then Komlós's method with table lookups |
| Buchsbaum, Kaplan, Rogers and Westbrook | 1998 | $O(m)$ | on a [pointer machine](/pointer-machine/) |

**Compare weights.** Compute any MST $T^*$ and answer yes if $T$ is a spanning tree with $w(T) = w(T^*)$. This is correct because all MSTs have the same weight. It is as slow as finding an MST, so it does not give linear time.

**Binary lifting.** Root $T$. For each vertex $v$ and each $i$, store the ancestor $\operatorname{up}_i(v)$ at distance $2^i$ and the heaviest edge on the way to it. A query $uv$ lifts $u$ and $v$ to their [lowest common ancestor](/lowest-common-ancestor/) and takes the maximum of $O(\log n)$ stored values. This is the usual method in practice.

**King's method.** Run [Borůvka](/boruvka/) steps on $T$ alone. They build a tree $B$ whose leaves are the vertices of $T$, all at the same depth, in which each internal node has at least two children. The heaviest edge on a path of $T$ equals the heaviest edge on the matching path of $B$, and in $B$ each path goes up from both ends to a common ancestor. Komlós's method then answers all queries with $O(m)$ comparisons, and King stores the sets of candidates as small bit strings in words, so the work for each node takes $O(1)$ word operations.

## Bounds

**Lower bound.** Each correct algorithm must compare the weight of every edge that is not a bridge or a self-loop, on every input where the answer is yes ([MST lower bound](/mst-lower-bound/)). So verification takes $\Omega(m)$ time on 2-edge-connected graphs.

**Upper bound.** $O(m)$ time on the word RAM (Dixon, Rauch and Tarjan; King) and on the pointer machine (Buchsbaum and others). With the lower bound, the complexity of verification is $\Theta(m)$.

**Comparisons.** Komlós's bound of $O(m)$ comparisons holds in the comparison model, where only comparisons of weights are counted. The work to decide which comparisons to make is what the later papers bring down to $O(m)$.

**The gap with the MST problem.** Verification is linear, but no deterministic linear-time algorithm is known for finding an MST. So checking an answer is known to be easier than the best known way of finding one.

## Reductions

- **Verification to path-maximum queries.** Ask one query for each non-tree edge, in $O(m)$ extra time.
- **Verification to MST.** Compute an MST and compare weights, as above.
- **Verification to sensitivity analysis.** Sensitivity analysis gives, for each non-tree edge $e$, the value $\operatorname{max}_T(e)$, so verification follows in $O(m)$ time.
- **MST to verification, with randomness.** The Karger-Klein-Tarjan algorithm finds an MST with recursion, random sampling and $F$-heavy edge removal. With linear-time verification, it runs in expected $O(m)$ time.
- **Second-best MST.** The [second-best MST](/second-best-mst/) is $T - f + e$ for a pair that minimizes $w(e) - w(f)$ with $f$ the heaviest edge of $P_T(e)$, so the same path-maximum queries find it.

## Applications

- **Linear-time randomized MST.** The filter step of the Karger-Klein-Tarjan algorithm.
- **Checking programs.** A verifier lets a fast but complex MST program be checked on each run at linear cost.
- **Updates.** After a weight changes, a verifier tells whether the old tree is still optimal.
- **Uniqueness.** The strict test tells whether a network design has one optimal answer or many.

## References
