---
tag: NQSKAE
kind: definition
slug: robust-path-delay-test
name: Robust path delay test
aliases:
- robust test
area: eda/test-and-diagnosis
level: advanced
summary: A two-pattern path delay test that detects the fault whatever the delays of other paths; a non-robust test needs the off-path inputs to be fault-free.
prereqs: [path-delay-fault-model]
see_also: [transition-fault-model, static-timing-analysis, false-path, ternary-simulation, launch-on-capture-and-launch-on-shift, automatic-test-pattern-generation, fault-coverage, timing-graph]
sources:
  - paper: "C. J. Lin and S. M. Reddy, On delay fault testing in logic circuits, IEEE Transactions on Computer-Aided Design CAD-6(5), 694 to 703, 1987"
    title: C. J. Lin and S. M. Reddy, On delay fault testing in logic circuits, IEEE Transactions on Computer-Aided Design CAD-6(5), 694 to 703, September 1987
    locator: the robust and non-robust tests of path delay faults, the conditions on the off-path inputs, and test generation for them
  - paper: "G. L. Smith, Model for delay faults based upon paths, Proceedings of the International Test Conference, 342 to 349, 1985"
    title: G. L. Smith, Model for delay faults based upon paths, Proceedings of the International Test Conference, 342 to 349, 1985
    locator: the path delay fault model and tests that hold whatever the delays of the other gates
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Delay Test (robust and non-robust sensitization, with the conditions for each gate input)
---

A robust path delay test is a pair of vectors that detects a [path delay fault](/path-delay-fault-model/) whatever the delays of the lines off the path. If the path is too slow, the output captured at the clock edge is wrong, even when other paths are slow too. A weaker class, the non-robust tests, detects the fault only when the lines off the path are on time. The difference is in the conditions on the off-path inputs of the gates along the path, and it depends on the direction of the transition at each gate.

## Definition

Let $P = (x_0, x_1, \ldots, x_k)$ be a path of a combinational circuit, with a transition at $x_0$, and let $(v_1, v_2)$ be a pair of vectors. For each gate $x_{i+1}$ on the path, $x_i$ is the on-path input and the others are the off-path inputs. For AND and NAND the controlling value is $c = 0$, and for OR and NOR it is $c = 1$; the other value is non-controlling. A line is **steady** at a value if it holds that value under $v_1$, under $v_2$, and at every moment in between, for every choice of gate delays. Sufficient conditions are easy to check: an input with the same value in both vectors is steady, a gate with a steady input at its controlling value is steady, and a gate whose inputs are all steady is steady.

The pair is a **non-robust test** of the fault if $x_0(v_1) \ne x_0(v_2)$ in the direction of the fault and, under $v_2$, every off-path input of every gate on the path has the non-controlling value of its gate. Under $v_2$ alone the path is then sensitized: changing $x_i$ changes $x_{i+1}$. XOR and XNOR gates have no controlling value and put no condition on $v_2$.

The pair is a **robust test** if it is a non-robust test and in addition, at each gate where the on-path input changes from the non-controlling to the controlling value, every off-path input is steady at the non-controlling value. Where the on-path input changes from the controlling to the non-controlling value, the condition on $v_2$ is enough. At an XOR or XNOR gate, every off-path input must be steady.

| on-path input | off-path inputs, robust test | off-path inputs, non-robust test |
|---|---|---|
| controlling to non-controlling | non-controlling under $v_2$ | non-controlling under $v_2$ |
| non-controlling to controlling | steady non-controlling | non-controlling under $v_2$ |

**Proposition.** Assume each gate input pin has a fixed positive delay, so that a gate output at time $t$ is the gate function of each input at $t$ minus the delay of its pin, and the circuit is settled under $v_1$ before $v_2$ is applied at time 0. Let $d(P)$ be the sum of the pin delays along $P$. Under a robust test, $x_k(t) = x_k(v_1) \ne x_k(v_2)$ for all $t < d(P)$, whatever the delays of all pins off the path. So if $d(P)$ exceeds the capture time, the captured value is wrong and the fault is detected.

