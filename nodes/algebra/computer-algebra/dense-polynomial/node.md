---
tag: RVZNCP
kind: data-structure
slug: dense-polynomial
name: Dense polynomial (recursive dense representation)
aliases:
- dense univariate representation
- recursive dense representation
- dense recursive polynomial
area: algebra/computer-algebra
level: core
summary: Stores every coefficient of a univariate polynomial in an array.
implements: [polynomial]
model: blum-shub-smale-machine
complexity:
  vars: {m: the number of coefficients of the first operand, n: the number of coefficients of the second operand}
  time: {worst: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m + n)}
prereqs: [dense-polynomial-representation, polynomial-ring]
see_also: [sparse-polynomial, pseudo-division, kronecker-substitution, horner-rule, polynomial-multiplication, canonical-form, primitive-prs, subresultant]
sources:
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 3 (normal forms and algebraic representations), the recursive and distributed, dense and sparse representations of multivariate polynomials; Chapter 2 for pseudo-division
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.6.1 (division of polynomials), Algorithm R (pseudo-division of polynomials)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 2 (fundamental algorithms, representation and arithmetic of polynomials) and Section 8.4 (multivariate multiplication by Kronecker substitution)
---

The dense representation stores a polynomial in one variable $x$ over a commutative ring $R$ as the array $[a_0, a_1, \ldots, a_{m-1}]$ of all its coefficients, with $a_{m-1} \ne 0$. In computer algebra the same array also handles several variables, by recursion on the ring: a polynomial in $R[x_1, \ldots, x_n]$ is a dense polynomial in the *main variable* $x_n$ whose coefficients are dense polynomials in $R[x_1, \ldots, x_{n-1}]$. This *recursive dense* form needs nothing beyond a univariate dense type that works over any commutative ring, and it makes the main-variable operations of computer algebra, such as pseudo-division, leading coefficients and evaluation of one variable, direct. The array layout, the univariate algorithms and their proofs are on the page [dense polynomial representation](/dense-polynomial-representation/); this page is about the recursive form and the ring-generic operations it relies on.

## In plain words

A polynomial in one letter can be stored as the list of its coefficients, from the constant term up, with no zero at the top. For a polynomial in two letters, say $x$ and $y$, pick one letter, $y$, as the main one. Collect the terms by powers of $y$. Each coefficient is now a polynomial in $x$ only, and can be stored as a list in the same way. So the whole polynomial is a list of lists.

With three letters you get lists of lists of lists, and so on. Every operation is written once, for a list whose entries can be added and multiplied, and it then works at every level. The price is that every coefficient, including the zero ones in the middle, takes room.

## The abstract type

The type is the [polynomial ring](/polynomial-ring/) $R[x]$ over a commutative ring $R$, where $R$ may itself be a polynomial ring. The operations are addition, subtraction, negation, multiplication, multiplication by an element of $R$, the degree and the leading coefficient $\operatorname{LC}$ in the main variable, evaluation of the main variable at an element of $R$, the formal derivative in the main variable, and pseudo-division. Pseudo-division is the division of computer algebra over rings: given $a, b \in R[x]$ with $b \ne 0$, $\deg a = m - 1$ and $\deg b = n - 1$, it returns $q, r$ with

$$\operatorname{LC}(b)^{\max(m - n + 1, 0)}\, a = q\, b + r, \qquad \deg r < \deg b,$$

and needs no division in $R$. Conversion to and from the distributed form, a map from exponent vectors to nonzero coefficients, links the recursive form to the [sparse](/sparse-polynomial/) representations.

## Representation

A value is a pair $(c, z)$: a list $c = [c_0, \ldots, c_{m-1}]$ of elements of $R$ and the zero $z$ of $R$. The zero must be stored, because when $R$ is a polynomial ring, its zero is itself a list. The value is $\sum_i c_i x^i$.

> **(N)** At every level, the last entry of the list is not the zero of its ring, and all entries of one list belong to the same ring.

As on the univariate page, (N) gives a unique list for each polynomial, so the representation is a [canonical form](/canonical-form/): equality is equality of nested lists. For $n$ variables the nesting depth is $n$.

**Example of the layout.** In $\mathbb{Q}[x][y]$, with $y$ the main variable,

$$f = (x^2 + 1)\, y^2 + 3x \quad\text{is stored as}\quad [\,[0, 3],\ [\,],\ [1, 0, 1]\,].$$

The coefficient of $y^0$ is $3x$, stored as $[0, 3]$; the coefficient of $y^1$ is the zero polynomial, the empty list; the coefficient of $y^2$ is $x^2 + 1$. The degree of $f$ in $y$ is 2 and $\operatorname{LC}_y(f) = x^2 + 1$, a polynomial, read off in $O(1)$.

