---
tag: DM08Z2
kind: algorithm
slug: dgkf-h-infinity-synthesis
name: Two-Riccati H-infinity synthesis
aliases:
- DGKF solution
- Doyle-Glover-Khargonekar-Francis solution
area: control/robust-and-adaptive-control
level: advanced
summary: Solves the suboptimal H-infinity problem by two Riccati equations and a coupling condition on their spectral radius.
solves: [h-infinity-control-problem]
model: real-ram
complexity:
  vars: {n: the number of plant states, m: the number of inputs w and u together, p: the number of outputs z and y together, c: the number of Newton steps of one matrix sign function, k: the number of bisection steps on gamma}
  time: {per-gamma: "O(c n^3 + n^2 (m + p))", total: "O(k (c n^3 + n^2 (m + p)))"}
  space: {extra: "O(n^2 + n (m + p))"}
properties: {deterministic: true, exact: false, recursive: false, iterative: true}
history:
  year: 1989
  people: [John C. Doyle, Keith Glover, Pramod P. Khargonekar, Bruce A. Francis]
  note: "Doyle, Glover, Khargonekar and Francis (1989) gave the state-space solution of the standard H-infinity problem with two Riccati equations of the same size as the plant, after Glover and Doyle (1988) parametrized all suboptimal controllers."
prereqs: [h-infinity-control-problem, continuous-algebraic-riccati-equation, hamiltonian-matrix, linear-fractional-transformation]
see_also: [lmi-h-infinity-synthesis, h-infinity-loop-shaping, mixed-sensitivity-design, dk-iteration, h2-optimal-control, h-infinity-norm-computation, bounded-real-lemma, stabilizing-riccati-solution-theorem]
sources:
  - paper: doi:10.1109/9.29425
    title: John C. Doyle, Keith Glover, Pramod P. Khargonekar and Bruce A. Francis, State-space solutions to standard H2 and H-infinity control problems, IEEE Transactions on Automatic Control 34(8), 831-847, 1989
    locator: the normalized output feedback problem, its assumptions, the three conditions on X and Y, and the central controller
  - paper: doi:10.1016/0167-6911(88)90055-2
    title: Keith Glover and John C. Doyle, State-space formulae for all stabilizing controllers that satisfy an H-infinity norm bound and relations to risk sensitivity, Systems and Control Letters 11(3), 167-172, 1988
    locator: the parametrization of all suboptimal controllers and the link to risk-sensitive control
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 16, H-infinity Control, Simple Case (the theorem and the central controller), and Chapter 17, H-infinity Control, General Case (loop shifting for general D matrices)
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Section 9.3.4, H-infinity optimal control (the formulas and the gamma iteration as used in design)
  - book: isbn:9780898716467
    title: Nicholas J. Higham, Functions of Matrices, Theory and Computation, SIAM, 2008
    locator: Chapter 5, Matrix Sign Function (the scaled Newton iteration and its convergence)
---

Two-Riccati H-infinity synthesis solves the [H-infinity control problem](/h-infinity-control-problem/) for a generalized plant in state-space form. For a level $\gamma > 0$ it either builds an internally stabilizing output feedback controller $K$ whose closed loop map from the disturbance $w$ to the error $z$ has [H-infinity norm](/h-infinity-norm/) below $\gamma$, or it proves that no controller of any order can do this. The test needs two [continuous algebraic Riccati equations](/continuous-algebraic-riccati-equation/) of the same size $n$ as the plant: a control equation for $X$ and a filter equation for $Y$. A controller exists if and only if both have stabilizing solutions $X \ge 0$ and $Y \ge 0$ and the spectral radius of $XY$ is below $\gamma^2$. Doyle, Glover, Khargonekar and Francis (1989) proved this, and the method is often called the DGKF solution. A bisection on $\gamma$ then finds the optimal level $\gamma_{\rm opt}$ to any wanted accuracy. The controller has the structure of an observer with state feedback, as in [LQG control](/lqg-control/), and it tends to the LQG controller as $\gamma \to \infty$.

## In plain words

