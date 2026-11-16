---
tag: ZZXTNV
kind: algorithm
slug: force-closure-test
name: Force-closure test
aliases:
- origin in the convex hull of primitive wrenches
area: robotics/grasping-and-manipulation
level: core
summary: Decides whether a grasp is in force closure on linearized friction cones, by an exact linear feasibility test on the primitive contact wrenches.
model: real-ram
complexity:
  vars: {N: "the number of primitive wrenches (c contacts times k cone edges)", d: "the dimension of the wrench space (3 in the plane and 6 in space)"}
  time: {worst: O(N^(d+1))}
  space: {extra: O(d N)}
properties: {deterministic: true, exact: true, certificate: true}
history:
  year: 1987
  people: [Bud Mishra, Jacob T. Schwartz, Micha Sharir]
  note: Mishra, Schwartz and Sharir wrote closure of a grasp as the origin inside the convex hull of the contact wrenches and used Steinitz's theorem to count fingers.
prereqs: [force-closure, polyhedral-friction-cone, linear-feasibility]
see_also: [form-closure, convex-hull, simplex-method, bland-rule, two-phase-simplex-method, seidel-linear-programming, ferrari-canny-metric, grasp-wrench-space]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 12, Section 12.1.7 (form closure, with the linear program test in Section 12.1.7.2) and Section 12.2.3 (force closure)"
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.4 (restraint analysis), Sections 38.4.1 (form closure, the linear program LP1) and 38.4.2 (force closure); the chapter is pages 955 to 988"
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 5 (grasp statics and force-closure grasps)
  - paper: "Bud Mishra, Jacob T. Schwartz and Micha Sharir, On the existence and synthesis of multifinger positive grips, Algorithmica 2(4), 541-558, 1987"
    locator: the whole paper (closure as the origin in the interior of the convex hull of the wrenches, and the finger counts from Steinitz's theorem)
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977
    locator: pages 103 to 107 (the smallest index rule and the proof that it does not cycle)
  - paper: doi:10.1007/BFb0121192
    title: David Avis and Vašek Chvátal, Notes on Bland's pivoting rule, Mathematical Programming Study 8, 1978
    locator: pages 24 to 34 (programs on which the smallest index rule makes an exponential number of pivots)
  - paper: "Nimrod Megiddo, Linear programming in linear time when the dimension is fixed, Journal of the ACM 31(1), 114-127, 1984"
    locator: the whole paper (an O(N) algorithm for a linear program with a fixed number of variables)
---

The force-closure test decides whether a set of contacts can hold a rigid body against every external force and moment. Each contact can push only into the body, and with friction it can also push sideways, inside a [friction cone](/friction-cone/). The test replaces each cone by a pyramid with a few edges, turns each edge into a wrench (a force together with its moment), and asks one question: can a strictly positive combination of these primitive wrenches sum to zero while the wrenches span all directions? That question is a small [linear feasibility](/linear-feasibility/) problem. It is the same as asking whether the origin lies strictly inside the [convex hull](/convex-hull/) of the primitive wrenches.

## In plain words

Hold a box between your fingers. Every push or twist that the world gives the box must be cancelled by your fingers. A finger can only push, it cannot pull, and it can push a bit sideways because of friction. So each finger gives a small fan of pushes. The grasp is safe when the fans of all fingers together can make a push in every direction. The test checks this with a short list of the extreme pushes. It looks for a way to use every extreme push a little, so that all of them cancel. If such a mix exists, and the pushes point in all directions, then any outside push can also be cancelled, and the grasp is safe.

## The problem

The input is a grasp of a rigid body with $c$ contacts. Contact $i$ has a point $p_i$ and a unit normal $n_i$ that points into the body, both in the body frame, and a friction coefficient $\mu$. The [contact model](/grasp-contact-models/) is a frictionless point, a point with friction, or a soft finger. A wrench is written moment first: $\mathcal{F} = (m, f)$ in space, with $d = 6$, and $\mathcal{F} = (m_z, f_x, f_y)$ in the plane, with $d = 3$.

Each friction cone is replaced by a [polyhedral cone](/polyhedral-friction-cone/) with edges $f_{i1}, \ldots, f_{ik}$. In the plane the cone has exactly the two edges $n_i \pm \mu t_i$, where $t_i$ is $n_i$ turned by 90 degrees. In space the edges are $n_i + \mu(\cos(2\pi j/k)\, t_{i1} + \sin(2\pi j/k)\, t_{i2})$ for $j = 0, \ldots, k-1$, where $t_{i1}, t_{i2}$ are unit tangents. These edges lie on the circular cone, so each pyramid is inside it. A frictionless contact has the one edge $n_i$. The primitive wrenches are

$$w = (p_i \times f_{ij},\ f_{ij}) \quad \text{for each contact } i \text{ and each edge } j.$$

There are $N$ of them; $N = ck$ when all contacts have $k$ edges. Let $F$ be the $d \times N$ matrix with these columns. The question is whether $\operatorname{pos}(F) = \{F k : k \ge 0\}$ is all of $\mathbb{R}^d$. That is [force closure](/force-closure/) of the linearized grasp. With frictionless contacts it is first-order [form closure](/form-closure/).

## The algorithm

Force closure holds if and only if $\operatorname{rank} F = d$ and $F k = 0$ for some $k$ with every entry positive. Scale $k$ so that its smallest entry is 1 and put $y = k - \mathbf{1}$: the second condition becomes $F y = -F\mathbf{1}$ with $y \ge 0$. Lynch and Park write the same test as the linear program "minimize $\mathbf{1}^T k$ subject to $F k = 0$ and $k \ge \mathbf{1}$". The feasibility problem is solved by phase one of the [simplex method](/simplex-method/), in exact rational arithmetic, with [Bland's rule](/bland-rule/) so that it cannot cycle.

```pseudo id=main
FORCE-CLOSURE(contacts, μ, k)               ▷ contacts (p_i, n_i), i = 1 .. c
L1  W ← empty list
L2  for each contact (p_i, n_i) do
L3      for each edge f of the linearized cone at contact i do
L4          append the wrench (p_i × f, f) to W
L5  F ← the d × N matrix with the wrenches of W as columns
L6  if rank F < d then return NOT CLOSED
L7  y ← PHASE-ONE(F, -F·1)                  ▷ find y ≥ 0 with F y = -F·1
L8  if y = NONE then return NOT CLOSED
L9  return CLOSED, with the certificate k = 1 + y

PHASE-ONE(A, b)                             ▷ find y ≥ 0 with A y = b, or NONE
L10 negate each row i of [A | b] with b_i < 0
L11 add an artificial variable a_i to row i; the first basis is a
L12 repeat
L13     compute the reduced cost r_j of each column for the cost a_1 + ... + a_m
L14     if no r_j < 0 or the cost of the basis is 0 then exit the loop
L15     q ← the smallest j with r_j < 0                     ▷ Bland's rule
L16     i ← the row with the least ratio b_i / A_iq over A_iq > 0, ties to the smallest basic index
L17     pivot on (i, q)
L18 if some a_i is not 0 then return NONE else return the y part of the basic solution
```

Line L6 rejects grasps whose wrenches lie in a proper subspace. Such a grasp can have $F k = 0$ with $k > 0$ (two opposite pushes along one line do), but it cannot resist a wrench outside that subspace. Line L14 stops as soon as the artificial variables are all zero. When $F\mathbf{1} = 0$ already, as in a symmetric grasp, the test stops at once with $k = \mathbf{1}$. The vector $k$ of line L9 is a certificate: anyone can check $k \ge \mathbf{1}$ and $F k = 0$ in exact arithmetic without trusting the solver.

## Example

Take a planar box and two fingers with $\mu = 3/5$. Finger 1 touches the left side at $p_1 = (-1, 1/2)$ with $n_1 = (1, 0)$; finger 2 touches the right side at $p_2 = (1, -1/2)$ with $n_2 = (-1, 0)$. With $t_i$ equal to $n_i$ turned by +90 degrees, the edges are $(1, \pm 3/5)$ at finger 1 and $(-1, \mp 3/5)$ at finger 2. The planar moment of a force $f$ at $p$ is $p_x f_y - p_y f_x$. Lines L1 to L5 give

$$F = \begin{pmatrix} -11/10 & 1/10 & -11/10 & 1/10 \\ 1 & 1 & -1 & -1 \\ 3/5 & -3/5 & -3/5 & 3/5 \end{pmatrix}, \qquad -F\mathbf{1} = (2, 0, 0).$$

The rank is 3, so line L6 passes. PHASE-ONE starts with the artificial values $a = (2, 0, 0)$ and cost 2.

| Pivot | Entering ($r_q$) | Leaving row (ratio) | Basic values | Cost |
|---|---|---|---|---|
| start | | | $a_1 = 2$, $a_2 = 0$, $a_3 = 0$ | 2 |
| 1 | $y_1$ ($-1/2$) | row 2 (0) | $a_1 = 2$, $y_1 = 0$, $a_3 = 0$ | 2 |
| 2 | $y_4$ ($-1/5$) | row 3 (0) | $a_1 = 2$, $y_1 = 0$, $y_4 = 0$ | 2 |
| 3 | $y_2$ ($-1/5$) | row 1 (10) | $y_2 = 10$, $y_1 = 0$, $y_4 = 10$ | 0 |

The first two pivots are degenerate: the basis changes and the point does not. After the third pivot the cost is 0, so line L14 exits and line L9 returns $k = (1, 11, 1, 11)$. The check: the moments give $-11/10 + 11/10 - 11/10 + 11/10 = 0$, the $x$ forces give $1 + 11 - 1 - 11 = 0$, and the $y$ forces give $3/5 - 33/5 - 3/5 + 33/5 = 0$. The grasp is in force closure.

With $\mu = 1/3$ the same fingers give $-F\mathbf{1} = (2, 0, 0)$ again, but after one pivot no reduced cost is negative and the cost is still 2. The test returns NOT CLOSED. The reason is geometric: the line through the two contacts makes the angle $\arctan(1/2) \approx 26.57$ degrees with the normals, and the fingers can squeeze along that line only when it is inside both friction cones, that is when $\mu > 1/2$ (the [antipodal grasp](/antipodal-grasp/) condition). At $\mu = 1/2$ exactly the line is on the edge of the cones, and the exact test correctly returns NOT CLOSED.

## Correctness

The full proof is in proofs/correctness.md. It has four steps. First, the wrenches that the contacts can apply are exactly $\operatorname{pos}(F)$, because a linearized cone is the set of nonnegative combinations of its edges. Second, $\operatorname{pos}(F) = \mathbb{R}^d$ if and only if $\operatorname{rank} F = d$ and $F k = 0$ for some $k > 0$: given any wrench $x = F z$, add a large multiple of $k$ to $z$ to make it nonnegative. Third, a $k > 0$ exists if and only if a $k \ge \mathbf{1}$ exists, by scaling. Fourth, phase one with Bland's rule stops, and it ends with cost 0 if and only if the system $F y = -F\mathbf{1}$, $y \ge 0$ has a solution. The proof also shows the convex hull form: $\operatorname{pos}(F) = \mathbb{R}^d$ if and only if the origin is in the interior of $\operatorname{conv}(F)$.

The answer is about the linearized cones. Because the spatial edges lie on the true cones, a CLOSED answer is also true for the circular cones. A NOT CLOSED answer is not: a grasp can be in force closure with the circular cones and fail the test with a coarse pyramid. In the plane the cone is exactly the two-edge cone, and the test is exact.

## Complexity

Let $N$ be the number of primitive wrenches and $d$ the dimension of the wrench space. Building $F$ costs $O(dN)$. The rank test by Gaussian elimination costs $O(d^2 N)$ arithmetic operations. Each simplex pivot updates a tableau with $d$ rows and $N + d + 1$ columns, so it costs $O(d(N + d))$ operations. Bland's rule never repeats a basis, and there are at most $\binom{N + d}{d}$ bases, so for fixed $d$ the test makes $O(N^d)$ pivots and $O(N^{d+1})$ operations in the worst case. This bound is weak in practice: the tableau has only $d \le 6$ rows, and on grasps the method typically stops after a few pivots. Avis and Chvátal (1978) gave programs on which Bland's rule takes an exponential number of pivots, so the bound in $N$ and $d$ together is not polynomial.

Other solvers give better worst cases. For fixed $d$, the linear program can be solved in $O(N)$ operations by Megiddo's algorithm, and in expected $O(d!\,N)$ by [Seidel's algorithm](/seidel-linear-programming/). An [interior point method](/interior-point-method/) runs in time polynomial in the input size for every $d$. The extra space is the tableau, $O(d(N + d)) = O(dN)$ entries.

The cost model here is the real RAM. The implementation uses exact rationals, and the size of the numbers grows during the pivots; for $d \le 6$ and a few dozen wrenches this growth is small.

## Properties

- **Exact.** With rational data and rational arithmetic, the answer is exact. It does not need a tolerance, and it gets boundary cases right, such as the cone edge at $\mu = 1/2$ in the example.
- **Certificate.** A CLOSED answer comes with $k \ge \mathbf{1}$ and $F k = 0$. A NOT CLOSED answer from line L18 comes with an optimal phase-one basis. Its dual solution gives a direction $u \ne 0$ with $u^T w \le 0$ for each primitive wrench $w$, so the contacts cannot apply the wrench $u$. A NOT CLOSED answer from line L6 has a $u$ orthogonal to all columns of $F$.
- **Frame invariant.** Moving the reference point or rotating the body frame multiplies $F$ by an invertible matrix (an adjoint transpose), which changes neither the rank nor the solutions of $F k = 0$. The answer does not depend on the frame or on the length unit, unlike the [Ferrari-Canny metric](/ferrari-canny-metric/).
- **Monotone.** Adding a contact or an edge adds a column, so a closed grasp stays closed.

## Variants and improvements

- **Lynch and Park's form.** Minimize $\mathbf{1}^T k$ subject to $F k = 0$, $k \ge \mathbf{1}$, after a rank check. For their example $F = ((0, 0, -1, 2), (-1, 0, 1, 0), (0, -1, 0, 1))$ the test returns $k = (2, 1, 2, 1)$.
- **A quantitative linear program.** The Handbook's LP1 maximizes a margin $\delta$ subject to $G_n \lambda = 0$, $\lambda \ge \delta\mathbf{1}$, $\delta \ge 0$ and $\mathbf{1}^T \lambda \le n_c$, where $G_n$ has the frictionless contact wrenches as columns and $n_c$ is the number of contacts. With full rank, a positive optimum means first-order form closure, and the size of the optimum measures how far the grasp is from the boundary. The value depends on the length unit.
- **Convex hull.** Compute the hull of the primitive wrenches, for example with [Quickhull](/quickhull/), and check that every facet has the origin strictly on its inner side. This also gives the [Ferrari-Canny metric](/ferrari-canny-metric/) as the least facet distance. It is practical for $d = 3$; for $d = 6$ the hull can have $\Theta(N^3)$ facets.
- **Circular cones.** Testing the true cones is a [second-order cone program](/second-order-cone-programming/). It avoids the error of the pyramid at the price of an iterative solver.
- **Soft fingers.** Each edge of the cone appears twice, with the torsional moment $+\gamma n_i$ and $-\gamma n_i$, for the model $\lvert m_n \rvert \le \gamma f_n$. Two soft fingers can then hold a body in space, while two point contacts never can.

## When to use it

Use the test to accept or reject a candidate grasp in a grasp planner, to check a fixture layout, or to check a contact set in a simulation. Use the exact version when grasps sit on the boundary by design, for example an antipodal grasp at the cone edge or a fixture with symmetric locators. Use a floating point linear program solver when the data come from sensors and a tolerance is acceptable. Use a quality score such as [Ferrari-Canny](/ferrari-canny-metric/) when you must rank closed grasps, not only accept them.

## Pitfalls

- **Forgetting the rank test.** $F k = 0$ with $k > 0$ is not enough. Two opposite fingers along one line satisfy it with rank 2 in the plane, and they cannot resist a moment.
- **$k \ge 0$ in place of $k > 0$.** The vector $k = 0$ always solves $F k = 0$. The condition must be strict, which the scaling to $k \ge \mathbf{1}$ makes explicit.
- **Float tolerances.** A float solver with a tolerance of $10^{-9}$ can call a boundary grasp closed. Either use exact arithmetic or report grasps within the tolerance as unsure.
- **Wrong normal direction.** The normal points into the body. An outward normal turns each push into a pull and gives a wrong answer with no error.
- **Pyramid outside the cone.** If the edges are on the circumscribed pyramid ($\mu / \cos(\pi/k)$), the pyramid is larger than the true cone, and a CLOSED answer can be wrong for the true cone.
- **Mixed conventions.** Murray, Li and Sastry write a wrench force first, Lynch and Park moment first. Any consistent order gives the same answer, but one matrix must not mix them.

## Implementations

## History

Reuleaux (1875) and Somov (1897) studied how many frictionless contacts immobilize a body. Salisbury and Roth (1983) analyzed articulated hands in terms of the wrenches that the fingers apply. Mishra, Schwartz and Sharir (1987) wrote closure as the origin inside the convex hull of the contact wrenches and used Steinitz's theorem to show that a bounded number of fingers suffices. The linear program form is now the standard textbook test; Lynch and Park (2017) give it for form closure, and the Handbook chapter of Prattichizzo and Trinkle gives a quantitative version.

## References
