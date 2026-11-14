---
tag: HYGZ61
kind: algorithm
slug: symbolic-simulation
name: Symbolic simulation
aliases:
- COSMOS symbolic simulation
area: eda/hardware-verification
level: core
summary: Simulates a circuit with Boolean variables instead of constants on the inputs, so each node holds a BDD or formula that covers all input values at once.
model: word-ram
complexity:
  vars: {k: the number of simulated cycles, P: the number of gate inputs of the circuit, B: "the number of nodes of the largest BDD of the run (at most 2^(v + 1), v the number of variables)"}
  time: {worst: "O(k P B^2)"}
  space: {extra: "O(k P B^2)"}
properties: {deterministic: true, exact: true, complete: true, recursive: true}
history:
  year: 1979
  people: [William C. Carter, William H. Joyner, Daniel Brand, Randal E. Bryant]
  note: Carter, Joyner and Brand simulated a machine description with symbols in 1979. Bryant made the method practical at gate and switch level with BDDs in the COSMOS work of 1987 and surveyed it in 1990.
prereqs: [logic-simulation, reduced-ordered-bdd, bdd-apply]
see_also: [ternary-simulation, symbolic-trajectory-evaluation, cycle-based-simulation, boolean-equivalence-checking, bounded-model-checking, symbolic-execution, multiplier-bdd-lower-bound, symbolic-reachability]
sources:
  - paper: "W. C. Carter, W. H. Joyner and D. Brand, Symbolic simulation for correct machine design, Proceedings of the 16th Design Automation Conference, 280 to 286, 1979"
    title: W. C. Carter, W. H. Joyner and D. Brand, Symbolic simulation for correct machine design, DAC 1979, 280 to 286
    locator: symbolic values for the inputs and the initial register contents of a machine description, and the comparison of the symbolic results with a specification
  - paper: doi:10.1109/TC.1986.1676819
    title: R. E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 677 to 691, 1986
    locator: the reduced ordered BDD, its canonical form under a fixed variable order, and the Apply operation with its cost of O(|f| |g|)
  - paper: doi:10.1145/37888.37890
    title: R. E. Bryant, D. L. Beatty, K. S. Brace, K. Cho and T. J. Sheffler, COSMOS, a compiled simulator for MOS circuits, DAC 1987, 9 to 16
    locator: the switch-level network turned into Boolean equations by the symbolic analyzer ANAMOS, which is the base of the symbolic mode
  - paper: doi:10.1145/123186.128296
    title: R. E. Bryant, Symbolic simulation, techniques and applications, Proceedings of the 27th Design Automation Conference, 517 to 521, 1990
    locator: the survey of symbolic simulation with BDDs, the encoding of inputs and initial states by variables, and its use for circuit verification
  - paper: doi:10.1109/12.73590
    title: R. E. Bryant, On the complexity of VLSI implementations and graph representations of Boolean functions with application to integer multiplication, IEEE Transactions on Computers 40(2), 205 to 213, 1991
    locator: the exponential lower bound on the BDD of the middle output bit of a multiplier under every variable order
---

Symbolic simulation runs a gate-level circuit with Boolean variables on its inputs in place of 0 and 1. Each node then holds a Boolean function of the variables, kept as a [reduced ordered BDD](/reduced-ordered-bdd/), and one run covers every input value at once. For a synchronous circuit the method gives the inputs a fresh variable in each clock cycle, and it gives each register either its reset value or a variable for an unknown initial value. After $k$ cycles the BDD of an output is the exact function from all input sequences of length $k$ to the value of that output. This is a verification page. The simulation here is zero-delay [cycle-based logic simulation](/cycle-based-simulation/) with the values 0 and 1, and the method is a check of the design before manufacturing. A property that must hold for all inputs becomes one BDD that must be the constant 1, and two designs are equal on all inputs when their BDDs are the same node.

## In plain words

A normal simulator puts one test vector on the inputs and gets one answer. To check all inputs of a 64-bit adder this way you need $2^{128}$ runs.

A symbolic simulator puts a name, such as $a_0$, on each input instead of a value. Each gate then works on formulas, not bits: an AND gate with inputs $a_0$ and $b_0$ gives the formula "$a_0$ and $b_0$". At the end, each output holds a formula that says what the output is for every input at once.

The formulas are kept in a form in which equal functions look the same, so a check is a comparison. The price is that some formulas get very large, for example those of a multiplier.

## The problem

The input is a synchronous circuit $C$ with one clock, a number $k$ of cycles, and a variable order. The circuit has primary inputs $X$, latches $S$ with a next-state node $\mathrm{next}(s)$ and an initial value $\mathrm{init}(s) \in \{0, 1, ?\}$, where $?$ means unknown, gates in topological order, and outputs $O$. A *run* of length $k$ is a choice of a value for every unknown initial latch and of an input vector for each cycle $0, \ldots, k - 1$. Two-valued simulation of a run gives a value $\mathrm{val}_t(u)$ for every node $u$ in every cycle $t$.

