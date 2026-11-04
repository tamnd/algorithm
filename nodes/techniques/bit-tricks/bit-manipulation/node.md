---
tag: E1MVVA
kind: technique
slug: bit-manipulation
name: Bit manipulation
aliases:
- bit twiddling
- bit hacks
- bit tricks
area: techniques/bit-tricks
level: intro
summary: Solving problems by directly operating on the binary representation of integers.
prereqs: [bitwise-operations, twos-complement]
see_also: [bitmask, lowest-set-bit, simd-within-a-register, bit-parallelism, branchless-programming, table-lookup, word-ram, population-count]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2 (Basics), Section 2-1 (Manipulating Rightmost Bits), and Chapter 5 (Counting Bits)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer (2011)
    locator: Chapter 1 (Bit wizardry), Sections 1.1 to 1.8
  - url: https://graphics.stanford.edu/~seander/bithacks.html
    title: Sean Eron Anderson, Bit Twiddling Hacks
    locator: the whole collection, in particular Determine if a word has a zero byte, and Compute the minimum or maximum of two integers without branching
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5, paragraph 5 (signed overflow), Section 6.5.7, paragraphs 3 to 5 (shifts), and Section 6.3.1.1 (integer promotions)
---

Bit manipulation solves a problem by working on the binary representation of integers with [bitwise operations](/bitwise-operations/), shifts and ordinary arithmetic, instead of on their numeric values alone. The two ideas behind it are that one word operation acts on all $w$ bits at once, which is [bit parallelism](/bit-parallelism/), and that a few algebraic identities connect arithmetic with the bit pattern, such as $x \wedge (x - 1)$, which clears the [lowest set bit](/lowest-set-bit/). With them, tasks such as testing for a [power of two](/power-of-two-test/), [counting 1-bits](/population-count/), finding the [lowest](/trailing-zero-count/) or [highest](/floor-log2/) 1-bit, or iterating over a [bitmask](/bitmask/) take a constant or logarithmic number of word operations and no branches. Warren's Hacker's Delight, Knuth's Section 7.1.3 and Arndt's Chapter 1 collect the tricks.

## In plain words

A computer stores an integer as a row of bits, and it can change all the bits of a row in one step. Bit manipulation uses this. Instead of looking at the bits one by one in a loop, you look for a short formula that does the whole job on the full row.

Many such formulas come from what happens when you add or subtract one: the change runs from the right end up to the first bit that stops it. Others come from cutting the row into small pieces and letting each piece do its own small sum at the same time. The formulas are short and fast, but each one has rules about the size of the row and about negative numbers, and you must know them.

## When it applies

Look for these signals.

- The data are small integers, flags or sets over a universe of at most a few hundred elements, so that they fit in one word or a few words.
- The question is about the bit pattern: the number of 1-bits, the position of the lowest or highest 1-bit, a power of two, a parity, a reversal or an interleaving of bits.
- The same simple operation must be applied to many small fields, such as the bytes of a word; then one word operation can do it for all fields, as in [SIMD within a register](/simd-within-a-register/).
- The code must run without branches, for speed on unpredictable data or for constant-time cryptographic code; see [branchless programming](/branchless-programming/).
- An exponential algorithm loops over all subsets of a small set; the subsets are then the integers $0, \dots, 2^n - 1$, as in [bitmask DP](/bitmask-dp/).
- A dynamic program over a string has a table whose columns differ by small amounts, so that a column can be stored as a bit vector, as in [bit-parallel LCS](/bit-parallel-lcs/) and the [Bitap algorithm](/bitap-algorithm/).

## The template

Most tricks follow one of two forms. All words are unsigned $w$-bit words with arithmetic modulo $2^w$, unless the trick says otherwise; the holes are the parts in capitals.

**Form 1: visit the 1-bits.** The work is done once per 1-bit, from the lowest to the highest.

```pseudo id=main
FOR-EACH-SET-BIT(x)                ▷ x: an unsigned w-bit word
L1  while x ≠ 0
L2      b ← x ∧ (−x)                ▷ the lowest 1-bit alone, b = 2^k
L3      VISIT(b)                    ▷ hole: the work for one member; k = CTZ(b) if the index is needed
L4      x ← x ⊕ b                   ▷ clear it; equal to x ∧ (x − 1)
```

The loop runs once per 1-bit of $x$, so its cost is the [population count](/population-count/) $\nu(x)$, not $w$. The identity of line L2 holds because $-x = \overline{x} + 1$ agrees with $x$ at the lowest 1-bit and below it and disagrees above it.

**Form 2: fold in $\lg w$ rounds.** The work combines the bits of a word by halves, quarters and so on.

