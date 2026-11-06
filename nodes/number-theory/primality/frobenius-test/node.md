---
tag: 3WFYQX
kind: algorithm
slug: frobenius-test
name: Frobenius primality test
aliases:
- Grantham Frobenius test
- quadratic Frobenius test
- random quadratic Frobenius test
- RQFT
area: number-theory/primality
level: research
summary: Randomized test that checks how x behaves in Z_n[x]/(x^2 - ax + b) for a random quadratic. It never rejects a prime and accepts a composite with probability below 1/7710 per round.
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested}
  time: {expected: O((log n)^3), best: O(1)}
  space: {extra: O(log n)}
properties: {deterministic: false, recursive: false, certifying: false}
history:
  year: 1998
  people: [Jon Grantham]
  note: Grantham defined Frobenius pseudoprimes and gave the random quadratic Frobenius test with the error bound 1/7710 in 1998. The full theory of Frobenius pseudoprimes for polynomials of any degree appeared in 2001.
prereqs: [jacobi-symbol, euler-criterion, strong-pseudoprime, irreducible-polynomial, modular-exponentiation]
see_also: [miller-rabin, baillie-psw, solovay-strassen, strong-pseudoprime, probable-prime, one-sided-error, carmichael-number, discriminant]
sources:
  - paper: doi:10.1006/jnth.1998.2247
    title: Jon Grantham, A probable prime test with high confidence, Journal of Number Theory 72 (1998)
    locator: pages 32 to 47 (the quadratic Frobenius test, the random version and the bound 1/7710)
  - paper: doi:10.1090/S0025-5718-00-01197-2
    title: Jon Grantham, Frobenius pseudoprimes, Mathematics of Computation 70 (2001)
    locator: pages 873 to 891 (Frobenius and strong Frobenius pseudoprimes for monic polynomials of any degree)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Sections 3.6.2 to 3.6.5 (Definition 3.6.5, Theorem 3.6.6, strong Frobenius pseudoprimes and Theorem 3.6.10)
  - paper: doi:10.1090/S0025-5718-1980-0583518-6
    title: Robert Baillie and Samuel S. Wagstaff Jr., Lucas pseudoprimes, Mathematics of Computation 35 (1980)
    locator: pages 1391 to 1417 (Lucas and strong Lucas pseudoprimes, which the Frobenius test refines)
  - url: https://en.wikipedia.org/wiki/Frobenius_pseudoprime
    title: Frobenius pseudoprime, Wikipedia
    locator: the definition and the quadratic case
---

The Frobenius test is a randomized [primality test](/primality-testing/) that works in the ring $\mathbb{Z}_n[x]/(x^2 - ax + b)$ instead of in $\mathbb{Z}_n$. If $n$ is prime and the quadratic has no root modulo $n$, this ring is a field with $n^2$ elements, and raising to the power $n$ swaps the two roots of the quadratic. The test checks this and a strong form of it, for a random quadratic. Grantham proved that a composite with no small factor passes for at most 1/7710 of the allowed quadratics, so one round costs a few [Miller-Rabin](/miller-rabin/) rounds but gives the confidence of about six and a half.

## In plain words

Simple primality tests raise a number to a large power and check the answer. The Frobenius test does the same with a slightly bigger kind of number: pairs that behave like the numbers of the form $u + v x$, where $x$ is a root of a chosen equation of degree two that has no solution modulo $n$.

For a prime, the large power of $x$ must turn $x$ into the other root of the equation, and some related powers must give plus or minus one. A composite number almost never fakes all of this. The test picks the equation at random, so no fixed bad case can fool it every time, and it never calls a prime composite.

## The problem

The input is an integer $n \ge 0$ and a source of random numbers. The output is true or false. If $n$ is prime the output must be true. If $n$ is composite the output should be false; a wrong true is allowed, with a small probability that is bounded for every composite $n$.

**Cost model.** The integers are of arbitrary precision, with $\lg n$ binary digits, and costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/). One product modulo $n$ costs $O((\log n)^2)$ with [schoolbook multiplication](/schoolbook-multiplication/), or $O(M(\log n))$ with fast multiplication. An element $u + v x$ of the ring is a pair of numbers modulo $n$, and one product of two elements is a fixed number of products modulo $n$.

## The algorithm

Let $f(x) = x^2 - ax + b$, with discriminant $\Delta = a^2 - 4b$, and let $B = 50000$.

```pseudo id=main
FROBENIUS(n)
L1  if n < 2 then return false
L2  for each prime q ≤ B: if q² > n then return true; if q | n then return n = q
L3  if n < (B + 1)² then return true
L4  if n is a perfect square then return false
L5  choose random a, b in [1, n) with gcd(bΔ, n) = 1, (Δ/n) = −1 and (b/n) = 1
L6      if a try gives 1 < gcd(bΔ, n) < n then return false
L7  y ← x^((n+1)/2) mod (f(x), n)
L8  if y has a nonzero x term then return false
L9  if y² ≢ b (mod n) then return false
L10 write n² − 1 = 2^r · s with s odd; z ← x^s mod (f(x), n)
L11 if z = 1 then return true
L12 for j ← 0 to r − 2: if z = −1 then return true; z ← z²
L13 return false
```

