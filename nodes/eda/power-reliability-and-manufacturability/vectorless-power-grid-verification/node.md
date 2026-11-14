---
tag: H1QXN8
kind: algorithm
slug: vectorless-power-grid-verification
name: Vectorless power grid verification
aliases:
- current-constraint power grid verification
- Kouroussis-Najm verification
area: eda/power-reliability-and-manufacturability
level: research
summary: Kouroussis and Najm's worst-case IR drop check that bounds block currents by constraints and solves one linear program per node, with no simulation vectors.
solves: [power-grid-analysis]
model: word-ram
complexity:
  vars: {K: the number of nodes checked, S: the number of current sources, F: the time to factor the conductance matrix once, Z: the number of nonzeros of the factor, L: the time of one linear program with S variables and the given constraints}
  time: {worst: "O(F + K (Z + L))"}
  space: {extra: "O(Z + S^2)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 2003
  people: [Dionysios Kouroussis, Farid N. Najm]
  note: Kouroussis and Najm gave the method at DAC 2003. They replaced the simulation of chosen load patterns by bounds on the block currents and found the worst drop at each node by linear programming.
prereqs: [power-grid-analysis, linear-programming-problem]
see_also: [simplex-method, fractional-knapsack, lp-duality, interior-point-method, cholesky-decomposition, multigrid-power-grid-analysis, random-walk-power-grid-analysis, monte-carlo-power-estimation]
sources:
  - paper: doi:10.1145/775832.775861
    title: Dionysios Kouroussis and Farid N. Najm, A static pattern-independent technique for power grid voltage integrity verification, Proceedings of the 40th Design Automation Conference, 99 to 104, 2003
    locator: the current constraints (local bounds per source and global bounds on groups), the worst drop at a node as a linear program, the DC and the transient form
---

Vectorless power grid verification checks that the voltage drop at every node of an on-chip power grid stays below a limit for every pattern of load currents that the design may draw, not only for the patterns that someone simulated. The currents are not known. What is known are bounds: each current source lies between 0 and a peak value, and groups of sources, such as the blocks that share a clock or a power budget, have a bound on their total. Since the drop $x = G^{-1} i$ is linear in the currents, the worst drop at node $k$ over all currents that meet the bounds is a [linear program](/linear-programming-problem/) in the currents. Kouroussis and Najm (2003) solved one such program per node. The answer is the exact worst case under the bounds, so it is safe when the bounds are right. When the only group bound is one bound on the total current, a greedy rule solves the program exactly, as a [fractional knapsack](/fractional-knapsack/).

## In plain words

Early in a design you do not know which blocks of the chip will be busy at the same time. You only know limits: this block never draws more than 0.4 A, and the chip as a whole never draws more than 0.5 A.

You want to know the worst voltage drop at each point of the power grid under any mix of currents that keeps to these limits. Each current adds a fixed share to the drop at a point, so the worst mix puts as much current as allowed into the blocks with the largest share. Finding that mix for each point is a linear program, and with one total limit it is just "fill the biggest shares first".

## The problem

The grid is in drop form, as on the [power grid analysis](/power-grid-analysis/) page: $G x = i$, where $G$ is a symmetric M-matrix and $x_k$ is the drop at node $k$. The loads are $S$ current sources at chosen nodes. The input is $G$, the bounds, a set of nodes to check and a limit $x_{\max}$. The bounds are

$$ 0 \le i_s \le u_s \text{ for every source } s, \qquad U i \le w, $$

where each row of $U$ has entries 0 and 1 and picks a group of sources with a bound $w_q$ on their total. The set $\mathcal{F}$ of current vectors that meet the bounds is the feasible space. The output is, for each node $k$ to check,

$$ z_k = \max_{i \in \mathcal{F}} x_k(i) = \max_{i \in \mathcal{F}} r_k^T i, \qquad r_k = (\text{row } k \text{ of } G^{-1}) \text{ on the sources}, $$

and the list of nodes with $z_k > x_{\max}$. The power grid analysis page shows that $G^{-1}$ has no negative entries, so $r_k \ge 0$: more current never lowers a drop. This page treats the DC case. The bounds $u_s$ and $w_q$ come from the designers or from power estimates of the blocks, for example from [Monte Carlo power estimation](/monte-carlo-power-estimation/) or a power budget, and they are only as good as those estimates. The conductances of $G$ come from layout extraction and foundry data, as on the power grid analysis page. The method fits no parameter of its own.

## The algorithm

```pseudo id=main
VECTORLESS-VERIFY(G, sources, u, U, w, nodes, x_max)
L1  for each node k in nodes do
L2      r ← the solution of G r = e_k, kept at the sources      ▷ row k of G⁻¹, since G is symmetric
L3      z_k ← max rᵀ i subject to 0 ≤ i ≤ u and U i ≤ w      ▷ a linear program
L4  return the nodes k with z_k > x_max, and all z_k

GREEDY-ONE-BOUND(r, u, W)                                   ▷ when U i ≤ w is the one bound Σ i_s ≤ W
L5  sort the sources by r_s, largest first
L6  rest ← W
L7  for each source s in this order do i_s ← min(u_s, rest); rest ← rest − i_s
L8  return rᵀ i
```

Line L2 uses one factorization of $G$, for example a sparse [Cholesky decomposition](/cholesky-decomposition/), and two triangular solves per node. Line L3 can use the [simplex method](/simplex-method/) or an [interior point method](/interior-point-method/). The code of this page uses a dense simplex in exact fractions with Bland's rule, which suits small tests.

## Example

Take a chain of 4 nodes, $0 - 1 - 2 - 3$, with wires of 10 S and pads of 20 S at nodes 0 and 3. Current sources sit at nodes 1 and 2, each with $u_s = 0.4$ A, and the total is at most $W = 0.5$ A. The limit is 40 mV.

Solving $G r = e_1$ gives row 1 of $G^{-1}$, $(1/32, 3/32, 9/160, 3/160)$ in ohms. At the sources it is $r = (3/32, 9/160) = (0.09375, 0.05625)$. The greedy of lines L5 to L8 fills the source at node 1 first, up to 0.4 A, and the source at node 2 with the remaining 0.1 A:

$$ z_1 = 0.4 \cdot \tfrac{3}{32} + 0.1 \cdot \tfrac{9}{160} = \tfrac{69}{1600} \approx 43.1 \text{ mV}. $$

By the symmetry of the chain, $z_2 = 69/1600$ with the worst vector $(0.1, 0.4)$, and $z_0 = z_3 = 23/1600 \approx 14.4$ mV. So nodes 1 and 2 fail the limit of 40 mV. Note that the worst vector for node 1 and the worst vector for node 2 are different. A simulation of one current pattern would find the worst case of at most one of the two nodes. Without the total bound, the worst vector is $(0.4, 0.4)$ for every node and $z_1 = 0.4 \cdot (3/32 + 9/160) = 3/50 = 60$ mV, so the global bound lowers the reported worst drop at node 1 from 60 mV to 43.1 mV.

## Correctness

The [proof file](proofs/correctness.md) proves three facts. First, $x = G^{-1} i$ is linear in $i$, so $x_k = r_k^T i$, and $z_k$ is the optimum of the linear program of line L3. The feasible space holds $i = 0$ and is bounded by $0 \le i \le u$, so the optimum exists and is attained at a vertex. Hence $z_k$ is both a bound and the least bound: every feasible current gives a drop of at most $z_k$, and some feasible current gives exactly $z_k$. Second, since $r_k \ge 0$, the worst case with local bounds only is $r_k^T u$, all sources at their peaks. Third, with one bound on the total, the program is a fractional knapsack with values $r_s$ per ampere and capacities $u_s$, and filling the largest $r_s$ first is optimal by the exchange argument.

What the method does not prove is that the real chip meets the bounds. If a block draws more than its $u_s$, or if blocks that the bounds treat as unable to peak together do so, the check is not safe. If the bounds are loose, the check is safe but pessimistic.

## Complexity

One factorization of $G$ costs $F$, and each node then needs two triangular solves, $O(Z)$ with $Z$ the nonzeros of the factor, and one linear program with $S$ variables, at cost $L$. The total is $O(F + K (Z + L))$ for $K$ nodes. With one total bound, $L$ is $O(S \log S)$ for the sort. With general bounds, interior point methods solve each program in polynomial time, and the simplex method is fast in practice but exponential in the worst case. The dense simplex of the code needs $O(S^2)$ space for the tableau. The cost of one program per node is what limits the method on large grids, and it is the target of most later work.

## Properties

- **Exact under the bounds, proved.** $z_k$ is the largest drop at $k$ over all currents that meet the bounds, and it is attained.
- **Safe, if the bounds are right.** No current pattern that meets the bounds gives a larger drop, so no pattern is missed, unlike a check by simulation of chosen patterns.
- **Monotone, proved.** Since $G^{-1} \ge 0$, raising any bound never lowers any $z_k$.
- **One program per node.** Each node has its own worst current vector, so the programs cannot be merged into one.
- **Measured cost.** The run times that Kouroussis and Najm report are measurements on their grids. This page does not repeat them.

## Variants and improvements

- **Transient constraints.** Kouroussis and Najm also treat currents that vary over time, with bounds at each time step and the grid discretized in time by the [companion model](/companion-model/). The worst drop at a node and a time is again a linear program, in the currents of all time steps.
- **Fewer programs.** Later work bounds $z_k$ cheaply for many nodes at once and solves the full program only for nodes whose bound is close to the limit. Other work uses an approximate row of $G^{-1}$ that keeps only its large entries, which makes each program smaller.
- **Duality.** By [LP duality](/lp-duality/), a feasible point of the dual program gives an upper bound on $z_k$ without solving the primal. A bound below $x_{\max}$ is already a proof that node $k$ passes.
- **Other solvers.** The [multigrid-like method](/multigrid-power-grid-analysis/) and the [random walk method](/random-walk-power-grid-analysis/) solve the grid for one known current vector. Vectorless verification asks about all vectors that meet the bounds.

## When to use it

Use it early in a design, when the floorplan and the power budgets of the blocks are known but the activity is not, and at sign-off as a check that does not depend on the choice of test patterns. It is the right tool when a missed worst case is costly. Use it with care when the bounds come from rough guesses, since a check is only as safe as its bounds.

## Pitfalls

- **Treating one worst vector as the worst for all nodes.** Each node has its own worst vector, as in the example. Running the worst vector of one node through a simulator does not check the others.
- **Missing global bounds.** With local bounds only, every source sits at its peak, which gives a safe but very pessimistic answer. The group bounds carry most of the real knowledge.
- **Wrong sign conventions.** In drop form the currents are drawn from the grid and $G^{-1} \ge 0$. With node voltages instead of drops, the program must minimize the voltage, not maximize it.
- **Rounding in large programs.** A floating point simplex can stop at a slightly infeasible point and report a drop that is too low. Check the final point against the bounds, or use the dual bound.
- **A grid part with no pad.** Then $G$ is singular, and no bound exists. Check the connectivity first.

## Implementations

## History

Before 2003, power grids were checked by simulating a few current patterns, often the peak current of every block at once, which is pessimistic, or patterns from logic simulation, which can miss the worst case. Kouroussis and Najm (2003) proposed to describe the unknown currents by constraints and to find the worst drop by linear programming, both for DC and for transient analysis. Najm and his students then worked for several years on making the per-node programs cheaper, with early bounds, sparse approximations of the inverse and better handling of the transient case.

## References
