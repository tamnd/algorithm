---
tag: PCP454
kind: problem
slug: power-of-two-test
name: Power-of-two test
aliases:
- is power of two
- check power of two
area: techniques/bit-tricks
level: intro
summary: Deciding whether x is a power of two, which holds exactly when x > 0 and x & (x-1) is zero.
prereqs: [lowest-set-bit, bitwise-operations]
see_also: [population-count, next-power-of-two, floor-log2, trailing-zero-count, hash-table, buddy-system, fast-fourier-transform, ac0]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2, Section 2-1 (Manipulating Rightmost Bits), and Chapter 3 (Power-of-2 Boundaries)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on removing and extracting the rightmost 1-bit
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer (2011)
    locator: Chapter 1, Section 1.3 (Operations on low bits or blocks of a word)
  - url: https://graphics.stanford.edu/~seander/bithacks.html
    title: Sean Eron Anderson, Bit Twiddling Hacks
    locator: section Determining if an integer is a power of 2
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5, paragraph 5 (signed overflow)
---

The power-of-two test decides whether an integer $x$ equals $2^k$ for some integer $k \ge 0$. On unsigned $w$-bit words the standard answer is the expression $x \ne 0 \wedge (x \wedge (x - 1)) = 0$: subtracting 1 clears the [lowest set bit](/lowest-set-bit/) of $x$ and sets the bits below it, so the AND is zero exactly when $x$ has no other 1-bit. The test takes three word operations, has no loop, and is equivalent to asking whether the [population count](/population-count/) of $x$ is 1. Programs use it to check sizes of [hash tables](/hash-table/), buffers and transforms that must be powers of two.

## In plain words

In binary, a power of two is a 1 followed by zeros: 1, 10, 100, 1000, and so on. Every other positive number has at least two 1-bits. So the question "is this a power of two" is the question "does this number have exactly one 1-bit".

Subtracting one from a number turns its rightmost 1 into a 0 and the zeros after it into ones. If that rightmost 1 was the only one, the number and the number minus one have no 1-bit in common. If there was another 1 further left, both numbers still have it. Zero needs its own test, because zero and "zero minus one" also have no 1-bit in common.

## Definition

**Input.** A word size $w \ge 1$ and an unsigned $w$-bit word $x \in \{0, 1, \dots, 2^w - 1\}$.

**Output.** True if $x \in \{2^0, 2^1, \dots, 2^{w-1}\}$, and false otherwise.

**Characterization.** For every unsigned $w$-bit word $x$, with arithmetic modulo $2^w$,

$$x \text{ is a power of two} \iff x \ne 0 \text{ and } x \wedge (x - 1) = 0 \iff \nu(x) = 1 \iff x \ne 0 \text{ and } x \wedge (-x) = x.$$

Here $\nu(x)$ is the number of 1-bits of $x$, Knuth's sideways sum. *Proof of the first equivalence.* If $x = 2^k$, then $x - 1 = 2^k - 1$ has 1-bits only at positions $0$ to $k - 1$, so the AND is 0. If $x \ne 0$ is not a power of two, let $k$ be the index of its lowest 1-bit; then $x - 1$ equals $x$ with bit $k$ cleared and bits $0$ to $k - 1$ set, so it keeps every 1-bit of $x$ above position $k$, and there is at least one, so the AND is not 0. For $x = 0$, $x - 1 = 2^w - 1$ and the AND is 0, which is why the test $x \ne 0$ is needed. The second and third equivalences follow from the same picture of $x - 1$ and $-x$; see [lowest set bit](/lowest-set-bit/).

**Count.** Exactly $w$ of the $2^w$ words are powers of two.

## Variants

- **Signed input.** For a signed integer, powers of two are positive by definition, so the test is $x > 0 \wedge (x \wedge (x - 1)) = 0$. In two's complement the most negative value $-2^{w-1}$ has the bit pattern $10\dots0$ and passes the bit test without the sign check.
- **Zero or a power of two.** $x \wedge (x - 1) = 0$ alone is true exactly for $x = 0$ and the $w$ powers of two. Some code wants this, for example when 0 means "no alignment constraint".
- **Power of four.** $x$ is a power of four exactly when it is a power of two and its single 1-bit is at an even position: $x \ne 0$, $x \wedge (x - 1) = 0$ and $x \wedge \texttt{0x5555\dots55} \ne 0$, with the mask of $w$ bits that has 1s at even positions (`0x55555555` for $w = 32$).
- **One less than a power of two.** $x = 2^j - 1$ for some $0 \le j \le w$ exactly when $x \wedge (x + 1) = 0$ modulo $2^w$; this tests that the 1-bits of $x$ form one block at the bottom.
- **Multiple of a power of two.** $x$ is a multiple of $2^k$ exactly when $x \wedge (2^k - 1) = 0$. This is the alignment test for an address and a power-of-two alignment.
- **Exponent.** When the test is true, the exponent $k$ is the [trailing-zero count](/trailing-zero-count/) of $x$, which equals [$\lfloor \lg x \rfloor$](/floor-log2/).
- **Arbitrary-precision integers.** In Python, `x > 0 and x & (x - 1) == 0` works for every size of `int`. `x.bit_count() == 1` (Python 3.10 and later) also works for $x > 0$, but `(-8).bit_count()` is 1, because `bit_count` counts the bits of the absolute value, so a negative input must be rejected first.

