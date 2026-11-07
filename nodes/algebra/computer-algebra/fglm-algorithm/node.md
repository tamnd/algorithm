---
tag: FWH4VF
kind: algorithm
slug: fglm-algorithm
name: FGLM algorithm
aliases:
- Faugère-Gianni-Lazard-Mora
- FGLM change of ordering
area: algebra/computer-algebra
level: advanced
summary: Converts a zero-dimensional Gröbner basis to a lex basis using linear algebra.
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of variables, D: the dimension of the quotient ring R/I over K}
  time: {worst: O(n D^3), best: O(D^3)}
  space: {extra: O(n D^2)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [reduced-groebner-basis, monomial-ordering, normal-form, gaussian-elimination]
see_also: [groebner-basis-conversion, groebner-walk, rational-univariate-representation, polynomial-system-solving, buchberger-algorithm, f4-algorithm, berlekamp-massey, elimination-ideal]
sources:
  - paper: doi:10.1006/jsco.1993.1051
    title: Jean-Charles Faugère, Patrizia Gianni, Daniel Lazard and Teo Mora, Efficient computation of zero-dimensional Gröbner bases by change of ordering, Journal of Symbolic Computation 16(4), 329-344, 1993
    locator: the algorithm, the multiplication matrices of the quotient ring and the bound of O(n D^3) field operations
  - book: isbn:9780387207063
    title: David A. Cox, John Little and Donal O'Shea, Using Algebraic Geometry, second edition, Springer, 2005
    locator: Chapter 2, Section 3 (Gröbner basis conversion, the FGLM algorithm with its correctness proof and a worked example)
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 3, Section 1 (lex bases and the elimination theorem) and Chapter 5, Section 3 (the finiteness theorem and standard monomials of zero-dimensional ideals)
  - paper: doi:10.1016/j.jsc.2016.07.025
    title: Jean-Charles Faugère and Chenqi Mou, Sparse FGLM algorithms, Journal of Symbolic Computation 80, 538-569, 2017
    locator: the variant with sparse multiplication matrices, Wiedemann sequences and Berlekamp-Massey
  - paper: "Jean-Charles Faugère, Pierrick Gaudry, Louise Huot and Guénaël Renault, Sub-cubic change of ordering for Gröbner basis: a probabilistic approach, Proceedings of ISSAC 2014, ACM, pages 170 to 177"
    locator: the change of ordering in shape position with fast matrix multiplication
---

The FGLM algorithm converts the reduced Gröbner basis of a zero-dimensional ideal for one monomial order into the reduced Gröbner basis of the same ideal for another order, usually from grevlex to lex. It works entirely by linear algebra in the quotient ring $K[x_1, \ldots, x_n]/I$, which is a vector space of finite dimension $D$ over $K$. It walks through monomials in increasing order of the new order, computes each one's normal form with respect to the old basis as a vector in $K^D$, and records a new basis element each time a normal form is a linear combination of earlier ones. Faugère, Gianni, Lazard and Mora published it in 1993 with a bound of $O(n D^3)$ field operations, and it is the second half of the standard solving strategy: compute a Gröbner basis in grevlex with [F4](/f4-algorithm/) or [Buchberger's algorithm](/buchberger-algorithm/), then convert to lex with FGLM.

## In plain words

A system of polynomial equations with finitely many solutions can be rewritten in many ways. One way is cheap to compute; another way puts the equations in a triangle, with one equation in one unknown, which is what a user needs to solve the system.

FGLM turns the cheap form into the triangular form. It lists products of the unknowns from small to large. It writes each product in a fixed finite list of basic coordinates, using the cheap form. As soon as a product can be written using the coordinates of products already seen, that relation is a new equation of the triangular form. The work is ordinary elimination on vectors whose length is the number of solutions.

## The problem

