---
tag: WGDS9V
kind: algorithm
slug: deductive-fault-simulation
name: Deductive fault simulation
aliases:
- Armstrong deductive simulation
area: eda/test-and-diagnosis
level: core
summary: Armstrong's fault simulator that propagates, with the good values, the list of faults that flip each line, computed by set operations at each gate.
solves: [fault-simulation]
model: word-ram
complexity:
  vars: {T: the number of vectors, L: the number of lines, P: the number of gate input pins, F: the number of faults}
  time: {worst: "O(T (L + P) (1 + F))"}
  space: {extra: O(L (1 + F))}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1972
  people: [D. B. Armstrong]
  note: Armstrong published the deductive method in IEEE Transactions on Computers in 1972.
prereqs: [fault-simulation, stuck-at-fault-model]
see_also: [concurrent-fault-simulation, parallel-fault-simulation, ppsfp, critical-path-tracing, event-driven-logic-simulation, fault-collapsing, fault-coverage, bit-vector]
sources:
  - paper: doi:10.1109/T-C.1972.223542
    title: D. B. Armstrong, A deductive method for simulating faults in logic circuits, IEEE Transactions on Computers C-21(5), 464 to 471, 1972
    locator: the method, with the fault list of each gate output computed from the good values and the lists of its inputs
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Logic and Fault Simulation (deductive fault simulation and its list rules for each gate type)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on fault simulation (deductive fault simulation, unknown values and its comparison with concurrent simulation)
---

Deductive fault simulation is a method for [fault simulation](/fault-simulation/) that simulates only the good circuit and, for each line, deduces the set of faults that would give the line the opposite value. This set, the fault list of the line, follows from the good values and the fault lists of the gate inputs by unions, intersections and differences. No faulty circuit is ever evaluated. The fault list of a primary output is the set of faults that the vector detects there, for all [single stuck-at faults](/stuck-at-fault-model/) at once, in one pass over the circuit.

## In plain words

Run the good circuit on one input. Next to each wire, keep a list of the breaks that would flip that wire.

The list of a gate output comes from the lists of its inputs. Take an AND gate whose inputs are all 1. Then any break that flips any input flips the output, so the output list is all the input lists together. If one input is 0, only a break that flips that input, and does not flip another input to 0, flips the output. If two inputs are 0, a break must flip both of them.

At each wire, add the break of that wire itself that gives the opposite value. The list at an output is the set of breaks this input finds.

## The problem

The input is a combinational circuit $C$ with $L$ lines in topological order, a list of single stuck-at faults, a sequence of two-valued input vectors, and a flag for fault dropping. The lines are the primary inputs, the gate outputs and the fanout branches, and $P$ is the number of gate input pins. The output is, for each vector, the set of faults that it detects among those still simulated. With dropping, a fault is not simulated after the first vector that detects it.

For a vector $t$, a line $k$ with good value $g(k)$ and an alive fault $f$, write $f(k)$ for the value of $k$ in the circuit with fault $f$. The fault list of $k$ is
$$\mathcal{L}_k = \{f \text{ alive} : f(k) \ne g(k)\}.$$
Since the values are 0 and 1, a fault in $\mathcal{L}_k$ gives $k$ the value $\lnot g(k)$, so the list needs no values, only faults.

## The algorithm

For a gate with inputs $j_1, \ldots, j_d$, the rule that gives the list of its output from the lists of its inputs depends on the gate type and the good input values. A buffer, an inverter and a fanout branch copy the list of their input. For AND and NAND the controlling value is $c = 0$, and for OR and NOR it is $c = 1$. Let $S$ be the set of inputs at $c$. Then
$$\mathcal{L}_{\text{gate}} = \begin{cases} \bigcup_{j} \mathcal{L}_j & \text{if } S = \emptyset, \\ \bigcap_{j \in S} \mathcal{L}_j \setminus \bigcup_{j \notin S} \mathcal{L}_j & \text{if } S \ne \emptyset. \end{cases}$$
For XOR and XNOR, the output list is the set of faults that appear in an odd number of input lists, the symmetric difference of the lists.

