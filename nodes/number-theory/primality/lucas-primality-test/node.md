---
tag: 12XYK5
kind: algorithm
slug: lucas-primality-test
name: Lucas primality test
aliases:
- Lucas test
- Lucas-Lehmer-type test
- n - 1 primality test
area: number-theory/primality
level: advanced
summary: Proves n prime from the prime factors of n - 1. For each prime q dividing n - 1 it finds a base a with a^(n-1) ≡ 1 and a^((n-1)/q) ≢ 1 (mod n).
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested, m: the number of distinct prime factors of n - 1}
  time: {worst: O(m n^(1/2) (log n)^3), best: O(1)}
  space: {extra: O(m log n)}
properties: {deterministic: true, recursive: false, certifying: true}
history:
  year: 1876
  people: [Édouard Lucas, Derrick Henry Lehmer, John Brillhart, John Selfridge]
  note: Lucas stated the converse of Fermat's little theorem with a primitive root in 1876. Lehmer gave the form with the prime factors of n - 1 in 1927. Brillhart Lehmer and Selfridge allowed a different base for each prime factor in 1975.
prereqs: [fermat-little-theorem, multiplicative-order, primitive-root, modular-exponentiation]
see_also: [pocklington-primality-test, pratt-certificate, proth-test, pepin-test, lucas-lehmer-test, primitive-root, fermat-primality-test, primality-certificate]
sources:
  - paper: doi:10.1090/S0002-9904-1927-04368-3
    title: D. H. Lehmer, Tests for primality by the converse of Fermat's theorem, Bulletin of the American Mathematical Society 33 (1927)
    locator: pages 327 to 340 (the test with the prime factors of n - 1)
  - paper: doi:10.1090/S0025-5718-1975-0384673-1
    title: John Brillhart, D. H. Lehmer and J. L. Selfridge, New primality criteria and factorizations of 2^m ± 1, Mathematics of Computation 29 (1975)
    locator: pages 620 to 647 (Theorem 1, a separate base for each prime factor of n - 1, and the partial factorization tests)
  - paper: doi:10.1137/0204018
    title: Vaughan R. Pratt, Every prime has a succinct certificate, SIAM Journal on Computing 4 (1975)
    locator: pages 214 to 220 (the recursive certificate built on the Lucas test)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.1, The n - 1 test (the Lucas theorem and its proof, and Pocklington's theorem)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.4, Factoring into primes (the converse of Fermat's theorem as a primality proof)
---

The Lucas primality test proves that an integer $n$ is [prime](/prime-number/) when the prime factors of $n - 1$ are known. It looks for bases $a$ with $a^{n-1} \equiv 1 \pmod n$ but $a^{(n-1)/q} \not\equiv 1$ for each prime $q$ dividing $n - 1$; such bases exist exactly when $n$ is prime. The answer is always right, and the bases found are a short certificate that anyone can check with a few modular exponentiations. Its weak point is the need to factor $n - 1$, so it is used for numbers of special form and inside recursive certificates.

## In plain words

Fermat's little theorem says that for a prime, raising a base to the power one less than the prime always gives a remainder of one. Many composite numbers also do this for some bases, so this alone proves nothing. Lucas found the missing piece: also check that no smaller power of the right kind gives one. If a base passes both checks, the number must be prime.

To know which smaller powers to check, the test needs the prime factors of the number just below. When those are known, for example for numbers built as a power of two times a small number, plus one, the test is fast and its result is a proof.

## The problem

The input is an integer $n \ge 0$ and the list $q_1, \ldots, q_m$ of the distinct primes that divide $n - 1$. The output is true if $n$ is prime and false otherwise, and the answer is always right. For a prime $n$ the test can also return one base $a_i$ for each $q_i$; together with the list of the $q_i$, this is a certificate of primality.

The test does not check that the $q_i$ are prime; a full proof needs a proof for each of them too. It does check that they divide $n - 1$ and that $n - 1$ has no other prime factor.

**Cost model.** The integers are of arbitrary precision, with $\ell = \lfloor \lg n \rfloor + 1$ binary digits. Costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/). One product modulo $n$ costs $O(\ell^2)$ with [schoolbook multiplication](/schoolbook-multiplication/), or $O(M(\ell))$ with fast multiplication and division; a [modular exponentiation](/modular-exponentiation/) with an exponent below $n$ is $O(\ell)$ products. On a word RAM with $n < 2^w$, a product modulo $n$ is $O(1)$ steps.

## The algorithm

```pseudo id=main
LUCAS(n, q_1, …, q_m)                       ▷ q_i: the distinct primes dividing n − 1
L1  if n < 3 then return n = 2
L2  for i ← 1 to m do
L3      a ← 2
L4      loop
L5          if a^(n−1) mod n ≠ 1 then return false     ▷ a is a Fermat witness
L6          if a^((n−1)/q_i) mod n ≠ 1 then exit loop   ▷ a_i ← a
L7          a ← a + 1
L8  return true
```

