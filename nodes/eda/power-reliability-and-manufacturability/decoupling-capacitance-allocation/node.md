---
tag: AHRKAH
kind: problem
slug: decoupling-capacitance-allocation
name: Decoupling capacitance allocation
aliases:
- decap placement
- decap sizing
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Place and size on-chip decoupling capacitors in free space so that power grid voltage droops meet their limit with the least total decap area.
prereqs: [power-grid-analysis, transient-circuit-analysis]
see_also: [adjoint-sensitivity-analysis, floorplanning, companion-model, multigrid-power-grid-analysis, vectorless-power-grid-verification, power-gating, leakage-power, gradient-descent]
sources:
  - paper: "Shiyou Zhao, Kaushik Roy and Cheng-Kok Koh, Decoupling capacitance allocation and its application to power-supply noise-aware floorplanning, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 21(1), 81 to 92, 2002"
    title: Shiyou Zhao, Kaushik Roy and Cheng-Kok Koh, Decoupling capacitance allocation and its application to power-supply noise-aware floorplanning, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 21(1), 81 to 92, 2002
    locator: the allocation of decoupling capacitance to the blocks of a floorplan from the noise of a transient grid model, and its use inside floorplanning
  - paper: "Haihua Su, Sachin S. Sapatnekar and Sani R. Nassif, Optimal decoupling capacitor sizing and placement for standard-cell layout designs, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 22(4), 428 to 436, 2003"
    title: Haihua Su, Sachin S. Sapatnekar and Sani R. Nassif, Optimal decoupling capacitor sizing and placement for standard-cell layout designs, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 22(4), 428 to 436, 2003
    locator: the problem with the free space of the rows as sites, the integral of the droop over the limit as the measure, and its gradient by the adjoint method
  - paper: "Sani R. Nassif, Power grid analysis benchmarks, Proceedings of the Asia and South Pacific Design Automation Conference, 376 to 381, 2008"
    title: Sani R. Nassif, Power grid analysis benchmarks, Proceedings of the Asia and South Pacific Design Automation Conference, 376 to 381, 2008
    locator: the RC and RLC grid models with node capacitances used for transient analysis
---

Decoupling capacitance allocation is the problem of choosing where to put extra capacitors on a chip, between the supply grid and the ground grid, and how large to make each one, so that the short dips of the supply voltage stay within their limit with the least total capacitor area. When a block starts to switch, it draws a burst of current within a fraction of a nanosecond. The grid and the package cannot deliver that current at once, because of their resistance and inductance, so the supply at the block droops. A capacitor near the block holds charge and gives it up during the burst, and the grid refills it afterwards. Decoupling capacitors, or decaps, take area, usually in the free space left between cells or blocks, and the common thin-oxide decaps leak, so they are not free. The problem is a nonlinear optimization over a transient simulation of the grid. A decap cannot fix a drop that persists, only a droop that is short compared with the time it takes the grid to recharge the capacitor.

## In plain words

Think of a busy kitchen tap fed by a long, thin pipe. When many people draw water at once, the pressure at the tap falls. A small tank next to the tap smooths this out: it gives water during the rush and refills when the rush is over.

Decaps are these tanks for electric charge. The question is how big each tank should be and where to put it, so that the voltage never falls too far, while using as little chip area as possible. A tank right next to the busy spot helps much more than the same tank far away.

## Definition

**Instance.** A power grid in drop form, as on the [power grid analysis](/power-grid-analysis/) page: a conductance matrix $G$, a diagonal matrix $C_0$ of the capacitance that the grid nodes already have from the cells and the wires, and load currents $i(t) \ge 0$ on a time window $[0, t_f]$, for example the current waveforms of the blocks over one clock cycle. A set of candidate sites $K$, each at a grid node, with a largest capacitance $c^{\max}_k$ that fits in the free space there. A droop limit $x_{\max}$.

**Output.** Decap values $c_k$ with $0 \le c_k \le c^{\max}_k$ such that the drop $x(t)$, the solution of

