---
tag: 1V1MTE
kind: problem
slug: kinematic-synthesis
name: Kinematic synthesis
aliases:
- mechanism synthesis
- linkage synthesis
area: cad/mechanism-and-assembly-design
level: core
summary: Find the type, number and dimensions of the links of a mechanism that performs a given motion, split into type, number and dimensional synthesis.
prereqs: [four-bar-linkage, grubler-formula]
see_also: [function-generation, path-generation, motion-generation, burmester-theory, standard-form-dyad-synthesis, optimization-based-linkage-synthesis, nine-point-path-synthesis, kempe-universality-theorem]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 3.2 (p. 100, function, path and motion generation), Section 2.7 (number synthesis), and Chapter 5 (analytical linkage synthesis, precision points and the number of positions that each method can match)
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: Chapter 8, Introduction to Kinematic Synthesis, Graphical and Linear Analytical Methods (the tasks, the dyad method and the count of free choices)
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 3 (pp. 55 to 74, graphical synthesis in the plane) and Chapter 5 (pp. 93 to 123, algebraic synthesis of planar chains)
  - paper: doi:10.1017/S0962492911000067
    title: Charles W. Wampler and Andrew J. Sommese, Numerical algebraic geometry and algebraic kinematics, Acta Numerica 20 (2011), 469 to 567
    locator: the part on mechanism design (precision point synthesis as a polynomial system, and the solution counts of the planar problems)
  - book: "Richard S. Hartenberg and Jacques Denavit, Kinematic Synthesis of Linkages, McGraw-Hill, New York, 1964"
    locator: the opening chapters on type, number and dimensional synthesis (general locator)
---

Kinematic synthesis is the design problem of mechanisms: given a motion that a machine must make, find a mechanism that makes it. The question is the inverse of kinematic analysis, which takes a mechanism and finds its motion. The work is split into type synthesis (which kind of mechanism), number synthesis (how many links and joints) and dimensional synthesis (the lengths and the pivot positions). Most of the theory is about dimensional synthesis of planar linkages, and in particular of the [four-bar linkage](/four-bar-linkage/), for the three tasks of [function generation](/function-generation/), [path generation](/path-generation/) and [motion generation](/motion-generation/).

## In plain words

Analysis asks what a given machine does. Synthesis asks the other way round: you know what the machine must do, and you must find the machine. For example, a wiper blade must sweep a given arc, a pick-up tool must pass through a list of points, or a lid must open from one pose to another.

You decide in three steps. First pick the kind of mechanism, for example a linkage, a cam or a gear train. Then pick how many links and joints it has. Last, find the sizes: the length of each link and the place of each fixed pivot.

The last step is the hard one. A designer gives a few exact positions that the machine must pass through, or asks for the best fit to many positions. Each choice leads to a different set of equations, and the methods on the linked pages solve them.

## Definition

There is no single formal statement in the literature. The texts agree on the parts below, and each named method fixes one version.

**The task.** A motion requirement on one link of a mechanism with one degree of freedom (or more). It is one of three kinds:

- *Function generation.* The angle (or slide) of an output link must be a given function $\psi = f(\varphi)$ of the angle of an input link.
- *Path generation.* A point on a floating link (the coupler) must pass along a given curve, or through given points, with or without a given timing against the input.
- *Motion generation*, also called rigid body guidance. A floating link must take given positions, each a location and an angle in the plane.

**Type synthesis.** Choose the class of mechanism: linkage, [cam and follower](/cam-profile-synthesis/), gear train, or a combination.

