---
tag: 9JAVQE
kind: algorithm
slug: retiming
name: Retiming
aliases:
- Leiserson-Saxe retiming
- minimum period retiming
area: eda/logic-synthesis
level: core
summary: Leiserson and Saxe's moving of registers across gates without changing behaviour. A minimum clock period retiming is found by binary search and Bellman-Ford.
model: word-ram
complexity:
  vars: {V: the number of gates with the host, E: the number of wires}
  time: {worst: O(V^3 log V)}
  space: {extra: O(V^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1983
  people: [Charles E. Leiserson, Flavio M. Rose, James B. Saxe]
  note: Leiserson, Rose and Saxe introduced retiming at the Caltech VLSI conference in 1983. The journal version by Leiserson and Saxe in Algorithmica (1991) gives the W and D matrices, the algorithms OPT1, OPT2 and FEAS, and minimum-area retiming.
prereqs: [difference-constraints, bellman-ford, static-timing-analysis]
see_also: [minimum-area-retiming, clock-skew-scheduling, floyd-warshall, negative-cycle-detection, timing-graph, setup-and-hold-constraints, dag-longest-path, karp-minimum-mean-cycle]
sources:
  - paper: doi:10.1007/BF01759032
    title: Charles E. Leiserson and James B. Saxe, Retiming synchronous circuitry, Algorithmica 6(1-6), 5 to 35, 1991
    locator: the circuit graph, the W and D matrices, the theorem that characterizes legal retimings of period at most c, and the algorithms OPT1, OPT2 and FEAS
  - paper: "Charles E. Leiserson, Flavio M. Rose and James B. Saxe, Optimizing synchronous circuitry by retiming, Proceedings of the Third Caltech Conference on VLSI, 87 to 116, 1983"
    title: Optimizing synchronous circuitry by retiming
    locator: the first statement of retiming and of the minimum period problem (general locator)
  - paper: "Hervé J. Touati and Robert K. Brayton, Computing the initial states of retimed circuits, IEEE Transactions on Computer-Aided Design 12(1), 157 to 162, 1993"
    title: Computing the initial states of retimed circuits
    locator: equivalent initial states after retiming, and the case where a backward move has no equivalent state
  - paper: "Narendra Shenoy and Richard Rudell, Efficient implementation of retiming, Proceedings of ICCAD 1994"
    title: Efficient implementation of retiming
    locator: the pruning of the period constraints for large circuits (general locator)
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 9, Sequential Logic Optimization (the sections on retiming)
---

Retiming moves the registers of a synchronous circuit across its gates, so that the circuit computes the same output streams with a shorter clock period or with fewer registers. Leiserson and Saxe model the circuit as a graph with a delay on each gate and a register count on each wire, and they describe a retiming by one integer per gate. A retiming with clock period at most $c$ exists exactly when a system of [difference constraints](/difference-constraints/) has a solution, so [Bellman-Ford](/bellman-ford/) tests each $c$ and a binary search over $O(V^2)$ candidate values finds the least period in $O(V^3 \log V)$ time. This page treats the least period. The least register count is [minimum-area retiming](/minimum-area-retiming/).

## In plain words

A clocked circuit has blocks of logic with registers between them. The clock must wait for the slowest stretch of logic between two registers. Retiming slides registers forward or backward through the gates. A register that leaves all the outputs of a gate reappears on all of its inputs, and the other way round. The values that come out of the circuit stay the same, but the long stretches can get shorter. The method gives each gate a number: how many registers it pushes from its outputs back to its inputs. Two simple rules on these numbers say that no wire gets a negative count and that no long stretch is left without a register. The rules are of the form "this number minus that number is at most a constant", and a shortest path algorithm solves them.

## The problem

The circuit is a graph $G = (V, E)$. A vertex is a gate with an integer delay $d(v) \ge 0$. The host vertex $h$ stands for the outside world, with $d(h) = 0$. An edge $e = (u, v)$ is a wire from the output of $u$ to an input of $v$, and $w(e) \ge 0$ is the number of registers on it. Every cycle has at least one register. For a path $p$, $w(p)$ is the sum of the register counts and $d(p)$ is the sum of the delays of its vertices, ends included. The clock period is
$$c(G) = \max \{ d(p) : w(p) = 0 \}.$$
A retiming is a map $r : V \to \mathbb{Z}$ with $r(h) = 0$. It gives the new counts $w_r(e) = w(e) + r(v) - r(u)$ for $e = (u, v)$, and it is legal when every $w_r(e) \ge 0$. The output is a legal retiming $r$ that minimizes $c(G_r)$, and that least period.

Retiming moves registers. The clock still reaches every register at the same time. [Clock skew scheduling](/clock-skew-scheduling/) does the opposite: it keeps the registers where they are and moves the clock arrival time $c_i$ of each register. Both lead to difference constraints solved by Bellman-Ford, but the variables are different.

## The algorithm

Let $W(u, v)$ be the fewest registers on a path from $u$ to $v$, and $D(u, v)$ the largest delay of a path from $u$ to $v$ with $W(u, v)$ registers. The empty path gives $W(v, v) = 0$ and $D(v, v) = d(v)$.

```pseudo id=main
MIN-PERIOD-RETIMING(G, w, d, h)
L1  best(u, v) ← the least sum of the pairs (w(e), -d(tail of e)) over the paths from u to v,
        by Floyd-Warshall with lexicographic order, and best(v, v) ← (0, 0)
L2  W(u, v) ← the first part of best(u, v);  D(u, v) ← d(v) minus the second part
L3  let c_1 < c_2 < ... < c_k be the distinct values of D
L4  lo ← 1, hi ← k, best_r ← 0
L5  while lo < hi do
L6      mid ← ⌊(lo + hi) / 2⌋
L7      S ← { r(u) - r(v) ≤ w(e) : e = (u, v) ∈ E }
L8          ∪ { r(u) - r(v) ≤ W(u, v) - 1 : D(u, v) > c_mid }
L9      r ← BELLMAN-FORD on S, from a virtual source with a 0 edge to every vertex
L10     if a negative cycle is found then lo ← mid + 1
L11     else hi ← mid, best_r ← r - r(h)
L12 return (c_lo, best_r)
```

Lines L1 and L2 compute the two matrices with one all-pairs pass. A path is better when it has fewer registers, and among paths with the same count, when it has more delay. So the weight of an edge is the pair $(w(e), -d(u))$, and pairs add and compare in lexicographic order. Floyd-Warshall works for this order because it is a total order that addition preserves and no cycle has a negative pair, since every cycle has a register. The constraint $r(u) - r(v) \le b$ is the edge $v \to u$ of weight $b$ in the constraint graph, and the shortest distances from the virtual source are a solution when no negative cycle exists. Line L8 holds the period constraints: a pair $(u, v)$ with $D(u, v) > c$ needs at least one register on every path from $u$ to $v$ after the retiming. When $u = v$ and $d(v) > c$, line L8 gives $0 \le -1$, a negative self loop, and no retiming works, as it should be.

## Example

The correlator of Leiserson and Saxe has a host $0$, four comparators $1$ to $4$ with delay 3 and three adders $5$ to $7$ with delay 7. Its edges are $(0,1,1)$, $(1,2,1)$, $(2,3,1)$, $(3,4,1)$, $(4,5,0)$, $(5,6,0)$, $(6,7,0)$, $(7,0,0)$, $(3,5,0)$, $(2,6,0)$ and $(1,7,0)$, written $(u, v, w)$. It has 4 registers, all on the chain of comparators. The path $3 \to 5 \to 6 \to 7$ has no register and delay $3 + 7 + 7 + 7 = 24$, so $c(G) = 24$.

The matrix $D$ has 20 distinct values: 0, 3, 6, 7, 9, 10, 12, 13, 14, 16, 17, 19, 20, 21, 23, 24, 26, 27, 30 and 33. The binary search probes them as follows.

| probe | $c$ | Bellman-Ford | interval of indices after the probe |
|---|---|---|---|
| 1 | 16 | a solution | values up to 16 |
| 2 | 9 | a negative cycle | from 10 to 16 |
| 3 | 13 | a solution | from 10 to 13 |
| 4 | 12 | a negative cycle | only 13 |

The least period is 13. A retiming that reaches it is $r = (0, -1, -1, -2, -2, -2, -1, 0)$ for the vertices $0$ to $7$. The new counts put one register on each of the edges $(1,2)$, $(3,4)$, $(5,6)$, $(6,7)$ and $(1,7)$, and none on the other edges, so the retimed circuit has 5 registers. Its longest path with no register is $2 \to 3 \to 5$, with delay $3 + 3 + 7 = 13$. The circuit has 143 legal retimings with $r(0) = 0$. Four of them have period 13, and none has a smaller period.

## Correctness

The key fact is that a retiming changes the register count of a path only through its two ends: $w_r(p) = w(p) + r(v) - r(u)$ for a path $p$ from $u$ to $v$, because the terms of the inner vertices cancel. From this, Leiserson and Saxe prove that $r$ is legal with $c(G_r) \le c$ exactly when $r$ satisfies the constraints of lines L7 and L8. A path with $D(u, v) > c$ needs a register after the retiming, and it is enough to ask this of the paths with $W(u, v)$ registers, since the other paths from $u$ to $v$ have at least one more register to start with and legality keeps their count at least 1. The least period over legal retimings is one of the values $D(u, v)$, and the test is monotone in $c$, so the binary search finds it. The largest value $c_k$ is at least $c(G)$, so the retiming $r = 0$ meets it. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Line L1 runs Floyd-Warshall in $O(V^3)$ time on pairs of integers. Each probe builds at most $E + V^2$ constraints, and Bellman-Ford takes $O(V \cdot (E + V^2)) = O(V^3)$ time on them. There are $k \le V^2$ values, so the search makes $O(\log V)$ probes. The total is $O(V^3 \log V)$ time and $O(V^2)$ space for $W$, $D$ and the constraints. Here $V$ and $E$ are the numbers of gates and wires of the netlist.

## Properties

- **Exact.** The result is the least period over all legal retimings of the circuit, with gate delays as given.
- **The function is kept.** A retiming changes where the registers are, not what the gates compute. After a start-up phase, the retimed circuit produces the same output streams as the original. See the pitfall on initial states.
- **Integral.** The constraints have integer bounds, so Bellman-Ford returns an integer retiming.
- **Registers are not minimized.** The retiming that Bellman-Ford returns is one feasible point of the constraints. Another retiming with the same period can use fewer registers.

## Variants and improvements

- **OPT2 with FEAS.** Leiserson and Saxe also test a period $c$ with FEAS, which needs no constraint system. Start from $r = 0$ and repeat $V - 1$ times: compute the arrival time of each gate in $G_r$ by [longest paths in the DAG](/dag-longest-path/) of edges with no register, and add 1 to $r(v)$ for each gate whose arrival time is more than $c$. If a retiming with period at most $c$ exists, the result has period at most $c$. Each test takes $O(VE)$ time, so the binary search takes $O(VE \log V)$ time after $W$ and $D$ are known.
- **Least registers.** [Minimum-area retiming](/minimum-area-retiming/) adds a linear objective to the same constraints and solves the dual [min-cost flow](/min-cost-flow-problem/) problem.
- **Fewer constraints.** Shenoy and Rudell (1994) keep only the period constraints that matter and do not store $W$ and $D$ in full, which makes retiming of large netlists practical.
- **A cycle bound.** A retiming does not change the register count $w(C)$ of a cycle $C$, and the $w(C)$ registers cut the cycle into $w(C)$ stretches with no register. So every legal retiming has a period of at least $d(C) / w(C)$, for every cycle $C$. The largest such ratio is a cycle ratio problem, related to [Karp's minimum mean cycle](/karp-minimum-mean-cycle/) method, and it gives a quick lower bound before the search.

## When to use it

Use retiming when the logic of a pipelined or sequential circuit is fixed and the registers are badly placed, for example after a pipeline was added by hand or after logic optimization changed the delays. It needs exact gate delays in the model; with wire delays and setup times, it gives an estimate that [static timing analysis](/static-timing-analysis/) must confirm. Use [minimum-area retiming](/minimum-area-retiming/) when the period is good enough and the register count matters. When the registers must stay where they are, use clock skew scheduling.

## Pitfalls

- **Initial states.** A retiming keeps the behaviour after a start-up phase, but the new registers need an initial value. For a register moved forward through a gate, the new value is the gate applied to the old values. For a register moved backward, one must find inputs to the gate that give the old value, and such inputs may not exist. Touati and Brayton (1993) compute equivalent initial states and show when none exists.
- **Signs.** With $w_r(e) = w(e) + r(v) - r(u)$, a positive $r(v)$ moves registers from the outputs of $v$ to its inputs. Mixing this with the opposite convention flips every constraint.
- **The host.** The host vertex must have $r(h) = 0$, or the retiming adds registers at the inputs and outputs and changes the latency that the outside world sees.
- **Cycles without registers.** A cycle with no register has no finite period. The input must be checked before the search.
- **Fanout.** Adding 1 to $r(v)$ takes one register off each edge out of $v$ and puts one on each edge into $v$. A gate with $k$ fanout edges has $k$ edge registers after a forward move, but the hardware can share them as one chain. So the sum of $w_r(e)$ is not the hardware count. [Minimum-area retiming](/minimum-area-retiming/) shows how to count shared registers.

## Implementations

## History

Leiserson, Rose and Saxe presented retiming at the Third Caltech Conference on VLSI in 1983. The journal version by Leiserson and Saxe appeared in Algorithmica in 1991, with the W and D matrices, the characterization of legal retimings of period at most $c$, the algorithms OPT1, OPT2 and FEAS, and the reduction of the least register count to a min-cost flow dual. Touati and Brayton (1993) treated the initial states of retimed circuits, and Shenoy and Rudell (1994) made the method practical for large netlists.

## References
