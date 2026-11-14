---
tag: THPQ1N
kind: algorithm
slug: ppsfp
name: Parallel-pattern single-fault propagation
aliases:
- PPSFP
area: eda/test-and-diagnosis
level: core
summary: Waicukauski and coauthors' fault simulator that packs many test patterns into a word and propagates one fault at a time only as far as it differs from good values.
solves: [fault-simulation]
model: word-ram
complexity:
  vars: {T: the number of vectors, L: the number of lines, P: the number of gate input pins, F: the number of faults, w: the word size in bits}
  time: {worst: "O((T / w + 1) (1 + F) (L + P))"}
  space: {extra: O(L + F)}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1985
  people: [John A. Waicukauski, Edward B. Eichelberger, Donato O. Forlenza, Eric Lindbloom, Thomas McCarthy]
  note: Waicukauski and coauthors at IBM described fault simulation with many patterns per word and one fault at a time for scan designs in 1985.
prereqs: [fault-simulation, stuck-at-fault-model, bit-parallelism]
see_also: [parallel-fault-simulation, critical-path-tracing, deductive-fault-simulation, concurrent-fault-simulation, event-driven-logic-simulation, compiled-code-logic-simulation, transition-fault-model, scan-design]
sources:
  - paper: "J. A. Waicukauski, E. B. Eichelberger, D. O. Forlenza, E. Lindbloom and T. McCarthy, Fault simulation for structured VLSI, VLSI Systems Design 6(12), 20 to 32, December 1985"
    title: J. A. Waicukauski, E. B. Eichelberger, D. O. Forlenza, E. Lindbloom and T. McCarthy, Fault simulation for structured VLSI, VLSI Systems Design 6(12), 20 to 32, December 1985
    locator: the fault simulator for scan designs with many patterns per word and one fault propagated at a time
  - paper: "J. A. Waicukauski, E. B. Eichelberger, D. O. Forlenza, E. Lindbloom and T. McCarthy, A statistical calculation of fault detection probabilities by fast fault simulation, Proceedings of the International Test Conference, 779 to 784, 1985"
    title: J. A. Waicukauski, E. B. Eichelberger, D. O. Forlenza, E. Lindbloom and T. McCarthy, A statistical calculation of fault detection probabilities by fast fault simulation, Proceedings of the International Test Conference, 779 to 784, 1985
    locator: the same group's fast fault simulator, used to estimate detection probabilities of random patterns
  - paper: doi:10.1109/MDT.1987.295104
    title: J. A. Waicukauski, E. Lindbloom, B. K. Rosen and V. S. Iyengar, Transition fault simulation, IEEE Design and Test of Computers 4(2), 32 to 38, April 1987
    locator: the transition fault model and its simulation by parallel-pattern single-fault propagation
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Logic and Fault Simulation (parallel pattern single fault propagation)
---

Parallel-pattern single-fault propagation, or PPSFP, is a method for [fault simulation](/fault-simulation/) of combinational circuits. It puts $w$ input vectors in the $w$ bits of a machine word and simulates the good circuit once for all of them. Then it takes one [single stuck-at fault](/stuck-at-fault-model/) at a time, sets its line to the stuck value in all $w$ bits, and evaluates forward only the gates where the faulty word still differs from the good word. The bits where an output differs are the vectors that detect the fault.

## In plain words

A computer word holds 64 bits, so it can hold one wire's value for 64 different inputs at once. The simulator first runs the good circuit on 64 inputs together.

Then it takes the breaks one by one. For a break, it changes the broken wire and looks only at the gates just after it. If the gate output is the same as in the good circuit for all 64 inputs, the break is hidden there, and the walk stops on that side. If it differs, the walk goes on to the next gates.

When the walk reaches an output, the bits that differ show which of the 64 inputs find the break. Most breaks die out after a few gates, so most walks are short.

## The problem

The input is a combinational circuit $C$ with $L$ lines in topological order, a list of single stuck-at faults, a sequence of $T$ two-valued input vectors, a flag for fault dropping, and the word size $w \ge 1$. The lines are the primary inputs, the gate outputs and the fanout branches, and $P$ is the number of gate input pins. The output is, for each vector, the set of faults that it detects among those still simulated. With dropping, a fault is reported only at the first vector that detects it.

The vectors must be independent of each other, which holds for a combinational circuit and for a sequential circuit with [full scan](/scan-design/), where each vector is applied from a scanned-in state.

## The algorithm