You have a plant, a list of disturbances $w$ that act on it, and a list of errors $z$ that you want small. You fix a number $\gamma$ and ask: is there a controller that keeps the energy of $z$ below $\gamma$ times the energy of $w$, for every disturbance? The answer comes from two Riccati equations, one for state feedback and one for state estimation, as in LQG. If both have the right kind of solution, and the two solutions are not too large together, the answer is yes, and a formula gives the controller. If not, no controller exists, of any order. Try smaller and smaller $\gamma$ by bisection to find the best level.

## The problem

The generalized plant has state $x \in \mathbb{R}^n$, disturbance $w$, control input $u$, error $z$ and measurement $y$:

$$\dot x = A x + B_1 w + B_2 u, \qquad z = C_1 x + D_{12} u, \qquad y = C_2 x + D_{21} w.$$

The controller is a finite-dimensional linear system with input $y$ and output $u$, and the loop is closed by $u = K y$ with no sign change. This is the lower [linear fractional transformation](/linear-fractional-transformation/) $T_{zw} = \mathcal{F}_l(P, K)$. A classical loop with $e = r - y$ and $u = C e$ has $K = -C$. The page uses the normalized form of the original paper. The assumptions are:

1. $(A, B_1)$ is [stabilizable](/stabilizability/) and $(C_1, A)$ is [detectable](/detectability/).
2. $(A, B_2)$ is stabilizable and $(C_2, A)$ is detectable.
3. $D_{12}^T \begin{bmatrix} C_1 & D_{12} \end{bmatrix} = \begin{bmatrix} 0 & I \end{bmatrix}$: the control input enters every direction of $z$ that it can reach, with unit weight, and with no cross term with the state.
4. $\begin{bmatrix} B_1 \\ D_{21} \end{bmatrix} D_{21}^T = \begin{bmatrix} 0 \\ I \end{bmatrix}$: every measurement has unit noise, independent of the process disturbance.
5. $D_{11} = 0$ and $D_{22} = 0$.

Assumptions 3 and 4 imply that $D_{12}$ has full column rank and $D_{21}$ has full row rank. Together with assumption 1 they also imply the rank conditions on the imaginary axis: $\begin{bmatrix} A - j\omega I & B_2 \\ C_1 & D_{12} \end{bmatrix}$ has full column rank and $\begin{bmatrix} A - j\omega I & B_1 \\ C_2 & D_{21} \end{bmatrix}$ has full row rank for every real $\omega$. A plant with general $D$ matrices that satisfy the rank conditions is brought to this form by scaling and loop shifting (Zhou, Doyle and Glover 1996, chapter 17).

For $\gamma > 0$ define the two Hamiltonian matrices

$$H_\infty = \begin{bmatrix} A & \gamma^{-2} B_1 B_1^T - B_2 B_2^T \\ -C_1^T C_1 & -A^T \end{bmatrix}, \qquad J_\infty = \begin{bmatrix} A^T & \gamma^{-2} C_1^T C_1 - C_2^T C_2 \\ -B_1 B_1^T & -A \end{bmatrix}.$$

$X = \mathrm{Ric}(H_\infty)$ means: $H_\infty$ has no eigenvalue on the imaginary axis, its stable invariant subspace is the range of $\begin{bmatrix} I \\ X \end{bmatrix}$, and then $X$ is symmetric, solves $A^T X + X A + X(\gamma^{-2} B_1 B_1^T - B_2 B_2^T)X + C_1^T C_1 = 0$, and makes $A + (\gamma^{-2} B_1 B_1^T - B_2 B_2^T) X$ [Hurwitz](/hurwitz-matrix/). The same holds for $Y = \mathrm{Ric}(J_\infty)$ with the dual equation.

**Theorem** (Doyle, Glover, Khargonekar and Francis 1989; Zhou, Doyle and Glover 1996, chapter 16). Under assumptions 1 to 5, an internally stabilizing controller with $\|T_{zw}\|_\infty < \gamma$ exists if and only if

1. $X = \mathrm{Ric}(H_\infty)$ exists and $X \ge 0$,
2. $Y = \mathrm{Ric}(J_\infty)$ exists and $Y \ge 0$,
3. $\rho(XY) < \gamma^2$, where $\rho$ is the spectral radius.