```pseudo id=main
DEDUCTIVE-FAULT-SIMULATION(C, vectors, faults, drop)
    alive ← faults
L1  for each vector t do
L2      simulate the good circuit on t, which gives g(k) for every line k
L3      for each line k in topological order do
L4          if k is a primary input then 𝓛[k] ← ∅
L5          else 𝓛[k] ← the rule of the gate of k on the good values and the lists of its inputs
L6          if the fault k stuck at ¬g(k) is alive then add it to 𝓛[k]
L7      D ← the union of 𝓛[o] over the primary outputs o; report D as detected by t
L8      if drop then alive ← alive ∖ D
```

Line L6 adds the local fault of the line. The fault $k$ stuck at $g(k)$ never enters a list, since it does not change $k$ under this vector. A stem fault enters the list of the stem and, through the copy rule, the lists of all its branches. A branch fault enters only the list of its branch.

## Example

The circuit is $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ into $g$ and $b_h$ into $h$, so there are 8 lines and 16 faults. Take the vector $abc = 111$, with all 16 faults alive.

| line | good value | how the list is formed | fault list |
|---|---|---|---|
| $a$ | 1 | input, plus a/0 | {a/0} |
| $b$ | 1 | input, plus b/0 | {b/0} |
| $b_g$ | 1 | copy of $b$, plus $b_g$/0 | {b/0, $b_g$/0} |
| $b_h$ | 1 | copy of $b$, plus $b_h$/0 | {b/0, $b_h$/0} |
| $c$ | 1 | input, plus c/0 | {c/0} |
| $g$ | 0 | no input at 0: union, plus g/1 | {a/0, b/0, $b_g$/0, g/1} |
| $h$ | 0 | no input at 0: union, plus h/1 | {b/0, $b_h$/0, c/0, h/1} |
| $z$ | 1 | both inputs at 0: intersection, plus z/0 | {b/0, z/0} |

The vector detects b/0 and z/0. At $z$ both inputs are at the controlling value 0, so a fault flips $z$ only if it flips both $g$ and $h$. Only the stem fault b/0 does that, since it reaches $g$ through $b_g$ and $h$ through $b_h$. The fault a/0 flips $g$ alone and leaves $h = 0$, which keeps $z = 1$. This is reconvergent fanout, and the intersection handles it with no special case.

For the sequence 101, 010, 011, 110 with dropping, the list of $z$ is {b/1, $b_g$/1, $b_h$/1, g/0, h/0, z/1}, then {a/1, c/1}, then {b/0, $b_h$/0, c/0, h/1, z/0}, then {a/0, $b_g$/0, g/1}, the first detections in the table of the [fault simulation](/fault-simulation/) page. The set operations of the run touch 40 list elements in all, against 54 without dropping.

## Correctness

The proof is an induction over the lines in topological order. Assume that the list of each input $j$ of a gate is correct, so that a fault $f$ that does not sit on the gate output flips exactly the inputs whose lists hold $f$. The gate output then flips in exactly the cases that the rule selects. For an AND-type gate with no input at $c$, the output flips as soon as one input flips to $c$. With inputs at $c$, the output flips only if no input is at $c$ under $f$: every input of $S$ flips, and no other input flips to $c$. For XOR, each flipped input flips the output once, so the output flips for an odd number of them. A fault on the gate output sets it to its stuck value and differs exactly when that value is $\lnot g(k)$, which is line L6. The [full proof](proofs/correctness.md) checks each gate type and the induction.

## Complexity

The good simulation costs $O(L + P)$ per vector. The rule of a gate with inputs $j_1, \ldots, j_d$ costs $O(|\mathcal{L}_{j_1}| + \cdots + |\mathcal{L}_{j_d}|)$ with lists kept sorted by fault number and merged, or the same in expected time with hash sets. A list never holds more than the $F$ alive faults. A line with fanout feeds several gates, but each gate input pin reads one list, so a vector costs $O((L + P)(1 + F))$ in the worst case, and $T$ vectors cost $O(T (L + P)(1 + F))$. This is the same order as serial fault simulation. The lists of all lines take $O(L (1 + F))$ space; a version that frees the list of a line after its last fanout is read keeps fewer.

