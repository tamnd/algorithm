---
tag: DNQS3X
kind: abstract-type
slug: polynomial
name: Polynomial
aliases:
- Polynomial (abstract type)
- multivariate polynomial
- polynomial ADT
area: algebra/polynomial-arithmetic
level: intro
summary: Finite formal sum of monomials with coefficients in a ring; the object every algorithm in this area manipulates.
prereqs: [asymptotic-notation]
see_also: [dense-polynomial-representation, point-value-representation, sparse-polynomial-representation, polynomial-ring, polynomial-degree, horner-rule, monic-polynomial, straight-line-program]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 2.2, Representation and addition of polynomials; Section 2.3, Multiplication; Section 2.4, Division with remainder; Section 8.3, Schonhage and Strassen's multiplication algorithm; Section 25.3, Polynomials and fields
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6, Polynomial arithmetic (the introduction, on polynomials over a commutative ring as formal sums), and Section 4.6.4, Evaluation of polynomials
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Polynomials and the FFT, Section 30.1, Representing polynomials
  - book: isbn:9783540605829
    title: Peter Burgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer, 1997
    locator: Chapter 2, Efficient polynomial arithmetic; Chapter 4, Models of computation; Chapter 8, The degree bound; Part IV, Low degree (multiplicative and bilinear complexity)
  - paper: arXiv:cs/0301016
    title: Peter Burgisser and Martin Lotz, Lower bounds on the bounded coefficient complexity of bilinear maps, Journal of the ACM 51(3) (2004), preprint on arXiv
    locator: pages 464 to 482 (an Omega(n log n) bound for polynomial multiplication by bounded coefficient circuits over the complex numbers)
  - paper: doi:10.1007/BF01178683
    title: David G. Cantor and Erich Kaltofen, On fast multiplication of polynomials over arbitrary algebras, Acta Informatica 28(7) (1991)
    locator: pages 693 to 701 (the bound O(n log n loglog n) for multiplication over any algebra)
---

A polynomial in one variable $x$ over a commutative ring $R$ is a finite formal sum $f = \sum_{i=0}^{n} f_i x^i$ with coefficients $f_i \in R$. The abstract type *polynomial* has the values $R[x]$ and the operations of a ring (addition, negation, multiplication), together with the degree, the coefficients, evaluation at a point and, when the divisor allows it, division with remainder. Every algorithm of this area works on this type, and their costs are all stated in one unit: the number of operations in $R$.

## In plain words

A polynomial is a list of numbers, the coefficients, together with rules for adding and multiplying two such lists. To add, you add the coefficients in the same position. To multiply, you multiply each coefficient of the first list by each coefficient of the second, and you add each product into the position given by the sum of the two positions. The numbers can be whole numbers, fractions, or remainders modulo a prime: any number system where addition and multiplication follow the usual rules.

A polynomial is not the same as the function that it computes. Two different lists can give the same value at every point when the number system is finite. So a program compares two polynomials by their coefficients, not by their values. The cost of an algorithm here is the number of additions and multiplications of coefficients that it does.

## Operations

**Notation used on all pages of this area.** $R$ is a commutative ring with $1$. When an algorithm divides by coefficients, the page says that $R$ must be a field, written $F$. A polynomial is $f = \sum_{i \ge 0} f_i x^i$ with only finitely many $f_i \ne 0$. Its [degree](/polynomial-degree/) $\deg f$ is the largest $i$ with $f_i \ne 0$, and $\deg 0 = -\infty$. Its leading coefficient is $\operatorname{lc}(f) = f_{\deg f}$, with $\operatorname{lc}(0) = 0$. A polynomial of degree less than $n$ has at most $n$ coefficients, and $n$ is the size of the input. $\mathsf{M}(n)$ is the number of ring operations that some fixed algorithm uses to multiply two polynomials of degree less than $n$. Unless a page says otherwise, costs are in the **algebraic complexity model**: each addition, subtraction, multiplication and test for zero in $R$ costs one unit, and so does each division in a field. This is the model of a [machine over the ring $R$](/blum-shub-smale-machine/). It does not count the size of the coefficients, so a bound in it is a bound in time only when the coefficients have bounded size, for example in $\mathbb{Z}/p\mathbb{Z}$ with $p$ less than a machine word.

The operations of the type are listed below. The costs are those of the [dense representation](/dense-polynomial-representation/), for operands of degree less than $n$.