## Examples

All with $w = 8$.

| $x$ | binary | $x - 1$ | $x \wedge (x - 1)$ | answer |
|---|---|---|---|---|
| 0 | 00000000 | 11111111 | 00000000 | false ($x = 0$) |
| 1 | 00000001 | 00000000 | 00000000 | true ($2^0$) |
| 64 | 01000000 | 00111111 | 00000000 | true ($2^6$) |
| 96 | 01100000 | 01011111 | 01000000 | false |
| 128 | 10000000 | 01111111 | 00000000 | true ($2^7$) |
| 255 | 11111111 | 11111110 | 11111110 | false |

Read as a signed 8-bit value, the word 128 is $-128$, which is not a power of two; the signed test rejects it by the sign check. For the power-of-four variant, $64 = 2^6$ has its 1-bit at the even position 6 and is $4^3$, while $128 = 2^7$ is not a power of four.

## Known algorithms

| method | operations | notes |
|---|---|---|
| $x \ne 0 \wedge x \wedge (x - 1) = 0$ | 3 | the standard test, via the [lowest set bit](/lowest-set-bit/) |
| $x \ne 0 \wedge x \wedge (-x) = x$ | 3 | same idea, isolates the lowest 1-bit |
| [population count](/population-count/) $= 1$ | 1 with a popcount instruction | the hardware instruction or [SWAR popcount](/swar-popcount/) |
| $x \ne 0$ and $2^{\lfloor \lg x \rfloor} = x$ | a [leading-zero count](/leading-zero-count/) and a shift | also gives $k$ |
| divide by 2 while even | up to $w$ steps | the school method; slower |
| $\log_2 x$ in floating point is an integer | one call | wrong for large $x$, see below |

The floating-point method fails because a double has a 53-bit significand. `math.log2(2**k + 1)` returns exactly the integer $k$ for every $k$ from 49 to 63, so the test accepts $2^{49} + 1$ and the other 14 words of this form below $2^{64}$.

## Bounds

On the [word RAM](/word-ram/) the test takes $\Theta(1)$ time, with three operations. As a Boolean function of $w$ input bits, "exactly one bit is 1" is computed by a circuit of depth 3 and $O(w^2)$ gates: the OR over $i$ of ($x_i$ and no other $x_j$). So it lies in [AC0](/ac0/), unlike [parity](/bit-parity/). The bound $\Omega(1)$ is trivial; any correct test must read every bit of $x$ in the worst case, which a word operation does at once.

## Reductions

- **To population count.** $x$ is a power of two exactly when $\nu(x) = 1$, so one popcount and one comparison decide it.
- **To the lowest set bit.** $x$ is a power of two exactly when $x \ne 0$ and $x$ equals its lowest set bit $x \wedge (-x)$.
- **From the next power of two.** For $x \ge 1$, $x$ is a power of two exactly when the [next power of two](/next-power-of-two/) of $x$ is $x$ itself. This is slower than the direct test and only a check.

## Applications

- **Table sizes.** A [hash table](/hash-table/) whose size $m$ is a power of two maps a hash $h$ to a slot by $h \wedge (m - 1)$ instead of $h \bmod m$. The code checks $m$ with the power-of-two test.
- **Transforms.** The radix-2 [fast Fourier transform](/fast-fourier-transform/) needs a length that is a power of two; inputs of other lengths are padded to the [next power of two](/next-power-of-two/).
- **Memory allocators.** The [buddy system](/buddy-system/) splits blocks whose sizes are powers of two, and alignment arguments of allocation functions are required to be powers of two.
- **Trees on arrays.** A [segment tree](/segment-tree/) laid out in an array is a perfect binary tree when the number of leaves is a power of two, which some implementations require.
- **Circular buffers.** A ring buffer of size $2^k$ wraps its indices with one AND.

## References
