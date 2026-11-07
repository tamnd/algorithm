---
tag: 4X5MRR
kind: algorithm
slug: hermite-reduction
name: Hermite reduction
aliases:
- Hermite's method
- Hermite reduction for rational functions
- Mack's linear Hermite reduction
area: algebra/computer-algebra
level: core
summary: Separates the rational part of an integral from a remaining integrand with square-free denominator.
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the denominator D}
  time: {worst: O(n^3), best: O(n^2)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [integration-of-rational-functions, polynomial-gcd, square-free-factorization, partial-fraction-decomposition]
see_also: [horowitz-ostrogradsky, rothstein-trager, lazard-rioboo-trager, risch-algorithm, symbolic-integration, yun-square-free-factorization, half-gcd, creative-telescoping]
sources:
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Section 2.2 (the Hermite reduction, the original version and Mack's linear version HermiteReduce), with Section 2.3 for Horowitz-Ostrogradsky
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 22.2 (Hermite's method), with the cost analysis there
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 11 (integration of rational functions), the sections on Hermite's method and the Horowitz reduction
  - paper: "Charles Hermite, Sur l'intégration des fractions rationnelles, Nouvelles Annales de Mathématiques, 2e série, 11, 145-148, 1872"
    locator: the original reduction of a rational integral to one with a squarefree denominator
---

Hermite reduction takes a rational function $A/D$ over a field $K$ of characteristic zero and writes

$$\frac{A}{D} = \left(\frac{G_n}{G_d}\right)' + \frac{a}{d}, \qquad d \text{ squarefree},\ \deg a < \deg d,$$

using only polynomial arithmetic and gcds in $K[x]$, never factoring $D$. Then $\int A/D = G_n/G_d + \int a/d$: the first part is the whole *rational part* of the integral, and the second has only simple poles, so its integral is a sum of logarithms, found by [Rothstein-Trager](/rothstein-trager/) or [Lazard-Rioboo-Trager](/lazard-rioboo-trager/). The version below is Mack's linear variant as given by Bronstein, Section 2.2. It needs $O(n)$ gcd and extended gcd computations for $\deg D = n$, and it is the first step of [rational function integration](/integration-of-rational-functions/) and, in generalized form, of the [Risch algorithm](/risch-algorithm/).

## In plain words

To integrate a fraction of polynomials, the hard part comes from repeated factors in the bottom. A factor that appears squared or cubed produces terms in the answer that are again fractions, while factors that appear once produce logarithms. Hermite's idea is to strip the repeated factors one power at a time.

At each step the method writes the current fraction as the derivative of a simpler fraction plus a remainder whose bottom has one power less of every repeated factor. It does this by solving a small equation between polynomials with the Euclidean algorithm. When no factor is repeated any more, the derivative pieces add up to the fraction part of the answer, and what is left integrates to logarithms.

## The problem

**Input:** polynomials $A, D \in K[x]$ with $D \ne 0$, where $K$ is a field of characteristic 0, such as $\mathbb{Q}$.

**Output:** a rational function $g \in K(x)$ and polynomials $a, d$ with $d$ squarefree and $\deg a < \deg d$, such that $A/D = g' + a/d$.

The decomposition is unique in the following sense. If $A/D$ is proper and the denominator of $g$ divides $\gcd(D, D')$ with a proper $g$, then $g$ and $a/d$ are unique (Bronstein, Section 2.2; von zur Gathen and Gerhard, Section 22.2). Uniqueness holds because a derivative of a proper rational function has no simple poles, while $a/d$ has only simple poles. The cost is counted in operations in $K$.

## The algorithm

Write $D^- = \gcd(D, D')$ and $D^* = D / D^-$. If $D = \prod_i D_i^{\,i}$ is the [squarefree factorization](/square-free-factorization/), then $D^- = \prod_i D_i^{\,i-1}$ and $D^* = \prod_i D_i$, the product of the distinct irreducible factors. Each pass replaces $D^-$ by $\gcd(D^-, (D^-)')$, which lowers every exponent by one.

```pseudo id=main
HERMITE-REDUCE(A, D)                       ▷ D ≠ 0; K of characteristic 0
L1  (P, A) ← (quo(A, D), rem(A, D)); g ← ∫ P dx
L2  D⁻ ← gcd(D, D′); D* ← D / D⁻
L3  while deg D⁻ > 0 do
L4      D⁻⁻ ← gcd(D⁻, D⁻′); D⁻* ← D⁻ / D⁻⁻
L5      solve B · (−D* D⁻′ / D⁻) + C · D⁻* = A for B, C with deg B < deg D⁻*
L6      A ← C − B′ D* / D⁻*
L7      g ← g + B / D⁻
L8      D⁻ ← D⁻⁻
L9  return (g, A / D*)
```

Line L1 removes the polynomial part, which is integrated term by term. Line L2 computes the gcd with the derivative once. In each pass, $D^{-*}$ is the product of the factors that still occur in $D^-$ (line L4). Line L5 is one extended Euclidean computation: $D^{-*}$ and $D^* (D^-)' / D^-$ are coprime, so $B$ and $C$ exist and are unique under the degree bound. Lines L6 and L7 move $(B / D^-)'$ out of the integrand. The gcds are monic, so the loop ends with $D^- = 1$.

## Example

Take $A = x^7 - 24x^4 - 4x^2 + 8x - 8$ and $D = x^8 + 6x^6 + 12x^4 + 8x^2 = x^2 (x^2 + 2)^3$ over $\mathbb{Q}$. Since $\deg A < \deg D$, line L1 leaves $A$ and sets $g = 0$. Line L2 gives $D^- = x (x^2 + 2)^2 = x^5 + 4x^3 + 4x$ and $D^* = x^3 + 2x$.

| pass | $D^-$ | $D^{-*}$ (L4) | $-D^* D^{-\prime}/D^-$ | $B$, $C$ (L5) | new $A$ (L6) | added to $g$ (L7) |
|---|---|---|---|---|---|---|
| 1 | $x(x^2+2)^2$ | $x^3 + 2x$ | $-5x^2 - 2$ | $8x^2 + 4$, $x^4 - 2x^2 + 16x + 4$ | $x^4 - 2x^2 + 4$ | $\dfrac{8x^2 + 4}{x(x^2+2)^2}$ |
| 2 | $x^2 + 2$ | $x^2 + 2$ | $-2x^2$ | $3$, $x^2 + 2$ | $x^2 + 2$ | $\dfrac{3}{x^2 + 2}$ |

After pass 2, $D^- = 1$, and line L9 returns $a/d = (x^2 + 2)/(x^3 + 2x) = 1/x$ and

$$g = \frac{8x^2 + 4}{x(x^2 + 2)^2} + \frac{3}{x^2 + 2} = \frac{3x^3 + 8x^2 + 6x + 4}{x(x^2 + 2)^2}.$$

So $\int A/D\,dx = \dfrac{3x^3 + 8x^2 + 6x + 4}{x(x^2+2)^2} + \ln x$. The test file checks the returned $g$ and $a/d$, and checks that $g' + 1/x = A/D$ by differentiation.

## Correctness

The invariant of the loop of line L3 is

$$\frac{A_{\text{in}}}{D} = g' + \frac{A}{D^* D^-}, \qquad \deg A < \deg (D^* D^-).$$

It holds after line L2 because $D^* D^- = D$ and $g = \int P$. A pass keeps it: with $A = B F + C D^{-*}$ for $F = -D^* D^{-\prime}/D^-$, a direct computation gives $\frac{A}{D^* D^-} - \left(\frac{B}{D^-}\right)' = \frac{C - B' D^*/D^{-*}}{D^* D^{--}}$, which is the new $A$ over the new $D^* D^-$. When the loop stops, $D^- = 1$ and $D^*$ is squarefree. The loop stops because each pass lowers the largest multiplicity in $D^-$ by one. The full proof, with the coprimality that line L5 needs, is in the proof file below.

## Complexity

The cost model is operations in $K$, on the [BSS model](/blum-shub-smale-machine/); for $K = \mathbb{Q}$ the bit cost also depends on the growth of the coefficients, which is polynomial but not bounded here. Let $n = \deg D$ and let $m$ be the largest multiplicity of a factor of $D$.

- **Passes.** The loop runs $m - 1 \le n - 1$ times. If $D$ is squarefree it does not run at all, and the cost is the one gcd of line L2, $O(n^2)$ with the classical Euclidean algorithm. This is the best case.
- **One pass.** Each pass does one gcd, one extended gcd and a few products and exact divisions of polynomials of degree at most $n$, so $O(n^2)$ operations with classical arithmetic.
- **Total.** So the implementation here uses $O(m n^2) \subseteq O(n^3)$ field operations, a proved bound. It is reached in order for $D = x^n$, where every pass works with polynomials of degree about $n - k$.
- **Fast arithmetic.** With fast multiplication $M(n)$ and the [half-gcd](/half-gcd/) algorithm, von zur Gathen and Gerhard (Section 22.2) bound Hermite reduction by $O(M(n) \log n)$ operations in $K$, by computing the squarefree factorization with [Yun's algorithm](/yun-square-free-factorization/) and then solving one equation per squarefree factor.

The space is $O(n)$ field elements for the polynomials alive at any time, plus the output.

## Properties

- **No factorization.** Only gcds, exact divisions and extended gcds in $K[x]$ are used, so everything stays in $K$; no algebraic numbers appear in the rational part.
- **Linear in A.** For fixed $D$, the map $A \mapsto (g, a)$ is $K$-linear, since each step solves linear equations whose coefficients depend only on $D$.
- **Rational part is complete.** The integral of $a/d$ with $d$ squarefree and $a/d$ proper has no rational part: it is a sum of $c \ln(x - \alpha)$ over the roots $\alpha$ of $d$. So $g$ is the whole rational part of $\int A/D$.
- **Exact.** Over $\mathbb{Q}$ every step is exact rational arithmetic.

## Variants and improvements

- **Hermite's original version.** Compute the squarefree factorization $D = \prod D_i^{\,i}$ first, split $A/D$ by partial fractions over the $D_i^{\,i}$, and reduce each $A_i / D_i^{\,i}$ by one power at a time, with an extended gcd of $D_i$ and $D_i'$ (Bronstein, Section 2.2). Its cost is quadratic in $n$ when done with care; it needs the full squarefree factorization.
- **Mack's linear version.** The version above, which avoids partial fractions and works with $D^-$ and $D^*$ throughout.
- **[Horowitz-Ostrogradsky](/horowitz-ostrogradsky/).** Write $A/D = (B/D^-)' + C/D^*$ with unknown coefficients of $B$ and $C$ and solve one linear system of size $n$. It is simple, and the tests use it as an independent oracle, but the system costs $O(n^3)$ with Gaussian elimination.
- **Generalizations.** Hermite reduction works in any differential field for the *normal* part of the denominator, which is how the [Risch algorithm](/risch-algorithm/) handles denominators in transcendental extensions (Bronstein, Chapter 5). Reductions of the same kind are used for algebraic functions (Trager's integral bases) and, as *Hermite-type reductions*, in [creative telescoping](/creative-telescoping/).

## When to use it

Use Hermite reduction as the first step of every rational function integration: it finds the rational part with gcds only, and leaves a squarefree denominator for the logarithmic part. It is also the right tool when only the rational part is wanted, for example to decide whether an integral of a rational function is rational, which holds exactly when $a = 0$.

## Pitfalls

- **Characteristic zero.** The method relies on $\gcd(D, D')$ to find repeated factors. In characteristic $p$, $D' $ can be 0, as for $D = x^p$, and the reduction fails.
- **Polynomial part.** Line L1 is needed: the degree bound of line L5 only makes sense for proper fractions, and the polynomial part must be integrated separately.
- **The output is not reduced.** The returned $a/d$ can have common factors; in the example, $(x^2 + 2)/(x^3 + 2x)$ is $1/x$. Cancel before the logarithmic part, or the Rothstein-Trager resultant has spurious roots.
- **Monic gcds.** If the gcds are not made monic, the loop ends with a constant $D^- \ne 1$ that must be divided out of the final answer.
- **Coefficient growth.** Over $\mathbb{Q}$ intermediate coefficients grow. Modular or fraction-free versions of the extended gcd keep the growth down; see [expression swell](/expression-swell/).

## Implementations

## History

Ostrogradsky (1845) and Hermite (1872) both showed how to find the rational part of the integral of a rational function without factoring the denominator: Ostrogradsky by the linear system now named after him and Horowitz, Hermite by a reduction one power at a time. Horowitz (1971) analyzed both for computer algebra. Mack (1975) gave the linear version that does not need partial fractions, and Bronstein's book presents it as the standard form. Hermite reduction is the first step of rational integration in all major computer algebra systems.

## References
