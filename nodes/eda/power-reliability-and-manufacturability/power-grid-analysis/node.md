---
tag: YA5KK3
kind: problem
slug: power-grid-analysis
name: Power grid analysis
aliases:
- IR drop analysis
- power distribution network analysis
area: eda/power-reliability-and-manufacturability
level: core
summary: Compute the voltage drop at every node of an on-chip power grid, modelled as a large RC or RLC mesh with current loads, statically or over time.
prereqs: [modified-nodal-analysis, laplacian-matrix, kirchhoff-circuit-laws]
see_also: [multigrid-power-grid-analysis, random-walk-power-grid-analysis, vectorless-power-grid-verification, decoupling-capacitance-allocation, cholesky-decomposition, conjugate-gradient-method, electrical-flow, black-equation]
sources:
  - paper: "Sani R. Nassif, Power grid analysis benchmarks, Proceedings of the Asia and South Pacific Design Automation Conference, 376 to 381, 2008"
    title: Sani R. Nassif, Power grid analysis benchmarks, Proceedings of the Asia and South Pacific Design Automation Conference, 376 to 381, 2008
    locator: the model of the grid as resistors, capacitors, inductors and current loads, the DC and transient problems, and the IBM power grid benchmarks
  - paper: "Joseph N. Kozhaya, Sani R. Nassif and Farid N. Najm, A multigrid-like technique for power grid analysis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 21(10), 1148 to 1160, October 2002"
    title: Joseph N. Kozhaya, Sani R. Nassif and Farid N. Najm, A multigrid-like technique for power grid analysis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 21(10), 1148 to 1160, October 2002
    locator: the formulation of DC and transient power grid analysis as a sparse symmetric positive definite system
  - book: isbn:9780898713213
    title: Abraham Berman and Robert J. Plemmons, Nonnegative Matrices in the Mathematical Sciences, SIAM, 1994
    locator: the chapter on M-matrices and their equivalent conditions, including the nonnegative inverse
---

Power grid analysis is the problem of finding the voltage at every node of the on-chip network that carries the supply to the cells, given the wires of the network, the connections to the package, and the currents that the cells draw. The difference between the supply voltage and the voltage that a cell sees is its IR drop. A cell that sees too low a supply is slow and can fail timing, so every chip is checked for its worst drop. The grid is a mesh of metal wires on several layers, with vias between them and from millions to billions of nodes. In the static or DC case the drops solve one sparse linear system $G x = i$, where $G$ is a symmetric M-matrix, a weighted [Laplacian](/laplacian-matrix/) plus the conductances of the pads. In the dynamic case, capacitors and the inductance of the package add a system of differential equations. The problem is easy in theory, a linear system with a unique solution, and hard in practice only through its size.

## In plain words

The supply enters the chip at a few pads and spreads over a fine mesh of metal wires to all the cells. Each wire has a small resistance. Each cell pulls a current out of the mesh. The current flowing through the resistance of the wires makes the voltage sag, a little near the pads and more far from them, the same way water pressure falls along a long hose.

Power grid analysis computes this sag at every point of the mesh. It is a big but well-behaved set of equations: one equation per node, saying that the current flowing in equals the current flowing out.

## Definition

**Instance (DC).** An undirected graph on the grid nodes $1, \ldots, N$, with a conductance $g_{jk} = g_{kj} > 0$ on each wire or via $\{j, k\}$; a pad conductance $g^{\mathrm{pad}}_k \ge 0$ from node $k$ to an ideal supply at $V_{DD}$, which models the path through a pad, a bump and the package; and a load current $i_k \ge 0$ drawn at each node. Every connected part of the graph has at least one node with $g^{\mathrm{pad}}_k > 0$.

