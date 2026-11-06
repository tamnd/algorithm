---
tag: SYYJVH
kind: algorithm
slug: bit-matrix-transpose
name: Bit matrix transpose algorithm
aliases:
- 8x8 bit matrix transpose
- Hacker's Delight transpose
area: techniques/bit-tricks
level: advanced
summary: Transposes an n by n bit matrix in lg n rounds of block swaps with masks and shifts, O(log n) word operations when the matrix fits in one word.
solves: [bit-matrix-transposition]
model: word-ram
complexity:
  vars: {n: "the number of rows and columns, a power of 2 with n at most the word size"}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: O(1)}
prereqs: [bit-matrix-transposition, bitwise-operations, bitmask]
see_also: [bit-matrix-transposition, bit-slicing, bit-interleaving, bit-reversal, bitboard, morton-encoding]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 7-3, Transposing a Bit Matrix
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
---

The bit matrix transpose algorithm transposes an $n \times n$ matrix of bits, stored one row to a word, by swapping blocks across the diagonal: first the two off-diagonal blocks of side $n/2$, then the off-diagonal blocks of side $n/4$ inside each diagonal block, and so on down to single bits. Each round is $n/2$ masked swaps between a pair of rows, so the whole transpose takes $\lg n$ rounds and $\Theta(n \log n)$ word operations, in place and with no table. Warren gives it for $32 \times 32$ matrices in Section 7-3 of Hacker's Delight, together with a version for an $8 \times 8$ matrix in one 64-bit word that needs only three rounds. The round with block side $j$ exchanges bit $j$ of the row index with bit $j$ of the column index, which gives a short proof.

## In plain words

Cut the square grid of bits into four equal quarters. Swap the top-right quarter with the bottom-left quarter. Now cut each of the two quarters on the diagonal into four smaller pieces, and again swap the top-right piece with the bottom-left piece. Go on until the pieces are single bits. At the end the grid is flipped over its diagonal.

The trick is that one step handles many pieces at once. The rows are words, and a mask picks out the left or right part of every piece in a row. One shift, a few XORs and a mask swap the parts between two rows. A grid of 32 rows needs five rounds of 16 such swaps.

## The problem

The input is $n$ words $A[0], \ldots, A[n-1]$, with $n$ a power of 2 and $n \le w$, holding an $n \times n$ bit matrix $M$ with $M[r][c]$ at bit $c$ of $A[r]$, column 0 at the least significant bit. The output, in the same words, is the transpose: afterwards bit $r$ of $A[c]$ is the old $M[r][c]$. This is the [bit matrix transposition](/bit-matrix-transposition/) problem.

## The algorithm

```pseudo id=main
TRANSPOSE(A, n)                           ▷ n a power of 2, n ≤ w
L1  j ← n / 2 ; m ← 2^j − 1                ▷ m marks the columns c with c AND j = 0
L2  while j ≥ 1
L3      for each k in 0, …, n − 1 with k AND j = 0
L4          t ← ((A[k] >> j) XOR A[k + j]) AND m
L5          A[k + j] ← A[k + j] XOR t
L6          A[k] ← A[k] XOR (t << j)
L7      j ← j / 2 ; m ← m XOR (m << j)
L8  return A
```

In the round with block side $j$, the rows split into pairs $k$ and $k + j$ with bit $j$ of $k$ equal to 0. The mask $m$ has a one at each column $c$ with bit $j$ of $c$ equal to 0. Line L4 lines up the columns $c + j$ of row $k$ with the columns $c$ of row $k + j$ and records where they differ. Lines L5 and L6 then flip both entries wherever they differ, which swaps them; this is the XOR swap of two fields. Line L7 halves $j$ and updates the mask: from $2^{n/2} - 1$, which marks the low half, it goes to the columns with bit $n/4$ equal to 0, and so on down to the even columns.

