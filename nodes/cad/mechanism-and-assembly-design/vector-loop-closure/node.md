---
tag: V3P14V
kind: technique
slug: vector-loop-closure
name: Vector loop closure equation
aliases:
- loop closure equation
- Raven's method
area: cad/mechanism-and-assembly-design
level: core
summary: Writes a closed linkage as a sum of link vectors equal to zero, solves the scalar equations for the unknown angles, and differentiates them for velocities.
prereqs: [four-bar-linkage, kinematic-chain]
see_also: [freudenstein-equation, slider-crank-mechanism, grashof-condition, transmission-angle, newton-method-for-systems, forward-kinematics, quadratic-formula, degrees-of-freedom-analysis]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Sections 4.5 (p. 187, the vector loop equation for a fourbar on p. 189), 4.6 and 4.7 (pp. 196 to 198, crank-slider), 4.12 (p. 211, toggle positions), 4.13 (p. 212, circuits and branches), 4.14 (p. 214, Newton-Raphson) and 6.7 (p. 321, analytical velocity solutions)
  - paper: doi:10.1115/1.4011678
    title: Francis H. Raven, Velocity and acceleration analysis of plane and space mechanisms by means of independent-position equations, Journal of Applied Mechanics 25(1), 1958, 1 to 6
    locator: the position equations of a closed loop and their first and second time derivatives
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: the chapters on displacement and velocity analysis of planar linkages
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: the chapters on position and velocity analysis (loop closure equations)
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 2 (pp. 15 to 53), analysis of planar linkages
---

The vector loop closure equation describes a closed [kinematic chain](/kinematic-chain/) as a cycle of link vectors whose sum is zero. Each link is a vector of fixed length and unknown angle, so the loop gives two scalar equations per planar loop, and these fix as many unknown angles as there are equations once the input angles are given. Its time derivatives are linear in the velocities and the accelerations, so after the position step the rest of the analysis is linear algebra. Raven proposed this way of writing the analysis in 1958, and it is the standard first step of position analysis in the textbooks.

This page uses the notation of the [four-bar linkage](/four-bar-linkage/): the ground $d$ runs from $O_2 = (0, 0)$ to $O_4 = (d, 0)$, the input (crank) $a$ runs from $O_2$ to the pin $A$, the coupler $b$ runs from $A$ to the pin $B$, and the output $c$ runs from $O_4$ to $B$. The angles $\theta_2, \theta_3, \theta_4$ of $a$, $b$, $c$ are measured counterclockwise from the ground line. With complex numbers for plane vectors, the loop is

$$a e^{i\theta_2} + b e^{i\theta_3} - c e^{i\theta_4} - d = 0.$$

## In plain words

Walk around a closed linkage from one fixed pivot, along each link in turn, and you come back to where you started. So the arrows of the links add up to nothing. Each arrow has a known length and an unknown direction. Split the sum into its sideways part and its up-and-down part, and you get two equations for each closed loop.

If you know the angle of the input link, you can solve these equations for the other angles. A loop of four bars usually gives two answers, because the linkage can be put together in two mirror-image ways. To get speeds, take the rate of change of the same equations. The unknown speeds then appear in a simple linear system, which has no answer only when two links are in line.

## When it applies

- The mechanism is a closed chain of rigid links with lower pairs (pins and slides), and you know its input angles or input slide positions. Count the inputs with the [Grübler formula](/grubler-formula/), which says how many are needed. The page on [degrees of freedom analysis](/degrees-of-freedom-analysis/) gives the count and its exceptions.
- The question is about position, velocity or acceleration: where is each link, how fast does it turn, and where does a point on the coupler go.
- The number of independent loops is $L = j - n + 1$ for $n$ links and $j$ joints. A four-bar or a slider-crank has one loop and two scalar equations. A six-bar has two loops and four equations.
- An open chain, such as a serial robot arm, has no loop. Its positions come from [forward kinematics](/forward-kinematics/), a product of link transforms, and need no equation solving. Loop closure is the step that makes a chain with a cycle harder than an open one.

## The template

The holes of the template are the loop (which vectors, which unknowns), the elimination that leaves one unknown, and the rule that names the branch. The block below fills them for the four-bar. The [slider-crank mechanism](/slider-crank-mechanism/) fills them in the same way with $x$ as one unknown.

