---
tag: ZCQDX5
kind: problem
slug: parameterized-disjoint-paths
name: Parameterized disjoint paths
aliases:
- k-disjoint paths
- linkage problem
area: complexity/parameterized-complexity
level: advanced
summary: "Join k terminal pairs by pairwise vertex-disjoint paths, with parameter k. NP-complete for unbounded k, FPT in k on undirected graphs, and NP-complete for k = 2 on directed graphs."
prereqs: [vertex-disjoint-paths, fixed-parameter-tractable]
see_also: [minor-testing, irrelevant-vertex-technique, grid-minor-theorem, menger-theorem, edge-disjoint-paths, kernel-lower-bounds, para-np-hardness, graph-minor-theorem]
sources:
  - paper: doi:10.1006/jctb.1995.1006
    title: "Neil Robertson and Paul D. Seymour, Graph minors. XIII. The disjoint paths problem, Journal of Combinatorial Theory, Series B 63(1), 65-110 (1995)"
    locator: the main algorithm, k disjoint paths in O(n^3) time for fixed k
  - paper: doi:10.1016/j.jctb.2011.07.004
    title: "Ken-ichi Kawarabayashi, Yusuke Kobayashi and Bruce Reed, The disjoint paths problem in quadratic time, Journal of Combinatorial Theory, Series B 102(2), 424-435 (2012)"
    locator: the main theorem, O(n^2) time for fixed k
  - paper: doi:10.1109/FOCS61266.2024.00014
    title: "Tuukka Korhonen, Michal Pilipczuk and Giannos Stamoulis, Minor containment and disjoint paths in almost-linear time, FOCS 2024, 53-61"
    locator: the main theorem, disjoint paths for fixed k in almost-linear time (arXiv 2404.03958)
  - paper: doi:10.1016/0304-3975(80)90009-2
    title: "Steven Fortune, John Hopcroft and James Wyllie, The directed subgraph homeomorphism problem, Theoretical Computer Science 10(2), 111-121 (1980)"
    locator: NP-completeness of 2 disjoint paths in directed graphs, and the n^O(k) algorithm on acyclic digraphs
  - book: isbn:9780716710455
    title: "Michael R. Garey and David S. Johnson, Computers and Intractability: A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979"
    locator: "Appendix A2, problem ND40, Disjoint connecting paths (NP-complete, with references to Karp 1975 and Lynch 1975)"
  - paper: doi:10.1016/j.tcs.2011.04.039
    title: "Hans L. Bodlaender, Stéphan Thomassé and Anders Yeo, Kernel bounds for disjoint cycles and disjoint paths, Theoretical Computer Science 412(35), 4570-4578 (2011)"
    locator: no polynomial kernel for disjoint paths with parameter k unless NP is a subset of coNP/poly
  - paper: doi:10.1137/070697781
    title: "Aleksandrs Slivkins, Parameterized tractability of edge-disjoint paths on directed acyclic graphs, SIAM Journal on Discrete Mathematics 24(1), 146-157 (2010)"
    locator: W[1]-hardness of edge-disjoint paths on acyclic digraphs with parameter k
  - paper: doi:10.1109/FOCS.2013.29
    title: "Marek Cygan, Daniel Marx, Marcin Pilipczuk and Michal Pilipczuk, The planar directed k-vertex-disjoint paths problem is fixed-parameter tractable, FOCS 2013, 197-206"
    locator: "the main theorem, time 2^(2^O(k^2)) n^O(1) on planar digraphs"
---

The disjoint paths problem asks for $k$ pairwise vertex-disjoint paths that join $k$ given pairs of terminals. The parameter is the number of pairs $k$. When $k$ is part of the input the problem is NP-complete, but on undirected graphs it is [fixed-parameter tractable](/fixed-parameter-tractable/): Robertson and Seymour solved it in time $f(k) \cdot n^3$ in Graph Minors XIII. On directed graphs the problem is NP-complete already for $k = 2$.

## In plain words

You have a network and a list of pairs of points. Each pair wants its own route, and two routes may not share any point. The question is whether all routes can exist at the same time. With many pairs the question is hard. With a few pairs on a network without one-way links, it can be answered in a time that grows like a fixed polynomial in the size of the network, times a huge factor that depends only on the number of pairs. With one-way links, two pairs are already enough to make the question hard. If the routes may start and end at any of the given points, without a fixed pairing, the problem is a flow problem and is easy.

## Definition

- Instance: an undirected graph $G$ with $n$ vertices, given as adjacency lists, and pairs $(s_1, t_1), \dots, (s_k, t_k)$ of vertices of $G$, with all $2k$ terminals distinct.
- Parameter: $k$.
- Question: Are there paths $P_1, \dots, P_k$ in $G$, pairwise vertex-disjoint, such that $P_i$ joins $s_i$ and $t_i$ for each $i$?

