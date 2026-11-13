---
tag: D55C38
kind: problem
slug: geometric-constraint-problem
name: Geometric constraint solving problem
aliases:
- geometric constraint satisfaction
area: cad/geometric-constraint-solving
level: core
summary: Given geometric entities in the plane or in space and constraints between them, find placements that satisfy every constraint, up to rigid motion, or report none.
prereqs: [geometric-constraint, polynomial-system-solving]
see_also: [geometric-constraint-graph, well-constrained-system, root-identification-problem, constructive-constraint-solving, variational-geometry, assembly-constraint-solving, laman-theorem, partition-problem]
sources:
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the introductory chapters on the problem, its variants and the solution methods (general locator)
  - paper: "James B. Saxe, Embeddability of weighted graphs in k-space is strongly NP-hard, Proceedings of the 17th Allerton Conference on Communication, Control and Computing, 480 to 489, 1979"
    locator: NP-completeness in one dimension by a reduction from PARTITION, and strong NP-hardness in every dimension k by a reduction from 3SAT
  - paper: doi:10.1007/978-1-4614-0110-0_24
    title: Marcus Schaefer, Realizability of graphs and linkages, in Thirty Essays on Geometric Graph Theory, Springer, 461 to 482, 2013
    locator: the existential theory of the reals, and the completeness of graph realizability with given edge lengths for this class (general locator)
  - paper: doi:10.1145/248210.248223
    title: Ioannis Fudos and Christoph M. Hoffmann, A graph-constructive approach to solving systems of geometric constraints, ACM Transactions on Graphics 16(2), 179 to 216, 1997
    locator: the planar problem with points, lines, distances, angles and incidences, and the comparison of the solution methods (general locator)
  - paper: doi:10.1007/s00454-003-2902-0
    title: Ciprian Borcea and Ileana Streinu, The number of embeddings of minimally rigid graphs, Discrete and Computational Geometry 31(2), 287 to 303, 2004
    locator: the upper bound on the number of planar embeddings of a Laman graph, and the example with 24 embeddings (general locator)
  - paper: "Christophe Jermann, Gilles Trombettoni, Bertrand Neveu and Pascal Mathis, Decomposition of geometric constraint systems, a survey, International Journal of Computational Geometry and Applications 16(5-6), 379 to 414, 2006"
    locator: the classes of solvers and what each one guarantees (general locator)
---

The geometric constraint problem gives a set of geometric entities, such as points, lines and circles in the plane or points, planes and rigid bodies in space, and a set of [geometric constraints](/geometric-constraint/) between them, with values. It asks for placements of the entities that satisfy all the constraints. Since the constraints do not change under rotations and translations, the answer is a set of shapes, each one up to a rigid motion. This is the problem that the sketcher of every parametric CAD system solves each time the user changes a dimension. Algebraically it is the solution of a [polynomial system](/polynomial-system-solving/) over the reals, and in this generality it is hard: NP-hard already for distances in one dimension. The practical solvers work on the [constraint graph](/geometric-constraint-graph/) and break the system into small pieces.

## In plain words

You draw a rough shape and say what must be true about it: this side is 40 mm long, these two lines are parallel, this circle touches that line. The program must move the parts of the drawing until every statement is true, without moving more than it has to. Usually the statements fix the shape but not where it sits on the page, so the shape can still slide and turn as a whole.

There can be no answer, when the statements contradict each other. There can be many answers, because a triangle can open to the left or to the right. Or there can be infinitely many, when the statements leave some part free to move. The program must find out which case it is in, and in the common case of a few answers it must find the one you meant.

## Definition

**Input.** The input has these parts.

- The dimension $d$: $d = 2$ for a sketch and $d = 3$ for a 3D sketch or an assembly.
- A finite set of entities, each of a type with a fixed number of parameters (its DOF): in the plane, points and lines (2 each) and circles (3); in space, points (3), planes (3), lines (4) and rigid bodies (6).
- A finite set of constraints, each from a fixed list of types and each with its value: in the plane, distance between two points, distance from a point to a line, incidence of a point and a line, angle between two lines, parallel and perpendicular lines, tangency with a circle, and a fixed radius; in space, the same with planes and axes added. The page on [geometric constraints](/geometric-constraint/) lists the equations and their weights.

With $N$ parameters in all and $m$ scalar equations $f_k(x) = c_k$, the constraints define the real solution set
$$ Z(c) = \{x \in \mathbb{R}^N : f_k(x) = c_k \text{ for } k = 1, \ldots, m\}. $$
Each $f_k$ is invariant under the group $\mathcal{G}$ of proper rigid motions, of dimension $D = d(d + 1)/2$, so $Z(c)$ is a union of orbits of $\mathcal{G}$.

**Output.** One of these answers.

- $Z(c)$ is empty: the system is inconsistent.
- $Z(c)$ is a finite, nonzero number of orbits: return the shapes, one representative per orbit, or the one that the user wants.
- $Z(c)$ has orbits that form a family: the system is under-constrained; return one solution, usually the one nearest to the draft, and the free directions.

