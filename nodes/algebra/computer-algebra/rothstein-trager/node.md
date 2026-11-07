---
tag: 2HTAE6
kind: algorithm
slug: rothstein-trager
name: Rothstein-Trager algorithm
aliases: [Rothstein-Trager method, Rothstein-Trager resultant, Rothstein-Trager theorem]
area: algebra/computer-algebra
level: advanced
summary: Computes the logarithmic part of a rational integral from the resultant of the denominator and a log-derivative equation.
solves: [integration-of-rational-functions]
model: blum-shub-smale-machine
complexity:
  vars: {n: "the degree of D, at least 1"}
  time: {worst: O(n^5)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [resultant, polynomial-gcd, square-free-factorization, partial-fraction-decomposition]
see_also: [integration-of-rational-functions, hermite-reduction, lazard-rioboo-trager, horowitz-ostrogradsky, liouville-theorem, risch-algorithm, subresultant-prs, symbolic-integration]
sources:
  - paper: doi:10.1145/800205.806338
    title: Barry M. Trager, Algebraic factoring and rational function integration, Proceedings of the third ACM Symposium on Symbolic and Algebraic Computation (SYMSAC 1976)
    locator: pp. 219 to 226 (the resultant for the logarithmic part and the minimal field of constants)
  - paper: "Michael Rothstein, Aspects of symbolic integration and simplification of exponential and primitive functions, PhD thesis, University of Wisconsin, Madison, 1976"
    locator: the resultant method for the logarithmic part, found independently of Trager
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 2, Integration of Rational Functions (the Rothstein-Trager theorem and algorithm, and the Lazard-Rioboo-Trager improvement)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 22, Symbolic integration (the method of Lazard, Rioboo, Rothstein and Trager)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 11, Integration of Rational Functions (the logarithmic part)
  - paper: doi:10.1016/S0747-7171(08)80026-0
    title: Daniel Lazard and Renaud Rioboo, Integration of rational functions, rational computation of the logarithmic part, Journal of Symbolic Computation 9(2), 1990
    locator: pp. 113 to 115
---

The Rothstein-Trager algorithm finds the logarithmic part of $\int A/D \, dx$ for a rational function with a squarefree denominator, without the roots of $D$. It forms one resultant $R(z) = \operatorname{res}_x(D, A - z D')$, whose roots are exactly the residues of $A/D$, and for each root $c$ it takes $\gcd(D, A - c D')$ as the argument of the logarithm with coefficient $c$. The only algebraic numbers in the answer are roots of $R$, and Trager proved that no smaller extension of the constants is enough. It is the second half of rational integration, after [Hermite reduction](/hermite-reduction/), and the base case of the logarithmic part of the [Risch algorithm](/risch-algorithm/).

## In plain words

To integrate a fraction of polynomials, the school method splits it into simple fractions, one for each root of the bottom polynomial. Each simple fraction gives a logarithm with a constant in front. But the roots can be ugly numbers, and many of them are not needed: when two roots have the same constant, their two logarithms join into one logarithm of a polynomial with nicer numbers.

Rothstein and Trager found a way to get the constants without the roots. One polynomial, built from the top and the bottom of the fraction, has exactly these constants as its roots. For each constant, a greatest common divisor gives the polynomial inside the logarithm. So the answer uses only the numbers that it really needs.

## The problem

**Notation.** $K$ is a field of characteristic $0$, in the implementation $\mathbb{Q}$, and $\overline{K}$ is an algebraic closure. $A, D \in K[x]$ with $D$ squarefree, $n = \deg D \ge 1$ and $\deg A < n$. $D'$ is the derivative, and $\operatorname{LC}$ is the leading coefficient. $R(z) = \operatorname{res}_x(D, A - z D') \in K[z]$ is the resultant with the formal degrees $n$ and $n - 1$, in the [Sylvester matrix](/sylvester-matrix/) convention of the [resultant](/resultant/) page. For a root $\alpha$ of $D$, the *residue* of $A/D$ at $\alpha$ is $r_\alpha = A(\alpha) / D'(\alpha)$.

