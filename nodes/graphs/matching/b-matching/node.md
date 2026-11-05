---
tag: SD154P
kind: problem
slug: b-matching
name: b-matching
aliases:
- capacitated matching
- degree-constrained subgraph
area: graphs/matching
level: advanced
summary: Choose edges so that each vertex v has at most b(v) chosen edges incident to it.
prereqs: [bipartite-matching]
see_also: [f-factor-problem, maximum-matching, max-flow-problem, min-cost-flow-problem, fractional-matching, edmonds-blossom, assignment-problem, edmonds-polytope-theorem]
sources:
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 21, Bipartite b-matchings and transportation, and Chapters 31 to 33, b-matchings, capacitated b-matchings, and simple b-matchings and b-factors
  - paper: doi:10.4153/CJM-1954-033-3
    title: William T. Tutte, A short proof of the factor theorem for finite graphs, Canadian Journal of Mathematics 6, 347 to 352 (1954)
    locator: the whole paper (the reduction of degree-constrained subgraphs to perfect matchings by vertex gadgets)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing (2009 reprint of the 1986 edition)
    locator: Chapter 10, The f-factor problem (b-matchings, f-factors and the reductions to matching)
---

The b-matching problem gives each vertex $v$ of a [graph](/graph/) a capacity $b(v)$ and asks for a largest set of edges in which each vertex $v$ meets at most $b(v)$ chosen edges. With $b \equiv 1$ it is [maximum matching](/maximum-matching/). In a [bipartite graph](/bipartite-graph/) it is a [maximum flow](/max-flow-problem/) problem, and with edge weights a [min-cost flow](/min-cost-flow-problem/) problem; in a general graph it reduces to ordinary matching by a gadget of Tutte. The page covers both bipartite and general graphs, without weights and with them.

## In plain words

In a matching every point takes at most one partner. In a b-matching each point has its own quota: a teacher may take up to three students, a server up to ten clients, and a student only one teacher. The task is to choose as many links as possible without any point going over its quota.

When the points split into two sides with links only across, the problem is a pipe network: water flows from a source through each point of one side, across a link, and through a point of the other side to a sink, and each point lets through only its quota. When links can join any two points, odd loops make it harder, but each point can be copied as many times as its quota and the problem turns into ordinary pairing.

## Definition

**Input.** A finite undirected graph $G = (V, E)$, bipartite or general, and a capacity $b: V \to \mathbb{Z}_{\ge 0}$. Optionally, edge weights $w: E \to \mathbb{R}$.

**Simple b-matching.** A set $F \subseteq E$ with $\deg_F(v) \le b(v)$ for every $v \in V$, where $\deg_F(v)$ is the number of edges of $F$ at $v$. The goal is to maximize $|F|$, or $w(F)$ in the weighted version. This is the *degree-constrained subgraph* problem.

**Uncapacitated b-matching.** A vector $x \in \mathbb{Z}_{\ge 0}^E$ with $x(\delta(v)) = \sum_{e \ni v} x_e \le b(v)$ for every $v$, so an edge may be used several times. The *capacitated* version adds $x_e \le c(e)$; simple b-matching is the case $c \equiv 1$.

**Perfect b-matching.** Equality $\deg_F(v) = b(v)$ at every vertex. A perfect simple b-matching is an $f$-factor with $f = b$, the subject of the [f-factor problem](/f-factor-problem/).

The size of a b-matching is at most $\lfloor \frac12 \sum_v b(v) \rfloor$, since each edge uses two units of capacity. For $V = \emptyset$ or $E = \emptyset$ the only b-matching is empty.

## Variants

- **Matching.** $b \equiv 1$: [maximum matching](/maximum-matching/), or [bipartite matching](/bipartite-matching/) when $G$ is bipartite.
- **Weighted.** Maximize $w(F)$; the bipartite weighted case with perfect constraints on both sides is the transportation problem, and with $b \equiv 1$ the [assignment problem](/assignment-problem/).
- **2-matchings.** $b \equiv 2$. Perfect simple 2-matchings are 2-factors, spanning unions of disjoint cycles, used as a relaxation of the travelling salesman problem.
- **Lower and upper bounds.** $a(v) \le \deg_F(v) \le b(v)$, the general degree-constrained subgraph problem; Lovász's general factor problem allows an arbitrary set of degrees at each vertex and is NP-hard when the sets have gaps of length 2 or more.
- **b-edge cover.** Each vertex must meet *at least* $b(v)$ chosen edges, with as few edges as possible; it is the complement of a simple b-matching with capacities $\deg(v) - b(v)$, the analogue of [edge cover](/edge-cover/).
- **Fractional.** Relax $x$ to real values: the fractional b-matching linear program, which is integral for bipartite graphs and half-integral in general, as for [fractional matching](/fractional-matching/).

## Examples

| graph | $b$ | best | a b-matching |
|---|---|---|---|
| no edges | any | 0 | $\emptyset$ |
| triangle $abc$ | $1, 1, 1$ | 1 | $\{ab\}$ |
| triangle $abc$ | $2, 2, 2$ | 3 | all three edges, a 2-factor |
| star $K_{1,3}$, centre $c$ | $c$: 2, leaves: 1 | 2 | two edges at $c$ |
| path $a\,b\,c$ | $a$: 1, $b$: 2, $c$: 1 | 2 | both edges, a perfect b-matching |
| one edge $uv$, uncapacitated | $3, 2$ | 2 | $x_{uv} = 2$ |

