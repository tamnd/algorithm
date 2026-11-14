---
tag: 5CYJ3W
kind: definition
slug: transmission-angle
name: Transmission angle
aliases:
- linkage transmission angle
area: cad/mechanism-and-assembly-design
level: intro
summary: The angle between the coupler and the output link of a four-bar, a measure of how well force is passed on, kept within about 40 to 140 degrees.
prereqs: [four-bar-linkage]
see_also: [grashof-condition, vector-loop-closure, freudenstein-equation, cam-pressure-angle, instant-center-of-velocity, kinematic-synthesis, slider-crank-mechanism]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 4.11 (p. 208, transmission angles, with the extreme values on p. 209) and Section 4.12 (p. 211, toggle positions)
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: the chapter on the fundamentals of linkages, transmission angle and mechanical advantage
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the sections on the transmission angle in the chapters on linkages and on linkage design
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 2 (pp. 15 to 53), the planar 4R linkage
---

The transmission angle $\mu$ of a [four-bar linkage](/four-bar-linkage/) is the angle at the output pin between the coupler and the output link. When the joints have no friction and the links no mass, the coupler can push on the output only along its own line, and the part of that push that turns the output is proportional to $\sin\mu$. So $\mu$ near $90°$ means that the force goes into torque, and $\mu$ near $0°$ or $180°$ means that it goes into the bearings. It depends on the position, and for a full turn of a crank it is smallest when the crank lies along the ground toward the output pivot and largest when it points the other way.

This page is about the quality of the force path at each position. The [Grashof condition](/grashof-condition/) is about the same linkage as a whole, and says which joints can turn fully.

## Definition

Use the notation of the four-bar page: ground $d$ from $O_2 = (0, 0)$ to $O_4 = (d, 0)$, input $a$ from $O_2$ to $A$, coupler $b$ from $A$ to $B$, output $c$ from $O_4$ to $B$, and the input angle $\theta_2$ counterclockwise from the ground line. The **transmission angle** is the angle of the triangle $A B O_4$ at $B$:

$$\mu = \angle A B O_4 \in [0, \pi].$$

On the open branch with the crank above the ground, $\mu = \theta_4 - \theta_3$. Some texts, Norton among them, use the acute angle $\min(\mu, \pi - \mu)$ instead, since $\sin\mu$ is the same for both, and then ask for a large lower bound.

### The formula

**Claim.** In every assembly at the input angle $\theta_2$,

$$\cos\mu = \frac{b^2 + c^2 - a^2 - d^2 + 2ad\cos\theta_2}{2bc}.$$

*Proof.* Let $\delta = |A - O_4|$. The law of cosines in the triangle $O_2 A O_4$, whose angle at $O_2$ is $\theta_2$, gives $\delta^2 = a^2 + d^2 - 2ad\cos\theta_2$. The law of cosines in the triangle $A B O_4$, whose angle at $B$ is $\mu$, gives $\delta^2 = b^2 + c^2 - 2bc\cos\mu$. Set the two equal and solve for $\cos\mu$. $\blacksquare$

The two assemblies at one $\theta_2$ are mirror images in the line $AO_4$, so they have the same $\mu$. The formula needs only the lengths and $\theta_2$, not the position solution.

### Extreme values over a crank revolution

**Claim.** If the input turns fully, $\mu$ takes its smallest value at $\theta_2 = 0$ and its largest at $\theta_2 = \pi$:

$$\mu_{\min} = \arccos\frac{b^2 + c^2 - (d - a)^2}{2bc}, \qquad \mu_{\max} = \arccos\frac{b^2 + c^2 - (d + a)^2}{2bc}.$$

*Proof.* In the formula, $\cos\mu$ is an increasing affine function of $\cos\theta_2$, because the coefficient $2ad/(2bc)$ is positive. Since $\arccos$ is decreasing, $\mu$ is a decreasing function of $\cos\theta_2$. As $\theta_2$ runs over a full turn, $\cos\theta_2$ takes all values in $[-1, 1]$, with $1$ at $\theta_2 = 0$ and $-1$ at $\theta_2 = \pi$. Put $\cos\theta_2 = \pm 1$ in the formula: $a^2 + d^2 \mp 2ad = (d \mp a)^2$. $\blacksquare$

If the input only rocks, its range ends where $\delta = b + c$ or $\delta = |b - c|$, that is where $\mu = \pi$ or $\mu = 0$. These are the toggle positions, at which the coupler and the output are in line. There the output cannot be driven through the coupler, and the velocity equations of the [vector loop closure](/vector-loop-closure/) page are singular.

