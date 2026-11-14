---
tag: BSQ8WP
kind: problem
slug: dc-operating-point-analysis
name: DC operating point analysis
aliases:
- DC analysis
- operating point analysis
- bias point
area: eda/logic-and-circuit-simulation
level: intro
summary: Find the node voltages and branch currents of a circuit at rest, with capacitors open and inductors shorted, by solving the nonlinear MNA equations.
prereqs: [modified-nodal-analysis, systems-of-nonlinear-equations]
see_also: [newton-method-for-systems, junction-voltage-limiting, gmin-stepping, source-stepping, pseudo-transient-analysis, homotopy-continuation, shichman-hodges-model, tellegen-theorem]
sources:
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 4 (solution of nonlinear algebraic circuit equations), Section 4.1.2 (nonlinear MNA formulation) and Section 4.4 (source stepping, gmin stepping and pseudo-transient)
  - paper: doi:10.1109/43.229761
    title: Robert C. Melville, Ljiljana Trajković, San-Chin Fang and Layne T. Watson, Artificial parameter homotopy methods for the DC operating point problem, IEEE Transactions on Computer-Aided Design 12(6), 861 to 877, 1993
    locator: the operating point problem, its multiple solutions, and globally convergent probability-one homotopies with the circuit conditions that make them work
  - paper: "Laurence W. Nagel, SPICE2: A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, Electronics Research Laboratory, University of California, Berkeley, 1975"
    title: Laurence W. Nagel, SPICE2, A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, University of California, Berkeley, May 1975
    locator: the chapter on DC analysis (Newton iteration on the nonlinear circuit equations and the convergence aids)
  - book: "Leon O. Chua and Pen-Min Lin, Computer-Aided Analysis of Electronic Circuits: Algorithms and Computational Techniques, Prentice-Hall, 1975"
    title: Leon O. Chua and Pen-Min Lin, Computer-Aided Analysis of Electronic Circuits, Prentice-Hall, 1975
    locator: the chapters on the DC analysis of nonlinear circuits (existence, uniqueness and multiple solutions, and Newton's method)
---

DC operating point analysis asks for the voltages and currents of a circuit at rest under constant sources: the solution of the circuit equations with every capacitor replaced by an open circuit and every inductor by a short. For a circuit with diodes or transistors this is a [system of nonlinear equations](/systems-of-nonlinear-equations/) in the unknowns of [modified nodal analysis](/modified-nodal-analysis/), and it may have no solution, exactly one, or several. It is the problem of the circuit simulation half of the logic and circuit simulation sub-area that every other analysis starts from: small-signal AC analysis linearizes at the operating point, and transient analysis starts from it.

## In plain words

Switch a circuit on, keep every supply fixed, and wait until nothing changes any more. The voltages and currents you would then measure are the operating point, also called the bias point.

At rest, no current flows into a capacitor, and an inductor acts like a plain wire. What remains is a circuit of resistors, sources and devices such as diodes and transistors. The currents must balance at every connection, and each device must obey its own law.

For resistors and sources alone, this is one linear system. Diodes and transistors make it nonlinear, and then strange things can happen: there may be no answer at all, or there may be several, as in a memory cell that can rest in either of two states.

## Definition

**Input.** A lumped circuit with nodes $0, \ldots, n$ (node 0 is ground) and branches of these kinds: independent DC voltage sources $s_V$ and current sources $s_I$; capacitors, which carry no DC current; inductors, which have no DC voltage; and resistive devices whose branch currents are given functions of the branch voltages, $i_N = g(v_N)$ with $g : \mathbb{R}^{b_N} \to \mathbb{R}^{b_N}$ continuous. A transistor is a resistive multi-port: its terminal currents are functions of its terminal voltages.

**Equations.** At DC an inductor acts as a voltage source of value 0 and a capacitor is removed. Let $A_N$, $A_V$ and $A_I$ be the columns of the reduced incidence matrix for the resistive devices, for the voltage sources (with the inductors) and for the current sources. The unknowns are $x = (e, j) \in \mathbb{R}^{n + m}$, the node voltages and the currents of the $m$ voltage sources and inductors. The DC operating point equations are

$$F(x) = \begin{pmatrix} A_N\, g(A_N^{\mathsf T} e) + A_V\, j + A_I\, s_I \\ A_V^{\mathsf T} e - s_V \end{pmatrix} = 0,$$

KCL at every node and the law of every voltage source, with KVL built in through $v = A^{\mathsf T} e$.

**Output.** A vector $x^\ast$ with $F(x^\ast) = 0$, or the statement that none exists. The problem has no objective: it is a feasibility problem. When several solutions exist, the task names which one is wanted: any one, all of them, or the one reached from a given initial state (the state that the physical circuit settles into after power-up).

**Accepted accuracy.** In floating point a simulator accepts $x$ when the KCL residuals are below an absolute current tolerance and the last change of each unknown is below a relative tolerance plus an absolute one. In SPICE these are ABSTOL, RELTOL and VNTOL. These are acceptance tests, not part of the mathematical problem.

## Variants

- **Linear DC analysis.** With linear resistors only, $F$ is affine and the problem is one MNA solve; the MNA page gives the exact condition for a unique solution.
- **DC sweep.** Solve a family of problems as one source value varies, for example to trace a transfer curve. The previous solution is a good starting point for the next.
- **All operating points.** Find every solution, for example to check that a bias circuit has only the intended state, or to find the three states of a latch.
- **Operating point with initial conditions.** Some node voltages are fixed by the user (the SPICE .NODESET and .IC statements); the first only guides the search, the second changes the equations.
- **Periodic steady state.** For periodic sources the analogue of an operating point is a periodic solution, found by [shooting](/shooting-newton-steady-state/) or [harmonic balance](/harmonic-balance-analysis/); it is a different problem.

## Examples

**Exactly one solution.** A 5 V source in series with $R = 1\ \text{k}\Omega$ drives a diode with $i = I_s(e^{v/V_t} - 1)$, $I_s = 10^{-14}$ A and $V_t = 25.852$ mV. KCL at the diode node is $h(v) = (5 - v)/R - I_s(e^{v/V_t} - 1) = 0$. The function $h$ is strictly decreasing, $h(0) > 0$ and $h(5) < 0$, so there is exactly one root, $v \approx 0.6925$ V, with current $(5 - v)/R \approx 4.307$ mA. By hand, bisection on $[0, 5]$ finds it, since $h$ changes sign once.

**No solution.** A current source drives 1 mA through a diode in the reverse direction: the source carries 1 mA from the anode node to ground, so KCL demands $i_D = -1$ mA. The diode law gives $i_D > -I_s = -10^{-14}$ A for every $v$, so no voltage works and the circuit has no operating point. Two ideal voltage sources of 1 V and 2 V in parallel are a second example: KVL around the loop cannot hold.

**Three solutions.** A source $E = 6$ V with a series $R = 1\ \Omega$ drives a nonlinear resistor with the N-shaped law $g(v) = v^3 - 6v^2 + 10v$, a model of a tunnel diode. KCL is $6 - v = g(v)$, that is

$$v^3 - 6v^2 + 11v - 6 = (v - 1)(v - 2)(v - 3) = 0,$$

so the operating points are $v = 1, 2, 3$ V with currents $5, 4, 3$ A. At $v = 2$ the element has negative slope, $g'(2) = -2$. With a small capacitor $C$ across the element, $C\, \dot v = 6 - v - g(v)$, whose slope $-1 - g'(v)$ is $-2$ at $v = 1$ and $v = 3$ and $+1$ at $v = 2$, so the middle point is unstable: the circuit is bistable. A latch of two cross-coupled inverters has the same structure, with two stable states and one unstable state between them.

**Infinitely many solutions.** Two equal 1 V sources in parallel satisfy KVL, but their currents can be $j$ and $-j$ for any $j$: the solutions form a line, and the MNA Jacobian is singular everywhere.

## Known algorithms

- [Newton's method for systems](/newton-method-for-systems/) on $F$, with one MNA solve of the linearized circuit per iteration. Guarantee: local quadratic convergence when the Jacobian is nonsingular at the solution and Lipschitz near it ([Kantorovich theorem](/kantorovich-theorem/)). No global guarantee; from a poor start it can diverge, cycle or overflow the exponentials of diode laws.
- [Junction voltage limiting](/junction-voltage-limiting/) (pnjlim in SPICE) bounds the change of each junction voltage per iteration. Guarantee: no overflow; convergence is measured, not proved in general.
- [Gmin stepping](/gmin-stepping/) and [source stepping](/source-stepping/) solve a sequence of easier circuits that ends in the given one. They are [homotopy continuation](/homotopy-continuation/) methods with natural parameters; with fixed steps they can fail at turning points of the solution path.
- Probability-one homotopies of Melville, Trajković, Fang and Watson (1993): globally convergent for circuits that satisfy their coercivity conditions, with probability one over the random start.
- [Pseudo-transient analysis](/pseudo-transient-analysis/) adds capacitors and integrates the resulting circuit in time until it stops changing; Kelley and Keyes proved convergence under conditions on the dynamics.
- For a circuit with one unknown and a monotone law, the [bisection method](/bisection-method/) on the KCL residual is guaranteed to converge, as in the first example.

## Bounds

- **Uniqueness.** If every resistive device is a two-terminal element with a strictly increasing current law, the voltage sources form no loop and the devices and voltage sources connect every node to ground, then there is at most one operating point. The proof is the difference argument with [Tellegen's theorem](/tellegen-theorem/) on that page.
- **Number of solutions for polynomial laws.** If every element law is a polynomial and the solutions are isolated, Bézout's theorem bounds their number by the product of the degrees of the equations of $F$ after the linear unknowns are eliminated. The three-solution example meets this bound with one cubic equation.
- **Cost per iteration.** Each Newton iteration costs one device evaluation per element and one MNA solve, $\Theta(N^3)$ with dense LU for $N = n + m$ unknowns and less with sparse LU. Inside the Kantorovich region the number of iterations to reach accuracy $\varepsilon$ is $O(\log \log (1/\varepsilon))$. Outside it, no bound on the number of iterations holds in general.

## Reductions

- **To nonlinear equations.** The problem is the root finding problem $F(x) = 0$ above, so every method for [systems of nonlinear equations](/systems-of-nonlinear-equations/) applies.
- **From nonlinear equations.** Conversely, any system $f(x) = 0$ with $f : \mathbb{R}^n \to \mathbb{R}^n$ continuous is the operating point problem of a circuit: give node $k$ a nonlinear voltage-controlled current source that draws the current $f_k(e)$ from node $k$ to ground, and nothing else. KCL at node $k$ is $f_k(e) = 0$. So the general problem is as hard as solving arbitrary nonlinear systems, and no method can be guaranteed for all circuits; the guarantees above rest on circuit structure.
- **To an equilibrium of the circuit dynamics.** With the capacitors and inductors kept, the circuit is a system of differential-algebraic equations, and its equilibria are exactly the operating points. Integrating in time to an equilibrium is the idea behind [pseudo-transient analysis](/pseudo-transient-analysis/), and the stability of each equilibrium tells which states a real circuit can rest in.

## Applications

- The bias point for [small-signal AC analysis](/ac-small-signal-analysis/) and [noise analysis](/circuit-noise-analysis/), which linearize every device there.
- The initial state of [transient circuit analysis](/transient-circuit-analysis/).
- DC transfer curves of amplifiers and logic gates, such as the switching threshold of an inverter.
- [Adjoint sensitivity analysis](/adjoint-sensitivity-analysis/) of a DC output, which uses the Jacobian at the operating point.
- IR drop analysis of power grids, a large linear DC problem ([power grid analysis](/power-grid-analysis/)).

## References