A block is $w$ consecutive vectors, and bit $i$ of every word stands for vector $i$ of the block. For a word $u$, the lowest set bit is the first vector of the block in which $u$ has a 1.

```pseudo id=main
PPSFP(C, vectors, faults, drop, w)
    alive ← faults
L1  for each block B of w consecutive vectors do
L2      good[k] ← the word of line k in the good circuit on B, for every line k in topological order
L3      for each fault f = (ℓ, v) in alive do
L4          seen ← PROPAGATE(f): set the word of ℓ to v in every bit, evaluate the lines after ℓ in topological order, and keep a faulty word for a line only where it differs from good; seen is the OR over the primary outputs of faulty word XOR good word
L5          if seen = 0 then keep f for the next block
L6          else if drop then report f at the vector of the lowest set bit of seen, and do not keep f; else report f at the vector of every set bit of seen, and keep f
L7      alive ← the kept faults
```

Line L4 is a single fault simulation of a whole block. It starts at the fault site, and if the stuck word equals the good word of $\ell$, no vector of the block activates the fault and nothing is evaluated. Otherwise it schedules the fanouts of $\ell$. When a scheduled line is taken, its gate is evaluated on words: the faulty word for an input that has one, and the good word for the others. If the result equals the good word of the line, the difference has died there, and the fanouts are not scheduled. Taking the scheduled line with the smallest index first is a topological order, as in [event-driven logic simulation](/event-driven-logic-simulation/) with zero delay, so each line is evaluated at most once per fault. Line L2 is plain [compiled-code logic simulation](/compiled-code-logic-simulation/) on words.

## Example

The circuit is $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ into $g$ and $b_h$ into $h$, so there are 8 lines and 16 faults. The four vectors 101, 010, 011, 110 fill one block with $w = 4$. Each word below lists the bits in vector order, bit 0 on the left.

| line | $a$ | $b$, $b_g$, $b_h$ | $c$ | $g$ | $h$ | $z$ |
|---|---|---|---|---|---|---|
| good word | 1001 | 0111 | 1010 | 1110 | 1101 | 0011 |

Take b/1. The stuck word 1111 differs from 0111, so $b_g$ and $b_h$ get 1111. Then $g = \mathrm{NAND}(1001, 1111) = 0110$, which differs from 1110 in bit 0, and $h = \mathrm{NAND}(1111, 1010) = 0101$, which differs from 1101 in bit 0. Then $z = \mathrm{NAND}(0110, 0101) = 1011$ against 0011, so seen = 1000: only vector 101 detects b/1. That walk made 5 gate evaluations. The fault g/0 needs one: $g$ becomes 0000, and $z = \mathrm{NAND}(0000, 1101) = 1111$, so seen = 1100. The fault z/0 needs none: $z$ is an output, and seen = 0011 at once.

| fault | seen | fault | seen | fault | seen | fault | seen |
|---|---|---|---|---|---|---|---|
| a/0 | 0001 | $b_g$/0 | 0001 | c/0 | 0010 | h/0 | 1100 |
| a/1 | 0100 | $b_g$/1 | 1000 | c/1 | 0100 | h/1 | 0010 |
| b/0 | 0011 | $b_h$/0 | 0010 | g/0 | 1100 | z/0 | 0011 |
| b/1 | 1000 | $b_h$/1 | 1000 | g/1 | 0001 | z/1 | 1100 |

With dropping, each fault is reported at its lowest set bit, which gives the same first vectors as the table on the [fault simulation](/fault-simulation/) page. The ones in this table are the 21 detections without dropping. The 16 walks make 30 gate evaluations on words, plus 5 for the good circuit. Serial fault simulation of the same four vectors evaluates the 5 lines that are not inputs once per faulty circuit and vector, which is 320 evaluations without dropping.

## Correctness

Bitwise operations act on each bit on its own, so the good words of line L2 hold the good value of every line under every vector of the block. For one fault, a line that is never assigned a faulty word has all its inputs at their good words, so its faulty word is the good word, and skipping it loses nothing. A line that is evaluated has all its inputs final, because the lines are taken in increasing index and every input has a smaller index. So when line L4 ends, the faulty word of every line is correct, and bit $i$ of seen is 1 exactly when some output differs under vector $i$. Line L5 keeps exactly the faults that the block does not detect. With dropping, a fault reaches a block only if no earlier block detected it, so the lowest set bit is the first vector that detects it. The [full proof](proofs/correctness.md) gives the details.

## Complexity

