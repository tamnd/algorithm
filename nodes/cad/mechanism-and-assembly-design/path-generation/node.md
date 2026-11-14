---
tag: FWWMAP
kind: problem
slug: path-generation
name: Path generation
aliases:
- path synthesis of linkages
area: cad/mechanism-and-assembly-design
level: core
summary: Find a linkage in which a coupler point passes through given points or follows a given curve, with or without prescribed timing.
prereqs: [kinematic-synthesis, coupler-curve]
see_also: [nine-point-path-synthesis, standard-form-dyad-synthesis, roberts-chebyshev-theorem, optimization-based-linkage-synthesis, function-generation, motion-generation, peaucellier-lipkin-linkage, homotopy-continuation]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 3.2 (p. 100, path generation), Section 3.7 (p. 134, cognates) and Chapter 5 (analytical synthesis of a path generator with prescribed timing)
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: Chapter 8, Introduction to Kinematic Synthesis (path generation with and without prescribed timing, the standard form and the count of free choices)
  - paper: doi:10.1002/zamm.19230030103
    title: H. Alt, Über die Erzeugung gegebener ebener Kurven mit Hilfe des Gelenkvierecks, Zeitschrift für Angewandte Mathematik und Mechanik 3(1), 1923, 13 to 19
    locator: the problem of a four-bar coupler curve through nine given points
  - paper: "Charles W. Wampler, Alexander P. Morgan and Andrew J. Sommese, Complete solution of the nine-point path synthesis problem for four-bar linkages, ASME Journal of Mechanical Design 114(1), 1992, 153 to 159"
    locator: the count of 1442 cognate triples of four-bars through nine generic points, found by homotopy continuation
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 5 (pp. 93 to 123), algebraic synthesis of planar chains
---

Path generation is the [kinematic synthesis](/kinematic-synthesis/) task in which a point on the floating link of a mechanism must pass through given points of the plane, or follow a given curve. The point is the coupler point and its trace is a [coupler curve](/coupler-curve/). The task comes in two forms: with prescribed timing, each point must be reached at a given input angle; without it, only the path matters. For a [four-bar linkage](/four-bar-linkage/) the most points that can be met exactly are nine without timing and five with timing.

## In plain words

You want one point of a machine to move along a given track. A tool must pass over a row of holes, a film claw must go in, down and out, or a walking toy must move a foot along a flat line and then lift it. You write down a few points of the track, or the whole track, and look for a linkage whose moving part carries a point through them.

Sometimes it matters when the point arrives, for example when the input crank is at a given angle. Then the problem has prescribed timing. Sometimes only the track matters. A four-bar has nine sizes to choose, so it can pass exactly through at most nine points in general. Between the points the track can bend away, so the designer must check the whole curve.

## Definition

**Input.**

- Precision points $P_1, \ldots, P_n$ in the plane, or a curve $\gamma$ given by many sample points or a parameterization.
- With prescribed timing, input angles $\theta_{2,1}, \ldots, \theta_{2,n}$, usually as rotations $\beta_j = \theta_{2,j} - \theta_{2,1}$ from the first position.
- A type of mechanism, usually the four-bar, sometimes a slider-crank or a six-bar.

**Unknowns of a four-bar path generator.** The two ground pivots (4 reals), the lengths of input, coupler and output (3 reals), and the coupler point in the frame of the coupler (2 reals): 9 reals in all. With prescribed timing, the start angle of the input is fixed by the data and only the rotations matter.

**Output, exact form.** A mechanism and an assembly branch such that the coupler point passes through each $P_j$ (at the input angle $\theta_{2,j}$ when the timing is prescribed), and the motion from $P_1$ to $P_n$ stays on one branch and visits the points in order.

**Output, approximate form.** A mechanism that minimizes a distance between its coupler curve and $\gamma$. Without timing, the distance is between sets of points, for example the largest distance from a sample point of $\gamma$ to the curve. With timing, it is a sum of $|C(\theta_{2,j}) - P_j|^2$ where $C$ is the coupler point as a function of the input angle.

## Variants

