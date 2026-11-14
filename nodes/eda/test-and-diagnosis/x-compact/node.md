---
tag: B2D4SQ
kind: technique
slug: x-compact
name: X-Compact
aliases:
- X-tolerant response compaction
area: eda/test-and-diagnosis
level: research
summary: Mitra and Kim's combinational space compactor of scan outputs built from an XOR matrix that still detects errors when some outputs carry unknown X values.
prereqs: [parity-check-matrix, scan-design]
see_also: [multiple-input-signature-register, embedded-deterministic-test, broadcast-scan, hamming-code, syndrome, hamming-weight, binomial-coefficient, ternary-simulation]
sources:
  - paper: doi:10.1109/TCAD.2004.823341
    title: Subhasish Mitra and Kee Sup Kim, X-Compact, an efficient response compaction technique, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 23(3), 421 to 432, 2004
    locator: the X-compact matrix, the conditions for detecting errors with and without unknown values, the constructions from columns of equal odd weight, and diagnosis from the compacted outputs
  - paper: "S. Mitra and K. S. Kim, X-Compact: an efficient response compaction technique for test cost reduction, Proceedings of the International Test Conference, 311 to 320, 2002"
    title: S. Mitra and K. S. Kim, X-Compact, an efficient response compaction technique for test cost reduction, Proceedings of the International Test Conference, 311 to 320, 2002
    locator: the first presentation of X-Compact
  - book: isbn:9780123705976
    title: Laung-Terng Wang, Cheng-Wen Wu and Xiaoqing Wen, VLSI Test Principles and Architectures, Morgan Kaufmann, 2006
    locator: the chapter Test Compression (space compaction of responses with unknown values, and X-masking)
---

X-Compact reduces the $n$ scan chain outputs of a chip to $m$ tester outputs with a network of XOR gates, chosen so that errors are still seen when some chain outputs are unknown values (X). Mitra and Kim (2002, 2004) describe the network by an $m \times n$ binary matrix $H$: output $r$ is the XOR of the chains $i$ with $H_{r,i} = 1$. An error vector $e$ on the chains at one shift cycle shows up as $He$ on the outputs, as in a [parity-check matrix](/parity-check-matrix/). An X on chain $j$ makes every output that reads chain $j$ unknown, so the tester ignores those outputs in that cycle. The compactor has no memory, so an X spoils only one cycle of a few outputs, unlike a [MISR](/multiple-input-signature-register/), where one X spoils the whole signature. The choice of columns decides what is detected: distinct columns of odd weight catch any one, two or any odd number of errors, and columns of which none is covered by another catch any single error in the presence of one X.

## In plain words

A chip has hundreds of test chains, but the tester has only a few pins to read them. X-Compact mixes the chain outputs together with XOR gates, so each pin shows the XOR of a fixed group of chains, and each chain feeds a few pins.

A wrong bit in one chain flips every pin it feeds. Some chain bits are unknown, for example from memory that was never written, and an unknown bit makes every pin it feeds unreadable for that cycle. The trick is to wire each chain to a group of pins that no other chain fully covers. Then, if one chain is unknown and another is wrong, the wrong one still flips a pin that the unknown one does not touch.

## When it applies

- The design has many scan chains, possibly fed by a decompressor such as [EDT](/embedded-deterministic-test/) or [broadcast scan](/broadcast-scan/), and too few tester pins to read them all.
- Some response bits are unknown, from uninitialized memories, bus contention, false paths or analog blocks, and they cannot all be removed by design. The values are computed in three-valued simulation, as in [ternary simulation](/ternary-simulation/), so the tester knows where the X's are.
- Errors are expected in few chains per cycle, which holds for one defect in a design whose chains are mixed well.
- A memoryless compactor is wanted, so that every cycle can be read and diagnosed on its own.

## The template

Let the chain outputs at one shift cycle be $y_1, \ldots, y_n \in \{0, 1, X\}$ and the expected values $g_1, \ldots, g_n$.

```pseudo id=main
X-COMPACT-CYCLE(H, the chain outputs y_1, ..., y_n)
L1  for r ← 1 to m do
L2      if some chain i with H[r][i] = 1 has y_i = X then z_r ← X
L3      else z_r ← XOR of y_i over the chains i with H[r][i] = 1
L4  return z_1, ..., z_m                       ▷ the tester compares every z_r ≠ X
```

The holes are the matrix $H$ (its number of rows $m$, the weight of each column and which columns are used) and the handling of cycles with too many X's. In hardware, lines L2 and L3 are one XOR tree per output; the X in line L2 is not a value but the tester's knowledge, from simulation, that this output is unknown.

**What is detected.** Let $E$ be the set of chains with an error at one cycle and $S$ the set of chains with an X, disjoint from $E$. Write $h_i$ for column $i$ of $H$ and $\mathrm{supp}(h)$ for its set of ones. The outputs that the tester reads are those outside $U = \bigcup_{j \in S} \mathrm{supp}(h_j)$, and on them the faulty values differ from the good ones by $\bigoplus_{i \in E} h_i$. So the errors are detected exactly when $\bigoplus_{i \in E} h_i$ has a 1 outside $U$. From this:

