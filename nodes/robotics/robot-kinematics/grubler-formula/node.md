---
tag: RD6YTN
kind: theorem
slug: grubler-formula
name: "Grubler's formula"
aliases:
- Chebychev-Grubler-Kutzbach criterion
- mobility formula
area: robotics/robot-kinematics
level: intro
summary: "A mechanism of N links and J joints has m(N - 1 - J) + sum of f_i degrees of freedom, m = 3 planar, m = 6 spatial, if the joint constraints are independent. Special geometry can break it."
prereqs: [kinematic-chain, kinematic-pair]
see_also: [maxwell-counting-rule, degrees-of-freedom-analysis, four-bar-linkage, watt-and-stephenson-six-bar, parallel-manipulator, configuration-space, kinematic-chain, kinematic-pair]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Section 2.2.2, Grübler's formula (Equation 2.4, the hypothesis that the joint constraints are independent, and the examples that include the Stewart-Gough platform)
  - paper: doi:10.1016/j.euromechsol.2004.12.003
    title: Grigore Gogu, Chebychev-Grübler-Kutzbach's criterion for mobility calculation of multi-loop mechanisms revisited via theory of linear transformations, European Journal of Mechanics A/Solids 24(3), 2005
    locator: pages 427 to 441 (a survey of the many forms of the formula and of the mechanisms for which they fail, and a rank form of the mobility)
  - book: "Martin Grübler, Allgemeine Eigenschaften der zwangläufigen ebenen kinematischen Ketten, Der Civilingenieur 29, 1883"
    locator: the count for planar chains with one freedom (general locator; the page range differs between sources)
  - book: "Karl Kutzbach, Mechanische Leitungsverzweigung, ihre Gesetze und Anwendungen, Maschinenbau (Der Betrieb) 8(21), 1929"
    locator: pages 710 to 716, the count for spatial chains
  - book: "G. T. Bennett, A new mechanism, Engineering 76, 1903"
    locator: pages 777 to 778, the spatial four-bar with four revolute joints that moves although the count is negative
---

Grübler's formula counts the degrees of freedom of a mechanism from its parts list. Take $N$ links, the ground included, and $J$ joints, where joint $i$ allows $f_i$ relative motions. Each moving link has $m$ freedoms, with $m = 3$ for a planar mechanism and $m = 6$ for a spatial one, and each joint removes $m - f_i$ of them. So the mechanism has $m(N - 1 - J) + \sum_i f_i$ degrees of freedom, *if the joint constraints are independent*. The count is a rule, not a law: special geometry can make the constraints dependent, and then the true mobility differs, as in the Bennett linkage. [Maxwell's counting rule](/maxwell-counting-rule/) is the same kind of count for bars and point joints in a framework, used to test stiffness, and [degrees of freedom analysis](/degrees-of-freedom-analysis/) applies such counts to the constraints of a CAD sketch.

## Statement

Let a mechanism be a connected [kinematic chain](/kinematic-chain/) with one fixed link. It has $N$ links, the ground included, and $J$ joints. Joint $i$ is a [kinematic pair](/kinematic-pair/) whose set of allowed relative poses $K_i$ is a smooth manifold of dimension $f_i$. Let $m = 6$ and $G = SE(3)$ for a spatial mechanism. For a planar mechanism, where all links move in parallel planes, let $m = 3$ and $G = SE(2)$.

The joint values form the manifold $Q = K_1 \times \dots \times K_J$ of dimension $\sum_i f_i$. Choose a spanning tree of the graph of the chain. Each of the $L = J - N + 1$ joints that are not in the tree closes one loop, and the loop closes when the product of the joint transforms around it is the identity. This gives a smooth map $\Phi : Q \to G^L$, and the configuration space of the mechanism is $C = \Phi^{-1}(e)$, where $e$ is the identity of $G^L$.

