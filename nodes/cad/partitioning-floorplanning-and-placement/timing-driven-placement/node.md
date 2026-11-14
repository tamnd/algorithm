---
tag: T0K6FT
kind: problem
slug: timing-driven-placement
name: Timing-driven placement
aliases:
- net weighting placement
area: cad/partitioning-floorplanning-and-placement
level: advanced
summary: Place cells to meet timing as well as wire length, usually by raising the weights of nets on critical paths or by path constraints.
prereqs: [placement-problem, static-timing-analysis, arrival-and-required-time]
see_also: [timing-graph, elmore-delay, setup-and-hold-constraints, analytical-placement, quadratic-placement, linear-programming-problem, lagrangian-relaxation, bandwidth-reduction]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 8, Timing Closure (timing-driven placement, net weights and net constraints; general locator)
  - paper: "Alfred E. Dunlop, Vishwani D. Agrawal, David N. Deutsch, M. F. Jukl, P. Kozak and M. Wiesel, Chip layout optimization using critical path weighting, Proceedings of the 21st Design Automation Conference (DAC), 133 to 136, 1984"
    locator: weights on the nets of critical paths in a placer that minimizes weighted wire length
  - paper: "Ren-Song Tsay and Jürgen Koehl, An analytic net weighting approach for performance optimization in circuit placement, Proceedings of the 28th Design Automation Conference (DAC), 620 to 625, 1991"
    locator: net weights derived from the sensitivity of the path delays to the net lengths, in an analytical placer
  - paper: doi:10.1145/74382.74444
    title: Michael A. B. Jackson and Ernest S. Kuh, Performance-driven placement of cell based IC's, Proceedings of the 26th Design Automation Conference (DAC), 370 to 375, 1989
    locator: the placement with timing constraints on paths written as a linear program
  - paper: doi:10.1007/BF02280884
    title: Christos H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16(3), 263 to 270, 1976
    locator: the NP-completeness of bandwidth, which gives the hardness of net length bounds on this page
---

Timing-driven placement is the [placement problem](/placement-problem/) with timing in the objective or in the constraints. The cells of a netlist must get legal positions, as in ordinary placement, but the delay of every path from a register or an input to a register or an output must also meet its required time. The delay of a wire grows with its length, so the placement decides a large part of the delay. The usual formulation keeps the weighted wirelength as the objective and asks that the worst slack of [static timing analysis](/static-timing-analysis/) be at least 0, or puts the slack into the objective. The problem contains ordinary placement, so it is [NP-hard](/np-hard/); even deciding whether a placement meets bounds on the net lengths is NP-complete. This page states the problem; the methods are named under Known algorithms.

## In plain words

A signal must travel from one storage element to the next in one clock tick. On its way it passes through gates and along wires, and long wires make it slow. A placer that only makes the total wire short may leave a few signals on long wires, and then the chip cannot run at the planned speed.

Timing-driven placement asks the placer to keep the wires short in total, and also to keep the wires on the slow routes short enough that every signal arrives in time. The two goals can disagree: the place that is best for the total is not always fast enough for the slow route.

## Definition

**Input.**

- A netlist $H = (C \cup Q, N)$ with $n$ cells, $m$ nets, net weights $w_e \ge 0$, rows $y_1, \ldots, y_K$ with sites of width $s$, and fixed pads, as in the [placement problem](/placement-problem/).
- A [timing graph](/timing-graph/) $G$ on the pins: an edge for each arc through a cell, with a delay $d_{\mathrm{cell}}$, and an edge from the driver of each net to each of its sinks, with a delay that is a function of the placement.
- A wire delay model, which maps a placement to the delay of each net arc: for example a linear model $d = \alpha \cdot \mathrm{HPWL}(e)$, the length from the driver to the sink, or the [Elmore delay](/elmore-delay/) of an estimated tree.
- Arrival times at the timing start points and required times at the end points, from the clock period and the [setup constraints](/setup-and-hold-constraints/).

**Output.** A legal placement: every cell on a site of a row, inside the region, with no overlap.

**Timing.** For a placement, [arrival and required times](/arrival-and-required-time/) are propagated through $G$. The slack of a pin is its required time minus its arrival time, and the worst negative slack is $\mathrm{WNS} = \min(0, \min_v \mathrm{slack}(v))$. The total negative slack $\mathrm{TNS}$ is the sum of the negative slacks of the end points.

**Objective.** The common forms are:

- **Constrained.** Minimize $\mathrm{WL} = \sum_e w_e \mathrm{HPWL}(e)$ subject to $\mathrm{slack}(v) \ge 0$ at every end point $v$.
- **Max slack.** Maximize the worst slack, or minimize the clock period, with the wirelength as a second goal.
- **Weighted sum.** Minimize $\mathrm{WL} - \lambda \, \mathrm{WNS}$ or $\mathrm{WL} - \lambda \, \mathrm{TNS}$ for a given $\lambda > 0$.

A page or tool must say which form and which delay model it uses, because the best placement differs between them.

## Variants

- **Net-based constraints.** Give each net a length bound $L_e$, so that the delay of each path is met when every net meets its bound. Then the constraint is $\mathrm{HPWL}(e) \le L_e$ for each net, and no timing analysis is needed during placement. The split of the slack of a path into bounds on its nets is called net budgeting.
- **Path-based constraints.** Keep the path delays as constraints in the formulation, through variables for the arrival times at the pins. This is exact for the delay model but has many more constraints.
- **Global or detailed.** The constraints can act during global placement, during [legalization](/placement-legalization/) as a bound on the movement of critical cells, or during [detailed placement](/detailed-placement/) as a slack term in the cost of each move.
- **With other changes.** Placement is often done together with [gate sizing](/gate-sizing/), [buffer insertion](/van-ginneken-buffer-insertion/) and the choice of cell drive strengths, which change the delays for the same placement.
- **Hold and clock.** Most formulations use only the setup checks; hold violations are fixed later by added delay. With a clock tree, the clock arrival times also depend on the placement of the registers.

