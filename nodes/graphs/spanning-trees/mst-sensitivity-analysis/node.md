---
tag: 3H75JC
kind: problem
slug: mst-sensitivity-analysis
name: MST sensitivity analysis
aliases:
- MST weight sensitivity
area: graphs/spanning-trees
level: advanced
summary: For each edge, find how far its weight can change while the given tree stays minimum.
model: comparison-model
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: "O(m log α(m, n))"}
prereqs: [minimum-spanning-tree, mst-optimality-conditions, mst-verification, fundamental-cycle]
see_also: [mst-verification, second-best-mst, lp-sensitivity-analysis, replacement-paths, binary-lifting, disjoint-set, cut-property, cycle-property]
sources:
  - paper: doi:10.1137/0221070
    title: Brandon Dixon, Monika Rauch and Robert E. Tarjan, Verification and sensitivity analysis of minimum spanning trees in linear time, SIAM Journal on Computing 21(6) (1992), 1184-1192
    locator: the whole paper (sensitivity of tree and non-tree edges)
  - paper: doi:10.7155/jgaa.00365
    title: Seth Pettie, Sensitivity analysis of minimum spanning trees in sub-inverse-Ackermann time, Journal of Graph Algorithms and Applications 19(1) (2015), 375-391
    locator: the main theorem, O(m log α(m, n)) deterministic time, and the survey of earlier bounds in the introduction
  - paper: doi:10.1007/BF02579443
    title: János Komlós, Linear verification for spanning trees, Combinatorica 5(1) (1985), 57-65
    locator: the path-maximum method, which gives the sensitivity of the non-tree edges
---

MST sensitivity analysis takes a [minimum spanning tree](/minimum-spanning-tree/) $T$ of a weighted graph and finds, for each edge, the range of weights over which $T$ stays minimum when only that edge's weight changes. A non-tree edge may get lighter down to the heaviest weight on its tree path, and a tree edge may get heavier up to the lightest non-tree edge that covers it. The first half is [MST verification](/mst-verification/) and takes linear time. The second half is the harder part: Tarjan solved it in $O(m\,\alpha(m, n))$ time and Pettie in $O(m \log \alpha(m, n))$ deterministic time.

## In plain words

You have built the cheapest network of cables. Prices change, and you want to know, for each cable, how much its price can move before your network stops being the cheapest.

For a cable you did not use, a price rise changes nothing. It may drop until it equals the most expensive cable on the route that your network uses between its ends. Below that, a swap would help.

For a cable you did use, a price drop changes nothing. It may rise until it equals the cheapest unused cable that could take its place. Above that, a swap would help. If no unused cable can take its place, the price may rise without limit.

## Definition

**Input.** A finite, [connected](/connected-graph/), undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, a weight $w(e) \in \mathbb{R}$ on each edge, and an MST $T$ of $(G, w)$. Weights may tie. Parallel edges are allowed.

**Notation.** For $e = uv \notin T$, let $P_T(e)$ be the path from $u$ to $v$ in $T$. Say that $e$ *covers* each tree edge on $P_T(e)$.

**Output.** For each edge, its *tolerance*: the set of values $x$ such that $T$ is still an MST when $w(e)$ is replaced by $x$ and all other weights stay the same. This set is a ray.

- For a non-tree edge $e$: the ray $[\,\operatorname{max}_T(e), +\infty)$, where $\operatorname{max}_T(e) = \max \{ w(f) : f \in P_T(e) \}$.
- For a tree edge $f$: the ray $(-\infty, \operatorname{cov}_T(f)\,]$, where $\operatorname{cov}_T(f) = \min \{ w(e) : e \notin T \text{ covers } f \}$, or $+\infty$ if no edge covers $f$, which happens exactly when $f$ is a [bridge](/bridge/).

**Why these values.** By the [path optimality condition](/mst-optimality-conditions/), $T$ is an MST if and only if $w(e) \ge w(f)$ for each non-tree edge $e$ and each $f \in P_T(e)$. A change of $w(e)$ for $e \notin T$ affects only the conditions of $e$, and they hold exactly when $w(e) \ge \operatorname{max}_T(e)$. A change of $w(f)$ for $f \in T$ affects only the conditions of the edges that cover $f$, and they hold exactly when $w(f) \le w(e)$ for each of them, that is, $w(f) \le \operatorname{cov}_T(f)$.

**Ties.** The ends of each ray belong to it: at $x = \operatorname{max}_T(e)$ or $x = \operatorname{cov}_T(f)$, the tree $T$ is still an MST, but no longer the only one. The question "how far can the weight move while $T$ stays the unique MST" has the open rays instead, and it makes sense only if $T$ is unique to begin with.

**Disconnected graphs.** For a minimum spanning forest, the same definitions apply in each component: a non-tree edge has both ends in one tree, and a tree edge is covered only by edges of its own component.

## Variants

- **Non-tree edges only.** Compute $\operatorname{max}_T(e)$ for each $e \notin T$. These are the path-maximum queries of MST verification.
- **Tree edges only.** Compute $\operatorname{cov}_T(f)$ for each $f \in T$, the *path-minimum covering* problem. The lightest covering edge is also the *replacement edge* of $f$: if $f$ fails, $T - f + e$ for that $e$ is an MST of $G - f$.
- **Several changes at once.** Tolerances of single edges do not always combine. A tree edge $f$ may rise to $w(e)$ for a non-tree edge $e$ that covers it, and $e$ may drop to $\operatorname{max}_T(e)$, but together the two changes must keep $w(e) \ge w(f)$. Changes to tree edges alone do combine, and so do changes to non-tree edges alone, because each condition of the path test involves one tree edge and one non-tree edge.
- **Shortest path trees.** Tarjan's method also gives the sensitivity of a [shortest path tree](/shortest-path-tree/).
- **Linear programs.** This is the graph form of [LP sensitivity analysis](/lp-sensitivity-analysis/) on the spanning tree LP: the tolerance of a weight is its range of optimality.

