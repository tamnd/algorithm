---
tag: 5Q7QV8
kind: problem
slug: polynomial-factorization-over-integers
name: Polynomial factorization over the integers
aliases:
- factoring over Z
- factoring over Q
- factoring polynomials with rational coefficients
area: algebra/polynomial-arithmetic
level: advanced
summary: Factor an integer polynomial into its content and irreducible primitive integer polynomials. It is solvable in polynomial time by lattice reduction.
model: multitape-turing-machine
complexity:
  vars: {n: the degree of f, L: the length in binary digits of the largest coefficient of f}
  time: {worst: O(n^12 + n^9 L^3)}
prereqs: [polynomial-factorization-over-finite-fields, gauss-lemma, primitive-polynomial]
see_also: [zassenhaus-algorithm, hensel-lifting, lll-algorithm, polynomial-factorization-over-finite-fields, square-free-factorization, gauss-lemma, kronecker-factorization-method, polynomial-irreducibility-testing]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 15, Hensel lifting and factoring polynomials; Chapter 16, Short vectors in lattices (factoring in Q[x] in polynomial time); Section 6.6 for Mignotte's factor bound
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of Polynomials (factoring over the integers)
  - paper: doi:10.1016/0022-314X(69)90047-X
    title: Hans Zassenhaus, On Hensel factorization I, Journal of Number Theory 1(3), 1969
    locator: pp. 291 to 311
  - paper: doi:10.1007/BF01457454
    title: Arjen K. Lenstra, Hendrik W. Lenstra Jr. and László Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261(4), 1982
    locator: pp. 515 to 534
  - paper: doi:10.1006/jnth.2001.2763
    title: Mark van Hoeij, Factoring polynomials and the knapsack problem, Journal of Number Theory 95(2), 2002
    locator: pp. 167 to 189
  - paper: doi:10.1145/800205.806338
    title: Barry M. Trager, Algebraic factoring and rational function integration, SYMSAC 1976
    locator: pp. 219 to 226
---

