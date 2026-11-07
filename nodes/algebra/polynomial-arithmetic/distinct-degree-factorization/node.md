---
tag: 9GANAE
kind: algorithm
slug: distinct-degree-factorization
name: Distinct-degree factorization
aliases:
- DDF
- distinct degree factorization
area: algebra/polynomial-arithmetic
level: advanced
summary: Groups the irreducible factors of a square-free polynomial by degree using gcds with x^(p^d) - x.
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of f, p: the size of the prime field, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(n M(n) log(n p)), best: O(M(n) log(n p))}
  space: {extra: O(n)}
  frobenius_steps: {worst: n/2}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1981
  people: [David G. Cantor, Hans Zassenhaus]
  note: The gcd of f with x^(p^i) - x was used to group factors by degree before 1981; Cantor and Zassenhaus made it the first stage of their factoring algorithm, and later work by von zur Gathen, Kaltofen, Shoup, Kedlaya and Umans made it faster.
prereqs: [irreducible-polynomial, square-free-factorization, polynomial-gcd, binary-exponentiation, fermat-little-theorem]
see_also: [equal-degree-factorization, cantor-zassenhaus-algorithm, berlekamp-factorization, polynomial-factorization-over-finite-fields, rabin-irreducibility-test, polynomial-irreducibility-testing, brent-kung-composition, yun-square-free-factorization]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 14.2, Distinct-degree factorization; Section 14.7, The iterated Frobenius algorithm
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.4.3, Distinct degree factorization
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 20.4, Factoring polynomials, the Cantor-Zassenhaus algorithm (the distinct degree stage)
  - paper: doi:10.1090/S0025-5718-1981-0606517-5
    title: David G. Cantor and Hans Zassenhaus, A new algorithm for factoring polynomials over finite fields, Mathematics of Computation 36(154), 587-592, 1981
    locator: the separation of the factors by degree before the random splitting
---

Distinct-degree factorization splits a square-free polynomial $f$ over a prime field $\mathbb{F}_p$ into parts $g_1, g_2, \ldots$, where $g_i$ is the product of all irreducible factors of $f$ of degree $i$. It uses one fact: $x^{p^i} - x$ is the product of all monic irreducible polynomials whose degree divides $i$. So a gcd with $x^{p^i} - x$, after the factors of smaller degree have been removed, collects exactly the factors of degree $i$. It is the first stage of the [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/); the second stage, [equal-degree factorization](/equal-degree-factorization/), splits each $g_i$.

Notation: $p$ is a prime and $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$. The polynomial $f \in \mathbb{F}_p[x]$ is monic and square-free, of degree $n$. The algorithm uses arithmetic modulo $f$ in $\mathbb{F}_p[x]$, so $\mathbb{F}_p$ must be a field. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$. Costs count operations in $\mathbb{F}_p$ in the algebraic complexity model.

## In plain words

Over a finite field, every polynomial breaks into pieces that cannot be broken further, and these pieces can have different sizes. This method sorts the pieces by size without finding them one by one. It uses a special polynomial for each size that contains every piece of that size, and of the sizes that divide it, exactly once. Taking the common part of this special polynomial and the input picks out all pieces of the given size together. The method starts with size one, removes what it found, and goes up one size at a time until what is left must be a single piece.

## The problem

**Input:** a prime $p$ and a monic square-free $f \in \mathbb{F}_p[x]$ of degree $n$.

**Output:** the pairs $(g_i, i)$ with $g_i \ne 1$, where $g_i$ is the product of the monic irreducible factors of $f$ of degree $i$. So $f = \prod_i g_i$, and $\deg g_i$ is a multiple of $i$.

A general polynomial is first made monic and split into square-free parts by [square-free factorization](/square-free-factorization/).

## The algorithm

```pseudo id=main
DISTINCT-DEGREE(f)
L1  h ← x mod f;  r ← f;  i ← 0
L2  while deg r ≥ 2(i + 1) do
L3      i ← i + 1
L4      h ← h^p mod r                       ▷ now h ≡ x^(p^i) mod r
L5      g ← gcd(h - x, r)
L6      if g ≠ 1 then output (g, i);  r ← r / g;  h ← h mod r
L7  if deg r > 0 then output (r, deg r)       ▷ the rest is irreducible
L8  return the output list
```

Line L4 raises to the power $p$ by [binary exponentiation](/binary-exponentiation/) modulo $r$, with $O(\log p)$ multiplications. Since $h \equiv x^{p^{i-1}}$, the result is $x^{p^i}$ modulo $r$. The modulus $r$ shrinks as factors are removed, which saves work. The loop ends when $\deg r < 2(i + 1)$: every factor left has degree at least $i + 1$, so two of them would have degree at least $2(i + 1)$.

## Example

Take $p = 3$ and $f = (x + 1)(x^2 + 1)(x^3 - x + 1)(x^3 - x + 2)$, of degree $9$. The two cubics are irreducible over $\mathbb{F}_3$ because they have no root, and $x^2 + 1$ is irreducible because $-1$ is not a square modulo $3$.

| $i$ | $h = x^{3^i} \bmod r$ | $g = \gcd(h - x, r)$ | $\deg r$ after |
|---|---|---|---|
| 1 | $x^3$ | $x + 1$ | 8 |
| 2 | $x^7 + x^5 + x$ | $x^2 + 1$ | 6 |
| 3 | $x$ | $x^6 + x^4 + x^2 + 2$ | 0 |

