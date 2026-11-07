---
tag: G8MNQA
kind: data-structure
slug: macaulay-matrix
name: Macaulay matrix
aliases:
- Macaulay's matrix
- degree-D Macaulay matrix
- Macaulay coefficient matrix
area: algebra/computer-algebra
level: advanced
summary: Matrix of coefficients of multiples of generators up to a degree bound; linear algebra over it solves ideal problems.
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of variables, s: the number of polynomials, D: the degree bound, N: the number of monomials of degree at most D, t: the largest number of terms of a generator}
  time: {build: O(s N t + N log N), echelon: O(s N^3), member: O(N^2)}
  space: {total: O(s N^2)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1902
  people: [Francis S. Macaulay, Daniel Lazard, Jean-Charles Faugère]
  note: Macaulay used these matrices in 1902 to define the multivariate resultant; Lazard showed in 1983 that their row echelon forms give Gröbner bases, and Faugère's F4 algorithm of 1999 builds them selectively.
prereqs: [monomial-ordering, polynomial-ideal, gaussian-elimination, leading-term, monomial]
see_also: [f4-algorithm, xl-algorithm, f5-algorithm, groebner-basis, hilbert-series, ideal-membership-problem, sylvester-matrix, buchberger-algorithm]
sources:
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 10, Section 3 (the F4 algorithm, with the matrices of monomial multiples of polynomials and their row reduction) and Chapter 9, Section 3 (Hilbert functions from leading monomials)
  - paper: "Daniel Lazard, Gröbner bases, Gaussian elimination and resolution of systems of algebraic equations, EUROCAL 1983, Lecture Notes in Computer Science 162"
    locator: Gröbner bases of homogeneous ideals as row echelon forms of Macaulay matrices in each degree
  - paper: doi:10.1016/S0022-4049(99)00005-5
    title: Jean-Charles Faugère, A new efficient algorithm for computing Gröbner bases (F4), Journal of Pure and Applied Algebra 139(1-3), 61-88, 1999
    locator: the symbolic preprocessing that selects rows of a Macaulay matrix and their reduction by sparse linear algebra
  - paper: "Francis S. Macaulay, Some formulae in elimination, Proceedings of the London Mathematical Society 35, 1902"
    locator: the matrix of coefficients of monomial multiples of homogeneous polynomials and the multivariate resultant
---

The Macaulay matrix $M_D(F)$ of polynomials $F = (f_1, \ldots, f_s)$ in $K[x_1, \ldots, x_n]$, for a field $K$ and a degree bound $D$, has one row for each product $m f_i$ with $m$ a [monomial](/monomial/) and $\deg(m f_i) \le D$. It has one column for each monomial of degree at most $D$, with the columns sorted from largest to smallest in a [monomial order](/monomial-ordering/) such as grevlex. Each row holds the coefficients of its product. The row space is the set $V_D$ of all combinations $\sum h_i f_i$ with $\deg(h_i f_i) \le D$, a finite-dimensional piece of the ideal $\langle F \rangle$. [Gaussian elimination](/gaussian-elimination/) with the columns in this order turns it into a row echelon form whose pivot columns are exactly the leading monomials of $V_D$. So linear algebra answers ideal questions in bounded degree: membership, Hilbert functions, and for $D$ large enough a [Gröbner basis](/groebner-basis/). This is the data structure behind Lazard's method, [F4](/f4-algorithm/), [F5](/f5-algorithm/) and [XL](/xl-algorithm/).

## In plain words

Multiply each of your polynomials by every monomial that keeps the degree within a limit. Write the results as rows of a big table, with one column per monomial, ordered so that the most important monomial comes first. Everything you can build from these rows by adding and scaling them belongs to the ideal. Now do ordinary row reduction on the table. The columns where a row starts after the reduction tell you which leading terms the ideal has up to that degree. A polynomial is in the row space exactly when it reduces to zero against the reduced rows. Raising the limit makes the table bigger and catches more of the ideal, and once it is large enough the reduced rows contain a Gröbner basis.

## The abstract type

A static matrix built once from $(F, D, >)$, and then reduced. Notation: $K$ is a field, $S = K[x_1, \ldots, x_n]$, $>$ is lex, grlex or grevlex, and $\operatorname{LM}$, $\operatorname{LT}$ and $\operatorname{LC}$ are the leading monomial, term and coefficient for $>$. For a set $V$ of polynomials, $\operatorname{LM}(V) = \{ \operatorname{LM}(g) : g \in V, g \ne 0 \}$.

- $\text{BUILD}(F, D, >)$: the matrix $M_D(F)$, with its rows labelled by the pairs $(m, i)$.
- $\text{ECHELON}()$: the reduced row echelon form $E$ and its pivot columns $P$.
- $\text{RANK}()$: $\dim_K V_D$.
- $\text{LEADING-MONOMIALS}()$: the set $\operatorname{LM}(V_D)$, which equals $P$.
- $\text{MEMBER}(g)$: whether $g \in V_D$, for $g$ of degree at most $D$.
- $\text{HILBERT}()$: for homogeneous $F$ in the homogeneous variant, $\dim_K (S/I)_D$ as the number of columns minus the rank.

## Representation

- **Columns.** The monomials of degree at most $D$, there are $N = \binom{n + D}{n}$ of them, sorted decreasingly for $>$. A dictionary maps each monomial to its column. In the homogeneous variant only the $\binom{n + D - 1}{n - 1}$ monomials of degree exactly $D$ are used.
- **Rows.** For each $f_i$ of degree $d_i \le D$ and each monomial $m$ with $\deg m \le D - d_i$, the coefficient vector of $m f_i$. There are $\sum_i \binom{n + D - d_i}{n}$ rows. A row has at most $t$ nonzero entries if $f_i$ has $t$ terms, so the matrix is very sparse, and real implementations store rows sparsely.
- **Echelon form.** The nonzero rows after elimination, each with a pivot entry $1$ in a column that no other row uses.

## Operations

```pseudo id=main
BUILD(F, D, >)
L1  rows ← empty list
L2  for each f_i in F and each monomial m with deg(m) + deg(f_i) ≤ D do
L3      append the coefficient vector of m · f_i to rows
L4  columns ← the monomials of degree ≤ D, sorted decreasingly for >
L5  return M with these rows and columns;  E ← empty;  P ← empty

ECHELON(M)
L6  for each column j from left to right: if some unused row has a nonzero entry in j,
        make it the pivot row of j, scale its entry to 1, and clear column j in all other rows
L7  E ← the pivot rows;  P ← their pivot columns

MEMBER(E, P, g)
L8  for each pivot row e of E with pivot column j: g ← g − g[j] · e
L9  return g = 0
```

Line L4 sorts the columns so that the leftmost nonzero entry of every vector is its leading monomial, which is what makes the pivots meaningful. Line L6 is Gauss-Jordan elimination, with pivots chosen by column. Line L8 cancels the pivot entries of $g$ one at a time. The row operations never mix columns, so any field and any monomial order work.

## Example

Take $F = (x^2 - y^2, \; xy)$ in $\mathbb{Q}[x, y]$ with grevlex, $x > y$, in the homogeneous variant. In degree $2$ the columns are $x^2, xy, y^2$, and the two rows $(1, 0, -1)$ and $(0, 1, 0)$ are already reduced. The rank is $2$, so $\dim (S/I)_2 = 1$, and $y^2$ is not a member. In degree $3$ the columns are $x^3, x^2 y, x y^2, y^3$:

| row | $x^3$ | $x^2 y$ | $x y^2$ | $y^3$ |
|---|---|---|---|---|
| $x \cdot (x^2 - y^2)$ | $1$ | $0$ | $-1$ | $0$ |
| $y \cdot (x^2 - y^2)$ | $0$ | $1$ | $0$ | $-1$ |
| $x \cdot xy$ | $0$ | $1$ | $0$ | $0$ |
| $y \cdot xy$ | $0$ | $0$ | $1$ | $0$ |

Elimination gives the identity matrix: the pivots are all four monomials, so $\dim (S/I)_3 = 0$. In particular $y^3 = x \cdot xy - y \cdot (x^2 - y^2)$ is in $I$, the combination that cancels the second and third rows. Its leading monomial $y^3$ is not a multiple of $x^2$ or $xy$, the leading monomials of $F$, so $F$ is not a Gröbner basis. Adding $y^3$ gives the Gröbner basis $\{x^2 - y^2, xy, y^3\}$, and the Hilbert function of $S/I$ is $1, 2, 1, 0, 0, \ldots$.

## Correctness

The row space of $M_D(F)$ is $V_D$ by construction, and row operations do not change it. In a reduced row echelon form with columns in decreasing order, every nonzero vector of the row space is a combination of the pivot rows, and its leftmost nonzero entry is in the pivot column of the first pivot row that it uses. So the pivot columns are exactly $\operatorname{LM}(V_D)$, and $\operatorname{RANK}() = |\operatorname{LM}(V_D)|$. MEMBER subtracts multiples of the pivot rows, and returns true exactly when $g$ is a combination of them. For homogeneous $F$ in the homogeneous variant, the row space is the whole degree-$D$ part $I_D$ of $I = \langle F \rangle$, so the number of columns minus the rank is $\dim (S/I)_D$, and the pivots are the degree-$D$ part of $\langle \operatorname{LT}(I) \rangle$. The full proof is in the proof file below.

## Complexity

The cost model counts operations in $K$, as on a [BSS machine](/blum-shub-smale-machine/) over $K$. Let $N = \binom{n + D}{n}$ be the number of columns and $r \le s N$ the number of rows. These bounds are proved:

| operation | time | case |
|---|---|---|
| BUILD | $O(r t + N \log N)$: $r t$ to place the coefficients of generators with at most $t$ terms, $N \log N$ comparisons to sort the columns | worst |
| ECHELON | $O(r N \rho)$ for rank $\rho \le N$, so $O(s N^3)$ | worst, dense |
| MEMBER | $O(\rho N) = O(N^2)$ against the echelon form | worst |

The dense matrix takes $O(r N) = O(s N^2)$ space.

$N$ grows like $D^n / n!$, and the degree needed for a Gröbner basis can be doubly exponential in $n$ in the worst case, by the examples of Mayr and Meyer (1982). In better cases the degree is known. For a homogeneous zero-dimensional regular sequence of degrees $d_1, \ldots, d_n$, Lazard's bound $D = \sum_i (d_i - 1) + 1$ suffices for grevlex, so $N$ is single exponential in $n$. In practice the matrices are sparse, and sparse elimination as in F4 is much faster than the dense bound. That is an observation, not a theorem.

## Variants

- **Homogeneous Macaulay matrix.** Only rows and columns of degree exactly $D$. For homogeneous $F$ it computes $I_D$ exactly, and one matrix per degree gives the Hilbert function.
- **Selected rows (F4).** [F4](/f4-algorithm/) builds only the rows needed to reduce a batch of S-polynomials, by symbolic preprocessing, and reduces them together.
- **Signature-based row removal (F5).** [F5](/f5-algorithm/) labels each row by its signature $(m, i)$ and drops rows that are known to reduce to zero, which for regular sequences removes every zero reduction.
- **XL and linearization.** [XL](/xl-algorithm/) builds $M_D$ for growing $D$ and looks for a univariate polynomial in the row space, a method used in cryptanalysis.
- **Macaulay resultant.** For $n$ homogeneous polynomials in $n$ variables, the determinant of a square submatrix of the Macaulay matrix in degree $\sum_i (d_i - 1) + 1$, divided by a minor, is the multivariate resultant, which generalizes the [Sylvester matrix](/sylvester-matrix/).
- **Numerical linear algebra.** Over $\mathbb{R}$ or $\mathbb{C}$, singular value decompositions of Macaulay matrices give numerically stable root finding.

## When to use it

Use it when ideal computations in bounded degree are wanted with plain linear algebra: testing ideal membership up to a degree, computing Hilbert functions, or building a Gröbner basis by batched reductions as in F4. It also serves as an independent oracle for testing Gröbner basis code, since membership in $V_D$ is a rank computation. For one-by-one reductions with few polynomials, [Buchberger's algorithm](/buchberger-algorithm/) with a good selection strategy can be cheaper, because it never builds rows that are not needed.

## Pitfalls

- **Wrong column order.** If the columns are not sorted by the monomial order, the pivots are not leading monomials, and the echelon form says nothing about $\langle \operatorname{LT}(I) \rangle$.
- **Affine degree fall.** For non-homogeneous $F$, $V_D$ can be strictly smaller than $I \cap S_{\le D}$, because a combination of high-degree products can cancel down to a low-degree polynomial in $I$ that needs higher-degree rows. A polynomial outside $V_D$ may still be in $I$. Homogenize, or raise $D$.
- **Size.** $N = \binom{n + D}{n}$ grows fast. Dense storage of $s N^2$ entries becomes impossible quickly, so store rows sparsely.
- **Redundant rows.** Most rows are linear combinations of others, through the syzygies such as $f_j \cdot f_i - f_i \cdot f_j = 0$. They cost time but are harmless. F5 removes them.
- **Coefficient growth.** Over $\mathbb{Q}$ elimination can blow up the entries. Work modulo a prime and lift, as in [modular methods](/modular-methods/).

## Implementations

## History

Macaulay introduced the matrix in 1902 to define the resultant of $n$ homogeneous polynomials in $n$ variables, extending Sylvester's construction for two polynomials. Lazard observed in 1983 that, for homogeneous ideals, Gaussian elimination on these matrices degree by degree computes a Gröbner basis, linking Buchberger's algorithm to linear algebra. Faugère turned this into the practical F4 algorithm in 1999, which selects rows and uses sparse elimination, and into F5 in 2002, which removes rows that reduce to zero. Courtois, Klimov, Patarin and Shamir proposed XL in 2000 for cryptanalysis.

## References