*Proof.* Let $T_i$ be the sum of the pin delays along $P$ up to $x_i$, so $T_0 = 0$ and $T_k = d(P)$. We show by induction on $i$ that $x_i(v_1) \ne x_i(v_2)$ and $x_i(t) = x_i(v_1)$ for all $t < T_i$. For $i = 0$, this holds since $x_0$ changes at time 0. Let it hold for $x_i$, and let $\delta$ be the delay of the on-path pin of $x_{i+1}$, so $T_{i+1} = T_i + \delta$. Take $t < T_{i+1}$, so $t - \delta < T_i$ and the on-path input at time $t - \delta$ has its old value $x_i(v_1)$.

If $x_i(v_1) = c$, the gate output at time $t$ is its controlled value, which is $x_{i+1}(v_1)$, whatever the off-path inputs do. Under $v_2$, the on-path input is not $c$ and the off-path inputs are not $c$, so $x_{i+1}(v_2)$ is the other value.

If $x_i(v_1)$ is non-controlling, then $x_i(v_2) = c$, and the off-path inputs are steady non-controlling, so at time $t$ minus their pin delays they are still non-controlling. All inputs seen at time $t$ are non-controlling, so the output is the non-controlled value, which is $x_{i+1}(v_1)$. Under $v_2$ the on-path input is $c$, so $x_{i+1}(v_2)$ is the controlled value.

For a buffer, an inverter, a fanout branch, and XOR or XNOR with steady off-path inputs, the output is a one-to-one function of the on-path input at time $t - \delta$, so both claims carry over. $\square$

The first case uses nothing about the off-path inputs before $v_2$: while the on-path input holds the controlling value, it alone fixes the output. The second case needs them steady, since an off-path input that passes through $c$ late could hold the output at the right final value by itself. This is why the rule depends on the direction.

## Examples and non-examples

**A robust test.** In $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, take the path $a\,g\,z$ with $a$ rising, and the pair $v_1 = 010$, $v_2 = 110$ on $abc$. At $g$, the input $a$ changes from 0, controlling for NAND, to 1, so the off-path input $b_g$ needs only the value 1 under $v_2$. At $z$, the input $g$ falls from 1 to 0, from non-controlling to controlling, so the off-path input $h$ must be steady at 1. It is, since $c$ is steady at 0, the controlling value of $h$. The pair is robust.

**A non-robust test that is not robust.** Take $z = \mathrm{AND}(x, y)$ and the path $x\,z$ with $x$ falling. The pair $v_1 = 10$, $v_2 = 01$ on $xy$ is a non-robust test: $y = 1$ under $v_2$. In the good circuit, both changes arrive before the capture and $z$ ends at 0. If $x$ is slow and $y$ is on time, $z$ rises with $y$ and falls only when $x$ arrives, so at the capture $z = 1$, which is wrong, and the slow path is found. If $y$ is slow too, $z$ stays 0 until the capture, the expected value, and the slow path passes. The pair $v_1 = 11$, $v_2 = 01$ keeps $y$ steady at 1 and is a robust test.

**Non-example: a launch without sensitization.** For the same AND gate, the pair 10, 00 launches the fall at $x$, but $y = 0$ under $v_2$ holds $z$ at 0 whatever $x$ does. It is not a test of the path.

**Non-example: a stuck-at test.** A single vector that detects $x_i/0$ with the path sensitized is not a delay test, since nothing changes. A delay test always needs two vectors.

**Paths with no robust test.** A path can have a non-robust test and no robust one, when every pair that sensitizes it lets some off-path input change at a gate where the on-path input goes to the controlling value. A path can also have no test at all, as for a [false path](/false-path/). The robust coverage of a path list is then below 100% even for a perfect test set.

## Related definitions

- **Path delay fault.** A path with a rising or falling transition at its start whose delay exceeds the clock period. See [path delay fault model](/path-delay-fault-model/).
- **Static sensitization.** Under a single vector, the off-path inputs of every gate of a path are non-controlling. A non-robust test is a launch at $x_0$ with a statically sensitized path under $v_2$.
- **Steady values and hazards.** The condition "steady" is checked by simulating the pair in a multi-valued algebra with values for steady 0, steady 1, rising, falling and possibly glitching, as in [ternary simulation](/ternary-simulation/), where an unknown value stands for a possible hazard.
- **Validatable non-robust test.** A non-robust test whose off-path inputs that can be late are themselves checked by robust tests in the same test set, so that the set together detects the fault.
- **Transition fault.** A gross delay at one line. A test of the [transition fault model](/transition-fault-model/) needs the launch and a stuck-at test under $v_2$ but no condition on paths.

## References
