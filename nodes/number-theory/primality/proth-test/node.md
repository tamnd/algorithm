---
tag: ACSTC1
kind: algorithm
slug: proth-test
name: Proth's test
aliases:
- Proth primality test
area: number-theory/primality
level: advanced
summary: Decides exactly whether a Proth number n = k·2^m + 1, with k odd and k < 2^m, is prime. It finds a base a with Jacobi symbol (a/n) = -1, and n is prime if and only if a^((n-1)/2) = -1 mod n.
solves: [primality-proving, primality-testing]
model: multitape-turing-machine
complexity:
  vars: {n: the Proth number tested, A: the least integer a >= 2 with Jacobi symbol (a/n) not equal to 1}
  time: {worst: O((log n)^3 + A (log n)^2), best: O(log n)}
  space: {extra: O(log n)}
properties: {deterministic: true, recursive: false, certifying: true}
history:
  year: 1878
  people: [François Proth]
  note: Proth stated the theorem in the Comptes Rendus of the Paris Academy. It is the case F = 2^m of the later theorem of Pocklington, and it contains the Pepin test for Fermat numbers.
prereqs: [proth-prime, jacobi-symbol, euler-criterion, modular-exponentiation]
see_also: [pocklington-primality-test, pepin-test, fermat-prime, quadratic-residue, lucas-lehmer-test, primality-proving, integer-square-root, montgomery-multiplication]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.1.1 (Theorem 4.1.2 and the remark after it), Section 4.1.2 (Theorem 4.1.3 and Corollary 4.1.4), Exercise 4.10 (Proth's theorem) and Section 9.2.3 (Algorithm 9.2.14)
  - paper: "F. Proth, Theoremes sur les nombres premiers, Comptes Rendus de l'Academie des Sciences de Paris 87 (1878)"
    title: Theoremes sur les nombres premiers
    locator: page 926
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 12.1 (Legendre symbol and Euler's criterion) and Section 12.3 (computing the Jacobi symbol)
---

Proth's test decides whether a [Proth number](/proth-prime/) $n = k \cdot 2^m + 1$, with $k$ odd and $k < 2^m$, is [prime](/prime-number/). It finds a base $a$ with [Jacobi symbol](/jacobi-symbol/) $\left(\frac{a}{n}\right) = -1$ and computes one power: $n$ is prime if and only if $a^{(n-1)/2} \equiv -1 \pmod n$. The answer is exact in both directions, and the cost is that of one [probable prime test](/probable-prime/). Searches for large primes use it to prove numbers of this form prime.

## In plain words

Some numbers are one more than a small odd number times a large power of two. For these numbers there is a quick and exact test. Pick a base that would be a "non-square" if the number were prime; a simple rule finds one without knowing the answer. Raise the base to half of one less than the number, and keep only the remainder. If the remainder is one less than the number, the number is prime. If it is anything else, the number is composite. No error is possible either way. The test works only for numbers of this special form, because it relies on knowing the large power of two that divides one less than the number.

## The problem

The input is an integer $n$. If $n$ is a Proth number, the output is "prime" or "composite", and it is always right. A "prime" answer comes with the base $a$, which is a [primality certificate](/primality-certificate/): anyone can check $a^{(n-1)/2} \equiv -1$ with one power. If $n$ is not a Proth number, the test does not apply and the implementation raises an error; use a general test such as [Pocklington's test](/pocklington-primality-test/) or [Miller-Rabin](/miller-rabin/) for it.

**Cost model.** The integers are of arbitrary precision, and $\ell = \lfloor \lg n \rfloor + 1$ is the bit length of $n$. Costs are bit operations with schoolbook multiplication, as on a [multitape Turing machine](/multitape-turing-machine/).

## The algorithm

The test rests on two facts. **Proth's theorem** (Crandall and Pomerance, Exercise 4.10): if $2^m \mid n - 1$, $2^m > \sqrt n$ and $a^{(n-1)/2} \equiv -1 \pmod n$ for some $a$, then $n$ is prime. **[Euler's criterion](/euler-criterion/):** if $n$ is an odd prime and $\left(\frac{a}{n}\right) = -1$, then $a^{(n-1)/2} \equiv -1 \pmod n$. So a base with Jacobi symbol $-1$ settles the question both ways.

```pseudo id=main
PROTH-TEST(n)
L1  if n is not k·2^m + 1 with k odd, m ≥ 1 and k < 2^m then error "not a Proth number"
L2  if n is a perfect square then return COMPOSITE
L3  a ← 2
L4  while (a/n) = 1 do a ← a + 1             ▷ Jacobi symbol
L5  if (a/n) = 0 then return COMPOSITE       ▷ gcd(a, n) is a proper factor
L6  x ← a^((n−1)/2) mod n
L7  if x = n − 1 then return PRIME (base a)
L8  return COMPOSITE
```

Line L1 needs only the number $m$ of trailing zero bits of $n - 1$. Line L2 uses an [integer square root](/integer-square-root/); it is needed because for a square $n$ every unit has Jacobi symbol $1$, and line L4 would not stop. For a non-square $n$ the Jacobi symbol is a nontrivial homomorphism on the units, so some $a < n$ has $\left(\frac{a}{n}\right) = -1$ and line L4 stops. Line L4 computes the Jacobi symbol by quadratic reciprocity, with no factoring of $n$ (Shoup, Section 12.3).

**Choosing the base.** For $m \ge 3$, $n \equiv 1 \pmod 8$, so $\left(\frac{2}{n}\right) = 1$ and the base 2 never works. Since $n \equiv 1 \pmod 4$, reciprocity gives $\left(\frac{3}{n}\right) = \left(\frac{n}{3}\right)$, so the base 3 works whenever $n \equiv 2 \pmod 3$. For a [Fermat number](/fermat-prime/) $2^{2^j} + 1$ with $j \ge 1$ this is always the case, and the test becomes [Pepin's test](/pepin-test/) with base 3 (Crandall and Pomerance, Theorem 4.1.2).

## Example

**A prime.** $n = 97 = 3 \cdot 2^5 + 1$, with $3 < 32$.

| line | step | value |
|---|---|---|
| L2 | $\lfloor \sqrt{97} \rfloor = 9$, $81 \ne 97$ | not a square |
| L4 | $\left(\frac{2}{97}\right)$ | $1$, since $97 \equiv 1 \pmod 8$ |
| L4 | $\left(\frac{3}{97}\right) = \left(\frac{97}{3}\right) = \left(\frac{1}{3}\right)$ | $1$ |
| L4 | $\left(\frac{4}{97}\right)$ | $1$, a square |
| L4 | $\left(\frac{5}{97}\right) = \left(\frac{97}{5}\right) = \left(\frac{2}{5}\right)$ | $-1$, stop with $a = 5$ |
| L6 | $5^{48} \bmod 97$ | $96$ |
| L7 | $96 = n - 1$ | PRIME, base 5 |

**A composite.** $n = 65 = 1 \cdot 2^6 + 1$, with $1 < 64$. It is not a square, $\left(\frac{2}{65}\right) = 1$, and $\left(\frac{3}{65}\right) = \left(\frac{3}{5}\right)\left(\frac{3}{13}\right) = (-1)(1) = -1$, so $a = 3$. Then $3^{32} \equiv 61 \pmod{65}$, which is not $64$, so line L8 returns COMPOSITE. Indeed $65 = 5 \cdot 13$.

**Other cases.** For $n = 25 = 3 \cdot 2^3 + 1$, line L2 finds the square root 5. For the [Carmichael number](/carmichael-number/) $1729 = 27 \cdot 2^6 + 1$, the search reaches $a = 7$ with $\left(\frac{7}{1729}\right) = 0$, and line L5 returns the factor 7.

## Correctness

**PRIME is right** (Proth's theorem). Suppose $a^{(n-1)/2} \equiv -1 \pmod n$, and let $p$ be a prime factor of $n$. Then $a^{n-1} \equiv 1$ and $a^{(n-1)/2} \not\equiv 1 \pmod p$, because $p$ is odd. So the [order](/multiplicative-order/) of $a$ modulo $p$ divides $k \cdot 2^m$ but not $k \cdot 2^{m-1}$, so $2^m$ divides it, and it divides $p - 1$. Hence $p > 2^m$. From $k < 2^m$, $n < 2^{2m}$, so $p > \sqrt n$. A composite $n$ has a prime factor at most $\sqrt n$, so $n$ is prime. This is [Pocklington's theorem](/pocklington-primality-test/) with $F = 2^m$, where the condition $\gcd(a^{(n-1)/2} - 1, n) = 1$ holds because $a^{(n-1)/2} - 1 \equiv -2$ and $n$ is odd.

**COMPOSITE is right.** Line L2 returns it for a perfect square, and a perfect square $n > 1$ is composite. Line L5 returns it when $\left(\frac{a}{n}\right) = 0$, that is $1 < \gcd(a, n)$, and $a < n$ by the argument for line L4. Line L8 returns it when $\left(\frac{a}{n}\right) = -1$ and $a^{(n-1)/2} \not\equiv -1$. If $n$ were prime, the Jacobi symbol would be the Legendre symbol, and Euler's criterion would give $a^{(n-1)/2} \equiv -1$. So $n$ is composite.

**No error.** Every step is deterministic, and both answers are proved, so the test has no error on any Proth number. The full proof is in the proofs.

## Complexity

**The power.** Line L6 is one [modular exponentiation](/modular-exponentiation/) with an exponent of $\ell - 1$ bits: $\ell - 2$ squarings and a few products, since $(n - 1)/2 = k \cdot 2^{m-1}$ has few 1 bits when $k$ is small. That is $O(\ell^3)$ bit operations with schoolbook multiplication, or $O(\ell \, M(\ell))$ with a multiplication of cost $M(\ell)$.

**Special reduction.** For $n = k \cdot 2^m + 1$ with a small $k$, reduction modulo $n$ needs only shifts, one small multiplication and additions, so it costs $O(\ell)$ instead of a full division (Crandall and Pomerance, Algorithm 9.2.14). For $k = 1$ this is the reduction modulo $2^m + 1$.

**The base.** Each Jacobi symbol costs $O(\ell^2)$ bit operations, so line L4 costs $O(A \ell^2)$, where $A$ is the least $a \ge 2$ with $\left(\frac{a}{n}\right) \ne 1$. In practice $A$ is tiny: over all 1487 Proth numbers below $10^6$ the search never went past $a = 37$. The page states no general bound on $A$. A variant that draws $a$ at random from $[2, n - 2]$ finds a base with symbol $-1$ in about 2 tries on average for a non-square $n$, since the symbol is $-1$ on exactly half of the units.

**Total.** $O(\ell^3 + A \ell^2)$ bit operations and $O(\ell)$ extra space. The best case is $O(\ell)$, when line L1 rejects $n$ or line L2 finds a square and $n$ is small; computing $m$ alone takes $O(\ell)$.

## Properties

- **Exact.** Unlike [Miller-Rabin](/miller-rabin/), the test proves both answers. It is the Proth-number analogue of the [Lucas-Lehmer test](/lucas-lehmer-test/) for Mersenne numbers.
- **Certifying for primes.** The base $a$ is a short certificate of primality. A composite answer from line L8 comes with no factor, only the residue $x \ne -1$.
- **Same cost as a probable prime test.** One power modulo $n$, so proving a Proth prime costs about as much as testing a random number of the same size.
- **Restricted input.** It applies only when the power of 2 in $n - 1$ is larger than $\sqrt n$.

## Variants and improvements

- **Pepin's test.** For Fermat numbers $F_j = 2^{2^j} + 1$, $j \ge 1$, the base 3 always has symbol $-1$; see [Pepin's test](/pepin-test/). Pepin used 5, and Proth and Lucas noticed that 3 works (Crandall and Pomerance, remark after Theorem 4.1.2).
- **Pocklington's test.** With any factored part $F > \sqrt n$ of $n - 1$, not only a power of 2; see the [Pocklington test](/pocklington-primality-test/). The $n^{1/3}$ criterion of Brillhart, Lehmer and Selfridge relaxes the size condition further.
- **Numbers $k \cdot b^m + 1$.** The same argument works for a prime $b$ with $b^m \mid n - 1$ and $b^m > \sqrt n$, with a base $a$ for which $a^{n-1} \equiv 1$ and $\gcd(a^{(n-1)/b} - 1, n) = 1$.
- **Numbers $k \cdot 2^m - 1$.** Here $n + 1$ has the large power of 2, and a Lucas sequence test of the $n + 1$ type, such as the Lucas-Lehmer test for Mersenne numbers, plays the same role.
- **Fast arithmetic.** Large searches use FFT multiplication and the special reduction above.

## When to use it

Use it to prove the primality of numbers of the form $k \cdot 2^m + 1$ with $k < 2^m$: in searches for large primes, for Fermat number factors, and to build primes with a known factorization of $n - 1$. Run trial division by small primes first, since most candidates have a small factor. For numbers of any other form use [Pocklington's test](/pocklington-primality-test/) if $n - 1$ factors well, or a general method such as [ECPP](/ecpp/).

## Pitfalls

- **Skipping the square test.** For a square $n$, every unit has Jacobi symbol $1$, so the search of line L4 runs up to $n$ without finding a base. Proth squares exist, for example $(2^a + 1)^2 = 2^{a+1}(2^{a-1} + 1) + 1$.
- **A fixed base.** The base 2 never works for $m \ge 3$, and the base 3 works only when $n \equiv 2 \pmod 3$. A fixed base with $\left(\frac{a}{n}\right) = 1$ can give $a^{(n-1)/2} \equiv 1$ for a prime, which is not a proof of anything.
- **Applying it outside Proth numbers.** If $k \ge 2^m$, the congruence $a^{(n-1)/2} \equiv -1$ only shows that each prime factor is $\equiv 1 \pmod{2^m}$, which does not exclude two such factors.
- **Treating $a^{(n-1)/2} \equiv 1$ as "probably prime".** With $\left(\frac{a}{n}\right) = -1$, the value $1$ already proves $n$ composite.

## Implementations

## History

Proth published his theorem in 1878, in the Comptes Rendus of the Paris Academy. It is closely related to Pepin's test for Fermat numbers, and Proth and Lucas observed that Pepin's base 5 can be replaced by 3 (Crandall and Pomerance, Section 4.1.1). The general form with any factored part of $n - 1$ is Pocklington's theorem of 1914.

## References
