---
tag: MM9FFR
kind: technique
slug: local-propagation-solving
name: Local propagation solving
aliases:
- propagation of known states
area: cad/geometric-constraint-solving
level: intro
summary: Solves constraints one at a time when one unknown of a constraint is left, as in Sketchpad and ThingLab. It fails on cycles of constraints.
prereqs: [geometric-constraint-problem, constraint-propagation]
see_also: [constructive-constraint-solving, fudos-hoffmann-reduction, henneberg-construction, variational-geometry, topological-sort, dataflow-analysis, attribute-grammar, strongly-connected-components]
sources:
  - paper: doi:10.48456/tr-574
    title: Ivan E. Sutherland, Sketchpad, a man-machine graphical communication system, PhD thesis, MIT, 1963; reprinted as Technical Report UCAM-CL-TR-574, University of Cambridge Computer Laboratory, 2003
    locator: the chapter on constraint satisfaction, with the one-pass method that orders the variables and the relaxation method used when the one-pass method fails (general locator)
  - paper: doi:10.1145/76372.77531
    title: Bjorn N. Freeman-Benson, John Maloney and Alan Borning, An incremental constraint solver, Communications of the ACM 33(1), 54 to 63, 1990
    locator: the DeltaBlue algorithm, with multi-way constraints, one method per output variable, strengths, and the incremental update of the plan; cycles are not handled (general locator)
  - paper: doi:10.1145/248210.248223
    title: Ioannis Fudos and Christoph M. Hoffmann, A graph-constructive approach to solving systems of geometric constraints, ACM Transactions on Graphics 16(2), 179 to 216, 1997
    locator: the survey of earlier solvers, with propagation methods and their failure on constraint cycles (general locator)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on decomposition and the earlier solution methods (general locator)
---

Local propagation solves a system of constraints by looking at one constraint at a time. Some values are known at the start. When a constraint has all its variables known but one, the constraint computes that one, and the new value can make another constraint ready. The method repeats this until every variable is known, or until no constraint is ready. Sutherland's Sketchpad (1963) used an ordering of this kind, Borning's ThingLab and the DeltaBlue solver of Freeman-Benson, Maloney and Borning built on it, and every spreadsheet recalculates its cells in the same way. Each step is a small direct computation, so the method is fast and exact when it works. It fails when the constraints form a cycle, where each constraint has two or more unknowns until the others are solved, and a cycle is common in geometry: two triangles joined by three bars are a cycle that no step can start.

## In plain words

Think of a set of rules such as "C is the sum of A and B" and "D is twice C". If you know A and B, you can find C, and then D. Each rule waits until it has enough known values to compute one new value. You never need to solve two rules at the same time.

In a drawing, a rule may say "this point is 3 from point P and 4 from point Q". When P and Q are already placed, the point is where the two circles cross. Then this point helps to place the next one. The method gets stuck when every rule is waiting for another rule, like two people at a door who each wait for the other to go first.

## When it applies

- The system is given by constraints, each with a known small set of variables, and for some or all of its variables a constraint has a *method*: a direct formula that computes that variable from the others.
- The values to start from are known: fixed parameters, inputs, or, in a sketch, a grounded point and a grounded direction.
- The dependency structure has no cycle. More exactly, it must be possible to give each constraint one output variable so that the directed graph "input of the constraint to its output" has no directed cycle.

In a sketch with points and distances in the plane, the geometric form of the rule is: a point is ready when it has distance constraints to two placed points, and its method is a [circle-circle intersection](/circle-circle-intersection/). Starting from two adjacent placed points, the method succeeds exactly when the constraint graph has a [Henneberg](/henneberg-construction/) order of type I steps that starts from those two points.

## The template

