---
tag: CRFS04
kind: theorem
slug: fundamental-theorem-of-arithmetic
name: Fundamental theorem of arithmetic
aliases:
- unique factorization theorem
area: number-theory/divisibility-and-gcd
level: intro
summary: Every integer greater than 1 factors uniquely, up to order, into primes.
prereqs: [divisibility, prime-number, euclids-lemma]
see_also: [greatest-common-divisor, least-common-multiple, integer-factorization, trial-division, legendre-formula, multiplicative-function, euclidean-domain, divisor-function]
sources:
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Section 1.3, Statement of the fundamental theorem of arithmetic; Section 2.10, Proof of the fundamental theorem of arithmetic; Section 2.11, Another proof of the fundamental theorem
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 1, Section 1.5, The fundamental theorem of arithmetic
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1, Elementary number-theoretic notions (unique prime factorization, proved from the theorem that a prime dividing a product divides a factor)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.2, Primes (unique factorization and the exponent notation)
  - url: "https://en.wikipedia.org/wiki/Fundamental_theorem_of_arithmetic"
    locator: section History (Euclid, Elements, Book VII, Propositions 30 to 32 and Book IX, Proposition 14; Gauss, Disquisitiones Arithmeticae, Article 16)
---

The fundamental theorem of arithmetic says that every integer greater than 1 is a product of [prime numbers](/prime-number/), and that this product is unique apart from the order of the factors. Existence is easy; uniqueness rests on [Euclid's lemma](/euclids-lemma/), which in turn rests on [Bézout's identity](/bezouts-identity/). The theorem is the reason that the [greatest common divisor](/greatest-common-divisor/), the [least common multiple](/least-common-multiple/), the [divisor function](/divisor-function/) and every [multiplicative function](/multiplicative-function/) can be read off the exponents of the primes. It says nothing about how to find the factors: [integer factorization](/integer-factorization/) has no known polynomial-time algorithm on a classical computer.

## Statement

A **prime** is an integer $p \ge 2$ whose only positive divisors are 1 and $p$.

**Theorem.** Every integer $n \ge 2$ can be written as a product of primes

$$n = p_1 p_2 \cdots p_r \qquad (r \ge 1,\ p_i \text{ prime}),$$

and if also $n = q_1 q_2 \cdots q_s$ with primes $q_j$, then $r = s$ and the $q_j$ are the $p_i$ in some order.

**Canonical form.** Grouping equal primes, each $n \ge 2$ has exactly one representation

$$n = p_1^{a_1} p_2^{a_2} \cdots p_k^{a_k}, \qquad p_1 < p_2 < \cdots < p_k \text{ prime},\ a_i \ge 1.$$

For a prime $p$ and an integer $n \ne 0$, the exponent of $p$ in $|n|$ is written $v_p(n)$, the $p$-adic valuation; it is 0 when $p \nmid n$. With the empty product equal to 1, the statement also covers $n = 1$ (no primes, $r = 0$), and each nonzero integer is $\pm 1$ times a unique product of primes. The integer 0 has no factorization.

## In plain words

Primes are the building blocks of whole numbers under multiplication. If you keep splitting a number into smaller factors until no piece splits further, every piece you end with is a prime. The theorem says that you always get the same pieces, whichever splits you choose along the way. For example, three hundred sixty can be split as ten times thirty-six or as twelve times thirty, but both routes end with three twos, two threes and one five.

This is why a number can be described by its list of primes and how often each one appears. Many questions about divisors, common divisors and common multiples become simple questions about those counts.

## Proof

The proof has two parts: existence and uniqueness.

**Existence.** By strong induction on $n \ge 2$. If $n$ is prime, then $n = n$ is a product of one prime. If $n$ is not prime, it has a divisor $a$ with $1 < a < n$, so $n = ab$ with $1 < b = n/a < n$. By the induction hypothesis, $a$ and $b$ are products of primes, and so is $n = ab$.

**Euclid's lemma.** If a prime $p$ divides $ab$, then $p \mid a$ or $p \mid b$. Proof: assume $p \nmid a$. The only positive divisors of $p$ are 1 and $p$, so $\gcd(a, p) = 1$. By Bézout's identity there are integers $x$ and $y$ with $ax + py = 1$. Multiply by $b$: $b = (ab)x + p(by)$. Both terms on the right are multiples of $p$, so $p \mid b$. By induction on the number of factors, if $p \mid c_1 c_2 \cdots c_s$, then $p \mid c_j$ for some $j$: apply the lemma to $c_1 \cdot (c_2 \cdots c_s)$.

**Uniqueness.** By strong induction on $n \ge 2$. Let $n = p_1 \cdots p_r = q_1 \cdots q_s$ with all $p_i$ and $q_j$ prime and $r, s \ge 1$.

1. $p_1$ divides $n = q_1 \cdots q_s$. By Euclid's lemma, $p_1 \mid q_j$ for some $j$.
2. The positive divisors of $q_j$ are 1 and $q_j$, and $p_1 \ge 2$, so $p_1 = q_j$. Reorder the $q$'s so that $j = 1$.
3. Cancel $p_1$: $m = n / p_1 = p_2 \cdots p_r = q_2 \cdots q_s$.
4. If $m = 1$, then $r = 1$ and $s = 1$, because a product of one or more primes is at least 2. The two factorizations are both $p_1$.
5. If $m \ge 2$, then $r \ge 2$, $s \ge 2$ and $m < n$. By the induction hypothesis, $r - 1 = s - 1$ and $q_2, \ldots, q_s$ are $p_2, \ldots, p_r$ in some order. With $p_1 = q_1$ the claim holds for $n$.