For each prime $q_i$, lines L3 to L7 try the bases $2, 3, 4, \ldots$ in turn. A base that fails the Fermat condition of line L5 proves $n$ composite at once. A base that passes it and also has $a^{(n-1)/q_i} \not\equiv 1$ settles $q_i$, and the search moves to the next prime. When every $q_i$ is settled, line L8 returns true.

**Why it works.** If $a^{n-1} \equiv 1$ and $a^{(n-1)/q} \not\equiv 1$, the [multiplicative order](/multiplicative-order/) of $a$ modulo $n$ divides $n - 1$ but not $(n - 1)/q$, so it contains the full power $q^e$ of $q$ that divides $n - 1$. That order also divides $\varphi(n)$, the number of units modulo $n$. If this holds for every $q$, then $n - 1$ divides $\varphi(n)$, and since $\varphi(n) < n - 1$ for every composite $n$, the number $n$ is prime. In the other direction, a prime $n$ has a [primitive root](/primitive-root/) $g$, of order $n - 1$, which passes for every $q$; so each search ends by $a = g$.

**Why each search ends.** For a composite $n$, let $p$ be its smallest prime factor. When the search reaches $a = p$, $a^{n-1} \equiv 0 \pmod p$, so line L5 returns false. So no search goes past $p \le \sqrt n$, and for a prime it goes no further than the least primitive root.

**One base or many.** Lucas's and Lehmer's form asks for one base $a$ that works for all $q$ at once, that is, a primitive root. The form here, due to Brillhart, Lehmer and Selfridge, lets each $q$ have its own base, which is easier to find: $a$ settles $q$ unless $a$ is a $q$-th power modulo $n$, and for a prime $n$ only a fraction $1/q \le 1/2$ of the units are.

## Example

**$n = 1009$, a prime.** Here $n - 1 = 1008 = 2^4 \cdot 3^2 \cdot 7$, so the primes are $2, 3, 7$, and the exponents are $504$, $336$ and $144$.

| $q$ | bases tried | $a^{1008} \bmod 1009$ | $a^{1008/q} \bmod 1009$ | base found |
|---|---|---|---|---|
| 2 | $2, 3, \ldots, 10$ | $1$ | $1$ for each | |
| 2 | $11$ | $1$ | $1008$ | $a_1 = 11$ |
| 3 | $2$ | $1$ | $374$ | $a_2 = 2$ |
| 7 | $2$ | $1$ | $105$ | $a_3 = 2$ |

The bases $2, \ldots, 10$ are all quadratic residues modulo 1009, so $a^{504} \equiv 1$ for each; 11 is the least non-residue, and also the least primitive root of 1009. The certificate is $\{2 \mapsto 11, 3 \mapsto 2, 7 \mapsto 2\}$, which a reader checks with six exponentiations. With a single base for all $q$, the search would also stop at 11, after 10 failures.

**$n = 561 = 3 \cdot 11 \cdot 17$, a [Carmichael number](/carmichael-number/).** Here $560 = 2^4 \cdot 5 \cdot 7$. For $q = 2$, the base 2 gives $2^{560} \equiv 1$ and $2^{280} \equiv 1$, so the search goes on. The base 3 gives $3^{560} \equiv 375 \ne 1$, since 3 divides 561, and line L5 returns false.

## Correctness

**Theorem (Lucas, Lehmer, Brillhart-Lehmer-Selfridge).** Let $n \ge 3$. Then $n$ is prime if and only if for each prime $q$ dividing $n - 1$ there is an integer $a_q$ with $a_q^{n-1} \equiv 1 \pmod n$ and $a_q^{(n-1)/q} \not\equiv 1 \pmod n$.

