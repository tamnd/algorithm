---
tag: ZN9QN5
kind: technique
slug: logical-effort
name: Logical effort
aliases:
- Sutherland-Sproull logical effort
area: cad/timing-and-verification
level: core
summary: Sutherland and Sproull's delay model d = gh + p for a gate, which shows that a path is fastest when every stage bears the same effort.
prereqs: [boolean-circuit, timing-graph]
see_also: [gate-sizing, nonlinear-delay-model, static-timing-analysis, geometric-programming, tilos, elmore-delay, van-ginneken-buffer-insertion]
sources:
  - paper: "Ivan E. Sutherland and Robert F. Sproull, Logical effort: designing for speed on the back of an envelope, Proceedings of the 1991 UC Santa Cruz Conference on Advanced Research in VLSI, MIT Press, 1 to 16, 1991"
    locator: the delay model d = gh + p, the logical efforts of simple gates and the rule of equal stage effort
  - book: isbn:9781558605572
    title: Ivan Sutherland, Bob Sproull and David Harris, Logical Effort, Designing Fast CMOS Circuits, Morgan Kaufmann, 1999
    locator: Chapter 1, the method of logical effort (path effort, branching effort, the minimum delay and the best number of stages)
---

Logical effort is a method to estimate and to minimize the delay of a path of CMOS gates by hand. It was introduced by Sutherland and Sproull (1991) and is the subject of the book by Sutherland, Sproull and Harris (1999). Each gate has delay $d = g h + p$ in units of a technology constant $\tau$: $g$ is the *logical effort* of the gate type, $h$ is the *electrical effort*, the ratio of its load to its input capacitance, and $p$ is its *parasitic delay*. For a path, the product of the stage efforts is fixed by the gate types, the branching and the end loads. The AM-GM inequality then shows that the delay is smallest when every stage has the same effort, and it gives the minimum delay $N F^{1/N} + P$ and the best number of stages in closed form.

## In plain words

A gate has to charge the input capacitance of the gates it drives. A big gate drives a big load fast but is itself a big load for the gate before it. Logical effort puts a number on each part of this trade.

Each gate type has a fixed cost factor, its logical effort: an inverter has 1, a two-input NAND has 4/3. The work a stage does is its logical effort times its fanout ratio. Over a whole path, the product of these works is fixed. A product with a fixed value has its smallest sum when all factors are equal, so the fastest path gives every stage the same work. This gives the gate sizes, the path delay and the right number of stages from a few multiplications.

## When it applies

- **A path of static CMOS gates** whose delay is mainly the charging of gate capacitance through transistors, and where the gates can be sized freely, as in custom design or in a library with many sizes.
- **Early design.** It compares circuit topologies, such as NAND against NOR forms or 2 against 4 stages, before any layout exists.
- **Fixed end conditions.** The input capacitance of the path and its output load are given, and the off-path loads are known as ratios (branching efforts).
- **Not for sign-off timing.** The model ignores the input slew, the wire resistance and the difference between rising and falling edges. A [nonlinear delay model](/nonlinear-delay-model/) and [static timing analysis](/static-timing-analysis/) give the timing of the final design.
- **Not for whole circuits directly.** The closed form is for one path. A network with reconvergent paths and fixed wire loads leads to a [gate sizing](/gate-sizing/) problem, which is a [geometric program](/geometric-programming/) in the same model.

## The template

The model, in units of $\tau$, with input capacitances measured relative to the inverter:

- *Logical effort* $g$: the input capacitance of the gate divided by that of an inverter that gives the same output current. With PMOS transistors twice as wide as NMOS ones, $g = 1$ for an inverter, $g = (n + 2)/3$ for an $n$-input NAND and $g = (2n + 1)/3$ for an $n$-input NOR, so $4/3$ and $5/3$ for two inputs.
- *Electrical effort* $h = C_{\text{out}} / C_{\text{in}}$ of the stage.
- *Parasitic delay* $p$: about $p_{\text{inv}} \approx 1$ for an inverter and $n \, p_{\text{inv}}$ for an $n$-input NAND or NOR.
- *Stage effort* $f = g h$, and stage delay $d = f + p$.

For a path of $N$ stages from input capacitance $C_{\text{in}}$ to load $C_{\text{out}}$:

- path logical effort $G = \prod g_i$, path electrical effort $H = C_{\text{out}} / C_{\text{in}}$,
- branching effort $b_i = (C_{\text{on-path}} + C_{\text{off-path}}) / C_{\text{on-path}}$ at the output of stage $i$, and $B = \prod b_i$,
- path effort $F = G B H$ and parasitic delay $P = \sum p_i$.

```pseudo id=main
LOGICAL-EFFORT-DESIGN(path, C_in, C_out)
L1  for each stage i of the path: g_i ← ⟨logical effort of its gate type⟩;  p_i ← ⟨parasitic delay⟩
L2  for each stage i: b_i ← ⟨branching effort at its output⟩
L3  F ← (∏ g_i) · (∏ b_i) · C_out / C_in;   P ← ∑ p_i
L4  N ← ⟨number of stages⟩: about log_4 F; add or remove inverters to reach it    ▷ see below
L5  f̂ ← F^(1/N)                                                                 ▷ the same effort at every stage
L6  D̂ ← N · f̂ + P                                                                ▷ the minimum path delay
L7  C ← C_out
L8  for i ← N down to 1
L9      C ← g_i · b_i · C / f̂                                                     ▷ input capacitance of stage i
L10     size gate i for input capacitance C;  ⟨round to an available size⟩
L11 return the sizes and D̂
```

The loop ends with $C = C_{\text{in}}$, because the product of the factors $g_i b_i / \hat f$ is $G B / F = 1 / H$. This is a check on the arithmetic.

