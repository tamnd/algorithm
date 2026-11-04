---
tag: NGG0JJ
kind: technique
slug: simd-within-a-register
name: SIMD within a register
aliases:
- SWAR
- packed arithmetic in a word
area: techniques/bit-tricks
level: advanced
summary: Performing lane-wise arithmetic on several packed fields of one machine word using masks to block carries.
prereqs: [bitwise-operations, bitmask, twos-complement, bit-packing]
see_also: [bit-parallelism, swar-popcount, population-count, bit-packing, bit-slicing, branchless-programming, word-ram, fusion-tree]
sources:
  - paper: doi:10.1145/360933.360994
    title: Leslie Lamport, Multiple byte processing with full-word instructions, Communications of the ACM 18(8), 1975
    locator: pp. 471 to 475
  - paper: doi:10.1007/3-540-48319-5_19
    title: Randall J. Fisher and Henry G. Dietz, Compiling for SIMD within a register, Languages and Compilers for Parallel Computing (LCPC 1998), Lecture Notes in Computer Science 1656
    locator: pp. 290 to 305
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 2-18, Multibyte Add, Subtract, Absolute Value; Section 5-1, Counting 1-Bits; Section 6-1, Find First 0-Byte
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
---

SIMD within a register, or SWAR, treats one machine word as a vector of small fields, called lanes, and does the same arithmetic on all lanes with ordinary word instructions. Additions and subtractions would carry from one lane into the next, so SWAR code uses masks to block those carries, typically by clearing the top bit of each lane before the operation and fixing it after. With 8-bit lanes a 64-bit word does 8 additions in a handful of instructions, and the same idea gives the classic [SWAR population count](/swar-popcount/), the test for a zero byte in string functions, and lane-wise averages and comparisons. Lamport described multiple byte processing with full-word instructions in 1975, and Fisher and Dietz named the technique and compiled for it in 1998.

## In plain words

A 64-bit number can hold eight small numbers of 8 bits each, side by side. If you add two such words, the machine adds all eight pairs at once, which is what you want, except for one thing: when a pair adds up to more than 8 bits can hold, the extra bit spills into the next pair and spoils it.

The fix is to stop the spill. Set aside the top bit of each small number, add the rest, so that nothing can overflow, then put the top bits back with an XOR, which adds bits without any carry. The answer for each small number is now correct, and it took four or five instructions for all eight.

## When it applies

- The data are many small values, of 2 to 16 bits each, packed into words by [bit packing](/bit-packing/), and the same operation applies to all of them.
- The operation is built from additions, subtractions, shifts and Boolean operations, where the only interaction between lanes is the carry or the borrow, which masks can stop.
- There are no vector instructions, or the data already sit in general registers, or the lane width is not one that the vector unit supports, such as 2, 4 or 12 bits.
- A reduction across lanes, such as a sum of all lanes, can be done with a multiplication or a few shift-and-add steps.

## The template

Fix the lane width $k$ and the number of lanes $L$ with $kL \le w$. Let $H$ be the word with a 1 at the top bit of each lane, $\bar H = \lnot H$ restricted to the $kL$ bits, and $\mathbf 1$ the word with a 1 at the bottom bit of each lane. For 8-bit lanes in 64 bits, $H$ = 0x8080808080808080, $\bar H$ = 0x7F7F7F7F7F7F7F7F and $\mathbf 1$ = 0x0101010101010101.

- **Lane-wise addition modulo $2^k$.** $s = ((x \mathbin{\&} \bar H) + (y \mathbin{\&} \bar H)) \oplus ((x \oplus y) \mathbin{\&} H)$. The low $k - 1$ bits of two lanes add to less than $2^k$, so no carry leaves a lane; the carry into the top bit stays in the lane, and the XOR adds the two top bits modulo 2.
- **Lane-wise subtraction modulo $2^k$.** $d = ((x \mathbin{|} H) - (y \mathbin{\&} \bar H)) \oplus ((x \oplus \lnot y) \mathbin{\&} H)$. Setting the top bit of each lane of $x$ gives each lane a value of at least $2^{k-1}$, which is more than the low part of $y$, so no borrow leaves a lane.
- **Lane-wise average, rounded down.** $(x \mathbin{\&} y) + (((x \oplus y) \mathbin{\&} \lnot \mathbf 1) \gg 1)$, from $a + b = 2(a \mathbin{\&} b) + (a \oplus b)$; the mask removes the bit that would move into the next lane down.
- **Exact zero-lane test.** $t = (x \mathbin{\&} \bar H) + \bar H$; then $\lnot(t \mathbin{|} x \mathbin{|} \bar H)$ has a 1 at the top bit of exactly the lanes of $x$ that are 0. Adding $\bar H$ sets the top bit of each lane whose low bits are not all 0, and OR with $x$ adds the lanes whose top bit is 1.
- **Quick zero-lane test.** $(x - \mathbf 1) \mathbin{\&} \lnot x \mathbin{\&} H$ is nonzero exactly when some lane of $x$ is 0, and its lowest set bit is in the lowest zero lane. Lanes above the first zero lane may be flagged wrongly, so use it only to test for a zero lane or to find the first one.
- **Reduction.** The sum of the lanes, when it fits in $k$ bits, is the top lane of $x \cdot \mathbf 1$, that is $(x \cdot \mathbf 1) \gg k(L - 1)$, modulo $2^w$.

