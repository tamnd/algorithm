---
tag: 7A0696
kind: algorithm
slug: jury-stability-test
name: Jury stability test
aliases:
- Jury test
- Jury criterion
area: control/stability
level: core
summary: Decides from a table built on the coefficients whether every root of a real polynomial lies inside the unit circle, and counts the roots outside. O(n^2) operations.
model: real-ram
complexity:
  vars: {n: the degree of the polynomial}
  time: {worst: "O(n^2)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1961
  people: [Eliahu I. Jury, J. Blanchard]
  note: Jury and Blanchard published the stability test in table form in the Proceedings of the IRE in 1961. It is a tabular form of the Schur-Cohn recursion for real polynomials.
prereqs: [characteristic-polynomial, z-transform]
see_also: [schur-cohn-test, routh-array, bilinear-transform, sampled-data-system, zero-order-hold-discretization, levinson-durbin-recursion, lyapunov-theorem-for-linear-systems, asymptotic-stability]
sources:
  - paper: "E. I. Jury and J. Blanchard, A stability test for linear discrete systems in table form, Proceedings of the IRE 49(12), 1947-1948, 1961"
    locator: the table of the coefficients and the inequalities that decide whether all roots lie inside the unit circle
  - book: "E. I. Jury, Theory and Application of the z-Transform Method, Wiley, 1964"
    locator: the stability test for discrete-time systems in table form
  - book: isbn:9780133148992
    title: Karl J. Åström and Björn Wittenmark, Computer-Controlled Systems, Theory and Design, third edition, Prentice Hall, 1997
    locator: Chapter 3, Analysis of Discrete-Time Systems (Jury's stability criterion)
  - book: isbn:9780130342812
    title: Katsuhiko Ogata, Discrete-Time Control Systems, second edition, Prentice Hall, 1995
    locator: Chapter 4 (the Jury stability test in the classic form, with its necessary conditions at z = 1 and z = -1)
  - paper: "A. Cohn, Über die Anzahl der Wurzeln einer algebraischen Gleichung in einem Kreise, Mathematische Zeitschrift 14 (1922) 110-148"
    locator: the reduction of the degree by the reversed polynomial, which the table puts in rows
---

The Jury stability test decides whether every root of a real polynomial $p(z)$ lies inside the open unit circle, that is, whether $p$ is *Schur*. It never computes a root. It builds a table from the coefficients: each pass removes the constant term of the current polynomial with a multiple of its reversed copy, which lowers the degree by one, and the leading coefficients of the polynomials form the first column of the table. If $p$ is the [characteristic polynomial](/characteristic-polynomial/) of a discrete-time linear system $x_{k+1} = A x_k$, or the denominator of a closed-loop transfer function in the variable $z$ of the [z-transform](/z-transform/), the test decides whether $A$ is Schur, and so whether the equilibrium is [asymptotically stable](/asymptotic-stability/). It is the discrete-time counterpart of the [Routh array](/routh-array/). The [Schur-Cohn test](/schur-cohn-test/) on another page uses the same recursion for complex polynomials; this page says below how the two tables differ.

## In plain words

Write the coefficients of the polynomial in a row, and below them the same numbers in reverse order. Divide the last number of the top row by the first one. Subtract that multiple of the reversed row from the top row. The last entry becomes zero, so drop it. The new row is one shorter. Repeat with the new row and its reverse until one number is left. Read down the first entries of the rows. If all of them are positive, every root is inside the unit circle. If none of them is zero, the number of negative entries is the number of roots outside the circle. A zero entry means that the test is singular: some root is on the circle, or two roots are mirror images in the circle.

## The problem

Given a real polynomial $p(z) = a_0 z^n + a_1 z^{n-1} + \dots + a_n$ with $a_0 \ne 0$, written with the highest power first, decide whether all its roots satisfy $|z| < 1$. When the answer is no, count the roots with $|z| > 1$, counted with multiplicity, if the table allows it.

A matrix is Schur if every eigenvalue has modulus less than $1$, and a polynomial is Schur in the same sense for its roots. The usual source of $p$ is $\det(zI - A)$ for the matrix $A$ of a discrete-time model, for example the [zero-order hold](/zero-order-hold-discretization/) model $A_d = e^{A h}$ of a continuous plant with sampling period $h$, or the closed-loop characteristic polynomial of a [sampled-data system](/sampled-data-system/).

Notation. $p_k$ is the polynomial of degree $k$ in the table, with coefficients $c_0, \dots, c_k$ (highest power first). Its reversed polynomial is $p_k^*(z) = z^k p_k(1/z) = c_k z^k + \dots + c_0$. The number $\alpha_k = c_k / c_0$ is the *reflection coefficient* of step $k$, and $F$ is the first column: the leading coefficients of $p_n, p_{n-1}, \dots, p_0$.

## The algorithm

```pseudo id=main
JURY(a_0, ..., a_n)                          ▷ p(z) = a_0 z^n + ... + a_n, real
L1  remove zero leading coefficients (error if none is left); if a_0 < 0 then negate every a_i
L2  c ← (a_0, ..., a_n);  F ← (a_0)
L3  for k ← n down to 1 do                    ▷ c holds the k + 1 coefficients of p_k
L4      α_k ← c_k / c_0
L5      c ← (c_i - α_k · c_{k-i}  for i = 0, ..., k - 1)        ▷ p_{k-1}: (p_k - α_k p_k*) / z
L6      append c_0 to F
L7      if c_0 = 0 then return (F, "singular")                  ▷ |α_k| = 1: p is not Schur
L8  N ← the number of negative entries of F
L9  return (F, N)                             ▷ N roots outside the circle; p is Schur iff N = 0
```

Line L1 makes the leading coefficient positive, which changes no root. Line L5 subtracts $\alpha_k$ times the reversed row from the row. The last entry becomes $c_k - \alpha_k c_0 = 0$, so the result is $z\,p_{k-1}(z) = p_k(z) - \alpha_k p_k^*(z)$, and the new leading coefficient is $c_0 (1 - \alpha_k^2)$. So the first entry keeps its sign when $|\alpha_k| < 1$, changes its sign when $|\alpha_k| > 1$, and is zero when $|\alpha_k| = 1$. Line L7 stops on a zero entry. In a printed Jury table each polynomial $p_k$ takes two rows, the coefficients and their reverse, so the table has $2n + 1$ rows.

The implementation computes in exact rational arithmetic and converts floating point input exactly. It returns the rows, the first column, the numbers $\alpha_k$, the count $N$ (or "singular"), and the verdict. It also has the classic $n + 1$ conditions of Jury and Blanchard (see Variants) as a second, independent check.

## Example

**The check value.** For $p(z) = z^2 - z + 0.5$:

| row | entries | $\alpha_k$ |
|---|---|---|
| $p_2$ | $1$, $-1$, $1/2$ | $\alpha_2 = 1/2$ |
| $p_2^*$ | $1/2$, $-1$, $1$ | |
| $p_1$ | $1 - \frac12 \cdot \frac12 = 3/4$, $-1 - \frac12 \cdot (-1) = -1/2$ | $\alpha_1 = -2/3$ |
| $p_1^*$ | $-1/2$, $3/4$ | |
| $p_0$ | $3/4 - (-\frac23)(-\frac12) = 5/12$ | |

The first column $1, 3/4, 5/12$ is positive, so $p$ is Schur. Indeed the roots are $0.5 \pm 0.5 i$, both of modulus $1/\sqrt 2 = 0.70711$.

**One root outside.** For $p(z) = 4 z^3 + 4 z^2 - 7 z + 2 = 4 (z - \frac12)^2 (z + 2)$ the rows are $(4, 4, -7, 2)$, then with $\alpha_3 = 1/2$ the row $(3, 15/2, -9)$, then with $\alpha_2 = -3$ the row $(-24, 30)$, then with $\alpha_1 = -5/4$ the row $(27/2)$. The first column $4, 3, -24, 27/2$ has one negative entry, so one root lies outside the circle: the root $-2$. The double root $1/2$ causes no difficulty.

**A gain range.** Take the plant $1/(s + 1)$, with time in seconds, sampled with a zero-order hold at $h = 1$ s, a delay of one sample for the computation, and the controller $u_k = K e_k$. The loop transfer function is $L(z) = K b / (z (z - a))$ with $a = e^{-1} = 0.36788$ and $b = 1 - e^{-1} = 0.63212$, and the closed-loop polynomial is $z^2 - a z + K b$. For a general $z^2 + a_1 z + a_2$ the table gives $\alpha_2 = a_2$, the first entry $1 - a_2^2$, then $\alpha_1 = a_1 / (1 + a_2)$. The first column is positive exactly when

$$|a_2| < 1, \qquad |a_1| < 1 + a_2 ,$$

the well known stability triangle. Here this gives $-1 < K < 1/b = 1.58198$. At $K = 1.58198$ the two closed-loop poles are on the unit circle at the angle $\arccos(a/2) = 1.3858$ rad. The continuous loop without the sample and the delay would be asymptotically stable for every $K > -1$; the sampling and the delay create the upper limit.

**Singular tables.** For $(z - 1)(z - \frac12) = z^2 - \frac32 z + \frac12$ the first column is $1, 3/4, 0$: a root on the circle. For $(z - 2)(z - \frac12) = z^2 - \frac52 z + 1$ it is $1, 0$ at once, because $\alpha_2 = 1$. This polynomial has no root on the circle, but its two roots are mirror images in the circle. The cubic $8 z^3 - 18 z^2 + 3 z + 2 = (z - 2)(2 z - 1)(4 z + 1)$ gives $8, 15/2, 0$ for the same reason.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **One step (proved).** If $p_k$ has no root on the circle and $|\alpha_k| \ne 1$, then $p_{k-1}$ has no root on the circle. It has as many roots outside the circle as $p_k$ when $|\alpha_k| < 1$, and $k$ minus that number when $|\alpha_k| > 1$. The proof uses $|p_k^*(z)| = |p_k(z)|$ on the circle and Rouché's theorem.
- **The count (proved).** If no entry of $F$ is zero, $p$ has no root on the circle, and the number of negative entries of $F$ is the number of roots outside the circle. So $p$ is Schur exactly when every entry is positive.
- **Singular tables (proved).** A root on the circle, or a pair of roots $\zeta$ and $1/\zeta$, always gives a zero entry. A Schur polynomial never gives one, so a singular table means that $p$ is not Schur. The count is not available in that case.
- **The classic conditions (proved).** For $a_0 > 0$ and $n \ge 2$, $p$ is Schur if and only if $p(1) > 0$, $(-1)^n p(-1) > 0$ and $|\alpha_k| < 1$ for $k = n, \dots, 2$.
- **Termination (proved).** Each pass shortens the row by one, so there are at most $n$ passes.

The tests compare the verdict and the count with the moduli of the roots from the [Durand-Kerner method](/durand-kerner-method/) on more than 1000 random polynomials of degree at most 6 with integer coefficients from $-4$ to $4$, skipping those with a root within $10^{-6}$ of the circle. They also check the stability triangle on a grid, exact counts for polynomials built from known rational roots, and the relation to the Schur transform below.

## Complexity

Costs are in the real-RAM model, one unit per arithmetic operation on the coefficients.

- **Time.** The pass for degree $k$ costs one division and $k$ multiplications and subtractions. In all this is $n$ divisions and $n (n + 1)/2$ multiplications, so $O(n^2)$ operations.
- **Space.** $O(n)$ numbers if only the current row and the first column are kept, and $O(n^2)$ for the whole printed table.
- **Exact arithmetic.** With rational coefficients the entries are rational, and their numerators and denominators can grow from row to row. The operation count stays $O(n^2)$, but the cost in bit operations is higher.
- **Compared with root finding.** Computing all roots and their moduli also costs $O(n^2)$ operations per iteration of a method such as Durand-Kerner, but it needs a tolerance. The table gives an exact answer in rational arithmetic, and it works with symbolic coefficients such as a gain $K$.

## Properties

- **Exact.** In rational arithmetic the verdict is a proof, not an estimate.
- **Symbolic.** Entries can contain a parameter, and the conditions "first column positive" become inequalities in that parameter, as in the gain example.
- **Scale.** Multiplying $p$ by a positive number scales every row by that number and does not change $F$ in sign.
- **Reflection coefficients.** $p$ is Schur if and only if $|\alpha_k| < 1$ for every $k$. The numbers $\alpha_k$ are the reflection coefficients of the step-down recursion that inverts the [Levinson-Durbin recursion](/levinson-durbin-recursion/), which is how signal processing checks that an all-pole filter is stable.

## Variants and improvements

- **The classic table of Jury and Blanchard.** It forms each new row without division, as the $2 \times 2$ determinants $c_0 c_i - c_k c_{k-i}$, and stops at the row of degree 2, so the table has $2n - 3$ rows. The test is then the $n + 1$ conditions $p(1) > 0$, $(-1)^n p(-1) > 0$, $|a_n| < a_0$, and $|\text{first entry}| > |\text{last entry}|$ in each later row (Ogata 1995, Chapter 4). The first two conditions are cheap necessary checks that often end the test early. The rows differ from the rows of this page only by a nonzero factor, and the conditions are equivalent (see the proof).
- **Relation to the Schur-Cohn test.** The [Schur-Cohn test](/schur-cohn-test/) allows complex coefficients. It cancels the leading coefficient with the transform $T p = \overline{p(0)}\, p - \operatorname{lead}(p)\, p^*$, keeps the coefficients as integers by dividing by their content, and counts the roots inside the circle. The Jury table cancels the constant term instead, divides by the leading coefficient, and reads the signs of the first column. For a real $p_k$ the row $p_{k-1}$ is $T p_k$ in reversed order, multiplied by $-1/c_0$. So the two tables carry the same polynomials, and they become singular for the same inputs.
- **The bilinear map.** The substitution $z = (1 + w)/(1 - w)$ maps the unit disc onto the left half plane, so the [Routh array](/routh-array/) of the transformed polynomial also decides the question. This is the [bilinear transform](/bilinear-transform/) without the sampling period. It costs more operations and can create a root at infinity that needs care, so the direct table is usually better.
- **The Bistritz table.** A later table by Bistritz works with a three-term recursion on the symmetric and antisymmetric parts of $p$, and needs fewer multiplications.
- **Margins inside the disc.** To test whether all roots satisfy $|z| < r$, run the table on $p(r z)$. For the damping of a sampled loop, $r < 1$ gives a decay rate per sample.

## When to use it

Use the Jury table for the characteristic polynomial of a discrete-time loop of small order, for hand calculations, and when a coefficient depends on a parameter, as for the range of a gain. For a numerical matrix of high order, do not form the characteristic polynomial, because its roots can be very sensitive to the coefficients (see [root conditioning](/root-conditioning/)). Compute the eigenvalues, or the [spectral radius](/spectral-radius/), of the matrix instead, or use the discrete [Lyapunov theorem](/lyapunov-theorem-for-linear-systems/) $A^T P A - P = -Q$.

## Pitfalls

- **Zero entries in floating point.** A first entry that is zero in exact arithmetic comes out as a tiny number of either sign in floating point, and the count can then be wrong. A tiny entry means that a root is near the circle. The implementation computes exactly to avoid this.
- **Singular without a root on the circle.** A zero entry does not prove a root on the circle. The polynomial $z^2 - \frac52 z + 1$ has the roots $2$ and $\frac12$. The verdict "not Schur" is still correct, but the count needs another method, for example the table of $p(r z)$ for an $r$ slightly different from $1$.
- **A negative leading coefficient.** The count "number of negative entries" assumes $a_0 > 0$. Negate $p$ first.
- **The two forms of the table.** Some books write the coefficients with the lowest power first, and some build the rows from the last entries. The meaning of "first entry" changes with the form. Check the conditions on a known polynomial, such as $z^2 - z + 0.5$, before you use a table from a book.
- **Continuous-time rules.** Positive coefficients are necessary for a Hurwitz polynomial, but they say nothing for the unit circle: $z^2 - z + 0.5$ is Schur with a negative coefficient, and $z + 2$ is not Schur with positive coefficients.

## Implementations

## History

Issai Schur studied in 1917 and 1918 the transform that lowers the degree of a polynomial with its reversed polynomial, and Arthur Cohn used it in 1922 to count the roots of a polynomial in a circle. Eliahu I. Jury and J. Blanchard put the recursion for real polynomials into a table with sign and modulus conditions in 1961, and Jury's book of 1964 on the z-transform made the table the standard stability test for sampled-data control systems. Control textbooks present it in two forms: the division-free table with $n + 1$ conditions, as in Ogata, and the normalized table whose first column counts the roots outside the circle, as in Åström and Wittenmark.

## References
