---
tag: A0MCRT
kind: definition
slug: geometric-constraint
name: Geometric constraint
aliases:
- dimensional constraint
area: cad/geometric-constraint-solving
level: intro
summary: A relation between geometric elements, such as a distance, an angle, incidence, parallelism or tangency, that a sketch or an assembly must satisfy.
prereqs: [special-euclidean-group]
see_also: [geometric-constraint-graph, geometric-constraint-problem, well-constrained-system, bar-and-joint-framework, degrees-of-freedom-analysis, kinematic-pair, constraint-satisfaction-problem, feature-based-modeling]
sources:
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the introductory chapters on geometric constraint systems, their entities and constraint types (general locator)
  - paper: doi:10.1145/248210.248223
    title: Ioannis Fudos and Christoph M. Hoffmann, A graph-constructive approach to solving systems of geometric constraints, ACM Transactions on Graphics 16(2), 179 to 216, 1997
    locator: the planar entities (points and lines) and the distance, angle and incidence constraints of the solver (general locator)
  - book: isbn:9780262111645
    title: Glenn A. Kramer, Solving Geometric Constraint Systems, A Case Study in Kinematics, MIT Press, 1992
    locator: the geometric entities with their translational and rotational degrees of freedom, and the constraints between markers on rigid bodies (general locator)
  - paper: "Christophe Jermann, Gilles Trombettoni, Bertrand Neveu and Pascal Mathis, Decomposition of geometric constraint systems, a survey, International Journal of Computational Geometry and Applications 16(5-6), 379 to 414, 2006"
    locator: the definition of a geometric constraint system and the degrees of freedom of its objects and constraints (general locator)
---

A geometric constraint is a relation between geometric entities, such as points, lines, circles, planes or rigid bodies, that a placement of these entities must satisfy. Typical constraints are a distance between two points, an angle between two lines, a point on a line, two parallel lines and a line tangent to a circle. In a CAD sketch the user draws an approximate shape and adds constraints, and a solver moves the entities until all constraints hold. Each constraint is a small set of equations in the coordinates, and these equations do not change when the whole sketch is rotated or translated. So a constraint fixes the shape, not the position of the sketch in the plane.

## Definition

Fix the space $\mathbb{R}^d$, with $d = 2$ for a sketch and $d = 3$ for an assembly. Let $\mathcal{G}$ be the group of proper rigid motions of $\mathbb{R}^d$, the rotations followed by translations ([special Euclidean group](/special-euclidean-group/)). Its dimension is $D = d(d + 1)/2$: 3 in the plane, 6 in space.

**Entities.** Each geometric entity has a type and a vector of real parameters. The number of free parameters is its *degrees of freedom* (DOF). A rigid motion acts on the parameters.

| entity | parameters | DOF |
|---|---|---|
| point in the plane | $p = (x, y)$ | 2 |
| line in the plane | unit normal $n = (\cos\varphi, \sin\varphi)$ and offset $h$, the line $n \cdot z = h$ | 2 |
| circle in the plane | center $c$ and radius $r$ | 3 |
| point in space | $(x, y, z)$ | 3 |
| plane in space | unit normal and offset | 3 |
| line in space | a direction and a point, up to the choice of the point | 4 |
| rigid body in space | a rotation and a translation | 6 |

A *configuration* is a choice of parameters for all entities, a vector $x \in \mathbb{R}^N$, where $N$ is the sum of the DOF of the entities.

**Constraint.** A geometric constraint on entities $e_1, \ldots, e_k$ is a system of equations
$$ f_j(x_{e_1}, \ldots, x_{e_k}) = c_j, \qquad j = 1, \ldots, w, $$
in the parameters of these entities only, such that each $f_j$ is invariant under $\mathcal{G}$: $f_j(g \cdot x) = f_j(x)$ for all $g \in \mathcal{G}$. The constants $c_j$ are the *values* of the constraint, such as a length or the cosine of an angle; for a relation without a value, such as incidence, they are 0. The number $w$ of independent equations is the number of DOF that the constraint removes, its *weight*. Most constraints are binary ($k = 2$). A constraint with $k = 1$, such as a fixed radius, restricts the shape of one entity.

The planar constraints of most sketchers, with the equations used here, are these.