A block costs $O(L + P)$ word operations for the good circuit. A walk evaluates each line at most once, and a gate with $d$ inputs costs $O(d)$ word operations, so a walk costs $O(L + P)$ in the worst case. With a bucket of scheduled lines per level, or a bit per line and a scan in index order, the scheduling adds no more than this. The code of this page uses a binary heap, which adds a factor $\log L$. There are $\lceil T / w \rceil$ blocks, so the worst case is $O((T / w + 1)(1 + F)(L + P))$ word operations for $F$ faults. The extra space is a good word per line, the faulty words of one walk and the fault list, $O(L + F)$.

This worst case is the same as serial fault simulation divided by $w$. The gains beyond it are measured, not proved. A walk stops where the difference dies, and most faults are dropped in the first blocks, so the total is often far below the bound. For the c17 benchmark circuit with its 34 faults and all 32 input vectors in one 64-bit block, the code of this page makes 34 walks and 128 gate evaluations on words. These are counts on a 6-gate toy circuit, not benchmark results.

## Properties

- **Exact.** For two-valued vectors on a combinational circuit, the result is the same as serial fault simulation, with or without dropping.
- **Activity-driven.** A walk costs only the lines where the fault makes a difference for at least one vector of the block.
- **Combinational only.** The bits of a word are different vectors, so they cannot carry a state from one vector to the next. Sequential circuits need full scan or another method.
- **Faults one at a time.** The memory holds the good words and one walk, whatever the number of faults. Faults are independent, so the fault list can be split over several processors.
- **Dropping at block size.** A fault that is detected in a block is still simulated for all $w$ vectors of that block. Dropping takes effect from the next block.

## Variants and improvements

- **Stem faults and fanout-free regions.** Inside a fanout-free region, the vectors that detect a fault follow from those of the root of the region by [critical path tracing](/critical-path-tracing/) on words. So only the stems need walks, and the faults inside each region are found by a backward pass. Fault simulators for scan designs often combine PPSFP with this.
- **Transition faults.** Waicukauski, Lindbloom, Rosen and Iyengar used PPSFP to simulate [transition faults](/transition-fault-model/) with pairs of vectors: the first vector of a pair sets the initial value, and the second acts as a stuck-at test under the condition that the line changes.
- **Three values.** With unknown values, each line holds two words. The walk compares both words with the good ones.
- **Parallel faults and patterns.** [Parallel fault simulation](/parallel-fault-simulation/) puts faults in the bits instead. A word can also hold a few faults times a few patterns, which helps when few faults are alive.

## When to use it

Use PPSFP to grade large sets of vectors for combinational circuits and full scan designs, and inside the loop of [automatic test pattern generation](/automatic-test-pattern-generation/), where each new test is simulated against all faults that are still alive. It also grades the pseudorandom patterns of [built-in self-test](/built-in-self-test/), where the number of vectors is large and the coverage curve matters. For sequential circuits applied without scan, and for fault models with many logic values and timing, [concurrent fault simulation](/concurrent-fault-simulation/) fits better. The result gives the [fault coverage](/fault-coverage/) of the vectors.

## Pitfalls

- **Unused bits in the last block.** A last block with fewer than $w$ vectors must use a mask of that many ones for inverting gates. Otherwise the unused bits of the good and faulty words may differ and report detections at vectors that do not exist.
- **Comparing too early.** A walk may stop only where the faulty word equals the good word in every bit. Stopping when one bit agrees loses the vectors that still differ.
- **Wrong order of evaluation.** A line evaluated before one of its inputs has its final faulty word uses a stale value. A stack or a plain queue does not give a topological order, so take the scheduled line of smallest index or level.
- **Dropping within a block.** Report the lowest set bit as the first detection. Reporting the highest, or the first bit found by a scan from the top, gives a later vector than serial simulation.
- **Faults at the fault site only.** A stem fault must start on the stem line and reach every branch. A branch fault must start on its branch. If the stem and its branches share one line, the branch faults are lost.

## Implementations

## History

Waicukauski, Eichelberger, Forlenza, Lindbloom and McCarthy at IBM described the method for structured designs with scan in 1985, in the trade journal VLSI Systems Design and in a paper at the International Test Conference on estimating detection probabilities. The later literature calls it parallel pattern single fault propagation. Waicukauski, Lindbloom, Rosen and Iyengar applied it to transition faults at the International Test Conference of 1986 and in IEEE Design and Test in 1987. The method, often with critical path tracing inside fanout-free regions, became a standard fault simulator for scan-based combinational test.

## References
