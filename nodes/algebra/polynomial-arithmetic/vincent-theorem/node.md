---
tag: 2B10DH
kind: theorem
slug: vincent-theorem
name: Vincent's theorem
aliases:
- Vincent's continued fraction theorem
- Vincent-Akritas theorem
- one-circle and two-circle theorems
area: algebra/polynomial-arithmetic
level: advanced
summary: Repeated transformation and sign-variation counting isolates the real roots of a polynomial.
prereqs: [descartes-rule-of-signs, continued-fraction]
see_also: [vincent-collins-akritas, descartes-rule-of-signs, real-root-isolation, sturm-theorem, continued-fraction, budan-fourier-theorem, multiplicity-of-roots, cauchy-root-bound]
sources:
  - url: https://www.numdam.org/item/JMPA_1836_1_1__341_0/
    title: Alexandre Joseph Hidulphe Vincent, Note sur la résolution des équations numériques, Journal de Mathématiques Pures et Appliquées, first series, volume 1, 1836
    locator: pp. 341 to 372
  - paper: doi:10.2307/1969443
    title: Alexander M. Ostrowski, Note on Vincent's theorem, Annals of Mathematics, second series, 52(3), 1950
    locator: pp. 702 to 707
  - paper: doi:10.1016/j.jsc.2005.02.004
    title: Werner Krandick and Kurt Mehlhorn, New bounds for the Descartes method, Journal of Symbolic Computation 41(1), 2006
    locator: pp. 49 to 66 (proofs of the one-circle and two-circle theorems)
  - paper: doi:10.1145/1145768.1145786
    title: Arno Eigenwillig, Vikram Sharma and Chee K. Yap, Almost tight recursion tree bounds for the Descartes method, ISSAC 2006
    locator: Section 2, Propositions 2.2 and 2.3 (one-circle and two-circle theorems)
  - book: isbn:9780195125160
    title: Chee K. Yap, Fundamental Problems of Algorithmic Algebra, Oxford University Press, 2000
    locator: Section 6.6 (root separation bounds)
---

Vincent's theorem says that a real polynomial, transformed so that a small enough interval becomes the positive half-line, has at most one sign variation in its coefficients. Then [Descartes' rule of signs](/descartes-rule-of-signs/) is exact, and the interval holds no root or exactly one. The modern form gives the condition as two regions in the complex plane: no root in one disc gives no sign variation, and exactly one root in a two-disc region gives exactly one. It is the termination argument for the [Vincent-Collins-Akritas](/vincent-collins-akritas/) method and for the [continued fraction](/continued-fraction/) method of [real root isolation](/real-root-isolation/).

## Statement

Let $p \in \mathbb{R}[x]$ have degree $n \ge 1$. For a list of reals, $\operatorname{Var}$ is the number of sign changes after the zeros are removed. For real $a \ne b$ define the *interval transform*

$$T_{a,b}\,p(y) = (y + 1)^n \, p\!\left(\frac{a y + b}{y + 1}\right),$$

a polynomial in $y$. The map $y \mapsto (ay + b)/(y + 1)$ sends $(0, \infty)$ one to one onto the open interval between $b$ and $a$, so the positive roots of $T_{a,b}\,p$ are the images of the roots of $p$ in that interval, with the same multiplicities. Let $\operatorname{Var}(T_{a,b}\,p)$ be the number of sign variations of its coefficients.

For $\alpha \in \mathbb{C} \setminus \{a, b\}$ let $\theta(\alpha) = |\arg((b - \alpha)/(a - \alpha))| \in [0, \pi]$, the angle at $\alpha$ in the triangle with corners $a$, $\alpha$, $b$. Let $w = |b - a|$ and $m = (a + b)/2$. Define

- $D_{a,b} = \{\alpha : \theta(\alpha) > \pi/2\}$, the open disc with diameter $[a, b]$;
- $E_{a,b} = \{\alpha : \theta(\alpha) > \pi/3\}$, the union of the two open discs with centres $m \pm i\,w\sqrt{3}/6$ whose boundary circles pass through $a$ and $b$.

