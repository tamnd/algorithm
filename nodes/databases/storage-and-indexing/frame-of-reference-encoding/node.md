---
tag: PWP268
kind: technique
slug: frame-of-reference-encoding
name: Frame-of-reference encoding
aliases:
- FOR encoding
area: databases/storage-and-indexing
level: core
summary: "Store the values of a block as small offsets from a base value of the block, packed in as few bits as the largest offset needs."
prereqs: [bit-packing]
see_also: [pfor-delta, delta-encoding, bit-packing, dictionary-encoding, late-materialization, zone-map, simd-within-a-register, run-length-encoding]
sources:
  - paper: "Jonathan Goldstein, Raghu Ramakrishnan and Uri Shaft, Compressing relations and indexes, Proceedings of the 14th International Conference on Data Engineering (ICDE), 1998, 370 to 379"
    title: Compressing relations and indexes
    locator: the frame of reference scheme, with a minimum per page and per attribute and offsets in the bits that the range needs
  - paper: "Marcin Zukowski, Sandor Heman, Niels Nes and Peter Boncz, Super-scalar RAM-CPU cache compression, Proceedings of the 22nd International Conference on Data Engineering (ICDE), 2006"
    title: Super-scalar RAM-CPU cache compression
    locator: the PFOR and PFOR-DELTA schemes, which extend frame of reference with exceptions
  - paper: "Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos and Samuel Madden, The design and implementation of modern column-oriented database systems, Foundations and Trends in Databases 5(3), 2013, 197 to 280"
    title: The design and implementation of modern column-oriented database systems
    locator: the section on compression in column stores
---

Frame-of-reference encoding, or FOR, compresses a column of integers block by block. Each block of $B$ consecutive values keeps a *base*, the minimum of the block, and stores each value as its *offset* from the base. All offsets of the block are then packed with [bit packing](/bit-packing/) in $w$ bits, the number of bits of the largest offset. Values that are large but close to each other, such as dates, timestamps, prices or keys of one range, have small offsets: a block of timestamps that spans 4,000 seconds needs 12 bits per value instead of 64. The scheme keeps two properties that matter for query processing. The value at any position is one read of $w$ bits plus one addition, and a range predicate on values becomes a range predicate on offsets, so a scan compares offsets and never decodes the records that fail. Goldstein, Ramakrishnan and Shaft (1998) introduced the scheme for pages of relations and indexes. It is the base of [PForDelta](/pfor-delta/), which applies it to the gaps of [delta encoding](/delta-encoding/) and moves rare large values out of the block.

## In plain words

Think of a list of prices that are all between 1,000 and 1,100. Each one takes four digits to write. But if you write "1,000" once at the top, you can write each price as how much it is above 1,000, and that needs at most three digits.

Frame of reference does this for each group of numbers. It finds the smallest number of the group, writes it once, and stores every number of the group as its distance from that smallest number, using only as many bits as the largest distance needs.

To read a number, add its distance to the smallest one. To find the numbers in a range, first look at the smallest and largest number of each group. Many groups are fully out of the range, or fully in it, and you never need to open them.

## When it applies

- The column holds integers, or values stored as integers, such as dates, timestamps, fixed-point prices, identifiers or dictionary codes.
- Inside a block the values are close to each other, even if they are large. This is true for sorted or nearly sorted columns, for columns that grow with time, and for values of a small range.
- Queries need random access to single values, for example to fetch the values at the positions of [late materialization](/late-materialization/), and range predicates evaluated during the scan.
- The values have few outliers. One far value in a block raises $w$ for every value of the block.

## The template

The column has integers $a_0, \ldots, a_{N-1}$. A range predicate keeps the positions with $lo \le a_i \le hi$; either bound may be open.

```pseudo id=main
ENCODE(a, B)
L1  for each block k of the positions kB to min(N, kB + B) - 1 do
L2      base_k ← the minimum of the block; max_k ← the maximum of the block
L3      w_k ← the number of bits of max_k - base_k     ▷ 0 if all values are equal
L4      for each position i of the block do write a[i] - base_k in w_k bits at bit (i - kB)·w_k

GET(i)
L5  k ← ⌊i / B⌋; o ← the w_k bits at bit (i - kB)·w_k of block k
L6  return base_k + o

SELECT(lo, hi)
L7  for each block k in order do
L8      if max_k < lo or base_k > hi then skip the block
L9      else if lo ≤ base_k and max_k ≤ hi then output every position of the block
L10     else s ← max(lo - base_k, 0); e ← hi - base_k
L11         output the positions i of the block with s ≤ o_i ≤ e, where o_i is the offset of i
```

The header of a block holds $\mathrm{base}_k$, $w_k$ and, as a [zone map](/zone-map/) does, $\mathrm{max}_k$. The implementation keeps these in 17 bytes. A comparison with a constant is a range over integers: $< v$ is the range up to $v - 1$, and $> v$ the range from $v + 1$.

**Why it works.** The base is the minimum, so every offset is non-negative, and it is at most $\mathrm{max}_k - \mathrm{base}_k$, which has $w_k$ bits, so every offset fits in its field. The fields of a block do not overlap, so GET reads back exactly the offset that was written, and adding the base gives the value. For a selection, every value of block $k$ is in $[\mathrm{base}_k, \mathrm{max}_k]$, so a block that misses $[lo, hi]$ has no match and a block inside $[lo, hi]$ matches fully. In the other blocks, $lo \le a_i \le hi$ is the same as $lo - \mathrm{base}_k \le o_i \le hi - \mathrm{base}_k$, so comparing offsets gives exactly the matching positions. The proof file has the details.

