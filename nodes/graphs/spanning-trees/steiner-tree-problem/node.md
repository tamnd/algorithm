---
tag: 0DCXSX
kind: problem
slug: steiner-tree-problem
name: Steiner tree problem
aliases:
- Steiner minimal tree
area: graphs/spanning-trees
level: core
summary: Connect a given set of terminals with minimum cost, possibly using extra Steiner vertices.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of terminals}
  time: {worst: "O(3^k n + 2^k n^2 + n m + n^2 log n)"}
prereqs: [minimum-spanning-tree, shortest-path, weighted-graph, np-hard]
see_also: [kou-markowsky-berman, steiner-forest, steiner-tree-inapproximability, euclidean-steiner-tree-problem, rectilinear-steiner-tree-problem, prize-collecting-steiner-tree, parameterized-steiner-tree, steiner-ratio]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A2, problem ND12, Steiner tree in graphs
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum (1972), 85-103
    locator: the list of reductions (Steiner tree from exact cover)
  - paper: doi:10.1002/net.3230010302
    title: Stuart E. Dreyfus and Robert A. Wagner, The Steiner problem in graphs, Networks 1(3) (1971), 195-207
    locator: the whole paper (the dynamic program over subsets of terminals)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer (2001)
    locator: Chapter 3, Steiner Tree and TSP (Section 3.1, the metric Steiner tree problem and the factor 2 algorithm)
  - paper: doi:10.1145/2432622.2432628
    title: Jarosław Byrka, Fabrizio Grandoni, Thomas Rothvoß and Laura Sanità, Steiner tree approximation via iterative randomized rounding, Journal of the ACM 60(1) (2013), Article 6
    locator: the main theorem, a ln 4 + ε approximation
---

The Steiner tree problem asks, for an undirected graph with nonnegative edge weights and a set of *terminal* vertices, for a tree of least weight that contains every terminal. The tree may also pass through other vertices, called *Steiner vertices*, when that makes it cheaper. With two terminals it is the [shortest path](/shortest-path/) problem and with all vertices as terminals it is the [minimum spanning tree](/minimum-spanning-tree/) problem, but in general it is [NP-hard](/np-hard/). An exact dynamic program runs in time exponential only in the number of terminals, and a minimum spanning tree of the shortest path distances between terminals gives a factor 2 approximation.

## In plain words

Some towns must be joined by roads, and other towns may be used on the way if that helps. Each possible road has a price. You want all the chosen towns connected at the least total price.

If every town must be joined, this is the cheapest network problem, and simple greedy rules solve it. If only two towns must be joined, the answer is the cheapest route between them. The hard part is the choice of which extra towns to pass through. A town in the middle of three chosen towns can make a cheaper network than any network that joins the three towns to each other directly. There are many sets of extra towns to try, and no fast method is known that always finds the best one.

## Definition

**Input.** A finite undirected graph $G = (V, E)$ with $n = |V|$ vertices and $m = |E|$ edges, a weight $w(e) \ge 0$ for each edge, and a set $R \subseteq V$ of $k \ge 1$ *terminals*. Weights may tie. Parallel edges and self-loops are allowed; a self-loop is never used, and of parallel edges only a lightest one matters.

**Output.** A subgraph $T$ of $G$ that is a [tree](/tree/), contains every vertex of $R$, and has least total weight $w(T) = \sum_{e \in T} w(e)$ among all such trees. Such a $T$ is a **Steiner minimal tree**, and the vertices of $T$ that are not terminals are its **Steiner vertices**.

**Connectivity.** The graph need not be [connected](/connected-graph/). A solution exists if and only if all terminals lie in one component, and then a solution lies in that component. If the terminals are in two or more components, the answer is that no tree exists.

**Why a tree.** The problem is often stated as: find a connected subgraph that contains $R$ and has least weight. The two forms have the same optimum value. A connected subgraph contains a spanning tree of itself, and with weights $\ge 0$ that tree is no heavier. When some weights are 0, an optimal connected subgraph can contain a cycle of weight 0, but a tree of the same weight always exists.

**Negative weights.** They are not allowed. With a negative edge anywhere in the component, the "connected subgraph" form would add it even when no terminal needs it, and the two forms no longer agree.

**Decision version.** Given $G$, $w$, $R$ and a bound $B$, is there a tree that contains $R$ with weight at most $B$? This is NP-complete, even when every weight is 1 (Garey and Johnson, ND12).

## Variants

