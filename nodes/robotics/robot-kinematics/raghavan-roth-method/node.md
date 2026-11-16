---
tag: MTT21K
kind: algorithm
slug: raghavan-roth-method
name: Raghavan-Roth method
aliases:
- Raghavan-Roth elimination
area: robotics/robot-kinematics
level: research
summary: Solves the general 6R inverse kinematics by dialytic elimination to one polynomial of degree 16 in the tangent of a half angle.
model: real-ram
complexity:
  vars: {d: "the degree of the final polynomial (16 for a general 6R arm and 4 for the 3R position problem)"}
  time: {worst: Θ(d^3)}
  space: {extra: Θ(d^2)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1990
  people: [Madhusudan Raghavan, Bernard Roth]
  note: Raghavan and Roth reduced the inverse kinematics of the general 6R arm to a polynomial of degree 16 by dialytic elimination; the journal paper appeared in 1993.
prereqs: [inverse-kinematics, resultant, denavit-hartenberg-convention]
see_also: [six-r-inverse-kinematics-sixteen-solutions, sylvester-matrix, generalized-eigenvalue-problem, companion-matrix-method, homotopy-continuation, groebner-basis, pieper-criterion, paden-kahan-subproblems]
sources:
  - book: "Madhusudan Raghavan and Bernard Roth, Inverse kinematics of the general 6R manipulator and related linkages, Journal of Mechanical Design 115(3), 502-508, 1993"
    locator: the 14 equations, the elimination to a 12 by 12 matrix and the polynomial of degree 16
  - book: "Hong-You Lee and Chong-Gao Liang, Displacement analysis of the general spatial 7-link 7R mechanism, Mechanism and Machine Theory 23(3), 219-226, 1988"
    locator: the first reduction to a polynomial of degree 16 for the 7R loop, which is equivalent to the 6R arm
  - book: "Dinesh Manocha and John F. Canny, Efficient inverse kinematics for general 6R manipulators, IEEE Transactions on Robotics and Automation 10(5), 648-657, 1994"
    locator: the matrix polynomial of the elimination solved as an eigenvalue problem
---

The Raghavan-Roth method solves the [inverse kinematics](/inverse-kinematics/) of a general arm with six revolute joints (a 6R arm) in closed form, up to the roots of one polynomial.
It writes the pose equations as equations that are linear in products of sines and cosines, eliminates five joint angles by linear algebra, and is left with one polynomial of degree 16 in $x_3 = \tan(\theta_3/2)$.
Each real root then gives one solution, found by solving linear systems.
The key step is the dialytic elimination: multiply the equations by powers of a variable so that the products of the variables become unknowns of a square linear system, whose determinant must vanish.
The implementation here runs the same steps on a smaller problem, the position of a general 3R arm, where the final polynomial is a quartic.

## In plain words

An arm with six hinges in general position has no simple geometric shortcut.
The equations that say "the hand is at this pose" mix sines and cosines of all six angles.
The trick is to treat each product of sines and cosines as a new unknown.
Then most of the equations become linear, and linear equations can be combined to cancel unknowns.
After enough cancelling, only one angle is left, in one equation, a polynomial with at most 16 roots.
Find its roots, and walk back through the linear equations to get the other angles.
Some factors of the polynomial are false and must be removed first.

## The problem

**Input.** The Denavit-Hartenberg parameters of an arm with revolute joints and a target: for the 6R arm a full pose of the hand, for the 3R demo a point $p$ for the origin of frame 3.

**Output.** All joint vectors that reach the target.

The arm must be general: special arms, such as arms with a spherical wrist, make some matrices of the method singular, and they have simpler methods anyway, see the [Pieper criterion](/pieper-criterion/).

## The algorithm

The pseudocode shows the 3R position version that the implementation runs.
With $T_i = R_z(\theta_i)T_z(d_i)T_x(a_i)R_x(\alpha_i)$, the point is $p = R_z(\theta_1)g$ with $g$ free of $\theta_1$, and $h$ is the part that depends on $\theta_3$ only.

```pseudo id=main
RAGHAVAN-ROTH-3R(dh, p)
L1  from |p|^2 = |g|^2 and p_z = g_z: E_j: P_j c2 + Q_j s2 + K_j = 0 (j = 1, 2), with P_j, Q_j, K_j linear in (c3, s3)
L2  put c_i = (1 - x_i^2)/(1 + x_i^2), s_i = 2x_i/(1 + x_i^2) for i = 2, 3: E_j becomes A_j x2^2 + B_j x2 + C_j, coefficients of degree 2 in x3
L3  multiply each by 1 and by x2: M(x3) (x2^3, x2^2, x2, 1)^T = 0, with the 4 × 4 matrix M
L4  Δ(x3) ← det M(x3)                                   ▷ degree 8
L5  q(x3) ← Δ(x3) / (4 (h̃1^2 + h̃2^2))                  ▷ remove the extraneous factor; degree 4
L6  for each real root x3 of q
L7      θ3 ← 2 arctan x3; (c2, s2, 1) ∝ (P_1, Q_1, K_1) × (P_2, Q_2, K_2); θ2 ← atan2(s2, c2)
L8      θ1 ← atan2(p_y, p_x) - atan2(g_y, g_x)
L9  return the joint vectors that pass a forward kinematics check
```

**The 6R method.** Raghavan and Roth follow the same plan with more equations.

1. Write the loop equation so that $\theta_1$ and $\theta_2$ are on one side, and take the two vectors $\mathbf p$ (a position) and $\mathbf l$ (an axis) on each side.
From them form 14 scalar equations: the components of $\mathbf p$ and $\mathbf l$, the products $\mathbf p \cdot \mathbf p$ and $\mathbf p \cdot \mathbf l$, the vector $\mathbf p \times \mathbf l$, and the vector $(\mathbf p \cdot \mathbf p)\mathbf l - 2(\mathbf p \cdot \mathbf l)\mathbf p$.
These are linear in 8 products of the sines and cosines of $\theta_1, \theta_2$ and in 9 products of those of $\theta_4, \theta_5$, with coefficients that depend on $\theta_3$.
2. Eliminate the 8 products of $\theta_1, \theta_2$ by linear algebra: this leaves 6 equations in the 9 products of $\theta_4, \theta_5$.
3. Put $x_4 = \tan(\theta_4/2)$ and $x_5 = \tan(\theta_5/2)$, multiply the 6 equations by $x_4$, and get 12 equations that are linear in 12 power products, with a $12 \times 12$ matrix $\Sigma(x_3)$.
4. A solution needs $\det\Sigma(x_3) = 0$.
This determinant has degree 24 in $x_3$ and contains the factor $(1 + x_3^2)^4$, which has no real roots.
The rest is the polynomial of degree 16.
5. For each real root, a null vector of $\Sigma(x_3)$ gives $\theta_4$ and $\theta_5$, and linear equations give $\theta_1$, $\theta_2$ and $\theta_6$.

Manocha and Canny (1994) do not expand the determinant: they write $\Sigma(x_3)$ as a matrix polynomial of degree 2 and find its roots as the eigenvalues of a [generalized eigenvalue problem](/generalized-eigenvalue-problem/), which is much more accurate.

## Example

The 3R arm has $(a_1, \alpha_1, d_1) = (0.5\text{ m}, 120°, 0.5\text{ m})$, $(a_2, \alpha_2, d_2) = (0.5\text{ m}, 30°, 1.0\text{ m})$ and $(a_3, \alpha_3, d_3) = (1.5\text{ m}, 0°, 0\text{ m})$.
The target is the point that the joint vector $(1, -0.5, -1)$ rad reaches: $p = (0.209252, 1.203738, -1.059310)$ m.

- The determinant $\Delta(x_3)$ of the $4 \times 4$ matrix has degree 8.
- The extraneous factor is $\tilde h_1^2 + \tilde h_2^2 = 4 + 2.75x_3^2 + x_3^4$, which is positive for all real $x_3$.
- The quotient is the quartic $2.474388x_3^4 - 9.122939x_3^3 + 4.164800x_3^2 + 4.377061x_3 - 0.559587$.
- Its four roots are real: $x_3 = -0.546302$, $0.117923$, $1.207093$ and $2.908236$.

| $x_3$ | $\theta_1$ (rad) | $\theta_2$ (rad) | $\theta_3$ (rad) |
|---|---|---|---|
| -0.546302 | 1.000000 | -0.500000 | -1.000000 |
| 0.117923 | -2.125286 | -2.692609 | 0.234761 |
| 1.207093 | -2.873565 | 2.405672 | 1.757909 |
| 2.908236 | 2.098607 | 2.860655 | 2.479220 |

Forward kinematics puts each of the four joint vectors on $p$ to about $10^{-15}$ m.
The first row is the joint vector that made the target, and the other three are the other solutions.

## Correctness

The proof page proves, for the 3R version and a general arm, that the real roots of the quartic give exactly the solutions, one each.

- $|p|^2$ and $p_z$ do not depend on $\theta_1$, so they give two equations in $\theta_2$ and $\theta_3$, and $\theta_1$ follows from the other two.
- The two equations are linear in $(c_2, s_2)$; they have a solution on the unit circle exactly when $(h_1^2 + h_2^2)\,q = 0$, which is the condition on $\theta_3$.
- The determinant of the dialytic matrix is the resultant of the two quadratics in $x_2$, and it equals $4(\tilde h_1^2 + \tilde h_2^2)\tilde q$; the first factor is extraneous.
- The null vector of the $2 \times 3$ coefficient matrix gives $(c_2, s_2)$, so each root gives one solution.

For the 6R arm the same argument runs on the 14 equations, and Raghavan and Roth prove that the polynomial of degree 16 has the solutions among its roots; see the [16 solutions theorem](/six-r-inverse-kinematics-sixteen-solutions/) for the bound.

## Complexity

For a fixed arm type, every step has a fixed size, so the work is a constant.
In terms of the degree $d$ of the final polynomial, building the matrix costs a constant for a fixed number of joints, and finding all roots costs $\Theta(d^3)$ with a companion matrix or with the eigenvalue form of Manocha and Canny, whose matrices have size proportional to $d$, in the [real RAM](/real-ram/), counting a fixed number of QR iterations per eigenvalue, as is usual.
The back substitution costs $\Theta(1)$ per root.
For the 6R arm this is an eigenvalue problem of size 24, which runs in well under a millisecond.

## Properties

- **All solutions.** The method finds every solution, with no starting guess, unlike [Newton-Raphson inverse kinematics](/newton-raphson-inverse-kinematics/).
- **General arms only.** Special geometry makes some matrices singular; such arms need a special version or a different method.
- **Extraneous roots.** The determinant contains factors that give no solution, such as $(1 + x_3^2)^4$ for the 6R arm; they must be removed or the roots checked.
- **Half angle at $\pi$.** The angle $\theta_3 = \pi$ maps to $x_3 = \infty$ and shows up only as a drop of the degree.
- **Numerical accuracy.** Expanding the determinant into coefficients is badly conditioned; the eigenvalue form is the accurate way.

## Variants and improvements

- **Eigenvalue form.** Manocha and Canny (1994) solve the matrix polynomial as a generalized eigenvalue problem and get all solutions fast and accurately.
- **Lee and Liang.** Lee and Liang (1988) first reached a polynomial of degree 16, for the equivalent 7R closed loop.
- **Continuation.** [Homotopy continuation](/homotopy-continuation/), as in Tsai and Morgan (1985), tracks all solutions from a start system instead of eliminating.
- **Other elimination.** [Gröbner bases](/groebner-basis/) and other [resultants](/resultant/) give the same polynomial in other ways, with more cost.
- **Special arms.** When three axes meet or are parallel, the problem splits into smaller ones, see [kinematic decoupling](/kinematic-decoupling/) and the [Paden-Kahan subproblems](/paden-kahan-subproblems/).

## When to use it

Use the Raghavan-Roth method, in the eigenvalue form, when an arm with six revolute joints has no special geometry and all solutions are needed, for example in design studies of new arms or in offline planning that must choose among all poses.
For an arm with a spherical wrist, use the closed form of [kinematic decoupling](/kinematic-decoupling/); for one solution near the current pose, use [damped least squares](/damped-least-squares-inverse-kinematics/).

## Pitfalls

- **Expanding the determinant.** Forming the coefficients of the polynomial of degree 16 loses many digits; prefer the eigenvalue form.
- **Dividing by a factor.** Long division by an extraneous factor can be inaccurate when its leading coefficient is small; the implementation here uses a least squares division.
- **Near double roots.** Two solutions that are close give roots that rounding can push off the real axis; check by forward kinematics and with a tolerance.
- **Degenerate arms.** If $a_1 = 0$ or $\sin\alpha_1 = 0$ in the 3R version, the two equations no longer fix $\theta_2$, and the method needs a special case.

## Implementations

## History

Pieper (1968) solved arms with three intersecting axes in closed form and noted that the general 6R arm was much harder.
Duffy and Crane (1980) reduced the general 7R closed loop, equivalent to the 6R arm, to a polynomial of degree 32 in one half angle tangent, as the determinant of a $16 \times 16$ matrix.
Tsai and Morgan (1985) found 16 solutions by continuation and conjectured that 16 is the bound, and Primrose (1986) proved that there are at most 16.
Lee and Liang (1988) reached a polynomial of degree 16.
Raghavan and Roth presented their elimination in 1990 and published it in 1993; it is the form found in most texts.
Manocha and Canny (1994) turned it into an eigenvalue problem.

## References
