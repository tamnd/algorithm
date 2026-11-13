---
tag: RDTV4C
kind: definition
slug: geometric-constraint-graph
name: Geometric constraint graph
aliases:
- constraint graph of a sketch
area: cad/geometric-constraint-solving
level: core
summary: A graph with a vertex per geometric entity and an edge per constraint, weighted by degrees of freedom; graph-based solvers decompose it to plan the solution.
prereqs: [geometric-constraint, graph]
see_also: [degrees-of-freedom-analysis, laman-theorem, maxwell-counting-rule, dr-plan, fudos-hoffmann-reduction, owen-triconnected-decomposition, dulmage-mendelsohn-decomposition, constraint-graph]
sources:
  - paper: doi:10.1145/248210.248223
    title: Ioannis Fudos and Christoph M. Hoffmann, A graph-constructive approach to solving systems of geometric constraints, ACM Transactions on Graphics 16(2), 179 to 216, 1997
    locator: the constraint graph with a vertex per geometric element and an edge per constraint, and its analysis for solvability (general locator)
  - paper: doi:10.1006/jsco.2000.0402
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Decomposition plans for geometric constraint systems, Part I, Performance measures for CAD, Journal of Symbolic Computation 31(4), 367 to 408, 2001
    locator: the weighted constraint graph, its density, and the dense, well-constrained and over-constrained subgraphs (general locator)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on the combinatorics of constraint systems and on decomposition (general locator)
  - paper: "Christophe Jermann, Gilles Trombettoni, Bertrand Neveu and Pascal Mathis, Decomposition of geometric constraint systems, a survey, International Journal of Computational Geometry and Applications 16(5-6), 379 to 414, 2006"
    locator: the graph and hypergraph models of a constraint system and the structural rigidity counts on them (general locator)
---

The geometric constraint graph of a sketch has a vertex for each geometric entity and an edge for each constraint between two entities. Each vertex carries the degrees of freedom of its entity, 2 for a point or a line in the plane, and each edge carries the number of degrees of freedom that its constraint removes. Graph-based solvers never look at the coordinates first. They find, on this graph, small parts that are rigid by themselves, solve those, and join the results. The counts on the graph also predict whether the sketch is well-constrained, under-constrained or over-constrained, for generic values.

## Definition

Let a [geometric constraint](/geometric-constraint/) system in $\mathbb{R}^d$ have entities $V$ and constraints $E$, and let $D = d(d + 1)/2$ be the dimension of the group of rigid motions (3 in the plane, 6 in space).

**Constraint graph.** If every constraint involves two entities, the constraint graph is the weighted multigraph $G = (V, E, w)$, where an edge $e = uv$ joins the two entities of a constraint, $w(v)$ is the number of DOF of entity $v$, and $w(e)$ is the weight of constraint $e$, the number of independent equations it adds. Two constraints between the same pair, such as an incidence and a distance between a point and a line, give two parallel edges, or one edge whose weight is their sum. A constraint on one entity, such as a fixed radius, lowers the weight of its vertex.

**Hypergraph and bipartite form.** A constraint on three or more entities, such as "$m$ is the midpoint of $p$ and $q$" (2 equations on 3 points), is a hyperedge. The general model is the bipartite graph with entity vertices on one side, constraint vertices on the other, and an edge when a constraint involves an entity. With one vertex per scalar unknown and per scalar equation instead, this is the graph on which the [Dulmage-Mendelsohn decomposition](/dulmage-mendelsohn-decomposition/) works.

**Density.** For a set $S \subseteq V$, let $E(S)$ be the constraints with all their entities in $S$. The density of $S$ is
$$ \rho(S) = \sum_{e \in E(S)} w(e) - \sum_{v \in S} w(v). $$
The number $-\rho(S)$ is the count of DOF left to the entities of $S$ by their own constraints. A rigid part keeps exactly the $D$ DOF of a rigid motion. So, by the counts alone (for generic values, see below), the system is

