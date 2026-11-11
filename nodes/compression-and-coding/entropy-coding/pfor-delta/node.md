---
tag: 3ZJB2A
kind: algorithm
slug: pfor-delta
name: PForDelta
aliases:
- PFOR
- patched frame of reference
- PFOR-DELTA
area: compression-and-coding/entropy-coding
level: advanced
summary: Codes blocks of 128 integers, usually the gaps of a sorted list, at one bit width b; values that do not fit are exceptions stored apart and patched in after a branch-free unpack.
model: word-ram
complexity:
  vars: {n: the count of integers, w: the largest width tried (the word size)}
  time: {worst: Θ(n w), average: Θ(n w), best: Θ(n w)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 2006
  people: [Marcin Zukowski, Sándor Héman, Niels Nes, Peter Boncz]
  note: PFOR and PFOR-DELTA were designed for the MonetDB/X100 column store, to decompress faster than RAM can deliver data.
prereqs: [delta-encoding, bit-packing]
see_also: [variable-byte-encoding, elias-fano-encoding, interpolative-coding, rice-coding, elias-gamma-coding, simd-within-a-register, run-length-encoding, inverted-index]
sources:
  - paper: doi:10.1109/ICDE.2006.150
    title: Marcin Zukowski, Sándor Héman, Niels Nes and Peter Boncz, Super-scalar RAM-CPU cache compression, Proceedings of the 22nd International Conference on Data Engineering (ICDE), 2006
    locator: pp. 59 to 70 (PFOR, PFOR-DELTA and PDICT, exceptions linked through the code slots, compulsory exceptions)
  - paper: doi:10.1145/1526709.1526764
    title: Hao Yan, Shuai Ding and Torsten Suel, Inverted index compression and query processing with optimized document ordering, Proceedings of the 18th International World Wide Web Conference (WWW), 2009
    locator: pp. 401 to 410 (NewPFD and OptPFD)
  - paper: doi:10.1145/3415148
    title: Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys 53(6), Article 125, 2020
    locator: Section 3.3, PForDelta (arXiv:1908.10598v2)
  - paper: doi:10.1002/spe.2203
    title: Daniel Lemire and Leonid Boytsov, Decoding billions of integers per second through vectorization, Software, Practice and Experience 45(1), 2015
    locator: the FastPFor scheme, with exceptions grouped per page of blocks
---

PForDelta codes a sorted list of integers, such as a posting list of document numbers, in blocks of 128. It first takes the gaps between neighbors, so the values are small. In each block it picks one bit width $b$ and a base, and stores every value $v$ with $v - \text{base} < 2^b$ in a $b$-bit slot. The few values that do not fit are *exceptions*: they go into a separate area, and their slots link them in a chain. The decoder unpacks all slots in one loop with no branch, then walks the chain and *patches* the exceptions in. One large gap no longer forces a wide width on the whole block, which is the weak point of plain frame-of-reference coding. Zukowski, Héman, Nes and Boncz introduced the scheme in 2006.

## In plain words

Most gaps in a posting list are small, but now and then a gap is huge. If every number in a block must use the same number of bits, one huge gap makes the whole block wide.

So pick a width that suits most of the numbers, and treat the rest as special cases. The normal numbers go into equal slots, packed tightly. The special numbers go at the end of the block, in full. The slot of each special number does not hold the number; it says how far ahead the next special number is, so the reader can hop from one to the next.

The reader first fills every position from the slots, very fast, without any tests. Then it hops through the special positions and puts in the right values. This implementation tries every width and keeps the one that gives the smallest block.

## The problem

The input is a sorted list $x_1 \le x_2 \le \cdots \le x_n$ of integers below $2^{32}$, or any list of integers in a column. The task is a compressed form that decodes at a speed of the order of a few CPU cycles per integer or less, with good compression when most values are small and a few are large. Bit-serial codes such as the [Elias gamma code](/elias-gamma-coding/) or the [Rice code](/rice-coding/) compress well but decode one value at a time with a branch per bit or per value.

Notation: $n$ is the count of integers, $v_0, \ldots, v_{m-1}$ are the values of one block with $m \le 128$, $b$ is the slot width, $E$ is the sorted list of exception positions, and $w = 32$ is the largest width. Logarithms are base 2.

## The algorithm

PForDelta replaces the list by its gaps $x_1, x_2 - x_1, \ldots, x_n - x_{n-1}$ (this is [delta encoding](/delta-encoding/)), cuts the gaps into blocks of 128, and codes each block with PFOR:

```pseudo id=main
PFOR-ENCODE-BLOCK(v[0..m−1])
L1  base ← min v
L2  b ← the width in 0..w with the smallest block size        ▷ size from L3, L4 and L7
L3  E ← the positions i with v[i] − base ≥ 2^b                ▷ true exceptions
L4  while two neighbors p < q in E have q − p > 2^b: insert p + 2^b into E   ▷ compulsory
L5  code[i] ← v[i] − base for each position i not in E
L6  code[E_j] ← E_{j+1} − E_j − 1 for each j; code[last of E] ← 0
L7  write m, b, base, E_0, |E|; the m codes in b bits each; then v[e] − base for e in E, 32 bits each

PFOR-DECODE-BLOCK(block)
L8  read the header and the m codes; out[i] ← base + code[i] for all i   ▷ no branch
L9  cur ← E_0; for j ← 0 to |E| − 1 do
L10     nxt ← cur + code[cur] + 1; out[cur] ← base + exception j; cur ← nxt
L11 return out
```

Line L3 marks every value that does not fit in $b$ bits. The slot of an exception holds the distance to the next exception minus 1, which must fit in $b$ bits, so two neighbors in the chain can be at most $2^b$ apart. Line L4 keeps that true: where a gap in the chain is too long, it makes a value that would fit an exception anyway, a *compulsory exception*. Line L6 writes the chain. Line L8 is the fast part: it unpacks all $m$ slots as if there were no exceptions. Line L10 then follows the chain and overwrites the $|E|$ wrong values.

**Choosing $b$.** The size of a block in this layout is $5 + \lceil m b / 8 \rceil + 4|E_b|$ bytes, plus the bytes of the base beyond the first, where $E_b$ is the exception list for width $b$, compulsory ones included. Line L2 computes it for each $b$ from 0 to 32 and keeps the smallest, the first one on a tie. Other systems use a simpler rule, for example the smallest $b$ that leaves at most about 10% of the values as exceptions.

**This implementation.** It uses the layout of Zukowski and others (slots, chain, compulsory exceptions, 32-bit exceptions after the slots) with the exhaustive width choice of OptPFD. The exceptions follow the slots here; in the original they grow backward from the end of the block. The base is the minimum of the block; for gaps, a base of 0 is also common.

## Example

One block of 11 values: $v = [3, 4, 7, 21, 9, 12, 5, 16, 6, 2, 34]$. Line L1 gives base 2, so the values to store are $1, 2, 5, 19, 7, 10, 3, 14, 4, 0, 32$.

With $b = 4$, line L3 finds two exceptions, $19$ at position 3 and $32$ at position 10. They are 7 apart, at most $2^4$, so line L4 adds nothing. Line L6 writes $10 - 3 - 1 = 6$ into slot 3 and 0 into slot 10:

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $v - \text{base}$ | 1 | 2 | 5 | **19** | 7 | 10 | 3 | 14 | 4 | 0 | **32** |
| slot (4 bits) | 1 | 2 | 5 | 6 | 7 | 10 | 3 | 14 | 4 | 0 | 0 |

The block is the header `0b 04 02 03 02` (11 values, $b = 4$, base 2, first exception 3, two exceptions), the slots `12 56 7a 3e 40 00`, and the exceptions `13 00 00 00` and `20 00 00 00`: 19 bytes. To decode, line L8 gives $[3, 4, 7, 8, 9, 12, 5, 16, 6, 2, 2]$. Line L10 starts at position 3: the next exception is at $3 + 6 + 1 = 10$, and position 3 becomes $2 + 19 = 21$. Then at position 10 it writes $2 + 32 = 34$.

Line L2 tries every width. For this block:

| $b$ | exception positions | bytes |
|---|---|---|
| 2 | 2, 3, 4, 5, 7, 8, 10 | 36 |
| 3 | 3, 5, 7, 10 | 26 |
| 4 | 3, 10 | 19 |
| 5 | 10 | 16 |
| 6 | none | 14 |
| 7 | none | 15 |

So $b = 6$ wins: with 32-bit exceptions, each exception costs as much as 32 slots of one bit, and this block is short. In a full block of 128 gaps with a few large ones, a small $b$ with a few exceptions wins.

**Compulsory exceptions.** The values $0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0$ with $b = 1$ have true exceptions at positions 1 and 8, which are 7 apart, but a 1-bit slot can only say "next" or "one after next". Line L4 adds positions 3, 5 and 7, which gives the chain $1, 3, 5, 7, 8$.

## Correctness

The invariant of line L10 is: when the loop starts round $j$, *cur* is the $j$-th exception position $E_j$, and every position not in $\{E_j, \ldots\}$ already holds its right value. Line L8 sets each non-exception position to $\text{base} + (v_i - \text{base}) = v_i$, which is right because line L5 stored $v_i - \text{base} < 2^b$ in its slot. In round $j$, the slot of $E_j$ holds $E_{j+1} - E_j - 1$, which fits in $b$ bits because line L4 made every step at most $2^b$, so *nxt* is $E_{j+1}$; the exceptions were written in the order of $E$, so exception $j$ is $v_{E_j} - \text{base}$. After $|E|$ rounds every position is right. The gaps decode block by block, and a prefix sum gives back the sorted list. The full proof is in the proof file.

## Complexity

**Time.** Decoding a block takes $\Theta(m)$ for line L8 and $\Theta(|E|)$ for the chain, so $\Theta(n)$ for the list. Line L8 has no data-dependent branch, and for a fixed $b$ it is a fixed sequence of shifts and masks that compilers unroll and that [SIMD](/simd-within-a-register/) code can run on several slots at once. Encoding with the exhaustive choice of line L2 takes $\Theta(m)$ per width, so $\Theta(m w)$ per block and $\Theta(n w)$ in all. With a histogram of the bit lengths in the block, the counts of true exceptions for all widths take $O(m + w)$; the compulsory exceptions still need one pass per width.

**Space.** A block takes $\lceil m b / 8 \rceil$ bytes of slots, $4|E|$ bytes of exceptions, and a header of a few bytes. The extra working space is $O(m)$ for one block.

## Properties

- **Branch-free bulk decode.** The cost of an exception is moved out of the main loop into a short patch loop.
- **Robust to outliers.** One large value costs one exception, not $m$ wide slots, which is the gain over plain frame-of-reference (FOR) coding.
- **Block-aligned random access.** A skip list or a table of block offsets lets a decoder jump to any block of 128 and decode it alone, which posting list intersection needs.
- **Not prefix-free per value.** The unit is the block: the header gives $m$ and $b$, and the decoder must read the whole block.

## Variants and improvements

- **PFOR, PFOR-DELTA and PDICT.** Zukowski and others defined three schemes on the same exception mechanism: PFOR on the values minus a base, PFOR-DELTA on the differences of neighbors, and PDICT on indices into a dictionary.
- **NewPFD** (Yan, Ding and Suel, 2009). An exception slot keeps the low $b$ bits of the exception, and the high bits and the positions go into two separate arrays, compressed with Simple16. There is no chain, so there are no compulsory exceptions, and the block can use a smaller $b$.
- **OptPFD** (same paper). The NewPFD layout, with $b$ chosen per block to minimize the compressed size, or a mix of size and decode speed. It gives smaller output at a small loss of speed.
- **FastPFor and SIMD-BP128** (Lemire and Boytsov, 2015). FastPFor stores the exceptions of a page of many blocks together, grouped by width, and decodes them in bulk. SIMD-BP128 drops exceptions and packs blocks of 128 with SIMD instructions.
- **Parallel PFor** (Ao and others). The slot keeps the low $b$ bits of each exception and the overflow bits go into a separate array, so the patching can run in parallel with the unpacking.

## When to use it

Use PForDelta for posting lists and integer columns where decode speed matters most and the values are mostly small with rare outliers: search engine indexes, column stores, time series of counters. For lists that need random access by value or rank, [Elias-Fano encoding](/elias-fano-encoding/) is often both smaller and faster to search. For the best compression of clustered lists, [binary interpolative coding](/interpolative-coding/) is smaller but much slower. For short lists or single values, [variable-byte encoding](/variable-byte-encoding/) is simpler.

## Pitfalls

- **No compulsory exceptions.** If line L4 is missing, two exceptions more than $2^b$ apart need a slot value that does not fit in $b$ bits. Line L6 then writes a truncated distance and the decoder jumps to a wrong position. The fix is line L4: make a value at most $2^b$ ahead an exception.
- **Distance instead of distance minus 1.** Line L6 must store $E_{j+1} - E_j - 1$. Storing $E_{j+1} - E_j$ wastes one value and breaks $b = 0$, where the only slot value is 0 and every step must be 1.
- **Overwrite before read.** A decoder that works in place, with the output in the slot array, must read the next distance in line L10 before it writes the exception value into the same position. In the other order it loses the chain.
- **Last block length.** The last block of a list usually has fewer than 128 values. Line L7 must record $m$ (or the decoder must know the list length), or line L8 decodes padding as values.
- **Choosing $b$ as the largest bit length.** This is plain FOR: it never makes an exception, and one outlier makes every slot of the block wide. Line L2 must compare the sizes with exceptions.

## Implementations

## History

Zukowski, Héman, Nes and Boncz introduced PFOR, PFOR-DELTA and PDICT at ICDE 2006 for the MonetDB/X100 column store, under the title "super-scalar RAM-CPU cache compression": the aim was to decompress faster than main memory delivers data, so that compressed columns speed up queries. Zhang, Long and Suel (WWW 2008) applied PForDelta to inverted indexes with blocks of 128 gaps. Yan, Ding and Suel (WWW 2009) proposed NewPFD and OptPFD. Lemire and Boytsov (2015) gave SIMD versions, FastPFor and SIMD-BP128, which became common baselines.

## References
