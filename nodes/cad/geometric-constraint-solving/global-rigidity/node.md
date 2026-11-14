---
tag: X32JGR
kind: definition
slug: global-rigidity
name: Global rigidity
aliases:
- unique realizability
area: cad/geometric-constraint-solving
level: advanced
summary: A framework is globally rigid when every framework with the same bar lengths is congruent to it, so the constraint system has one solution up to rigid motion.
prereqs: [bar-and-joint-framework, generic-rigidity]
see_also: [jackson-jordan-theorem, generic-rigidity, laman-theorem, henneberg-construction, root-identification-problem, well-constrained-system, distance-based-formation-control, k-vertex-connected-graph]
sources:
  - paper: doi:10.1137/0221008
    title: Bruce Hendrickson, Conditions for unique graph realizations, SIAM Journal on Computing 21(1), 65 to 84, 1992
    locator: the necessary conditions for generic global rigidity, (d + 1)-connectivity and redundant rigidity
  - paper: doi:10.1007/s00454-004-1124-4
    title: Robert Connelly, Generic global rigidity, Discrete and Computational Geometry 33(4), 549 to 563, 2005
    locator: the stress matrix condition that implies global rigidity of a generic framework
  - paper: doi:10.1353/ajm.0.0132
    title: Steven J. Gortler, Alexander D. Healy and Dylan P. Thurston, Characterizing generic global rigidity, American Journal of Mathematics 132(4), 897 to 939, 2010
    locator: the converse of Connelly's condition, so generic global rigidity is a property of the graph in every dimension
  - paper: doi:10.1016/j.jctb.2004.11.002
    title: Bill Jackson and Tibor Jordán, Connected rigidity matroids and unique realizations of graphs, Journal of Combinatorial Theory, Series B 94(1), 1 to 29, 2005
    locator: the characterization of generic global rigidity in the plane
  - paper: doi:10.1109/TMC.2006.174
    title: J. Aspnes, T. Eren, D. K. Goldenberg, A. S. Morse, W. Whiteley, Y. R. Yang, B. D. O. Anderson and P. N. Belhumeur, A theory of network localization, IEEE Transactions on Mobile Computing 5(12), 1663 to 1678, 2006
    locator: unique localization of a sensor network and its relation to global rigidity
  - paper: "James B. Saxe, Embeddability of weighted graphs in k-space is strongly NP-hard, Proceedings of the 17th Allerton Conference on Communication, Control and Computing, 480 to 489, 1979"
    locator: strong NP-hardness of realizability in every fixed dimension, and the hardness of deciding whether a realization is unique, already on the line
---

A [framework](/bar-and-joint-framework/) is globally rigid when its bar lengths determine all distances between its joints: every framework in the same space with the same bar lengths is congruent to it. Rigidity asks this only for frameworks near the given one, so a rigid framework can still have a second, distant realization, and a constraint solver that finds a solution of a rigid system may find the wrong one. Global rigidity is what a sensor network needs for unique positions and what a CAD sketch would need to have exactly one solution. In the plane its generic form has a combinatorial test, the [Jackson-Jordán theorem](/jackson-jordan-theorem/).

## Definition

Let $(G, p)$ be a framework in $\mathbb{R}^d$: a graph $G = (V, E)$ with $n$ vertices and a placement $p$ of the vertices.

**Equivalent and congruent.** A framework $(G, q)$ in $\mathbb{R}^d$ is *equivalent* to $(G, p)$ if $|q_i - q_j| = |p_i - p_j|$ for every edge $ij$. It is *congruent* to $(G, p)$ if this holds for every pair $i, j$ of vertices, which means that $q$ is the image of $p$ under an isometry of $\mathbb{R}^d$.

**Global rigidity.** $(G, p)$ is *globally rigid* if every framework in $\mathbb{R}^d$ equivalent to it is congruent to it. Compare *rigidity*: $(G, p)$ is rigid if every equivalent framework close enough to $p$ is congruent to it. So global rigidity implies rigidity.

**Generic global rigidity.** $G$ is *generically globally rigid* in $\mathbb{R}^d$ if $(G, p)$ is globally rigid for every generic placement $p$, one whose coordinates are algebraically independent over $\mathbb{Q}$. Gortler, Healy and Thurston (2010) proved that if one generic framework of $G$ is globally rigid, then all are, so this is a property of the graph, as [generic rigidity](/generic-rigidity/) is.

**Redundant rigidity.** $G$ is *redundantly rigid* in $\mathbb{R}^d$ if $G - e$ is generically rigid for every edge $e$.

**Proposition 1 (connectivity, Hendrickson 1992).** Let $n \ge d + 2$. If $G$ is generically globally rigid in $\mathbb{R}^d$, then $G$ is $(d + 1)$-connected.

*Proof.* Suppose that a set $S$ of at most $d$ vertices separates $G$, so $V \setminus S = A \cup B$ with $A, B$ nonempty and no edge between $A$ and $B$. Take a generic $p$. The at most $d$ points $p(S)$ lie on a hyperplane $H$, and since $p$ is generic we may choose $H$ through no other point of $p$. Let $\sigma$ be the reflection in $H$, and let $q_i = \sigma(p_i)$ for $i \in B$ and $q_i = p_i$ otherwise. Every edge lies inside $A \cup S$ or inside $B \cup S$. On the first set $q = p$, and on the second $q = \sigma \circ p$, where $\sigma$ is an isometry, so all edge lengths stay. Take $x \in A$ and $y \in B$. Then $|q_x - q_y| = |p_x - \sigma(p_y)|$, and this equals $|p_x - p_y|$ only if $p_x$ lies on the perpendicular bisector of $p_y$ and $\sigma(p_y)$, which is $H$. It does not, so $(G, q)$ is equivalent to $(G, p)$ and not congruent to it. $\square$

