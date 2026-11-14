---
tag: 3QAECD
kind: model
slug: four-bar-linkage
name: Four-bar linkage
aliases:
- four-bar mechanism
- 4R linkage
area: cad/mechanism-and-assembly-design
level: intro
summary: A closed chain of four rigid links joined by four revolute joints with one link fixed, the simplest and most used planar mechanism with one degree of freedom.
prereqs: [kinematic-chain, kinematic-pair]
see_also: [grashof-condition, vector-loop-closure, freudenstein-equation, slider-crank-mechanism, coupler-curve, transmission-angle, instant-center-of-velocity, watt-and-stephenson-six-bar]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Sections 2.12 (p. 53, inversion), 2.13 (p. 55, the Grashof condition and the classification of the fourbar on p. 60), 3.2 (p. 100, function, path and motion generation), 3.6 (p. 124, coupler curves), 4.5 (p. 187), 4.12 (p. 211, toggle positions) and 4.13 (p. 212, circuits and branches)
  - book: isbn:9780198561248
    title: Kenneth H. Hunt, Kinematic Geometry of Mechanisms, Clarendon Press, Oxford, 1978
    locator: Chapter 7, the four-bar linkage and its coupler curves
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 2 (pp. 15 to 53), analysis of planar linkages, the planar 4R linkage
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: Section 1.6 (mobility) and Section 1.9 (Grashof's law)
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: the chapters on the fundamentals of linkages and on position analysis
---

A four-bar linkage is a closed [kinematic chain](/kinematic-chain/) of four rigid links joined in a cycle by four revolute joints, with one link fixed as the ground. It has one degree of freedom, so one input angle fixes the whole linkage up to a choice of assembly. It is the simplest planar mechanism that can turn one rotation into another rotation with a varying ratio, and most planar linkage theory starts with it.

This page is of kind model, and its standard sections hold the parts of a mechanism model: the mechanism (under The machine), its parameters and configuration space (under What it counts), what it can do (under Relation to other models), and the known results.

## The machine

### The mechanism

The links, in the notation of Norton, are the ground $d$ from the pivot $O_2 = (0, 0)$ to the pivot $O_4 = (d, 0)$, the input $a$ from $O_2$ to the pin $A$, the coupler $b$ from $A$ to the pin $B$, and the output $c$ from $O_4$ to $B$. The four joints $O_2$, $A$, $B$, $O_4$ are revolute [kinematic pairs](/kinematic-pair/), which is why the chain is also written 4R. The link angles $\theta_2$, $\theta_3$, $\theta_4$ of $a$, $b$, $c$ are measured counterclockwise from the ground line. The position of the linkage is a solution of the loop equation

$$a e^{i\theta_2} + b e^{i\theta_3} - c e^{i\theta_4} - d = 0.$$

A coupler point $P$ is a point fixed to the coupler, at distance $p$ from $A$ and at the angle $\delta$ from the line $AB$: $P = a e^{i\theta_2} + p e^{i(\theta_3 + \delta)}$. The input is usually driven by a motor, and the output, the coupler angle or the coupler point is used.

The [Grübler formula](/grubler-formula/) for planar chains with $n$ links and $j_1$ joints of one degree of freedom gives $M = 3(n - 1) - 2j_1 = 3 \cdot 3 - 2 \cdot 4 = 1$. The four-bar has this mobility for all link lengths that allow it to be assembled, so it is not one of the exceptions of the count that the page on [degrees of freedom analysis](/degrees-of-freedom-analysis/) lists.

A step of the model is one input angle. The model answers the questions: can the linkage be assembled at this angle, what are the other angles and their rates, and where is the coupler point.

## What it counts

A mechanism model counts no cost. This section gives the parameters, the configuration space and the motions that the model can describe.

### Parameters and configuration space

The shape of the linkage is fixed by the four lengths, and since a scaled linkage moves in the same way, by three ratios such as $K_1 = d/a$, $K_2 = d/c$ and $K_3 = (a^2 - b^2 + c^2 + d^2)/(2ac)$ of the [Freudenstein equation](/freudenstein-equation/). A coupler point adds $p$ and $\delta$. So a function generator has 3 shape parameters, a path generator 5 (plus the place and the angle of the ground in the plane, 3 more), and a motion generator the same.

The linkage can be assembled at all only when the longest link is at most the sum of the other three, $2l \le a + b + c + d$. The configuration space is the set

$$C = \{(\theta_2, \theta_3, \theta_4) \in T^3 : a e^{i\theta_2} + b e^{i\theta_3} - c e^{i\theta_4} = d\},$$

a closed subset of the 3-torus. These facts describe it:

1. *For each $\theta_2$ there are 0, 1 or 2 points of $C$*, which are the open and crossed assemblies. The half-angle substitution turns the loop into a quadratic whose roots are these points, as proved on the [vector loop closure](/vector-loop-closure/) page.
2. *$C$ is a smooth closed curve, except at a configuration with all four links on one line.* The loop is two real equations in three angles. Its Jacobian has the columns $i a e^{i\theta_2}$, $i b e^{i\theta_3}$ and $-i c e^{i\theta_4}$, seen as vectors in the plane. These columns span the plane unless all three are parallel, and then the loop puts $d$ on the same line. Where the rank is 2, the implicit function theorem makes $C$ a smooth curve, and $C$ is compact, so it is a union of disjoint circles.
3. *A configuration with all links on one line exists exactly when the four lengths split into two groups with equal sums.* With $s \le p \le q \le l$, this means $s + l = p + q$ (a change point) or $l = s + p + q$ (the linkage can only be assembled flat).
4. *When no configuration has all links on one line, the circles of $C$ are the circuits: two when $s + l < p + q$, one when $s + l > p + q$.* A circuit is a set of configurations that the linkage can reach without being taken apart (Norton, Section 4.13). The proof follows.

For item 4, look at the triangle $A O_4 B$. An assembly at $\theta_2$ exists exactly when the diagonal $\delta = |A - O_4|$, with $\delta^2 = a^2 + d^2 - 2ad\cos\theta_2$, lies in $[|b - c|, b + c]$, and there are two assemblies when $\delta$ is strictly inside and one (a toggle) at an end. Since $\delta$ grows with $\theta_2$ on $[0, \pi]$ and is even in $\theta_2$, the feasible input angles are the whole circle when both $\theta_2 = 0$ and $\theta_2 = \pi$ are feasible, one arc when exactly one of them is, and two mirror arcs when neither is. On the whole circle the two assemblies never meet, so $C$ is two circles. On an arc they meet at the two ends, so each arc gives one circle. It remains to see which case occurs. Write $x \ge y$ for $a, d$ and $u \ge w$ for $b, c$. Then $\theta_2 = 0$ is feasible iff $x + w \ge y + u$, and $\theta_2 = \pi$ is feasible iff $u + w \ge x + y$. Each is a comparison of the two sums of a split of the four lengths into two pairs. A split that puts $l$ with $p$ or $q$ always has the pair with $l$ at least as large, so only the split $\{s, l\}$ against $\{p, q\}$ depends on the lengths. If $l = x$ and $s = y$, then $\theta_2 = 0$ is always feasible and $\theta_2 = \pi$ is feasible iff $s + l \le p + q$. If $l = x$ and $s = w$, then $\theta_2 = \pi$ is feasible only when $s + l = p + q$, and $\theta_2 = 0$ iff $s + l \ge p + q$. The cases $l = u$ are the same with $0$ and $\pi$ exchanged. So for $s + l > p + q$ exactly one of the two angles is feasible, one arc and one circuit. For $s + l < p + q$ either both are (the input turns fully) or neither is, and there are two circuits. $\blacksquare$

A branch is one of the two assemblies taken along an arc of $\theta_2$ between two toggles. On a crank-rocker the open and the crossed branches are also the two circuits. On a triple-rocker they are the two halves of the one circuit.

### What it can do

The [Grashof condition](/grashof-condition/) says which links can turn fully. With $s$ the shortest link, the classes for $s + l < p + q$ are:

| shortest link | name | input $a$ | output $c$ |
|---|---|---|---|
| ground $d$ | double-crank (drag link) | turns fully | turns fully |
| input $a$ | crank-rocker | turns fully | rocks |
| output $c$ | rocker-crank | rocks | turns fully |
| coupler $b$ | Grashof double-rocker | rocks | rocks |

With $s + l > p + q$ every joint to the ground rocks and the linkage is a triple-rocker. With $s + l = p + q$ it is a change point linkage. The four rows are the four inversions of one Grashof chain: the same links with a different link fixed.

**A crank-rocker.** Take $a = 2$, $b = 7$, $c = 5$, $d = 6$, so $s + l = 2 + 7 \le 5 + 6$ with the input shortest. On the open circuit the output rocks between two positions in which the crank and the coupler are in line. In the extended position $|O_2B| = a + b = 9$, so $B = (23/3, 10\sqrt2/3)$, $\cos\theta_4 = 1/3$, $\theta_4 = 70.53°$, and $\theta_2 = 31.59°$. In the folded position $|O_2B| = b - a = 5$, so $B = (3, 4)$, $\theta_4 = 126.87°$, and $\theta_2 = 233.13°$. The output swing is $56.34°$. The crank turns $201.54°$ for the forward stroke and $158.46°$ for the return, so with a constant crank speed the return is faster by the time ratio $201.54/158.46 = 1.27$. This is a quick-return mechanism.

The tasks of [kinematic synthesis](/kinematic-synthesis/) are those that a four-bar can do:

- [function generation](/function-generation/): the output angle follows a given function of the input angle, exactly at a few precision points;
- [path generation](/path-generation/): a coupler point follows a given path. The paths that a four-bar can trace are its [coupler curves](/coupler-curve/), algebraic curves of degree 6;
- [motion generation](/motion-generation/): the coupler takes given positions, which [Burmester theory](/burmester-theory/) solves for up to five positions.

A four-bar cannot draw an exact straight line; its straight-line linkages, such as those of Watt and Chebyshev, are approximations. The [Peaucellier-Lipkin linkage](/peaucellier-lipkin-linkage/) with more links draws an exact one.

## Relation to other models

- **Slider-crank.** Let the output length $c$ and the pivot $O_4$ go to infinity together so that $B$ stays at a finite place. Then $B$ moves on a straight line, the output joint becomes a slide, and the linkage becomes the [slider-crank mechanism](/slider-crank-mechanism/).
- **Six-bars.** Adding a dyad (two links and three joints) to a four-bar keeps one degree of freedom and gives the [Watt and Stephenson six-bars](/watt-and-stephenson-six-bar/), which can dwell or trace more general curves.
- **Cognates.** By the [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/), every coupler curve is traced by three different four-bars.
- **Spatial and spherical four-bars.** With all four joint axes through one point, the 4R chain moves on a sphere and has mobility 1. With skew axes the 4R chain is rigid by the spatial count $M = 6 \cdot 3 - 4 \cdot 5 = -2$, except for the Bennett linkage, which moves because of special link dimensions.
- **Open chains.** A serial 2R or 3R arm has no loop, so its positions come directly from [forward kinematics](/forward-kinematics/). The four-bar is a 3R arm whose end is pinned to the ground, and its loop closure is the extra condition.

## Known results in the model

- **Mobility.** $M = 1$ by the Grübler count, for every length vector that can be assembled.
- **Rotatability.** Some link turns fully relative to its neighbours exactly when $s + l \le p + q$, and then it is the shortest one: the [Grashof condition](/grashof-condition/), with the change point when equality holds.
- **Position.** Each input angle gives at most two assemblies, the roots of a quadratic in $\tan(\theta_4/2)$ ([vector loop closure](/vector-loop-closure/)). The input and output angles are related by the [Freudenstein equation](/freudenstein-equation/), which is linear in three length ratios.
- **Transmission.** The [transmission angle](/transmission-angle/) $\mu$ between coupler and output satisfies $\cos\mu = (b^2 + c^2 - a^2 - d^2 + 2ad\cos\theta_2)/(2bc)$, with its extremes at $\theta_2 = 0$ and $\theta_2 = \pi$. For the crank-rocker above, $\mu$ goes from $34.05°$ to $81.79°$.
- **Velocity.** Four links have $\binom{4}{2} = 6$ [instant centers](/instant-center-of-velocity/). Four of them are the pins, and the [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/) gives the other two: $I_{13}$ where the lines $O_2A$ and $O_4B$ meet, and $I_{24}$ where the lines $AB$ and $O_2O_4$ meet.
- **Coupler curves.** A coupler curve is an algebraic curve of degree 6 that passes three times through each of the two circular points at infinity (Hunt 1978, Chapter 7), and three four-bars trace it.
- **Synthesis.** Three precision points of function generation give a linear system ([Freudenstein equation](/freudenstein-equation/)). Five positions of motion generation give at most four dyads, which pair up into at most six four-bars ([Burmester theory](/burmester-theory/)). Nine points of path generation give a finite number of solutions found with polynomial continuation ([nine-point path synthesis](/nine-point-path-synthesis/)).

## References