### Why sin μ measures the force path

Assume no friction, no mass and no outside load on the coupler. Then the coupler is a two-force member: the forces on it at $A$ and $B$ are equal, opposite and along the line $AB$. At $B$ it pushes on the output with a force $F$ along $AB$. Split $F$ into a part along $O_4B$, which only loads the bearing at $O_4$, and a part perpendicular to $O_4B$, which gives the torque $T_4 = F c\sin\mu$ about $O_4$. So for a given coupler force the output torque is largest at $\mu = 90°$ and zero at $\mu = 0$ or $\pi$. The angle between the force and the velocity of $B$, which is perpendicular to $O_4B$, is $|90° - \mu|$. This is the pressure angle at $B$, the same quantity that the [cam pressure angle](/cam-pressure-angle/) measures for a cam.

### A rule of thumb, not a theorem

Designers try to keep $\mu$ between about $40°$ and $140°$, or in the acute convention $\mu \ge 40°$, over the working range. This is a rule of thumb from practice, not a theorem. The real limit depends on friction, on the speed, on the stiffness of the links and on the play in the joints. No proof shows that a linkage with $\mu_{\min} = 39°$ fails or that one with $41°$ works.

## Examples and non-examples

**A crank-rocker below the rule.** For $a = 2$, $b = 7$, $c = 5$, $d = 6$, the extremes are $\cos\mu_{\min} = (49 + 25 - 16)/70 = 29/35$ and $\cos\mu_{\max} = (49 + 25 - 64)/70 = 1/7$, so $\mu$ runs from $34.05°$ to $81.79°$:

| $\theta_2$ | $0°$ | $60°$ | $90°$ | $120°$ | $180°$ |
|---|---|---|---|---|---|
| $\mu$ | $34.05°$ | $48.92°$ | $60.94°$ | $71.68°$ | $81.79°$ |

The crank turns fully, but near $\theta_2 = 0$ the transmission angle is below $40°$. By the rule of thumb this linkage should not drive a large load near that position.

**A crank-rocker that meets the rule.** For $a = 1$, $b = 4$, $c = 3$, $d = 4$, the input is the shortest link and $1 + 4 < 3 + 4$, so it is a crank-rocker. At $\theta_2 = 0$, $\delta = 3$ and $\cos\mu_{\min} = (16 + 9 - 9)/24 = 2/3$, so $\mu_{\min} = 48.19°$. At $\theta_2 = \pi$, $\delta = 5$, the triangle $A B O_4$ has sides $4, 3, 5$, and $\mu_{\max} = 90°$ exactly.

**A triple-rocker at its limits.** For $a = 3$, $b = 4$, $c = 5$, $d = 7$, $s + l = 10 > 9$, so the input rocks. The diagonal $\delta$ can take values in $[|a - d|, a + d] = [4, 10]$ from the input side and in $[|b - c|, b + c] = [1, 9]$ from the output side, so it moves in $[4, 9]$. Both ends of the input range have $\delta = 9$, at $\cos\theta_2 = (9 + 49 - 81)/42 = -23/42$, that is $\theta_2 = \pm 123.2°$, and there $\mu = 180°$. The linkage cannot be driven from the input through these positions.

**Non-example: the angle at the crank pin.** The angle between the input and the coupler at $A$ is not the transmission angle. It matters when the output drives the input, as in a linkage driven backward. Then the roles of the links swap, and the transmission angle is measured at $A$.

**Non-example: a slider-crank.** For the [slider-crank mechanism](/slider-crank-mechanism/) there is no output pivot. The force path is measured by the angle between the rod and the normal to the guide, which is $90°$ minus the rod angle $|\theta_3|$ in the notation of that page.

## Related definitions

- [Four-bar linkage](/four-bar-linkage/): the mechanism and its notation.
- [Grashof condition](/grashof-condition/): which joints turn fully, so for which linkages the extreme values above are over a full turn.
- [Vector loop closure](/vector-loop-closure/): the position solution, in which $\mu = 0$ or $\pi$ is a toggle position.
- [Instant center of velocity](/instant-center-of-velocity/): the instant centers give the velocity ratio and the mechanical advantage, which depends on $\mu$ through $\sin\mu$.
- [Cam pressure angle](/cam-pressure-angle/): the same measure for a cam and its follower.
- [Kinematic synthesis](/kinematic-synthesis/) and the [Freudenstein equation](/freudenstein-equation/): synthesis methods whose results are checked against a bound on $\mu$.

## References
