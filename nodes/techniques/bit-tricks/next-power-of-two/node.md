---
tag: DBSK6R
kind: problem
slug: next-power-of-two
name: Next power of two
aliases:
- round up to power of two
- ceiling power of two
area: techniques/bit-tricks
level: intro
summary: Finding the smallest power of two that is at least x, using bit smearing or leading-zero count.
prereqs: [power-of-two-test, floor-log2, bitwise-operations]
see_also: [leading-zero-count, de-bruijn-bit-scan, hash-table, fast-fourier-transform, buddy-system, segment-tree, dynamic-array, integer-overflow]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 3, Section 3-2 (Rounding Up/Down to the Next Power of 2), and Section 3-1 (Rounding Up/Down to a Multiple of a Known Power of 2)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on the binary logarithm λx and smearing bits to the right
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer (2011)
    locator: Chapter 1, Section 1.7 (Functions related to the base-2 logarithm)
  - url: https://graphics.stanford.edu/~seander/bithacks.html
    title: Sean Eron Anderson, Bit Twiddling Hacks
    locator: section Round up to the next highest power of 2
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5.7 (Bitwise shift operators), paragraph 3
---

The next power of two of a positive integer $x$ is the smallest power of two that is at least $x$, written $\lceil x \rceil_2 = 2^{\lceil \lg x \rceil}$. Warren calls it $clp2(x)$. On unsigned $w$-bit words there are two standard methods: smear the highest 1-bit of $x - 1$ into all lower positions and add 1, which takes $2\lg w + 2$ operations and no branch, or compute $2^{w - \mathrm{clz}(x - 1)}$ with one [leading-zero count](/leading-zero-count/). Both must deal with two edge cases: $x = 0$, and $x > 2^{w-1}$, where the answer $2^w$ does not fit in the word. The result is used to size [hash tables](/hash-table/), buffers of a [dynamic array](/dynamic-array/) and inputs of the [fast Fourier transform](/fast-fourier-transform/).

## In plain words

You have a number and you want the first power of two that is not smaller than it: for 5 that is 8, for 8 it is 8, for 9 it is 16. In binary, the answer has a single 1, one place to the left of the highest 1 of the number, unless the number is already a power of two.

The bit method first subtracts one, so that an exact power of two does not jump up. Then it copies the highest 1 into every place to its right, which turns the number into a block of ones such as 0111 1111. Adding one to a block of ones gives the next power of two, 1000 0000.

## Definition

**Input.** A word size $w \ge 1$ and an unsigned integer $x$ with $1 \le x \le 2^{w-1}$.

**Output.** The integer $\lceil x \rceil_2 = \min\{2^k : k \ge 0,\ 2^k \ge x\}$.

**Formulas.** For $x \ge 1$,

$$\lceil x \rceil_2 = 2^{\lceil \lg x \rceil} = 2^{\mathrm{bitlen}(x - 1)},$$

where $\mathrm{bitlen}(y)$ is the number of bits of $y$, with $\mathrm{bitlen}(0) = 0$; on $w$-bit words $\mathrm{bitlen}(y) = w - \mathrm{clz}(y)$. *Proof.* Let $b = \mathrm{bitlen}(x - 1)$. Then $x - 1 < 2^b$, so $x \le 2^b$. If $b = 0$, then $x = 1 = 2^0$. If $b \ge 1$, then $x - 1 \ge 2^{b-1}$, so $x > 2^{b-1}$, and no smaller power of two is at least $x$. $\square$

The input range stops at $2^{w-1}$ because for $2^{w-1} < x < 2^w$ the answer $2^w$ needs $w + 1$ bits.

**The companion.** The previous power of two, $\lfloor x \rfloor_2 = 2^{\lfloor \lg x \rfloor}$ for $x \ge 1$, is the largest power of two that is at most $x$; Warren calls it $flp2(x)$. It is $x$ with all 1-bits but the highest cleared; see [floor of log2](/floor-log2/).

## Variants

- **Value at zero.** The definition leaves $x = 0$ open. The smearing method returns 0 for $x = 0$, because $x - 1$ wraps to $2^w - 1$ and the final $+1$ wraps back to 0. C++20 `std::bit_ceil(0)` returns 1. A caller that sizes a buffer usually wants 1.
- **Overflow.** For $x > 2^{w-1}$, the smearing method wraps to 0. The leading-zero method computes a shift by $w$, which is undefined behaviour in C (C11 Section 6.5.7, paragraph 3). A safe function either checks $x \le 2^{w-1}$ first or returns a flag.
- **Strictly greater.** The smallest power of two strictly greater than $x$ is $2^{\mathrm{bitlen}(x)}$, the smearing method applied to $x$ instead of $x - 1$.
- **Previous power of two.** Smear $x$ to get $s$, then $\lfloor x \rfloor_2 = s - (s \gg 1)$, or $s \oplus (s \gg 1)$.
- **Exponent only.** The exponent $\lceil \lg x \rceil = \mathrm{bitlen}(x - 1)$ is often what the caller needs, for example the depth of a tree.
- **Multiple of a fixed power of two.** Rounding up to a multiple of $2^k$, not to a power of two, is $(x + 2^k - 1) \wedge \overline{(2^k - 1)}$ (Warren, Section 3-1). It is a different problem with a similar name.
- **Signed input.** On a signed type, negative $x$ has no next power of two in this sense; convert to unsigned only after checking $x \ge 1$.

