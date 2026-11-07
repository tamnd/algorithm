---
tag: KJ9098
kind: algorithm
slug: rational-univariate-representation
name: Rational univariate representation
aliases: [RUR, Rouillier's rational univariate representation, rational parametrization of a zero-dimensional system]
area: algebra/computer-algebra
level: advanced
summary: Expresses all solutions of a zero-dimensional system as rational functions of one root of a univariate polynomial.
solves: [polynomial-system-solving]
model: blum-shub-smale-machine
complexity:
  vars: {D: "the dimension of K[x]/I as a vector space, at least 1", n: "the number of variables"}
  time: {worst: O(n D^6)}
  space: {extra: O(D^3)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [groebner-basis, normal-form, characteristic-polynomial, square-free-factorization]
see_also: [polynomial-system-solving, fglm-algorithm, lazard-structure-theorem, triangular-decomposition, real-root-isolation, groebner-basis-conversion, elimination-theorem, hilbert-nullstellensatz]
sources:
  - paper: doi:10.1007/s002000050114
    title: Fabrice Rouillier, Solving zero-dimensional systems through the rational univariate representation, Applicable Algebra in Engineering, Communication and Computing 9(5), 1999
    locator: pp. 433 to 461 (the definition, the trace formulas and the test for a separating element)
  - paper: "Leopold Kronecker, Grundzüge einer arithmetischen Theorie der algebraischen Grössen, Journal für die reine und angewandte Mathematik 92, 1882"
    locator: the representation of the solutions by a primitive element and a linear form
  - paper: doi:10.1007/978-1-4612-2752-6_15
    title: Paul Pedersen, Marie-Françoise Roy and Aviva Szpirglas, Counting real zeros in the multivariate case, Computational Algebraic Geometry, Progress in Mathematics 109, Birkhäuser, 1993
    locator: pp. 203 to 224 (the trace form and its rank and signature)
  - paper: doi:10.1006/jcom.2000.0571
    title: Marc Giusti, Grégoire Lecerf and Bruno Salvy, A Gröbner free alternative for polynomial system solving, Journal of Complexity 17(1), 2001
    locator: pp. 154 to 211 (the geometric resolution, a Kronecker representation computed without Gröbner bases)
  - paper: doi:10.1007/s00200-003-0133-5
    title: Alin Bostan, Bruno Salvy and Éric Schost, Fast algorithms for zero-dimensional polynomial systems using duality, Applicable Algebra in Engineering, Communication and Computing 14(4), 2003
    locator: pp. 239 to 272
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 12, Polynomial System Solving (univariate representations and the trace form)
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, fourth edition, Springer, 2015
    locator: Chapter 5, Section 3 (the normal set and the finiteness theorem used in step L1)
---

The rational univariate representation (RUR) of a zero-dimensional system of polynomial equations is one univariate polynomial $\bar f(T)$ and $n + 1$ polynomials $g_1, g_{x_1}, \ldots, g_{x_n}$ such that the solutions are exactly the points $(g_{x_1}(t) / g_1(t), \ldots, g_{x_n}(t) / g_1(t))$ for the roots $t$ of $\bar f$. Rouillier (1999) computes it with linear algebra in the quotient ring, from traces of multiplication matrices, so the coefficients stay small compared with a lexicographic Gröbner basis and multiplicities are kept.

## In plain words

A system of several polynomial equations with finitely many solutions can be hard to read. A rational univariate representation turns it into one equation in one unknown, plus a recipe. Solve the single equation, and for each of its roots the recipe gives the full solution of the system, one coordinate at a time, as a fraction of two polynomials evaluated at that root.

The single unknown is a fixed combination of the original unknowns, chosen so that different solutions give different values. The method finds it by trying simple combinations until a count shows that no two solutions share a value. All the work is linear algebra on a finite table that describes multiplication modulo the equations, so it can be done exactly with fractions.

## The problem

**Notation.** $K$ is a field of characteristic $0$, here $K = \mathbb{Q}$, with algebraic closure $\overline{K}$. $I \subseteq K[x_1, \ldots, x_n]$ is an ideal with finitely many zeros $V(I) \subset \overline{K}^n$ (a *zero-dimensional* ideal), and $A = K[x_1, \ldots, x_n] / I$ is the quotient ring, a $K$-vector space of finite dimension $D$. For $\alpha \in V(I)$, $\mu(\alpha) \ge 1$ is its multiplicity, the dimension of the local ring of $A$ at $\alpha$, and $\sum_\alpha \mu(\alpha) = D$. Grevlex is the monomial order used for the Gröbner basis, and $\mathrm{LM}$ is the leading monomial.

**Separating forms.** A linear form $u = \sum_i \lambda_i x_i$ is *separating* if $u(\alpha) \ne u(\beta)$ for all distinct $\alpha, \beta \in V(I)$.

**Output.** For a separating $u$, the RUR is

- $f_u(T) = \prod_{\alpha \in V(I)} (T - u(\alpha))^{\mu(\alpha)}$, the characteristic polynomial of multiplication by $u$ on $A$, and its squarefree part $\bar f_u(T) = \prod_{\alpha} (T - u(\alpha))$, of degree $d = |V(I)|$;
- for each $v \in A$, $g_v(T) = \sum_{\alpha} \mu(\alpha)\, v(\alpha) \prod_{\beta \ne \alpha} (T - u(\beta))$, of degree less than $d$, for $v = 1, x_1, \ldots, x_n$.

Then $V(I) = \left\{ \left( \frac{g_{x_1}(t)}{g_1(t)}, \ldots, \frac{g_{x_n}(t)}{g_1(t)} \right) : \bar f_u(t) = 0 \right\}$, and $g_1(u(\alpha)) / \bar f_u'(u(\alpha)) = \mu(\alpha)$. All these polynomials have coefficients in $K$, although the points $\alpha$ need not.

## The algorithm

Let $B$ be the normal set of $I$ for grevlex: the monomials not divisible by any $\mathrm{LM}(g)$, $g$ in the Gröbner basis. It is a basis of $A$. $M_v$ is the $D \times D$ matrix of multiplication by $v$ on $A$ in the basis $B$, and $\operatorname{Tr}(v) = \operatorname{tr}(M_v)$.

```pseudo id=main
RUR(F)                                              ▷ F generates a zero-dimensional I in K[x_1..x_n]
L1  G ← reduced Gröbner basis of (F) for grevlex;  B ← normal set;  D ← |B|
L2  M_i ← matrix of x_i on A in basis B, from the normal forms of x_i·b, b in B
L3  r ← rank of the Hermite matrix (Tr(b·c)) for b, c in B          ▷ r = |V(I)|
L4  for λ = 0, 1, 2, ... do
L5      u ← x_1 + λ x_2 + ... + λ^(n-1) x_n;  M_u ← Σ λ^(i-1) M_i
L6      s_j ← tr(M_u^j) for j = 0..D;  f_u ← polynomial with power sums s_j (Newton identities)
L7      f̄ ← f_u / gcd(f_u, f_u'), made monic;  d ← deg f̄
L8      if d = r then exit the loop                                  ▷ u is separating
L9  for v in 1, x_1, ..., x_n: g_v ← Σ_{j<d} Tr(v·u^j) H_{d-1-j}(T)
L10 return (u, f̄, g_1, g_{x_1}, ..., g_{x_n})
```

In L9, $H_k(T) = \sum_{m=0}^{k} a_{d-m} T^{k-m}$ are the Horner polynomials of $\bar f = \sum_{i=0}^{d} a_i T^i$, and $\operatorname{Tr}(v u^j) = \operatorname{tr}(M_v M_u^j)$ uses the powers of $M_u$ from L6. If $D = 0$ the ideal is the unit ideal, there are no zeros, and the output is $\bar f = 1$ with zero polynomials $g$. If some variable has no pure power among the leading monomials, $I$ is not zero-dimensional and L1 stops with an error.

## Example

**Distinct values for $u = x$.** Let $F = \{x^2 + y^2 - 5, \; x y - 2\}$ over $\mathbb{Q}$, with zeros $(1, 2)$, $(2, 1)$, $(-1, -2)$, $(-2, -1)$. Then $D = 4$, the Hermite rank is $r = 4$, and at $\lambda = 0$, $u = x$ takes four distinct values. The output is

$$\bar f = T^4 - 5T^2 + 4, \quad g_1 = 4T^3 - 10T, \quad g_x = 10T^2 - 16, \quad g_y = 8T^2 - 20.$$

At the root $t = 2$: $g_1(2) = 12$, $g_x(2) = 24$ and $g_y(2) = 12$, so the point is $(2, 1)$. At $t = 1$: $g_1 = -6$, $g_x = -6$, $g_y = -12$, so the point is $(1, 2)$. Since the ideal is radical, $g_1 = \bar f'$, and $g_x \equiv T g_1 \pmod{\bar f}$, as it must be for $u = x$.

**Trials for $\lambda$.** Let $F = \{x^2 - 1, \; y^2 - 1\}$, with the four zeros $(\pm 1, \pm 1)$, so $r = 4$.

| $\lambda$ | $u$ | values of $u$ | $d$ | separating |
|---|---|---|---|---|
| $0$ | $x$ | $1, 1, -1, -1$ | $2$ | no |
| $1$ | $x + y$ | $2, 0, 0, -2$ | $3$ | no |
| $2$ | $x + 2y$ | $3, -1, 1, -3$ | $4$ | yes |

The output at $\lambda = 2$ is $\bar f = T^4 - 10 T^2 + 9$, $g_1 = 4T^3 - 20T$, $g_x = 4T^2 + 12$, $g_y = 8T^2 - 24$. At $t = 1$: $g_1 = -16$, $g_x = 16$, $g_y = -16$, so the point is $(-1, 1)$, and indeed $u(-1, 1) = 1$.

**A multiple zero.** For $F = \{x^2, \; y - x\}$, $D = 2$ but $V(I) = \{(0, 0)\}$, so $r = 1$. At $\lambda = 0$, $f_u = T^2$ and $\bar f = T$, and the output is $g_1 = 2$, $g_x = g_y = 0$. The point is $(0, 0)$, and $g_1(0) / \bar f'(0) = 2$ is its multiplicity.

The implementation reproduces all three outputs exactly.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It rests on Stickelberger's theorem: the eigenvalues of $M_v$ on $A$ are the values $v(\alpha)$, each with algebraic multiplicity $\mu(\alpha)$, so $\operatorname{Tr}(v) = \sum_\alpha \mu(\alpha) v(\alpha)$. From it, $f_u$ in L6 is $\prod (T - u(\alpha))^{\mu(\alpha)}$, the rank of the Hermite form in L3 is $|V(I)|$, so L8 accepts exactly the separating forms, and the trace formula in L9 equals the defining sum for $g_v$. At most $(n - 1) \binom{r}{2}$ values of $\lambda$ fail, so the loop ends.

## Complexity

Cost model: operations in $K$ (unit cost, as on a [Blum-Shub-Smale machine](/blum-shub-smale-machine/)), counted after the Gröbner basis and the multiplication matrices are known. Over $\mathbb{Q}$ each operation costs a number of bit operations that grows with the size of the numbers, which is not bounded here.

| Step | Operations in $K$ | Bound |
|---|---|---|
| L3: matrices $M_b$ for $b \in B$ and the Hermite matrix | $O(D^4)$ | proved |
| L5 to L7, per value of $\lambda$: powers $M_u^j$, traces, Newton identities, squarefree part | $O(D^4)$ | proved |
| number of values of $\lambda$ | at most $(n - 1) \binom{D}{2} + 1$ | proved |
| L9: traces $\operatorname{tr}(M_v M_u^j)$ and Horner sums | $O(n D^3)$ | proved |
| total | $O(n D^6)$ in the worst case, $O(D^4 + n D^3)$ when few trials are needed | proved; few trials observed |

The bound on the trials holds because, for two distinct zeros $\alpha \ne \beta$, the polynomial $\sum_i \lambda^{i-1} (\alpha_i - \beta_i)$ in $\lambda$ is nonzero of degree at most $n - 1$, so it has at most $n - 1$ roots. In practice $\lambda = 0$ or $\lambda = 1$ almost always works for generic systems; a random $\lambda$ from a set of size $N$ fails with probability at most $(n - 1) \binom{D}{2} / N$.

Not included are L1 and L2. For a zero-dimensional system of $n$ equations of degree at most $\delta$, $D \le \delta^n$ by Bézout's theorem, and Gröbner bases of zero-dimensional ideals can be computed in $\delta^{O(n)}$ operations (a result usually attributed to Lakshman, 1991). The Buchberger loop in the implementation has no such bound. Rouillier's own method uses the multiplication table more cleverly and avoids most matrix products, and Bostan, Salvy and Schost (2003) need fewer operations again by working with the dual of $A$.

Space: the $D + 1$ powers of $M_u$ and the $D$ matrices $M_b$ take $O(D^3)$ entries.

## Properties

- **Deterministic.** The search over $\lambda = 0, 1, 2, \ldots$ ends after a bounded number of trials, and the test in L8 is exact.
- **Multiplicities.** They are kept: $\mu(\alpha) = g_1(u(\alpha)) / \bar f'(u(\alpha))$. A lex Gröbner basis or a triangular decomposition of the radical loses them.
- **Unique given $u$.** The polynomials $\bar f$ and $g_v$ depend only on $I$ and $u$, not on the Gröbner basis or the normal set used.
- **Rational coefficients.** All output polynomials are in $K[T]$, so over $\mathbb{Q}$ they are exact.
- **Small coefficients.** With $g_1$ as common denominator, the coefficients are often much smaller than in the shape-lemma form $x_i = h_i(T)$, $h_i = g_{x_i} g_1^{-1} \bmod \bar f$. Dahan and Schost proved a bound of this kind for triangular sets; for the RUR it is an observation from experiments.

## Variants and improvements

- **Kronecker representation.** Kronecker (1882) used a generic linear form and a primitive element to describe the zeros. The geometric resolution of Giusti, Lecerf and Salvy (2001) computes such a representation without Gröbner bases, by Newton lifting along a curve, in time polynomial in a geometric degree of the system.
- **Shape lemma form.** If $I$ is radical and $u = x_1$ is separating, the lex Gröbner basis is $\{\bar f(x_1), x_2 - h_2(x_1), \ldots, x_n - h_n(x_1)\}$. It can be obtained from the RUR by inverting $g_1$ modulo $\bar f$, or computed directly by the [FGLM algorithm](/fglm-algorithm/).
- **Faster linear algebra.** Rouillier's original method avoids most matrix products by computing the traces of products of basis elements once. Bostan, Salvy and Schost use the dual of $A$ and baby-step giant-step for power projections.
- **Modular and sparse methods.** The RUR over $\mathbb{Q}$ is often computed modulo many primes and lifted by the Chinese remainder theorem and rational reconstruction, since its coefficients are known to have moderate size.
- **Real solutions.** The real zeros correspond to the real roots of $\bar f$ (when $K \subseteq \mathbb{R}$), which are found by [real root isolation](/real-root-isolation/), and the signature of the Hermite form counts them (Pedersen, Roy and Szpirglas).

## When to use it

Use the RUR when a zero-dimensional system over $\mathbb{Q}$ must be solved exactly and certified: it gives all complex zeros, the real ones by univariate root isolation, and their multiplicities. It is the method in Rouillier's RS library, which Maple uses for real solving. For systems with positive-dimensional components, use a [triangular decomposition](/triangular-decomposition/) or a Gröbner basis of an elimination ideal instead. For floating point answers only, homotopy continuation is often faster.

## Pitfalls

- **Not zero-dimensional.** The normal set is infinite, and the algorithm must stop; checking that each variable has a pure power among the leading monomials is the test.
- **Separation by the squarefree part.** Comparing $\deg \bar f$ with $D$ instead of with the Hermite rank $r$ never succeeds for ideals with multiple zeros. The comparison must be with the number of distinct zeros.
- **Characteristic $p$.** Newton identities divide by $1, \ldots, D$, and the Hermite rank counts zeros only when $p$ does not divide any multiplicity. For $p \le D$ the trace method needs changes.
- **Coefficient growth in L1.** Over $\mathbb{Q}$, the Gröbner basis step can be far more expensive than the rest. In the tests of the implementation, a Buchberger loop without the normal selection strategy and the chain criterion was too slow on some systems in three variables of degree four, and fast with them.
- **Reading off $x_i$ as polynomials.** The form $x_i = h_i(T)$ with $h_i = g_{x_i} / g_1 \bmod \bar f$ is valid, but $h_i$ usually has much larger coefficients than $g_{x_i}$ and $g_1$.

## Implementations

## History

Kronecker (1882) described the zeros of a system through a generic linear form and its minimal polynomial, which is the origin of the method. The trace form and its use to count real zeros go back to Hermite and were made effective by Pedersen, Roy and Szpirglas (1993). Alonso, Becker, Roy and Wörmann (1996) gave related univariate representations with multiplicities. Rouillier (1999) defined the rational univariate representation with $g_1$ as the common denominator, gave the trace formulas and the test for a separating element, and made it the basis of the RS solver. Giusti, Lecerf and Salvy (2001) gave a Gröbner-free algorithm for the Kronecker representation, and Bostan, Salvy and Schost (2003) gave fast algorithms from the multiplication matrices.

## References
