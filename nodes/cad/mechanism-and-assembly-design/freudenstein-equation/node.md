---
tag: Z9SNZM
kind: technique
slug: freudenstein-equation
name: Freudenstein's equation
aliases:
- Freudenstein equation of the four-bar
area: cad/mechanism-and-assembly-design
level: core
summary: Relates the input and output angles of a four-bar by K1 cos(psi) - K2 cos(phi) + K3 = cos(phi - psi), linear in link ratios, for analysis and function generation.
prereqs: [vector-loop-closure, four-bar-linkage]
see_also: [function-generation, chebyshev-spacing, kinematic-synthesis, gaussian-elimination, optimization-based-linkage-synthesis, grashof-condition, burmester-theory, transmission-angle]
sources:
  - paper: "Ferdinand Freudenstein, An analytical approach to the design of four-link mechanisms, Transactions of the ASME 76(3), 1954, 483 to 492"
    locator: the displacement equation of the four-bar in link ratios and its use for design
  - paper: "Ferdinand Freudenstein, Approximate synthesis of four-bar linkages, Transactions of the ASME 77(8), 1955, 853 to 861"
    locator: function generation with precision points and the structural error
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 4.5 (p. 187, the equation from the vector loop), Section 5.13 (p. 267, analytical synthesis of a fourbar function generator)
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: the chapter on analytical synthesis of function generators
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 2 (pp. 15 to 53), the output angle of the planar 4R linkage
---

Freudenstein's equation is the relation between the input angle $\varphi$ and the output angle $\psi$ of a [four-bar linkage](/four-bar-linkage/) that remains after the coupler angle is eliminated from the [vector loop closure equation](/vector-loop-closure/):

$$K_1\cos\psi - K_2\cos\varphi + K_3 = \cos(\varphi - \psi), \qquad K_1 = \frac{d}{a}, \quad K_2 = \frac{d}{c}, \quad K_3 = \frac{a^2 - b^2 + c^2 + d^2}{2ac}.$$

For a given linkage it is an equation in the angles, and its half-angle form gives the two assemblies. For given angles it is linear in $K_1, K_2, K_3$, so three pairs of angles give a $3 \times 3$ linear system whose solution is a four-bar that passes the three pairs exactly. That second use is three-point [function generation](/function-generation/). Freudenstein published the equation in 1954 and used it for approximate function generation in 1955.

The notation is that of the four-bar page: ground $d$ from $O_2 = (0, 0)$ to $O_4 = (d, 0)$, input $a$, coupler $b$, output $c$, and $\varphi = \theta_2$, $\psi = \theta_4$, both counterclockwise from the ground line. The constants above are for this convention, which is the one of Norton. Texts differ in the names and signs of the constants, for example when an angle is measured from the other end of the ground link, so check the convention of a source before you use its constants.

## In plain words

A four-bar has an input link and an output link joined by a coupler. If you know the angle of the input link, the angle of the output link is fixed (up to two choices). Freudenstein's equation writes that link between the two angles with three numbers that depend only on the link lengths.

The useful part is the other way round. Suppose you want the output to follow some rule of the input, for example the logarithm. Choose three input angles and the output angles that the rule asks for. Each pair gives one simple equation in the three numbers, so three pairs give three equations that you can solve with school algebra. From the three numbers you get the link lengths. The linkage then meets the rule exactly at those three pairs, and close to it in between.

## When it applies

- The mechanism is a planar four-bar with four pin joints, and the task relates only the input and output angles. This is [function generation](/function-generation/), one of the three tasks of [kinematic synthesis](/kinematic-synthesis/). Path and motion generation need the coupler, which the equation does not see.
- The angles are absolute: measured from the ground line. In a function generator you choose the start angles $\varphi_0, \psi_0$ and the ranges $\Delta\varphi, \Delta\psi$, and then map $x$ and $y = f(x)$ linearly to the angles.
- You want exact agreement at a few points. Three pairs give a linear system. With $\varphi_0$ and $\psi_0$ also unknown, up to five pairs can be met, but the system is no longer linear.
- For analysis, the same equation with known lengths gives $\psi$ from $\varphi$, as the [vector loop closure](/vector-loop-closure/) page shows.

## The template

The holes are the precision pairs $(\varphi_j, \psi_j)$ and the ground length $d$, which sets the scale.

```pseudo id=main
THREE-POINT-SYNTHESIS((φ1, ψ1), (φ2, ψ2), (φ3, ψ3), d)
L1  for j ← 1 to 3: row j of M ← (cos ψj, −cos φj, 1);  rj ← cos(φj − ψj)
L2  solve M (K1, K2, K3) = r by Gaussian elimination
L3  if M is singular or K1 = 0 or K2 = 0 then return "no unique four-bar"
L4  a ← d/K1;  c ← d/K2
L5  b² ← a² + c² + d² − 2ac K3
L6  return (a, b², c); it is a real four-bar when b² > 0
```

