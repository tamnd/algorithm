---
tag: D0TMW5
kind: algorithm
slug: hart-one-line-factorization
name: Hart's one line factoring algorithm
aliases:
- OLF
area: number-theory/factorization
level: research
summary: For i = 1, 2, ..., takes s = ceil(sqrt(MNi)) and tests if s^2 - MNi is a square t^2; then gcd(N, s - t) is a factor. Heuristically O(N^(1/3)) steps after trial division to N^(1/3).
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, K: the iteration limit, M: the multiplier}
  time: {worst: O(K), heuristic: O(N^(1/3))}
  space: {extra: O(1)}
  bit_operations: {worst: O(K n^2), heuristic: O(N^(1/3) n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [fermat-factorization, lehman-factorization, trial-division, integer-square-root, greatest-common-divisor]
see_also: [shanks-squfof, congruence-of-squares, knuth-schroeppel-multiplier, dixon-random-squares, pollard-rho, relation-collection, quadratic-sieve, integer-factorization]
sources:
  - paper: doi:10.1017/S1446788712000146
    title: William B. Hart, A one line factoring algorithm, Journal of the Australian Mathematical Society 92(1) (2012)
    locator: pages 61 to 69; Section 2 (page 62, the algorithm, and page 63, the Pari/GP line and the example); Section 3 (page 63, the multiplier M = 480 and the variant with Dixon's method); Section 4 (page 64, the heuristic analysis); Section 5 (pages 64 to 66, Table 1, timings against Pari/GP and the 41-bit limit for 64-bit words); Section 6 (pages 66 to 67, Table 2, Lehman's algorithm and the guaranteed variant); Section 7 (pages 67 to 68, the special form); Section 8 (page 68, summary)
  - paper: "R. Sherman Lehman, Factoring large integers, Mathematics of Computation 28(126), 1974"
    locator: pages 637 to 646
  - paper: "James McKee, Speeding Fermat's factoring method, Mathematics of Computation 68(228), 1999"
    locator: pages 1729 to 1737 (a Fermat variant with expected time O(N^(1/4+e)), cited by Hart as related work)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 5.1.1 (Fermat's method and multipliers) and Section 5.1.2 (Lehman's method), pages 225 to 228
---

Hart's one line factoring algorithm, OLF, is a variant of [Fermat's method](/fermat-factorization/) in which only the multiplier changes. For $i = 1, 2, \dots$ it computes $s = \lceil \sqrt{MNi} \rceil$ and tests whether $m = s^2 - MNi$ is a perfect square $t^2$. If it is, then $\gcd(N, s - t)$ is a proper factor of $N$, as long as $s$ stays below about $N/2$. After [trial division](/trial-division/) up to $N^{1/3}$, a heuristic argument gives $O(N^{1/3})$ iterations, and in practice the method is competitive with [SQUFOF](/shanks-squfof/) for numbers below about $2^{42}$.

## In plain words

Fermat's method looks for a number $s$ just above the square root of $N$ such that $s^2 - N$ is a square. It is fast only when the two factors of $N$ are close. Lehman made it general: if the ratio of the two factors is near a fraction with small terms, a suitable multiple of $N$ has two close factors.

Hart's version does not search for that fraction. It takes the multiples $N, 2N, 3N, \dots$ in turn, and for each one it does a single Fermat step: round the square root up, square it, subtract, and test if the result is a square. When the right multiple comes, this single step is enough. A gcd with $N$ then gives a factor.

## The problem

**Input.** An integer $N \ge 2$, a multiplier $M \ge 1$ and an iteration limit $K \ge 1$.

**Output.** A proper factor $g$ of $N$ (with $1 < g < N$ and $g \mid N$), or $1$ for a failure. A [prime](/prime-number/) $N$ always gives $1$.

**The full factorization.** The analysis assumes that $N$ has no prime factor up to $N^{1/3}$. So a complete [integer factorization](/integer-factorization/) routine first runs trial division up to $N^{1/3}$. Then the part $R$ that is left has all prime factors above $N^{1/3} \ge R^{1/3}$, so it has at most two of them: $R$ is $1$, a prime, the square of a prime, or a product $pq$ of two distinct primes. A primality test and a square test settle the first three cases, and OLF splits the last one. The implementation below tries $M = 480$, then $M = 1$, with $K = 8N^{1/3} + 64$, and falls back to trial division up to $\sqrt R$, which happens rarely.

**Cost model.** On the [word RAM](/word-ram/) with $MNK < 2^w$, a multiplication, a subtraction, an [integer square root](/integer-square-root/) and a [gcd](/greatest-common-divisor/) of single words cost $O(1)$. The products $MNi$ have about $\frac{4}{3}\log_2 N + \log_2 M$ binary digits when $i$ runs up to $N^{1/3}$, so Hart notes that a 64-bit word handles $N$ up to about $2^{41}$ with $M = 480$. For an arbitrary-precision $N$ with $n$ binary digits, each step costs $O(n^2)$ bit operations with schoolbook arithmetic.

## The algorithm

Hart writes line L3 as $m \leftarrow s^2 \bmod N$. The two forms agree while $s^2 - MNi < N$, which line L2 makes sure of, and the subtraction is cheaper. Line L2 also stops the loop before the range in which a square can give a trivial gcd.

```pseudo id=main
OLF(N, M, K)                              ▷ N ≥ 2, M ≥ 1, K ≥ 1; returns g with 1 < g < N and g | N, or 1
L1  for i = 1, 2, …, K do
L2      s ← ⌈√(MNi)⌉; if 2s − 1 ≥ N then return 1
L3      m ← s² − MNi                      ▷ 0 ≤ m ≤ 2s − 2
L4      if m = t² for an integer t ≥ 0 then
L5          return gcd(N, s − t)
L6  return 1
```

Line L1 runs over the multipliers $Mi$. Line L2 computes the smallest $s$ with $s^2 \ge MNi$; this is the first value that Fermat's method tries on $MNi$. Line L3 forms the excess $m$, which is less than $2s - 1$ because $(s - 1)^2 < MNi$. Line L4 is the square test. If it succeeds, then $(s - t)(s + t) = MNi$, so $N$ divides a product of two numbers, both smaller than $N$, and line L5 takes the gcd with $N$, not with $MNi$, so that the factors of $Mi$ are not returned. Line L6 reports a failure after $K$ steps.

## Example

Let $N = 200633$ and $M = 1$. Here $N^{1/3} \approx 58.5$ and no prime up to $58$ divides $N$, so $N$ is a prime or a product of two primes above $58$. Fermat's method alone needs $30$ values of $s$, from $448$ to $477$, before $477^2 - N = 164^2$.

| $i$ | $Ni$ | $s = \lceil \sqrt{Ni} \rceil$ | $m = s^2 - Ni$ | square? |
|---|---|---|---|---|
| 1 | 200633 | 448 | 71 | no |
| 2 | 401266 | 634 | 690 | no |
| 3 | 601899 | 776 | 277 | no |
| 4 | 802532 | 896 | 284 | no |
| 5 | 1003165 | 1002 | 839 | no |
| 6 | 1203798 | 1098 | 1806 | no |
| 7 | 1404431 | 1186 | 2165 | no |
| 8 | 1605064 | 1267 | 225 | yes, $t = 15$ |

At $i = 8$, line L5 returns $\gcd(200633, 1267 - 15) = \gcd(200633, 1252) = 313$, and $N = 313 \cdot 641$. The reason is visible in the factors: $s - t = 1252 = 4 \cdot 313$ and $s + t = 1282 = 2 \cdot 641$, so $8N = (4 \cdot 313)(2 \cdot 641)$ is a product of two close numbers. This happens because $641/313 \approx 2.05$ is near $2/1$. For two close numbers $A < B$ of the same parity, $\lceil \sqrt{AB} \rceil = (A + B)/2$ as soon as $(\sqrt B - \sqrt A)^2 < 2$, and here $(\sqrt{1282} - \sqrt{1252})^2 \approx 0.18$.

With $M = 480$ the method finds the other factor at $i = 21$: $s = 44971$, $m = 10201 = 101^2$, and $\gcd(200633, 44870) = 641$, with $s - t = 44870 = 70 \cdot 641$ and $s + t = 45072 = 144 \cdot 313$.

Hart's own example has $p = \operatorname{nextprime}(10^{29} + 5342347) = 10^{29} + 5342361$ and $q = \operatorname{nextprime}(10^{31} + 2232788) = 10^{31} + 2232811$. OLF with $M = 1$ splits $N = pq$, a number of $61$ decimal digits, at $i = 400$, where $s - t = 2q$ and $s + t = 200p$; the gcd is $q$. At $i = 399$ it has still found nothing. With $M = 480$ it needs $30$ steps.

## Correctness

If line L4 succeeds, then $(s - t)(s + t) = MNi$ with $0 \le t < s$. Line L2 makes sure that $s + t \le 2s - 1 < N$, so neither $s - t$ nor $s + t$ is divisible by $N$. Since $N$ divides their product, $\gcd(N, s - t)$ cannot be $N$, and it cannot be $1$, because then $N$ would divide $s + t$. So every value that line L5 returns is a proper factor, and a prime $N$ never gives a square in this range. The loop has at most $K$ passes, so the algorithm stops. A converse shows when it succeeds: if $MNi = AB$ with $A < B$ of the same parity and $(\sqrt B - \sqrt A)^2 < 2$, then iteration $i$ gives $s = (A + B)/2$ and $t = (B - A)/2$. The full proof is below.

## Complexity

- **Per iteration.** One multiplication, one square root to round up, one square test and, on success, one gcd. On the word RAM this is $O(1)$; for an $n$-digit $N$ it is $O(n^2)$ bit operations.
- **Worst case.** $O(K)$ operations, proved. There is no proved bound on the number of iterations that OLF needs to find a factor, so the limit $K$ is part of the input.
- **Heuristic.** Hart's analysis (Section 4) assumes $M = 1$, that trial division up to $N^{1/3}$ found nothing, and that $N$ is not a square. Then $0 < m < 2\sqrt{Ni}$, and there are about $\sqrt 2 (Ni)^{1/4}$ squares below $2\sqrt{Ni}$, so if $m$ behaves like a random number in that range, it is a square with probability about $1/(\sqrt 2 (Ni)^{1/4})$. For $i \le N^{1/3}$ this is at least about $1/(\sqrt 2\, N^{1/3})$, so $O(N^{1/3})$ independent trials are likely to find a square. With the trial division, the total is $O(N^{1/3})$ operations heuristically, written $O(N^{1/3 + \varepsilon})$ in Hart's Section 4. This is not a theorem, because the values $m$ are not random and not independent.
- **Measured.** On $300$ random products $N = pq$ of two primes above $N^{1/3}$ (seed $5$), the number of iterations divided by $N^{1/3}$ had a median between $0.33$ and $0.37$ for $M = 1$ and between $0.07$ and $0.10$ for $M = 480$, at $24$, $32$ and $40$ binary digits. The largest ratio was close to $10$ for $M = 1$ and below $0.82$ for $M = 480$, so the multiplier also shortens the long tail.
- **Space.** $O(1)$ numbers.

For comparison, [Lehman's method](/lehman-factorization/) has a proved $O(N^{1/3})$ bound, and [SQUFOF](/shanks-squfof/) and [Pollard's rho](/pollard-rho/) need about $N^{1/4}$ steps heuristically.

## Properties

- **Deterministic.** For fixed $N$, $M$ and $K$ the output is fixed.
- **No false factors.** Every returned value is a proper factor of $N$, by the range test of line L2. A failure returns $1$ and says nothing about primality.
- **Not a primality test.** A prime $N$ gives $1$, but so can a composite $N$ when $K$ is too small. Use a primality test such as [Miller-Rabin](/miller-rabin/) first.
- **Small numbers.** Apart from the products $MNi$, every value is below $2\sqrt{MNK} + 1$, so the method suits single-word arithmetic.
- **Special forms.** It splits $N = \operatorname{nextprime}(c^a \pm d_1) \cdot \operatorname{nextprime}(c^b \pm d_2)$ with small $c, d_1, d_2$ and $a > b$ fast, because once $i$ reaches about $c^{a - b}$ (times a small factor for parity), one Fermat step on $Ni$ is enough. Hart reports that numbers of this form with many thousands of digits can be factored.

## Variants and improvements

- **A constant multiplier.** Hart observed that $M = 480 = 2^5 \cdot 3 \cdot 5$ speeds the method up considerably compared with $M = 1$ or a smaller multiplier. The primes of $M$ must be removed from $N$ first. Each multiplier $Mi$ has many divisors, so more pairs $(u, v)$ with $uv \mid Mi$ are tried at once, as in the choice of $k$ in [Lehman's method](/lehman-factorization/) and in the [Knuth-Schroeppel multiplier](/knuth-schroeppel-multiplier/).
- **Fast square detection.** Most values $m$ are not squares, and tables of the [quadratic residues](/quadratic-residue/) modulo a few small numbers reject most of them before any square root, as in Fermat's method.
- **Dixon's trick.** Hart (Section 3) chooses $C = \lceil \log \log N \rceil$ small primes $q_j \equiv 1 \pmod 4$, accepts the values $m$ of the form $q_1^{e_1} \cdots q_C^{e_C} t^2$ with $e_j \in \{0, 1\}$, and combines such [relations](/relation-collection/) by linear algebra over $\mathbb{F}_2$ into a [congruence of squares](/congruence-of-squares/), as in [Dixon's method](/dixon-random-squares/). He did not see a real speedup below about $2^{40}$, because a square comes too fast.
- **A guaranteed variant.** For $k > N^{1/3}/16$ the search interval of each $k$ in Lehman's method contains one integer. An anonymous referee of Hart's paper noted that one can turn Lehman's loops inside out, with one value of $x$ per interval and the multiplier $k$ in the outer loop. This gives a method that looks like OLF and keeps Lehman's proved bound; Hart reports the same times as OLF up to about $40$ binary digits.
- **McKee's method.** McKee's variant of Fermat's method uses square roots of $N$ modulo $m^2$ to search for small solutions of a quadratic equation, with expected time $O(N^{1/4 + \varepsilon})$. It is a different algorithm, cited by Hart as related work.

## When to use it

Use OLF to split numbers below about $2^{42}$ after trial division to $N^{1/3}$, for example in a general factoring routine or in the [large prime](/relation-collection/) phase of the [quadratic sieve](/quadratic-sieve/), where many small cofactors must be split. In Hart's Table 1 it is faster than the factoring routines of Pari/GP from $28$ to $40$ binary digits. From about $17$ to $27$ binary digits Pari is slightly faster, and Hart notes that trial division up to $\sqrt N$ is enough in that range. It is also the right tool for products of primes near powers of a small base. For larger general numbers use [SQUFOF](/shanks-squfof/), [Pollard's rho](/pollard-rho/), the [elliptic curve method](/elliptic-curve-factorization/) or the [quadratic sieve](/quadratic-sieve/).

