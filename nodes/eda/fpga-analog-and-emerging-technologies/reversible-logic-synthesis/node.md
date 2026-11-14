---
tag: W2MCTV
kind: problem
slug: reversible-logic-synthesis
name: Reversible logic synthesis
aliases:
- reversible circuit synthesis
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Build a circuit of reversible gates, such as Toffoli gates, that computes a given permutation of bit vectors with the fewest gates or quantum cost.
prereqs: [reversible-computation, toffoli-gate, permutation-parity]
see_also: [transformation-based-reversible-synthesis, cnot-gate, ancilla-qubits, quantum-oracle, breadth-first-search, bidirectional-search, sat, qubit-mapping]
sources:
  - paper: arxiv:quant-ph/0207001
    title: "Vivek V. Shende, Aditya K. Prasad, Igor L. Markov and John P. Hayes, Synthesis of reversible logic circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 22(6), 2003, pages 710 to 722"
    locator: "numbered as in arXiv version 4: Lemma 11 (gates on fewer than n wires give even permutations), Theorem 12 (every even permutation is a circuit of NOT, CNOT and Toffoli gates with no extra wire), Corollary 13 (one extra wire for odd permutations), Theorem 33 (every permutation on 3 wires, and O(n 2^n) gates), Corollary 34 (some circuits need a number of gates of the order of n 2^n / log n), Table 1 (the number of 3-wire functions whose optimal circuit has k gates)"
  - paper: doi:10.1145/775832.775915
    title: "D. Michael Miller, Dmitri Maslov and Gerhard W. Dueck, A transformation based algorithm for reversible logic synthesis, Proceedings of the 40th Design Automation Conference (DAC 2003), pages 318 to 323"
    locator: Section 3 (synthesis as the transformation of the function into the identity by gates on the outputs or the inputs), Section 5 and Table 4 (all 40,320 functions of 3 bits)
  - paper: doi:10.1109/TCAD.2005.847911
    title: "Dmitri Maslov, Gerhard W. Dueck and D. Michael Miller, Toffoli network synthesis with templates, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 24(6), 2005, pages 807 to 817"
    locator: Section III and Theorem 1 (the basic algorithm uses at most (n - 1) 2^n + 1 gates, and some function needs that many), the templates that remove gates afterwards
  - paper: doi:10.1145/2431211.2431220
    title: "Mehdi Saeedi and Igor L. Markov, Synthesis and optimization of reversible circuits, a survey, ACM Computing Surveys 45(2), 2013, article 21 (arXiv:1110.2574)"
    locator: Section 2.1 (ancillae, garbage lines and the ceil(log2 M) garbage lines that an irreversible function needs), Section 2.3 (cost models), Section 4.1 (optimal methods, by search and by satisfiability), Section 4.3 (transformation, search, cycle, ESOP and BDD-based heuristics)
  - paper: doi:10.1007/3-540-10003-2_104
    title: "Tommaso Toffoli, Reversible computing, ICALP 1980, Lecture Notes in Computer Science 85, Springer, 1980, pages 632 to 644"
    locator: the realization of every function by Toffoli gates with constant inputs and garbage outputs
---

Reversible logic synthesis takes a reversible Boolean function, a bijection of the $2^n$ bit vectors of length $n$, and builds a cascade of reversible gates that computes it. The usual gates are NOT, [CNOT](/cnot-gate/), the [Toffoli gate](/toffoli-gate/) and their generalization with more controls. The circuit has no fan-out and no feedback: each gate acts on the current values of the $n$ lines and replaces them. The goal is few gates, a low quantum cost, or few extra lines. The problem comes from [reversible computation](/reversible-computation/) and from quantum computing, where every classical subroutine of a quantum algorithm, such as an [oracle](/quantum-oracle/), must be a reversible circuit.

## In plain words

Write the function as a table with $2^n$ rows. Each row has an input pattern of $n$ bits and an output pattern of $n$ bits, and no two rows have the same output, so the table only shuffles the patterns. You have $n$ wires and one kind of move: flip one wire, but only in the rows where some other chosen wires are all 1. Find a short list of moves that turns every input pattern into its output pattern at the same time.

