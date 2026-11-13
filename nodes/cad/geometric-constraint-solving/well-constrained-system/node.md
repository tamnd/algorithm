---
tag: 002JWQ
kind: definition
slug: well-constrained-system
name: Well-constrained system
aliases:
- structurally well-constrained
area: cad/geometric-constraint-solving
level: core
summary: A constraint system with finitely many solutions up to rigid motion. With fewer constraints it is under-constrained, with dependent ones over-constrained.
prereqs: [geometric-constraint-problem, infinitesimal-rigidity]
see_also: [degrees-of-freedom-analysis, laman-theorem, dr-plan, root-identification-problem, dulmage-mendelsohn-decomposition, geometric-constraint-graph, global-rigidity, matroid-intersection]
sources:
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 2, Infinitesimal Rigidity, and Chapter 4, Linear and Planar Rigidity (independence and the generic counts)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on combinatorial rigidity and on decomposition of constraint systems (general locator)
  - paper: doi:10.1006/jsco.2000.0402
    title: Christoph M. Hoffmann, Andrew Lomonosov and Meera Sitharam, Decomposition plans for geometric constraint systems, Part I, Performance measures for CAD, Journal of Symbolic Computation 31(4), 367 to 408, 2001
    locator: well-constrained, under-constrained and over-constrained systems and subsystems, defined by degree of freedom counts on the constraint graph
  - paper: "Christophe Jermann, Gilles Trombettoni, Bertrand Neveu and Pascal Mathis, Decomposition of geometric constraint systems, a survey, International Journal of Computational Geometry and Applications 16(5-6), 379 to 414, 2006"
    locator: the count-based notions of rigidity of constraint systems and the examples on which they fail (general locator)
  - paper: doi:10.1007/BF01534980
    title: G. Laman, On graphs and rigidity of plane skeletal structures, Journal of Engineering Mathematics 4(4), 331 to 340, 1970
    locator: the counts that decide regularity of generic point and distance systems in the plane
---

A geometric constraint system is well-constrained when it has at least one solution and only finitely many solutions up to the rigid motions of the space. It is under-constrained when its solutions form a continuum that rigid motions do not explain, and over-constrained when some of its constraints depend on the others, so that they are redundant or contradict each other. A CAD sketch should be well-constrained, so that its shape is fixed by its dimensions and a solver can find it. Counts of degrees of freedom on the constraint graph predict this for generic dimensions, but they can pass while the actual geometry is degenerate.

## Definition

Fix the space $\mathbb{R}^d$ and the group $\mathcal{G}$ of its rigid motions, the translations and rotations, of dimension $D = d(d + 1)/2$: 3 in the plane, 6 in space.

**Constraint system.** The unknowns are the coordinates $x \in \mathbb{R}^N$ of the geometric entities, 2 for a point in the plane, 3 for a point in space, and so on. The constraints are $m$ equations $f_k(x) = c_k$, where each $f_k$ is a polynomial that does not change under $\mathcal{G}$ (a squared distance, an incidence, a tangency, a parallelism) and $c_k$ is the dimension value. The solution set is $Z(c) = \{x : f_k(x) = c_k \text{ for all } k\}$. It is a union of orbits $\mathcal{G} x$. See [geometric constraint problem](/geometric-constraint-problem/).

**Definition.** The system is

- *well-constrained* if $Z(c)$ is nonempty and is the union of finitely many orbits,
- *under-constrained* if $Z(c)$ contains infinitely many orbits,
- *over-constrained* if $Z(c)$ is empty, or some constraint is *redundant*: there is a solution $x^*$ with a neighborhood $U$ such that every point of $U$ that satisfies the other constraints also satisfies this one.

A system can be both over-constrained and under-constrained, when one part has a redundant constraint and another part is loose.

**Regular solutions.** Let $J(x)$ be the $m \times N$ Jacobian of $(f_1, \ldots, f_m)$. Each $f_k$ is constant on orbits, so the tangent space of the orbit, the infinitesimal rigid motions at $x$, lies in $\ker J(x)$. Call a solution $x^*$ *regular* if its orbit has dimension $D$ and
$$ \operatorname{rank} J(x^*) = m = N - D. $$
The rows are then independent and the kernel is exactly the infinitesimal rigid motions. For points and distances, $J$ is twice the rigidity matrix, and a regular solution is a minimally [infinitesimally rigid](/infinitesimal-rigidity/) framework.

**Proposition 1.** If every solution is regular and $Z(c)$ is nonempty, the system is well-constrained. Moreover, every small change of the values $c$ keeps a solution near each solution.

*Proof.* At a regular solution the $m$ functions have independent differentials, so by the implicit function theorem $Z(c)$ is, near $x^*$, a manifold of dimension $N - m = D$. The orbit $\mathcal{G} x^*$ is a connected manifold of the same dimension $D$ inside it, so it is open in $Z(c)$ near each of its points; it is also closed, because the action of the rigid motions on configurations with orbits of full dimension is proper. So each connected component of $Z(c)$ that meets $x^*$ is a single orbit. $Z(c)$ is a real algebraic set, and a real algebraic set has finitely many connected components, so there are finitely many orbits. For the second claim, $J(x^*)$ has full row rank $m$, so the map $x \mapsto (f_k(x))_k$ is a submersion at $x^*$, and its image contains a neighborhood of $c$. $\square$

**Proposition 2 (the count is necessary).** If $x^*$ is regular, then $m = N - D$, and every subset of $m'$ constraints that involves only entities with $N'$ coordinates in total satisfies $m' \le N' - D'$, where $D'$ is the dimension of the orbit of those entities. In the plane, for points and distances, this is the [Laman](/laman-theorem/) count $m' \le 2k - 3$ on every $k \ge 2$ points.