Lines L1 to L4 are trial division by the primes up to $B$ and a square test. They settle every $n < (B + 1)^2$ exactly, and they rule out the inputs for which the error bound fails: numbers with a small prime factor, and squares. For a square $n$ the [Jacobi symbol](/jacobi-symbol/) $(\Delta / n)$ is never $-1$, so line L5 would never stop.

Line L5 draws pairs $(a, b)$ at random until the quadratic looks irreducible modulo $n$, that is $(\Delta / n) = -1$, and $b$ looks like a square, $(b / n) = 1$. About one try in four succeeds. A try that hits a common factor with $n$ proves $n$ composite.

Lines L7 to L9 are the Frobenius step. Powers of $x$ are computed by square and multiply on pairs $(u, v)$ meaning $u + v x$, with $x^2$ replaced by $a x - b$. For a prime, $y^2 = x^{n+1}$ is the product of the two roots of $f$, which is $b$, and $y$ itself is a square root of $b$ in $\mathbb{Z}_n$.

Lines L10 to L13 are the strong step, as in Miller-Rabin. For a prime, $x^{n^2 - 1} = 1$, and the sequence $x^s, x^{2s}, x^{4s}, \ldots$ must reach 1 through $-1$, unless it starts at 1. It even reaches 1 by the index $r - 1$, since $x^{(n^2-1)/2} = b^{(n-1)/2} = 1$ by [Euler's criterion](/euler-criterion/), so the search for $-1$ stops at $r - 2$.

**Why primes pass.** If $n$ is an odd prime and $(\Delta / n) = -1$, $f$ is [irreducible](/irreducible-polynomial/) modulo $n$, and $R = \mathbb{Z}_n[x]/(f)$ is the field with $n^2$ elements. The map $z \mapsto z^n$ is its Frobenius automorphism; it fixes $\mathbb{Z}_n$ and sends the root $x$ of $f$ to the other root $a - x$. So $x^{n+1} = x (a - x) = b$, and $y = x^{(n+1)/2}$ has $y^2 = b$. As $b$ is a square in $\mathbb{Z}_n$, the two square roots of $b$ in the field $R$ are the two square roots in $\mathbb{Z}_n$, so $y$ has no $x$ term. In a field, $1$ has only the square roots $\pm 1$, which gives the strong step. The full proof is in the proofs.

## Example

**$n = 97$, a prime, with $f = x^2 - x + 2$.** Lines L1 to L4 are skipped in this example, as if $B$ were small. Here $\Delta = -7$, $(-7 / 97) = -1$ and $(2 / 97) = 1$, so the pair $(a, b) = (1, 2)$ is allowed. Line L7 computes $y = x^{49} \equiv 83$, with no $x$ term, and $83^2 = 6889 \equiv 2 = b$, so lines L8 and L9 pass. Then $97^2 - 1 = 9408 = 2^6 \cdot 147$, so $r = 6$ and $s = 147$.

| $j$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $x^{2^j \cdot 147} \bmod (f, 97)$ | 69 | 8 | 64 | 22 | 96 |

At $j = 4$ the value is $96 \equiv -1$, so line L12 returns true. As a check, $x^{97} \equiv 1 - x = a - x$, the other root of $f$.

**$n = 5777 = 53 \cdot 109$ with $f = x^2 - x - 1$.** This $n$ passes every step for this polynomial: $x^{2889} \equiv 5701$, $5701^2 \equiv -1 = b$, and $x^s \equiv 5701$, $x^{2s} \equiv -1$. It is a Lucas pseudoprime and a strong Frobenius pseudoprime with respect to this fixed quadratic. But for random allowed pairs $(a, b)$ it fails almost always: in 2000 random draws in the tests of this page it passed at most a few times. This is why the test picks the quadratic at random.

**$n = 35 = 5 \cdot 7$.** Of the 132 allowed pairs $(a, b)$ modulo 35, two pass lines L7 to L13: $x^2 - x + 1$ and $x^2 + x + 1$, whose roots are roots of unity of order 6. That rate, 1/66, is far above 1/7710, which is why the bound needs trial division first.

## Correctness

**Primes are never rejected.** Line L2 accepts a prime $n \le B$ when $q = n$, and accepts any $n$ with no prime factor up to $\sqrt n$. Line L3 accepts only numbers with no prime factor up to $B \ge \sqrt n$, which are prime. A prime above $(B + 1)^2$ is not a square, line L6 cannot fire, and lines L7 to L13 accept it by the field argument above.

**False is always right.** Every false answer comes with a proof: a factor at line L2 or line L6, a square root at line L4, or a property that every prime has, at lines L8, L9 and L13.

**Error bound (Grantham).** Let $n$ be composite, not a square, and with no prime factor up to 50000. Then $n$ passes lines L7 to L13 for at most $1/7710$ of the pairs $(a, b)$ allowed at line L5 (Crandall and Pomerance, Theorem 3.6.10). Line L5 draws an allowed pair uniformly, so one round accepts $n$ with probability at most $1/7710$, and $k$ independent rounds with probability at most $7710^{-k}$. The error is one-sided: only composites can be misjudged, and only as prime. The bound depends on the trial division bound $B$ and holds for every such $n$, not only on average.

**Termination.** Line L2 has a fixed number of steps, and each power is a loop over the binary digits of the exponent. Line L5 is a random search; for an odd non-square $n$ allowed pairs exist, so it ends with probability 1, after about 4 tries on average for a prime.

## Complexity

**One round.** Line L7 is about $\lg n$ squarings in $R$, and line L10 about $2 \lg n$, since $s < n^2$. A squaring of $u + v x$ costs three products modulo $n$ and a product by $x$ costs two, so a round is $O(\log n)$ products modulo $n$: $O((\log n)^3)$ bit operations with schoolbook arithmetic and $O(\log n \, M(\log n))$ with fast multiplication. Grantham arranges the work to cost about three Miller-Rabin rounds; the plain code of this page costs more, as Python's built-in modular power is in C.

**Line L5.** Each try is two Jacobi symbols, $O((\log n)^2)$ bit operations, and the expected number of tries is a small constant.

**Trial division.** Lines L2 and L3 use the 5133 primes below 50000, a fixed number of divisions of $n$ by small numbers, $O(\log n)$ each.

**Best case.** An even $n$ or one with a small factor stops in line L2 after a few divisions.

**Space.** A few elements of $R$, $O(\log n)$ bits.

## Properties

- **Randomized, one-sided error.** A Monte Carlo test with [one-sided error](/one-sided-error/): a false answer is always right, a true answer is wrong with probability at most $1/7710$ per round for every composite.
- **Stronger than Lucas and Fermat.** If $n$ passes with respect to $x^2 - ax + b$, it is a Fermat probable prime to the base $b$ and a strong Lucas probable prime with parameters $(a, b)$. So the test combines a [strong pseudoprime](/strong-pseudoprime/) style check with a Lucas check, much like [Baillie-PSW](/baillie-psw/), but with a proved error bound.
- **Better confidence per unit of work.** One round costs about as much as three Miller-Rabin rounds, which together give the bound $1/64$; one Frobenius round gives $1/7710$.
- **Not certifying.** A true answer gives no proof of primality.

## Variants and improvements

- **Fixed quadratic.** Using one fixed quadratic, chosen by a rule like Selfridge's in Baillie-PSW, gives a deterministic probable prime test. Frobenius pseudoprimes for such a quadratic are very rare, but they exist, such as 5777 for $x^2 - x - 1$, and the error bound is lost.
- **The general Frobenius test.** Grantham's 2001 paper uses any monic polynomial $f$ of degree $d$. It computes the distinct degree factorization of $f$ modulo $n$ as if $n$ were prime, and checks that the pieces have the degrees and the sign, measured by the Jacobi symbol of the [discriminant](/discriminant/) of $f$, that Galois theory demands of a prime.
- **Extended quadratic Frobenius test.** Damgård and Frandsen gave a variant with a much smaller error bound per round, and a better average error for random inputs, which matters when generating random primes.
- **Combined tests.** Tests that combine a strong probable prime test to base 2 with one Lucas or Frobenius check are used in place of several rounds of Miller-Rabin.

## When to use it

Use the random quadratic Frobenius test when a probable prime test must have a proved error bound and the cost of each round matters, for example to reach an error of $2^{-128}$ with fewer rounds than Miller-Rabin would need. For general use, [Baillie-PSW](/baillie-psw/) is simpler and has no known counterexample, but no proved bound. When a proof is needed, follow the test with a primality proof such as ECPP.

## Pitfalls

- **Skipping trial division or the square test.** The bound $1/7710$ assumes no prime factor up to 50000 and that $n$ is not a square. Without these steps small composites such as 35 pass far more often, and for a square $n$ line L5 may never find a pair.
- **A fixed or chosen quadratic.** The bound is over random quadratics. An adversary who knows the quadratic can pick a pseudoprime for it.
- **Forgetting the Jacobi conditions.** If $(\Delta/n) = 1$, the ring is not a field even for prime $n$, and the checks of lines L8 to L13 are wrong for primes.
- **Wrong reduction rule.** In $\mathbb{Z}_n[x]/(x^2 - ax + b)$, $x^2 = a x - b$; a sign error changes the polynomial and the test.
- **Recursion.** Write the powering as a loop over the binary digits of the exponent.

## Implementations

## History

Lucas tests, which use sequences tied to a quadratic, go back to Lucas and Lehmer, and Baillie and Wagstaff studied Lucas pseudoprimes in 1980. Jon Grantham saw that both Fermat and Lucas tests check properties of the Frobenius automorphism, and he defined Frobenius pseudoprimes for any monic polynomial. In 1998 he gave the random quadratic Frobenius test and proved its error bound of $1/7710$ for numbers with no prime factor below 50000, and his paper on Frobenius pseudoprimes in general appeared in Mathematics of Computation in 2001. Later work, such as the extended test of Damgård and Frandsen, lowered the error bounds further.

## References
