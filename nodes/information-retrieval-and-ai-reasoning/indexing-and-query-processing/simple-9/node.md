---
tag: QCGBFK
kind: algorithm
slug: simple-9
name: Simple-9 coding
aliases:
- Simple9
- Anh-Moffat word-aligned coding
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Packs as many small integers as fit into each 32-bit word, using 4 selector bits to choose one of nine equal-width layouts.
model: word-ram
complexity:
  vars: {n: the number of integers, W: the number of 32-bit words of the output}
  time: {encode: O(n), decode: O(n + W)}
  space: {output: Θ(W), extra: O(1)}
properties: {deterministic: true, online: false, recursive: false, comparison: false}
prereqs: [postings-gap-encoding, bit-packing]
see_also: [variable-byte-encoding, pfor-delta, elias-gamma-coding, elias-fano-encoding, partitioned-elias-fano, interpolative-coding, posting-list, delta-encoding]
sources:
  - paper: doi:10.1023/B:INRT.0000048490.99518.5c
    title: Vo Ngoc Anh and Alistair Moffat, Inverted index compression using word-aligned binary codes, Information Retrieval 8(1), 2005, pages 151 to 166
    locator: the Simple-9 code with its nine layouts and 4-bit selector, and the Relative-10 and Carryover-12 codes of the same paper
  - paper: "Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys, 2021, arXiv 1908.10598"
    title: Techniques for inverted index compression
    locator: Section 3, the word-aligned codes Simple9, Simple16 and Simple8b, with the table of the Simple9 layouts
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 6, Section 6.3 (compressing postings lists), and Section 6.3.4 (index compression for high query performance)
---

Simple-9 codes a list of nonnegative integers below $2^{28}$, usually the gaps of a [posting list](/posting-list/), in 32-bit words. Each word has a 4-bit selector and 28 data bits, and the selector picks one of nine ways to cut the 28 bits into equal fields: 28 fields of 1 bit, 14 of 2, 9 of 3, 7 of 4, 5 of 5, 4 of 7, 3 of 9, 2 of 14, or 1 of 28. The encoder packs, in each word, as many of the next values as fit in one layout. Anh and Moffat introduced it in 2005. It differs from [variable-byte encoding](/variable-byte-encoding/), which spends one flag bit in each byte of each value, and from [PForDelta](/pfor-delta/), which fixes one width for a block of 128 values and stores the exceptions apart: here every word has its own width, chosen for a few values at a time. How the gaps are formed is the subject of [postings gap encoding](/postings-gap-encoding/); this page is only the word-aligned code.

## In plain words

A computer reads memory one word at a time, and a word is 32 bits. Small numbers need only a few bits, so it is a waste to give each one a full word. Simple-9 puts several numbers in one word. It keeps 4 bits of each word for a small label that says how the other 28 bits are cut. If the next 28 numbers are all 0 or 1, one word holds all of them, one bit each. If the next numbers are larger, the word holds fewer of them, each with more bits. The reader looks at the label and knows at once how to cut the word, with no work for each bit. This is why Simple-9 decodes fast.

## The problem

The input is a list $x_0, \ldots, x_{n-1}$ of integers with $0 \le x_i < 2^{28}$. The output is a list of 32-bit words from which the decoder, given $n$, gets the list back. The goal is a small output with a decoder that does a constant amount of work for each word and each value, with no bit-by-bit loop. For a posting list $d_1 < d_2 < \cdots$, the input is the list of gaps $d_1, d_2 - d_1, d_3 - d_2, \ldots$.

## The algorithm

The nine layouts, as (count $c_s$, width $w_s$) for selector $s$, are:

| $s$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| values $c_s$ | 28 | 14 | 9 | 7 | 5 | 4 | 3 | 2 | 1 |
| bits each $w_s$ | 1 | 2 | 3 | 4 | 5 | 7 | 9 | 14 | 28 |
| unused bits | 0 | 0 | 1 | 0 | 3 | 0 | 1 | 0 | 0 |

There are nine layouts, not sixteen, because these are the ways to cut 28 bits into equal fields with few unused bits. Four bits can name sixteen selectors, so seven are free.