Roots of $p$ at $a$ or $b$ are allowed; they are not counted in the hypotheses.

**Theorem.**

1. **(One circle.)** If no root of $p$ lies in $D_{a,b}$, then $\operatorname{Var}(T_{a,b}\,p) = 0$.
2. **(Two circles.)** If exactly one root of $p$, counted with multiplicity, lies in $E_{a,b}$, then that root is real and lies between $a$ and $b$, and $\operatorname{Var}(T_{a,b}\,p) = 1$.
3. **(Vincent's theorem.)** Let $p$ be [square-free](/square-free-polynomial/) of degree $n \ge 2$, and let $\operatorname{sep}(p) > 0$ be the least distance between two distinct complex roots of $p$. If $|b - a| \le \operatorname{sep}(p)/\sqrt 3$, then $\operatorname{Var}(T_{a,b}\,p) \in \{0, 1\}$, and it equals the number of roots of $p$ strictly between $a$ and $b$.
4. **(Continued fraction form.)** Let $a_0 \in \mathbb{Z}$ and $a_1, \ldots, a_k \ge 1$ be integers with $k \ge 1$, and let $P_j/Q_j$ be the convergents of $[a_0; a_1, \ldots, a_k]$. Put $p_k(z) = (Q_k z + Q_{k-1})^n \, p\big((P_k z + P_{k-1})/(Q_k z + Q_{k-1})\big)$, the polynomial obtained by the substitution $x = [a_0; a_1, \ldots, a_k, z]$. With $p$ as in part 3, if $Q_k Q_{k-1} \ge \sqrt 3/\operatorname{sep}(p)$, then $p_k$ has at most one sign variation, and it has one exactly when $p$ has a root strictly between $P_{k-1}/Q_{k-1}$ and $P_k/Q_k$. This holds for every choice of the $a_j$ once $k \ge \big(3 + \log_\phi(\sqrt 3/\operatorname{sep}(p))\big)/2$, where $\phi = (1 + \sqrt 5)/2$.

Part 4 is the form in which Vincent stated the result: after enough substitutions $x = a + 1/y$ with positive integers $a$, the transformed equation has at most one sign variation. Parts 1 and 2 are the one-circle and two-circle theorems in the form of Eigenwillig, Sharma and Yap, Propositions 2.2 and 2.3.

## In plain words

Pick an interval on the real line and stretch it, by a simple change of variable, so that it becomes all positive numbers. Then count the sign changes in the list of coefficients of the new polynomial. That count is never smaller than the number of roots in the interval, and the two differ by an even number. The theorem says when the count is exact. If no root, real or complex, is close to the interval, the count is zero. If exactly one root is close and all other roots are farther away, the count is one. So once the interval is short compared with the gaps between the roots, the count is zero or one, and it tells you directly whether the interval holds a root.

## Proof

Throughout, $p = \operatorname{lc}(p) \prod_{i=1}^{n}(x - \alpha_i)$ over $\mathbb{C}$, with roots repeated by multiplicity.

**Step 1: a product formula.** Since $(ay + b) - \alpha (y + 1) = (a - \alpha) y + (b - \alpha)$,

$$T_{a,b}\,p(y) = \operatorname{lc}(p) \prod_{i=1}^{n} \ell_i(y), \qquad \ell_i(y) = (a - \alpha_i)\, y + (b - \alpha_i).$$

No $\ell_i$ is zero because $a \ne b$. The root of $\ell_i$ is $y_i = -(b - \alpha_i)/(a - \alpha_i)$; it is positive exactly when $\alpha_i$ is real and strictly between $a$ and $b$, and $y_i \mapsto \alpha_i$ under $y \mapsto (ay + b)/(y + 1)$. This proves the remark on positive roots in the statement. If $\alpha_i = a$, then $\ell_i$ is the nonzero constant $b - a$; if $\alpha_i = b$, then $\ell_i = (a - b)\,y$. Neither changes $\operatorname{Var}$ of a product, since multiplying by a nonzero constant or by $y$ keeps the sign pattern.

**Step 2: the regions.** Put $h = (b - a)/2$ and $\zeta = (\alpha - m)/h$. Then $(b - \alpha)/(a - \alpha) = (1 - \zeta)/(-1 - \zeta) = (\zeta - 1)/(\zeta + 1)$, so $\theta(\alpha)$ is the absolute value of the argument of $(\zeta - 1)/(\zeta + 1)$, which has the same argument as $(\zeta - 1)(\bar\zeta + 1) = |\zeta|^2 - 1 + 2 i \eta$, where $\eta = \operatorname{Im}\zeta$. For a complex number $s$, $|\arg s| > \pi/2$ means $\operatorname{Re} s < 0$, and $|\arg s| > \pi/3$ means $\operatorname{Re} s < |\operatorname{Im} s|/\sqrt 3$. So:

- $\theta(\alpha) > \pi/2$ if and only if $|\zeta| < 1$, that is, $|\alpha - m| < w/2$: the disc with diameter $[a, b]$.
- $\theta(\alpha) > \pi/3$ if and only if $|\zeta|^2 - 1 < 2|\eta|/\sqrt 3$, that is, $\operatorname{Re}(\zeta)^2 + (|\eta| - 1/\sqrt 3)^2 < 4/3$: the union of the discs with centres $\pm i/\sqrt 3$ and radius $2/\sqrt 3$, which in terms of $\alpha$ have centres $m \pm i\, w\sqrt 3/6$ and radius $w/\sqrt 3$.

Both regions are symmetric under complex conjugation. A real $\alpha$ strictly between $a$ and $b$ has $\theta = \pi$, and a real $\alpha$ outside $[a, b]$ has $\theta = 0$. So both regions meet the real line in the open interval between $a$ and $b$. Also $D_{a,b} \subseteq E_{a,b}$.

**Step 3: the real part.** For each $i$ with $\alpha_i \notin \{a, b\}$,

$$\operatorname{Re}\frac{b - \alpha_i}{a - \alpha_i} = \frac{\operatorname{Re}\big((b - \alpha_i)\overline{(a - \alpha_i)}\big)}{|a - \alpha_i|^2},$$

and for a non-real root the pair $\ell_i$, $\ell_j$ with $\alpha_j = \bar\alpha_i$ multiplies to

$$\ell_i \ell_j = |a - \alpha_i|^2 y^2 + 2 \operatorname{Re}\big((a - \alpha_i)\overline{(b - \alpha_i)}\big)\, y + |b - \alpha_i|^2,$$

a real quadratic. For a real root, $\ell_i$ is real and its two coefficients have product $(a - \alpha_i)(b - \alpha_i)$.

**Proof of part 1.** Assume no root lies in $D_{a,b}$. For a real root $\alpha_i \notin \{a, b\}$, it lies outside the open interval, so $(a - \alpha_i)(b - \alpha_i) > 0$ and both coefficients of $\ell_i$ have the same sign. For a non-real pair, $\theta(\alpha_i) \le \pi/2$ means the real part in step 3 is $\ge 0$, so all three coefficients of $\ell_i \ell_j$ are $\ge 0$. So $T_{a,b}\,p$ is a nonzero constant times a product of nonzero polynomials with nonnegative coefficients. Such a product has nonnegative coefficients, so $\operatorname{Var}(T_{a,b}\,p) = 0$.

**Two lemmas for part 2.** Call a list $c_0, \ldots, c_d$ of positive reals *log-concave* if $c_i^2 \ge c_{i-1} c_{i+1}$ for $0 < i < d$.

*Lemma A. If $u$ and $v$ have positive log-concave coefficient lists, so does $uv$.* Extend each list by zeros to all integer indices, and for a list $c$ let $M_c$ be the matrix with entry $c_{j - i}$ in row $i$ and column $j$. (i) Every $2 \times 2$ minor of $M_c$ is $\ge 0$. With rows $i_1 < i_2$ and columns $j_1 < j_2$ the minor is $c_{\beta} c_{\gamma} - c_{s} c_{t}$, where $\beta = j_1 - i_1$, $\gamma = j_2 - i_2$, $s = j_1 - i_2$ and $t = j_2 - i_1$. Here $s < \beta \le t$, $s \le \gamma < t$ and $\beta - s = t - \gamma = i_2 - i_1$. If $c_s c_t = 0$ the minor is $\ge 0$. Otherwise $s$ and $t$ lie in $[0, d]$, so $\beta$ and $\gamma$ do too, and all four entries are positive. Log-concavity says the ratios $r_i = c_{i+1}/c_i$ are nonincreasing in $i$. So $c_\beta / c_s = \prod_{e=0}^{\beta - s - 1} r_{s + e} \ge \prod_{e=0}^{t - \gamma - 1} r_{\gamma + e} = c_t / c_\gamma$, because $s \le \gamma$; this is $c_\beta c_\gamma \ge c_s c_t$. (ii) $M_u M_v = M_{uv}$, since the entry in row $i$ and column $j$ of the product is $\sum_l u_{l - i} v_{j - l} = (uv)_{j - i}$. (iii) By the Cauchy-Binet formula, a $2 \times 2$ minor of $M_u M_v$ is a sum of products of $2 \times 2$ minors of $M_u$ and $M_v$ (a finite sum, since the lists are finite), so it is $\ge 0$. The minor of $M_{uv}$ in rows $0, 1$ and columns $k, k + 1$ is $(uv)_k^2 - (uv)_{k+1}(uv)_{k-1}$. Finally every coefficient of $uv$ from degree $0$ to $\deg u + \deg v$ is positive, since it is a sum of nonnegative terms of which at least one is positive.

*Lemma B. If $g$ has a positive log-concave coefficient list $g_0, \ldots, g_d$ and $\rho > 0$, then $(y - \rho)\, g$ has exactly one sign variation.* Its coefficients are $e_i = g_{i-1} - \rho g_i$ for $0 \le i \le d + 1$, with $g_{-1} = g_{d+1} = 0$. So $e_0 = -\rho g_0 < 0$ and $e_{d+1} = g_d > 0$. For $1 \le i \le d$, $e_i = g_i (q_i - \rho)$ with $q_i = g_{i-1}/g_i$, and log-concavity says $q_i$ is nondecreasing. So the signs of $e_0, \ldots, e_{d+1}$ are first negative, then possibly zero, then positive, which is exactly one sign variation.

**Proof of part 2.** Let $\alpha_1$ be the only root in $E_{a,b}$. If it were not real, $\bar\alpha_1 \ne \alpha_1$ would be a second root in $E_{a,b}$, by symmetry. So $\alpha_1$ is real, and by step 2 it lies strictly between $a$ and $b$. Then $(a - \alpha_1)(b - \alpha_1) < 0$ and $\ell_1 = (a - \alpha_1)(y - \rho)$ with $\rho = (\alpha_1 - b)/(a - \alpha_1) > 0$. Look at the other roots, none of which lies in $E_{a,b}$.

- A real root $\alpha_i \notin \{a, b\}$ lies outside $[a, b]$, so $\ell_i = (a - \alpha_i)(y + r_i)$ with $r_i = (b - \alpha_i)/(a - \alpha_i) > 0$. The list $r_i, 1$ is positive and log-concave.
- A non-real pair $\alpha_i, \alpha_j = \bar\alpha_i$ with $\theta(\alpha_i) \le \pi/3$: write $(b - \alpha_i)/(a - \alpha_i) = \sigma e^{i\varphi}$ with $\sigma > 0$ and $|\varphi| \le \pi/3$. Then $\ell_i = (a - \alpha_i)(y + \sigma e^{i\varphi})$, and $\ell_i \ell_j = |a - \alpha_i|^2 (y^2 + 2\sigma\cos\varphi\, y + \sigma^2)$. Since $\cos\varphi \ge 1/2$, the list $\sigma^2, 2\sigma\cos\varphi, 1$ is positive, and $(2\sigma\cos\varphi)^2 \ge \sigma^2$ makes it log-concave.
- Roots at $a$ or $b$ contribute a nonzero constant or a factor $y$, by step 1.

So $T_{a,b}\,p = C\, y^{e}\, (y - \rho)\, g(y)$ with a real constant $C \ne 0$, an integer $e \ge 0$, and $g$ a product of polynomials with positive log-concave coefficient lists ($g = 1$ if there are none). By Lemma A, $g$ has a positive log-concave list, and by Lemma B, $(y - \rho)\, g$ has one sign variation. The factors $C$ and $y^e$ do not change it. So $\operatorname{Var}(T_{a,b}\,p) = 1$.

**Proof of part 3.** By step 2, every point of $E_{a,b}$ lies in one of two open discs of radius $w/\sqrt 3$ whose centres are at distance $w\sqrt 3/6$ from $m$, so $|\alpha - m| < w/\sqrt 3 + w\sqrt 3/6 = w\sqrt 3/2$ for $\alpha \in E_{a,b}$. Two distinct roots in $E_{a,b}$ would be less than $w\sqrt 3 \le \operatorname{sep}(p)$ apart, which is impossible. Since $p$ is square-free, $E_{a,b}$ contains at most one root, counted with multiplicity. If it contains none, then neither does $D_{a,b} \subseteq E_{a,b}$, and part 1 gives $\operatorname{Var} = 0$. If it contains one, part 2 gives $\operatorname{Var} = 1$. In both cases $\operatorname{Var} \le 1$. By Descartes' rule of signs, $\operatorname{Var}$ minus the number of positive roots of $T_{a,b}\,p$ is even and nonnegative, so the two are equal. By step 1, the positive roots of $T_{a,b}\,p$ correspond to the roots of $p$ strictly between $a$ and $b$.

**Proof of part 4.** With $P_{-1} = 1$, $Q_{-1} = 0$, $P_0 = a_0$, $Q_0 = 1$ and $P_j = a_j P_{j-1} + P_{j-2}$, $Q_j = a_j Q_{j-1} + Q_{j-2}$, induction gives $[a_0; a_1, \ldots, a_k, z] = (P_k z + P_{k-1})/(Q_k z + Q_{k-1})$ and $P_k Q_{k-1} - P_{k-1} Q_k = (-1)^{k-1}$. Put $a = P_k/Q_k$ and $b = P_{k-1}/Q_{k-1}$, which is defined because $Q_{k-1} \ge 1$ for $k \ge 1$. Then $|b - a| = 1/(Q_k Q_{k-1})$. Substituting $y = (Q_k/Q_{k-1})\, z$ gives

$$\frac{P_k z + P_{k-1}}{Q_k z + Q_{k-1}} = \frac{a y + b}{y + 1}, \qquad (Q_k z + Q_{k-1})^n = Q_{k-1}^n (y + 1)^n,$$

so $p_k(z) = Q_{k-1}^n \, T_{a,b}\,p\big((Q_k/Q_{k-1})\, z\big)$. Replacing $y$ by a positive multiple of $z$ multiplies each coefficient by a positive number, so $\operatorname{Var}(p_k) = \operatorname{Var}(T_{a,b}\,p)$. If $Q_k Q_{k-1} \ge \sqrt 3/\operatorname{sep}(p)$, then $|b - a| \le \operatorname{sep}(p)/\sqrt 3$, and part 3 gives the claim. For the bound on $k$, let $F_1 = F_2 = 1$ and $F_{j+1} = F_j + F_{j-1}$ be the Fibonacci numbers. Then $Q_0 = 1 = F_1$, $Q_1 = a_1 \ge F_2$, and $Q_j \ge Q_{j-1} + Q_{j-2} \ge F_{j+1}$ by induction. Also $F_j \ge \phi^{j-2}$ for $j \ge 1$, by induction from $\phi^2 = \phi + 1$. So $Q_k Q_{k-1} \ge F_{k+1} F_k \ge \phi^{2k-3}$, which is at least $\sqrt 3/\operatorname{sep}(p)$ when $k$ satisfies the stated bound. $\blacksquare$

## Consequences

- **Termination of the Descartes method.** Bisection of an interval of length $w_0$ that contains all real roots reaches intervals of length at most $\operatorname{sep}(p)/\sqrt 3$ after $\lceil \log_2(\sqrt 3\, w_0/\operatorname{sep}(p)) \rceil$ levels, and by part 3 no interval at that depth is split again. This bounds the depth of the [Vincent-Collins-Akritas](/vincent-collins-akritas/) recursion. With the Davenport-Mahler bound on products of root distances, Eigenwillig, Sharma and Yap bound the size of the whole recursion tree by $O(n(L + \log n))$ for integer polynomials with coefficients less than $2^L$ in absolute value.
- **Termination of the continued fraction method.** Part 4 shows that the continued fraction method, which follows the partial quotients of each root, stops after a number of steps that is logarithmic in $1/\operatorname{sep}(p)$ on every branch.
- **Exact counts from Descartes' rule.** On an interval that satisfies part 1 or part 2, Descartes' rule gives the exact number of roots, $0$ or $1$, without a [Sturm sequence](/sturm-sequence/).
- **Root separation bounds.** For an integer polynomial, lower bounds on $\operatorname{sep}(p)$ in terms of $n$ and the coefficient size, such as Mahler's bound in Yap, Section 6.6, turn part 3 into an explicit bound on the bisection depth.

## Tightness

- **Square-free is needed in part 3.** For $p = x^2$ and any $a < 0 < b$, $T_{a,b}\,p$ has a double positive root, so by Descartes' rule $\operatorname{Var} \ge 2$ on every interval around $0$, however short.
- **The two-circle region cannot be replaced by the disc.** Take $a = -1$, $b = 1$ and $p = x(x^2 + 441/400)$, with roots $0$ and $\pm 1.05\, i$. The non-real roots lie outside $D_{-1,1}$, the unit disc, but inside $E_{-1,1}$. The transform is $\tfrac{1}{400}(841 - 759 y + 759 y^2 - 841 y^3)$, with three sign variations, although the interval holds only one root. So in part 2 the other roots must avoid $E_{a,b}$, not only $D_{a,b}$.
- **The conditions are sufficient, not necessary.** For $p = x^3 - 7x + 7$, with roots near $-3.0489$, $1.3569$ and $1.6920$, the separation is about $0.3351$ and $\operatorname{sep}(p)/\sqrt 3 \approx 0.1935$. Still $T_{1,3/2}\,p = -\tfrac18 - \tfrac14 y + y^2 + y^3$ and $T_{3/2,2}\,p = 1 + \tfrac12 y - \tfrac12 y^2 - \tfrac18 y^3$ each have one sign variation, on intervals of length $0.5$. On $(1, 2)$ the transform $T_{1,2}\,p = 1 - 2y - y^2 + y^3$ has two, matching the two roots there.

## History

Vincent (1836) proved that repeated substitutions $x = a + 1/y$, with positive integers $a$ chosen by the partial quotients of the roots, lead to an equation with at most one sign variation, and used this to separate the real roots. Ostrowski (1950) returned to the theorem in his note on it. Collins and Akritas (1976) used the same sign-variation test with bisection instead of continued fractions, which is the [Vincent-Collins-Akritas](/vincent-collins-akritas/) method. Krandick and Mehlhorn (2006) give proofs of the one-circle and two-circle theorems, and Eigenwillig, Sharma and Yap (2006) state them as Propositions 2.2 and 2.3 and use them to bound the recursion tree.

## References
