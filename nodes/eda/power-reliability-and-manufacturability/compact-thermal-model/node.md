---
tag: KNKRTS
kind: model
slug: compact-thermal-model
name: Compact thermal model
aliases:
- thermal RC network model
- HotSpot model
area: eda/power-reliability-and-manufacturability
level: advanced
summary: An equivalent RC network of the die, spreader and heat sink whose nodes are block temperatures, solved to give chip temperature maps from power maps quickly.
prereqs: [heat-equation, positive-definite-matrix]
see_also: [finite-difference-method, power-grid-analysis, laplacian-matrix, cholesky-decomposition, conjugate-gradient-method, backward-euler-method, leakage-power, black-equation]
sources:
  - paper: doi:10.1109/TVLSI.2006.876103
    title: Wei Huang, Shougata Ghosh, Sivakumar Velusamy, Karthik Sankaranarayanan, Kevin Skadron and Mircea R. Stan, HotSpot, a compact thermal modeling methodology for early-stage VLSI design, IEEE Transactions on Very Large Scale Integration (VLSI) Systems 14(5), 501 to 513, 2006
    locator: the duality between heat flow and electrical current, the construction of the RC network for the die, the interface material, the spreader and the sink at block and grid granularity, the fitted factors, and the comparison with a finite element solver
  - paper: "Kevin Skadron, Mircea R. Stan, Wei Huang, Sivakumar Velusamy, Karthik Sankaranarayanan and David Tarjan, Temperature-aware microarchitecture, International Symposium on Computer Architecture (ISCA), 2003"
    title: Kevin Skadron, Mircea R. Stan, Wei Huang, Sivakumar Velusamy, Karthik Sankaranarayanan and David Tarjan, Temperature-aware microarchitecture, Proceedings of the 30th International Symposium on Computer Architecture, 2003
    locator: the first form of the block-level thermal RC model and its use with architectural power models (general locator, page numbers not checked)
---

A compact thermal model represents the heat flow in a chip package by a network of thermal resistances and capacitances. Each node stands for a block of the die, a cell of a grid, or a part of the package such as the heat spreader or the heat sink, and its unknown is that part's temperature. Given the power that each block dissipates, the model gives the temperatures by solving a small linear system in the steady state, or a linear system of ordinary differential equations in the transient. It is the thermal counterpart of an electrical RC network: temperature plays the part of voltage and heat flow the part of current. Architects and physical designers use it to get a temperature map from a power map in milliseconds, where a finite element solve takes much longer.

The network is a coarse discretization of the [heat equation](/heat-equation/), so its structure is physics. Several of its parameters, though, are fitted: the convection resistance from the heat sink to the air, the conductivity and thickness of the thermal interface material, and correction factors for the spreading of heat and for the lumped capacitances, which make the coarse model match a fine solver or a measurement. The temperatures it gives are as good as these fits.

## The machine

**Nodes.** One node per die block (or grid cell), plus nodes for the interface material, the spreader and the sink, often several per layer. Let $\theta_i = T_i - T_{\text{amb}}$ be the temperature of node $i$ above the ambient air.

**Conductances.** Between two nodes $i$ and $j$ that share a face, heat flows at the rate $g_{ij}(\theta_i - \theta_j)$, Fourier's law in discrete form. For a slab of conductivity $\kappa$, area $A$ and thickness $t$ crossed by the heat, $g = \kappa A / t$. Lateral conductances between neighbor blocks use the shared edge and the distance between the block centers. Nodes on the outside, usually the sink, lose heat to the air at the rate $g_{i0}\, \theta_i$, with $g_{i0}$ the inverse of a fitted convection resistance. All $g_{ij} = g_{ji} \ge 0$.

**Capacitances.** Node $i$ stores heat with capacitance $C_i = c\, V_i > 0$, the volumetric heat capacity times the volume, often scaled by a fitted factor.

**Sources.** $P_i(t) \ge 0$ is the power dissipated in node $i$: switching ([dynamic power](/dynamic-power-dissipation/)) plus [leakage power](/leakage-power/) for die blocks, and 0 for package nodes.

