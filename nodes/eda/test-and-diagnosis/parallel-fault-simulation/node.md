---
tag: S63TGE
kind: algorithm
slug: parallel-fault-simulation
name: Parallel fault simulation
aliases:
- Seshu parallel fault simulation
- bit-parallel fault simulation
area: eda/test-and-diagnosis
level: core
summary: Simulates the good circuit and w - 1 faulty circuits at once by packing them into the bits of a machine word and evaluating gates with bitwise operations.
solves: [fault-simulation]
model: word-ram
complexity:
  vars: {T: the number of vectors, L: the number of lines, P: the number of gate input pins, F: the number of faults, w: the word size in bits}
  time: {worst: "O(T (F / (w - 1) + 1) (L + P))"}
  space: {extra: O(L + F)}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1965
  people: [Sundaram Seshu]
  note: Textbooks credit Seshu's diagnosis programs of the early 1960s, described in 1965, with simulating several faulty machines in the bits of one word.
prereqs: [fault-simulation, stuck-at-fault-model, bit-parallelism]
see_also: [ppsfp, deductive-fault-simulation, concurrent-fault-simulation, critical-path-tracing, compiled-code-logic-simulation, event-driven-logic-simulation, fault-collapsing, fault-coverage]
sources:
  - paper: "Sundaram Seshu, On an improved diagnosis program, IEEE Transactions on Electronic Computers EC-14(1), 76 to 79, 1965"
    title: S. Seshu, On an improved diagnosis program, IEEE Transactions on Electronic Computers EC-14(1), 76 to 79, February 1965
    locator: the diagnosis program that simulates faulty machines, which later textbooks cite as the origin of parallel fault simulation
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Logic and Fault Simulation (parallel fault simulation, with one faulty circuit per bit and masks that insert the faults)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on fault simulation (parallel fault simulation, fault insertion by masks, and three-valued words)
---

Parallel fault simulation is a method for [fault simulation](/fault-simulation/) that puts the good circuit and $w - 1$ faulty circuits, each with one [single stuck-at fault](/stuck-at-fault-model/), in the $w$ bits of a machine word. Each gate is evaluated once per word with [bitwise operations](/bitwise-operations/), so one pass over the circuit simulates $w - 1$ faults and the good circuit together. Two masks per line put each fault into its own bit. The method gives exactly the answer of serial fault simulation, with about $w - 1$ times fewer gate evaluations.

## In plain words

A computer adds or compares 64 bits in one step. Each bit can hold the value of a wire in a different copy of the circuit. Copy 0 is the good circuit. Copies 1 to 63 each have one wire that is broken.

So the simulator walks through the gates once, as for one circuit, but each step computes the gate in all 64 copies at the same time. Where a copy has its broken wire, a mask forces that bit to the stuck value. At the outputs, each copy is compared with copy 0. A copy that differs shows a break that this input finds.

If there are more broken copies than bits, the simulator does more walks, one group of 63 at a time.

## The problem

The input is a combinational circuit $C$ with $L$ lines in topological order, a list of single stuck-at faults, a sequence of two-valued input vectors, a flag for fault dropping, and the word size $w \ge 2$. The lines are the primary inputs, the gate outputs and the fanout branches, as in the [stuck-at fault model](/stuck-at-fault-model/), and $P$ is the number of gate input pins. The output is, for each vector, the set of faults that it detects among those still simulated. With dropping, a fault is not simulated after the first vector that detects it.

This is the problem of the [fault simulation](/fault-simulation/) page, for combinational circuits. A sequential circuit with [full scan](/scan-design/) gives this problem too.

## The algorithm

A group $G$ holds at most $w - 1$ alive faults. The fault in position $i$ of the group uses bit $i$ of every word, for $1 \le i \le |G|$, and bit 0 holds the good circuit. For a line $k$, the mask $\mathrm{clear}[k]$ has bit $i$ set when fault $i$ is $k$ stuck at 0, and $\mathrm{set}[k]$ has bit $i$ set when fault $i$ is $k$ stuck at 1. A line can have both of its faults in one group, in two different bits.

```pseudo id=main
PARALLEL-FAULT-SIMULATION(C, vectors, faults, drop, w)
    alive ← faults
L1  for each vector t do
L2      for each group G of at most w − 1 faults of alive do
L3          build clear[k] and set[k] for every line k from the faults of G
L4          for each line k in topological order do
L5              if k is a primary input then W ← all ones if t gives k the value 1, else all zeros
L6              else W ← the gate of k applied bitwise to the words of the inputs of k
L7              word[k] ← (W AND NOT clear[k]) OR set[k]
L8          diff ← OR over the primary outputs o of (word[o] XOR bit 0 of word[o] copied into every bit)
L9          report the fault of each set bit i ≥ 1 of diff as detected by t
L10     if drop then remove the detected faults from alive
```