**Proposition 2 (redundant rigidity, Hendrickson 1992).** Let $n \ge d + 2$. If $G$ is generically globally rigid in $\mathbb{R}^d$, then $G$ is redundantly rigid.

*Proof sketch* (Hendrickson 1992, the section on redundant rigidity). Let $p$ be generic and suppose that $G - e$ is not rigid for some edge $e = uv$. Add edges to $G - e$, if needed, to get a graph $H$ whose generic frameworks have exactly one degree of freedom up to congruence; every framework equivalent to $(H + e, p)$ is equivalent to $(G, p)$. Near $p$, the frameworks equivalent to $(H, p)$, taken up to congruence, form a smooth curve. Hendrickson shows that its component through $p$ is compact, so it is a closed curve, and that the length of $e$, as a smooth function on this curve, takes the value $|p_u - p_v|$ at a second point $q$ that is not congruent to $p$. Then $(G, q)$ is equivalent to $(G, p)$ and not congruent to it.

**Sufficient conditions.** Connelly (2005) proved that a generic framework with an equilibrium stress whose stress matrix has rank $n - d - 1$ is globally rigid, and Gortler, Healy and Thurston (2010) proved the converse for generic frameworks. In the plane, Jackson and Jordán (2005) proved that for $n \ge 4$ the two necessary conditions above are also sufficient. So a graph is generically globally rigid in the plane if and only if it is a complete graph on at most 3 vertices or it is 3-connected and redundantly rigid. In $\mathbb{R}^3$ the two conditions are not sufficient, as Connelly showed with $K_{5,5}$, and no combinatorial test is known.

**Hardness for given lengths.** For a given framework, not a generic one, global rigidity is hard to decide. Already on the line, a cycle $1, 2, \ldots, k$ with lengths $a_1, \ldots, a_k$ has a realization exactly when there are signs $\epsilon_t \in \{\pm 1\}$ with $\sum_t \epsilon_t a_t = 0$, since the steps of a closed walk on a line must sum to zero. This is the [partition problem](/partition-problem/), so it is NP-complete to decide whether given lengths can be realized at all. Saxe (1979) proved that realizability is NP-hard in every fixed dimension and that deciding whether a realization is unique is also hard.

**For robotics and sensors.** A team of robots or a sensor network that knows some of its pairwise distances, plus the positions of at least $d + 1$ anchors in general position, can compute unique positions only if the graph with the anchors joined to each other is globally rigid, as Aspnes and others (2006) put it. Rigidity alone only gives finitely many candidate positions.

## Examples and non-examples

- **Complete graphs.** $K_n$ is globally rigid at every placement, because all distances are given, so the realization is fixed up to an isometry.
- **$K_4$ minus an edge.** Put $p_a = (0, 0)$, $p_b = (2, 0)$, $p_c = (1, 1)$, $p_d = (1, -2)$, with all edges except $cd$. The framework is rigid. Reflect $d$ in the line $ab$ to $q_d = (1, 2)$: the lengths of $ad$ and $bd$ stay $\sqrt{5}$, but $|cd|$ changes from 3 to 1. So it is rigid and not globally rigid. Its graph is a Laman graph, so it is not redundantly rigid, and it is only 2-connected, since $\{a, b\}$ separates $c$ from $d$.
- **Wheels.** A wheel, a cycle of $k \ge 3$ vertices plus a hub joined to all of them, has $n = k + 1$ vertices and $2k = 2n - 2$ edges. It is 3-connected, and removing any edge leaves a Laman graph, so it is redundantly rigid. So it is generically globally rigid in the plane.
- **$K_{3,3}$ and the prism.** Both are 3-connected, but they have $9 = 2n - 3$ edges and are minimally rigid, so not redundantly rigid. Their generic frameworks are rigid and have a second realization that is not congruent. A CAD sketch with this graph has several solutions, and since every vertex has degree 3, a solver that places one point at a time from two placed points cannot start on it.
- **A collinear chain.** Four joints at $0, 1, 2, 3$ on a line in the plane, with bars of lengths $1, 1, 1$ between neighbors and a bar of length 3 between the ends, form a globally rigid framework: equality in the triangle inequality forces every equivalent framework to be collinear in the same order. It is not infinitesimally rigid and not generic, and its graph, a 4-cycle, is not even generically rigid. Global rigidity of one framework says nothing about the generic case.
- **A chain of triangles.** A strip of $k$ triangles, each sharing an edge with the next, is rigid, but each triangle can be flipped across its shared edge, which gives up to $2^{k - 1}$ realizations that are not congruent. This is the source of the [root identification problem](/root-identification-problem/) in CAD.

## Related definitions

- **[Generic rigidity](/generic-rigidity/).** The local version. Generic global rigidity implies generic rigidity, and in the plane it also needs one more edge in every part, through redundant rigidity.
- **[Jackson-Jordán theorem](/jackson-jordan-theorem/).** The characterization of generic global rigidity in the plane by 3-connectivity and redundant rigidity.
- **[Henneberg construction](/henneberg-construction/).** Edge splits keep generic global rigidity (Connelly 2005), and with edge additions they build every 3-connected, redundantly rigid graph in the plane from $K_4$.
- **Universal rigidity.** A stronger property: every equivalent framework in any $\mathbb{R}^{d'}$, $d' \ge d$, is congruent. It can be tested for a given framework by [semidefinite programming](/semidefinite-programming/) in some cases.
- **[Well-constrained system](/well-constrained-system/).** A well-constrained system has finitely many solutions up to rigid motion; a globally rigid one has exactly one.
- **[Vertex connectivity](/k-vertex-connected-graph/).** The $(d + 1)$-connectivity of Proposition 1 is the usual vertex connectivity of the graph.

## References
