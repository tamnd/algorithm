---
tag: V9GAPW
kind: theorem
slug: kharitonov-theorem
name: Kharitonov's theorem
aliases:
- Kharitonov polynomials
area: control/robust-and-adaptive-control
level: core
summary: "Real polynomials whose coefficients vary independently in intervals, with the leading interval not containing 0, are all Hurwitz if and only if four Kharitonov polynomials are Hurwitz."
prereqs: [routh-hurwitz-criterion, characteristic-polynomial]
see_also: [edge-theorem, routh-hurwitz-criterion, routh-array, model-uncertainty, quadratic-stability, interval-arithmetic, nyquist-stability-criterion, poles-and-zeros]
sources:
  - paper: "V. L. Kharitonov, Asymptotic stability of an equilibrium position of a family of systems of linear differential equations, Differentsial'nye Uravneniya 14(11), 2086-2088, 1978 (in Russian)"
    locator: the original statement for real interval polynomials
  - book: isbn:013781576X
    title: S. P. Bhattacharyya, H. Chapellat and L. H. Keel, Robust Control, The Parametric Approach, Prentice Hall, 1995
    locator: Chapter 5, Interval Polynomials, Kharitonov's Theorem (Theorem 5.1, the four polynomials, the rectangular value set and the proof by zero exclusion)
  - paper: doi:10.1109/TAC.1987.1104459
    title: B. D. O. Anderson, E. I. Jury and M. Mansour, On robust Hurwitz polynomials, IEEE Transactions on Automatic Control 32(10), 1987
    locator: the reduction to fewer than four polynomials for degrees 3, 4 and 5
---

Kharitonov's theorem answers a question that looks hopeless at first: if each coefficient of a characteristic polynomial is only known to lie in an interval, are all the polynomials in this box Hurwitz? The box has infinitely many members and $2^{n+1}$ corners for degree $n$. Kharitonov showed in 1978 that it is enough to test four particular corner polynomials, built from the interval ends in a fixed pattern. Each test is one [Routh-Hurwitz](/routh-hurwitz-criterion/) check, so robust stability of an interval polynomial costs four times as much as stability of one polynomial. The result needs the coefficients to vary independently, which is rarely exactly true for a physical system; for coefficients that depend on common parameters, the [edge theorem](/edge-theorem/) takes over.

## Statement

**Setting.** For real numbers $x_i \le y_i$, $i = 0, 1, \dots, n$, the interval polynomial family is

$$\mathcal{I} = \{\, \delta_0 + \delta_1 s + \dots + \delta_n s^n : x_i \le \delta_i \le y_i \text{ for each } i \,\}.$$

Assume $0 \notin [x_n, y_n]$, so every member has degree $n$; after multiplication by $-1$ if needed, $x_n > 0$. A real polynomial is Hurwitz if all its roots have negative real part. The four Kharitonov polynomials repeat the pattern of lower ($x$) and upper ($y$) ends with period 4 in the index:

$$\begin{aligned}
K_1(s) &= x_0 + x_1 s + y_2 s^2 + y_3 s^3 + x_4 s^4 + x_5 s^5 + y_6 s^6 + \dots \\
K_2(s) &= x_0 + y_1 s + y_2 s^2 + x_3 s^3 + x_4 s^4 + y_5 s^5 + y_6 s^6 + \dots \\
K_3(s) &= y_0 + x_1 s + x_2 s^2 + y_3 s^3 + y_4 s^4 + x_5 s^5 + x_6 s^6 + \dots \\
K_4(s) &= y_0 + y_1 s + x_2 s^2 + x_3 s^3 + y_4 s^4 + y_5 s^5 + x_6 s^6 + \dots
\end{aligned}$$

**Theorem (Kharitonov 1978).** Every polynomial in $\mathcal{I}$ is Hurwitz if and only if $K_1$, $K_2$, $K_3$ and $K_4$ are Hurwitz.

## In plain words

Put $s = j\omega$ into every polynomial of the box. At each frequency the values fill a rectangle in the complex plane with sides parallel to the axes, and the four Kharitonov polynomials sit at its four corners. A member of the box can only lose stability by having a root cross the imaginary axis, and at that frequency the rectangle would have to contain the origin. The corners of a Hurwitz polynomial turn around the origin in one direction only, counterclockwise. If all four corners do this, the rectangle can never sweep over the origin, so no member can lose stability.

## Proof