When they hold, one such controller is the central controller

$$\dot{\hat x} = \hat A \hat x - Z L y, \qquad u = F \hat x,$$

with $F = -B_2^T X$, $L = -Y C_2^T$, $Z = (I - \gamma^{-2} Y X)^{-1}$ and $\hat A = A + \gamma^{-2} B_1 B_1^T X + B_2 F + Z L C_2$. It has $n$ states.

## The algorithm

```pseudo id=main
DGKF-SYNTHESIS(A, B1, B2, C1, C2, tol, delta)
L1  lo ← 0, hi ← 1
L2  while not FEASIBLE(hi) do lo ← hi, hi ← 2 hi
L3  while hi - lo > tol · hi do
L4      g ← (lo + hi) / 2
L5      if FEASIBLE(g) then hi ← g else lo ← g
L6  g ← (1 + delta) · hi                        ▷ back off from the optimum
L7  (X, Y) ← the solutions found by FEASIBLE(g)
L8  F ← -B2^T X, L ← -Y C2^T, Z ← (I - g^-2 Y X)^-1
L9  Â ← A + g^-2 B1 B1^T X + B2 F + Z L C2
L10 return hi, controller (Â, -Z L, F, 0)

FEASIBLE(g)
L11 X ← Ric(H∞(g)); fail if it does not exist or X is not ≥ 0
L12 Y ← Ric(J∞(g)); fail if it does not exist or Y is not ≥ 0
L13 return ρ(X Y) < g^2
```

**Computing Ric.** The implementation forms the $2n \times 2n$ Hamiltonian $H$ and computes its matrix sign function $W = \mathrm{sign}(H)$ by the scaled Newton iteration $W \leftarrow \tfrac12(\mu W + \mu^{-1} W^{-1})$ with $\mu = |\det W|^{-1/(2n)}$. The iteration converges when $H$ has no eigenvalue on the imaginary axis. The stable invariant subspace of $H$ is the kernel of $W + I$. Split $W + I$ into $n \times n$ blocks. Then $(W + I)\begin{bmatrix} I \\ X \end{bmatrix} = 0$ gives the overdetermined linear system

$$\begin{bmatrix} W_{12} \\ W_{22} + I \end{bmatrix} X = -\begin{bmatrix} W_{11} + I \\ W_{21} \end{bmatrix},$$

which the code solves by the normal equations. The code then makes $X$ symmetric, and it accepts $X$ only if the Riccati residual is below $10^{-7}$ times the size of the terms and $A + R X$ is Hurwitz. These checks catch a stable subspace that is not the range of some $\begin{bmatrix} I \\ X \end{bmatrix}$. A production code uses the ordered [Schur decomposition](/schur-decomposition/) of $H$ instead, as in the [Schur method](/schur-method-riccati/); the sign function keeps the code short.

## Example

Take the scalar plant $\dot x = x + w_1 + u$ with errors $z = (x, u)$ and measurement $y = x + w_2$. So $A = 1$, $B_1 = [1, 0]$, $B_2 = 1$, $C_1 = [1; 0]$, $D_{12} = [0; 1]$, $C_2 = 1$ and $D_{21} = [0, 1]$. All five assumptions hold. With $c = 1 - \gamma^{-2}$ the control equation is $-c X^2 + 2X + 1 = 0$, and the filter equation is the same, so $Y = X$. For $c > 0$ the stabilizing root is $X = (1 + \sqrt{1 + c})/c$, and condition 3 is $X^2 < \gamma^2$.

| $\gamma$ | $X = Y$ | $\rho(XY)$ | $\gamma^2$ | feasible |
|---|---|---|---|---|
| 2.5 | 2.80532 | 7.86980 | 6.25 | no |
| 2.7 | 2.74082 | 7.51212 | 7.29 | no |
| 2.75 | 2.72730 | 7.43815 | 7.5625 | yes |
| 3 | 2.67116 | 7.13512 | 9 | yes |