```pseudo id=main
S9-ENCODE(x[0..n-1])                   ▷ each x[i] in [0, 2^28)
L1  out ← empty list, i ← 0
L2  while i < n do
L3      for s ← 0 to 8 do              ▷ most values first
L4          k ← min(c_s, n - i)
L5          if x[i], ..., x[i + k - 1] are all below 2^(w_s) then stop the loop
L6      word ← s · 2^28                 ▷ selector in the top 4 bits
L7      for j ← 0 to k - 1 do put x[i + j] in bits j·w_s to (j+1)·w_s - 1 of word
L8      append word to out, i ← i + k
L9  return out

S9-DECODE(out, n)
L10 x ← empty list
L11 for each word of out do
L12     s ← ⌊word / 2^28⌋
L13     for j ← 0 to c_s - 1 while |x| < n do append bits j·w_s to (j+1)·w_s - 1 of word to x
L14 return x
```

Line L3 tries the layouts from the one with the most values to the one with the fewest. Line L4 takes $k = c_s$ values, or the values that are left at the end of the list. Line L5 tests whether they all fit in $w_s$ bits. The first layout that passes is used. Selector 8, one value of 28 bits, always passes, so the loop always stops. Lines L6 and L7 build the word: the selector in the top 4 bits and the values in the data fields, here with the first value in the lowest bits. The last word can be partly filled, so the decoder needs $n$, or some other end mark.

The decoder reads the selector of each word at line L12, and line L13 cuts the data bits into $c_s$ fields of $w_s$ bits each. Real decoders write one unrolled block of shifts and masks for each of the nine selectors, and jump to it with a table.

## Example

Take the posting list with ids 1, 2, 4, 8, 11, 12, 22, 23, 223, 230, 237, 238. Its gaps are 1, 1, 2, 4, 3, 1, 10, 1, 200, 7, 7, 1.

| word | line L3 tries | first layout that fits | values packed | word in hexadecimal |
|---|---|---|---|---|
| 1 | $s = 0$: 2 does not fit 1 bit. $s = 1$: 4 does not fit 2 bits. $s = 2$: 10 does not fit 3 bits | $s = 3$, 7 values of 4 bits | 1, 1, 2, 4, 3, 1, 10 | 3A134211 |
| 2 | $s = 0$ to 4: 200 does not fit 5 bits or less. $s = 5$: 200 does not fit 7 bits | $s = 6$, 3 values of 9 bits | 1, 200, 7 | 601D9001 |
| 3 | $s = 0$ and $s = 1$: 7 does not fit 2 bits | $s = 2$, 9 values of 3 bits, 2 used | 7, 1 | 2000000F |

The first word is $3 \cdot 2^{28}$ plus the values 1, 1, 2, 4, 3, 1, 10 in fields of 4 bits from the low end, which gives the hexadecimal digits 3, then A, 1, 3, 4, 2, 1, 1 from the top. The 12 gaps take 3 words, 96 bits, or 8 bits for each gap. For comparison, [Elias gamma coding](/elias-gamma-coding/) takes 48 bits for the same gaps, and variable-byte encoding takes 13 bytes, 104 bits, because 200 needs two bytes. Simple-9 is not the smallest here; it is chosen for decode speed, and on long lists of small gaps its words are full and the gap to gamma is smaller.

## Correctness

The encoder always ends, because selector 8 fits any value below $2^{28}$, and each word takes at least one value. In each word the selector is in the top four bits, and the $k$ values are in disjoint fields of $w_s$ bits below bit $k w_s \le 28$, each value small enough for its field by the test of line L5. The decoder reads the selector, so it knows the layout of each word, and it reads the fields in the order the encoder wrote them. Only the last word can hold fewer than $c_s$ values, and the count $n$ tells the decoder where to stop. So decoding returns the input. The full proof, with the word count below, is in the proof file below.

## Complexity

