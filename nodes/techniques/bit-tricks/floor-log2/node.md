---
tag: YBA3D2
kind: problem
slug: floor-log2
name: Floor of log base 2
aliases:
- integer logarithm base 2
- ilog2
- most significant bit index
area: techniques/bit-tricks
level: intro
summary: Computing the index of the most significant 1-bit, which equals floor(log2 x) for x > 0.
prereqs: [logarithms, bitwise-operations]
see_also: [leading-zero-count, trailing-zero-count, next-power-of-two, de-bruijn-bit-scan, sparse-table, elias-gamma-coding, radix-heap, fusion-tree]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 5, Section 5-3 (Counting Leading 0's), and Chapter 11, Section 11-4 (Integer Logarithm)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on the binary logarithm function
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Springer (2011)
    locator: Chapter 1, Section 1.7 (Functions related to the base-2 logarithm)
  - url: https://graphics.stanford.edu/~seander/bithacks.html
    title: Sean Eron Anderson, Bit Twiddling Hacks
    locator: section Find the log base 2 of an integer (with the MSB N set in O(N) operations, with a lookup table, with a de Bruijn multiply, and with an IEEE float)
---

The floor of log base 2 of a positive integer $x$ is the integer $\lfloor \lg x \rfloor$, the largest $k$ with $2^k \le x$. In binary it is the index of the highest 1-bit, so it equals the number of binary digits of $x$ minus one, and $w - 1 - \operatorname{clz}(x)$ for a $w$-bit word. Knuth writes it $\lambda x$. It is computed exactly with integer operations: a binary search in $\Theta(\log w)$ steps, a [leading zero count](/leading-zero-count/) instruction, or a [de Bruijn](/de-bruijn-bit-scan/) multiplication after smearing. A floating-point `log2` is not a safe substitute: in double precision it rounds $\lg(2^{49} - 1)$ up to exactly 49.

## In plain words

Ask how many times you can double 1 before you pass the number. For 180, the powers of two are 1, 2, 4, 8, 16, 32, 64, 128 and then 256, which is too big; 128 is two to the power 7, so the answer is 7. In binary, 180 is 10110100, and the leading 1 sits at position 7 when you count positions from 0 on the right.

So the answer is the position of the leading 1, or the number of binary digits minus one. Programs use it to pick a size class, the level of a tree, or a table row, and they compute it with bit operations, not with a floating-point logarithm, which can round to the wrong whole number.

## Definition

**Input.** An integer $x$ with $1 \le x < 2^w$, as an unsigned $w$-bit word, or an integer $x \ge 1$ of any size.

**Output.** The unique integer $k \ge 0$ with
$$2^k \le x < 2^{k+1},$$
written $\lfloor \lg x \rfloor$ or $\lambda x$. The definitions agree: since $\lg$ is increasing, $2^k \le x < 2^{k+1}$ is the same as $k \le \lg x < k + 1$. If the highest 1-bit of $x$ is at position $k$, then $x \ge 2^k$, and $x \le \sum_{i \le k} 2^i = 2^{k+1} - 1$. So $\lfloor \lg x \rfloor$ is that position, and
$$\lfloor \lg x \rfloor = \operatorname{bitlen}(x) - 1 = w - 1 - \operatorname{clz}_w(x).$$

**Zero.** $\lg 0$ is not defined. Knuth sets $\lambda 0 = -\infty$; many libraries return $-1$, which matches $\operatorname{bitlen}(0) - 1$. The caller must handle $x = 0$.

**Signed inputs.** For a signed type, only $x > 0$ is valid. A negative value has its top bit set in [two's complement](/twos-complement/), so a bit-level method returns $w - 1$, which is not a logarithm of anything.

## Variants

- **Ceiling.** $\lceil \lg x \rceil$ for $x \ge 1$ is $\operatorname{bitlen}(x - 1)$: it is $\lfloor \lg x \rfloor$ when $x$ is a power of two and one more otherwise. For $x = 1$ it is 0.
- **Highest power of two.** $2^{\lfloor \lg x \rfloor}$, the largest power of two at most $x$; see [next power of two](/next-power-of-two/).
- **Other bases.** $\lfloor \log_{10} x \rfloor$ is computed from $\lfloor \lg x \rfloor$ with a table and one comparison, as in Hacker's Delight Section 11-4.
- **Lowest set bit.** The index of the *lowest* 1-bit is the [trailing zero count](/trailing-zero-count/); for a power of two the two indices are equal.
- **Arbitrary-precision integers.** `int.bit_length() - 1` in Python, `BigInteger.bitLength() - 1` in Java: the library stores the number of words, so the cost is $O(1)$ plus one word operation.

## Examples

| $x$ | binary | $\lfloor \lg x \rfloor$ | $\lceil \lg x \rceil$ | $\operatorname{clz}_{32}(x)$ |
|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 31 |
| 2 | 10 | 1 | 1 | 30 |
| 3 | 11 | 1 | 2 | 30 |
| 180 | 10110100 | 7 | 8 | 24 |
| 1000 | 1111101000 | 9 | 10 | 22 |
| $2^{31}$ | 1 followed by 31 zeros | 31 | 31 | 0 |

**Floating point gives a wrong answer.** For $x = 2^{49} - 1 = 562949953421311$, the true value is $\lfloor \lg x \rfloor = 48$, because $x < 2^{49}$. The number $x$ is exactly representable as a double, but $\lg x = 49 - 2.56 \ldots \times 10^{-15}$, and the nearest double to that is 49.0. Python's `math.log2(2**49 - 1)` returns `49.0`, and the floor is 49. Among the values $2^k - 1$ for $k = 1$ to 63, the floor of `math.log2` is wrong for each $k$ from 49 to 63.

## Known algorithms

Costs are word operations on the [word RAM](/word-ram/), for $1 \le x < 2^w$.

| method | operations | notes |
|---|---|---|
| loop: shift right until $x = 1$, counting | $\Theta(\lfloor \lg x \rfloor + 1)$ | fine for small $x$ |
| binary search over shifts | $\Theta(\log w)$ | if $x \ge 2^{16}$, add 16 and shift right by 16; then 8, 4, 2, 1 |
| [leading zero count](/leading-zero-count/) | 1 instruction and a subtraction | $w - 1 - \operatorname{clz}(x)$; x86 `BSR` returns the index directly |
| smear, isolate, [de Bruijn](/de-bruijn-bit-scan/) | $2 \lg w + O(1)$, a table of $w$ entries | smear $x$ to $s = 2^{k+1} - 1$, then $s \oplus (s \gg 1) = 2^k$ |
| table of 256 entries | $O(\log(w/8))$ tests and one lookup | find the top nonzero byte |
| double conversion | $O(1)$ | read the exponent field of the double nearest to $x$, minus 1023; exact only for $x < 2^{53}$ |
| Fredman and Willard | $O(1)$ with multiplication | the most significant bit in constant time; see [fusion tree](/fusion-tree/) |

**Binary search for $w = 32$.** Set $k \gets 0$. For $s = 16, 8, 4, 2, 1$ in turn: if $x \ge 2^s$, then $k \gets k + s$ and $x \gets x \gg s$. Return $k$. The invariant is that the answer equals $k + \lfloor \lg x \rfloor$ for the current $x$, and the current $x$ is less than $2^{2s}$ before the step with $s$. After the step with $s = 1$, $x = 1$.

**Why the double exponent works and when it fails.** For $1 \le x < 2^{53}$, the conversion to IEEE double precision is exact, and the stored value is $1.f \times 2^e$ with $e = \lfloor \lg x \rfloor$. For larger $x$ the conversion rounds to the nearest double; when $x$ is just below a power of two, it rounds up to that power: $2^{64} - 1$ becomes $2^{64}$, with $e = 64$.

## Bounds

**Upper bounds.** $O(\log w)$ operations with comparisons and shifts; $O(1)$ with multiplication on the word RAM, by Fredman and Willard; one instruction on processors with `LZCNT`, `BSR` or `CLZ`.

**Output size.** The answer lies in $[0, w - 1]$, so it has $\lceil \lg w \rceil$ bits; for a 64-bit word, 6 bits.

## Reductions

- **To and from the leading zero count**: $\lfloor \lg x \rfloor = w - 1 - \operatorname{clz}_w(x)$, one subtraction each way.
- **From the trailing zero count of a power of two**: after isolating the top bit as $2^k$, any method for the index of a single 1-bit gives $k$, including the [de Bruijn bit scan](/de-bruijn-bit-scan/).
- **The next power of two**: $2^{\lceil \lg x \rceil} = 2^{\operatorname{bitlen}(x - 1)}$ for $x \ge 1$.

## Applications

- **[Sparse tables](/sparse-table/).** A range minimum query on $[l, r]$ uses the level $\lfloor \lg (r - l + 1) \rfloor$.
- **Size classes.** Memory allocators pick the size class of a request from $\lceil \lg n \rceil$, and a common form of the [radix heap](/radix-heap/) puts a key into the bucket given by the bit length of its XOR with the last extracted key.
- **Codes.** [Elias gamma coding](/elias-gamma-coding/) writes $\lfloor \lg x \rfloor$ zeros, then $x$ in binary.
- **Tree levels.** In an implicit [binary heap](/binary-heap/) stored from index 1, node $i$ is at depth $\lfloor \lg i \rfloor$.
- **Starting points.** The first guess of Newton's method for the [integer square root](/integer-square-root/) is $2^{\lceil (\lfloor \lg x \rfloor + 1) / 2 \rceil}$, which is at least $\sqrt{x}$.

## References
