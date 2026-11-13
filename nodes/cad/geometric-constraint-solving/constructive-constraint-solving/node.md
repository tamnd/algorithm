---
tag: X1CRDR
kind: technique
slug: constructive-constraint-solving
name: Graph-constructive constraint solving
aliases:
- constructive geometric constraint solving
area: cad/geometric-constraint-solving
level: core
summary: Analyses the constraint graph to find an order of ruler and compass steps that place the elements, then carries out the steps to compute one or all solutions.
prereqs: [geometric-constraint-graph, well-constrained-system, ruler-and-compass-constructibility]
see_also: [fudos-hoffmann-reduction, owen-triconnected-decomposition, dr-plan, root-identification-problem, local-propagation-solving, henneberg-construction, degrees-of-freedom-analysis, circle-circle-intersection]
sources:
  - paper: doi:10.1145/248210.248223
    title: Ioannis Fudos and Christoph M. Hoffmann, A graph-constructive approach to solving systems of geometric constraints, ACM Transactions on Graphics 16(2), 179 to 216, 1997
    locator: the two phases of analysis and construction, the cluster rules for points and lines, and Section 2.2 on multiple solutions and root identification
  - paper: "William Bouma, Ioannis Fudos, Christoph M. Hoffmann, Jiazhen Cai and Robert Paige, Geometric constraint solver, Computer-Aided Design 27(6), 1995"
    locator: the design of the constructive solver, its constraint graph and the selection of the intended solution (general locator)
  - paper: doi:10.1145/112515.112573
    title: John C. Owen, Algebraic solution for geometry from dimensional constraints, ACM Symposium on Solid Modeling Foundations and CAD/CAM Applications (SMA '91), 397 to 407, 1991
    locator: the top-down analysis at separation pairs and the solution by quadratic equations (general locator)
  - paper: doi:10.1145/566282.566300
    title: Robert Joan-Arinyo, Antoni Soto-Riera, Sebastià Vila-Marta and Josep Vilaplana-Pastó, Revisiting decomposition analysis of geometric constraint graphs, ACM Symposium on Solid Modeling and Applications (SM '02), 105 to 115, 2002
    locator: the proof that the top-down method of Owen and the bottom-up method of Fudos and Hoffmann solve the same class of systems (general locator)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on decomposition and constructive solving (general locator)
---

Graph-constructive constraint solving splits the solution of a geometric constraint system into two phases. The analysis phase looks only at the [constraint graph](/geometric-constraint-graph/) and finds a plan: an order in which small rigid groups of entities are put together, each by one step that a geometer could do with ruler and compass. The construction phase then runs the plan on the actual values. Each step is a closed-form computation, such as a [circle-circle intersection](/circle-circle-intersection/), with two solutions, and the solver chooses one by a sign kept from the user's draft, or follows both to list all solutions. The plan depends only on the graph, so the solver can reuse it when the user changes a dimension. The method works exactly for the systems that its rules decompose, which are [ruler-and-compass constructible](/ruler-and-compass-constructibility/); this is a strict subclass of the [well-constrained](/well-constrained-system/) systems.

## In plain words

Before you compute anything, you look at which parts of the drawing are tied to which. You find a small piece that is fixed by itself, a triangle with three known sides for example. Then you find another piece that this one fixes, and so on, until you have a recipe: first build this triangle, then put that point where two circles cross, then glue these two pieces at their common points.

Only then do you put in the numbers and follow the recipe. Each step has two answers, left or right, and you choose the one that looks like the drawing. If you change a length, the recipe stays the same, and only the numbers change. If the drawing has a part that no recipe of this kind can build, the method reports that part and another solver must take it.

## When it applies

- The system is in the plane, with points and lines, and with constraints of distance, angle, incidence and the like. The rules have been extended to circles, tangency and some 3D cases, but the classic methods are planar.
- The system is well-constrained, or it is made well-constrained by the user or by an automatic completion.
- The constraint graph decomposes by the rules: for distances between points, it is triangle-decomposable, so it can be built from edges by repeated merges of three rigid clusters that pairwise share one point. On six points, 3285 of the 3355 labeled Laman graphs are decomposable in this way; the other 70 are the 10 labelings of $K_{3,3}$ and the 60 of the triangular prism.

## The template

```pseudo id=main
CONSTRUCTIVE-SOLVE(G, values, draft)
L1  S ← ⟨SEED(G)⟩                            ▷ the first rigid clusters, for example the edges
L2  plan ← empty list
L3  while ⟨RULE⟩ applies to some clusters R ⊆ S do
L4      N ← the union of the clusters in R
L5      append (rule, R, N) to plan; S ← (S − R) ∪ {N}
L6  if S has more than one cluster then return ⟨FALLBACK(S)⟩   ▷ under-constrained or beyond the rules
L7  for each step (rule, R, N) in plan do
L8      compute the candidate placements of N from those of R by ⟨CONSTRUCT(rule, values)⟩
L9      keep the candidate given by ⟨SELECT(draft)⟩, or keep all of them
L10 return the placement of the last cluster
```

The holes are these.

- **SEED.** The rigid pieces to start from: each constraint between two points is a rigid cluster of two points; for lines, a pair of lines with an angle is a rigid set of directions.
- **RULE.** A pattern of clusters whose union is rigid and can be placed in closed form. The [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/) uses one main rule: three clusters that pairwise share one entity, at three different entities, merge into one. [Owen's decomposition](/owen-triconnected-decomposition/) finds the same steps from the top, by splits at separation pairs.
- **CONSTRUCT.** The closed form for a rule. For three clusters sharing the points $p, q, r$, the distances $\lvert pq \rvert$, $\lvert pr \rvert$ and $\lvert qr \rvert$ are known inside the clusters, so the triangle $pqr$ is placed by a circle-circle intersection, and each cluster is moved onto it by a proper rigid motion.
- **SELECT.** The branch. Each circle-circle intersection has two solutions, and the solver keeps the one where the sign of the [orientation test](/orientation-test/) of $p, q, r$ equals the sign in the draft. This is one answer to the [root identification problem](/root-identification-problem/).
- **FALLBACK.** What to do when the rules stop: report the clusters to the user, add constraints to make the system well-constrained, or hand the remaining system, with each cluster as one rigid body, to a numerical or algebraic solver, as a [DR-plan](/dr-plan/) does.

**Walk-through.** Lines L1 to L6 are the analysis. They use only the graph and run in polynomial time, $O(n^2)$ for $n$ entities in the Fudos-Hoffmann form. Lines L7 to L10 are the construction. Each step solves one quadratic equation and moves the clusters, so the construction costs $O(n^2)$ in the worst case and $O(n)$ steps. Since the plan does not depend on the values, a change of a dimension runs only lines L7 to L10 again.

**The sign and its degenerate cases.** The test in SELECT is the sign of a $2 \times 2$ determinant of draft coordinates. Computed in floating point, a value near zero can have the wrong sign through [catastrophic cancellation](/catastrophic-cancellation/), so compute it exactly on the integer or rational draft, or with a filtered predicate such as [Shewchuk's](/shewchuk-expansion-sum/), as in [exact geometric computation](/exact-geometric-computation/). When the draft has $p, q, r$ collinear, the sign is 0 and the draft does not choose; a fixed rule such as [simulation of simplicity](/simulation-of-simplicity/) or a fixed default side does. When the values make the triangle $pqr$ flat ($\lvert pq \rvert + \lvert qr \rvert = \lvert pr \rvert$), the two solutions coincide and the solution is not regular; when they violate the triangle inequality, the step has no real solution and the solver reports which step failed.

**Example.** Take seven points with the constraints $01, 02, 12, 15, 25, 03, 04, 34, 36, 46, 56$, two diamonds $\{0, 1, 2, 5\}$ and $\{0, 3, 4, 6\}$ (each two triangles with a common edge) that meet at point 0, and the bar $56$. The draft is $(0, 0)$, $(3, 2)$, $(4, -1)$, $(7, 1)$, $(-2, 4)$, $(1, 5)$, $(4, 7)$ for the points 0 to 6, and the distances are measured on it. [Local propagation](/local-propagation-solving/) cannot solve this system from any pair of points. The analysis with the Fudos-Hoffmann rule finds this plan of $n - 2 = 5$ merges.

| step | clusters merged | shared points | new cluster |
|---|---|---|---|
| 1 | $\{4, 6\}$, $\{3, 6\}$, $\{3, 4\}$ | 6, 4, 3 | $\{3, 4, 6\}$ |
| 2 | $\{3, 4, 6\}$, $\{0, 4\}$, $\{0, 3\}$ | 4, 3, 0 | $\{0, 3, 4, 6\}$ |
| 3 | $\{2, 5\}$, $\{1, 5\}$, $\{1, 2\}$ | 5, 2, 1 | $\{1, 2, 5\}$ |
| 4 | $\{1, 2, 5\}$, $\{0, 2\}$, $\{0, 1\}$ | 2, 1, 0 | $\{0, 1, 2, 5\}$ |
| 5 | $\{0, 1, 2, 5\}$, $\{5, 6\}$, $\{0, 3, 4, 6\}$ | 5, 0, 6 | all seven |

The last step is the one that propagation cannot do. It needs $\lvert 05 \rvert$ and $\lvert 06 \rvert$, which are not constraints but follow from the diamonds: with the draft folds, $\lvert 05 \rvert^2 = 26$ and $\lvert 06 \rvert^2 = 65$, and with $\lvert 56 \rvert^2 = 13$ the step places the triangle $0, 5, 6$. With the draft signs, the construction returns the draft up to a proper motion. The 5 steps have $2^5 = 32$ sign vectors. The other fold of the first diamond gives $\lvert 05 \rvert^2 = 39.2$, and the other fold of the second gives $\lvert 06 \rvert^2 = 5$; with both other folds, $\sqrt 5 + \sqrt{13} \approx 5.84 < \sqrt{39.2} \approx 6.26$, so the last step has no real solution. That removes 8 sign vectors, and the system has 24 real solutions up to proper motion.

## Classic examples

- **[Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/).** The bottom-up form: start from the edges and merge three clusters that pairwise share a point, until one cluster is left. It runs in $O(n^2)$ time.
- **[Owen's decomposition](/owen-triconnected-decomposition/).** The top-down form: split the graph at a separation pair, add a virtual edge to the side that is not rigid, and recurse down to triangles. Joan-Arinyo, Soto-Riera, Vila-Marta and Vilaplana-Pastó showed that it solves the same class of systems as the bottom-up form.
- **[DR-plans](/dr-plan/).** The general form: the clusters are any minimal dense subsystems, found by flows, and a step that is not ruler-and-compass is solved by a general solver.
- **[Henneberg](/henneberg-construction/) and propagation orders.** Placing one point at a time from two placed points is the simplest rule, the one of [local propagation](/local-propagation-solving/). Merging clusters instead of points is what makes the method work on cycles.
- **Kramer's action plans.** [Degrees of freedom analysis](/degrees-of-freedom-analysis/) builds a plan of closed-form actions on rigid bodies, the 3D relative of the same idea.

## Variations

- **Bottom-up and top-down.** Merging from the edges and splitting from the whole graph find the same decompositions on the same class of graphs; they differ in cost and in how easily they report a failure.
- **Points and lines.** With lines and angles, a set of lines with angle constraints between them fixes only their directions, so the methods keep two kinds of clusters, rigid clusters and sets of fixed directions, with rules for each.
- **Under-constrained systems.** The analysis stops with several clusters. A completion step adds distance constraints between the clusters, chosen to keep the system triangle-decomposable, and then the plan runs.
- **Exact or numerical construction.** The steps can run in floating point, as most CAD systems do, or with exact nested square roots, since each step adds at most one square root.

## Pitfalls

- **Triangle-decomposable is not the same as well-constrained.** The triangular prism and $K_{3,3}$ are Laman graphs, so they are well-constrained for generic lengths, but no three of their clusters pairwise share a point, and the analysis stops at line L6. On the prism it stops with two triangles and three bars. Report the clusters and use a fallback; do not report the system as under-constrained.
- **The plan does not promise a real solution.** In the example above, 8 of the 32 sign vectors fail at the last step. A plan is a statement about the graph, and the values can still violate a triangle inequality in some or all branches.
- **The branch from the draft can fail far from the draft.** When the user changes a dimension a lot, the triangle of a step can flip through a flat position, and the draft sign then selects a shape that looks very different. The heuristics for this are not proved; see the [root identification problem](/root-identification-problem/).
- **Over-constrained input.** A merge of clusters that share two or more points means a redundant or conflicting constraint. The analysis must stop and report it instead of merging, as the Fudos-Hoffmann reduction does.
- **The sign from floating point.** A draft with three nearly collinear points gives an orientation near zero, and a floating-point sign can be wrong; compute it exactly.

## Exercises

1. Show that a triangle-decomposable system with $n$ points and generic lengths has at most $2^{n-2}$ real solutions up to proper motion, and that the bound is reached by a strip of triangles.
2. Show that each merge of three clusters reduces the number of clusters by 2, and that a Laman graph that reduces to one cluster needs exactly $n - 2$ merges.
3. In the example above, find the values of $\lvert 05 \rvert^2$ for the two folds of the diamond $\{0, 1, 2, 5\}$ from the draft coordinates, and check the count of 24 real solutions.
4. Show that the prism has no three clusters that pairwise share one point, at any stage of the reduction.

## References