- **Encoding.** Each word tries at most 9 layouts and tests at most 28 values for each, so $O(1)$ work per word and $O(n)$ in total. A table of bit lengths or a running maximum makes the test faster in practice.
- **Decoding.** $O(1)$ work for each word and for each value, so $O(n + W)$. There is no branch for each bit and no test for each value, which is the point of the code.
- **Size for values of one width.** If every value has bit length exactly $w$, the encoder uses the layout with the least width $w_s \ge w$, so it writes $\lceil n / c_s \rceil$ words, that is $32 \lceil n / c_s \rceil$ bits. For $w = 6$ this is the layout with 4 values of 7 bits, so 8 bits for each value; for $w = 1$ it is 28 values in one word, about 1.14 bits for each value.
- **Overhead.** Each word spends 4 bits on its selector, and up to 3 data bits are unused in some layouts, so the cost is at least $32/28$ of the data bits. A run of values of one width can take about twice their bits: values of 15 bits take a whole word each, and values of 10 bits take 16 bits each in the layout with 2 fields of 14 bits.
- **Range.** Values must be below $2^{28}$. Gaps of very large collections can exceed this, and need an escape.

## Properties

- **Word aligned.** Each word decodes on its own, so decoding can start at any word, and the code suits skips by block.
- **Greedy, not optimal.** The rule of line L3 takes the most values that fit in the current word. This does not always give the fewest words. For $x = 7, 300, 0, 2, 5, 3, 12, 3, 0, 100, 1, 300$ the encoder writes 4 words, while the split into 2 values of 14 bits, 7 values of 4 bits and 3 values of 9 bits uses 3. A dynamic program over the positions finds the fewest words in $O(n)$ time, but the gain is usually small.
- **A code for sequences.** The code is for a list, not for one value, and the decoder needs the count of values or a fixed block size.

## Variants and improvements

- **Simple-16.** Uses all 16 selector values with layouts whose fields have different widths inside one word, which packs better. Zhang, Long and Suel used it in their study of compressed list caching.
- **Simple-8b.** Anh and Moffat later applied the same idea to 64-bit words, with a 4-bit selector and 60 data bits, and selectors for long runs of equal values.
- **Relative-10 and Carryover-12.** In the same 2005 paper, Anh and Moffat describe codes that choose the next layout relative to the last one, with 2-bit selectors, and that use the unused bits of a word to hold the selector of the next word.
- **Blocks with a common width.** [PForDelta](/pfor-delta/) and binary packing fix one width for a block of 128 values, which suits SIMD decoding better than one selector per word.
- **Optimal split.** A shortest path over the positions, with one edge for each layout that fits, gives the least number of words for the same nine layouts.

## When to use it

Use Simple-9 for posting lists of small gaps when decoding speed matters more than the last bits of space, and when the engine reads whole words. It is a simple choice on 32-bit platforms and needs no SIMD. For lists with very uneven gaps, a code with exceptions such as PForDelta usually packs better. For lists that need fast skips over ranges of ids, [Elias-Fano encoding](/elias-fano-encoding/) or a [partitioned Elias-Fano index](/partitioned-elias-fano/) gives direct NEXT-GEQ without full decoding.

## Pitfalls

- **Values of $2^{28}$ or more.** Line L5 never passes for such a value, not even at $s = 8$, and a loop that assumes it does runs past the end of the layout table. The input must be checked, as the implementation does, or large values need an escape word.
- **Partial last word.** If the decoder takes $c_s$ values from every word in place of stopping at $n$ in line L13, it adds zeros from the unused fields of the last word. Store $n$, or pad with a value the caller can tell apart.
- **Testing only the first value.** A test of line L5 that checks only $x[i]$ in place of all $k$ values packs a larger later value into a field that is too small, and the extra high bits spill into the next field.
- **Gaps of zero.** Strictly increasing ids give gaps of at least 1. Simple-9 can code 0, so an engine can store gap minus 1 to gain a little in the narrow layouts; encoder and decoder must agree on this.
- **Byte order.** The words are 32-bit integers. A file written on one machine and read on a machine with another byte order must convert the words.

## Implementations

## History

Anh and Moffat published Simple-9, with Relative-10 and Carryover-12, in Information Retrieval in 2005, as word-aligned codes that decode faster than bit-aligned codes such as Elias gamma and Golomb codes at a small cost in space. Later work extended the idea to 16 layouts in Simple-16 and to 64-bit words in Simple-8b, and the survey of Pibiri and Venturini lists these codes next to block codes such as PForDelta.

## References