**Cost.** Block $k$ with $c$ values takes the header plus $\lceil c w_k / 8 \rceil$ bytes. GET is $O(1)$: one header and one field of $w_k$ bits, with no access to the other values, unlike [delta encoding](/delta-encoding/), which must add the gaps from the start of a block. SELECT reads every header and reads offsets only in the blocks that meet $[lo, hi]$ without lying inside it. In a sorted column the blocks that meet the range are consecutive and only the first and the last of them can be partial, so a selection reads at most $2B$ offsets and $\lceil N / B \rceil$ headers.

**Example.** Take $B = 4$ and the 12 values below.

| block | values | base | max | $w$ | offsets |
|---|---|---|---|---|---|
| 0 | 1000, 1003, 1001, 1007 | 1000 | 1007 | 3 | 0, 3, 1, 7 |
| 1 | 1012, 1010, 1015, 1011 | 1010 | 1015 | 3 | 2, 0, 5, 1 |
| 2 | 1020, 1020, 1020, 1020 | 1020 | 1020 | 0 | none |

Blocks 0 and 1 need 12 bits of offsets each, 2 bytes, and block 2 needs none, since all its values equal the base. GET(6) finds block 1, reads the offset 5 at bit 6 of the block, and returns $1010 + 5 = 1015$. For $1011 \le a \le 1016$, block 0 is skipped because $1007 < 1011$, and block 2 because $1020 > 1016$. Block 1 is partial, so the bounds become offsets $s = 1$ and $e = 6$, and the offsets 2, 0, 5 and 1 give positions 4, 6 and 7. The scan read 4 offsets and no value of the other two blocks. For $1000 \le a \le 1020$ every block lies inside the range, and the scan outputs all 12 positions without reading an offset. On a larger scale, the sorted column $0, 3, 6, \ldots$ of 4,096 values with $B = 128$ has $w = 9$ in every block, so it takes 32 blocks of $17 + 144$ bytes, 5,152 bytes against 32,768 bytes as 64-bit integers.

## Classic examples

- **Compressed pages.** Goldstein, Ramakrishnan and Shaft (1998) compress each page of a relation or an index with a frame of reference per attribute, so that a page holds more tuples and a tuple can still be decoded alone.
- **PForDelta.** Zukowski, Heman, Nes and Boncz (2006) designed PFOR and PFOR-DELTA for the MonetDB/X100 column store. They choose $w$ so that most values fit and store the few others as exceptions, so that one outlier no longer sets the width of a whole block; see [PForDelta](/pfor-delta/).
- **Column stores and file formats.** Column stores use frame of reference, often together with [dictionary encoding](/dictionary-encoding/) and [run-length encoding](/run-length-encoding/), for integer, date and code columns. The minimum and maximum of each block double as a [zone map](/zone-map/).
- **Inverted lists.** Search engines store the gaps between document numbers with FOR-type codes of fixed width per block, which decode fast with [SIMD within a register](/simd-within-a-register/) and with vector instructions.

## Variations

- **Choice of base.** The base can be the minimum, as here, so that offsets are non-negative, or the first value of the block, with signed offsets. A fixed base for the whole column gives one width and no block headers, but loses the local range.
- **FOR on deltas.** For a sorted column, first take the gaps between neighbors with [delta encoding](/delta-encoding/) and then pack the gaps with FOR. The gaps are smaller than the offsets from the minimum, but random access must add the gaps from the start of the block.
- **Patched FOR.** [PForDelta](/pfor-delta/) picks $w$ so that only a small fraction of the values of the block do not fit, and stores those as exceptions to patch in after unpacking.
- **Block size.** A small $B$ gives tighter ranges and better skipping, at the cost of more headers. Blocks of 128 values or so are common, so that a block fits in cache and unpacks with vector code.
- **Width per block or per page.** The width can be chosen per block of values, per page, or per column chunk of a file, and each choice is a trade between header space and the fit of the width.

## Pitfalls

- **Outliers.** One value far from the others sets $w$ for the whole block. A block of small values with one value near $2^{60}$ needs 60 bits per value, no better than plain storage. Use patched FOR, or smaller blocks.
- **Updates.** A new value outside $[\mathrm{base}_k, \mathrm{max}_k]$ can change the base or the width, and then every offset of the block must be rewritten. FOR suits columns that are written in batches.
- **Bounds outside the block.** The translated bounds $lo - \mathrm{base}_k$ and $hi - \mathrm{base}_k$ can be negative or larger than any offset. Clamp them before comparing, or test the block range first as lines L8 and L9 do.
- **Overflow.** In fixed-width machine arithmetic, $\mathrm{max}_k - \mathrm{base}_k$ can overflow when the values span almost the whole signed range. Compute the difference in an unsigned type of the same width.
- **Only integers.** Floating-point values and strings do not have exact small offsets. Map them to integers first, for instance by [dictionary encoding](/dictionary-encoding/) or by a fixed-point scale.

## Exercises

1. A block of 128 timestamps covers 3,600 seconds. Compute its size with FOR and a 17-byte header, and compare it with 64-bit storage.
2. Give a block of $B$ values in which one outlier makes FOR no better than plain storage, and compute how many bits PForDelta needs for the same block with one exception of 64 bits.
3. Prove that if the column is sorted, SELECT reads at most $2B$ offsets, and give an unsorted column where it must read all $N$ offsets for a range that matches one value.
4. Change SELECT so that it sums the matching values instead of listing them. Show that a block inside the range can add $c \cdot \mathrm{base}_k$ plus the sum of its offsets, and say when the sum of the offsets can be kept in the header.

## References
