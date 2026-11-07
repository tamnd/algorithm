---
tag: PFW69P
kind: problem
slug: integration-of-rational-functions
name: Integration of rational functions
aliases:
- rational function integration
- antiderivative of a rational function
- symbolic integration of rational functions
area: algebra/computer-algebra
level: core
summary: Find antiderivatives of rational functions, which are always rational plus logarithmic terms.
model: blum-shub-smale-machine
prereqs: [partial-fraction-decomposition, square-free-factorization, resultant]
see_also: [hermite-reduction, horowitz-ostrogradsky, rothstein-trager, lazard-rioboo-trager, liouville-theorem, risch-algorithm, subresultant-prs, indefinite-summation]
sources:
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 2, Integration of rational functions (Sections 2.1 to 2.8, from the Bernoulli method and Hermite reduction through Horowitz-Ostrogradsky, Rothstein-Trager, Lazard-Rioboo-Trager and Rioboo's real form)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 22, Symbolic integration (Hermite's method and the method of Lazard, Rioboo, Rothstein and Trager, with cost analyses)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 11, Integration of rational functions
  - paper: doi:10.1145/800205.806338
    title: Barry M. Trager, Algebraic factoring and rational function integration, SYMSAC 1976
    locator: the resultant method for the logarithmic part and the minimality of its constant field
  - paper: doi:10.1145/800204.806290
    title: Ellis Horowitz, Algorithms for partial fraction decomposition and rational function integration, SYMSAM 1971
    locator: the rational part by one linear system
---

Integration of rational functions asks for an antiderivative of $A/D \in K(x)$, where $K$ is a field of characteristic $0$, such as $\mathbb{Q}$. The answer always has the form of a rational function plus a sum of constant multiples of logarithms, $\int A/D = R + \sum_i c_i \log v_i$. The rational part $R$ lies in $K(x)$ and can be found with rational operations alone. The logarithmic part may need an algebraic extension of $K$, and the problem is to find the smallest such extension without factoring $D$ over $\overline{K}$. The methods of Hermite, [Horowitz and Ostrogradsky](/horowitz-ostrogradsky/), [Rothstein and Trager](/rothstein-trager/), and [Lazard, Rioboo and Trager](/lazard-rioboo-trager/) solve it with gcds, [resultants](/resultant/) and linear algebra. It is the base case of the [Risch algorithm](/risch-algorithm/).

## In plain words

Calculus courses integrate a fraction of polynomials by splitting it into simple pieces and integrating each piece. The pieces with a repeated factor in the bottom give fractions, and the pieces with a simple factor give logarithms. The catch is that the textbook method needs every root of the bottom polynomial, and the roots may be ugly algebraic numbers. A computer algebra system avoids roots. It finds the fraction part with gcds and division alone. For the logarithm part, it computes one auxiliary polynomial whose roots are exactly the constants in front of the logarithms. It then works only with numbers that actually appear in the answer, which is often far less than the full set of roots.

## Definition

Notation: $K$ is a field of characteristic $0$, $\overline{K}$ its algebraic closure, and $'$ is $d/dx$ on $K(x)$. Polynomials are in $K[x]$, $d = \deg D$, and $M(d)$ is the cost of multiplying two polynomials of degree $d$.

**Input.** Polynomials $A, D \in K[x]$ with $D \ne 0$ and $\gcd(A, D) = 1$.

**Output.** A polynomial $P \in K[x]$, polynomials $B, E \in K[x]$, finitely many distinct nonzero constants $c_1, \ldots, c_m \in \overline{K}$ and polynomials $v_1, \ldots, v_m \in K(c_1, \ldots, c_m)[x]$ such that

