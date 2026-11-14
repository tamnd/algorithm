---
tag: WZABZ7
kind: algorithm
slug: transformation-based-reversible-synthesis
name: Transformation-based reversible synthesis
aliases:
- MMD algorithm
- Miller-Maslov-Dueck synthesis
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Miller, Maslov and Dueck's method that walks the truth table in order and adds Toffoli gates to map each row to itself, always ending with a correct circuit.
solves: [reversible-logic-synthesis]
model: word-ram
complexity:
  vars: {n: the number of lines}
  time: {worst: "O(n 4^n)"}
  space: {tables: "O(2^n)", circuit: "O(n 2^n)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2003
  people: [D. Michael Miller, Dmitri Maslov, Gerhard W. Dueck]
  note: A greedy synthesis method for reversible functions that needs no search, always ends with a correct circuit on the given lines, and has a proved bound on the number of gates.
prereqs: [reversible-logic-synthesis, toffoli-gate, cnot-gate]
see_also: [reversible-computation, permutation-parity, hamming-distance, selection-sort, greedy-algorithm, breadth-first-search, quantum-oracle, ancilla-qubits]
sources:
  - paper: doi:10.1145/775832.775915
    title: "D. Michael Miller, Dmitri Maslov and Gerhard W. Dueck, A transformation based algorithm for reversible logic synthesis, Proceedings of the 40th Design Automation Conference (DAC 2003), pages 318 to 323"
    locator: Section 3.1 (the basic algorithm, Table 1 and the function that needs (m - 1) 2^m + 1 gates), Section 3.2 (output permutation and control input reduction), Section 3.3 (the bidirectional algorithm, Table 3), Section 4 (templates), Section 5 and Table 4 (all 40,320 functions of 3 bits)
  - paper: doi:10.1109/TCAD.2005.847911
    title: "Dmitri Maslov, Gerhard W. Dueck and D. Michael Miller, Toffoli network synthesis with templates, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 24(6), 2005, pages 807 to 817"
    locator: Section III (the basic algorithm, Table I, Theorem 1 with the bound (n - 1) 2^n + 1 and the worst-case functions for 3 and 4 bits, Section III.B the bidirectional algorithm), the template sections
  - paper: arxiv:quant-ph/0207001
    title: "Vivek V. Shende, Aditya K. Prasad, Igor L. Markov and John P. Hayes, Synthesis of reversible logic circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 22(6), 2003, pages 710 to 722"
    locator: Table 1 (the number of 3-wire functions whose optimal NOT, CNOT and Toffoli circuit has k gates), as numbered in arXiv version 4
  - paper: doi:10.1145/2431211.2431220
    title: "Mehdi Saeedi and Igor L. Markov, Synthesis and optimization of reversible circuits, a survey, ACM Computing Surveys 45(2), 2013, article 21 (arXiv:1110.2574)"
    locator: Section 4.3 (transformation-based methods and the other heuristics), Section 5 (post-synthesis optimization)
---

Transformation-based synthesis, from Miller, Maslov and Dueck (DAC 2003), builds a circuit of multiple-control [Toffoli gates](/toffoli-gate/) for a reversible function given as a truth table. It reads the rows in increasing order. For row $i$, it adds gates at the outputs that change the current output of that row into $i$, with controls chosen so that the rows already done do not change. When every row maps to itself, the gates, read backward, form a circuit for the function. It needs no search and no extra lines, always ends with a correct circuit, and uses at most $(n - 1) 2^n + 1$ gates on $n$ lines. The bidirectional form also adds gates at the inputs when that is cheaper.

## In plain words

Write the function as a table: input pattern on the left, output pattern on the right, one row per pattern. Change the right column, one gate at a time, until it equals the left column. Then the gates you used, in reverse order, compute the function.

Go down the rows from the top. In the current row, flip the bits that are wrong. Choose each flip so that it fires only on patterns at least as large as this row, so it cannot spoil the rows above, which already match. When you reach the last row it is right by itself, because every other pattern is already used.

## The problem

Given a permutation $f$ of $\{0, \dots, 2^n - 1\}$, a reversible function on $n$ lines, find a circuit of NOT, CNOT, Toffoli and larger Toffoli gates on the same $n$ lines that computes it, with few gates. The [problem page](/reversible-logic-synthesis/) defines the gates and the costs. Here a gate $T(C; t)$ flips line $t$ when every line in the set $C$ is 1, and line $t$ is bit $t$ of the number.

## The algorithm

The algorithm keeps the current table $\mathit{out}$ and its inverse $\mathit{inv}$. A gate $G$ added at the outputs replaces $\mathit{out}$ by $G \circ \mathit{out}$. A gate added at the inputs replaces $\mathit{out}$ by $\mathit{out} \circ G$, which is the same as replacing $\mathit{inv}$ by $G \circ \mathit{inv}$, since every gate is its own inverse. Row $i$ is *done* when $\mathit{out}[i] = i$. Write $d$ for the [Hamming distance](/hamming-distance/) and $\mathrm{ones}(x)$ for the set of lines where $x$ is 1.

```pseudo id=main
SYNTHESIZE(f, bidirectional)
L1  out ← f; inv ← f⁻¹
L2  for i ← 0 to 2^n − 1:
L3      if out[i] = i: continue
L4      if bidirectional and d(i, inv[i]) < d(i, out[i]): a ← inv (gates at the inputs) else a ← out (gates at the outputs); v ← a[i]
L5      for each line t with i_t = 1 and v_t = 0: add the gate T(ones(v); t)
L6      for each line t with i_t = 0 and v_t = 1: add the gate T(ones(i); t)
L7      apply each new gate G to every entry of a, a[x] ← G(a[x]), and recompute the other table as the inverse of a
L8      record the new gates on the chosen side
L9  return the input-side gates in the order found, then the output-side gates in reverse order
```

**Why the controls are safe.** At row $i$, rows $0, \dots, i - 1$ are done, and the tables are bijections, so $v = a[i] \ge i$. A gate of line L5 has the controls $\mathrm{ones}(v)$. It fires on a value $x$ only if $x$ has all bits of $v$, so $x \ge v \ge i$, and the done rows hold values below $i$. The values it meets in row $i$ only gain bits, so they keep all bits of $v$, and it fires there. A gate of line L6 has the controls $\mathrm{ones}(i)$. It fires on $x$ only if $x \ge i$, and after L5 the value of row $i$ has every bit of $i$. In both cases the target is not a control.

**The order of the output gates.** Gates found at the outputs act on the table from outside, so the first one found is the last one the circuit applies. The gates found at the inputs act from inside, so the first one found is the first one applied. Line L9 puts them in this order.

**A slip in the papers.** The text of both papers (DAC 2003, Section 3.1, and TCAD 2005, Section III) gives the gates of line L5 the controls $\mathrm{ones}(i)$, which would contain the target. Their worked examples use $\mathrm{ones}(v)$, as here, and the proof needs it.

**The code** follows the basic algorithm of Section 3.1 with `bidirectional=False`, and the rule of Section 3.3 with `bidirectional=True`: at a tie it takes the outputs. It does not try other output orders, does not reduce the controls, and does not apply templates, the three improvements that the papers add.

## Example

Take $f = [1, 0, 3, 2, 5, 7, 4, 6]$ on lines $a$ (bit 0), $b$ (bit 1) and $c$ (bit 2), the example of Maslov, Dueck and Miller (Table I). The columns show $\mathit{out}$ as $cba$ after each gate of the basic algorithm.

| row $cba$ | $f$ | after NOT($a$) | after $T(c,b; a)$ | after $T(c,a; b)$ | after $T(c,b; a)$ |
|---|---|---|---|---|---|
| 000 | 001 | 000 | 000 | 000 | 000 |
| 001 | 000 | 001 | 001 | 001 | 001 |
| 010 | 011 | 010 | 010 | 010 | 010 |
| 011 | 010 | 011 | 011 | 011 | 011 |
| 100 | 101 | 100 | 100 | 100 | 100 |
| 101 | 111 | 110 | 111 | 101 | 101 |
| 110 | 100 | 101 | 101 | 111 | 110 |
| 111 | 110 | 111 | 110 | 110 | 111 |

Row 0 holds 001, so line L6 clears bit $a$ with no controls: a NOT. Rows 1 to 4 are then done. Row 5 holds $v = 110$ and needs $101$: line L5 sets $a$ with controls $\mathrm{ones}(110) = \{c, b\}$, and line L6 clears $b$ with controls $\mathrm{ones}(101) = \{c, a\}$. Row 6 holds 111 and needs 110: one gate clears $a$ with controls $\{c, b\}$. Row 7 is then done by itself. Read backward, the circuit is $T(c,b; a)$, $T(c,a; b)$, $T(c,b; a)$, NOT($a$), 4 gates, which is optimal for this function.

**The bidirectional form.** For $f(x) = x - 1 \bmod 8$, that is $[7, 0, 1, \dots, 6]$, the basic algorithm needs 3 NOT gates for row 0 alone and 7 gates in all. The bidirectional form sees that $\mathit{inv}[0] = 1$ is one bit from 0, so it adds NOT($a$) at the inputs. Then row 1 holds 7 but $\mathit{inv}[1] = 3$, one bit away, so it adds a CNOT from $a$ to $b$ at the inputs. Row 3 then holds 7, one bit from 3 on both sides, and the tie goes to the outputs: a Toffoli gate with controls $a, b$ and target $c$. The 3 gates are optimal (Miller, Maslov and Dueck, Section 3.3).

## Correctness

The [proof file](proofs/correctness.md) proves the following, for both forms. Each row step maps $v$ to $i$ with $d(v, i)$ gates and fixes every value below $i$. By induction over the rows, the rows above the current one stay done, the two tables stay inverse to each other, and the table always equals $A \circ f \circ B$, where $A$ is the product of the output gates and $B$ that of the input gates. After the last row the table is the identity, so the circuit of line L9 computes $f$. It uses only the $n$ lines of $f$, with no extra line. Every row $i$ costs at most $h(i) + 1$ gates, where $h(i)$ is the position of the highest 0 bit of $i$, and summing over the rows gives at most $(n - 1) 2^n + 1$ gates.

## Complexity

The circuit has at most $(n - 1) 2^n + 1$ gates. Each gate is applied to the $2^n$ entries of one table, and the inverse is rebuilt in $O(2^n)$, so the time is $O(n 2^n \cdot 2^n) = O(n 4^n)$ in the worst case, and $O(2^n)$ times the number of gates in general. The input itself has $n 2^n$ bits. The tables take $O(2^n)$ words, and the circuit $O(n 2^n)$ gates of one word each. Keeping only the table and applying the gates lazily to the rows as they are reached would save time on functions with short circuits; the code does the simple thing.

## Properties

**What is proved.** For every reversible function on $n$ lines, both forms end with a circuit of multiple-control Toffoli gates on the same $n$ lines that computes it, with no extra line, and with at most $(n - 1) 2^n + 1$ gates. The proof file has the details.

**What is cited.** The bound is tight for the basic algorithm: Maslov, Dueck and Miller (Theorem 1) build a function that needs exactly $(n - 1) 2^n + 1$ gates for every $n$, $[7, 1, 4, 3, 0, 2, 6, 5]$ for $n = 3$. Over all 40,320 functions of 3 bits, Miller, Maslov and Dueck (Table 4) report a mean of 8.67 gates for the basic algorithm, 6.53 with output permutation, control reduction and the bidirectional rule, and 6.18 with templates as well, against 5.63 for optimal circuits in a library that also has SWAP gates. Shende et al. (Table 1) give the optimal sizes with NOT, CNOT and Toffoli gates.

**What is measured.** The test file runs both forms on all 40,320 functions of 3 bits and checks every circuit against the truth table. The basic algorithm reproduces the distribution of Table 4, column (a), exactly: a mean of 8.67 gates, and 17 gates for one function. The bidirectional form, without the other improvements, has a mean of 7.37 gates and needs at most 15. A breadth-first search over all functions reproduces Shende et al.'s Table 1, a mean of 5.87 gates and at most 8. The basic algorithm is optimal on 3,484 functions (8.6%) and the bidirectional form on 10,828 (26.9%). On random functions of 4 to 7 lines both forms stay within the bound, and the 4-bit worst case of Maslov, Dueck and Miller takes exactly 49 gates. The test file runs in about 4 seconds.

## Variants and improvements

- **Control input reduction.** Any subset of the controls works if it still fires on the current row and on no done row. The papers pick the subset that most lowers the total Hamming distance of the table, which gives smaller gates and so a lower quantum cost.
- **Output permutation.** Relabel the outputs first, trying all $n!$ orders for small $n$, and keep the smallest circuit; the relabeling is free if wires can be renamed, and costs SWAP gates if not.
- **Templates.** A template is a circuit that computes the identity. When more than half of one appears in the output, it is replaced by the inverse of the rest. Maslov, Dueck and Miller (2005) list all templates with up to 6 gates, and template passes are still used after many synthesis methods.
- **Other gates.** The same idea works with Toffoli gates with negative controls, with Fredkin gates, and with gates that change two lines at once (mEXOR gates), for which Maslov, Dueck and Miller give a variant with $O(2^n)$ gates.
- **Exact and other heuristics.** For 3 and 4 bits, exact search finds optimal circuits, as on the [problem page](/reversible-logic-synthesis/). For larger functions, cycle-based, ESOP-based and BDD-based methods scale further, at the price of extra lines (Saeedi and Markov, Section 4.3).

## When to use it

Use it when the function is given as a truth table, $n$ is at most about 20, and no extra lines are allowed: it always gives a correct circuit on exactly $n$ lines, fast, and it is a good start for template simplification. For 3 or 4 bits, use exact search instead. For functions with many inputs, or when extra lines are cheap, a method that works from an ESOP or a BDD scales better.

## Pitfalls

- **The order of the output gates.** The gates found at the outputs must be reversed. Since every gate is its own inverse this is the only change needed, but forgetting it gives the circuit of a different function.
- **The controls of the gates that set bits.** They must be the 1-bits of the current output $v$, not of $i$; see the slip in the papers above.
- **Large gates.** The basic algorithm gives gates with up to $n - 1$ controls. A gate with many controls costs many elementary gates, or extra lines, on real hardware, so the gate count alone flatters it; use control reduction and count the quantum cost.
- **Odd permutations.** On $n \ge 4$ lines every NOT, CNOT and Toffoli gate is an even permutation, so for an odd permutation the circuit must contain a gate with $n - 1$ controls, or one extra line. The algorithm handles this by itself, since it is free to use any number of controls, but a later step that breaks gates into Toffoli gates must keep this in mind.
- **Irreversible functions.** The function must be a permutation. An irreversible one must first be embedded with constant inputs and garbage outputs, as on the problem page.

## Implementations

## History

Before 2003, synthesis methods for reversible circuits searched over circuits, as Shende, Prasad, Markov and Hayes did for all functions of 3 bits, or built on spectral techniques and on rewriting rules for CNOT and Toffoli circuits, which the DAC paper cites. Miller, Maslov and Dueck presented the transformation-based method at DAC 2003: a greedy pass through the truth table that always ends with a correct circuit, with the bidirectional rule, output permutation, control reduction and templates on top. The journal version (Maslov, Dueck and Miller, TCAD 2005) proved the bound $(n - 1) 2^n + 1$, showed that it is tight, and gave the full set of templates up to 6 gates. Many later methods start from the same idea of transforming the function into the identity.

## References