```pseudo id=main
FOURBAR-POSITIONS(a, b, c, d, θ2)
L1  K1 ← d/a;  K2 ← d/c;  K3 ← (a² − b² + c² + d²)/(2ac)          ▷ hole 1: the loop
L2  A ← cos θ2 − K1 − K2 cos θ2 + K3;  B ← −2 sin θ2;  C ← K1 − (K2 + 1) cos θ2 + K3
L3  Δ ← B² − 4AC                                                   ▷ hole 2: eliminate θ3
L4  if Δ < 0 then return ∅                                         ▷ the loop does not close at θ2
L5  for each root t of A t² + B t + C = 0, with t = ∞ when A = 0:
L6      θ4 ← 2 arctan t;  θ3 ← atan2(c sin θ4 − a sin θ2, d + c cos θ4 − a cos θ2)
L7      σ ← +1 if B is left of the directed line from A to O4, else −1   ▷ hole 3: the branch
L8  return the triples (θ3, θ4, σ), with σ = +1 first

FOURBAR-VELOCITIES(θ2, θ3, θ4, ω2)
L9  solve [−b sin θ3, c sin θ4; b cos θ3, −c cos θ4] (ω3, ω4) = (a ω2 sin θ2, −a ω2 cos θ2)
```

**Hole 1, the loop.** Split the loop equation into its real and imaginary parts:

$$a\cos\theta_2 + b\cos\theta_3 - c\cos\theta_4 - d = 0, \qquad a\sin\theta_2 + b\sin\theta_3 - c\sin\theta_4 = 0.$$

**Hole 2, the elimination.** Put the coupler terms alone on one side, $b\cos\theta_3 = c\cos\theta_4 + d - a\cos\theta_2$ and $b\sin\theta_3 = c\sin\theta_4 - a\sin\theta_2$, then square and add. The left side becomes $b^2$, and $\theta_3$ is gone:

$$b^2 = a^2 + c^2 + d^2 + 2cd\cos\theta_4 - 2ad\cos\theta_2 - 2ac\cos(\theta_2 - \theta_4).$$

Divide by $2ac$ to get the [Freudenstein equation](/freudenstein-equation/) $K_1\cos\theta_4 - K_2\cos\theta_2 + K_3 = \cos(\theta_2 - \theta_4)$ with the constants of line L1. Expand $\cos(\theta_2 - \theta_4)$ and collect the terms in $\theta_4$:

$$P\cos\theta_4 + Q\sin\theta_4 + R = 0, \quad P = K_1 - \cos\theta_2, \quad Q = -\sin\theta_2, \quad R = K_3 - K_2\cos\theta_2.$$

With $t = \tan(\theta_4/2)$, $\cos\theta_4 = (1 - t^2)/(1 + t^2)$ and $\sin\theta_4 = 2t/(1 + t^2)$. Multiply by $1 + t^2$ to get $(R - P)t^2 + 2Qt + (R + P) = 0$, which is the quadratic $At^2 + Bt + C = 0$ of line L2, with discriminant $\Delta = 4(P^2 + Q^2 - R^2)$.

**Hole 3, the branch.** Line L7 names each solution by the side of the diagonal $AO_4$ on which $B$ lies. When the crank is above the ground line, the solution with $\sigma = +1$ has $O_2$ and $B$ on opposite sides of $AO_4$, so the links do not cross. This is the open assembly. The solution with $\sigma = -1$ is the crossed assembly.

### Why the quadratic gives exactly the two assemblies

Fix $\theta_2$, and assume $a, b, c, d > 0$ and $A \ne O_4$.

1. *An assembly is the same as a solution $\theta_4$ of the Freudenstein equation.* The equation of hole 2 says $|c e^{i\theta_4} + d - a e^{i\theta_2}| = b$. Given a solution $\theta_4$, the vector $c e^{i\theta_4} + d - a e^{i\theta_2}$ has length $b > 0$, so it is $b e^{i\theta_3}$ for exactly one $\theta_3$ in $(-\pi, \pi]$, and this is the atan2 of line L6. The pair satisfies the loop. Conversely, every assembly gives a solution, as the derivation shows.
2. *The solutions $\theta_4$ match the roots $t$ one to one.* The map $\theta_4 \mapsto \tan(\theta_4/2)$ is a bijection from $(-\pi, \pi)$ onto the real line, and $\theta_4 = \pi$ is the root $t = \infty$. That value solves $P\cos\theta_4 + Q\sin\theta_4 + R = 0$ exactly when $R - P = 0$, that is when $A = 0$, and then the quadratic drops to degree one. So the solutions in $(-\pi, \pi]$ are the finite roots, plus $\theta_4 = \pi$ when $A = 0$.
3. *There are 0, 1 or 2 solutions, as $\Delta < 0$, $= 0$, $> 0$.* Since $A \ne O_4$, $(P, Q) \ne (0, 0)$, and the equation says that the unit vector $(\cos\theta_4, \sin\theta_4)$ lies on the line $Px + Qy + R = 0$. That line is at distance $|R|/\sqrt{P^2 + Q^2}$ from the origin, so it meets the unit circle twice, once or never as $P^2 + Q^2 - R^2$ is positive, zero or negative.
4. *The two assemblies are mirror images.* Each $B$ lies on the circle of radius $b$ about $A$ and on the circle of radius $c$ about $O_4$. Two circles with different centers meet in two points that are mirror images in the line of centers $AO_4$, or in one point on that line. So the two solutions have opposite $\sigma$, and $\Delta = 0$ exactly when $B$ is on the line $AO_4$, which means that the coupler and the output are in line. That is a toggle position.
5. *The branch does not change between toggles.* As $\theta_2$ moves, the roots move continuously. The sign $\sigma$ of a root can change only when $B$ crosses the line $AO_4$, and by step 4 that happens only at a toggle. So on an interval of $\theta_2$ without a toggle, following one root keeps one value of $\sigma$. $\blacksquare$