| constraint | entities | equation | weight |
|---|---|---|---|
| distance $\delta$ | two points $p, q$ | $\lvert p - q \rvert^2 = \delta^2$ | 1 |
| incidence | point $p$, line $(n, h)$ | $n \cdot p - h = 0$ | 1 |
| distance $\delta$ to a line | point $p$, line $(n, h)$ | $n \cdot p - h = \pm\delta$ | 1 |
| angle $\theta$ | two lines | $n_1 \cdot n_2 = \cos\theta$ and a choice of sign | 1 |
| parallel | two lines | $n_1 \times n_2 = 0$ | 1 |
| perpendicular | two lines | $n_1 \cdot n_2 = 0$ | 1 |
| tangency | line $(n, h)$, circle $(c, r)$ | $n \cdot c - h = \pm r$ | 1 |
| tangency | two circles | $\lvert c_1 - c_2 \rvert = r_1 \pm r_2$ | 1 |
| coincidence | two points | $p = q$ | 2 |

In space, the weights are: coincidence of two points 3, a point on a plane 1, a point on a line 2, two coincident planes 3, two coaxial lines 4, two parallel planes 2, and one each for an angle, a perpendicularity and a distance. [Kinematic pairs](/kinematic-pair/), the joints of a mechanism, are constraints between rigid bodies of the same kind.

**Signs and branches.** Many constraints have more than one branch: a tangent line can touch the circle on either side, and an angle constraint does not say whether the second line turns to the left or to the right. The equation defines the union of the branches. A solver chooses a branch by a sign in the user's draft, for example the sign of the [orientation test](/orientation-test/) of three points, computed exactly. This choice is the [root identification problem](/root-identification-problem/).

**Degenerate values.** The weight is the number of equations, and it is the rank of their Jacobian only at regular points. A distance of 0 is the main trap: over the reals, $\lvert p - q \rvert^2 = 0$ forces $p = q$, which removes 2 DOF, and the Jacobian of the equation is zero at every solution. CAD systems therefore treat a distance of 0 as a coincidence, with weight 2, and treat two parallel lines at angle 0 with the parallel constraint, not with the angle equation.

## Examples and non-examples

- **A distance.** The points $p = (0, 0)$ and $q = (3, 4)$ satisfy the distance constraint with $\delta = 5$, since $3^2 + 4^2 = 25$. Rotate both points by 90 degrees about the origin to $(0, 0)$ and $(-4, 3)$: the constraint still holds, because the squared distance is invariant.
- **A tangency.** The line $y = 2$ has $n = (0, 1)$ and $h = 2$. The circle with center $(5, 0)$ and radius 2 satisfies $n \cdot c - h = -2 = -r$, so the line touches this circle above its center. The circle with center $(5, 4)$ and radius 2 also satisfies the equation, with the other sign, and the line touches it below its center. The two choices are two branches of one constraint.
- **A bar.** A set of points with distance constraints only is a [bar-and-joint framework](/bar-and-joint-framework/). Its theory of rigidity applies directly to such sketches.
- **Not a geometric constraint: a fixed coordinate.** The condition "the $x$-coordinate of $p$ is 3" is not invariant under translations. It ties $p$ to the frame of the sheet. A sketcher models it as a constraint between $p$ and a fixed entity, such as the origin or a grounded axis, which removes the rigid motions.
- **Not a geometric constraint: a side condition.** The condition "$p$ is to the left of the line $l$" is an inequality, not an equation. It does not remove a degree of freedom. Solvers use such conditions only to choose among the solutions of the equations.
- **Not invariant under reflections.** An oriented angle of $+30$ degrees from $l_1$ to $l_2$ is invariant under proper motions but not under reflections. Distances are invariant under reflections too, so a system of distances only has the mirror image of each solution as a solution. For this reason the group here is the group of proper motions.

## Related definitions

- A [geometric constraint graph](/geometric-constraint-graph/) has a vertex for each entity and an edge for each constraint, weighted by DOF.
- A [geometric constraint problem](/geometric-constraint-problem/) asks for a configuration that satisfies a given set of constraints.
- A system of constraints is [well-constrained](/well-constrained-system/) when it has finitely many solutions up to rigid motion.
- [Degrees of freedom analysis](/degrees-of-freedom-analysis/) counts the DOF of the entities against the weights of the constraints.
- A [constraint satisfaction problem](/constraint-satisfaction-problem/) is the general version over finite domains; geometric constraints have real domains and are solved by algebra and numerical methods.
- In [feature-based modeling](/feature-based-modeling/), the sketches of the features carry geometric constraints, and the [persistent naming problem](/persistent-naming-problem/) arises when a constraint refers to an entity that a later change removes.

## References