- *structurally well-constrained* if $\rho(V) = -D$ and $\rho(S) \le -D$ for every $S$ that is large enough to have the full group of motions,
- *structurally over-constrained* if some such $S$ has $\rho(S) > -D$ (a *dense* set),
- *structurally under-constrained* if $\rho(V) < -D$ and no set is dense.

"Large enough" excludes the sets with a smaller group of motions, such as one point, whose orbit has dimension 2 in the plane. For points with distance constraints in the plane, $w(v) = 2$ and $w(e) = 1$, so $\rho(S) \le -3$ on every $k \ge 2$ points says that $k$ points span at most $2k - 3$ edges. This is the condition of [Laman's theorem](/laman-theorem/) and of the [Maxwell counting rule](/maxwell-counting-rule/).

**What the counts mean.** The counts depend only on the graph. They are necessary for a regular solution, and for points and distances in the plane they are also sufficient for generic values (Laman). For other entities, and in space, the counts can pass while the system is not well-constrained, and the actual values can make any system degenerate. The page on [well-constrained systems](/well-constrained-system/) gives the exact definitions and the examples where the two notions differ.

## Examples and non-examples

**A sketch with a line.** Take points $A$, $B$, $C$ and a line $L$ in the plane, with six constraints: $A$ on $L$, $B$ on $L$, $\lvert AB \rvert = 4$, $\lvert AC \rvert = 3$, $\lvert BC \rvert = 3$, and the distance from $C$ to $L$ is 2. All vertex weights are 2 and all edge weights are 1.

| set $S$ | edges in $S$ | $\rho(S)$ |
|---|---|---|
| $\{A, B, C\}$ | $AB$, $AC$, $BC$ | $3 - 6 = -3$ |
| $\{A, B, L\}$ | $AL$, $BL$, $AB$ | $3 - 6 = -3$ |
| $\{C, L\}$ | $CL$ | $1 - 4 = -3$ |
| $\{A, B, C, L\}$ | all six | $6 - 8 = -2$ |

The whole set is dense, so the system is over-constrained. The geometry agrees: $A$ and $B$ lie on $L$ at distance 4, so $C$ lies on the perpendicular bisector at height $\sqrt{9 - 4} = \sqrt{5}$ from $L$, and the value 2 contradicts this. Without the last constraint, $\rho(V) = -3$ and the system is well-constrained, with two solutions, $C$ above or below $L$.

**Points and distances.** For a sketch with points only, the constraint graph is the graph of the [bar-and-joint framework](/bar-and-joint-framework/), and the triangle-based solvers ([Fudos-Hoffmann](/fudos-hoffmann-reduction/), [Owen](/owen-triconnected-decomposition/)) work on it directly.

**A ternary constraint.** "$p$ and $q$ are symmetric about the line $l$" is 2 equations on three entities. Replacing it by an edge $pq$ of weight 2 hides the role of $l$; the hyperedge or the bipartite form keeps it.

**Not a constraint graph: the drawing.** The graph of the drawn segments of a sketch, with an edge for each segment between two end points, is not the constraint graph. A segment without a length has no distance constraint, and two points can have a distance constraint without a segment between them.

**Not a constraint graph: the feature history.** In [feature-based modeling](/feature-based-modeling/), the graph of which feature depends on which earlier feature is a dependency graph between whole features. Each sketch inside a feature has its own constraint graph.

## Related definitions

- [Geometric constraint](/geometric-constraint/) and [geometric constraint problem](/geometric-constraint-problem/): the objects that the graph models.
- [Degrees of freedom analysis](/degrees-of-freedom-analysis/): the counts on the graph, and how to find dense sets with flows.
- [DR-plan](/dr-plan/): a hierarchy of rigid subgraphs of the constraint graph that tells a solver in which order to solve.
- [Well-constrained system](/well-constrained-system/): the exact notion, and the structural notion that the counts test.
- The [constraint graph](/constraint-graph/) of a finite constraint satisfaction problem is the same idea, with variables over finite domains and no rigid motions.

## References
