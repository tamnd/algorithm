---
tag: HMKXPX
kind: algorithm
slug: frontier-vertex-algorithm
name: Frontier vertex algorithm
aliases:
- Hoffmann-Lomonosov-Sitharam frontier algorithm
area: cad/geometric-constraint-solving
level: research
summary: Builds a DR-plan of a constraint graph by finding minimal dense clusters with network flow and collapsing each to its frontier vertices, step by step.
model: word-ram
complexity:
  vars: {n: the number of entities, m: the number of constraints}
  time: {worst: "O(m^5 (n + m)^2)", best: "Θ(n + m)"}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2001
  people: [Christoph M. Hoffmann, Andrew Lomonosov, Meera Sitharam]
  note: Hoffmann, Lomonosov and Sitharam found dense subgraphs by network flow in 1997, and in 2001 they defined DR-plans and gave the Frontier algorithm, which keeps the frontier vertices of each cluster so that clusters can share entities.
prereqs: [dr-plan, degrees-of-freedom-analysis, maximum-weight-closure]
see_also: [laman-theorem, generic-rigidity, pebble-game-rigidity, fudos-hoffmann-reduction, owen-triconnected-decomposition, double-banana-graph, max-flow-min-cut-theorem, witness-configuration-method]
sources:
  - paper: doi:10.1006/jsco.2000.0403
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Decomposition plans for geometric constraint problems, Part II, New algorithms, Journal of Symbolic Computation 31(4), 409 to 427, 2001
    locator: the Frontier algorithm, its simplification of a cluster to its frontier vertices and one core vertex, and its modified form MFA (general locator)
  - paper: doi:10.1006/jsco.2000.0402
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Decomposition plans for geometric constraint systems, Part I, Performance measures for CAD, Journal of Symbolic Computation 31(4), 367 to 408, 2001
    locator: the definition of a DR-plan and the measures by which DR-planners are compared (general locator)
  - paper: doi:10.1007/BFb0017460
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Finding solvable subsets of constraint graphs, Principles and Practice of Constraint Programming (CP97), LNCS 1330, 1997
    locator: the network flow test for dense subgraphs and the reduction of a dense subgraph to a minimal one (general locator)
  - paper: doi:10.1007/BF01534980
    title: G. Laman, On graphs and rigidity of plane skeletal structures, Journal of Engineering Mathematics 4(4), 331 to 340, 1970
    locator: the counts that make a minimal dense set of points and distances rigid in the plane
  - paper: doi:10.1016/j.cagd.2015.07.001
    title: Troy Baker, Meera Sitharam, Menghan Wang and Joel Willoughby, Optimal decomposition and recombination of isostatic geometric constraint systems for designing layered materials, Computer Aided Geometric Design 40, 1 to 25, 2015
    locator: the abstract and introduction, on canonical DR-plans and the hardness of optimal DR-planning
---

The Frontier vertex algorithm of Hoffmann, Lomonosov and Sitharam builds a [DR-plan](/dr-plan/) for a weighted constraint graph. It starts with every constraint as a small cluster. Then it repeats one step: find a smallest set of clusters and entities that is dense, that is, has no more degrees of freedom than one rigid body, by the network flows of [degrees of freedom analysis](/degrees-of-freedom-analysis/); record that set as a new cluster with the old clusters as its children; and replace the new cluster in the graph by its *frontier vertices*, the entities that still have constraints to the outside, tied to one new core vertex. Keeping the frontier vertices is what lets two clusters share an entity, which the older planners that contract a cluster to one node get wrong. For points and distances in the plane, every cluster it finds is rigid and the roots of the plan are the rigid components of the graph.

## In plain words

A drawing has many points and many rules between them. Some groups of points are fixed in shape by their own rules. The method finds such a group, the smallest one it can, and writes it down as one stiff piece. Then it simplifies the drawing: the inside of the piece is replaced by one block, but the points of the piece that touch other rules stay, so other pieces can still use them. On the simpler drawing it looks for the next small stiff group, which may now contain whole pieces, and so on. When no stiff group is left, the record of which piece was built from which smaller pieces is a plan for the solver: solve the small pieces first, then put them together.

## The problem

