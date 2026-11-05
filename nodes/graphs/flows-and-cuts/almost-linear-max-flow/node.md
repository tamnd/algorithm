---
tag: 8Q450K
kind: algorithm
slug: almost-linear-max-flow
name: Almost-linear-time maximum flow algorithm
aliases:
- almost-linear max flow
- Chen-Kyng-Liu-Peng-Probst Gutenberg-Sachdeva algorithm
area: graphs/flows-and-cuts
level: research
summary: Max flow and min-cost flow in m^(1+o(1)) time by an l1 interior point method whose steps are min-ratio cycles kept by a dynamic data structure.
solves: [max-flow-problem, min-cost-flow-problem]
model: word-ram
complexity:
  vars: {m: the number of edges, U: the largest capacity}
  time: {worst: O(m^(1+o(1)) log(U))}
  space: {extra: O(m^(1+o(1)))}
properties: {deterministic: false, recursive: false}
history:
  year: 2022
  people: [Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst Gutenberg, Sushant Sachdeva]
  note: Presented at FOCS 2022, where it received the best paper award; a deterministic version by van den Brand and others followed in 2023.
prereqs: [max-flow-problem, min-cost-flow-problem, interior-point-method]
see_also: [electrical-flow, low-stretch-spanning-tree, cycle-canceling, minimum-mean-cycle-problem, push-relabel, dinic, dynamic-max-flow-problem, flow-integrality-theorem]
sources:
  - paper: url:https://arxiv.org/abs/2203.00671
    title: Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst Gutenberg and Sushant Sachdeva, Maximum flow and minimum-cost flow in almost-linear time, FOCS 2022
    locator: the overview (the potential function, min-ratio cycles and their stability) and the main theorem (m^(1+o(1)) log U log C time for min-cost flow)
  - paper: doi:10.1145/1993636.1993674
    title: Paul Christiano, Jonathan A. Kelner, Aleksander Madry, Daniel A. Spielman and Shang-Hua Teng, Electrical flows, Laplacian systems, and faster approximation of maximum flow in undirected graphs, STOC 2011
    locator: the introduction (the earlier line of work through electrical flows)
  - paper: doi:10.1109/FOCS.2013.35
    title: Aleksander Madry, Navigating central path with electrical flows, from flows to matchings, and back, FOCS 2013
    locator: the introduction (the first interior point method for exact maximum flow below m^(3/2))
---

The almost-linear-time maximum flow algorithm of Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva (2022) computes an exact [maximum flow](/max-flow-problem/), and more generally a [minimum-cost flow](/min-cost-flow-problem/), on a directed graph with integer capacities in $m^{1 + o(1)} \log U$ time. It is an [interior point method](/interior-point-method/) whose steps follow cycles: each step augments the current fractional flow along a cycle that minimizes the ratio of gradient to length, and a randomized dynamic data structure, built from [low-stretch spanning trees](/low-stretch-spanning-tree/) and recursive graph sparsification, finds such a cycle approximately in amortized $m^{o(1)}$ time. About $m^{1 + o(1)}$ steps bring the cost within a tiny gap of optimal, and the fractional flow is then rounded to an exact integral optimum. This page explains the method and gives a small exact version in which the data structure is replaced by a slow but exact cycle search.

## In plain words

Start with every pipe half full, and fix the leftover at each place with temporary pipes that are expensive to use. A score measures how far the plan is from the best one, plus a penalty that grows as any pipe gets close to empty or full. In each step, find the loop of pipes along which a small shift helps the score most per unit of risk, and shift some water around that loop. After many such steps the plan is almost the best, with every pipe still strictly between empty and full. Then round the amounts to whole numbers along loops without making the plan worse, and finish with a few ordinary extra routes. The clever part of the real algorithm is finding a good loop in each step with almost no work.

## The problem

**Input.** A directed graph with $n$ vertices and $m$ edges, a source $s$ and a sink $t \ne s$, and integer capacities $u(e) \ge 0$ with largest value $U$. Parallel and antiparallel edges are separate variables; antiparallel edges are never merged. An edge of capacity 0 is dropped, since it can carry nothing, and so is a self-loop.

**Output.** An integral maximum s-t flow and its value. The general algorithm also handles integer costs up to $C$, lower bounds and demands, which gives the min-cost flow problem in $m^{1 + o(1)} \log U \log C$ time.

**As a circulation.** Add a return edge $(t, s)$ of capacity $U_s$, the total capacity leaving $s$, with cost $-1$; all other edges cost 0. A circulation of cost $-F$ is then an s-t flow of value $F$ plus $F$ units on the return edge, so a least-cost circulation is a maximum flow. Let $c$ be the cost vector, $f$ the flow vector and $F^* = \min c^\top f$.

## The algorithm

