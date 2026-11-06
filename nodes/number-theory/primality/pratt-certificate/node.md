---
tag: QY13TB
kind: algorithm
slug: pratt-certificate
name: Pratt certificate
aliases:
- Pratt primality certificate
area: number-theory/primality
level: advanced
summary: A proof that p is prime from a primitive root of p and the factorization of p - 1, repeated for each odd prime factor. It has O((log p)^2) size and needs fewer than 2 lg^2 p products to check.
solves: [primality-proving]
model: multitape-turing-machine
complexity:
  vars: {n: the prime that the certificate proves}
  time: {worst: O((log n)^4), best: O(1)}
  space: {extra: O((log n)^2)}
properties: {deterministic: true, recursive: false, certifying: true}
history:
  year: 1975
  people: [Vaughan Pratt]
  note: Published as "Every prime has a succinct certificate" in SIAM Journal on Computing. It showed that the set of primes is in NP, and so in NP and co-NP together.
prereqs: [lucas-primality-test, primitive-root, multiplicative-order, modular-exponentiation]
see_also: [primality-certificate, primality-proving, pocklington-primality-test, np, co-np, ecpp, aks-primality-test, addition-chain]
sources:
  - paper: doi:10.1137/0204018
    title: Vaughan R. Pratt, Every prime has a succinct certificate, SIAM Journal on Computing 4 (1975)
    locator: pages 214 to 220
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.1.1 (Theorem 4.1.1) and Section 4.1.3 (Theorem 4.1.8, the Lucas tree for 1279, Theorem 4.1.9 and its proof)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Section 4.3.2 (Fact 4.38) and the chapter notes on Section 4.3
  - paper: doi:10.1090/S0025-5718-1987-0866117-4
    title: Carl Pomerance, Very short primality proofs, Mathematics of Computation 48 (1987)
    locator: pages 315 to 322
---

A Pratt certificate is a short proof that a number $n$ is [prime](/prime-number/). It gives a [primitive root](/primitive-root/) $a$ of $n$ and the full factorization of $n - 1$, which by Lucas's theorem prove $n$ prime once the factors are known to be prime; it then gives the same data for each odd prime factor, down to small primes. Pratt showed in 1975 that the whole tree has fewer than $\lg n$ entries and is checked with fewer than $2 \lg^2 n$ modular products, so the primes are in [NP](/np/). This page gives the checker, which is deterministic and fast, and a builder, whose cost is that of factoring.

## In plain words

To prove a number prime, give a special base for it and list the prime factors of the number just below it. A quick calculation with the base shows that the number is prime, as long as the listed factors are really prime. So prove each of those factors in the same way, and their factors, until only the prime 2 is left. The proof is a small tree of numbers. It is short, because the numbers get smaller fast, and anyone can check it with a few multiplications for each entry. Finding the proof is hard, since it needs the factors, but checking it is easy. That difference is what it means for the primes to be in the class NP.

## The problem

The input of the checker is an integer $n$ and a list $C$ of entries $(p, a, \{q: e\})$. Each entry claims that $p$ is prime, with base $a$ and the factorization $p - 1 = \prod q^{e}$. Each odd prime $q$ of an entry must be the $p$ of an earlier entry, so the list is the Lucas tree of $n$ in bottom-up order, with each prime listed once. The output is "true" if the list proves $n$ prime and "false" otherwise. The checker never accepts a composite, and it accepts every prime with a correct list.

The builder takes a number $n$ and returns a certificate, or nothing if $n$ is composite. It must factor $p - 1$ for each prime $p$ of the tree.

**Cost model.** The integers are of arbitrary precision, and $\ell = \lfloor \lg n \rfloor + 1$ is the bit length of $n$. Costs are bit operations with schoolbook multiplication, as on a [multitape Turing machine](/multitape-turing-machine/), and every number in the certificate is at most $n$.

## The algorithm

Each entry uses this form of Lucas's theorem (Crandall and Pomerance, Theorem 4.1.8). Let $p > 1$ be odd. If
$$a^{(p-1)/2} \equiv -1 \pmod p \quad \text{and} \quad a^{(p-1)/(2q)} \not\equiv -1 \pmod p \text{ for every odd prime } q \mid p - 1,$$
then $p$ is prime. Conversely, every primitive root of an odd prime $p$ satisfies these conditions. The form treats the prime $q = 2$ apart, and it needs no separate check of $a^{p-1} \equiv 1$.

