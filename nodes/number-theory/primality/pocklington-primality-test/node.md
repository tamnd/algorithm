---
tag: 1J28JY
kind: algorithm
slug: pocklington-primality-test
name: Pocklington primality test
aliases:
- Pocklington test
- Pocklington-Lehmer test
area: number-theory/primality
level: advanced
summary: Proves n prime from a factored part F of n-1 with F^2 > n. For each prime q of F it needs a base a with a^(n-1) = 1 and gcd(a^((n-1)/q) - 1, n) = 1 modulo n.
solves: [primality-proving]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested, t: the number of distinct primes of F, k: the number of tries per prime}
  time: {worst: O(k t (log n)^3), best: O(1)}
  space: {extra: O(t log n)}
properties: {deterministic: false, recursive: false, certifying: true}
history:
  year: 1914
  people: [Henry Cabourn Pocklington]
  note: Published in the Proceedings of the Cambridge Philosophical Society. It extends the theorem of Lucas (1876) from a full to a partial factorization of n-1. Brillhart, Lehmer and Selfridge (1975) lowered the needed size of F from n^(1/2) to n^(1/3).
prereqs: [fermat-little-theorem, multiplicative-order, greatest-common-divisor, modular-exponentiation]
see_also: [lucas-primality-test, pratt-certificate, primality-certificate, primality-proving, proth-test, pepin-test, random-prime-generation, ecpp]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.1.1 (Theorem 4.1.1) and Section 4.1.2 (Theorem 4.1.3, Corollary 4.1.4, Theorems 4.1.5 and 4.1.6, Algorithm 4.1.7)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Section 4.3.2 (Facts 4.38 to 4.42, Note 4.39) and the chapter notes on Section 4.3
  - paper: "H. C. Pocklington, The determination of the prime or composite nature of large numbers by Fermat's theorem, Proceedings of the Cambridge Philosophical Society 18 (1914 to 1916)"
    title: H. C. Pocklington, The determination of the prime or composite nature of large numbers by Fermat's theorem
    locator: pages 29 to 30
  - paper: doi:10.1090/S0025-5718-1975-0384673-1
    title: John Brillhart, D. H. Lehmer and J. L. Selfridge, New primality criteria and factorizations of 2^m ± 1, Mathematics of Computation 29 (1975)
    locator: pages 620 to 647
---

The Pocklington test proves that an integer $n$ is [prime](/prime-number/) when part of $n - 1$ is factored. If $n - 1 = F R$ with the prime factors of $F$ known and $F^2 > n$, a base $a$ with $a^{n-1} \equiv 1$ and $\gcd(a^{(n-1)/q} - 1, n) = 1$ for each prime $q \mid F$ shows that every prime factor of $n$ is $\equiv 1 \pmod F$, so larger than $\sqrt n$, so $n$ is prime. Unlike a probable prime test, its answer "prime" is a proof, and the bases form a [primality certificate](/primality-certificate/) that anyone can check. It is the basis of the [Proth test](/proth-test/), of Maurer's [random provable primes](/random-prime-generation/), and, in an elliptic curve form, of [ECPP](/ecpp/).

## In plain words

To show that a number is prime, the test does not factor the number itself. It factors the number just below it, at least in part. If the known part is large enough, one well chosen base can show that every prime factor of the number must be larger than its square root. A number whose prime factors are all larger than its square root has only one prime factor, itself, so it is prime. The base acts as a key: once found, anyone can check it quickly. The hard part is the factoring, which is easy only when the number has a special form or was built that way.

## The problem

The input is an odd integer $n \ge 5$ and the factorization $F = \prod_{j=1}^{t} q_j^{e_j}$ of a divisor $F$ of $n - 1$ with $F^2 > n$. The primes $q_j$ must be known to be prime; proving them is a separate task, which a [Pratt certificate](/pratt-certificate/) or Maurer's recursion handles. The output is "prime" with a base $a_q$ for each $q$, "composite" with a witness or a factor, or "unknown" when no base was found within the allowed tries. "Prime" and "composite" are always right.

