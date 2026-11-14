---
tag: TEDKXZ
kind: problem
slug: motion-generation
name: Motion generation
aliases:
- rigid body guidance
- body guidance synthesis
area: cad/mechanism-and-assembly-design
level: core
summary: Find a linkage whose coupler takes a set of given positions and orientations, the problem Burmester theory solves for up to five positions.
prereqs: [kinematic-synthesis, four-bar-linkage]
see_also: [burmester-theory, standard-form-dyad-synthesis, path-generation, function-generation, optimization-based-linkage-synthesis, grashof-condition, transmission-angle, circle-circle-intersection]
sources:
  - book: "Ludwig Burmester, Lehrbuch der Kinematik, Erster Band, Die ebene Bewegung, Arthur Felix, Leipzig, 1888"
    locator: the theory of a plane moving through four and five given positions, the center-point and circle-point curves (general locator)
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 3 (pp. 55 to 74, graphical synthesis in the plane, the pole and the center-point theorem) and Chapter 5 (pp. 93 to 123, algebraic synthesis of planar chains)
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 3.2 (p. 100, motion generation) and Chapter 5 (two- and three-position motion generation by analytical synthesis, center-point and circle-point circles, four- and five-position synthesis)
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: Chapter 8, Introduction to Kinematic Synthesis (motion generation with the standard form, the count of free choices, and the branch and order defects)
---

Motion generation is the [kinematic synthesis](/kinematic-synthesis/) task in which a floating link of a mechanism must take a list of given positions in the plane. Each position is a location and an angle, so the link is guided as a rigid body, which is why the problem is also called rigid body guidance. For a [four-bar linkage](/four-bar-linkage/) the coupler is the guided link, and the problem splits into two independent problems, one for each grounded side. [Burmester theory](/burmester-theory/) describes all solutions for up to five positions.

## In plain words

You want to move an object from one pose to another, and maybe through a few poses in between. A pose says where the object is and which way it points. A car hood must open to a given pose, a folding seat must lie flat and then stand up, a bucket must dig and then lift without spilling.

A four-bar can do this with its middle link, the coupler. You fix the object to the coupler. Each of the two side links holds one point of the coupler on a circle around a fixed pivot. So the question for each side is: which point of the object, and which pivot, give a circle through all the poses? With two or three poses there are many answers. With four there is a curve of answers. With five there are at most four, and often none.

## Definition

**Input.** Positions $M_1, \ldots, M_n$ of a moving plane, each given by a point $P_j$ and an angle $\theta_j$. The map of the moving frame into the fixed frame is

$$D_j(x) = R(\theta_j)\,x + P_j,$$

where $R(\theta)$ is the rotation by $\theta$. In complex numbers, $D_j(z) = e^{i\theta_j} z + P_j$.

**Output.** A mechanism that has one floating link which takes all the positions $M_j$, in the given order, on one branch of its motion. For a four-bar this is two dyads. A dyad of revolute joints is a fixed pivot $m$ (the center point) and a point $c$ in the moving frame (the circle point) such that

$$|D_j(c) - m| = r \quad\text{for } j = 1, \ldots, n,$$

for some radius $r > 0$. The four-bar is the ground $m_A m_B$, the links $m_A D_j(c_A)$ and $m_B D_j(c_B)$, and the coupler $c_A c_B$. A slider dyad is the limit case $m \to \infty$, where the $n$ positions of $c$ lie on a line.

**Side conditions.** The four-bar must move from $M_1$ to $M_n$ without being taken apart (no branch defect), must reach the positions in the given order (no order defect), and should satisfy the [Grashof condition](/grashof-condition/) and a [transmission angle](/transmission-angle/) bound when a crank must turn.

## Variants

- **Number of positions.** Two and three positions leave free choices. Four positions give a one-parameter family of dyads. Five positions give finitely many. More than five have no exact solution in general, so they are met approximately.
- **Infinitesimal positions.** Some positions are infinitely close, which prescribes the velocity or the curvature of the motion at a position. The same theory holds with the poles replaced by the instant center and its derivatives.
- **Prescribed pivots.** The designer fixes one or both ground pivots and asks for the circle points. This is the inverse problem, solved with the inverse motion.
- **Other chains.** Slider-cranks (one dyad replaced by a slider), six-bars that guide a link through more positions, and spatial chains that guide a body in space.
- **Mixed tasks.** If only $P_j$ is prescribed and the angles are free, the task is [path generation](/path-generation/).

## Examples

**Two positions.** Let $M_1$ be $P_1 = (0, 0)$, $\theta_1 = 0°$, and $M_2$ be $P_2 = (4, 2)$, $\theta_2 = 90°$. The displacement is a rotation by $90°$ about its pole, the fixed point of $z \mapsto iz + (4 + 2i)$, which is $(1, 3)$. The circle point $c = (1, 0)$ moves to $(4, 3)$, so its center point lies on the perpendicular bisector of $(1, 0)$ and $(4, 3)$; the circle point $c = (0, 1)$ moves to $(3, 2)$, with its own bisector. Both bisectors pass through the pole. Picking points on them gives four-bars:

