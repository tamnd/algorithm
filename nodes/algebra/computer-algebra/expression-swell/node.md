---
tag: F04XNN
kind: concept
slug: expression-swell
name: Expression swell
aliases:
- intermediate expression swell
- coefficient explosion
- coefficient growth
area: algebra/computer-algebra
level: advanced
summary: Rapid growth in size of intermediate expressions during symbolic computation.
prereqs: [canonical-form, euclidean-algorithm, gaussian-elimination]
see_also: [modular-methods, bareiss-algorithm, subresultant, primitive-prs, hensel-lifting, expression-dag, hadamard-bound, groebner-basis-computation]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.6.1 (division of polynomials), the example of the Euclidean, primitive and subresultant remainder sequences for x^8 + x^6 - 3x^4 - 3x^3 + 8x^2 + 2x - 5 and 3x^6 + 5x^4 - 4x^2 - 9x + 21
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 5 (homomorphisms and Chinese remainder algorithms), Chapter 6 (Newton's iteration and the Hensel construction) and Chapter 7 (polynomial gcd computation, the growth of polynomial remainder sequences)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 5 (modular algorithms and interpolation) and Chapter 6 (the resultant and gcd computation, coefficient growth in the Euclidean algorithm over Q)
  - paper: doi:10.1090/S0025-5718-1968-0226829-0
    title: Erwin H. Bareiss, Sylvester's identity and multistep integer-preserving Gaussian elimination, Mathematics of Computation 22, 565-578, 1968
    locator: the fraction-free elimination whose intermediate entries are minors of the input
---

Expression swell is the growth of intermediate results in a symbolic computation far beyond the size of both the input and the output. A gcd of two polynomials with one-digit coefficients can be 1, yet the Euclidean algorithm over $\mathbb{Q}$ passes through remainders with numbers of dozens of digits. Elimination on an integer matrix without care doubles the length of its entries at every step. Swell is the main practical obstacle of exact computation, and much of computer algebra consists of methods that avoid it: content removal, subresultants, fraction-free elimination, [modular methods](/modular-methods/) and [Hensel lifting](/hensel-lifting/), and shared representations such as the [expression DAG](/expression-dag/).

## In plain words

When a computer works with exact numbers and formulas, it never rounds. That is the point, but it has a cost: numbers and formulas can grow at every step. A calculation that starts with small numbers and ends with a small answer can, in the middle, produce numbers with hundreds of digits, or formulas that fill pages.

This growth in the middle is called expression swell. It is not a bug in one program. It comes from the method. The cure is to choose methods that keep the middle steps small, for example by doing the work with small remainders and putting the answer together at the end.

## The idea

Measure the size of an object by the number of bits of its coefficients and the number of its terms. An algorithm has expression swell when the largest intermediate object is much larger than the input and the output together. Three sources account for most of it.

**Growth of coefficients.** Rational arithmetic adds the lengths of numerators and denominators at each product. Repeated over $k$ dependent steps, as in elimination or remainder sequences, the lengths can grow like $2^k$ unless common factors are removed.

**Growth of the number of terms.** Expanding a product or a power multiplies the number of terms. The expression $\prod_{i=1}^{n}(x_i + y_i)$ of size $\Theta(n)$ expands to $2^n$ terms; derivatives of trees without sharing grow quadratically or worse.

**Growth of degree and nesting.** Substitution and composition multiply degrees: composing a polynomial of degree $d$ with itself $k$ times gives degree $d^k$.

The remedies are of three kinds.

- *Keep the intermediate results reduced.* Remove contents and common factors, or divide by factors known in advance: the [primitive](/primitive-prs/) and [subresultant](/subresultant/) remainder sequences, and the fraction-free elimination of [Bareiss](/bareiss-algorithm/), whose entries are minors of the input and so bounded by the [Hadamard bound](/hadamard-bound/).
- *Work in small images.* Map the problem to $\mathbb{Z}/p\mathbb{Z}$ for several primes $p$, or to evaluations at points, where entries have fixed size; solve there; and recover the answer by the Chinese remainder theorem and interpolation, or by Hensel lifting from one prime. Then the cost depends on the size of the *output*, not of the intermediate results. These are the [modular methods](/modular-methods/).
- *Share instead of copying.* Represent expressions as [DAGs](/expression-dag/) or straight-line programs, so that repeated subexpressions are stored once, and expand only at the end, if at all.

## Examples

**Euclid's algorithm over the integers.** Knuth's example (Section 4.6.1) takes

$$a = x^8 + x^6 - 3x^4 - 3x^3 + 8x^2 + 2x - 5, \qquad b = 3x^6 + 5x^4 - 4x^2 - 9x + 21,$$

which are coprime, so the gcd is 1. Compute the remainder sequence by [pseudo-division](/pseudo-division/), with no removal of common factors. A short script, run in exact integer arithmetic, gave these largest coefficient sizes:

| remainder | degree | largest coefficient, decimal digits |
|---|---|---|
| 1 | 4 | 2 |
| 2 | 2 | 5 |
| 3 | 1 | 16 |
| 4 | 0 | 35 |

The last remainder is a 35-digit constant, for an answer of "1". The *primitive* sequence, which divides each remainder by the gcd of its coefficients, gives instead, up to sign, $5x^4 - x^2 + 3$, $13x^2 + 25x - 49$, $4663x - 6150$ and $1$. Over $\mathbb{Q}$ with monic division the coefficients are fractions such as $-102500/6591$ and $-1288744821/543589225$. The growth in the plain sequence is exponential in the number of steps; the primitive and subresultant sequences keep it polynomial, and a modular gcd avoids it entirely by computing modulo primes.

**Gaussian elimination on an integer matrix.** For a random $10 \times 10$ matrix with entries in $[-9, 9]$ (seed 1 of Python's `random`), the division-free elimination that replaces row $i$ by $a_{kk} \cdot \text{row}_i - a_{ik} \cdot \text{row}_k$ produced entries of at most 7, 13, 24, 40, 79, 153, 304, 606 and 1202 bits after steps 1 to 9: the length roughly doubles at each step. Bareiss's fraction-free elimination divides each new entry exactly by the previous pivot and stayed at 7, 11, 15, 18, 22, 25, 28, 31 and 28 bits. Its last pivot is the determinant, $-231387889$, a 28-bit number; Gaussian elimination over $\mathbb{Q}$ gives the same value. Elimination over $\mathbb{Q}$ with reduced fractions also stays polynomial, but each step pays for gcds.

**Expanding and dividing.** The quotient of $\prod_{i=1}^{100}(x - i)$ by $\prod_{i=2}^{100}(x - i)$ is $x - 1$. Computed by expanding both products and dividing, it passes through coefficients of up to 160 decimal digits (the constant term alone is $100!$, with 158 digits). Kept in factored form, the same quotient is a cancellation of common factors with no arithmetic at all.

**Derivatives.** Differentiating a chain of $N$ products as a tree that copies its subtrees gives about $N^2$ nodes; with sharing, $O(N)$. See the counts on the [expression tree](/expression-tree/) page.

**Gröbner bases.** Over $\mathbb{Q}$, Buchberger's algorithm can produce intermediate polynomials with very large coefficients even when the reduced basis is small, and the degrees can grow as well; in the worst case they are doubly exponential in the number of variables. Practical systems run the computation modulo primes and lift, or use modular tracing; see [Gröbner basis computation](/groebner-basis-computation/).

## Where it is used

- **Algorithm design.** The modular gcd algorithms of Brown and Collins, modular determinants and linear system solving, modular Gröbner bases and the [Hensel lifting](/hensel-lifting/) approach to factorization exist mainly to avoid swell.
- **Analysis of algorithms.** Bit complexity bounds in computer algebra, such as those in von zur Gathen and Gerhard, are proved by bounding the size of intermediate results; the [subresultant](/subresultant/) theory shows that the remainders of a gcd computation are, up to known factors, determinants of Sylvester-type matrices, and so bounded by the Hadamard bound.
- **Representation choices.** Systems keep expressions in factored or shared form when expansion would swell, and expand only on request. See [canonical form](/canonical-form/) for the trade-off.
- **Numerical alternatives.** When swell cannot be avoided, approximate methods with certified error bounds, such as interval arithmetic or numerical algebraic geometry, trade exactness for size.

## References
