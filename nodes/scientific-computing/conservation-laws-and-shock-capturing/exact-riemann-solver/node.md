---
tag: P7B1QH
kind: algorithm
slug: exact-riemann-solver
name: Exact Riemann solver for the Euler equations
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: Finds the star-region pressure by Newton iteration on the shock and rarefaction relations, then samples the self-similar solution.
solves: [riemann-problem]
model: real-ram
complexity:
  vars: {k: "the number of Newton iterations for the star pressure"}
  time: {worst: "O(k)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, exact: true, iterative: true, detects_vacuum: true}
history:
  year: 1959
  people: [S. K. Godunov, E. F. Toro]
  note: Godunov (1959) used exact solutions of the gas dynamics Riemann problem inside his scheme. Toro's book gives the form used here, Newton iteration on one pressure function.
prereqs: [riemann-problem, euler-equations-of-gas-dynamics, newton-raphson-method]
see_also: [godunov-method, roe-solver, hll-riemann-solver, hllc-riemann-solver, rankine-hugoniot-conditions, lax-entropy-condition, bisection-method, shallow-water-equations]
sources:
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Chapter 4 (Sections 4.2 equations for pressure and particle velocity, 4.3 numerical solution for pressure, 4.4 the complete solution, 4.5 sampling the solution, 4.6 vacuum)
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 14 (Sections 14.8 to 14.13, the Riemann problem for the Euler equations, Riemann invariants, the structure of rarefaction waves, shock tubes)
  - paper: "S. K. Godunov, A difference method for numerical calculation of discontinuous solutions of the equations of hydrodynamics, Matematicheskii Sbornik 47(89) (1959) 271-306"
    locator: the scheme with exact Riemann solutions at the cell faces
---

The exact Riemann solver computes the exact solution of the [Riemann problem](/riemann-problem/) for the [Euler equations](/euler-equations-of-gas-dynamics/) of an ideal gas: two constant gas states that meet at $x = 0$ at time $0$. The Riemann problem page states the problem and its wave structure; this page is the algorithm that solves it for gas dynamics. The solver reduces the problem to one scalar equation $f(p) = 0$ for the pressure $p^*$ between the two outer waves, solves it by Newton iteration, and then evaluates the solution at any point $x/t$. [Godunov's method](/godunov-method/) uses it to get the flux at each cell face. The [Roe](/roe-solver/), [HLL](/hll-riemann-solver/) and [HLLC](/hllc-riemann-solver/) solvers are approximate solvers that replace the iteration by a closed form.

## In plain words

Put a thin wall in a long tube. On one side there is gas at high pressure, and on the other side gas at low pressure. Remove the wall. Three waves move away from the wall position. On the outside there is a shock or a smooth expansion on each side, and in the middle there is a contact surface that separates the two gases. Between the outer waves, the pressure and the speed are the same on both sides of the contact. The solver finds this middle pressure first. For a trial pressure, the shock rules and the expansion rules each give the speed that the gas on each side would have. The solver adjusts the trial pressure until the two speeds agree. Then it knows every wave, and it can give the gas state at any place and time.

## The problem

Given $\gamma > 1$ and two primitive states $W_L = (\rho_L, u_L, p_L)$ and $W_R = (\rho_R, u_R, p_R)$ with positive density and pressure, find the entropy solution of

$$U_t + F(U)_x = 0, \qquad U = (\rho, \rho u, E), \quad F(U) = (\rho u, \rho u^2 + p, u(E + p)), \quad E = \frac{p}{\gamma - 1} + \frac12\rho u^2,$$

with $U = U_L$ for $x < 0$ and $U = U_R$ for $x > 0$ at $t = 0$. The solution is self-similar, $U(x, t) = W(x/t)$, so the output is a procedure that returns $W(\xi)$ for any $\xi = x/t$. The sound speed is $c = \sqrt{\gamma p/\rho}$.

## The algorithm

Let $z = (\gamma - 1)/(2\gamma)$. For each side $K \in \{L, R\}$ the wave function is

$$f_K(p) = \begin{cases} (p - p_K)\sqrt{\dfrac{A_K}{p + B_K}}, & p > p_K \text{ (shock)}, \\[2mm] \dfrac{2c_K}{\gamma - 1}\Big(\big(\tfrac{p}{p_K}\big)^{z} - 1\Big), & p \le p_K \text{ (rarefaction)}, \end{cases} \qquad A_K = \frac{2}{(\gamma + 1)\rho_K}, \quad B_K = \frac{\gamma - 1}{\gamma + 1}p_K.$$

The star pressure is the root of $f(p) = f_L(p) + f_R(p) + u_R - u_L$.

```pseudo id=main
EXACT-RIEMANN(W_L, W_R, γ, tol)
L1  if (2/(γ-1))(c_L + c_R) ≤ u_R - u_L then report a vacuum and stop
L2  p ← ((c_L + c_R - (γ-1)(u_R - u_L)/2) / (c_L/p_L^z + c_R/p_R^z))^(1/z)     ▷ the two-rarefaction guess
L3  repeat
L4      compute f(p) and f'(p) from f_L and f_R
L5      p_new ← p - f(p)/f'(p)
L6      if p_new ≤ 0 then p_new ← tol · min(p_L, p_R)
L7      δ ← 2|p_new - p|/(p_new + p); p ← p_new
L8  until δ < tol
L9  u* ← (u_L + u_R)/2 + (f_R(p) - f_L(p))/2
L10 for each side K with p > p_K: star density ρ*_K = ρ_K (p/p_K + g)/(g p/p_K + 1) with g = (γ-1)/(γ+1), and shock speed u_K ∓ c_K sqrt(((γ+1)/(2γ)) p/p_K + z)
L11 for each side K with p ≤ p_K: ρ*_K = ρ_K (p/p_K)^(1/γ), head speed u_K ∓ c_K, tail speed u* ∓ c_K (p/p_K)^z
SAMPLE(ξ)
L12 K ← L if ξ ≤ u*, else K ← R
L13 if ξ is outside the K wave then return W_K
L14 if ξ is between the K wave and the contact then return (ρ*_K, u*, p)
L15 return the state inside the K fan at ξ
```

The upper sign in $\mp$ is for the left side. Inside the left fan the state is $c = c_Lw$ with $w = \frac{2}{\gamma + 1} + \frac{\gamma - 1}{(\gamma + 1)c_L}(u_L - \xi)$, $u = \frac{2}{\gamma + 1}\big(c_L + \frac{\gamma - 1}{2}u_L + \xi\big)$, $\rho = \rho_Lw^{2/(\gamma - 1)}$ and $p = p_Lw^{2\gamma/(\gamma - 1)}$. The right fan is the mirror image.

## Example

**Sod's shock tube**, $\gamma = 1.4$, $W_L = (1, 0, 1)$ and $W_R = (0.125, 0, 0.1)$. The sound speeds are $c_L = 1.18322$ and $c_R = 1.05830$. The vacuum test passes, because $\frac{2}{0.4}(c_L + c_R) = 11.2$ is larger than $u_R - u_L = 0$. The guess of line L2 is $p_0 = 0.306767$. The Newton iterates are $0.303113$, $0.30313018$ and $0.3031301781$, with relative changes $1.2 \times 10^{-2}$, $5.6 \times 10^{-5}$ and $1.2 \times 10^{-9}$, and the fourth step stops the loop.

You can check the root by hand. At $p = 0.30313$ the left side is a rarefaction, because $p < p_L = 1$: $f_L = 5.91608\,(0.30313^{1/7} - 1) = 5.91608 \times (0.84323 - 1) = -0.92746$. The right side is a shock, because $p > p_R = 0.1$: $A_R = 6.6667$, $B_R = 0.016667$, and $f_R = 0.20313\sqrt{6.6667/0.31980} = 0.92745$. So $f(p) \approx 0$, and $u^* = \frac12(0.92745 + 0.92746) = 0.92745$.

The solution at $t = 1$:

| $\xi = x/t$ | region | $\rho$ | $u$ | $p$ |
|---|---|---|---|---|
| $-1.5$ | left state | 1 | 0 | 1 |
| $-1.0$ | left fan | 0.877453 | 0.152680 | 0.832747 |
| $-0.5$ | left fan | 0.602938 | 0.569347 | 0.492472 |
| $0.0$ | left star | 0.426319 | 0.927453 | 0.303130 |
| $1.0$ | right star | 0.265574 | 0.927453 | 0.303130 |
| $2.0$ | right state | 0.125 | 0 | 0.1 |

The fan runs from $\xi = -1.18322$ to $-0.07027$, the contact moves at $u^* = 0.92745$, and the shock moves at $1.75216$. The Godunov flux at $x = 0$ is $F(W(0)) = (0.395391, 0.669837, 1.154038)$.

**Toro's five tests** (Toro 2009, Section 4.3.3), computed with the code on this page. The iteration counts are measurements with tol $= 10^{-12}$.

| test | waves | $p^*$ | $u^*$ | iterations |
|---|---|---|---|---|
| 1 (Sod) | rarefaction, shock | 0.30313 | 0.92745 | 4 |
| 2 (123 problem) | two rarefactions | 0.001894 | 0 | 1 |
| 3 | rarefaction, shock | 460.894 | 19.5975 | 6 |
| 4 | shock, rarefaction | 46.0950 | $-6.19633$ | 6 |
| 5 | two shocks | 1691.65 | 8.68977 | 5 |

In test 2 the guess of line L2 is already exact, because that guess is the exact root when both waves are rarefactions.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem: the [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/) across a shock and the isentropic relation with the Riemann invariant across a rarefaction give $u^* = u_L - f_L(p^*)$ and $u^* = u_R + f_R(p^*)$. So $p^*$ is a root of $f$, and line L9 gives $u^*$. Each $f_K$ is $C^1$, strictly increasing and concave on $(0, \infty)$, and the two branches meet with the same slope $1/(\rho_Kc_K)$ at $p_K$. So $f$ has exactly one positive root when the vacuum test of line L1 fails, and none when it passes. For a concave increasing function, every Newton iterate after the first lies at or below the root, and the iterates then increase to it with quadratic convergence. The sampling formulas follow from the wave order and from the fan relations $u - c = \xi$ and $u + 2c/(\gamma - 1) = $ const.

## Complexity

Theorem: with $k$ Newton iterations, the star state costs $O(k)$ arithmetic operations, square roots and powers, and each later sample costs $O(1)$. The memory is $O(1)$. Measurement: on Toro's five tests, $k$ is between 1 and 6 with tol $= 10^{-12}$. In Godunov's method with $M$ cells and $N$ time steps, the solver runs $N(M + 1)$ times. That cost, with its powers and square roots, is the main reason why codes use approximate solvers.

## Properties

- **Exact.** Up to the stopping tolerance, the result is the exact entropy solution, with the correct shock speeds and an exact contact.
- **Robust root finding.** Newton on a concave increasing function cannot overshoot after the first step, so no bracketing is necessary when $p^*$ is not extremely small.
- **Vacuum detection.** The test of line L1 is exact. When it passes, the solution has a vacuum region between two rarefactions, and the formulas for that case are different (Toro 2009, Section 4.6).
- **Entropy satisfying.** A shock forms only where $p^* > p_K$, which is the [Lax entropy condition](/lax-entropy-condition/) for the genuinely nonlinear fields 1 and 3.

## Variants and improvements

- **Other initial guesses.** Toro (2009, Section 4.3) also gives the linearised guess and the two-shock guess, and switches between them by the pressure ratio. Fewer iterations result, but the root does not change.
- **Bisection or a safeguarded method.** Because $f$ is increasing, [bisection](/bisection-method/) on $[\varepsilon, p_{\max}]$ always works. The tests on this page use it as an independent check.
- **Other equations of state.** For a stiffened gas or a covolume gas the same plan works with different wave functions. For a general equation of state the shock relations need an inner iteration.
- **Shallow water.** For the [shallow water equations](/shallow-water-equations/) the same plan applies to the depth $h^*$, with the wave function $(h - h_K)\sqrt{g(h + h_K)/(2hh_K)}$ for a shock and $2(\sqrt{gh} - \sqrt{gh_K})$ for a rarefaction.
- **Approximate solvers.** [Roe](/roe-solver/), [HLL](/hll-riemann-solver/), [HLLC](/hllc-riemann-solver/) and the [Rusanov flux](/rusanov-flux/) replace the iteration by a closed form. They are cheaper, and each one gives up some exactness.

## When to use it

Use the exact solver to make reference solutions for tests of numerical schemes, such as Sod's tube and Toro's tests. Use it also inside Godunov's method when the cost is acceptable, or as a check on an approximate solver. In large production codes, use an approximate solver for the face fluxes, and keep the exact solver for verification.

## Pitfalls

- **A non-positive iterate.** From a large starting pressure, a Newton step can give $p \le 0$. Line L6 resets it to a small positive value. Without that line the next power $p^z$ fails.
- **Near-vacuum data.** When $p^*$ is very small, the iteration needs many steps, and the reset of line L6 can be above the root. Detect a vacuum with line L1 first, and use bisection as a fallback.
- **A wrong sampling side.** The side is chosen by the contact speed $u^*$, not by $x = 0$. A sample at $\xi = 0$ can be in the right star region when $u^* < 0$.
- **Confusing sound speeds.** The tail of a rarefaction moves at $u^* \mp c^*_K$ with the star sound speed $c^*_K = c_K(p^*/p_K)^z$, not with $c_K$.
- **Conserved and primitive variables.** The solver works on $(\rho, u, p)$. Convert conserved cell averages to primitive states before the call, and convert the sampled state back to a flux after it.

## Implementations

## History

Godunov (1959) used exact solutions of the gas dynamics Riemann problem at the cell faces of his scheme. Sod (1978) compared finite difference schemes on the shock tube problem that now has his name, with the exact solution as the reference. The form on this page, one pressure function with Newton iteration and a choice of initial guesses, is the one set out in Toro's book (Toro 2009, Chapter 4), which also gives a FORTRAN program.

## References
