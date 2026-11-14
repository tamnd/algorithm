---
tag: QF22WC
kind: technique
slug: source-stepping
name: Source stepping
aliases:
- source ramping
- supply stepping
area: eda/logic-and-circuit-simulation
level: core
summary: Ramps all independent sources from zero to their full values and solves the DC operating point at each step, a continuation method for hard circuits.
prereqs: [dc-operating-point-analysis, homotopy-continuation, newton-method-for-systems]
see_also: [gmin-stepping, pseudo-transient-analysis, junction-voltage-limiting, modified-nodal-analysis, kantorovich-theorem, bisection-method, systems-of-nonlinear-equations, tellegen-theorem]
sources:
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 4, Section 4.4.3 (source stepping) and Section 4.4.6 (the justification of the continuation methods)
  - url: "https://sourceforge.net/p/ngspice/ngspice/ci/master/tree/src/spicelib/analysis/cktop.c"
    title: ngspice source, src/spicelib/analysis/cktop.c
    locator: the functions spice3_src (equal steps of the source factor CKTsrcFact) and gillespie_src (adaptive steps, after a gmin ramp at zero sources)
  - book: isbn:9780898715446
    title: Eugene L. Allgower and Kurt Georg, Introduction to Numerical Continuation Methods, SIAM Classics in Applied Mathematics 45, 2003 (first published 1990)
    locator: the chapters on predictor-corrector methods and on step length control along a smooth solution curve
  - book: isbn:9780898714616
    title: James M. Ortega and Werner C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000 (first published 1970)
    locator: Section 6.4, the uniform monotonicity theorem
  - paper: doi:10.1109/43.229761
    title: Robert C. Melville, Ljiljana Trajković, San-Chin Fang and Layne T. Watson, Artificial parameter homotopy methods for the DC operating point problem, IEEE Transactions on Computer-Aided Design 12(6), 861 to 877, 1993
    locator: the discussion of natural parameter homotopies such as source stepping and their failure at turning points, which motivates artificial parameter homotopies
---

Source stepping finds the [DC operating point](/dc-operating-point-analysis/) of a circuit by multiplying every independent source by a factor $\lambda$ and raising $\lambda$ from 0 to 1 in steps. At $\lambda = 0$ every source is off and the answer is known, all voltages and currents zero; at each later step Newton's method starts from the previous answer, which is close to the new one when the step is small. It is a technique of the circuit simulation half of the logic and circuit simulation sub-area, and a [homotopy continuation](/homotopy-continuation/) whose parameter is the strength of the supplies.

## In plain words

Newton's method needs a good first guess. For a circuit switched off, the guess is easy: nothing flows and every voltage is zero.

So turn the supplies up slowly. Raise them to one tenth of their value, and solve the circuit starting from the switched-off state. The answer changes only a little, so this works. Raise them again, and start from the last answer. Keep going until the supplies reach their full value. If a step is too large and Newton fails, go back and take a smaller step. If steps go well, take larger ones.

## When it applies

Use it for the DC operating point when Newton from the usual start fails, and as the alternative to [gmin stepping](/gmin-stepping/). It needs one thing from the circuit: with all sources off, the zero vector must be an operating point. That holds when every device carries no current at zero bias, as diodes, bipolar transistors and the [Shichman-Hodges model](/shichman-hodges-model/) do. It works best when the solution moves smoothly with the supply, and it fails when the solution path turns back, as in circuits with positive feedback. It changes only the right side of the [MNA](/modified-nodal-analysis/) system, not the matrix.

## The template

Let $F(x, \lambda) = 0$ be the operating point equations with every independent source value $s$ replaced by $\lambda s$. In the notation of [DC operating point analysis](/dc-operating-point-analysis/),

$$F(x, \lambda) = \begin{pmatrix} A_N\, g(A_N^{\mathsf T} e) + A_V\, j + \lambda A_I s_I \\ A_V^{\mathsf T} e - \lambda s_V \end{pmatrix}.$$

```pseudo id=main
SOURCE-STEPPING(F, Δ_0, Δ_min)
L1  λ ← 0; x ← 0                              ▷ every source off: x = 0 solves F(·, 0)
L2  Δ ← Δ_0
L3  while λ < 1 do
L4      λ' ← min(λ + Δ, 1)
L5      (x', ok) ← NEWTON(F(·, λ'), x)          ▷ hole: the corrector, Newton with limiting
L6      if ok then λ ← λ'; x ← x'; Δ ← 2Δ        ▷ hole: the step rule
L7      else Δ ← Δ / 2; if Δ < Δ_min then return FAILURE
L8  return x
```