$$\frac{A}{D} = P' + \left(\frac{B}{E}\right)' + \sum_{i=1}^{m} c_i \frac{v_i'}{v_i}.$$

Then $\int A/D = P + B/E + \sum_i c_i \log v_i$.

**Structure of the answer.** Write $D^- = \gcd(D, D')$ and $D^* = D / D^-$, the square-free part of $D$. After removing the polynomial part, $\int A/D = B/D^- + \int C/D^*$ with $\deg B < \deg D^-$ and $\deg C < \deg D^*$, and $B$, $C$ are unique (Ostrogradsky's formula). The integral $\int C/D^*$ has a square-free denominator and is purely logarithmic. Its constants $c_i$ are the residues $C(\alpha)/D^{*\prime}(\alpha)$ at the roots $\alpha$ of $D^*$.

**Minimal extension.** The theorem of Rothstein and Trager says the residues are the roots of

$$Q(t) = \operatorname{res}_x\bigl(D^*, \; C - t\, D^{*\prime}\bigr) \in K[t],$$

that the logarithmic part can be written over $K(c_1, \ldots, c_m)$ where $c_1, \ldots, c_m$ are the distinct roots of $Q$, and that no smaller extension of $K$ suffices. For each root $c$ the argument of the logarithm is $v_c = \gcd(D^*, C - c\, D^{*\prime})$.

## Variants

- **Rational part only.** Compute $P$ and $B/D^-$ and leave $\int C/D^*$ unevaluated. [Hermite reduction](/hermite-reduction/) and the [Horowitz-Ostrogradsky method](/horowitz-ostrogradsky/) do this with operations in $K$ only.
- **Logarithmic part with algebraic constants.** Return $\sum_{Q_j(c) = 0} c \log S_j(c, x)$, a formal sum over the roots of each square-free factor $Q_j$ of $Q$. This is what the [Lazard-Rioboo-Trager](/lazard-rioboo-trager/) algorithm returns.
- **Real form.** For $K \subseteq \mathbb{R}$, write the answer with real logarithms and arctangents instead of complex logarithms. Rioboo's algorithm avoids arctangents of rational functions with spurious poles, so the real antiderivative is continuous wherever the integrand is (Bronstein, Section 2.8).
- **Full splitting.** Factor $D$ over $\overline{K}$ and integrate each term of the [partial fraction decomposition](/partial-fraction-decomposition/). This is the Bernoulli method. It is correct but may introduce many more algebraic numbers than the answer needs.
- **Definite integrals.** Evaluate an antiderivative at the endpoints. This needs care: a discontinuous antiderivative, such as an arctangent with a pole, gives wrong values across the pole.

## Examples

**A rational and a logarithmic part.** The [partial fraction decomposition](/partial-fraction-decomposition/) of the integrand is

$$\frac{x^5 + 2}{(x - 1)^2 (x^2 + 1)} = x + 2 + \frac{3/2}{(x - 1)^2} + \frac{1}{x - 1} + \frac{x - 1/2}{x^2 + 1},$$

so

$$\int \frac{x^5 + 2}{(x - 1)^2 (x^2 + 1)} \, dx = \frac{x^2}{2} + 2x - \frac{3/2}{x - 1} + \log(x - 1) + \frac{1}{2} \log(x^2 + 1) - \frac{1}{2} \arctan x.$$

Here $D^- = x - 1$, the rational part is $-\tfrac{3}{2}/(x - 1)$, and the logarithmic part has $D^* = (x - 1)(x^2 + 1)$ and $C = 2x^2 - \tfrac{3}{2} x + \tfrac{3}{2}$. The Rothstein-Trager resultant is a constant multiple of $(t - 1)(16 t^2 - 16 t + 5)$. The root $t = 1$ gives $\log(x - 1)$. The quadratic factor gives $\sum_{16 c^2 - 16 c + 5 = 0} c \log\bigl(x - 1/(2 - 4c)\bigr)$, and for $c = \tfrac{1}{2} \pm \tfrac{i}{4}$ the argument is $x \mp i$. In real form this pair is the $\tfrac{1}{2} \log(x^2 + 1) - \tfrac{1}{2} \arctan x$ above.

**An extension is necessary.** For $1/(x^2 - 2)$ over $\mathbb{Q}$, $Q(t) = \operatorname{res}_x(x^2 - 2, 1 - 2tx) = 1 - 8t^2$. Its roots $\pm \sqrt{2}/4$ are irrational, so

$$\int \frac{dx}{x^2 - 2} = \frac{\sqrt{2}}{4} \log\bigl(x - \sqrt{2}\bigr) - \frac{\sqrt{2}}{4} \log\bigl(x + \sqrt{2}\bigr),$$

and by the Rothstein-Trager theorem no antiderivative of this form exists over $\mathbb{Q}$.

**No extension is needed, though $D$ does not split.** For $1/(x^3 + x)$ the residues are $1$ at $0$ and $-\tfrac{1}{2}$ at $\pm i$. So $Q$ has the rational roots $1$ and $-\tfrac{1}{2}$, and $\gcd\bigl(x^3 + x, 1 + \tfrac{1}{2}(3x^2 + 1)\bigr) = x^2 + 1$. The answer is $\log x - \tfrac{1}{2} \log(x^2 + 1)$, with no $i$ in sight, although the Bernoulli method would compute with $\mathbb{Q}(i)$.

## Known algorithms

| algorithm | computes | operations used | cost |
|---|---|---|---|
| Bernoulli | everything | factorization of $D$ over $\overline{K}$ | needs the roots of $D$ |
| [Hermite reduction](/hermite-reduction/) | $P$ and $B/D^-$, and $C/D^*$ | [square-free factorization](/square-free-factorization/), extended Euclid | $O(d^2)$ in $K$ classically, proved |
| [Horowitz-Ostrogradsky](/horowitz-ostrogradsky/) | $B/D^-$ and $C/D^*$ | one linear system of size $d$ | $O(d^3)$ in $K$ by Gaussian elimination, proved |
| [Rothstein-Trager](/rothstein-trager/) | $\int C/D^*$ | a resultant, factorization of $Q$ over $K$, gcds over $K(c)$ | polynomial in $d$ plus the cost of factoring $Q$ |
| [Lazard-Rioboo-Trager](/lazard-rioboo-trager/) | $\int C/D^*$ | the [subresultant PRS](/subresultant-prs/) of $D^*$ and $C - tD^{*\prime}$, square-free factorization of $Q$ | polynomial in $d$, no factorization and no arithmetic in $K(c)$ |
| Czichowski | $\int C/D^*$ | a lex [Gröbner basis](/groebner-basis/) of $\langle D^*, C - tD^{*\prime} \rangle$ | same output as Lazard-Rioboo-Trager |

Von zur Gathen and Gerhard (Chapter 22) analyse Hermite reduction with fast arithmetic in $O(M(d) \log d)$ operations in $K$ and give polynomial bounds for the Lazard-Rioboo-Trager method in operations and, over $\mathbb{Q}$, in word operations.

## Bounds

- **Form of the answer.** By [Liouville's theorem](/liouville-theorem/), or directly from partial fractions, every antiderivative of a rational function is rational plus a linear combination of logarithms. No new exponentials or other functions are ever needed.
- **Degrees.** In the Ostrogradsky form, $\deg B < \deg D^-$ and $\deg C < \deg D^*$, and $\deg Q \le \deg D^*$, so the number $m$ of distinct logarithmic constants is at most $\deg D^*$.
- **Size of the constant field.** The extension $K(c_1, \ldots, c_m)$ is the splitting field of $Q$ and is the smallest possible, by the Rothstein-Trager theorem. It can be large. For $1/(x^p - 2)$ with $p$ prime, the residues are $\alpha/(2p)$ over the roots $\alpha$ of $x^p - 2$, so the field is the splitting field of $x^p - 2$, of degree $p(p - 1)$ over $\mathbb{Q}$. This is why practical systems return formal sums over the roots of the square-free factors of $Q$ instead of explicit algebraic numbers.
- **Coefficient growth.** Over $\mathbb{Q}$ the resultant $Q$ can have much larger coefficients than $A$ and $D$, and the bit cost is dominated by the subresultant computation. The polynomial bounds are proved; practical speed comes from modular and subresultant techniques.

## Reductions

- **To partial fractions and gcds.** The rational part reduces to a [square-free factorization](/square-free-factorization/) and one [partial fraction decomposition](/partial-fraction-decomposition/) with respect to it.
- **To resultants and subresultants.** The logarithmic part reduces to the resultant $Q(t)$ and to the [subresultant](/subresultant/) of the right index for each square-free factor of $Q$.
- **Into the Risch algorithm.** For a tower $K(x, \theta_1, \ldots, \theta_k)$ of elementary extensions, the [Risch algorithm](/risch-algorithm/) generalizes Hermite reduction and the Rothstein-Trager resultant to each level. Rational integration is the case $k = 0$.
- **Discrete analogue.** Rational [indefinite summation](/indefinite-summation/) has the same structure, with the shift $x \mapsto x + 1$ replacing $d/dx$ and Abramov's method replacing Hermite reduction.

## Applications

- Every computer algebra system integrates rational functions this way. The answer is exact and has the smallest algebraic extension.
- The rational case is the base case of integration of elementary functions by the [Risch algorithm](/risch-algorithm/).
- Inverse Laplace transforms, residue computations and closed forms of definite integrals all rest on the same partial fraction and residue computations.

## References