1. **No X.** A single error is detected when its column is not zero. Any two errors are detected exactly when all columns are distinct, since $h_i \oplus h_j = 0$ means $h_i = h_j$. If every column has odd [Hamming weight](/hamming-weight/), any odd number of errors is detected, since a sum of an odd number of odd-weight vectors has odd weight and is not zero.
2. **One X.** A single error on chain $i$ with one X on chain $j \ne i$ is detected exactly when $\mathrm{supp}(h_i) \not\subseteq \mathrm{supp}(h_j)$, since the error shows on the outputs of $h_i$ outside those of $h_j$. So the compactor detects every single error with up to one X exactly when no column is covered by another, that is when the supports form an antichain. $\blacksquare$
3. **The best size for one X.** By Sperner's theorem (1928), an antichain of subsets of $m$ outputs has at most $\binom{m}{\lfloor m/2 \rfloor}$ members, and the subsets of size $\lfloor m/2 \rfloor$ reach it. So $m$ outputs can serve at most $\binom{m}{\lfloor m/2 \rfloor}$ chains with this property, and no more; for example 252 chains on 10 outputs.
4. **$t$ X's.** A single error with up to $t$ X's is always detected exactly when no column is covered by the union of $t$ other columns. Such families are the superimposed codes of Kautz and Singleton (1964). They need many more outputs: the number of rows must grow roughly like $t^2 \log n / \log t$, a known result of coding theory that this page does not prove.

## Classic examples

- **All 3-subsets of 5 outputs.** Take $m = 5$ and the 10 columns of weight 3. They are distinct, odd and form an antichain. Counting over all cases gives: every set of 1, 2, 3 or 5 errors is detected; 15 of the 210 sets of 4 errors cancel; every single error with one X is detected (90 cases); a single error with two X's is lost in 180 of the 360 cases, for example the chain 00111 under the X's of 01011 and 01101, whose union 01111 covers it; and two errors with one X are lost in 90 of the 360 cases. So 10 chains need 5 pins instead of 10, with exact guarantees for one X.
- **Hamming-like columns.** Using the columns of a [Hamming code](/hamming-code/) parity-check matrix gives the most chains for detecting any one or two errors with no X, but its columns cover each other, so it does not tolerate an X.
- **Diagnosis from the outputs.** With distinct columns and no X, a single failing chain $i$ shows exactly $h_i$ on the outputs, the [syndrome](/syndrome/) of the error, so the failing chain is identified from one cycle, and the cycle gives the cell.
- **Next to a decompressor.** In [EDT](/embedded-deterministic-test/) and other compression schemes, a space compactor of this kind reads the chains on the output side, with masking for cycles where the X's exceed what the matrix tolerates.

## Variations

- **X-masking.** Gate off the chains that carry X in a given pattern, using control bits from the tester. Masking removes X's that the matrix cannot tolerate, at the cost of extra test data.
- **Weight and rows.** Odd weight is chosen for odd error counts, and weight near $m/2$ for the antichain. Smaller weights use fewer XOR gates and less wiring but give fewer chains for the same guarantee.
- **Compactors with memory.** Feeding the outputs into short shift registers spreads each error over a few cycles and outputs, which raises the error detection at the cost of letting an X spoil a few cycles.
- **Signature on top.** When a design has no X's in some patterns, the $m$ outputs can feed a [MISR](/multiple-input-signature-register/) for those patterns, which reduces the data further.

## Pitfalls

- **Even-weight columns.** With even-weight columns, odd numbers of errors are no longer guaranteed: the three columns 011, 101 and 110 sum to zero, so errors on those three chains in one cycle cancel. Use odd weight.
- **Columns covered by others.** A matrix with distinct but nested columns, such as 001 and 011, detects every single error with no X but loses an error on the first chain when the second chain is X. Check the antichain condition, not only distinctness.
- **More X's than designed.** The guarantees hold for the number of X's the matrix was built for. With dense X's, many outputs are unknown and coverage falls quickly. Measure the X density per cycle and mask above the limit.
- **Errors in many chains at once.** A defect that fans out to many chains can produce four or more errors in one cycle, which may cancel. Run fault simulation through the compactor to measure the real coverage loss, which the theorems do not bound.
- **Errors in an X chain.** If a chain is X in a cycle, an error on it cannot be seen there by any compactor; it is not a weakness of the matrix.

## Exercises

1. Show that for $m = 5$ there is no antichain of 11 subsets, and give one of 10 subsets in which every set has odd size.
2. Prove that with odd-weight distinct columns and no X, any set of 1, 2 or 3 errors is detected. Give a set of 4 errors that cancels in the 10-column example.
3. For the 10-column example, count the pairs of X chains that leave a given error chain undetected, and check that it is 18 for every chain.
4. Show that a family where no column is covered by the union of two others needs more than $\log_2 n$ rows, and give such a family with $n = 7$ columns.

## References