For $i = 1$, $\gcd(x^3 - x, f)$ is the product of the linear factors, here only $x + 1$. For $i = 3$, $h - x = 0$, so the gcd is all of $r$, the product of the two cubics. The output is $(x + 1, 1)$, $(x^2 + 1, 2)$ and $(x^6 + x^4 + x^2 + 2, 3)$. A script checked every entry.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The key lemma: for a monic irreducible $q$ of degree $d$, $x^{p^i} \equiv x \pmod q$ if and only if $d \mid i$, because $\mathbb{F}_p[x]/(q)$ is a field with $p^d$ elements on which the Frobenius map $y \mapsto y^p$ has order exactly $d$. Since $x^{p^i} - x$ has derivative $-1$, it is square-free, so it is the product of the monic irreducibles of degree dividing $i$. The loop invariant is that, at line L5, $r$ is the product of the irreducible factors of $f$ of degree at least $i$ and $h \equiv x^{p^i} \pmod r$; then the gcd is the product of the factors of degree exactly $i$.

## Complexity

The bounds are proved and count operations in $\mathbb{F}_p$.

- **One iteration.** Line L4 costs $O(\log p)$ products modulo $r$, so $O(M(n) \log p)$ with fast division. Line L5 is one gcd, $O(M(n) \log n)$ with the fast Euclidean algorithm or $O(n^2)$ classically.
- **Number of iterations.** At most $n/2$, because of the test at line L2.
- **Total.** $O(n M(n) \log(n p))$, as in von zur Gathen and Gerhard, Section 14.2. With schoolbook arithmetic, as in the implementation, $O(n^3 \log p)$.
- **Best case.** If $f$ splits into linear factors, or has degree $2$ or $3$, one iteration decides everything.
- **Space.** $O(n)$ field elements.

**In practice (observed).** The powering at line L4 dominates for large $p$. For large $n$, the loop over $i$ up to $n/2$ dominates, which is why the faster methods below batch the gcds. The early exit at line L2 often stops the loop well before $n/2$, since a random polynomial has a factor of degree more than $n/2$ with probability about $\ln 2$.

## Properties

- **Deterministic.** No randomness is needed; the splitting of each $g_i$ into irreducibles is the randomized part.
- **Counts factors.** $\deg g_i / i$ is the number of irreducible factors of degree $i$. So the algorithm tells how many factors of each degree $f$ has, and whether $f$ is irreducible.
- **Needs square-free input.** A repeated factor $q^2$ with $\deg q = i$ is caught by $\gcd(x^{p^i} - x, r)$ only once, so $g_i$ would miss a copy.
- **Iterative.** No recursion.

## Variants and improvements

- **Irreducibility test.** If only irreducibility matters, [Rabin's test](/rabin-irreducibility-test/) checks $x^{p^n} \equiv x$ and the gcds for the maximal proper divisors of $n$ only.
- **Iterated Frobenius.** Von zur Gathen and Shoup compute the powers $x^{p^i} \bmod f$ by [modular composition](/brent-kung-composition/) instead of by powering, which removes the $\log p$ factor from most iterations; von zur Gathen and Gerhard, Section 14.7.
- **Baby-step giant-step.** Kaltofen and Shoup group the gcds into blocks of about $\sqrt{n}$ indices and take one gcd per block with a product of differences, which gives a total cost below $n^2$ operations for fixed $p$.
- **Fast modular composition.** With the Kedlaya-Umans method, the total cost is about $n^{1.5}$ times factors in $\log p$, the best known bound.
- **Larger fields.** Over $\mathbb{F}_q$ with $q = p^k$, replace $p$ by $q$ everywhere.

## When to use it

Use distinct-degree factorization as the first stage after square-free factorization in any factoring algorithm over a finite field, in particular before [equal-degree factorization](/equal-degree-factorization/). It is also the simple way to find the degree pattern of a polynomial modulo $p$, which [the Zassenhaus algorithm](/zassenhaus-algorithm/) uses to choose a good prime and to rule out factor degrees over $\mathbb{Z}$.

## Pitfalls

- **Not square-free.** Run square-free factorization first, or the output misses repeated factors.
- **Not reducing $h$ modulo the new $r$.** It is correct but wastes work; forgetting the division $r \leftarrow r/g$ is wrong, since later gcds would then contain factors of smaller degree.
- **Powering $x^{p^i}$ from scratch.** Compute $h \leftarrow h^p$ from the previous $h$, not $x^{p^i}$ with an exponent of $i \log_2 p$ digits each time.
- **Stopping too late.** Without the exit test at line L2, the loop runs up to $i = n$. With it, the rest is known to be irreducible as soon as $\deg r < 2(i + 1)$.

## Implementations

## History

That $x^{p^i} - x$ is the product of the irreducible polynomials of degree dividing $i$ is classical finite field theory, going back to Gauss and Galois. Grouping factors by degree with these gcds was in use before 1981. Cantor and Zassenhaus made it the first stage of their factoring algorithm in 1981, followed by equal-degree splitting. Von zur Gathen and Shoup (1992), Kaltofen and Shoup (1998), and Kedlaya and Umans (2008) made the stage faster with modular composition and baby-step giant-step methods.

## References