A function that loses information, such as AND, is not a shuffle. Before synthesis it is padded with extra input wires set to constants and extra output wires whose values are not needed, until it becomes one.

## Definition

**Reversible function.** A function $f : \{0, 1\}^n \to \{0, 1\}^n$ that is a bijection. Read each bit vector as a binary number, line 0 as the lowest bit. Then $f$ is a permutation of $\{0, \dots, 2^n - 1\}$, given as the list $[f(0), f(1), \dots, f(2^n - 1)]$. The input has $n 2^n$ bits.

**Gates.** A *multiple-control Toffoli gate* $T(C; t)$ has a set $C$ of control lines and a target line $t \notin C$. It flips line $t$ when every line of $C$ is 1, and changes nothing else:
$$T(C; t)(x) = x \oplus 2^t \text{ if } x_c = 1 \text{ for every } c \in C, \text{ and } x \text{ otherwise}.$$
With $|C| = 0$ it is NOT, with $|C| = 1$ it is CNOT, and with $|C| = 2$ it is the Toffoli gate. Each such gate is its own inverse. On $n$ lines there are $n 2^{n-1}$ of them: $n$ choices of target and $2^{n-1}$ sets of controls. The *NCT library* has only NOT, CNOT and Toffoli, which is $n + n(n-1) + n(n-1)(n-2)/2$ gates on $n$ lines. The *MCT library* has all of them. Other libraries add negative controls (the gate fires when a control is 0), the Fredkin gate (a controlled swap), the Peres gate, or the quantum gates of the NCV library.

**Circuit.** A list of gates $G_1, G_2, \dots, G_k$ on the $n$ lines. It computes $G_k \circ \cdots \circ G_2 \circ G_1$: $G_1$ acts first.

**Problem.** Given $f$ and a library $L$, find a circuit of gates from $L$ that computes $f$ and has the least cost. The decision version asks if a circuit of cost at most $k$ exists.

**Costs.** The gate count is the usual one. The *quantum cost* counts the elementary quantum gates of each gate: a Toffoli gate costs 5 two-qubit gates (the decomposition is on the [Toffoli gate](/toffoli-gate/) page), and a gate with more controls costs more. For fault-tolerant hardware the cost is the number of T gates. The number of lines also counts, since each line is a qubit.

**Irreversible functions.** A function $g : \{0, 1\}^m \to \{0, 1\}^p$ that is not a bijection is first *embedded* in a reversible one: add constant inputs and *garbage* outputs whose values are not used, so that the inputs and outputs have the same number of lines and every output pattern is used once. Let $M$ be the largest number of inputs that $g$ sends to the same output. Then the embedding needs at least $\lceil \log_2 M \rceil$ garbage outputs (Saeedi and Markov, Section 2.1). Proof: the $M$ inputs with the same value of $g$ must get different full output patterns, and they agree on the $p$ outputs of $g$, so they differ only in the garbage bits; $r$ garbage bits take at most $2^r$ values, so $2^r \ge M$.

## Variants

- **Exact or heuristic.** Exact synthesis finds a circuit of least cost and works only for a few lines. Heuristics find some circuit, usually larger, for many more lines.
- **Libraries.** NCT, MCT, MCT with negative controls, MCT with Fredkin gates, or a quantum library such as NCV, where the gates are not all permutations but the whole circuit must be.
- **Cost.** Gate count, quantum cost, T count, depth, or the number of lines.
- **Lines.** *Ancilla-free* synthesis uses exactly $n$ lines. With [ancilla](/ancilla-qubits/) lines that start at 0 and must end at 0, or with garbage lines that may end in any state, larger functions become easy, at the price of qubits.
- **Input form.** A truth table for small $n$, or a compact form such as an exclusive-or sum of products or a decision diagram for large $n$. The truth table grows as $2^n$, so it limits $n$ to about 20.

## Examples