```pseudo id=main
VERIFY-PRATT(n, C)          ▷ C: entries (p, a, {q: e}), children before parents
L1  if n = 2 then return true
L2  if n < 3 or n is even then return false
L3  proven ← {2}
L4  for each entry (p, a, {q: e}) of C, in order do
L5      if p < 3 or p is even or ∏ q^e ≠ p − 1 (with each e ≥ 1) then return false
L6      if some q is not in proven then return false
L7      if a^((p−1)/2) mod p ≠ p − 1 then return false
L8      for each prime q of the entry do
L9          if q ≠ 2 and a^((p−1)/(2q)) mod p = p − 1 then return false
L10     add p to proven
L11 return n ∈ proven
```

Line L5 checks that the list of $q$ is a complete factorization, and line L6 checks that each $q$ is already proven, so the proof is not circular. Lines L7 to L9 are the conditions of the theorem.

**The builder.** Start from $n$ and keep a stack of primes still to factor. For each prime $p$, factor $p - 1$ by [trial division](/trial-division/) and the [Pollard rho method](/pollard-rho/), and push its odd prime factors that are not yet factored. Then, from the smallest prime up, find the smallest base $a$ that meets the conditions of lines L7 to L9, and append the entry. A loop with a stack does this; it needs no recursion. A quick probable prime test rejects most composites at the start; any other composite fails when no base is found.

## Example

The Lucas tree for $p = 1279$ (Crandall and Pomerance, Section 4.1.3). Here $1278 = 2 \cdot 3^2 \cdot 71$, $70 = 2 \cdot 5 \cdot 7$, $6 = 2 \cdot 3$, $4 = 2^2$ and $2 = 2$. The certificate lists each prime once, children first:

| entry | $p$ | $a$ | $p - 1$ | line L7 | line L9 | products |
|---|---|---|---|---|---|---|
| 1 | 3 | 2 | $2$ | $2^1 \equiv -1$ | none | 0 |
| 2 | 5 | 2 | $2^2$ | $2^2 \equiv -1$ | none | 1 |
| 3 | 7 | 3 | $2 \cdot 3$ | $3^3 \equiv -1$ | $3^1 \equiv 3$ | 2 + 0 |
| 4 | 71 | 7 | $2 \cdot 5 \cdot 7$ | $7^{35} \equiv -1$ | $7^7 \equiv 14$, $7^5 \equiv 51$ | 7 + 4 + 3 |
| 5 | 1279 | 3 | $2 \cdot 3^2 \cdot 71$ | $3^{639} \equiv -1$ | $3^{213} \equiv 775$, $3^9 \equiv 498$ | 16 + 11 + 4 |

The last column counts the modular products of the left-to-right binary method, $\lfloor \lg e \rfloor$ squarings plus one product fewer than the number of 1 bits of $e$. The total is $48$, which is the value $M(1279) = 48$ of Crandall and Pomerance; in their tree the prime 3 appears twice, but each copy costs 0 products. The bound of Theorem 4.1.9 is $2 \lg^2 1279 \approx 213$. Each base here is the smallest that works, and the builder of the implementation finds the same list.

## Correctness

