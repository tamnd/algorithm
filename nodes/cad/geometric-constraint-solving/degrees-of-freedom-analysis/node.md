---
tag: HPGM76
kind: technique
slug: degrees-of-freedom-analysis
name: Degrees of freedom analysis
aliases:
- DOF analysis
- Kramer degree of freedom analysis
area: cad/geometric-constraint-solving
level: core
summary: Kramer's method that counts the freedoms of bodies and those that each constraint removes, and solves the system by a plan of steps that each fix some freedoms.
prereqs: [geometric-constraint-graph, well-constrained-system]
see_also: [maxwell-counting-rule, pebble-game-rigidity, grubler-formula, dr-plan, assembly-constraint-solving, max-flow-min-cut-theorem, hall-theorem, kinematic-pair]
sources:
  - book: isbn:9780262111645
    title: Glenn A. Kramer, Solving Geometric Constraint Systems, A Case Study in Kinematics, MIT Press, 1992
    locator: degrees of freedom analysis, with the translational and rotational freedoms of each body, the actions that satisfy a constraint and remove freedoms, and the plan fragments that compute each action in closed form (general locator)
  - paper: doi:10.1007/BFb0017460
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Finding solvable subsets of constraint graphs, Principles and Practice of Constraint Programming (CP97), LNCS 1330, 1997
    locator: the network flow test for dense subgraphs of a weighted constraint graph (general locator)
  - paper: doi:10.1006/jsco.2000.0402
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Decomposition plans for geometric constraint systems, Part I, Performance measures for CAD, Journal of Symbolic Computation 31(4), 367 to 408, 2001
    locator: the density of a subgraph, the structural notions of well-constrained and over-constrained, and their limits (general locator)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on the combinatorics of rigidity and on decomposition (general locator)
---

Degrees of freedom analysis decides how a constraint system can be solved by counting freedoms, before it computes any coordinate. Each entity has some degrees of freedom (DOF), each constraint removes some, and a rigid part keeps exactly the DOF of a rigid motion. The counts on the [constraint graph](/geometric-constraint-graph/) find the parts that are rigid by themselves, the parts that are over-constrained and the parts that are still free, and a solver then handles each part in turn. Kramer (1992) made this a solver for assemblies and mechanisms: each body keeps a record of its translational and rotational freedoms, and each constraint is satisfied by an action, a translation or a rotation computed in closed form, that removes some of them. Hoffmann, Lomonosov and Sitharam found the over-constrained and rigid subsystems of any weighted graph with network flows. The counts are fast and exact as counts, but they see only the graph: a system with dependent constraints can pass every count and still be wrong.

## In plain words

A part lying free on a table can slide in two directions and turn, so it has three freedoms. A rule such as "this corner touches that edge" takes away one freedom. If you add up the freedoms of all the parts and take away what the rules remove, you can tell, before you compute anything, whether the drawing can still move, is just fixed, or has too many rules.

The count must hold for every group of parts, not only for the whole drawing. One small group can have too many rules while another group is still loose, and the total looks right. The method checks the groups one at a time with a flow of "rule weight" into the parts. And the count can be fooled: two rules that say the same thing in different words remove fewer freedoms than they seem to.

## When it applies

