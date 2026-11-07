---
tag: HMRZF4
kind: algorithm
slug: polynomial-extended-euclidean-algorithm
name: Extended Euclidean algorithm for polynomials
aliases:
- polynomial Bezout coefficients
- extended Euclidean algorithm over F[x]
- polynomial XGCD
area: algebra/polynomial-arithmetic
level: core
summary: Returns s and t with s f + t g = gcd(f, g), used for modular inverses and Hensel lifting.
solves: [polynomial-gcd]
model: blum-shub-smale-machine
complexity:
  vars: {m: the larger of the degrees of f and g, n: the smaller of the degrees of f and g}
  time: {worst: O(m n + m)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [polynomial-euclidean-algorithm, bezouts-identity]
see_also: [polynomial-euclidean-algorithm, extended-euclidean-algorithm, modular-inverse, hensel-lifting, half-gcd, partial-fraction-decomposition, pade-approximation, reed-solomon-decoding]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 3.2, The Extended Euclidean Algorithm (p. 47; the algorithm, the invariants and the degrees of s and t), and Section 3.3, Cost analysis for Z and F[x] (p. 51)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (Algorithm X, the extended algorithm for integers), and Section 4.6.1, Division of Polynomials
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 2, Algebra of Polynomials, Rational Functions, and Power Series (the extended Euclidean algorithm in a Euclidean domain)
---

The extended Euclidean algorithm for polynomials computes, for $f, g$ over a field $F$, the monic $h = \gcd(f, g)$ together with polynomials $s$ and $t$ such that $s f + t g = h$. It runs the [Euclidean algorithm](/polynomial-euclidean-algorithm/) and applies each quotient also to two extra sequences of coefficients, so its cost stays $O(mn + m)$ field operations for degrees $m \ge n$. The cofactors are small: when $g \nmid f$, $\deg s < \deg g - \deg h$ and $\deg t < \deg f - \deg h$, and these bounds make them unique. It is the standard way to invert in $F[x]/(m)$, and it gives the Bézout coefficients for [Hensel lifting](/hensel-lifting/), the polynomial Chinese remainder theorem and partial fractions.

## In plain words

The plain Euclidean method finds the greatest common divisor by taking remainders again and again. Every remainder is a combination of the two inputs: some polynomial times the first one plus some polynomial times the second one. The extended method keeps track of these two multipliers for each remainder. When the remainder that is the divisor appears, its two multipliers are the answer.

Keeping track costs little. The method uses each quotient once more on each list of multipliers, in the same way that it uses it on the remainders.

The main use is division modulo a polynomial. If the greatest common divisor of a polynomial and the modulus is one, then the first multiplier is the inverse of that polynomial modulo the modulus.

## The problem

Given a field $F$ and $f, g \in F[x]$, find the monic $h = \gcd(f, g)$ and $s, t \in F[x]$ with $s f + t g = h$. Such $s, t$ exist by [Bézout's identity](/bezouts-identity/) for the Euclidean domain $F[x]$; see [polynomial GCD](/polynomial-gcd/). Polynomials are dense coefficient arrays, lowest degree first.

## The algorithm

```pseudo id=main
XGCD(f, g)                              ▷ f, g in F[x], F a field
L1  (r_0, s_0, t_0) ← (f, 1, 0); (r_1, s_1, t_1) ← (g, 0, 1); strip f and g
L2  while r_1 ≠ 0 do
L3      (q, r) ← long division of r_0 by r_1
L4      (r_0, s_0, t_0, r_1, s_1, t_1) ← (r_1, s_1, t_1, r, s_0 − q·s_1, t_0 − q·t_1)
L5  if r_0 = 0 then return (0, s_0, t_0)   ▷ only when f = g = 0
L6  u ← lc(r_0)^(−1)
L7  return (u·r_0, u·s_0, u·t_0)
```

Write $r_0 = f, r_1 = g, r_2, \ldots, r_\ell, r_{\ell+1} = 0$ for the remainder sequence, $q_i$ for the quotient of $r_{i-1}$ by $r_i$, and $s_i, t_i$ for the multipliers of $r_i$. Line L4 sets $r_{i+1} = r_{i-1} - q_i r_i$ and applies the same rule to $s$ and $t$:

$$s_{i+1} = s_{i-1} - q_i s_i, \qquad t_{i+1} = t_{i-1} - q_i t_i .$$

Line L3 is [long division](/polynomial-long-division/), which over a field needs no condition on the divisor. Lines L6 and L7 make the gcd monic and scale $s$ and $t$ by the same constant, so the identity $s f + t g = h$ stays true.

## Example

Over $\mathbb{Q}$, take $f = x^4 - 1$ and $g = x^3 + 2x^2 + 2x + 1$, as on the page of the [Euclidean algorithm](/polynomial-euclidean-algorithm/).

| $i$ | $r_i$ | $s_i$ | $t_i$ | $q_i$ |
|---|---|---|---|---|
| 0 | $x^4 - 1$ | $1$ | $0$ | |
| 1 | $x^3 + 2x^2 + 2x + 1$ | $0$ | $1$ | $x - 2$ |
| 2 | $2x^2 + 3x + 1$ | $1$ | $-x + 2$ | $\tfrac12 x + \tfrac14$ |
| 3 | $\tfrac34 x + \tfrac34$ | $-\tfrac12 x - \tfrac14$ | $\tfrac12 x^2 - \tfrac34 x + \tfrac12$ | $\tfrac83 x + \tfrac43$ |
| 4 | $0$ | $\tfrac43 (x^2 + x + 1)$ | $-\tfrac43 (x^3 - x^2 + x - 1)$ | |

The last nonzero remainder is $r_3$, with $u = 4/3$. So $h = x + 1$, $s = -\tfrac13 - \tfrac23 x$ and $t = \tfrac23 - x + \tfrac23 x^2$. Check: $s f + t g = x + 1$. The degrees obey the bounds: $\deg s = 1 < 3 - 1$ and $\deg t = 2 < 4 - 1$. The last row holds the cofactors up to a constant: $x^2 + x + 1 = g / h$ and $x^3 - x^2 + x - 1 = f / h$.

**An inverse in $\mathbb{F}_8$.** Over $\mathbb{F}_2$, $m = x^3 + x + 1$ is irreducible, and $\mathbb{F}_8 = \mathbb{F}_2[x]/(m)$. XGCD$(m, x^2 + 1)$ takes the quotients $x$ and $x^2 + 1$, with remainders $1$ and $0$, and returns $h = 1$, $s = 1$, $t = x$. So $1 \cdot m + x (x^2 + 1) = 1$, and $x$ is the inverse of $x^2 + 1$ in $\mathbb{F}_8$: indeed $x^3 + x \equiv (x + 1) + x = 1$.

## Correctness

The algorithm keeps the [invariant](/loop-invariant/)

$$s_0 f + t_0 g = r_0 \qquad\text{and}\qquad s_1 f + t_1 g = r_1 ,$$

which holds after line L1 and is kept by line L4, because the new pair is a linear combination of the old one with the same coefficients for $r$, $s$ and $t$. The $r$ part of the loop is the Euclidean algorithm, so at the end $r_0$ is a gcd and $u r_0$ is the monic gcd. Multiplying the first invariant by $u$ gives $(u s_0) f + (u t_0) g = u r_0$. The degree bounds follow from the formulas $\deg s_i = \deg g - \deg r_{i-1}$ and $\deg t_i = \deg f - \deg r_{i-1}$, proved by induction. The full proof is below.

## Complexity

The cost counts field operations at unit cost, as in [polynomial ring](/polynomial-ring/). Let $m = \deg f \ge n = \deg g$; the case $m < n$ costs one extra step that swaps the inputs.

- **Remainders.** As for the [Euclidean algorithm](/polynomial-euclidean-algorithm/), at most $(2n + 1)(m + n + 1)$ operations and $n + 1$ inversions.
- **Multipliers.** With $n_i = \deg r_i$, the quotient $q_i$ has degree $n_{i-1} - n_i$, and $\deg t_i = m - n_{i-1}$, $\deg s_i = n - n_{i-1}$ for $i \ge 2$. The product $q_i t_i$ costs $O((n_{i-1} - n_i + 1)(m + 1))$ operations, and $\sum_{i \ge 2} (n_{i-1} - n_i + 1) \le 2n + 1$, so all updates of $t$ cost $O(mn + m)$. The updates of $s$ cost $O(n^2 + 1)$ in the same way, and the first step only sets $s_2 = 1$ and $t_2 = -q_1$.
- **Total.** $O(mn + m)$ operations and at most $n + 2$ inversions. Von zur Gathen and Gerhard (Section 3.3) give the exact counts. If only $s$ is needed, as for an inverse modulo $g$, the $t$ updates can be skipped, and $t = (h - s f)/g$ can be computed afterwards if needed.
- **Space.** $O(m)$ for the current six polynomials.

These counts are proved. Over $\mathbb{Q}$ they hide the growth of the fractions in $s_i$ and $t_i$, as for the plain algorithm.

## Properties

- **Degree formulas.** If $m \ge n$, then $\deg t_i = m - n_{i-1}$ for $2 \le i \le \ell + 1$ and $\deg s_i = n - n_{i-1}$ for $2 \le i \le \ell + 1$.
- **Small and unique cofactors.** If $f, g \ne 0$ and $h$ is neither the monic $f$ nor the monic $g$, then $\deg s < \deg g - \deg h$ and $\deg t < \deg f - \deg h$, and $(s, t)$ is the only pair with $s f + t g = h$ and these bounds. *Proof of uniqueness.* If $s' f + t' g = h$ too, then $(s - s')(f/h) = (t' - t)(g/h)$. Since $f/h$ and $g/h$ are coprime, $g/h$ divides $s - s'$, whose degree is less than $\deg(g/h)$; so $s = s'$ and then $t = t'$.
- **The last multipliers are the cofactors.** $s_{\ell+1} f + t_{\ell+1} g = r_{\ell+1} = 0$, so $(f/h)\, s_{\ell+1} = -(g/h)\, t_{\ell+1}$. As $f/h$ and $g/h$ are coprime, $f/h$ divides $t_{\ell+1}$, and both have degree $m - n_\ell$, so $t_{\ell+1} = c f/h$ and $s_{\ell+1} = -c g/h$ for a constant $c \ne 0$.
- **Every row is a Padé form.** For each $i$, $r_i \equiv t_i\, g \pmod f$ with $\deg r_i + \deg t_i < \deg f$ for $i \ge 2$. This is the basis of rational reconstruction.

## Variants and improvements

- **Monic remainders.** Von zur Gathen and Gerhard (Section 3.2) divide each $r_i$, $s_i$, $t_i$ by $\operatorname{lc}(r_i)$, so that all remainders are monic. The results are the same after line L7.
- **Half extended.** Track only $s$ (or only $t$) when only one multiplier is needed.
- **Fast extended Euclidean algorithm.** The [half-gcd](/half-gcd/) method computes $h$, $s$ and $t$, or any single row $(r_i, s_i, t_i)$, in $O(M(n) \log n)$ operations; von zur Gathen and Gerhard, Section 11.1.
- **Stop early.** Stop at the first $i$ with $\deg r_i < k$: this gives a [Padé approximation](/pade-approximation/) or a rational reconstruction, and with $f = x^{2k}$ it is the Euclidean form of [Berlekamp-Massey](/berlekamp-massey/) and of [Reed-Solomon decoding](/reed-solomon-decoding/).
- **Integers.** The same algorithm for $\mathbb{Z}$ is the [extended Euclidean algorithm](/extended-euclidean-algorithm/) for integers.

## When to use it

Use it for inverses in $F[x]/(m)$ and in finite fields $\mathbb{F}_{p^k}$ of small degree, for the Bézout coefficients in [Hensel lifting](/hensel-lifting/), for the polynomial Chinese remainder theorem, and for [partial fraction decomposition](/partial-fraction-decomposition/). For large degrees, use the fast extended algorithm. For an inverse in $\mathbb{F}_{p^k}$ with large $p^k$, inversion by the power $a^{p^k - 2}$ is an alternative that needs no gcd but costs more multiplications.

## Pitfalls

- **Wrong order of the multipliers.** The update must use the old $s_0$ and $s_1$ together, as in line L4. Updating $s_0$ first and then computing $s_1$ from the new value gives wrong multipliers.
- **Forgetting to scale $s$ and $t$.** Making $h$ monic without scaling $s$ and $t$ by the same $u$ breaks $s f + t g = h$.
- **Integer coefficients.** Over $\mathbb{Z}$, $s$ and $t$ with $s f + t g = \gcd(f, g)$ need not exist in $\mathbb{Z}[x]$: for $f = 2$ and $g = x$, the gcd is $1$, but $2s + xt$ always has an even constant term. Work over $\mathbb{Q}$, or ask only for $s f + t g = \operatorname{res}(f, g)$, which is always possible in $\mathbb{Z}[x]$.
- **Inverse of a non-unit.** If $\gcd(a, m) \ne 1$, $a$ has no inverse modulo $m$. Check $h = 1$ before using $s$.

## Implementations

## History

Knuth gives the extended algorithm for integers as Algorithm X in Section 4.5.2. Von zur Gathen and Gerhard, Section 3.2, state it for every Euclidean domain, with the degree formulas for $F[x]$ and its use for inverses and the Chinese remainder algorithm.

## References
