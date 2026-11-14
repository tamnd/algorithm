---
tag: NCVK7P
kind: algorithm
slug: concurrent-fault-simulation
name: Concurrent fault simulation
aliases:
- Ulrich-Baker concurrent simulation
area: eda/timing-and-verification
level: advanced
summary: Simulates the good circuit and, at each gate, only the faulty circuits whose values there differ from the good one, as lists updated with each event.
solves: [fault-simulation]
model: word-ram
complexity:
  vars: {T: the number of vectors, L: the number of lines, P: the number of gate input pins, F: the number of faults}
  time: {worst: "O(T (L + P) (1 + F))"}
  space: {extra: O(L (1 + F))}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1973
  people: [Ernst G. Ulrich, T. Baker]
  note: Ulrich and Baker presented concurrent simulation at the Design Automation Workshop of 1973 and in IEEE Computer in 1974.
prereqs: [fault-simulation, event-driven-simulation]
see_also: [stuck-at-fault-model, fault-collapsing, automatic-test-pattern-generation, built-in-self-test, bit-parallelism]
sources:
  - paper: "Ernst G. Ulrich and T. Baker, The concurrent simulation of nearly identical digital networks, Proceedings of the 10th Design Automation Workshop, 145 to 150, 1973"
    title: E. G. Ulrich and T. Baker, The concurrent simulation of nearly identical digital networks, Proceedings of the 10th Design Automation Workshop, 145 to 150, 1973
    locator: the method, with one list of bad gates per good gate and evaluation only where a bad gate differs
  - paper: "Ernst G. Ulrich and T. Baker, Concurrent simulation of nearly identical digital networks, IEEE Computer 7(4), 39 to 44, 1974"
    title: E. G. Ulrich and T. Baker, Concurrent simulation of nearly identical digital networks, IEEE Computer 7(4), 39 to 44, April 1974
    locator: the journal version of the method
  - paper: doi:10.1109/T-C.1972.223542
    title: D. B. Armstrong, A deductive method for simulating faults in logic circuits, IEEE Transactions on Computers C-21(5), 464 to 471, 1972
    locator: deductive fault simulation with fault lists computed by set operations, the method that concurrent simulation is compared with
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Logic and Fault Simulation (serial, parallel, deductive and concurrent fault simulation)
---

Concurrent fault simulation is a method for [fault simulation](/fault-simulation/): for each input vector, find which [single stuck-at faults](/stuck-at-fault-model/) it detects. It runs one [event-driven](/event-driven-simulation/) simulation of the good circuit. Each line also keeps a list of the faulty circuits whose value on that line differs from the good value, with that value. A faulty circuit is evaluated only at the gates where it differs from the good circuit on an input or where its fault sits, so the many faulty circuits that agree with the good one at a gate cost nothing there.

## In plain words

A circuit with one broken wire behaves almost like the good circuit. On most wires, for most input values, the two give the same value. So simulating every broken circuit from scratch repeats the same work again and again.

Concurrent simulation runs the good circuit once. Next to each wire it keeps a short note: "in broken circuit number 7 this wire is 0, not 1". At each gate it looks only at the broken circuits that appear in the notes of the gate inputs, or whose break is at this gate. It computes their output and keeps a note only if the output differs from the good one.

When the notes on an output wire are not empty, those broken circuits are found by this input. They can then be removed.

## The problem

The input is a combinational circuit $C$ with $L$ lines in topological order, a list of faults, a sequence of two-valued input vectors, and a flag for fault dropping. The lines are the primary inputs, the gate outputs and the fanout branches. The output is, for each vector, the set of faults that it detects among those still simulated. With dropping, a fault is no longer simulated after the first vector that detects it.

For a fault $f$ and a line $k$, the faulty value $f(k)$ is the value of $k$ in the circuit with fault $f$. The fault list of $k$ is the set of pairs $(f, f(k))$ with $f(k)$ different from the good value of $k$.

## The algorithm

