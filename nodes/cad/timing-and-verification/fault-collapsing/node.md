---
tag: P3T8F3
kind: technique
slug: fault-collapsing
name: Fault collapsing
aliases:
- fault equivalence and dominance
area: cad/timing-and-verification
level: core
summary: Shrinks the fault list by keeping one fault of each equivalence class and dropping faults dominated by others, about halving test work.
prereqs: [stuck-at-fault-model]
see_also: [fault-simulation, automatic-test-pattern-generation, equivalence-checking, sat-sweeping, disjoint-set, built-in-self-test]
sources:
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Fault Modeling (fault equivalence, fault dominance, equivalence and dominance collapsing, and the checkpoint theorem)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on fault modeling (equivalence and dominance of single stuck faults, and checkpoints)
---

Fault collapsing reduces the list of [single stuck-at faults](/stuck-at-fault-model/) that test generation and fault simulation must handle. Two faults are equivalent when their faulty circuits compute the same function, so one test detects both or neither, and only one fault of each class needs to stay. A fault dominates another when every test of the other also detects it, so the dominating fault can usually be dropped as well. Simple rules at each gate find most of these relations in one pass, and the checkpoint theorem gives a small list that is complete for circuits of AND, OR, NAND, NOR, NOT and BUF gates.

## In plain words

Many faults look the same from outside. If one input of an AND gate is stuck at 0, the output is 0. If the output itself is stuck at 0, the output is also 0. No test can tell the two apart, so a test for one is a test for the other. Keep one and drop the other.

Some faults are easier to catch than others. The output of an AND gate stuck at 1 is caught by every test that catches one input stuck at 1, and by more. If the list keeps the input fault, the output fault comes for free.

Doing this at every gate often shrinks a list of faults to about half its size, and every later step of test gets faster.

## When it applies

- A list of faults goes to [fault simulation](/fault-simulation/) or to [ATPG](/automatic-test-pattern-generation/), and the cost grows with the length of the list.
- The fault model has local faults whose effect on a gate can be compared, such as stuck-at faults, and the comparison does not need the rest of the circuit.
- The report needs fault coverage on a standard list. Equivalence collapsing keeps the coverage figure meaningful, since it only merges faults that are detected together. Dominance collapsing changes what the coverage counts, so the report must say which list it uses.

Write $T(f)$ for the set of vectors that detect fault $f$. Faults $f$ and $g$ are **equivalent** when the faulty circuits $C_f$ and $C_g$ have the same output function, which implies $T(f) = T(g)$. Fault $f$ **dominates** $g$ when $T(g) \subseteq T(f)$, so every test of $g$ detects $f$.

## The template

```pseudo id=main
COLLAPSE(C, EQUIV, DOM)
L1  put every fault of C in a class of its own
L2  for each gate G of C do
L3      for each pair (f, g) in EQUIV(G) do merge the classes of f and g
L4  R ← one fault of each class
L5  for each gate G of C do
L6      for each pair (f, g) in DOM(G) with f dominating g do
L7          if the class of g is in R then remove the class of f from R
L8  return R
```

The holes are the local rules. EQUIV(G) and DOM(G) list pairs of faults on the lines of one gate $G$, for gate inputs that feed only $G$:

| gate | EQUIV(G) | DOM(G): the output fault dominates |
|---|---|---|
| AND | each input/0 with output/0 | each input/1, by output/1 |
| NAND | each input/0 with output/1 | each input/1, by output/0 |
| OR | each input/1 with output/1 | each input/0, by output/0 |
| NOR | each input/1 with output/0 | each input/0, by output/1 |
| NOT | input/0 with output/1, input/1 with output/0 | none |
| BUF, branch | input/v with output/v | none |

A fanout stem and its branches are not merged: a fault on one branch changes one path only. A [disjoint-set](/disjoint-set/) structure does lines L1 to L3 in near-linear time. Lines L1 to L4 alone are **equivalence collapsing**, and with lines L5 to L7 the result is **dominance collapsing**. The rules are found from the gate alone, so they give **structural** equivalence. **Functional** equivalence, the same faulty function, can merge more faults, but proving it needs [equivalence checking](/equivalence-checking/) of two faulty circuits.

**Example.** Take $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, with the stem $b$ split into the branches $b_g$ and $b_h$. The 8 lines give 16 faults.

| step | classes |
|---|---|
| L3 at $g$ | {a/0, $b_g$/0, g/1} |
| L3 at $h$ | {$b_h$/0, c/0, h/1} |
| L3 at $z$ | {g/0, h/0, z/1} |
| L4 | these 3 classes and 7 single faults: a/1, b/0, b/1, $b_g$/1, $b_h$/1, c/1, z/0, so 10 classes |
| L7 at $g$ | the class of g/0 dominates a/1: remove {g/0, h/0, z/1} |
| L7 at $z$ | z/0 dominates g/1: remove {z/0} |