**Equations.** Energy balance at each node gives

$$ C_i \frac{d\theta_i}{dt} = P_i - g_{i0}\theta_i - \sum_j g_{ij} (\theta_i - \theta_j), $$

that is, $C \dot\theta = -G\theta + P$, with $C$ diagonal and $G$ the *conductance matrix*: $G_{ii} = g_{i0} + \sum_j g_{ij}$ and $G_{ij} = -g_{ij}$. In the steady state, $G\theta = P$.

**The duality.**

| thermal | electrical |
|---|---|
| temperature rise $\theta$ (K) | voltage (V) |
| heat flow (W) | current (A) |
| thermal resistance (K/W) | resistance (Ω) |
| heat capacity (J/K) | capacitance (F) |
| power of a block | current source |
| ambient air | ground |

Under this map, $G\theta = P$ is the nodal equation of a resistor network fed by current sources, the same equation as in [power grid analysis](/power-grid-analysis/). $G$ is a weighted [Laplacian matrix](/laplacian-matrix/) of the network plus the diagonal of the ambient conductances.

## What it counts

The model counts temperatures: the steady temperature of each node for a constant power map, and the temperature trajectory for a power trace. It does not resolve features smaller than a node, so the peak temperature inside a block is higher than the node value, and a finer grid is used for hot spots. It assumes constant conductivities (silicon conductivity in fact falls as temperature rises), linear convection at the sink, and a known ambient temperature.

## Relation to other models