The input is a constraint graph $G = (V, E)$ in the sense of the [constraint graph](/geometric-constraint-graph/) page. Each entity $v$ has a weight $w(v) > 0$, its degrees of freedom, and each constraint $e$ has a weight $w(e) > 0$, the number of equations it adds. $D$ is the number of degrees of freedom of a rigid body: 3 in the plane and 6 in space. For a set $X$ of entities, let $E(X)$ be the constraints with all their entities in $X$, and let the density be
$$ \rho(X) = w(E(X)) - w(X). $$
This page calls $X$ *dense* when $\rho(X) \ge -D$, as Hoffmann, Lomonosov and Sitharam do. (The [DR-plan](/dr-plan/) page calls such a set rigid, and the [constraint graph](/geometric-constraint-graph/) page keeps "dense" for $\rho(X) > -D$.) The main case is points and distances in the plane: $w(v) = 2$, $w(e) = 1$ and $D = 3$, so $\rho(X) = |E(X)| - 2|X|$ and the counts are those of [Laman's theorem](/laman-theorem/).

The output is a DR-plan: a list of *clusters*, each with its vertex set $U \subseteq V$, its *children* (earlier clusters), its *leaves* (entities of $U$ in no child), its frontier and its density $\rho(U)$ in $G$. Each cluster is the union of its children and leaves, and the *roots* are the clusters that are no one's child, together with the entities in no constraint. A set $X$ with $|X| \ge 2$ is *rigid* when $G[X]$ is [generically rigid](/generic-rigidity/) in the plane, and the *rigid components* of $G$ are the maximal rigid sets.

## The algorithm

The algorithm works on a *simplified graph* $S$. Its nodes are *points*, the entities that are still present, and *cores*, one for each cluster that is not yet a child of another one. A cluster $K$ with frontier $F$ is shown in $S$ as its core $c$, of weight $D$, with an edge $cf$ of weight $w(f)$ to each $f \in F$. The rest of $K$ is gone from $S$. The core, its frontier and these edges have density $|F| \cdot w(f) - D - |F| \cdot w(f) = -D$ when all frontier weights are equal, so they look like one rigid body, which is what the cluster is.

A set of nodes of $S$ is *closed* when it holds the whole frontier of each core in it, and a *target* is a closed set that is dense and holds at least two cores. A target that holds two cores and no shared point would have density at most $-2D$, so every target holds two cores $a$ and $b$ that share a point, a *candidate pair*. Given $a$ and $b$, a set $Z$ of largest density with $\{a, b\} \subseteq Z \subseteq S$ is a [maximum-weight closure](/maximum-weight-closure/): an edge of $S$ is a profit $w(e)$ that needs both its ends, and a node is a cost $w(x)$. One [minimum cut](/min-cut-problem/) finds it.

```pseudo id=main
FRONTIER(V, E, w, D)
L1  for each constraint uv of E, unless uv already lies inside a cluster do
L2      SIMPLIFY({u, v})                                      ▷ each constraint starts as a cluster
L3  repeat
L4      for each candidate pair {a, b} of S do
L5          Z ← MAX-CLOSURE(S, {a, b});  if ρ(Z) ≥ -D then X ← Z plus the frontier of each core in Z;  leave the for
L6      if no pair gave a dense set then leave the repeat
L7      while some core c of X has a target inside X ∖ {c} do
L8          search X ∖ {c}, without the points that touch no other core of X, as in lines L4 and L5
L9          X ← the target found
L10     SIMPLIFY(X):  U ← the union of the vertex sets of the nodes of X
L11         add to X every core whose cluster lies inside U;  their clusters are the children
L12         F ← the points of X with a neighbor outside X                ▷ the frontier
L13         delete from S the nodes of X that are not in F, and the edges inside X
L14         add a core c of weight D, and an edge cf of weight w(f) for each f ∈ F
L15         record the cluster U with its children, leaves, frontier F and density ρ(U) in G
L16 return the clusters
```

Line L1 skips a repeated constraint, which the first copy has made a cluster. After lines L1 and L2, every edge of $S$ joins a core to a point. Line L5 adds the frontier of each core of $Z$, which keeps the set closed and never lowers its density, since a point $f$ with $k \ge 1$ cores costs $w(f)$ and brings $k \cdot w(f)$. Lines L7 to L9 make the target minimal: they drop one core at a time, and the points that no other core touches, and look again. They drop cores and not points, because a set without a frontier point of one of its cores is not closed. Line L11 also absorbs clusters that the new set swallows whole, so that no cluster lies inside another one. Line L15 records the density in $G$, not in $S$: the simplified graph has lost the extra constraints inside each cluster.

## Example

Take the triangular prism: points 0 to 5, the triangles 012 and 345, and the bars 03, 14 and 25. It has $9 = 2 \cdot 6 - 3$ constraints and it is a Laman graph, so it is rigid. Every point has three constraints.

| step | target found | cores in it | density in $S$ | new cluster | frontier |
|---|---|---|---|---|---|
| L1, L2 | each bar | none | $1 - 4 = -3$ | 9 clusters of two points | both ends |
| 1 | $\{e_{01}, e_{02}, e_{12}, 0, 1, 2\}$ | 3 | $3 \cdot 2 - 9 = -3$ | $\{0, 1, 2\}$ | $\{0, 1, 2\}$ |
| 2 | $\{e_{34}, e_{35}, e_{45}, 3, 4, 5\}$ | 3 | $-3$ | $\{3, 4, 5\}$ | $\{3, 4, 5\}$ |
| 3 | all of $S$ | 5 | $6 \cdot 2 - 15 = -3$ | $\{0, \ldots, 5\}$ | none |

The densities in $S$ use the count of the proofs page: a closed set with $k$ cores has density $\sum_p 2(d(p) - 1) - 3k$, where $d(p)$ is the number of its cores at the point $p$. In step 1 the first candidate pair is $e_{01}, e_{02}$, which share the point 0, and the largest closure that holds them is the triangle. No smaller target exists: without $e_{12}$, the set $\{e_{01}, e_{02}, 0, 1, 2\}$ has density $2 - 6 = -4$. The triangle keeps all three points, because each of them has a bar to the other triangle. In step 3 the simplified graph has the cores $T_1$ and $T_2$ of the triangles and the cores of the three bars, and every point lies in two cores. A proper closed part, such as $T_1$ with the bar 03, has density $2 - 6 = -4$. So the last cluster has five children: two triangles and three bars. This is the step that the triangle merges of [Fudos and Hoffmann](/fudos-hoffmann-reduction/) cannot make, since no three of the clusters pairwise share a point. The solver must place the two triangles against each other with all three bars at once.

The frontier matters in the graph with triangles 012 and 345 and the bars 03, 04 and 15. When $\{0, 1, 2\}$ becomes a cluster, the point 0 stays on its frontier, since it has the bars 03 and 04. So the triangle 034 is still visible, and after $\{3, 4, 5\}$ the algorithm finds the cluster $\{0, 3, 4, 5\}$, made of the bars 03 and 04 and the triangle 345. A planner that contracts $\{0, 1, 2\}$ to one node no longer sees that 03 and 04 meet at one point (see the pitfalls of the [DR-plan](/dr-plan/) page).

## Correctness

The [proof](proofs/correctness.md) shows the following for the algorithm above.

- **The plan.** Each cluster is the union of its children and leaves, each child is a proper subset made earlier, each cluster is a child at most once, every constraint lies in a root, and the roots cover $V$. The main loop stops after at most $m - 1$ steps. This holds for any positive weights.
- **Finding and shrinking.** A frontier vertex shared by two live clusters is never deleted, so shared entities stay visible. The search of lines L4 and L5 finds a target whenever there is one, and lines L7 to L9 return a target with no proper closed subset that is a target. This also holds for any positive weights.
- **Rigidity in the plane.** For points and distances in the plane, every cluster is generically rigid, and when the algorithm stops, the roots with two or more points are exactly the rigid components of $G$. The proof uses Laman's theorem and the fact that the rigidity rank of a graph is the sum of $2|R| - 3$ over its rigid components.

The rigidity claims need the plane and the weights 2, 1 and 3. In space, with $w(v) = 3$, $w(e) = 1$ and $D = 6$, the [double banana](/double-banana-graph/) has $\rho = 18 - 24 = -6$ with no smaller dense part, so the algorithm makes it a cluster, but it is not rigid.

What is measured: the tests on this page check by brute force over all vertex subsets that every cluster is rigid by the Laman count, that the plan has the structure above, and that the roots are the rigid components, on random graphs with at most 7 points, together with the prism, $K_4$, two triangles that share a point and the graph with the shared point 0. A further run on 400 random graphs with 2 to 7 points found no failure.

## Complexity

Let $s$ be the size of $S$. The number of core-point edges never grows: a new core gets at most one edge for each point of $X$, and each such point had an edge to a core of $X$, which is deleted. So $S$ has at most $n + m$ nodes and $2m$ edges, and $s = O(n + m)$. One MAX-CLOSURE is a maximum flow in a network with $O(n + m)$ nodes and arcs, and the flow is at most $w(V) + D \cdot m$; with augmenting paths of [Edmonds and Karp](/edmonds-karp/) and the weights 2, 1 and 3, each path carries at least one unit, so one flow costs $O((n + m)^2)$. There are $O(m^2)$ candidate pairs, since two cores share a point in at most $\sum_p d(p)^2 \le (2m)^2$ ways. Lines L7 to L9 make at most $m$ rounds, each of at most $m$ searches. The main loop runs at most $m - 1$ times. That gives $O(m^5)$ flows and $O(m^5 (n + m)^2)$ time, a crude bound for this simple version, in which each flow starts from zero. The flow test of [degrees of freedom analysis](/degrees-of-freedom-analysis/), which adds the constraints one at a time and keeps the flow, is faster. In the best case no two constraints share an entity: there are no candidate pairs and the work is $\Theta(n + m)$, with an index from points to clusters for line L11. The Python code scans all clusters in line L11 and needs $O(m^2)$ for this case. Space is $\Theta(n + m)$ for $S$, the network and the plan.

As a measured point, the Python code takes about 2 seconds on a random graph with 20 points and 69 constraints.

## Properties

- **Deterministic and exact.** All weights are integers and the flows are integer flows, so the densities are exact. The order of the candidate pairs fixes which plan comes out.
- **Bottom-up and not unique.** A graph can have many DR-plans. The plan depends on which target is found first, and the largest cluster size, the cost of the plan, can depend on that order.
- **Shared entities.** A point in two live clusters is on the frontier of both, and it stays in $S$ until a cluster swallows both of them.
- **Counts only.** The algorithm sees the graph and the weights, not the geometry. Dependent or special constraints, such as three collinear points, are not seen.

## Variants and improvements

- **MFA.** Hoffmann, Lomonosov and Sitharam also gave a modified Frontier algorithm, which changes how a cluster is found so that the plan stays closer to an optimal one more often (Part II).
- **Incremental flows.** The flow test of degrees of freedom analysis adds the constraints one at a time and detects a dense set when the extra $D$ units of the new constraint cannot be pushed. It reuses the flow and is faster than a fresh flow for each pair.
- **Canonical DR-plans.** For systems that are not over-constrained, Baker, Sitharam, Wang and Willoughby give canonical DR-plans and a polynomial algorithm that finds an optimal one, while optimal DR-planning is NP-hard in general.
- **The pebble game.** For points and distances in the plane, the [pebble game](/pebble-game-rigidity/) finds the rigid components in $O(nm)$ time. It gives the roots of the plan but not the plan below them.
- **Witness checks.** A cluster that is dense by the count can still be flexible in space, or at special positions. A rank test at a random [witness configuration](/witness-configuration-method/) can confirm each cluster.

## When to use it

Use it when a constraint system must be solved in small pieces and the pieces can share entities, as in large 2D sketches and in assemblies of parts. It handles any weights, so it plans for points, lines, circles and rigid bodies with constraints of any number of equations. In the plane with points and distances its clusters are rigid. In space, or with special geometry, the counts can lie, and each cluster needs a check. If only the rigid components are needed, the pebble game is faster. If the whole system can be built by merging three clusters at a time, the triangle merges of Fudos and Hoffmann are simpler.

## Pitfalls

- **Contracting a cluster to one node.** It hides shared entities, and the planner then misses clusters such as the triangle 034 of the example. Keep the frontier vertices.
- **Shrinking by points.** If the minimal step drops a frontier point of a core, the set is no longer closed and the core stands for points that are not there. The new frontier can then hold a core. Drop cores, and with them the points that no other core touches.
- **The density in the simplified graph.** In $S$ every cluster counts as exactly $-D$. For $K_4$ with points and distances the last target has density $-3$ in $S$, but $\rho(V) = 6 - 8 = -2$ in $G$: one constraint is redundant. Compute the density of a cluster in $G$.
- **A single point is dense.** With $w(v) = 2$ and $D = 3$, one point has $\rho = -2 \ge -3$. Ask for at least two cores, or two entities, in every target.
- **Dense is not rigid in space.** The double banana passes the count in space and is flexible. In the plane the counts are exact only for generic points and distances; other constraints, such as angles, break Laman's theorem.

## Implementations

## History

Earlier planners of the 1990s, such as the triangle merges of Fudos and Hoffmann and the splits of Owen, found rigid parts by patterns in the graph. In 1997 Hoffmann, Lomonosov and Sitharam showed how to find dense subgraphs of any weighted constraint graph with network flows, and how to shrink a dense subgraph to a minimal one. In 2001 they defined DR-plans and measures to compare planners (Part I), and gave the Frontier algorithm and its modified form (Part II), with the simplification to frontier vertices and a core. Later work by Sitharam and others studied optimal and canonical DR-plans; Baker, Sitharam, Wang and Willoughby (2015) showed that optimal DR-planning is NP-hard for over-constrained 2D systems and gave a polynomial algorithm for a broad class of other systems.

## References
