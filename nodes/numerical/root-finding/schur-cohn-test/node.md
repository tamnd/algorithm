---
tag: AXFQZ4
kind: algorithm
slug: schur-cohn-test
name: Schur-Cohn test
aliases:
- Schur-Cohn criterion
- Schur-Cohn algorithm
- Schur transform test
area: numerical/root-finding
level: research
summary: Counts the zeros of a complex polynomial in a disc without computing them, by at most n Schur transforms that each lower the degree. Exact in rational arithmetic; it reports singular steps.
solves: [real-root-counting]
model: real-ram
complexity:
  vars: {n: the degree of the polynomial}
  time: {worst: "O(n^2)"}
  space: {extra: "O(n)"}
  evaluations: {worst: "n"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, local: false}
history:
  year: 1922
  people: [Issai Schur, Arthur Cohn]
  note: Schur's 1917 and 1918 papers on bounded power series introduced the transform; Cohn used it in 1922 to count the zeros of a polynomial in a circle.
prereqs: [polynomial-root-finding, real-root-counting]
see_also: [lehmer-schur-method, real-root-counting, sturm-sequence, root-conditioning, fundamental-theorem-of-algebra, polynomial-root-finding, horner-rule, z-transform]
sources:
  - paper: "I. Schur, Über Potenzreihen, die im Innern des Einheitskreises beschränkt sind, Journal für die reine und angewandte Mathematik 147 (1917) 205-232 and 148 (1918) 122-145"
    locator: the transform of a function bounded in the unit disc, the origin of the Schur transform
  - paper: "A. Cohn, Über die Anzahl der Wurzeln einer algebraischen Gleichung in einem Kreise, Mathematische Zeitschrift 14 (1922) 110-148"
    locator: the count of the zeros in the unit circle by the reduced polynomials and the corresponding Hermitian form
  - book: "M. Marden, Geometry of Polynomials, second edition, Mathematical Surveys 3, American Mathematical Society, 1966"
    locator: Chapter X, The number of zeros in a half-plane, a sector or a circle (the Schur-Cohn criterion and the singular cases)
  - book: "P. Henrici, Applied and Computational Complex Analysis, Volume 1, Wiley, 1974"
    locator: Chapter 6, Polynomials (the Schur-Cohn algorithm and Lehmer's method)
  - paper: doi:10.1145/321062.321064
    title: "D. H. Lehmer, A machine method for solving polynomial equations, Journal of the ACM 8 (1961) 151-162"
    locator: the use of the Schur-Cohn test to decide whether a disc contains a zero
  - book: "E. I. Jury, Theory and Application of the z-Transform Method, Wiley, 1964"
    locator: the stability table for discrete-time systems, a tabular form of the Schur-Cohn recursion
---

The Schur-Cohn test counts how many zeros of a complex polynomial $p$ lie inside the open unit disc, or, after a shift and a scaling, inside any disc $|z - c| < r$, without computing any zero. It applies the *Schur transform* $Tp = \overline{p(0)}\,p - a_n\,p^*$, where $p^*$ is the polynomial with the conjugated coefficients in reverse order. The transform lowers the degree by at least one, and by Rouché's theorem the sign of the real number $Tp(0) = |a_0|^2 - |a_n|^2$ tells how the zero count of $p$ relates to that of $Tp$. After at most $n$ transforms the count is known. With rational coefficients the test is exact; it cannot give a wrong count, but it stops with "singular" when some $|a_0| = |a_n|$, which happens when $p$ has a zero on the circle and occasionally otherwise. It is the decision step of the [Lehmer-Schur method](/lehmer-schur-method/) and, as the Jury table, a standard stability test for discrete-time systems.

## In plain words

You want to know how many roots of a polynomial lie inside a circle, without finding them. Compare the constant term with the leading coefficient. Combine the polynomial with its mirror image (the same coefficients, reversed and conjugated) so that the top term cancels. The new polynomial has smaller degree, and which of the two coefficients was larger tells you whether it has the same number of roots inside the circle or the complementary number. Repeat until only a constant is left, then read the count back.

## The problem

Given a polynomial $p(z) = a_n z^n + \cdots + a_0$ with complex coefficients, $a_n \ne 0$, a centre $c$ and a radius $r > 0$, return the number of zeros of $p$, counted with multiplicity, in the open disc $|z - c| < r$; or report that the test is singular for this input. The disc case reduces to the unit disc by $q(w) = p(c + rw)$.

Notation on the root-finding pages: $n$ is the degree, $k(p)$ the number of zeros of $p$ in the open unit disc $\mathbb{D}$, $p^*(z) = z^n\,\overline{p(1/\bar z)} = \sum_{i=0}^n \overline{a_{n-i}}\,z^i$ the reciprocal polynomial, $p_0 = p$, $p_{j+1} = Tp_j$, $n_j = \deg p_j$ and $\delta_{j+1} = p_{j+1}(0)$.

## The algorithm

```pseudo id=main
SCHUR-COHN(p)
L1  remove zero leading coefficients of p; if p = 0 then error
L2  j ← 0; p_0 ← p
L3  while deg p_j ≥ 1 do
L4      n_j ← deg p_j; p*_j ← coefficients of p_j conjugated and reversed
L5      p_{j+1} ← conj(p_j(0)) · p_j − lead(p_j) · p*_j;  δ_{j+1} ← p_{j+1}(0)     ▷ real, equals |p_j(0)|² − |lead(p_j)|²
L6      if δ_{j+1} = 0 then return (none, "singular")
L7      remove zero leading coefficients of p_{j+1}; divide it by a positive rational to keep its coefficients small; j ← j + 1
L8  k ← 0                                          ▷ p_j is a nonzero constant, with no zeros
L9  for i ← j − 1 down to 0 do if δ_{i+1} < 0 then k ← n_i − k
L10 return (k, "count")
```

Line L4 forms the reciprocal polynomial. In line L5 the coefficients of $z^{n_j}$ cancel, so $\deg p_{j+1} \le n_j - 1$, and the constant term is the real number $|p_j(0)|^2 - |\operatorname{lead}(p_j)|^2$. Line L6 stops on a singular step. Line L7 removes the leading zeros, and divides by the positive content, which changes neither the zeros nor the sign of the next constant term. Line L9 reads the counts back: $k(p_i) = k(p_{i+1})$ when $\delta_{i+1} > 0$ and $k(p_i) = n_i - k(p_{i+1})$ when $\delta_{i+1} < 0$. For a disc $|z - c| < r$ the implementation first forms $p(c + rw)$ by an exact Taylor shift.

## Example

Take $p(z) = 6z^3 - 19z^2 + 2z + 3 = (2z - 1)(3z + 1)(z - 3)$, with zeros $\frac12$, $-\frac13$ and $3$. The implementation computes:

| $j$ | $p_j$ (after L7) | $n_j$ | $\delta_{j+1}$ |
|---|---|---|---|
| 0 | $6z^3 - 19z^2 + 2z + 3$ | 3 | $9 - 36 = -27$ |
| 1 | $-23z^2 + 40z - 9$ | 2 | $81 - 529 = -448$ |
| 2 | $5z - 4$ | 1 | $16 - 25 = -9$ |
| 3 | $-1$ | 0 | |

Line L5 gives $p_1 = -69z^2 + 120z - 27$, which line L7 divides by 3. Reading back: $k(p_3) = 0$; $\delta_3 < 0$, so $k(p_2) = 1 - 0 = 1$ (the zero $0.8$); $\delta_2 < 0$, so $k(p_1) = 2 - 1 = 1$ (the zeros of $p_1$ are $0.266$ and $1.473$); $\delta_1 < 0$, so $k(p) = 3 - 1 = 2$. Indeed $\frac12$ and $-\frac13$ are inside and $3$ is outside. The same polynomial in the disc $|z - 3| < \frac1{10}$ gives 1, and with $c = 0$, $r = 4$ gives 3.

Two singular inputs: $(z - \frac12)(z - 2) = z^2 - \frac52 z + 1$ has $|a_0| = |a_2|$, and in fact $Tp = 0$, because its zeros are symmetric in the circle; $z^2 + z + i$ has zeros of moduli $0.693$ and $1.443$, none on the circle and not symmetric, but again $|a_0| = |a_2|$.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **The count is exact (proved).** If the algorithm returns a count $k$, then $p$ has no zeros on the circle and exactly $k$ zeros, with multiplicity, in the open disc. This holds in exact arithmetic for every input; the implementation uses exact rationals, converting floating point coefficients exactly.
- **Singular cases (proved).** If $p$ and $p^*$ have a common zero, in particular if $p$ has a zero on the circle or a pair of zeros $z$, $1/\bar z$, the algorithm returns "singular". It may also return "singular" for other inputs, as in the example; it never returns a wrong count.
- **Termination (proved).** The degree drops by at least one per pass, so there are at most $n$ passes.

## Complexity

The cost is counted in arithmetic operations on the coefficients; the test makes no evaluations of $p$ at points.

- **Passes.** At most $n$ Schur transforms, one per degree.
- **Operations.** The pass at degree $n_j$ costs $O(n_j)$ multiplications, so $O(n^2)$ in all, plus $O(n^2)$ for the Taylor shift to a general disc.
- **Number sizes.** Without the division in line L7 the coefficient sizes would double in each pass. With it, in the experiments (degree 16, random integer coefficients below 10 in absolute value), the numerators grew by about 7.5 binary digits per pass, linearly (observed, not proved).
- **Space.** $O(n)$ numbers.

### Floating point

In floating point the constant terms $\delta_j = |a_0|^2 - |a_n|^2$ suffer cancellation when a zero is close to the circle, and an error in the sign of one $\delta_j$ changes the count. The forward recursion is also known to amplify errors for high degree. There is no reliable tolerance that separates a tiny $\delta_j$ from zero, so floating point versions can only report a count together with a warning when some $|\delta_j|$ is small relative to the coefficient sizes. The implementation avoids the issue by computing exactly; its counts are certain for the polynomial whose coefficients are the given numbers, but if those numbers are rounded data, zeros within the [conditioning](/root-conditioning/) radius of the circle can still be on either side.

## Properties

- **Exact and certified.** In rational arithmetic the count is a proof, not an estimate.
- **No derivatives and no point evaluations.** Only coefficient arithmetic.
- **Not a root finder.** It gives counts; locating roots needs subdivision, as in the Lehmer-Schur method.
- **Multiplicities.** Multiple zeros are counted with multiplicity, and cause no difficulty unless they lie on the circle.

## Variants and improvements

- **Schur-Cohn determinants.** Cohn's form counts zeros by the signs of the leading principal minors of a Hermitian matrix built from the coefficients; the number of zeros inside equals the number of negative eigenvalues of that form in the regular case (Marden, Chapter X).
- **Jury table.** For real coefficients and the stability question "are all zeros inside?", Jury's table gives the same recursion with sign tests on its first column.
- **Bistritz test.** A three-term recursion on symmetric and antisymmetric parts, with about half the operations, and a cleaner treatment of singular cases.
- **Singular cases.** Marden gives rules to continue through some singular steps; the simplest remedy, used by the Lehmer-Schur method, is to change the radius slightly.
- **Half-planes.** The Möbius map $z = (1 + w)/(1 - w)$ turns the half-plane problem into the disc problem; the direct analogue for half-planes is the Routh-Hurwitz criterion.

## When to use it

Use it to decide whether a polynomial has zeros in a disc, or how many, when a certain answer is needed: stability of discrete-time systems, the inclusion test in subdivision root finders, or checking a computed set of roots. For locating all roots of a well-behaved polynomial in floating point, eigenvalue methods or [Laguerre's method](/laguerre-method/) with [deflation](/polynomial-deflation/) are faster.

## Pitfalls

- **A zero on the circle.** The test then always reports "singular", and no small tolerance can rescue a floating point version.
- **Singular without a zero on the circle.** $|a_0| = |a_n|$ can occur by accident, and always does for self-reciprocal polynomials. Perturbing the radius, for example to $r(1 + 2^{-20})$, usually makes the test regular.
- **Coefficient growth.** Exact arithmetic without the content division in line L7 makes the numbers grow exponentially with the degree.
- **Rounded data.** An exact count for rounded coefficients is a count for a nearby polynomial; near-circle zeros may be miscounted relative to the intended data.
- **Wrong reciprocal.** For complex coefficients $p^*$ must use conjugates; reversing alone gives wrong counts.

## Implementations

## History

Issai Schur studied functions bounded in the unit disc in 1917 and 1918 and introduced the transformation that now carries his name. Arthur Cohn applied it to polynomials in 1922, giving the count of zeros in a circle by the sequence of reduced polynomials and by a Hermitian form. M. Fujiwara and others studied the associated quadratic forms. D. H. Lehmer used the test in 1961 to decide which discs contain zeros in his machine method for polynomial equations. In control theory the recursion became the Jury stability table (Jury, 1964) for discrete-time systems, and Bistritz (1984) gave a more efficient variant.

## References