A set of such paths is a *linkage*. This problem is different from [vertex-disjoint paths](/vertex-disjoint-paths/) between two vertex sets, where any source may join any sink. That version has no pairing, and by [Menger's theorem](/menger-theorem/) it is solved by maximum flow in polynomial time for every $k$.

## Variants

- **Edge-disjoint paths.** The paths may share vertices but not edges. On undirected graphs this version is also FPT in $k$, by a reduction to the vertex version on the [line graph](/line-graph/) (see Reductions). The flow version without pairing is [edge-disjoint paths](/edge-disjoint-paths/).
- **Directed graphs.** The paths must follow edge directions. Fortune, Hopcroft and Wyllie (1980) proved that the problem is NP-complete for $k = 2$. So the directed problem is [para-NP-hard](/para-np-hardness/) and is not even in XP unless $\mathsf{P} = \mathsf{NP}$.
- **Directed acyclic graphs.** Fortune, Hopcroft and Wyllie gave an $n^{O(k)}$ algorithm, so the problem is in XP. Slivkins (2010) proved that the edge-disjoint version on acyclic digraphs is [W[1]-hard](/w-hardness/), so it is not FPT unless $\mathsf{FPT} = \mathsf{W}[1]$.
- **Planar directed graphs.** Schrijver (1994) gave an $n^{O(k)}$ algorithm. Cygan, Marx, Pilipczuk and Pilipczuk (2013) proved that the problem is FPT, with time $2^{2^{O(k^2)}} \cdot n^{O(1)}$.
- **Two pairs.** For $k = 2$ on undirected graphs there is a structural answer, found around 1980 by Seymour, by Shiloach and by Thomassen: roughly, the answer is no exactly when the graph can be drawn in the plane, after some reductions, with the four terminals on the outer face in the crossing order $s_1, s_2, t_1, t_2$.

## Examples

All answers below come from a brute-force search over the paths of the first pair. In the 3 by 3 grid, number the vertices 0 to 8 in row-major order, so the corners are 0, 2, 6 and 8.

| pairs | linkage? |
|---|---|
| $(0, 8)$ and $(2, 6)$ (the two diagonals) | no |
| $(0, 2)$ and $(6, 8)$ (top and bottom rows) | yes |
| $(0, 6)$ and $(2, 8)$ (left and right columns) | yes |

For the first row, the unpaired question has the answer yes: there are 2 disjoint paths from $\{0, 2\}$ to $\{6, 8\}$, namely 0-3-6 and 2-5-8. The pairing is what makes the problem hard.

On the 4 by 4 grid, take two pairs whose 4 terminals lie on the outer ring of 12 vertices. There are 495 ways to choose the 4 terminals and 3 ways to pair them, so 1485 instances. In 495 of them the pairs cross (they alternate around the ring). A brute-force check gives the answer yes in exactly the 990 instances where the pairs do not cross. This matches the planar two-pair structure in the Variants section.

## Known algorithms

- Robertson and Seymour (Graph Minors XIII, 1995) solve the problem in time $f(k) \cdot n^3$ on a RAM, by the [irrelevant vertex technique](/irrelevant-vertex-technique/) and the structure theory of graph minors.
- Kawarabayashi, Kobayashi and Reed (2012) lower the time to $f(k) \cdot n^2$ on a RAM.
- Korhonen, Pilipczuk and Stamoulis (FOCS 2024) give an algorithm with time almost linear in the size of $G$ for each fixed $k$.
- On graphs of treewidth $t$, the problem is solved by a [dynamic program on a tree decomposition](/dp-on-tree-decompositions/) in time $f(k, t) \cdot n$, or by [Courcelle's theorem](/courcelle-theorem/).

The function $f$ in the general algorithms is huge. The same algorithms solve [minor testing](/minor-testing/).

## Bounds

- **NP-complete when $k$ is part of the input**, under polynomial-time many-one reductions. This is problem ND40, Disjoint connecting paths, in Garey and Johnson, with references to Karp (1975) and Lynch (1975).
- **FPT in $k$** on undirected graphs, by the algorithms above.
- **No polynomial kernel.** Bodlaender, Thomassé and Yeo (2011) proved that the problem with parameter $k$ has no [polynomial kernel](/polynomial-kernel/) unless NP is a subset of coNP/poly. See [kernel lower bounds](/kernel-lower-bounds/).
- **Directed graphs:** NP-complete for $k = 2$ (Fortune, Hopcroft and Wyllie 1980).

## Reductions

- **Edge-disjoint to vertex-disjoint.** Take the line graph $L(G)$, whose vertices are the edges of $G$. For each pair $i$, add a new vertex $s'_i$ adjacent to the edges at $s_i$, and a new vertex $t'_i$ adjacent to the edges at $t_i$. Edge-disjoint paths in $G$ give vertex-disjoint paths from $s'_i$ to $t'_i$ in the new graph. In the other direction, the inner vertices of a path from $s'_i$ to $t'_i$ are edges of $G$ that form a connected subgraph containing $s_i$ and $t_i$, so they contain a path from $s_i$ to $t_i$, and different pairs use different edges. This is a polynomial-time parameterized reduction that keeps $k$.
- **Disjoint paths as a rooted minor problem.** A linkage exists if and only if a graph with $k$ disjoint edges is a minor of $G$ with the endpoints of the edges fixed to the terminals. Graph Minors XIII solves this rooted form and [minor testing](/minor-testing/) with one method.
- **Linkage to flow, when the pairing is dropped.** Without the pairing, add a super source joined to all $s_i$ and a super sink joined to all $t_i$, and ask for a flow of value $k$ with unit vertex capacities. This answers a different question; it is the reason that the unpaired version is in P.

## Applications

- **Routing.** Wire routing in VLSI layout and the setup of circuits in a network ask for disjoint routes between fixed pairs.
- **A subroutine of graph minor algorithms.** The algorithms for [minor testing](/minor-testing/) and for many problems on minor-closed classes call the disjoint paths algorithm.
- **The origin of the irrelevant vertex technique.** The method that Robertson and Seymour built for this problem became a general technique; see [irrelevant vertex technique](/irrelevant-vertex-technique/).

## References
