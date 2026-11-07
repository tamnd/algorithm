---
tag: KX6NMH
kind: algorithm
slug: horowitz-ostrogradsky
name: Horowitz-Ostrogradsky method
aliases:
- Horowitz method
- Ostrogradsky method
- Ostrogradsky-Hermite method
area: algebra/computer-algebra
level: advanced
summary: Computes the rational part of a rational integral by solving a linear system for undetermined coefficients.
solves: [integration-of-rational-functions]
model: blum-shub-smale-machine
complexity:
  vars: {d: the degree of the denominator D}
  time: {worst: O(d^3)}
  space: {extra: O(d^2)}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  year: 1845
  people: [Mikhail Ostrogradsky, Ellis Horowitz]
  note: Ostrogradsky showed in 1845 that the rational part of the integral of a rational function can be found without factoring, by undetermined coefficients; Horowitz analysed it as an algorithm in 1971 and compared it with Hermite reduction.
prereqs: [integration-of-rational-functions, polynomial-gcd, square-free-factorization, gaussian-elimination]
see_also: [hermite-reduction, rothstein-trager, lazard-rioboo-trager, partial-fraction-decomposition, risch-algorithm, liouville-theorem, square-free-polynomial, linear-system-solving]
sources:
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 2, Integration of rational functions, Section 2.3 (the Horowitz-Ostrogradsky algorithm, with the linear system and its uniqueness), next to Section 2.2 (Hermite reduction)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 11, Integration of rational functions (Hermite's method and Horowitz's method for the rational part)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 22, Symbolic integration (Hermite reduction and the cost of computing the rational part)
  - paper: "Ellis Horowitz, Algorithms for partial fraction decomposition and rational function integration, Proceedings of the Second ACM Symposium on Symbolic and Algebraic Manipulation, 1971"
    locator: the method of undetermined coefficients for the rational part and its cost
  - paper: "Mikhail Ostrogradsky, De l'intégration des fractions rationnelles, Bulletin de la classe physico-mathématique de l'Académie Impériale des Sciences de Saint-Pétersbourg 4, 1845"
    locator: the decomposition of the integral into a rational part and an integral with square-free denominator
---