| center for $c = (1, 0)$ | center for $c = (0, 1)$ | link lengths | moves from $M_1$ to $M_2$ on one branch |
| --- | --- | --- | --- |
| $(4, 0)$ | $(3, -3)$ | 3 and 5, coupler $\sqrt 2$ | yes, the crank turns $90°$ clockwise |
| $(4, 0)$ | $(2, 0)$ | 3 and $\sqrt 5$, coupler $\sqrt 2$ | no |

The second four-bar assembles in both positions, but the two assemblies are on different branches. Moving the crank from $180°$ to $90°$ on the branch of $M_1$ ends $0.555$ away from the right place for the second pin, and the other way round the crank cannot turn. This is the branch defect, and it was found here by stepping the crank in 4000 parts.

**Three positions.** Take the positions of the coupler of the four-bar with $O_2 = (0, 0)$, $O_4 = (9, 0)$, $a = 15$, $b = 5$, $c = 13$ from the [kinematic synthesis](/kinematic-synthesis/) page, with the moving frame at the midpoint of $AB$ and along $AB$:

$$M_1 = ((14.4, 9.7), 16.26°), \qquad M_2 = ((11.5, 12), 0°), \qquad M_3 = ((2, 13.5), -36.87°).$$

For three positions, the center point of a chosen circle point is the center of the circle through its three positions. In the moving frame, $A$ is $(-2.5, 0)$ and $B$ is $(2.5, 0)$, and their centers are $O_2$ and $O_4$, as they must be. The circle point $(-2.5, 2.5)$ moves through $(11.3, 11.4)$, $(9, 14.5)$, $(1.5, 17)$, and the center of that circle is $(2.4, 7.2)$ with radius $\sqrt{96.85} \approx 9.841$.

| dyads joined | ground pivots | moves through $M_1$, $M_2$, $M_3$ in order |
| --- | --- | --- |
| $B$ and the new dyad | $(9, 0)$, $(2.4, 7.2)$ | yes, with the crank at $O_4$ turning from $53.13°$ to $112.62°$ |
| $A$ and the new dyad | $(0, 0)$, $(2.4, 7.2)$ | no: it reaches $M_2$ but misses $M_3$ by $4.04$ |

Both four-bars meet the three positions as assemblies, and only one of them is a solution. A synthesis method that returns dyads must be followed by this check.

**Five positions.** For five general positions only up to four dyads exist, so at most $\binom{4}{2} = 6$ four-bars. The real dyads come in pairs, so there are 0, 2 or 4 of them. The [Burmester theory](/burmester-theory/) page has an example.

## Known algorithms

- Graphical construction: perpendicular bisectors and the pole for two positions, the circle through three positions of a circle point for three.
- [Standard form dyad synthesis](/standard-form-dyad-synthesis/) writes each dyad as two complex vectors and solves a linear system for two or three positions once the free choices are made.
- [Burmester theory](/burmester-theory/) gives the center-point and circle-point cubics for four positions and the Burmester points for five.
- [Optimization-based dimensional synthesis](/optimization-based-linkage-synthesis/) fits a dyad to more than five positions in a least squares sense, for example by minimizing the variance of $|D_j(c) - m|$ over $j$.

## Bounds

- **Positions.** Five positions for a dyad, so five for a four-bar, in general.
- **Number of dyads.** For $n$ positions there are $5 - n$ free real parameters per dyad. For five positions there are at most four dyads, so at most six four-bars, and the number of real dyads is 0, 2 or 4.
- **Feasibility.** The bounds count assemblies. The number of four-bars that also avoid the branch and order defects is smaller and depends on the data, and the sources give no general bound for it.

## Reductions

- **To two dyad problems.** The two sides of a four-bar share only the moving frame, so each is a separate problem $|D_j(c) - m| = r$.
- **To a linear system.** For three positions and a chosen circle point $c$, the equations $|D_j(c) - m|^2 = |D_1(c) - m|^2$ are linear in $m$, because the squares of $m$ cancel. They are the equations of the perpendicular bisectors. The [standard form](/standard-form-dyad-synthesis/) gives a different linear system with the rotations of the link as free choices.
- **To polynomial equations.** For four and five positions the equations are polynomial in the four coordinates of $m$ and $c$, which leads to the cubic curves and their intersection in [Burmester theory](/burmester-theory/).
- **Function generation reduces to it.** In the frame of the input link of a four-bar, the output link makes a rigid motion, so [function generation](/function-generation/) is motion generation of the output link relative to the input.

## Applications

Motion generators guide hoods, trunk lids and doors of cars, folding seats and tables, the buckets of loaders, landing gear doors, and the platforms of lifts. They also lay out the links of prosthetic knees, where the knee must take a few given poses. Mechanism design software includes the three-position and Burmester methods for these tasks.

## References