When $A = O_4$, which needs $a = d$ and $\theta_2 = 0$, the equation is $R = 0$: if $b = c$ every $\theta_4$ is an assembly and the output turns freely, and otherwise there is none.

### Velocity

Take the time derivative of the loop with $\omega_k = \dot\theta_k$: $i a\omega_2 e^{i\theta_2} + i b\omega_3 e^{i\theta_3} - i c\omega_4 e^{i\theta_4} = 0$. Its real and imaginary parts are the system of line L9. The determinant is $bc\sin(\theta_3 - \theta_4)$, and Cramer's rule gives

$$\omega_3 = \frac{a\omega_2\sin(\theta_4 - \theta_2)}{b\sin(\theta_3 - \theta_4)}, \qquad \omega_4 = \frac{a\omega_2\sin(\theta_2 - \theta_3)}{c\sin(\theta_4 - \theta_3)}.$$

The system has no unique solution exactly at a toggle, the case $\Delta = 0$ of step 4. A second derivative gives the accelerations from a system with the same matrix and a new right side.

### Cost and accuracy

One position solve is a fixed number of operations, and so is each velocity solve. The quadratic should be solved in the stable form $q = -\tfrac12(B + \operatorname{sign}(B)\sqrt\Delta)$, $t_1 = q/A$, $t_2 = C/q$, as on the [quadratic formula](/quadratic-formula/) page. The implementation keeps the roots as angles, $\theta_4/2 = \operatorname{atan2}(q, A)$ and $\operatorname{atan2}(C, q)$, so that $A = 0$ needs no special case. Near a toggle the two roots meet and the position is ill-conditioned: a small change of a length moves $\theta_4$ by about the square root of that change.

## Classic examples

**A crank-rocker, both branches.** Take $a = 2$, $b = 7$, $c = 5$, $d = 6$, a crank-rocker by the [Grashof condition](/grashof-condition/). Then $K_1 = 3$, $K_2 = 6/5$, $K_3 = 4/5$. At $\theta_2 = 0$, $A = -12/5$, $B = 0$, $C = 8/5$, so $t^2 = 2/3$, $\cos\theta_4 = 1/5$, and the open assembly has $B = (7, 2\sqrt6)$ and $\theta_4 = 78.463°$. At $\theta_2 = 180°$, $A = -2$, $B = 0$, $C = 6$, so $t = \pm\sqrt3$ and $\theta_4 = \pm 120°$ exactly. In between ($\omega_2 = 1$ rad/s):

| $\theta_2$ | $A$ | $B$ | $C$ | open $\theta_3$, $\theta_4$ | $\omega_3$, $\omega_4$ (open) | crossed $\theta_3$, $\theta_4$ |
|---|---|---|---|---|---|---|
| 0° | −2.4 | 0 | 1.6 | 44.415°, 78.463° | −0.5, −0.5 | 315.585°, 281.537° |
| 60° | −2.3 | −1.732 | 2.7 | 26.311°, 75.229° | −0.0996, 0.2944 | 295.476°, 246.558° |
| 90° | −2.2 | −2 | 3.8 | 25.278°, 86.219° | 0.0216, 0.4138 | 297.852°, 236.911° |
| 120° | −2.1 | −1.732 | 4.9 | 27.268°, 98.950° | 0.1081, 0.4209 | 304.936°, 233.254° |
| 180° | −2 | 0 | 6 | 38.213°, 120° | 0.25, 0.25 | 321.787°, 240° |

At $\theta_2 = 90°$, $\Delta = 37.44$ and the roots are $t = 0.936$ (open) and $t = -1.845$ (crossed). The angle between coupler and output is the [transmission angle](/transmission-angle/), $\theta_4 - \theta_3$ on the open branch, here from 34.05° at $\theta_2 = 0$ to 81.79° at $\theta_2 = 180°$. The tests of this page check these values, a residual of the loop below $10^{-9}$ on thousands of random linkages, and the velocities against finite differences.

