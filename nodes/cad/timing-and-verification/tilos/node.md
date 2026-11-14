---
tag: Q10RHR
kind: algorithm
slug: tilos
name: TILOS
aliases:
- Fishburn-Dunlop sizing
- TILOS sizing
area: cad/timing-and-verification
level: advanced
summary: Fishburn and Dunlop's transistor sizing that, on the Elmore model where delay is a posynomial, enlarges the device with the best delay gain on the critical path.
solves: [gate-sizing]
model: real-ram
complexity:
  vars: {n: the number of gates, m: the number of connections, K: the total number of size steps over all gates}
  time: {worst: O(K (n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, greedy: true, exact: false}
history:
  year: 1985
  people: [John P. Fishburn, Alfred E. Dunlop]
  note: Fishburn and Dunlop presented TILOS at ICCAD 1985, as a posynomial approach to transistor sizing.
prereqs: [static-timing-analysis, elmore-delay, greedy-algorithm]
see_also: [gate-sizing, lagrangian-relaxation-gate-sizing, geometric-programming, logical-effort, arrival-and-required-time, hill-climbing, van-ginneken-buffer-insertion, timing-graph]
sources:
  - paper: "John P. Fishburn and Alfred E. Dunlop, TILOS: a posynomial programming approach to transistor sizing, Proceedings of the IEEE International Conference on Computer-Aided Design (ICCAD), 326 to 328, 1985"
    locator: the posynomial form of the Elmore delay and the greedy bumping of the transistor with the best sensitivity on the critical path
  - paper: "Sachin S. Sapatnekar, Vasant B. Rao, Pravin M. Vaidya and Sung-Mo Kang, An exact solution to the transistor sizing problem for CMOS circuits using convex optimization, IEEE Transactions on Computer-Aided Design 12(11), 1621 to 1634, 1993"
    locator: the convex formulation of the same problem and the measured comparison with TILOS
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 2011
    locator: Chapter 8, Timing Closure, Section 8.5.1, Gate Sizing
---

TILOS is a greedy method for [gate sizing](/gate-sizing/): it starts with every device at its smallest size, and while the circuit is too slow it makes one device on the critical path one step larger, the one that gives the largest decrease of the path delay per unit of added area. Fishburn and Dunlop gave it in 1985 for transistor sizing, under an Elmore delay model in which every delay is a posynomial in the sizes. The output always meets the target when the method succeeds, but it is a heuristic: the area is not the least in general, and the method can fail when a solution exists.

## In plain words

A circuit is too slow. Larger gates drive their loads faster, but they cost area, and they also load the gates in front of them, which then get slower.

TILOS starts with every gate as small as it can be. It finds the slowest path through the circuit, since only that path decides the delay. For each gate on that path it asks: if this gate were one size larger, how much faster would the path get, and how much area would that cost? It makes the best one larger. Then it measures the circuit again, because the slowest path may now be a different one.

It stops when the circuit is fast enough. If no step on the slowest path makes it faster, it gives up. It never makes a gate smaller again.

## The problem

The circuit is a DAG of gates in topological order, and gate $i$ has a size $x_i$ from an increasing list $\mathcal S_i$. With the notation of [static timing analysis](/static-timing-analysis/), the delay of gate $i$ is the [Elmore delay](/elmore-delay/) of a switch-level RC model,
$$ D_i(x) = p_i + \frac{r_i}{x_i} \Big( f_i + \sum_{j \in \mathrm{out}(i)} c_j x_j \Big), $$
where $p_i$ is the intrinsic delay, $r_i / x_i$ the drive resistance, $c_j x_j$ the input capacitance of a fanout gate and $f_i$ the fixed load of wires and outputs. The arrival time of a gate is the latest arrival time of its fanins plus its own delay, and the circuit delay $\Delta(x)$ is the latest arrival time. Given a target $T$, find sizes with $\Delta(x) \le T$ and least area $\sum_i a_i x_i$. TILOS sizes one device per step, transistor or gate; the page uses gates, as the implementation does.

## The algorithm

```pseudo id=main
TILOS(circuit, size lists, target T)
L1  x ← the smallest size of every gate
    repeat
L2      if Δ(x) ≤ T then return x
L3      P ← a critical path, traced back from the latest arrival
L4      for each gate g on P that is below its largest size do
L5          G_g ← the decrease of the delay of P if g moves one size up
L6      g* ← the gate with G_g > 0 and the largest G_g / (area added)
L7      if there is no such gate then return failure
L8      move g* one size up
```

The gain in line L5 is local. A larger $x_g$ lowers $D_g$ and raises the delay of each fanin of $g$, through its input capacitance, and changes no other delay. So the gain is the change of $D_g$ plus the change of the delays of the fanins of $g$ that are on $P$. Fishburn and Dunlop sized transistors and multiplied a size by a fixed bump factor in each step; a list of library sizes is the discrete form of the same rule.

## Example

Take a chain of four gates $0 \to 1 \to 2 \to 3$ with all $p_i = c_i = 1$, resistances $r = (3, 1, 2, 3)$, areas $a = (2, 1, 3, 1)$ and a load $f_3 = 12$ at the output. Gate 0 is a fixed driver of size 1, the other gates have the sizes $\{1, 2, 3, 4\}$, and the target is $T = 24$.

| step | sizes $x_1, x_2, x_3$ | delay | area | gains $G_1$, $G_2$, $G_3$ | move |
| --- | --- | --- | --- | --- | --- |
| 0 | 1, 1, 1 | 46 | 7 | $-5/2$, 0, 16 | gate 3 |
| 1 | 1, 1, 2 | 30 | 8 | $-5/2$, 1, 4 | gate 3 |
| 2 | 1, 1, 3 | 26 | 9 | $-5/2$, 2, 1 | gate 3 |
| 3 | 1, 1, 4 | 25 | 10 | $-5/2$, 3, at the top | gate 2 |
| 4 | 1, 2, 4 | 22 | 13 | | done |

In step 2 the ratios are $2/3$ for gate 2 (area 3 per step) and $1$ for gate 3, so gate 3 grows again. Gate 1 never helps: a larger gate 1 loads the weak driver more than it gains. TILOS ends with area 13 and delay 22. Enumeration of all 64 sizings gives the least area 12, at sizes $(1, 2, 3)$ with delay $4 + 3 + 4 + 13 = 24$. TILOS cannot reach it, because it would have to make gate 3 smaller after gate 2 grows.

TILOS can also fail when a sizing exists. Take the same chain with $r = (1, 3, 3, 1)$, all areas 1, $f_3 = 6$ and $T = 16$. The smallest sizes give delay 17. TILOS makes gate 1 larger (gain $1/2$) and reaches delay $33/2$; then no single step on the path has a positive gain, and it stops. The sizes $(2, 2, 2)$ give delay $3 + 4 + 4 + 4 = 15$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The path traced back from the latest arrival through the fanin that sets each arrival time has a delay equal to the circuit delay. Every move takes the next size in a list, so the sizes stay legal, and the method returns sizes only after it checks $\Delta(x) \le T$; so a returned sizing always meets the target, and if no sizing does, TILOS fails. Each move raises one position in one list, so the loop ends after at most $K$ moves. Each $D_i$ is a posynomial in the sizes, so the continuous problem is a [geometric program](/geometric-programming/) and every local minimum is global. TILOS does not find that minimum: the example shows that it can end with more area than the discrete optimum.

## Complexity

Each round does one timing pass in $O(n + m)$, traces the path in $O(n)$, and computes all the local gains on the path in $O(n + m)$ in total. There are at most $K = \sum_i (|\mathcal S_i| - 1)$ rounds, so the time is $O(K (n + m))$ and the extra space is $O(n + m)$. With a bump factor $\beta$ on continuous sizes, the number of rounds is at most the sum over the gates of $\log_\beta$ of the ratio of the largest to the smallest size.

## Properties

- Sound: when it returns a sizing, the sizing meets the target (proved).
- Monotone: sizes only grow and the area strictly grows in each round.
- Not optimal and not complete: it can use more area than the optimum, and it can fail on targets that some sizing meets (shown by examples). Its area is at least the optimum, as for any feasible sizing.
- It only looks at one critical path at a time. When many paths are near critical, it can spend area on gates that help only one of them.
- Its quality is measured, not proved. Sapatnekar, Rao, Vaidya and Kang measured the gap between TILOS and the exact convex optimum on their test circuits.

## Variants and improvements

- **Continuous bumping.** The original multiplies a size by a factor slightly above 1 in each step, which approximates the continuous problem.
- **Area recovery.** A second pass that tries to make gates smaller while the target still holds removes some of the overshoot shown in the example.
- **Exact continuous sizing.** Since the delay is a posynomial, the continuous problem can be solved to optimality, as a geometric program by convex optimization, or by [Lagrangian relaxation gate sizing](/lagrangian-relaxation-gate-sizing/). A TILOS result is often used as the start point for these methods or for a rounding step.
- **Other delay models.** The greedy loop works with any delay model that gives the gain of a single move, for example a table model. The posynomial argument then no longer holds.

## When to use it

Use it as a fast first sizing of a circuit that misses its target by a moderate amount, when the sizes come from a small library and an optimal answer is not needed. It is simple to add to a timing engine, because it needs only the critical path and a local delay change. When area or power matters a lot, follow it with area recovery, or use an exact continuous method and round the result.

## Pitfalls

- A gain that counts only the delay of the resized gate is wrong. A larger gate loads its fanins, and that change often cancels the gain, as gate 1 in the example shows.
- An earlier gate on the critical path can also be a direct fanin of the resized gate, not only its predecessor on the path. Its delay changes too.
- The critical path must be found again after each move; the old path may no longer be the longest.
- Failure does not mean that no sizing meets the target. Check the target against the delay with a better method before you report that it cannot be met.
- The sizes never go down, so the result depends on the start. Starting from larger sizes can give a different answer.

## Implementations

## History

John Fishburn and Alfred Dunlop of AT&T Bell Laboratories presented TILOS at ICCAD 1985. They noted that under the Elmore model of a switch-level RC circuit the delay is a posynomial in the transistor sizes, so the continuous sizing problem has no local minimum that is not global, and they gave the greedy bumping rule as a fast way to a good solution. In 1993 Sapatnekar, Rao, Vaidya and Kang solved the same problem exactly by convex optimization and compared the results with TILOS. In 1999 Chen, Chu and Wong solved the gate and wire sizing form exactly by Lagrangian relaxation.

## References