**Cost model.** The integers are of arbitrary precision; $\ell = \lfloor \lg n \rfloor + 1$ is the bit length of $n$. Costs are bit operations with schoolbook multiplication, as on a [multitape Turing machine](/multitape-turing-machine/). The cost of factoring $n - 1$ is not included.

## The algorithm

The test uses a separate base for each prime of $F$, as Brillhart and Selfridge allowed (HAC, chapter notes on Section 4.3).

```pseudo id=main
POCKLINGTON(n, {q₁: e₁, …, q_t: e_t}, k)    ▷ F = ∏ q_j^e_j divides n − 1
L1  if n < 5 then return (n ∈ {2, 3}) ? PRIME : COMPOSITE
L2  if n is even then return COMPOSITE
L3  if F ∤ n − 1 or F² ≤ n then error "F is too small"
L4  for each prime q of F do
L5      repeat at most k times
L6          a ← a uniform random integer in [2, n − 2]
L7          if a^(n−1) mod n ≠ 1 then return COMPOSITE (Fermat witness a)
L8          g ← gcd(a^((n−1)/q) − 1 mod n, n)
L9          if 1 < g < n then return COMPOSITE (factor g)
L10         if g = 1 then a_q ← a; go to the next q
L11     return UNKNOWN                          ▷ k bases all gave g = n
L12 return PRIME with the bases a_q
```

Line L7 is a [Fermat test](/fermat-primality-test/). Line L8 asks whether $a^{(n-1)/q} \equiv 1$ modulo some prime factor of $n$. For a prime $n$ the gcd is $1$ or $n$, and it is $n$ exactly when $a$ is a $q$-th power residue, so a few tries find a good base. For a composite $n$ a gcd strictly between $1$ and $n$ is a proper factor, and line L9 returns it.

## Example

**A prime.** Let $n = 1000003$. Then $n - 1 = 6 \cdot 166667$, and $F = 166667$ is prime (trial division up to 408 shows it) with $F^2 \approx 2.8 \cdot 10^{10} > n$. So only $q = 166667$ needs a base, and $(n-1)/q = 6$.

| base $a$ | $a^{n-1} \bmod n$ | $a^{6} \bmod n$ | $g = \gcd(a^6 - 1, n)$ | line | result |
|---|---|---|---|---|---|
| 2 | $1$ | $64$ | $\gcd(63, 1000003) = 1$ | L10 | $a_q = 2$ |

So every prime factor $p$ of $1000003$ satisfies $p \equiv 1 \pmod{166667}$, so $p \ge 166668 > \sqrt{1000003} \approx 1000.0015$; hence $1000003$ is prime. The certificate is the triple $(n, F = 166667, a = 2)$ plus a proof that 166667 is prime.

**A composite.** Let $n = 561 = 3 \cdot 11 \cdot 17$, with $560 = 2^4 \cdot 5 \cdot 7$ and $F = 2^4 \cdot 5 = 80 > \sqrt{561}$. The first prime is $q = 2$, with $(n-1)/2 = 280$:

| base $a$ | $a^{560} \bmod 561$ | $a^{280} \bmod 561$ | $g$ | line | result |
|---|---|---|---|---|---|
| 2 | $1$ | $1$ | $561$ | L10 fails | try again |
| 5 | $1$ | $67$ | $\gcd(66, 561) = 33$ | L9 | COMPOSITE, factor 33 |

The [Carmichael number](/carmichael-number/) 561 passes the Fermat check of line L7 for every unit base, but the gcd of line L8 finds the factor $33 = 3 \cdot 11$.

## Correctness