## Examples

**A graph with six vertices.** Take the vertices $a$ to $f$ and these nine edges.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

The unique MST is $T = \{ac, bc, bd, ce, ef\}$, of weight 13. For the non-tree edges:

| non-tree edge | weight | path in $T$ | lower end $\operatorname{max}_T$ |
|---|---|---|---|
| $ab$ | 4 | $ac, bc$ | 3 |
| $cd$ | 4 | $bc, bd$ | 2 |
| $de$ | 7 | $bd, bc, ce$ | 5 |
| $df$ | 6 | $bd, bc, ce, ef$ | 5 |

For the tree edges:

| tree edge | weight | covered by | upper end $\operatorname{cov}_T$ |
|---|---|---|---|
| $ac$ | 3 | $ab$ | 4 |
| $bc$ | 1 | $ab, cd, de, df$ | 4 |
| $bd$ | 2 | $cd, de, df$ | 4 |
| $ce$ | 5 | $de, df$ | 6 |
| $ef$ | 2 | $df$ | 6 |

So $ce$ may rise from 5 to 6 and $T$ stays an MST; at 6 the tree $T - ce + df$ is also an MST, and above 6 it is better. The edge $df$ may drop from 6 to 5, with the same swap at the end.

**A bridge.** Add a vertex $g$ and an edge $fg$ of weight 9. It is in every spanning tree, it is covered by no edge, and its tolerance is $(-\infty, +\infty)$.

**Ties.** In the triangle with weights $1, 2, 2$, take $T$ with the edge of weight 1 and the first edge of weight 2. The other edge of weight 2 has tolerance $[2, +\infty)$, which contains its current weight as its end, so $T$ is an MST but not the only one. The first edge of weight 2 has tolerance $(-\infty, 2]$.

## Known algorithms

| algorithm | year | time | notes |
|---|---|---|---|
| Walk each path | | $O(n m)$ | for each non-tree edge, update every edge of its path |
| Sorted covering with union-find | | $O(m \log m)$ | the sort dominates; $O(m\,\alpha(m, n))$ after sorting |
| [Binary lifting](/binary-lifting/) and sorted covering | | $O(m \log n)$ | simple and practical |
| Tarjan | 1982 | $O(m\,\alpha(m, n))$ | path compression on balanced trees |
| Komlós; Dixon, Rauch and Tarjan; King | 1985 to 1997 | $O(m)$ for the non-tree edges | the verification algorithms |
| Dixon, Rauch and Tarjan | 1992 | optimal, the exact bound is unknown | decision trees for small subproblems |
| Pettie | 2005 | $O(m \log \alpha(m, n))$ | split-findmin structure; journal version 2015 |

**Sorted covering.** Root $T$ and sort the non-tree edges by weight. Keep a [disjoint-set](/disjoint-set/) structure in which each set is a vertex together with the ancestors reached through tree edges that already have a value; the representative is the top vertex of the set. For each non-tree edge $uv$ in increasing order, jump from $u$ and from $v$ to their representatives and walk up, one unassigned tree edge at a time, until the two walks meet at the [lowest common ancestor](/lowest-common-ancestor/). Each tree edge met gets $\operatorname{cov}_T = w(uv)$ and is merged into the set above it. Each tree edge is assigned once, since the first covering edge in sorted order is the lightest. Tree edges never assigned are bridges.

**Path maxima.** The values $\operatorname{max}_T(e)$ come from any MST verification method.

## Bounds

**Lower bound.** Each correct algorithm must examine every edge that is not a bridge, by the argument of the [MST lower bound](/mst-lower-bound/), so the problem takes $\Omega(m)$ time.

**Upper bounds.** The non-tree half is $\Theta(m)$. For the tree half, the best deterministic bound is Pettie's $O(m \log \alpha(m, n))$. The algorithm of Dixon, Rauch and Tarjan is optimal, but its exact time is not known, and the question of a deterministic $O(m)$ bound is open.

**Relation to the MST problem.** Pettie shows that sensitivity analysis is no harder than finding an MST, up to a constant factor. When the edges are given in sorted order, the sorted covering method runs in $O(m\,\alpha(m, n))$ time.

## Reductions

- **Verification to sensitivity analysis.** Given a spanning tree $T$, compute $\operatorname{max}_T(e)$ for each non-tree edge and check $w(e) \ge \operatorname{max}_T(e)$.
- **Second-best MST to sensitivity analysis.** The [second-best MST](/second-best-mst/) when the MST is unique is $T - f + e$ for the pair that minimizes $w(e) - w(f)$ with $e$ covering $f$. This minimum equals both $\min_{f \in T} (\operatorname{cov}_T(f) - w(f))$ and $\min_{e \notin T} (w(e) - \operatorname{max}_T(e))$.
- **Replacement edges.** The replacement edge of each tree edge, for the failure of one edge, is the covering edge that attains $\operatorname{cov}_T$.

## Applications

- **Robust network design.** The tolerance tells how much a cost estimate may be wrong before the chosen network must change.
- **Edge failures.** The replacement edges give an MST of $G - f$ for each tree edge $f$ at once, a form of [replacement paths](/replacement-paths/) for trees.
- **Most vital edge.** The tree edge $f$ whose removal raises the MST weight the most maximizes $\operatorname{cov}_T(f) - w(f)$.
- **Updates.** After one weight changes, the tolerance tells in $O(1)$ time whether the old tree is still optimal.

## References
