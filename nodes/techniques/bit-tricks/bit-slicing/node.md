---
tag: 6FDGG8
kind: technique
slug: bit-slicing
name: Bit slicing
aliases:
- bitslicing
- bit-sliced implementation
area: techniques/bit-tricks
level: research
summary: Representing data by bit position across many words so that a circuit runs on 64 or more instances at once.
prereqs: [boolean-circuit, bitwise-operations, bit-matrix-transposition]
see_also: [bit-matrix-transposition, data-encryption-standard, advanced-encryption-standard, s-box, timing-attack, ripple-carry-adder, bit-parallelism, bitmap-index]
sources:
  - paper: doi:10.1007/BFb0052352
    title: Eli Biham, A fast new DES implementation in software, Fast Software Encryption (FSE 1997), Lecture Notes in Computer Science 1267
    locator: pp. 260 to 272
  - paper: doi:10.1007/978-3-642-04138-9_1
    title: Emilia Käsper and Peter Schwabe, Faster and timing-attack resistant AES-GCM, Cryptographic Hardware and Embedded Systems (CHES 2009), Lecture Notes in Computer Science 5747
    locator: pp. 1 to 17
  - paper: doi:10.1145/253260.253268
    title: Patrick O'Neil and Dallan Quass, Improved query performance with variant indexes, Proceedings of the 1997 ACM SIGMOD International Conference on Management of Data
    locator: pp. 38 to 49
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 7-3, Transposing a Bit Matrix
---

Bit slicing stores many instances of a computation side by side, with one word for each bit position: bit $j$ of word $i$ holds bit $i$ of instance $j$. A program written as a [Boolean circuit](/boolean-circuit/) then runs on all $w$ instances at once, since each AND, OR, XOR or NOT of words evaluates one gate for every instance. Biham introduced the method for software DES in 1997, where it computes 64 encryptions in parallel on a 64-bit machine, and it is now the standard way to write table-free, constant-time code for ciphers such as AES. Data enter and leave the sliced form by [bit matrix transposition](/bit-matrix-transposition/).

## In plain words

Usually a number sits in one word, with its bits next to each other. Bit slicing turns this sideways. Take 64 numbers. Put the lowest bit of all 64 numbers into one word, the next bit of all 64 numbers into a second word, and so on.

Now one instruction on two words works on one bit of 64 numbers at the same time. If you can describe your job as a network of simple logic gates, every gate becomes one instruction, and the whole network runs on 64 inputs for the price of one. The machine never branches and never looks up a table, so the time does not depend on the data.

## When it applies

- The same computation runs on many independent inputs: many blocks of a cipher, many test vectors of a circuit, many rows of a table.
- The computation is a fixed [Boolean circuit](/boolean-circuit/), or can be written as one: no data-dependent branches and no data-dependent memory addresses.
- The circuit is small in gates, or most of its work is permutations of bits, which cost nothing in the sliced form because they only rename words.
- Constant time matters. Table lookups with secret indexes leak through the cache, and the sliced form has no lookups; see [timing attack](/timing-attack/).

## The template

1. **Choose the slices.** Fix the number of bits $k$ of the state of one instance, and the number of instances $m$, usually the word size $w$ or the width of a vector register.
2. **Transpose in.** From the $m$ inputs of $k$ bits each, build the $k$ words $S_0, \ldots, S_{k-1}$, where bit $j$ of $S_i$ is bit $i$ of input $j$. This is the transposition of an $m \times k$ bit matrix, $O(k \log m)$ word operations with masked block swaps when $k = m$.
3. **Run the circuit.** Replace each gate by the same operation on words: $x \land y$ by `X AND Y`, $x \oplus y$ by `X XOR Y`, $\lnot x$ by `NOT X`. A permutation of wires is a renaming of the words and costs no instruction. A constant is the word of all zeros or all ones.
4. **Transpose out.** Turn the $k'$ output words back into $m$ outputs of $k'$ bits.

**Cost.** A circuit with $G$ gates costs $G$ word operations for $m$ instances, so $G / m$ operations for each instance, plus the two transpositions. The method wins when $G / m$ is below the cost of the usual code for one instance.

