---
tag: XY5Z26
kind: algorithm
slug: f4-algorithm
name: F4 algorithm
aliases:
- Faugère F4
- F4
area: algebra/computer-algebra
level: advanced
summary: Reduces many S-polynomials at once via sparse linear algebra on Macaulay matrices.
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of variables, d: the largest degree of an input polynomial, r: the rows of a Macaulay matrix, c: the columns of a Macaulay matrix}
  time: {worst: d^(2^O(n)), best: "O(r c min(r, c))"}
  space: {extra: O(r c)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [buchberger-algorithm, macaulay-matrix, gaussian-elimination, s-polynomial]
see_also: [f5-algorithm, gebauer-moller-criteria, buchberger-criteria, groebner-basis-computation, sugar-strategy, fglm-algorithm, reduced-groebner-basis, groebner-basis]
sources:
  - paper: doi:10.1016/S0022-4049(99)00005-5
    title: Jean-Charles Faugère, A new efficient algorithm for computing Gröbner bases (F4), Journal of Pure and Applied Algebra 139(1-3), 61-88, 1999
    locator: the algorithm F4, symbolic preprocessing, the function Simplify, the normal selection strategy and the proof of correctness
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 10, Section 3 (the F4 algorithm, with symbolic preprocessing and a proof that the result is a Gröbner basis); Chapter 2, Section 6 (the Buchberger criterion)
  - paper: "Daniel Lazard, Gröbner bases, Gaussian elimination and resolution of systems of algebraic equations, Proceedings of EUROCAL 83, Lecture Notes in Computer Science 162, Springer, 1983, pages 146 to 156"
    locator: the link between Gröbner bases and row echelon forms of Macaulay matrices
  - paper: doi:10.1016/S0747-7171(88)80048-8
    title: Rüdiger Gebauer and H. Michael Möller, On an installation of Buchberger's algorithm, Journal of Symbolic Computation 6(2-3), 275-286, 1988
    locator: the procedure UPDATE that maintains the critical pairs
  - paper: doi:10.1016/0001-8708(82)90048-2
    title: Ernst W. Mayr and Albert R. Meyer, The complexity of the word problems for commutative semigroups and polynomial ideals, Advances in Mathematics 46(3), 305-329, 1982
    locator: the ideals whose Gröbner bases need degrees doubly exponential in the number of variables
---

F4 is an algorithm for computing Gröbner bases that replaces the one-at-a-time reductions of [Buchberger's algorithm](/buchberger-algorithm/) by the row reduction of a matrix. In each round it selects many critical pairs together, writes the two halves of each [S-polynomial](/s-polynomial/) and every multiple of a basis element that could be needed to reduce them as rows of a [Macaulay matrix](/macaulay-matrix/), and brings that matrix to row echelon form. The rows whose leading monomials are new become new basis elements. Faugère published it in 1999. Because the matrices are large, sparse and structured, F4 can use fast sparse linear algebra, and it is the algorithm behind the Gröbner basis engines of Magma, Maple and other systems.

## In plain words

Buchberger's algorithm cleans up one pair of polynomials at a time, by long division. Many of those divisions repeat the same steps, because the same multiples of the same polynomials show up again and again.

F4 collects a whole batch of pairs first. It writes all the polynomials it might need, for the whole batch, as rows of one big table of coefficients, one column per monomial. Then it cleans up the whole table at once, with the same elimination used to solve linear equations. Rows that end up with a new leading term are the new results. Doing the work as one big elimination is much faster than many small divisions.

## The problem

Let $K$ be a field and $R = K[x_1, \ldots, x_n]$, with a monomial order $>$ such as lex, grlex or grevlex, and $x_1 > \cdots > x_n$. For $f \ne 0$, $\operatorname{LT}(f)$, $\operatorname{LM}(f)$ and $\operatorname{LC}(f)$ are its leading term, monomial and coefficient. Write $d$ for the largest degree of an input polynomial, $t$ for the number of terms, and $M(d)$ for the cost of multiplying polynomials of degree $d$; the analysis below is in terms of the matrix sizes instead.

**Input:** polynomials $f_1, \ldots, f_s \in R$ and the order $>$.

**Output:** the [reduced Gröbner basis](/reduced-groebner-basis/) of $I = \langle f_1, \ldots, f_s \rangle$ for $>$.

For a finite set $H$ of polynomials, the *Macaulay matrix* of $H$ has one row per polynomial and one column per monomial occurring in $H$, sorted by $>$ in decreasing order; its row echelon form $\tilde N$ is a basis of the span of $H$ with distinct leading monomials. A pair $(g_i, g_j)$ of basis elements has the halves $(\operatorname{lcm}/\operatorname{LM}(g_i))\, g_i$ and $(\operatorname{lcm}/\operatorname{LM}(g_j))\, g_j$, where $\operatorname{lcm} = \operatorname{lcm}(\operatorname{LM}(g_i), \operatorname{LM}(g_j))$, and its S-polynomial is a combination of them.

## The algorithm

```pseudo id=main
F4(F, >)                            ▷ F = (f_1, ..., f_s) in K[x_1, ..., x_n]
L1  G ← [], P ← []; for f in F, f ≠ 0: UPDATE(G, P, f)          ▷ Gebauer-Möller pair update
L2  while P ≠ ∅ do
L3      δ ← the smallest total degree of lcm(i, j) for (i, j) ∈ P; P_δ ← those pairs; P ← P \ P_δ
L4      L ← the halves (lcm/LM(g_i)) g_i and (lcm/LM(g_j)) g_j of the pairs in P_δ
L5      H ← SYMBOLIC-PREPROCESSING(L, G)    ▷ add u g for every monomial m of H with LM(g) | m
L6      Ñ ← row echelon form of the Macaulay matrix of H
L7      Ñ⁺ ← {h ∈ Ñ : LM(h) ∉ LM(H)}
L8      for h in Ñ⁺: UPDATE(G, P, h)
L9  return the reduced basis of G
```

SYMBOLIC-PREPROCESSING keeps a set of monomials already handled, initialized with $\operatorname{LM}(L)$. While some monomial $m$ of a row of $H$ is not handled, it marks $m$ as handled and, if $\operatorname{LM}(g)$ divides $m$ for some $g \in G$, appends the reducer $(m/\operatorname{LM}(g))\, g$ to $H$. UPDATE is the procedure of the [Gebauer-Möller criteria](/gebauer-moller-criteria/), which removes pairs covered by Buchberger's product and chain criteria. Choosing the pairs of lowest lcm degree is the *normal strategy*; with it, F4 on a homogeneous input computes the basis degree by degree.

## Example

Let $I = \langle x^2 + y^2 - 4,\ xy - 1 \rangle \subseteq \mathbb{Q}[x, y]$ with grevlex and $x > y$, a circle and a hyperbola. Call the generators $g_1$ and $g_2$. UPDATE keeps the single pair $(g_1, g_2)$, with lcm $x^2 y$. The trace, from the implementation:

| round | $\delta$ | rows of $H$ | columns | $\tilde N^+$ | pairs after UPDATE |
|---|---|---|---|---|---|
| 1 | 3 | $y g_1 = x^2y + y^3 - 4y$, $x g_2 = x^2y - x$ | $x^2y, y^3, x, y$ | $g_3 = y^3 + x - 4y$ | $(g_2, g_3)$; $(g_1, g_3)$ is coprime |
| 2 | 4 | $y^2 g_2$, $x g_3$, reducers $g_1$ (for $x^2$) and $g_2$ (for $xy$) | $xy^3, x^2, xy, y^2, 1$ | empty | none |

In round 1 the difference of the two rows is $y^3 + x - 4y$, whose leading monomial $y^3$ is not a leading monomial of $H$, so it is new. In round 2 the matrix is $4 \times 5$ and its echelon form has leading monomials $xy^3, x^2, xy$ and one more row that reduces to zero, all already leading monomials of $H$; so the S-polynomial of $(g_2, g_3)$ reduces to zero and nothing is added. The reduced basis is $\{xy - 1,\ x^2 + y^2 - 4,\ y^3 + x - 4y\}$.

For larger inputs the effect of batching shows in the matrix sizes. On the Katsura system $x + 2y + 2z - 1$, $x^2 + 2y^2 + 2z^2 - x$, $2xy + 2yz - y$ in grevlex, the implementation needs three rounds with matrices of sizes $6 \times 10$, $7 \times 10$ and $11 \times 13$.

## Correctness

The full proof is in the correctness file. Every row of $H$ is a monomial multiple of an element of $G$, so the new elements lie in $I$. Symbolic preprocessing guarantees that every monomial of $H$ divisible by a leading monomial of $G$ is the leading monomial of some row. From this, every polynomial in the span of $H$, and in particular each S-polynomial of the selected pairs, reduces to zero by $G \cup \tilde N^+$. A new element $h$ has a leading monomial divisible by no element of $\operatorname{LM}(G)$, so the monomial ideal $\langle \operatorname{LM}(G) \rangle$ grows strictly with each addition, and by Dickson's lemma only finitely many additions occur. When $P$ is empty, every pair has either been reduced to zero or been removed by the Gebauer-Möller criteria, and Buchberger's criterion shows that $G$ is a Gröbner basis.

## Complexity

The cost model is operations in $K$ on a Blum-Shub-Smale machine; over $\mathbb{Q}$ the bit cost also depends on coefficient growth, which is not bounded here.

- **One round, proved.** An $r \times c$ matrix is reduced by Gaussian elimination in $O(r c \min(r, c))$ operations, and less when it is sparse. Symbolic preprocessing costs only monomial operations, no field operations.
- **Whole run, worst case.** No bound specific to F4 is known that is better than the general one. Gröbner bases of ideals generated in degree $d$ can need degree $d^{2^{\Theta(n)}}$ (Mayr and Meyer 1982), so the matrices can be doubly exponential in $n$, and so can the time. The upper bound of the same shape follows from Dubé's degree bound $2(d^2/2 + d)^{2^{n-1}}$ for reduced Gröbner bases.
- **Better cases.** For zero-dimensional ideals the cost of computing a Gröbner basis is single exponential, $d^{O(n)}$ (Lakshman 1991); for homogeneous zero-dimensional ideals in generic coordinates, the grevlex basis has degree at most $n(d - 1) + 1$ (Lazard 1983). For homogeneous regular sequences in grevlex, the degrees are bounded by the Macaulay bound $\sum_i (d_i - 1) + 1$, and the matrices have at most $\binom{n + D}{n}$ columns for that degree $D$. The known complexity bounds in this setting are proved for F5 and the matrix version of Lazard; for F4 they are observed rather than proved.
- **Space.** The largest matrix dominates, $O(r c)$ field elements in a dense representation and the number of nonzero entries in a sparse one.
- **In practice.** The matrices are very sparse and have a block structure: the reducer rows already have distinct pivots, so most of the elimination is a triangular solve. Faugère's implementations exploit this, and over finite fields this step is the bulk of the time.

## Properties

- **Exact and deterministic.** The result is the reduced Gröbner basis, the same for any selection strategy.
- **Generalizes Buchberger.** If each round selects only one pair, F4 is Buchberger's algorithm with a particular choice of reducers; with the normal strategy it reduces all pairs of the lowest degree together.
- **Linear algebra step is replaceable.** Any method that computes a row echelon basis of the span of $H$ can be used, including sparse, structured and modular elimination.
- **Not signature-based.** F4 still computes reductions to zero, visible as zero rows of the echelon form. [F5](/f5-algorithm/) avoids most of them.

## Variants and improvements

- **Simplify.** Faugère's version replaces a reducer $u g$ by $u' g'$, where $g'$ is a row computed in an earlier round with $\operatorname{LM}(g') \mid u\, \operatorname{LM}(g)$, so that earlier eliminations are reused. The implementation here omits it.
- **Modular F4.** Over $\mathbb{Q}$, run F4 modulo several primes and reconstruct the result by Chinese remaindering and rational reconstruction, with a check at the end. This avoids the growth of rational coefficients.
- **Sugar degree.** For inhomogeneous input, selecting by the [sugar](/sugar-strategy/) degree instead of the lcm degree imitates the homogeneous computation and often gives smaller matrices.
- **Linear algebra.** Faugère and Lachartre (2010) designed a dedicated elimination for F4 matrices over finite fields that exploits their block structure; later implementations such as those in Magma and msolve use similar ideas.
- **F4 with signatures.** Combining the matrix formulation with signature criteria gives matrix versions of F5, such as F4/5 and the Matrix-F5 of Bardet, Faugère and Salvy.

## When to use it

Use F4 for large Gröbner basis computations over finite fields or over $\mathbb{Q}$ through modular methods, especially in grevlex for zero-dimensional systems that are then converted with [FGLM](/fglm-algorithm/). For small inputs, Buchberger's algorithm with the Gebauer-Möller criteria is simpler and just as fast. When the input is a regular sequence and many reductions to zero would occur, prefer a signature-based algorithm.

## Pitfalls

- **Preprocessing must be complete.** Every monomial of every row, including the monomials of the added reducers, must be checked. Missing one leaves a row whose new leading monomial is divisible by $\operatorname{LM}(G)$, and the termination argument fails.
- **Leading monomials of the halves.** The halves are already multiples of elements of $G$, so their leading monomials are marked as handled at the start. Adding another reducer with the same leading monomial is not wrong, but it only enlarges the matrix.
- **Selecting new elements.** Only rows with leading monomials outside $\operatorname{LM}(H)$ are new. Adding every row of $\tilde N$ to $G$ is correct but floods the basis and the pair list with redundant elements.
- **Degree selection in lex.** The normal strategy uses the total degree of the lcm, which is not compatible with lex; the result is still correct, but the number of rounds can be large.
- **Coefficient growth.** Exact rational elimination on large matrices is slow. Real implementations work modulo primes.

## Implementations

## History

Lazard (1983) observed that a Gröbner basis can be read from the row echelon form of a Macaulay matrix of large enough degree, linking Buchberger's algorithm with linear algebra. Faugère turned this into a practical algorithm: F4 (1999) builds the matrices on demand from the critical pairs instead of taking all multiples up to a degree. It was followed by F5 (2002), and F4 became the core of the Gröbner basis engines of Magma and Maple, and later of open implementations such as msolve.

## References
