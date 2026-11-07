---
tag: MMBZW0
kind: theorem
slug: fundamental-theorem-of-algebra
name: Fundamental theorem of algebra
aliases:
- d'Alembert-Gauss theorem
- existence of complex roots
- FTA
area: numerical/root-finding
level: intro
summary: Every nonconstant complex polynomial has a complex root, so a polynomial of degree n has exactly n roots counted with multiplicity.
prereqs: [polynomial, factor-theorem]
see_also: [abel-ruffini-theorem, polynomial-root-finding, durand-kerner-method, aberth-ehrlich-method, companion-matrix-method, vieta-formulas, homotopy-continuation, gauss-lucas-theorem]
sources:
  - book: "Heinz-Dieter Ebbinghaus et al., Numbers, Graduate Texts in Mathematics 123, Springer, 1991"
    locator: Chapter 4 (by Reinhold Remmert), The fundamental theorem of algebra (the proofs, among them the proof by d'Alembert's lemma and the minimum of the modulus, and the history from d'Alembert and Gauss to Argand)
  - book: "Benjamin Fine and Gerhard Rosenberger, The Fundamental Theorem of Algebra, Undergraduate Texts in Mathematics, Springer, 1997"
    locator: the historical introduction and the analytic proof by the minimum of the modulus
  - paper: doi:10.1090/S0273-0979-1981-14858-8
    title: Steve Smale, The fundamental theorem of algebra and complexity theory, Bulletin of the American Mathematical Society (New Series) 4(1), 1-36, 1981
    locator: the cost of finding an approximate root by a Newton-type path method
  - paper: doi:10.1137/S0036144595288554
    title: Victor Y. Pan, Solving a polynomial equation, some history and recent progress, SIAM Review 39(2), 187-220, 1997
    locator: the history of the theorem and of the constructive proofs that lead to algorithms
---

The fundamental theorem of algebra says that every [polynomial](/polynomial/) of degree $n \ge 1$ with complex coefficients has a root in $\mathbb{C}$. With the [factor theorem](/factor-theorem/) it follows that such a polynomial is the product of $n$ linear factors, so it has exactly $n$ roots counted with [multiplicity](/multiplicity-of-roots/). The theorem says that the roots exist, not how to find them; there is no formula in radicals from degree 5 on ([Abel-Ruffini theorem](/abel-ruffini-theorem/)), so [polynomial root finding](/polynomial-root-finding/) uses iterative methods, and the count $n$ tells those methods how many roots to look for.

## Statement

Let $p(z) = a_n z^n + a_{n-1} z^{n-1} + \cdots + a_0$ with $a_j \in \mathbb{C}$, $n \ge 1$ and $a_n \ne 0$.

**Theorem.** There is $z^* \in \mathbb{C}$ with $p(z^*) = 0$.

**Corollary (factorization).** There are $z_1, \ldots, z_n \in \mathbb{C}$, unique up to order, with

$$p(z) = a_n (z - z_1)(z - z_2) \cdots (z - z_n) \quad \text{for all } z \in \mathbb{C}.$$

The number of indices $i$ with $z_i = w$ is the multiplicity of $w$ as a root, and the multiplicities add up to $n$.

**Corollary (real coefficients).** If all $a_j$ are real, the non-real roots come in conjugate pairs $w, \bar w$ of the same multiplicity, and $p$ is a product of real linear factors and real quadratic factors $z^2 - 2\operatorname{Re}(w) z + |w|^2$ with no real root. A real polynomial of odd degree has a real root.

## In plain words

A polynomial is a sum of powers of the unknown, each with a fixed number in front. The theorem says that if you allow complex numbers, each such sum with at least one power above zero is zero at some point. You can then divide out that root and repeat. So a polynomial whose highest power is the fifth has exactly five roots, if you count a repeated root as often as it repeats. With only real numbers this fails: the square of a real number plus one is never zero. The complex numbers are exactly large enough to hold all the roots. The theorem gives no recipe to find the roots; numerical methods do that.

## Proof

The proof uses two facts from analysis: a continuous real function on a closed disc attains its minimum (the extreme value theorem), and each complex number $c$ has a $k$-th root for each $k \ge 1$ (from the polar form $c = r e^{i\theta}$, take $r^{1/k} e^{i\theta/k}$).

*Step 1: $|p|$ attains a global minimum.* Let $S = |a_0| + \cdots + |a_{n-1}|$ and $R = \max(1, (S + |a_0|)/|a_n|)$. For $|z| \ge R$ we have $|z| \ge 1$, so $|a_j z^j| \le |a_j||z|^{n-1}$ for $j < n$, and

$$|p(z)| \ge |a_n||z|^n - S|z|^{n-1} = |z|^{n-1}\big(|a_n||z| - S\big) \ge |z|^{n-1} |a_0| \ge |a_0| = |p(0)|.$$

The function $|p|$ is continuous, so it attains a minimum on the closed disc $|z| \le R$ at some point $z_0$. Since $0$ is in the disc, $|p(z_0)| \le |p(0)|$, and the display shows $|p(z)| \ge |p(0)| \ge |p(z_0)|$ outside the disc. So $|p(z_0)| \le |p(z)|$ for all $z \in \mathbb{C}$.

*Step 2: d'Alembert's lemma. If $p(z_0) \ne 0$, then some $z$ has $|p(z)| < |p(z_0)|$.* Expand $p$ around $z_0$: $p(z_0 + h) = b_0 + b_1 h + \cdots + b_n h^n$, with $b_0 = p(z_0)$ and $b_n = a_n \ne 0$. Let $k \ge 1$ be the least index with $b_k \ne 0$. Let $\omega$ be a $k$-th root of $-b_0/b_k$, so $b_k \omega^k = -b_0$. For real $t$ with $0 < t \le 1$,

$$p(z_0 + t\omega) = b_0 - b_0 t^k + \sum_{j=k+1}^{n} b_j \omega^j t^j = b_0(1 - t^k) + t^{k+1} Q(t),$$

where $|Q(t)| \le M = \sum_{j > k} |b_j||\omega|^j$ because $t \le 1$. Hence

$$|p(z_0 + t\omega)| \le |b_0|(1 - t^k) + M t^{k+1} = |b_0| - t^k\big(|b_0| - M t\big).$$

If $M = 0$, take $t = 1$. Otherwise take $0 < t < \min(1, |b_0|/M)$. In both cases $|b_0| - Mt > 0$, so $|p(z_0 + t\omega)| < |b_0| = |p(z_0)|$.

*Step 3.* The point $z_0$ of Step 1 is a global minimum of $|p|$. If $p(z_0) \ne 0$, Step 2 gives a point with a smaller value, which is impossible. So $p(z_0) = 0$, and $z^* = z_0$ is a root.

*The factorization.* By induction on $n$. For $n = 1$, $p(z) = a_1(z - z_1)$ with $z_1 = -a_0/a_1$. For $n \ge 2$, the theorem gives a root $z_n$, and the factor theorem gives $p(z) = (z - z_n) r(z)$ with $r$ of degree $n - 1$ and leading coefficient $a_n$. Apply the hypothesis to $r$. Uniqueness: if $a_n \prod (z - z_i) = a_n \prod (z - w_i)$, then $z_1$ is a root of the right side, so $z_1 = w_j$ for some $j$; cancel the common factor (the ring $\mathbb{C}[z]$ has no zero divisors) and use induction.

*Real coefficients.* If the $a_j$ are real, $\overline{p(z)} = p(\bar z)$. So $p(w) = 0$ implies $p(\bar w) = 0$. For non-real $w$, $(z - w)(z - \bar w) = z^2 - 2\operatorname{Re}(w)z + |w|^2$ is real, and dividing $p$ by it gives a real quotient with the same property. Induction on the degree pairs the non-real roots with equal multiplicities. A real polynomial of odd degree cannot have all its roots in pairs, so it has a real root. $\blacksquare$

## Consequences

- **The number of roots.** A method that looks for all roots at once, such as the [Durand-Kerner method](/durand-kerner-method/) and the [Aberth-Ehrlich method](/aberth-ehrlich-method/), starts with exactly $n$ approximations, because there are exactly $n$ roots with multiplicity.
- **[Vieta's formulas](/vieta-formulas/).** Expanding the factorization gives $\sum_i z_i = -a_{n-1}/a_n$ and $\prod_i z_i = (-1)^n a_0/a_n$, and the other elementary symmetric functions. For $z^4 + 4 = (z^2 - 2z + 2)(z^2 + 2z + 2)$ the roots are $\pm 1 \pm i$, their sum is 0 and their product is 4.
- **Eigenvalues.** The [characteristic polynomial](/characteristic-polynomial/) of an $n \times n$ complex matrix has degree $n$, so each such matrix has an [eigenvalue](/eigenvalue/). The [companion matrix method](/companion-matrix-method/) uses the converse: the roots of $p$ are the eigenvalues of a matrix.
- **Deflation.** After one root is found, [deflation](/polynomial-deflation/) divides it out and leaves a polynomial of degree $n - 1$, which by the theorem has the remaining roots.
- **Partial fractions.** Over $\mathbb{C}$ each rational function splits into terms $c/(z - z_i)^j$ ([partial fraction decomposition](/partial-fraction-decomposition/)).
- **A descent step.** Step 2 is constructive. It shows that at a non-root there is a direction in which $|p|$ falls, and minimum-modulus methods search along such directions. Smale (1981) followed a path of Newton steps to turn the theorem into an algorithm with a cost bound, an idea close to [homotopy continuation](/homotopy-continuation/).

## Tightness

- **The field.** Over $\mathbb{R}$ the theorem fails: $z^2 + 1$ has no real root. Over $\mathbb{Q}$, $z^2 - 2$ has no root. The theorem says that $\mathbb{C}$ is algebraically closed.
- **Degree at least 1.** A nonzero constant has no root.
- **Polynomials, not all smooth functions.** The entire function $e^z$ has no zero in $\mathbb{C}$. Step 1 needs the growth $|p(z)| \to \infty$, which $e^z$ does not have along the negative real axis.
- **Existence, not a formula.** The proof gives no formula for the root. By the Abel-Ruffini theorem there is no formula in radicals for degree 5 and more, so the theorem cannot be improved to a closed form.
- **The count.** The count $n$ is exact only with multiplicity: $(z - 1)^3$ has one distinct root of multiplicity 3.

## History

D'Alembert gave an incomplete proof in 1746, based on the lemma of Step 2. Gauss gave a proof in his 1799 doctoral thesis, and three more proofs later. Argand gave the proof by the minimum of the modulus in 1806 and 1814; it needs the existence of the minimum, which Weierstrass's theorem on continuous functions later made rigorous. Remmert (in Ebbinghaus et al., Chapter 4) and Fine and Rosenberger tell this history. Smale (1981) and later work gave the theorem a complexity theory: how many steps an algorithm needs to find an approximate root.

## References