Line L1 writes one row per pair, line L2 is [Gaussian elimination](/gaussian-elimination/) on a $3 \times 3$ system, and lines L4 and L5 invert the definitions of the constants. A negative $a$ or $c$ is a signed length: that link points the other way, which is length $|a|$ at the angle $\varphi + \pi$. If $b^2 \le 0$ no real coupler exists for these pairs. When $\cos\varphi_j$ and $\cos\psi_j$ are rational, as for the points $((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$ of the unit circle with rational $t$, every step is exact in rational arithmetic.

### Derivation from the loop

The loop is $a e^{i\varphi} + b e^{i\theta_3} - c e^{i\psi} - d = 0$, with $\theta_3$ the coupler angle. Put the coupler alone: $b e^{i\theta_3} = c e^{i\psi} + d - a e^{i\varphi}$. Take the squared modulus of both sides:

$$b^2 = a^2 + c^2 + d^2 + 2cd\cos\psi - 2ad\cos\varphi - 2ac\cos(\varphi - \psi),$$

since $\operatorname{Re}(c e^{i\psi} \cdot \overline{a e^{i\varphi}}) = ac\cos(\varphi - \psi)$. Divide by $2ac$ and move terms:

$$\cos(\varphi - \psi) = \frac{d}{a}\cos\psi - \frac{d}{c}\cos\varphi + \frac{a^2 - b^2 + c^2 + d^2}{2ac},$$

which is the equation with the stated $K_1, K_2, K_3$. The step is reversible: if $(\varphi, \psi)$ satisfies the equation, then $c e^{i\psi} + d - a e^{i\varphi}$ has length $b$, so it equals $b e^{i\theta_3}$ for one $\theta_3$ and the loop closes. So the equation holds exactly when the linkage can be assembled with input $\varphi$ and output $\psi$. $\blacksquare$

### Why the synthesis is correct

Suppose line L2 finds $K$ with $K_1, K_2 \ne 0$, and $b^2 > 0$ in line L5. Lines L4 and L5 give lengths whose constants are exactly $K_1 = d/a$, $K_2 = d/c$ and $K_3 = (a^2 - b^2 + c^2 + d^2)/(2ac)$, because L5 is the definition of $K_3$ solved for $b^2$. Each pair satisfies row $j$ of the system, which is the equation for these lengths. By the reverse step of the derivation the linkage can be assembled at each pair. The tests check this with exact rational arithmetic on random rational pairs: the identity and $|B - A|^2 = b^2$ hold exactly at all three pairs.

What the proof does not give: the three assemblies can be on different branches, or on different circuits of a non-Grashof linkage. Then the linkage passes the pairs only if it is taken apart and put together again. Check the branch at each pair, as the pitfalls say.

### Cost

One synthesis is a fixed number of operations. With $m > 3$ pairs the system is overdetermined, and a least-squares solution costs $O(m)$.

## Classic examples

**An exact example with integer pins.** Take the input angles with $\tan(\varphi_j/2) = 1/3, 1/2, 1$, which are $36.87°$, $53.13°$, $90°$, and the output angles with $\tan(\psi_j/2) = 1/2, 2/3, 3/2$, which are $53.13°$, $67.38°$, $112.62°$, and $d = 9$. Then $(\cos\varphi_j, \sin\varphi_j)$ is $(4/5, 3/5)$, $(3/5, 4/5)$, $(0, 1)$ and $(\cos\psi_j, \sin\psi_j)$ is $(3/5, 4/5)$, $(5/13, 12/13)$, $(-5/13, 12/13)$. The system

$$\begin{pmatrix} 3/5 & -4/5 & 1 \\ 5/13 & -3/5 & 1 \\ -5/13 & 0 & 1 \end{pmatrix} \begin{pmatrix} K_1 \\ K_2 \\ K_3 \end{pmatrix} = \begin{pmatrix} 24/25 \\ 63/65 \\ 12/13 \end{pmatrix}$$

has the solution $K_1 = 3/5$, $K_2 = 9/13$, $K_3 = 15/13$. So $a = 15$, $c = 13$, and $b^2 = 225 + 169 + 81 - 2 \cdot 15 \cdot 13 \cdot 15/13 = 25$, $b = 5$. The pins at the three pairs are:

| pair | $A = a e^{i\varphi}$ | $B = d + c e^{i\psi}$ | $B - A$ | $\lvert B - A\rvert$ |
|---|---|---|---|---|
| 1 | $(12, 9)$ | $(84/5, 52/5)$ | $(24/5, 7/5)$ | 5 |
| 2 | $(9, 12)$ | $(14, 12)$ | $(5, 0)$ | 5 |
| 3 | $(0, 15)$ | $(4, 12)$ | $(4, -3)$ | 5 |

The linkage $(a, b, c, d) = (15, 5, 13, 9)$ is a Grashof double-rocker by the [Grashof condition](/grashof-condition/): $5 + 15 \le 13 + 9$ and the coupler is the shortest link. Its input rocks between about $26.4°$ and $94°$, and all three pairs lie on the open branch of that interval, so it moves through them without being taken apart.

**A logarithm generator.** Let $y = \log_{10} x$ for $1 \le x \le 2$, with $\varphi$ from $90°$ to $150°$ and $\psi$ from $15°$ to $75°$, and $d = 1$. The [Chebyshev spacing](/chebyshev-spacing/) of three points, $x_j = 1.5 - 0.5\cos((2j - 1)\pi/6)$, gives $x = 1.06699$, $1.5$, $1.93301$ and the pairs $(94.019°, 20.613°)$, $(120°, 50.098°)$, $(145.981°, 72.051°)$. The solution is $K = (1.02934, 0.84016, -0.73676)$ and $a = 0.97149$, $b = 2.25042$, $c = 1.19026$. Measured on a grid of 2001 values of $x$ along the open branch, the largest structural error, the difference between the output angle and the ideal one, is $0.061°$ at $x = 1$. With equally spaced points $1.25, 1.5, 1.75$ it is $0.167°$. The end errors of the Chebyshev design ($0.061°$ and $0.046°$) are not equal to the inner peaks ($0.011°$ and $0.037°$), so this spacing reduces the error here but it is not the minimax design.

**Position analysis.** For a given linkage, write the equation as $P\cos\psi + Q\sin\psi + R = 0$ and substitute $t = \tan(\psi/2)$. The result is the quadratic whose two roots are the open and crossed assemblies, as proved on the [vector loop closure](/vector-loop-closure/) page.

**Synthesis with more conditions.** [Kinematic synthesis](/kinematic-synthesis/) needs more than three pairs when the range must be met more closely. Least squares on the equation residual is linear, and [optimization-based linkage synthesis](/optimization-based-linkage-synthesis/) minimizes the true structural error instead.

## Variations

- **More than three pairs.** With $m > 3$ pairs, solve the normal equations of the $m \times 3$ system. This minimizes the residual of the equation, which is not the angle error, so the result is only a good start for a local search.
- **Free start angles.** With $\varphi_0$ and $\psi_0$ unknown, four or five pairs can be met exactly, and the equations become polynomial in $\cos\varphi_0, \sin\varphi_0, \cos\psi_0, \sin\psi_0$.
- **Derivative conditions.** Instead of three separate pairs, ask that the linkage match $f$ and its first derivatives at one point (infinitesimally close precision points). Differentiating the equation in $\varphi$ gives linear equations in the same $K_1, K_2, K_3$.
- **The slider-crank.** The same elimination for a [slider-crank mechanism](/slider-crank-mechanism/) relates the crank angle to the slider position, and gives a linear system for crank-angle to slider-position generators.

## Pitfalls

- **The wrong sign convention.** If the source measures $\psi$ from the other end of the ground, or calls the input $\psi$, the constants change sign or swap. Constants from one source in the equation of another give a linkage that fails all three pairs. Derive the constants from the loop of your own figure, as above.
- **Branch defect.** Line L6 proves only that each pair can be assembled. Check that all pairs are on one branch and one circuit, for example with the branch sign of the [vector loop closure](/vector-loop-closure/) page, before you accept the design.
- **Order defect and poor transmission.** The linkage may pass the pairs in the wrong order, or only with a small [transmission angle](/transmission-angle/). Check both over the full range, not only at the pairs.
- **Singular or useless systems.** Repeated pairs, or two pairs with equal $\cos\psi_j$ and equal $\cos\varphi_j$, make $M$ singular. A tiny $K_1$ or $K_2$ gives very long links. Choose the ranges $\Delta\varphi$, $\Delta\psi$ and the start angles again.

## Exercises

1. Check the three rows of the exact example by hand, and find the open and crossed values of $\psi$ for the linkage $(15, 5, 13, 9)$ at $\varphi = 60°$.
2. Derive the constants of the equation when $\psi$ is measured clockwise from the line $O_4 O_2$ instead of counterclockwise from $O_2 O_4$.
3. Design a three-point generator for $y = x^2$, $0 \le x \le 1$, with $\Delta\varphi = \Delta\psi = 90°$, and measure its structural error on a grid.
4. Show that the matrix of line L1 is singular when two pairs have the same $\cos\varphi$ and the same $\cos\psi$. When is the system then still solvable?
5. Write the linear system for the case of one exact pair and the first and second derivatives of $\psi(\varphi)$ at that pair.

## References