```pseudo id=fold
FOLD(x)                            ▷ x: an unsigned w-bit word, w a power of two
F1  for s ← w/2, w/4, …, 1         ▷ or 1, 2, 4, …, w/2, depending on the trick
F2      x ← COMBINE(x, (x ≫ s) ∧ MASK_s)   ▷ holes: COMBINE (⊕, ∨ or +) and the masks
F3  return RESULT(x)               ▷ hole: the field of x that holds the answer
```

With COMBINE $= \oplus$ and no mask, bit 0 ends as the [parity](/bit-parity/) of $x$. With COMBINE $= \vee$ and the shifts in the order 1, 2, 4, the word ends with every bit below the highest 1-bit set, the smear used for the [next power of two](/next-power-of-two/). With COMBINE $= +$ and the masks `0x55…`, `0x33…`, `0x0F…`, the fields hold partial sums of bits, the [SWAR popcount](/swar-popcount/). Each round costs $O(1)$ word operations, so a fold costs $O(\lg w)$.

To use either form: choose the encoding of the data as bits, fill the holes, and prove the identity on which each line rests. Since the identities involve only $+$, $-$ and bitwise operations, in which bit $t$ of the result depends only on bits $0$ to $t$ of the operands, a trick that is right for one word size is usually right for every size; a test on all 8-bit or all 16-bit words then catches most errors.

## Classic examples

