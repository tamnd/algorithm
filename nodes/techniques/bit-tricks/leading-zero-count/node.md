---
tag: FB970N
kind: problem
slug: leading-zero-count
name: Leading zero count
aliases:
- count leading zeros
- clz
- bit scan reverse
area: techniques/bit-tricks
level: intro
summary: Counting the zero bits above the most significant 1-bit of a fixed-width integer.
prereqs: [bitwise-operations, floor-log2]
see_also: [trailing-zero-count, floor-log2, next-power-of-two, de-bruijn-bit-scan, population-count, hyperloglog, fusion-tree, integer-square-root]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 5, Section 5-3 (Counting Leading 0's)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on the binary logarithm function and the leftmost bit
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Springer (2011)
    locator: Chapter 1, Section 1.6 (Operations on high bits or blocks of a word) and Section 1.7 (Functions related to the base-2 logarithm)
  - paper: doi:10.1016/0022-0000(93)90040-4
    title: Michael L. Fredman and Dan E. Willard, Surpassing the information theoretic bound with fusion trees, Journal of Computer and System Sciences 47(3), 1993
    locator: pp. 424 to 436 (the constant-time computation of the most significant bit with multiplication)
---

The leading zero count $\operatorname{clz}(x)$ of a $w$-bit word $x$ is the number of 0-bits above its highest 1-bit. For $x \ne 0$ it equals $w - 1 - \lfloor \lg x \rfloor$, so it is the [floor of log2](/floor-log2/) seen from the other end of the word, and unlike the [trailing zero count](/trailing-zero-count/) it depends on the word size $w$. Software computes it by binary search in $\Theta(\log w)$ steps, by smearing the highest bit down and taking a [population count](/population-count/), or through the exponent of a floating-point conversion; most processors have an instruction. The value for $x = 0$ is a convention, and the C built-in `__builtin_clz(0)` is undefined.

## In plain words

Write a number in binary with a fixed number of digits, padded with zeros on the left, and count the zeros before the first one. In 32 bits, the number 180 is twenty-four zeros followed by 10110100, so the count is 24.

The count tells you how many bits the number really uses: 32 minus 24 is 8 bits. Programs use it to shift a number left until its top bit is set (as floating-point hardware does), to find the next power of two, to estimate how many distinct items a stream has, and to start a square root at a good first guess.

## Definition

**Input.** A $w$-bit word $x$, read as an unsigned integer $0 \le x < 2^w$.

**Output.** For $x \ne 0$,
$$\operatorname{clz}_w(x) = w - 1 - \max\{\, i : x_i = 1 \,\} = w - 1 - \lfloor \lg x \rfloor = w - \operatorname{bitlen}(x),$$
an integer from 0 to $w - 1$. Here $\operatorname{bitlen}(x) = \lfloor \lg x \rfloor + 1$ is the number of binary digits of $x$, which is `int.bit_length` in Python.

**The zero input.** The usual convention is $\operatorname{clz}_w(0) = w$, so that $\operatorname{clz}_w(x) = w - \operatorname{bitlen}(x)$ holds with $\operatorname{bitlen}(0) = 0$. The x86 instruction `LZCNT`, the ARM instruction `CLZ`, C++20 `std::countl_zero` and C23 `stdc_leading_zeros` follow it. The older x86 instruction `BSR` returns the index $\lfloor \lg x \rfloor$, not the count, and leaves its destination undefined when $x = 0$. GCC's `__builtin_clz(0)` is undefined.

**Width.** The answer changes with $w$: $\operatorname{clz}_{64}(x) = \operatorname{clz}_{32}(x) + 32$ for $0 < x < 2^{32}$. In C, `__builtin_clz` works on `unsigned int` and `__builtin_clzll` on `unsigned long long`, and a `uint8_t` argument is first promoted, so the count includes the extra 24 zeros.

**Signed words.** A negative value in [two's complement](/twos-complement/) has its top bit set, so its clz is 0. Counting leading *sign* bits ($\operatorname{cls}$, the number of bits equal to the sign bit after it) is a separate operation.

## Variants

- **Index of the highest set bit.** $\lfloor \lg x \rfloor = w - 1 - \operatorname{clz}(x)$; see [floor of log2](/floor-log2/).
- **Leading ones.** $\operatorname{clo}(x) = \operatorname{clz}(\lnot x)$.
- **Normalization shift.** The shift $s = \operatorname{clz}(x)$ makes $x \ll s$ have its top bit set. Long division of big integers (Knuth's Algorithm D) and software floating point use it.
- **Highest set bit as a mask.** $2^{\lfloor \lg x \rfloor}$, the [previous power of two](/next-power-of-two/).
- **Leading sign bits.** For signed fixed-point arithmetic, the count of redundant sign bits.

## Examples

For $w = 32$:

| $x$ | $\operatorname{bitlen}(x)$ | $\operatorname{clz}_{32}(x)$ |
|---|---|---|
| 0 | 0 | 32 by convention |
| 1 | 1 | 31 |
| 180 | 8 | 24 |
| 65535 $= 2^{16} - 1$ | 16 | 16 |
| 65536 $= 2^{16}$ | 17 | 15 |
| $2^{31}$ | 32 | 0 |

**Smearing and popcount.** For $x = 180$, the steps $x \gets x \vee (x \gg 1)$, $x \gets x \vee (x \gg 2)$, $x \gets x \vee (x \gg 4)$, $x \gets x \vee (x \gg 8)$, $x \gets x \vee (x \gg 16)$ give $x = 2^8 - 1 = 255$: all bits from the highest 1-bit down are set. Then $\operatorname{clz}_{32}(180) = 32 - \nu(255) = 24$, or equally $\nu(\lnot 255)$ in 32 bits.

**A floating-point pitfall.** Converting a 32-bit integer to IEEE single precision and reading its exponent gives $\lfloor \lg x \rfloor$ only when the conversion is exact. For $x = 2^{25} - 1$ the conversion rounds to $2^{25}$, so the exponent is 25, which gives $\operatorname{clz}_{32} = 6$; the right value is 7. Double precision is exact for all 32-bit integers, so the trick is safe there, but not for 64-bit integers above $2^{53}$.

## Known algorithms

Costs are word operations on the [word RAM](/word-ram/).

| method | operations | notes |
|---|---|---|
| loop: shift left until the top bit is 1 | $\Theta(\operatorname{clz}(x) + 1)$, up to $w$ | slow for small $x$ |
| binary search | $\Theta(\log w)$; five tests for $w = 32$ | Hacker's Delight 5-3 |
| smear, then popcount | $2 \lg w$ for the smear, then one popcount | branch-free; $\operatorname{clz}(x) = \nu(\lnot s)$ for the smeared $s$ |
| smear, isolate, [de Bruijn](/de-bruijn-bit-scan/) | $2 \lg w + O(1)$ and a table of $w$ entries | isolate the top bit with $s \oplus (s \gg 1)$ |
| floating-point conversion | $O(1)$ | exact for $x < 2^{53}$ with doubles |
| table of 256 entries | $O(\log(w/8))$ tests, then one lookup | find the top nonzero byte, then look it up |
| multiplication tricks of Fredman and Willard | $O(1)$ | constant time on the word RAM with multiplication; large constants |
| hardware | 1 | x86 `LZCNT`, `BSR`; ARM `CLZ` |

**Binary search for $w = 32$.** Set $n \gets 0$. If $x \le \texttt{0x0000FFFF}$, then $n \gets n + 16$ and $x \gets x \ll 16$. Then test $x \le \texttt{0x00FFFFFF}$ with step 8, $x \le \texttt{0x0FFFFFFF}$ with step 4, $x \le \texttt{0x3FFFFFFF}$ with step 2, and $x \le \texttt{0x7FFFFFFF}$ with step 1. The result is $n$. Each test asks whether the top half of the remaining window is empty and, if so, shifts the window up. For $x = 0$ this returns 31, so a separate test must return 32.

## Bounds

**Upper bounds.** $O(\log w)$ operations with comparisons and shifts, by binary search. $O(1)$ operations on the word RAM with multiplication, by Fredman and Willard's method for the most significant bit, which their fusion trees use. With an instruction, one step.

**Cost of the smear.** The smear takes $\lg w$ rounds of shift and OR, so each method that starts with it costs $\Theta(\log w)$ operations, even when the step after it is $O(1)$.

## Reductions

- **clz and floor of log2.** $\operatorname{clz}_w(x) = w - 1 - \lfloor \lg x \rfloor$ for $x \ne 0$, in both directions with one subtraction.
- **clz from popcount.** $\operatorname{clz}_w(x) = \nu(\lnot \operatorname{smear}(x))$, where $\operatorname{smear}(x)$ sets all bits below the highest 1-bit.
- **ctz from clz.** $\operatorname{ctz}(x) = w - 1 - \operatorname{clz}(x \wedge -x)$ for $x \ne 0$, because $x \wedge -x$ is a single bit at position $\operatorname{ctz}(x)$.
- **Next power of two from clz.** For $2 \le x \le 2^{w-1}$, the smallest power of two at least $x$ is $2^{w - \operatorname{clz}(x - 1)}$; see [next power of two](/next-power-of-two/).

## Applications

- **Normalization.** Floating-point addition and big-integer division shift operands by clz so that the top bit is set.
- **[HyperLogLog](/hyperloglog/).** Each register stores the largest value of $\operatorname{clz}$ plus one over the hashed items it sees, an estimate of the logarithm of the number of distinct items.
- **[Integer square root](/integer-square-root/).** The bit length gives a first guess within a factor of two for Newton's method.
- **Variable-length encodings.** The number of bytes or bits needed to store $x$ is computed from $\operatorname{bitlen}(x) = w - \operatorname{clz}(x)$.
- **Priority bitmaps.** The highest-priority nonempty queue is the highest set bit of a bitmap.

## References