## Examples

**Weights overshoot under HPWL.** All pins lie on one horizontal line, so the HPWL of a net is the spread of its $x$ coordinates. Pad $P$ is at $x = 0$, pads $Q_1$ and $Q_2$ at $x = 10$, and one movable cell $c$, a point, is at $x_c$. The nets are $\{P, c\}$, $\{c, Q_1\}$ and $\{c, Q_2\}$, each of weight 1. The net $\{P, c\}$ is on a critical path, and with a linear delay model the path meets its required time if and only if $\mathrm{HPWL}(\{P, c\}) = x_c \le 4$, for $0 \le x_c \le 10$.

| formulation | best $x_c$ | $\mathrm{WL}$ | slack $4 - x_c$ |
| --- | --- | --- | --- |
| wirelength only | 10 | 10 | $-6$ |
| constraint $x_c \le 4$ | 4 | 16 | 0 |
| weight $w < 2$ on $\{P, c\}$ | 10 | 10 | $-6$ |
| weight $w > 2$ on $\{P, c\}$ | 0 | 20 | 4 |

On $0 \le x_c \le 10$ the weighted wirelength is $w x_c + 2 (10 - x_c)$, a linear function of $x_c$, so its minimum is at an end of the interval for every $w \ne 2$. No net weight gives the constrained optimum $x_c = 4$: a small weight leaves the path late, and a large one meets the timing with 4 units of wirelength more than needed. A constraint, or a smooth delay term, finds the trade-off that a weight on a linear objective cannot.

**Bounds that cannot all hold.** One row of 4 unit sites and 4 unit cells, with a 2-pin net between every pair of cells, each with the length bound $L_e = 2$ (distances between cell centers). Some two cells sit on sites 0 and 3, at distance 3, so no legal placement meets all six bounds. With $L_e = 3$ every placement meets them.

## Known algorithms

- **Net weighting.** Raise the weights $w_e$ of the nets on paths with small slack, run a wirelength placer, run timing analysis, and repeat. Dunlop et al. (1984) weighted the nets of critical paths. Tsay and Koehl (1991) derived the weights from the sensitivity of the delay to the length of each net in an analytical placer.
- **Net budgeting.** Turn the slack of the paths into length bounds $L_e$ on the nets, by a zero-slack distribution of the slack along each path, and place with these bounds as constraints or as penalties.
- **Path-based linear programs.** Jackson and Kuh (1989) wrote the placement with a linear delay model as a [linear program](/linear-programming-problem/) in the cell coordinates, the bounding box of each net and the arrival times, with the path constraints as linear inequalities.
- **[Lagrangian relaxation](/lagrangian-relaxation/).** Move the timing constraints into the objective with multipliers. The multipliers act as net weights that are updated from the slacks, which gives a basis for net weighting.
- **Timing terms in analytical placers.** [Analytical placers](/analytical-placement/) add a smooth function of the slack, or of the delay of the critical nets, to their wirelength and density terms.

All of these are measured on industrial designs and benchmark suites by WNS, TNS and wirelength. None of the iterative weighting schemes has a proof that it converges to a placement that meets timing.

## Bounds

- **NP-hard.** With no timing constraints the problem is the [placement problem](/placement-problem/), which is NP-hard for unit cells, 2-pin nets and one row.
- **Strongly NP-complete feasibility of net bounds.** Deciding whether a legal placement meets the bounds $\mathrm{HPWL}(e) \le L$ on all nets is NP-complete, by the bandwidth reduction below; the numbers in that instance are at most $n$.
- **Fixed order is polynomial.** With a linear delay model and the relative order of the cells fixed in each coordinate, the constrained problem without overlap is a linear program: the bounding box of each net and the arrival times are linear variables, and every constraint is linear. So it is solved in polynomial time.
- **One timing analysis.** For a given placement, static timing analysis on $G$ costs $O(|V(G)| + |E(G)|)$ time, so checking a placement is easy.

## Reductions

- **From bandwidth.** Given a graph $G$ on $n$ vertices and an integer $B$, make one row of $n$ unit sites, a unit cell per vertex, a 2-pin net per edge, and the bound $L_e = B$ on every net. With pins at the cell centers, a legal placement is a bijection $\pi$ from the vertices to $\{0, \ldots, n - 1\}$ and $\mathrm{HPWL}(\{u, v\}) = |\pi(u) - \pi(v)|$. So a placement meets all bounds if and only if $G$ has [bandwidth](/bandwidth-reduction/) at most $B$, which is NP-complete (Papadimitriou 1976).
- **From placement.** Set every required time to $+\infty$: all slacks are infinite, and the constrained form is plain placement.
- **To linear programming.** For a fixed order of the cells and a linear delay model, the problem is a [linear program](/linear-programming-problem/), as above.

## Applications

- **Closing timing in physical design.** Every flow for a high-speed chip uses a timing-driven placer, so that later steps such as gate sizing and buffering have less to fix.
- **Incremental timing fixes.** After timing analysis of a routed design, a few critical cells are moved by a detailed placer with a slack term.
- **Trade-off studies.** The weighted form, with several values of $\lambda$, shows how much wirelength each unit of slack costs.

## References
