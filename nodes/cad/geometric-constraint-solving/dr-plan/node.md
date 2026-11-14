---
tag: DCFR07
kind: technique
slug: dr-plan
name: Decomposition-recombination plan
aliases:
- DR-plan
- DR-planning
area: cad/geometric-constraint-solving
level: research
summary: Hoffmann, Lomonosov and Sitharam's plan that recursively splits a constraint system into minimal dense subsystems, so each step solves a small system and recombines.
prereqs: [degrees-of-freedom-analysis, constructive-constraint-solving]
see_also: [fudos-hoffmann-reduction, owen-triconnected-decomposition, root-identification-problem, assembly-constraint-solving, pebble-game-rigidity, laman-theorem, homotopy-continuation, max-flow-min-cut-theorem]
sources:
  - paper: doi:10.1006/jsco.2000.0402
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Decomposition plans for geometric constraint systems, Part I, Performance measures for CAD, Journal of Symbolic Computation 31(4), 367 to 408, 2001
    locator: the definition of a DR-plan, the performance measures for DR-planners, and the analysis of the older planners against them (general locator)
  - paper: doi:10.1006/jsco.2000.0403
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Decomposition plans for geometric constraint problems, Part II, New algorithms, Journal of Symbolic Computation 31(4), 409 to 427, 2001
    locator: the Frontier algorithm and its modified form MFA, which build a DR-plan from minimal dense subgraphs found by flows (general locator)
  - paper: doi:10.1007/BFb0017460
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Finding solvable subsets of constraint graphs, Principles and Practice of Constraint Programming (CP97), LNCS 1330, 1997
    locator: the flow algorithm for dense subgraphs and the reduction of a dense subgraph to a minimal one (general locator)
  - paper: doi:10.1016/j.cagd.2015.07.001
    title: Troy Baker, Meera Sitharam, Menghan Wang and Joel Willoughby, Optimal decomposition and recombination of isostatic geometric constraint systems for designing layered materials, Computer Aided Geometric Design 40, 1 to 25, 2015
    locator: the abstract and introduction, on the NP-hardness of optimal DR-planning for over-constrained 2D bar-and-joint systems, the O(n^3) algorithm for a broad class of isostatic or under-constrained systems, and the optimality of canonical DR-plans
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on decomposition and recombination planning (general locator)
---

A decomposition-recombination plan, or DR-plan, tells a solver in which order to solve the parts of a geometric constraint system. It is a directed acyclic graph whose nodes are rigid subsystems. The leaves are the single entities, each node is the union of its children, and the roots are the maximal rigid subsystems. The solver works from the leaves up: at each node it treats the children, already solved, as rigid bodies, places them so that the constraints between them hold, and passes the result up as one rigid body. Hoffmann, Lomonosov and Sitharam defined DR-plans in 2001 as the common frame for all decomposition methods. The triangle merges of [Fudos and Hoffmann](/fudos-hoffmann-reduction/) and the splits of [Owen](/owen-triconnected-decomposition/) are DR-plans with small nodes. Their Frontier algorithm builds a plan for any weighted constraint graph from minimal dense subgraphs, found by the network flows of [degrees of freedom analysis](/degrees-of-freedom-analysis/). The cost of a plan is its width, the largest number of children of a node, because that node needs the hardest solve. Finding a plan of the smallest width is NP-hard in general, but Baker, Sitharam, Wang and Willoughby gave an $O(n^3)$ algorithm for a broad class of systems that are not over-constrained.

## In plain words

A large drawing with many dimensions is hard to solve all at once. But it usually has small parts that are fixed in shape by themselves: a triangle, a rectangle with a diagonal, a bracket. Solve those first, and then treat each one as a single stiff piece. Now the drawing has fewer pieces, and some groups of pieces are again fixed by themselves. Solve them, glue them, and go on.

The record of what was glued to what, and in which order, is the plan. It is a tree of parts, except that two parts may share a point, so a point can sit under two parents. A good plan keeps every step small. Sometimes a step cannot be made small: some drawings have no stiff part except the whole, and then the solver must solve that whole part at once.

## When it applies