The canonical form follows: sort the primes and count each one. Two canonical forms of $n$ give two prime factorizations, which by uniqueness have the same primes with the same multiplicities. $\blacksquare$

**A proof without Bézout.** Uniqueness also follows from a least counterexample, with no use of Bézout's identity. Let $n$ be the least integer with two different factorizations $n = p_1 \cdots p_r = q_1 \cdots q_s$, each sorted so that $p_1$ and $q_1$ are the least primes of each side. No $p_i$ equals a $q_j$, or we could cancel it and get a smaller counterexample. So $p_1 \ne q_1$, say $p_1 < q_1$. Also $r, s \ge 2$: if $r = 1$, then $n = p_1$ is prime, its only factor $q_1 \ge 2$ must be $n$, and then $q_1 = p_1$. So $p_1^2 \le n$ and $q_1^2 \le n$, and $p_1 q_1 < q_1^2 \le n$. Let $N = n - p_1 q_1$. Then $0 < N < n$, and $p_1 \mid N$ and $q_1 \mid N$, so $N \ge 2$. By the choice of $n$, $N$ has only one factorization. Writing $N = p_1 \cdot (N/p_1)$ and factoring $N/p_1$ gives a factorization that contains $p_1$, and in the same way one that contains $q_1$; since they are the same, it contains both, so $p_1 q_1 \mid N$, hence $p_1 q_1 \mid n$ and $q_1 \mid n/p_1$. Then $n/p_1 < n$ has a factorization that contains $q_1$, and also the factorization $p_2 \cdots p_r$, which does not. This contradicts the choice of $n$.

## Consequences

- **Gcd and lcm from exponents.** For positive $a$ and $b$, $v_p(\gcd(a, b)) = \min(v_p(a), v_p(b))$ and $v_p(\operatorname{lcm}(a, b)) = \max(v_p(a), v_p(b))$. Since $\min + \max$ is the sum, this proves the [GCD and LCM identity](/gcd-lcm-identity/).
- **Divisors.** The positive divisors of $n = \prod p_i^{a_i}$ are exactly the numbers $\prod p_i^{b_i}$ with $0 \le b_i \le a_i$. So $n$ has $\prod (a_i + 1)$ divisors, the [divisor function](/divisor-function/) $d(n)$. For $360 = 2^3 \cdot 3^2 \cdot 5$ this is $4 \cdot 3 \cdot 2 = 24$. [Enumerating divisors](/enumerating-divisors/) from a factorization uses this form.
- **Multiplicative functions.** A [multiplicative function](/multiplicative-function/) is fixed by its values on prime powers, because the canonical form splits $n$ into coprime prime powers. The [Möbius function](/mobius-function/) and Euler's totient are defined or computed this way.
- **Valuations of products.** $v_p(ab) = v_p(a) + v_p(b)$. [Legendre's formula](/legendre-formula/) computes $v_p(n!)$ from this.
- **Irrationality.** If $\sqrt{2} = a/b$, then $a^2 = 2b^2$, but $v_2(a^2)$ is even and $v_2(2b^2)$ is odd. The same argument shows that $\sqrt{n}$ is irrational unless $n$ is a perfect square.
- **Computation.** The theorem guarantees one answer to the factoring problem, but not a fast way to find it. [Trial division](/trial-division/) uses $O(n^{1/2})$ divisions in the worst case; the best known classical algorithms are subexponential in the number of digits. The [Euclidean algorithm](/euclidean-algorithm/) finds the gcd without any factoring.

Examples of canonical forms: $360 = 2^3 \cdot 3^2 \cdot 5$; $1001 = 7 \cdot 11 \cdot 13$; $1024 = 2^{10}$; $600851475143 = 71 \cdot 839 \cdot 1471 \cdot 6857$; $2^{32} + 1 = 641 \cdot 6700417$.

## Tightness

The proof of uniqueness uses Euclid's lemma, and the lemma uses division with remainder, which works in $\mathbb{Z}$. In number systems without it, factorizations into pieces that do not split further can exist without being unique.

- **Hilbert numbers.** In the set $\{1, 5, 9, 13, \ldots\}$ of positive integers $\equiv 1 \pmod 4$, which is closed under multiplication, call an element irreducible if it is not a product of two smaller elements of the set greater than 1. Then 9, 21, 33 and 77 are irreducible, because their factors in $\mathbb{Z}$ (3, 7 and 11) are $\equiv 3 \pmod 4$. But $693 = 9 \cdot 77 = 21 \cdot 33$ has two different factorizations.
- **The ring $\mathbb{Z}[\sqrt{-5}]$.** Here $6 = 2 \cdot 3 = (1 + \sqrt{-5})(1 - \sqrt{-5})$. With the norm $N(x + y\sqrt{-5}) = x^2 + 5y^2$, which is multiplicative, the four factors have norms 4, 9, 6 and 6. No element has norm 2 or 3, so none of the four factors splits further, and the two factorizations are different.

Every [Euclidean domain](/euclidean-domain/), such as the Gaussian integers or the polynomials over a field, has unique factorization by the same proof, up to the order and up to unit factors.

## History

Euclid's Elements contains the key steps: Book VII, Proposition 30 is Euclid's lemma, Propositions 31 and 32 show that each number has a prime divisor, and Book IX, Proposition 14 gives a form of uniqueness for products of distinct primes. Euclid does not state the full theorem. The first clear statement with a proof of uniqueness is usually credited to Gauss, in Article 16 of the Disquisitiones Arithmeticae (1801). Hardy and Wright state the theorem as their Theorem 2 in Section 1.3 and prove it in Sections 2.10 and 2.11.

## References
