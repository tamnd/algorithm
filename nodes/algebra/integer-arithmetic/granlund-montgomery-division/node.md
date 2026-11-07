---
tag: N5CE12
kind: algorithm
slug: granlund-montgomery-division
name: Granlund-Montgomery division
aliases:
- division by invariant integers
- Möller-Granlund division
- division by multiplication
area: algebra/integer-arithmetic
level: advanced
summary: Division by a fixed divisor using a precomputed multiplicative inverse and shifts.
solves: [division-by-constant]
model: word-ram
complexity:
  vars: {w: the number of bits in a machine word}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  note: Granlund and Montgomery (1994) gave multipliers and shifts that divide every w-bit word exactly, and Möller and Granlund (2011) gave the faster two-word by one-word form used in GMP.
prereqs: [division-by-constant, division-with-remainder, word-ram]
see_also: [division-by-constant, barrett-reduction, montgomery-multiplication, newton-raphson-division, integer-division, long-division, burnikel-ziegler-division, modular-inverse]
sources:
  - paper: doi:10.1145/178243.178249
    title: Torbjörn Granlund and Peter L. Montgomery, Division by invariant integers using multiplication, Proceedings of the ACM SIGPLAN 1994 Conference on Programming Language Design and Implementation (PLDI), 1994
    locator: Section 4, Unsigned division (Theorem 4.2 and Figure 4.1, the multiplier m' and the shifts sh1 and sh2), and Section 8 for dividing two words by one
  - paper: doi:10.1109/TC.2010.143
    title: Niels Möller and Torbjörn Granlund, Improved division by invariant integers, IEEE Transactions on Computers 60(2), 2011
    locator: Section 4, Algorithm 4 (the 2/1 division with the reciprocal v and two conditional adjustments) and its correctness theorem
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley, 2013
    locator: Chapter 10, Integer division by constants (unsigned division with the add indicator, and the proofs for each divisor class)
  - url: https://gmplib.org/manual/Single-Limb-Division
    title: The GNU Multiple Precision Arithmetic Library manual, Single Limb Division
    locator: the use of a precomputed inverse for division of many limbs by one limb
---

Granlund-Montgomery division divides machine words by a fixed divisor $d$ with one multiplication, one subtraction, an addition and two shifts, after a precomputation that depends only on $d$. Hardware division is many times slower than multiplication, so when the same $d$ is used many times, by a compiler for `n / 7`, or by a big-number library dividing each limb by the same divisor, replacing the division by a multiplication with an approximate reciprocal pays. The method of Granlund and Montgomery (1994) is exact for every dividend of $w$ bits and every divisor, even when the ideal multiplier needs $w + 1$ bits. Möller and Granlund (2011) gave the companion step that divides a two-word number by a one-word divisor, the inner loop of [long division](/long-division/) in GMP. Both solve the [division by a constant](/division-by-constant/) problem.

## In plain words

Dividing by 7 is the same as multiplying by one seventh. A computer cannot store one seventh exactly, but it can store a whole number close to $2^k / 7$ for a large $k$, multiply by it, and then throw away the low $k$ bits of the result. If the stored number is chosen carefully, the answer is exactly the quotient, with no rounding error, for every possible input.

The work of finding that number is done once. After that, each division costs a multiplication and a few cheap operations. The trick that makes it work in all cases is to split the final shift into two parts, so that no intermediate sum is too big for a word.

## The problem

Words have $w$ bits and $\beta = 2^w$. Given a divisor $1 \le d < \beta$, compute once some data that depends on $d$; then, for each dividend $0 \le n < \beta$, return $q = \lfloor n/d \rfloor$ and $r = n - qd$. The two-word form takes a normalized $d$, with $\beta/2 \le d < \beta$, and $u = u_1\beta + u_0$ with $u_1 < d$, so that the quotient fits in one word, and returns $\lfloor u/d \rfloor$ and $u \bmod d$.

**Cost model.** The [word RAM](/word-ram/) with $w$-bit words, where addition, subtraction, shifts, comparison and the full product of two words (both its high and low words) each cost $O(1)$. A division costs a constant number of these operations, so $\Theta(1)$, and the precomputation one division of a two-word number by $d$. The exactness of both methods for all inputs is proved; the speedup over a hardware divide instruction is observed and depends on the processor.

## The algorithm

```pseudo id=main
PRECOMPUTE(d)                                  ▷ 1 ≤ d < β = 2^w
L1  ℓ ← ⌈log₂ d⌉                                ▷ 2^(ℓ−1) < d ≤ 2^ℓ
L2  m ← ⌊β (2^ℓ − d) / d⌋ + 1                   ▷ fits in one word
L3  (s₁, s₂) ← (min(ℓ, 1), max(ℓ − 1, 0))

DIVIDE(n)                                      ▷ 0 ≤ n < β
L4  t ← ⌊m · n / β⌋                             ▷ the high word of the product
L5  q ← (t + ((n − t) >> s₁)) >> s₂
L6  return (q, n − q · d)

DIVIDE-2BY1(u₁, u₀, d, v)                      ▷ β/2 ≤ d < β, u₁ < d, v = ⌊(β² − 1)/d⌋ − β
L7  (q₁, q₀) ← v · u₁ + (u₁, u₀)                ▷ a two-word product plus a two-word sum
L8  q₁ ← (q₁ + 1) mod β;  r ← (u₀ − q₁ · d) mod β
L9  if r > q₀ then q₁ ← (q₁ − 1) mod β; r ← (r + d) mod β
L10 if r ≥ d then q₁ ← q₁ + 1; r ← r − d
L11 return (q₁, r)
```

The true multiplier is $\beta + m = \lfloor 2^{w + \ell}/d \rfloor + 1$, which has $w + 1$ bits. Line L4 multiplies by its low part $m$ only, and line L5 adds the missing $n \cdot \beta / \beta = n$ back in: $q = \lfloor (n + t)/2^\ell \rfloor$. Computing $n + t$ directly could overflow a word, so line L5 halves $n - t$ first, which is why the shift is split into $s_1$ and $s_2$. In DIVIDE-2BY1, the reciprocal $v$ is the same idea for a quotient of a full word: $\beta + v$ approximates $\beta^2/d$, line L8 forms a candidate quotient, and lines L9 and L10 correct it by at most one each.

## Example

**One word.** Take $w = 8$ and $d = 7$. Line L1 gives $\ell = 3$, line L2 gives $m = \lfloor 256 \cdot 1 / 7 \rfloor + 1 = 37$, and line L3 gives $s_1 = 1$, $s_2 = 2$. Divide $n = 200$:

| line | computation | value |
|---|---|---|
| L4 | $t = \lfloor 37 \cdot 200 / 256 \rfloor = \lfloor 7400/256 \rfloor$ | 28 |
| L5 | $(200 - 28) \gg 1$ | 86 |
| L5 | $(28 + 86) \gg 2 = 114 \gg 2$ | $q = 28$ |
| L6 | $200 - 28 \cdot 7$ | $r = 4$ |

Indeed $200 = 28 \cdot 7 + 4$. The intermediate $t + 86 = 114$ fits in 8 bits; the direct sum $n + t = 228$ would also fit here, but for $n = 255$ and $d = 7$ it is $255 + 36 = 291$, which does not.

**Two words by one.** Take $w = 8$, $d = 200$, so $v = \lfloor 65535/200 \rfloor - 256 = 71$, and $u = 150 \cdot 256 + 77 = 38477$. Line L7 gives $71 \cdot 150 + 38477 = 49127 = 191 \cdot 256 + 231$, so $q_1 = 191$ and $q_0 = 231$. Line L8 gives $q_1 = 192$ and $r = (77 - 38400) \bmod 256 = 77$. Since $77 \le 231$ and $77 < 200$, no correction is made: $38477 = 192 \cdot 200 + 77$.

## Correctness

For PRECOMPUTE and DIVIDE, write $M = \beta + m = (2^{w+\ell} + e)/d$ with $1 \le e \le d$. For $n = qd + r$, $Mn / 2^{w+\ell} = q + r/d + en/(d \cdot 2^{w+\ell})$, and $en < 2^\ell \cdot 2^w$, so the extra terms are less than $(r + 1)/d \le 1$: hence $q = \lfloor Mn/2^{w+\ell} \rfloor = \lfloor (n + t)/2^\ell \rfloor$, and line L5 computes this without overflow. For DIVIDE-2BY1, the candidate remainder $\tilde r = u - (q_1 + 1)d$ of line L8 lies in an interval $[M' - \beta, M')$ with $M' = \max(\beta - d, q_0)$, so its residue mod $\beta$ determines it, the test $r > q_0$ of line L9 detects $\tilde r < 0$ or a harmless overshoot, and line L10 fixes the overshoot. The full proof is below.

## Complexity

**Per division, proved.** DIVIDE does one high product, one subtraction, one addition, two shifts, one low product and one subtraction for the remainder: $O(1)$ word operations, against one divide instruction. DIVIDE-2BY1 does one full product $v u_1$, one low product $q_1 d$, a two-word addition and at most two corrections, also $O(1)$.

**Precomputation, proved.** PRECOMPUTE needs one division of the two-word number $\beta(2^\ell - d)$ by $d$, and the reciprocal $v$ one division of $\beta^2 - 1$ by $d$; both are done once per divisor.

**Speed, observed.** On current 64-bit processors a multiply has a latency of about 3 to 4 cycles, while a 64-bit divide takes from about 10 to more than 40 cycles depending on the processor; compilers therefore emit this sequence for every unsigned division by a constant. In GMP, dividing an $n$-limb number by one limb with DIVIDE-2BY1 in a loop is several times faster than using the hardware divide.

## Properties

- **Exact.** There is no error to correct after DIVIDE: the quotient is exact for all $2^w$ dividends, as proved and as checked exhaustively for $w = 8$ by the test script.
- **Branch-free.** DIVIDE has no data-dependent branches. DIVIDE-2BY1 has two adjustments; the first is rare and the second very rare, and both can be done with masks.
- **Special cases are cheaper.** If $d$ is a power of two, $m = 1$ and the sequence is a shift; if $\lfloor 2^{w+\ell}/d \rfloor + 1$ is even or can be chosen with fewer bits, a single multiply-high and shift suffices, which compilers detect.
- **Normalization.** DIVIDE-2BY1 needs $d \ge \beta/2$; a divisor with $k$ leading zero bits is shifted left by $k$, and the dividend with it, and the remainder shifted back.

## Variants and improvements

- **Signed division.** Granlund and Montgomery also give sequences for signed division rounding toward zero and for floor division, with a correction of $-1$ from the sign of $n$.
- **Exact division.** If $d$ is known to divide $n$, then for odd $d$, $n/d = n \cdot d^{-1} \bmod \beta$, a single low product with the [inverse of $d$ modulo $2^w$](/modular-inverse/); the same inverse gives a test for divisibility.
- **3/2 division.** Möller and Granlund also give the division of a three-word number by a two-word normalized divisor with a reciprocal, used to get one quotient word per step when dividing by a long number.
- **Direct remainder.** Lemire, Kaser and Kurz (2019) compute $n \bmod d$ directly from the low bits of a product with a $2w$-bit fraction, which is faster when only the remainder is needed.
- **Many words.** For a long divisor the analogous method is [Barrett reduction](/barrett-reduction/) or [Newton-Raphson division](/newton-raphson-division/); [Montgomery multiplication](/montgomery-multiplication/) avoids division altogether in modular arithmetic.

## When to use it

Use it whenever the divisor is fixed and the dividends are many: a compiler dividing by a constant, a hash table with a fixed prime size, base conversion by $10^k$, or the division of a long number by one limb. If the divisor changes with every division, the precomputation costs as much as a division and the hardware instruction is better. For numbers of many words, use the long-number methods above.

## Pitfalls

- **Adding before halving.** Writing line L5 as $q \gets (t + n) \gg \ell$ overflows when $n + t \ge \beta$, as for $n = 255$, $d = 7$, $w = 8$, where $t + n = 291$. The right form halves the difference first: $(t + ((n - t) \gg s_1)) \gg s_2$.
- **Rounding the multiplier down.** Using $m = \lfloor \beta(2^\ell - d)/d \rfloor$ in line L2, without the $+1$, makes the quotient one too small for some $n$; for $w = 8$ the test script finds 955 wrong pairs. The multiplier must round up.
- **Forgetting to normalize.** Calling DIVIDE-2BY1 with $d < \beta/2$ breaks the bound on the candidate remainder, and lines L9 and L10 are no longer enough. Shift $d$ and $u$ left until the top bit of $d$ is set.
- **Comparing with the wrong word.** Line L9 compares $r$ with the low word $q_0$ of line L7, not with $d$ or with $0$; the comparison with $q_0$ is what detects a negative candidate remainder in a single word.

## Implementations

## History

Multiplying by an approximate reciprocal to divide by a constant was used by compilers in the 1980s, for example by Magenheimer, Peters, Pettis and Zuras (1988) for the HP Precision Architecture, which had no divide instruction, and Alverson (1991) analysed the method for the Tera computer. Granlund and Montgomery (1994) gave the general unsigned and signed sequences, proved them exact for all divisors, including those whose multiplier needs $w + 1$ bits, and implemented them in the GNU C compiler. Möller and Granlund (2011) improved the division of two words by one, which GMP and other big-number libraries now use.

## References