Factoring over the integers writes a nonzero $f \in \mathbb{Z}[x]$ as $f = \pm\operatorname{cont}(f) \cdot g_1^{e_1} \cdots g_s^{e_s}$, with distinct irreducible [primitive](/primitive-polynomial/) polynomials $g_i$. By [Gauss's lemma](/gauss-lemma/) this is the same as factoring over $\mathbb{Q}$, up to constants. The practical method is the [Zassenhaus algorithm](/zassenhaus-algorithm/): factor modulo a prime, lift with [Hensel lifting](/hensel-lifting/), and recombine. Lenstra, Lenstra and Lovász (1982) showed with lattice reduction that the problem is solvable in polynomial time.

## In plain words

A polynomial with whole-number coefficients can often be written as a product of smaller ones with whole-number coefficients. The task is to find the pieces that cannot be split further. A common whole-number factor of all coefficients is kept apart, because splitting a whole number into primes is a different and harder task.

The usual method does not search over whole numbers directly. It splits the polynomial modulo a small prime, where splitting is easy, then makes those pieces exact modulo a very large power of the prime, and then puts pieces together until their products are true factors. A different method uses short vectors in lattices, and it is fast even in the worst case.

## Definition

Let $f \in \mathbb{Z}[x]$ be nonzero of degree $n$. Its *content* $\operatorname{cont}(f)$ is the gcd of its coefficients, and $\operatorname{pp}(f) = f / \operatorname{cont}(f)$ is its primitive part, as on the [primitive polynomial](/primitive-polynomial/) page.

**Problem.** Find a sign $\varepsilon = \pm 1$, distinct irreducible primitive $g_1, \ldots, g_s \in \mathbb{Z}[x]$ of degree at least $1$ with positive leading coefficients, and integers $e_i \ge 1$, such that

$$f = \varepsilon \operatorname{cont}(f) \prod_{i=1}^{s} g_i^{\,e_i}.$$

The factorization exists and is unique up to order, since $\mathbb{Z}[x]$ is a unique factorization domain. A complete factorization in $\mathbb{Z}[x]$ also splits $\operatorname{cont}(f)$ into primes, but that is [integer factorization](/integer-factorization/), for which no polynomial-time algorithm is known; the standard problem leaves the content as a number.

**Over $\mathbb{Q}$.** For $f \in \mathbb{Q}[x]$, multiply by a common denominator. The factorization over $\mathbb{Q}$ is $f = c \prod g_i^{e_i}$ with $c \in \mathbb{Q}$ and the same $g_i$, by Gauss's lemma: a primitive polynomial is irreducible in $\mathbb{Z}[x]$ exactly when it is irreducible in $\mathbb{Q}[x]$.

**Cost model.** Coefficients grow, so costs count bit operations, as on a [multitape Turing machine](/multitape-turing-machine/). The input size is $n$ and the length $L$ of the largest coefficient in binary digits.

## Variants

- **Irreducibility testing** only asks whether $s = 1$ and $e_1 = 1$; see [irreducibility testing](/polynomial-irreducibility-testing/).
- **Square-free input.** After removing the content and taking a [square-free factorization](/square-free-factorization/), each part is square-free, and the algorithms factor each part.
- **Number fields.** Factor over $\mathbb{Q}(\alpha)$. Trager (1976) reduces this to factoring the norm of $f(x - c\alpha)$ over $\mathbb{Q}$ for a suitable integer $c$.
- **Multivariate polynomials.** Over $\mathbb{Z}$ they are factored by substituting values for all variables but one, factoring the univariate image, and lifting; this is a separate problem.
- **Sparse polynomials.** For polynomials given by few terms of very high degree, finding factors of low degree has special algorithms; the dense methods here would be exponential in the input size.

## Examples

The implementation of the [Zassenhaus algorithm](/zassenhaus-algorithm/) checked every factorization below.

- $x^6 - 1 = (x - 1)(x + 1)(x^2 + x + 1)(x^2 - x + 1)$, the product of the cyclotomic polynomials $\Phi_1, \Phi_2, \Phi_3, \Phi_6$.
- $24x^3 + 16x^2 - 6x - 4 = 2 \cdot (2x - 1)(2x + 1)(3x + 2)$. The content is $2$. Over $\mathbb{Q}$ the same factorization reads $24 (x - \tfrac12)(x + \tfrac12)(x + \tfrac23)$.
- $x^4 - x^2 - 2 = (x^2 - 2)(x^2 + 1)$. Modulo $5$ it has three factors, $(x + 2)(x + 3)(x^2 + 3)$, and the recombination puts $x + 2$ and $x + 3$ together.
- $x^4 + 1$, $x^4 - x^2 + 1$ and $x^8 + 2$ are irreducible. The first two split modulo every prime, so no single prime proves them irreducible.
- **Factors can have larger coefficients than the input.** All coefficients of $x^{105} - 1$ are $0$ or $\pm 1$, but its factor $\Phi_{105}$, of degree $48$, has a coefficient $-2$. So factor coefficients need a bound such as Mignotte's, not the coefficients of $f$.

## Known algorithms

- **[Kronecker's method](/kronecker-factorization-method/).** A factor of degree at most $n/2$ is fixed by its values at $n/2 + 1$ integer points, and these values divide the values of $f$. Try all choices of divisors and interpolate. It is finite and simple, but exponential in $n$; Knuth, Section 4.6.2, discusses it.
- **[Zassenhaus algorithm](/zassenhaus-algorithm/)** (1969). Factor modulo a small prime with [Berlekamp's](/berlekamp-factorization/) or the [Cantor-Zassenhaus](/cantor-zassenhaus-algorithm/) algorithm, Hensel lift to $p^k$ above twice a bound on the coefficients of factors, and test products of subsets. Polynomial except for the recombination, which can try about $2^r$ subsets for $r$ factors modulo $p$.
- **Lenstra, Lenstra and Lovász** (1982). After lifting one modular factor, find the true factor that it divides as a short vector in a lattice, with the [LLL algorithm](/lll-algorithm/). This is the first algorithm with a polynomial worst case.
- **Van Hoeij** (2002). Keep the Zassenhaus framework, but solve the recombination as a knapsack-type problem with lattice reduction on traces of the modular factors. It is much faster in practice than the earlier lattice method and avoids the exponential search; modern computer algebra systems use methods of this kind.

## Bounds

- **Polynomial time.** Lenstra, Lenstra and Lovász (1982) give $O(n^{12} + n^9 L^3)$ bit operations with schoolbook integer arithmetic. This is proved. Later lattice methods have better proved bounds.
- **Zassenhaus.** $O(r\, 2^r n^2 (n + L)^2 + r\, n^2 (n + L)^3)$ expected bit operations for the implementation on its page, exponential in $r$ in the worst case. The worst case occurs: the Swinnerton-Dyer polynomials of degree $n = 2^m$ are irreducible, but have at least $n/2$ factors modulo every prime.
- **Factor coefficients.** If $h$ divides $f$ in $\mathbb{Z}[x]$ and $\deg h = m$, then $\|h\|_\infty \le \|h\|_1 \le 2^m \|f\|_2$. This Mignotte bound makes Hensel lifting finite; the proof is on the [Zassenhaus algorithm](/zassenhaus-algorithm/) page.
- **Lower bound.** $\Omega(n L)$, the input size. No better general lower bound is known.

## Reductions

- **From $\mathbb{Q}$ to $\mathbb{Z}$,** by clearing denominators, and from $\mathbb{Z}$ to primitive square-free polynomials, by the content and the square-free factorization.
- **To factoring over a finite field.** The Zassenhaus algorithm and its successors start from a factorization modulo $p$, see [factorization over finite fields](/polynomial-factorization-over-finite-fields/), and lift it.
- **Number fields to $\mathbb{Q}$,** by Trager's norm method.
- **Integer factorization is not part of it.** Factoring polynomials over $\mathbb{Q}$ is in polynomial time, while factoring the content is integer factorization; the two problems are separate.

## Applications

- **Computer algebra.** Simplifying expressions, solving polynomial equations exactly, and partial fraction decomposition.
- **Algebraic numbers.** Finding minimal polynomials and working in number fields.
- **Symbolic integration.** Factoring denominators of rational functions, after the [square-free factorization](/square-free-factorization/).
- **Lattice methods.** The 1982 paper on factoring is where the [LLL algorithm](/lll-algorithm/) first appeared, and the algorithm is now used widely in cryptanalysis and number theory.

## References