The Horowitz-Ostrogradsky method splits the integral of a proper rational function $A/D$ over a field $K$ of characteristic $0$ into a rational part and a part with a square-free denominator:
$$\int \frac{A}{D}\, dx = \frac{B}{D^-} + \int \frac{C}{D^*}\, dx, \qquad D^- = \gcd(D, D'), \quad D^* = D / D^-.$$
Both denominators come from one gcd, so no factorization is needed. The numerators $B$ and $C$, with $\deg B < \deg D^-$ and $\deg C < \deg D^*$, have $\deg D$ unknown coefficients in all. Clearing denominators turns the equation into a square linear system for them, and the system always has exactly one solution. The remaining integral has only simple poles, so its antiderivative is purely logarithmic, and the [Rothstein-Trager](/rothstein-trager/) or [Lazard-Rioboo-Trager](/lazard-rioboo-trager/) algorithm finishes the job. [Hermite reduction](/hermite-reduction/) computes the same $B$ and $C$ with gcd steps instead of a linear system.

## In plain words

A rational function such as $1/(x^2 + 1)^2$ has an integral with two kinds of pieces. One piece is again a fraction, here $x / (2(x^2 + 1))$. The other piece is a logarithm or an arctangent, here $\tfrac{1}{2} \arctan x$. The fraction piece comes from the repeated factors of the denominator. Ostrogradsky noticed that you can predict the denominators of both pieces with a gcd, without factoring anything. Then you write the unknown numerators with letters for their coefficients, differentiate, compare coefficients, and solve the linear equations you get. What is left to integrate has no repeated factors in the denominator, and that part needs logarithms.

## The problem

**Input.** A field $K$ of characteristic $0$, such as $\mathbb{Q}$, and $A, D \in K[x]$ with $D \ne 0$ and $\deg A < \deg D$. A polynomial part, if any, is removed first by [polynomial division](/polynomial-long-division/) and integrated termwise.

**Output.** $B, C \in K[x]$ with $\deg B < \deg D^-$ and $\deg C < \deg D^*$ such that
$$\frac{A}{D} = \left( \frac{B}{D^-} \right)' + \frac{C}{D^*},$$
where $D^- = \gcd(D, D')$ is taken monic and $D^* = D / D^-$. The polynomial $D^*$ is square-free.

## The algorithm

Let $n = \deg D^-$ and $m = \deg D^*$, so $n + m = \deg D = d$. Multiplying the output equation by $D = D^- D^*$ gives the polynomial identity
$$A = B' D^* - B E + C D^-, \qquad E = \frac{D^* \, (D^-)'}{D^-},$$
where $E$ is a polynomial of degree less than $m$. Each side has degree less than $d$, so comparing the coefficients of $x^0, \ldots, x^{d-1}$ gives $d$ linear equations in the $d$ unknown coefficients of $B$ and $C$.

```pseudo id=main
HOROWITZ-OSTROGRADSKY(A, D)            ▷ deg A < deg D, char K = 0
L1  D⁻ ← gcd(D, D')                              ▷ monic
L2  D* ← D / D⁻                                  ▷ exact division, square-free
L3  n ← deg D⁻;  m ← deg D*
L4  B ← Σ_{i<n} b_i x^i;  C ← Σ_{j<m} c_j x^j   ▷ d = n + m unknowns
L5  set up the d × d system: coefficients of B' D* − B E + C D⁻ equal those of A
L6  solve the system for b_0, ..., b_{n−1}, c_0, ..., c_{m−1}
L7  return B / D⁻ and C / D*
```

Line L5 builds the matrix column by column: the column of $b_i$ holds the coefficients of $i x^{i-1} D^* - x^i E$, and the column of $c_j$ those of $x^j D^-$. Line L6 uses [Gaussian elimination](/gaussian-elimination/). The theorem in the correctness section says the matrix is nonsingular.

## Example

Take $A = 1$ and $D = (x^2 + 1)^2 = x^4 + 2x^2 + 1$ over $\mathbb{Q}$.

| line | result |
|---|---|
| L1 | $D' = 4x^3 + 4x$, $D^- = \gcd(D, D') = x^2 + 1$ |
| L2 | $D^* = D / D^- = x^2 + 1$, and $E = D^* (D^-)' / D^- = 2x$ |
| L3 | $n = 2$, $m = 2$ |
| L4 | $B = b_0 + b_1 x$, $C = c_0 + c_1 x$ |
| L5 | $B' D^* - B E + C D^- = c_1 x^3 + (c_0 - b_1) x^2 + (c_1 - 2 b_0) x + (b_1 + c_0)$, which must equal $1$: $c_1 = 0$, $c_0 - b_1 = 0$, $c_1 - 2b_0 = 0$, $b_1 + c_0 = 1$ |
| L6 | $b_0 = 0$, $b_1 = \tfrac{1}{2}$, $c_0 = \tfrac{1}{2}$, $c_1 = 0$ |
| L7 | $\displaystyle \int \frac{dx}{(x^2 + 1)^2} = \frac{x}{2(x^2 + 1)} + \frac{1}{2} \int \frac{dx}{x^2 + 1}$ |

The remaining integral is $\tfrac{1}{2} \arctan x$, or a sum of logarithms over $\mathbb{Q}(i)$. A second example: for $A = x^2$ and $D = (x - 1)^2 (x^2 + 1)$, $D^- = x - 1$, $D^* = x^3 - x^2 + x - 1$, $B = -\tfrac{1}{2}$ and $C = \tfrac{1}{2}(x + 1)$. Both examples are checked by differentiation in the tests.

## Correctness

Two facts about characteristic $0$ carry the proof. First, if $D = c \prod_i p_i^{e_i}$ with distinct monic irreducible $p_i$, then $D^- = \prod_i p_i^{e_i - 1}$ and $D^* = c \prod_i p_i$, so $D^*$ is square-free and $E$ is a polynomial. Second, differentiating a fraction whose reduced denominator contains $p^k$, $k \ge 1$, gives a reduced denominator containing exactly $p^{k+1}$. So $(B / D^-)'$ can never equal $-C / D^*$, whose denominator is square-free, unless $B = 0$. This makes the linear map $(B, C) \mapsto B' D^* - B E + C D^-$ injective between two spaces of dimension $d$, hence bijective, and the system has exactly one solution for each $A$. The full proof is in the proof file below.