- The system is a weighted [constraint graph](/geometric-constraint-graph/): each entity $v$ has $w(v)$ degrees of freedom and each constraint $e$ removes $w(e)$, and a rigid body keeps $D$ freedoms, $D = 3$ in the plane and $D = 6$ in space.
- A set $S$ of entities is *rigid* when $\rho(S) = w(E(S)) - w(S) \ge -D$ and $S$ has at least two entities. Hoffmann, Lomonosov and Sitharam call such a set *dense*; the page on the [constraint graph](/geometric-constraint-graph/) keeps the word "dense" for the stricter $\rho(S) > -D$, so this page says "rigid".
- The counts are structural. For points and distances in the plane they decide rigidity for generic values by [Laman's theorem](/laman-theorem/); for other systems they are a necessary condition, as the page on [well-constrained systems](/well-constrained-system/) explains, and the solve of each node must check its own result.
- A *DR-plan* is a directed acyclic graph with these properties: every node is a rigid set; the leaves are the single entities; each other node is the union of its children, which are proper rigid subsets of it or leaves; the roots are the maximal rigid sets. The *fan-in* of a node is its number of children, and the *width* of the plan is its largest fan-in. An *optimal* DR-plan has the smallest width.

## The template

```pseudo id=main
DR-PLAN(G, w, D)
L1  C ← an empty set of clusters; make one leaf per entity
L2  loop
L3      U ← ⟨FIND⟩ a minimal rigid set of entities that does not lie inside one cluster of C
L4      if there is no such U then break
L5      make a node U whose children are the maximal clusters of C inside U and the entities of U in none of them
L6      C ← (C − {the clusters inside U}) ∪ {U}            ▷ ⟨SIMPLIFY⟩ the graph for the next search
L7  RECOMBINE: for each node U in the order made do
L8      ⟨SOLVE⟩ the children of U as rigid bodies, with the constraints of U that lie inside no child
L9      ⟨SELECT⟩ one solution of U, and store it as the rigid body U
L10 return the plan; the clusters of C are the roots
```

The holes are these.

- **FIND.** Use the flow test of [degrees of freedom analysis](/degrees-of-freedom-analysis/) with slack $D + 1$, so that it reports sets with $\rho \ge -D$. Then shrink the set: drop one entity at a time and test again whether a rigid set is left, which gives a minimal one with $O(n)$ more flow tests. In the Frontier algorithm the flow runs on the simplified graph of SIMPLIFY, so a set that lies inside one cluster is not found again.
- **SIMPLIFY.** The Frontier algorithm replaces a new cluster by its *frontier* entities, those with constraints to entities outside it, joined to one core vertex that stands for the inside, with weights that make the replacement rigid. Keeping the frontier entities is what lets two clusters share an entity. Contracting a cluster to one vertex is simpler, but it loses the shared entities (see the pitfalls).
- **SOLVE.** A node with fan-in 2 or 3 in the plane is often a triangle of clusters, solved by a [circle-circle intersection](/circle-circle-intersection/). A larger node needs a general method: [Newton's method](/newton-method-for-systems/) from the draft, [homotopy continuation](/homotopy-continuation/) for all complex solutions, or a [Gröbner basis](/groebner-basis/).
- **SELECT.** Each node has several solutions. The choice by the orientations of the draft is the [root identification problem](/root-identification-problem/); a choice at a low node can leave a higher node with no real solution.

**Why a plan exists.** By line L3 every new node is rigid, by line L5 it is the union of its children, and line L6 keeps the clusters maximal. When line L4 stops, every rigid set lies inside one cluster, and no cluster lies inside another, so the clusters are the maximal rigid sets, which are the roots. Each pass makes a rigid set that was not a cluster before and removes only clusters inside it, so no set is made twice, and the loop ends.

**Example.** Take the triangular prism: points 0 to 5 with $w = 2$, the triangles $01, 02, 12$ and $34, 35, 45$, and the bars $03, 14, 25$, each constraint with $w = 1$, and $D = 3$. The whole set has $\rho = 9 - 12 = -3$, so it is rigid, and for generic lengths it is well-constrained.

| passes | rigid set $U$ found | $\rho(U)$ | children |
|---|---|---|---|
| 1 to 9 | each constraint $\{u, v\}$ | $1 - 4 = -3$ | the leaves $u$ and $v$ |
| 10 | $\{0, 1, 2\}$ | $3 - 6 = -3$ | $\{0, 1\}$, $\{0, 2\}$, $\{1, 2\}$ |
| 11 | $\{3, 4, 5\}$ | $3 - 6 = -3$ | $\{3, 4\}$, $\{3, 5\}$, $\{4, 5\}$ |
| 12 | $\{0, 1, 2, 3, 4, 5\}$ | $9 - 12 = -3$ | $\{0, 1, 2\}$, $\{3, 4, 5\}$, $\{0, 3\}$, $\{1, 4\}$, $\{2, 5\}$ |

No other set is rigid: every other set has too few edges, for example $\{0, 1, 3, 4\}$ has $4 < 5$ and $\{0, 1, 2, 3, 4\}$ has $6 < 7$. So passes 10 and 11 are triangles, each solved by one circle-circle intersection with two solutions, and pass 12 has fan-in 5. A plan may also give the root only the two triangles as children, with the bars as constraints of the node; its width is then 3, but the solve at the root is the same. At this node the solver must place two rigid triangles, with 3 freedoms left between them, so that the three bars hold. That is a system with no rigid part smaller than the whole, and it is not solvable by ruler and compass (see [constructibility](/ruler-and-compass-constructibility/)); over the complex numbers it can have up to 24 solutions. No plan avoids this node, because the prism has no other rigid sets. On $K_{3,3}$ the plan is even flatter: its only proper rigid sets are its nine edges, so the root has fan-in 9, and the whole system is one solve.

## Classic examples

- **Triangle-decomposable sketches.** The merges of the [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/) give a DR-plan in which every node above the edges has fan-in 3, three clusters that pairwise share one point. Each node is a quadratic step.
- **Owen's splits.** The tree of [Owen's decomposition](/owen-triconnected-decomposition/), read from the leaves up, is a DR-plan whose nodes glue two rigid sides at a separation pair.
- **Sketches with a hard core.** A sketch whose core is a prism or $K_{3,3}$, with triangles and other easy parts around it, gets a plan with many small nodes and one node for the core. Only that node needs a general solver.
- **Assemblies.** In [assembly constraint solving](/assembly-constraint-solving/), a node is a rigid subassembly of parts, and $D = 6$.
- **Layered materials.** Baker, Sitharam, Wang and Willoughby use optimal DR-plans for the design of materials made of layers of rigid units, where the constraint systems are large and are not over-constrained.

## Variations

- **Frontier and MFA.** The Frontier algorithm of Hoffmann, Lomonosov and Sitharam (Part II) builds the plan bottom-up as in the template, with the frontier simplification. Its modified form, MFA, changes how a cluster is found so that the plan stays close to optimal more often.
- **Canonical DR-plans.** Baker and his coauthors define a *canonical* DR-plan, in which the children of each node are its maximal proper rigid subsets, and show that every canonical DR-plan is optimal for isostatic or under-constrained systems in a broad class, with an $O(n^3)$ algorithm in the plane.
- **Optimal plans in general.** Finding an optimal DR-plan is NP-hard; Baker and his coauthors note that this holds already for over-constrained 2D bar-and-joint systems.
- **Older planners.** Part I measures the older planners against criteria such as the classes of input they accept, whether every node is really solvable, how close the width is to the optimum and how the plan changes when a constraint is added. It shows that planners that only recognize fixed shapes, such as triangles, and planners based on matchings each fail some of these.
- **Incremental plans.** When the user changes the value of a constraint, only the node that solves it and the nodes above that node must be solved again; the other nodes keep their shapes. When the user adds or removes a constraint, a planner can update the plan near it instead of starting again, which is one of the measures of Part I.

## Pitfalls

- **Contracting a cluster loses shared entities (SIMPLIFY).** Take points 0 to 5 with the constraints $01, 02, 12, 34, 35, 45, 03, 04, 15$. If the cluster $\{0, 1, 2\}$ is contracted to one body $B$ of weight 3, then the set $\{B, 3, 4\}$ with the constraints $03$, $04$, $34$ has $\rho = 3 - 7 = -4$ and is not rigid, so the planner misses the triangle $\{0, 3, 4\}$: it no longer sees that $03$ and $04$ meet at the same point. It later sees two bodies joined by three bars, which looks like the prism, though the step is two triangles. Keep the frontier entities.
- **A rigid count is not a rigid system (SOLVE).** The counts are structural. In space, or with special values such as parallel lines, a node can pass the count and still flex or have no solution. Check the rank of the Jacobian at the solution of each node, or use the action analysis of Kramer.
- **Over-constrained nodes (FIND).** A minimal set with $\rho > -D$ has more constraints than it needs. Its solve has a solution only if the extra constraints agree, so report it, or drop a constraint, before the solve.
- **Local choices of roots (SELECT).** Each node may have several solutions, and a choice that is valid for the node can make a higher node unsolvable, as when a fold of one triangle makes a later triangle too long. Keep the orientations of the draft at every node, and be ready to go back.
- **Width is not the whole cost (SOLVE).** Fan-in counts children, not the difficulty of the solve. A node of fan-in 3 can be a triangle, solved by a quadratic equation, or a part that needs a high-degree solve.

## Exercises

1. Show that a DR-plan of a triangle-decomposable Laman graph exists in which every node that is not an edge or a leaf has exactly three children.
2. Show that every DR-plan of the prism has the whole prism as a node whose children lie inside the two triangles, so that its solve must place the two triangles with the three bars between them.
3. In the pitfall graph, find the plan that the template makes with the frontier simplification, and give the fan-in of each node.
4. Show that the set returned by the shrink step of FIND is minimal: no proper subset with two or more entities is rigid.
5. Find a weighted constraint graph with points and lines in which a node passes the count but its solve has a continuum of solutions.

## References
