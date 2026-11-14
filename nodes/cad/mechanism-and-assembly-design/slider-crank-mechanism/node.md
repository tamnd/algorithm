---
tag: Z9N6MV
kind: model
slug: slider-crank-mechanism
name: Slider-crank mechanism
aliases:
- crank-slider mechanism
- RRRP linkage
area: cad/mechanism-and-assembly-design
level: intro
summary: A four-bar chain with one prismatic joint that turns rotation into straight line motion, as in engines and pumps, with a closed-form position solution.
prereqs: [kinematic-chain, kinematic-pair]
see_also: [four-bar-linkage, vector-loop-closure, grashof-condition, instant-center-of-velocity, grubler-formula, degrees-of-freedom-analysis, freudenstein-equation, transmission-angle]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Sections 2.12 (p. 53, inversions of the slider-crank chain), 4.6 and 4.7 (pp. 196 to 198, position of the crank-slider), 4.8 (p. 201, the inverted crank-slider) and 6.7 (p. 321, velocity)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: Chapter 1 (mobility, inversion of the slider-crank chain) and the chapters on position and velocity analysis
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: the chapters on the fundamentals of linkages and on displacement analysis
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 2 (pp. 15 to 53), the planar RRRP linkage
---

The slider-crank mechanism is a closed chain of four links with three revolute joints and one prismatic joint: a crank turns about a fixed pivot, a connecting rod joins the crank to a slider, and the slider moves along a straight guide. It turns a full rotation into a straight back-and-forth motion, or the reverse, as in piston engines, compressors and pumps. It has one degree of freedom and a position solution in closed form, with no half-angle step.

This page is of kind model, and its standard sections hold the parts of a mechanism model: the mechanism (under The machine), its parameters and configuration space (under What it counts), what it can do (under Relation to other models), and the known results.

## The machine

### The mechanism

The crank $a$ runs from the fixed pivot $O_2 = (0, 0)$ to the crank pin $A = a e^{i\theta_2}$. The connecting rod $b$ runs from $A$ to the slider pin $B = (x, e)$. The slider moves on the line $y = e$, parallel to the $x$ axis, and $e$ is the offset: $e = 0$ is the in-line slider-crank. Angles are counterclockwise from the $x$ axis, as on the [four-bar linkage](/four-bar-linkage/) page. The loop equation is

$$a e^{i\theta_2} + b e^{i\theta_3} - x - ie = 0.$$

The ground, the crank, the rod and the slider are four links. The joints at $O_2$, $A$ and $B$ are revolute and the joint between the slider and the guide is prismatic, each a [kinematic pair](/kinematic-pair/) with one degree of freedom, so the chain is written RRRP. The [Grübler formula](/grubler-formula/) gives $M = 3(4 - 1) - 2 \cdot 4 = 1$.

A step of the model is one crank angle $\theta_2$, or one slider position $x$ when the slider drives, as in an engine.

## What it counts

A mechanism model counts no cost. This section gives the parameters, the configuration space and the motions that the model can describe.

### Parameters and configuration space

The parameters are $a$, $b$ and $e$, so two ratios up to scale, $b/a$ and $e/a$. A point on the rod adds two more for path generation.

The imaginary part of the loop gives $b\sin\theta_3 = e - a\sin\theta_2$, and the real part gives $x = a\cos\theta_2 + b\cos\theta_3$. So

$$x = a\cos\theta_2 + \sigma\sqrt{b^2 - (e - a\sin\theta_2)^2}, \qquad \sigma = \pm 1.$$

The branch $\sigma = +1$ has the slider to the right of the crank pin, $\cos\theta_3 > 0$, and $\sigma = -1$ to the left. The two branches meet only where the root is zero, which is where the rod is perpendicular to the guide.

**Full rotation.** The crank turns fully exactly when $b \ge a + |e|$. *Proof.* The linkage can be assembled at $\theta_2$ exactly when $|e - a\sin\theta_2| \le b$. As $\theta_2$ runs over a full turn, $e - a\sin\theta_2$ takes all values in $[e - a, e + a]$, and the largest absolute value is $a + |e|$. So every $\theta_2$ is feasible iff $a + |e| \le b$. $\blacksquare$

When $b > a + |e|$ the root is never zero, the branches never meet, and the configuration space is two circles, one for each side. When $b = a + |e|$ the two circles touch at one configuration with the rod perpendicular to the guide, the analogue of a change point. When $b < a + |e|$ the crank rocks.

**Stroke.** Assume $b > a + |e|$ and the branch $\sigma = +1$. The time derivative of the loop gives $\omega_3 = -a\omega_2\cos\theta_2/(b\cos\theta_3)$ and

$$\dot x = -a\omega_2\frac{\sin(\theta_2 - \theta_3)}{\cos\theta_3}.$$

So $\dot x = 0$ exactly when the crank and the rod are in line, $\theta_2 = \theta_3$ or $\theta_2 = \theta_3 + \pi$. In the first case $B = (a + b)e^{i\theta_3}$ and in the second $B = (b - a)e^{i\theta_3}$. On this branch $\cos\theta_3 > 0$, so each case is one configuration, with $x = \sqrt{(a + b)^2 - e^2}$ and $x = \sqrt{(b - a)^2 - e^2}$. These are the only two critical points of $x$ on the circle, so they are its maximum and minimum, and the stroke is