**Theorem (Grübler's formula).**

1. The two counts agree: $\ m(N - 1 - J) + \sum_{i=1}^{J} f_i = \sum_{i=1}^{J} f_i - mL$. Call this number $\mathrm{dof}$.
2. Let $q \in C$. If the differential $d\Phi_q$ has rank $mL$, that is, if the $mL$ loop constraints are independent at $q$, then near $q$ the set $C$ is a smooth manifold of dimension $\mathrm{dof}$. The mechanism then moves near $q$ with exactly $\mathrm{dof}$ degrees of freedom, and if $\mathrm{dof} = 0$ the configuration $q$ is isolated.
3. If $\mathrm{dof} < 0$, the constraints are dependent at every point of $C$.

The formula says nothing when the constraints are dependent. The section Tightness gives mechanisms where the true mobility is then larger and one where it is smaller.

## In plain words

Take each moving part of a machine on its own. In space a free part can move in six ways: three slides and three turns. In a flat machine it can move in three ways. Now add the joints one at a time. A hinge lets two parts turn about one line, so it takes away all but one of their relative motions. Count the motions of the free parts, take away what each joint removes, and what is left is the number of motors you need to drive the machine.

This works when every joint takes away motions that no other joint has already taken away. In some machines, parts are made exactly parallel or exactly equal, and two joints then take away the same motion. Such a machine can move although the count says that it is locked. The count is a quick test, not a proof.

## Proof

**Part 1.** By the loop count of the [kinematic chain](/kinematic-chain/) page, $L = J - N + 1$, so $\sum f_i - mL = \sum f_i - mJ + mN - m = m(N - 1 - J) + \sum f_i$.

The left side has a direct meaning that Lynch and Park use. Without joints the $N - 1$ moving links have $m(N - 1)$ freedoms. Joint $i$ allows $f_i$ of the $m$ relative motions of its two links, so it imposes $m - f_i$ constraints. If no constraint repeats another, the remaining freedoms are $m(N - 1) - \sum_i (m - f_i) = m(N - 1 - J) + \sum_i f_i$.

**Part 2.** The map $\Phi$ is smooth, because each joint transform is smooth on $K_i$ and the group product of $G$ is smooth. The rank of $d\Phi$ is lower semicontinuous, and its largest possible value is $\dim G^L = mL$. So if $d\Phi_q$ has rank $mL$, it has rank $mL$ on a neighborhood $U$ of $q$, and $\Phi$ is a submersion on $U$. By the submersion theorem (the implicit function theorem), $\Phi^{-1}(e) \cap U$ is a smooth submanifold of $U$ of dimension $\dim Q - mL = \sum f_i - mL$, which is $\mathrm{dof}$ by part 1. A manifold of dimension 0 is a discrete set, so for $\mathrm{dof} = 0$ the point $q$ is isolated.

**Part 3.** The rank of $d\Phi_q$ is at most $\dim Q = \sum f_i$. If $\mathrm{dof} < 0$ then $\sum f_i < mL$, so the rank cannot be $mL$ at any $q$. $\blacksquare$

The spanning tree does not matter. A different tree gives a different set of loops, but each new loop product is a product of the old loop products and their conjugates, so the new map is $\Phi'(q) = \psi_q(\Phi(q))$, where for each $q$ the map $\psi_q$ is a local diffeomorphism of $G^L$ that fixes $e$. So the two maps have the same zero set $C$, and at each point of $C$ their differentials have the same rank.

## Consequences

Each count below can be checked by hand. All joints are revolute (R, $f = 1$), prismatic (P, $f = 1$), universal (U, $f = 2$) or spherical (S, $f = 3$).

| mechanism | $m$ | $N$ | $J$ | $\sum f_i$ | count | true mobility |
|---|---|---|---|---|---|---|
| planar four-bar | 3 | 4 | 4 | 4 | $3(4 - 1 - 4) + 4 = 1$ | 1 |
| slider-crank (3 R, 1 P) | 3 | 4 | 4 | 4 | $1$ | 1 |
| planar five-bar | 3 | 5 | 5 | 5 | $3(5 - 1 - 5) + 5 = 2$ | 2 |
| Watt or Stephenson six-bar | 3 | 6 | 7 | 7 | $3(6 - 1 - 7) + 7 = 1$ | 1 |
| planar 3-RPR parallel robot | 3 | 8 | 9 | 9 | $3(8 - 1 - 9) + 9 = 3$ | 3 |
| serial arm with $n$ R joints | 6 | $n + 1$ | $n$ | $n$ | $6 \cdot 0 + n = n$ | $n$ |
| Stewart-Gough, 6 UPS legs | 6 | 14 | 18 | 36 | $6(14 - 1 - 18) + 36 = 6$ | 6 |
| Stewart-Gough, 6 SPS legs | 6 | 14 | 18 | 42 | $6(14 - 1 - 18) + 42 = 12$ | 6 for the platform |

- **Open chains.** For a serial or tree chain, $J = N - 1$, so $L = 0$, there is no constraint, and the mobility is $\sum f_i$ exactly, with no hypothesis.
- **Idle freedoms.** With SPS legs each leg can spin about its own axis between its two ball joints. These 6 spins do not move the platform, so the formula gives 12 while the platform has 6. Replacing one S by a U in each leg removes the spins, as in the UPS row. The formula counts every freedom, including those that a designer does not care about.
- **Choice of $m$.** Using $m = 3$ is itself a claim about the geometry: the joint axes of a planar mechanism are exactly parallel. Counted as a spatial mechanism, the planar four-bar gives $6(4 - 1 - 4) + 4 = -2$, yet it moves. Spherical mechanisms, whose joint axes all meet in one point, also use $m = 3$ with $G = SO(3)$.
- **Where it sits.** [Degrees of freedom analysis](/degrees-of-freedom-analysis/) in CAD constraint solvers uses the same subtraction for points, lines and geometric constraints, and checks it on subsystems. [Maxwell's counting rule](/maxwell-counting-rule/) is the case of bars between point joints, and Calladine's form of it, bars minus needed bars equals self-stresses minus mechanisms, is the exact version of the count in that setting.

## Tightness

Each example below breaks the hypothesis of part 2, and the true mobility is not the count.

- **The Bennett linkage (count too low).** Four links joined in a ring by four revolute joints with skew axes. In space, $6(4 - 1 - 4) + 4 = -2$, so by part 3 the constraints are always dependent. Bennett (1903) showed that if opposite links have equal lengths $a_1 = a_3$, $a_2 = a_4$ and equal twist angles $\alpha_1 = \alpha_3$, $\alpha_2 = \alpha_4$, with $\sin\alpha_1 / a_1 = \sin\alpha_2 / a_2$, the loop moves with one freedom.
- **The double parallelogram (count too low).** In the plane, join a ground link and a coupler by three parallel cranks of equal length, with equal spacing of the pivots on the ground and on the coupler. Then $N = 5$, $J = 6$ and $3(5 - 1 - 6) + 6 = 0$, but the coupler moves in a circular translation with one freedom. The third crank adds constraints that the first two already impose. If the third crank is a little longer, the mechanism locks, and the count is right again.
- **A four-bar that cannot move (count too high).** Take a planar four-bar with ground $d = 3$ and the other three links of length 1. The three links must span the distance 3, which is their total length, so the only configuration is the straight one, and the true mobility is 0, not 1. In the loop equations $\cos\theta_2 + \cos\theta_3 - \cos\theta_4 = 3$ and $\sin\theta_2 + \sin\theta_3 - \sin\theta_4 = 0$, the Jacobian at $\theta_2 = \theta_3 = 0$, $\theta_4 = \pi$ is $\begin{pmatrix} 0 & 0 & 0 \\ 1 & 1 & 1 \end{pmatrix}$, of rank 1, not 2. So the constraints are dependent there. Some texts say that the count is a lower bound on the mobility when the constraints are dependent. That holds for the dimension of the complex solution set of the loop equations, but not for the real mechanism, as this example shows.

## History

Chebyshev (1869) gave a count for planar linkages in his work on parallel motions. Grübler (1883) stated the planar count for chains with one freedom, and Kutzbach (1929) gave the spatial form, which is why the rule is also called the Chebyshev-Grübler-Kutzbach criterion. Bennett (1903) found the first spatial overconstrained loop. Many later forms of the criterion were proposed to cover such mechanisms. Gogu (2005) surveys them and gives a form based on the theory of linear transformations, which works with the rank of the constraint equations, as part 2 above does.

## References