**Example.** With two 8-bit lanes, $x$ = 0x12F0 and $y$ = 0x3420: the lane-wise sum is 0x4610, since $\mathtt{0xF0} + \mathtt{0x20} = \mathtt{0x110}$ keeps 0x10 and does not carry into the upper lane, which gets $\mathtt{0x12} + \mathtt{0x34} = \mathtt{0x46}$. A plain addition gives 0x4710. The lane-wise difference of 0x1210 and 0x3420 is 0xDEF0. For the zero test on $x$ = 0x0100, the exact test gives 0x0080, which flags only the lower lane, while the quick test gives 0x8080 and flags the upper lane too, because the borrow from the zero lane makes the lane 0x01 look like 0.

## Classic examples

- **Population count.** Count the ones in pairs of bits, then in nibbles, then in bytes, with lane-wise additions, and add the bytes by a multiplication by $\mathbf 1$. See [SWAR population count](/swar-popcount/) and Warren, Section 5-1.
- **String functions.** A C `strlen` or `memchr` reads 8 bytes at a time and uses the zero-lane test, after an XOR with the target byte repeated in all lanes, to find the end or the match (Warren, Section 6-1).
- **Multibyte arithmetic.** Saturating or modular additions of pixels, and lane-wise absolute differences, for image code on machines without vector units (Warren, Section 2-18).
- **Packed comparisons.** With $k - 1$ data bits in each lane and a spare top bit, $((x \mathbin{|} H) - y) \mathbin{\&} H$ has the top bit of a lane set exactly when that lane of $x$ is at least that lane of $y$. This lane-wise compare is a step of the [fusion tree](/fusion-tree/) and of the sorting algorithms of the [word RAM](/word-ram/) that pack several keys into a word.
- **Hash tables.** Some open-addressing tables keep a 7-bit tag for each slot in a group of 8 or 16 bytes and find the candidate slots of a key with one lane-wise compare.

## Variations

- **Spare bits.** Leave the top bit of each lane empty as a guard. Then plain addition and subtraction work lane by lane as long as the results stay in range, and the guard bit holds the carry or the comparison result.
- **Vector registers.** SSE, AVX and NEON give the same lanes in hardware, with no masks for 8, 16, 32 and 64 bits. SWAR remains useful for other widths and in scalar code.
- **Mixed widths.** Lanes can widen as values grow, as the popcount does from 2 to 4 to 8 bits, with a mask and shift that adds adjacent lanes.
- **Lane-wise shifts.** A shift moves bits across lanes; mask after it. $(x \gg 1) \mathbin{\&} (\bar H)$ halves each 8-bit lane.
- **Contrast with bit slicing.** [Bit slicing](/bit-slicing/) puts each bit position of the values in its own word, so there are no carries at all; SWAR keeps each value together and blocks its carries.

## Pitfalls

- **Forgetting the carry block.** A plain $x + y$ is wrong in every lane above a lane that overflows. Test with lanes at 0xFF.
- **The quick zero test lies above the first zero.** It may flag a lane 0x01 that sits just above a zero lane, as in the example; for a full mask of zero lanes use the exact test.
- **Signed lanes.** The formulas above are for unsigned lanes modulo $2^k$. Signed comparisons and sign extension of lanes need an extra XOR with $H$ to bias the values.
- **Reading past the end.** Reading a string 8 bytes at a time may read bytes past its end. This is safe only for aligned words inside one page, and tools that check memory may still report it.
- **Endianness.** The lowest lane is the first byte in memory only on a little-endian machine. On a big-endian machine the first zero byte is at the highest flagged lane, which a [leading zero count](/leading-zero-count/) finds.

## Exercises

1. Prove the lane-wise subtraction formula: show that no borrow crosses a lane boundary, and that the XOR fixes the top bit of each lane.
2. Give a SWAR formula for the lane-wise maximum of two words of unsigned 7-bit values with a spare top bit in each 8-bit lane. Hint: build a mask of all ones in the lanes where $x \ge y$ from the compare above.
3. Prove that the quick zero test $(x - \mathbf 1) \mathbin{\&} \lnot x \mathbin{\&} H$ is nonzero if and only if some lane of $x$ is 0, and give a lane value other than 0x01 that it can flag wrongly, or prove there is none.
4. Count the number of bytes equal to a given byte $c$ in a 64-bit word with $O(1)$ word operations, using the exact zero test and a population count or a multiplication.
5. Show that the reduction $(x \cdot \mathbf 1) \gg k(L - 1)$ gives the sum of the lanes when that sum is below $2^k$, and find the smallest input with 8-bit lanes in 64 bits where it fails.

## References
