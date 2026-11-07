---
tag: 6CAYMS
kind: algorithm
slug: rabin-irreducibility-test
name: Rabin's irreducibility test
aliases:
- Rabin test
- Rabin's test for irreducibility
area: algebra/polynomial-arithmetic
level: advanced
summary: Tests irreducibility over GF(q) by checking that x^(q^n) is x modulo f and that x^(q^(n/r)) - x is coprime to f for each prime r dividing n.
solves: [polynomial-irreducibility-testing]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of f, q: the number of elements of the field, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(n M(n) log q)}
  space: {extra: O(n)}
  schoolbook_time: {worst: O(n^3 log q)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [polynomial-irreducibility-testing, polynomial-gcd, modular-exponentiation]
see_also: [polynomial-irreducibility-testing, irreducible-polynomial, distinct-degree-factorization, polynomial-factorization-over-finite-fields, cantor-zassenhaus-algorithm, berlekamp-factorization, binary-exponentiation, mobius-function]
sources:
  - paper: doi:10.1137/0209024
    title: Michael O. Rabin, Probabilistic algorithms in finite fields, SIAM Journal on Computing 9(2), 1980
    locator: pp. 273 to 280
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 14.9, Testing irreducibility and constructing irreducible polynomials; Section 14.2 for the factorization of x^(q^d) - x
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 20.1 (testing and constructing irreducible polynomials)
  - paper: doi:10.1109/SFCS.1981.37
    title: Michael Ben-Or, Probabilistic algorithms in finite fields, 22nd Annual Symposium on Foundations of Computer Science, 1981
    locator: pp. 394 to 398
  - paper: doi:10.1007/BF01272074
    title: Joachim von zur Gathen and Victor Shoup, Computing Frobenius maps and factoring polynomials, Computational Complexity 2, 1992
    locator: pp. 187 to 224
---

Rabin's test decides whether a polynomial $f$ of degree $n$ over the finite field $\mathbb{F}_q$ is [irreducible](/irreducible-polynomial/). It uses one fact: $x^{q^m} - x$ is the product of all monic irreducible polynomials whose degree divides $m$. So $f$ is irreducible exactly when $f$ divides $x^{q^n} - x$ and shares no factor with $x^{q^{n/r}} - x$ for each prime $r$ that divides $n$. The test computes these powers of $x$ modulo $f$ and needs $O(n\, M(n) \log q)$ field operations; it is deterministic, although Rabin published it in 1980 in a paper on randomized algorithms.

## In plain words

Over a finite field, there is one special polynomial for each size: it is the product of every irreducible polynomial whose degree divides that size, each one time. An irreducible polynomial of degree n divides the special polynomial for n, but it does not divide the special polynomial for any smaller size.

The test checks these two things for the input. First, it checks that the input divides the special polynomial for its own degree. Then, for each prime that divides the degree, it checks that the input shares nothing with the special polynomial for the degree divided by that prime. A polynomial that passes both checks cannot have a factor of smaller degree, so it is irreducible. The work is done with remainders modulo the input, so the large special polynomials are never written out.

## The problem

Given $f \in \mathbb{F}_q[x]$ of degree $n \ge 1$, decide whether $f$ is irreducible: whether $f = gh$ implies that $g$ or $h$ is a constant. This is the [irreducibility testing problem](/polynomial-irreducibility-testing/) over a finite field. Here $\mathbb{F}_q$ must be a field; the implementation uses the prime field $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$. A constant, including zero, is not irreducible.

**Cost model.** We count operations in $\mathbb{F}_q$ at unit cost, in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $\mathbb{F}_q$. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$; a product modulo $f$ costs $O(M(n))$ with fast division. $\omega(n)$ is the number of distinct prime divisors of $n$.

## The algorithm

```pseudo id=main
RABIN-IRREDUCIBLE(f, q)                        ▷ f ∈ F_q[x], deg f = n ≥ 1
L1  f ← f / lc(f)                              ▷ make f monic
L2  P ← the set of prime divisors of n
L3  h ← x rem f
L4  for j ← 1 to n do
L5      h ← h^q rem f                          ▷ now h = x^(q^j) rem f
L6      if j < n and n / j ∈ P then
L7          if gcd(h − x, f) ≠ 1 then return false
L8  return h = x rem f
```

Line L5 uses [binary exponentiation](/binary-exponentiation/) modulo $f$, which takes $O(\log q)$ products modulo $f$. After pass $j$, $h = x^{q^j} \bmod f$, because raising to the $q$-th power commutes with taking remainders modulo $f$. Line L6 picks out the passes $j = n / r$ for primes $r \mid n$, and line L7 tests the second condition there. Line L8 tests the first condition, $x^{q^n} \equiv x \pmod f$. Line L3 writes $x \bmod f$ rather than $x$ so that the case $n = 1$ also works.

## Example

Over $\mathbb{F}_2$ let $f = x^4 + x + 1$, so $n = 4$, $P = \{2\}$, and $x^4 \equiv x + 1 \pmod f$.

| $j$ | $h = x^{2^j} \bmod f$ | check |
|---|---|---|
| 1 | $x^2$ | |
| 2 | $x^4 \equiv x + 1$ | $n/j = 2 \in P$: $\gcd(h - x, f) = \gcd(1, f) = 1$, continue |
| 3 | $(x + 1)^2 = x^2 + 1$ | |
| 4 | $(x^2 + 1)^2 = x^4 + 1 \equiv x$ | |

Line L8 finds $h = x$, so $f$ is irreducible.

Two reducible inputs show the two ways to fail.

- $f = x^4 + x^2 + 1 = (x^2 + x + 1)^2$ over $\mathbb{F}_2$. At $j = 2$, $h = x^2 + 1$ and $\gcd(h - x, f) = x^2 + x + 1$, so line L7 returns false. The gcd is the factor of degree $2$.
- $f = x^4 + 1 = (x^2 + x + 2)(x^2 + 2x + 2)$ over $\mathbb{F}_3$. Here $x^9 = x \cdot x^8 \equiv x$, so already at $j = 2$, $h = x$ and $\gcd(0, f) = f$: line L7 returns false. This input also satisfies the first condition, $x^{81} \equiv x$, so the gcd tests are needed.

A script checks these traces, and the tests run them.

## Correctness

The proof rests on the lemma that $x^{q^m} - x$ is the product of all monic irreducible polynomials of degree dividing $m$, each one time. This holds because the derivative of $x^{q^m} - x$ is $-1$, so it is square-free; because every element $\beta$ of the field $\mathbb{F}_q[x]/(g)$ with $q^d$ elements satisfies $\beta^{q^d} = \beta$; and because the Frobenius map $\beta \mapsto \beta^q$ has order exactly $d$ on that field. If $f$ is irreducible of degree $n$, it divides $x^{q^n} - x$, and it cannot divide $x^{q^{n/r}} - x$ because $n \nmid n/r$, so the gcd at line L7 is $1$. Conversely, if both conditions hold, $f$ is a product of distinct irreducibles of degree dividing $n$; a factor of degree $d < n$ would divide $x^{q^{n/r}} - x$ for a prime $r$ dividing $n/d$, and the gcd would not be $1$. The full proof is below.

## Complexity

- **Powers.** Line L5 runs $n$ times, and each run uses $O(\log q)$ products modulo $f$, each costing $O(M(n))$. Total $O(n\, M(n) \log q)$ field operations. This is proved.
- **Gcds.** Line L7 runs $\omega(n) \le \log_2 n$ times. Each gcd costs $O(n^2)$ with the [Euclidean algorithm](/polynomial-euclidean-algorithm/) or $O(M(n) \log n)$ with a fast gcd. This is dominated by the powers.
- **Prime divisors.** Line L2 factors the integer $n$ by [trial division](/trial-division/) in $O(n^{1/2})$ integer operations, which is negligible.
- **Space.** $O(n)$ field elements.
- **The implementation.** It uses schoolbook products and remainders, $O(n^2)$ each, so it costs $O(n^3 \log p)$ operations in $\mathbb{F}_p$.

An irreducible input always runs all $n$ passes, so the bound is also the cost of every accepted input. A reducible input can stop early at line L7.

The loop can be shortened. It needs only $x^{q^{n/r}} \bmod f$ for the primes $r$ and $x^{q^n} \bmod f$. Von zur Gathen and Shoup (1992) compute these iterated Frobenius powers with modular composition, which costs less than $n$ separate powerings when $n$ is large. With fast modular composition the cost becomes subquadratic in $n$; see [polynomial composition](/polynomial-composition/).

## Properties

- **Deterministic and exact.** The test makes no random choices and never errs. Rabin's paper uses it inside a randomized algorithm that finds irreducible polynomials.
- **Uses only field arithmetic.** It needs products, remainders and gcds modulo $f$; it never factors $f$.
- **A by-product: the number of irreducibles.** Comparing degrees in the lemma gives $q^n = \sum_{d \mid n} d\, N_d$, where $N_d$ is the number of monic irreducible polynomials of degree $d$. [Möbius inversion](/mobius-function/) gives $N_n = \frac{1}{n} \sum_{d \mid n} \mu(d)\, q^{n/d}$, Gauss's formula. The tests check the implementation against these counts for small $p$ and $n$.
- **Probability.** By Gauss's formula $N_n \ge (q^n - 2 q^{n/2})/n$, so about one random monic polynomial of degree $n$ in $n$ is irreducible.
- Not recursive.

## Variants and improvements

- **Ben-Or's test.** Ben-Or (1981) computes $\gcd(x^{q^i} - x, f)$ for $i = 1, 2, \ldots, \lfloor n/2 \rfloor$ and stops at the first gcd that is not $1$. The worst case is the same order, but a random reducible polynomial usually has a factor of small degree, so the test stops early. For random inputs, this is faster in practice. Von zur Gathen and Gerhard, Section 14.9, compare the two tests.
- **Constructing irreducible polynomials.** Choose random monic polynomials of degree $n$ and test them until one passes. By the probability bound above, the expected number of trials is $O(n)$. This is the use that Rabin (1980) described, and the method of von zur Gathen and Gerhard, Section 14.9.
- **[Distinct-degree factorization](/distinct-degree-factorization/).** It computes the same gcds for every $i$ up to $n/2$, divides out each factor it finds, and so splits $f$ into products of irreducibles of equal degree.
- **Iterated Frobenius.** Compute $x^q \bmod f$ one time, then get $x^{q^{j+1}}$ from $x^{q^j}$ by composing with $x^q$ modulo $f$. This replaces $\log q$ products by one modular composition per step and is the basis of the faster method of von zur Gathen and Shoup.
- **Extension fields.** For $q = p^k$, the same algorithm works with arithmetic in $\mathbb{F}_q$; only the exponent $q$ in line L5 changes.

## When to use it

Use Rabin's test to certify that a given polynomial is irreducible, for example the modulus of an extension field $\mathbb{F}_{p^n}$ or of a [linear feedback shift register](/linear-feedback-shift-register/). Use Ben-Or's test when searching through random candidates, where most inputs are reducible. If you need the factors, not only a yes or no, use a [factoring algorithm](/polynomial-factorization-over-finite-fields/) such as [Cantor-Zassenhaus](/cantor-zassenhaus-algorithm/) or [Berlekamp](/berlekamp-factorization/).

## Pitfalls

- **Testing only $x^{q^n} \equiv x$.** This condition alone accepts every square-free product of irreducibles whose degrees divide $n$, such as $x^4 + 1$ over $\mathbb{F}_3$. The gcd tests are needed.
- **Testing only the condition for one prime.** For $n = 6$ both $r = 2$ and $r = 3$ are needed: a product of irreducibles of degrees $2$ and $4$ is not possible, but degrees $3 + 3$ and $2 + 2 + 2$ are, and each is caught by a different prime.
- **Computing $x^{q^n}$ directly.** The exponent $q^n$ has about $n \log_2 q$ binary digits. Raise to the $q$-th power $n$ times instead, as in line L5, which needs the same number of products and no huge exponent.
- **Leading coefficient and constants.** Make $f$ monic first. A nonzero constant is a unit, not an irreducible, and the zero polynomial is not irreducible either.
- **The field must be finite.** The lemma holds only over $\mathbb{F}_q$. Over $\mathbb{Q}$ use the methods on the [irreducibility testing](/polynomial-irreducibility-testing/) page.

## Implementations

## History

Rabin (1980) gave the test in a paper on probabilistic algorithms in finite fields, where it serves to find irreducible polynomials at random. Ben-Or (1981) gave the variant that tests small degrees first. Von zur Gathen and Shoup (1992) made the computation of the Frobenius powers faster. The lemma on $x^{q^m} - x$ goes back to the study of finite fields in the nineteenth century; von zur Gathen and Gerhard, Section 14.2, and Shoup, Chapter 20, give modern proofs.

## References
