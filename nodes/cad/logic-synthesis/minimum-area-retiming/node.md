---
tag: HEA0W3
kind: algorithm
slug: minimum-area-retiming
name: Minimum-area retiming
aliases:
- minimum register retiming
area: cad/logic-synthesis
level: advanced
summary: Retimes a circuit to the fewest registers under a clock period bound, as the dual of a minimum cost flow problem.
model: word-ram
complexity:
  vars: {V: the number of gates with the host, E: the number of wires, M: "the number of constraints, at most E + V^2"}
  time: {worst: O(E V M)}
  space: {extra: O(V^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1991
  people: [Charles E. Leiserson, James B. Saxe]
  note: Leiserson and Saxe stated the least register count under a period bound as a linear program whose dual is a min-cost flow problem, and they gave the mirror vertices that count shared fanout registers.
prereqs: [retiming, min-cost-flow-problem, lp-duality]
see_also: [successive-shortest-path, network-simplex, total-unimodularity, complementary-slackness, difference-constraints, bellman-ford, clock-skew-scheduling, dual-linear-program]
sources:
  - paper: doi:10.1007/BF01759032
    title: Charles E. Leiserson and James B. Saxe, Retiming synchronous circuitry, Algorithmica 6(1-6), 5 to 35, 1991
    locator: the sections on minimizing the number of registers, the linear program and its min-cost flow dual, and the mirror vertices for fanout sharing
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 9, Sequential Logic Optimization (retiming for area)
  - paper: "Narendra Shenoy and Richard Rudell, Efficient implementation of retiming, Proceedings of ICCAD 1994"
    title: Efficient implementation of retiming
    locator: the reduction of the period constraints that makes minimum-area retiming run on large circuits (general locator)
---

Minimum-area retiming moves the registers of a synchronous circuit so that it has the fewest registers, either with no clock period bound or with a period of at most $c$. The variables are the same as in [retiming](/retiming/): one integer $r(v)$ per gate. The register count of the retimed circuit is a linear function of $r$, and the constraints are [difference constraints](/difference-constraints/), so the problem is a linear program. Leiserson and Saxe observed that its [dual](/lp-duality/) is a [min-cost flow](/min-cost-flow-problem/) problem with no capacities, and that the node potentials of an optimal flow give an optimal integer retiming.

## In plain words

A register costs area and power. Retiming can move registers to places where fewer of them do the same job, for example from the two inputs of a gate to its one output. Each gate gets a number, which says how many registers it pushes from its outputs back to its inputs. The total count of registers is a sum of these numbers with plus and minus signs. The rules are the same as for retiming: no wire gets a negative count, and no long stretch of logic stays without a register when a clock period is given. So the task is to minimize a sum under rules of the form "this number minus that number is at most a constant". This is the mirror image of a cheapest way to ship goods through a network, and a flow algorithm solves it exactly.

## The problem

The circuit is $G = (V, E)$ with gate delays $d(v)$, register counts $w(e)$, and a host $h$, as on the [retiming](/retiming/) page. A retiming $r$ with $r(h) = 0$ gives $w_r(e) = w(e) + r(v) - r(u)$ for $e = (u, v)$, and it is legal when all $w_r(e) \ge 0$. The input also has an optional period bound $c$. The output is a legal retiming with $c(G_r) \le c$ that minimizes the register count, and that count. Two counts are common.

- **Per edge.** $N(r) = \sum_e w_r(e)$, one register for each register on each wire.
- **Shared.** $N_s(r) = \sum_u \max_{e \text{ out of } u} w_r(e)$. The fanout edges of a gate can share one chain of registers, and the gate needs as many as its most delayed fanout.

Like retiming, this page moves registers and keeps a single clock time for all of them. [Clock skew scheduling](/clock-skew-scheduling/) keeps the registers and moves the clock arrival times. All three are solved through difference constraints.

## The algorithm

Since $\sum_e (r(v) - r(u))$ counts $r(x)$ once for each edge into $x$ and minus once for each edge out of $x$, the per-edge count is
$$N(r) = \sum_e w(e) + \sum_x a(x)\, r(x), \qquad a(x) = \mathrm{indeg}(x) - \mathrm{outdeg}(x).$$
So the problem is the linear program: minimize $\sum_x a(x) r(x)$ subject to $r(u) - r(v) \le b$ for each constraint $(u, v, b)$. Its dual has one variable $f \ge 0$ per constraint: minimize $\sum b f$ subject to "inflow minus outflow equals $a(x)$" at every vertex, where the constraint $(u, v, b)$ is an arc $u \to v$ of cost $b$. That is a min-cost flow problem.

```pseudo id=main
MIN-AREA-RETIMING(G, w, d, h, c, shared)
L1  S ← { (u, v, w(e)) : e = (u, v) ∈ E }            ▷ (u, v, b) means r(u) - r(v) ≤ b
L2  B ← every edge e of G with breadth β(e) = 1        ▷ the terms of the objective
L3  if shared then for each gate u with k ≥ 2 fanout edges e_i = (u, v_i) do
L4      add a mirror vertex m_u, and add (v_i, m_u, w_max(u) - w(e_i)) to S for each i
L5      in B, give e_i and the new edge (v_i, m_u) the breadth 1/k; scale all breadths to integers
L6  if c is given then compute W and D, and add (u, v, W(u, v) - 1) to S for each D(u, v) > c
L7  a(x) ← Σ β(e) over the edges of B into x  -  Σ β(e) over the edges of B out of x
L8  arcs ← { u → v with cost b, no capacity : (u, v, b) ∈ S }
L9  f ← a min-cost flow on arcs with inflow(x) - outflow(x) = a(x) at each x,
        by successive shortest paths with Bellman-Ford
L10 if the arcs have a negative cycle or no flow meets a, return "infeasible"
L11 π ← shortest distances in the residual graph of f, from a virtual source
L12 r ← π(h) - π on the vertices of G
L13 return r and the count of G_r
```

Here $w_{\max}(u)$ is the largest $w(e_i)$ over the fanout edges of $u$. Lines L3 to L5 build the mirror vertices of Leiserson and Saxe. The path $u \to v_i \to m_u$ has $w_{\max}(u)$ registers for every $i$, so the $k$ paths, each with breadth $1/k$, add up to $w_{\max}(u) + r(m_u) - r(u)$. The constraint on the edge $(v_i, m_u)$ forces this value to be at least $w_r(e_i)$ for each $i$, and the optimum makes it equal to the largest one. Line L6 adds the period constraints of the [retiming](/retiming/) page. Lines L11 and L12 read the retiming off the flow: the potentials $\pi$ make every reduced cost $b + \pi(u) - \pi(v)$ nonnegative and make it zero on every arc that carries flow, which is complementary slackness for the pair of programs.

## Example

**One gate.** A gate $1$ with delay 1 reads the host twice, through edges $(0,1)$ with one register each, and drives the host by $(1,0)$ with none. So $N = 2$, and $a(0) = 1 - 2 = -1$, $a(1) = 2 - 1 = 1$. The arcs are $0 \to 1$ of cost 1, twice, and $1 \to 0$ of cost 0. The flow sends one unit from $0$ to $1$ along an arc of cost 1, so the dual optimum is 1, and $N$ drops by 1. The potentials have $\pi(1) - \pi(0) = 1$, which gives $r(1) = \pi(0) - \pi(1) = -1$. The two input registers become one register on the output edge $(1, 0)$, and the count is 1.

**The correlator.** Take the correlator of the [retiming](/retiming/) page, with 4 registers and period 24.

| period bound $c$ | least per-edge count | least shared count |
|---|---|---|
| none | 4 | 4 |
| 24, 16 | 4 | 4 |
| 14, 13 | 5 | 4 |
| 12 | infeasible | infeasible |

At $c = 13$, every legal retiming that meets the bound puts at least 5 registers on the edges. One of them is the retiming of the retiming page, with registers on the edges $(1,2)$, $(3,4)$, $(5,6)$, $(6,7)$ and $(1,7)$. The edges $(1,2)$ and $(1,7)$ both leave gate 1 with one register, so with sharing they use one register, and the count is 4.

## Correctness

The per-edge count is the linear function above, and by the theorem on the retiming page, the constraints of lines L1 and L6 describe exactly the legal retimings that meet the period bound. With the mirror vertices, the minimum of the modeled objective over $r(m_u)$ is the shared count, so the program is right for both counts. The constraint matrix is the transpose of a network matrix, so it is [totally unimodular](/total-unimodularity/), and with integer bounds the program has an integer optimum. Bellman-Ford returns integer potentials, the potentials meet complementary slackness with the optimal flow, and so $r = -\pi$ (shifted to $r(h) = 0$) is optimal for the primal. The [full proof](proofs/correctness.md) gives the details.

## Complexity

The system has $M \le E + V^2$ constraints, or $E$ with no period bound. Lines L1 to L7 take $O(V^3)$ time with the period bound, for $W$ and $D$, and $O(E)$ without it. For the per-edge count, the total demand $\sum_x \max(a(x), 0)$ is at most $E$, and each shortest path pushes at least one unit, so successive shortest paths make at most $E$ rounds of Bellman-Ford, each in $O(VM)$ time. That is $O(EVM)$ time and $O(V^2)$ space. For the shared count, the scale factor of line L5 multiplies the demands, so this bound grows with the least common multiple of the fanout sizes. A min-cost flow method whose time does not depend on the demands, such as [cost scaling](/cost-scaling/), removes this factor.

## Properties

- **Exact.** The count is the least over all legal retimings with the period bound, for the count model chosen.
- **Integral.** The optimum is reached by an integer retiming, by total unimodularity.
- **Infeasibility is detected.** If no retiming meets the period bound, the constraint graph has a negative cycle, and line L10 reports it.
- **The function is kept.** As for any retiming, the gates are unchanged, and the output streams are the same after the start-up phase.

## Variants and improvements

- **Weighted registers.** Give each edge a cost per register, for example for wide buses. The breadths of line L2 become these costs, and nothing else changes.
- **Least period first.** Run [retiming](/retiming/) for the least period $c^*$, then minimum-area retiming with $c = c^*$. This gives the fewest registers among the fastest retimings.
- **Fewer constraints.** Most period constraints are implied by others. Shenoy and Rudell (1994) prune them, which makes the method practical for large netlists.
- **Other flow solvers.** Any min-cost flow solver that returns optimal potentials works, for example [network simplex](/network-simplex/), whose dual values are the potentials, or [successive shortest paths](/successive-shortest-path/) with Dijkstra and reduced costs.

## When to use it

Use it when the clock period is fixed by the design and the register count, area or power should go down, for example after a pipeline was added by hand. Use the shared count for real hardware, since a gate with many fanouts can share one register chain. When the registers must stay put, for example because of test or verification, use [clock skew scheduling](/clock-skew-scheduling/) for timing instead.

## Pitfalls

- **Per-edge counts overstate the area.** Without the mirror vertices, the program pays for every fanout edge, and it may refuse a move that a shared register makes cheap. In the correlator at $c = 13$, the per-edge count is 5, but the circuit needs only 4 registers.
- **Lost constraints in the flow.** The arcs have no capacity. A flow code that gives them a finite capacity must make it large enough that no arc is saturated, or the saturated arc drops out of the residual graph and its constraint is lost from the potentials. Then $r$ can break the period bound.
- **The sign of the potentials.** The constraint $r(u) - r(v) \le b$ is met by $r = -\pi$, not by $r = \pi$, when the arc is $u \to v$ of cost $b$.
- **Initial states.** As for [retiming](/retiming/), the moved registers need new initial values, and a backward move can make them impossible to find.

## Implementations

## History

Leiserson and Saxe (1991) stated the minimum register problem as a linear program over the retiming variables, observed that its dual is a min-cost flow problem, and gave the mirror vertex construction for shared fanout registers. Shenoy and Rudell (1994) reduced the number of period constraints so that the method runs on large netlists.

## References