The usual target is a [well-constrained system](/well-constrained-system/): a system whose solution set is a finite, nonzero set of orbits, at regular points where the Jacobian has rank $m = N - D$.

**The variant on this page.** Unless a section says otherwise, the problem here is the planar problem ($d = 2$) with points and lines and with the constraints of distance, angle, incidence, parallelism and perpendicularity, over the real numbers, up to proper rigid motion. The special case with points and distances only is the realization problem of a weighted graph: given a graph $G$ and a length $\ell(uv) > 0$ for each edge, find $p : V \to \mathbb{R}^d$ with $\lvert p(u) - p(v) \rvert = \ell(uv)$ for every edge.

## Variants

- **Decision, one solution, all solutions.** Deciding whether $Z(c)$ is empty, finding one point of $Z(c)$, and listing all its orbits are three problems. The hardness results below are for the decision problem; the other two are at least as hard.
- **The intended solution.** A CAD system must return the solution that the user meant, usually the one with the same orientations of point triples as the draft. This is the [root identification problem](/root-identification-problem/). The orientations are signs of the [orientation test](/orientation-test/). A sign near zero computed in floating point can be wrong because of [catastrophic cancellation](/catastrophic-cancellation/), so the sign is taken with exact arithmetic or with a filtered predicate in the style of [Shewchuk](/shewchuk-expansion-sum/), as in [exact geometric computation](/exact-geometric-computation/). A draft with three collinear points has no sign to keep; the solver then uses a fixed rule, such as [simulation of simplicity](/simulation-of-simplicity/), or asks the user.
- **Dimension.** In one dimension the problem with distances is already NP-complete (below). In the plane, the graph theory of [Laman](/laman-theorem/) gives an exact count for points and distances. In space no such count is known, and the [3D sketch and assembly problems](/assembly-constraint-solving/) are harder to analyze.
- **Over the complex numbers.** Algebraic methods solve over $\mathbb{C}$ and then keep the real solutions. A system can have complex solutions and no real one, as a triangle with sides 1, 1 and 3 does.
- **Under-constrained and over-constrained systems.** For an under-constrained system, the user expects the solver to move as little as possible from the draft and to report which parts are still free. For an over-constrained system, the solver reports the redundant or conflicting constraints, or finds a least-squares compromise with [nonlinear least squares](/nonlinear-least-squares/).
- **Incremental solving.** The user adds or changes one constraint at a time, and the solver must update the solution fast and keep it close to the previous one. [Variational geometry](/variational-geometry/) solves the whole system again with Newton's method from the old solution.

## Examples

**A square with one diagonal.** Take points $A, B, C, D$ in the plane with $\lvert AB \rvert = \lvert BC \rvert = \lvert CD \rvert = \lvert DA \rvert = 1$ and $\lvert AC \rvert = \sqrt 2$. That is 5 constraints on 8 coordinates, and $8 - 5 = 3 = D$. Fix $A = (0, 0)$ and $B = (1, 0)$, which uses up the rigid motions. Then $C$ meets $x^2 + y^2 = 2$ and $(x - 1)^2 + y^2 = 1$; subtracting gives $x = 1$, so $C = (1, 1)$ or $C = (1, -1)$. With $C = (1, 1)$, the point $D$ meets $x^2 + y^2 = 1$ and $(x - 1)^2 + (y - 1)^2 = 1$; subtracting gives $x + y = 1$, so $D = (0, 1)$ or $D = (1, 0)$. So there are 4 solutions up to proper motion: the square, its mirror image, and two shapes in which $D$ falls on $B$ and the square folds along the diagonal. The equations do not exclude the folded shapes, and only a rule outside the equations, such as "keep the orientations of the draft", picks the square.

**Distances on a line.** In one dimension, a cycle $v_0 v_1 \cdots v_{k-1} v_0$ with edge lengths $a_0, \ldots, a_{k-1}$ has a placement if and only if signs $s_i \in \{+1, -1\}$ exist with $\sum_i s_i a_i = 0$, because $x_{i+1} - x_i = s_i a_i$ and the steps around the cycle must add to 0. For the lengths $1, 2, 3, 4$, the signs $(+, -, -, +)$ work, and the points are $0, 1, -1, -4$. For the lengths $2, 2, 2, 4$ no signs work, since the sum 10 cannot be split into two halves of 5 from even numbers, so the cycle has no placement on a line. In the plane the same cycle is an ordinary quadrilateral, because $4 < 2 + 2 + 2$.

**No real solution.** Three points with $\lvert AB \rvert = 1$, $\lvert BC \rvert = 1$ and $\lvert AC \rvert = 3$ have no placement, since $3 > 1 + 1$. Over the complex numbers the system has solutions.

## Known algorithms

Each method below solves a different version of the problem, with a different guarantee.