So equivalence collapsing keeps 10 of 16 faults, and dominance collapsing keeps 8. The functional classes are 8, not 10: a/1 and c/1 have the same faulty function, $z = b$, and so do b/0 and z/0, which give the constant 0. The gate rules cannot see these, because the faults are on different gates. On the c17 benchmark circuit, the 34 faults collapse to 22 classes, and here the structural and the functional classes are the same.

**The checkpoint theorem.** The checkpoints are the primary inputs and the fanout branches. In a combinational circuit of AND, OR, NAND, NOR, NOT and BUF gates, a test set that detects every single stuck-at fault on the checkpoints detects every single stuck-at fault. The hypothesis needs all checkpoint faults to be detectable, so the theorem says nothing about a circuit with a redundant checkpoint fault. Proof: a line that is not a checkpoint is a gate output, and each input of a gate is a checkpoint or the output of an earlier gate with no fanout. Take a gate $G$ in topological order, and assume that the test set $T$ detects the faults on its inputs. For an AND gate, output/0 is equivalent to input/0, because the input feeds only $G$. A test $t$ of input $a$/1 sets $a = 0$ and must change the output of $G$, since $a$ feeds nothing else, so the circuit with $a$/1 and the circuit with output/1 agree on $t$, and $t$ detects output/1. The other gates are the same up to inversion. So $T$ detects both faults on the output of $G$. In the example, the checkpoints $a, b, b_g, b_h, c$ carry 10 faults, and the equivalences $a/0 = b_g/0$ and $b_h/0 = c/0$ leave the same 8 faults as dominance collapsing. On c17 the 11 checkpoints carry 22 faults.

The theorem needs gates with a controlling value. For $z = \mathrm{XOR}(a, b)$ with the test set {11, 00}, every checkpoint fault a/0, a/1, b/0, b/1 is detected, and so is z/1, but z/0 is not: it needs $z = 1$ in the good circuit, that is, 01 or 10.

## Classic examples

- [Stuck-at fault model](/stuck-at-fault-model/): the $2L$ faults of a circuit with $L$ lines are the list that collapsing shrinks. The checkpoint theorem is one of the basic results of the model.
- [Fault simulation](/fault-simulation/): a simulator runs on the collapsed list and reports coverage on it, which cuts the work in proportion to the number of faults removed.
- [Automatic test pattern generation](/automatic-test-pattern-generation/): ATPG targets one fault of each class. With dominance collapsing it targets the fault that is harder to detect, whose tests also catch the dropped one.
- [SAT sweeping](/sat-sweeping/): the same idea of merging equivalent signals, there applied to the nodes of a circuit, with random simulation to guess classes and SAT to prove them, as for functional fault equivalence.
- [Built-in self-test](/built-in-self-test/): coverage of the random patterns is graded on the collapsed list, so the reported number depends on the list used.

## Variations

- **Functional collapsing.** Merge faults whose faulty circuits are equivalent, proved with [SAT](/sat/) or BDDs on the miter of the two faulty circuits. It merges more, as in the example, at a much higher cost. Random simulation finds candidate pairs first.
- **Collapsing for diagnosis.** In diagnosis the aim is to tell faults apart. Equivalent faults cannot be told apart by any test, so the classes are the best possible resolution. Dominance is not used, since it does not preserve distinguishability.
- **Other fault models.** Transition faults have equivalence rules much like stuck-at faults. Bridging and path delay faults have few local relations, and their lists are pruned by other means, such as layout extraction of likely bridges.
- **Hierarchical collapsing.** Collapse the faults of each library cell once and reuse the classes at every instance of the cell.

## Pitfalls

- **Merging a stem with its branches.** A stem fault changes every branch, a branch fault only one. In the example, b/0 is detected by 011, 110 and 111, but $b_h$/0 only by 011. Treating them as one fault loses tests.
- **Dominance with redundant faults.** If $g$ is undetectable, then $T(g)$ is empty and every fault dominates it, but the tests for $g$ do not exist and cannot detect $f$. Line L7 is safe only when the kept fault $g$ is detectable, or when $f$ is kept if $g$ turns out to be redundant.
- **Dominance in sequential circuits.** In a circuit with state, a test is a sequence, and a dominated fault can mask the dominating one through the state. Dominance collapsing is used for combinational logic or full scan only.
- **XOR gates.** XOR and XNOR have no controlling value, so they have no local equivalence or dominance rule, and the checkpoint theorem fails, as the example shows. Put the output faults of XOR gates on the list.
- **Coverage numbers that are not comparable.** Coverage on the full list, the equivalence list and the dominance list are three different numbers for the same test set. State which list a figure uses.

## Exercises

1. Show that for a two-input AND gate with inputs that have no fanout, the 6 faults collapse to 4 by equivalence and to 3 by dominance. Which 3 vectors test the gate completely?
2. Show that structural equivalence implies functional equivalence, but that the converse fails, using a/1 and c/1 in the example.
3. Find the smallest test set for the example circuit by the table on the [stuck-at fault model](/stuck-at-fault-model/) page and check that it detects all 8 faults of the dominance list.

## References
