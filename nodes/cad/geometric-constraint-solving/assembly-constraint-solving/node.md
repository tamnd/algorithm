---
tag: N0F97R
kind: problem
slug: assembly-constraint-solving
name: Assembly constraint solving
aliases:
- assembly mating
area: cad/geometric-constraint-solving
level: advanced
summary: Place rigid parts in 3D so that mating constraints such as coincident faces, concentric axes and fixed distances hold, often split into rigid subsystems.
prereqs: [geometric-constraint-problem, special-euclidean-group, degrees-of-freedom-analysis]
see_also: [tay-theorem, kinematic-pair, grubler-formula, root-identification-problem, dr-plan, stewart-gough-forward-kinematics, inverse-kinematics, tolerance-stack-up]
sources:
  - book: isbn:9780262111645
    title: Glenn A. Kramer, Solving Geometric Constraint Systems, A Case Study in Kinematics, MIT Press, 1992
    locator: rigid bodies with markers, the constraints between markers, and the solution of assemblies and linkages by degrees of freedom analysis (general locator)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on body frameworks, on constraint systems in three dimensions and on decomposition (general locator)
  - paper: doi:10.1016/0095-8956(84)90016-9
    title: Tiong-Seng Tay, Rigidity of multigraphs. I. Linking rigid bodies in n-space, Journal of Combinatorial Theory, Series B 36(1), 95 to 112, 1984
    locator: the main theorem, generic rigidity of body-and-bar frameworks by edge-disjoint spanning trees
  - paper: "James B. Saxe, Embeddability of weighted graphs in k-space is strongly NP-hard, Proceedings of the 17th Allerton Conference on Communication, Control and Computing, 480 to 489, 1979"
    locator: strong NP-hardness of the realization of a graph with edge lengths in every fixed dimension
  - paper: doi:10.1007/978-1-4614-0110-0_24
    title: Marcus Schaefer, Realizability of graphs and linkages, in Thirty Essays on Geometric Graph Theory, Springer, 461 to 482, 2013
    locator: the completeness of graph realization with given edge lengths for the existential theory of the reals (general locator)
---

Assembly constraint solving places the rigid parts of a mechanical assembly in space so that the *mates* between them hold: this face lies on that face, this hole is concentric with that pin, these two edges are 5 mm apart. Each part has the 6 degrees of freedom (DOF) of a rigid motion, a pose in the [special Euclidean group](/special-euclidean-group/) $SE(3)$, and each mate removes some of them. It is the [geometric constraint problem](/geometric-constraint-problem/) in three dimensions with rigid bodies as the entities. The general problem is NP-hard, and in space no count of DOF decides rigidity, because real mates share freedoms. CAD systems therefore split the assembly into rigid subassemblies, solve the easy mates in closed form as Kramer did, and give the rest to Newton's method.

## In plain words

You have parts made in separate files, and you say how they fit: the bolt goes through the hole, the lid sits on the box, the door turns on its hinge. The program must move and turn each part until all these statements are true. One part stays fixed, the ground, and every other part can move in three directions and turn about three axes.

Each statement takes away some of this freedom. When all the freedom is gone, the parts are locked in place. When some is left, a part can still move, like a door on its hinge. The hard cases come when two statements take away the same freedom, and a simple count of freedoms then gives the wrong answer.

## Definition

**Input.** The input has these parts.

- A finite set of rigid bodies $B_0, B_1, \ldots, B_N$. Each body carries *features* in its own frame: points, axes (oriented lines) and planes (with a normal). The body $B_0$ is the ground and does not move.
- A finite set of mates, each between a feature of one body and a feature of another, with a value where the type has one.

**Unknowns.** A pose $g_i = (R_i, t_i) \in SE(3)$ for each body $B_i$ with $i \ge 1$, with $R_i$ a rotation and $t_i$ a translation. A point $a$ of $B_i$ is at $R_i a + t_i$, and a direction $u$ of $B_i$ points along $R_i u$. So there are $6N$ unknowns, and the solution set lies in $SE(3)^N$.

**The mates.** Each mate is a few equations in the poses. The weight is the number of DOF that the mate removes when it acts alone.