The code of this page follows these lines, with plain Newton as the corrector, a limit of 20 iterations per Newton run and the step doubled after each success and halved after each failure. SPICE3 uses equal steps $\lambda = i/N$ and stops at the first failure. The adaptive version of ngspice first solves the circuit with all sources off under gmin stepping, then raises $\lambda$ by a step that starts at $10^{-3}$, grows by a factor 1.5 after fast Newton runs, shrinks by half after slow ones and by ten after failures, and gives up when the step falls below $10^{-7}$.

**The end points.** $F(\cdot, 1)$ is the given circuit. At $\lambda = 0$, $x = 0$ gives $A_N g(0) = 0$ and $A_V^{\mathsf T} 0 = 0$, so $x = 0$ solves $F(\cdot, 0)$ when every device law passes through the origin. If, in addition, the devices are two-terminal with nondecreasing laws and the voltage sources form no loop, $x = 0$ is the only solution at $\lambda = 0$ (the uniqueness argument with [Tellegen's theorem](/tellegen-theorem/)), so the path starts at a known, unique point.

**Theorem (the path is smooth for monotone circuits).** Assume every resistive device is a two-terminal element with a continuously differentiable law, the voltage sources form no loop, and the devices are uniformly monotone on $W = \{w : A_V^{\mathsf T} w = 0\}$ with a constant $\mu > 0$: $(e - e')^{\mathsf T} A_N(g(A_N^{\mathsf T} e) - g(A_N^{\mathsf T} e')) \ge \mu \|e - e'\|^2$ when $e - e' \in W$. This holds, for example, when linear resistors alone connect every node to ground or to a node held by a voltage source. Then for every $\lambda \in [0, 1]$ the circuit $F(\cdot, \lambda) = 0$ has exactly one solution $x(\lambda)$, and $\lambda \mapsto x(\lambda)$ is continuously differentiable.

*Proof.* Fix $\lambda$ and pick $e_0$ with $A_V^{\mathsf T} e_0 = \lambda s_V$. As on the gmin stepping page, the node equations projected onto $W$ form a map of $W$ into itself that is uniformly monotone with constant $\mu$, so the uniform monotonicity theorem (Ortega and Rheinboldt, Section 6.4) gives exactly one $e$, and then exactly one $j$ because $A_V$ has independent columns. For the smoothness, the Jacobian in $x$ is $\begin{pmatrix} K & A_V \\ A_V^{\mathsf T} & 0 \end{pmatrix}$ with $K = A_N D A_N^{\mathsf T}$, and uniform monotonicity of a differentiable map gives $w^{\mathsf T} K w \ge \mu \|w\|^2$ for $w \in W$. If $(w, y)$ is in the null space, then $w \in W$ and $0 = w^{\mathsf T} K w + w^{\mathsf T} A_V y = w^{\mathsf T} K w \ge \mu \|w\|^2$, so $w = 0$, then $A_V y = 0$ and $y = 0$. The Jacobian is nonsingular everywhere, and the implicit function theorem gives a continuously differentiable curve through each $x(\lambda)$, which by uniqueness is $x(\lambda)$. $\blacksquare$

**Corollary (the stepping succeeds).** Under the theorem's assumptions, with device laws whose derivatives are Lipschitz on bounded sets, there is a $\Delta^\ast > 0$ such that Newton started at $x(\lambda)$ converges to $x(\lambda')$ whenever $|\lambda' - \lambda| \le \Delta^\ast$. *Proof sketch.* The path is compact, so $\|J^{-1}\|$ is bounded along it and the Jacobian is Lipschitz near it; the [Kantorovich theorem](/kantorovich-theorem/) then gives one radius $r > 0$ of quadratic convergence around every $x(\lambda)$. The path is uniformly continuous on $[0, 1]$, so a small enough $|\lambda' - \lambda|$ keeps $x(\lambda)$ within $r$ of $x(\lambda')$. $\blacksquare$ So in exact arithmetic, with an iteration limit large enough for that radius, the step of line L7 never falls below $\Delta^\ast / 2$, each accepted step except the last is at least $\Delta^\ast/2$, and the loop ends after finitely many steps if $\Delta_{\min} < \Delta^\ast/2$. The value of $\Delta^\ast$ is not known in advance, which is why the step is adapted.

**What is proved and what is measured.** The theorem and the corollary cover monotone circuits: diodes, resistors and sources. Transistor circuits are not monotone, and for them no general guarantee holds; the success of source stepping on them is measured, not proved. The table below is measured with the code of this page.

**Worked example.** A source $E$ drives a diode ($I_s = 10^{-14}$ A, $V_t = 25.852$ mV) through $1\ \text{k}\Omega$. Plain Newton from zero first puts nearly all of $E$ on the diode.

| $E$ | plain Newton from 0 | source stepping, $\Delta_0 = 0.1$ | answer $v$ |
|---|---|---|---|
| 5 V | 173 iterations | $\lambda$ = 0.1, 0.2, 0.4, 0.8, 1; one rejected step; 41 iterations | 0.692544 V |
| 20 V | overflow: $e^{20/V_t} = e^{774}$ in iteration 2 | $\lambda$ = 0.05, 0.15, 0.35, 0.75, 1; one rejected step; 46 iterations | 0.731273 V |

The answers agree with [bisection](/bisection-method/) on the KCL residual of the diode node to $10^{-9}$ V. Both runs use plain Newton as the corrector; with [junction voltage limiting](/junction-voltage-limiting/) in the corrector the counts fall further.

**A turning point.** Drive the tunnel-diode law $g(v) = v^3 - 6v^2 + 10v$ by $7\lambda$ volts through $1\ \Omega$. KCL is $7\lambda - v = g(v)$, so along the path $\lambda = (v^3 - 6v^2 + 11v)/7$. This has $d\lambda/dv = 0$ at $v = 2 - 1/\sqrt 3 \approx 1.4226$, where $\lambda \approx 0.9121$. Below this value the path from $v = 0$ rises smoothly; above it the low branch no longer exists, and at $\lambda = 1$ the only solution is $v \approx 3.3245$, on another branch. The Jacobian $1 + g'(v)$ is zero at the fold, so no step size lets the corrector follow the path past it: it must jump, and whether it lands on the far branch is luck.

## Classic examples

- The DC analysis of SPICE3 and ngspice tries source stepping when Newton and [gmin stepping](/gmin-stepping/) fail.
- A DC sweep in a simulator is source stepping on one source, with the answers kept at every step; it traces transfer curves and is how the folds of latches are seen.
- [Pseudo-transient analysis](/pseudo-transient-analysis/) can ramp the supplies in time, which is source stepping with added capacitors.
- [Homotopy continuation](/homotopy-continuation/) with arc-length parametrization follows the same path through turning points, at the price of a larger system per step.

## Variations

- **Equal steps.** Take $\lambda = i/N$ for $i = 1, \ldots, N$ and stop at the first failure. Simple, but a hard spot near $\lambda = 1$ needs a large $N$ everywhere.
- **Adaptive steps.** Grow the step after easy Newton runs and shrink it after slow runs or failures, as in the code of this page and in ngspice.
- **Predictor.** Start Newton at $x(\lambda) + \Delta\, x'(\lambda)$ instead of $x(\lambda)$; $x'(\lambda)$ solves one linear system with the Jacobian already factored, since $F_x x' = -F_\lambda$, and the tangent prediction allows longer steps.
- **Arc-length continuation.** Make the arc length the parameter and solve for $(x, \lambda)$ together; this passes turning points ([homotopy continuation](/homotopy-continuation/)).
- **Supply only.** Ramp only the supply voltages and keep the signal sources fixed, or the reverse; the start point must still be known.

## Pitfalls

- **Turning points.** Positive feedback makes the path fold, as in the tunnel-diode example; natural-parameter stepping fails or jumps there.
- **The start must be a solution.** A device that carries current at zero bias, or a current source that is not scaled, breaks the end point at $\lambda = 0$.
- **Which solution.** For a circuit with several operating points, the stepping finds the one connected to the zero state along the path, which need not be the one the circuit settles in after power-up.
- **Tolerances.** The corrector at an intermediate $\lambda$ need not be accurate; only the last solve at $\lambda = 1$ needs the full tolerances, and loose intermediate solves save iterations.

## Exercises

1. For a source $E$, a resistor $R$ and a diode, show that $v(\lambda)$ is increasing in $\lambda$ and that the path is smooth, directly from the scalar KCL equation.
2. Show that for a circuit of linear resistors and sources the solution is $x(\lambda) = \lambda x(1)$, and that source stepping with any steps takes one Newton iteration per step plus one for the convergence test.
3. In the tunnel-diode example, find the value of $\lambda$ at which a second turning point appears on the way back, and describe the three branches of the path.
4. Derive the predictor $x'(\lambda) = -F_x^{-1} F_\lambda$ and compute it at $\lambda = 0$ for the diode circuit.

## References
