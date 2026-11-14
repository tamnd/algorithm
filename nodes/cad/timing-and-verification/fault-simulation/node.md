---
tag: 7ZXSNC
kind: problem
slug: fault-simulation
name: Fault simulation
aliases:
- fault grading
area: cad/timing-and-verification
level: core
summary: Given a circuit, a fault list and test vectors, find which faults each vector detects, to measure fault coverage and drop detected faults.
prereqs: [stuck-at-fault-model]
see_also: [concurrent-fault-simulation, fault-collapsing, automatic-test-pattern-generation, built-in-self-test, event-driven-simulation, bit-parallelism, circuit-value-problem]
sources:
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Logic and Fault Simulation (serial, parallel, deductive and concurrent fault simulation, fault dropping and fault coverage)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on fault simulation (the methods, their comparison and fault sampling)
  - paper: doi:10.1109/T-C.1972.223542
    title: D. B. Armstrong, A deductive method for simulating faults in logic circuits, IEEE Transactions on Computers C-21(5), 464 to 471, 1972
    locator: deductive fault simulation, with the fault list of each line computed from the lists of its inputs by set operations
  - paper: "Ernst G. Ulrich and T. Baker, The concurrent simulation of nearly identical digital networks, Proceedings of the 10th Design Automation Workshop, 145 to 150, 1973"
    title: E. G. Ulrich and T. Baker, The concurrent simulation of nearly identical digital networks, Proceedings of the 10th Design Automation Workshop, 145 to 150, 1973
    locator: concurrent fault simulation
  - paper: "Sundaram Seshu, On an improved diagnosis program, IEEE Transactions on Electronic Computers EC-14(1), 76 to 79, 1965"
    title: S. Seshu, On an improved diagnosis program, IEEE Transactions on Electronic Computers EC-14(1), 76 to 79, February 1965
    locator: an early program that simulates faulty machines to build tests and diagnosis data
---

Fault simulation is the problem of finding which faults of a fault list a given sequence of test vectors detects. Its input is a circuit, a list of faults, usually [single stuck-at faults](/stuck-at-fault-model/), and the vectors; its output is, for each fault, the vectors that detect it, or the first one. The fraction of faults detected is the fault coverage of the test set, and computing it is called fault grading. Each single instance is easy, two runs of the circuit, but the number of faults times the number of vectors makes it one of the most expensive steps of test.

## In plain words

You have a circuit, a list of ways it can break, and a list of inputs to try on the tester. For each break, you want to know if some input on the list would show it: the broken circuit gives an output that differs from the good circuit.

The simple way is to build each broken circuit in software and run it on every input. That is correct but slow, since there can be a million breaks and a million inputs.

Most of the work is the same for many breaks, and once a break is seen there is no need to look at it again. Fast methods use both facts. The result tells how good the test inputs are, and which breaks still need a new input.

## Definition

Let $C$ be a circuit with primary inputs $x_1, \ldots, x_n$ and outputs $z_1, \ldots, z_m$, and let $\Phi$ be a list of faults. Each $f \in \Phi$ gives a faulty circuit $C_f$. The test sequence is $t_1, \ldots, t_T \in \{0, 1\}^n$.

For a combinational circuit, the output is the detection matrix

$$D[i][f] = [\, C(t_i) \ne C_f(t_i) \,], \qquad 1 \le i \le T,\ f \in \Phi,$$

where $C(t)$ is the vector of output values. With **fault dropping**, the output is only the first index $\mathrm{first}(f) = \min\{i : D[i][f] = 1\}$, or $\infty$. The **fault coverage** of the sequence is

$$\mathrm{FC} = \frac{|\{f \in \Phi : \mathrm{first}(f) < \infty\}|}{|\Phi|}.$$

For a sequential circuit, $C(t_i)$ means the outputs at clock cycle $i$, from a given initial state, and the faulty machine has the fault on every cycle. A fault whose faulty machine has an unknown output where the good one is known is only "potentially detected", and is counted apart.

## Variants

- **With or without dropping.** Grading needs only $\mathrm{first}(f)$. Diagnosis and test compaction need the full matrix, or at least $k$ detections per fault for $n$-detect tests.
- **Fault dictionary.** For diagnosis, store for each fault the full output response, not just "detected", so that the response of a failing chip can be matched against the list.
- **Combinational or sequential.** With full [scan design](/scan-design/), the circuit seen by test is combinational and the vectors are independent. A sequential circuit needs the state from cycle to cycle, and the order of the vectors matters.
- **Other fault models.** Transition faults need pairs of vectors, bridging faults need values of two lines, and delay faults need timing.
- **Fault sampling.** Simulate a random sample of $\Phi$ and estimate the coverage, with a confidence interval from the sample size.

