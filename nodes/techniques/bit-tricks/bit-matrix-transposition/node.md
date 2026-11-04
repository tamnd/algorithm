---
tag: 0XR14M
kind: problem
slug: bit-matrix-transposition
name: Bit matrix transposition
aliases:
- transpose a bit matrix
area: techniques/bit-tricks
level: advanced
summary: Transposing a square matrix of bits packed into words.
model: word-ram
complexity:
  vars: {n: the number of rows and columns, with n at most the word size}
  time: {worst: O(n log n)}
prereqs: [bitwise-operations, bitmask, word-ram]
see_also: [bit-matrix-transpose, bit-slicing, bit-interleaving, bit-reversal, bitboard, bitset-gaussian-elimination, bitset-adjacency-matrix, graph-transpose]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 7-3, Transposing a Bit Matrix
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
---

Bit matrix transposition is the problem of transposing an $n \times n$ matrix of bits that is stored with one row in each machine word, so that the output has one column of the input in each word. Reading one bit at a time costs $n^2$ steps, but the [bit matrix transpose algorithm](/bit-matrix-transpose/) of Warren's Hacker's Delight, Section 7-3, does it in $\lg n$ rounds of masked block swaps, $O(n \log n)$ word operations in all. A small matrix that fits in one word, such as an $8 \times 8$ matrix in 64 bits, needs only $\lg n$ rounds of $O(1)$ operations each. The problem appears whenever data must change between a layout by items and a layout by bit position, as in [bit slicing](/bit-slicing/).

## In plain words

Think of a square grid of on and off switches, for example 32 rows of 32 switches. Each row is stored as one number, so row 5 is one number whose digits are the switches of row 5.

Now you want the columns instead: one number for each column, made of the switches of that column from top to bottom. That is the transpose of the grid. It is the same grid flipped over its diagonal, so row 5 becomes column 5.

The slow way copies the switches one by one. The fast way swaps whole blocks of the grid at once: first the top-right quarter with the bottom-left quarter, then the same inside each quarter, and so on.

## Definition

**Input.** An integer $n$ with $1 \le n \le w$, and words $A[0], \ldots, A[n-1]$ with $0 \le A[r] < 2^n$. The entry in row $r$ and column $c$ is $M[r][c] = \lfloor A[r] / 2^c \rfloor \bmod 2$, so bit $c$ of the word of row $r$, with column 0 at the least significant bit.

**Output.** The words $B[0], \ldots, B[n-1]$ with $M^{\mathsf T}$ in the same layout:
$$ B[c] = \sum_{r=0}^{n-1} M[r][c] \, 2^r \qquad \text{for } 0 \le c < n . $$

**As a permutation.** Index the $n^2$ bits by the pairs $(r, c)$. Transposition is the fixed permutation $(r, c) \mapsto (c, r)$ of these positions, and an involution. It moves bits and does no arithmetic on them, so it commutes with AND, OR, XOR and NOT applied to whole matrices.

**Conventions.** Warren numbers the columns from the most significant bit, and some code stores row 0 in the high byte of a word. These conventions change the masks and the shifts of the algorithms, not the problem.

## Variants

- **One word.** The whole matrix fits in one word, for example $8 \times 8$ in 64 bits, with $M[r][c]$ at bit $8r + c$. This is the form for [bitboards](/bitboard/) in chess programs, where the transpose flips the board about the diagonal from a1 to h8.
- **Rectangular matrices.** An $m \times n$ matrix with $m \ne n$; pad it to a square of the next power of 2, or transpose $w \times w$ blocks and move the blocks.
- **Large matrices.** For $n > w$, store each row in $\lceil n / w \rceil$ words; then transpose the matrix of $w \times w$ blocks and transpose each block.
- **Anti-diagonal flip.** The map $(r, c) \mapsto (n - 1 - c, n - 1 - r)$. It is a transposition followed by a reversal of both indices, so it uses [bit reversal](/bit-reversal/) on each row and a reversal of the order of the rows.
- **Transposition of byte or field matrices.** The same block swaps work when each entry is a field of $k$ bits, with the shifts multiplied by $k$.

## Examples

For $n = 4$ with rows $A = [0011_2, 0101_2, 1001_2, 0000_2]$, the matrix and its transpose, with column 0 on the left, are