The "only if" part holds because the four $K_i$ are members of $\mathcal{I}$. For the "if" part, assume the $K_i$ are Hurwitz. Three facts are used.

**Fact 1 (monotone phase).** If $p$ is Hurwitz, the argument of $p(j\omega)$ is a strictly increasing function of $\omega$. Write $p(s) = a_n \prod_k (s - \lambda_k)$ with $\lambda_k = -\sigma_k + j\beta_k$, $\sigma_k > 0$. Then $\arg p(j\omega) = \arg a_n + \sum_k \arctan((\omega - \beta_k)/\sigma_k)$, and each term increases strictly. In particular $p(j\omega) \ne 0$ for all $\omega$.

**Fact 2 (the value set is a rectangle).** For $\omega \ge 0$ and $p \in \mathcal{I}$,

$$p(j\omega) = (\delta_0 - \delta_2 \omega^2 + \delta_4 \omega^4 - \dots) + j\omega(\delta_1 - \delta_3 \omega^2 + \delta_5 \omega^4 - \dots).$$

The real part depends only on the even coefficients and the imaginary part only on the odd ones. The real part is smallest with $x_0, y_2, x_4, y_6, \dots$ (the even part of $K_1$ and $K_2$) and largest with $y_0, x_2, y_4, x_6, \dots$ (the even part of $K_3$ and $K_4$). For $\omega > 0$ the imaginary part is smallest with $x_1, y_3, x_5, \dots$ ($K_1$ and $K_3$) and largest with $y_1, x_3, y_5, \dots$ ($K_2$ and $K_4$). Since the two parts use disjoint sets of coefficients that vary independently, and each part takes every value between its extremes, the value set $\{p(j\omega) : p \in \mathcal{I}\}$ is the rectangle $R(\omega)$ with corners $K_1(j\omega)$ (lower left), $K_2(j\omega)$ (upper left), $K_3(j\omega)$ (lower right) and $K_4(j\omega)$ (upper right). The rectangle may be degenerate (a segment or a point).

**Fact 3 (zero exclusion).** If some member $q$ of $\mathcal{I}$ is not Hurwitz, then $0 \in R(\omega)$ for some $\omega \ge 0$. Indeed, the box is convex, so $p_t = (1 - t) K_1 + t q$ lies in $\mathcal{I}$ for $t \in [0, 1]$, and all $p_t$ have degree $n$. The roots of $p_t$ depend continuously on $t$ and cannot go to infinity, because the leading coefficient stays away from 0. At $t = 0$ they are all in the open left half plane, and at $t = 1$ one is not, so for some $t$ a root lies on the imaginary axis: $p_t(j\omega) = 0$. Since $p_t$ has real coefficients, $p_t(-j\omega) = 0$ too, so $\omega \ge 0$ can be taken.

**Conclusion.** Suppose $0 \in R(\omega)$ for some $\omega \ge 0$. At $\omega = 0$, $R(0)$ is the real interval $[x_0, y_0]$, and $x_0 > 0$ because $K_1$ is Hurwitz with positive leading coefficient, so all its coefficients are positive. The corners move continuously with $\omega$, so the set of $\omega$ with $0 \in R(\omega)$ is closed and has a smallest element $\omega_0 > 0$. At $\omega_0$ the origin is not a corner (Fact 1), and it is not inside $R(\omega)$ for $\omega$ slightly below $\omega_0$. So the origin lies on an edge of $R(\omega_0)$, between two corners on opposite sides of an axis, and for $\omega$ slightly below $\omega_0$ the rectangle lies strictly on one side of that axis. Take the case of the left edge, from $K_1$ to $K_2$, on the imaginary axis: $\operatorname{Re} K_1(j\omega_0) = 0$, $\operatorname{Im} K_1(j\omega_0) < 0 < \operatorname{Im} K_2(j\omega_0)$.

- If the rectangle was in $\operatorname{Re} > 0$ just before $\omega_0$, then $K_1(j\omega)$ was in the open fourth quadrant and reaches the negative imaginary axis at $\omega_0$. Moving from the fourth quadrant onto the negative imaginary axis decreases the argument, which contradicts Fact 1 for $K_1$.
- If the rectangle was in $\operatorname{Re} < 0$, then $K_2(j\omega)$ moves from the open second quadrant onto the positive imaginary axis, which again decreases the argument, against Fact 1 for $K_2$.

