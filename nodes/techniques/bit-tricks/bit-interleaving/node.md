---
tag: S9XWQ7
kind: problem
slug: bit-interleaving
name: Bit interleaving
aliases:
- interleaving bits
- Morton interleave
area: techniques/bit-tricks
level: advanced
summary: Merging the bits of several integers into one integer, alternating by position.
model: word-ram
complexity:
  vars: {b: the number of bits of each coordinate, d: the number of coordinates}
  time: {worst: O(d log b)}
prereqs: [bitwise-operations, bitmask]
see_also: [morton-encoding, z-order-curve, space-filling-curve, hilbert-curve, geohash, linear-quadtree, bit-reversal, bit-matrix-transposition]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 7-2, Shuffling Bits; Sections 7-4 and 7-5, Compress and Expand
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
  - url: "https://domino.research.ibm.com/library/cyberdig.nsf/papers/0DABF9473B9C86D48525779800566A39/$File/Morton1966.pdf"
    title: G. M. Morton, A computer oriented geodetic data base and a new technique in file sequencing, technical report, IBM Ltd., Ottawa, March 1966
    locator: the whole report (the interleaved order of map cells)
---

Bit interleaving is the problem of merging the bits of $d$ integers of $b$ bits each into one integer of $db$ bits, so that bit $i$ of coordinate $j$ goes to bit $d \cdot i + j$. The result is the Morton code of the point, its index on the [Z-order curve](/z-order-curve/), and the inverse problem, deinterleaving, recovers the coordinates. On the [word RAM](/word-ram/) it takes $O(\log b)$ shift-and-mask steps for each coordinate, by [Morton encoding](/morton-encoding/), and one instruction for each coordinate on processors with a bit-deposit instruction. In one word, the same operation is the outer perfect shuffle of its bits, which Warren treats in Section 7-2 of Hacker's Delight.

## In plain words

Take two numbers written in binary, for example a column number and a row number on a map. Make a new number by taking one digit from the first number, then one from the second, then the next from the first, and so on, from the right end. The new number has twice as many digits.

Points that are close on the map often get close new numbers, because their high digits agree, and the high digits of the new number are made of the high digits of both. So sorting points by the new number keeps nearby points near each other in the list. Undoing the mix, by taking every second digit, gives back the two numbers.

## Definition

**Input.** Integers $d \ge 1$ and $b \ge 1$, and coordinates $x^{(0)}, \ldots, x^{(d-1)}$ with $0 \le x^{(j)} < 2^b$. Write $x^{(j)}_i$ for bit $i$ of $x^{(j)}$.

**Output.**
$$ Z(x^{(0)}, \ldots, x^{(d-1)}) = \sum_{i=0}^{b-1} \sum_{j=0}^{d-1} x^{(j)}_i \, 2^{d i + j} . $$

**Inverse.** Given $z < 2^{db}$, deinterleaving returns the unique coordinates with $Z = z$: bit $i$ of $x^{(j)}$ is bit $di + j$ of $z$. So $Z$ is a bijection from $\{0, \ldots, 2^b - 1\}^d$ to $\{0, \ldots, 2^{db} - 1\}$.

**Spread.** The map $S_d(x) = \sum_i x_i 2^{di}$ puts the bits of one coordinate $d$ places apart. Then $Z = \bigvee_j S_d(x^{(j)}) \ll j$, so the problem reduces to $d$ spreads, $d - 1$ shifts and an OR, and the bit sets of the terms are disjoint.

**Order.** For $d = 2$, comparing $Z(x, y)$ with $Z(x', y')$ compares the highest bit level where the points differ; it is a total order that refines the order of the quadtree cells that contain the points. This order is the [Z-order curve](/z-order-curve/).

## Variants

- **Two coordinates.** $d = 2$, the common case for maps, images and textures.
- **Three coordinates.** $d = 3$, for octrees, voxels and particle simulations; 21 bits for each coordinate fill a 63-bit code.
- **Perfect shuffle of one word.** Interleave the low half and the high half of one word: bit $i$ of the low half goes to bit $2i$ and bit $i$ of the high half to bit $2i + 1$. The inverse is the unshuffle. Warren calls these the outer perfect shuffle and unshuffle.
- **Different coordinate sizes.** When one coordinate has more bits, its extra high bits go above the interleaved part.
- **Arithmetic on codes.** Some algorithms add to one coordinate inside the code without decoding, by filling the gaps of the other coordinate with ones so that carries jump over them.
- **Other orders.** The [Hilbert curve](/hilbert-curve/) also maps cells to a line but keeps consecutive cells adjacent, at a higher cost; [geohash](/geohash/) writes the interleaved bits of longitude and latitude in base 32.

## Examples

