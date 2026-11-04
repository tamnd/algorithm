---
tag: JEHNP6
kind: algorithm
slug: morton-encoding
name: Morton encoding
aliases:
- Z-order encoding
- Morton code
area: techniques/bit-tricks
level: advanced
summary: Computes the Z-order index of a point by interleaving the bits of its coordinates, using magic-mask spreading.
solves: [bit-interleaving]
model: word-ram
complexity:
  vars: {b: the number of bits of each coordinate, d: the number of coordinates}
  time: {worst: Θ(d log b), average: Θ(d log b), best: Θ(d log b)}
  space: {extra: O(1)}
history:
  year: 1966
  people: [Guy M. Morton]
  note: Morton described the interleaved order of map cells in an IBM technical report, Ottawa, March 1966.
prereqs: [bit-interleaving, bitwise-operations, z-order-curve]
see_also: [bit-interleaving, z-order-curve, space-filling-curve, hilbert-curve, geohash, linear-quadtree, quadtree]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 7-2, Shuffling Bits; Section 7-5, Expand, or Generalized Insert
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
  - url: "https://domino.research.ibm.com/library/cyberdig.nsf/papers/0DABF9473B9C86D48525779800566A39/$File/Morton1966.pdf"
    title: G. M. Morton, A computer oriented geodetic data base and a new technique in file sequencing, technical report, IBM Ltd., Ottawa, March 1966
    locator: the whole report (the interleaved order of map cells)
---

Morton encoding computes the Morton code of a point, its index on the [Z-order curve](/z-order-curve/), by spreading the bits of each coordinate apart with a few shift, OR and AND steps and then merging the spread coordinates. For two 32-bit coordinates and a 64-bit code it uses five stages for each coordinate, with the masks 0x0000FFFF0000FFFF, 0x00FF00FF00FF00FF, 0x0F0F0F0F0F0F0F0F, 0x3333333333333333 and 0x5555555555555555. It solves the [bit interleaving](/bit-interleaving/) problem in $\Theta(d \log b)$ word operations, with no loop over bits and no table, and the same stages run backwards decode the code. The order is named after Guy Morton, who described it in a 1966 IBM report.

## In plain words

You want to put a gap after every bit of a number, so that a second number can fill the gaps. Moving bits one at a time is slow. Move them in blocks instead.

First cut the number into two halves and move the top half up, far enough that each half has room to grow. Then cut each half into two quarters and move the top quarter of each half up. Go on until single bits are moved. A mask after each move clears the copies that are in the wrong place.

A 32-bit number needs five such steps. Do the same for the second number, shift it by one place, and combine the two. The result has the bits of the two numbers in turn.

## The problem

The input is two coordinates $x, y$ with $0 \le x, y < 2^{32}$. The output is the 64-bit code $Z(x, y) = \sum_{i=0}^{31} (x_i 2^{2i} + y_i 2^{2i+1})$, where $x_i$ and $y_i$ are bit $i$ of $x$ and $y$; decoding is the inverse map. This is the case $d = 2$, $b = 32$ of the [bit interleaving](/bit-interleaving/) problem. The variant for $d = 3$ is below.

## The algorithm

All words are 64-bit unsigned. The first block is the encoder, the second the decoder.

```pseudo id=main
SPREAD(x)                                         ▷ 0 ≤ x < 2^32
L1  x ← (x OR (x << 16)) AND 0x0000FFFF0000FFFF
L2  x ← (x OR (x << 8))  AND 0x00FF00FF00FF00FF
L3  x ← (x OR (x << 4))  AND 0x0F0F0F0F0F0F0F0F
L4  x ← (x OR (x << 2))  AND 0x3333333333333333
L5  x ← (x OR (x << 1))  AND 0x5555555555555555
L6  return x                                      ▷ bit i of x is now at bit 2i

MORTON-ENCODE(x, y)
L7  return SPREAD(x) OR (SPREAD(y) << 1)
```