- Each entity has a known number of DOF $w(v)$, and each constraint a known weight $w(e)$, the number of independent equations it adds. The tables are on the page on [geometric constraints](/geometric-constraint/).
- A rigid part keeps $K$ DOF: $K = 3$ in the plane, $K = 6$ in space, or less when the part is fixed to the ground.
- The question is structural: which subsets are well-constrained, over-constrained or free for generic values. For points and distances in the plane the answer is exact by [Laman's theorem](/laman-theorem/); otherwise it is a necessary condition, as the page on [well-constrained systems](/well-constrained-system/) explains.
- For Kramer's action form, the system is made of rigid bodies with markers (a point and two axes on each body), joined by constraints between markers, as in [kinematic pairs](/kinematic-pair/).

## The template

The density of a set $S$ of entities is $\rho(S) = w(E(S)) - w(S)$, where $E(S)$ is the set of constraints with all their entities in $S$. A set is *dense* when $\rho(S) > -K$. The template finds a dense set by flows, adding the constraints one at a time.

```pseudo id=main
DOF-ANALYSIS(V, E, w, K)
L1  N ← network with a node per entity v (arc v → t, capacity w(v)) and a node per constraint
L2  for each constraint e, in ⟨ORDER⟩ do
L3      add arcs s → e (capacity w(e) + K) and e → each entity of e (capacity ∞)
L4      push flow from s through e until the flow from s to e is w(e) + K, or no path is left
L5      if the flow from s to e is less than w(e) + K then
L6          S ← the entities reachable from e in the residual network
L7          ⟨ON-DENSE(S)⟩                        ▷ S is dense and holds e
L8      lower the capacity of s → e to w(e), and return the extra flow of K
L9  return the flow, and the dense sets found
```

The holes are these.

- **ORDER.** Any order finds a dense set when one exists, since a dense set becomes dense when its last constraint is added. The order changes which dense set is found first.
- **K.** The slack for rigid motions: 3 in the plane. Use $K + 1$ to find sets with $\rho(S) \ge -K$, the well-constrained ones, which are the rigid clusters.
- **ON-DENSE(S).** Report $S$ as over-constrained and drop $e$; or, in a decomposition, treat $S$ as one rigid cluster, contract it, and go on. The second choice is the step of a [DR-plan](/dr-plan/).

**Why the flow finds dense sets.** The flow sends the weight of each constraint to its entities, and an entity can absorb at most its DOF. By the max-flow min-cut theorem, all weight on a set $F$ of constraints can be absorbed if and only if $w(F') \le w(N(F'))$ for every $F' \subseteq F$, where $N(F')$ is the set of entities of $F'$; this is [Hall's condition](/hall-theorem/) with weights. With the extra $K$ on the new constraint $e$, the flow fails exactly when some set $F$ of constraints with $e \in F$ has $w(F) + K > w(N(F))$, that is, when $S = N(F)$ has $\rho(S) > -K$. The entities reached from $e$ in the residual network after the failure are such a set. Each test pushes $w(e) + K$ units, each by one search of the network, so the whole run costs $O(m (w_{\max} + K)(n + m))$ for $n$ entities and $m$ constraints. For bars in the plane ($w(v) = 2$, $w(e) = 1$, $K = 3$) this is the [pebble game](/pebble-game-rigidity/).

**Example.** Take points $P, Q$ and lines $L, M$ in the plane, all with $w = 2$, and six constraints of weight 1, added in this order: $P$ on $L$, $Q$ on $L$, $\lvert PQ \rvert = 5$, $L$ parallel to $M$, distance from $P$ to $M$ is 2, distance from $Q$ to $M$ is 2.

| constraint added | demand from $s$ | max flow | dense set found |
|---|---|---|---|
| $P$ on $L$ | 4 | 4 | none |
| $Q$ on $L$ | 5 | 5 | none |
| $\lvert PQ \rvert$ | 6 | 6 | none |
| $L \parallel M$ | 7 | 7 | none |
| $d(P, M)$ | 8 | 8 | none |
| $d(Q, M)$ | 9 | 8 | $\{P, Q, L, M\}$, $\rho = 6 - 8 = -2$ |

The last constraint makes the whole set dense. The geometry agrees: $P$ and $Q$ lie on $L$, and $L$ is parallel to $M$, so $Q$ has the same distance to $M$ as $P$. The last constraint is redundant when its value is 2 and in conflict for any other value.

## Classic examples