**Example.** Add four pairs of 3-bit numbers, $a = (5, 3, 6, 0)$ and $b = (1, 7, 2, 4)$, modulo 8 with a sliced [ripple-carry adder](/ripple-carry-adder/). Writing each word with instance 3 on the left, the slices are $A_0 = 0011$, $A_1 = 0110$, $A_2 = 0101$ and $B_0 = 0011$, $B_1 = 0110$, $B_2 = 1010$. With $c = 0$, for $i = 0, 1, 2$, set $S_i = A_i \oplus B_i \oplus c$ and $c = (A_i \land B_i) \lor (c \land (A_i \oplus B_i))$. This gives $S_0 = 0000$, $S_1 = 0011$, $S_2 = 1001$, and the final carry $0110$. Read by columns, the sums are $6, 2, 0, 4$, and the carries out of instances 1 and 2 show that $3 + 7$ and $6 + 2$ overflowed. The same 15 word operations would add 64 pairs on a 64-bit machine.

## Classic examples

- **DES.** Biham wrote the eight S-boxes of the [Data Encryption Standard](/data-encryption-standard/) as gate circuits and ran 64 encryptions at once on a 64-bit Alpha. The bit permutations of DES, which are slow in the usual software, are free in the sliced form. Brute-force key search, where many keys are tried on the same block, fits the method well.
- **AES.** Käsper and Schwabe gave a sliced implementation of the [Advanced Encryption Standard](/advanced-encryption-standard/) in counter mode that keeps 8 blocks in eight 128-bit registers, with the [S-box](/s-box/) as a circuit. It has no table lookups, so it resists cache-timing attacks, and the paper reports it as faster than the previous implementations on 64-bit Intel processors.
- **Bit-sliced indexes.** O'Neil and Quass store a numeric column of a table as one [bitmap](/bitmap-index/) for each bit position. A range predicate such as $x < c$ then is a sliced comparison circuit over the bitmaps, with one bit for each row: for each bit from the top, `lt = lt OR (eq AND NOT X_i AND C_i)` and `eq = eq AND NOT (X_i XOR C_i)`.
- **Circuit simulation.** Running a gate-level netlist on 64 test vectors at once is the same idea, used in test generation and fault simulation.
- **Sorting networks and comparators.** A [sorting network](/sorting-network/) on $k$-bit keys becomes a circuit of sliced comparators and multiplexers, `Z = (X AND M) OR (Y AND NOT M)`, which sorts $w$ independent small arrays at once.

## Variations

- **Partial slicing.** Slice by bytes or by nibbles instead of by bits, and keep the bits of a byte together, so that byte-level operations such as a byte shuffle still apply. Käsper and Schwabe use an arrangement of this kind.
- **Vector registers.** With 128-bit, 256-bit or 512-bit registers, $m$ grows to the register width.
- **Arithmetic.** Additions and comparisons become ripple circuits of $O(k)$ word operations for $w$ instances, as in the example; multiplication costs $O(k^2)$.
- **Lookups inside slices.** A table with secret index can be emulated by a multiplexer tree over the slices, which costs $O(2^k)$ gates for a $k$-bit index; this is why S-boxes are written as small custom circuits instead.
- **Contrast with SWAR.** [SIMD within a register](/simd-within-a-register/) keeps the bits of each value together in a field and blocks the carries between fields. Bit slicing has no carries at all, since each bit position of a value is a different word.

## Pitfalls

- **Transposition cost.** The transposition in and out costs $O(k \log m)$ word operations for $m$ instances. For a short computation it can cost more than the circuit; keep the data sliced across several steps.
- **Not enough instances.** The speedup needs $m$ independent instances. A cipher in a chaining mode such as CBC encryption has one block at a time, so slicing it gains nothing.
- **Gate count, not depth.** The cost is the number of gates, not the depth. A circuit tuned for small depth in hardware may be large in gates and slow when sliced; S-box circuits for slicing are optimized for gate count.
- **Register pressure.** A circuit with many live wires needs many words; if they do not fit in registers, the loads and stores dominate.
- **Compiler branches.** A compiler may turn a multiplexer back into a branch. For constant-time code, check the machine code.

## Exercises

1. Write the sliced form of a full subtractor and use it to compute $a - b$ modulo $2^k$ for $w$ pairs at once. Count the word operations.
2. Give a sliced circuit that tests $a < b$ for $w$ pairs of unsigned $k$-bit numbers with $O(k)$ word operations, scanning the bits from the top, and prove it correct.
3. Show that a fixed permutation of the $k$ bits of every instance costs no word operations in the sliced form, and compare with the cost in the usual layout, as in [bit reversal](/bit-reversal/).
4. Sort $w$ independent arrays of 4 keys of 8 bits each with the 5-comparator sorting network for 4 inputs, sliced. Count the word operations for one comparator.
5. A sliced multiplexer tree selects one of $2^k$ constant $k'$-bit table entries for each of $w$ instances. Bound its gate count, and explain why it is constant time while a table lookup is not.

## References