**Number synthesis.** Choose the number of links $n$ and the number of joints $j$ for a given mobility $M$. For planar chains with revolute (or prismatic) joints only, the mobility is given by [Grübler's formula](/grubler-formula/) $M = 3(n - 1) - 2j$, when the joint constraints are independent.

**Dimensional synthesis.** For a chosen chain, find the vector $x$ of design variables (link lengths, fixed pivot coordinates, coupler point coordinates, initial angles) such that the mechanism does the task. Two forms are in use:

- *Precision point synthesis.* The task is given at finitely many positions $1, \ldots, n$, and the mechanism must meet them exactly. This gives a system of equations $F(x) = 0$, usually polynomial after a change of variables.
- *Approximate synthesis.* The task is given at many positions or as a continuous curve, and $x$ minimizes an error measure $E(x)$, subject to constraints.

**Side constraints.** In both forms, the mechanism must also be usable: it assembles at every position, it reaches the positions in the right order on one branch (no branch or circuit change between positions), the [transmission angle](/transmission-angle/) stays away from $0°$ and $180°$, the [Grashof condition](/grashof-condition/) holds when a link must turn fully, and the pivots fit in the available space.

## Variants

- **By task.** Function, path and motion generation, as above. Path generation is with prescribed timing when each path point is tied to a given input angle, and without it otherwise.
- **Exact against approximate.** Precision point methods meet a finite set of conditions exactly and say nothing about the motion between them. Approximate methods spread the error over the whole range.
- **Finite against infinitesimal positions.** Some positions can be given as infinitely close, which prescribes a velocity, acceleration or curvature at a point. Burmester theory covers this case too.
- **By mechanism.** Four-bars (4R), slider-cranks, six-bars of the [Watt and Stephenson](/watt-and-stephenson-six-bar/) types, geared linkages, and spatial linkages each have their own count of design variables.
- **Exact curve tracing.** The task is a whole algebraic curve, not a list of points. [Kempe's universality theorem](/kempe-universality-theorem/) says that a linkage exists for each bounded piece of each algebraic curve, and the [Peaucellier-Lipkin linkage](/peaucellier-lipkin-linkage/) is the classic exact straight line.

## Examples

**Number synthesis for one degree of freedom.** With revolute joints only, $M = 1$ in Grübler's formula gives $j = (3n - 4)/2$, so $n$ must be even.

| links $n$ | joints $j$ | chains with $M = 1$ |
| --- | --- | --- |
| 4 | 4 | 1 (the four-bar) |
| 6 | 7 | 2 (Watt and Stephenson) |
| 8 | 10 | 16 |

The counts of chains are those quoted on the [Watt and Stephenson](/watt-and-stephenson-six-bar/) page.

**One linkage, three tasks.** Take the four-bar with ground $d = 9$, input $a = 15$, coupler $b = 5$ and output $c = 13$, with $O_2 = (0, 0)$ and $O_4 = (9, 0)$. At three input angles the pins sit at exact rational points, which can be checked by hand. One branch of the linkage passes through all three positions as the input turns from $36.87°$ to $90°$ (checked by a step of the input in 1000 parts).

| position | input $\theta_2$ | pin $A$ | pin $B$ | output $\theta_4$ | coupler $\theta_3$ | midpoint $P$ of $AB$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | $36.87°$ | $(12, 9)$ | $(16.8, 10.4)$ | $53.13°$ | $16.26°$ | $(14.4, 9.7)$ |
| 2 | $53.13°$ | $(9, 12)$ | $(14, 12)$ | $67.38°$ | $0°$ | $(11.5, 12)$ |
| 3 | $90°$ | $(0, 15)$ | $(4, 12)$ | $112.62°$ | $-36.87°$ | $(2, 13.5)$ |

The three synthesis problems read this table from the other side. Function generation gives the pairs $(\theta_2, \theta_4)$ and asks for the linkage. Path generation gives the points $P$, perhaps with the matching $\theta_2$. Motion generation gives $P$ together with $\theta_3$. Each problem has many solutions, and this linkage is one of them. The [transmission angle](/transmission-angle/) at the three positions is $36.9°$, $67.4°$ and $149.5°$, so position 1 is near the edge of the usual design range of $40°$ to $140°$. An analysis step of this kind is always part of a synthesis.

**Free choices of a dyad.** The [standard form dyad](/standard-form-dyad-synthesis/) for motion generation has two complex unknowns (four reals) and one unknown rotation per position after the first, against two real equations per position after the first. With $n$ positions there are $4 + (n - 1) - 2(n - 1) = 5 - n$ free real choices.

| positions $n$ | equations | unknowns | free choices | solutions for one dyad |
| --- | --- | --- | --- | --- |
| 2 | 2 | 5 | 3 | a 3-parameter family |
| 3 | 4 | 6 | 2 | a 2-parameter family, linear for each choice |
| 4 | 6 | 7 | 1 | a curve: the circle-point and center-point cubics |
| 5 | 8 | 8 | 0 | at most 4 dyads |

## Known algorithms

The algorithms are on their own pages. This list gives what each one guarantees.

- [Freudenstein's equation](/freudenstein-equation/) turns three-point function generation for a four-bar into a $3 \times 3$ linear system in link ratios. It is exact at the three points when the system is regular and the result assembles.
- [Chebyshev spacing](/chebyshev-spacing/) places the precision points of function generation at the mapped zeros of a Chebyshev polynomial. It lowers a bound on the structural error, but it does not minimize the error itself.
- [Standard form dyad synthesis](/standard-form-dyad-synthesis/) writes each side of a linkage as a dyad and gives a linear system in the dyad vectors once the rotations are chosen. It solves two and three positions exactly.
- [Burmester theory](/burmester-theory/) describes all dyads for four positions (a cubic curve of center points) and for five positions (at most four dyads).
- [Nine-point path synthesis](/nine-point-path-synthesis/) is the largest precision point problem for a four-bar path generator. It is solved by [homotopy continuation](/homotopy-continuation/), with 1442 linkages up to cognates for generic data.
- [Optimization-based dimensional synthesis](/optimization-based-linkage-synthesis/) minimizes an error over many points with local or global optimizers. It handles many points and side constraints but has no guarantee of a global optimum.
- Graphical methods (the pole, the perpendicular bisector, the center-point circle) are the hand forms of the dyad and Burmester methods.

## Bounds

The useful bounds for dimensional synthesis are counts of positions and of solutions, not running times.

- **Maximum number of exact positions.** Motion generation with a four-bar: 5 positions (Burmester). Path generation with a four-bar and no timing: 9 points (Alt). Function generation with a four-bar: 3 points with the ratio form of Freudenstein's equation, and 5 when the start angles of input and output are also free.
- **Number of solutions.** Five-position motion generation: at most 4 dyads, so at most 6 four-bars. Nine-point path generation: 1442 linkages up to [Roberts cognates](/roberts-chebyshev-theorem/), found numerically by Wampler, Morgan and Sommese in 1992. These are complex solution counts; the real solutions are fewer and depend on the data.
- **Existence.** For each bounded piece of a real algebraic curve there is a planar linkage that traces it ([Kempe's universality theorem](/kempe-universality-theorem/)). The linkage can need many bars, so this is a statement of existence and not a design method.

The literature measures the difficulty of the precision point problems by solution counts. No complexity class result for linkage synthesis in general appears in the sources cited here.

## Reductions

- **Motion generation splits into dyads.** A four-bar is two grounded dyads joined by the coupler. Each dyad must meet the same rigid body positions, so the problem splits into two independent dyad problems, which is the basis of [Burmester theory](/burmester-theory/).
- **Function generation becomes motion generation by inversion.** Fix the input link and watch the output link. The output link then makes a rigid motion relative to the input, and a dyad that guides it is the coupler. The precision points become relative positions.
- **Precision point synthesis becomes polynomial system solving.** The loop equations, written with $e^{i\theta}$ and its conjugate as separate unknowns, are polynomial, and all their solutions can be found by [homotopy continuation](/homotopy-continuation/) or by [polynomial system solving](/polynomial-system-solving/).
- **Approximate synthesis becomes nonlinear least squares or global optimization.** A sum of squared errors over sample points is a [nonlinear least squares](/nonlinear-least-squares/) problem, and the design space usually has many local minima.

## Applications

Kinematic synthesis is used to design the linkages of wipers, hood and trunk hinges, folding seats, landing gears, packaging and printing machines, walking toys, and prosthetic and orthotic joints. A linkage is often chosen over a cam because pin joints are cheap and wear well. Synthesis software for these tasks implements the dyad and Burmester methods and adds an analysis step that checks the side constraints.

## References