Let $K$ be a field and $R = K[x_1, \ldots, x_n]$. For a monomial order $>$ (lex, grlex or grevlex, always with $x_1 > x_2 > \cdots > x_n$), $\operatorname{LT}(f)$, $\operatorname{LM}(f)$ and $\operatorname{LC}(f)$ are the leading term, leading monomial and leading coefficient of $f \ne 0$. Write $d$ for a bound on the degrees of the input polynomials, $t$ for the number of terms, and $M(d)$ for the cost of multiplying univariate polynomials of degree $d$; FGLM itself needs only $n$ and $D$.

**Input:** two monomial orders $>_1$ and $>_2$, and the [reduced Gröbner basis](/reduced-groebner-basis/) $G_1$ of a zero-dimensional ideal $I \subseteq R$ for $>_1$.

**Output:** the reduced Gröbner basis $G_2$ of $I$ for $>_2$.

The ideal is zero-dimensional when $R/I$ has finite dimension $D$ over $K$. Then the set $B_1$ of *standard monomials*, those divisible by no $\operatorname{LM}_{>_1}(g)$ with $g \in G_1$, is a basis of $R/I$, and it is finite exactly when each variable has a pure power $x_i^{e_i}$ among the leading monomials of $G_1$ (CLO Chapter 5, Section 3). Let $\varphi : R \to K^D$ send $f$ to the coordinates of its [normal form](/normal-form/) $\operatorname{NF}_{G_1}(f)$ in the basis $B_1$. It is $K$-linear, its kernel is $I$, and $\varphi(x_i f) = M_i\, \varphi(f)$ for the *multiplication matrix* $M_i$ of $x_i$ on $R/I$.

## The algorithm

```pseudo id=main
FGLM(G_1, >_1, >_2)                 ▷ G_1 reduced Gröbner basis of a zero-dimensional I for >_1
L1  B_1 ← standard monomials of G_1; build M_1, ..., M_n from NF_{G_1}(x_i b), b ∈ B_1
L2  S ← [], G_2 ← [], C ← {1}        ▷ S the new staircase, C the candidate monomials
L3  while C ≠ ∅ do
L4      m ← the smallest element of C for >_2; remove it from C
L5      if LM(g) divides m for some g ∈ G_2 then continue
L6      v ← φ(m), computed as M_i φ(m') where m = x_i m' and m' ∈ S (or φ(1) if m = 1)
L7      if v = Σ_j c_j φ(s_j) for s_j ∈ S then append m − Σ_j c_j s_j to G_2
L8      else append m to S and add x_1 m, ..., x_n m to C
L9  return G_2
```

Line L7 is incremental Gaussian elimination: the vectors $\varphi(s)$ for $s \in S$ are kept in echelon form, together with the combination of the original vectors that produced each echelon row, so a dependency is detected and expressed in $O(D^2)$ operations.

## Example

Let $I = \langle x^2 + y^2 - 4,\ xy - 1 \rangle \subseteq \mathbb{Q}[x, y]$, a circle and a hyperbola meeting in four points. Its reduced grevlex basis is $G_1 = \{x^2 + y^2 - 4,\ xy - 1,\ y^3 + x - 4y\}$, with standard monomials $B_1 = (1, y, x, y^2)$, so $D = 4$. Convert to lex with $x > y$. Vectors are coordinates in $B_1$. The trace, from the implementation:

| step | $m$ | computed as | $\operatorname{NF}_{G_1}(m)$ | $\varphi(m)$ | outcome |
|---|---|---|---|---|---|
| 1 | $1$ | | $1$ | $(1, 0, 0, 0)$ | into $S$; $C = \{x, y\}$ |
| 2 | $y$ | $M_y \varphi(1)$ | $y$ | $(0, 1, 0, 0)$ | into $S$; add $xy$, $y^2$ |
| 3 | $y^2$ | $M_y \varphi(y)$ | $y^2$ | $(0, 0, 0, 1)$ | into $S$; add $xy^2$, $y^3$ |
| 4 | $y^3$ | $M_y \varphi(y^2)$ | $-x + 4y$ | $(0, 4, -1, 0)$ | into $S$; add $xy^3$, $y^4$ |
| 5 | $y^4$ | $M_y \varphi(y^3)$ | $4y^2 - 1$ | $(-1, 0, 0, 4)$ | $= 4\varphi(y^2) - \varphi(1)$: output $y^4 - 4y^2 + 1$ |
| 6 | $x$ | $M_x \varphi(1)$ | $x$ | $(0, 0, 1, 0)$ | $= -\varphi(y^3) + 4\varphi(y)$: output $x + y^3 - 4y$ |
| 7 to 9 | $xy$, $xy^2$, $xy^3$ | | | | skipped at L5, divisible by $x$ |

