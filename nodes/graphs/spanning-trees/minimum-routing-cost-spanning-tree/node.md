---
tag: VGTV64
kind: problem
slug: minimum-routing-cost-spanning-tree
name: Minimum routing cost spanning tree problem
aliases:
- minimum routing cost tree
area: graphs/spanning-trees
level: research
summary: Minimize the sum of pairwise distances measured within the spanning tree.
prereqs: [spanning-tree, shortest-path-tree, np-hard, all-pairs-shortest-paths]
see_also: [minimum-diameter-spanning-tree, minimum-spanning-tree, steiner-tree-problem, ptas, dijkstra, metric-space, tree-center, np-complete]
sources:
  - paper: doi:10.1002/net.3230080402
    title: D. S. Johnson, J. K. Lenstra and A. H. G. Rinnooy Kan, The complexity of the network design problem, Networks 8(4) (1978), 279-285
    locator: the whole paper (NP-hardness of choosing a subgraph that minimizes the total of all pairwise distances)
  - paper: doi:10.1137/0601008
    title: Richard T. Wong, Worst-case analysis of network design problem heuristics, SIAM Journal on Algebraic and Discrete Methods 1(1) (1980), 51-63
    locator: the whole paper (the shortest path tree from the best vertex is within a factor 2 of optimal)
  - paper: doi:10.1137/S009753979732253X
    title: Bang Ye Wu, Giuseppe Lancia, Vineet Bafna, Kun-Mao Chao, R. Ravi and Chuan Yi Tang, A polynomial-time approximation scheme for minimum routing cost spanning trees, SIAM Journal on Computing 29(3) (2000), 761-778
    locator: the whole paper (the PTAS by trees with few internal vertices, the edge formula for the routing cost, and the survey of earlier results)
  - paper: doi:10.1137/0203015
    title: T. C. Hu, Optimum communication spanning trees, SIAM Journal on Computing 3(3) (1974), 188-195
    locator: the whole paper (the general problem with pairwise requirements, and the cases that are easy)
---

The minimum routing cost spanning tree problem asks for a [spanning tree](/spanning-tree/) $T$ of a weighted graph that minimizes the sum, over all pairs of vertices, of their distance in $T$. It models a network in which every pair of nodes sends the same amount of traffic along the tree. The problem is [NP-hard](/np-hard/), even with unit lengths, but the [shortest path tree](/shortest-path-tree/) from a well chosen vertex is within a factor 2 of the optimum, and Wu and others gave a polynomial-time approximation scheme in 2000. It is the case with equal requirements of Hu's optimum communication spanning tree problem.

## In plain words

You must build a tree of links between a set of sites, choosing links from a given list, each with a length. Every pair of sites will send messages to each other along the tree. You pay for the total travel: add up, for every pair, the length of its route in the tree. You want this total to be as small as possible.

A cheapest tree by total link length can be bad here, since it may force long detours. A good simple choice is to pick a central site and join every other site to it by its shortest route. This is never worse than twice the best answer. Finding the exact best tree is hard in general.

## Definition

**Input.** A finite connected undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and lengths $w(e) \ge 0$. Parallel edges and self-loops are allowed; self-loops are never in a tree.

**Output.** A spanning tree $T$ that minimizes the *routing cost*

$$C(T) = \sum_{\{u, v\} \subseteq V} d_T(u, v),$$

where $d_T(u, v)$ is the length of the path from $u$ to $v$ in $T$.

**Edge formula.** Removing an edge $e$ of $T$ splits $V$ into two sides with $s_e$ and $n - s_e$ vertices, and exactly the $s_e (n - s_e)$ pairs on different sides route through $e$. So

$$C(T) = \sum_{e \in T} w(e)\, s_e\, (n - s_e).$$

Edges near the middle of the tree weigh the most. This is why a cheap tree by total length, the [minimum spanning tree](/minimum-spanning-tree/), can be far from optimal: it puts no premium on central edges.

**Connectivity.** The graph must be [connected](/connected-graph/); a disconnected graph has no spanning tree. For a forest one could sum within components only, which splits into one problem per component.

**Ties.** Lengths may tie, and the optimum tree need not be unique; the optimal value is. Shortest path trees from one root can differ when two shortest paths tie, and their routing costs can differ too, so a heuristic that breaks ties arbitrarily may return different values.

## Variants

- **Optimum communication spanning tree (Hu 1974).** Each pair $u, v$ has a requirement $r(u, v) \ge 0$, and the cost is $\sum r(u, v)\, d_T(u, v)$. The routing cost problem is the case $r \equiv 1$. Hu showed two easy cases: on a complete graph with all lengths equal, a Gomory-Hu cut tree of the requirements is optimal, and with all requirements equal and lengths that meet a further condition, a star is optimal.
- **Product and sum requirements.** With $r(u, v) = p(u)\, p(v)$ or $r(u, v) = p(u) + p(v)$ for vertex weights $p$, Wu and others gave constant factor approximations and schemes.
- **Metric version.** When $G$ is complete and $w$ is a [metric](/metric-space/), the problem keeps its hardness and the same approximation results hold.
- **Steiner version.** The tree may use extra vertices that are not counted in the sum, as in the [Steiner tree problem](/steiner-tree-problem/).
- **Maximum instead of sum.** Minimizing the largest pairwise tree distance is the [minimum diameter spanning tree](/minimum-diameter-spanning-tree/) problem, which is solvable in polynomial time.

