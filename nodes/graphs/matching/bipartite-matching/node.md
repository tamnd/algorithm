---
tag: NX93A8
kind: problem
slug: bipartite-matching
name: Bipartite matching
aliases:
- maximum bipartite matching
- maximum cardinality bipartite matching
area: graphs/matching
level: core
summary: Find a largest matching in a bipartite graph.
prereqs: [bipartite-graph, augmenting-path]
see_also: [hopcroft-karp, kuhn-algorithm, hall-theorem, konig-theorem, assignment-problem, max-flow-problem, maximum-matching, path-cover-by-bipartite-matching]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.3, Maximum bipartite matching (the reduction to flow), and Section 25.1, Maximum bipartite matching (revisited) (the Hopcroft-Karp algorithm)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 7.5, A First Application, The Bipartite Matching Problem
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 16, Cardinality bipartite matching and vertex cover (Sections 16.1 to 16.5, and the complexity survey in Section 16.7a)
  - paper: doi:10.1137/0202019
    title: John E. Hopcroft and Richard M. Karp, An n^(5/2) algorithm for maximum matchings in bipartite graphs, SIAM Journal on Computing 2(4), 225 to 231 (1973)
    locator: the whole paper
---

Bipartite matching is the problem of finding a largest set of edges with no common end in a [bipartite graph](/bipartite-graph/). It models any one-to-one assignment between two kinds of objects, such as workers and jobs, where only some pairs are allowed. The graph is bipartite and unweighted; with costs on the edges it becomes the [assignment problem](/assignment-problem/), and in a general graph it is the [maximum matching](/maximum-matching/) problem. It is solvable in $O(m\sqrt n)$ time by [Hopcroft-Karp](/hopcroft-karp/), and its min-max theorem, [Kőnig's theorem](/konig-theorem/), says that the answer equals the least size of a [vertex cover](/vertex-cover/).

## In plain words

You have a group of people and a group of tasks. Each person can do only some of the tasks. Each person takes at most one task, and each task goes to at most one person. The goal is to give out as many tasks as possible.

Drawing a line from each person to each task they can do gives a graph with two sides, where every line joins the two sides. A choice of lines in which no person and no task appears twice is a matching. The problem asks for a matching with as many lines as possible. When every person can get a task, the matching shows how.

## Definition

**Input.** A finite undirected graph $G = (X \cup Y, E)$ with $X \cap Y = \emptyset$ and $E \subseteq \{ xy : x \in X, y \in Y \}$. We write $n = |X| + |Y|$ and $m = |E|$. If the sides are not given, a [bipartite test](/bipartite-testing/) finds them in $O(n + m)$ time, or reports an odd cycle.

**Output.** A matching $M \subseteq E$, that is, a set of edges with $|\{e \in M : v \in e\}| \le 1$ for every vertex $v$, of the largest size

$$\nu(G) = \max \{ |M| : M \subseteq E \text{ is a matching} \}.$$

A matching is *perfect* if it covers every vertex, which needs $|X| = |Y| = \nu(G)$.

**Certificate of optimality.** A set $C \subseteq X \cup Y$ that meets every edge with $|C| = |M|$. Every matching has at most $|C|$ edges, because each edge of a matching needs its own vertex of $C$, so $M$ is then maximum. By [Kőnig's theorem](/konig-theorem/) such a $C$ always exists, and augmenting-path algorithms find it.

## Variants

- **Decision: perfect matching.** Does $G$ have a [perfect matching](/perfect-matching/)? By [Hall's theorem](/hall-theorem/), yes if and only if $|X| = |Y|$ and $|N(S)| \ge |S|$ for all $S \subseteq X$.
- **Saturating one side.** Is there a matching that covers all of $X$? Hall's condition again, without $|X| = |Y|$.
- **Weighted.** With weights on the edges, find a matching of largest weight, or a perfect matching of least cost: the [assignment problem](/assignment-problem/) and [maximum weight matching](/maximum-weight-matching/).
- **Bottleneck.** Find a perfect matching whose largest edge cost is least: [bottleneck matching](/bottleneck-matching/).
- **Capacities.** Each vertex $v$ may take up to $b(v)$ edges: [b-matching](/b-matching/), which in bipartite graphs is a flow problem.
- **Preferences.** Each vertex ranks its neighbours, and the goal is a matching with no blocking pair: [stable matching](/stable-matching/) and the [hospitals-residents problem](/hospitals-residents-problem/).
- **Counting.** The number of perfect matchings of $G$ is the permanent of its $|X| \times |Y|$ biadjacency matrix. Counting them is #P-complete (Valiant, 1979), although deciding whether one exists is easy.
- **Online.** The vertices of $Y$ arrive one at a time with their edges, and each must be matched or rejected at once. The RANKING algorithm of Karp, Vazirani and Vazirani matches at least $(1 - 1/e)\nu(G)$ vertices in expectation, and no online algorithm does better against every input.
- **Dynamic.** Edges are inserted and deleted, and a large matching must be kept: [dynamic matching](/dynamic-matching/).

## Examples

**Five people and five tasks.** Let $X = \{A, B, C, D, E\}$ and $Y = \{1, 2, 3, 4, 5\}$, with $A$, $B$ and $C$ each adjacent to 1 and 2, $D$ adjacent to 3 and 4, and $E$ adjacent to 4 and 5.

- A maximum matching is $\{A1, B2, D3, E4\}$, so $\nu(G) = 4$.
- No perfect matching exists: $S = \{A, B, C\}$ has $N(S) = \{1, 2\}$, so one of $A$, $B$, $C$ is left out. This is the deficiency form of Hall's theorem, $\nu = 5 - (3 - 2)$.
- The vertex cover $C = \{1, 2, D, E\}$ has 4 vertices, so it certifies that 4 is optimal.

**Edge cases.**

| input | $\nu(G)$ | a maximum matching |
|---|---|---|
| no edges, any number of vertices | 0 | $\emptyset$ |
| $X = \emptyset$ | 0 | $\emptyset$ |
| complete bipartite $K_{3,5}$ | 3 | three disjoint edges, saturating the side of size 3 |
| star $K_{1,4}$ | 1 | any one edge |
| even cycle $C_6$ | 3 | every second edge, a perfect matching |
| the 3-cube $Q_3$, 3-regular | 4 | a perfect matching, as every regular bipartite graph has one |

**Not an instance.** The odd cycle $C_5$ is not bipartite. Its maximum matching has 2 edges, and the bipartite algorithms do not apply to it; use a [general matching](/maximum-matching/) algorithm such as [Edmonds' blossom algorithm](/edmonds-blossom/).

## Known algorithms

- [Kuhn's algorithm](/kuhn-algorithm/) (the Hungarian method for unit weights): one [augmenting path](/augmenting-path/) per search, $O(nm)$ time.
- [Ford-Fulkerson](/ford-fulkerson/) on the unit-capacity flow network: the same as Kuhn's algorithm, $O(nm)$ time.
- [Hopcroft-Karp](/hopcroft-karp/): a maximal set of shortest vertex-disjoint augmenting paths in each phase, $O(\sqrt n)$ phases, $O(m\sqrt n)$ time.
- [Dinic's algorithm](/dinic/) on the unit-capacity network: $O(m\sqrt n)$ time; on this network it does the same work as Hopcroft-Karp.
- [Push-relabel](/push-relabel/) methods: $O(m\sqrt n)$ with suitable rules, and fast in practice.
- Algebraic methods: a [Tutte matrix](/tutte-matrix/) or the biadjacency matrix with random entries gives a randomized $O(n^{\omega})$ algorithm, where $\omega < 2.38$ is the exponent of matrix multiplication (Mucha and Sankowski, 2004). See [RNC perfect matching](/rnc-perfect-matching/).
- [Almost-linear max flow](/almost-linear-max-flow/): $m^{1 + o(1)}$ time, by the reduction to flow below.

## Bounds

- **Upper bound.** $m^{1+o(1)}$ time, through the almost-linear time maximum flow algorithm of Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva (2022). For a simple combinatorial algorithm, $O(m\sqrt n)$ by Hopcroft-Karp (1973). Schrijver's Section 16.7a surveys the bounds between these.
- **Lower bound.** $\Omega(n + m)$ in the adjacency-list model in the worst case: an algorithm that never reads some edge $xy$ of a graph whose only perfect matching uses $xy$ cannot tell it from the same graph without $xy$. No better lower bound is known for general algorithms.
- **Regular graphs.** A $k$-regular bipartite graph has a perfect matching by Hall's theorem, and it can be found in $O(m)$ time (Cole, Ost and Schirra, 2001).
- **The value.** $\nu(G) \le \min(|X|, |Y|)$, and $\nu(G) = \tau(G)$ by Kőnig's theorem. In every graph, a [maximal matching](/maximal-matching/) has at least $\nu(G)/2$ edges.

## Reductions

- **To maximum flow.** Add a source $s$ with an arc of capacity 1 to each $x \in X$, a sink $t$ with an arc of capacity 1 from each $y \in Y$, and orient each edge from $X$ to $Y$ with capacity 1. By the [integrality theorem](/flow-integrality-theorem/), a maximum flow can be taken with values 0 and 1, and its arcs from $X$ to $Y$ that carry flow form a maximum matching. The network has $n + 2$ nodes and $n + m$ arcs. See the [max flow problem](/max-flow-problem/).
- **To general matching.** A bipartite graph is a graph, so any [maximum matching](/maximum-matching/) algorithm solves it, at a higher cost.
- **Minimum vertex cover and maximum independent set.** From a maximum matching, Kőnig's construction gives a minimum vertex cover in $O(n + m)$ time, and its complement is a [maximum independent set](/bipartite-maximum-independent-set/).
- **Minimum path cover of a DAG.** Split each vertex $v$ into $v^{\text{out}} \in X$ and $v^{\text{in}} \in Y$, and add an edge $u^{\text{out}}v^{\text{in}}$ for each arc $uv$. A DAG with $n$ vertices can be covered by $n - \nu$ vertex-disjoint paths and no fewer. See [path cover by bipartite matching](/path-cover-by-bipartite-matching/). Dilworth's theorem on chains in a partial order follows in the same way; see [Dilworth's theorem](/dilworth-theorem/).
- **Minimum edge cover.** By [Gallai's identity](/gallai-identity/), a maximum matching plus one edge at each free vertex is a minimum [edge cover](/edge-cover/).

## Applications

- Assigning workers to jobs, students to projects, or tasks to machines, when each pair is allowed or not.
- Scheduling: rounds of a tournament or time slots for meetings, through the edge colouring of a bipartite graph by repeated perfect matchings.
- Sparse matrix computation: a maximum matching of the row-column graph puts nonzero entries on the diagonal before a factorization, and the [Dulmage-Mendelsohn decomposition](/dulmage-mendelsohn-decomposition/) gives a block triangular form.
- Image and data association: matching detected objects in two frames, or records in two databases, when only some pairs are plausible.
- A subroutine in the [Hungarian algorithm](/hungarian-algorithm/), and in [edge colouring](/edge-coloring/) of bipartite graphs.

## References
