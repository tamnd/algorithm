---
tag: STT7KY
kind: algorithm
slug: clustered-voltage-scaling
name: Clustered voltage scaling
aliases:
- CVS
- Usami-Horowitz voltage scaling
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Usami and Horowitz's method that moves gates with slack to a low supply, growing clusters back from the outputs so that level converters are needed only at the registers.
model: word-ram
complexity:
  vars: {n: the number of gates, m: the number of gate input pins}
  time: {worst: "O(n (n + m))"}
  space: {extra: "O(n + m)"}
properties: {deterministic: true, exact: false, greedy: true, recursive: false}
history:
  year: 1995
  people: [Kimiyoshi Usami, Mark Horowitz]
  note: Usami and Horowitz gave the method at the International Symposium on Low Power Design in 1995. Usami and coworkers at Toshiba applied it, with automated tools, to a media processor and reported it in the IEEE Journal of Solid-State Circuits in 1998.
prereqs: [dynamic-power-dissipation, static-timing-analysis, topological-sort]
see_also: [speed-scaling, gate-sizing, tilos, multi-threshold-voltage-assignment, leakage-power, power-gating, dag-longest-path, greedy-algorithm]
sources:
  - paper: doi:10.1145/224081.224083
    title: Kimiyoshi Usami and Mark Horowitz, Clustered voltage scaling technique for low-power design, Proceedings of the International Symposium on Low Power Design, 3 to 8, 1995
    locator: the two supplies, the rule that a low gate drives only low gates, the backward search from the outputs, and the level-converting flip-flops
  - paper: "Kimiyoshi Usami, Mototsugu Igarashi, Fujio Minami, Takashi Ishikawa, Masahiro Kanazawa, Makoto Ichida and Kazutaka Nogami, Automated low-power technique exploiting multiple supply voltages applied to a media processor, IEEE Journal of Solid-State Circuits 33(3), 1998"
    title: Kimiyoshi Usami, Mototsugu Igarashi, Fujio Minami, Takashi Ishikawa, Masahiro Kanazawa, Makoto Ichida and Kazutaka Nogami, Automated low-power technique exploiting multiple supply voltages applied to a media processor, IEEE Journal of Solid-State Circuits 33(3), March 1998
    locator: the automated flow with two supplies on a media processor, with the level-converting flip-flop and the layout of the two supply rails
  - paper: doi:10.1109/4.52187
    title: Takayasu Sakurai and A. Richard Newton, Alpha-power law MOSFET model and its applications to CMOS inverter delay and other formulas, IEEE Journal of Solid-State Circuits 25(2), 584 to 594, April 1990
    locator: the drain current model with the fitted exponent alpha and the inverter delay that follows from it
---

Clustered voltage scaling (CVS) is a method to lower the [dynamic power](/dynamic-power-dissipation/) of a synchronous circuit with two supply voltages, a high one $V_H$ and a low one $V_L$. Since $P = \alpha C V^2 f$, a gate moved to $V_L$ spends $(V_L/V_H)^2$ of its old switching power, but it is slower. CVS moves gates that have timing slack to $V_L$. It keeps the rule that a low gate never drives a high gate, because a high gate driven by a low signal can draw static current. So the low gates form clusters at the ends of the paths, next to the registers, and only the registers need level converters. The method visits the gates from the outputs back to the inputs, tries each gate whose fanouts are all low, and keeps it low when the circuit still meets the clock period. Usami and Horowitz gave it in 1995. Under a simple additive delay model this page proves that the greedy result is the largest legal set and so is optimal. With real delay models it is a heuristic.

## In plain words

A chip can have two supply rails, one at a high voltage and one at a low voltage. Gates on the low rail use much less energy per switch, but they are slower. Many gates are not on the slowest paths, so they can afford to be slower.

There is a catch. When a low-voltage gate drives a high-voltage gate, the high gate does not switch off fully and wastes current. So the low gates must sit at the ends of the paths, where they feed the registers, and the registers convert the level back.

CVS starts at the registers at the end of the logic and walks back. It tries to move each gate to the low rail when all the gates it drives are already low. If the circuit is still fast enough, the gate stays low.

## The problem

**Circuit.** The logic between registers is a DAG of $n$ gates with $m$ gate input pins. The primary inputs come from registers clocked at time 0 at $V_H$. A set $O$ of gates drive registers. Each gate $g$ has a switched capacitance $C_g$, an activity $\alpha_g$, a delay $d_H(g)$ at $V_H$ and a delay $d_L(g) \ge d_H(g)$ at $V_L$. A register driven by a low gate is a level-converting register and adds a delay $\ell_c \ge 0$.

