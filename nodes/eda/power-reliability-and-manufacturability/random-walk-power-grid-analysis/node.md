---
tag: 4F39NW
kind: algorithm
slug: random-walk-power-grid-analysis
name: Random walk power grid analysis
aliases:
- Qian-Nassif-Sapatnekar random walk
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Qian, Nassif and Sapatnekar's solver that estimates the drop at one node as the mean reward of random walks on the grid's conductance graph, an unbiased estimate that is fast for local queries.
solves: [power-grid-analysis]
model: word-ram
complexity:
  vars: {W: the number of walks, S: the mean number of steps of a walk, d: the largest number of wires at a node, N: the number of grid nodes, E: the number of wires}
  time: {expected: "O(N + E + W S log d)"}
  space: {extra: "O(N + E)"}
properties: {deterministic: false, exact: false, recursive: false}
history:
  year: 2003
  people: [Haifeng Qian, Sani R. Nassif, Sachin S. Sapatnekar]
  note: Qian, Nassif and Sapatnekar gave the method at DAC 2003 and in IEEE Transactions on Computer-Aided Design in 2005, using the old link between random walks and electric networks to find the voltage at a few nodes of a power grid without solving the whole grid.
prereqs: [power-grid-analysis, markov-chain]
see_also: [floating-random-walk-capacitance, monte-carlo-integration, law-of-large-numbers, central-limit-theorem, confidence-interval, multigrid-power-grid-analysis, vectorless-power-grid-verification, electrical-flow]
sources:
  - paper: doi:10.1145/775832.775860
    title: Haifeng Qian, Sani R. Nassif and Sachin S. Sapatnekar, Random walks in a supply network, Proceedings of the 40th Design Automation Conference, 93 to 98, 2003
    locator: the game in which a walker pays a cost at each node and is paid at the pads, its equality with the node voltage, and the solver for single nodes
  - paper: "Haifeng Qian, Sani R. Nassif and Sachin S. Sapatnekar, Power grid analysis using random walks, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 24(8), 1204 to 1224, August 2005"
    title: Haifeng Qian, Sani R. Nassif and Sachin S. Sapatnekar, Power grid analysis using random walks, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 24(8), 1204 to 1224, August 2005
    locator: the journal version, with DC and transient analysis, the error and the number of walks, and the measured results on industrial grids
---

Random walk power grid analysis estimates the voltage drop at one node of an on-chip power grid by the mean payoff of random walks. A walker starts at the node. At each node it collects a reward equal to the load current there divided by the total conductance at the node, and then it either moves along a wire, with probability proportional to the wire's conductance, or stops at the supply through a pad. The expected total reward of a walk is exactly the drop at the start node, so the mean over many walks is an unbiased estimate whose error shrinks as one over the square root of the number of walks. Qian, Nassif and Sapatnekar (2003, 2005) used it to answer queries about a few nodes of a grid with millions of nodes, without solving for all of them. It is the [power grid analysis](/power-grid-analysis/) form of a [Monte Carlo](/monte-carlo-integration/) method, close in spirit to the [floating random walk](/floating-random-walk-capacitance/) of capacitance extraction.

## In plain words

Picture a walker on the grid of wires. It starts at the node you care about. At each node it picks up a coin worth the load current there, scaled down by how well that node is wired. Then it picks a wire at random, a thick wire more often than a thin one, and walks along it. Sometimes it picks the pad instead, which leads to the supply, and then the walk ends.

Add up the coins of one walk. Do this for many walks and take the mean. That mean is the voltage drop at the start node. A node close to a pad has short walks and a small drop. A node far from the pads, among heavy loads, has long walks with many coins.

## The problem

The grid is in drop form, as on the [power grid analysis](/power-grid-analysis/) page: $G x = i$ with $G = \mathcal{L} + \mathrm{diag}(g^{\mathrm{pad}})$, where $\mathcal{L}$ is the [Laplacian](/laplacian-matrix/) of the wire conductances $g_{mj}$, $g^{\mathrm{pad}}_m \ge 0$ is the conductance from node $m$ to the ideal supply, $i_m \ge 0$ is the load current at $m$, and $x_m = V_{DD} - v_m$ is the drop. Every connected part of the grid has a pad. The input is the grid and one node $k$, and the output is an estimate of $x_k$ with a measure of its error. The method fits no parameter of its own. The conductances and loads come from layout extraction, foundry data and power estimates, as the power grid analysis page explains, and the estimate is only as good as they are.