**Why equal efforts are best (line L5).** The stage efforts satisfy $\prod f_i = \prod g_i h_i = G B H = F$, because each $h_i$ is $b_i$ times the ratio of the next on-path input to this input, and these ratios multiply to $H$. The path delay is $D = \sum f_i + P$, and $P$ does not depend on the sizes. By the inequality of arithmetic and geometric means, $\sum_{i=1}^N f_i \ge N (\prod f_i)^{1/N} = N F^{1/N}$, with equality if and only if all $f_i$ are equal. Every choice of efforts with product $F$ comes from sizes (line L9 builds them), so the minimum delay is $\hat D = N F^{1/N} + P$. $\square$

**The best number of stages (line L4).** Adding $k$ inverters to a path changes neither $G$ nor $B$ nor $H$, but adds $k \, p_{\text{inv}}$ to $P$. Treat $N$ as a real number and write $\rho = F^{1/N}$, so $N = \ln F / \ln \rho$. The part of the delay that changes is $N (\rho + p_{\text{inv}}) = \ln F \cdot (\rho + p_{\text{inv}}) / \ln \rho$. Its derivative in $\rho$ is zero when
$$ \rho \, (\ln \rho - 1) = p_{\text{inv}}. $$
The solution is $\rho = e \approx 2.718$ for $p_{\text{inv}} = 0$, $\rho \approx 3.59$ for $p_{\text{inv}} = 1$ and $\rho \approx 4.32$ for $p_{\text{inv}} = 2$. The minimum is flat: with $p_{\text{inv}} = 1$, a stage effort of 4 costs 0.4 percent more delay than 3.59, and any value from 2.4 to 6 costs less than 9 percent more. That is why the rule of thumb is a stage effort of about 4, and $N \approx \log_4 F$.

**Example.** A path of three NAND2 gates has input capacitance 1 and drives a load of 27, with no branching. Then $G = (4/3)^3 = 64/27$, $H = 27$, $F = 64$ and $P = 3 \cdot 2 = 6$. With $N = 3$, $\hat f = 4$ and $\hat D = 3 \cdot 4 + 6 = 18$. Line L9 gives the input capacitances from the output back: $(4/3) \cdot 27 / 4 = 9$, then $(4/3) \cdot 9 / 4 = 3$, then $(4/3) \cdot 3 / 4 = 1 = C_{\text{in}}$, as the check says. If all three gates had input capacitance 1, the stage efforts would be $4/3$, $4/3$ and $(4/3) \cdot 27 = 36$, and the delay $116/3 + 6 = 134/3 \approx 44.7$. The best real number of stages is $\ln 64 / \ln 3.59 \approx 3.25$. With one more inverter the delay is $4 \cdot 64^{1/4} + 7 \approx 18.3$, so three stages are best here.

## Classic examples

- **A chain of inverters driving a large load.** Here $G = B = 1$ and $F = H$, so the chain has about $\log_4 H$ stages, each about 4 times larger than the one before. Without parasitic delay, the best ratio is $e$, the classic result for tapered buffers.
- **NAND against NOR.** A NOR2 has $g = 5/3$ and a NAND2 has $g = 4/3$, because series PMOS transistors must be wider. So designs prefer NAND forms, and the method says by how much.
- **Decoders and multiplexers.** The method chooses between one wide gate and a tree of small gates, and finds where to put inverters, from $F$ and the rule $N \approx \log_4 F$.
- **Forks.** A signal and its complement must arrive at the same time; the method sizes the two legs of a fork for equal delay.

## Variations

- **Asymmetric gates.** Inputs of one gate can have different logical efforts when the transistors for a critical input are made larger.
- **Unequal rising and falling delays.** Separate logical efforts for the two edges, or skewed gates that favor one edge.
- **Interconnect.** A fixed wire capacitance breaks the product form, because it does not scale with the gate sizes. The delay is still a posynomial in the sizes, so the exact minimum is a [geometric program](/geometric-programming/), and heuristics such as [TILOS](/tilos/) apply.
- **Other circuit families.** Domino and pseudo-NMOS gates have their own logical efforts and parasitic delays.
- **Calibration.** $\tau$, $p_{\text{inv}}$ and the logical efforts of a technology are fitted to circuit simulations of the real gates.

## Pitfalls

- **Treating the model as exact.** It is linear in the load and ignores the input slew. Its numbers are estimates, good for comparing designs, not for sign-off.
- **Forgetting branching.** Off-path loads multiply the path effort. If a path has $B = 3$ and is designed as if $B = 1$, its real path effort is 3 times the planned one, and the stages next to the branches are much slower than planned.
- **Equal sizes instead of equal efforts.** Equal efforts mean a geometric growth of the sizes along the path, not equal gates, as the example shows.
- **Too many or too few stages.** A stage effort far from 4, such as 10 or 1.5, wastes delay. Adding inverters can make a path faster, but an added inverter also inverts the logic.
- **Rounding.** Library cells come in a few sizes. Rounding each size changes the efforts, and the minimum is flat, so small rounding errors cost little.

## Exercises

1. Show that the logical effort of an $n$-input NOR gate is $(2n + 1)/3$ when PMOS transistors are twice as wide as NMOS transistors of the same strength.
2. Redo the example with a load of 216 instead of 27. Find $F$, the best number of stages with inverters added at the end, and the minimum delay.
3. Show that for $p_{\text{inv}} > 0$ the equation $\rho (\ln \rho - 1) = p_{\text{inv}}$ has exactly one solution with $\rho > e$, and that it gives the minimum of $(\rho + p_{\text{inv}}) / \ln \rho$.

## References