**The potential.** For a flow strictly inside its bounds $0 < f_e < u_e$, Chen and others use
$$\Phi(f) = 20 m \log(c^\top f - F^*) + \sum_e \left( (u_e - f_e)^{-\alpha} + f_e^{-\alpha} \right), \qquad \alpha = \frac{1}{1000 \log(m U)}.$$
The first term pulls the cost down and the barrier keeps every edge away from its bounds; $\Phi$ is very negative only when the cost is close to $F^*$.

**The step.** Let $g = \nabla \Phi(f)$ and give edge $e$ the length $\ell_e = (u_e - f_e)^{-1-\alpha} + f_e^{-1-\alpha}$, which is large near a bound. A **min-ratio cycle** is a circulation $\Delta$ minimizing $g^\top \Delta / \lVert L \Delta \rVert_1$, where $L$ is the diagonal matrix of lengths; it can be taken to be a simple cycle in the graph with each edge usable in both directions. Pushing a small multiple of it lowers $\Phi$ by $m^{-o(1)}$, even when the cycle is only an $m^{o(1)}$ approximation of the best. Since $\Phi$ starts at $O(m \log(m U))$, after about $m^{1 + o(1)} \log U$ steps the cost is within $m^{-10}$ of $F^*$.

**The data structure.** The key point is that the gradients and lengths change slowly, so the min-ratio cycle problem can be solved dynamically. Chen and others keep a few low-stretch spanning trees: every cycle in a tree plus one edge is a candidate, and some candidate is an $m^{o(1)}$ approximation. The trees are made small by recursive vertex sparsification, giving amortized $m^{o(1)}$ time per step. The structure is randomized; the deterministic version came in 2023.

**The exact version on this page.** The implementation below keeps the outer method and replaces the data structure by an exact min-ratio cycle search, Dinkelbach's method with [Bellman-Ford](/bellman-ford/) as the negative cycle test. It does not know $F^*$, so it uses the lower bound $F_{\mathrm{lo}} = -U_s - 1$ in place of $F^*$ in the first term. It starts at half of each capacity, which is not a circulation, and fixes the imbalance with edges to and from a new vertex $z$, each carrying the imbalance at half its capacity, with cost 4.

```pseudo id=main
ALMOST-LINEAR-MAX-FLOW(G, u, s, t)
L1  variables: each edge with u_e > 0, and a return edge (t, s) of capacity U_s and cost −1; f_e ← u_e / 2
L2  add a vertex z and, for each vertex v with imbalance b(v) ≠ 0, an edge between v and z of capacity 2|b(v)| and cost 4 carrying |b(v)|
L3  repeat at most a fixed number of steps
L4      g ← ∇Φ(f);  ℓ_e ← (u_e − f_e)^(−1−α) + f_e^(−1−α) for each variable
L5      Δ ← a cycle minimizing g·Δ / Σ ℓ_e |Δ_e|;  stop if no cycle has a negative ratio
L6      f ← f + η Δ for the largest η among 1/2, 1/4, ... of the room to the bounds that lowers Φ;  stop if none does
L7  round f to an integral circulation by pushing along cycles of fractional variables in the direction that does not raise the cost
L8  cancel the flow on the edges at z along cycles through z
L9  augment along shortest residual s-t paths until none is left; return the flow on the original edges
```

Lines L3 to L6 are the interior point method; in the real algorithm line L5 is answered approximately by the data structure, and the number of steps is $m^{1 + o(1)} \log U$. Lines L7 to L9 make the answer exact whatever the interior point phase reached. If the phase ends with $c^\top f < F^* + 1$, line L9 makes no augmentation at all.

## Example

Take the running network $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10. Here $U_s = 20$, so the return edge has capacity 20 and $F_{\mathrm{lo}} = -21$; the maximum flow value is 19, so $F^* = -19$. Starting from half capacities (10 on the return edge), $a$ has a net outflow of 2, $c$ a net inflow of 1.5 and $d$ a net inflow of 0.5, so they get edges from or to $z$; $s$, $b$ and $t$ are balanced. The table shows how far the cost $c^\top f$ (including the cost 4 per unit on edges at $z$) is above $F^*$ after some steps.

| step | 1 | 2 | 5 | 10 | 20 | 40 | 60 | 119 |
|---|---|---|---|---|---|---|---|---|
| $c^\top f - F^*$ | 19 | 16 | 10.94 | 5.30 | 1.19 | 0.071 | 0.0044 | 0.0023 |

After 119 steps no step lowers $\Phi$; the gap stays at 0.0023 because the barrier balances the pull toward $F_{\mathrm{lo}}$, which is 2 below $F^*$. Rounding gives the integral flow $s a$ 10, $s c$ 9, $a b$ 4, $a c$ 0, $a d$ 6, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 9 of value 19, and line L9 finds no augmenting path. With the step limit set to 0, rounding the starting point and then line L9 alone also give 19, after several augmentations.