**No perfect b-matching.** The triangle with $b \equiv 1$ has $\sum b = 3$, which is odd, so no perfect b-matching exists. The star $K_{1,3}$ with $b = 2$ at the centre and 1 at each leaf has $\sum b = 5$; its best value 2 leaves one leaf uncovered. Parity is not the only obstruction: the star $K_{1,3}$ with $b = 1$ everywhere has $\sum b = 4$ but only one edge fits.

**Reviewer assignment, bipartite.** Reviewers $r_1, r_2$ with $b = 2$ each, papers $p_1, p_2, p_3$ with $b = 1$ each, and edges $r_1 p_1, r_1 p_2, r_2 p_2, r_2 p_3$. The b-matching $\{r_1 p_1, r_1 p_2, r_2 p_3\}$ covers every paper, of size 3, the upper bound $\sum_{\text{papers}} b$.

## Known algorithms

- **Bipartite, by flow.** With sides $X$ and $Y$, add a source $s$ with an arc $s \to u$ of capacity $b(u)$ for $u \in X$, an arc $u \to v$ of capacity 1 (simple) or unbounded (uncapacitated) for each edge, and an arc $v \to t$ of capacity $b(v)$ for $v \in Y$. By the [integrality theorem](/integrality-theorem/), an integer maximum flow, found by [Dinic's algorithm](/dinic/) or any other maximum flow method, is a maximum b-matching. With costs $-w$ on the middle arcs, a [min-cost flow](/min-cost-flow-problem/) gives the weighted version.
- **General, by Tutte's gadget.** Replace each vertex $v$ by $b(v)$ copies, and each edge $e = uv$ by two new vertices $e_u, e_v$ with the edge $e_u e_v$, $e_u$ joined to all copies of $u$ and $e_v$ to all copies of $v$. A simple b-matching $F$ gives a matching of size $|E| + |F|$: match $e_u$ and $e_v$ to distinct copies for $e \in F$, and use $e_u e_v$ for $e \notin F$. Conversely a gadget contributes two edges only when both $e_u$ and $e_v$ go to copies. So the maximum b-matching has size $\nu(G') - |E|$, found by [Edmonds' blossom algorithm](/edmonds-blossom/) on $G'$. The weighted version uses weighted matching on the same gadget.
- **Strongly polynomial methods.** The gadget has $\sum_v b(v) + 2|E|$ vertices, so it is only pseudo-polynomial when $b$ is large. Polynomial algorithms first solve the fractional relaxation by flow on the bipartite double cover, round to a near-optimal integer solution, and finish with a few augmentations on a graph of size independent of $b$ (Anstee); Gabow gave direct blossom-style algorithms for b-matching. Schrijver's Chapters 31 to 33 survey the bounds.

## Bounds

- **Upper bounds.** Bipartite: the cost of one maximum flow or min-cost flow computation on a network with $|V| + 2$ nodes and $|V| + |E|$ arcs. General simple b-matching: polynomial in $|V|$ and $|E|$ alone, independent of the size of $b$, by the strongly polynomial methods above.
- **Min-max formula.** For bipartite $G$, the maximum size of a simple b-matching equals $\min_{X' \subseteq X,\, Y' \subseteq Y} \bigl( b(X \setminus X') + b(Y \setminus Y') + |E(X', Y')| \bigr)$, by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) on the network above: a cut either pays $b$ at a vertex or cuts the edges between the kept sets. For general graphs Tutte's f-factor theorem, applied through the gadget, gives a formula of Tutte-Berge type.
- **Polytope.** For bipartite graphs the degree constraints describe the b-matching polytope. In general graphs, Edmonds added the odd-set constraints $x(E[U]) \le \lfloor b(U)/2 \rfloor$ for the uncapacitated case, generalizing [Edmonds' matching polytope theorem](/edmonds-polytope-theorem/), with blossom-type constraints with edge sets for the capacitated case.

## Reductions

- **From matching.** $b \equiv 1$.
- **To max flow and min-cost flow,** for bipartite graphs, as above.
- **To maximum matching,** for general graphs, by Tutte's gadget; perfect b-matchings correspond to perfect matchings of the gadget graph that use the copies fully.
- **To perfect matching for f-factors.** The [f-factor problem](/f-factor-problem/) asks for a perfect simple b-matching; Tutte's second gadget, with $\deg(v) - f(v)$ inner vertices per vertex, reduces it to [perfect matching](/perfect-matching/) in a graph with $O(|E|)$ vertices.
- **b-edge cover to b-matching** by complementing: $F$ is a b-edge cover if and only if $E \setminus F$ is a simple b-matching for the capacities $\deg(v) - b(v)$.

## Applications

- Assigning reviewers to papers, students to schools, or jobs to machines, where one side has quotas: bipartite b-matching, or its stable version, the [hospitals/residents problem](/hospitals-residents-problem/).
- Graph sparsification in machine learning: a maximum-weight b-matching of a similarity graph gives a balanced neighbourhood graph in which every point keeps at most $b$ neighbours.
- The 2-matching relaxation of the travelling salesman problem, solved as a b-matching with $b \equiv 2$ and strengthened by subtour and comb inequalities.
- Network design and peer-to-peer overlays, where each node may keep a bounded number of connections and the total link weight should be large.

## References
