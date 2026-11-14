---
tag: 01NV03
kind: algorithm
slug: quadratic-placement
name: Quadratic placement
aliases:
- quadratic wirelength minimization
area: eda/partitioning-floorplanning-and-placement
level: core
summary: Minimizes the sum of squared two-pin wire lengths, a convex quadratic solved by sparse linear systems, which clusters cells near the centre.
solves: [placement-problem]
model: real-ram
complexity:
  vars: {n: the number of movable cells, P: the number of pins, E: "the number of two-pin edges of the net model, at most the sum of p(p - 1)/2 over the nets", k: the number of conjugate gradient steps}
  time: {worst: "O(P + E + n (n + E))", average: "O(P + E + k (n + E))", best: "O(P + E + n + E)"}
  space: {extra: "O(n + E)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1970
  people: [Kenneth M. Hall, Jürgen M. Kleinhans, Georg Sigl, Frank M. Johannes, Kurt J. Antreich]
  note: Hall placed the vertices of a graph by minimizing a weighted sum of squared distances in 1970; GORDIAN (1991) made the version with fixed pads and sparse linear solves the core of a cell placer.
prereqs: [placement-problem, clique-net-model, laplacian-matrix, conjugate-gradient-method]
see_also: [force-directed-placement, simpl-placement, analytical-placement, min-cut-placement, half-perimeter-wirelength, tutte-embedding, sparse-linear-systems, positive-definite-matrix]
sources:
  - paper: doi:10.1287/mnsc.17.3.219
    title: Kenneth M. Hall, An r-dimensional quadratic placement algorithm, Management Science 17(3), 219 to 229, 1970
    locator: the sum of squared distances weighted by connections, and its minimum under a normalization by eigenvectors of the Laplacian (no fixed points)
  - paper: "Jürgen M. Kleinhans, Georg Sigl, Frank M. Johannes and Kurt J. Antreich, GORDIAN: VLSI placement by quadratic programming and slicing optimization, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 10(3), 356 to 365, 1991"
    locator: the global optimization by quadratic programs with unique minima, alternated with partitioning steps that add center of gravity constraints
  - paper: doi:10.6028/jres.049.044
    title: Magnus R. Hestenes and Eduard Stiefel, Methods of conjugate gradients for solving linear systems, Journal of Research of the National Bureau of Standards 49(6), 409 to 436, 1952
    locator: the method, and its exact termination in at most n steps for a positive definite system of order n
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (quadratic placement, the clique and star net models and the linear system; general locator)
  - paper: doi:10.1109/TCAD.2011.2170567
    title: Myung-Chul Kim, Dong-Jin Lee and Igor L. Markov, SimPL, an effective placement algorithm, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 31(1), 50 to 60, 2012
    locator: the quadratic lower-bound placement and its use inside a modern placer
---

Quadratic placement gives each movable cell of a netlist a point in the plane by minimizing the sum of the squared lengths of two-pin wires, with the pads fixed. It belongs to chip design (EDA): it is the global placement step of many standard cell placers. The nets are first turned into two-pin edges by the [clique net model](/clique-net-model/). The objective is a convex quadratic in the cell coordinates, so its minimum is the solution of one sparse linear system per coordinate, whose matrix is a [Laplacian](/laplacian-matrix/) plus a diagonal; the [conjugate gradient method](/conjugate-gradient-method/) solves it. The minimum is exact for the quadratic objective, but that objective is only a model of [HPWL](/half-perimeter-wirelength/), and the minimum ignores overlap: the cells crowd together inside the convex hull of the pads. So quadratic placement is a heuristic for the [placement problem](/placement-problem/), and real placers add spreading.

## In plain words

Tie each wire as a rubber band between its two ends, and nail the pads to the board. Let the parts go: they slide until the pull of the bands is balanced. That balance is the placement. Each part ends at the weighted middle of the parts it is tied to.

The bands pull hard on long wires, so the result has no very long wire. But nothing pushes the parts apart. They bunch up in the middle, often on top of each other, and a later step must spread them out.

## The problem

The input is a netlist with $n$ movable cells $0, \ldots, n - 1$ and fixed pads at positions $(x_q, y_q)$, nets $e$ of $p_e$ pins with weights $w_e > 0$, and every pin at the center of its cell or pad (no pin offsets). The clique model gives each pair of pins of net $e$ the weight $w_e / (p_e - 1)$. Summing over the nets gives a weight $w_{ij}$ for each pair. The output is real positions $(x_i, y_i)$ that minimize

$$ \Phi(x, y) = \sum_{\{i, j\}} w_{ij} \left( (x_i - x_j)^2 + (y_i - y_j)^2 \right), $$

the sum over all pairs with a cell or a pad on each end. The output is not a legal placement; it may have overlap.

The objective is the sum of a part in $x$ and a part in $y$, so the two coordinates are solved apart. For the $x$ part, let $A$ be the $n \times n$ matrix with

$$ A_{ii} = \sum_{j} w_{ij}, \qquad A_{ij} = -w_{ij} \;\; (i \ne j \text{ both cells}), \qquad b_i = \sum_{q \text{ pad}} w_{iq} x_q, $$

where the first sum runs over cells and pads. Then $\Phi_x(x) = x^{\mathsf T} A x - 2 b^{\mathsf T} x + c$ for a constant $c$, and $A$ is the Laplacian of the cell to cell edges plus the diagonal of the cell to pad weights.

## The algorithm

```pseudo id=main
QUADRATIC-PLACE(n, nets, w, pads)
L1  for each net e with p ≥ 2 pins: add w_e / (p − 1) to w_ij for each pair {i, j} of its pins
L2  build A and b_x, b_y from the weights w_ij as above
L3  if some connected group of cells has no edge to a pad then stop: A is singular
L4  for each coordinate c ∈ {x, y}
L5      z ← 0; r ← b_c; d ← r
L6      while |r|^2 > tol^2 |b_c|^2
L7          α ← |r|^2 / (dᵀ A d)
L8          z ← z + α d; r_new ← r − α A d
L9          β ← |r_new|^2 / |r|^2; d ← r_new + β d; r ← r_new
L10     c_i ← z_i for each cell i
L11 return the positions (x_i, y_i)
```

Lines L1 and L2 build the system; an edge between two pads is a constant and is left out. Line L3 checks the condition of the Theorem below: without it the cells of a free group can slide together to any place, and the minimum is not unique. Lines L5 to L9 are the [conjugate gradient method](/conjugate-gradient-method/) from $z = 0$, with residual $r = b - A z$ and search direction $d$. With exact rational arithmetic and $tol = 0$, the loop stops with $r = 0$ after at most $n$ steps. With floating point it stops when the residual is small relative to $b$.

## Example

Four cells $a, b, c, d$ and two pads, $P$ at $(0, 0)$ and $Q$ at $(6, 3)$. The nets, all of weight 1, are

$$ \{P, a\}, \; \{a, b\}, \; \{a, c\}, \; \{b, c, d\}, \; \{d, Q\}. $$

The 3-pin net gives the pairs $bc$, $bd$ and $cd$ the weight $\frac12$ each; every other pair has weight 1. With the cells in the order $a, b, c, d$,

$$ A = \begin{pmatrix} 3 & -1 & -1 & 0 \\ -1 & 2 & -\frac12 & -\frac12 \\ -1 & -\frac12 & 2 & -\frac12 \\ 0 & -\frac12 & -\frac12 & 2 \end{pmatrix}, \qquad b_x = (0, 0, 0, 6), \qquad b_y = (0, 0, 0, 3). $$

Exact conjugate gradients on $A x = b_x$, from the implementation with Fractions:

| step | $\lvert r \rvert^2$ after the step | $x$ after the step |
| --- | --- | --- |
| 0 | 36 | $(0, 0, 0, 0)$ |
| 1 | $\frac92$ | $(0, 0, 0, 3)$ |
| 2 | $\frac{144}{25}$ | $(\frac{6}{5}, \frac{12}{5}, \frac{12}{5}, \frac{21}{5})$ |
| 3 | 0 | $(\frac{12}{7}, \frac{18}{7}, \frac{18}{7}, \frac{30}{7})$ |

The residual norm goes up in step 2: conjugate gradients make the error small in the norm of $A$, not the residual. The method stops after 3 steps, not 4, because $b$ and $c$ play the same role, so $A$ has only 3 different eigenvalues on the space that $b_x$ spans. The $y$ system has $b_y = b_x / 2$, so $y = x / 2$. The result is

$$ a = (\tfrac{12}{7}, \tfrac{6}{7}), \quad b = c = (\tfrac{18}{7}, \tfrac{9}{7}), \quad d = (\tfrac{30}{7}, \tfrac{15}{7}). $$

Each cell is at the weighted mean of its neighbors: for $a$, $(0 + \frac{18}{7} + \frac{18}{7}) / 3 = \frac{12}{7}$. The cells $b$ and $c$ lie on the same point, which is the overlap that a later step must remove. All four cells lie on the segment from $P$ to $Q$. The objective is $\Phi = \frac{90}{7}$, and the HPWL of the result is $\frac{72}{7}$.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **The system.** $\Phi_x(x) = x^{\mathsf T} A x - 2 b^{\mathsf T} x + c$, so the gradient is $2 (A x - b)$.
- **Uniqueness.** $x^{\mathsf T} A x = \sum w_{ij} (x_i - x_j)^2 + \sum w_{iq} x_i^2$ over the cell to cell and the cell to pad edges. If every connected group of cells has an edge to a pad, this is zero only for $x = 0$, so $A$ is [positive definite](/positive-definite-matrix/) and $\Phi$ has exactly one minimum, the solution of $A x = b$. If some group has no edge to a pad, $A$ is singular and line L3 stops.
- **Termination.** For a positive definite $A$, exact conjugate gradients reach $r = 0$ in at most $n$ steps (Hestenes and Stiefel 1952).
- **Weighted means and the hull.** At the minimum each cell is at the weighted mean of its neighbors, and every cell lies in the convex hull of the pads that its group reaches. So the result puts all cells in the hull of the pads, and with few pads, many cells meet in a small area.

## Complexity

- **Building.** Line L1 makes $p_e (p_e - 1) / 2$ pairs for a net of $p_e$ pins, so it costs $O(P + E)$. The star model replaces each net by $p_e$ edges to a new free node, so $E = O(P)$, at the price of one more variable per net.
- **One step.** A product $A d$ costs $O(n + E)$, and the other lines of a step cost $O(n)$.
- **Steps.** In exact arithmetic at most $n$ steps, which gives $O(n (n + E))$. In floating point the number of steps $k$ to reduce the error in the $A$ norm by a factor $\varepsilon$ is $O(\sqrt{\kappa} \log(1/\varepsilon))$ for the [condition number](/condition-number/) $\kappa$ of $A$. With [preconditioning](/preconditioning/) placers need far fewer than $n$ steps; this is measured, not proved.
- **Space.** The sparse rows of $A$ and the vectors: $O(n + E)$.
- **The implementation** uses exact Fractions by default. The bit size of the fractions can grow, so the real RAM count above is a count of arithmetic operations, not of bit operations.

## Properties

**What is proved.** For a netlist in which every group of cells reaches a pad, the quadratic objective has one minimum, the linear system finds it, and the cells lie in the convex hull of the pads. With the clique weight $1/(p - 1)$ a net of 2 pins counts as one squared length. No bound relates the HPWL of the quadratic minimum to the least HPWL, and the minimum is not legal.

**What is measured.** Quadratic placement with spreading (GORDIAN, FastPlace, Kraftwerk2, SimPL) was compared with other placers on the ISPD 2005 and 2006 placement contest benchmarks; see those papers for the numbers. The quadratic step alone gives a strongly overlapped placement, and published placers do not report it alone.

- **Convexity.** The objective is convex, so the result does not depend on a start point or on the order of cells. Min-cut and annealing placers do not have this property.
- **Squares favor short wires.** A wire of length 4 costs 16, four wires of length 1 cost 4. So the quadratic objective spreads the length over many wires, and it is not the same as HPWL even for 2-pin nets.
- **The two coordinates are independent.** The $x$ and $y$ systems have the same matrix $A$, and only $b$ differs.

## Variants and improvements

- **Star model.** Replace a net of $p$ pins by a star with a free center node. With the center weight $p \, w$ the star has the same quadratic minimum as the clique of weight $w$ (see the [clique net model](/clique-net-model/)), with $p$ edges instead of $p (p - 1) / 2$.
- **Bound to bound net model.** Kraftwerk2 (Spindler, Schlichtmann and Johannes, 2008) joins the two extreme pins of a net of $p$ pins to each other and joins every inner pin to both of them, each edge with the weight $\frac{2}{(p - 1) |x_i - x_j|}$ at the current distance. Each inner pin then adds $\frac{2}{p - 1}$ times the span of the net, and so does the edge between the extremes, so at the current placement the quadratic cost of the net in $x$ equals twice its span in $x$. The weights change, so the system is solved again and again.
- **Linearization.** Divide each weight by the current length $|x_i - x_j|$ so that the squared cost behaves like a linear one near the current placement.
- **Spreading by partitioning.** GORDIAN splits the region and the cells and adds a linear constraint that keeps the center of gravity of each part at the center of its region.
- **Spreading by forces or anchors.** [Force-directed placement](/force-directed-placement/) in the Kraftwerk form adds constant spreading forces to $b$; [SimPL](/simpl-placement/) and FastPlace add pseudo nets from each cell to a spread position. Both keep the problem a positive definite system.
- **Eigenvector placement.** With no pads, Hall minimized $\Phi$ under the condition $\sum x_i^2 = 1$; the minimum is an eigenvector of the Laplacian, the same idea as [spectral partitioning](/spectral-partitioning/).

## When to use it

Use quadratic placement as the first step of global placement when the netlist is large and you need a good relative order of the cells fast. It is convex and solved by a sparse linear solve, so it scales to millions of cells and is stable under small changes of the netlist. It needs fixed pads or anchors, it does not model HPWL exactly, and it needs a spreading method. For the final wirelength, the nonlinear models of [analytical placement](/analytical-placement/), such as the [log-sum-exp wirelength](/log-sum-exp-wirelength/), are closer to HPWL. [Min-cut placement](/min-cut-placement/) is legal by construction but has no global view.

## Pitfalls

- **No pads.** A group of cells without a path to a pad makes $A$ singular, and conjugate gradients fail or drift. Check the condition, as line L3 does, or add a weak anchor to each free group.
- **Wrong clique weight.** With weight 1 per pair, a large net pulls with $p (p - 1) / 2$ pairs and dominates the system. Use $w_e / (p - 1)$ or $2 w_e / p$, and say which one.
- **Clique edges of large nets.** A net with 1000 pins has about 500000 pairs. Use the star or the bound to bound model for large nets.
- **Reading the result as a placement.** The minimum overlaps heavily. Its HPWL is not the HPWL of any legal placement, and must not be reported as one.
- **Floating point stop test.** A test on the residual alone can stop too early on a badly conditioned system. Precondition, and check the result on a few cells.

## Implementations

## History

Hall (1970) placed the vertices of a weighted graph in $r$ dimensions by minimizing the weighted sum of squared distances under a normalization, and solved it with eigenvectors of the Laplacian. Tutte (1963) had used the same balance of springs with a fixed outer face to draw planar graphs (see the [Tutte embedding](/tutte-embedding/)). In chip placement, the system with fixed pads became the global step of placers in the late 1980s. GORDIAN (Kleinhans, Sigl and Johannes, ICCAD 1988; journal version with Antreich, 1991) alternated quadratic solves with partitioning. Later quadratic placers include Kraftwerk (Eisenmann and Johannes, 1998), FastPlace (Viswanathan and Chu, 2004) and SimPL (Kim, Lee and Markov, 2010 and 2012).

## References