- **With or without prescribed timing.** Timing ties each point to an input angle. Without timing, the input angles are extra unknowns.
- **Exact points or a whole curve.** A finite set of points gives a system of equations. A whole curve gives an approximation problem.
- **Closed or open path.** A closed path asks for a coupler curve of the right shape, often on a fully turning crank. An open path asks only that the curve contains an arc through the points.
- **Exact straight lines and exact curves.** The classic straight-line four-bars of Watt, Chebyshev and Hoeken give a line only approximately. The [Peaucellier-Lipkin linkage](/peaucellier-lipkin-linkage/) traces an exact line with eight links, and [Kempe's universality theorem](/kempe-universality-theorem/) gives a linkage for any bounded piece of an algebraic curve.
- **Points with orientation.** If the angle of the coupler is also given at each point, the task is [motion generation](/motion-generation/).

## Examples

**One path, three linkages.** Take the four-bar with $O_2 = (0, 0)$, $O_4 = (9, 0)$, input $a = 15$, coupler $b = 5$, output $c = 13$, and let the coupler point $P$ be the midpoint of $AB$. At the input angles $36.87°$, $53.13°$ and $90°$ (the exact positions on the [kinematic synthesis](/kinematic-synthesis/) page), $P$ is at

$$P_1 = (14.4, 9.7), \qquad P_2 = (11.5, 12), \qquad P_3 = (2, 13.5).$$

The path generation problem gives these three points and asks for a linkage. The four-bar above is one answer. The [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/) gives two more that trace the same whole curve. Here $P$ divides $AB$ in the ratio $\rho = (P - A)/(B - A) = 1/2$, so the third ground pivot is $O_C = O_2 + \rho(O_4 - O_2) = (4.5, 0)$, and each cognate is the original linkage scaled by $\rho$ or $1 - \rho$ with the roles of the links changed. The pins below were computed in complex numbers from the Cayley diagram and are exact:

| linkage | ground pivots | grounded links | coupler | $P$ on the coupler | pins at position 1 | pins at position 3 |
| --- | --- | --- | --- | --- | --- | --- |
| original | $(0, 0)$, $(9, 0)$ | 15, 13 | 5 | midpoint of $AB$ | $(12, 9)$, $(16.8, 10.4)$ | $(0, 15)$, $(4, 12)$ |
| cognate 1 | $(0, 0)$, $(4.5, 0)$ | 2.5, 6.5 | 7.5 | 15 from the first pin, on the coupler line | $(2.4, 0.7)$, $(8.4, 5.2)$ | $(2, -1.5)$, $(2, 6)$ |
| cognate 2 | $(9, 0)$, $(4.5, 0)$ | 2.5, 7.5 | 6.5 | 13 from the first pin, on the coupler line | $(6.6, -0.7)$, $(10.5, 4.5)$ | $(7, 1.5)$, $(4.5, 7.5)$ |

All three pass through $P_1$, $P_2$, $P_3$. In cognate 2 the link from $O_C$ to the pin $(10.5, 4.5)$ is at $36.87°$, $53.13°$ and $90°$ at the three positions, the same angles as the input of the original. So cognate 2 is also an answer with prescribed timing when it is driven from $O_C$. In cognate 1 the grounded link at $O_2$ turns with the coupler of the original, through $16.26°$, $0°$ and $-36.87°$, so with the original timing it is not an answer.

**Free choices with prescribed timing.** Write each side of the four-bar as a dyad that carries the coupler point (the [standard form](/standard-form-dyad-synthesis/)). For the input side, the rotations $\beta_j$ are given and the coupler rotations $\alpha_j$ are unknown. Each position after the first gives two real equations, so for $n$ points the input dyad has $4 + (n - 1) - 2(n - 1) = 5 - n$ free choices, the same count as for motion generation. Once the $\alpha_j$ are fixed by the input dyad, the output dyad has its own unknown rotations, and the same count holds for it. So timing allows at most five exact points.

**Free choices without timing.** The nine unknowns of the four-bar against two equations per point (with one unknown input angle per point) give $9 - n$ free parameters for $n$ points in general. Nine points leave none, and the solutions are isolated.

| points $n$ | with timing: free choices per dyad | without timing: free parameters |
| --- | --- | --- |
| 3 | 2 | 6 |
| 4 | 1 | 5 |
| 5 | 0 | 4 |
| 9 | none (too many) | 0 |

## Known algorithms

- [Standard form dyad synthesis](/standard-form-dyad-synthesis/) solves path generation with prescribed timing for two or three points as a linear system once the free choices are made.
- For four and five points with timing, the dyad equations are nonlinear, and they are solved like the [Burmester](/burmester-theory/) equations of motion generation, by elimination or [homotopy continuation](/homotopy-continuation/).
- [Nine-point path synthesis](/nine-point-path-synthesis/) is the exact problem with the most points. It was solved completely by homotopy continuation, with 1442 cognate triples of solutions for generic points.
- [Optimization-based dimensional synthesis](/optimization-based-linkage-synthesis/) fits a coupler curve to many points or to a whole curve, with local or global optimizers.
- Atlases of coupler curves let a designer choose a linkage by the shape of its curve and then scale, rotate and move it.

## Bounds

- **Exact points for a four-bar.** Nine without timing (Alt 1923), five with prescribed timing.
- **Number of solutions for nine points.** For nine generic points there are 1442 nondegenerate four-bars up to Roberts cognates, so 4326 linkages. This count was found numerically by Wampler, Morgan and Sommese in 1992. Only some of these are real, and fewer still move through the points in order on one branch.
- **Curves that a four-bar cannot follow.** A four-bar coupler curve lies on an algebraic curve of degree six with fixed singularities at the circular points, so a general curve is followed only approximately. A linkage with more bars can follow any bounded piece of an algebraic curve exactly, by [Kempe's universality theorem](/kempe-universality-theorem/).

## Reductions

- **With timing, to two dyad problems.** The input dyad fixes the coupler rotations; the output dyad then meets the same coupler point with those rotations. Each is a standard form system.
- **Without timing, to a polynomial system.** The nine-point problem becomes a system of eight polynomial equations after a change of variables, which [homotopy continuation](/homotopy-continuation/) solves.
- **To motion generation.** If the coupler rotations $\alpha_j$ are chosen by the designer, the task becomes [motion generation](/motion-generation/) for the positions $(P_j, \alpha_j)$.
- **Approximate synthesis to nonlinear least squares.** With timing, the error is a sum of squares of smooth functions of the dimensions, a [nonlinear least squares](/nonlinear-least-squares/) problem.

## Applications

Path generators move the claw of film projectors, the needle bar and feed of sewing machines, the pick-up arms of packaging machines, and the legs of walking machines such as the Chebyshev and Jansen linkages. Straight-line linkages guided the piston rods of beam engines before machined slides were cheap. Path generation with prescribed timing is used when a moving point must meet a part on a conveyor at a known moment.

## References
