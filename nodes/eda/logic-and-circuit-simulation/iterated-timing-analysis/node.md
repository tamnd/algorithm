---
tag: 8PGXDW
kind: algorithm
slug: iterated-timing-analysis
name: Iterated timing analysis
aliases:
- ITA
- SPLICE relaxation
area: eda/logic-and-circuit-simulation
level: advanced
summary: Saleh, Kleckner and Newton's event-driven Gauss-Seidel-Newton relaxation that solves the backward Euler node equations of a circuit node by node at each time point.
solves: [transient-circuit-analysis]
model: real-ram
complexity:
  vars: {s: the number of time steps, N: the number of unknown nodes, T: the number of circuit elements, K: the largest number of relaxation sweeps at one time point}
  time: {worst: "O(s K (N + T))", best: "O(s N + T)"}
  space: {extra: "O(N + T)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1983
  people: [Resve A. Saleh, James E. Kleckner, A. Richard Newton]
  note: Iterated timing analysis was described for the SPLICE1 mixed-mode simulator at the IEEE International Conference on Computer-Aided Design in 1983.
prereqs: [transient-circuit-analysis, timing-simulation, gauss-seidel-method, newton-method-for-systems, backward-euler-method, shichman-hodges-model]
see_also: [timing-simulation, mixed-mode-simulation, picard-iteration, event-driven-logic-simulation, channel-connected-component, diagonally-dominant-matrix, modified-nodal-analysis, tr-bdf2]
sources:
  - paper: "Resve A. Saleh, James E. Kleckner and A. Richard Newton, Iterated timing analysis in SPLICE1, IEEE International Conference on Computer-Aided Design (ICCAD-83), Digest of Technical Papers, 139 to 140, 1983"
    title: Resve A. Saleh, James E. Kleckner and A. Richard Newton, Iterated timing analysis in SPLICE1, ICCAD-83 Digest of Technical Papers, 139 to 140, 1983
    locator: the method (event-driven nonlinear Gauss-Seidel relaxation with one Newton step per node, repeated at each time point until convergence) and its use in SPLICE1
  - paper: doi:10.1109/TCAD.1984.1270089
    title: A. R. Newton and A. L. Sangiovanni-Vincentelli, Relaxation-based electrical simulation, IEEE Transactions on Computer-Aided Design 3(4), 308 to 331, 1984
    locator: nonlinear relaxation at the level of the time-discretized equations, Gauss-Seidel-Newton and its convergence conditions, timing simulation as one sweep, iterated timing analysis, and waveform relaxation
  - paper: doi:10.1109/TCS.1975.1084003
    title: B. R. Chawla, H. K. Gummel and P. Kozak, MOTIS, an MOS timing simulator, IEEE Transactions on Circuits and Systems CAS-22(12), 901 to 910, 1975
    locator: the one-sweep node-by-node update that iterated timing analysis repeats to convergence
  - book: isbn:9780898714616
    title: James M. Ortega and Werner C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000 (first published 1970)
    locator: Chapter 10, Ostrowski's theorem on points of attraction and its use for nonlinear Gauss-Seidel and SOR-Newton iterations
  - paper: doi:10.1109/JSSC.1968.1049902
    title: Harold Shichman and David A. Hodges, Modeling and simulation of insulated-gate field-effect transistor switching circuits, IEEE Journal of Solid-State Circuits 3(3), 285 to 289, 1968
    locator: the square-law MOSFET model used by the tests
---

Iterated timing analysis (ITA) computes the transient response of a large MOS circuit by solving the [backward Euler](/backward-euler-method/) node equations at each time point with nonlinear [Gauss-Seidel](/gauss-seidel-method/) relaxation: it updates one node at a time by one Newton step on that node's own equation, and repeats the updates that events trigger until no node moves by more than a tolerance. It belongs to the circuit simulation half of the logic and circuit simulation sub-area. It is [timing simulation](/timing-simulation/) iterated to convergence: MOTIS makes one sweep per time point, and ITA keeps sweeping, so it gets the backward Euler solution of [transient circuit analysis](/transient-circuit-analysis/) without building or factoring a circuit matrix. Saleh, Kleckner and Newton introduced it in the SPLICE1 simulator in 1983.

## In plain words

A circuit simulator moves time forward in small steps. At each step it must find voltages that make the currents at every node add up to zero. The usual way solves for all nodes at once with a large matrix, which costs a lot for a big chip.

Iterated timing analysis takes the nodes one at a time. For one node it holds its neighbours still and moves the node to make its own currents balance, as well as one quick correction allows. Then it goes to the next node. A node that moves wakes up its neighbours, because their currents changed; a node that does not move lets them sleep. When nothing is awake, the time step is done.

In a digital chip most nodes are quiet most of the time. Those nodes cost nothing, and that is where the speed comes from.

## The problem

The circuit has nodes, some fixed (ground, supplies and inputs, with given waveforms) and $N$ unknown. Its elements are capacitors, resistors, voltage-controlled current sources and MOSFETs with the square-law [Shichman-Hodges model](/shichman-hodges-model/), whose transconductance $k$, threshold $V_T$ and channel-length modulation $\lambda$ are fitted to measured device curves. With step $h$ and previous voltages $v^n$, the backward Euler [companion model](/companion-model/) turns each capacitor $C$ between nodes $i$ and $j$ into a current $C(\Delta v_i - \Delta v_j)/h$ with $\Delta v = v - v^n$. The node equation of unknown node $i$ is

$$F_i(v) = \sum_{\text{capacitors at } i} \frac{C}{h} (\Delta v_i - \Delta v_j) + \sum_{\text{other elements at } i} I_{\text{out}}(v) = 0,$$

the sum of the currents that leave node $i$. This is the nodal part of [modified nodal analysis](/modified-nodal-analysis/), with voltage sources only at fixed nodes, so no branch currents appear. The *fanout* of node $i$ is the set of unknown nodes $j$ whose $F_j$ depends on $v_i$: the nodes that share an element with $i$ through which current flows at $j$. It includes $i$ and, for a transistor, the drain and source nodes of every transistor whose gate is $i$.

Input: the circuit, the initial voltages $v^0$ (consistent, for example a DC operating point), the step $h$, the number of steps $s$ and the tolerance $\tau$. Output: the voltages at the times $h, 2h, \ldots, sh$.

## The algorithm

```pseudo id=main
ITA(circuit, v0, h, s, τ)
L1  v ← v0 with the fixed nodes at time 0; A ← all unknown nodes
L2  for k = 1, 2, ..., s
L3      vⁿ ← v; set the fixed nodes to their values at t = kh; add to A the fanout of each fixed node that changed
L4      Q ← a first-in first-out queue holding the nodes of A
L5      while Q is not empty
L6          i ← remove the first node of Q
L7          (F, D) ← F_i(v) and ∂F_i/∂v_i, at the newest voltages
L8          δ ← −F / D; v_i ← v_i + δ
L9          if |δ| > τ: append to Q each node of fanout(i) that is not in Q
L10     A ← the fanout of each node with |v_i − vⁿ_i| > τ; record v at t = kh
L11 return the recorded waveforms
```

Line L8 is one Newton step on the equation of node $i$ alone, with every other voltage at its newest value: a Gauss-Seidel-Newton update. Line L9 is the selective trace of [event-driven logic simulation](/event-driven-logic-simulation/) moved to the analog level: a node that changed by more than $\tau$ schedules the nodes whose equations read it, itself included, since one Newton step does not solve a nonlinear equation. A node is evaluated again only when something it reads has moved. Lines L5 to L9 end when every node has settled.

Line L10 exploits latency. A node that did not move by more than $\tau$ in this step, and whose neighbours did not either, is not evaluated in the next step; it keeps its voltage. A guard on the number of evaluations at one time point (here $200N$) stops the loop if the relaxation does not converge.

## Example

**One time point by hand.** Two nodes, each with a capacitor of 1 F and a conductance of 1 S to ground, joined by a conductance of 1 S; $h = 1$ s, $v^n = (1, 0)$ V and $\tau = 0.01$ V. The node equations are $F_1 = 3v_1 - v_2 - 1$ and $F_2 = 3v_2 - v_1$, linear, so each update solves its node exactly. The backward Euler solution is $(3/8, 1/8)$.

| update | node | new value | $\delta$ | queue after |
| --- | --- | --- | --- | --- |
| 1 | 1 | $1/3$ | $-2/3$ | 2, 1 |
| 2 | 2 | $1/9$ | $1/9$ | 1, 2 |
| 3 | 1 | $10/27$ | $1/27$ | 2, 1 |
| 4 | 2 | $10/81$ | $1/81$ | 1, 2 |
| 5 | 1 | $91/243$ | $1/243$ | 2 |
| 6 | 2 | $91/729$ | $1/729$ | empty |

After update 2 the errors are $1/24$ and $1/72$; after update 4 they are $1/216$ and $1/648$, nine times smaller. This is Gauss-Seidel on $\begin{pmatrix} 3 & -1 \\ -1 & 3 \end{pmatrix}$, whose rate is $(1/3)^2$. The loop stops after six evaluations, when both moves are below $\tau$, with errors $5.1 \times 10^{-4}$ and $1.7 \times 10^{-4}$ V.

**An inverter chain.** Four CMOS inverters with $V_{DD} = 1.8$ V, $k = 200\ \mu\mathrm{A/V^2}$, $V_T = 0.5$ V and $\lambda = 0.05\ \mathrm{V^{-1}}$ for both device types (typical fitted values), a load of 10 fF on each output and a gate-drain capacitance of 2 fF from each output to its input, which couples neighbouring nodes in both directions. The input rises from 0 to 1.8 V between 100 and 150 ps, and $h = 1$ ps for 600 steps. The 0.9 V crossings of the first three outputs, measured by linear interpolation of the waveforms:

| method | output 1 (ps) | output 2 (ps) | output 3 (ps) | largest difference from full Newton (V) | work |
| --- | --- | --- | --- | --- | --- |
| backward Euler, full Newton | 225.45 | 381.95 | 544.15 | 0 | 1600 Newton iterations, each with a 4 by 4 LU |
| ITA, $\tau = 10^{-4}$ | 225.45 | 381.95 | 544.13 | $3.9 \times 10^{-4}$ | 4588 node evaluations |
| ITA, $\tau = 10^{-6}$ | 225.45 | 381.95 | 544.15 | $2.9 \times 10^{-6}$ | 7712 node evaluations |
| ITA, $\tau = 10^{-8}$ | 225.45 | 381.95 | 544.15 | $2.7 \times 10^{-8}$ | 10797 node evaluations |
| one sweep per step (MOTIS) | 226.37 | 377.78 | 531.32 | 0.129 | 2400 node evaluations |

ITA reproduces the backward Euler waveforms to within about $3\tau$. The single sweep does not: the gate-drain capacitances couple each output back to its input, and one sweep takes that coupling one step late, which moves the third crossing by 12.8 ps.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows the following.

1. On a linear node equation, one Newton node update solves it exactly, so on a linear circuit ITA is linear Gauss-Seidel.
2. If the node Jacobian $C/h + G(v)$ is strictly [diagonally dominant](/diagonally-dominant-matrix/) by rows with ratio $\rho < 1$, a sweep of exact node solves reduces the maximum-norm error by the factor $\rho$, and a sweep that moves no node by more than $\tau$ is within $\rho\tau/(1 - \rho)$ of the backward Euler solution.
3. With one Newton step per node, the sweeps converge locally at an asymptotic rate of at most $\rho$ (by Ostrowski's theorem, cited).
4. If every node has a capacitance to ground, small enough steps make the Jacobian dominant: $\rho \to \max_i \kappa_i / C_{ii}$ as $h \to 0$, where $\kappa_i$ is the capacitance from node $i$ to other unknown nodes.
5. The event-driven loop performs only Newton node updates and stops only when every node's last update, and every later update of a node it reads, is at most $\tau$.

The distance between the event-driven result and the backward Euler solution is not bounded by the proof. The tests measure it. They compare with backward Euler solved by full Newton on all nodes ($\|\Delta x\|_\infty \le 10^{-12}$ V), on the chain above, on a victim node coupled by 20 fF to an aggressor, and on random linear RC networks (seed 63), where each measured sweep ratio stays below the computed $\rho$.

## Complexity

One node evaluation reads the elements at the node. A sweep costs $O(N + T)$, and with at most $K$ sweeps' worth of evaluations per time point, $s$ steps cost $O(s K (N + T))$. No matrix is formed or factored, and the memory is $O(N + T)$ beyond the waveforms. When all nodes are latent, a step costs only the copy of the voltages, $O(N)$.

On a chain of eight inverters, the node evaluations with $\tau = 10^{-6}$ V were 23394 in the first 1000 steps, 25157 in the next 1000 and 0 in the 1000 after that, once the edge had passed the last stage (measured). A method without latency spends at least $N$ evaluations in every step.

## Properties

- **Matrix-free.** Only diagonal derivatives $\partial F_i/\partial v_i$ are needed; the off-diagonal derivatives never appear.
- **Converges to backward Euler.** Unlike one-sweep timing simulation, the result does not depend on the node order once the relaxation has converged.
- **Conditional convergence.** It needs a diagonally dominant node Jacobian, which small steps and grounded capacitances give. Full Newton does not need it.
- **Event-driven.** Work follows activity, both within a time point (selective trace) and across time points (latency).
- **First order in time.** The accuracy in time is that of backward Euler. The relaxation tolerance $\tau$ adds an error of about the same order as $\tau$.

## Variants and improvements

- **Subcircuits instead of nodes.** Group tightly coupled nodes, for example the [channel-connected components](/channel-connected-component/) of the transistor network, and solve each group by Newton's method with a small matrix, then relax between groups. This keeps strong two-way coupling inside a group.
- **Gauss-Jacobi and SOR.** Updating all nodes from the old values allows parallel evaluation at a slower rate; over-relaxation can speed up the convergence of linear parts.
- **Variable and per-node time steps.** SPLICE-style simulators choose the step from the activity of the nodes and schedule node evaluations as timed events.
- **Higher-order formulas.** The trapezoidal rule or [TR-BDF2](/tr-bdf2/) can replace backward Euler in the node equations; the relaxation is the same.
- **Waveform relaxation.** Relax whole waveforms of subcircuits over a time window instead of values at one time point. It is the [Picard iteration](/picard-iteration/) on subcircuits and lets each subcircuit take its own steps.
- **Mixed mode.** ITA fits an event-driven [mixed-mode simulator](/mixed-mode-simulation/), since an analog node that is not active is not evaluated.

## When to use it

Use ITA for large digital or mostly digital MOS circuits, where most nodes are idle at any time, couplings are mostly one-way through transistor gates, every node has a capacitance to ground, and a full sparse factorization at each Newton iteration is too costly. Use full Newton with a sparse solver, such as [KLU](/klu-solver/), for analog blocks with strong feedback, for circuits with floating nodes or large coupling capacitances, and whenever the relaxation stops converging at the step size that accuracy needs.

## Pitfalls

- **Strong two-way coupling.** If off-diagonal terms outweigh the diagonal, the relaxation diverges where full Newton does not. Two nodes with 1 F and 1 S to ground, coupled by controlled sources of $+2$ and $-2$ S (a stable circuit), have a Gauss-Seidel rate of $4/(1/h + 1)^2$. ITA converged at $h = 0.25$ and $0.5$ s and exceeded the evaluation limit at $h = 1$ and $2$ s, while full Newton solved every step.
- **Steps too large for dominance.** On the inverter chain the measured $\rho$ along the trajectory was 0.283 at $h = 1$ ps, close to the limit $4/14$ of the coupling capacitances, but above 1 at $h = 100$ ps.
- **A loose tolerance freezes nodes.** With $\tau = 10^{-4}$ V on the eight-stage chain over 4 ns, nodes went latent while still settling, and the largest difference from full Newton was 5.6 mV.
- **Floating nodes.** A node with no capacitance to ground has $c_i = 0$, so $\kappa_i/C_{ii} = 1$ and small steps do not help.
- **No error bound from the tolerance alone.** The stop of the event-driven loop is local; many small moves of a neighbour can add up. Keep $\tau$ well below the accuracy that is needed.

## Implementations

## History

MOTIS (Chawla, Gummel and Kozak, 1975) introduced the one-sweep node-by-node update for MOS circuits. Saleh, Kleckner and Newton described iterated timing analysis for the SPLICE1 mixed-mode simulator at ICCAD-83: the sweep is repeated at each time point, with event-driven scheduling of the nodes to evaluate, until the relaxation converges. Newton and Sangiovanni-Vincentelli (1984) placed timing simulation, ITA and waveform relaxation in one framework of relaxation methods for circuit equations, with their convergence conditions.

## References