Conditions 1 and 2 hold for every $\gamma > 1$ here; only the coupling condition fails for small $\gamma$. Set $X = \gamma$ and solve: $c\gamma - 1 = \sqrt{1 + c}$ gives $c\gamma^2 - 2\gamma = 1$, so $\gamma^2 - 2\gamma - 2 = 0$ and $\gamma_{\rm opt} = 1 + \sqrt 3 = 2.73205$. In general $\gamma_{\rm opt} = a + \sqrt{a^2 + 2}$ for $A = a$, and bisection in the code reproduces this to six digits for $a = -1, 0, 1, 2$.

At $\gamma = 3$: $F = -2.67116$, $L = -2.67116$, $Z = 4.82603$, $\hat A = -14.26554$ and $-ZL = 12.89117$. The controller is

$$K(s) = \frac{-34.43444}{s + 14.26554},$$

with $K(0) = -2.41383$. The closed loop poles are $-11.51383$ and $-1.75171$, so the loop is internally stable. A frequency sweep of the $2 \times 2$ closed loop map gives its largest singular value $2.98632$ at $\omega = 0$, below $\gamma = 3$, as the theorem says.

## Correctness

The theorem gives the meaning of FEASIBLE: it returns true at $g$ if and only if some controller reaches $\|T_{zw}\|_\infty < g$. That set of levels is closed upward, so it is the open interval $(\gamma_{\rm opt}, \infty)$. Bisection keeps the invariant that `lo` is infeasible (or 0) and `hi` is feasible, so after the loop $\gamma_{\rm opt} \in [\text{lo}, \text{hi}]$ and $\text{hi} - \text{lo} \le \text{tol} \cdot \text{hi}$. The Riccati routine returns the stabilizing solution or nothing, because a stabilizing solution is unique and the code checks the equation and the Hurwitz property directly. The central controller at $(1 + \delta)\,\text{hi}$ meets the bound by the theorem. The proofs of the bisection invariant, of the subspace step and of the scalar formula are in [proofs/correctness.md](proofs/correctness.md); the theorem itself is cited.

The proof of the theorem in Zhou, Doyle and Glover (1996, chapter 16) has two parts. Sufficiency: with $u = F x$ and the worst disturbance $w = \gamma^{-2} B_1^T X x$, a completion of squares shows that $\|z\|_2^2 - \gamma^2 \|w\|_2^2$ splits into a term that the controller can cancel and a term that only depends on an estimation error. This reduces the output feedback problem to an estimation problem for a modified plant, whose Riccati solution is $Y(I - \gamma^{-2} X Y)^{-1}$; this is where $\rho(XY) < \gamma^2$ appears. Necessity goes through the same split into a full information problem and an output estimation problem, which is the H-infinity form of the separation principle. The [bounded real lemma](/bounded-real-lemma/) links the norm bound to the Riccati equations in each step.

## Complexity

Let $n$ be the number of states, $m$ the number of inputs $(w, u)$ and $p$ the number of outputs $(z, y)$. In the real-RAM model with dense factorizations at $O(n^3)$ flops, one test of FEASIBLE forms the Hamiltonians in $O(n^2(m + p))$ and computes two sign functions, each with $c$ Newton steps of $O(n^3)$. Near convergence the Newton iteration converges quadratically (Higham 2008, chapter 5); $c$ depends on how close the eigenvalues of $H$ are to the imaginary axis, so it is not bounded by a function of $n$ alone. The bisection needs $k = \lceil \log_2(\text{hi}_0 / (\text{tol} \cdot \gamma_{\rm opt})) \rceil$ tests, up to a constant. The total is $O(k(c n^3 + n^2(m + p)))$ time and $O(n^2 + n(m + p))$ extra space. The controller itself costs $O(n^3)$ once.

## Properties