**Each entry is sound** (Theorem 4.1.8). Let $p$ be odd with $a^{(p-1)/2} \equiv -1 \pmod p$. Then $a^{p-1} \equiv 1$ and $a^{(p-1)/2} \not\equiv 1$, since $-1 \not\equiv 1$ for $p > 2$. For an odd prime $q \mid p - 1$, put $m = a^{(p-1)/(2q)}$. If $a^{(p-1)/q} = m^2 \equiv 1$, then $m^q = (m^2)^{(q-1)/2} m \equiv m$, and also $m^q = a^{(p-1)/2} \equiv -1$, so $m \equiv -1$, which line L9 excludes. So $a^{(p-1)/q} \not\equiv 1$ for every prime $q \mid p - 1$. The [order](/multiplicative-order/) $d$ of $a$ modulo $p$ divides $p - 1$; if $d < p - 1$, then $d$ divides $(p-1)/q$ for some prime $q$, which is false. So $d = p - 1$, the group of units modulo $p$ has at least $p - 1$ elements, and $p$ is prime (Lucas's theorem; Crandall and Pomerance, Theorem 4.1.1).

**The list is sound.** By induction on the entries, every number in *proven* is prime: line L6 lets an entry use only primes already proven, and line L5 checks that these primes give the whole factorization of $p - 1$, so the theorem applies with the true prime factors of $p - 1$. Hence a "true" answer means that $n$ is prime.

**Every prime has a certificate.** Every prime has a primitive root, and every primitive root meets the conditions. The prime factors of $p - 1$ are smaller than $p$, so listing the tree in increasing order puts children before parents. The full proof is in the proofs.

**No error.** The checker is deterministic and never errs. The builder returns only lists that the checker accepts. Its probable prime test can call a composite factor of $p - 1$ prime; that factor then gets no base, and the builder returns nothing, so this rare event can only cause a missing answer, never a wrong one.

## Complexity

**Size** (Theorem 4.1.9 and its proof). Let $N(p)$ be the number of odd primes in the Lucas tree. If $p - 1$ has odd prime factors $q_1, \ldots, q_k$, then by induction $N(p) = 1 + \sum N(q_i) < 1 + \sum \lg q_i \le 1 + \lg \frac{p - 1}{2} < \lg p$. So the tree has fewer than $\ell$ entries. Each entry holds a base below $p$ and a factorization of $p - 1$, which take $O(\ell)$ bits together, so the certificate takes $O(\ell^2)$ bits.

**Checking.** Crandall and Pomerance prove that the checks of the whole tree use fewer than $2 \lg^2 n$ modular products with the binary method. Each product of numbers below $n$ costs $O(\ell^2)$ bit operations, and line L5 costs $O(\ell^2)$ for each entry, so the checker uses $O(\ell^4)$ bit operations. With a multiplication of cost $M(\ell)$ this is $O(\ell^2 M(\ell))$. The best case is $O(1)$, for $n = 2$, an even $n$ or $n < 3$.

**Building.** The builder must factor $p - 1$ for each $p$ in the tree. No polynomial time method for this is known, so the builder is practical only when the $p - 1$ factor easily. Finding a base takes few tries, because a random unit is a primitive root with probability $\varphi(p - 1)/(p - 1)$, so the expected number of tries is $(p - 1)/\varphi(p - 1) = O(\ln \ln p)$ (HAC Note 4.39).

## Properties

- **Deterministic and exact.** The checker uses no randomness and has no error on any input.
- **Polynomial size.** The certificate has $O(\ell^2)$ bits and the check takes time polynomial in $\ell$. This places the primes in NP. Since a nontrivial factor shows that a number is composite, the primes are also in co-NP (HAC, chapter notes on Section 4.3).
- **Shared subtrees.** A prime that occurs several times in the tree needs only one entry. The bound $N(p) < \lg p$ already holds with repeats.
- **Hard to find, easy to check.** The builder needs factorizations; the checker does not.

## Variants and improvements

- **Fewer products.** Pomerance (1987) showed that every prime has a proof that uses only $O(\log p)$ modular products.
- **Pocklington nodes.** Each entry can use the [Pocklington test](/pocklington-primality-test/) with a factored part $F > \sqrt p$ of $p - 1$ in place of the full factorization, so only the primes of $F$ need certificates. This makes certificates far easier to build.
- **ECPP certificates.** [Elliptic curve primality proving](/ecpp/) produces a chain of curves whose orders have a large prime factor. Its certificates are short and can be built in practice for numbers with thousands of digits, without factoring $p - 1$.
- **The $n + 1$ form.** A Lucas sequence and the factorization of $p + 1$ give a similar certificate for primes where $p + 1$ factors more easily.
- **Polynomial time without certificates.** The [AKS test](/aks-primality-test/) decides primality in deterministic polynomial time and needs no certificate, but it is much slower than checking one.

## When to use it

Use a Pratt certificate when a proof of primality must be checked by someone else, or by a small trusted program, and $n - 1$ and the numbers below it in the tree are easy to factor. It is practical for primes up to a few dozen digits and for primes of special form. For large primes of no special form, use [ECPP](/ecpp/) certificates instead, since factoring each $p - 1$ is too hard.

## Pitfalls

- **An incomplete factorization.** If the list of $q$ misses a prime factor of $p - 1$, the order argument fails. Check that the product of the prime powers is exactly $p - 1$, as in line L5.
- **Unproven factors.** The entry for $p$ proves nothing unless each $q$ is prime. Check each odd $q$ against the earlier entries, as in line L6, and require children before parents, so that no entry relies on itself.
- **Checking $a^{(p-1)/(2q)} \not\equiv 1$ in place of $\not\equiv -1$.** The shortcut of Theorem 4.1.8 needs the test against $-1$. With full exponents, check $a^{(p-1)/q} \not\equiv 1$ and $a^{p-1} \equiv 1$ instead.
- **A base that is a residue.** Line L7 requires $a$ to be a quadratic non-residue modulo $p$. For $p \equiv 1 \pmod 8$, small bases such as 2 are residues, so the base search must go on.
- **Checking the same prime twice.** A prime can occur many times in the tree. Keep a set of proven primes, as in line L3, so that each one is factored and checked once.

## Implementations

## History

Lucas gave the criterion from the factorization of $n - 1$ in 1876, and Lehmer gave the form with prime divisors (Crandall and Pomerance, Section 4.1.1). Pratt (1975) noticed that the factors can be proved prime in the same way and that the tree stays small, which showed that every prime has a "succinct certificate" and that the primes are in NP. Pomerance (1987) reduced the number of products to $O(\log p)$. In 2002 Agrawal, Kayal and Saxena showed that primality is in P.

## References