$$ (C_0 + \mathrm{diag}(c))\, \dot{x}(t) + G x(t) = i(t), \qquad x(0) = G^{-1} i(0), $$

meets $x_m(t) \le x_{\max}$ at every node $m$ and every time $t$ in the window, with the least total $\sum_{k \in K} c_k$. Here $c$ is placed on the diagonal at the nodes of the sites. For an RLC grid, the inductances of the package add their currents as extra unknowns.

**Decision version.** Given also a budget $A$, is there a feasible allocation with $\sum_k c_k \le A$?

**What is fitted.** The capacitance per unit area of a decap, about $\varepsilon_{ox} / t_{ox}$ for a thin-oxide MOS decap, is a property of the process. Its leakage and its series resistance are fitted to measurements. The current waveforms $i(t)$ come from simulation or from estimates of the activity of each block, and they are the least certain input. The grid conductances and the package model are as on the power grid analysis page.

## Variants

- **Floorplan level.** The sites are the white space between the blocks of a [floorplan](/floorplanning/), and the floorplanner can move blocks to make room for decaps near noisy blocks, as in Zhao, Roy and Koh (2002).
- **Placement level.** The sites are the free space in the rows of a standard-cell layout, as in Su, Sapatnekar and Nassif (2003).
- **Soft violation measure.** Instead of the hard limit at every node and time, minimize the integral over time and nodes of the droop above the limit, $\sum_m \int_0^{t_f} \max(0, x_m(t) - x_{\max})\, dt$, which is smoother and has a gradient almost everywhere.
- **With leakage.** Add the leakage of the decaps to the cost, since thin-oxide decaps leak much.
- **With package inductance.** With RLC models the chip capacitance and the package inductance form a resonant circuit, and too much or too little decap can move the resonance to a frequency at which the loads are strong.
- **Frequency domain.** Require that the impedance of the grid seen from each load stays below a target over a band of frequencies, a common rule at the board and package level.
- **Unknown loads.** With bounds on the currents instead of waveforms, as in [vectorless verification](/vectorless-power-grid-verification/).

## Examples

**One node.** A node gets its supply through a conductance $g = 10$ S, that is $0.1\ \Omega$. A block at this node draws a step of $I = 2$ A for $\tau = 1$ ns, from rest. Without decap the drop jumps to $I / g = 200$ mV. The limit is $x_{\max} = 100$ mV. With a decap $c$ at the node, $c \dot{x} + g x = I$ gives

$$ x(t) = \frac{I}{g} \left(1 - e^{-g t / c}\right), $$

which grows with $t$, so the worst drop is at $t = \tau$. The limit holds if and only if

$$ c \ \ge\ \frac{g \tau}{-\ln(1 - g x_{\max} / I)} = \frac{10 \cdot 10^{-9}}{\ln 2} \approx 14.4 \text{ nF}. $$

The simple charge rule $c = Q / \Delta V = I \tau / x_{\max} = 20$ nF is safe but asks for 39% more, because it ignores the current that the grid supplies during the burst. With an assumed density of 10 fF per square micrometer, 14.4 nF takes about 1.44 square millimeters. If the burst lasted much longer, the drop would reach $I / g = 200$ mV for any finite $c$: a decap only delays the drop.

**Location matters.** Take a chain: a pad of 10 S at node 1, a wire of 10 S from node 1 to node 2, and a step of 1 A for 1 ns at node 2, with no other capacitance. The DC drops are 100 mV at node 1 and 200 mV at node 2. The limit at node 2 is 120 mV. A decap at node 2 sees the whole path of $0.2\ \Omega$, so $x_2(t) = 0.2 (1 - e^{-5 t / c})$, and it needs $c \ge 5 \cdot 10^{-9} / \ln 2.5 \approx 5.46$ nF. A decap at node 1 cannot help with the wire from node 1 to node 2, which always carries the full 1 A and adds 100 mV, so it must hold $x_1(1 \text{ ns}) \le 20$ mV, which needs $c \ge 10 \cdot 10^{-9} / \ln 1.25 \approx 44.8$ nF. Putting the decap one wire away from the load costs 8.2 times more capacitance. A backward Euler simulation with 20000 steps and a bisection on $c$ gave the same two values to three digits.

