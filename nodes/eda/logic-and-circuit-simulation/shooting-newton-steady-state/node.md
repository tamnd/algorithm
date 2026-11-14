---
tag: FS9DNT
kind: algorithm
slug: shooting-newton-steady-state
name: Shooting Newton periodic steady state
aliases:
- Aprille-Trick shooting
- periodic steady-state shooting
area: eda/logic-and-circuit-simulation
level: advanced
summary: Aprille and Trick's method that searches for the initial state whose transient over one period returns to itself, solved by Newton with the sensitivity matrix.
model: real-ram
complexity:
  vars: {n: the number of MNA unknowns, S: the number of time steps per period, I: the number of Newton iterations}
  time: {worst: "O(I S n^3)"}
  space: {extra: "O(n^2 + S n)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1972
  people: [Thomas J. Aprille, Timothy N. Trick]
  note: Aprille and Trick found the periodic steady state of a nonlinear circuit by Newton's method on the condition that one period of transient analysis returns to its initial state, with the Jacobian from the sensitivity of the transient.
prereqs: [transient-circuit-analysis, shooting-method, newton-method-for-systems, modified-nodal-analysis]
see_also: [harmonic-balance-analysis, phase-noise-analysis, companion-model, trapezoidal-rule, backward-euler-method, gmres, fixed-point-iteration, tr-bdf2]
sources:
  - paper: doi:10.1109/PROC.1972.8563
    title: Thomas J. Aprille and Timothy N. Trick, Steady-state analysis of nonlinear circuits with periodic inputs, Proceedings of the IEEE 60(1), 108 to 114, 1972
    locator: the formulation of the periodic steady state as x(T) = x(0), the Newton iteration and the sensitivity (state transition) matrix computed along the transient
  - paper: doi:10.1109/JSSC.1973.1050394
    title: F. R. Colon and Timothy N. Trick, Fast periodic steady-state analysis for large-signal electronic circuits, IEEE Journal of Solid-State Circuits 8(4), 260 to 269, 1973
    locator: the faster computation of the periodic steady state that followed the 1972 method
  - paper: doi:10.1145/217474.217574
    title: Ricardo Telichevesky, Kenneth S. Kundert and Jacob K. White, Efficient steady-state analysis based on matrix-free Krylov-subspace methods, Proceedings of the 32nd Design Automation Conference, 480 to 484, 1995
    locator: the solution of the shooting Newton equations with GMRES and matrix-vector products from the stored step matrices
  - book: doi:10.1007/978-1-4757-2081-5
    title: Kenneth S. Kundert, Jacob K. White and Alberto Sangiovanni-Vincentelli, Steady-State Methods for Simulating Analog and Microwave Circuits, Springer, 1990
    locator: the chapter Time-Domain Methods, pages 55 to 79, on shooting methods for circuits
---

Shooting Newton finds the periodic steady state of a circuit with periodic sources by searching for the initial state from which one period of transient analysis returns to the same state. Aprille and Trick (1972) solved this condition, $x(T) = x(0)$, with [Newton's method](/newton-method-for-systems/), and got the Jacobian from the sensitivity of the transient to its initial state, the monodromy matrix. It belongs to the circuit simulation half of the logic and circuit simulation sub-area, next to [harmonic balance](/harmonic-balance-analysis/), and it suits circuits with sharp edges and slow time constants.

## In plain words

A circuit with a slow filter can take thousands of periods to settle after power-up. A plain transient run must simulate all of them, even when only the final repeating waveform matters.

Shooting asks a sharper question: from which starting state does one period of simulation end exactly where it started? It guesses a start, simulates one period, and sees how far the end is from the start. It also tracks how the end would move if the start moved a little. With that information it corrects the guess, as a gunner corrects the aim after one shot. For a linear circuit the second guess is right; for a nonlinear one a few more corrections usually suffice, and each costs about one period of simulation.

## The problem

The circuit is in [modified nodal analysis](/modified-nodal-analysis/) form, $f(x) + \frac{d}{dt} q(x) = u(t)$, with $x = (e_1, \ldots, e_n, j_1, \ldots, j_m)$, $G = \partial f/\partial x$, $C = \partial q/\partial x$, and every source has period $T$. A periodic steady state is a solution with $x(t + T) = x(t)$. Its initial state is a root of

$$r(x_0) = \phi_T(x_0) - x_0,$$

where $\phi_T(x_0)$ is the state at time $T$ of the transient that starts at $x_0$. This is the [shooting method](/shooting-method/) for a boundary value problem whose boundary condition is periodicity.

In practice $\phi_T$ is the [transient analysis](/transient-circuit-analysis/) with $S$ fixed steps of size $h = T/S$, with the trapezoidal rule ($\theta = \tfrac12$) or backward Euler ($\theta = 1$):

$$q(x_{k+1}) - q(x_k) + h\big[\theta\,(f(x_{k+1}) - u_{k+1}) + (1 - \theta)(f(x_k) - u_k)\big] = 0.$$

The method finds the exact periodic solution of this discrete map, which differs from the continuous steady state by the integration error. Input: the circuit, $T$, $S$, $\theta$ and a start. Output: $x_0$ and the states of one period. The device equations have fitted parameters: in the example, the diode saturation current $I_S$ and emission coefficient $N$ are fitted to measurements.

## The algorithm

```pseudo id=main
SHOOT(circuit, T, S, θ)
L1  x₀ ← a start state (zero, or the DC operating point); h ← T/S
L2  repeat
L3      for k = 0, ..., S − 1: x_{k+1} ← one implicit step from x_k at time kh
L4          Φ ← (C_{k+1} + θhG_{k+1})⁻¹ (C_k − (1 − θ)hG_k) Φ, starting from Φ = I
L5      r ← x_S − x₀
L6      solve (Φ − I)Δ = −r; x₀ ← x₀ + λΔ with a step limit λ ≤ 1
L7  until λ = 1 and Δ is small
L8  return x₀ and the states x_0, ..., x_S of one period
```

Line L3 is an ordinary transient step: Newton's method on the step equation, with the matrix $C_{k+1} + \theta h G_{k+1}$ of the [companion model](/companion-model/). Line L4 is the extra work of shooting. Differentiating the step equation with respect to $x_0$ gives $(C_{k+1} + \theta hG_{k+1})\,\partial x_{k+1}/\partial x_0 = (C_k - (1 - \theta)hG_k)\,\partial x_k/\partial x_0$, and the matrix on the left is the one the step has just factored. After $S$ steps, $\Phi = \partial x_S/\partial x_0$ is the monodromy matrix of the discrete map, and line L6 is exactly Newton's step for $r$. The step limit keeps node voltages from moving more than 1 V per iteration.

The implementation stores $\Phi$ as a dense $n \times n$ matrix and solves line L6 directly. For large circuits, Telichevesky, Kundert and White (1995) never form $\Phi$: they solve line L6 with [GMRES](/gmres/), and each product $\Phi v$ is one pass of $S$ triangular solves with the stored factors of the steps.

## Example

**An RC circuit, by hand.** A current source $\cos(\omega t)/R$ drives $R = 1$ kΩ in parallel with $C$, where $\omega = 2\pi \cdot 1$ MHz and $\omega RC = 1$. The continuous steady state is $v(t) = \operatorname{Re}\big(e^{j\omega t}/(1 + j)\big)$, so $v(0) = 0.5$. With the trapezoidal rule and $S = 100$, starting from $x_0 = 0$, one period ends at $x_S = 0.49890$ V. Each step multiplies a change of the state by $\rho = (1 - a)/(1 + a)$ with $a = h/(2RC)$, so $\Phi = \rho^{100} = 0.0018636$, close to $e^{-T/RC} = e^{-2\pi} = 0.0018674$. Newton gives $x_0 = 0 - (0.49890 - 0)/(0.0018636 - 1) = 0.49984$ V. A second period from this state returns to it to rounding, so the method stops after one correction. The value is the exact steady state of the discrete map, the AC phasor at the warped frequency $\tfrac2h\tan\tfrac{\omega h}2$, and it differs from 0.5 by $1.6 \times 10^{-4}$, the second-order error of the integration.

**A rectifier with a slow load, measured.** A 2 V, 1 MHz sine source behind 1 kΩ (with 10 pF at its node) drives a diode into a load of 100 kΩ in parallel with 1 nF, a time constant of 100 periods. The diode has $I_S = 10^{-14}$ A and $N = 1$, fitted values for a small silicon diode. With the trapezoidal rule and $S = 100$, shooting from zero needs 7 Newton iterations. The residual $\max|x_S - x_0|$ of the successive iterations was:

| iteration | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| residual (V) | 0.286 | 0.0503 | 0.00745 | 4.97e-4 | 3.27e-6 | 1.47e-10 | 8.9e-16 |

The last steps show the quadratic convergence of Newton's method: from iteration 4 to 6, each residual is about 13 times the square of the one before, and iteration 7 reaches rounding. The output settles at a mean of 1.2569 V with a ripple of 10.7 mV. The plain transient from zero with the same steps needs 155 periods before $x(T)$ changes by less than 1 nV in one period, and it then stops $7.3 \times 10^{-9}$ V from the shooting result. The dominant eigenvalue of $\Phi$ at the steady state is 0.8906, which is the factor by which the transient's error falls in each period. Measured with Python's process time on one machine, shooting took 0.04 s and the transient 0.69 s. With $S = 200$ and $S = 400$ the iteration counts and residuals are the same, and the output voltage at $t = 0$ changes by $1.9 \times 10^{-5}$ V and then $4.8 \times 10^{-6}$ V, a factor of 4 per halving of $h$.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **A periodic steady state is a root of $x(T) - x(0)$.** The sources repeat after $S$ steps, so the step maps repeat, and a solution with $x_S = x_0$ repeats forever. The same argument holds for the exact flow when its initial value problem has unique solutions.
2. **Shooting Newton uses the monodromy matrix.** By implicit differentiation of each step and the chain rule, the product of line L4 is $\partial x_S/\partial x_0$, so $\Phi - I$ is the Jacobian of $r$ and line L6 is Newton's step; it converges quadratically near a root where $\Phi - I$ is nonsingular.
3. **Linear circuits.** $r$ is affine, so one Newton step solves it, and the discrete steady state for a sinusoidal source is the AC phasor at the frequency $j\tfrac2h\tan\tfrac{\omega h}2$ (trapezoidal) or $(1 - e^{-j\omega h})/h$ (backward Euler), within $O(h^2)$ or $O(h)$ of the exact one.
4. **The trapezoidal rule and algebraic rows.** For a row with no charge term, such as a voltage source, the trapezoidal rule gives $g^{\mathsf T}\Phi = (-1)^S g^{\mathsf T}$, so $\Phi - I$ is singular for even $S$; backward Euler gives $g^{\mathsf T}\Phi = 0$.

The discretization error for nonlinear circuits and the convergence rate of the plain transient are measured, not proved.

The tests check, with fixed seeds:

- A parallel RLC circuit with the trapezoidal rule at $S = 40, 80, 160$: one Newton step, and every state equal to the warped-frequency phasor to $10^{-12}$.
- An RC circuit with a voltage source and backward Euler: the same against its discrete phasor.
- The error against the analytic steady state: $1.50 \times 10^{-3}$, $3.74 \times 10^{-4}$ and $9.35 \times 10^{-5}$ V, a ratio of 4.0 per halving.
- $\Phi$ against central differences of the period map for random starts (seed 61), to a relative error of $10^{-6}$.
- The rectifier against the long transient, and the quadratic decrease of the residuals.
- The identity $g^{\mathsf T}(\Phi - I) = 0$ for $S = 64$ and $-2g^{\mathsf T}$ for $S = 65$ with the trapezoidal rule, and $g^{\mathsf T}\Phi = 0$ with backward Euler. With $S = 64$, the Newton matrix has an exactly zero pivot.

## Complexity

One Newton iteration is one transient period of $S$ steps plus the sensitivity. With dense matrices, each step costs $O(n^3)$ for its own Newton solves and $O(n^3)$ for the product in line L4, so $I$ iterations cost $O(I S n^3)$ time; the states of one period take $O(Sn)$ space and $\Phi$ takes $O(n^2)$. With sparse factors, the sensitivity costs $n$ sparse solves per step, which is still too much for large $n$. The matrix-free form replaces it by GMRES on line L6, where one product $\Phi v$ costs $S$ solves with stored factors, so an iteration costs about one transient period plus one period of solves per GMRES step. Compared with a plain transient, shooting costs $O(I)$ periods instead of the number of periods the circuit needs to settle, which grows with its slowest time constant.

## Properties

- **Time-domain accuracy.** The waveform is computed by the same integration method as a transient run, so sharp edges, switching and strongly nonlinear devices cost no more than in transient analysis.
- **Independent of slow time constants.** The number of Newton iterations does not grow with the settling time, unlike a plain transient.
- **Quadratic convergence** near a root, as in the measured residuals.
- **Floquet information.** The eigenvalues of $\Phi$ at the solution are the Floquet multipliers of the discrete steady state; one with magnitude above 1 shows that the steady state is unstable.
- **Exact for the discrete map.** The result is the steady state of the integration method, with its error.

## Variants and improvements

- **Matrix-free Krylov shooting.** GMRES with products $\Phi v$ from stored step factors, as above; this makes shooting practical for large integrated circuits.
- **Autonomous circuits.** For an oscillator the period is unknown. Add $T$ as an unknown and a phase condition, such as fixing one node voltage at $t = 0$; the extended Newton matrix uses $\Phi$ and the derivative $\partial x_S/\partial T = \dot x(T)$. The result feeds [phase noise analysis](/phase-noise-analysis/).
- **Multiple shooting.** Split the period into segments with their own start states, which helps when $\Phi$ is badly conditioned.
- **Damped integrators.** Backward Euler, Gear's methods or [TR-BDF2](/tr-bdf2/) avoid the singular algebraic rows of the trapezoidal rule.
- **Periodic small-signal analysis.** The step matrices of the converged period give the periodic AC, transfer function and noise analyses of mixers and switched-capacitor circuits.

## When to use it

Use shooting for the periodic steady state of circuits with sharp edges or strong nonlinearity: switching power converters, switched-capacitor filters, frequency dividers and digital or sampling circuits, and any circuit with a slow bias or filter network that makes plain transient runs long. Use [harmonic balance](/harmonic-balance-analysis/) when the waveforms are nearly sinusoidal or when the circuit has distributed elements known only in the frequency domain.

## Pitfalls

- **Trapezoidal rule with algebraic unknowns.** With MNA unknowns and an even number of steps, $\Phi - I$ is singular for every voltage source row; the measured Newton matrix had an exactly zero pivot at $S = 64$. Use a damped method, an odd $S$, or shoot on the state variables only.
- **Multiplier near 1.** If a Floquet multiplier is close to 1, as for a lightly damped resonance or an oscillator, $\Phi - I$ is nearly singular and Newton is slow or fails.
- **Fixed steps.** The method needs the same steps in every period, or at least the same discrete map. Adaptive step control between iterations changes the map and can stop convergence; production codes fix the time points before the final iterations.
- **Cost of a dense $\Phi$.** Forming $\Phi$ costs $n$ solves per step. Use the matrix-free form for more than a few hundred unknowns.
- **Discretization error is not reported.** The method returns the exact periodic solution of the discrete map; refine $S$ to check it, as in the example.
- **Fitted parameters.** The rectified output depends on the diode's fitted $I_S$ and $N$; the steady state is only as good as the model.

## Implementations

## History

Aprille and Trick (1972) formulated the periodic steady state of a nonlinear circuit as the boundary value problem $x(T) = x(0)$ and solved it with Newton's method, computing the needed sensitivity matrix along the transient. Colon and Trick (1973) made the method faster for large-signal circuits. The book of Kundert, White and Sangiovanni-Vincentelli (1990) described shooting next to harmonic balance as one of the two main steady-state methods. Telichevesky, Kundert and White (1995) removed the dense sensitivity matrix with a matrix-free Krylov solver, which made shooting usable on large RF integrated circuits.

## References