Let $D_m = \sum_j g_{mj} + g^{\mathrm{pad}}_m$ be the total conductance at $m$. Row $m$ of $G x = i$, divided by $D_m$, reads

$$ x_m = \frac{i_m}{D_m} + \sum_j \frac{g_{mj}}{D_m}\, x_j + \frac{g^{\mathrm{pad}}_m}{D_m} \cdot 0 . $$

The weights $g_{mj}/D_m$ and $g^{\mathrm{pad}}_m/D_m$ are nonnegative and sum to 1, so they are the step probabilities of a walk, and the supply is a stopping state with drop 0. This identity is the discrete harmonic property of the grid with sources.

## The algorithm

```pseudo id=main
RANDOM-WALK-DROP(grid, k, W)
L1  s ← 0
L2  repeat W times
L3      m ← k; R ← 0
L4      loop
L5          R ← R + i_m / D_m                         ▷ the reward of this visit
L6          with probability g^pad_m / D_m stop the walk
L7          otherwise move to a neighbor j with probability g_mj / D_m
L8      s ← s + R
L9  return s / W, and the standard error from the sample variance of R
```

The tables of line L7, one cumulative list of $g_{mj}/D_m$ per node, are built once, and each step picks a neighbor by a binary search on a uniform number. A walk that starts at a node of a part with no pad would never stop, so the code checks that every part has a pad before it starts.

## Example

Take a chain of 3 nodes: node 0 has a pad of 20 S, the wires 0 to 1 and 1 to 2 have 10 S each, and the loads are 0.2 A at node 1 and 0.3 A at node 2. Then $D = (30, 20, 10)$, and the rewards $i_m/D_m$ are $(0, 0.01, 0.03)$ V. By hand: all 0.5 A flows through the pad, so $x_0 = 0.5/20 = 0.025$ V. Wire 0 to 1 carries 0.5 A, so $x_1 = 0.025 + 0.05 = 0.075$ V. Wire 1 to 2 carries 0.3 A, so $x_2 = 0.075 + 0.03 = 0.105$ V.

From node 2 the walker always moves to node 1. From node 1 it moves to node 0 or node 2 with probability 1/2 each. From node 0 it moves to node 1 with probability 1/3 and stops with probability 2/3. With the seed 2024, the first three walks from node 2 are $2, 1, 2, 1, 2, 1, 2, 1, 0$ with reward $4 \cdot 0.03 + 4 \cdot 0.01 = 0.16$, then $2, 1, 0$ twice, with reward $0.04$ each. The walks vary a lot, but their mean is right:

| walks $W$ | estimate of $x_2$ (V) | standard error (V) |
|---|---|---|
| 100 | 0.1188 | 0.0093 |
| 1000 | 0.10832 | 0.00272 |
| 10 000 | 0.104211 | 0.000814 |
| 100 000 | 0.104914 | 0.000259 |

The exact value is 0.105. The exact standard deviation of one walk's reward is $\sqrt{0.006675} \approx 0.0817$ V, and the standard errors follow $0.0817/\sqrt{W}$. A walk from node 2 makes 7 visits and 6 steps on average. The table comes from the code of this page with Python's generator and the seed 1. It is a toy grid, and these are not benchmark results.

## Correctness

The [proof file](proofs/correctness.md) proves that the walk stops with probability 1 and that the expected reward of a walk from $k$ is exactly $x_k$. The step matrix $Q$ with $Q_{mj} = g_{mj}/D_m$ has rows that sum to at most 1, and from every node some path reaches a node with a pad, so $Q^t \to 0$ and the [spectral radius](/spectral-radius/) of $Q$ is below 1. The expected reward is $\sum_t (Q^t r)_k = ((I - Q)^{-1} r)_k$ with $r_m = i_m/D_m$, and since $D (I - Q) = G$, this is $(G^{-1} i)_k = x_k$. The number of visits has a geometric tail, so the reward has a finite variance. The estimate is therefore unbiased, it converges to $x_k$ by the [law of large numbers](/law-of-large-numbers/), and by the [central limit theorem](/central-limit-theorem/) the interval of two standard errors on each side covers $x_k$ about 95% of the time when $W$ is large.