## Examples

All with $w = 8$, using the smearing method, which returns 0 for $x = 0$ and for $x > 128$.

| $x$ | 0 | 1 | 2 | 3 | 5 | 64 | 65 | 100 | 128 | 129 | 255 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $\lceil x \rceil_2$ | (1 or 0) | 1 | 2 | 4 | 8 | 64 | 128 | 128 | 128 | (256) | (256) |
| smearing result | 0 | 1 | 2 | 4 | 8 | 64 | 128 | 128 | 128 | 0 | 0 |

**Trace of the smearing method on $x = 100$.** Each step ORs the word with a right shift of itself; after the shifts by 1, 2 and 4, every bit below the highest 1-bit is set.

| step | word | binary |
|---|---|---|
| $y \gets x - 1$ | 99 | 01100011 |
| $y \gets y \vee (y \gg 1)$ | 115 | 01110011 |
| $y \gets y \vee (y \gg 2)$ | 127 | 01111111 |
| $y \gets y \vee (y \gg 4)$ | 127 | 01111111 |
| $y + 1$ | 128 | 10000000 |

With the leading-zero method, $\mathrm{clz}_8(99) = 1$, and $2^{8 - 1} = 128$. For $x = 37$ the smear goes $36 = 00100100_2$, $54 = 00110110_2$, $63 = 00111111_2$, and the answer is 64. The previous power of two of 100 is 64.

## Known algorithms

| method | operations on $w$-bit words | notes |
|---|---|---|
| smear $x - 1$, add 1 | $\lg w$ shifts and ORs, 2 additions | Warren's $clp2$; branch-free; wraps to 0 at the edges |
| $1 \ll (w - \mathrm{clz}(x - 1))$ | one [leading-zero count](/leading-zero-count/), a shift | $\Theta(1)$ with a hardware instruction; needs care at $x = 1$ and $x > 2^{w-1}$ |
| double from 1 while below $x$ | up to $w$ steps | simple, slow for large $x$ |
| smear, then [de Bruijn bit scan](/de-bruijn-bit-scan/) | smear, multiply, table | gives the exponent without a clz instruction |
| floating point: $2^{\lceil \log_2 x \rceil}$ | one call | wrong near large powers of two, as for [floor of log2](/floor-log2/) |

In Python, `1 << (x - 1).bit_length()` is exact for every integer $x \ge 1$.

## Bounds

On the [word RAM](/word-ram/) with a leading-zero instruction, or with multiplication by the method of Fredman and Willard for the most significant bit, the next power of two takes $\Theta(1)$ time. With only shifts, Boolean operations and addition, the smearing method uses $\Theta(\lg w)$ operations. As a Boolean function of the $w$ bits, each output bit of the smear is an OR of input bits, so the problem has constant-depth circuits of polynomial size and is in [AC0](/ac0/).

## Reductions

- **To the leading-zero count.** $\lceil x \rceil_2 = 2^{w - \mathrm{clz}(x - 1)}$ for $2 \le x \le 2^{w-1}$, and 1 for $x = 1$. So one [leading-zero count](/leading-zero-count/) and one shift solve it.
- **To the floor of the logarithm.** $\lceil x \rceil_2 = 2^{\lfloor \lg (x - 1) \rfloor + 1}$ for $x \ge 2$; see [floor of log2](/floor-log2/).
- **To the previous power of two.** $\lceil x \rceil_2 = 2 \lfloor x - 1 \rfloor_2$ for $x \ge 2$.
- **Power-of-two test.** $x \ge 1$ is a power of two exactly when $\lceil x \rceil_2 = x$; the [power-of-two test](/power-of-two-test/) does it directly in three operations.

## Applications

- **Hash tables.** A [hash table](/hash-table/) of size $2^k$ reduces a hash by masking; the table for $n$ keys at load factor $\alpha$ gets size $\lceil n / \alpha \rceil_2$.
- **Growth of arrays.** A [dynamic array](/dynamic-array/) that doubles its capacity keeps capacities that are powers of two; the first capacity for $n$ items is $\lceil n \rceil_2$.
- **Transforms.** The radix-2 [fast Fourier transform](/fast-fourier-transform/) pads an input of length $n$ with zeros to length $\lceil n \rceil_2$; a product of polynomials of degrees $a$ and $b$ needs length $\lceil a + b + 1 \rceil_2$.
- **Trees on arrays.** An iterative [segment tree](/segment-tree/) over $n$ leaves often uses $\lceil n \rceil_2$ leaves so that the tree is perfect.
- **Memory allocators.** The [buddy system](/buddy-system/) serves a request of $s$ bytes from a block of size $\lceil s \rceil_2$.

## References