## Operations

The main block holds addition, multiplication and normalization, written over a general ring $R$, and pseudo-division. Each $+$ or $\cdot$ of two coefficients is an operation in $R$; when $R$ is a polynomial ring, it runs the same code one level down.

```pseudo id=main
ADD(a, b)                                  ▷ m = |a|, n = |b|; missing entries are 0 of R
L1  c ← the list with c[i] ← a[i] + b[i] for 0 ≤ i < max(m, n)
L2  return NORMALIZE(c)

MUL(a, b)
L3  if m = 0 or n = 0 then return [ ]
L4  c ← a list of m + n − 1 zeros of R
L5  for i ← 0 to m − 1, for j ← 0 to n − 1 do c[i + j] ← c[i + j] + a[i] · b[j]
L6  return NORMALIZE(c)

NORMALIZE(c)
L7  while c is not empty and the last entry of c is the zero of R do remove it
L8  return c

PSEUDO-DIVMOD(a, b)                        ▷ b ≠ 0; R any commutative ring
L9  r ← a; q ← [ ]; ℓ ← LC(b); e ← max(m − n + 1, 0)
L10 while deg r ≥ deg b do
L11     t ← LC(r) · x^(deg r − deg b)
L12     q ← ℓ · q + t; r ← ℓ · r − t · b
L13     e ← e − 1
L14 return (ℓ^e · q, ℓ^e · r)
```

In line L12 the top coefficient of $\ell r - t b$ is $\ell \operatorname{LC}(r) - \operatorname{LC}(r) \ell = 0$, so the degree of $r$ falls by at least one in each pass; the loop runs at most $m - n + 1$ times, and $e$ ends at zero or above. Line L14 brings the multiplier to exactly $\ell^{m-n+1}$, which makes the result unique.