Line L7 is the fault insertion. AND with the complement of the clear mask forces the bits of the stuck-at-0 faults on $k$ to 0, and OR with the set mask forces the bits of the stuck-at-1 faults to 1. The other bits keep the value that the gate computed. The inverting gates NOT, NAND, NOR and XNOR complement with a word of $|G| + 1$ ones, so that unused high bits stay 0. A fanout branch is a buffer of its stem, so a fault on the stem reaches every branch, and a fault on one branch changes only the bit in that branch.

Every line is evaluated in every pass, whatever its value, as in [compiled-code logic simulation](/compiled-code-logic-simulation/). There is no event queue.

## Example

The circuit is $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ into $g$ and $b_h$ into $h$. The 8 lines in topological order are $a, b, b_g, b_h, c, g, h, z$, and there are 16 faults. The code names a branch b>g.

Take $w = 8$ and the vector $abc = 101$. The first group holds the first 7 faults in line order: bit 1 is a/0, bit 2 a/1, bit 3 b/0, bit 4 b/1, bit 5 $b_g$/0, bit 6 $b_g$/1 and bit 7 $b_h$/0. The table writes each word with bit 0 on the left.

| line | $W$ from line L5 or L6 | clear | set | word after L7 |
|---|---|---|---|---|
| $a$ | 11111111 | 01000000 | 00100000 | 10111111 |
| $b$ | 00000000 | 00010000 | 00001000 | 00001000 |
| $b_g$ | 00001000 | 00000100 | 00000010 | 00001010 |
| $b_h$ | 00001000 | 00000001 | 00000000 | 00001000 |
| $c$ | 11111111 | 00000000 | 00000000 | 11111111 |
| $g$ | 11110101 | 00000000 | 00000000 | 11110101 |
| $h$ | 11110111 | 00000000 | 00000000 | 11110111 |
| $z$ | 00001010 | 00000000 | 00000000 | 00001010 |

Bit 0 of $z$ is 0, the good output. Bits 4 and 6 are 1, so line L9 reports b/1 and $b_g$/1. Bit 1, the fault a/0, gives $a = 0$ and $g = 1$, which is the good value of $g$, so the fault does not reach $z$. Bit 7, the fault $b_h$/0, does nothing at all, since $b_h$ is already 0. The second and third groups hold the other 9 faults and report $b_h$/1, g/0, h/0 and z/1, so vector 101 detects 6 faults.

With dropping and $w = 8$, the four vectors 101, 010, 011, 110 see 16, 10, 8 and 3 alive faults, so they take 3, 2, 2 and 1 passes. That is 8 passes of 8 line evaluations, 64 word evaluations in all. Serial fault simulation with dropping simulates 16 + 10 + 8 + 3 = 37 faulty circuits of 8 lines, which is 296 line evaluations. Without dropping, parallel simulation needs 12 passes. With $w = 64$ all 16 faults fit in one group, and each vector takes one pass. The detected sets are those of the table on the [fault simulation](/fault-simulation/) page.

## Correctness

Bitwise operations act on each bit on its own: bit $i$ of $u \mathbin{\&} v$ depends only on bit $i$ of $u$ and of $v$. So the pass of lines L4 to L7 is $|G| + 1$ independent simulations, one per bit, that share their instructions. In bit 0 no mask has a set bit, so it is the good circuit. In bit $i \ge 1$ the masks change only the line of fault $i$, and only to its stuck value, which is the faulty circuit of fault $i$. Lines are taken in topological order, so every input word is final before it is read. Line L8 sets bit $i$ of diff exactly when some output differs between the good circuit and faulty circuit $i$, which is the definition of detection. The groups cover the alive faults, so line L9 reports exactly the alive faults that $t$ detects, and line L10 drops them as serial simulation does. The [full proof](proofs/correctness.md) writes this as an induction over the lines.

## Complexity

A pass evaluates each line once. A gate with $d$ inputs costs $O(d)$ word operations, so a pass costs $O(L + P)$ word operations, plus $O(L + w)$ to build and clear the masks. A vector with $A$ alive faults takes $\lceil A / (w - 1) \rceil$ passes. Over $T$ vectors and $F$ faults, the worst case is $O(T (F / (w - 1) + 1)(L + P))$ word operations, against $O(T F (L + P))$ for serial simulation. The extra space is one word and two masks per line, and the fault list, so $O(L + F)$ words.