| mate | equations | weight |
|---|---|---|
| point on point | the two points are equal | 3 |
| point on plane | the point lies on the plane | 1 |
| point on axis | the point lies on the line | 2 |
| plane on plane | opposite normals and a common point | 3 |
| parallel planes at a distance | parallel normals and the offset | 3 |
| concentric axes | the two lines are equal | 4 |
| angle between axes | the dot product of the directions | 1 |
| distance between points | the squared distance | 1 |

**Output.** Poses that satisfy all the mates; or a report that no poses do, with the mates in conflict; or, if the solution set has positive dimension, one solution near the current poses and the motions that are still free.

**The variant on this page.** Bodies with point, axis and plane features, the mates of the table, a fixed ground body, and real solutions. The count is $6N - \sum w$ over the mates; the assembly is *well-constrained* when its solution set is finite and nonzero and the Jacobian of the mate equations has rank $6N$ at the solutions.

## Variants

- **Mechanisms.** A mechanism is an assembly that is under-constrained on purpose. A hinge is a concentric mate and a point on plane, which leave the turn about the axis, as a revolute [kinematic pair](/kinematic-pair/) does. The solver must then find a pose for a given input angle, the problem of the forward kinematics of a closed linkage, and the [Grübler formula](/grubler-formula/) counts the DOF of the mechanism.
- **Body-and-bar frameworks.** If every mate is a distance between two points on different bodies, the assembly is a body-and-bar framework. For generic positions of the points, [Tay's theorem](/tay-theorem/) decides rigidity by the graph alone: the framework is rigid exactly when its multigraph of bars has 6 edge-disjoint spanning trees.
- **Up to motion.** Without a ground body, the solution is a set of poses up to one common rigid motion, and the count is $6(N + 1) - 6 - \sum w$, the same number.
- **Over-constrained assemblies.** Real designs often have redundant mates that agree, such as a pin and its shoulder face. The solver must tell redundant mates from conflicting ones, which needs the rank of the equations, not the count.
- **Tolerances.** With tolerances on the mate values, the question is how far the poses can move, the [tolerance stack-up](/tolerance-stack-up/) of the assembly.

## Examples

**A door on a hinge.** The ground has the $z$-axis and the plane $z = 0$. The door $B_1$ has an axis along its local $z$-axis through its local origin $o$, and a corner point $c = (3, 0, 0)$. The mates are: the door axis concentric with the $z$-axis (weight 4), the point $o$ on the plane $z = 0$ (weight 1), and $\lvert c\, s \rvert = 4$ for the ground point $s = (5, 0, 0)$ (weight 1). The count is $6 - 4 - 1 - 1 = 0$.

The first two mates fix $o$ at the origin and leave only a turn $R_z(\theta)$ about the axis: the linear equations of the two mates in the twist $(\omega, v)$ of the door are $\omega_x = \omega_y = 0$ and $v = 0$, of rank 5. The third gives $\lvert R_z(\theta) c - s \rvert^2 = 9 + 25 - 30 \cos\theta = 16$, so $\cos\theta = 3/5$ and $\sin\theta = \pm 4/5$, and the corner is at $(9/5, 12/5, 0)$ or $(9/5, -12/5, 0)$. In both solutions the derivative of the distance mate is $12\, \omega_z$, which is not 0, so the Jacobian has rank 6 and the assembly is well-constrained with 2 solutions. The choice between the two is the [root identification problem](/root-identification-problem/) in space. If the distance is changed to 2, the two solutions meet at $\theta = 0$, and the rank drops to 5. For a distance outside $[2, 8]$, no pose exists.

**A pin with a shoulder.** A pin concentric with a hole (weight 4) whose shoulder face lies on the face around the hole (weight 3) gives the count $6 - 4 - 3 = -1$. Both mates fix the two tilts, so the rank is 5, and the turn about the axis is free. The page on [degrees of freedom analysis](/degrees-of-freedom-analysis/) treats this case: the count reports a conflict that is not there and misses a freedom that is.

## Known algorithms

- **Newton's method on all poses.** As in [variational geometry](/variational-geometry/), write all mate equations in the $6N$ pose parameters and apply [Newton's method](/newton-method-for-systems/) or the [Levenberg-Marquardt method](/levenberg-marquardt/) from the current poses, with the rotations updated by the [Rodrigues formula](/rodrigues-rotation-formula/) or kept as unit quaternions. It converges fast near a regular solution and has no global guarantee; redundant mates make the Jacobian singular and need a least-squares step.
- **Degrees of freedom analysis.** [Kramer's method](/degrees-of-freedom-analysis/) keeps, for each body, the translational and rotational DOF that are left, and satisfies one mate at a time by a translation or rotation computed in closed form. It solves the assemblies that its table of actions covers, in a plan that runs again fast when values change, and hands the others to a numerical solver.
- **Decomposition.** The [DR-plan](/dr-plan/) method of Hoffmann, Lomonosov and Sitharam works on any weighted constraint graph, with weight 6 for a body and the mate weights on the edges. It finds the subassemblies that are dense by the count and solves them from the inside out. In space the count is necessary for rigidity but not sufficient, so a dense subassembly can still be flexible.
- **Combinatorial rigidity for bars.** For body-and-bar frameworks with generic points, a pebble game for 6 edge-disjoint spanning trees decides rigidity and finds the rigid parts exactly, by [Tay's theorem](/tay-theorem/).
- **Loop closure.** A closed chain of bodies joined by kinematic pairs is a loop, and the solver can cut the loop and solve its closure as an [inverse kinematics](/inverse-kinematics/) problem, in closed form for chains with 6 joints of simple geometry.
- **Algebraic methods.** Small, hard subsystems go to [homotopy continuation](/homotopy-continuation/) or [Gröbner bases](/groebner-basis/), which give all their complex solutions. The [forward kinematics of the Stewart-Gough platform](/stewart-gough-forward-kinematics/), a body on six distance mates, has up to 40 solutions.

## Bounds

**Proved hardness.**

- **NP-hard.** Give each point of a graph its own body, and each edge a distance mate between the two points. The assembly has a solution exactly when the graph with its edge lengths has a placement in space, and Saxe proved that this is strongly NP-hard. So the decision whether an assembly with distance mates has a solution is strongly NP-hard.
- **The exact class.** Add a point on plane mate that keeps each of these points on the plane $z = 0$ of the ground. Then the assembly has a solution exactly when the graph has a placement in the plane, which is complete for the existential theory of the reals by Schaefer. The mate equations are polynomial, with $R_i^\top R_i = I$ and $\det R_i = 1$, so the decision is in this class too, and it is complete for it.

**Proved combinatorics.** For body-and-bar frameworks in generic position, rigidity is exactly the condition of 6 edge-disjoint spanning trees (Tay 1984), and it is tested in polynomial time. For mates that share freedoms, as the axes and planes of real parts do, no such count is known: the pin with a shoulder fails the count and is still a correct design. When the mate equations are independent, the count is necessary: the total weight is $6N$, the mates among any $k$ moving bodies and the ground have weight at most $6k$, and the mates among $k \ge 2$ moving bodies alone have weight at most $6k - 6$. In space this count is not sufficient.

**What is only measured.** That most industrial assemblies split into small rigid subassemblies, that Kramer's actions cover most of the mates in practice, and that Newton's method converges from the poses that the user drags into place, all come from experience with CAD systems and from the examples in the sources. They are not proved.

## Reductions

- **From graph realization.** A graph with edge lengths becomes an assembly with one body per vertex and a distance mate per edge, as above, so the hardness of realization transfers.
- **To polynomial systems.** Each pose is a rotation matrix with $R^\top R = I$ and $\det R = 1$, or a unit quaternion, and a translation, and each mate is a few polynomial equations in these unknowns, so the problem is a case of [polynomial system solving](/polynomial-system-solving/).
- **To body-and-bar frameworks.** For a rigidity test, a mate of weight $w$ can be replaced by $w$ bars between the two bodies, when the mate is generic. Tay's theorem then applies; the replacement is not valid for mates whose freedoms overlap.
- **To the planar problem.** If all axes are parallel and all motions are in one plane, the assembly is a planar system with 3 DOF per body, and the methods of [constructive solving](/constructive-constraint-solving/) for the plane apply.

## Applications

- **Mechanical CAD.** The assembly module of a CAD system solves the mates each time the user adds a part or changes a value, and reports the parts that are still free.
- **Mechanism design.** The positions of a linkage for a range of input angles, and the collision checks along the path, come from solving the assembly with one free DOF.
- **Robotics.** Closed kinematic chains, such as parallel robots, are assemblies of links and joints, and their forward kinematics is an assembly problem.
- **Molecules.** Proteins are modeled as rigid groups of atoms joined by bonds about which they turn, a body-and-hinge framework, and their flexibility is analyzed with the same rigidity theory.

## References
