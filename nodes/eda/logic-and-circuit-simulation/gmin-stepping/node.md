---
tag: 55H27K
kind: technique
slug: gmin-stepping
name: Gmin stepping
aliases:
- conductance stepping
- gmin continuation
area: eda/logic-and-circuit-simulation
level: core
summary: Adds a large conductance from every node to ground and reduces it in steps to zero, solving the DC equations at each step from the last answer to reach convergence.
prereqs: [dc-operating-point-analysis, homotopy-continuation, newton-method-for-systems]
see_also: [source-stepping, pseudo-transient-analysis, junction-voltage-limiting, modified-nodal-analysis, tellegen-theorem, kantorovich-theorem, convex-function, systems-of-nonlinear-equations]
sources:
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 4, Section 4.4.4 (gmin stepping) and Section 4.4.6 (the justification of the continuation methods)
  - url: "https://sourceforge.net/p/ngspice/ngspice/ci/master/tree/src/spicelib/analysis/cktop.c"
    title: ngspice source, src/spicelib/analysis/cktop.c
    locator: the functions spice3_gmin (fixed factor steps) and dynamic_gmin (adaptive factor), which set CKTdiagGmin and remove it at the end
  - book: isbn:9780898714616
    title: James M. Ortega and Werner C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000 (first published 1970)
    locator: Section 6.4, the uniform monotonicity theorem (a continuous, uniformly monotone map of R^n onto itself has exactly one zero)
  - paper: doi:10.1109/43.229761
    title: Robert C. Melville, Ljiljana Trajković, San-Chin Fang and Layne T. Watson, Artificial parameter homotopy methods for the DC operating point problem, IEEE Transactions on Computer-Aided Design 12(6), 861 to 877, 1993
    locator: the conductance homotopies for the operating point problem and the conditions under which their paths reach a solution
---

Gmin stepping finds the [DC operating point](/dc-operating-point-analysis/) of a circuit that plain Newton cannot solve. It connects a conductance $\gamma$ from every node to ground, solves the circuit with a large $\gamma$, where the equations are close to linear and easy, and then lowers $\gamma$ step by step, starting each Newton run from the previous solution, until the conductance is removed. It is a technique of the circuit simulation half of the logic and circuit simulation sub-area, and a [homotopy continuation](/homotopy-continuation/) whose parameter is a physical conductance.

## In plain words

A circuit can be hard to solve because some parts of it are floating or very sensitive: a node held only by switched-off transistors, or a loop with large gain. Tie every node to ground through a strong resistor, and all voltages are pulled close to zero. That circuit is easy.

Now weaken those resistors a little. The answer moves only a little, so the previous answer is a good guess, and Newton's method finds the new one in a few steps. Repeat, making the extra resistors weaker each time, until they are so weak that they no longer matter, and then remove them.

## When it applies

Use it for the DC operating point after Newton, with [junction voltage limiting](/junction-voltage-limiting/), has failed from the usual start. It suits circuits with nodes that are almost floating, such as the internal nodes of stacks of transistors that are off, and circuits whose Jacobian is singular at the starting point. It needs only one change to [modified nodal analysis](/modified-nodal-analysis/): add $\gamma$ to each diagonal entry of a node row. It is a standard fallback in SPICE, tried before or after [source stepping](/source-stepping/).

## The template

Write the operating point equations as $F(x) = 0$ with $x = (e, j)$, the node voltages and the currents of the voltage sources, and let $P = \operatorname{diag}(I_n, 0)$ select the node voltages. The gmin circuit with conductance $\gamma \ge 0$ is

$$H(x, \gamma) = F(x) + \gamma P x = 0,$$

KCL with an extra current $\gamma e_k$ leaving each node $k$ to ground. At $\gamma = 0$ it is the given circuit.

```pseudo id=main
GMIN-STEPPING(F, γ_0, γ_min, ρ)
L1  γ ← γ_0; x ← 0
L2  x ← NEWTON(H(·, γ), x)                      ▷ the easy circuit
L3  while γ > γ_min do
L4      γ' ← max(γ / ρ, γ_min)
L5      (x', ok) ← NEWTON(H(·, γ'), x)          ▷ hole: the corrector, Newton with limiting
L6      if ok then γ ← γ'; x ← x'
L7      else ρ ← a smaller factor; if ρ is too close to 1 then return FAILURE      ▷ hole: the step rule
L8  x ← NEWTON(F, x)                              ▷ remove the added conductance
L9  return x
```