The variables are one variable $s^0$ for each latch $s$ with unknown initial value and one variable $x_t$ for each input $x$ and cycle $t$. A run is then the same thing as an assignment $\alpha$ of 0 or 1 to all variables. The output is, for each cycle $t$ and output $o$, the BDD $O_t(o)$ with $O_t(o)(\alpha) = \mathrm{val}_t(o)$ for the run $\alpha$, for all $\alpha$.

## The algorithm

```pseudo id=main
SYMBOLIC-SIMULATE(C, k)
L1  for each latch s do S(s) ← init(s) if it is 0 or 1, else a fresh variable s⁰
L2  for t ← 0 to k − 1 do
L3      for each primary input x do V(x) ← a fresh variable x_t
L4      for each latch s do V(s) ← S(s)
L5      for each gate u in topological order do V(u) ← APPLY(op(u), V of the fanins of u)
L6      for each output o do O_t(o) ← V(o)
L7      for each latch s do S(s) ← V(next(s))
L8  return O_0, ..., O_(k−1)
```

The loop is the loop of a [cycle-based simulator](/cycle-based-simulation/). The only change is the value type. Line L1 gives a known reset value as the constant BDD, and an unknown value as a variable, so the result holds for every initial state. Line L3 makes a new variable in every cycle. The input of cycle 1 is then free to differ from the input of cycle 0. Line L5 is the [Apply](/bdd-apply/) operation of the gate, for example the AND of two BDDs, and the BDD package keeps one node per function in its unique table. Line L7 moves the next-state functions into the latches, which is the clock edge.

A check comes after the run. To prove that a property $P$ of the outputs holds in all runs, build the BDD of $P$ from the $O_t(o)$ and compare it with the constant 1. If it is not 1, any path to the 0 terminal is a run that breaks $P$, which a normal simulator can then replay. To compare two circuits, simulate both with one manager and the same variables. They agree on all runs of length $k$ exactly when their output BDDs are the same nodes.

## Example

Take one input $a$, one latch $r$ with reset value 0, and two gates $n = r \oplus a$ and $z = r \wedge a$, with $\mathrm{next}(r) = n$ and the output $z$. So $r$ holds the parity of the inputs so far, and $z$ is 1 when the input and the parity are both 1. Simulate $k = 3$ cycles. The sizes count the BDD nodes, terminals included, under the order $a_0 < a_1 < a_2$.

| cycle $t$ | $V(a)$ | $V(r)$ at L4 | $V(z) = O_t(z)$ | size | $V(n)$, the next $r$ | size |
|---|---|---|---|---|---|---|
| 0 | $a_0$ | $0$ | $0$ | 1 | $a_0$ | 3 |
| 1 | $a_1$ | $a_0$ | $a_0 \wedge a_1$ | 4 | $a_0 \oplus a_1$ | 5 |
| 2 | $a_2$ | $a_0 \oplus a_1$ | $(a_0 \oplus a_1) \wedge a_2$ | 6 | $a_0 \oplus a_1 \oplus a_2$ | 7 |

The three BDDs of $z$ cover all $2^3 = 8$ runs of length 3. Each run takes 3 cycles of normal simulation, and the 8 runs together take 24.

Now check the property "$z$ is never 1 in two cycles in a row" for cycles 1 and 2. The BDD of $O_1(z) \wedge O_2(z)$ is $a_0 a_1 (a_0 \oplus a_1) a_2$. When $a_0 = a_1 = 1$, the parity $a_0 \oplus a_1$ is 0, so the BDD package returns the 0 terminal, and the property holds in every run. If the latch starts unknown instead, line L1 gives it the variable $r^0$. Then $O_0(z) = r^0 \wedge a_0$, and the result covers 16 runs.

The parity BDD grows by 2 nodes per cycle, so its size is linear in $k$ while the number of runs is $2^k$. That gap is the gain of the method. The tests build these BDDs and check them against normal simulation of all runs.

## Correctness

The result is exact: for every cycle $t$, output $o$ and assignment $\alpha$, $O_t(o)(\alpha)$ is the value of $o$ in cycle $t$ of the run $\alpha$. The invariant, kept in each cycle and at each gate in topological order, is that $V(u)$ evaluated at $\alpha$ equals $\mathrm{val}_t(u)$ in the run $\alpha$. Inputs and latches start it at lines L3, L4 and L1. Line L5 keeps it because Apply returns the BDD of the gate function of its arguments, and evaluation at one point commutes with every gate operator. Line L7 carries it to the next cycle. Since a reduced ordered BDD is canonical for a fixed variable order (Bryant 1986), two outputs agree in all runs exactly when their BDDs are the same node, and a property holds in all runs exactly when its BDD is the terminal 1. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM with hashing in expected constant time. Let $v$ be the number of variables, $P$ the number of gate inputs, and $B$ the largest BDD of the run.

- Apply of two BDDs with $|f|$ and $|g|$ nodes, with a cache, costs $O(|f| |g|)$ time (Bryant 1986). A gate with $d$ inputs costs $d - 1$ applies, so line L5 costs $O(P B^2)$ per cycle.
- Lines L1, L3, L4, L6 and L7 cost $O(|S| + |X| + |O|)$ per cycle.
- Over $k$ cycles the time is $O(k P B^2)$, and the unique table and the cache hold one entry per step, which gives the same space bound.