$$x_{\max} - x_{\min} = \sqrt{(a + b)^2 - e^2} - \sqrt{(b - a)^2 - e^2}.$$

For $e = 0$ it is exactly $2a$. For $e \ne 0$ it is larger than $2a$.

**Quick return.** The crank angles of the two dead positions are $\theta_2 = \arcsin(e/(a + b))$ (extended) and $\theta_2 = \pi + \arcsin(e/(b - a))$ (folded). For $e > 0$ the crank turns $\pi + \arcsin(e/(b - a)) - \arcsin(e/(a + b))$, more than $\pi$, from the extended to the folded position, and the rest of the turn back. With a constant crank speed the two strokes take different times. For $e = 0$ both angles are $\pi$ and the ratio is 1.

**A worked example.** Take $a = 2$, $b = 7$, $e = 1$. Then $b \ge a + |e|$, so the crank turns fully. The stroke is $\sqrt{80} - \sqrt{24} = 8.9443 - 4.8990 = 4.0453$, slightly more than $2a = 4$. The extended position is at $\theta_2 = \arcsin(1/9) = 6.379°$ and the folded one at $\theta_2 = 180° + \arcsin(1/5) = 191.537°$. The crank turns $185.158°$ while the slider moves in from $x = 8.9443$ to $x = 4.8990$ and $174.842°$ while it moves out, a time ratio of $1.059$. The tests on the [vector loop closure](/vector-loop-closure/) page check the full-rotation condition and the stroke formula against a sweep of $\theta_2$.

### What it can do

- **Rotation to translation.** With the crank as input, the slider gives a reciprocating motion. In-line, the motion is symmetric. Offset, the two strokes take different crank angles, which gives a mild quick return.
- **Translation to rotation.** With the slider as input (the piston of an engine), the crank turns, but at the two dead positions, where the crank and the rod are in line, the force of the slider gives no torque. A flywheel carries the crank through them.
- **Near-harmonic motion.** For the in-line case, $x = a\cos\theta_2 + \sqrt{b^2 - a^2\sin^2\theta_2}$. Expanding the root to first order in $(a/b)^2$ gives the approximation $x \approx b - \frac{a^2}{4b} + a\cos\theta_2 + \frac{a^2}{4b}\cos 2\theta_2$, used in engine dynamics. It is an approximation, with an error of order $a^4/b^3$.

## Relation to other models

- **A limit of the four-bar.** Take a [four-bar linkage](/four-bar-linkage/) and let the output length $c$ and its pivot $O_4$ go to infinity in the direction perpendicular to the guide, with $B$ fixed. The arc of $B$ becomes the straight guide, and the output joint becomes the prismatic joint. The [Grashof condition](/grashof-condition/) for the four-bar becomes $b \ge a + |e|$ in this limit.
- **Inversions.** Fixing a different link of the same chain gives the four inversions: the ground fixed (engines and compressors), the crank fixed (the Whitworth quick-return mechanism and the rotary engine), the rod fixed (the oscillating cylinder engine and the crank and slotted lever), and the slider fixed (the hand pump). In the inverted slider-crank, the slide moves along a link that turns, and the [vector loop closure](/vector-loop-closure/) is solved for the slide length and an angle.
- **The Scotch yoke.** If the rod is replaced by a slot perpendicular to the guide, the output is exactly harmonic, $x = a\cos\theta_2$. That chain has two prismatic joints, so it is a different chain.
- **Mobility exceptions.** The slider-crank has the mobility of its Grübler count for all lengths. The page on [degrees of freedom analysis](/degrees-of-freedom-analysis/) gives the count and the linkages for which it fails.

## Known results in the model

- **Mobility.** $M = 1$ by the Grübler count.
- **Position.** Each crank angle gives at most two assemblies, $x = a\cos\theta_2 \pm \sqrt{b^2 - (e - a\sin\theta_2)^2}$, from the loop equation of the [vector loop closure](/vector-loop-closure/) page.
- **Rotatability.** The crank turns fully exactly when $b \ge a + |e|$, as proved above.
- **Stroke and quick return.** The stroke is $\sqrt{(a + b)^2 - e^2} - \sqrt{(b - a)^2 - e^2}$, equal to $2a$ in-line, and the two dead positions are at $\arcsin(e/(a + b))$ and $\pi + \arcsin(e/(b - a))$.
- **Velocity.** $\dot x = -a\omega_2\sin(\theta_2 - \theta_3)/\cos\theta_3$. The [instant center](/instant-center-of-velocity/) of the slider and the ground is the point at infinity in the direction perpendicular to the guide, and the [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/) gives the other centers.
- **Function generation.** The relation between $\theta_2$ and $x$ is, like the [Freudenstein equation](/freudenstein-equation/), linear in suitable combinations of the lengths: $2ax\cos\theta_2 + 2ae\sin\theta_2 - (a^2 - b^2 + e^2) = x^2$. Three pairs $(\theta_2, x)$ give a linear system in $2a$, $2ae$ and $a^2 - b^2 + e^2$.

## References