- **Special cases in P.** With $k = 1$ the answer is the single terminal, weight 0. With $k = 2$ it is a shortest path. With $R = V$ it is a minimum spanning tree, and more generally, when no Steiner vertex can help, it is the MST of the subgraph induced by $R$.
- **Metric Steiner tree.** The input is a complete graph whose weights obey the triangle inequality. Each instance of the graph problem reduces to this form (see Reductions), so the two have the same approximation ratios.
- **[Steiner forest](/steiner-forest/).** The input is a list of terminal pairs, and each pair must be connected, not all terminals together. The [Goemans-Williamson](/goemans-williamson-steiner-forest/) primal-dual method gives a factor 2.
- **[Prize-collecting Steiner tree](/prize-collecting-steiner-tree/).** A terminal may be left out at a given penalty.
- **[Generalized Steiner network](/generalized-steiner-network/) and [survivable network design](/survivable-network-design/).** Each pair of terminals needs a given number of edge-disjoint paths.
- **Geometric versions.** In the [Euclidean Steiner tree problem](/euclidean-steiner-tree-problem/) the terminals are points in the plane and Steiner points may be placed anywhere. In the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/) the distance is the $L_1$ distance, which models wires on a chip. The [Steiner ratio](/steiner-ratio/) compares the optimum with the MST of the terminals.
- **Planar graphs.** A [PTAS](/planar-steiner-tree-ptas/) exists for planar input.
- **Online.** In the [online Steiner tree problem](/online-steiner-tree-problem/) terminals arrive one at a time and each must be connected at once.
- **Parameterized.** With the number of terminals $k$ as the parameter, the problem is [fixed-parameter tractable](/fixed-parameter-tractable/) ([parameterized Steiner tree](/parameterized-steiner-tree/)).

## Examples

**A graph with six vertices.** Take the vertices $a$ to $f$ and these nine edges.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

With the terminals $R = \{a, d, e\}$, the unique optimum is $\{ac, bc, bd, ce\}$ of weight $3 + 1 + 2 + 5 = 11$, with the Steiner vertices $b$ and $c$. The subgraph induced by $R$ has only the edge $de$, so the terminals cannot be connected without Steiner vertices. The shortest path distances between the terminals are $d(a, d) = 6$, $d(a, e) = 8$ and $d(d, e) = 7$. The MST of these three distances has weight $6 + 7 = 13$, so the [factor 2 method](/kou-markowsky-berman/) can return a tree of weight 13 here, more than the optimum 11. The optimum uses the vertex $c$ as a branch point that the paths between pairs of terminals do not share.

**Ties.** With the terminals $R = \{a, d, f\}$ in the same graph, two trees have the least weight 12: $\{ab, bd, df\}$ and $\{ac, bc, bd, df\}$. The first uses one Steiner vertex and the second uses two. An optimal tree need not be unique, and two optimal trees can have different numbers of edges.

**All terminals.** With $R = V$, the optimum is the MST $\{ac, bc, bd, ce, ef\}$ of weight 13.

**A star.** Take a center $c$ joined to three terminals $x, y, z$ by edges of weight 1, and the three edges $xy, yz, zx$ of weight 2. The optimum is the star of weight 3, with $c$ as its only Steiner vertex. Each tree that uses only edges between terminals has weight 4. In the metric form, the MST method returns such a tree. With $k$ terminals around a center, it returns weight $2(k - 1)$ against the optimum $k$, and the ratio tends to 2, so the factor 2 is tight for that method.

**Disconnected input.** If a terminal lies in a component that holds no other terminal, and $k \ge 2$, no tree contains all terminals, and the answer is that no solution exists.

## Known algorithms

| algorithm | year | result | notes |
|---|---|---|---|
| Brute force over sets of Steiner vertices | | exact, $O(2^{n-k} m \log n)$ | take an MST of the subgraph induced by $R \cup S$ for each $S$ |
| Dreyfus and Wagner | 1971 | exact, $O(3^k n + 2^k n^2 + n m + n^2 \log n)$ | dynamic program over subsets of terminals |
| Björklund, Husfeldt, Kaski and Koivisto | 2007 | exact, $O^*(2^k W)$ for integer weights at most $W$ | fast subset convolution |
| MST of the distance graph ([Kou, Markowsky and Berman](/kou-markowsky-berman/)) | 1981 | ratio $2(1 - 1/l)$, $l$ the number of leaves of an optimum | Takahashi and Matsuyama (1980) and Mehlhorn (1988) give the same bound |
| Zelikovsky | 1993 | ratio $11/6$ | greedy contraction of triples of terminals |
| Robins and Zelikovsky | 2005 | ratio $1 + \frac{\ln 3}{2} \approx 1.55$ | loss-contracting greedy method |
| Byrka, Grandoni, Rothvoß and Sanità | 2010 | ratio $\ln 4 + \varepsilon \approx 1.39$ | [iterative](/iterative-rounding/) randomized rounding of a directed component LP |

**Brute force.** An optimal tree $T$ has some set $S$ of Steiner vertices, and $T$ is then a spanning tree of the subgraph induced by $R \cup S$. Each spanning tree of that subgraph is a feasible solution. So the optimum is the least, over all $S \subseteq V \setminus R$ for which $R \cup S$ induces a connected subgraph, of the MST weight of that subgraph.