## Pitfalls

- **No range test.** Without line L2 a square can give a trivial gcd. For the prime $N = 101$ and $M = 1$, iteration $i = 75$ gives $s = 88$, $m = 169 = 13^2$, and $\gcd(101, 75) = 1$. There $2s - 1 = 175 \ge N$, and $s^2 \bmod N = 68$ is not equal to $s^2 - Ni$ either.
- **No trial division.** The heuristic needs both prime factors above $N^{1/3}$. For $N = 3 \cdot 1000003 = 3000009$, OLF with $M = 1$ first finds a square at $i = 332393$, while $N^{1/3} \approx 144$.
- **Returning $s - t$.** At $i = 8$ in the example, $s - t = 1252 = 4 \cdot 313$ is not a divisor of $N$. Take the gcd with $N$.
- **The gcd with $MNi$.** A gcd with $MNi$ instead of $N$ can return a divisor of $Mi$.
- **Overflow.** The product $MNi$ is about $N^{4/3} M$ for $i$ near $N^{1/3}$. In a 64-bit word with $M = 480$ this limits $N$ to about $2^{41}$, and beyond that point Hart saw many failures.
- **Floating-point square roots.** Hart's Pari line sets a precision of 38 digits for his example. With doubles, $\lceil \sqrt{MNi} \rceil$ is wrong for large products. Use an [integer square root](/integer-square-root/) and correct $s$ by one if $s^2 < MNi$.
- **Squares.** If $N = r^2$, then $i = 1$ gives $m = 0$ and the factor $r$. This is correct, but $r$ may be composite, so a full factorization must check its factors again.

## Implementations

## History

William Hart found the algorithm while he tested an implementation of the quadratic sieve on numbers of the form $\operatorname{nextprime}(10^a) \cdot \operatorname{nextprime}(10^b)$, and saw that this simple loop split them fast. He named it after the fact that it fits in one line of Pari/GP or Sage. The paper, received in 2011 and published in 2012 in the Journal of the Australian Mathematical Society, places it next to [Lehman's method](/lehman-factorization/) of 1974, which also gives Fermat's method a multiplier but searches over fractions $u/v$, and next to McKee's 1999 variant. Hart's C implementation is part of the FLINT library, with SQUFOF as the fallback when OLF fails.

## References