**The slider-crank.** For the [slider-crank mechanism](/slider-crank-mechanism/) with offset $e$, the slider pin is $B = (x, e)$ and the loop is $a e^{i\theta_2} + b e^{i\theta_3} - x - ie = 0$. The imaginary part gives $\sin\theta_3 = (e - a\sin\theta_2)/b$ directly, so no half-angle step is needed, and $x = a\cos\theta_2 \pm \sqrt{b^2 - (e - a\sin\theta_2)^2}$. The two signs are the two branches, with the slider on either side of the crank pin. The velocity is $\omega_3 = -a\omega_2\cos\theta_2/(b\cos\theta_3)$ and $\dot x = -a\omega_2\sin\theta_2 - b\omega_3\sin\theta_3$.

**Function generation.** The elimination of hole 2, read the other way, is the [Freudenstein equation](/freudenstein-equation/). There the angles are given and the lengths are unknown, and the equation is linear in $K_1, K_2, K_3$.

**The Grashof class by a sweep.** Sweep $\theta_2$ over a full turn and test $\Delta \ge 0$ at each step. The input turns fully exactly when the loop closes for every $\theta_2$. The tests check this sweep against the inequality of the [Grashof condition](/grashof-condition/) for every joint of 500 random integer linkages.

**Six-bars.** A [Watt or Stephenson six-bar](/watt-and-stephenson-six-bar/) has two independent loops. Choose them so that one loop holds the input and only one other unknown pair, solve that loop as a four-bar, and then solve the second loop with the now known angles. Where no such order exists, solve the four scalar equations together with [Newton's method for systems](/newton-method-for-systems/).

**A planar two-link arm.** The [inverse kinematics](/inverse-kinematics/) of a planar 2R arm is the loop closure of the triangle made by the two links and the line to the target. The elbow-up and elbow-down solutions are its two branches.

## Variations

- **Vector components instead of complex numbers.** The same equations follow from $\sum r_k(\cos\theta_k, \sin\theta_k) = 0$. The complex form makes the derivatives short, since $\frac{d}{dt}e^{i\theta} = i\omega e^{i\theta}$.
- **Other unknowns.** The unknowns can be any two of the angles and slide lengths of a loop. An inverted slider-crank has a slide of variable length along a link that turns, and the loop is solved for that length and an angle in the same way.
- **Numerical solution.** For many loops, or for spatial loops, write the loop as the product of $4 \times 4$ link transforms equal to the identity and solve with Newton's method from the last position, as Norton (Section 4.14) and Raven (1958) do. This gives only the branch near the start point. All branches need [homotopy continuation](/homotopy-continuation/) or elimination with a [resultant](/resultant/).
- **Points on a link.** After the angles are known, a coupler point is $a e^{i\theta_2} + p e^{i(\theta_3 + \delta)}$ for its distance $p$ and angle $\delta$ from $A$. The set of these points is the [coupler curve](/coupler-curve/).

## Pitfalls

- **arctan instead of atan2.** $\theta_3 = \arctan\big((c\sin\theta_4 - a\sin\theta_2)/(d + c\cos\theta_4 - a\cos\theta_2)\big)$ loses the quadrant, and the wrong value still looks reasonable. Use atan2 with the two parts, as in line L6.
- **Branch jumps in a sweep.** Two roots taken in a fixed order (first the minus sign, then the plus sign) can swap when $A$ changes sign, and an animation then jumps from one assembly to the other. Name each root by $\sigma$ as in line L7, or follow the root that is nearest to the last position.
- **Division by A.** The textbook form $t = (-B \pm \sqrt\Delta)/(2A)$ fails when $A = 0$ ($\theta_4 = \pi$) and loses digits when $|A|$ is small. Use the stable form or the angle form above.
- **Toggle positions.** At $\Delta = 0$ the velocity system is singular. Code that divides by $\sin(\theta_3 - \theta_4)$ there returns a huge number. The implementation raises an error instead.
- **A small residual is not a good answer.** Near a toggle many angles give a small residual. Check $\Delta$ against a tolerance relative to the size of $A$, $B$ and $C$, as line L4 does, and report the toggle.

## Exercises

1. For $a = 2$, $b = 7$, $c = 5$, $d = 6$, show that $\theta_2 = 180°$ gives $\theta_4 = 120°$ exactly, and find the coupler point $B$.
2. Derive the half-angle quadratic for $\theta_3$ instead of $\theta_4$. Which constants take the place of $K_1, K_2, K_3$?
3. Show that the slider-crank with offset $e$ can be assembled at every $\theta_2$ exactly when $b \ge a + |e|$.
4. Differentiate the velocity equations once more and write the $2 \times 2$ system for $\alpha_3$ and $\alpha_4$. Show that its matrix is the matrix of line L9.
5. For $a = 2$, $b = 4$, $c = 4$, $d = 6$ at $\theta_2 = 180°$, show that $\Delta = 0$ and that all four links are in line. Which theorem explains this linkage?

## References