**Output.** The node voltages $v$ that satisfy [Kirchhoff's current law](/kirchhoff-circuit-laws/) at every node, or the drops $x = V_{DD} \mathbf{1} - v$, which solve

$$ G x = i, \qquad G = \mathcal{L} + \mathrm{diag}(g^{\mathrm{pad}}), \qquad \mathcal{L}_{kk} = \sum_j g_{kj}, \quad \mathcal{L}_{jk} = -g_{jk} \ (j \ne k). $$

Write $D_k = G_{kk} = \sum_j g_{kj} + g^{\mathrm{pad}}_k$. This is the [modified nodal analysis](/modified-nodal-analysis/) of a circuit of resistors and current sources, with the supply nodes eliminated. The usual question that follows is a check: is $\max_k x_k$ below a limit, often 5% to 10% of $V_{DD}$, and does each wire carry a current density below its [electromigration](/black-equation/) limit?

**Instance (transient).** Also a capacitance $C$ from the nodes to ground, for the cells, the wires and the [decoupling capacitors](/decoupling-capacitance-allocation/), loads $i(t)$ that change over time, and for an RLC grid the inductances of the package. The output is $x(t)$ on a time interval, which for an RC grid solves

$$ C \dot{x}(t) + G x(t) = i(t), $$

with $x(0)$ the DC drop. With inductors, the inductor currents become extra unknowns, as in modified nodal analysis, and the drop can ring.

**IR drop.** The IR drop at node $k$ is $x_k = V_{DD} - v_k$, the loss of supply voltage caused by the currents through the resistance of the grid. On the ground grid the same model gives the rise of the ground voltage, often called ground bounce. The cell sees the sum of the two.

**M-matrix.** A square real matrix $A$ is a nonsingular M-matrix when its entries off the diagonal are $\le 0$, it is nonsingular, and its inverse has no negative entries. This is one of many equivalent definitions.

**Discrete harmonic function.** A function $h$ on the nodes is discrete harmonic at node $m$ when $h_m = \sum_j (g_{mj} / D_m) h_j$, a weighted mean of its neighbors, with the supply counted as a neighbor of value 0 through the weight $g^{\mathrm{pad}}_m / D_m$. Row $m$ of $G x = i$ divided by $D_m$ reads $x_m = i_m / D_m + \sum_j (g_{mj} / D_m) x_j$, so the drop is discrete harmonic at every node without a load, and at a loaded node it is above the mean of its neighbors by $i_m / D_m$.

**What is fitted.** The wire conductances come from the layout and from the sheet resistance of each metal layer and the resistance of each via, which are measured on test structures and given by the foundry. The pad conductance and the package inductance are fitted to measurements or to a package model. The load currents are estimates, from simulation or from [power estimation](/rtl-power-macromodeling/), and they are the least certain input. The analysis is exact for its inputs. Its answer is as good as these numbers.

## Variants

- **Static (DC) IR drop.** Average or peak currents, one linear solve.
- **Dynamic IR drop.** Currents over time, a transient solve with the decoupling capacitance and, at the chip level, the package inductance.
- **Vectorless verification.** The currents are not known, only bounds on them, and the question is the worst drop over all currents that meet the bounds. See [vectorless power grid verification](/vectorless-power-grid-verification/).
- **Single-node queries.** The drop at a few nodes only, for example after a local change.
- **Incremental analysis.** The grid or the loads change a little, and the old answer should be reused.
- **Electromigration check.** From $x$ follow the current of each wire, $g_{jk} (x_k - x_j)$, and its current density, which [Black's equation](/black-equation/) and the [Blech length](/blech-length/) turn into a lifetime check.

## Examples

Take a chain of 3 nodes. Node 0 has a pad of 20 S, the wires 0 to 1 and 1 to 2 have 10 S each, and the loads are 0.2 A at node 1 and 0.3 A at node 2. Then

$$ G = \begin{pmatrix} 30 & -10 & 0 \\ -10 & 20 & -10 \\ 0 & -10 & 10 \end{pmatrix}, \qquad i = \begin{pmatrix} 0 \\ 0.2 \\ 0.3 \end{pmatrix}. $$

By hand: all 0.5 A leaves through the pad, so $x_0 = 0.5 / 20 = 25$ mV. The wire from 0 to 1 carries 0.5 A, so $x_1 = 25 + 50 = 75$ mV. The wire from 1 to 2 carries 0.3 A, so $x_2 = 75 + 30 = 105$ mV. With $V_{DD} = 1$ V the cell at node 2 sees 0.895 V. Check row 1: $-10 \cdot 0.025 + 20 \cdot 0.075 - 10 \cdot 0.105 = 0.2$. Node 0 has no load, and indeed $x_0 = (10 \cdot 0.075 + 20 \cdot 0) / 30 = 0.025$, the weighted mean of its neighbor and the supply.

A second check shows why the worst drop is at a load. On a $5 \times 5$ mesh of 10 S wires with pads of 50 S at the four corners and loads at the center and two other nodes, the worst drop of 8.25 mV is at the center load. The [multigrid-like method](/multigrid-power-grid-analysis/) page works through this mesh.

## Known algorithms

- **Direct sparse solvers.** A [Cholesky decomposition](/cholesky-decomposition/) of $G$ with a fill-reducing order such as [nested dissection](/nested-dissection/). Exact up to rounding, and the factor is reused for every time step of a transient run with a fixed step. Memory limits it on the largest grids.
- **Iterative solvers.** The [conjugate gradient method](/conjugate-gradient-method/) with a [preconditioner](/preconditioning/), such as incomplete Cholesky or a multigrid cycle. Exact in the limit, with a stopping tolerance.
- **[Multigrid-like analysis](/multigrid-power-grid-analysis/)** (Kozhaya, Nassif and Najm, 2002). One coarse solve with interpolation, no smoothing. Approximate, with the best error in the energy norm over its coarse space.
- **[Random walks](/random-walk-power-grid-analysis/)** (Qian, Nassif and Sapatnekar, 2003). The drop at one node as the mean reward of walks. Unbiased, with a random error.
- **[Algebraic multigrid](/algebraic-multigrid/).** Coarse grids chosen from the matrix, for irregular grids.
- **[Vectorless verification](/vectorless-power-grid-verification/)** (Kouroussis and Najm, 2003). The worst drop over a set of currents, by one linear program per node.
- **Transient analysis.** The [backward Euler method](/backward-euler-method/) or the [trapezoidal rule](/trapezoidal-rule/), with each capacitor replaced by its [companion model](/companion-model/), turns each time step into a DC problem with the matrix $G + C/h$, which has the same structure. See [transient circuit analysis](/transient-circuit-analysis/).

## Bounds

**Theorem.** If every connected part of the grid has a pad, then $G$ is a symmetric, positive definite, nonsingular M-matrix, so for every $i$ the drop $x$ exists and is unique. If $i \ge 0$, then $x \ge 0$.

*Proof.* $G$ is symmetric because $g_{jk} = g_{kj}$, and its entries off the diagonal are $-g_{jk} \le 0$. For any vector $z$,

$$ z^T G z = \sum_{\{j, k\} \text{ wires}} g_{jk} (z_j - z_k)^2 + \sum_k g^{\mathrm{pad}}_k z_k^2 \ \ge 0 . $$

If $z^T G z = 0$, then $z$ is constant on each connected part, and $z_k = 0$ at a pad node of that part, so $z = 0$. So $G$ is positive definite, hence nonsingular, and $x = G^{-1} i$ is the unique drop.

For the inverse, let $G z = f$ with $f \ge 0$, and suppose that the least entry $z_m$ is negative. Row $m$ gives $D_m z_m = f_m + \sum_j g_{mj} z_j \ge \sum_j g_{mj} z_j \ge (D_m - g^{\mathrm{pad}}_m) z_m$, since $z_j \ge z_m$. So $g^{\mathrm{pad}}_m z_m \ge 0$, which forces $g^{\mathrm{pad}}_m = 0$, and then all the inequalities are equalities, so $z_j = z_m$ for every neighbor $j$. Repeating this along a path to a pad node of the same part reaches a pad node with the value $z_m < 0$, where $g^{\mathrm{pad}} > 0$ gives a contradiction. So $z \ge 0$. With $f = e_j$ this shows that column $j$ of $G^{-1}$ is nonnegative, so $G^{-1} \ge 0$, and $G$ is an M-matrix. Then $i \ge 0$ gives $x = G^{-1} i \ge 0$. $\square$

The same argument gives a **discrete maximum principle**: at a node with no load, $x_m$ is at most the largest drop among its neighbors, so the largest drop of the grid is at a node with a load. And more load never lowers any drop, since $G^{-1} \ge 0$.

- **Polynomial.** Gaussian elimination solves the DC problem in $O(N^3)$ time. For a planar mesh, nested dissection gives $O(N^{3/2})$ time and $O(N \log N)$ fill. $G$ is symmetric and diagonally dominant, so the nearly linear time solvers for such systems (Spielman and Teng, 2004) apply in theory.
- **Transient.** Each time step of backward Euler with step $h$ solves $(G + C/h) x = i + (C/h) x_{\text{old}}$, again a symmetric M-matrix when $C$ is diagonal with nonnegative entries.
- **What is measured.** How fast each solver is on real grids is measured, for example on the IBM power grid benchmarks (Nassif, 2008), which have up to a few million nodes.

## Reductions

- **Same as symmetric diagonally dominant M-matrix systems.** Any symmetric matrix with entries $\le 0$ off the diagonal and row sums $\ge 0$ is the $G$ of a grid: put a wire of conductance $-A_{jk}$ for each nonzero $A_{jk}$, and a pad of conductance equal to the row sum. So power grid analysis is exactly the problem of solving such systems.
- **[Electrical flow](/electrical-flow/).** The wire currents of the solution are the flow that carries the loads from the supply with the least energy $\sum g_{jk}^{-1} I_{jk}^2$, by Thomson's principle.
- **Random walks.** By the discrete harmonic property, $x_k$ is the expected reward of a random walk that moves along wires with probabilities $g_{mj} / D_m$, as on the [random walk](/random-walk-power-grid-analysis/) page, and $G^{-1}$ counts its expected visits.
- **Worst case to linear programming.** With bounds on the currents instead of fixed values, the worst drop at a node is a [linear program](/linear-programming-problem/), since $x_k$ is linear in $i$ with nonnegative coefficients.

## Applications

- **Sign-off.** Every chip is checked for its worst static and dynamic drop and for the current densities of its grid before tape-out, and the drop at each cell feeds back into the delay of the cell in [static timing analysis](/static-timing-analysis/).
- **Grid design.** Wire widths, the number of straps and the pad positions are chosen in a loop that runs the analysis many times.
- **Decoupling capacitance.** Dynamic analysis tells where to place [decoupling capacitors](/decoupling-capacitance-allocation/).
- **Power gating.** The resistance of the sleep transistors adds to the grid, and the drop across them must stay small, as on the [power gating](/power-gating/) page.

## References