- **[Gröbner bases](/groebner-basis/) and [Wu's method](/wu-characteristic-set-method/).** Exact symbolic methods for the polynomial system. They decide whether a complex solution exists, find the dimension of the solution set and give all complex solutions of a zero-dimensional system in a triangular form. They do not decide real solvability by themselves, and their cost grows very fast with the number of unknowns.
- **[Cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) and [quantifier elimination](/quantifier-elimination/).** Exact decision over the [real closed field](/real-closed-field/) of the reals: they decide whether $Z(c)$ is empty and describe all its real points. The cost is doubly exponential in the number of unknowns, so they apply only to small systems.
- **[Homotopy continuation](/homotopy-continuation/).** Numerical, with the guarantee that, for generic random choices in the start system, every isolated complex solution is at the end of some path. The real solutions are then kept. The number of paths grows with the Bézout number of the system.
- **[Newton's method](/newton-method-for-systems/) from the draft.** The method of [variational geometry](/variational-geometry/). It converges quadratically when it starts near a regular solution and finds one solution, usually the one near the draft. Far from a solution it can converge to an unwanted solution or diverge. The [interval Newton method](/interval-newton-method/) adds a proof that a box holds exactly one solution.
- **[Local propagation](/local-propagation-solving/).** Solves one constraint at a time. It is exact and fast, but only on systems without cycles of constraints.
- **[Graph-constructive solvers](/constructive-constraint-solving/).** The [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/) and [Owen's decomposition](/owen-triconnected-decomposition/) find, in polynomial time, a plan of ruler and compass steps, and they give all real solutions exactly when the plan exists. The plan exists only for the triangle-decomposable systems, which are [ruler-and-compass constructible](/ruler-and-compass-constructibility/). [DR-plans](/dr-plan/) extend the idea to any system and hand the parts that do not decompose to one of the methods above.

## Bounds

**Proved hardness.**

- **One dimension.** Saxe (1979) proved that deciding whether a graph with integer edge lengths has a placement on a line is NP-complete, by the reduction from the [partition problem](/partition-problem/) in the example above. The problem is in NP: for a connected graph, a certificate is a sign for each edge of a spanning tree, from which the positions follow by additions, and then each other edge is checked.
- **Every dimension.** Saxe also proved that the problem is strongly NP-hard for every fixed dimension $k \ge 1$, by a reduction from 3SAT. So even lengths written in unary do not make it easy.
- **The exact class.** Schaefer (2013) proved that the realization of a graph with given edge lengths in the plane is complete for the existential theory of the reals, the class of problems that reduce to the question whether a system of polynomial equations and inequalities with integer coefficients has a real solution. This class contains NP and is contained in [PSPACE](/pspace/). So the planar problem is NP-hard, and it is in NP only if this class equals NP, which is not known.

**Proved bounds on the number of solutions.** For points and distances in the plane, a well-constrained system on a [Laman graph](/laman-theorem/) with $n$ points has at most $\binom{2n-4}{n-2}$ complex solutions up to rigid motion (Borcea and Streinu 2004). The triangular prism, two triangles joined by three disjoint edges, reaches 24. A strip of triangles on $n$ points has $2^{n-2}$ real solutions for generic lengths, so the number of solutions can be exponential even for the easiest systems.

**What is only measured.** No theorem says how often Newton's method from a draft reaches the intended solution. The claims that most real sketches are triangle-decomposable, and that Newton's method converges from a good draft, come from experience with CAD systems and from the test sets in the papers. They are not proved.

## Reductions

- **[Partition](/partition-problem/) to distances on a line.** The cycle with lengths $a_0, \ldots, a_{k-1}$ has a placement on a line exactly when the numbers split into two sets of equal sum. This is Saxe's reduction.
- **To [polynomial system solving](/polynomial-system-solving/).** Each constraint is a few polynomial equations in the coordinates. Fixing one point and one direction removes the rigid motions and makes a well-constrained system zero-dimensional.
- **To the existential theory of the reals.** Realizability is a single existential statement over the reals, and Schaefer shows that the reverse reduction also holds, so the two are equivalent.
- **To [inverse kinematics](/inverse-kinematics/) and linkages.** A linkage is an under-constrained system, and its configurations are the solutions. The [forward kinematics of the Stewart-Gough platform](/stewart-gough-forward-kinematics/) is a well-constrained 3D instance with six distance constraints.

## Applications

- **Parametric sketches.** Every sketcher in [feature-based modeling](/feature-based-modeling/) solves this problem when the user drags a point or changes a dimension.
- **Assemblies.** Mates between parts are constraints between rigid bodies in space; see [assembly constraint solving](/assembly-constraint-solving/).
- **Molecular geometry.** The positions of atoms from measured distances are a realization problem in space; with all pairwise distances known it is solved by [multidimensional scaling](/multidimensional-scaling/).
- **Sensor networks.** The positions of sensors from measured ranges between neighbors are a realization problem in the plane, and the [rigidity](/generic-rigidity/) of the graph decides whether the answer is unique up to finitely many choices.

## References