## Examples

**The weighted example graph.** On the graph on $a$ to $f$ with lengths $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$, a search over all 55 spanning trees finds a unique optimum, the tree $\{ac, bc, bd, ce, ef\}$, with routing cost 83. By the edge formula:

| edge | $ac$ | $bc$ | $bd$ | $ce$ | $ef$ |
|---|---|---|---|---|---|
| $w(e)$ | 3 | 1 | 2 | 5 | 2 |
| $s_e (n - s_e)$ | 5 | 8 | 5 | 8 | 5 |
| contribution | 15 | 8 | 10 | 40 | 10 |

The sum of all graph distances is 78, a lower bound that no tree can beat. Here the optimum is also the minimum spanning tree and the shortest path tree from $c$, which is not true in general.

**Shortest path trees from each root on that graph.** The vertex $c$ has the least total distance, 19, and its shortest path tree is optimal. Other roots give worse trees:

| root | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ |
|---|---|---|---|---|---|---|
| total distance from root | 31 | 21 | 19 | 24 | 28 | 33 |
| routing cost of one shortest path tree | 119 | 99 | 83 | 108 | 110 | 131 |

From $a$, the two paths to $b$ tie at length 4 ($ab$, or $ac$ then $cb$), so the root $a$ has more than one shortest path tree.

**Unit lengths.** On the same graph with all lengths 1, the sum of all graph distances is 22, and the optimum routing cost is 28, attained by 4 of the 55 trees. The minimum spanning tree of the weighted graph has routing cost 31 here.

**A star and a path.** On $n$ vertices with unit lengths, a star has routing cost $(n - 1) + 2 \binom{n - 1}{2} = (n - 1)^2$ and a path has $\binom{n + 1}{3}$. So in a complete graph with unit lengths the star is optimal: each tree has $n - 1$ pairs at distance 1 and all other pairs at distance at least 2, and the star attains this bound.

## Known algorithms

| method | guarantee | time | source |
|---|---|---|---|
| Try all spanning trees | exact | exponential | |
| Best shortest path tree over all roots | factor $2(n-1)/n$ | $O(mn + n^2 \log n)$ | Wong 1980 |
| Best tree with few internal vertices | factor $1 + \varepsilon$ | polynomial for fixed $\varepsilon$ | Wu and others 2000 |

**Shortest path tree from the best vertex.** Compute all distances. Pick the vertex $r$ with the least total distance $S(r) = \sum_x d_G(r, x)$, and return a shortest path tree from $r$.

*Why it is within $2(n-1)/n$.* In a shortest path tree from $r$, $d_T(u, v) \le d_G(u, r) + d_G(r, v)$. Summing over pairs, each vertex appears in $n - 1$ pairs, so $C(T) \le (n - 1)\, S(r)$. Let $W = \sum_{\{u,v\}} d_G(u, v)$. Summing $S(r)$ over all $r$ counts each pair twice, so $\sum_r S(r) = 2W$ and the best $r$ has $S(r) \le 2W / n$. So $C(T) \le 2(n - 1) W / n$, and every spanning tree has $C \ge W$, since tree distances are at least graph distances.

**The approximation scheme.** Wu and others show that, for each $k$, some tree in which all vertices hang from a small core of at most $k$ internal vertices, a *$k$-star*, has routing cost at most $(k + 3)/(k + 1)$ times the optimum. They then find the best such tree by trying all small cores and solving an assignment for the rest. Taking $k$ large gives a factor $1 + \varepsilon$, with a running time polynomial in $n$ for each fixed $\varepsilon$, which is a [PTAS](/ptas/).

## Bounds

**Hardness.** The problem is NP-hard, by the result of Johnson, Lenstra and Rinnooy Kan on network design, and it stays NP-hard with unit lengths. So an exact polynomial algorithm would give P = NP.

**Approximation.** It has a PTAS, so every constant factor above 1 is possible in polynomial time. It has no fully polynomial scheme unless P = NP: with unit lengths the value is an integer at most $n^3$, so a scheme with $\varepsilon = 1/n^3$ would solve the NP-hard unit case exactly in polynomial time.

**Value bounds.** $W \le C(T^\ast) \le 2(n-1)W/n$, where $W$ is the sum of graph distances.

## Reductions

- **From known NP-complete problems.** Johnson, Lenstra and Rinnooy Kan reduce a known NP-complete problem to the choice of tree edges.
- **To shortest paths.** The factor 2 method needs only [all-pairs shortest paths](/all-pairs-shortest-paths/), for example by running [Dijkstra's algorithm](/dijkstra/) from each vertex.
- **To the general communication problem.** The problem is the case $r \equiv 1$ of the optimum communication spanning tree problem, so any algorithm for that problem applies.

## Applications

- **Network design.** A tree that minimizes total routing cost is cheap to operate when all pairs exchange the same amount of traffic, as in peer-to-peer and sensor networks.
- **Multiple sequence alignment.** Wu and others note that the routing cost of a tree of sequences relates to the sum of pairs score; trees with small routing cost give approximate alignments.
- **Chemistry and graph theory.** For unit lengths, the routing cost of a tree is its Wiener index, a classical measure of molecular graphs.

## References