| | $c = 0$ | $c = 1$ | $c = 2$ | $c = 3$ |
| --- | --- | --- | --- | --- |
| $M$, row 0 | 1 | 1 | 0 | 0 |
| $M$, row 1 | 1 | 0 | 1 | 0 |
| $M$, row 2 | 1 | 0 | 0 | 1 |
| $M$, row 3 | 0 | 0 | 0 | 0 |
| $M^{\mathsf T}$, row 0 | 1 | 1 | 1 | 0 |
| $M^{\mathsf T}$, row 1 | 1 | 0 | 0 | 0 |
| $M^{\mathsf T}$, row 2 | 0 | 1 | 0 | 0 |
| $M^{\mathsf T}$, row 3 | 0 | 0 | 1 | 0 |

so $B = [7, 1, 2, 4]$. Column 0 of $M$ has ones in rows 0, 1 and 2, so $B[0] = 0111_2 = 7$.

For the $8 \times 8$ matrix in one 64-bit word with $M[r][c]$ at bit $8r + c$, the word 0xFF (row 0 full of ones) transposes to 0x0101010101010101 (column 0 full of ones), and the identity matrix 0x8040201008040201 is its own transpose.

A non-example: reversing the order of the bits of a word of $n^2$ bits maps $(r, c)$ to $(n - 1 - r, n - 1 - c)$, a rotation of the matrix by 180 degrees, not a transposition.

## Known algorithms

- **Bit by bit.** For each $(r, c)$, test bit $c$ of $A[r]$ and set bit $r$ of $B[c]$. $\Theta(n^2)$ operations.
- **Recursive block swap.** The [bit matrix transpose algorithm](/bit-matrix-transpose/): for $j = n/2, n/4, \ldots, 1$, swap the blocks of side $j$ above the diagonal with those below, with one masked swap for each pair of rows $k$ and $k + j$. $\lg n$ rounds of $n/2$ swaps, $O(n \log n)$ word operations, in place, with no table. Warren gives it for $n = 32$ in Section 7-3.
- **In one word.** For an $8 \times 8$ matrix in 64 bits, three masked swaps inside the word, with the shifts 7, 14 and 28: $t = (x \oplus (x \gg s)) \mathbin{\&} m$, $x = x \oplus t \oplus (t \ll s)$, with $m$ = 0x00AA00AA00AA00AA, 0x0000CCCC0000CCCC and 0x00000000F0F0F0F0.
- **Gather one column at a time.** On x86 the SSE2 instruction PMOVMSKB collects the top bit of each of 16 bytes into a 16-bit mask, which gives one column of 16 rows of 8 bits. Shifting each 16-bit lane of the register left by one bit and repeating gives the next column, eight times in all.

## Bounds

- **Upper bound.** $O(n \log n)$ word operations on the [word RAM](/word-ram/) with shifts and Boolean operations, for $n \le w$; $O(\log n)$ when $n^2 \le w$, so that the matrix fits in one word.
- **Lower bound.** This page claims only the trivial $\Omega(n)$, since the $n$ input words must be read and the $n$ output words written.
- **Large matrices.** For $n > w$, the block method gives $O((n/w)^2 \cdot w \log w) = O(n^2 \log w / w)$ word operations.

## Reductions

- **[Bit interleaving](/bit-interleaving/) reduces to it.** Interleaving $d$ words of $b$ bits is the transpose of the $d \times b$ matrix whose rows are the coordinates, read row by row.
- **Conversion to [bit-sliced](/bit-slicing/) form.** Turning $w$ words of $k$ bits into $k$ words of $w$ bits, one word for each bit position, is a transposition of a $w \times k$ matrix.
- **Column access in GF(2) linear algebra.** A matrix stored by rows gives its columns after one transposition, which code for [Gaussian elimination over bitsets](/bitset-gaussian-elimination/) and for $A^{\mathsf T} x$ uses.
- **It is a fixed bit permutation.** The block swaps are a case of the general method for bit permutations by masked swaps, which Knuth treats in Section 7.1.3; [bit reversal](/bit-reversal/) is another case.

## Applications

- **Bit slicing.** A bitsliced cipher, such as Biham's bitsliced DES, keeps bit $i$ of 64 blocks in word $i$. The data enter and leave this form by transposition. See [bit slicing](/bit-slicing/) and the [Data Encryption Standard](/data-encryption-standard/).
- **Bitboards.** Chess programs flip and rotate [bitboards](/bitboard/) by transposition, for example to reuse code for ranks on files.
- **Graphs.** For a [bitset adjacency matrix](/bitset-adjacency-matrix/) of a directed graph, the transpose gives the in-neighbors of each vertex as a bitset, the matrix of the [transpose graph](/graph-transpose/).
- **Graphics and displays.** Converting between planar bitmaps, with one plane for each bit of a pixel, and packed pixels is a transposition of small bit matrices.

## References