- **Heat equation.** The network is a finite volume discretization of the [heat equation](/heat-equation/) on a few coarse cells, the same kind of matrix the [finite difference method](/finite-difference-method/) gives on a fine grid. A fine grid of the same layers turns the compact model into a full solver.
- **Power grid.** The electrical twin of the steady state is the IR drop problem. The same solvers apply: [Cholesky decomposition](/cholesky-decomposition/) for small and medium networks, and the [conjugate gradient method](/conjugate-gradient-method/) with a preconditioner for large grids.
- **Transient.** $C\dot\theta = -G\theta + P$ is a stiff linear system: the die responds in milliseconds and the sink in seconds or minutes. Implicit steps such as the [backward Euler method](/backward-euler-method/) are the usual choice.
- **Leakage.** Leakage power grows roughly exponentially with temperature, so $P$ depends on $\theta$ and the steady state is a fixed point (see below).
- **Reliability.** Temperature enters [Black's equation](/black-equation/) and the NBTI [reaction-diffusion model](/nbti-reaction-diffusion-model/) through Arrhenius factors, so their lifetimes need this model's temperature map.

## Known results in the model

Assume every connected part of the network has at least one node with $g_{i0} > 0$, a path for heat to reach the air. Without it, no steady state exists for positive power.

**Theorem 1 (symmetric positive definite).** $G$ is symmetric and [positive definite](/positive-definite-matrix/).

*Proof.* Symmetry holds since $g_{ij} = g_{ji}$. For any vector $x$, grouping the terms of $x^T G x$ by edge gives

$$ x^T G x = \sum_{\{i,j\}} g_{ij} (x_i - x_j)^2 + \sum_i g_{i0}\, x_i^2 \ \ge\ 0 . $$

If it is 0, then $x_i = x_j$ across every edge with $g_{ij} > 0$, so $x$ is constant on each connected part, and $x_i = 0$ at each node with $g_{i0} > 0$. Each part has such a node, so $x = 0$. $\square$

**Corollary (the steady state).** For each power vector $P$, the steady state is the unique solution of $G\theta = P$. It can be computed by Cholesky, and every eigenvalue of $C^{-1}G$ is real and positive, since $C^{-1}G$ is similar to the symmetric positive definite $C^{-1/2} G C^{-1/2}$. So every transient mode decays, with time constants $1/\lambda$, and $\theta(t)$ tends to $G^{-1}P$ for constant $P$.

**Theorem 2 (more power never cools).** If $P \ge 0$ then $\theta \ge 0$. If the network is connected and $P \ge 0$, $P \ne 0$, then $\theta > 0$ at every node. So all entries of $G^{-1}$ are positive, and raising any block's power raises every temperature.

*Proof.* Let $i$ be a node of smallest $\theta_i$ and suppose $\theta_i < 0$. Row $i$ of $G\theta = P$ reads $g_{i0}\theta_i + \sum_j g_{ij}(\theta_i - \theta_j) = P_i \ge 0$. Each term on the left is $\le 0$, so each is 0: $\theta_j = \theta_i$ for every neighbor, and $g_{i0} = 0$. Repeating at the neighbors spreads the minimum over the connected part, which contains a node with $g_{i0} > 0$, a contradiction. So $\theta \ge 0$. For strictness, if $\theta_i = 0$ at some node, the same row gives $-\sum_j g_{ij}\theta_j = P_i \ge 0$ with all $\theta_j \ge 0$, so the neighbors are 0 and $P_i = 0$, and by connectivity $\theta = 0$ and $P = 0$. Taking $P$ equal to a unit vector shows that each column of $G^{-1}$ is positive. $\square$

**Example.** Three die blocks in a row (nodes 1 to 3), one spreader (node 4) and one sink (node 5). Conductances in W/K: lateral $g_{12} = g_{23} = 1/2$, each block to the spreader 2, spreader to sink 10, sink to air 2. Powers $P = (10, 2, 5, 0, 0)$ W.

$$ G = \begin{pmatrix} 5/2 & -1/2 & 0 & -2 & 0 \\ -1/2 & 3 & -1/2 & -2 & 0 \\ 0 & -1/2 & 5/2 & -2 & 0 \\ -2 & -2 & -2 & 16 & -10 \\ 0 & 0 & 0 & -10 & 12 \end{pmatrix} $$

Its leading principal minors are $5/2$, $29/4$, $35/2$, $175$ and $350$, all positive, as Theorem 1 says. The exact solution, in rational arithmetic, is

$$ \theta = \Big(\tfrac{1019}{70}, \tfrac{839}{70}, \tfrac{879}{70}, \tfrac{51}{5}, \tfrac{17}{2}\Big) \approx (14.56,\ 11.99,\ 12.56,\ 10.20,\ 8.50)\ \text{K}. $$

The sink is at $17/2$ K because all 17 W leave through its 2 W/K, and the spreader is $17/10$ K above it because all 17 W cross the 10 W/K link. The smallest entry of $G^{-1}$ is $1/2$ K/W, positive, as Theorem 2 says. Putting all 17 W in block 1 gives block temperatures $(17.24, 11.41, 10.44)$ K, and putting it in block 2 gives $(11.41, 16.27, 11.41)$ K. The package nodes do not change, but the hottest block is 1.0 K cooler when the power sits in the middle, where it spreads both ways.

**Leakage and thermal runaway.** Take one node with thermal resistance $R$ to the air, dynamic power $P_d$ and a leakage model $P_\ell(\theta) = P_{\ell 0} e^{\beta\theta}$, itself a fitted law. The steady state solves $\theta = R(P_d + P_{\ell 0} e^{\beta\theta})$. A solution stops existing when the right side becomes tangent to the line, that is when $R\beta P_{\ell 0} e^{\beta\theta} = 1$ at a solution, which gives the critical $R$ by $1 + \beta R P_d = \ln(1/(R\beta P_{\ell 0}))$. For $P_d = 40$ W, $P_{\ell 0} = 10$ W and $\beta = 0.02$ per K, the iteration $\theta \leftarrow R(P_d + P_{\ell 0}e^{\beta\theta})$ from $\theta = 0$ converges in 18 steps to $\theta = 28.92$ K for $R = 0.5$ K/W. The critical value is $R \approx 0.897$ K/W, and above it the iteration diverges: in this model the chip has no steady state and heats without bound, which is thermal runaway. Real packages limit power before this point, and the exponential leakage law stops holding at high temperature.

## References