**Edge cases.** An edge of capacity 0 is not a variable and gets flow 0. In the network $s \to a$ 5, $t \to a$ 5 there is no s-t path; the answer is 0. With antiparallel edges $0 \to 1$ 3, $1 \to 0$ 2, $1 \to 2$ 3, $2 \to 1$ 4 the answer is 3 with flows 3, 0, 3, 0, each edge with its own variable. If no capacity leaves $s$, the answer 0 is returned at once.

## Correctness

The [correctness proof](proofs/correctness.md) covers the exact version. Each step of line L6 adds a multiple of a cycle and stays strictly inside the bounds, so $f$ remains a circulation. Line L7 keeps a circulation within the bounds: a vertex touching a fractional variable has an integral net flow, so it touches at least two, and the fractional variables contain a cycle; each push makes at least one more variable integral and does not raise the cost. Line L8 removes the flow at $z$, since flow conservation gives a path back to $z$ whenever flow leaves it, which leaves an integral s-t flow in the original network. Line L9 is [Ford-Fulkerson](/ford-fulkerson/) from that flow, which ends with a maximum flow. If the interior point phase ends with $c^\top f < F^* + 1$, the rounded circulation has an integer cost below $F^* + 1$, so it is optimal; an optimal circulation sends nothing through $z$, since a cycle through $z$ costs at least $2 \cdot 4 - 1 > 0$; so lines L8 and L9 change nothing.

The bound on the number of steps in the real algorithm, that each approximate min-ratio cycle lowers $\Phi$ by $m^{-o(1)}$, is proved in the paper and not on this page.

## Complexity

**The real algorithm.** $m^{1 + o(1)} \log U$ steps at amortized $m^{o(1)}$ time each, so $m^{1 + o(1)} \log U$ in total, with high probability; the $m^{o(1)}$ factor is $\exp(O(\log^{7/8} m \log \log m))$. For min-cost flow a factor $\log C$ is added. The space is $m^{1 + o(1)}$.

**The exact version here.** Each min-ratio cycle search runs Bellman-Ford, $O(nm)$, a number of times that depends on the data, and each step also costs $O(m)$; with a fixed limit of $30 m$ steps it is polynomial but far slower than Dinic or push-relabel. Rounding takes $O(m)$ cycle pushes of $O(m)$ each, and line L9 takes $O(m)$ per augmentation. It shows the method, not the speed.

## Properties

- **Exact and integral** for integer capacities, after the rounding.
- **Randomized** in the original; deterministic since 2023.
- **Handles directed graphs and costs**, unlike the earlier electrical-flow methods, which gave approximate flows on undirected graphs.
- **Not practical yet.** The $m^{o(1)}$ factors and the data structure make it slower than [push-relabel](/push-relabel/) or [Dinic](/dinic/) on any realistic input.

## Variants and improvements

- **Deterministic.** Van den Brand, Chen, Kyng, Liu, Meierhans, Probst Gutenberg and Sachdeva (2023) removed the randomness.
- **Incremental and dynamic.** Follow-up work keeps approximately or exactly optimal flows under edge insertions in almost-linear total time; see the [dynamic maximum flow problem](/dynamic-max-flow-problem/).
- **Consequences.** Almost-linear time also follows for negative-weight single-source shortest paths, bipartite matching, [Gomory-Hu trees](/gomory-hu-tree/) in the undirected case, and many other problems that reduce to min-cost flow.

## When to use it

In theory, for any flow problem with polynomially bounded integers, where it gives the best known bound. In practice, never yet; use push-relabel, Dinic or a network simplex code, and keep this as a guide to what is possible.

## Pitfalls

- **Calling it an electrical flow method.** The earlier line of work by Christiano and others, Madry and Lee and Sidford solved Laplacian systems for [electrical flows](/electrical-flow/); this algorithm uses an $\ell_1$ step, the min-ratio cycle, and no Laplacian solve.
- **Rounding too early.** Rounding a fractional flow with cost $F^* + 1$ or more can give a non-optimal integral flow; the exact version finishes with augmenting paths for that reason.
- **Starting on the boundary.** The barrier needs $0 < f_e < u_e$, so the zero flow cannot be the start; that is why the edges at $z$ exist.
- **Floating point.** The barrier values grow fast near the bounds; the exact version snaps values within $10^{-9}$ of an integer before rounding.

## Implementations

The Python version takes the vertex count, a list of directed edges $(u, v, c)$ with integer capacities, $s$ and $t$, and returns the value and the integral flow on each edge. It accepts a step limit and a callback that reports the gap $c^\top f - F_{\mathrm{lo}}$ after each step and the number of augmentations at the end.

## History

Christiano, Kelner, Madry, Spielman and Teng (2011) found approximate undirected flows through electrical flows, and Madry (2013) gave the first exact interior point method below $m^{3/2}$ on unit-capacity graphs. Interior point methods with faster linear algebra followed, by Lee and Sidford and by van den Brand and others. Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva announced the almost-linear algorithm in March 2022 and presented it at FOCS 2022.

## References