**The answer prime is right** (Pocklington's theorem; Crandall and Pomerance, Theorem 4.1.3 and Corollary 4.1.4; HAC Fact 4.40). Let $p$ be a prime factor of $n$ and $q^e$ the exact power of a prime $q$ in $F$. Put $b = a_q^{(n-1)/q^e}$. Then $b^{q^e} = a_q^{n-1} \equiv 1 \pmod p$, while $b^{q^{e-1}} = a_q^{(n-1)/q} \not\equiv 1 \pmod p$, because $\gcd(a_q^{(n-1)/q} - 1, n) = 1$. So the [order](/multiplicative-order/) of $b$ modulo $p$ is exactly $q^e$, and it divides $p - 1$ by [Fermat's little theorem](/fermat-little-theorem/). This holds for every prime power in $F$, so $F \mid p - 1$ and $p > F > \sqrt n$. A composite $n$ has a prime factor at most $\sqrt n$, so $n$ is prime.

**The answer composite is right.** Line L7 returns only when $a^{n-1} \not\equiv 1$, which is impossible for a prime $n$ with $n \nmid a$. Line L9 returns a divisor $g$ of $n$ with $1 < g < n$.

**The answer unknown is rare for primes.** For a prime $n$, $\mathbb{Z}_n^*$ is cyclic, and the bases with $a^{(n-1)/q} \equiv 1$ form its subgroup of index $q$, of size $(n-1)/q$, which contains 1. So at most $(n-1)/q - 1 \le (n-3)/2$ of the $n - 3$ bases in $[2, n-2]$ are bad, a try fails with probability at most $1/2$, and the call returns UNKNOWN with probability at most $t \, 2^{-k}$. For a composite $n$ the call returns COMPOSITE or UNKNOWN, never PRIME. The full proof is in the proofs.

## Complexity

**Per try.** Lines L7 and L8 are two modular exponentiations with exponents below $n$, so $O(\ell)$ products modulo $n$ and $O(\ell^3)$ bit operations; line L8 also does a gcd in $O(\ell^2)$. Computing $c = a^{(n-1)/q}$ first and then $c^q$ saves part of the work.

**All tries.** With $t$ distinct primes in $F$ and at most $k$ tries for each, the worst case is $O(k t \ell^3)$ bit operations. For a prime $n$ the expected number of tries for each $q$ is at most 2, so the expected cost is $O(t \ell^3)$, and since $t \le \lg F < \ell$ this is $O(\ell^4)$ at most. The best case is $O(1)$ for $n < 5$ or even $n$. With a multiplication algorithm of cost $M(\ell)$, replace $\ell^3$ by $\ell \, M(\ell)$.

**Space.** The bases kept for the certificate take $O(t \ell)$ bits; the working space is $O(\ell)$.

**Verification.** Checking a certificate repeats lines L7 and L8 once for each $q$, so it costs $O(t \ell^3)$ bit operations with no randomness, plus the cost of checking that the $q_j$ are prime.

**Factoring.** The real cost is the factorization of $F$. For a random $n$, finding a factored part above $\sqrt n$ is as hard as factoring a number of half the size, which is why the test is used for numbers of special form ($k 2^m + 1$, $2^{2^m} + 1$) and for primes built together with their certificate.

## Properties

- **Certifying.** The output PRIME comes with the bases $a_q$, and the triple ($n$, the factorization of $F$, the bases) is a primality certificate. A factor or a Fermat witness certifies COMPOSITE.
- **Las Vegas in its answers.** Randomness affects only the running time and the chance of UNKNOWN, never the correctness of PRIME or COMPOSITE (HAC Fact 4.41 and the text after it).
- **Needs only half of $n - 1$.** Lucas's theorem needs the full factorization of $n - 1$ (HAC Fact 4.38); Pocklington needs a factored part above $\sqrt n$.
- **Conditional on the primes $q$.** The proof is only as good as the proofs that the $q_j$ are prime. A recursive certificate proves them too.

## Variants and improvements

