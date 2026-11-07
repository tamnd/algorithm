---
tag: 48QJRY
kind: algorithm
slug: brent-kung-composition
name: Brent-Kung composition algorithm
aliases:
- baby-step giant-step composition
- Brent-Kung modular composition
- Brent-Kung algorithm
area: algebra/polynomial-arithmetic
level: advanced
summary: Composes polynomials in O(sqrt(n) M(n)) operations by baby-step giant-step over the Horner form.
solves: [polynomial-composition]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the modulus h, M: the cost function M(n) of multiplying two polynomials of degree less than n, ω: an exponent of matrix multiplication (2 ≤ ω ≤ 3)}
  time: {worst: O(n^(1/2) M(n) + n^((ω + 1)/2)), best: O(n^(1/2) M(n) + n^((ω + 1)/2))}
  space: {extra: Θ(n^(3/2))}
  ring_operations: {worst: O(n^(1/2) M(n) + n^2)}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1978
  people: [Richard P. Brent, H. T. Kung]
  note: Brent and Kung gave the method in 1978 in their paper on fast algorithms for formal power series, for composition of power series and of polynomials modulo a polynomial.
prereqs: [paterson-stockmeyer-algorithm, fast-polynomial-division, polynomial-composition]
see_also: [polynomial-composition, paterson-stockmeyer-algorithm, matrix-multiplication-exponent, strassen-algorithm, newton-power-series-inversion, polynomial-factorization-over-finite-fields, distinct-degree-factorization, horner-rule]
sources:
  - paper: doi:10.1145/322092.322099
    title: Richard P. Brent and H. T. Kung, Fast algorithms for manipulating formal power series, Journal of the ACM 25(4), 581-595, 1978
    locator: the composition algorithm with matrix multiplication
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 12.2 (modular composition by the Brent and Kung method)
---