## Complexity

The cost model counts arithmetic operations in $K$, as on a [BSS machine](/blum-shub-smale-machine/) over $K$, with classical polynomial arithmetic. Let $d = \deg D$. These bounds are proved:

- **Lines L1 and L2.** The Euclidean gcd and one exact division cost $O(d^2)$ operations.
- **Line L5.** The $d$ columns cost $O(d^2)$ operations in all, since each is a product of a monomial with a polynomial of degree less than $d$.
- **Line L6.** Gaussian elimination on a dense $d \times d$ system costs $O(d^3)$ operations and $O(d^2)$ space.

So the total is $O(d^3)$ operations and $O(d^2)$ extra space. Over $\mathbb{Q}$ the entries of the matrix are small, but the elimination can produce large intermediate fractions, which this count does not see. A fraction-free or modular solver bounds the bit cost. Hermite reduction computes the same output with $O(d^2)$ operations, and with fast arithmetic in $O(M(d) \log d)$ (von zur Gathen and Gerhard, Chapter 22). In practice the linear system is usually not the bottleneck for small $d$. That is an observation, not a theorem.

## Properties

- **No factorization.** Only one gcd, one division and one linear solve over $K$ are needed, and everything stays in $K$.
- **Unique output.** For each $A$ there is exactly one pair $(B, C)$ with the degree bounds. So the rational part is well defined, and every method returns the same $B / D^-$.
- **Rational part is all of the algebraic part.** If $C = 0$, the integral is the rational function $B / D^-$. Otherwise the integral is not rational, since $\int C / D^*$ with $C \ne 0$ and square-free $D^*$ has a logarithmic singularity at some root of $D^*$.

## Variants and improvements

- **Hermite reduction.** Use the [square-free factorization](/square-free-factorization/) of $D$ and the extended Euclidean algorithm to reduce the multiplicity of each factor step by step. It is faster, $O(d^2)$ classically, and is the standard choice.
- **Structured solving.** The columns of the matrix are shifted copies of the coefficient vectors of $D^*$, $E$ and $D^-$, as in a [Sylvester matrix](/sylvester-matrix/), so structured linear algebra can solve it faster than dense elimination.
- **Fraction-free or modular solving.** Over $\mathbb{Q}$, solve the system with fraction-free elimination or by a [modular method](/modular-methods/) to control coefficient growth.
- **The logarithmic part.** Pass $C / D^*$ to [Rothstein-Trager](/rothstein-trager/) or [Lazard-Rioboo-Trager](/lazard-rioboo-trager/), which find the logarithms over the smallest possible algebraic extension.

## When to use it

Use it when a linear solver is readily available and the degree is small, or when a single linear system is easier to implement and to parallelize than the sequence of gcds of Hermite reduction. It is also a clean way to explain why the rational part needs no factoring. For large degree, Hermite reduction is faster. Both need characteristic $0$, or at least characteristic larger than $\deg D$.

## Pitfalls

- **An improper fraction.** If $\deg A \ge \deg D$, the system is not square: divide first and integrate the polynomial part separately.
- **Positive characteristic.** In characteristic $p$, $\gcd(D, D')$ can be all of $D$, for example $D = x^p - a$, and the decomposition fails.
- **Not making $D^-$ monic.** Any constant multiple works for the identity, but the constant must be used consistently in $E$ and in the returned fraction $B / D^-$.
- **Forgetting that $E$ is a polynomial.** Computing $(D^-)'/D^-$ as a fraction and then multiplying by $D^*$ introduces rational functions into the system. Divide $D^* (D^-)'$ by $D^-$ exactly instead.
- **Coefficient growth.** Plain Gaussian elimination over $\mathbb{Q}$ on large systems is slow because of the fractions. See the variants.

## Implementations

## History

Ostrogradsky published the method in 1845. He showed that the rational part of the integral can be computed from $\gcd(D, D')$ and undetermined coefficients, without finding the roots of $D$. Hermite gave his reduction in 1872. Horowitz, in his 1971 paper and thesis, analysed both as algorithms, and the combined name comes from his presentation. Bronstein, Chapter 2, and Geddes, Czapor and Labahn, Chapter 11, give the modern form used here.

## References