## Examples

Take $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, with the stem $b$ split into the branches $b_g$ and $b_h$, and all 16 single stuck-at faults. The test sequence is 101, 010, 011, 110, with dropping.

| $i$ | $t_i$ | good $z$ | faults with $\mathrm{first}(f) = i$ | coverage |
|---|---|---|---|---|
| 1 | 101 | 0 | b/1, $b_g$/1, $b_h$/1, g/0, h/0, z/1 | 6/16 |
| 2 | 010 | 0 | a/1, c/1 | 8/16 |
| 3 | 011 | 1 | b/0, $b_h$/0, c/0, h/1, z/0 | 13/16 |
| 4 | 110 | 1 | a/0, $b_g$/0, g/1 | 16/16 |

Without dropping, vector 010 also detects g/0, h/0 and z/1, and vector 110 also detects b/0 and z/0, so the matrix has 21 ones, not 16. The coverage reaches 100%, and no shorter sequence does it. The curve of coverage against the number of vectors is typical in shape: the first vectors detect many faults, and the last ones are needed for few hard faults.

For a redundant fault, such as $r$ stuck at 0 in $z = \mathrm{OR}(ab, \bar{a}c, bc)$ with the AND gate $r = bc$, the column of the matrix is zero for every sequence. Fault simulation alone cannot tell such a fault from one that the sequence misses. That needs [ATPG](/automatic-test-pattern-generation/).

## Known algorithms

- **Serial fault simulation.** Simulate the good circuit and each $C_f$ on its own. It is the reference method and costs $O(T |\Phi| (L + P))$ for $L$ lines and $P$ gate input pins.
- **Parallel fault simulation.** Put the good circuit and $w - 1$ faulty circuits in the $w$ bits of a machine word, and evaluate each gate with [bitwise operations](/bitwise-operations/), which divides the work of serial simulation by about $w$.
- **Parallel pattern single fault propagation.** For combinational circuits, put $w$ vectors in a word, simulate the good circuit, and for each fault simulate forward from the fault site only until the difference dies out.
- **Deductive fault simulation** (Armstrong, 1972). Compute the set of faults that differ on each line from the sets of its inputs by set operations, in one pass per vector.
- **[Concurrent fault simulation](/concurrent-fault-simulation/)** (Ulrich and Baker, 1973). Keep a list of differing faulty circuits on each line, and evaluate a faulty circuit only where it differs, with [event-driven simulation](/event-driven-simulation/).
- **Critical path tracing.** For fanout-free regions, trace back from the outputs the lines whose value change would change an output. Faults on these lines at the opposite value are detected.

## Bounds

Every method above computes the same answer, and in the worst case each costs $O(T |\Phi| (L + P))$, since one vector and one fault can make every line differ. For the full list of $2L$ stuck-at faults, this is $O(T L (L + P))$. The output of the version without dropping has $T |\Phi|$ bits, which is a lower bound for that version. For one fault and one vector, the problem is as hard as evaluating the circuit, which is the reduction below.

All speed-up claims among the methods are measured on benchmark circuits, not proved. Textbooks report that parallel pattern methods are fast for combinational circuits, that concurrent methods are the usual choice for sequential circuits with timing, and that dropping removes most of the work once most faults are detected. These depend on the circuit and the test set.

## Reductions

- **From the [circuit value problem](/circuit-value-problem/).** Given a circuit and an input, add the fault "output stuck at 0". The input detects this fault exactly when the output is 1. So one instance of fault simulation, with one fault and one vector, is P-complete under log-space reductions, as circuit value is.
- **To circuit evaluation.** Each pair (vector, fault) takes two evaluations of a circuit, so the problem is in P, with the cost given above.
- **From ATPG for small circuits.** Fault simulation of all $2^n$ input vectors decides detectability of every fault, which is the brute force reference for [ATPG](/automatic-test-pattern-generation/) when $n$ is small.

## Applications

- **Fault grading.** Measure the coverage of a test set, the main figure of test quality.
- **ATPG loops.** After ATPG finds a test for one fault, fault simulation of that test drops all the other faults it detects, so ATPG targets each remaining fault only.
- **Test compaction.** Simulating the tests in reverse order shows which tests detect no fault that later tests miss, and these can be removed.
- **[Built-in self-test](/built-in-self-test/).** Grade the coverage of pseudorandom patterns, and find the hard faults that need test points or stored seeds.
- **Diagnosis.** Compare the responses of a failing chip with a fault dictionary, or simulate candidate faults, to find where the defect is.

## References
