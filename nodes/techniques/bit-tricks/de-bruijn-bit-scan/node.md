---
tag: 3BENJ1
kind: algorithm
slug: de-bruijn-bit-scan
name: de Bruijn bit scan
aliases:
- de Bruijn multiplication
- de Bruijn sequence bit scan
area: techniques/bit-tricks
level: advanced
summary: Isolates the lowest set bit, multiplies by a de Bruijn constant and indexes a table to get the bit position in constant time.
solves: [trailing-zero-count]
model: word-ram
complexity:
  vars: {w: "the word size in bits, a power of two"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(w)}
properties: {deterministic: true, recursive: false}
prereqs: [lowest-set-bit, de-bruijn-sequence, twos-complement, trailing-zero-count]
see_also: [leading-zero-count, floor-log2, table-lookup, bitboard, perfect-hash-function, multiplicative-hashing, ruler-sequence, fusion-tree]
sources:
  - paper: "Charles E. Leiserson, Harald Prokop and Keith H. Randall, Using de Bruijn Sequences to Index a 1 in a Computer Word, unpublished manuscript, MIT Laboratory for Computer Science, 7 July 1998"
    locator: the whole note (the method and the 64-bit construction)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on computing the ruler function by multiplication with a de Bruijn cycle
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 5, Section 5-4 (Counting Trailing 0's)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer (2011)
    locator: Chapter 1, Section 1.5 (Computing the index of a single set bit)
  - url: https://graphics.stanford.edu/~seander/bithacks.html
    title: Sean Eron Anderson, Bit Twiddling Hacks
    locator: section Count the consecutive zero bits (trailing) on the right with multiply and lookup
---

The de Bruijn bit scan finds the index $k$ of the lowest 1-bit of a nonzero unsigned $w$-bit word $x$, which is the [trailing-zero count](/trailing-zero-count/) of $x$, with no loop and no branch. It isolates the [lowest set bit](/lowest-set-bit/) as $b = x \wedge (-x) = 2^k$, multiplies $b$ by a constant $D$ modulo $2^w$, takes the top $\lg w$ bits of the product, and reads $k$ from a table of $w$ entries. The constant is a binary [de Bruijn sequence](/de-bruijn-sequence/) of order $\lg w$, written as a $w$-bit word with $\lg w$ zeros at the top, so that the $w$ possible products have $w$ different top fields. Leiserson, Prokop and Randall described the method in 1998. It runs in $\Theta(1)$ time on the [word RAM](/word-ram/) with one multiplication, and it is the usual fallback on machines that have no trailing-zero instruction.

## In plain words

You want the position of the rightmost 1 in a word. First you erase every 1 except the rightmost one. Now the word is one of only $w$ values: 1, 2, 4, and so on. Multiplying by one of these values only moves a fixed bit pattern to the left by that many places.

The trick is to choose the pattern so that each of these moves leaves a different group of bits at the top of the word. A de Bruijn sequence has this property: each short group of bits occurs at exactly one place in it. So the top bits after the multiplication name the position without doubt, and a small table turns this name into the position.

## The problem

The input is an unsigned $w$-bit word $x$ with $x \ne 0$, where $w = 2^n$ is the word size. The output is $\rho(x)$, the index of the lowest 1-bit, that is, the unique $k$ with $0 \le k < w$ such that bit $k$ of $x$ is 1 and bits $0$ to $k - 1$ are 0. Knuth writes $\rho x$ and calls it the ruler function; it equals the number of trailing zeros of $x$. For $x = 0$ the value is not defined here; see [trailing-zero count](/trailing-zero-count/) for the conventions.

## The algorithm

All words are unsigned and all arithmetic is modulo $2^w$; $-x$ is the [two's complement](/twos-complement/) negation $2^w - x$. The constant $D$ is a $w$-bit word whose bits, read from the top, form a binary de Bruijn sequence of order $n$ that begins with $n$ zeros. The table $T$ has $w$ entries and is filled once, before any call: for $k = 0, 1, \dots, w - 1$, set $T[((2^k \cdot D) \bmod 2^w) \gg (w - n)] \gets k$.

```pseudo id=main
DE-BRUIJN-SCAN(x)              ▷ x is an unsigned w-bit word, x ≠ 0, w = 2^n
L1  b ← x ∧ (−x)               ▷ b = 2^k, only the lowest 1-bit of x
L2  p ← (b · D) mod 2^w        ▷ D shifted left by k places
L3  i ← p ≫ (w − n)            ▷ the top n bits of p
L4  return T[i]                ▷ the k with this top field
```

Line L1 uses the identity $x \wedge (-x) = 2^{\rho(x)}$ for $x \ne 0$: the negation $-x = \overline{x} + 1$ inverts all bits above bit $k$ and keeps bits $0$ to $k$, so only bit $k$ is 1 in both words. Line L2 multiplies by a power of two, so $p$ is $D$ shifted left by $k$ places, with the high bits that pass bit $w - 1$ discarded. Line L3 keeps the top $n$ bits of $p$. These $n$ bits are bits $w - 1 - k$ down to $w - n - k$ of $D$, with zeros in place of positions below 0; that is, the window of length $n$ that starts at position $k$ when $D$ is read from the top. Line L4 maps the window back to $k$.

The constants in the table below are binary de Bruijn sequences with $n$ leading zeros. Each was checked for the property that the $w$ windows are distinct.

| $w$ | $n$ | $D$ |
|---|---|---|
| 8 | 3 | `0x1D` |
| 16 | 4 | `0x09AF` |
| 32 | 5 | `0x077CB531` |
| 64 | 6 | `0x03F79D71B4CB0A89` |

For $w = 32$ the table is $T = [0, 1, 28, 2, 29, 14, 24, 3, 30, 22, 20, 15, 25, 17, 4, 8, 31, 27, 13, 23, 21, 19, 16, 7, 26, 12, 18, 6, 11, 5, 10, 9]$. For $w = 64$ it is $T = [0, 1, 48, 2, 57, 49, 28, 3, 61, 58, 50, 42, 38, 29, 17, 4, 62, 55, 59, 36, 53, 51, 43, 22, 45, 39, 33, 30, 24, 18, 12, 5, 63, 47, 56, 27, 60, 41, 37, 16, 54, 35, 52, 21, 44, 32, 23, 11, 46, 26, 40, 15, 34, 20, 31, 10, 25, 14, 19, 9, 13, 8, 7, 6]$.

## Example

Take $w = 8$, $n = 3$ and $D = \texttt{0x1D} = 00011101_2$. Read cyclically from the top, the eight windows of length 3 of $00011101$ are 000, 001, 011, 111, 110, 101, 010, 100: all eight 3-bit words, each once. The table is built from the products $2^k \cdot D \bmod 2^8$.

| $k$ | $2^k \cdot D \bmod 2^8$ | top 3 bits | index $i$ |
|---|---|---|---|
| 0 | 00011101 | 000 | 0 |
| 1 | 00111010 | 001 | 1 |
| 2 | 01110100 | 011 | 3 |
| 3 | 11101000 | 111 | 7 |
| 4 | 11010000 | 110 | 6 |
| 5 | 10100000 | 101 | 5 |
| 6 | 01000000 | 010 | 2 |
| 7 | 10000000 | 100 | 4 |

So $T = [0, 1, 6, 2, 7, 5, 4, 3]$: for instance $T[7] = 3$ because the row $k = 3$ has index 7. Now run the scan on $x = 104 = 01101000_2$.

| after line | value | binary |
|---|---|---|
| start | $x = 104$ | 01101000 |
| L1 | $-x = 152$, $b = 8$ | 00001000 |
| L2 | $p = 8 \cdot 29 \bmod 256 = 232$ | 11101000 |
| L3 | $i = 232 \gg 5 = 7$ | 111 |
| L4 | $T[7] = 3$ | |

The answer is 3: $104 = 8 \cdot 13$ has three trailing zeros. For $x = 180 = 10110100_2$ the same steps give $b = 4$, $p = 116 = 01110100_2$, $i = 3$ and $T[3] = 2$. For $w = 32$ and $x = \texttt{0x00F00000}$ they give $b = 2^{20}$, $p = \texttt{0x53100000}$, $i = 10$ and $T[10] = 20$.

## Correctness

**Claim.** For each nonzero unsigned $w$-bit word $x$, DE-BRUIJN-SCAN returns $\rho(x)$, provided the windows $((2^k D) \bmod 2^w) \gg (w - n)$ for $k = 0, \dots, w - 1$ are pairwise distinct. They are distinct when $D$ is a de Bruijn sequence of order $n$ whose top $n$ bits are zero.

The key fact is that the window for $k$ is the length-$n$ substring of $D$ that starts at position $k$ from the top, read cyclically. For $k \le w - n$ the window lies inside $D$. For $k > w - n$ the window runs past the low end of $D$; the shift fills these places with zeros, and the cyclic reading would take them from the top of $D$, which is also zero. A de Bruijn sequence has each $n$-bit word exactly once among its $w = 2^n$ cyclic windows, so the $w$ windows are distinct, and $T$ is well defined and inverts the map $k \mapsto i$. The full proof, with the identity of line L1, is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** Line L1 is one negation and one AND, line L2 one multiplication, line L3 one shift and line L4 one memory read. On the word RAM, where a multiplication of two $w$-bit words costs one step, this is $\Theta(1)$ in every case. The table is filled once in $\Theta(w)$ steps, or written into the program as a constant.

**Space.** The table holds $w$ small integers, so the extra space is $\Theta(w)$ words, or $\Theta(w \log w)$ bits; 32 bytes for $w = 32$ and 64 bytes for $w = 64$ when each entry is one byte. Apart from the table the scan uses $\Theta(1)$ words.

**On real hardware.** The four lines form a dependency chain whose length is about the latency of one multiplication plus a few cycles. A processor with a trailing-zero instruction does the same work in one instruction, so the de Bruijn scan pays only where that instruction is missing or slow.

## Properties

- **Word size and sign.** It needs $w$ to be a power of two, $w = 2^n$, and treats $x$ as unsigned. For other widths, use the next power of two and a de Bruijn sequence of that order, or the modulo-37 method of [trailing-zero count](/trailing-zero-count/).
- **Branch-free.** There is no loop and no branch, so the time does not depend on $x$.
- **Perfect hash.** The map $2^k \mapsto ((2^k D) \bmod 2^w) \gg (w - n)$ is a minimal [perfect hash function](/perfect-hash-function/) from the $w$ powers of two onto $\{0, \dots, w - 1\}$, of the [multiplicative](/multiplicative-hashing/) kind.
- **Many constants.** The number of binary de Bruijn sequences of order $n$ is $2^{2^{n-1} - n}$, and each has one rotation that starts with $n$ zeros. For $n = 3$ there are two, $00010111$ and $00011101$, that is `0x17` and `0x1D`; for $n = 6$ there are $2^{26}$. The rotation one place to the left also works: it starts with $n - 1$ zeros and ends with a zero, and the shift brings zeros in from the right, so the windows stay distinct. These are exactly the other constants that work. For $w = 8$ they are `0x2E` and `0x3A`, so four constants work in all, and for $w = 16$ there are 32.
- **Zero is not handled.** For $x = 0$, line L1 gives $b = 0$, so $p = 0$ and $i = 0$, and the scan returns $T[0] = 0$, the same answer as for $x = 1$.

## Variants and improvements

- **Highest set bit.** To get $\lfloor \lg x \rfloor$, first smear the highest 1-bit to the right, $s = x \vee (x \gg 1) \vee (x \gg 2) \vee \dots$, with $n$ shift-and-OR steps. Then $s \oplus (s \gg 1)$ is $2^{\lfloor \lg x \rfloor}$, and the same multiplication and table give its index. This computes the [floor of the base-2 logarithm](/floor-log2/) and the [leading-zero count](/leading-zero-count/) $w - 1 - \lfloor \lg x \rfloor$. For $w = 32$ one can also multiply $s = 2^{j+1} - 1$ directly by `0x07C4ACDD` with its own table, since the 32 values of $s$ also give 32 distinct top fields.
- **Clear instead of isolate.** Some versions multiply $x \oplus (x - 1) = 2^{k+1} - 1$ instead of $x \wedge (-x)$. The product is then a sum of shifted copies of $D$, and the constant must be chosen for these values instead; the 64-bit constant above happens to work for both.
- **Modulo a prime.** The value $2^k \bmod 37$ is different for $k = 0, \dots, 31$, because 2 has order 36 modulo 37. So $T[b \bmod 37]$ is another constant-time scan, with a division instead of a multiplication and a table of 37 entries.
- **Larger words.** For a word of $2w$ bits, scan the low half, and the high half when the low half is zero. In the [fusion tree](/fusion-tree/) and similar word-RAM structures the most significant bit of a word is found in constant time with multiplications only, without a table of size $w$.
- **Hardware.** Use the trailing-zero or bit-scan instruction when the target has one; compilers expose it as `__builtin_ctz` or C++20 `std::countr_zero`.

## When to use it

Use the hardware instruction when the processor has it, through the compiler intrinsic. Use the de Bruijn scan when it does not, or when the code must be portable and branch-free with a fixed running time. Against the binary search on the bits described under [trailing-zero count](/trailing-zero-count/), which takes $n$ steps with branches or masks, it is shorter and has no data-dependent branch, but it needs a fast multiplier. Against a byte-wise [table lookup](/table-lookup/), it needs a table of only $w$ entries. In loops that visit every 1-bit of a word, as in [bitboard](/bitboard/) programs and in iterations over a [bit set](/bit-set/), combine it with $x \gets x \wedge (x - 1)$ to clear the bit just found.

## Pitfalls

- **Zero input.** Line L1 gives $b = 0$ for $x = 0$, and line L4 then returns 0 as if bit 0 were set. Test $x \ne 0$ before the call, or return $w$ for zero by a separate test.
- **Missing reduction modulo $2^w$.** Line L2 must keep only the low $w$ bits of the product. In C with `uint16_t` or `uint8_t`, the operands are promoted to `int` (C11 Section 6.3.1.1), the product is not truncated, and the shift of line L3 then reads the wrong bits. Write line L2 as `(uint16_t)(b * 0x09AF)` before the shift, or use a type of exactly $w$ bits.
- **Signed types.** On a signed `int`, `x & -x` overflows when `x` is `INT_MIN`, which is undefined behaviour (C11 Section 6.5, paragraph 5), and `b * D` can overflow too. Do lines L1 to L3 on `uint32_t` or `uint64_t`, where arithmetic wraps modulo $2^w$.
- **Constant suffix.** The 64-bit constant needs a 64-bit type, for example `0x03F79D71B4CB0A89ULL` with `uint64_t` operands; with a 32-bit operand type, line L2 loses the high bits.
- **Wrong shift in line L3.** The shift must be $w - n$: 27 for $w = 32$ and 58 for $w = 64$. Copying the 32-bit shift into 64-bit code gives indices up to $2^{37}$ and reads outside the table.
- **Wrong constant for the variant.** A constant that works for $2^k$ does not always work for $2^{k+1} - 1$, and the reverse. Build the table from the values that line L2 actually multiplies, and check that no index occurs twice.

## Implementations

## History

Leiserson, Prokop and Randall wrote the method up in an MIT technical note dated 7 July 1998, with the construction for 64-bit words; their motivation was a fast way to find the position of a set bit. Knuth treats the ruler function $\rho x$ and this use of de Bruijn cycles in Volume 4A, Section 7.1.3, and Warren gives it among the trailing-zero methods of Hacker's Delight, Section 5-4. The underlying sequences are named after N. G. de Bruijn; see [de Bruijn sequence](/de-bruijn-sequence/) and the [de Bruijn graph](/de-bruijn-graph/), whose Eulerian circuits give them.

## References
