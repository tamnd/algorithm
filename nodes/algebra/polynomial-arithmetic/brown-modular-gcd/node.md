---
tag: 02TR5G
kind: algorithm
slug: brown-modular-gcd
name: Brown's modular GCD algorithm
aliases:
- Brown's modular GCD
- Modular GCD algorithm
- modular GCD
- small primes modular gcd
area: algebra/polynomial-arithmetic
level: advanced
summary: Computes integer polynomial gcds by gcds modulo several primes followed by Chinese remaindering.
solves: [polynomial-gcd]
model: word-ram
complexity:
  vars: {n: the larger of the degrees of f and g, A: the largest absolute value of a coefficient of f and g, l: the number of word-size primes used}
  time: {worst: O(l n^2 + l^2 n + l n log A)}
  space: {extra: O(n l)}
  lucky_primes_needed: {worst: O(n + log A)}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1971
  people: [W. S. Brown]
  note: Brown published the modular gcd algorithm for multivariate polynomials over the integers in 1971, with images modulo primes and at evaluation points combined by Chinese remaindering and interpolation.
prereqs: [polynomial-gcd, chinese-remainder-theorem, polynomial-euclidean-algorithm, gauss-lemma, primitive-polynomial]
see_also: [modular-methods, subresultant-gcd, primitive-prs, heuristic-gcd, garner-algorithm, polynomial-extended-euclidean-algorithm, resultant, hensel-lifting]
sources:
  - paper: doi:10.1145/321662.321664
    title: W. S. Brown, On Euclid's algorithm and the computation of polynomial greatest common divisors, Journal of the ACM 18(4), 478-504, 1971
    locator: the modular gcd algorithm, unlucky primes and the multivariate method by evaluation and interpolation
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 6.4, Modular gcd algorithms; Section 6.6, Mignotte's factor bound and a modular gcd algorithm in Z[x]; Section 6.7, Small primes modular gcd algorithms
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.6.1, Modular methods for gcds in Z[X]
---

Brown's modular gcd algorithm computes the greatest common divisor of two polynomials with integer coefficients without the coefficient growth of the Euclidean algorithm over $\mathbb{Q}$. It computes the gcd modulo many word-size primes, which is cheap, keeps the images of the smallest degree, and combines them with the [Chinese remainder theorem](/chinese-remainder-theorem/) until a size test proves that the combined polynomial is the gcd. Primes that give a wrong degree, called unlucky, are few, and the algorithm detects them by their degree.

Notation: $f, g \in \mathbb{Z}[x]$ are nonzero, $n$ is the larger degree, $A$ is the largest absolute value of a coefficient, $\mathrm{lc}$ is the leading coefficient, $\mathrm{cont}$ is the gcd of the coefficients, and $\mathrm{pp}(f) = f/\mathrm{cont}(f)$ is the primitive part, with a positive leading coefficient. $\|a\|_1$ and $\|a\|_\infty$ are the sum and the largest absolute value of the coefficients of $a$. The gcd in $\mathbb{Z}[x]$ is taken with a positive leading coefficient. Costs count word operations on a word RAM, with primes that fit in one word.

## In plain words

Finding the common factor of two polynomials with whole-number coefficients by the school method makes the numbers grow very large on the way. The modular method works with remainders instead. For each of many primes it computes the common factor using only remainders after division by that prime, where numbers stay small. A few primes give a common factor that is too big; they are noticed and thrown away. The results for the good primes are glued together, digit by digit in a mixed base, until the glued polynomial is small enough that a simple size check proves it is the answer.

## The problem

**Input:** $f, g \in \mathbb{Z}[x]$, not both zero.