```pseudo id=main
LOCAL-PROPAGATION(X, C, K)                 ▷ X variables, C constraints, K known at the start
L1  Q ← the constraints c with ⟨READY(c, K)⟩
L2  while Q is not empty do
L3      c ← pop(Q); if c is used then continue
L4      u ← the variable that c will compute
L5      value(u) ← ⟨METHOD(c, u)⟩ from the known variables of c
L6      K ← K ∪ {u}; mark c used
L7      for each unused constraint c' on u with ⟨READY(c', K)⟩ do push c' on Q
L8  for each unused constraint c do ⟨CHECK(c)⟩ ▷ redundant or in conflict
L9  if K ≠ X then return STUCK               ▷ a cycle, or too few constraints
L10 return value
```

The holes are these.

- **READY(c, K).** In the algebraic form, all variables of $c$ but one are in $K$. In the geometric form, the constraint is a group: the unknown point $u$ has two distance constraints to points in $K$, or a distance and an incidence to a placed line.
- **METHOD(c, u).** The direct formula: a subtraction for "$a + b = s$", a circle-circle or circle-line intersection for a point. A geometric method usually has two results, and it chooses one by a sign kept from the draft, the [orientation test](/orientation-test/) of the known points and $u$.
- **CHECK(c).** A constraint whose variables all became known through other constraints was not used. It is either redundant, if it holds, or in conflict with the others.