**Delay model.** This page uses an additive model in which the delay of a gate depends only on its own supply. For a set $L$ of low gates, the arrival time is $a(g) = \max_{f} a(f) + d(g)$ over the fanins $f$ of $g$, with $a = 0$ at the primary inputs and $d(g) = d_L(g)$ if $g \in L$ and $d_H(g)$ otherwise. The circuit meets the clock period $T$ when $a(o) + \ell_c [o \in L] \le T$ for every $o \in O$. This is the timing of [static timing analysis](/static-timing-analysis/) with fixed gate delays, a [longest path](/dag-longest-path/) in the DAG.

**Legality.** A set $L$ is legal when no gate of $L$ drives a gate outside $L$.

**Goal.** Find a legal set $L$ that meets $T$ and has the largest saving $\sum_{g \in L} \alpha_g C_g (V_H^2 - V_L^2) f$.

**Physical numbers.** How much slower a low gate is follows the alpha-power law of Sakurai and Newton (1990): the delay of a gate is about proportional to $C V / (V - V_T)^{a}$. The threshold $V_T$ and the exponent $a$ are fitted to the transistors of a process. The exponent is near 2 for long channels and between 1 and 1.5 for short channels. The capacitances $C_g$ come from extraction, and the activities $\alpha_g$ from [switching activity](/switching-activity/) estimation. The level converter delay $\ell_c$ is a characterized cell value.

## The algorithm

```pseudo id=main
CVS(circuit, T, ℓc)
L1  L ← ∅; if the circuit misses T with every gate high then fail
L2  for each gate g in reverse topological order do
L3      if every gate driven by g is in L then
L4          L ← L ∪ {g}
L5          if some output o has a(o) + ℓc [o ∈ L] > T then
L6              L ← L − {g}
L7  return L
```

Line L2 visits each gate after all the gates that it drives. Line L3 keeps the set legal. Line L5 is a full timing check, or an incremental one that updates the arrival times in the fanout cone of $g$.

## Example

Take $V_H = 1.8$ V, $V_L = 1.2$ V, $V_T = 0.4$ V and $a = 1.3$. The alpha-power law gives a delay ratio of $\frac{1.2 / 0.8^{1.3}}{1.8 / 1.4^{1.3}} \approx 1.38$. For $a = 1$ the ratio would be 1.17, and for $a = 2$ it would be 2.04, which shows how much the fitted exponent matters. The power ratio is $(1.2/1.8)^2 = 0.444$, so each low gate saves 56% of its switching power.

For a check by hand, the circuit below uses whole numbers for the delays. The inputs $a$ and $b$ come from registers. The gate $g_1$ is driven by $a$, $g_2$ by $g_1$, $g_3$ by $b$, $g_4$ by $g_2$ and $g_3$, and $g_5$ by $g_3$. The outputs are $g_4$ and $g_5$. The level converter adds $\ell_c = 1$, and $T = 8$.

| gate | $d_H$ | $d_L$ | $C_g$ |
|---|---|---|---|
| $g_1$ | 2 | 3 | 2 |
| $g_2$ | 2 | 3 | 2 |
| $g_3$ | 1 | 2 | 3 |
| $g_4$ | 2 | 3 | 2 |
| $g_5$ | 1 | 2 | 1 |

With every gate high, the longest path $a, g_1, g_2, g_4$ takes 6, so line L1 passes. The reverse topological order is $g_5, g_4, g_3, g_2, g_1$.

| gate | line L3 | worst output time with $g$ low | result |
|---|---|---|---|
| $g_5$ | an output, no gate fanout | $\max(6, 1 + 2 + 1) = 6$ | low |
| $g_4$ | an output, no gate fanout | $2 + 2 + 3 + 1 = 8$ | low |
| $g_3$ | $g_4$ and $g_5$ are low | $\max(8, 2 + 3 + 1, 2 + 2 + 1) = 8$ | low |
| $g_2$ | $g_4$ is low | $2 + 3 + 3 + 1 = 9 > 8$ | back to high |
| $g_1$ | $g_2$ is high | not tried | high |

The result is $L = \{g_3, g_4, g_5\}$ with switched capacitance 6 of 10. If all gates have the same activity, the switching power falls from 10 units to $4 + 6 \cdot 0.444 = 6.67$, a saving of 33%, before the cost of the converters. A search over all 32 subsets confirms that no legal set that meets $T$ saves more.

## Correctness

Two invariants hold after each pass of lines L2 to L6: $L$ is legal, since line L4 adds a gate only when all of its gate fanouts are in $L$ already, and $L$ meets $T$, since line L6 undoes any addition that breaks it. So the result is legal and meets $T$. It is also maximal: a gate that line L6 removed would still miss $T$ if added to the final set, because adding low gates never makes a path faster.