```pseudo id=main
CONCURRENT-FAULT-SIMULATION(C, vectors, faults, drop)
    alive ← faults; every good value is X; every fault list is empty
L1  for each vector t do
L2      schedule every primary input
L3      while a line is scheduled do: take the scheduled line k with the smallest index
L4          g ← the value of k in t if k is an input, else the gate of k on the good values of its inputs
L5          S ← the alive faults that sit on k or appear in the list of an input of k
L6          for each f ∈ S do v ← the stuck value if f sits on k, else the gate of k on the values of f at its inputs
L7              if v ≠ g then put (f, v) in the new list of k
L8          if g or the new list differs from the stored one then store both and schedule the fanouts of k
L9      report the alive faults in the lists of the primary outputs as detected by t
L10     if drop then remove them from alive
```

At line L6, the value of $f$ at an input $j$ is the value in the list of $j$ if $f$ appears there, and the good value of $j$ otherwise. Taking the smallest index first is a levelized order for a combinational circuit, so each line is evaluated at most once per vector, after all its inputs. Dropped faults may stay in old lists. Every read keeps only the alive faults, so they cost nothing until the list is next rebuilt.

## Example

The circuit is $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ into $g$ and $b_h$ into $h$, so there are 8 lines and 16 faults. The vectors are $abc = 110$, then 011. The table shows each line as good value [fault list]. A fault written $x/v$ means line $x$ stuck at $v$, and every value in a list is the complement of the good value, so the list shows only the faults.

| line | after 110 | after 011, without dropping |
|---|---|---|
| $a$ | 1 [a/0] | 0 [a/1] |
| $b$ | 1 [b/0] | 1 [b/0] |
| $b_g$ | 1 [b/0, b_g/0] | 1 [b/0, b_g/0] |
| $b_h$ | 1 [b/0, b_h/0] | 1 [b/0, b_h/0] |
| $c$ | 0 [c/1] | 1 [c/0] |
| $g$ | 0 [a/0, b/0, b_g/0, g/1] | 1 [a/1, g/0] |
| $h$ | 1 [c/1, h/0] | 0 [b/0, b_h/0, c/0, h/1] |
| $z$ | 1 [a/0, b/0, b_g/0, g/1, z/0] | 1 [b/0, b_h/0, c/0, h/1, z/0] |

The first vector detects a/0, b/0, $b_g$/0, g/1 and z/0, the list of $z$. At $g$ the list holds the faults of the lists of $a$ and $b_g$ and the fault g/1, and they all differ, because both inputs are at the non-controlling value 1. At $h$ the fault b/0 is evaluated but not kept: $c = 0$ already makes $h = 1$.

For the second vector, the inputs $a$ and $c$ change and $b$ does not. So line L8 schedules $g$ and $h$ but not $b_g$ and $b_h$, whose values and lists stay as they are, and then $z$. The new list of $g$ loses b/0 and $b_g$/0, because $a = 0$ now blocks them. The list of $z$ adds the four faults of $h$. With dropping, the second vector reports $b_h$/0, c/0 and h/1, since b/0 and z/0 were dropped after the first vector. The run with dropping makes 14 line evaluations and 22 faulty gate evaluations, where serial simulation of the 16 faulty circuits would evaluate the 5 non-input lines once per circuit and vector.

## Correctness

The good value and the fault list of a line depend only on the good values and the fault lists of its inputs, and on the faults that sit on the line. A fault that sits elsewhere and appears in no input list sees the good values on all inputs, so its value equals the good value and it belongs in no list. So lines L5 to L7 compute the correct list from correct input lists. Because the smallest index is taken first, every input of a line is final before the line is evaluated. A line that is not scheduled had no input change since the last vector, so its old value and list are still correct. By induction over the lines and the vectors, every list is correct after each vector, and line L9 reads exactly the faults whose faulty output differs. Restricting the lists to the alive faults keeps them correct, because each fault's entry is computed from that fault's entries only. The [full proof](proofs/correctness.md) gives the details.

## Complexity

One evaluation of line $k$ costs $O((1 + |S|) \cdot \mathrm{fanin}(k))$ time, up to the cost of the set operations, and $|S|$ is at most the number of alive faults. Each line is evaluated at most once per vector, so a vector costs $O((L + P)(1 + F))$ time in the worst case, where $P$ is the number of gate input pins and $F$ the number of faults. This is the same order as serial simulation of every fault. The lists hold at most $F$ entries per line, so the space is $O(L (1 + F))$.