| operation | signature | what it returns | cost |
|---|---|---|---|
| `zero`, `one` | $() \to f$ | the polynomials $0$ and $1$ | $O(1)$ |
| `monomial` | $(c, k) \to f$ | $c x^k$ for $c \in R$, $k \ge 0$ | $O(k)$ |
| `coeff` | $(f, i) \to R$ | $f_i$, which is $0$ for $i > \deg f$ | $O(1)$ |
| `degree` | $f \to \mathbb{N} \cup \{-\infty\}$ | $\deg f$ | $O(1)$ |
| `lc` | $f \to R$ | $\operatorname{lc}(f)$ | $O(1)$ |
| `add`, `sub` | $(f, g) \to h$ | $f + g$ and $f - g$, coefficient by coefficient | $n$ additions |
| `scale` | $(c, f) \to h$ | $c f$ | $n$ multiplications |
| `mul` | $(f, g) \to h$ | $f g$, with $h_k = \sum_{i + j = k} f_i g_j$ | $\mathsf{M}(n)$ |
| `eval` | $(f, a) \to R$ | $f(a) = \sum_i f_i a^i$ | $2n$ with [Horner's rule](/horner-rule/) |
| `divmod` | $(f, g) \to (q, r)$ | for $\operatorname{lc}(g)$ a unit: $f = q g + r$ with $\deg r < \deg g$ | $O(\mathsf{M}(n))$ |
| `derivative` | $f \to f'$ | $\sum_{i \ge 1} i f_i x^{i-1}$ | $n$ multiplications |
| `compose` | $(f, g) \to h$ | $f(g(x))$ | see [polynomial composition](/polynomial-composition/) |
| `equal` | $(f, g) \to$ bool | true when $f_i = g_i$ for each $i$ | $n$ tests |

Known values of $\mathsf{M}(n)$: the schoolbook product uses $n^2$ multiplications and $(n-1)^2$ additions, so $\mathsf{M}(n) \le 2n^2$. [Karatsuba's method](/karatsuba-multiplication/) gives $\mathsf{M}(n) = O(n^{\log_2 3})$ over every commutative ring. [FFT-based multiplication](/fft-polynomial-multiplication/) gives $O(n \log n)$ when $R$ has suitable [roots of unity](/roots-of-unity/), and the method of Schonhage and Strassen (von zur Gathen and Gerhard, Section 8.3), in the general form of Cantor and Kaltofen (1991), gives $O(n \log n \log\log n)$ over every commutative ring. The pages of this area use only that $\mathsf{M}(n) \ge n$ and that $\mathsf{M}(n)/n$ does not decrease, which hold for all of these.

**Several variables.** A polynomial in $x_1, \ldots, x_k$ is a finite sum of terms $c\, x_1^{e_1} \cdots x_k^{e_k}$, a coefficient times a monomial. The ring $R[x_1, \ldots, x_k]$ is the same as $R[x_1, \ldots, x_{k-1}][x_k]$, polynomials in $x_k$ whose coefficients are polynomials in the other variables. So each operation above works in several variables by recursion on the number of variables, and [Kronecker substitution](/kronecker-substitution/) maps a product in several variables to a product in one. The [sparse representation](/sparse-polynomial-representation/) is the usual one in several variables, because most of the possible monomials are absent.

## Laws

Every implementation satisfies these equations, for all $f, g, h \in R[x]$ and $a \in R$.

- **Ring laws.** $R[x]$ with `add` and `mul` is a commutative ring with zero $0$ and one $1$: addition and multiplication are associative and commutative, $f + 0 = f$, $f + (-f) = 0$, $1 \cdot f = f$, and $f(g + h) = fg + fh$.
- **Equality is by coefficients.** $f = g$ exactly when $f_i = g_i$ for each $i \ge 0$. A representation that stores leading zeros must remove them before it compares.
- **Degree of a sum.** $\deg(f + g) \le \max(\deg f, \deg g)$, with equality when $\deg f \ne \deg g$.
- **Degree of a product.** $\deg(fg) \le \deg f + \deg g$, with equality exactly when $\operatorname{lc}(f)\operatorname{lc}(g) \ne 0$. Then $\operatorname{lc}(fg) = \operatorname{lc}(f)\operatorname{lc}(g)$. Equality always holds when $R$ is an integral domain, and then $R[x]$ is also an integral domain.
- **Evaluation is a homomorphism.** $(f + g)(a) = f(a) + g(a)$, $(fg)(a) = f(a)\,g(a)$, and $1(a) = 1$. This needs $R$ commutative.
- **Division with remainder.** If $\operatorname{lc}(g)$ is a unit of $R$, there is exactly one pair $(q, r)$ with $f = qg + r$ and $\deg r < \deg g$. Over a field this holds for every $g \ne 0$.
- **Derivative.** $(f + g)' = f' + g'$, $(fg)' = f'g + fg'$, and $(cf)' = c f'$ for $c \in R$.
- **Composition.** $(f \circ g)(a) = f(g(a))$. Over an integral domain, $\deg(f \circ g) = \deg f \cdot \deg g$ when $\deg g \ge 1$.

The product law gives the degree of a product: if $f_n g_m \ne 0$, the coefficient of $x^{n+m}$ in $fg$ is $\sum_{i + j = n + m} f_i g_j = f_n g_m$, because each other pair has $i > n$ or $j > m$, and the coefficients of higher powers are sums of such pairs only, so they are $0$. Uniqueness of division: if $qg + r = q'g + r'$, then $(q - q')g = r' - r$. When $q \ne q'$, the left side has degree $\deg(q - q') + \deg g \ge \deg g$, because $\operatorname{lc}(g)$ is a unit and so not a zero divisor, while the right side has degree less than $\deg g$. So $q = q'$ and $r = r'$.

**Examples.** Over $\mathbb{Z}$, $(1 + x + 3x^3)(2 - x) = 2 + x - x^2 + 6x^3 - 3x^4$, of degree $3 + 1$, and $f = 2x^3 - 6x^2 + 2x - 1$ has $f(3) = 5$. Over $\mathbb{Z}/4\mathbb{Z}$, $(2x)(2x) = 0$ and $(2x + 1)^2 = 4x^2 + 4x + 1 = 1$: the degree of a product falls when the leading coefficients multiply to zero, and $2x + 1$ is a unit of degree 1. Over $\mathbb{Z}/2\mathbb{Z}$, the polynomial $x^2 + x$ is not zero, but its value is $0$ at both points $0$ and $1$ of the ring. A polynomial over a finite ring is therefore not determined by its function.

## Implementations

| implementation | stores | add | mul | eval at one point | notes |
|---|---|---|---|---|---|
| [dense representation](/dense-polynomial-representation/) | all $n$ coefficients | $n$ | $\mathsf{M}(n)$ | $2n$ | the default in one variable; also [dense polynomial](/dense-polynomial/) |
| [sparse representation](/sparse-polynomial-representation/) | the $t$ nonzero terms | $O(t \log t)$ comparisons, $t$ additions | $O(t_1 t_2)$ products | $O(t \log n)$ | for few terms of high degree, and in several variables |
| [point-value representation](/point-value-representation/) | values at $n$ fixed points | $n$ | $n$, for degree of the product less than $n$ | interpolation first | needs distinct points with invertible differences |
| [straight-line program](/straight-line-program/) | a sequence of ring operations | $O(1)$ | $O(1)$ | the length of the program | very compact for some polynomials; testing for zero is hard |

The dense representation is the reference for all costs of this area. The point-value representation makes `mul` linear but makes `coeff` and `degree` need an interpolation. A straight-line program can store $(1 + x)^{2^k}$ with $k$ squarings although it has $2^k + 1$ coefficients.

## Lower bounds

All bounds here are in the algebraic model, where a computation is a [straight-line program](/straight-line-program/) of ring operations.

- **Addition.** For $f, g$ with indeterminate coefficients, each output coefficient $f_i + g_i$ is a different sum of two inputs, so $n$ additions are necessary and sufficient.
- **Evaluation at one point.** A general polynomial of degree $n$ needs $n$ multiplications and $n$ additions, so Horner's rule is optimal. Ostrowski (1954) asked the question, and Pan (1966) proved the bound for multiplications; the sources differ on who first proved the bound for additions. The page [optimality of Horner's rule](/horners-rule-optimality/) gives the precise statements. With preprocessing of the coefficients the number of multiplications falls to about $n/2$.
- **Multiplication.** Over an infinite field, the product of two polynomials of degree less than $n$ needs $2n - 1$ nonscalar multiplications, and evaluation at $2n - 1$ points followed by interpolation reaches this bound (Burgisser, Clausen and Shokrollahi, Part IV, Low degree). No lower bound of more than a constant times $n$ is known for the total number of operations in the general model. For circuits over $\mathbb{C}$ whose constants have absolute value at most $1$, Burgisser and Lotz (2004) proved an $\Omega(n \log n)$ bound, which matches the FFT.
- **Many points.** Strassen's degree bound gives $\Omega(n \log n)$ multiplications for the evaluation of a general polynomial of degree $n$ at $n$ general points over $\mathbb{C}$ (Burgisser, Clausen and Shokrollahi, Chapter 8). So [fast multipoint evaluation](/fast-multipoint-evaluation/) is optimal up to a factor of $\log n$ when $\mathsf{M}(n) = O(n \log n)$.

## References
