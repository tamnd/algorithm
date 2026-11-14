---
tag: AB69M9
kind: algorithm
slug: lagrangian-relaxation-gate-sizing
name: Lagrangian relaxation gate sizing
aliases:
- Chen-Chu-Wong sizing
- LR gate sizing
area: eda/timing-and-verification
level: advanced
summary: Chen, Chu and Wong's sizing that moves the timing constraints into the objective with multipliers that obey flow conservation, and solves each subproblem by local resizing.
solves: [gate-sizing]
model: real-ram
complexity:
  vars: {n: the number of gates, m: the number of connections, S: the number of local resizing sweeps in a round}
  time: {per_round: O(S (n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, iterative: true, exact: true}
history:
  year: 1998
  people: [Chung-Ping Chen, Chris C. N. Chu, D. F. Wong]
  note: Chen, Chu and Wong presented the method at ICCAD 1998, and the journal version appeared in IEEE Transactions on Computer-Aided Design in 1999.
prereqs: [lagrangian-relaxation, static-timing-analysis, elmore-delay]
see_also: [gate-sizing, tilos, geometric-programming, lagrangian-duality, kkt-conditions, flow-conservation, coordinate-descent, subgradient]
sources:
  - paper: "Chung-Ping Chen, Chris C. N. Chu and D. F. Wong, Fast and exact simultaneous gate and wire sizing by Lagrangian relaxation, IEEE Transactions on Computer-Aided Design 18(7), 1014 to 1025, 1999"
    locator: the flow conservation of the optimal multipliers, the local resizing subproblem and its greedy solution, and the optimality of the method under the Elmore delay
  - paper: "Chung-Ping Chen, Chris C. N. Chu and D. F. Wong, Fast and exact simultaneous gate and wire sizing by Lagrangian relaxation, Proceedings of ICCAD 1998, 617 to 624"
    locator: the conference version
  - paper: doi:10.1287/opre.1050.0254
    title: Stephen Boyd, Seung-Jean Kim, Dinesh D. Patil and Mark A. Horowitz, Digital circuit optimization via geometric programming, Operations Research 53(6), 2005
    locator: gate sizing as a geometric program and its solution by convex optimization
---

Lagrangian relaxation gate sizing is an exact method for the continuous form of [gate sizing](/gate-sizing/) under the Elmore delay. It puts a multiplier on every edge of the timing graph and moves the timing constraints into the objective. The optimality conditions force the multipliers to obey flow conservation, which removes the arrival times from the problem. What remains, for fixed multipliers, is a weighted sum of area and gate delays that one pass of closed-form updates, gate by gate, minimizes. An outer loop adjusts the multipliers until the target is met with least area. Chen, Chu and Wong gave the method in 1998 for gates and wires together.

## In plain words

Each connection in the circuit gets a price, which says how much a delay on that connection costs. The prices follow a rule like water in pipes: the total price that flows into a gate also flows out of it, and the total reaching the outputs says how hard the target is.

With prices fixed, the problem is easy: make the sum of the area and the priced delays small. A gate that sits on expensive connections becomes larger, and a gate that loads expensive gates stays small. A short formula gives the best size of one gate when the others are fixed, and a few passes over the gates settle all sizes.

Then the circuit is timed. Prices go up where the circuit is late and down on connections with spare time. The loop repeats until the prices stop changing.

## The problem

The circuit and the delay model are those of [TILOS](/tilos/): gate $i$ has delay $D_i(x) = p_i + (r_i / x_i)(f_i + \sum_{j \in \mathrm{out}(i)} c_j x_j)$ and area $a_i x_i$, but its size $x_i$ is now continuous in an interval $[\ell_i, h_i]$. The timing graph has a source $s$ before the gates without fanins and a sink $t$ after the gates without fanouts, and $E$ is its edge set. With arrival times $A_i$ as variables, the problem is
$$ \min \sum_i a_i x_i \quad \text{subject to} \quad A_u + D_v(x) \le A_v \text{ for each edge } (u, v) \text{ with } v \ne t, \qquad A_u \le T \text{ for each edge } (u, t), $$
with $A_s = 0$ and $\ell \le x \le h$. Each $D_v$ is a posynomial, so this is a [geometric program](/geometric-programming/).

With a multiplier $\mu_e \ge 0$ on each edge, the [Lagrangian relaxation](/lagrangian-relaxation/) has a finite minimum over the arrival times only if, at every gate, the flow of multipliers in equals the flow out ([flow conservation](/flow-conservation/)). Then it becomes
$$ \sum_i a_i x_i + \sum_i \lambda_i D_i(x) - T \sum_{(u, t) \in E} \mu_{ut}, \qquad \lambda_i = \sum_{e \text{ into } i} \mu_e . $$
Minimizing the first two terms over the sizes is the *local resizing subproblem*.

## The algorithm

```pseudo id=main
LR-SIZING(circuit, target T, rounds R)
L1  μ ← 1 on the edges into t, then make μ conserve flow at every gate
L2  repeat R times
L3      λ_i ← the sum of μ over the edges into gate i, for every gate i
L4      repeat until no size moves: for each gate i, x_i ← clamp of √(λ_i r_i (f_i + Σ_{j∈out(i)} c_j x_j) / (a_i + c_i Σ_{k∈in(i)} λ_k r_k / x_k)) into [ℓ_i, h_i]
L5      A ← the arrival times for x, by static timing analysis
L6      for each edge e = (u, v): μ_e ← μ_e · (A_u + D_v) / A_v, or μ_e ← μ_e · A_u / T if v = t
L7      from the outputs back to the inputs, scale the multipliers into each gate so that they sum to the flow out of it
L8  return x
```

Line L4 is the local resizing. The formula of a gate follows from the terms of the subproblem that contain $x_i$: its area, its own priced delay, which falls as $1/x_i$, and the priced delays of its fanins, which grow with its input capacitance. Line L6 lowers the multiplier of every edge that is not critical, since there $A_u + D_v < A_v$, and raises or lowers the flow into the sink by how late or early each output is. Chen, Chu and Wong update the multipliers by a [subgradient](/subgradient/) step with step sizes that go to zero; the implementation uses the multiplicative rule of line L6, which keeps every multiplier positive. Line L7 is the projection back onto flow conservation.

## Example

Take a fixed driver of size 1 and a chain of two gates with sizes in $[1, 16]$, all $p_i = r_i = c_i = a_i = 1$, a load $f_2 = 16$ at the output and the target $T = 12$. The delay is $(1 + x_1) + (1 + x_2 / x_1) + (1 + 16 / x_2)$, which is 21 at the smallest sizes. On a chain, flow conservation makes every multiplier equal to one number $\mu$, and the local resizing is
$$ x_1 = \sqrt{\frac{\mu\, x_2}{1 + \mu}}, \qquad x_2 = \sqrt{\frac{16 \mu}{1 + \mu / x_1}} . $$

| round | $\mu$ used | $x_1$ | $x_2$ | delay | area |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1.2173 | 2.9638 | 12.0505 | 5.1811 |
| 2 | 1.0042 | 1.2196 | 2.9684 | 12.0436 | 5.1880 |
| 10 | 1.0241 | 1.2294 | 2.9889 | 12.0137 | 5.2183 |
| 50 | 1.0317 | 1.2339 | 2.9984 | 12.0000 | 5.2324 |

In round 1 the circuit is 0.05 late, so the multiplier grows by the factor $12.0505 / 12$, and each round moves the sizes toward the target. The method settles at $\mu \approx 1.0318$, $x_1 \approx 1.234$ and $x_2 \approx 2.998$, with area 5.2324 and delay 12. A search over a refined grid of both sizes gives the same least area to four digits. The stage ratios are $x_1 / 1 \approx 1.23$, $x_2 / x_1 \approx 2.43$ and $16 / x_2 \approx 5.34$. The fastest sizing of [logical effort](/logical-effort/) would make all three equal to $16^{1/3} \approx 2.52$; here the early gates stay small because area costs and the target leaves room.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The coefficient of each arrival time in the Lagrangian is the flow out of its gate minus the flow in, so the dual function is finite only on flow-conserving multipliers, and there the arrival times drop out. For every such $\mu$, the dual value is at most the least area ([weak duality](/lagrangian-duality/)). For fixed multipliers, the subproblem as a function of one size is $\alpha x_i + \beta / x_i$, minimized at $\sqrt{\beta/\alpha}$ clamped to the interval. After the change of variables $x_i = e^{y_i}$ the subproblem is strictly convex, so a point where no single size can improve is its unique minimum. The whole problem is convex in $(y, A)$, so when the target can be beaten strictly there is no duality gap: the best multipliers exist, conserve flow, and their subproblem solution is the optimal sizing. This is what makes the method exact. The convergence of the multiplier update of line L6 is not proved here; the tests measure it.

## Complexity

A sweep of line L4 costs $O(n + m)$, since each gate needs its load and the priced resistance of its fanins. Timing, the update and the projection also cost $O(n + m)$ each. A round with $S$ sweeps costs $O(S (n + m))$, and the space is $O(n + m)$ for the multipliers. The number of rounds depends on the step rule and the accuracy and has no closed-form bound. On the small circuits of the tests, 3000 rounds reach a relative error below $10^{-3}$; this is measured, not proved.

## Properties

- Exact for continuous sizes under the Elmore delay: the optimal multipliers give the optimal sizing, with no duality gap (proved).
- Every flow-conserving set of multipliers gives a lower bound on the least area, so the gap between the bound and a feasible sizing certifies how close it is (proved).
- The local resizing works on one gate at a time, so it scales to large circuits without a general convex solver.
- At the optimum, the multiplier of an edge whose timing constraint is not tight is zero (complementary slackness), and the flow into a gate is the price of its delay.
- Discrete library sizes are not handled. The continuous answer must be rounded, which can break the target or add area.

## Variants and improvements

- **Wire sizing.** The original method sizes gates and wire segments together. Each wire segment is a node of the RC interconnect tree with its own width, and its local formula has the same form.
- **Multiplier updates.** The subgradient step of Chen, Chu and Wong, $\mu_e \leftarrow \max(0, \mu_e + \rho_k (A_u + D_v - A_v))$ with $\rho_k \to 0$, and multiplicative rules like line L6 are both used; they differ in speed and in how they handle multipliers near zero.
- **General convex solvers.** The same geometric program can be solved by interior point methods, as Boyd, Kim, Patil and Horowitz describe for digital circuits. These are robust but slower on very large circuits.
- **Discrete sizes and other delay models.** With library cells and table delays, the relaxed problem is no longer convex. The relaxation with multipliers is then used as a heuristic: the local resizing picks the best library cell for each gate under the current prices.

## When to use it

Use it to size gates, or gates and wires, of a large circuit to a delay target with least area or power, when the Elmore delay or another posynomial model is acceptable and a provable lower bound is wanted. It is much faster than a general geometric programming solver on large circuits. For a quick sizing with discrete cells, [TILOS](/tilos/) is simpler. For sizing with buffers on long wires, combine it with [van Ginneken buffer insertion](/van-ginneken-buffer-insertion/).

## Pitfalls

- The multipliers must conserve flow before the subproblem is solved. Without it the arrival times do not drop out and the subproblem is not the dual.
- With an additive step, the multiplier of an edge can reach zero early. The proportional projection of line L7 keeps it at zero while another edge into the same gate carries flow, and a critical edge gets a step of zero, so the edge cannot regain its price if it becomes critical later. The multiplicative rule of line L6 keeps every multiplier positive.
- The step sizes decide the speed. With steps $\rho_k = \rho_0 / k$, a poor $\rho_0$ can leave the sizing far from the target after many rounds.
- A gate with $\lambda_i = 0$ goes to its smallest size. That is right only if none of its paths is critical.
- The sizing at a given round can miss the target slightly. Check the timing of the final sizing, and use the dual bound to judge how far it is from optimal.
- Optimality holds for the continuous problem. After rounding to library sizes, the result is no longer optimal, and the discrete problem is strongly NP-hard.

## Implementations

## History

Fishburn and Dunlop observed in 1985 that under the Elmore model the sizing problem is posynomial, and Sapatnekar, Rao, Vaidya and Kang solved transistor sizing exactly by convex optimization in 1993. Chung-Ping Chen, Chris Chu and D. F. Wong presented Lagrangian relaxation for simultaneous gate and wire sizing at ICCAD 1998 and in IEEE Transactions on Computer-Aided Design in 1999. Their observation that the optimal multipliers conserve flow made the relaxed problem simple enough for very large circuits. Later work on sizing with library cells kept the multipliers and the local resizing, and changed the update of the multipliers.

## References