**Decrement on 3 bits.** Take $f(x) = x - 1 \bmod 8$ on lines $a$ (bit 0), $b$ (bit 1) and $c$ (bit 2), that is $f = [7, 0, 1, 2, 3, 4, 5, 6]$. The circuit NOT($a$), then CNOT from $a$ to $b$, then Toffoli with controls $a, b$ and target $c$ computes it. After the NOT, line $a$ holds $\bar a$. The CNOT sets $b$ to $b \oplus \bar a$, which is bit 1 of $x - 1$. The Toffoli flips $c$ when $\bar a (b \oplus \bar a) = \bar a \bar b = 1$, that is when both low bits were 0 and the subtraction borrows from bit 2. So the circuit has 3 gates. No circuit has fewer: $f(0) = 7$ differs from 0 in all three bits, and each gate flips at most one bit of each row. The transformation-based algorithm finds this circuit only in its bidirectional form; its output-only form uses 7 gates here (Miller, Maslov and Dueck, Section 3.3).

**AND.** $g(a, b) = ab$ sends three inputs to 0, so $M = 3$ and the embedding needs $\lceil \log_2 3 \rceil = 2$ garbage outputs. Two inputs and three outputs need one constant input. The Toffoli gate with the constant 0 on its target is such an embedding: $(a, b, 0) \mapsto (a, b, ab)$, with $a$ and $b$ as the garbage.

**A function with no circuit on its own lines.** On 4 lines, let $f$ exchange the patterns 1110 and 1111 and fix the other 14. This is one transposition, an odd permutation. A NOT, CNOT or Toffoli gate on 4 lines is a product of 8, 4 or 2 disjoint transpositions, an even permutation, so every NCT circuit on 4 lines is even (see [parity of a permutation](/permutation-parity/)), and no NCT circuit on 4 lines computes $f$. The MCT gate with controls on lines 1, 2 and 3 and target line 0 computes it in one gate, and with one extra line NCT gates can compute it too.

## Known algorithms

- **Exact search.** A circuit is a path in the graph whose vertices are the permutations and whose edges are the gates, so a [breadth-first search](/breadth-first-search/) from the identity finds an optimal circuit for every function at once. Shende, Prasad, Markov and Hayes (2003) did this for all $8! = 40{,}320$ functions of 3 bits. For 4 bits the space has $16! \approx 2.1 \times 10^{13}$ elements. Golubitsky et al. (2010) stored all optimal circuits of half the length in a hash table and joined two halves, a meet-in-the-middle form of [bidirectional search](/bidirectional-search/), and used the symmetries of the problem to cut the search by a factor of more than 48. Some 4-bit functions need 15 NCT gates (Saeedi and Markov, Section 4.1).
- **Satisfiability.** Encode "there is a circuit of $k$ gates" as a formula, with variables for the controls and the target of each gate and for the values on the lines, and give it to a [SAT](/sat/) solver for $k = 0, 1, 2, \dots$ The first $k$ that is satisfiable is optimal. This works for a few lines and short circuits (Section 4.1).
- **Transformation-based.** [The algorithm of Miller, Maslov and Dueck](/transformation-based-reversible-synthesis/) (DAC 2003) walks the truth table in order and adds gates at the outputs, or at the inputs in the bidirectional form, until each row maps to itself. It always ends, with at most $(n - 1) 2^n + 1$ MCT gates, in time polynomial in $2^n$.
- **Cycle-based.** Write the permutation as a product of cycles and build each cycle, or each pair of disjoint transpositions, from a fixed small circuit. Shende et al. build every even permutation this way from NCT gates.
- **ESOP and decision diagrams.** For functions with many inputs, an exclusive-or sum of products or a [binary decision diagram](/binary-decision-diagram/) of the function gives one Toffoli gate per term or a few gates per node, with extra lines. These scale to large functions but add many lines (Section 4.3).
- **Templates.** After synthesis, rewrite rules replace a part of a circuit by a shorter equal one. A *template* is a circuit that computes the identity; when a long part of a template appears in the circuit, it is replaced by the inverse of the short rest (Maslov, Dueck and Miller, 2005).

## Bounds

