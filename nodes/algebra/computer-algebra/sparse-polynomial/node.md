---
tag: 28C10S
kind: data-structure
slug: sparse-polynomial
name: Sparse polynomial representation
aliases: [sparse distributed representation, distributed polynomial, term list in monomial order]
area: algebra/computer-algebra
level: core
summary: Stores only nonzero terms, as a list or map from exponents to coefficients.
implements: [polynomial]
model: blum-shub-smale-machine
complexity:
  vars: {s: "the number of terms of the shorter factor", t: "the number of terms of the longer factor", n: the number of variables}
  time: {worst: O(n s t log s)}
  space: {extra: O(s)}
prereqs: [sparse-polynomial-representation, monomial-ordering, binary-heap]
see_also: [sparse-polynomial-multiplication, dense-polynomial, leading-term, multivariate-division-algorithm, buchberger-algorithm, straight-line-program, sparse-polynomial-interpolation, k-way-merge]
sources:
  - paper: doi:10.1145/1086837.1086847
    title: Stephen C. Johnson, Sparse polynomial arithmetic, ACM SIGSAM Bulletin 8(3), 1974
    locator: pp. 63 to 71 (the heap of term products for multiplication and division)
  - paper: doi:10.1016/j.jsc.2010.08.014
    title: Michael Monagan and Roman Pearce, Sparse polynomial division using a heap, Journal of Symbolic Computation 46(7), 2011
    locator: pp. 807 to 822 (packed exponent vectors, heap multiplication and division, and the cost analysis)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 3, Normal Forms and Algebraic Representations (recursive and distributive, dense and sparse representations of multivariate polynomials)
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 2, Section 2 (monomial orders, and the compatibility of an order with multiplication)
---

