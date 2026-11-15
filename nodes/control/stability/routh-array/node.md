---
tag: 43YJD3
kind: algorithm
slug: routh-array
name: Routh array
aliases:
- Routh table
- Routh tabulation
area: control/stability
level: intro
summary: Builds a table from the coefficients of a polynomial by cross products, and counts its right half plane roots by the sign changes in the first column. O(n^2) operations.
model: real-ram
complexity:
  vars: {n: the degree of the polynomial}
  time: {worst: "O(n^2)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1877
  people: [Edward John Routh]
  note: Routh gave the tabulation and the count of roots with positive real part in his Adams Prize essay of 1877; Hurwitz gave the equivalent determinant conditions in 1895.
prereqs: [characteristic-polynomial, hurwitz-matrix]
see_also: [routh-hurwitz-criterion, hurwitz-matrix, jury-stability-test, schur-cohn-test, sturm-sequence, kharitonov-theorem, root-locus, euclidean-algorithm]
sources:
  - book: "E. J. Routh, A Treatise on the Stability of a Given State of Motion, Particularly Steady Motion, Macmillan, London, 1877"
    locator: the Adams Prize essay, with the tabulation of the coefficients and the count of the roots with positive real part
  - paper: doi:10.1007/BF01446812
    title: "A. Hurwitz, Ueber die Bedingungen, unter welchen eine Gleichung nur Wurzeln mit negativen reellen Theilen besitzt, Mathematische Annalen 46, 273-284, 1895"
    locator: the determinant form of the conditions
  - book: isbn:9780821826645
    title: F. R. Gantmacher, The Theory of Matrices, Volume 2, AMS Chelsea Publishing, 2000 (reprint of the Chelsea edition of 1959)
    locator: Chapter XV, The problem of Routh-Hurwitz and related questions (Routh's scheme, its singular cases, and the Hurwitz determinants)
  - paper: doi:10.1016/0167-6911(94)00089-E
    title: G. Meinsma, Elementary proof of the Routh-Hurwitz test, Systems and Control Letters 25(4), 237-242, 1995
    locator: the reduction of the degree by one and the continuity argument that the correctness proof follows
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Chapter 5 (Routh's stability criterion, with the special cases of a zero first entry and a row of zeros)
---

The Routh array is a table of numbers built from the coefficients of a real polynomial $p(s) = a_0 s^n + a_1 s^{n-1} + \dots + a_n$. The first two rows hold the coefficients with even and odd index, and each later row is made from the two rows above it by $2 \times 2$ cross products. The number of sign changes in the first column of the table equals the number of roots of $p$ in the open right half plane, when the table has no zero in its first column. So the table tells whether a linear system with characteristic polynomial $p$ has a [Hurwitz](/hurwitz-matrix/) matrix without computing any root. The theorem behind it is the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/); this page gives the algorithm, its two special cases, an exact implementation and its proof. The method needs about $n^2/4$ cross products, and it works with symbolic coefficients, which is why it is still used to find the gains that keep a feedback loop asymptotically stable.

## In plain words

Write the coefficients of the polynomial in two rows, alternating: the first, third, fifth in the top row, and the second, fourth, sixth below. Make each new row from the two rows above it: for each position, cross-multiply the first column with the next column, take the difference, and divide by the first number of the row just above. Each new row is shorter than the one two rows above. Stop when there are $n + 1$ rows. Then read down the first column and count how often the sign flips. That count is the number of roots with a positive real part. If a first entry is zero, the table needs one of two repairs, described below.

## The problem

Given a real polynomial $p(s) = a_0 s^n + a_1 s^{n-1} + \dots + a_n$ with $a_0 \ne 0$, written with the highest power first, count its roots in the open right half plane $\{\operatorname{Re} s > 0\}$, counted with multiplicity, and decide whether all roots lie in the open left half plane. The usual source of $p$ is the [characteristic polynomial](/characteristic-polynomial/) $\det(sI - A)$ of a linear system, or the denominator of a closed-loop [transfer function](/transfer-function/).

Notation. Row $i$ belongs to the power $s^{n-i}$, for $i = 0, \dots, n$, and has $\lfloor (n - i)/2 \rfloor + 1$ entries $r_{i,0}, r_{i,1}, \dots$. The first column is $r_i = r_{i,0}$. An entry outside a row counts as $0$. $V$ is the number of sign changes in $r_0, r_1, \dots, r_n$, and $N(p)$ and $Z(p)$ are the numbers of roots of $p$ in the open right half plane and on the imaginary axis.

## The algorithm

```pseudo id=main
ROUTH-ARRAY(a_0, ..., a_n)
L1  remove zero leading coefficients; if no coefficient is left then error
L2  row_0 ← (a_0, a_2, a_4, ...);  row_1 ← (a_1, a_3, a_5, ...)         ▷ pad row_1 with 0 to length ⌊(n-1)/2⌋ + 1
L3  for i ← 1 to n do
L4      if i ≥ 2 then
L5          c ← row_{i-1}[0]
L6          for j ← 0 to ⌊(n-i)/2⌋ do row_i[j] ← (c · row_{i-2}[j+1] - row_{i-2}[0] · row_{i-1}[j+1]) / c
L7      if every entry of row_i is 0 then                               ▷ zero row
L8          d ← n - i + 1;  A(s) ← Σ_j row_{i-1}[j] · s^(d-2j)            ▷ auxiliary polynomial
L9          row_i[j] ← (d - 2j) · row_{i-1}[j] for every j                ▷ the coefficients of A'(s)
L10     else if row_i[0] = 0 then                                         ▷ zero first entry
L11         row_i[0] ← ε                                                  ▷ ε is a positive infinitesimal
L12 V ← number of sign changes in row_0[0], ..., row_n[0], each sign taken as ε → 0+
L13 return the rows, V, and the list of the special cases met
```

Line L2 splits the coefficients by parity. Line L6 is the cross product rule: for rows $(u_0, u_1, \dots)$ and $(c_0, c_1, \dots)$ the next row is $((c_0 u_1 - u_0 c_1)/c_0, (c_0 u_2 - u_0 c_2)/c_0, \dots)$. Lines L7 to L9 handle a row of zeros: the row above defines an even or odd *auxiliary polynomial* $A$ of degree $d$, and the zero row is replaced by the coefficients of its derivative. Lines L10 and L11 handle a zero first entry in a row that is not all zero: it is replaced by a small positive number $\varepsilon$, the later entries become rational functions of $\varepsilon$, and line L12 uses their signs for small $\varepsilon > 0$. A row may be multiplied by a positive number at any point without changing $V$, which keeps hand calculations small.

The implementation computes in exact rational arithmetic, and it converts floating point input exactly. It keeps an entry that depends on $\varepsilon$ as a quotient of two polynomials in $\varepsilon$; the sign as $\varepsilon \to 0+$ is the sign of the quotient of the lowest nonzero coefficients. It also returns the list of special cases with the auxiliary polynomials, and `is_hurwitz(p)`, which is true exactly when no special case occurs and $V = 0$.

## Example

**The regular case.** For $p(s) = s^3 + s^2 + 2s + 8$:

| row | power | entries |
|---|---|---|
| 0 | $s^3$ | $1$, $2$ |
| 1 | $s^2$ | $1$, $8$ |
| 2 | $s^1$ | $(1 \cdot 2 - 1 \cdot 8)/1 = -6$ |
| 3 | $s^0$ | $(-6 \cdot 8 - 1 \cdot 0)/(-6) = 8$ |

The first column $1, 1, -6, 8$ has two sign changes, so $p$ has two roots in the right half plane. Indeed $p(s) = (s + 2)(s^2 - s + 4)$, with the roots $-2$ and $0.5 \pm 1.93649 i$. All coefficients of $p$ are positive, so the coefficient signs alone would not show this.

**A gain range.** For $p(s) = s^3 + 3 s^2 + 2 s + K$ the rows are $(1, 2)$, $(3, K)$, $((6 - K)/3)$ and $(K)$. The first column is positive exactly when $0 < K < 6$, so the companion matrix of $p$ is Hurwitz for exactly these gains. For $K = 8$ it is $1, 3, -2/3, 8$, with two sign changes.

**A zero row.** At $K = 6$, row 2 is $(6 - 6)/3 = 0$. The row above gives $A(s) = 3 s^2 + 6$, and row 2 becomes the coefficient of $A'(s) = 6 s$. Then row 3 is $(6 \cdot 6 - 3 \cdot 0)/6 = 6$. The first column $1, 3, 6, 6$ has no sign change, so no root lies in the right half plane. The roots of $A$ are $\pm i \sqrt 2$, and they are roots of $p$: $p(s) = (s + 3)(s^2 + 2)$. So $p$ has one root in the left half plane and two on the axis, and it is not Hurwitz, although $V = 0$.

**A zero first entry.** For $p(s) = s^5 + 2 s^4 + 2 s^3 + 4 s^2 + 11 s + 10$:

| row | power | entries |
|---|---|---|
| 0 | $s^5$ | $1$, $2$, $11$ |
| 1 | $s^4$ | $2$, $4$, $10$ |
| 2 | $s^3$ | $0 \to \varepsilon$, $6$ |
| 3 | $s^2$ | $(4 \varepsilon - 12)/\varepsilon$, $10$ |
| 4 | $s^1$ | $6 - 10 \varepsilon^2 / (4 \varepsilon - 12) \to 6$ |
| 5 | $s^0$ | $10$ |

For small $\varepsilon > 0$ the signs are $+, +, +, -, +, +$, so $V = 2$. The roots are $-1.30871$, $-1.24066 \pm 1.0375 i$ and $0.89502 \pm 1.4561 i$: two in the right half plane.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md). They follow the degree reduction of Meinsma (1995).

- **Regular case (proved).** If no special case occurs, $p$ has no root on the imaginary axis and $N(p) = V$.
- **Zero rows only (proved).** If zero rows occur and no zero first entry does, then $N(p) = V$. The roots of $p$ on the imaginary axis are exactly those of the first auxiliary polynomial $A_1$, with multiplicity, and $p$ has $n - V - Z(A_1)$ roots in the open left half plane.
- **One zero first entry (proved).** If exactly one $\varepsilon$ substitution and no zero row occur, and $p$ has no root on the imaginary axis, then $N(p) = V$. With several substitutions the implementation reuses the same $\varepsilon$; the count was correct on all the random tests, but this case is not proved.
- **Roots on the axis with $\varepsilon$ (counterexample).** If $p$ has roots on the imaginary axis and an $\varepsilon$ substitution occurs, $V$ can be larger than $N(p)$. See Pitfalls.
- **The Hurwitz decision (proved).** `is_hurwitz(p)` is true if and only if all roots of $p$ have negative real part. A Hurwitz polynomial never produces a special case.
- **Hurwitz determinants (proved).** In the regular case the leading principal minors of the Hurwitz matrix of $p$ are $\Delta_k = r_1 r_2 \cdots r_k$.
- **Termination (proved).** The loop runs $n$ times, and each row is computed once.

The tests compare the count with roots computed numerically by the [Durand-Kerner method](/durand-kerner-method/). They use more than 1000 random polynomials of degree up to 6 with integer coefficients from $-3$ to $3$ and no root within $10^{-6}$ of the axis, more than 50 of which need the $\varepsilon$ method, and more than 300 random polynomials whose table has a zero row.

## Complexity

- **Time.** Row $i$ has $\lfloor (n - i)/2 \rfloor + 1$ entries, each made by two multiplications, one subtraction and one division. In all that is about $n^2/4$ cross products, $O(n^2)$ arithmetic operations. A zero row costs $O(n)$ more.
- **Space.** $O(n^2)$ numbers for the whole table, or $O(n)$ if only the last two rows and the first column are kept.
- **Exact arithmetic.** The numbers in the table are rational functions of the coefficients, and their size can grow with $n$. With symbolic coefficients, such as a gain $K$, the entries are rational functions of $K$, and the conditions $r_i > 0$ become polynomial inequalities in $K$.
- **The $\varepsilon$ case.** The entries become rational functions of $\varepsilon$ whose degree can grow with each row, so the cost of that case is higher than $O(n^2)$ operations on numbers.

## Properties

- **Exact.** In rational arithmetic the count is a proof, not an estimate.
- **No roots computed.** Only coefficient arithmetic, and no evaluation of $p$.
- **Symbolic.** The table can be built with unknown parameters, which gives the parameter region in which $p$ is Hurwitz.
- **Scaling.** Multiplying a row by a positive number, or $p$ by a nonzero number, does not change $V$.
- **Same as Gaussian elimination.** The table is the elimination of the Hurwitz matrix of $p$ without pivoting, which is why $\Delta_k = r_1 \cdots r_k$ (see [Gaussian elimination](/gaussian-elimination/)). It is also a form of the [Euclidean algorithm](/euclidean-algorithm/) on the even and odd parts of $p$, and the rows with polynomial meaning form a sequence of the [Sturm](/sturm-sequence/) kind.

## Variants and improvements

- **Hurwitz determinants.** The conditions $\Delta_1 > 0, \dots, \Delta_n > 0$ (for $a_0 > 0$) are equivalent to a positive first column. They are easier to state with symbols and harder to compute; see [Routh-Hurwitz criterion](/routh-hurwitz-criterion/).
- **Liénard-Chipart test.** If all coefficients are positive, only every second Hurwitz determinant needs to be checked (Gantmacher, Chapter XV).
- **Relative stability.** To test whether all roots satisfy $\operatorname{Re} s < -\sigma$, build the table for $p(s - \sigma)$.
- **Discrete time.** For roots inside the unit circle use the [Jury stability test](/jury-stability-test/) or the [Schur-Cohn test](/schur-cohn-test/), or apply the [bilinear transform](/bilinear-transform/) and then the Routh array.
- **Families of polynomials.** For coefficients that vary in intervals, [Kharitonov's theorem](/kharitonov-theorem/) reduces the question to four Routh tests, and the [edge theorem](/edge-theorem/) treats polytopes of polynomials.
- **Other ways around zero entries.** Instead of $\varepsilon$, one can apply the table to $p(s) (s + 1)$ or to the reversed polynomial $s^n p(1/s)$, which have the same number of right half plane roots and may avoid the zero.

## When to use it

Use the Routh array for polynomials of small degree, for hand calculations, and above all when the coefficients contain parameters: the range of a gain $K$ for which a loop is asymptotically stable comes straight from the first column, and it matches the crossing points of the [root locus](/root-locus/) with the imaginary axis. For a numerical matrix of high order it is better not to form the characteristic polynomial at all, because its roots can be very sensitive to its coefficients (see [root conditioning](/root-conditioning/)). Compute the eigenvalues of the matrix, or use the [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/), instead.

## Pitfalls

- **Zero tests in floating point.** In floating point a first entry that should be zero comes out as a tiny number of either sign, and the count can be wrong. A tiny entry means that some root is close to the imaginary axis. The implementation computes exactly to avoid this.
- **No sign change is not enough.** $V = 0$ means no root in the right half plane; it does not exclude roots on the axis. The example at $K = 6$ has $V = 0$ and roots $\pm i \sqrt 2$. The polynomial is Hurwitz only if no special case occurs and $V = 0$.
- **The $\varepsilon$ method with roots on the axis.** For $p(s) = s^5 + 3 s^3 + s^2 + 2 s + 1 = (s^2 + 1)(s^3 + 2 s + 1)$, row 1 starts with $0$, the $\varepsilon$ method gives the signs $+, +, -, +, -, +$ and $V = 4$, but $p$ has only two roots in the right half plane, $0.2267 \pm 1.46771 i$. The roots $\pm i$ on the axis are counted as if they were in the right half plane. When $\varepsilon$ is needed, check for roots on the axis, for example with the greatest common divisor of the even and odd parts (see [polynomial GCD](/polynomial-gcd/)).
- **Rows multiplied by a negative number.** Only positive factors are allowed; a negative factor changes the signs.
- **A missing coefficient.** A zero or negative coefficient already shows that $p$ is not Hurwitz (for $a_0 > 0$). The table is still needed to count the right half plane roots.
- **Leading zeros.** A zero leading coefficient changes the degree; the implementation removes it, and it rejects the zero polynomial.

## Implementations

## History

The question of stability conditions for a polynomial was raised by J. C. Maxwell in his 1868 paper on governors. E. J. Routh answered it in his Adams Prize essay, A Treatise on the Stability of a Given State of Motion (1877), with the tabulation now named after him and the count of the roots with positive real part. A. Hurwitz, unaware of Routh's work, gave the conditions in determinant form in 1895, prompted by a question of A. Stodola on turbine regulators. Liénard and Chipart (1914) showed that about half of the determinant conditions suffice when the coefficients are positive. Gantmacher's book treats the singular cases in general, and short proofs of the counting rule appeared much later, among them Meinsma's in 1995.

## References