Under the additive model more is true, and the [proof file](proofs/correctness.md) gives the details. In a legal set, the low gates on any path form a suffix of it, so the delay of a path under $L_1 \cup L_2$ equals its delay under $L_1$ or under $L_2$. Hence the legal sets that meet $T$ are closed under union, and there is a largest one. The greedy returns exactly this largest set, so it is optimal for every choice of the nonnegative weights $\alpha_g C_g$, and the order among gates with no path between them does not matter.

**Why the rule.** A static CMOS gate on $V_H$ whose input is driven high by a gate on $V_L$ sees the gate voltage $V_L$ at its PMOS transistor, whose source is at $V_H$. The PMOS then has $V_{GS} = V_L - V_H$, and it conducts when $V_H - V_L > |V_{Tp}|$, while the NMOS also conducts. The current flows from $V_H$ to ground as long as the input stays high. In the example $V_H - V_L = 0.6$ V is more than a threshold of 0.4 V. A level-converting register restores the full swing with a cross-coupled pair of PMOS transistors.

## Complexity

Line L5 runs once per gate. A full timing pass costs $O(n + m)$, so the total is $O(n (n + m))$ time, with $O(n + m)$ space for the arrival times and the fanout lists. Incremental timing updates only the fanout cone of the new gate, which is often small, but the worst case stays the same.

## Properties

- **Legal and timed, proved.** The result never has a low gate driving a high gate, and it meets $T$.
- **Optimal under the additive model, proved here.** The result contains every legal set that meets $T$, so it is the most power saving one for any nonnegative weights. This proof is not in the paper of Usami and Horowitz.
- **A heuristic under real delay models.** With delays that depend on the load and on the input slope, a low driver slows the gates it drives, and the union property can fail. Then the result depends on the order and can be worse than the best legal set.
- **Measured savings.** The power savings reported by Usami and Horowitz (1995) and by Usami and coworkers (1998) are measured on their circuits, not proved. They also depend on how much slack the circuit has, which is a property of the design.
- **Converters only at registers.** Since a low cluster ends at the registers, the only level converters are in the registers, which keeps the cost of the converters small.

## Variants and improvements

- **Level converters inside the logic.** Later work allows a converter on any edge from a low gate to a high gate, at a cost in delay, area and power. Then more gates can go low, but the choice becomes a harder search, and the legal sets are no longer closed under union.
- **Gate sizing at the same time.** A gate that misses timing at $V_L$ can be made faster by a larger size, as in [gate sizing](/gate-sizing/) and [TILOS](/tilos/). Joint methods trade the two moves against each other.
- **Threshold voltage as a third choice.** The same structure of a choice per gate under a timing bound appears in [multiple threshold voltage assignment](/multi-threshold-voltage-assignment/), which lowers [leakage](/leakage-power/) instead of switching power. Flows often run both.
- **Voltage per block and per time.** Coarser schemes give a whole block one supply, which needs fewer converters and simpler rails. [Speed scaling](/speed-scaling/) changes the supply and the clock over time instead of over gates.

## When to use it

Use it on synchronous logic with much slack off the critical paths, when the process and the library offer two supplies and level-converting registers. The gain is large when many gates feed the registers through short paths, as in datapaths with a few long paths. It gives little on a circuit in which most paths are near critical, and it needs a placement that can reach both supply rails.

## Pitfalls

- **Breaking the rule at a fanout stem.** A gate that drives both a low gate and a high gate cannot go low. Line L3 checks all gate fanouts, not only the one on the critical path.
- **Forgetting the converter delay.** A low output adds $\ell_c$ at the register. Without it, the timing check passes and the chip fails.
- **Trusting the fixed-delay model.** In a real library, a slower low driver also slows its fanout gates through the input slope. Rerun full timing with the real model on the result.
- **Hold time.** Low gates are slower, which helps hold time, but the converter registers have their own setup and hold times. Check [setup and hold](/setup-and-hold-constraints/) on every converter register.
- **Counting the saving in the wrong units.** The saving per gate is $\alpha_g C_g (V_H^2 - V_L^2) f$ with $\alpha_g$ the rising transitions per cycle, as on the [dynamic power](/dynamic-power-dissipation/) page. Leakage changes too, since it falls with the supply, but it is a separate term.

## Implementations

## History

Chandrakasan, Sheng and Brodersen (1992) showed that the supply voltage is the strongest lever on CMOS power, because power falls with its square while delay grows more slowly. Usami and Horowitz (1995) applied this inside one circuit, with a second supply for the gates that have slack, and with the rule that clusters of low gates end at registers. Usami and coworkers at Toshiba (1998) built an automated flow around it for a media processor, and later work allowed converters inside the logic and combined the supply choice with sizing and with the threshold voltage.

## References