This bound is a count of word operations in the word RAM, and the factor $w - 1$ is proved for that count. The time on a real machine is measured, not proved. For the c17 benchmark circuit with 17 lines, its 34 faults and all 32 input vectors in counting order, the code of this page with $w = 64$ makes 32 passes and 544 line evaluations without dropping, and 21 passes and 357 line evaluations with dropping, since every fault is dropped after the 21st vector. These are counts on a 6-gate toy circuit, not benchmark results.

## Properties

- **Exact.** For two-valued vectors on a combinational circuit, the result is the same as serial fault simulation, with or without dropping.
- **Compiled, not event-driven.** Every line is evaluated in every pass, even where no faulty circuit differs from the good one. The cost of a pass does not depend on the activity.
- **Speed-up at most $w - 1$.** The gain over serial simulation comes only from the word width. Dropping helps less than in other methods: when the alive faults fall below $w - 1$, a pass still costs a full walk over the circuit.
- **Sequential circuits.** Each bit can carry its own state from vector to vector, so the method also simulates sequential circuits, where the vectors must be applied in order.
- **Deterministic.** The detected sets do not depend on the order of the faults or on $w$. Only the number of passes does.

## Variants and improvements

- **Three values.** With the values 0, 1 and X, each line holds two words, for example one word for "the value can be 1" and one for "the value can be 0". Each gate then costs a few more word operations, as in [ternary simulation](/ternary-simulation/).
- **Event-driven passes.** A pass can skip a line whose input words did not change since the last pass, as in [event-driven logic simulation](/event-driven-logic-simulation/). For a group of faults that are far apart, few lines change.
- **Fault grouping.** Faults that sit close together are often detected by the same vectors. If one group holds them, the group can empty as a whole when they are dropped, and the event-driven variant has fewer lines to change.
- **Patterns in the bits.** [PPSFP](/ppsfp/) puts $w$ vectors, not $w - 1$ faults, in a word, and follows one fault at a time only as far as its effect goes. The textbooks in the references report it as the faster method for combinational circuits with dropping.
- **Wider words.** Vector registers and graphics processors give words of hundreds of bits. The algorithm does not change, and only $w$ grows.

## When to use it

Use parallel fault simulation when the circuit is small or when the vectors of a sequential circuit must be applied in order, so that patterns cannot share a word. It is also a simple reference that is easy to get right: the masks are the only part that differs from a [compiled-code logic simulator](/compiled-code-logic-simulation/). For combinational circuits and full scan designs, [PPSFP](/ppsfp/), often with [critical path tracing](/critical-path-tracing/) inside fanout-free regions, does less work. For sequential circuits with timing, [concurrent fault simulation](/concurrent-fault-simulation/) evaluates a faulty circuit only where it differs. In all cases [fault collapsing](/fault-collapsing/) first reduces the fault list, and the result gives the [fault coverage](/fault-coverage/) of the vectors.

## Pitfalls

- **Bit 0 is the good circuit.** A group has room for $w - 1$ faults, not $w$. Line L8 compares each bit with a copy of bit 0, not with bit 0 alone.
- **Unused bits.** An inverting gate must complement with a mask of $|G| + 1$ ones. With a full-width complement, a short last group gets 1s in its unused bits, and these can look like detected faults if line L9 does not stop at $|G|$.
- **Insertion after evaluation.** The masks act on the word that the gate computed, at line L7. Inserting them on the input words of the next gate instead puts a stem fault on one branch only.
- **Stem and branch.** A fault on a stem must be inserted on the stem line, and a fault on a branch on that branch line. If the branch lines are not built, the branch faults cannot be simulated.
- **Dropping changes the groups.** After line L10, the faults of the next vector are cut into new groups. The bit of a fault is different from vector to vector, so the report must map bits back to faults through the current group.

## Implementations

## History

Seshu's diagnosis programs of the early 1960s at the University of Illinois simulated faulty machines to build tests and diagnosis data, and the 1965 paper on an improved diagnosis program is the work that textbooks cite for parallel fault simulation. The method was a standard way to simulate faults in the 1960s and 1970s, beside serial simulation. Armstrong (1972) gave [deductive fault simulation](/deductive-fault-simulation/), Ulrich and Baker (1973) gave [concurrent fault simulation](/concurrent-fault-simulation/), and Waicukauski and coauthors (1985) turned the word around, with patterns in the bits, in [PPSFP](/ppsfp/).

## References