A BDD over $v$ variables has at most $2^i$ nodes at depth $i$, so $B \le 2^{v + 1} - 1$, and for a sequential circuit $v$ grows by $|X|$ per cycle. The exponent is real for some functions. For the middle output bit of an $n$-bit multiplier, every variable order gives a BDD with at least $2^{n/8}$ nodes ([Bryant 1991](/multiplier-bdd-lower-bound/)). The method cannot be polynomial for all circuits in any case: a circuit is satisfiable exactly when its output BDD is not the 0 terminal, so a polynomial method would decide circuit SAT. In practice the cost depends on the [variable order](/variable-ordering/), and for control logic and datapaths without multipliers a good order keeps $B$ small.

## Properties

- Exact and complete for runs of the chosen length $k$. It says nothing about longer runs.
- Deterministic. The BDD of a function does not depend on the circuit that computes it, only on the variable order.
- The result for a run is the same as normal two-valued simulation of that run, so a failing run from a BDD can be replayed in any simulator.
- Unknown initial values cost one variable each. The method uses only the values 0 and 1. The value X is the subject of [ternary simulation](/ternary-simulation/).

## Variants and improvements

- **Formulas in place of BDDs.** Each node holds a gate of a shared graph, such as an [and-inverter graph](/and-inverter-graph/), and the check is a SAT call. The graph is linear in $k P$, and the hard work moves to the solver. With a property at cycle $k$, this is [bounded model checking](/bounded-model-checking/) of the unrolled circuit.
- **Partly symbolic runs.** Some inputs get constants and some get variables, for example a fixed opcode with symbolic operands. Each run then covers one slice of the input space, and the BDDs stay small.
- **Ternary symbolic simulation.** Each node holds a pair of BDDs that encodes 0, 1 or X under each assignment. Unknown values that do not matter for a property then cost no variable. This is the engine of [symbolic trajectory evaluation](/symbolic-trajectory-evaluation/).
- **Switch level.** COSMOS first turns a transistor network into Boolean equations, then simulates them. A [switch-level](/switch-level-simulation/) simulator with BDD values gives symbolic simulation of MOS circuits.
- **Reachable states.** Applying the transition relation to sets of states, with existential quantification of the inputs, gives [symbolic reachability](/symbolic-reachability/). It covers all run lengths, but needs [image computation](/transition-function-image-computation/) in place of a simple forward pass.
- **Software.** [Symbolic execution](/symbolic-execution/) of programs keeps a path condition and splits at branches. A circuit has no branches, so symbolic simulation needs no path splitting.

## When to use it

Use it to prove a property for all inputs over a bounded number of cycles: the result of a pipeline after $k$ cycles, a datapath without multipliers, a check that two versions of a block are equal for $k$ cycles from reset. It also finds counterexamples that random simulation misses, because one BDD covers all runs. For combinational [equivalence](/boolean-equivalence-checking/) with much shared structure, [SAT sweeping](/sat-sweeping/) or a SAT check of the [miter](/miter-circuit/) is usually cheaper. For properties over all run lengths, use [symbolic reachability](/symbolic-reachability/) or the model checkers. For multipliers, use word-level methods.

## Pitfalls

- **One variable for an input in all cycles.** If line L3 reuses $x_0$ in every cycle, the result covers only runs with a constant input. In the example, $O_2(z)$ would become $(a \oplus a) \wedge a = 0$, and a bug at $a_0 = 1, a_2 = 1$ would be missed. Line L3 must make a fresh variable in every cycle.
- **Treating an unknown initial value as 0.** If line L1 uses 0 for a latch with no reset, the proof covers only one initial state. Give the latch a variable, or prove that the reset sets it first.
- **A bad variable order.** With the variables of one operand all before those of the other, the BDD of an $n$-bit equality comparator has about $2^n$ nodes, while an interleaved order gives $O(n)$ nodes. Interleave the bits of operands that are compared or added, and order the variables of a later cycle after those of an earlier one only when the circuit reads its inputs in that order.
- **Gates out of order.** Line L5 needs a topological order of the combinational logic. A combinational cycle has no such order, and a simulator that evaluates a gate before its fanins uses stale BDDs from the previous cycle.

## Implementations

## History

Carter, Joyner and Brand at IBM (DAC 1979) simulated a machine description with symbols for the inputs and for the initial contents of the registers, and compared the results with a specification. The symbolic expressions were hard to compare, and the work stopped for some years. Bryant's BDDs (1986) gave a canonical form in which a comparison is one test. The COSMOS simulator of Bryant, Beatty, Brace, Cho and Sheffler (DAC 1987) turned MOS transistor networks into Boolean equations, and its symbolic mode ran them with BDD values. Bryant surveyed the techniques and uses in 1990, and in 1991 he showed that multipliers have no small BDD under any order, which marks the limit of the method.

## References