What is not proved is the number of walks a real grid needs for a given error. It depends on the variance of the reward, which grows with the length of the walks, and it is measured.

## Complexity

Building the tables takes $O(N + E)$ time and space, where $N$ is the number of nodes and $E$ the number of wires. Each step costs $O(\log d)$ for the binary search. A run of $W$ walks with mean length $S$ steps costs $O(W S \log d)$ expected time beyond the tables. The mean length from node $k$ is $y_k - 1$, where $y$ solves $G y = D \mathbf{1}$, the expected number of visits. It grows with the distance to the pads, and on a mesh with pads far apart it can be large. The error after $W$ walks is $\sigma/\sqrt{W}$, so a tenfold smaller error costs a hundredfold more walks. The method does not need the whole grid in memory at once, only the parts that the walks visit, which is its main point for local queries.

## Properties

- **Unbiased, proved.** The expected reward of one walk is the exact drop. So the estimate has no systematic error, only a random one.
- **Local.** One query touches only the nodes that its walks visit. Nodes near pads are cheap. A full solve of the grid is not needed for one node.
- **Error from the sample.** The sample variance gives a [confidence interval](/confidence-interval/) at no extra cost.
- **Slow convergence.** The error falls as $1/\sqrt{W}$. For many nodes or a tight error, a direct or iterative solver of the whole grid is cheaper.
- **Parallel.** The walks are independent, so they run in parallel with no communication.

## Variants and improvements

- **Transient analysis.** With the [backward Euler method](/backward-euler-method/) and step $h$, each capacitor becomes a conductance $C/h$ to a source that holds the drop of the last time step, by the [companion model](/companion-model/). The walk then also stops at that source, with the old drop as its payoff.
- **Known nodes as stops.** Once the drop at some nodes is known, a walk that reaches one of them can stop there and take that drop as its payoff. The walks get shorter, and work done for one query helps the next.
- **Many nodes at once.** One walk visits many nodes, and the rewards of its tail from each node give samples for those nodes too, which lowers the cost per node when many nodes are queried.
- **Other solvers.** The [multigrid-like method](/multigrid-power-grid-analysis/) solves for every node at once, approximately. [Vectorless verification](/vectorless-power-grid-verification/) bounds the worst drop over a set of possible loads instead of one load vector.

## When to use it

Use it when you need the drop at a few nodes of a very large grid, for example after a local change of the grid near some cells, or to check a few hot spots. It also fits incremental analysis, since a local change affects only the walks that pass through it. Use a direct or preconditioned iterative solver when you need the drop everywhere, or a tight error at many nodes.

## Pitfalls

- **A part with no pad.** A walk there never stops. Check the connectivity before the walks start.
- **Floating rounding in the tables.** The cumulative list of line L7 must leave exactly the pad probability $g^{\mathrm{pad}}_m/D_m$ for the stop. At a node with no pad, rounding can leave a tiny stop probability or none, so build the tables in the same order in which they are summed.
- **Too few walks.** With few walks the sample variance itself is noisy. Report the standard error, and use more walks near nodes with long walks.
- **Treating one walk's payoff as a bound.** Single walks can pay much more or much less than the drop, as the example shows. Only the mean is right.
- **Nonlinear loads.** The identity needs fixed load currents. Loads that depend on the local voltage need an outer loop that updates the currents.

## Implementations

## History

The link between random walks and electric networks goes back to Kakutani's 1944 solution of the Dirichlet problem by Brownian motion and was made popular for networks by Doyle and Snell's book of 1984. In EDA it was first used in capacitance extraction, in the floating random walk of Le Coz and Iverson (1992). Qian, Nassif and Sapatnekar (2003) gave it to power grid analysis as a game in which the walker pays the load costs and is paid the supply voltage at the pads, and in 2005 they extended it to transient analysis. Later work used the same walks to build preconditioners for iterative grid solvers.

## References