*Proof.* The rows of the subset are zero outside the $N'$ columns of their entities, and on those columns they vanish on the $D'$-dimensional tangent space of the orbit of the sub-configuration, since each $f_k$ is invariant. So these rows have rank at most $N' - D'$, and they are independent, so $m' \le N' - D'$. $\square$

**Counts on the graph.** A degree of freedom count on the [constraint graph](/geometric-constraint-graph/), with each entity weighted by its freedoms and each constraint by the freedoms it removes, tests the condition of Proposition 2 on every subsystem. [Degrees of freedom analysis](/degrees-of-freedom-analysis/), the [DR-plan](/dr-plan/) and many solvers use it to find the well-constrained, under-constrained and over-constrained parts. This structural condition is different from the definition above. It depends only on the graph, and it says what happens for generic dimension values and generic positions. For points and distances in the plane it is exact for generic values, by Laman's theorem. In general the counts can pass while the geometry is degenerate, and for some constraint types or in space they can pass even generically while the system is not well-constrained. The examples below show both cases.

**Bipartite and matroid views.** The [Dulmage-Mendelsohn decomposition](/dulmage-mendelsohn-decomposition/) of the bipartite graph of equations and unknowns, computed by [bipartite matching](/bipartite-matching/), splits a general system into under-determined, well-determined and over-determined parts by structure alone. It does not know about rigid motions, so a sketch looks under-determined by $D$ unknowns unless the solver first fixes $D$ coordinates. The rigidity counts take the motions into account. For points and distances in the plane the independent constraint sets form a [matroid](/matroid/), the generic rigidity matroid, and its counts can be tested with spanning tree packing and [matroid intersection](/matroid-intersection/) algorithms or with the [pebble game](/pebble-game-rigidity/). In dimension 1 the matroid is the [graphic matroid](/graphic-matroid/), and a system of distances on a line is generically well-constrained when its graph is a spanning tree.

## Examples and non-examples

The Jacobian ranks below are exact ranks with rational arithmetic.

- **A triangle.** Three points with three generic distances: $N = 6$, $m = 3 = N - D$, the Jacobian has rank 3, and the system is well-constrained. It has two solutions up to rotations and translations, a triangle and its mirror image.
- **A chain of triangles.** A strip of $k$ triangles, each sharing an edge with the next, is well-constrained, with up to $2^k$ solutions up to rotations and translations, since each new point can be put on either side of its base. Picking the intended one is the [root identification problem](/root-identification-problem/). For points and distances in the plane, a single solution up to isometries needs [global rigidity](/global-rigidity/), and for $n \ge 4$ points that needs more than $2n - 3$ distances.
- **Under-constrained: a four-bar.** Four points with the four side lengths of a quadrilateral have $m = 4 < 5 = N - D$. The Jacobian has rank 4, and the quadrilateral flexes in a one-parameter family of shapes.
- **Over-constrained: $K_4$.** Four points with all six distances have $m = 6 > 5$. For random values there is no solution. For values measured on a real placement there is one shape, and near it any one distance is implied by the other five, because $K_4$ minus an edge is already rigid. So each distance is redundant.
- **Counts pass, geometry degenerate.** Three points $a, b, c$ with $|ab| = 1$, $|bc| = 2$, $|ac| = 3$. The counts are those of a triangle, the Laman graph $K_3$. But $3 = 1 + 2$, so every solution is collinear with $b$ between $a$ and $c$, and at such a solution the Jacobian has rank 2, not 3: the solution is not regular. The system has one solution up to motions, so it is well-constrained by the definition, and no constraint is redundant, since removing any one lets the points hinge. But changing $|ac|$ to $3.01$ leaves no solution, and changing it to $2.99$ gives two. A Newton solver meets a singular Jacobian here.
- **Counts pass, generically under-constrained and over-constrained.** Three points with three angle constraints, one at each corner of the triangle. The count gives $N - D = 6 - 3 = 3 = m$. But the angles do not change under scaling, so the kernel of the Jacobian contains the 3 rigid motions and the scaling, and its rank is at most 2. The three angles must sum to $\pi$, so one constraint is redundant or contradicts the others, and the size of the triangle is free. The correct count uses the 4-dimensional group of similarities for angle-only systems.
- **Counts pass in space, still flexible.** The double banana, two copies of $K_5$ minus an edge glued at the ends of the missing edge, has 8 points and $18 = 3 \cdot 8 - 6$ distances, and no subset breaks the count $3k - 6$. Its Jacobian has rank 17 at every placement, so it is under-constrained and over-constrained at once: one distance is redundant, and the two halves turn about the line through the shared points.

## Related definitions

- **[Degrees of freedom analysis](/degrees-of-freedom-analysis/).** The count-based method that solvers use to decompose a system into well-constrained pieces.
- **[DR-plan](/dr-plan/).** A plan that solves a well-constrained system by a sequence of small well-constrained subsystems.
- **[Laman's theorem](/laman-theorem/) and [generic rigidity](/generic-rigidity/).** For points and distances in the plane, a system is regular at generic values exactly when its graph is a Laman graph.
- **[Global rigidity](/global-rigidity/).** A well-constrained system has finitely many solutions; a globally rigid one has a single solution.
- **[Root identification problem](/root-identification-problem/).** The choice among the finitely many solutions of a well-constrained system.
- **[Maxwell's counting rule](/maxwell-counting-rule/).** The count $m = N - D$ of Proposition 2 for frameworks, with self-stresses for over-constrained and mechanisms for under-constrained frameworks.

## References