## Known algorithms

- **Charge-based rules.** Give each block a decap of $Q / \Delta V$ from the charge it draws in a cycle. Simple and safe at one node, as the bound below shows, and often wasteful.
- **Allocation to a floorplan.** Zhao, Roy and Koh (2002) estimate the noise of each block from a transient model of the grid, find the decap each block needs, and feed the demand for white space back into [floorplanning](/floorplanning/).
- **Sensitivity-based optimization.** Su, Sapatnekar and Nassif (2003) minimize the integral violation measure over the decap sizes. They compute its gradient for all sites at once with one forward and one backward transient run, by the [adjoint method](/adjoint-sensitivity-analysis/), and use it in a gradient-based nonlinear optimizer, a relative of [gradient descent](/gradient-descent/).
- **Transient analysis inside the loop.** Each check of a candidate needs a transient simulation of the grid with its [companion model](/companion-model/), which fast grid solvers such as the [multigrid-like method](/multigrid-power-grid-analysis/) make cheaper.

## Bounds

**Fact 1 (decaps cannot fix a persistent drop).** If the load is constant, $i(t) = i_0$, then $x(t) \to G^{-1} i_0$ as $t \to \infty$, whatever the decap. So if the DC drop $G^{-1} i_0$ exceeds $x_{\max}$ at some node and the load lasts long enough, no allocation is feasible.

*Proof.* Let $C = C_0 + \mathrm{diag}(c)$ with positive diagonal and $y = x - G^{-1} i_0$. Then $C \dot{y} = - G y$. With $E(t) = y^T C y$, $\dot{E} = 2 y^T C \dot{y} = -2 y^T G y \le -2 \lambda_{\min}(G) |y|^2 \le -2 (\lambda_{\min}(G) / \max_m C_{mm}) E$, and $\lambda_{\min}(G) > 0$ because $G$ is positive definite, as the power grid analysis page proves. So $E$ decays to 0 exponentially, and $y \to 0$. $\square$

**Fact 2 (the charge rule is safe at one node).** For one node with $c \dot{x} + g x = i(t)$, $i \ge 0$ and $x(0) = 0$, the drop satisfies $x(t) \le \frac{1}{c} \int_0^t i(s)\, ds$. So $c \ge Q / x_{\max}$, with $Q$ the charge drawn in the window, is sufficient.

*Proof.* Since $i \ge 0$ and $x(0) = 0$, the solution $x(t) = \frac{1}{c} \int_0^t e^{-g (t - s)/c} i(s)\, ds$ is nonnegative, and each factor $e^{-g(t-s)/c} \le 1$. $\square$

- **Complexity.** We do not know a published proof that the problem is NP-hard, and this page claims none. Each feasibility check is a transient simulation, and the constraint $\max_t x_m(t) \le x_{\max}$ is not convex in $c$ in general, so the known methods are local or heuristic.
- **What is measured.** The reductions of noise and decap area that the papers report are measurements on their own designs and grids. This page does not repeat them.

## Reductions

- **To nonlinear programming.** With the soft violation measure, the problem is a smooth nonlinear program in $c$ with box constraints, whose gradient the adjoint method gives.
- **One node to a closed form.** For one node and a step load, the example gives the least decap exactly.
- **From power grid analysis.** Every candidate is checked by a transient [power grid analysis](/power-grid-analysis/), so the problem calls that problem many times.

## Applications

- **Floorplanning and placement.** White space is kept near noisy blocks and filled with decap cells after placement.
- **Power gating.** When a gated block wakes up, the inrush current recharges it and can droop the grid of its neighbors. Decaps on the always-on grid absorb this, as on the [power gating](/power-gating/) page.
- **Sign-off.** Dynamic IR drop checks include the decap of each layout and report where more decap would help.

## References
