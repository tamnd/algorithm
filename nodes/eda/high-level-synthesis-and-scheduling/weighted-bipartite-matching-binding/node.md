---
tag: 6HS42N
kind: algorithm
slug: weighted-bipartite-matching-binding
name: Weighted bipartite matching binding
aliases:
- LYRA binding
- bipartite weighted matching allocation
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Huang, Chen, Lin and Hsu's binding that assigns variables to registers step by step through weighted bipartite matching, using the fewest registers and less interconnect.
solves: [register-binding]
model: word-ram
complexity:
  vars: {n: the number of values, L: the largest number of values live in one step, D: the number of unit input ports}
  time: {worst: O(n log n + n L^2 + n L D)}
  space: {extra: O(n + L^2 + L D)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1990
  people: [Chu-Yi Huang, Yen-Shen Chen, Youn-Long Lin, Yu-Chin Hsu]
  note: Huang, Chen, Lin and Hsu presented data path allocation by bipartite weighted matching at the Design Automation Conference in 1990.
prereqs: [register-binding, assignment-problem, hungarian-algorithm]
see_also: [left-edge-algorithm, interval-partitioning, tseng-siewiorek-clique-partitioning, interconnect-binding, resource-binding, resource-compatibility-graph, bipartite-graph, hopcroft-karp]
sources:
  - paper: doi:10.1145/123186.123350
    title: Chu-Yi Huang, Yen-Shen Chen, Youn-Long Lin and Yu-Chin Hsu, Data path allocation based on bipartite weighted matching, Proceedings of the 27th Design Automation Conference, 1990
    locator: whole paper (register allocation by one weighted bipartite matching per control step, with weights from the interconnect, then unit allocation)
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 6, Resource Sharing and Binding (register sharing and interconnect)
---

Weighted bipartite matching binding is a register binder of [high-level synthesis](/high-level-synthesis/), published by Huang, Chen, Lin and Hsu in 1990. It walks through the control steps in order. At each step, the values that start their lifetime there form one side of a [bipartite graph](/bipartite-graph/), the registers that are free form the other side, and an edge weight counts the wires that a value would share with a register. A largest-weight matching, found as an [assignment problem](/assignment-problem/), places the values. For straight-line code it always uses the fewest registers, the largest number of values live in one step, like the [left-edge algorithm](/left-edge-algorithm/), but it chooses among the free registers to save multiplexer inputs. Each step is optimal for that step. The whole binding is not always the one with the least interconnect.

## In plain words

Registers are boxes, and each box has wires to the units that fill it and to the unit inputs that read it. Every extra wire needs a switch. We go through time from left to right. Whenever new results appear, we see which boxes are empty at that moment and put each new result in a box. A result prefers a box that is already wired to the unit that makes it and to the inputs that will read it, since then no new wire is needed. Many results arrive at once, so we solve a small matching puzzle each time: give each new result a different empty box so that the total of reused wires is largest.

## The problem

The input is a set $X$ of $n$ values of a scheduled design of straight-line code, as on the [register binding](/register-binding/) page. Each value $x$ is held in the steps $\ell(x)$, a set of consecutive steps from $b(x)$ to $e(x)$. It is written by one unit $\mathrm{src}(x)$, and it is read by a set $\mathrm{Dst}(x)$ of unit input ports. A binding $\rho$ puts each value in a register, with no two values of one register live in the same step. A register $r$ has the sources $\mathrm{Src}(r) = \{\mathrm{src}(x) : \rho(x) = r\}$ and the destinations $\mathrm{Dst}(r) = \bigcup_{\rho(x) = r} \mathrm{Dst}(x)$. The cost is the number of connections,
$$\mathrm{cost}(\rho) = \sum_r \bigl(|\mathrm{Src}(r)| + |\mathrm{Dst}(r)|\bigr),$$
a stand-in for the multiplexer inputs in front of the registers and the ports. The goal is the fewest registers, and among those, a small cost.

## The algorithm

```pseudo id=main
MATCHING-BIND(X)
L1  R ← no registers; each register r will have Src(r), Dst(r) and end(r), the last step of its last value
L2  for each step t, in increasing order, such that some value has b(x) = t do
L3      A ← the values x with b(x) = t
L4      F ← the registers r with end(r) < t
L5      add max(0, |A| − |F|) fresh registers to R and to F, with empty Src, empty Dst and end = −∞
L6      for each x ∈ A and r ∈ F do w(x, r) ← [src(x) ∈ Src(r)] + |Dst(x) ∩ Dst(r)|
L7      M ← a matching that covers A, with each x matched to a distinct r ∈ F, of largest total weight w
L8      for each (x, r) ∈ M do ρ(x) ← r; add src(x) to Src(r); add Dst(x) to Dst(r); end(r) ← e(x)
L9  return ρ
```

Line L6 counts the connections that $x$ needs and $r$ already has. Line L7 is an assignment problem with $|A|$ rows and $|F| \ge |A|$ columns, solved by the [Hungarian algorithm](/hungarian-algorithm/). Line L5 adds fresh registers only when the free ones are too few.

## Example

Two units $U_0$ and $U_1$ write values, and three unit input ports $p_0$, $p_1$ and $p_2$ read them. Four values:

| value | steps held | written by | read by |
|---|---|---|---|
| $a$ | $\{1\}$ | $U_0$ | $p_0, p_2$ |
| $b$ | $\{2\}$ | $U_1$ | $p_2$ |
| $c$ | $\{2, 3, 4\}$ | $U_0$ | $p_0, p_1$ |
| $d$ | $\{3\}$ | $U_0$ | $p_0, p_1$ |

At most two values are live in one step, so two registers are needed.

- **Step 1.** $A = \{a\}$ and no register is free, so L5 makes $R_0$ and $a$ goes there. Now $\mathrm{Src}(R_0) = \{U_0\}$ and $\mathrm{Dst}(R_0) = \{p_0, p_2\}$.
- **Step 2.** $A = \{b, c\}$. $R_0$ is free, and L5 adds $R_1$. The weights are $w(b, R_0) = 0 + 1 = 1$, $w(c, R_0) = 1 + 1 = 2$ and $0$ for $R_1$. Placing $c$ in $R_0$ has weight 2, placing $b$ there has weight 1, so $c$ goes to $R_0$ and $b$ to $R_1$.
- **Step 3.** $A = \{d\}$. $R_0$ holds $c$ until step 4, so only $R_1$ is free, and $d$ goes there.

The binding is $R_0 = \{a, c\}$ with 1 source and 3 ports, and $R_1 = \{b, d\}$ with 2 sources and 3 ports: cost 9. The binding $\{a, b, d\}$, $\{c\}$ costs $(2 + 3) + (1 + 2) = 8$. At step 2, $c$ looked like the better match for $R_0$, but it kept $R_0$ busy at step 3, when $d$, which reads the same ports, needed a register. So each step was optimal for itself, and the whole binding was not.

## Correctness

What is proved, in the [full proof](proofs/correctness.md):

- **Valid.** A value enters a register only when the register's last value has ended, so no two values of one register are live in a common step.
- **Fewest registers.** The number of registers is exactly the largest number of values live in one step, which is the least possible. Fresh registers appear at step $t$ only when every register holds a value live at $t$.
- **Each step is optimal for its step.** Given the bindings of the earlier steps, the connections added at step $t$ equal $\sum_{x \in A} (1 + |\mathrm{Dst}(x)|) - w(M)$. So a matching of largest weight adds the fewest connections at that step.

What is not proved, and is false: that the total cost is least. The example above is an instance where it costs 9 and 8 is possible. In a measured run of the tests, on 500 random instances with at most 6 values, 2 units and 3 ports, the binder matched the exhaustive optimum on 479, was 1 above on 16 and 2 above on 5. This is a measurement on small random instances, not a bound.

## Complexity

Sorting the values by their first step takes $O(n \log n)$. The free registers number at most $L$, since only $L$ registers exist. At step $t$ with $a_t$ new values, L6 computes $a_t \cdot L$ weights, each in $O(D)$ time with bit sets or hash sets, and the Hungarian method takes $O(a_t^2 L)$ time. Since $a_t \le L$ and $\sum_t a_t = n$, the total is $O(n \log n + n L^2 + n L D)$. The space is $O(n)$ for the binding, $O(L^2)$ for one weight matrix and $O(L D)$ for the sets of the registers.

## Properties

- **Not exact for the interconnect.** It reaches the fewest registers, but not always the least cost, as the example shows.
- **Deterministic.** With a fixed tie rule in the matching, the same input gives the same binding.
- **Greedy over time.** Each step looks only at the registers and connections built so far, never at later values.
- **Polynomial.** Each step is one assignment problem, so it scales to large designs, unlike exact integer programs.

## Variants and improvements

- **Other weights.** The weights can count the multiplexer inputs saved, include the wire lengths of a floorplan, or add a term for switching activity. The weights of the original paper also come from the interconnect between registers and units, and the count of shared connections used here is one simple form of them.
- **Unit binding by matching.** The same idea binds operations to functional units, step by step, with weights from shared operand sources.
- **Joint register and port choice.** Later binders choose the operand ports of commutative operations together with the registers, see [interconnect binding](/interconnect-binding/).
- **Unweighted version.** With all weights 0, any matching works and the binder becomes [interval partitioning](/interval-partitioning/), which also reaches the fewest registers. The maximum matching can then come from [Hopcroft-Karp](/hopcroft-karp/), though any free register will do.

## When to use it

Use it for register binding of straight-line code, or of loop bodies after unrolling, when the interconnect matters and the register count must stay least. If only the register count matters, the [left-edge algorithm](/left-edge-algorithm/) is simpler. If the conflict graph is not an interval graph, for example with mutually exclusive values, the step-by-step order no longer gives the fewest registers, and a general method such as [Tseng-Siewiorek clique partitioning](/tseng-siewiorek-clique-partitioning/) or an integer program applies.

## Pitfalls

- **Expecting the least interconnect.** Each step is optimal only for itself. Later values can make an early choice bad.
- **Off-by-one in freeing.** A register is free at step $t$ only if its last value ends before $t$. With the timing rules of the [resource compatibility graph](/resource-compatibility-graph/) page, a register read in step $t - 1$ can be written at the end of step $t - 1$ and hold a value from step $t$.
- **Rectangular matching.** The matching must cover the new values, not the registers. A solver that expects a square matrix needs dummy rows with weight 0.
- **Early steps have no guidance.** At the first steps the registers are empty and every weight is 0, so the first choices are arbitrary.

## Implementations

## History

Kurdahi and Parker (1987) bound registers in straight-line code with the left-edge algorithm, which reaches the fewest registers but ignores interconnect. Huang, Chen, Lin and Hsu (1990) kept the step-by-step order and replaced the arbitrary choice among the free registers by a weighted bipartite matching, so that the register count stays least while the interconnect falls. They also bound functional units by matching. Later work added port choices and multiplexer costs for FPGA targets.

## References