The sparse distributed representation stores a polynomial in several variables as the list of its nonzero terms, each a pair of an exponent vector and a coefficient, sorted in decreasing order for a fixed [monomial order](/monomial-ordering/). Its size is proportional to the number of terms, not to the number of possible monomials, which is $\binom{n + d}{n}$ for $n$ variables and total degree $d$. The [leading term](/leading-term/) is the first entry, which is what [multivariate division](/multivariate-division-algorithm/) and [Buchberger's algorithm](/buchberger-algorithm/) read at each step. Addition is a merge of two sorted lists, and multiplication by Johnson's heap method produces the terms of the product already in order.

## In plain words

A polynomial in several letters, such as three x squared times y plus five z minus one, can have very few terms even when its degree is large. Writing a slot for every possible combination of powers would waste most of the memory. So this representation keeps only the terms that are present: for each one, the list of powers and the number in front.

The terms are kept in one fixed order, with the largest first. Which term counts as largest is set by a rule that the user picks once, and that rule never changes the order of two terms when both are multiplied by the same thing. Adding two polynomials is then like merging two sorted lists. To multiply, the method keeps a small priority queue of candidate products and always takes the largest one next.

## The abstract type

The representation implements the [polynomial](/polynomial/) type of $R[x_1, \ldots, x_n]$ for a commutative ring $R$ (a field $K$ in the Gröbner basis setting): `add`, `neg`, `sub`, `mul_term` (multiply by one term), `mul`, `leading_term` and `evaluate`. Costs are in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $R$: a ring operation or a zero test costs 1. A *monomial operation* is a comparison or a product of two exponent vectors, and it costs $O(n)$ integer operations; when the exponents are packed into one machine word, it costs $O(1)$ word operations. Over $\mathbb{Z}$ or $\mathbb{Q}$ the cost of a coefficient operation also grows with the size of the coefficients, and the bounds below then count coefficient operations, not bit operations.

## Representation

Fix $n$ and a monomial order $>$ on the monomials $x^\alpha = x_1^{\alpha_1} \cdots x_n^{\alpha_n}$, $\alpha \in \mathbb{N}^n$. The order is one of

- **lex**: $x^\alpha > x^\beta$ when the first nonzero entry of $\alpha - \beta$ is positive;
- **grlex**: compare $|\alpha| = \sum \alpha_i$ first, then lex;
- **grevlex**: compare $|\alpha|$ first, then $x^\alpha > x^\beta$ when the last nonzero entry of $\alpha - \beta$ is negative.

A value is a list $f = [(\alpha_1, c_1), \ldots, (\alpha_t, c_t)]$ that stands for $\sum_i c_i x^{\alpha_i}$.

**Invariant (D).** $x^{\alpha_1} > x^{\alpha_2} > \cdots > x^{\alpha_t}$ and every $c_i \ne 0$.

Each polynomial has exactly one list that meets (D). The zero polynomial is the empty list. Then $\operatorname{LT}(f) = c_1 x^{\alpha_1}$, $\operatorname{LM}(f) = x^{\alpha_1}$ and $\operatorname{LC}(f) = c_1$ in $O(1)$ time, and equality of two polynomials is equality of two lists.

Two properties of a monomial order make the operations work: it is a total order, and $x^\alpha > x^\beta$ implies $x^{\alpha + \gamma} > x^{\beta + \gamma}$ for every $\gamma$. The second one means that multiplying a sorted list by one term keeps it sorted.

The other common layout is the *recursive* representation, a polynomial in $x_1$ whose coefficients are polynomials in $x_2, \ldots, x_n$. It suits gcd and resultant algorithms that eliminate one variable at a time. The distributed layout suits algorithms driven by a monomial order, such as division and Gröbner bases. The [dense representation](/dense-polynomial/) stores all monomials up to a degree bound $d$, which costs $(d+1)^n$ or $\binom{n+d}{n}$ slots.

## Operations

### Multiplication

```pseudo id=main
MUL(f, g)                 ▷ f = [(α_1, a_1) .. (α_s, a_s)], g = [(β_1, b_1) .. (β_t, b_t)], both meet (D), s ≤ t
L1  if s = 0 or t = 0 then return [ ]
L2  H ← a max-heap with the entries (x^(α_i + β_1), i, 1) for i = 1 .. s
L3  h ← [ ]
L4  while H is not empty do
L5      (m, i, j) ← EXTRACT-MAX(H)                  ▷ the largest product not yet used
L6      c ← a_i b_j
L7      if h is not empty and the last monomial of h is m then add c to its coefficient
L8      else delete the last term of h if its coefficient is 0; append (m, c)
L9      if j < t then INSERT(H, (x^(α_i + β_(j+1)), i, j + 1))
L10 if h is not empty and the last coefficient of h is 0 then delete it
L11 return h
```

The heap holds one entry for each row $i$ of the $s \times t$ table of products $a_i b_j x^{\alpha_i + \beta_j}$: the first product of the row that is not yet used. Each row of the table is sorted, because $x^{\beta_1} > x^{\beta_2} > \cdots$ and the order is compatible with multiplication by $x^{\alpha_i}$. So the largest unused product is always at the top of the heap, and the products come out in non-increasing order. Equal monomials come out one after the other, and line L7 adds them. A term whose coefficient cancels to zero is deleted when the next monomial arrives (line L8) or at the end (line L10). This is Johnson's 1974 method. The heap keys are compared with the monomial order, and each comparison is a monomial operation.

Cost: $st$ extractions and at most $st$ insertions on a heap of at most $s$ entries, so $O(st \log s)$ monomial comparisons, $st$ products of exponent vectors and $st$ ring operations. With $s \le t$ by swapping the factors, this is $O(n \, s t \log s)$ integer operations. The extra space is the heap, $O(s)$ entries, plus the output, which has at most $st$ terms.

### Addition

```pseudo id=add
ADD(f, g)                            ▷ both meet (D)
A1  i ← 1; j ← 1; h ← [ ]
A2  while i ≤ |f| and j ≤ |g| do
A3      if LM(f[i]) > LM(g[j]) then append f[i] to h; i ← i + 1
A4      else if LM(f[i]) < LM(g[j]) then append g[j] to h; j ← j + 1
A5      else u ← coefficient of f[i] + coefficient of g[j]
A6           if u ≠ 0 then append (monomial of f[i], u) to h
A7           i ← i + 1; j ← j + 1
A8  append f[i ..] and g[j ..] to h; return h
```

This is the merge of two sorted lists, with like terms added and zero sums dropped. Cost: $O(s + t)$ monomial comparisons and at most $\min(s, t)$ ring additions. Subtraction is $f + (-g)$, where negation flips each coefficient in $O(t)$.

### Multiplication by a term, leading term and evaluation

`mul_term(f, γ, c)` replaces each $(\alpha_i, c_i)$ by $(\alpha_i + \gamma, c \, c_i)$. The order stays strictly decreasing by compatibility, so no sorting is needed. Over an integral domain no coefficient becomes zero when $c \ne 0$. Over a ring with zero divisors, such as $\mathbb{Z}/6\mathbb{Z}$, a product can vanish and is dropped. Cost: $O(t)$ monomial and ring operations. This is the inner step of [multivariate division](/multivariate-division-algorithm/): $f - (\operatorname{LT}(f)/\operatorname{LT}(g)) \, g$ is one `mul_term` and one `sub`.

`leading_term` returns the first pair in $O(1)$. `evaluate` computes $\sum_i c_i \prod_k p_k^{\alpha_{ik}}$ at a point $p$ with $O(t \, n \log d)$ ring operations by repeated squaring, for total degree at most $d$.

## Example

Take grlex with $x > y$, $f = x + y + 1$ and $g = x - y + 2$. In grlex order the terms of $f$ are $f_1 = x$, $f_2 = y$, $f_3 = 1$, and those of $g$ are $g_1 = x$, $g_2 = -y$, $g_3 = 2$. The heap starts with the products $f_1 g_1$, $f_2 g_1$ and $f_3 g_1$.

| step | extracted | heap after the step | output $h$ |
|---|---|---|---|
| 1 | $f_1 g_1 = x^2$ | $f_1 g_2, f_2 g_1, f_3 g_1$ | $x^2$ |
| 2 | $f_1 g_2 = -xy$ | $f_1 g_3, f_2 g_1, f_3 g_1$ | $x^2 - xy$ |
| 3 | $f_2 g_1 = xy$ | $f_1 g_3, f_2 g_2, f_3 g_1$ | $x^2 + 0 \cdot xy$ |
| 4 | $f_2 g_2 = -y^2$ | $f_1 g_3, f_2 g_3, f_3 g_1$ | $x^2 - y^2$ (the zero term is deleted) |
| 5 | $f_1 g_3 = 2x$ | $f_2 g_3, f_3 g_1$ | $x^2 - y^2 + 2x$ |
| 6 | $f_3 g_1 = x$ | $f_2 g_3, f_3 g_2$ | $x^2 - y^2 + 3x$ |
| 7 | $f_2 g_3 = 2y$ | $f_3 g_2$ | $x^2 - y^2 + 3x + 2y$ |
| 8 | $f_3 g_2 = -y$ | $f_3 g_3$ | $x^2 - y^2 + 3x + y$ |
| 9 | $f_3 g_3 = 2$ | empty | $x^2 - y^2 + 3x + y + 2$ |

The two $xy$ products cancel at step 3, and the zero term goes away at step 4. The heap never holds more than $s = 3$ entries, and the output is in grlex order with no sorting step.

## Correctness

Each operation returns a list that meets (D) and that represents the right polynomial. For MUL the key invariant is: the heap holds, for each row $i$ that is not finished, exactly the entry $(i, j_i)$ where $j_i$ is the first unused column, and every unused product is at most the top of the heap. So the products leave the heap in non-increasing order, equal monomials are adjacent, and $h$ is strictly decreasing with nonzero coefficients. The full proof is in the proof file below.

## Complexity

| operation | monomial operations | ring operations | extra space |
|---|---|---|---|
| `leading_term` | $O(1)$ | 0 | $O(1)$ |
| `add`, `sub` | $O(s + t)$ | $O(s + t)$ | $O(1)$ beyond the output |
| `mul_term` | $O(t)$ | $O(t)$ | $O(1)$ beyond the output |
| `mul` | $O(st \log s)$ | $st$ products and at most $st$ additions | $O(s)$ beyond the output |
| `evaluate` | 0 | $O(t \, n \log d)$ | $O(1)$ |

Each monomial operation costs $O(n)$ integer operations, which gives the $O(n \, st \log s)$ bound of the front matter for `mul`. These bounds are proved, in the worst case. In practice, Monagan and Pearce report that packing exponent vectors into words, inserting heap entries lazily (the entry of row $i+1$ only after row $i$ has started) and chaining equal monomials in the heap make heap multiplication faster than sorting or hashing methods for sparse inputs. The output can have as few as $s + t - 1$ terms or as many as $st$, and $\Omega(st)$ coefficient products are needed in the worst case, when no two products share a monomial.

## Variants

- **Hash table of terms.** Accumulate products in a dictionary keyed by the monomial, then sort the result once. This costs $O(st)$ expected for the accumulation plus $O(r \log r)$ to sort $r$ output terms. It is simple, but the leading term is unknown until the end.
- **Geobuckets.** Yan's geobuckets keep a sum as a few sorted lists of geometrically growing length, which makes the many subtractions of a division cheap.
- **Packed monomials.** Store an exponent vector in one 64-bit word, with a few bits for each variable and a total degree field for graded orders. A comparison is then one integer comparison, and a monomial product is one integer addition.
- **Heap division.** The same heap computes the quotient and remainder of [multivariate division](/multivariate-division-algorithm/) with a heap whose size is the number of terms of the quotient or the divisor (Monagan and Pearce 2011).
- **Recursive sparse form.** A sparse list in the main variable whose coefficients are sparse polynomials in the other variables. See [sparse polynomial representation](/sparse-polynomial-representation/) for the univariate case.

## When to use it

Use the distributed sparse form whenever an algorithm needs leading terms for a monomial order: division with remainder, Gröbner bases, normal forms. Use it when the number of terms is far below the number of monomials of the same degree, which is the common case in many variables. Use the [dense form](/dense-polynomial/) for one or two variables of low degree, where FFT methods are faster, and use a [straight-line program](/straight-line-program/) when even the term list is too large but evaluation is cheap.

## Pitfalls

- **Sorting with the wrong order.** All operations assume one fixed monomial order. Merging a lex list with a grevlex list breaks (D) without an error. Keep the order with the polynomial, as the implementation does, and convert before an operation.
- **Keeping zero coefficients.** If line L8 or line L10 of MUL is left out, a cancelled term stays in the list with coefficient 0. Then `leading_term` can return a zero term, and division never ends on that term.
- **A heap of all $st$ products.** Pushing every product into the heap at the start costs $O(st)$ space and $O(st \log(st))$ time. The method of line L2 and line L9 keeps only one entry per row.
- **Grevlex is not reverse lex.** Grevlex compares the total degree first. Comparing only by the last exponents, without the degree, is not a monomial order, because $1$ is then not the smallest monomial.

## Implementations

## History

Johnson described heap-based multiplication and division of sparse polynomials in 1974, for the ALTRAN system. Distributed representations sorted by a monomial order became standard with the spread of Gröbner basis software in the 1980s. Monagan and Pearce revisited the heap methods with packed monomials and lazy insertion, and showed in 2011 that they are competitive with the best methods on current hardware.

## References