The other three edges are the same with the roles of the corners rotated: on the right edge ($K_3$ to $K_4$) use $K_4$ or $K_3$, on the bottom edge ($K_1$ to $K_3$) use $K_3$ or $K_1$, and on the top edge ($K_2$ to $K_4$) use $K_2$ or $K_4$. In every case one corner would have to turn clockwise. So $0 \notin R(\omega)$ for all $\omega \ge 0$, and by Fact 3 every member of $\mathcal{I}$ is Hurwitz.

## Consequences

- **Cost.** The test is four Hurwitz tests, $O(n^2)$ arithmetic operations with the [Routh array](/routh-array/), against $2^{n+1}$ corners or a continuum of members.
- **Fewer polynomials for low degree.** Anderson, Jury and Mansour (1987) showed that for degrees 3, 4 and 5, one, two and three of the four polynomials suffice. For degree 3 with positive coefficients, the Hurwitz condition is $\delta_2 \delta_1 > \delta_3 \delta_0$, and the worst member has small $\delta_1, \delta_2$ and large $\delta_0, \delta_3$, which is $K_3$.
- **Robust stability of a loop.** If the closed-loop characteristic polynomial has coefficients in known independent intervals, the loop is robustly stable exactly when the four polynomials are Hurwitz. For an interval plant in a loop with a fixed controller, the coefficients are usually not independent, and the edge theorem or its refinements are needed.
- **A sufficient test for dependent coefficients.** If the coefficients depend on parameters in any way, take their ranges as intervals. The interval box contains the true family, so four Hurwitz polynomials still prove robust stability; a failure proves nothing.

**Example.** $p(s) = s^3 + \delta_2 s^2 + \delta_1 s + \delta_0$ with $\delta_2 \in [2, 3]$, $\delta_1 \in [2, 4]$, $\delta_0 \in [1, 3]$. The Kharitonov polynomials are

$$K_1 = s^3 + 3 s^2 + 2 s + 1, \quad K_2 = s^3 + 3 s^2 + 4 s + 1, \quad K_3 = s^3 + 2 s^2 + 2 s + 3, \quad K_4 = s^3 + 2 s^2 + 4 s + 3 .$$

The cubic test $a_2 a_1 > a_0$ gives $6 > 1$, $12 > 1$, $4 > 3$ and $8 > 3$, so the whole family is Hurwitz. At $\omega = 1$ the value set is the rectangle $[-2, 1] \times [1, 3]$ (real part $\delta_0 - \delta_2$, imaginary part $\delta_1 - 1$), which does not contain 0. If the range of $\delta_0$ is widened to $[1, 5]$, then $K_3 = s^3 + 2 s^2 + 2 s + 5$ fails ($4 < 5$), and $K_3$ itself is a member that is not Hurwitz.

## Tightness

- **Independence is needed for the "only if" direction of the box test.** Take $p_q(s) = s^3 + (2 + q) s^2 + (2 - q) s + 1$ with $q \in [-1, 1]$. Every member is Hurwitz, because $(2 + q)(2 - q) = 4 - q^2 \ge 3 > 1$. The interval box of the coefficients is $[1, 3] \times [1, 3]$ for $\delta_2, \delta_1$, and its $K_3 = s^3 + s^2 + s + 1 = (s + 1)(s^2 + 1)$ has roots $\pm j$. So the box test fails although the family is robustly stable: $K_3$ is not a member, because $\delta_2 = \delta_1 = 1$ needs $q = -1$ and $q = 1$ at once.
- **The theorem is about the left half plane.** The proof uses that the boundary is the imaginary axis, where the value set splits into an even part and an odd part and so becomes a rectangle with the four $K_i$ at its corners. For other root regions, such as the unit disc (Schur stability) or a sector of guaranteed damping, the value set is not such a rectangle and the proof does not carry over; the [edge theorem](/edge-theorem/) is the general tool there.
- **The leading interval.** The proof keeps the degree fixed along the path of Fact 3, so that no root can enter from infinity. This is why the theorem assumes $0 \notin [x_n, y_n]$.

## History

V. L. Kharitonov published the theorem in 1978 in the Soviet journal Differentsial'nye Uravneniya. It became widely known outside the Soviet Union in the 1980s and started the parametric approach to robust control: interval polynomials, polytopes of polynomials and the [edge theorem](/edge-theorem/) of Bartlett, Hollot and Lin (1988). The proof above, by the rectangular value set and zero exclusion, follows the later presentations, as in Bhattacharyya, Chapellat and Keel (1995).

## References