In SPICE3 the fixed version starts at a conductance $10^k$ times GMIN, divides by a fixed factor at each step, and after reaching GMIN sets the added conductance to GSHUNT (zero by default) for the final solve. The dynamic version of ngspice starts at $10^{-2}$ S, divides by an adaptive factor, and after a failure goes back to the last good point and replaces the factor by its fourth root. In both, the conductance GMIN ($10^{-12}$ S by default) that every pn junction model places across its junction stays in the circuit.

**Assumptions for the proofs.** Every resistive device is a two-terminal element with a continuous, nondecreasing law $i = g_k(v)$; the voltage sources form no loop, so $A_V$ has independent columns; and $W = \{w : A_V^{\mathsf T} w = 0\}$ is the set of changes of node voltages that keep every voltage source satisfied. Monotone laws give $(v - v')(g_k(v) - g_k(v')) \ge 0$, and summing over the devices with $v = A_N^{\mathsf T} e$ gives

$$(e - e')^{\mathsf T} A_N\big(g(A_N^{\mathsf T} e) - g(A_N^{\mathsf T} e')\big) \ge 0. \qquad (\ast)$$

**Theorem 1 (every gmin circuit has one solution).** Under the assumptions, for every $\gamma > 0$ the equation $H(x, \gamma) = 0$ has exactly one solution $x(\gamma)$, even when $F(x) = 0$ has none.

*Proof.* Pick $e_0$ with $A_V^{\mathsf T} e_0 = s_V$; it exists because $A_V^{\mathsf T}$ has full row rank. Every solution has $e = e_0 + w$ with $w \in W$. Let $\Pi$ be the orthogonal projection onto $W$ and $\Phi(w) = \Pi\big(A_N g(A_N^{\mathsf T}(e_0 + w)) + A_I s_I + \gamma (e_0 + w)\big)$, a continuous map of $W$ into itself. By $(\ast)$, $(w - w')^{\mathsf T}(\Phi(w) - \Phi(w')) \ge \gamma \|w - w'\|^2$, so $\Phi$ is uniformly monotone on $W$ and has exactly one zero by the uniform monotonicity theorem (Ortega and Rheinboldt, Section 6.4). At that zero, the KCL vector $r = A_N g(\cdot) + A_I s_I + \gamma e$ is orthogonal to $W$, and $W^\perp$ is the column space of $A_V$, so $A_V j = -r$ has exactly one solution $j$. Conversely every solution of $H = 0$ gives a zero of $\Phi$ this way, so the solution is unique. $\blacksquare$

**Theorem 2 (the large end).** Let $\bar e$ be the node voltage vector of least norm with $A_V^{\mathsf T} \bar e = s_V$. Then

$$\|e(\gamma) - \bar e\| \le \frac{\|A_N g(A_N^{\mathsf T} \bar e) + A_I s_I\|}{\gamma}.$$

*Proof.* Let $w = e(\gamma) - \bar e \in W$. The least norm solution lies in the column space of $A_V$, which is $W^\perp$, so $w^{\mathsf T} \bar e = 0$; also $w^{\mathsf T} A_V j = 0$. Multiply the KCL rows of $H = 0$ by $w^{\mathsf T}$: $w^{\mathsf T} A_N g(A_N^{\mathsf T} e(\gamma)) + w^{\mathsf T} A_I s_I + \gamma \|w\|^2 = 0$. By $(\ast)$ the first term is at least $w^{\mathsf T} A_N g(A_N^{\mathsf T} \bar e)$, so $\gamma \|w\|^2 \le -w^{\mathsf T}(A_N g(A_N^{\mathsf T} \bar e) + A_I s_I)$, and the Cauchy-Schwarz inequality gives the bound. $\blacksquare$

So for large $\gamma$ the solution is close to a known point, and Newton started there meets an almost linear problem: the start of the homotopy is easy. Without voltage sources $\bar e = 0$ and the bound is $\|A_I s_I\|/\gamma$ when the device laws pass through the origin.

