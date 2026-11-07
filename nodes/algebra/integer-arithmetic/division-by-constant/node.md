---
tag: X1D62T
kind: problem
slug: division-by-constant
name: Division by a constant
aliases:
- division by invariant integer
- constant division
- reciprocal multiplication
area: algebra/integer-arithmetic
level: advanced
summary: Divide many integers by one fixed divisor using precomputed multipliers and shifts.
model: word-ram
complexity:
  vars: {w: the number of bits in a machine word}
  time: {worst: Θ(1)}
prereqs: [division-with-remainder, integer-division, word-ram]
see_also: [granlund-montgomery-division, barrett-reduction, montgomery-multiplication, modular-inverse, newton-raphson-division, long-division, floor-division, integer-division]
sources:
  - paper: doi:10.1145/178243.178249
    title: Torbjörn Granlund and Peter L. Montgomery, Division by invariant integers using multiplication, Proceedings of the ACM SIGPLAN 1994 Conference on Programming Language Design and Implementation (PLDI), 1994
    locator: Sections 4 to 6 (unsigned, signed and floor division) and Section 9 (exact division and divisibility by multiplication with the inverse)
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley, 2013
    locator: Chapter 10, Integer division by constants (signed and unsigned magic numbers, exact division, and the test for zero remainder)
  - paper: doi:10.1002/spe.2689
    title: Daniel Lemire, Owen Kaser and Nathan Kurz, Faster remainder by direct computation, Software Practice and Experience 49(6), 2019
    locator: Sections 2 and 3 (the remainder from the fractional part of the product, and the divisibility test)
  - paper: doi:10.1109/TC.2010.143
    title: Niels Möller and Torbjörn Granlund, Improved division by invariant integers, IEEE Transactions on Computers 60(2), 2011
    locator: Sections 3 and 4 (dividing two words by a fixed one-word divisor)
---

Division by a constant is the problem of dividing many integers by the same divisor $d$, when $d$ is known in advance, at a lower cost per division than a general division. The answer is to precompute an approximation of $1/d$ as a fixed-point number, so that each division becomes a multiplication, which hardware does several times faster, followed by shifts and at most a small correction. Compilers do this for every division by a literal constant, and big-number libraries do it to divide long numbers by one limb. The standard exact solution for machine words is [Granlund-Montgomery division](/granlund-montgomery-division/).

## In plain words

Computers multiply much faster than they divide. If you have to divide by the same number again and again, say by 10 to print decimal digits, it pays to work out once a special number that stands for "one tenth" in binary, and then multiply by it each time.

The hard part is to make the answer exact, not just close. A whole number that is slightly too big for one tenth, multiplied by your number and then cut down by a shift, gives the right quotient every time, as long as it is chosen with enough bits. The problem asks for the cheapest such recipe for each divisor.

## Definition

**Input.** A word size $w$, with $\beta = 2^w$, and a divisor $1 \le d < \beta$, known in advance; then a stream of dividends $0 \le n < \beta$.

**Output.** For each $n$, the quotient $\lfloor n/d \rfloor$, and if asked the remainder $n \bmod d$.

The cost is split into a precomputation, which may depend on $d$ only, and the cost per dividend, which is what is minimized. In the signed version, $n$ and $d$ are $w$-bit two's complement integers and the quotient is rounded toward zero, or toward $-\infty$ for [floor division](/floor-division/).

**Cost model.** The [word RAM](/word-ram/) with $w$-bit words, where the full product of two words, additions, shifts and comparisons cost $O(1)$, and a hardware division costs $O(1)$ too but with a much larger constant. The existence of exact $(w + 1)$-bit multipliers is proved; the ratio of division to multiplication cost is observed and depends on the machine.

## Variants

- **Unsigned and signed.** Signed division needs a correction for negative dividends, since a multiply-high rounds toward $-\infty$.
- **Remainder only.** Hash tables and modular reduction need only $n \bmod d$; it can be read off the low bits of a product with a $2w$-bit fraction of $1/d$, without computing the quotient (Lemire, Kaser and Kurz, 2019).
- **Exact division.** When $d$ is known to divide $n$, write $d = 2^k d'$ with $d'$ odd; then $n/d = (n \gg k) \cdot d'^{-1} \bmod \beta$, a single low product with the [inverse of $d'$ modulo $2^w$](/modular-inverse/).
- **Divisibility test.** For odd $d$, $d \mid n$ exactly when $n \cdot d^{-1} \bmod \beta \le \lfloor (\beta - 1)/d \rfloor$, since multiplication by $d^{-1}$ maps the multiples of $d$ onto $[0, \lfloor (\beta - 1)/d \rfloor]$.
- **Long dividends.** Dividing an $n$-word number by a fixed one-word $d$ is a loop of two-word by one-word divisions, each done with a precomputed reciprocal (Möller and Granlund, 2011).
- **Long divisors.** For a fixed divisor of many words, as a fixed modulus in cryptography, the analogue is [Barrett reduction](/barrett-reduction/); [Montgomery multiplication](/montgomery-multiplication/) changes the representation to avoid the division.

## Examples