```pseudo id=decode
COMPACT(z)                                        ▷ keeps the bits at even positions
D1  z ← z AND 0x5555555555555555
D2  z ← (z XOR (z >> 1))  AND 0x3333333333333333
D3  z ← (z XOR (z >> 2))  AND 0x0F0F0F0F0F0F0F0F
D4  z ← (z XOR (z >> 4))  AND 0x00FF00FF00FF00FF
D5  z ← (z XOR (z >> 8))  AND 0x0000FFFF0000FFFF
D6  z ← (z XOR (z >> 16)) AND 0x00000000FFFFFFFF
D7  return z

MORTON-DECODE(z)
D8  return (COMPACT(z), COMPACT(z >> 1))
```

The mask after the stage with shift $s$ keeps, in each block of $2s$ bit positions, the low $s$ positions. Line L1 moves the high 16 bits of $x$ up by 16, into the upper 32-bit half of the word. Line L2 moves the high 8 bits of each 16-bit group up by 8, and so on. Each stage doubles the gaps; after line L5 each bit $i$ of $x$ sits at position $2i$, with a 0 at each odd position. Line L7 puts the spread $y$ in the odd positions.

COMPACT runs the stages backwards. After D1 each bit $i$ of the coordinate sits at position $2i$; each later line moves the bits in the upper half of each group down, halving the gaps. The XOR can be an OR, because the two terms have no common one-bits at the positions that the mask keeps.

## Example

Spread $x = 181 = 10110101_2$. Lines L1 and L2 change nothing, because $x < 2^8$ and its high bits are zero.

| line | shift | value (hex) | value (binary, low 16 bits) |
| --- | --- | --- | --- |
| input | | 0xB5 | 0000000010110101 |
| L1 | 16 | 0xB5 | 0000000010110101 |
| L2 | 8 | 0xB5 | 0000000010110101 |
| L3 | 4 | 0xB05 | 0000101100000101 |
| L4 | 2 | 0x2311 | 0010001100010001 |
| L5 | 1 | 0x4511 | 0100010100010001 |

At line L3 the high nibble 1011 moves up by 4, out of the low nibble 0101. At line L4 each nibble splits into two pairs 2 places apart, and at line L5 each pair splits into two single bits. The result 0x4511 has bits 0, 4, 8, 10 and 14 set, the doubles of the positions 0, 2, 4, 5 and 7 of the ones of 181.

For $y = 90 = 01011010_2$, SPREAD gives 0x1144. Line L7 gives $\mathtt{0x4511} \mathbin{|} (\mathtt{0x1144} \ll 1) = \mathtt{0x4511} \mathbin{|} \mathtt{0x2288} = \mathtt{0x6799} = 26521$. MORTON-DECODE(0x6799) gives back $(181, 90)$.

## Correctness

Number the five stages $j = 4, 3, 2, 1, 0$, with shift $2^j$, so line L1 is $j = 4$ and line L5 is $j = 0$. The key invariant is:

> After the stage with shift $2^j$, bit $i$ of the input sits at position $p_j(i) = i + 2^j \lfloor i / 2^j \rfloor$, and every other position of the word is 0.

Before line L1, with $j = 5$, every $i < 32$ has $\lfloor i / 32 \rfloor = 0$, so each bit is in its own place. In a stage with shift $2^j$, write $i = q 2^{j+1} + h 2^j + r$ with $h \in \{0, 1\}$ and $0 \le r < 2^j$. The bit is at $q 2^{j+2} + h 2^j + r$. If $h = 0$ it stays, and its copy moved by $2^j$ is cleared by the mask. If $h = 1$ the mask clears it in place and keeps its copy at $q 2^{j+2} + 2^{j+1} + r$. The kept positions of the two kinds differ modulo $2^{j+2}$, so no two bits collide. After $j = 0$, $p_0(i) = 2i$. COMPACT applies the inverse map of each stage in the reverse order. The full proof is below.

## Complexity

- **Encode.** SPREAD has five lines of three word operations each (shift, OR, AND), so 15 operations; MORTON-ENCODE does two spreads, a shift and an OR, 32 operations in all. In general, for $d$ coordinates of $b$ bits with $db \le w$, there are $\lceil \lg b \rceil$ stages for each coordinate, so $\Theta(d \log b)$ time in each case.
- **Decode.** COMPACT has one AND and five lines of three operations, 16 operations; MORTON-DECODE does two compacts and one shift.
- **Space.** $O(1)$ words; the masks are constants in the code.