**One word.** For an $8 \times 8$ matrix in one 64-bit word $x$, with $M[r][c]$ at bit $8r + c$, the same rounds act inside the word. Moving an entry from $(r, c)$ to $(r + j, c - j)$ moves it up by $8j - j = 7j$ bit positions, so the rounds are
```
t = (x ^ (x >> 7))  & 0x00AA00AA00AA00AA;  x = x ^ t ^ (t << 7)
t = (x ^ (x >> 14)) & 0x0000CCCC0000CCCC;  x = x ^ t ^ (t << 14)
t = (x ^ (x >> 28)) & 0x00000000F0F0F0F0;  x = x ^ t ^ (t << 28)
```
Each mask marks the positions of the entries $(r, c)$ with bit $j$ of $r$ equal to 0 and bit $j$ of $c$ equal to 1, for $j = 1, 2, 4$; such an entry trades places with the entry $7j$ positions higher. Here the three rounds run with $j = 1$ first; the proof below shows that the order does not matter.

## Example

Take $n = 4$ and $A = [0011_2, 0101_2, 1001_2, 0000_2]$, written with column 3 on the left as in binary. The matrix with column 0 on the left is

| | $c = 0$ | $c = 1$ | $c = 2$ | $c = 3$ |
| --- | --- | --- | --- | --- |
| row 0 | 1 | 1 | 0 | 0 |
| row 1 | 1 | 0 | 1 | 0 |
| row 2 | 1 | 0 | 0 | 1 |
| row 3 | 0 | 0 | 0 | 0 |

**Round $j = 2$, $m = 0011_2$.** The pairs are rows $(0, 2)$ and $(1, 3)$. For $k = 0$: $A[0] \gg 2 = 0000_2$, $A[2] = 1001_2$, so $t = 1001_2 \mathbin{\&} 0011_2 = 0001_2$. Then $A[2] = 1000_2$ and $A[0] = 0011_2 \oplus 0100_2 = 0111_2$. For $k = 1$: $A[1] \gg 2 = 0001_2$, $A[3] = 0000_2$, so $t = 0001_2$, $A[3] = 0001_2$ and $A[1] = 0101_2 \oplus 0100_2 = 0001_2$. Now $A = [0111_2, 0001_2, 1000_2, 0001_2]$: the top-right $2 \times 2$ block, rows 0 and 1 by columns 2 and 3, has changed places with the bottom-left block.

**Round $j = 1$, $m = 0101_2$.** The pairs are rows $(0, 1)$ and $(2, 3)$. For $k = 0$: $(0011_2 \oplus 0001_2) \mathbin{\&} 0101_2 = 0000_2$, so nothing changes. For $k = 2$: $(0100_2 \oplus 0001_2) \mathbin{\&} 0101_2 = 0101_2$, so $A[3] = 0100_2$ and $A[2] = 1000_2 \oplus 1010_2 = 0010_2$.

The result is $A = [0111_2, 0001_2, 0010_2, 0100_2] = [7, 1, 2, 4]$, the transpose: column 0 of the input had ones in rows 0, 1 and 2, and $A[0] = 0111_2$.

## Correctness

Write $r_j$ for bit $j$ of an index $r$. **Claim:** the round with block side $j$ moves the entry at $(r, c)$ to $(r', c')$, where $r'$ and $c'$ are $r$ and $c$ with their bits $j$ exchanged, and it leaves all other bits of the indices alone. If $r_j = c_j$ the entry stays. Otherwise the round swaps the entries at $(k, c + j)$ and $(k + j, c)$ for $k_j = 0$ and $c_j = 0$, which is the exchange of the two bits $j$. Lines L4 to L6 perform this swap, since for each column $c$ with $c_j = 0$ bit $c$ of $t$ is $A[k][c + j] \oplus A[k + j][c]$, and XOR with $t$ at both places swaps two bits.