**Output:** $\gcd(f, g) \in \mathbb{Z}[x]$, the greatest common divisor with a positive leading coefficient. By [Gauss's lemma](/gauss-lemma/), it is $\gcd(\mathrm{cont} f, \mathrm{cont} g) \cdot \mathrm{pp}(G)$, where $G$ is a gcd of $f$ and $g$ in $\mathbb{Q}[x]$.

If one input is zero, the gcd is the other one, with its sign fixed.

## The algorithm

Let $G = \gcd(\mathrm{pp} f, \mathrm{pp} g)$ and $b = \gcd(\mathrm{lc} f, \mathrm{lc} g)$. Then $\mathrm{lc}(G)$ divides $b$. For a prime $p$ that does not divide $b$, the reduction of $G$ divides $f$ and $g$ modulo $p$ and keeps its degree, so the gcd $v_p$ modulo $p$ has degree at least $\deg G$. The prime is lucky when equality holds; then $b\, v_p \equiv (b/\mathrm{lc}\,G)\, G \pmod p$ for the monic $v_p$. The scaling by $b$ makes all lucky images agree on one integer polynomial $H = (b/\mathrm{lc}\,G)\, G$. The cofactors $U = b f / H$ and $W = b g / H$ are lifted with $H$.

```pseudo id=main
BROWN-GCD(f, g)
L1  c ← gcd(cont f, cont g);  f ← pp(f);  g ← pp(g)
L2  b ← gcd(lc f, lc g);  d ← min(deg f, deg g);  m ← 1
L3  for each prime p that does not divide b do
L4      v ← monic gcd of f and g mod p;  u ← f / v mod p;  w ← g / v mod p;  v ← b v mod p
L5      if deg v > d then continue with the next prime                 ▷ p is unlucky
L6      if deg v < d or m = 1 then (H, U, W, m, d) ← (v, u, w, p, deg v)  ▷ earlier primes were unlucky
L7      else combine H, U, W with v, u, w by Chinese remaindering;  m ← m p
L8      map the coefficients of H, U, W to the symmetric range modulo m
L9      if 2‖H‖₁‖U‖₁ < m and 2‖H‖₁‖W‖₁ < m and 2 max(‖b f‖∞, ‖b g‖∞) < m then
L10         return c · pp(H)
```

Line L4 uses the [Euclidean algorithm](/polynomial-euclidean-algorithm/) in $(\mathbb{Z}/p\mathbb{Z})[x]$ and two exact divisions. The images satisfy $b f \equiv H U$ and $b g \equiv H W \pmod m$. The test at line L9 replaces a trial division: it shows that these congruences are equalities in $\mathbb{Z}[x]$. The implementation returns early when one input is zero or a constant, and takes the primes from any iterable, by default the primes below $2^{31}$ in decreasing order.

## Example

Take $f = 2x^3 + 6x^2 + x + 3 = (2x^2 + 1)(x + 3)$ and $g = 6x^3 - 2x^2 + 3x - 1 = (2x^2 + 1)(3x - 1)$, so $b = \gcd(2, 6) = 2$ and the gcd is $2x^2 + 1$. Use the primes $5, 7, 11$. Images are in the symmetric range.

| $p$ | monic gcd mod $p$ | $H$ after the step | $U$, $W$ | $m$ | test at L9 |
|---|---|---|---|---|---|
| 5 | $x^3 + 3x^2 + 3x + 4$ | $2x^3 + x^2 + x - 2$ | $2$, $1$ | 5 | fails |
| 7 | $x^2 + 4$ | $2x^2 + 1$ | $2x - 1$, $-x - 2$ | 7 | fails |
| 11 | $x^2 + 6$ | $2x^2 + 1$ | $2x + 6$, $6x - 2$ | 77 | passes |

The prime $5$ is unlucky: modulo $5$, both $x + 3$ and $3x - 1$ are multiples of $x - 2$, so the gcd modulo $5$ is $(x^2 + 3)(x - 2)$, of degree $3$. At $p = 7$ a smaller degree appears, and the algorithm restarts. At $p = 11$ the images are combined modulo $77$: $\|H\|_1 = 3$, $\|U\|_1 = \|W\|_1 = 8$, so $2 \cdot 3 \cdot 8 = 48 < 77$, and $\|b f\|_\infty = \|b g\|_\infty = 12$ with $24 < 77$. The output is $\mathrm{pp}(2x^2 + 1) = 2x^2 + 1$. A script checked every image.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). When the test at line L9 passes, $H U$ has coefficients of absolute value at most $\|H\|_1 \|U\|_1 < m/2$, and so has $b f$. They are congruent modulo $m$, so they are equal, and $H$ divides $b f$ and, by the same argument, $b g$. By Gauss's lemma $\mathrm{pp}(H)$ divides $f$ and $g$, hence $G$. Its degree is $d$, which is at least $\deg G$ because every image has degree at least $\deg G$. So $\mathrm{pp}(H) = G$. The algorithm stops because unlucky primes divide a nonzero resultant, so they are finite in number, and the lucky images converge to the true $H, U, W$, which have bounded norms.

## Complexity

The bounds are proved and count word operations, with $l$ the number of primes tried.