| $w$ | $d$ | per-dividend sequence | why it is exact |
|---|---|---|---|
| 32 | 3 | $q = (n \cdot \mathtt{0xAAAAAAAB}) \gg 33$ | $\mathtt{0xAAAAAAAB} = \lceil 2^{33}/3 \rceil$ with error $e = 1 \le 2^1$ |
| 32 | 10 | $q = (n \cdot \mathtt{0xCCCCCCCD}) \gg 35$ | $\lceil 2^{35}/10 \rceil$ with error $e = 2 \le 2^3$ |
| 32 | 7 | $t = (n \cdot \mathtt{0x24924925}) \gg 32$, $q = (t + ((n - t) \gg 1)) \gg 2$ | the exact multiplier $\lfloor 2^{35}/7 \rfloor + 1$ needs 33 bits |
| 32 | 8 | $q = n \gg 3$ | a power of two |
| 32 | 3, exact | $q = n \cdot \mathtt{0xAAAAAAAB} \bmod 2^{32}$ if $3 \mid n$ | $\mathtt{0xAAAAAAAB}$ is also $3^{-1} \bmod 2^{32}$ |

The rule behind the first two rows: if $M = \lceil 2^{w+s}/d \rceil$ and $e = Md - 2^{w+s} \le 2^s$, then $\lfloor n/d \rfloor = \lfloor Mn/2^{w+s} \rfloor$ for all $0 \le n < 2^w$. Indeed $Mn/2^{w+s} = n/d + en/(d 2^{w+s})$, and the second term is less than $1/d$, too small to cross the next integer. For $d = 7$ and $w = 32$, no multiplier of 32 bits works for all dividends, so the third row uses the $(w + 1)$-bit multiplier of Granlund and Montgomery with its low 32 bits. For $3 \mid 21$, $21 \cdot \mathtt{0xAAAAAAAB} \bmod 2^{32} = 7$; for 22 the same product is $2863311538$, larger than $\lfloor (2^{32} - 1)/3 \rfloor = 1431655765$, so 3 does not divide 22.

## Known algorithms

- **[Granlund-Montgomery division](/granlund-montgomery-division/).** For every $d$, a multiplier $m < \beta$ and shifts with $q = (t + ((n - t) \gg 1)) \gg (\ell - 1)$, $t = \lfloor mn/\beta \rfloor$: one multiply-high and four cheap operations, exact for all $n$. When the $w$-bit multiplier suffices, one multiply-high and one shift.
- **Möller-Granlund 2/1 and 3/2 division.** A reciprocal $v = \lfloor (\beta^2 - 1)/d \rfloor - \beta$ divides two words by a normalized word with one full product, one low product and two rare corrections.
- **Direct remainder.** Lemire, Kaser and Kurz compute $c = \lceil 2^{2w}/d \rceil$ once, then $n \bmod d = \lfloor ((cn) \bmod 2^{2w}) \cdot d / 2^{2w} \rfloor$ for $w$-bit $n$.
- **Shift-and-add sequences.** On machines without a fast multiplier, the product by the constant multiplier is expanded into shifts and additions, as with the signed-digit recoding of [Booth's multiplication](/booth-multiplication/).
- **Newton iteration.** For long divisors, the reciprocal is computed once by [Newton-Raphson division](/newton-raphson-division/), and each division is then a few multiplications plus a correction, as in Barrett reduction.

## Bounds

**Existence, proved.** For every $1 \le d < \beta$ there is a multiplier of at most $w + 1$ bits, $M = \lfloor 2^{w + \ell}/d \rfloor + 1$ with $\ell = \lceil \log_2 d \rceil$, such that $\lfloor n/d \rfloor = \lfloor Mn/2^{w+\ell} \rfloor$ for all $0 \le n < \beta$ (Granlund and Montgomery, 1994, Theorem 4.2).

**Necessity of the extra bit, proved.** For some divisors no $w$-bit multiplier works with any shift. For $d = 7$ and $w = 32$, the only candidates below $2^{32}$ are $\lceil 2^{32+s}/7 \rceil$ for $s = 0, 1, 2$ (a smaller multiplier undercounts and a larger one has a larger error), and each gives a wrong quotient for $n = 2^{32} - 5$, as a check run for this page confirms. That is why the add-and-shift form exists.

**Per-dividend cost.** In the word RAM every method here costs $O(1)$, so the interest is in the constant: the Granlund-Montgomery sequence uses one multiply-high and at most four cheap operations for every $d$, and one multiply-high and one shift when a $w$-bit multiplier suffices. The precomputation costs one division of a two-word number by $d$.

## Reductions

- **Remainder from quotient.** $n \bmod d = n - d \lfloor n/d \rfloor$, one more low product.
- **Signed to unsigned.** Divide $|n|$ by $|d|$ and fix the sign, or use the signed sequences directly with a correction from the sign bit.
- **Exact division to multiplication.** For $d \mid n$, the problem reduces to one product with $d^{-1} \bmod 2^w$, computed by Newton's iteration $x \gets x(2 - dx)$, which doubles the number of correct low bits each time.
- **Long division by one limb.** Dividing an $n$-word number by $d$ reduces to $n$ two-word by one-word divisions, so a fast 2/1 step gives a fast loop, as in [long division](/long-division/).

## Applications

- **Compilers.** GCC, Clang and other compilers replace `x / c` and `x % c` for constant `c` by these sequences.
- **Number formatting.** Converting binary to decimal divides repeatedly by 10 or by $10^k$.
- **Hash tables and random numbers.** Reducing a hash or a random word modulo a fixed table size or range.
- **Big-number libraries.** GMP divides by single limbs, and by $10^{19}$ in base conversion, with precomputed reciprocals.
- **Cryptography.** Reduction modulo a fixed modulus uses Barrett or Montgomery reduction, the multiword relatives.

## References