The result is $G_2 = \{y^4 - 4y^2 + 1,\ x + y^3 - 4y\}$, the same basis that Buchberger's algorithm computes directly in lex. At step 5, $\operatorname{NF}(y^4)$ comes from $y \cdot (-x + 4y) = -xy + 4y^2$, and $xy$ reduces to $1$. The lex basis is triangular: solve $y^4 - 4y^2 + 1 = 0$, then $x = 4y - y^3$.

## Correctness

The full proof is in the correctness file. The map $\varphi$ is linear with kernel $I$, so a monomial $m$ is a leading monomial of $I$ for $>_2$ exactly when $\varphi(m)$ is a combination of the $\varphi$ of smaller monomials. Candidates are taken in increasing order, because new candidates are multiples of the current one. The standard monomials for $>_2$ form a set closed under division, so by induction each of them becomes a candidate, is found independent of the earlier ones, and enters $S$. Each minimal generator of the leading monomial ideal is a candidate whose proper divisors are all in $S$. It gives an element $m - \sum c_j s_j$ of $I$ whose tail consists of standard monomials. Every other leading monomial is skipped at line L5. So $G_2$ is exactly the reduced Gröbner basis. The loop terminates because $|S| \le D$, so at most $nD + 1$ monomials ever enter $C$.

## Complexity

The cost model is operations in $K$, counted on a Blum-Shub-Smale machine over $K$; over $\mathbb{Q}$ the bit cost depends on coefficient growth, which is not bounded here.

- **Main loop, proved.** At most $nD + 1$ candidates are processed, since each element of $S$ adds $n$. For each, line L6 is a product of a $D \times D$ matrix with a vector, $O(D^2)$, and line L7 reduces the vector against at most $D$ echelon rows, $O(D^2)$. The total is $O(n D^3)$ operations, the bound of Faugère, Gianni, Lazard and Mora.
- **Multiplication matrices, proved.** The paper builds $M_1, \ldots, M_n$ in $O(n D^3)$ operations by computing normal forms of the border monomials $x_i b$ in increasing order, each as a combination of normal forms already known. The implementation here computes them by plain division by $G_1$, which is simpler and fast for small examples, but its cost is not covered by this bound.
- **Best case.** With dense matrices, the $D$ elements of $S$ each need a product with a matrix, so $\Omega(D^3)$ operations are spent whatever $n$ is; when most candidates are skipped, the cost is $O(D^3)$.
- **Space.** The $n$ matrices take $O(n D^2)$ field elements, and the echelon form $O(D^2)$.
- **In terms of the input.** By Bézout's theorem, $D \le d^n$ for $n$ generators of degree at most $d$, so conversion costs $O(n d^{3n})$, single exponential in $n$. Computing $G_1$ in the first place is the harder part. For zero-dimensional ideals it is also single exponential, $d^{O(n)}$ (Lakshman 1991). For ideals in general, Gröbner bases have doubly exponential worst-case degree, $d^{2^{O(n)}}$, by the examples of Mayr and Meyer (1982); FGLM does not apply there.

## Properties

- **Exact and deterministic.** Only field operations are used; over $\mathbb{Q}$ the result is exact.
- **Any pair of orders.** Nothing in the algorithm depends on $>_1$ beyond the normal form, and $>_2$ is used only to pick the smallest candidate. Lex is the usual target, but grevlex to grlex or to a block order works the same way.
- **Output-sensitive in $D$.** The cost depends on $D$, not on the degrees of the output. In the example of many reduction steps in the tests, the lex basis has a polynomial of degree 25 while the grevlex basis has degree 5.
- **Byproducts.** The matrices $M_i$ give the eigenvalue method of solving, and the staircase $S$ is a basis of $R/I$ adapted to $>_2$.