## Properties

- **Branch-free and data-independent.** The same 32 operations run for every input, with no table, so the time does not depend on the values.
- **Bijective.** On $x, y < 2^{32}$ encoding is a bijection onto the 64-bit words, and decoding is its inverse.
- **Order-preserving on each axis.** If $x < x'$, then $Z(x, y) < Z(x', y)$, since the codes differ only at the positions of $x$ and the highest differing bit of $x$ and $x'$ decides.
- **Quadtree prefix.** The top $2k$ bits of $Z(x, y)$ name the cell of side $2^{32-k}$ that holds the point, so all points of one aligned square cell have consecutive codes.

## Variants and improvements

- **Three coordinates.** For $d = 3$ and 10-bit coordinates in a 32-bit word: `x = (x | x << 16) & 0x030000FF`, `x = (x | x << 8) & 0x0300F00F`, `x = (x | x << 4) & 0x030C30C3`, `x = (x | x << 2) & 0x09249249`, then $Z = S(x) \mathbin{|} S(y) \ll 1 \mathbin{|} S(z) \ll 2$. For 21-bit coordinates in a 64-bit code the same scheme uses the shifts 32, 16, 8, 4, 2.
- **Bit deposit.** With the BMI2 instructions of x86, SPREAD is `PDEP(x, 0x5555555555555555)` and COMPACT is `PEXT(z, 0x5555555555555555)`, one instruction each. On some older processors these instructions are slow, and the mask method is faster.
- **Lookup tables.** Spread each byte with a table of 256 entries of 16 bits, then shift and OR. This trades the five stages for four loads.
- **Perfect shuffle in one word.** To interleave the two 16-bit halves of a 32-bit word, use the swap form of Warren, Section 7-2: `t = (x ^ (x >> s)) & m; x = x ^ t ^ (t << s)` for $(s, m) = (8, \mathtt{0x0000FF00})$, $(4, \mathtt{0x00F000F0})$, $(2, \mathtt{0x0C0C0C0C})$, $(1, \mathtt{0x22222222})$.
- **Neighbors without decoding.** To step one cell in $x$, add 1 to the $x$ bits only: `((z | 0xAAAA...) + 1) & 0x5555...` gives the new $x$ bits, and the $y$ bits are kept.
- **Hilbert order.** The [Hilbert curve](/hilbert-curve/) has better locality, since consecutive cells are always adjacent, but its encoder needs a state machine over the bit pairs.

## When to use it

Use Morton encoding to sort or index points, pixels, voxels or tree cells by a key that keeps nearby items near in the order, as in a [linear quadtree](/linear-quadtree/), a [geohash](/geohash/) or a texture layout. It is cheap, needs no table, and the codes compare as integers. Use the [Hilbert curve](/hilbert-curve/) when the locality of consecutive cells matters more than the cost of the encoder, for example for the layout of data on disk. Use PDEP and PEXT when the processor has fast versions of them.

## Pitfalls

- **Coordinates too large.** SPREAD assumes $x < 2^{32}$. A higher bit is moved up and out of the word, or into the wrong place, without any error. Mask the input first, `x AND 0xFFFFFFFF`, as the implementation does.
- **Wrong order of stages.** The stages must run with the largest shift first in SPREAD and the smallest first in COMPACT. Line L5 before line L1 gives a wrong code.
- **32-bit arithmetic.** In C, `x << 16` on a 32-bit `x` loses the high bits before the mask. Cast to a 64-bit unsigned type before the first shift.
- **Swapped axes.** Whether $x$ or $y$ takes the even positions is a convention. Mixing the two conventions between the encoder and the decoder swaps the axes.
- **Signed coordinates.** A negative coordinate has its sign bits set in two's complement. Offset the coordinates by $2^{b-1}$, or map them to unsigned integers, before encoding; otherwise the Z order breaks at 0.

## Implementations

## History

Guy M. Morton described the interleaved order in a technical report of IBM Ltd., Ottawa, in March 1966, as a new technique to sequence the records of a geodetic database. Warren gives the shuffle and unshuffle of the bits of a word in Section 7-2 of Hacker's Delight, and the generalized insert, which spreads bits at the positions of any mask, in Section 7-5.

## References
