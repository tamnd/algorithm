---
tag: YJ3TKE
kind: theorem
slug: routh-hurwitz-criterion
name: Routh-Hurwitz criterion
aliases:
- Routh-Hurwitz stability criterion
- Hurwitz criterion
area: control/stability
level: intro
summary: A real polynomial has all roots in the open left half plane if and only if the first column of its Routh array has no sign change and no zero entry, or all its Hurwitz determinants are positive.
prereqs: [routh-array, hurwitz-matrix]
see_also: [routh-array, hurwitz-matrix, lyapunov-theorem-for-linear-systems, jury-stability-test, kharitonov-theorem, nyquist-stability-criterion, sturm-sequence, descartes-rule-of-signs]
sources:
  - book: "E. J. Routh, A Treatise on the Stability of a Given State of Motion, Particularly Steady Motion, Macmillan, London, 1877"
    locator: the Adams Prize essay, with the tabulation of the coefficients and the count of the roots with positive real part
  - paper: doi:10.1007/BF01446812
    title: "A. Hurwitz, Ueber die Bedingungen, unter welchen eine Gleichung nur Wurzeln mit negativen reellen Theilen besitzt, Mathematische Annalen 46, 273-284, 1895"
    locator: the determinant form of the conditions
  - paper: "A. Lienard and M. H. Chipart, Sur le signe de la partie reelle des racines d'une equation algebrique, Journal de Mathematiques Pures et Appliquees (6) 10, 291-346, 1914"
    locator: the reduced set of conditions with positive coefficients and every second Hurwitz determinant
  - book: isbn:9780821826645
    title: F. R. Gantmacher, The Theory of Matrices, Volume 2, AMS Chelsea Publishing, 2000 (reprint of the Chelsea edition of 1959)
    locator: Chapter XV, The problem of Routh-Hurwitz and related questions (Routh's scheme, the Hurwitz determinants, the singular cases and the Lienard-Chipart criterion)
  - paper: doi:10.1016/0167-6911(94)00089-E
    title: G. Meinsma, Elementary proof of the Routh-Hurwitz test, Systems and Control Letters 25(4), 237-242, 1995
    locator: the reduction of the degree by one and the continuity argument used in the proof below
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Chapter 5 (Routh's stability criterion and its special cases, with applications to the range of a gain)
---

The Routh-Hurwitz criterion tells whether all roots of a real polynomial have negative real parts, and it does this without finding the roots. It uses only a short table of numbers made from the coefficients by cross products, the [Routh array](/routh-array/), or a set of determinants made from the coefficients, the [Hurwitz determinants](/hurwitz-matrix/). The question is the main one in the theory of linear systems: a linear differential equation with constant coefficients has all its solutions decaying to zero exactly when every root of its characteristic polynomial has a negative real part. In that sense the criterion is to the left half plane what [Descartes' rule of signs](/descartes-rule-of-signs/) and [Sturm sequences](/sturm-sequence/) are to the positive real axis: a count of roots in a region by sign changes in a sequence of numbers. In control, it gives the range of a gain for which a feedback loop is asymptotically stable, as a set of polynomial inequalities in the gain.

## Statement

Let $p(s) = a_0 s^n + a_1 s^{n-1} + \dots + a_{n-1} s + a_n$ be a real polynomial with $a_0 > 0$ and $n \ge 1$. Call $p$ *Hurwitz* if every root of $p$ has a negative real part. Let $r_0, r_1, \dots, r_n$ be the first column of the Routh array of $p$, and let $\Delta_1, \dots, \Delta_n$ be the leading principal minors of the $n \times n$ Hurwitz matrix $H$, $H_{ij} = a_{2j-i}$ (with $a_k = 0$ for $k < 0$ or $k > n$).

**Theorem (Routh 1877, Hurwitz 1895).** The following are equivalent.

1. $p$ is Hurwitz.
2. The Routh array of $p$ can be built without a special case, and $r_0, r_1, \dots, r_n$ are all positive (no sign change and no zero entry).
3. $\Delta_1 > 0, \Delta_2 > 0, \dots, \Delta_n > 0$.

When the array is regular, $\Delta_k = r_1 r_2 \cdots r_k$ for every $k$.

**Counting form (Routh).** If no entry of the first column is zero, then $p$ has no root on the imaginary axis, and the number of roots of $p$ with positive real part is the number $V$ of sign changes in $r_0, r_1, \dots, r_n$.

**The special cases.**

- *A zero first entry in a row that is not all zero.* Then $p$ is not Hurwitz. Replace the zero by a small $\varepsilon > 0$, continue, and take the signs as $\varepsilon \to 0+$. If $p$ has no root on the imaginary axis and this happens once, $V$ is again the number of roots with positive real part.
- *A row of zeros.* Let the row above it stand for the *auxiliary polynomial* $A(s)$, which is even or odd. Then $A$ divides $p$, its roots are symmetric about the origin, and they include every root of $p$ on the imaginary axis, with multiplicity. Replace the zero row by the coefficients of $A'(s)$ and continue. If no zero first entry occurs, the number $V$ of sign changes is the number of roots of $p$ with positive real part; $p$ has $Z(A)$ roots on the axis, where $Z(A)$ is the number of axis roots of $A$, and the rest are in the left half plane.

**Low degrees.** With $a_0 > 0$, the polynomial is Hurwitz exactly when:

- $n = 1$ or $n = 2$: all coefficients are positive.
- $n = 3$: all coefficients are positive and $a_1 a_2 > a_0 a_3$.
- $n = 4$: all coefficients are positive and $a_1 a_2 a_3 > a_0 a_3^2 + a_1^2 a_4$.

**Lienard-Chipart form (1914).** With $a_0 > 0$, $p$ is Hurwitz if and only if all coefficients are positive and $\Delta_{n-1} > 0, \Delta_{n-3} > 0, \Delta_{n-5} > 0, \dots$. So about half of the determinant conditions follow from the others when the coefficients are positive (Gantmacher, Chapter XV, gives this and the other forms of the criterion; it is not proved here).

## In plain words

Write the even and the odd coefficients of the polynomial in two rows. Make each new row from the two rows above it, by the same cross product that removes the first entry. Each new row is a polynomial one degree lower. If the two leading numbers of a row pair have the same sign, the step removes one root from the left half plane. If they have opposite signs, it removes one root from the right half plane. So each sign change in the first column is one root on the wrong side. The polynomial is Hurwitz exactly when the first column is all positive. The determinants say the same thing, because each one is a product of the first column entries.

## Proof

The full proof, which also covers the special cases, is on the [Routh array](/routh-array/) page. Here are the main steps, following Meinsma (1995). For a polynomial $g$, let $N(g)$ be the number of its roots with positive real part and $Z(g)$ the number on the imaginary axis.

**Step 1: a Hurwitz polynomial has positive coefficients.** If $p$ is Hurwitz, then $p / a_0$ is a product of factors $s + \rho$ with $\rho > 0$ and $s^2 + 2\sigma s + \sigma^2 + \tau^2$ with $\sigma > 0$. All these factors have positive coefficients, so all $a_i > 0$.

**Step 2: even and odd parts on the axis.** Split $p = F + G$, where $F$ holds the terms with the parity of $n$ and $G$ the others. At $s = i\omega$, an even polynomial is real and an odd one is purely imaginary. So $p(i\omega) = 0$ if and only if $F(i\omega) = G(i\omega) = 0$, and the roots of $p$ on the axis are the roots on the axis of $\gcd(F, G)$.

**Step 3: one step of the array.** Rows $0$ and $1$ of the array are the coefficients of $F$ and $G$. Let $a_0 a_1 \ne 0$, $\eta = a_0 / a_1$, and $q = G + (F - \eta s G)$. The cross product rule makes row $2$ the coefficients of $F - \eta s G$, so rows $1, 2, \dots$ are the array of $q$, which has degree $n - 1$. Consider

$$p_t = F + G - t \eta s G , \qquad 0 \le t \le 1 ,$$

with $p_0 = p$ and $p_1 = q$. For every $t$ the two parts of $p_t$ are $F - t\eta sG$ and $G$, with the same greatest common divisor as $F$ and $G$, so by Step 2 the roots of $p_t$ on the axis do not change with $t$. Its leading coefficient is $(1 - t) a_0$, and its coefficient of $s^{n-1}$ is $a_1$. For $t < 1$ no root crosses the axis, so $N(p_t)$ is constant. As $t \to 1$, $n - 1$ roots go to the roots of $q$, and one root goes to infinity. The sum of the roots is $-a_1 / ((1 - t) a_0)$, so that root goes to the right if $a_0 a_1 < 0$ and to the left if $a_0 a_1 > 0$. Hence

$$N(p) = N(q) + [a_0 a_1 < 0] , \qquad Z(p) = Z(q) .$$

**Step 4: the counting form and 1 if and only if 2.** If no first entry is zero, apply Step 3 to $p$, then to $q$, and so on, $n$ times. The last polynomial is the nonzero constant $r_n$. Adding up gives $N(p) = V$ and $Z(p) = 0$. So if the column is all positive, $p$ is Hurwitz. Conversely, if $p$ is Hurwitz, Step 1 gives $a_0 a_1 > 0$, and Step 3 gives $N(q) = Z(q) = 0$, so $q$ is Hurwitz of degree $n - 1$. By induction every polynomial in the chain is Hurwitz, so every $r_i$ is positive and no special case occurs.

**Step 5: 2 if and only if 3.** In $H$, subtract $\eta$ times row $2l - 1$ from row $2l$ for each $l$. This adds multiples of earlier rows to later rows, so the leading principal minors do not change. Column $1$ becomes $(a_1, 0, \dots, 0)^T$, and the rest is the Hurwitz matrix of $q$. So $\Delta_k(p) = a_1 \Delta_{k-1}(q)$ with $\Delta_0 = 1$, and by induction $\Delta_k = r_1 \cdots r_k$ as long as $r_1, \dots, r_{k-1}$ are nonzero. If all $r_i > 0$, all $\Delta_k > 0$. If all $\Delta_k > 0$, then $r_1 = \Delta_1 > 0$, $r_2 = \Delta_2 / \Delta_1 > 0$, and so on, so all $r_i > 0$. $\blacksquare$

## Consequences

- **The range of a gain.** The closed loop characteristic polynomial $s^3 + 3 s^2 + 2 s + K$ is Hurwitz if and only if $K > 0$ and $3 \cdot 2 > K$, that is $0 < K < 6$. At $K = 6$ the Routh array has a zero row, the auxiliary polynomial is $3 s^2 + 6$, and the closed loop has the roots $\pm i \sqrt 2$: this is where the [root locus](/root-locus/) crosses the axis, and $\sqrt 2$ is the frequency of the oscillation.
- **An example with numbers.** For $(s + 1)(s + 2)(s + 3)(s + 4) = s^4 + 10 s^3 + 35 s^2 + 50 s + 24$, the first column is $1, 10, 30, 42, 24$ and the Hurwitz determinants are $10, 300, 12600, 302400$, which are the products $10$, $10 \cdot 30$, $10 \cdot 30 \cdot 42$ and $10 \cdot 30 \cdot 42 \cdot 24$.
- **Matrices.** A real matrix is [Hurwitz](/hurwitz-matrix/) if and only if its characteristic polynomial passes the test. The [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/) gives a second test of the same property that works on the matrix and does not need the coefficients.
- **A shifted region.** All roots have real part less than $-\sigma$ if and only if $p(s - \sigma)$ is Hurwitz. So the same test checks a required decay rate.
- **Discrete time.** The analogue for the unit disc is the [Jury stability test](/jury-stability-test/). One can also map the disc to the half plane by the [bilinear transform](/bilinear-transform/) and apply this criterion.
- **Uncertain coefficients.** If each coefficient lies in an interval, [Kharitonov's theorem](/kharitonov-theorem/) reduces the test of the whole family to four fixed polynomials, each tested by this criterion.

## Tightness

- **"No zero entry" is needed in 2.** For $s^3 + s^2 + s + 1 = (s + 1)(s^2 + 1)$, row $2$ is zero, the auxiliary polynomial is $s^2 + 1$, and after the replacement the first column is $1, 1, 2, 1$, with no sign change. But the roots $\pm i$ are on the axis, so the polynomial is not Hurwitz. A sign count alone does not see roots on the axis; the special case does.
- **Positive coefficients are not enough for $n \ge 3$.** $s^3 + s^2 + 2 s + 8$ has positive coefficients, but $a_1 a_2 = 2 < 8 = a_0 a_3$. Its first column is $1, 1, -6, 8$, with two sign changes, and the roots are $-2$ and $0.5 \pm 1.93649 i$.
- **The $\varepsilon$ method needs no axis roots.** $s^5 + 3 s^3 + s^2 + 2 s + 1 = (s^2 + 1)(s^3 + 2 s + 1)$ gives four sign changes with $\varepsilon$, but it has only two roots with positive real part; the two roots $\pm i$ are counted on the wrong side.
- **Both parts of the degree three test are needed.** $s^3 - s^2 - 2 s + 1$ satisfies $a_1 a_2 = 2 > 1 = a_0 a_3$, but its roots have the sum $1$, so it is not Hurwitz; the sign conditions cannot be dropped. $s^3 + s^2 + s + 1$ has positive coefficients and $a_1 a_2 = a_0 a_3$, and its roots $\pm i$ are on the axis; the inequality must be strict.

## History

James Clerk Maxwell, in his paper "On governors" (Proceedings of the Royal Society of London, 1868), asked for conditions on the coefficients under which the motion of a regulated machine decays, and gave them for equations of the third degree. Edward John Routh solved the problem for every degree in his Adams Prize essay of 1877, with the tabulation that now has his name and the count of roots by sign changes. Adolf Hurwitz found the determinant conditions independently in 1895, when Aurel Stodola asked him about the regulation of turbines. Lienard and Chipart showed in 1914 that, with positive coefficients, only every second determinant needs to be checked. Gantmacher's book treats the criterion together with its singular cases. Meinsma gave the short continuity proof in 1995.

## References