The rounds use $j = n/2, \ldots, 2, 1$, so they exchange every bit of the row index with the same bit of the column index, and the composition maps $(r, c)$ to $(c, r)$. The exchanges of different bits act on different coordinates of the index pair, so they commute, and any order of the rounds gives the transpose. The proof is in full below.

## Complexity

- **Time.** There are $\lg n$ rounds. Each round runs lines L4 to L6 for the $n/2$ values of $k$, with a shift, an XOR and an AND on line L4, an XOR on line L5 and a shift and an XOR on line L6: 6 word operations and 4 memory accesses. Total: $3 n \lg n$ word operations plus the loop control, $\Theta(n \log n)$ in each case. For $n = 32$ that is 80 swaps.
- **One word.** The $8 \times 8$ version is 3 rounds of 6 operations, 18 operations in all; for a $k \times k$ matrix in one word it is $\lg k$ rounds, $O(\log k)$.
- **Space.** In place: $O(1)$ extra words for $j$, $m$, $k$ and $t$.

## Properties

- **In place and branch-free.** The sequence of operations does not depend on the data, which matters for code that must run in constant time, such as [bit slicing](/bit-slicing/) of ciphers.
- **Involution.** Running the algorithm twice restores the input.
- **Any order of rounds.** The rounds commute, so they can run with $j$ increasing or decreasing.
- **Linear over GF(2).** The output is a fixed permutation of the input bits.

## Variants and improvements

- **Columns from the most significant bit.** Warren's code numbers the columns from the left, with $m$ starting at 0x0000FFFF, `t = (A[k] ^ (A[k + j] >> j)) & m`, `A[k] ^= t` and `A[k + j] ^= t << j`. The structure is the same.
- **Unrolled code.** For a fixed $n$, the loops unroll into straight-line code with constant masks, which removes the loop control.
- **Larger matrices.** For $n > w$, transpose each $w \times w$ block in place and swap the block $(I, J)$ with the block $(J, I)$: $O(n^2 \log w / w)$ word operations.
- **SIMD registers.** With 128-bit or 256-bit registers, the rounds with large $j$ act on whole lanes and use shuffles, while the rounds with small $j$ use the masked swap on each lane.
- **Rectangular blocks.** Stopping after the rounds with $j \ge s$ transposes the matrix of $s \times s$ blocks and keeps each block as it is. The rounds with $j < s$ alone transpose each block in place.

## When to use it

Use it to turn rows into columns of a packed bit matrix: to move data into and out of a bit-sliced layout, to flip a [bitboard](/bitboard/), or to get the columns of a GF(2) matrix. It beats the bit-by-bit method, which takes $n^2$ steps, for all but tiny $n$. On a machine with a fast gather of bits, such as PMOVMSKB on x86 for rows of 8 bits, a column-at-a-time method can be faster; measure both.

## Pitfalls

- **Wrong bit order.** If the columns are numbered from the most significant bit, the masks and the direction of the shifts change. Mixing the conventions produces the transpose about the other diagonal.
- **Mask update order.** Line L7 halves $j$ before it computes `m XOR (m << j)`. With the old $j$ the mask comes out wrong: for $n = 8$ the second mask becomes 0xFF instead of 0x33.
- **$n$ not a power of 2.** The pairing $k$, $k + j$ needs $n$ to be a power of 2. Pad the matrix with zero rows and columns first.
- **Signed shifts.** In C, right shifts of signed words copy the sign bit. Use unsigned words.
- **Row order in memory.** Some code stores row 0 of an $8 \times 8$ board in the high byte. The masks of the one-word version above assume row 0 in the low byte.

## Implementations

## History

Warren presents the transpose of a $32 \times 32$ bit matrix by recursive block swaps, and the transpose of an $8 \times 8$ matrix in one word, in Section 7-3 of Hacker's Delight. Knuth treats the swaps of bit fields with masks, the "$\delta$-swaps", and their use for bit permutations such as transposition, in Section 7.1.3 of The Art of Computer Programming.

## References