- **Images.** Reducing $f$ and $g$ modulo one prime costs $O(n \log A)$, the Euclidean algorithm modulo $p$ costs $O(n^2)$, and the two exact divisions cost $O(n^2)$. Over $l$ primes, $O(l n^2 + l n \log A)$.
- **Chinese remaindering.** Adding one prime to residues of $O(l)$ words costs $O(n l)$, so $O(n l^2)$ in total; the norm tests cost the same.
- **Total.** $O(l n^2 + l^2 n + l n \log A)$.
- **Fast arithmetic.** With fast gcds modulo $p$ and fast Chinese remaindering, the cost drops to $O(n^2 + n \log A)$ for $l = O(n + \log A)$, up to logarithmic factors.
- **Lucky primes needed.** The test passes once $m$ exceeds $2 \|H\|_1 \|U\|_1$ and the similar quantities. By Mignotte's factor bound, $\|G\|_1 \|f/G\|_1 \le 2^n \|f\|_2$, so $\|H\|_1 \|U\|_1 \le b \cdot 2^n (n + 1)^{1/2} A$, and $O(n + \log A)$ word-size primes suffice.
- **Unlucky primes.** A prime $p$ that does not divide $b$ is unlucky only if it divides the resultant of $f/G$ and $g/G$, a nonzero integer with $O(n(n + \log A))$ digits. So the number of unlucky primes is bounded, and with $l = O(n + \log A)$ the total is $O(n^3 + n \log^2 A)$ up to the unlucky primes.

**In practice (observed).** With primes near $2^{31}$ or $2^{63}$, unlucky primes are rare, and the number of primes is close to the size of the gcd and its cofactors divided by the word size. Computer algebra systems use modular gcds, often with the [heuristic gcd](/heuristic-gcd/) as a first try for small inputs.

## Properties

- **No coefficient growth.** All gcd computations are modulo word-size primes; only the Chinese remaindering and the test use large integers.
- **Output sensitive.** The number of primes depends on the size of the gcd and its cofactors, not on a worst-case bound fixed in advance.
- **Deterministic.** For a fixed list of primes, the result and the work are fixed. Choosing the primes at random gives a bound on the expected number of unlucky primes.
- **Parallel.** The images for different primes are independent.
- **Iterative.** No recursion in the univariate case.

## Variants and improvements

- **Big prime version.** Choose one prime $p$ larger than twice the bound on $\|H\|_\infty$ and compute one image; von zur Gathen and Gerhard, Section 6.6, give this form with Mignotte's bound.
- **Multivariate gcds.** Brown's original algorithm reduces $\mathbb{Z}[x_1, \ldots, x_r]$ to $\mathbb{Z}/p\mathbb{Z}[x_1]$ by primes and evaluation points, and recovers the gcd by Chinese remaindering and interpolation. Zippel's sparse interpolation lowers the cost when the gcd has few terms.
- **Early termination by trial division.** Stop when the combined image does not change after adding a prime, then check by dividing $f$ and $g$.
- **Heuristic gcd.** Evaluate at one large integer and reconstruct the gcd from the integer gcd; see [heuristic gcd](/heuristic-gcd/).
- **Pseudo-remainder sequences.** The [subresultant algorithm](/subresultant-gcd/) works over $\mathbb{Z}$ directly, with controlled growth, and is preferred for small or sparse inputs.

## When to use it

Use the modular gcd for dense integer polynomials of moderate or large degree or with large coefficients, and inside [square-free factorization](/square-free-factorization/) and rational function arithmetic, where many gcds are needed. For tiny inputs the [primitive](/primitive-prs/) or [subresultant](/subresultant-gcd/) remainder sequences are simpler. Over a finite field, compute the gcd directly with the Euclidean algorithm.

## Pitfalls

- **Forgetting the scaling by $b$.** Monic images modulo different primes are images of $G/\mathrm{lc}(G)$, which has rational coefficients; the Chinese remainder theorem then gives nonsense. Multiply by $b$ first.
- **Combining images of different degrees.** An unlucky image has a higher degree and must not be mixed with lucky ones; a smaller degree means all earlier images were unlucky.
- **Primes dividing $b$.** Then the degree of $G$ can drop modulo $p$, and the image can be too small, which the algorithm would take for a better degree. Skip such primes.
- **Stopping without a proof.** A combined image that stays the same for one more prime is very likely, but not certainly, correct. Use the norm test or a trial division.
- **Contents.** The gcd of the contents must be put back at the end, and the primitive part needs a positive leading coefficient.

## Implementations

## History

W. S. Brown published the modular gcd algorithm in 1971 in the Journal of the ACM,. He showed how to compute gcds of multivariate integer polynomials with images modulo primes and at evaluation points, and handled unlucky primes and points by their degrees. Richard Zippel's sparse modular method of 1979 refined the multivariate case. The small primes method for $\mathbb{Z}[x]$ with Mignotte's factor bound and the norm test is presented in von zur Gathen and Gerhard, Sections 6.6 and 6.7, and in Cohen, Section 3.6.1.

## References