**Theorem 3 (the path is smooth).** If in addition the device laws are continuously differentiable, then $\gamma \mapsto x(\gamma)$ is continuously differentiable on $(0, \infty)$: the homotopy path has no turning points and no branch points.

*Proof.* The Jacobian of $H$ in $x$ is $\begin{pmatrix} K + \gamma I & A_V \\ A_V^{\mathsf T} & 0 \end{pmatrix}$ with $K = A_N D A_N^{\mathsf T}$ and $D$ the diagonal of the slopes $g_k' \ge 0$. If it maps $(w, y)$ to zero, then $A_V^{\mathsf T} w = 0$, so $0 = w^{\mathsf T}(K + \gamma I) w + w^{\mathsf T} A_V y = w^{\mathsf T}(K + \gamma I) w \ge \gamma \|w\|^2$, hence $w = 0$, then $A_V y = 0$ and $y = 0$. The Jacobian is nonsingular at every point, and the implicit function theorem gives a continuously differentiable solution curve through each $x(\gamma)$; by uniqueness these pieces are the one curve $x(\gamma)$. $\blacksquare$

With small enough steps the corrector of line L5 therefore always converges for monotone circuits, by the local convergence of Newton along the compact pieces $[\gamma_{\min}, \gamma_0]$ of the path. The theorems say nothing about the end $\gamma \to 0$: if the given circuit has no operating point, the path runs off to infinity. Transistor circuits are not monotone, and for them the path can turn back; then fixed decreasing steps fail, and only methods that follow the arc length of the path, as in [homotopy continuation](/homotopy-continuation/), can pass the turn.

**Theorem 4 (the error of a small leftover conductance).** Let $x^\ast$ solve $F = 0$ and $x(\gamma)$ solve $H(\cdot, \gamma) = 0$, and suppose the device and resistor laws are uniformly monotone on $W$ with constant $\mu > 0$, that is $(\ast)$ holds with right side $\mu \|e - e'\|^2$ whenever $e - e' \in W$. Then

$$\|e(\gamma) - e^\ast\| \le \frac{\gamma}{\mu + \gamma}\, \|\Pi e^\ast\| \le \frac{\gamma}{\mu}\, \|e^\ast\|.$$

*Proof.* Let $w = e(\gamma) - e^\ast \in W$. Subtract the KCL rows of $F(x^\ast) = 0$ from those of $H(x(\gamma), \gamma) = 0$ and multiply by $w^{\mathsf T}$; the terms with $A_V$ and the sources vanish, which leaves $w^{\mathsf T} A_N(g(\cdot) - g(\cdot)) + \gamma w^{\mathsf T}(w + e^\ast) = 0$. So $\mu \|w\|^2 + \gamma \|w\|^2 \le -\gamma w^{\mathsf T} e^\ast = -\gamma w^{\mathsf T} \Pi e^\ast \le \gamma \|w\| \|\Pi e^\ast\|$. $\blacksquare$

The bound is tight: a current source $I$ into a single resistor $R$ has $\mu = 1/R$, $e^\ast = IR$ and $e(\gamma) = IR/(1 + \gamma R)$, and the change $IR \cdot \gamma R/(1 + \gamma R)$ equals the bound. Linear resistors that connect every node to ground or to a node held by a voltage source make $\mu$ at least the smallest eigenvalue of their conductance matrix on $W$. For a circuit that is not monotone, the implicit function theorem at a solution with nonsingular Jacobian $J$ gives the first-order form $x(\gamma) = x^\ast - \gamma J^{-1} P x^\ast + O(\gamma^2)$, so the change is at most $\gamma \|J^{-1}\| \|e^\ast\|$ to first order.

**Worked example.** A 5 V source drives a diode ($I_s = 10^{-14}$ A, $V_t = 25.852$ mV) through $1\ \text{k}\Omega$; the operating point is $v^\ast = 0.692544$ V. With $\gamma$ from the diode node to ground (the source node is held by the source, so its $\gamma$ changes only the source current):

