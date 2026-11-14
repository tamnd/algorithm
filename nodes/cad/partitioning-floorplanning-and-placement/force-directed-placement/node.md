---
tag: 82M4RX
kind: algorithm
slug: force-directed-placement
name: Force-directed placement
aliases:
- Quinn-Breuer placement
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Treats nets as springs that pull connected cells together and moves each cell to the zero force position, with added forces to spread cells.
solves: [placement-problem]
model: real-ram
complexity:
  vars: {n: the number of movable cells, P: the number of pins, E: the number of springs of the clique model, R: the number of rounds, T: the number of sweeps in a round, G: the number of bins}
  time: {worst: "O(P + E + R (T (n + E) + G))", average: "O(P + E + R (T (n + E) + G))", best: "O(P + E + R (T (n + E) + G))"}
  space: {extra: "O(n + E + G)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1979
  people: [Neil R. Quinn, Melvin A. Breuer, Hans Eisenmann, Frank M. Johannes]
  note: Quinn and Breuer placed the components of printed circuit boards by the balance of spring forces in 1979; Kraftwerk (1998) added spreading forces from the cell density and made the method a global placer for standard cells.
prereqs: [placement-problem, clique-net-model, gauss-seidel-method, quadratic-placement]
see_also: [analytical-placement, electrostatics-based-placement, simpl-placement, tutte-embedding, laplacian-matrix, positive-definite-matrix, poisson-equation, placement-legalization]
sources:
  - paper: doi:10.1109/TCS.1979.1084652
    title: Neil R. Quinn and Melvin A. Breuer, A force directed component placement procedure for printed circuit boards, IEEE Transactions on Circuits and Systems CAS-26(6), 377 to 388, 1979
    locator: the spring model of the nets, the relative placement by the solution of the force equations, and the later assignment of components to slots
  - paper: "Hans Eisenmann and Frank M. Johannes, Generic global placement and floorplanning, Proceedings of the 35th Design Automation Conference (DAC), 1998"
    locator: the Kraftwerk placer, with additional forces from the cell density that are added in each step (general locator)
  - paper: "Peter Spindler, Ulf Schlichtmann and Frank M. Johannes, Kraftwerk2, a fast force-directed quadratic placement approach using an accurate net model, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 27(8), 2008"
    locator: the bound to bound net model and the move force and hold force formulation (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (force-directed placement and the zero-force target; general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on placement (force-directed placement methods)
---

Force-directed placement treats every net as a set of springs between the cells it connects, and moves each cell to the point where the pulls of its springs cancel, the zero-force position. It belongs to chip design (EDA), where it is one of the oldest global placers for the [placement problem](/placement-problem/). The springs come from the [clique net model](/clique-net-model/), and the pads are fixed. Moving one cell to its zero-force position is the exact minimum of the spring energy along that cell's coordinate, so repeated moves are the [Gauss-Seidel method](/gauss-seidel-method/) for the linear system of [quadratic placement](/quadratic-placement/), and the energy never increases. Springs alone pull all cells into a heap, so the method adds spreading forces that push cells from dense bins to sparse ones, as in Kraftwerk. The result is a global placement with less overlap, still to be legalized; it is a heuristic, not an optimum of HPWL.

## In plain words

Join every pair of parts that share a wire with a spring, and nail the pads to the board. Take one part at a time and put it where its springs pull equally in all directions. Do that again and again. The parts settle into a balance where long wires are rare.

But springs only pull, so the parts crowd together in the middle. To fix that, look at how full each patch of the board is, and give each part an extra push away from full patches toward empty ones. The pushes add up round by round until the parts are spread out enough.

## The problem

The input is a netlist with $n$ movable cells and fixed pads, nets $e$ with weights $w_e > 0$, cell widths $W_i$ and heights $H_i$, and a region $[0, X] \times [0, Y]$ cut into $G$ square bins of side $B$. A cell position is its center, and every pin is at the center of its cell or pad. The clique model gives each pair of pins of a net of $p$ pins a spring of stiffness $w_e / (p - 1)$, and $w_{ij}$ is the total stiffness between $i$ and $j$. The output is a position $(x_i, y_i)$ for each cell inside the region, with small HPWL and small density overflow. Overlap may remain.

With extra forces $(e^x_i, e^y_i)$ on the cells, the spring energy is

$$ \Phi(x, y) = \tfrac12 \sum_{\{i, j\}} w_{ij} \bigl( (x_i - x_j)^2 + (y_i - y_j)^2 \bigr) - \sum_i \bigl( e^x_i x_i + e^y_i y_i \bigr), $$

over all springs with a cell or a pad at each end. The force on cell $i$ in $x$ is $-\partial \Phi / \partial x_i = \sum_j w_{ij} (x_j - x_i) + e^x_i$. With $d_i = \sum_j w_{ij}$, it is zero at

$$ x_i = \frac{\sum_j w_{ij} x_j + e^x_i}{d_i}, $$

the zero-force position, a weighted mean of the neighbors shifted by $e^x_i / d_i$.

## The algorithm

```pseudo id=main
FORCE-DIRECTED(cells, nets, pads, R rounds, T sweeps, κ)
L1  turn the nets into springs w_ij by the clique model; d_i ← Σ_j w_ij
L2  e_i ← 0 for every cell; put the cells at a start point
L3  for round = 1 to R
L4      for sweep = 1 to T
L5          for each cell i
L6              (x_i, y_i) ← the zero-force position (Σ_j w_ij p_j + e_i) / d_i, clamped to the region
L7      D(u, v) ← the cell area in bin (u, v), divided by B²
L8      for each cell i, in bin (u, v)
L9          e_i ← e_i + κ d_i B (D(u−1, v) − D(u+1, v), D(u, v−1) − D(u, v+1)) / 2
L10 return the positions
```

Line L6 uses the newest positions of the neighbors, so a sweep is one Gauss-Seidel step. The clamp keeps the cell inside the region, between $W_i / 2$ and $X - W_i / 2$ in $x$, and likewise in $y$. Line L9 is the spreading force: a bin outside the region has density 0, and the force points from the denser neighbor bin to the sparser one. It is scaled by $d_i$, so a change of $D$ by 1 between the two neighbors moves the zero-force position by $\kappa B / 2$. The forces are added round after round, so a cell in a crowded area is pushed harder each round until the crowd thins out. Kraftwerk computes the force from a potential, by the [Poisson equation](/poisson-equation/), instead of from the neighbor bins.

## Example

Two unit cells $a$ and $b$ lie on the line $y = 1$ between the pads $P = (0, 1)$ and $Q = (6, 1)$, with the nets $\{P, a\}$, $\{a, b\}$ and $\{b, Q\}$ of weight 1, so each net is one spring of stiffness 1. Only $x$ matters, and $\Phi = \frac12 \bigl( x_a^2 + (x_b - x_a)^2 + (6 - x_b)^2 \bigr)$ with no extra force. Both cells start at $x = 3$, with $\Phi = 9$. Each move puts the cell at the mean of its two neighbors.

| move | cell | new $x$ | $x_a$ | $x_b$ | $\Phi$ | $\Phi - 6$ |
| --- | --- | --- | --- | --- | --- | --- |
| start | | | 3 | 3 | 9 | 3 |
| 1 | $a$ | $(0 + 3) / 2$ | $\frac32$ | 3 | $\frac{27}{4}$ | $\frac34$ |
| 2 | $b$ | $(\frac32 + 6) / 2$ | $\frac32$ | $\frac{15}{4}$ | $\frac{99}{16}$ | $\frac{3}{16}$ |
| 3 | $a$ | $(0 + \frac{15}{4}) / 2$ | $\frac{15}{8}$ | $\frac{15}{4}$ | $\frac{387}{64}$ | $\frac{3}{64}$ |
| 4 | $b$ | $(\frac{15}{8} + 6) / 2$ | $\frac{15}{8}$ | $\frac{63}{16}$ | $\frac{1539}{256}$ | $\frac{3}{256}$ |
| 5 | $a$ | $(0 + \frac{63}{16}) / 2$ | $\frac{63}{32}$ | $\frac{63}{16}$ | $\frac{6147}{1024}$ | $\frac{3}{1024}$ |
| 6 | $b$ | $(\frac{63}{32} + 6) / 2$ | $\frac{63}{32}$ | $\frac{255}{64}$ | $\frac{24579}{4096}$ | $\frac{3}{4096}$ |

The balance is $x_a = 2$, $x_b = 4$ with $\Phi = 6$, the solution of the linear system of quadratic placement. After the first move, each move divides $\Phi - 6$ by 4. The tests check this table with exact fractions.

Now let two cells sit on the same spot in one bin, with both neighbor bins empty. Their bin has density 2, but line L9 uses only the two neighbor bins, which are equal, so neither cell gets a spreading force. They get one only after the springs move one of them into another bin. This is a weakness of the simple force of line L9; Kraftwerk's potential, which sees the whole density, does not have it.

## Correctness

The method makes two exact claims: every move lowers $\Phi$ or keeps it, and without spreading and without the clamp the moves converge to the unique minimum of $\Phi$, which is the solution of quadratic placement. See the [proof](proofs/correctness.md). The second claim needs every cell to have a path of springs to a pad; otherwise $\Phi$ has no unique minimum, and the implementation stops with an error when a cell has no spring at all.

The spreading part has no such guarantee. Each round changes the forces $e_i$, so $\Phi$ changes between rounds; it is a different function each round. Nothing proves that the overflow falls, or that the HPWL stays near its minimum.

## Complexity

- **Springs.** Line L1 makes $E$ springs, $\sum_e p_e (p_e - 1) / 2$ in the worst case, in $O(P + E)$ time.
- **Sweeps.** Line L6 reads the springs of one cell, so a sweep costs $O(n + E)$, and a round $O(T (n + E))$.
- **Density and forces.** With no cell larger than a bin, each cell overlaps at most 4 bins, so line L7 costs $O(n + G)$ and lines L8 and L9 cost $O(n)$.

The total is $O(P + E + R (T (n + E) + G))$ time and $O(n + E + G)$ space. Large nets make $E$ large; placers use the star model or the bound to bound model for them.

## Properties

**What is proved.**

- One move puts the cell at the exact minimum of $\Phi$ along its coordinate inside the region, so $\Phi$ does not increase inside a round.
- If every cell has a path of springs to a pad, the matrix of the system is [positive definite](/positive-definite-matrix/), and without spreading and without the clamp the sweeps converge to the unique minimum of $\Phi$, the solution of quadratic placement. Each sweep is a Gauss-Seidel step, which converges for every positive definite system.
- The method stops after $R T n$ moves.

**What is measured.** The numbers below come from the implementation of this page on toy inputs, not from benchmarks. On 10 random netlists of 16 unit cells in an $8 \times 8$ region with $2 \times 2$ bins (seed 5, about 32 nets, 6 pads on the border, 40 sweeps per round), the springs alone end with a mean overflow of 1.005 bins and a mean HPWL of 87.4. After 10 rounds of spreading with $\kappa = \frac12$, the mean overflow is 0.299 and the mean HPWL 123.2. With 32 cells in the same region the overflow falls from 3.579 to 2.010 and the HPWL grows from 138.7 to 221.9. So spreading trades wirelength for density, and on dense inputs much overlap is left for the legalizer. Kraftwerk and Kraftwerk2 were measured on the ISPD placement benchmarks; see those papers for the numbers.

## Variants and improvements

- **Slot assignment.** Quinn and Breuer solved the force equations for relative positions and then assigned the components to the slots of the board. Many early placers instead moved one cell at a time to its zero-force target on a grid of slots and, if the slot was taken, swapped or moved the occupant in a chain.
- **Repulsive forces.** Some formulations add forces that push apart cells with no net between them. These make the energy nonconvex and the method slow.
- **Density forces from a potential.** Kraftwerk computes the spreading force as the gradient of a potential that solves the Poisson equation with the density as its source. This smooths the force over the whole region. The [electrostatics-based placement](/electrostatics-based-placement/) of ePlace uses the same idea with an exact solver and a different optimizer.
- **Hold and move forces.** Kraftwerk2 splits the extra force into a hold force, which keeps the cells where the last round left them, and a move force from the density. It uses the bound to bound net model, whose energy matches the HPWL at the current positions.
- **Anchors.** [SimPL](/simpl-placement/) replaces the forces by springs to anchor points from a rough legal placement. A spring to an anchor is a force that grows with the distance.

## When to use it

Use force-directed placement when you want a simple global placer that rests on linear algebra, with a clear energy and few parameters, or as the inner step of a quadratic placer. Its strength is that one round is a sparse linear system, solved fast and exactly. For large standard cell designs, nonlinear placers with a smooth wirelength and an electrostatic density, such as ePlace and RePlAce, reach smaller HPWL at a similar overflow, and they are the usual choice now.

## Pitfalls

- **A cell with no path to a pad.** Its position is not fixed by the springs, and the system is singular. Check that every connected part of the netlist has a pad.
- **Too strong spreading.** A large $\kappa$ throws cells to the border in one round and destroys the wirelength. A small one needs many rounds.
- **Forces from neighbor bins only.** A crowd inside one bin gets no force from line L9, as in the example. Smooth the density or use a potential.
- **Clique springs of large nets.** A net of $p$ pins makes $p (p - 1) / 2$ springs. Use a star or the bound to bound model.
- **Treating the energy as HPWL.** The squared spring length favors many medium wires over a few long ones, which differs from HPWL. Report HPWL after legalization.

## Implementations

## History

Quinn and Breuer published the force-directed placement of printed circuit board components in 1979: the nets became springs, the zero-force equations gave the relative positions, and a second phase assigned the components to slots. The zero-force position of a vertex is the same idea as Tutte's [spring embedding](/tutte-embedding/) of 1963, where each inner vertex is the mean of its neighbors. Eisenmann and Johannes made the method a global placer for large standard cell designs in Kraftwerk (1998), with spreading forces from the density, and Spindler, Schlichtmann and Johannes improved it in Kraftwerk2 (2008) with the bound to bound net model.

## References
