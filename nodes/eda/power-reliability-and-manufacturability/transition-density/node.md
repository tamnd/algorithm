---
tag: G6GC4V
kind: algorithm
slug: transition-density
name: Transition density
aliases:
- Najm transition density
area: eda/power-reliability-and-manufacturability
level: core
summary: Najm's measure of average transitions per second and its propagation through gates by Boolean difference probabilities, giving power without simulation vectors.
model: word-ram
complexity:
  vars: {G: the number of gates, P: the number of gate input pins, K: the largest fanin of a gate, n: the number of primary inputs}
  time: {worst: "O(G + P K)"}
  space: {extra: "O(G + n)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1991
  people: [Farid N. Najm]
  note: Najm defined the transition density of a logic signal as its average number of transitions per unit time, proved the Boolean difference formula for independent inputs, and propagated densities through a gate-level circuit.
prereqs: [signal-probability-propagation, switching-activity]
see_also: [glitch-power, bdd-switching-activity-estimation, monte-carlo-power-estimation, cofactor, shannon-expansion, inertial-and-transport-delay, stationary-process, dynamic-power-dissipation]
sources:
  - paper: "Farid N. Najm, Transition density: a new measure of activity in digital circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 12(2), 310 to 323, February 1993"
    title: Farid N. Najm, Transition density, a new measure of activity in digital circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 12(2), 310 to 323, February 1993
    locator: the definition of the transition density and equilibrium probability, the theorem that gives the density at the output of a Boolean module with independent inputs, and the propagation algorithm
  - paper: "Farid N. Najm, Transition density, a stochastic measure of activity in digital circuits, 28th ACM/IEEE Design Automation Conference, 644 to 649, 1991"
    title: Farid N. Najm, Transition density, a stochastic measure of activity in digital circuits, Proceedings of the 28th ACM/IEEE Design Automation Conference, 644 to 649, June 1991
    locator: the first presentation of the measure and of its propagation
  - paper: doi:10.1109/92.335013
    title: Farid N. Najm, A survey of power estimation techniques in VLSI circuits, IEEE Transactions on VLSI Systems 2(4), 446 to 455, December 1994
    locator: the section on probabilistic techniques, which compares transition density with signal probability and BDD methods
  - paper: "Farid N. Najm, Low-pass filter for computing the transition density in digital circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 13(9), 1123 to 1131, September 1994"
    title: Farid N. Najm, Low-pass filter for computing the transition density in digital circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 13(9), 1123 to 1131, September 1994
    locator: the filtering of short pulses by gates with inertial delay
---

The transition density $D(x)$ of a logic signal $x$ is its average number of transitions per unit time. Najm (1991, 1993) showed that for a gate or block $y = f(x_1, \ldots, x_n)$ with independent inputs,

$$ D(y) \;=\; \sum_{i=1}^{n} P\!\left(\frac{\partial y}{\partial x_i}\right) D(x_i), $$

where $\partial y / \partial x_i$ is the Boolean difference of $y$ with respect to $x_i$. The algorithm applies this rule gate by gate in topological order, with the [signal probabilities](/signal-probability-propagation/) of the gate inputs, and so turns input statistics into a density at every node in one pass, without input vectors or simulation. The [dynamic power](/dynamic-power-dissipation/) of a node is then $\frac{1}{2} C V_{DD}^2 D(y)$. The result is exact on circuits without reconvergent fanout when no two inputs switch at the same instant. With reconvergent fanout it is an approximation, and with inputs that switch together at a clock edge it counts glitches that a zero-delay view does not see.

## In plain words

Each input wire turns on and off at random, a known number of times per second, and the inputs act independently. The question is how often each wire inside the circuit switches.

When one input of a gate switches, the output switches only if the other inputs let the change through. An AND gate passes a change on one input only when its other inputs are on. So the output switches as often as each input switches, times the chance that the gate passes that input, summed over the inputs.

Going through the gates from the inputs to the outputs gives a switching rate for every wire. Multiply each rate by the energy of one switch and you have the power, with no simulation at all.

## The problem

The input is a combinational circuit $C$ with primary inputs $x_1, \ldots, x_n$ and gates in topological order, and for each input $x_i$ two numbers: its *equilibrium probability* $p_i = P(x_i = 1)$, the fraction of time it is 1, and its *transition density* $d_i$, its mean number of transitions per unit time. The model treats each input as a random 0-1 signal $x_i(t)$ in continuous time. The signals are mutually independent and [stationary](/stationary-process/), with a finite number of transitions in each finite interval. For a node $y$ with $N_y(T)$ transitions in $[0, T]$,

$$ D(y) \;=\; \lim_{T \to \infty} \frac{E[N_y(T)]}{T}. $$

The output is $P(y)$ and $D(y)$ for every node $y$.

For a Boolean function $f$ of $x_1, \ldots, x_n$, the **Boolean difference** of $f$ with respect to $x_i$ is

$$ \frac{\partial f}{\partial x_i} \;=\; f|_{x_i = 1} \oplus f|_{x_i = 0}, $$

the XOR of the two [cofactors](/cofactor/) of $f$. It does not depend on $x_i$, and it is 1 at exactly those values of the other variables for which a change of $x_i$ changes $f$. In test it is the condition for the effect of a fault on $x_i$ to reach the output. For a single gate it is simple: $\partial\, \mathrm{AND}(z_1, \ldots, z_k) / \partial z_j$ is the AND of the other inputs, the derivative of OR is the AND of the complements of the other inputs, and the derivative of XOR, BUF or NOT is 1. Complementing $f$ does not change $\partial f / \partial x_i$, so NAND, NOR and XNOR have the same derivatives as AND, OR and XOR.

## The algorithm

```pseudo id=main
TRANSITION-DENSITY(C, p, d)
L1  for each primary input x_i do P[x_i] ← p_i; D[x_i] ← d_i
L2  for each gate y = kind(z_1, …, z_k) in topological order do
L3      P[y] ← the signal probability of kind with input probabilities P[z_1], …, P[z_k]
L4      D[y] ← 0
L5      for j ← 1 to k do
L6          b ← P(∂y/∂z_j): ∏_{l≠j} P[z_l] for AND and NAND, ∏_{l≠j} (1 − P[z_l]) for OR and NOR, 1 for XOR, XNOR, BUF and NOT
L7          D[y] ← D[y] + b · D[z_j]
L8  return P, D
```

Line L3 is the numeric mode of [signal probability propagation](/signal-probability-propagation/). Line L6 computes the probability of the Boolean difference of the gate under the assumption that its inputs are independent, from the probabilities found at line L3 for the earlier gates.

## Example

**A fanout-free circuit.** Take $u = \mathrm{AND}(a, b)$ and $y = \mathrm{OR}(u, c)$, with densities in transitions per nanosecond.

| node | $P$ | $D$ |
|---|---|---|
| $a$ | $1/2$ | $2$ |
| $b$ | $1/4$ | $1$ |
| $c$ | $1/2$ | $4$ |
| $u$ | $1/2 \cdot 1/4 = 1/8$ | $P(b) D(a) + P(a) D(b) = 1/2 + 1/2 = 1$ |
| $y$ | $1 - (7/8)(1/2) = 9/16$ | $(1 - P(c)) D(u) + (1 - P(u)) D(c) = 1/2 + 7/2 = 4$ |

Each node drives one pin, so these values are exact under the model. A change on $c$ passes the OR gate whenever $u = 0$, which is 7/8 of the time, so $y$ inherits most of the activity of $c$. If $y$ drives 10 fF at 1 V, its power is $\frac{1}{2} \cdot 10^{-14} \cdot 1^2 \cdot 4 \cdot 10^9 = 20$ µW.

**A reconvergent circuit.** Take $u = \mathrm{AND}(a, b)$, $v = \mathrm{AND}(a, c)$ and $y = \mathrm{OR}(u, v)$, all inputs with $P = 1/2$ and $D = 1$. The algorithm gives $D(u) = D(v) = 1$ and $D(y) = \frac{3}{4} \cdot 1 + \frac{3}{4} \cdot 1 = 3/2$. The rule applied to the whole function $y = a(b \lor c)$ gives the true value: $\partial y / \partial a = b \lor c$, $\partial y / \partial b = a \bar c$ and $\partial y / \partial c = a \bar b$, so

$$ D(y) = \tfrac{3}{4} \cdot 1 + \tfrac{1}{4} \cdot 1 + \tfrac{1}{4} \cdot 1 = \tfrac{5}{4}. $$

The gate-by-gate value is 20 percent too high, because $u$ and $v$ both depend on $a$ and the gate rule at $y$ treats them as independent.

## Correctness

The proof has two parts, both in the [full proof](proofs/correctness.md).

**The rule for one block.** Suppose the inputs of $y = f(x_1, \ldots, x_n)$ are independent stationary signals, no two of them switch at the same instant, and $y$ follows $f$ with zero delay or with a fixed delay. Then $y$ changes only at a transition of some $x_i$, and at such an instant it changes exactly when $\partial f / \partial x_i = 1$ at the values of the other inputs. The other inputs are independent of the transition times of $x_i$ and stationary, so the expected count of the transitions of $x_i$ that pass is $P(\partial f / \partial x_i)$ times the expected count of the transitions of $x_i$. Summing over $i$ gives the formula. A fixed delay moves the transitions in time but does not change their number.

**The pass over the gates.** When the input pins of every gate have disjoint supports, as in a fanout-free circuit, the inputs of each gate are functions of disjoint groups of independent primary input signals. So they are independent stationary signals, with no common transition instants, and the rule for one block holds at each gate. The probabilities of line L3 are exact under the same condition. By induction in topological order every $P[y]$ and $D[y]$ is exact. Under reconvergent fanout the independence of the gate inputs fails, and the example above shows that the result can then be wrong.

## Complexity

A gate with $k$ inputs costs $O(k)$ at line L3 and $O(k)$ for each of its $k$ pins at line L6, so the pass costs $O(G + P K)$ arithmetic operations. With prefix and suffix products of $P[z_l]$ and $1 - P[z_l]$, line L6 costs $O(1)$ per pin and the pass costs $O(G + P)$. The space is one probability and one density per node, $O(G + n)$. This is the same cost as one zero-delay [logic simulation](/logic-simulation/) of one vector, while a simulation-based estimate needs many vectors.

Applying the rule to whole functions in place of gates is exact on every circuit with independent inputs, but it needs $P(\partial y / \partial x_i)$ for every node and input. That is a signal probability, which is #P-hard in general. With [BDDs](/reduced-ordered-bdd/) it costs time linear in the size of the BDD of $\partial y / \partial x_i$, which can be exponential in $n$.

## Properties

- **What it measures.** $D(y)$ counts all transitions, rising and falling, including glitches. The dynamic power of a node with load $C$ is $\frac{1}{2} C V_{DD}^2 D(y)$, because a full charge and discharge, two transitions, costs $C V_{DD}^2$.
- **Continuous time.** The density is a rate per unit time, not per clock cycle. For a synchronous circuit with clock frequency $f$, the [switching activity](/switching-activity/) per cycle is $D(y) / f$ if the assumptions hold.
- **Linear in the input densities.** For fixed probabilities, every $D[y]$ is a linear function of the input densities with nonnegative coefficients. So the share of each input in the activity of a node is explicit, and doubling all input densities doubles all node densities.
- **Delay does not enter.** The algorithm uses no gate delays. In the model a delay shifts the transitions of a signal but does not change their number.
- **Glitches through a gate.** When the inputs of a gate switch at different times, each passing input transition is counted, so the density includes the glitches that come from skew between independent inputs.

## Variants and improvements

- **Blocks in place of gates.** Najm's program, DENSIM, applies the rule to groups of gates, computing the Boolean difference probabilities of each block with BDDs. Larger blocks absorb local reconvergence, at a cost that grows with the block size.
- **Low-pass filtering.** A real gate with inertial delay does not pass a pulse shorter than its delay (see [inertial and transport delay](/inertial-and-transport-delay/)). Najm (1994) modified the rule to filter such pulses, which lowers the overestimate on deep logic.
- **Correlation coefficients.** Add pairwise correlation terms between gate inputs to correct part of the error from reconvergent fanout. This is a heuristic without a general bound.
- **Exact zero-delay activity.** If the question is the activity per clock cycle with zero delay, compute $P(y(t) \ne y(t+1))$ symbolically, as in [BDD-based switching activity estimation](/bdd-switching-activity-estimation/).
- **Statistical estimates.** [Monte Carlo power estimation](/monte-carlo-power-estimation/) simulates the circuit with a real delay model and stops at a stated accuracy, at a much higher cost per node.

## When to use it

Use transition density for fast, vectorless activity estimates on large gate-level netlists, for example to find the most active nets early, to compare design options, or to give an activity number to every net when no simulation testbench exists. It suits circuits with mostly independent inputs and limited reconvergence. When a number must be accurate within a known error, use simulation with a stopping rule, and use the density result as a starting point or a sanity check.

## Pitfalls

- **Simultaneous switching.** The rule assumes that two inputs never switch at the same instant. In a synchronous circuit all register outputs switch near the clock edge. For an AND gate with fresh random inputs each cycle ($P = 1/2$, $D = 1/2$ per cycle), the rule gives $1/2$ transition per cycle, while the zero-delay output changes only in $3/8$ of the cycles. If one input arrives a little later, the true count with that delay is again $1/2$: the difference is the glitch that the skew creates.
- **Reconvergent fanout.** The gate inputs then depend on each other and the result can be too high or too low. For $y = \mathrm{AND}(a, \mathrm{NOT}(a))$ the rule gives $D(y) = D(a)$, while the output is 0 with zero delay. With a delay on the inverter, each rising edge of $a$ makes a pulse of two transitions, so $D(a)$ is right for that delay model and wrong for a fast inverter that filters the pulse.
- **Correlated inputs.** Inputs from a counter, a shift register or the same bus are not independent, and the result can be far off.
- **Densities are not probabilities.** $D$ is a rate with a unit, not a number between 0 and 1. Mixing per-cycle and per-second values is a common unit error.
- **Glitches that do not exist.** In deep logic the rule passes every short pulse, while real gates filter many of them, so the estimate tends to be too high there.

## Implementations

## History

Najm introduced the transition density at the Design Automation Conference in 1991 and gave the full treatment in IEEE Transactions on CAD in 1993. He modeled logic signals as stationary random processes, proved the Boolean difference formula for a module with independent inputs, and propagated densities through a circuit by blocks whose Boolean differences were computed with BDDs. In 1994 he added a low-pass filter for gates with inertial delay, and his survey of power estimation in the same year placed the method next to simulation, signal probability and BDD-based methods.

## References