- **Lucas's theorem** (Crandall and Pomerance, Theorem 4.1.1; HAC Fact 4.38). With $F = n - 1$, one base of order $n - 1$ proves $n$ prime. See the [Lucas primality test](/lucas-primality-test/).
- **Brillhart, Lehmer and Selfridge: $F \ge n^{1/3}$** (Crandall and Pomerance, Theorem 4.1.5). If the conditions hold and $n^{1/3} \le F < n^{1/2}$, write $n = c_2 F^2 + c_1 F + 1$ in base $F$; then $n$ is prime exactly when $c_1^2 - 4 c_2$ is not a square. If it is a square $u^2$, then $n = (\frac{c_1 - u}{2} F + 1)(\frac{c_1 + u}{2} F + 1)$. HAC Fact 4.42 is a similar criterion for $F \ge n^{1/3}$.
- **Konyagin and Pomerance: $F \ge n^{3/10}$** (Theorem 4.1.6). A more involved criterion; Algorithm 4.1.7 of Crandall and Pomerance combines the three ranges.
- **Proth's theorem.** For $n = k 2^m + 1$ with $k < 2^m$, $F = 2^m$ and $q = 2$; one base with $a^{(n-1)/2} \equiv -1$ suffices. See the [Proth test](/proth-test/) and [Pepin's test](/pepin-test/) for Fermat numbers.
- **The $n + 1$ test.** A factored part of $n + 1$ and Lucas sequences give a similar proof, as in the [Lucas-Lehmer test](/lucas-lehmer-test/); combined $n^2 - 1$ tests use both.
- **Maurer's provable primes.** Build $n = 2 R q + 1$ from a smaller proven prime $q > R$ and prove $n$ with this test (HAC Algorithm 4.62); see [random prime generation](/random-prime-generation/).
- **Elliptic curves.** [ECPP](/ecpp/) replaces $\mathbb{Z}_n^*$ by the group of an elliptic curve, whose order can be chosen to factor easily (HAC Section 4.3.4).

## When to use it

Use it when $n - 1$ is easy to factor in part: numbers of the form $k \cdot 2^m + 1$ or $k \cdot b^m + 1$, primes built step by step with a known factor of $n - 1$, and certificates for small primes inside larger proofs. For a random large $n$ with no known structure, run a probable prime test first and then use [ECPP](/ecpp/) or the [AKS test](/aks-primality-test/) if a proof is needed. When $n + 1$ factors more easily, use the $n + 1$ test instead.

## Pitfalls

- **Checking $a^{(n-1)/q} \not\equiv 1$ instead of the gcd.** For a composite $n$, $a^{(n-1)/q} \not\equiv 1 \pmod n$ does not imply $a^{(n-1)/q} \not\equiv 1$ modulo each prime factor. The gcd condition is what the proof needs. Lucas's version with $F = n - 1$ can use the plain congruence, because there the order argument works modulo $n$ itself.
- **Too small a factored part.** With $F^2 \le n$ the conclusion "$p \equiv 1 \pmod F$" does not exclude two prime factors. Check $F^2 > n$ (or use the $n^{1/3}$ criterion with its square test).
- **Unproved primes in $F$.** If a $q_j$ is only a probable prime, the result is only a probable prime too.
- **One base for all $q$.** Requiring one $a$ for all primes of $F$ is correct but can need more tries; separate bases are allowed.
- **Treating UNKNOWN as composite.** If no base is found, $n$ is probably composite, but it is not proven; run a strong probable prime test or try more bases (HAC, text after Fact 4.41).

## Implementations

## History

Lucas gave a primality criterion from the full factorization of $n - 1$ in 1876, in the form with all proper divisors of $n - 1$, and Lehmer gave the form with prime divisors (Crandall and Pomerance, Section 4.1.1). Pocklington published the extension to a partial factorization in 1914, in the Proceedings of the Cambridge Philosophical Society. Brillhart, Lehmer and Selfridge (1975) lowered the size needed for $F$ to $n^{1/3}$ and allowed separate bases, and Konyagin and Pomerance lowered it to $n^{3/10}$. Pratt (1975) used the full-factorization criterion to show that every prime has a short certificate.

## References