*If.* Let $q^e$ be the exact power of $q$ in $n - 1$. The order $r$ of $a_q$ in the group of units modulo $n$ divides $n - 1$, since $a_q^{n-1} \equiv 1$, and does not divide $(n - 1)/q$. So $q^e \mid r$. By [Lagrange's theorem](/lagranges-theorem-group-theory/), $r \mid \varphi(n)$. Hence $q^e \mid \varphi(n)$ for every $q$, so $n - 1 \mid \varphi(n)$. As $\varphi(n) \le n - 1$, this gives $\varphi(n) = n - 1$, so every integer in $[1, n - 1]$ is coprime to $n$ and $n$ is prime.

*Only if.* A prime $n$ has a primitive root $g$, of order $n - 1$. Then $g^{n-1} \equiv 1$ and $g^{(n-1)/q} \not\equiv 1$ for each $q$, so $a_q = g$ works.

**The algorithm.** Line L5 returns false only for a Fermat witness, which a prime does not have, by [Fermat's little theorem](/fermat-little-theorem/). Line L8 returns true only when every $q_i$ has a base with both properties, so $n$ is prime by the theorem. Each search ends by $a = p$, the smallest prime factor, for composite $n$, and by $a = g$ for prime $n$. The full proof is in the proofs.

## Complexity

**One base.** Lines L5 and L6 are two modular exponentiations, $O(\ell)$ products modulo $n$, so $O(\ell^3)$ bit operations with schoolbook arithmetic and $O(\ell \, M(\ell))$ with fast arithmetic.

**Prime inputs.** For each $q$ the search stops at the least $a$ that is not a $q$-th power residue modulo $n$. For most primes this is 2 or 3. In the worst case it is bounded by the least primitive root: under the generalized Riemann hypothesis the least $q$-th power non-residue is $O((\log n)^2)$, by Bach's bounds, and without it only bounds that are a small power of $n$ are proved. So a typical run costs $O(m)$ exponentiations, $O(m (\log n)^3)$ bit operations; as $m \le \lg n$, at most $O((\log n)^4)$.

**Composite inputs.** Most composites fail line L5 with the base 2. A composite for which every base below its smallest prime factor $p$ passes the Fermat test, such as a Carmichael number, can force each search up to $a = p \le \sqrt n$, which gives the worst case $O(m \sqrt n (\log n)^3)$ of the front matter. In practice the test is run only on numbers that already passed a probable prime test, where this does not happen.

**Factoring $n - 1$.** This cost is not included, and it is usually the hard part: no polynomial-time method to factor general $n - 1$ is known.

**Checking a certificate.** Given the $q_i$ and the bases $a_i$, a check costs $2m$ exponentiations, $O(m (\log n)^3)$ bit operations, with no search.

**Space.** $O(\log n)$ for the current values, and $O(m \log n)$ to keep the certificate.

## Properties

- **Deterministic and exact.** No error in either direction; the only input it trusts is the list of primes $q_i$.
- **Certifying.** A true answer comes with the bases $a_i$, and a false answer with a Fermat witness $a$.
- **Recursive certificates.** Proving each $q_i$ prime the same way gives a [Pratt certificate](/pratt-certificate/), which shows that primality is in NP: the whole tree has $O(\log n)$ nodes and is checked in polynomial time.
- **Needs the factors.** The test is only as practical as the factorization of $n - 1$.
- **Related tests.** [Pépin's test](/pepin-test/) for Fermat numbers and the [Proth test](/proth-test/) are special cases with a fixed base and $n - 1$ a power of 2 times a small number. The [Lucas-Lehmer test](/lucas-lehmer-test/) is the analogue with $n + 1$ in place of $n - 1$.

## Variants and improvements

- **Partial factorization (Pocklington).** It is enough to factor part $F$ of $n - 1$ with $F > \sqrt n$: if for each prime $q \mid F$ some $a$ has $a^{n-1} \equiv 1$ and $\gcd(a^{(n-1)/q} - 1, n) = 1$, then $n$ is prime. See the [Pocklington test](/pocklington-primality-test/). Brillhart, Lehmer and Selfridge lowered the bound to about $n^{1/3}$ with extra work.
- **The $n + 1$ test.** When $n + 1$ is factored, Lucas sequences replace powers: $n$ is prime if a Lucas sequence has rank $n + 1$ modulo $n$. Combined tests use partial factors of both $n - 1$ and $n + 1$.
- **Random bases.** Choosing $a$ at random, a prime $n$ settles each $q$ with probability $1 - 1/q \ge 1/2$ per try, so the expected number of tries for all $q$ is at most $2m$.
- **Beyond $n \pm 1$.** When neither $n - 1$ nor $n + 1$ factors well, cyclotomic methods such as [APR-CL](/apr-cl-primality-test/) and elliptic curve methods such as [ECPP](/ecpp/) take over.

## When to use it

Use the Lucas test when $n - 1$ is easy to factor: numbers built as $2^k h + 1$, primes generated together with the factors of $n - 1$ for cryptography, and the nodes of a Pratt certificate. Run a cheap probable prime test such as [Miller-Rabin](/miller-rabin/) first, so that only likely primes reach it. When only part of $n - 1$ factors, use Pocklington's form; when $n - 1$ does not factor at all, use another proof method.

## Pitfalls

- **Unproved factors.** If some $q_i$ is not prime, the theorem does not apply, and a composite $q_i$ can hide a prime factor that was never checked. Prove each $q_i$ prime, or keep it small enough for trial division.
- **A missing prime factor.** If the list misses a prime factor of $n - 1$, a composite $n$ can pass. Check that $n - 1$ is a product of powers of the $q_i$.
- **One base for all $q$.** Requiring a single base to work for every $q$ is correct but wastes time: it needs a primitive root, while separate bases need only one non-residue per $q$.
- **Checking only $a^{n-1} \equiv 1$.** That is the [Fermat test](/fermat-primality-test/), which Carmichael numbers pass for every coprime base.
- **Slow on composites.** A composite that passes the Fermat test for many small bases makes the searches long; test for compositeness first.

## Implementations

## History

Édouard Lucas stated in 1876 that $n$ is prime if some $a$ has $a^{n-1} \equiv 1$ and $a^x \not\equiv 1$ for every proper divisor $x$ of $n - 1$, and he used such tests, with their $n + 1$ analogues, on Mersenne and Fermat numbers. Derrick Henry Lehmer reduced the check to the exponents $(n - 1)/q$ in 1927. In 1975 John Brillhart, Lehmer and John Selfridge allowed a separate base for each $q$ and gave tests that need only part of $n - 1$ factored, and in the same year Vaughan Pratt used the test to show that every prime has a certificate of polynomial size.

## References