## Variants and improvements

- **Shape position.** When the lex basis has the form $\{x_1 - g_1(x_n), \ldots, x_{n-1} - g_{n-1}(x_n), h(x_n)\}$ with $\deg h = D$, which holds for radical ideals after a generic linear change of coordinates, only the sequence $M_n^k \varphi(1)$ is needed. The minimal polynomial $h$ comes from a Krylov sequence, and each $g_i$ from one more linear system.
- **Sparse FGLM** (Faugère and Mou 2011, 2017). The matrices $M_i$ are often sparse. Compute the scalar sequence $u^{\mathsf T} M_n^k v$ and find $h$ by [Berlekamp-Massey](/berlekamp-massey/), as in the [Wiedemann algorithm](/wiedemann-algorithm/), then recover the $g_i$ from structured systems. The cost depends on the number of nonzero entries.
- **Sub-cubic FGLM** (Faugère, Gaudry, Huot and Renault 2014). In shape position, compute the powers of $M_n$ applied to a vector by repeated squaring with fast matrix multiplication, in $\tilde{O}(D^\omega)$ operations, where $\omega$ is the matrix multiplication exponent. The method is probabilistic.
- **Rational univariate representation.** Instead of the lex basis, output $h$ and the coordinates as $x_i = q_i(u)/h'(u)$ for a separating linear form $u$. Over $\mathbb{Q}$ these coefficients are much smaller; see [rational univariate representation](/rational-univariate-representation/).
- **Modular FGLM.** Over $\mathbb{Q}$, run FGLM modulo several primes and reconstruct the coefficients by Chinese remaindering and rational reconstruction.
- **Positive dimension.** FGLM needs a finite $B_1$. For other ideals use the [Gröbner walk](/groebner-walk/) or a Hilbert-driven Buchberger algorithm; see [Gröbner basis conversion](/groebner-basis-conversion/).

## When to use it

Use FGLM to solve a zero-dimensional polynomial system: compute $G_1$ in grevlex, where Gröbner basis computation is fastest, then convert to lex or to an [elimination](/elimination-ideal/) order to get a triangular description of the solutions. Use the sparse or shape-position variants when $D$ is in the thousands. Do not use it for positive-dimensional ideals, and do not use it when the lex basis is not needed, for example when only the number of solutions $D$ is wanted, which $G_1$ already gives.

## Pitfalls

- **Zero-dimensionality.** If some $x_i$ has no pure power among the leading monomials of $G_1$, the set $B_1$ is infinite and the loop never ends. Check this first; the implementation raises an error.
- **The input must be a Gröbner basis.** If $G_1$ is not a Gröbner basis for $>_1$, the normal form is not well defined, $\varphi$ is not linear modulo $I$, and the output is wrong without any warning.
- **Candidate order.** The candidates must be processed in increasing $>_2$ order, and a candidate divisible by a known leading monomial must be skipped before its vector is used. Processing in another order gives combinations whose tail contains larger monomials, and the result is not reduced.
- **Duplicate candidates.** The same monomial arises as $x_i m$ and $x_j m'$. It must be processed once; a set or a map from monomials to their parent does this.
- **Coefficient growth.** Over $\mathbb{Q}$ the lex basis can have much larger coefficients than the grevlex basis. Exact arithmetic is correct but can be slow; modular methods or the rational univariate representation are used in practice.

## Implementations

## History

Faugère, Gianni, Lazard and Mora published the algorithm in 1993. The idea of solving through the linear algebra of the quotient ring goes back to Buchberger's 1965 thesis, which computed the multiplication table of $R/I$ from a Gröbner basis, and to Lazard's work linking Gröbner bases with linear algebra on Macaulay matrices in the early 1980s. The algorithm is the change-of-ordering step of the polynomial system solvers in the main computer algebra systems, and its sparse and sub-cubic variants (Faugère and Mou; Faugère, Gaudry, Huot and Renault) came from systems arising in algebraic cryptanalysis.

## References