The gain of the method is in the typical case, and it is measured, not proved. Lists are short when few faulty circuits differ from the good one at a line, and few lines change from one vector to the next. With dropping the lists also shrink as tests are applied. For the c17 benchmark circuit with its 34 faults and all 32 input vectors in counting order, the implementation of this page makes 309 line evaluations and 130 faulty gate evaluations with dropping, and 350 and 816 without. In a shuffled order the counts change, to 384 and 153 with dropping for one fixed shuffle. These are counts on a 6-gate toy circuit, not timings.

## Properties

- **Exact.** For two-valued vectors on a combinational circuit, the result is the same as serial simulation of each faulty circuit, with or without dropping.
- **Event-driven in two ways.** A line is evaluated only if an input changed, and a faulty circuit only where it differs from the good one.
- **Any fault model with local effect.** A fault only has to change the value of the gate where it sits. Bridging faults, faults in sequential circuits and faults with more than two logic values fit the same lists.
- **Memory grows with the activity.** The lists can be long when many faulty circuits differ on many lines, for example early in a test set before dropping.
- **Deterministic.** The output does not depend on the order of the faults.

## Variants and improvements

- **Lists per gate.** Ulrich and Baker keep, for each good gate, a list of bad gates: copies of the gate with the input and output values of one faulty circuit. This page keeps the output value per line and reads the faulty input values from the input lines, which holds the same information.
- **Sequential circuits and timing.** The original method simulated sequential circuits with delays. A faulty circuit then can also differ in the state of a flip-flop, and its entries live in the lists of the state lines. A list entry that converges to the good value is removed, and one that diverges is added.
- **Multiple values.** The same scheme simulates faulty circuits with the values 0, 1, X and Z, which is needed for buses and for unknown initial states.
- **Deductive simulation.** Armstrong (1972) computes the list of a line from the lists of its inputs with set operations, such as the intersection of the lists of controlling inputs. It needs no faulty gate evaluation but is harder to extend to timing and to more values.
- **Parallel and PPSFP.** Parallel fault simulation puts one faulty circuit in each bit of a machine word, as in [bit-parallelism](/bit-parallelism/). Parallel pattern single fault propagation puts one vector in each bit and is the usual method for combinational circuits and full scan.

## When to use it

Use concurrent fault simulation for circuits with state and timing, where faulty circuits diverge and converge again, and for fault models with many logic values. For combinational logic and full scan designs, the bit-parallel pattern methods with fault dropping are often faster and simpler. Fault simulation of either kind runs in the loop of test generation: after each new test from [ATPG](/automatic-test-pattern-generation/), it removes all other faults that the test also detects, and it grades the random patterns of [built-in self-test](/built-in-self-test/).

## Pitfalls

- **Forgetting the local fault.** A fault on line $k$ has no entry in the lists of the inputs of $k$. Line L5 must add it, or the faults of each gate output never start a list.
- **Keeping equal values.** A list entry whose value equals the good value must be removed at line L7. If it stays, the list grows, and line L9 reports it as detected.
- **A wrong order.** Evaluating a line before one of its inputs gives a stale value. With unit delays the order is the time of the events, and with zero delay it is the topological order of line L3.
- **Stuck faults on stems and branches.** A fault on a stem enters every branch list. A fault on one branch enters only that branch. Merging them loses faults that only one branch detects, such as $b_h$/0 in the example.
- **Comparing lists without the alive filter.** Dropped faults left in an old list make it look different from the new one. The comparison of line L8 must use the alive faults only, or every line is rescheduled.

## Implementations

## History

Fault simulation in the 1960s simulated each faulty circuit on its own, or one faulty circuit per bit of a machine word. Armstrong (1972) gave deductive simulation, which computes fault lists by set operations. Ulrich and Baker presented concurrent simulation at the Design Automation Workshop of 1973, and in IEEE Computer in 1974, as a method for simulating many nearly identical networks at once. It became a common method in fault simulators for sequential circuits.

## References