**Walk-through.** Line L1 seeds the queue with the constraints that can fire at once. Lines L3 to L6 fire one constraint and make its output known. Line L7 is the propagation: only the constraints on the new variable can become ready, so the method looks only at them. To make line L7 cost $O(1)$ per constraint, keep with each constraint a counter of its unknown variables and decrement it when one becomes known. Then the whole loop costs $O(\lvert X \rvert + \sum_c \lvert c \rvert)$ plus the cost of the methods, as in [Kahn's topological sort](/topological-sort/). Lines L8 and L9 report what the method could not do.

**Degenerate steps.** A circle-circle step is degenerate when the two known points coincide, which gives a circle of solutions, or when the circles are tangent, which gives one double point and no sign to keep. The method then stops with an error, or it follows a fixed rule. The sign in METHOD is a determinant of the draft, and a value near zero computed in floating point can have the wrong sign through [catastrophic cancellation](/catastrophic-cancellation/); compute it exactly or with a filtered predicate, as in [exact geometric computation](/exact-geometric-computation/).

**Example.** Take six points with the distance constraints $01, 02, 12, 34, 35, 45, 03, 04, 15$, two triangles $\{0, 1, 2\}$ and $\{3, 4, 5\}$ joined by three bars. With $0$ and $1$ placed, point 2 is ready (constraints to 0 and 1). After that, point 3 has constraints to 0, 4 and 5, but only 0 is placed; point 4 has the same problem, and point 5 has only 1. The method returns STUCK with $K = \{0, 1, 2\}$. Started with $3$ and $4$ placed instead, it places 5 from $\{3, 4\}$, then 0 from $\{3, 4\}$, then 1 from $\{0, 5\}$, then 2 from $\{0, 1\}$, and it succeeds.

## Classic examples

- **Sketchpad.** Sutherland's one-pass method looked for a variable that few constraints touch, set it aside to be computed last, and repeated on the rest, which gives an order for solving one variable at a time. When no order exists, Sketchpad fell back to relaxation, an iterative numerical method on the whole system, the start of [variational geometry](/variational-geometry/).
- **DeltaBlue.** Each constraint has several methods, one per possible output, and a strength. When the user adds or removes a constraint, DeltaBlue changes the chosen methods incrementally so that every variable is computed by one constraint and the plan has no cycle. It refuses constraint cycles.
- **Spreadsheets and attribute grammars.** A spreadsheet recalculates the cells in an order in which each formula has its inputs ready. The evaluation of an [attribute grammar](/attribute-grammar/) does the same on a parse tree, and it also must check that the dependencies have no cycle.
- **Constraint satisfaction.** In a finite [constraint satisfaction problem](/constraint-satisfaction-problem/), [constraint propagation](/constraint-propagation/) such as [arc consistency](/arc-consistency/) removes values instead of fixing them, but it has the same structure: a change to one variable wakes only the constraints on it.
- **Sequential geometric construction.** In a planar sketch, placing each point from two placed points is a [Henneberg](/henneberg-construction/) order. The [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/) generalizes it: it merges whole rigid clusters, not single points, and solves systems in which no single point is ever ready.

## Variations

- **Propagation of degrees of freedom.** The reverse view, used in Sketchpad and ThingLab: find a variable that only one remaining constraint touches. That constraint can always be satisfied last by that variable, so remove both, and repeat. The removed pairs, in reverse order, are a propagation plan.
- **Plans by matching and cycles by strong components.** Choose an output variable for each constraint by a [bipartite matching](/bipartite-matching/) between constraints and variables. The directed graph of the plan then has cycles exactly in its [strongly connected components](/strongly-connected-components/). Each component is solved as one simultaneous system, for example by Newton's method, and the components are solved in topological order. This is the [Dulmage-Mendelsohn decomposition](/dulmage-mendelsohn-decomposition/) of the system.
- **Incremental solving.** DeltaBlue keeps the plan between edits and repairs it locally. Most edits change only a few methods.
- **Groups instead of single constraints.** The geometric READY rule above already fires a group of two constraints at once. Graph-constructive solvers go further and fire any small rigid group whose position is fixed by the placed entities; see [graph-constructive solving](/constructive-constraint-solving/).

## Pitfalls

- **Cycles.** The two equations $x + y = 10$ and $x - y = 2$ have one solution, $x = 6$ and $y = 4$, but each has two unknowns, so neither is ever ready. In geometry, a cycle can hide even in a system that ruler and compass can solve. On the seven points with constraints $01, 02, 12, 15, 25, 03, 04, 34, 36, 46, 56$, two diamonds $\{0, 1, 2, 5\}$ and $\{0, 3, 4, 6\}$, each made of two triangles with a common edge, meet at 0 and are joined by the bar $56$. From any placed pair of adjacent points, propagation fixes at most one diamond and stops, yet the three rigid pieces, the two diamonds and the bar, pairwise share the points 0, 5 and 6, and the Fudos-Hoffmann reduction merges them. A search over all planar systems of points and distances with up to six points, in which every triangle-decomposable graph is tested, found none that propagation cannot solve from some pair; with seven points, 630 of the 178101 labeled triangle-decomposable graphs are of this kind.
- **The start matters.** The six-point example above is stuck from the pair $0, 1$ and succeeds from the pair $3, 4$. A sketcher that grounds the first two points the user drew can fail where another choice works, so try every edge as the start, or use a cluster method.
- **A method that loses a sign.** The constraint $\lvert p - q \rvert = 3$ on a line gives $p = q \pm 3$. A method that always takes $+$ returns a solution but not the one the user drew. Keep the sign of the draft, computed exactly, as in the [root identification problem](/root-identification-problem/).
- **Unused constraints not checked.** If line L8 is skipped, a conflicting constraint whose variables were fixed by other constraints is silently ignored, and the output violates it.
- **Order changes the result in an over-constrained system.** When two constraints are both ready to compute the same variable, the result depends on which one fires first. Report the second as redundant or in conflict instead of overwriting.

## Exercises

1. Show that, for points and distances in the plane, the method with the geometric READY rule, started from the adjacent points $u$ and $v$, places every point if and only if the graph has a Henneberg order of type I steps that starts from the edge $uv$.
2. Check that every pair of adjacent points of the seven-point example in the pitfalls gets stuck, and find the three clusters that the Fudos-Hoffmann reduction merges.
3. Give a plan for $z = x \cdot y$, $x + y = 7$ and $y = 3$, and show that the plan is the topological order of the graph that the matching "each constraint to the variable it computes" defines.
4. Show that the counter form of line L7 makes the loop run in time $O(\lvert X \rvert + \sum_c \lvert c \rvert)$ plus the cost of the methods.

## References