**Dreyfus and Wagner.** For a set $D \subseteq R$ and a vertex $v$, let $t(D, v)$ be the least weight of a tree that contains $D \cup \{v\}$. First compute all shortest path distances $d$. For one terminal, $t(\{r\}, v) = d(r, v)$. For larger $D$, in an optimal tree for $D \cup \{v\}$, follow the path from $v$ until it reaches a terminal of $D$ or a vertex $u$ of degree at least 3. At $u$ the tree splits into two subtrees, each with a nonempty part of $D$. This gives

$$t(D, v) = \min_{u \in V} \Big( d(v, u) + \min_{\emptyset \ne D' \subsetneq D} \big( t(D', u) + t(D \setminus D', u) \big) \Big).$$

The inner minimum over all pairs $(D, D')$ costs $O(3^k n)$ in total, and the outer minimum over $u$ costs $O(2^k n^2)$. The answer is $t(R \setminus \{r\}, r)$ for any terminal $r$. The [submask enumeration](/submask-enumeration/) and [sum over subsets](/sum-over-subsets/) pages show the subset loops.

## Bounds

**NP-hardness.** The decision version is NP-complete, by Karp's reduction from exact cover by 3-sets (see Reductions). It stays NP-complete with unit weights.

**Inapproximability.** The problem is APX-hard (Bern and Plassmann, 1989), so it has no [PTAS](/ptas/) unless P = NP. No approximation ratio below $96/95$ is possible unless P = NP (Chlebík and Chlebíková, 2008); see [Steiner tree inapproximability](/steiner-tree-inapproximability/).

**The factor 2 bound.** Let $T^*$ be an optimal tree, and let $H$ be the complete graph on $R$ with the shortest path distance $d(a, b)$ as the weight of the edge $ab$. Double each edge of $T^*$. Each vertex now has even degree, so the doubled tree has an Euler tour of weight $2 w(T^*)$. Walk the tour and list the terminals in the order of their first visit. Consecutive terminals in this list are joined by a part of the tour, which is no shorter than their distance $d$. So the cycle in $H$ that visits the terminals in this order weighs at most $2 w(T^*)$. Remove its heaviest edge. The result is a spanning tree of $H$ of weight at most $2(1 - 1/k)\, w(T^*)$. An MST of $H$ is no heavier, and each of its edges expands to a path in $G$ of the same weight, whose union contains a tree that holds $R$. The sharper factor $2(1 - 1/l)$ comes from a tour that starts and ends at leaves of $T^*$. The star example shows that the factor tends to 2.

**Exact time.** The Dreyfus-Wagner bound is polynomial when $k = O(\log n)$. For integer weights at most $W$, fast subset convolution lowers the dependence on $k$ to $O^*(2^k W)$.

## Reductions

- **Exact cover by 3-sets to Steiner tree.** Take an instance of [exact cover by 3-sets](/exact-cover-by-3-sets/): a set $U$ of $3q$ elements and a family $C$ of 3-element subsets of $U$. Build a graph with a root $r$, a vertex for each set in $C$, and a vertex for each element of $U$. Join $r$ to each set vertex, and join each set vertex to its three elements. Give each edge weight 1, and let $R = \{r\} \cup U$. A tree that contains $R$ and $j$ set vertices has $1 + 3q + j$ vertices, so it has $3q + j$ edges. Its set vertices cover $U$, so $j \ge q$, and $j = q$ exactly when they form an exact cover. So an exact cover exists if and only if a tree of weight $4q$ exists. This is one of [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/).
- **Graph to metric form.** Replace $G$ by the complete graph on $V$ with the shortest path distance as weight, computed by [all-pairs shortest paths](/all-pairs-shortest-paths/). The two instances have the same optimum: a tree in the metric graph expands to a connected subgraph of $G$ that is no heavier, and each edge of $G$ is no lighter than the distance between its ends.
- **Steiner tree to MST.** When $R = V$, or when no vertex outside $R$ is allowed, the problem is the MST problem on the subgraph induced by $R$.
- **Steiner tree to shortest path.** When $k = 2$, an optimal tree is a shortest path between the two terminals.

## Applications

- **Network design.** Joining sites by cable, pipe or fibre at least cost, when junctions may be placed at other sites.
- **Chip design.** Routing a net of pins on a chip is a rectilinear Steiner tree problem.
- **Multicast routing.** A message sent from one source to a group of receivers in a network follows a tree that holds the source and the receivers.
- **Phylogenetics.** A [phylogenetic tree](/phylogenetic-tree/) of least total change, with ancestors as Steiner vertices, is a Steiner tree in a space of sequences.
- **Approximation algorithms.** The Steiner tree problem is a test case for LP methods: the [integrality gap](/integrality-gap/) of its relaxations and [iterative rounding](/iterative-rounding/) were developed in part for it.

## References