- The test is exact in real arithmetic: it decides the existence of a controller of any order, not only of order $n$.
- The central controller has the same order $n$ as the generalized plant, which includes the weights.
- As $\gamma \to \infty$, $X$ and $Y$ tend to the solutions of the LQR and Kalman filter Riccati equations, $Z \to I$, and the central controller tends to the [H2-optimal](/h2-optimal-control/) (LQG) controller. In the example, the static gain $K(0) = -2.414$ at $\gamma = 3$ is already close to the LQR gain $1 + \sqrt 2 = 2.41421$ of the scalar problem with $a = b = q = r = 1$.
- The controller is observer-based: $\hat x$ estimates the state under the worst-case disturbance $\gamma^{-2} B_1^T X x$.
- Every suboptimal controller is $K = \mathcal{F}_l(K_a, Q)$ for a fixed system $K_a$ and some stable $Q$ with $\|Q\|_\infty < \gamma$ (Glover and Doyle 1988). $Q = 0$ gives the central controller.

## Variants and improvements

- **General D matrices.** Loop shifting and scaling remove $D_{11}$ and normalize $D_{12}$ and $D_{21}$, at the price of a condition on $\gamma$ from $D_{11}$ (Zhou, Doyle and Glover 1996, chapter 17).
- **Singular problems.** If $D_{12}$ or $D_{21}$ loses rank, or the plant has zeros on the imaginary axis, the Riccati approach fails. [LMI-based H-infinity synthesis](/lmi-h-infinity-synthesis/) needs no rank assumptions.
- **Discrete time.** The same structure holds with two discrete Riccati equations and a coupling condition; the formulas are longer.
- **Special structure.** [H-infinity loop shaping](/h-infinity-loop-shaping/) has a closed form for the optimal level, so no bisection is needed.
- **Design use.** [Mixed sensitivity design](/mixed-sensitivity-design/) builds the generalized plant from weights; [D-K iteration](/dk-iteration/) calls this algorithm once per iteration on a scaled plant.

## When to use it

Use it when the plant model is linear and finite-dimensional, the requirements can be written as a bound on the H-infinity norm of a weighted closed loop map, and the normalization assumptions hold or can be reached by loop shifting. It is fast and gives the exact optimal level up to the bisection tolerance. If the assumptions fail, or extra constraints such as pole regions or several objectives are needed, use the LMI method. If the controller must have a low fixed order, neither method applies directly; that problem is harder (see the [problem page](/h-infinity-control-problem/)).

## Pitfalls

- **Controller at the optimum.** As $\gamma \to \gamma_{\rm opt}$ with coupling active, $I - \gamma^{-2} Y X$ becomes singular and the central controller gets very fast poles. In the example the controller pole is at $-14.3$ for $\gamma = 3$ and at $-111$ for $\gamma = 1.01\,\gamma_{\rm opt}$. Back off a few percent; the choice of $\delta$ is a rule of thumb.
- **Forgetting X ≥ 0.** The Riccati equation can have a stabilizing solution that is not positive semidefinite. Then the test fails, even if the coupling condition holds.
- **Imaginary axis eigenvalues.** Near the boundary of condition 1 or 2, the Hamiltonian has eigenvalues close to the imaginary axis, and the sign iteration or the Schur method loses accuracy. A floating point decision near $\gamma_{\rm opt}$ can be wrong in either direction; the bisection result is accurate to about the size of this region.
- **Normalization.** The formulas above are only valid in the normalized form. Applying them to a plant with $D_{12}^T D_{12} \ne I$ or $D_{12}^T C_1 \ne 0$ gives wrong answers without any warning.
- **Sign conventions.** The controller is wired as $u = K y$. Books on loop shaping use positive feedback, and classical loops use $u = C(r - y)$; check the sign before using a controller from another source.
- **Weights in the plant.** The order of the controller is the order of the plant plus all weights. High order weights give high order controllers, which may need [model order reduction](/model-order-reduction/).

## Implementations

## History

Zames (1981) posed the problem of minimizing a weighted sensitivity in the H-infinity norm. The first solutions in the early 1980s used the [Youla parametrization](/youla-parametrization/) and Nehari or Nevanlinna-Pick interpolation, and they gave controllers of high order. Glover and Doyle (1988) gave state-space formulas for all suboptimal controllers. Doyle, Glover, Khargonekar and Francis (1989) gave the full proof of the two-Riccati solution, together with the H2 case, in one paper. The LMI approach of Gahinet and Apkarian (1994) and Iwasaki and Skelton (1994) later removed the rank assumptions.

## References