The Brent-Kung algorithm computes the modular composition $f(g) \bmod h$, where $\deg h = n$ and $f$ and $g$ have degree less than $n$. It applies the [Paterson-Stockmeyer](/paterson-stockmeyer-algorithm/) splitting in the ring $R[x]/(h)$: about $\sqrt{n}$ baby steps $g^i \bmod h$, one matrix product that evaluates all blocks of $f$ at once, and about $\sqrt{n}$ giant steps by [Horner's rule](/horner-rule/) in $g^k \bmod h$. The cost is $O(\sqrt{n}\, M(n) + n^{(\omega+1)/2})$ ring operations, against $O(n\, M(n))$ for Horner's rule. Power series composition $f(g) \bmod x^n$ is the case $h = x^n$.

Notation: $R$ is a commutative ring, polynomials in $R[x]$ are lists of coefficients with the constant term first, and $h \in R[x]$ has degree $n \ge 1$ and a leading coefficient that is a unit (over a field, any nonzero $h$). $M(n)$ is the cost of multiplying two polynomials of degree less than $n$, and $\omega$ is an exponent for the product of two $r \times r$ matrices in $O(r^\omega)$ ring operations. Costs count ring operations in the algebraic complexity model.

## In plain words

To put one polynomial inside another and keep only the remainder after division by a third, the plain way is Horner's rule: about as many multiplications of large polynomials as the degree. Brent and Kung cut the outer polynomial into pieces of about the square root of the degree. First they compute that many powers of the inner polynomial, each reduced. Every piece is then a sum of these powers times numbers. All the pieces together are one product of two tables of numbers, which fast matrix methods do well. Last, Horner's rule joins the pieces, with one large power as the step. So only about twice the square root of the degree large multiplications remain.

## The problem

**Input:** polynomials $f, g, h \in R[x]$ with $\deg h = n \ge 1$, the leading coefficient of $h$ a unit, and $N$ the number of coefficients of $f$ (usually $N \le n$).

**Output:** the remainder $f(g) \bmod h$, of degree less than $n$.

This is the modular form of [polynomial composition](/polynomial-composition/). Every step works in $R[x]/(h)$, where each element has a unique representative of degree less than $n$, and the product of two of them costs one product in $R[x]$ and one division by $h$.

## The algorithm

Choose $k = \lceil \sqrt{N}\, \rceil$ and $m = \lceil N/k \rceil$, and pad $f$ with zero coefficients. Write $f = \sum_{j=0}^{m-1} F_j(y)\, y^{jk}$ with blocks $F_j = \sum_{i=0}^{k-1} f_{jk+i}\, y^i$. Then

$$f(g) \equiv \sum_{j=0}^{m-1} F_j(g)\, (g^k)^j \pmod{h},$$

and the reduced values $F_j(g) \bmod h = \sum_i f_{jk+i}\, (g^i \bmod h)$ are the rows of one matrix product: the $m \times k$ matrix of the coefficients of $f$ times the $k \times n$ matrix whose row $i$ is the coefficient vector of $g^i \bmod h$.

```pseudo id=main
BRENT-KUNG(f, g, h)                      ▷ N = number of coefficients of f, n = deg h
L1  k ← ⌈√N⌉;  m ← ⌈N/k⌉
L2  G_0 ← 1;  G_1 ← g mod h
L3  for i ← 2 to min(k, N - 1) do G_i ← G_{i-1} · G_1 mod h     ▷ baby steps
L4  A ← the m × k matrix with A[j][i] = f_{jk+i}  (0 past the end)
L5  B ← the k × n matrix whose row i is the coefficient vector of G_i
L6  C ← A · B                             ▷ row j of C is F_j(g) mod h
L7  S ← row m - 1 of C
L8  for j ← m - 2 downto 0 do
L9      S ← S · G_k mod h + row j of C    ▷ giant steps
L10 return S
```

The inverse of the reversal of $h$, which [fast polynomial division](/fast-polynomial-division/) needs, is computed once at the start and reused for every reduction modulo $h$.

## Example

Over $\mathbb{Z}$, take $f = 1 + 2y + 3y^2 + 4y^3$, $g = x + x^2$ and $h = x^4 - 2$. Then $N = 4$, $k = 2$ and $m = 2$.

| step | value |
|---|---|
| L2 | $G_0 = 1$, $G_1 = x + x^2$ |
| L3 | $G_2 = g^2 \bmod h = (x^2 + 2x^3 + x^4) \bmod h = 2 + x^2 + 2x^3$ |
| L4, L5 | $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$, rows of $B$: $(1, 0, 0, 0)$ and $(0, 1, 1, 0)$ |
| L6 | rows of $C$: $1 + 2x + 2x^2$ and $3 + 4x + 4x^2$ |
| L7 | $S = 3 + 4x + 4x^2$ |
| L9, $j = 0$ | $S \cdot G_2 \bmod h = 30 + 24x + 11x^2 + 10x^3$, plus row $0$: $31 + 26x + 13x^2 + 10x^3$ |

So $f(g) \bmod (x^4 - 2) = 31 + 26x + 13x^2 + 10x^3$, with two products modulo $h$: $G_2$ and one giant step. A script checked every row against a full expansion of $f(g)$ followed by long division.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Reduction modulo $h$ is a ring homomorphism from $R[x]$ onto $R[x]/(h)$, so it is enough to compute $f(\bar g)$ in this commutative ring, where $\bar g$ is the class of $g$. By induction $G_i$ is the representative of $\bar g^{\,i}$. Row $j$ of $A \cdot B$ is $\sum_i f_{jk+i} G_i$, a sum of polynomials of degree less than $n$, so it is the representative of $F_j(\bar g)$ with no further reduction. The loop of lines L8 and L9 is Horner's rule in $\bar g^{\,k}$, and the block identity $f(\bar g) = \sum_j F_j(\bar g)\, (\bar g^{\,k})^j$ completes the proof.

## Complexity

The bounds below are proved, in ring operations, under the usual assumption that $M(n)/n$ is nondecreasing.

- **Products modulo $h$.** Line L3 does $\min(k, N - 1) - 1$ of them and line L9 does $m - 1$, so at most $2\lceil\sqrt{N}\,\rceil - 2$. Each is a product of two polynomials of degree less than $n$ and a division of a polynomial of degree less than $2n - 1$ by $h$ with the stored inverse, at most $3M(n) + O(n)$ operations. The inverse costs $O(M(n))$ once. For $N \le n$ this is $O(\sqrt{n}\, M(n))$ in all.
- **The matrix product.** Line L6 multiplies an $m \times k$ matrix by a $k \times n$ matrix, with $m \le k \le \lceil\sqrt{n}\,\rceil$. Cut the second matrix into $\lceil n/k \rceil$ square blocks of size $k$. That is $O(\sqrt{n})$ products of $k \times k$ matrices, so $O(\sqrt{n} \cdot n^{\omega/2}) = O(n^{(\omega+1)/2})$ operations. With the schoolbook product, as in the code on this page, it is at most $k^2 n = O(n^2)$.
- **Total.** $O(\sqrt{n}\, M(n) + n^{(\omega+1)/2})$. With Strassen's $\omega = \log_2 7$ and $M(n) = O(n \log n)$, this is $O(n^{1.91})$. With the best known $\omega < 2.372$, it is $O(n^{1.69})$. The plain Horner method costs $O(n\, M(n))$.
- **Space.** The $k + 1$ baby steps take $\Theta(n^{3/2})$ ring elements.

**In practice (observed).** With schoolbook matrix products and FFT-based $M(n)$, the method is still a large gain over Horner's rule, because the $O(n^2)$ matrix step consists of plain multiply-adds with no division and runs fast. In computer algebra systems the matrix step often dominates for large $n$. Where the change from Horner's rule pays off depends on the machine and the ring.

## Properties

- **Exact.** It is an identity in $R[x]/(h)$, so it holds over every commutative ring once $h$ has a unit leading coefficient.
- **Linear in $f$.** For fixed $g$ and $h$, the map $f \mapsto f(g) \bmod h$ is $R$-linear, and the algorithm is a matrix product followed by Horner's rule. The baby steps can be reused for many $f$ with the same $g$.
- **Deterministic and iterative.** No recursion, no randomness.
- **Uses fast matrix multiplication.** It is one of the classical ways that matrix exponents below $3$ make polynomial algorithms faster.

## Variants and improvements

- **Power series.** For $h = x^n$, reduction is truncation. Brent and Kung also give a second method for power series, with about $(n \log n)^{1/2} M(n)$ operations, based on a Taylor expansion of $f$ around the low part of $g$.
- **Many outer polynomials.** If several $f$ share $g$ and $h$, stack their blocks as more rows of $A$. The matrix product grows, but the baby steps are shared.
- **Transposed version.** The transpose of the algorithm, by the transposition principle, gives the power projection problem, which is used in minimal polynomial computations.
- **Faster algorithms.** Kedlaya and Umans gave modular composition over finite fields in $n^{1+o(1)}$ bit operations up to factors in $\log q$, a different method based on multivariate evaluation. No algebraic algorithm with $n^{1+o(1)}$ ring operations is known for every field.
- **Plain composition.** Without a modulus, $f(g)$ has degree $\deg f \cdot \deg g$, and divide and conquer is better; see [polynomial composition](/polynomial-composition/).

## When to use it

Use the Brent-Kung algorithm for modular composition $f(g) \bmod h$ and for power series composition $f(g) \bmod x^n$ of large degree, in particular for the many compositions with the Frobenius map $x^q \bmod h$ in [polynomial factorization over finite fields](/polynomial-factorization-over-finite-fields/) and [distinct-degree factorization](/distinct-degree-factorization/). For small $n$, Horner's rule modulo $h$ is simpler and fast enough.

## Pitfalls

- **Reducing the rows of $C$ again.** The rows are sums of reduced polynomials and are already of degree less than $n$. A second reduction wastes time.
- **Recomputing the inverse of $h$.** Every product modulo $h$ uses the same divisor; compute the reversed inverse once.
- **Non-unit leading coefficient.** Over $\mathbb{Z}$, division by $h = 2x^2 + 1$ is not defined in $\mathbb{Z}[x]$. Use a monic $h$, or work over a field.
- **Forgetting to reduce $g$.** If $\deg g \ge n$, reduce $g$ modulo $h$ first, or the baby steps grow.
- **Memory.** The $k \times n$ matrix of baby steps has about $n^{3/2}$ entries; for very large $n$, use a smaller $k$.

## Implementations

## History

Richard Brent and H. T. Kung published the method in 1978 in the Journal of the ACM, with algorithms for composition and reversion of formal power series. They combined the baby-step giant-step splitting of Paterson and Stockmeyer with fast matrix multiplication. Von zur Gathen and Shoup used modular composition in 1992 to compute Frobenius maps for factoring over finite fields, and Kaltofen and Shoup later used it to get subquadratic factoring algorithms. In 2008, Kedlaya and Umans gave a nearly linear algorithm for modular composition over finite fields in the bit model.

## References