- **[Power-of-two test](/power-of-two-test/).** $x \ne 0$ and $x \wedge (x - 1) = 0$: one step of Form 1 shows whether a second 1-bit exists.
- **[Kernighan's popcount](/kernighan-popcount/).** Form 1 with VISIT counting: the loop of lines L1 to L4 runs $\nu(x)$ times.
- **[XOR swap](/xor-swap/) and [single number](/single-number/).** The group laws $a \oplus a = 0$ and $a \oplus 0 = a$ replace a temporary variable or a hash table.
- **[Bit parity](/bit-parity/) and [SWAR popcount](/swar-popcount/).** Form 2 with $\oplus$ and with $+$.
- **[Next power of two](/next-power-of-two/) and [floor of log2](/floor-log2/).** Form 2 with $\vee$ smears the highest 1-bit to the right, and then one more step reads it off.
- **[De Bruijn bit scan](/de-bruijn-bit-scan/).** Isolate the lowest 1-bit as in line L2, multiply by a de Bruijn constant, and look the top bits up in a table of $w$ entries.
- **[Sign extension](/sign-extension/).** $(v \oplus m) - m$ with $m = 2^{k-1}$ widens a signed $k$-bit field without a branch.
- **[Gosper's hack](/gospers-hack/) and [submask enumeration](/submask-enumeration/).** The next $k$-subset and the next submask, each in a few word operations, for loops over [bitmasks](/bitmask/).
- **[Bitap](/bitap-algorithm/) and [bit-parallel LCS](/bit-parallel-lcs/).** A column of a dynamic-programming table is one bit vector, and a step of the DP is a few shifts, ANDs and one addition whose carries do the work.

## Variations

- **Table lookup.** Replace a computation on $w$ bits by a [table lookup](/table-lookup/) on $w/8$ bytes, trading memory for operations; this is the [Four Russians](/four-russians-method/) idea at the scale of one word.
- **Multiplication as a parallel shift.** A product with a constant that has several 1-bits adds several shifted copies of a word at once. The SWAR popcount sums its bytes with one multiplication by `0x0101…01`, and the [de Bruijn bit scan](/de-bruijn-bit-scan/) and [Morton encoding](/morton-encoding/) use products in the same way.
- **Field-parallel tests.** Treat a word as an array of bytes. The expression $(x - \texttt{0x0101…01}) \wedge \overline{x} \wedge \texttt{0x8080…80}$ is nonzero exactly when some byte of $x$ is zero, which string functions use to scan 8 bytes at a time.
- **Branch-free selection.** A comparison result $c \in \{0, 1\}$ becomes the mask $-c$, all zeros or all ones, and $y \oplus ((x \oplus y) \wedge -c)$ selects $x$ when $c = 1$ and $y$ when $c = 0$; with $c = [x < y]$ this is $\min(x, y)$.
- **Hardware instructions.** Modern processors have instructions for popcount, leading and trailing zeros, bit extract and deposit, and carry-less multiplication. Compilers expose them as intrinsics, for example `__builtin_popcount` and C++20 `<bit>`; the tricks remain the portable fallback and the way to reason about what the instructions compute.
- **Words of many words.** The same operations on arrays of words give [bit sets](/bit-set/), [bitboards](/bitboard/) and the bit-vector rows of a [bitset adjacency matrix](/bitset-adjacency-matrix/).

## Pitfalls

- **Shift by the word size or more.** In C, `x << s` and `x >> s` with $s \ge$ the width of the promoted type, or $s < 0$, are undefined (C11 Section 6.5.7, paragraph 3), and x86 processors use only the low bits of the count. Expressions such as `x >> (w - k)` break at $k = 0$; handle the edge case or split the shift in two.
- **Signed overflow.** On signed types, `x + y`, `-x` and `x << s` can overflow, which is undefined behaviour (C11 Section 6.5, paragraph 5, and Section 6.5.7, paragraph 4); `x & -x` on `INT_MIN` is an example. Do bit tricks on unsigned types of a fixed width, such as `uint32_t`.
- **Right shift of a negative value.** It is implementation-defined in C (Section 6.5.7, paragraph 5). Tricks that need an arithmetic shift, such as the sign mask $x \gg (w - 1)$, should state this assumption or use unsigned arithmetic with the XOR-subtract form of [sign extension](/sign-extension/).
- **Integer promotion.** Operands of type `uint8_t` and `uint16_t` become `int` before the operation (C11 Section 6.3.1.1). Then `~x` is negative and `x << 8` keeps the high bits. Cast the result back to the narrow type before comparing or shifting right.
- **Precedence.** `&`, `^` and `|` bind more loosely than `==` and `<` in C, Java and related languages, so `x & mask == 0` tests `x & (mask == 0)`. Use parentheses.
- **The zero word.** Many tricks have an exception at $x = 0$: the lowest set bit, the trailing-zero count, the floor of the logarithm, the next power of two. GCC's `__builtin_ctz(0)` and `__builtin_clz(0)` are undefined. Test for zero, or use a function whose result at zero is defined.
- **Unbounded integers.** In Python, `~x` is $-x - 1$ and a negative number has infinitely many 1-bits, so `(-1).bit_count()` is 1 while the 64-bit word of $-1$ has 64 ones. Mask with `(1 << w) - 1` to simulate a $w$-bit word.
- **Clever but slower.** A trick that was fast on an old machine can be slower than the plain code on a modern one, and it is harder to read. The [XOR swap](/xor-swap/) is the standard example. Measure, and prefer the compiler intrinsic when one exists.

## Exercises

1. Prove that for every unsigned $w$-bit word $x \ne 2^w - 1$, $x \wedge (x + 1)$ clears the trailing 1-bits of $x$ and $\overline{x} \wedge (x + 1)$ isolates the lowest 0-bit. Write $x = c\,0\,1^j$ in binary.
   <details><summary>Hint</summary>Adding 1 carries through the $j$ trailing ones, so $x + 1 = c\,1\,0^j$.</details>
2. Prove that $\lfloor (x + y) / 2 \rfloor = (x \wedge y) + ((x \oplus y) \gg 1)$ for unsigned $x, y$, and explain why the right side cannot overflow a $w$-bit word while $x + y$ can.
   <details><summary>Hint</summary>Use $x + y = 2(x \wedge y) + (x \oplus y)$. The right side is computed without ever forming $x + y$, and its value is the average, which is at most $2^w - 1$.</details>
3. Show that the expression $(x - \texttt{0x0101}) \wedge \overline{x} \wedge \texttt{0x8080}$, on 16-bit words, is nonzero exactly when one of the two bytes of $x$ is zero. Then find a word $x$ for which the high byte is not zero but its flag bit is set anyway, and explain why the yes or no answer is still right.
   <details><summary>Hint</summary>A borrow from a zero low byte can reach the high byte. Try $x = \texttt{0x0100}$.</details>
4. Let $g(i) = i \oplus (i \gg 1)$. Prove that $g(i)$ and $g(i - 1)$ differ in exactly one bit for every $i \ge 1$, and find its position in terms of the lowest set bit of $i$. This is the [binary-to-Gray conversion](/binary-to-gray-conversion/).
5. Write a branch-free function that returns the absolute value of a signed 32-bit integer from the sign mask $s = x \gg 31$ (arithmetic shift), and state for which input it overflows and what it returns there in two's complement.
   <details><summary>Hint</summary>$(x \oplus s) - s$; the input $-2^{31}$ has no positive counterpart.</details>
6. Use Form 1 to list, for a mask $m$ over $n$ elements, all the elements of $m$ in increasing order, and use the loop $s \gets (s - 1) \wedge m$ to list all its submasks. Prove that the total number of submask steps over all $2^n$ masks is $3^n$.

## References
