---
tag: J4J4WD
kind: algorithm
slug: arc-length-method
name: Arc-length method
aliases:
- Riks method
- Crisfield method
area: scientific-computing/finite-element-practice
level: advanced
summary: Traces nonlinear equilibrium paths through limit points by constraining the step length in load and displacement space together.
solves: [systems-of-nonlinear-equations]
model: real-ram
complexity:
  vars: {n: the number of unknowns, b: the half bandwidth of the tangent stiffness, s: the number of arc-length steps, j: the number of Newton iterations per step}
  time: {worst: "Θ(s j n b^2)"}
  space: {extra: "Θ(n b)"}
properties: {deterministic: true, iterative: true, passes_limit_points: true, passes_snap_back: true, local_convergence: "quadratic for the linearized constraint at a regular point"}
history:
  year: 1979
  people: [E. Riks, G. A. Wempner, M. A. Crisfield]
  note: Wempner in 1971 and Riks in 1979 added the arc length of the path as a constraint to the equilibrium equations. Crisfield in 1981 gave the spherical and cylindrical forms that most finite element codes use.
prereqs: [newton-method-for-systems, finite-element-method]
see_also: [homotopy-continuation, newton-raphson-method, return-mapping-algorithm, broyden-method, newmark-beta-method, finite-element-assembly]
sources:
  - paper: doi:10.1016/0020-7683(79)90081-7
    title: E. Riks, An incremental approach to the solution of snapping and buckling problems, International Journal of Solids and Structures 15(7) (1979) 529-551
    locator: the arc-length constraint on the load and displacement increment, with the linearized (normal plane) correction
  - paper: doi:10.1016/0045-7949(81)90108-5
    title: M. A. Crisfield, A fast incremental/iterative solution procedure that handles snap-through, Computers and Structures 13(1-3) (1981) 55-62
    locator: the cylindrical arc-length constraint, the quadratic for the load correction and the choice of its root
  - paper: doi:10.1016/0020-7683(71)90038-2
    title: G. A. Wempner, Discrete approximations related to nonlinear theories of solids, International Journal of Solids and Structures 7(11) (1971) 1581-1599
    locator: the arc length as a path parameter for nonlinear structural problems
  - book: isbn:9780471987734
    title: Ted Belytschko, Wing Kam Liu and Brian Moran, Nonlinear Finite Elements for Continua and Structures, Wiley, 2000
    locator: Chapter 6 (solution methods for equilibrium problems, load and arc-length continuation)
---