For $d = 2$, $b = 2$, with $x$ the column and $y$ the row, the codes $Z(x, y)$ on a $4 \times 4$ grid are

| | $x = 0$ | $x = 1$ | $x = 2$ | $x = 3$ |
| --- | --- | --- | --- | --- |
| $y = 0$ | 0 | 1 | 4 | 5 |
| $y = 1$ | 2 | 3 | 6 | 7 |
| $y = 2$ | 8 | 9 | 12 | 13 |
| $y = 3$ | 10 | 11 | 14 | 15 |

Following the codes 0, 1, 2, 3 traces a Z in the top-left $2 \times 2$ block, then the same Z in each of the other blocks, in the same Z order.

For $d = 2$, $b = 8$, $x = 181 = 10110101_2$ and $y = 90 = 01011010_2$, the pairs of bits $(y_i, x_i)$ from $i = 7$ down to $0$ are 01, 10, 01, 11, 10, 01, 10, 01, so $Z = 0110\,0111\,1001\,1001_2 = \mathtt{0x6799} = 26521$.

A non-example: concatenating the coordinates, $y \cdot 2^b + x$, is row-major order, not interleaving. It keeps whole rows together, so two points in adjacent rows are $2^b$ apart in the order however close they are on the map.

## Known algorithms

- **Bit by bit.** Loop over the $db$ output bits. $O(db)$ steps.
- **Magic masks.** Spread each coordinate in $\lceil \lg b \rceil$ stages of `x = (x | (x << s)) & mask`, with the shift $s$ halved at each stage, then OR the shifted results. $O(d \log b)$ steps. This is [Morton encoding](/morton-encoding/), which also gives the masks for $d = 3$ and the inverse.
- **Shuffle by swaps.** For $d = 2$ in one word, the outer perfect shuffle is $\lg b$ stages of a masked swap of two fields, `t = (x ^ (x >> s)) & m; x = x ^ t ^ (t << s)`, with $s = 8, 4, 2, 1$ for 32 bits (Warren, Section 7-2). The same stages in reverse order unshuffle.
- **Table lookup.** Spread each byte with a table of 256 entries and combine: $O(db/8)$ lookups. See [table lookup](/table-lookup/).
- **Bit deposit and extract.** The expand operation (Warren, Section 7-5) deposits the low bits of $x$ at the positions of a mask, and the compress operation (Section 7-4) extracts them. On x86 processors with BMI2 these are the PDEP and PEXT instructions: $Z = \mathrm{PDEP}(x, \mathtt{0x5555\ldots}) \mathbin{|} \mathrm{PDEP}(y, \mathtt{0xAAAA\ldots})$ in two instructions and an OR.
- **Multiplication.** For a few bits at a time, a multiplication by a constant with spaced ones makes shifted copies that a mask then selects.

## Bounds

- **Upper bound.** $O(d \log b)$ time on the [word RAM](/word-ram/) with shifts and Boolean operations, when $db \le w$, by the magic masks. With a table of $2^{b/c}$ entries, $O(dc)$ time. With a deposit instruction, $O(d)$ time.
- **Lower bound.** This page claims only the trivial $\Omega(d)$, since each coordinate must be read.

## Reductions

- **To [bit matrix transposition](/bit-matrix-transposition/).** Interleaving $d$ words of $b$ bits is a transpose: write the coordinates as the $d$ rows of a $d \times b$ bit matrix; the code read column by column is the interleaving. The code is the transpose of this matrix, a $b \times d$ matrix, read row by row with row 0 at the low end.
- **To generalized expand.** Each spread is one expand with the mask of positions $\{di + j\}$.
- **From Z-order sorting.** Sorting points by Z-order reduces to computing their codes and sorting integers. Comparing two points in Z-order without the codes is also possible: find the coordinate $j$ whose XOR of the two values has the highest set bit, taking the larger $j$ on a tie; that coordinate decides the order.

## Applications

- **Spatial databases.** Morton described the order in a 1966 IBM report, as a new way to sequence the records of a geodetic database by their map cells. The code is the key of a [linear quadtree](/linear-quadtree/) and of range queries on one-dimensional indexes.
- **Geohash.** The [geohash](/geohash/) of a place is the interleaved bits of its longitude and latitude, written in base 32.
- **Graphics.** Textures stored in Morton order, also called swizzled, have better cache locality for 2D access than row-major order.
- **Space-filling curves for parallel work.** Sorting particles or mesh cells by their codes splits space into compact pieces of equal size, as in the [space-filling curve](/space-filling-curve/) method of load balancing.
- **Cache-friendly matrix layouts.** Storing a matrix in Z order makes each aligned square block contiguous, which helps recursive algorithms.

## References