- **Kramer's solver.** Kramer's solver handles linkages and assemblies by DOF analysis. Each body starts with 3 translational and 3 rotational DOF. For each pair of constraint type and current DOF state, a *plan fragment* gives an action, such as "translate the body so that the two markers meet" or "rotate it about this axis so that the two axes are parallel", and the new DOF state. The solver picks constraints that some action can satisfy, applies the action, and records the step in a plan. Each action is a closed-form computation, so the plan runs again fast when the dimensions change.
- **The Maxwell and Grübler counts.** The [Maxwell counting rule](/maxwell-counting-rule/) for frameworks and the [Grübler formula](/grubler-formula/) for mechanisms, $M = 3(n - 1) - 2j_1 - j_2$ in the plane with $n$ links, $j_1$ joints of one freedom and $j_2$ joints of two, are the count on the whole system. A slider-crank (ground, crank, coupler and slider, with 3 revolute joints and 1 prismatic joint) has $M = 3 \cdot 3 - 2 \cdot 4 = 1$.
- **Dense sets by flows.** The flow template above, in the form of Hoffmann, Lomonosov and Sitharam, finds the rigid and the over-constrained subsystems of a general weighted graph. It is the first step of the [DR-plan](/dr-plan/).
- **The pebble game.** For bars and joints in the plane the same test becomes the [pebble game](/pebble-game-rigidity/), which also gives the rigid components.
- **Assemblies.** In [assembly constraint solving](/assembly-constraint-solving/), each part has 6 DOF, and the count decides which groups of parts are fixed relative to each other.

## Variations

- **Count only.** Compare $w(V) - w(E)$ with $K$ for the whole system. This is the quick test of a sketcher's status bar ("3 DOF left"). It misses an over-constrained part that a free part elsewhere hides.
- **Flows for every subset.** The template, which checks every subset in polynomial time.
- **Action analysis.** Kramer's form keeps a DOF state per body, not one number, so it knows which freedoms are left: a body that may only turn about one axis has 1 rotational DOF, and a constraint that asks for a translation is then in conflict. This catches some dependencies that pure counts miss.
- **Numerical rank.** The [rank](/rank/) of the Jacobian at the draft is the exact number of independent equations at that point. It sees every dependency, also those of special values, but it needs coordinates and a tolerance, so it is not a structural test.

## Pitfalls

- **Dependent constraints.** A pin in a hole with a shoulder face: a body is coaxial with a fixed axis (weight 4, it fixes the two translations across the axis and the two tilts) and its face lies on a fixed plane perpendicular to the axis (weight 3, it fixes the translation along the axis and the two tilts). The count gives $6 - 4 - 3 = -1$, over-constrained. But the two tilts appear in both constraints, the rank of the equations is 5, and 1 DOF is left: the rotation about the axis. The count is wrong in both directions here: it reports a conflict that does not exist and misses a freedom that does. Kramer's action form, or the rank, gets this right.
- **Special geometry.** A parallelogram linkage with a third bar parallel to two sides has $M = 3 \cdot 4 - 2 \cdot 6 = 0$ by Grübler's formula, yet it moves with 1 DOF, because the third bar is parallel to the other two. The count is right for generic lengths and wrong for these.
- **Checking only the whole system.** The total count can be right while one part is over-constrained and another is free. Add to the example above a point $R$ with the one constraint $\lvert PR \rvert = 1$. The total is $7 - 10 = -3$, the count of a well-constrained system, but $\{P, Q, L, M\}$ is dense and $R$ can still turn about $P$. Test every subset, as the flow does.
- **The wrong slack for small sets.** The orbit of one point in the plane has dimension 2, not 3. Two points with a coincidence constraint (weight 2) have $\rho = 2 - 4 = -2 > -3$, so the template with $K = 3$ reports them as dense, but the pair is fine and keeps 2 DOF. The same happens to a circle with a fixed radius, $\rho = 1 - 3 = -2$. Merge coincident points into one entity and treat a constraint on one entity by lowering its weight, as on the [constraint graph](/geometric-constraint-graph/) page, before the flow runs.

## Exercises

1. Show that, for $w(v) = 2$, $w(e) = 1$ and $K = 3$, the flow template accepts the constraints one by one exactly as long as the edges form a Laman-sparse graph.
2. Show that if the flow of line L4 fails, the set of entities reachable from $e$ in the residual network is dense.
3. Count the DOF of a planar sketch with a circle tangent to two fixed perpendicular lines and with a fixed radius, and check the answer by placing the circle.
4. A body in space is constrained by three point-on-plane mates against three fixed planes that are pairwise perpendicular. Find the count, the rank and the DOF left.

## References