**Input.** $A$ and $D$, as above. A general rational function is first brought to this form by polynomial division and [Hermite reduction](/hermite-reduction/), see [integration of rational functions](/integration-of-rational-functions/).

**Output.** Pairs $(q_i, S_i)$ with $q_i \in K[z]$ monic and squarefree and $S_i \in (K[z]/(q_i))[x]$ monic in $x$, such that

$$\int \frac{A}{D} \, dx = \sum_i \; \sum_{c \in \overline{K}, \; q_i(c) = 0} c \log S_i(c, x).$$

A pair with $\deg q_i = 1$ is a plain term $c \log v(x)$ with $c \in K$ and $v \in K[x]$.

**The theorem.** $R(z) = \operatorname{LC}(D)^{n-1} \prod_{D(\alpha) = 0} D'(\alpha) \cdot \prod_{D(\alpha) = 0} (r_\alpha - z)$. So $\deg R = n$, the roots of $R$ are the residues, and

$$\int \frac{A}{D} \, dx = \sum_{c \ne 0, \; R(c) = 0} c \log \gcd(D, A - c D'),$$

where the sum is over the distinct roots of $R$ and the gcds are monic. The proof is in the correctness file. Trager also showed that $K(c_1, \ldots, c_k)$, generated by the nonzero roots of $R$, is the smallest extension of $K$ over which the integral can be written as a sum of constant multiples of logarithms (Trager 1976; Bronstein, Chapter 2).

## The algorithm

The classical form factors $R$ into irreducible factors $q_i$ over $K$ and computes $\gcd(D, A - z D')$ in the field $K[z]/(q_i)$. The form below does not factor $R$. It removes the rational roots, takes the squarefree part of the rest, and runs the Euclidean algorithm in the ring $K[z]/(q)$. When a leading coefficient has no inverse, the extended gcd that fails to invert it gives a proper factor of $q$, and $q$ splits. This is the dynamic evaluation idea of Della Dora, Dicrescenzo and Duval.

```pseudo id=main
ROTHSTEIN-TRAGER(A, D)          ▷ D squarefree, deg A < deg D = n
L1  R(z) ← res_x(D, A − z·D′)                  ▷ formal degrees n and n − 1
L2  for each rational root c of R, with c ≠ 0 do
L3      v ← monic gcd(D, A − c·D′); output (z − c, v)
L4  q ← squarefree part of R without its rational roots, made monic
L5  stack ← [q] if deg q > 0; while stack is not empty, pop q do
L6      try S ← monic gcd(D, A − z·D′) in (K[z]/(q))[x]
L7      on a leading coefficient u with no inverse: g ← monic gcd(u, q); push g and q/g; next q
L8      output (q, S)
```

Line L1 is one resultant in $K[z]$. The implementation evaluates it at $z = 0, 1, \ldots, n$ and interpolates, which is valid because $\deg R \le n$. Line L2 uses the rational root test over $\mathbb{Q}$. It only makes the output nicer, because it turns rational residues into plain logarithms; without it, lines L4 to L8 still give a correct answer. The root $c = 0$ is skipped because its term is $0 \cdot \log(\ldots)$. Line L4 makes every root of $q$ simple and drops the roots already handled. In line L6, every element of $K[z]/(q)$ is a polynomial in $z$ of degree less than $\deg q$, and each division step needs the inverse of a leading coefficient, found by the [extended Euclidean algorithm](/extended-euclidean-algorithm/) in $K[z]$. Line L7 handles the case where this extended gcd ends with a nonconstant $g = \gcd(u, q)$: the roots of $g$ are the residues where the remainder sequence changes, and both parts are pushed for a new pass.

## Example

**A quadratic field.** For $\int dx/(x^2 - 2)$, $A = 1$ and $D = x^2 - 2$, so $A - z D' = 1 - 2 z x$ and $R(z) = 1 - 8 z^2$. There is no rational root. $q = z^2 - 1/8$, and the gcd of $x^2 - 2$ and $1 - 2 z x$ in $(\mathbb{Q}[z]/(q))[x]$ is $S = x - 4z$. The roots of $q$ are $c = \pm \sqrt{2}/4$, so

$$\int \frac{dx}{x^2 - 2} = \frac{\sqrt 2}{4} \log(x - \sqrt 2) - \frac{\sqrt 2}{4} \log(x + \sqrt 2).$$

**A rational root and a complex pair.** Take $D = (x - 1)(x^2 + 1) = x^3 - x^2 + x - 1$ and $A = 2x^2 - \tfrac{3}{2} x + \tfrac{3}{2}$. This is the logarithmic part of the example on [integration of rational functions](/integration-of-rational-functions/).

| Line | Work | Result |
|---|---|---|
| L1 | $\operatorname{res}_x(D, A - z(3x^2 - 2x + 1))$ | $R = -16 z^3 + 32 z^2 - 21 z + 5 = -(z - 1)(16 z^2 - 16 z + 5)$ |
| L2 | rational roots of $R$ | $c = 1$ |
| L3 | $A - D' = -(x - 1)(x + \tfrac{1}{2})$, gcd with $D$ | output $(z - 1, \; x - 1)$ |
| L4 | $R / (z - 1)$, squarefree, monic | $q = z^2 - z + \tfrac{5}{16}$ |
| L6 | gcd of $D$ and $(2 - 3z) x^2 + (2z - \tfrac{3}{2}) x + (\tfrac{3}{2} - z)$ mod $q$ | $S = x + 2 - 4z$ |
| L8 | no zero divisor | output $(q, \; x + 2 - 4z)$ |

The roots of $q$ are $c = \tfrac{1}{2} \pm \tfrac{i}{4}$, and $S(c, x) = x \mp i$. So

$$\int \frac{A}{D} \, dx = \log(x - 1) + \Big(\tfrac{1}{2} + \tfrac{i}{4}\Big) \log(x - i) + \Big(\tfrac{1}{2} - \tfrac{i}{4}\Big) \log(x + i) = \log(x - 1) + \tfrac{1}{2} \log(x^2 + 1) - \tfrac{1}{2} \arctan x,$$

up to a constant. The derivative of the right side is $1/(x - 1) + (x - \tfrac{1}{2})/(x^2 + 1) = A/D$.

**A split at line L7.** Take $D = (x^4 - 2)(x^2 - 3)$ and $A = 6x^4 + 8x^3 - 24x - 12$, so that $A/D = 8x/(x^4 - 2) + 6/(x^2 - 3)$. Each root of $x^4 - 2$ has residue $\pm\sqrt 2$, and each root of $x^2 - 3$ has residue $\pm\sqrt 3$. Then $R$ is a constant times $(z^2 - 2)^2 (z^2 - 3)$, with no rational root, and $q = z^4 - 5z^2 + 6$. In the Euclidean algorithm modulo $q$, the fifth leading coefficient to invert is $u = (183924244 z^3 + 238833840 z^2 - 367848488 z - 477667680)/1216609$, which is $(z^2 - 2)$ times a unit. So $\gcd(u, q) = z^2 - 2$ and $q$ splits. The two new passes give $(z^2 - 3, \; x - z)$ and $(z^2 - 2, \; x^2 - z)$, that is

$$\int \frac{A}{D} \, dx = \sum_{c^2 = 3} c \log(x - c) + \sum_{c^2 = 2} c \log(x^2 - c).$$

The gcd degree is 1 at $\pm\sqrt 3$ and 2 at $\pm\sqrt 2$, so one gcd over all of $\mathbb{Q}[z]/(q)$ cannot exist, and the split is necessary. The large fractions in $u$ show the coefficient growth in the algebraic extension.

## Correctness

The proof is in the correctness file. It has three steps. First, the product formula for resultants gives $R(z) = \operatorname{LC}(D)^{n-1} \prod_\alpha (A(\alpha) - z D'(\alpha))$, and $D'(\alpha) \ne 0$ because $D$ is squarefree, so the roots of $R$ are the residues $r_\alpha$. Second, over a splitting field, $A/D = \sum_\alpha r_\alpha/(x - \alpha)$ by [partial fractions](/partial-fraction-decomposition/), and $\gcd(D, A - c D') = \prod_{r_\alpha = c} (x - \alpha)$, because $\alpha$ is a root of $A - c D'$ exactly when $r_\alpha = c$. Grouping the logarithms by their residues gives the theorem. Third, for the ring $K[z]/(q)$ with $q$ squarefree: if every leading coefficient is invertible, then evaluation at each root $c$ of $q$ is a ring homomorphism that keeps the degrees of all remainders, so it maps the remainder sequence to the remainder sequence of $D$ and $A - c D'$, and $S(c, x) = \gcd(D, A - c D')$. A split gives two coprime factors whose roots partition the roots of $q$.

## Complexity

**Cost model.** Operations in $K$ (additions, multiplications and divisions in $\mathbb{Q}$, each of unit cost), with $n = \deg D$. Line L2 is not a field operation and is counted apart.

- **Line L1.** $R$ has degree at most $n$, so $n + 1$ values of the resultant are enough. Each value is a determinant of order $2n - 1$, $O(n^3)$ operations by elimination, so the implementation uses $O(n^4)$. With the Euclidean algorithm for each value it is $O(n^3)$, and with a fast Euclidean algorithm $O(n \, M(n) \log n)$.
- **Line L3.** At most $n$ gcds in $K[x]$ of degree at most $n$: $O(n^3)$.
- **Line L4.** One squarefree part of a polynomial of degree at most $n$: $O(n^2)$.
- **Lines L5 to L8.** A pass with $k = \deg q$ does $O(n^2)$ operations in $K[z]/(q)$, each $O(k^2)$ in $K$ with schoolbook arithmetic and inverses by the extended Euclidean algorithm, so $O(n^2 k^2)$. Each split makes two factors of positive degree, so there are at most $\deg q - 1 < n$ splits and at most $2n$ passes, each with $k \le n$. This gives $O(n^5)$.

So the bound $O(n^5)$ operations in $K$ is proved by this count, for the lines other than L2. It is a worst case. In practice there are few splits, and the cost is dominated by the gcd in the largest extension.

**Line L2 over $\mathbb{Q}$.** The rational root test tries $p/q$ with $p$ dividing the constant and $q$ dividing the leading coefficient of the squarefree part, which is exponential in their length. A polynomial-time alternative is to take the linear factors from a [factorization](/polynomial-factorization/) of $R$ over $\mathbb{Q}$.

**Bit size over $\mathbb{Q}$.** The page does not bound the size of the coefficients. The coefficients of $R$ are determinants, so the [Hadamard bound](/hadamard-bound/) limits them, but the remainders in $K[z]/(q)$ can grow fast, as the split example shows. This growth is the main practical cost, and it is what the [Lazard-Rioboo-Trager](/lazard-rioboo-trager/) algorithm removes.

**Space.** The Sylvester matrix has $O(n^2)$ entries; the other data are $O(n)$ polynomials of degree $O(n)$ in $x$ and $z$.

## Properties

- **Minimal constants.** The output uses only roots of $R$, and by Trager's theorem no proper subfield of $K(c_1, \ldots, c_k)$ is enough. A method that factors $D$ over its splitting field can need an extension of degree up to $n!$; here each term uses an extension of degree at most $n$, the degree of its $q_i$.
- **Exact.** Every step is a rational operation in $K$ or in $K[z]/(q)$. There is no numerical root finding.
- **No factorization of $D$.** $D$ is never factored. In the form above, $R$ is not factored either, except for its linear factors over $\mathbb{Q}$.
- **Output is not canonical.** The split form returns pairwise coprime $q_i$ that need not be irreducible. Two runs that split in a different order give the same sum but can group it differently.
- **Deterministic.** No random choices.

## Variants and improvements

- **Classical form.** Factor $R$ into irreducibles $q_i$ over $K$ and compute each gcd in the field $K[z]/(q_i)$. This is Trager's form. It needs factorization in $K[z]$, which is polynomial time over $\mathbb{Q}$ in bit operations but is not available in every field.
- **Lazard-Rioboo-Trager.** [Lazard-Rioboo-Trager](/lazard-rioboo-trager/) computes the [subresultant PRS](/subresultant-prs/) of $D$ and $A - z D'$ in $K[z][x]$ once. With the squarefree factorization $R = \prod_i Q_i^i$, the subresultant of degree $i$, made primitive, gives $S_i$ for all roots of $Q_i$, with no arithmetic in an extension. This is the form in modern systems.
- **Real form.** For $K \subseteq \mathbb{R}$, a pair of complex conjugate terms $c \log S + \bar c \log \bar S$ can be rewritten with $\log$ of a real polynomial and $\arctan$ terms. Rioboo's algorithm does this with arctangents of polynomials, which avoids jumps in the result that a direct rewriting can bring in (Bronstein, Chapter 2).
- **Czichowski.** A [Gröbner basis](/groebner-basis/) of the ideal generated by $D$ and $A - z D'$ in lex order gives the same pairs.
- **Transcendental extensions.** The [Risch algorithm](/risch-algorithm/) uses the same resultant, with $x$ replaced by a monomial $\theta$ and the derivation of the extension, to find the logarithmic part and to decide if it exists with constant residues.

## When to use it

Use it for the logarithmic part after [Hermite reduction](/hermite-reduction/), when the answer must be exact and the logarithms must use the smallest algebraic extension. It is also the clearest way to state and prove what the logarithmic part is. For large inputs over $\mathbb{Q}$, prefer [Lazard-Rioboo-Trager](/lazard-rioboo-trager/), which gives the same answer without arithmetic in $K[z]/(q)$. When only numerical values are needed, a partial fraction expansion over approximate roots is simpler.

## Pitfalls

- **Non-squarefree $D$.** If $D$ has a repeated root, $D'$ vanishes there, and the residue formula and the theorem fail. Run [Hermite reduction](/hermite-reduction/) or [square-free factorization](/square-free-factorization/) first.
- **$\deg A \ge \deg D$.** The polynomial part must be removed first; otherwise $A/D$ is not a sum of simple fractions and the formal degree $n - 1$ for $A - z D'$ is wrong.
- **The formal degree.** $\deg(A - z D')$ is $n - 1$ for general $z$ but can be smaller for one value of $z$. Build the Sylvester matrix with the formal degree $n - 1$, or $R$ can be wrong by a factor or miss a root.
- **Common factors of $A$ and $D$.** They give the root $z = 0$ of $R$, with the term $0 \cdot \log$. Skip it, or cancel $\gcd(A, D)$ first.
- **Assuming a field.** $K[z]/(q)$ is a field only when $q$ is irreducible. Without factoring $q$, every inverse can fail and must split $q$, as at line L7. Testing invertibility only at the end gives wrong answers.
- **Coefficient growth.** The arithmetic modulo $q$ over $\mathbb{Q}$ makes large fractions. Reduce modulo $q$ after each product, and expect the cost to be dominated by these sizes.

## Implementations

## History

Johann Bernoulli integrated rational functions by partial fractions, which needs all the roots of the denominator. Hermite (1872) found the rational part without roots, and so the logarithmic part of a squarefree denominator remained. Michael Rothstein, in his 1976 thesis at Wisconsin, and Barry Trager, in his SYMSAC 1976 paper, found independently that the residues are the roots of $\operatorname{res}_x(D, A - z D')$ and that gcds give the logarithms. Trager also proved that the extension it uses is the smallest possible. Rothstein used the same resultant for logarithmic and exponential extensions, which became part of the [Risch algorithm](/risch-algorithm/) in Bronstein's treatment. Lazard and Rioboo (1990), and Trager in unpublished work, removed the arithmetic in algebraic extensions with subresultants.

## References