The gain is in the typical case and is measured, not proved: most lists are short, since most faults do not reach most lines. For the c17 benchmark circuit with its 34 faults and all 32 input vectors in counting order, the code of this page touches 1408 list elements without dropping and 206 with dropping. These are counts on a 6-gate toy circuit, not benchmark results.

## Properties

- **Exact.** For two-valued vectors on a combinational circuit, the result is the same as serial fault simulation, with or without dropping. The lists of all lines are exact, not only those of the outputs.
- **One pass per vector.** All faults are simulated together, and no faulty gate is evaluated.
- **Memory depends on the vector.** The size of a list can change a lot from one vector to the next, so the memory is hard to plan.
- **Two values.** The rules need the values 0 and 1. With an unknown value X, a fault can turn a 0 into X, and the lists must carry the faulty value too, which makes the rules much more complex.
- **Deterministic.** The detected sets do not depend on the order of the faults.

## Variants and improvements

- **Event-driven lists.** A line needs a new list only if the good value or the list of an input changed since the last vector. Recomputing only those lines, as in [event-driven logic simulation](/event-driven-logic-simulation/), saves work when vectors differ in few inputs.
- **Bit vectors.** For a small fault list, a list is a [bit vector](/bit-vector/) of $F$ bits, and the rules become word-wide AND, OR and XOR. The time is then $O(F / w)$ words per pin, whatever the list sizes.
- **Fanout-free regions.** Inside a fanout-free region, the list of each line flows to one gate only. So lists are needed only at the roots of the regions. Inside a region, [critical path tracing](/critical-path-tracing/) finds the lines whose flip reaches the root, and a fault on such a line is detected exactly when a flip of the root is detected.
- **Concurrent simulation.** [Concurrent fault simulation](/concurrent-fault-simulation/) keeps a faulty value per list entry and evaluates the faulty gates. It costs gate evaluations but handles more values, timing and sequential circuits more easily.

## When to use it

Use deductive simulation when all faults must be simulated against every vector of a combinational circuit, for example to build a [fault dictionary](/fault-dictionary/) for diagnosis, and when values are two-valued. The lists of all lines give, as a side result, the faults that each vector propagates to each line. For grading large test sets with dropping, the textbooks in the references report [PPSFP](/ppsfp/) as faster, and for sequential circuits with unknown initial states, [concurrent fault simulation](/concurrent-fault-simulation/) handles the X values that deductive rules do not.

## Pitfalls

- **Forgetting the local fault.** Line L6 must add the fault of the line itself. Without it, gate output faults never enter any list.
- **Adding both local faults.** Only $k$ stuck at $\lnot g(k)$ enters the list. The fault $k$ stuck at $g(k)$ does not flip $k$ under this vector.
- **Subtracting only for one controlling input.** With two or more inputs at $c$, the rule is the intersection of their lists minus the lists of the other inputs. Using the union of the controlling lists reports faults that flip only one of them, which leaves the output at its value.
- **XOR as union.** A fault that flips two inputs of an XOR leaves its output unchanged. Use the symmetric difference.
- **Stems without branch lines.** If a stem and its branches share one list, the faults on single branches are lost, and the list of the stem gets faults that act on one branch only.

## Implementations

## History

Armstrong published the deductive method in IEEE Transactions on Computers in 1972, as a way to simulate all faults in one pass with set operations instead of one faulty circuit per bit. Ulrich and Baker's [concurrent fault simulation](/concurrent-fault-simulation/) of 1973 kept the idea of lists of faults per line but stored faulty values and evaluated faulty gates, which extends to timing and more values. Deductive simulation remained a standard method of the textbooks, and its set rules for gates reappear in [critical path tracing](/critical-path-tracing/), which needs no lists at all inside fanout-free regions.

## References