**Which functions have a circuit.** Every gate is a bijection, so every circuit computes a reversible function. On $n \ge 4$ lines every NOT, CNOT and Toffoli gate is an even permutation, as in the example above, so NCT circuits with no extra line compute only even permutations (Shende et al., Lemma 11). They compute all of them (Theorem 12), and every odd permutation with one extra line (Corollary 13). On 3 lines or fewer, every permutation has an NCT circuit (Theorem 33). The MCT library computes every permutation on $n$ lines, as the transformation-based algorithm shows by construction.

**Lower bounds.** Each gate flips at most one bit of each row, so a circuit for $f$ has at least $\max_x d(x, f(x))$ gates, where $d$ is the Hamming distance. A counting argument gives the worst case. There are at most $(n 2^{n-1} + 1)^k$ MCT circuits of at most $k$ gates (each position holds a gate or nothing), and there are $(2^n)!$ functions, so some function needs
$$k \ge \frac{\log_2 (2^n)!}{\log_2 (n 2^{n-1} + 1)} \ge \frac{2^n (n - \log_2 e)}{n + \log_2 n}$$
MCT gates, using $k! \ge (k/e)^k$. This is $2^n (1 - o(1))$. The same count with the $O(n^3)$ NCT gates gives a bound of the order of $n 2^n / \log n$ NCT gates (Shende et al., Corollary 34).

**Upper bounds.** The transformation-based algorithm uses at most $(n - 1) 2^n + 1$ MCT gates, and the bound is tight for that algorithm (Maslov, Dueck and Miller, Theorem 1; the proof is on the [algorithm page](/transformation-based-reversible-synthesis/)). Every even permutation has an NCT circuit of $O(n 2^n)$ gates (Shende et al., Theorem 33), within a factor $O(\log n)$ of the lower bound.

**Three bits.** Every function of 3 bits has an NCT circuit of at most 8 gates. The numbers of functions whose optimal circuit has $0, 1, \dots, 8$ gates are 1, 12, 102, 625, 2,780, 8,921, 17,049, 10,253 and 577, a mean of 5.87 gates (Shende et al., Table 1). On 3 lines the NCT and MCT libraries are the same 12 gates. The test file of the [transformation-based page](/transformation-based-reversible-synthesis/) finds the same numbers by breadth-first search.

**Hardness.** The exact methods above search a space of $(2^n)!$ functions or of all circuits up to a length, which grows much faster than the size $n 2^n$ of the truth table. The sources of this page give no exact method that runs in time polynomial in $n 2^n$, and no proof that the minimum gate count problem is NP-hard.

## Reductions

**To shortest paths.** Optimal synthesis with gate count is the shortest path from the identity to $f$ in the graph on the $(2^n)!$ permutations whose edges are the gates of the library. Since every gate is its own inverse, the graph is undirected, and the distance of $f$ equals that of $f^{-1}$.

**To satisfiability.** As in Known algorithms: for each $k$, a formula with one copy of the lines per gate and one constraint per row of the truth table is satisfiable exactly when a circuit of $k$ gates exists.

**From irreversible functions.** The embedding above turns synthesis of any multiple-output function into reversible synthesis with $\lceil \log_2 M \rceil$ or more garbage outputs. [Bennett's method](/reversible-computation/) and [uncomputation](/uncomputation/) turn a garbage output back into a constant at the cost of more gates.

## Applications

- **Quantum oracles.** Grover's search and many other quantum algorithms call a classical function as a reversible circuit on qubits, $|x\rangle|y\rangle \mapsto |x\rangle|y \oplus g(x)\rangle$. Its gates are then decomposed into Clifford and T gates and mapped onto the hardware by [qubit mapping](/qubit-mapping/).
- **Quantum arithmetic.** The adders and multipliers inside [modular exponentiation](/quantum-modular-exponentiation/) for Shor's algorithm are reversible circuits, and their gate and line counts set the size of the quantum computer.
- **Low-power and emerging logic.** Landauer's principle ties the erasure of a bit to dissipated heat. Reversible logic erases nothing, which was the first reason to study it, and it is used in proposals for adiabatic CMOS, optical and other emerging technologies.

## References