The other operations are short. Negation and scaling act entry by entry and normalize. EVALUATE$(a, u)$ for $u \in R$ is [Horner's rule](/horner-rule/), $s \leftarrow s \cdot u + a_i$ from the top, with $m - 1$ multiplications in $R$; for nested lists it substitutes $u \in R[x_1, \ldots, x_{n-1}]$ for $x_n$. The derivative in $x_n$ is $[1 \cdot a_1, 2 \cdot a_2, \ldots]$, normalized. Conversion to the distributed form walks the nested lists with an explicit stack; conversion back groups terms by all exponents but the innermost one, builds the innermost lists, and repeats level by level.

## Example

Pseudo-division of $a = x^3 + 2x + 1$ by $b = 2x + 1$ over $\mathbb{Z}$, where $b$ cannot be divided into $a$ with integer quotient. Here $m = 4$, $n = 2$, $\ell = 2$ and $e = 3$ at the start.

| pass | $t$ (line L11) | $q$ after line L12 | $r$ after line L12 | $e$ |
|---|---|---|---|---|
| start | | $0$ | $x^3 + 2x + 1$ | 3 |
| 1 | $x^2$ | $x^2$ | $-x^2 + 4x + 2$ | 2 |
| 2 | $-x$ | $2x^2 - x$ | $9x + 4$ | 1 |
| 3 | $9$ | $4x^2 - 2x + 9$ | $-1$ | 0 |

So $2^3 (x^3 + 2x + 1) = (4x^2 - 2x + 9)(2x + 1) - 1$, which is $8x^3 + 16x + 8$ on both sides. Over $\mathbb{Q}$, dividing by $8$ gives the true quotient $\tfrac12 x^2 - \tfrac14 x + \tfrac98$ and remainder $-\tfrac18$. The tests check this example, and check the identity on random inputs in up to three variables, where $\ell$ is itself a polynomial.

## Correctness

ADD and MUL compute the coefficients of the sum and of the product by the definitions $(a + b)_i = a_i + b_i$ and $(ab)_k = \sum_{i + j = k} a_i b_j$, and NORMALIZE restores (N) by removing top zeros, using the zero test of $R$, which by (N) one level down is a test for the empty list. By induction on the number of variables, the result of each operation meets (N) at every level. For pseudo-division, the loop keeps the invariant $\ell^{k} a = q b + r$ after $k$ passes, and the degree of $r$ falls in each pass, so it ends with $\deg r < \deg b$ after $k \le m - n + 1$ passes; scaling by $\ell^{m - n + 1 - k}$ gives the stated identity. The full proof is in the proof file below.

## Complexity

Costs are in operations of the coefficient ring $R$. For $a$ and $b$ with $m$ and $n$ coefficients:

| operation | operations in $R$ | notes |
|---|---|---|
| add, subtract | $\max(m, n)$ | plus the top zeros removed |
| multiply (schoolbook) | $mn$ multiplications and at most $mn$ additions | $\Theta(mn)$, best and worst |
| evaluate the main variable | $m - 1$ multiplications and $m - 1$ additions | Horner |
| pseudo-division | $O(m(m - n + 1))$, more precisely $O(n (m - n + 1))$ for the products $t \cdot b$ plus $O(m (m - n + 1))$ for the scalings | coefficients grow, see below |
| degree, LC | $O(1)$ | |
| space | $m$ entries of $R$ | |

These counts are proved. For $n$ variables with degree less than $d$ in each, the recursive dense form holds $d^n$ base coefficients, and schoolbook multiplication costs $T(n) = d^2 (T(n-1) + O((2d)^{n-1}))$ base operations, which is $O(d^{2n})$ for $d \ge 3$: quadratic in the number $t = d^n$ of stored coefficients. Replacing the schoolbook product by a fast one, at cost $M(d)$ per level, or reducing the whole product to one univariate product by [Kronecker substitution](/kronecker-substitution/) $x_i \mapsto x^{(2d - 1)^{i-1}}$, gives $O(M((2d)^n))$ base operations. For a field these are field operations on the [BSS model](/blum-shub-smale-machine/); over $\mathbb{Z}$ the bit cost also depends on the size of the coefficients.

Pseudo-division multiplies $a$ by $\ell^{m - n + 1}$, so coefficient sizes grow; repeated in a remainder sequence, this growth is exponential unless the remainders are made primitive or reduced by known factors, as in the [primitive](/primitive-prs/) and [subresultant](/subresultant/) remainder sequences.

## Variants

- **Distributed dense.** A $d_1 \times \cdots \times d_n$ array of all coefficients, indexed by the exponent vector. It is the same memory as the recursive form but loses the main-variable view.
- **Recursive sparse.** The same recursion, but each level is a [sparse](/sparse-polynomial/) list of (exponent, coefficient) pairs. This is the default form in many systems, since multivariate polynomials met in practice are rarely dense in all variables.
- **Mixed.** Dense in the main variable and sparse below, or the reverse, chosen by measured density.
- **Distributed sparse.** A sorted list of terms under a [monomial order](/monomial-ordering/), the form used by Gröbner basis algorithms; see [sparse polynomial](/sparse-polynomial/).
- **Packed and Kronecker forms.** Dense coefficient arrays over small fields packed into machine words, or a whole multivariate polynomial packed into one univariate one by Kronecker substitution.

## When to use it

Use the recursive dense form when the polynomials are dense in each variable, as for generic polynomials of small degree, results of resultants, or modular images in [modular methods](/modular-methods/); and when the algorithm works one variable at a time, as in multivariate gcd by pseudo-remainders, resultants and evaluation and interpolation one variable at a time. Use a sparse form when the number of terms $t$ is much smaller than $d^n$, as for $x_1^{100} + x_2^{100} + \cdots + x_{10}^{100}$, which has 10 terms but would need $101^{10}$ dense entries.

## Pitfalls

- **Storing the zero.** An empty list has no entries from which to learn the ring. Each level must know its zero, or the empty list at an inner level cannot be told from the zero constant, and (N) cannot be checked.
- **Normalizing inner levels.** A sum like $(x + 1) y + (-x - 1) y + 2$ cancels the inner coefficient of $y$ to the empty list; the outer list must then also drop that entry. Each level normalizes its own list.
- **Order of variables.** The choice of main variable changes the sizes and the cost of main-variable algorithms. $(x^{50} + 1) y + 1$ has two coefficients in $y$ but 51 in $x$.
- **Exponential density.** Dense storage of sparse multivariate inputs is exponential in $n$; see the last example under "When to use it".
- **Pseudo-division is not division.** The quotient of pseudo-division is $\ell^{m-n+1}$ times the true quotient over the fraction field. Forgetting the factor gives wrong gcds.

## Implementations

## History

Dense coefficient lists are as old as programs for polynomials. The recursive representation of multivariate polynomials, as polynomials in a main variable with polynomial coefficients, was the standard in early systems such as Collins's PM and SAC-1 systems of the 1960s and early 1970s, and it underlies the algorithms of Collins and Brown for polynomial gcds by subresultants (Geddes, Czapor and Labahn, Chapter 3 and Chapter 7). Knuth's Algorithm R presents pseudo-division over a unique factorization domain.

## References