| $\gamma$ (S) | $10^{-1}$ | $10^{-2}$ | $10^{-3}$ | $10^{-6}$ | $10^{-9}$ | $10^{-12}$ |
|---|---|---|---|---|---|---|
| $v(\gamma)$ (V) | 0.04950 | 0.45451 | 0.68808 | 0.6925395 | 0.692543629 | 0.692543633 |
| $v(\gamma) - v^\ast$ | $-0.643$ | $-0.238$ | $-4.5 \times 10^{-3}$ | $-4.1 \times 10^{-6}$ | $-4.1 \times 10^{-9}$ | $-4.1 \times 10^{-12}$ |

Theorem 4 with $\mu = 1/R = 10^{-3}$ S bounds the change at $\gamma = 10^{-12}$ S by $6.9 \times 10^{-10}$ V. The first-order form is sharper: $J$ is the conductance $1/R + I/V_t \approx 0.168$ S at the solution, so the change is about $\gamma v^\ast / 0.168 = 4.1 \times 10^{-12}$ V, as measured. The circuit with no solution, a current source pulling 1 mA out of the anode of a diode, shows the other end: the gmin circuit has the solution $v \approx -10^{-3}/\gamma$, which runs to $-10^9$ V at $\gamma = 10^{-12}$ S, a sign that $F = 0$ has no solution.

## Classic examples

- The DC analysis of SPICE3 and ngspice tries gmin stepping when Newton fails from the initial junction voltages, before [source stepping](/source-stepping/).
- [Pseudo-transient analysis](/pseudo-transient-analysis/) is the other conductance-like regularization: the companion conductance $C/h$ of an added capacitor plays the role of $\gamma$, but centred at the previous point instead of ground.
- The artificial parameter homotopies of Melville, Trajković, Fang and Watson for the operating point problem, of the form $\lambda F(x) + (1 - \lambda)\, G (x - a)$, act like a conductance $G$ in series with a source $a$ at every node, so that the start is a chosen point $a$ instead of zero; they come with conditions under which the path reaches a solution.
- In [MOS transistor models](/shichman-hodges-model/) and diode models the fixed GMIN across each junction keeps the MNA matrix nonsingular when a node is held only by devices that are off; SPICE3 steps the node conductance down to the same value before it removes it.

## Variations

- **Fixed factor steps.** Divide $\gamma$ by a fixed factor, such as 10, at each step, and stop at the first failure (SPICE3).
- **Adaptive factor.** Divide by a factor that grows after easy steps and shrinks after failures, and return to the last good point after a failure (dynamic gmin in ngspice).
- **Gmin on device junctions only.** Step the conductance across each pn junction instead of from each node to ground; the proofs are the same with $P$ replaced by the junction incidence.
- **Combined with source stepping.** ngspice's source stepping first solves the circuit with all sources off under gmin stepping, and then raises the sources with the conductance in place.
- **Keep a final shunt.** Leave a small conductance GSHUNT from every node to ground in the final circuit; Theorem 4 bounds the error this makes.

## Pitfalls

- **Turning points.** For circuits with positive feedback, such as latches and Schmitt triggers, the solution path in $\gamma$ can fold back. A step past the fold has no nearby solution, and the corrector fails or jumps to another branch.
- **Too small an end value.** Removing the conductance is the last step and can itself fail when a node is truly floating; the MNA matrix of the final circuit is then singular, and the right answer is to report the floating node.
- **A wrong solution that looks right.** If the final $\gamma$ is kept and is not small next to the conductances of the circuit, the answer is that of a different circuit; Theorem 4 says how small it must be.
- **No operating point.** When $F = 0$ has no solution, every gmin circuit still has one, so success at each step proves nothing about the end; node voltages that grow like $1/\gamma$ are the sign.

## Exercises

1. For the circuit of a current source $I$ into a diode, write $H(v, \gamma) = 0$ and show that $v(\gamma)$ is decreasing in $\gamma$ for $I > 0$.
2. Prove Theorem 2 for a circuit without voltage sources directly from $(\ast)$, and show that the bound is reached by a single linear resistor.
3. Give a circuit with two nodes, one diode and one resistor for which $\mu$ of Theorem 4 is zero, and compute $e(\gamma) - e^\ast$ exactly.
4. For the tunnel-diode law $g(v) = v^3 - 6v^2 + 10v$ driven by $6$ V through $1\ \Omega$, write $\gamma$ as a function of $v$ along the gmin path and decide which of the three operating points the path from $\gamma = \infty$ reaches.

## References