The arc-length method follows the equilibrium path of a nonlinear structure, $f_{\rm int}(u) = \lambda P$, as the load factor $\lambda$ and the displacements $u$ change together. Plain load control fixes $\lambda$ and solves for $u$ with [Newton's method](/newton-method-for-systems/), so it fails at a limit point, where the load reaches a maximum and the tangent stiffness becomes singular. The arc-length method treats $\lambda$ as an unknown and adds one scalar equation: each step must move a fixed distance $\Delta l$ along the path, measured in the combined space of displacement and load. With this constraint the bordered system stays regular at limit points, so the method passes through snap-through, where the load falls after a peak, and snap-back, where the displacement also turns back.

## In plain words

Push down on the top of a shallow arch. At first it resists more and more, then at some point it gives way and jumps through to the other side. A computer that raises the push in fixed amounts cannot follow what happens after the peak, because no nearby position can carry a larger push. The arc-length method does not choose the push in advance. It asks for the next state to be a fixed distance away along the curve of all balanced states, where the distance counts both the movement and the change in push. So it can go over the top of the curve, follow it down while the arch gives way, and come back up on the other side.

## The problem

**Input.** An internal force $f_{\rm int} : \mathbb R^n \to \mathbb R^n$ and its tangent stiffness $K_T(u) = \partial f_{\rm int} / \partial u$, a fixed load pattern $P \in \mathbb R^n$, a start point $(u_0, \lambda_0)$ on the path, an arc length $\Delta l > 0$, a scale $\psi \ge 0$ for the load term, a tolerance and a number of steps $s$.

**Output.** Points $(u_k, \lambda_k)$, $k = 0, \ldots, s$, with $\|f_{\rm int}(u_k) - \lambda_k P\| \le$ tol, such that each increment $(\Delta u, \Delta\lambda) = (u_{k+1} - u_k, \lambda_{k+1} - \lambda_k)$ satisfies

$$\Delta u^\top \Delta u + \psi^2 \Delta\lambda^2 P^\top P = \Delta l^2,$$

and the points follow the path forward (no increment turns back against the previous one).

The constraint with $\psi > 0$ is the spherical form. With $\psi = 0$ it is the cylindrical form of Crisfield, which measures only the displacement and is not affected by the units of the load.

## The algorithm

```pseudo id=main
ARC-LENGTH(f_int, K_T, P, u_0, lambda_0, dl, psi, s)
L1  (u, lambda) <- (u_0, lambda_0)
L2  repeat s times
L3      solve K_T(u) u_t = P                                    ▷ tangent direction
L4      Dlambda <- ± dl / sqrt(u_t . u_t + psi^2 P . P); Du <- Dlambda u_t   ▷ sign: same way as the last step
L5      loop
L6          g <- f_int(u + Du) - (lambda + Dlambda) P; if |g| <= tol then exit loop
L7          solve K_T(u + Du) [u_r, u_t] = [-g, P]
L8          choose the root d of |Du + u_r + d u_t|^2 + psi^2 (Dlambda + d)^2 P . P = dl^2 that keeps the step direction
L9          Du <- Du + u_r + d u_t; Dlambda <- Dlambda + d
L10     (u, lambda) <- (u + Du, lambda + Dlambda); record the point
L11 return the recorded points
```

**The quadratic of line L8.** With $w = \Delta u + u_r$ the constraint is $a\,d^2 + b\,d + c = 0$ with

$$a = u_t^\top u_t + \psi^2 P^\top P, \qquad b = 2\big(u_t^\top w + \psi^2 \Delta\lambda\,P^\top P\big), \qquad c = w^\top w + \psi^2 \Delta\lambda^2 P^\top P - \Delta l^2.$$

Of the two roots, take the one for which the new increment has the larger inner product with the old one (Crisfield 1981). The other root usually sends the step back to the point it came from. If the roots are not real, the step is too long for the local curvature: halve $\Delta l$ and repeat the step. The reference code does this.

**Riks variant.** In place of the quadratic, use the linear condition that the correction is normal to the predictor, $\Delta u_0^\top(u_r + d\,u_t) + \psi^2 \Delta\lambda_0\,d\,P^\top P = 0$. Then each iteration is Newton's method on the bordered system of $n + 1$ equations, and no root has to be chosen.

## Example

**The two-bar truss.** Two bars of axial stiffness $EA = 1$ go from $(\pm 1, 0)$ to the apex $(0, \tfrac12)$, with a downward load $\lambda$ at the apex. Let $w$ be the downward displacement of the apex, $y = \tfrac12 - w$, $l = \sqrt{1 + y^2}$ and $l_0 = \sqrt{5}/2 = 1.1180$. The vertical force of the two bars is

$$f_{\rm int}(w) = 2\,EA\,y\,\Big(\frac1l - \frac1{l_0}\Big), \qquad K_T(w) = -2\,EA\Big(\frac{1}{l^3} - \frac1{l_0}\Big).$$

At $w = 0$, $K_T = 0.35777$. The load has a maximum where $l^3 = l_0$, at $w = 0.22212$ with $\lambda = 0.038384$. For larger loads there is no equilibrium near the start, so load control fails there. The apex then snaps through: the force is zero again at $w = \tfrac12$ (both bars horizontal), negative down to $\lambda = -0.038384$ at $w = 0.77788$, zero at $w = 1$ (the mirror image of the start), and rising after that.

**The first step.** With $\Delta l = 0.1$ and $\psi = 1$, line L3 gives $u_t = 1/0.35777 = 2.7951$ and line L4 gives $\Delta\lambda = 0.1/\sqrt{2.7951^2 + 1} = 0.033686$ and $\Delta u = 0.094155$. The residual of line L6 is $-0.0075738$, because the path bends below its tangent. Two corrections bring the residual below $10^{-10}$, at $w = 0.0964$, $\lambda = 0.02655$.

**The whole path.** Twelve steps with $\Delta l = 0.1$ give the points below. The reference code records them, and each needs two Newton corrections.

| step | $w$ | $\lambda$ | step | $w$ | $\lambda$ |
|---|---|---|---|---|---|
| 1 | 0.0964 | 0.02655 | 7 | 0.6897 | -0.03341 |
| 2 | 0.1958 | 0.03789 | 8 | 0.7896 | -0.03829 |
| 3 | 0.2957 | 0.03487 | 9 | 0.8892 | -0.02918 |
| 4 | 0.3948 | 0.02106 | 10 | 0.9861 | -0.00479 |
| 5 | 0.4928 | 0.00151 | 11 | 1.0786 | 0.03339 |
| 6 | 0.5908 | -0.01843 | 12 | 1.1657 | 0.08253 |

The steps pass the maximum between steps 2 and 3 and the minimum near step 8 with no special treatment. The largest sampled load misses the exact peak by $O(\Delta l^2)$: the measured gaps are $1.2 \times 10^{-4}$, $3.0 \times 10^{-5}$ and $8.2 \times 10^{-6}$ for $\Delta l = 0.04$, $0.02$ and $0.01$.

**Snap-back.** Put a spring of stiffness $k = 0.1$ between the apex and the loaded point. Then the loaded point moves $z = w + \lambda/k$. The truss softens with a slope down to $-0.2111$ at $w = \tfrac12$, which is steeper than $-k$, so on part of the path $z$ decreases while the path goes on. Load control and control by $z$ both fail there. The arc-length method with two unknowns follows the whole curve (`test_snap_back_with_a_soft_spring`).

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **Each recorded point is in equilibrium (theorem).** Line L10 is reached only after the test of line L6 succeeds.
- **The constraint holds exactly at every iterate (theorem).** The predictor of line L4 satisfies it by its choice of $\Delta\lambda$, and line L9 adds a correction whose $d$ is a root of the constraint quadratic.
- **The bordered system is regular at a limit point (theorem).** At a point where $K_T$ is singular with a one-dimensional null space spanned by $\phi$, and $\phi^\top P \ne 0$ (a limit point, not a bifurcation point), the $(n + 1) \times (n + 1)$ matrix of the equilibrium equations and the linearized constraint is nonsingular when the step direction is not orthogonal to the path tangent. So the Riks iteration is Newton's method on a regular system and converges locally quadratically. For Crisfield's quadratic form the local convergence is a standard result (Crisfield 1981) that the proof only sketches.
- **The method cannot be trusted at a bifurcation point.** If $\phi^\top P = 0$, the bordered matrix is singular at the point for every constraint, and the steps may follow either branch without warning.

## Complexity

In the [real-RAM model](/real-ram/), each Newton iteration assembles $K_T$ and factors it once. For a banded matrix with half bandwidth $b$ this costs $\Theta(n b^2)$. The two right sides of line L7 share the factor and cost $\Theta(n b)$, and the quadratic costs $\Theta(n)$. So $s$ steps with $j$ iterations each cost $\Theta(s j n b^2)$, the same as load control with the same number of iterations. The extra memory is one more vector of length $n$, so $\Theta(n b)$ for the factor. The number $j$ is a measurement, not a bound: it is 2 for the truss and at most 3 for the truss with a spring in the reference tests, with $\Delta l$ between 0.02 and 0.1. The reference code uses dense Gaussian elimination and is meant only for small systems.

## Properties

- **One extra scalar unknown.** The tangent matrix keeps its sparsity and symmetry, because line L7 solves with $K_T$ alone and the bordering is done by the two right sides.
- **Works when $K_T$ is singular at isolated points**, as at limit points, as long as the iterates do not land exactly on them.
- **The step size is a length, not a load.** Near a limit point the load changes little and the displacement a lot, so the method takes small load steps where they are needed without any rule for it.
- **Sign of the predictor.** The sign of $\Delta\lambda$ at line L4 changes when the path passes a limit point. The rule "same direction as the last increment" handles this, while the rule "sign of $\det K_T$" fails at bifurcation points.

## Variants and improvements

- **Riks normal plane and Ramm updated normal plane.** Linearize the constraint about the predictor (Riks) or about the current iterate (Ramm). Then no quadratic root has to be chosen, at the price of a slightly different step length.
- **Crisfield cylindrical ($\psi = 0$) and spherical ($\psi > 0$).** The cylindrical form is the default in many codes because the load and the displacement have different units.
- **Adaptive arc length.** Scale $\Delta l$ by the ratio of a target number of iterations to the actual number, for example $\Delta l_{\rm new} = \Delta l\,\sqrt{j_{\rm target}/j}$.
- **Local or indirect displacement control.** For problems with localized damage, measure the arc length only on a few chosen degrees of freedom, such as a crack mouth opening.
- **Pseudo-arclength continuation in numerical analysis.** Keller's method is the same idea for general parameter dependent equations $G(x, \lambda) = 0$, with the normal plane constraint. See [homotopy continuation](/homotopy-continuation/) for path following toward the roots of polynomial systems.

## When to use it

Use it for quasi-static nonlinear structural problems where the load reaches a maximum or the response turns back: buckling of shallow shells and arches, snap-through of trusses, post-peak softening in concrete and composites, and contact problems with a load drop. When the load only increases, plain load control with Newton's method is simpler. When the path has a bifurcation, add a check of the sign and the number of negative pivots of $K_T$, and perturb the structure or switch branches on purpose.

## Pitfalls

- **Wrong root.** Choosing the root of line L8 by the smaller absolute value, or by sign, can send the path back on itself, which looks like a loop of converged points.
- **Steps that are too long.** Near a sharp turn of the path the quadratic has no real root, or Newton converges to a far part of the path. Halve the step and retry.
- **Units in the spherical form.** With $\psi = 1$ the constraint adds a displacement squared and a load squared. If the load is in newtons and the displacements in metres, the load term dominates and the method behaves like load control. Scale $\psi$ or use the cylindrical form.
- **Bifurcation is not a limit point.** At a symmetric bifurcation $\phi^\top P = 0$, and the method passes the point on the primary path without noticing the secondary path. Monitor the number of negative pivots of $K_T$.
- **Path dependent materials.** For plasticity or damage, the internal force depends on the history. Each step must start from the converged state of the last step, and the iterations within a step must not update the history. See the [return mapping algorithm](/return-mapping-algorithm/).

## Implementations

## History

Wempner in 1971 used the arc length of the equilibrium path as a parameter for nonlinear structural problems. Riks in 1979 gave an incremental method that adds the arc-length constraint and solves with Newton corrections normal to the predictor, for snapping and buckling problems. Crisfield in 1981 gave the cylindrical form with a quadratic for the load correction and a rule to choose its root, and showed it on snap-through problems. Ramm in 1981 gave the updated normal plane variant. In numerical analysis Keller developed the same idea as pseudo-arclength continuation in 1977.

## References
