---
tag: 11KYBY
kind: theorem
slug: cauchy-root-bound
name: Cauchy root bound
aliases:
- Cauchy bound
- Cauchy bound on roots
- Cauchy's root bound
- Cauchy's bound on the zeros of a polynomial
area: numerical/root-finding
level: advanced
summary: Every root of a0 z^n + ... + an lies in the disc |z| <= R, where R is the positive root of |a0| x^n - |a1| x^(n-1) - ... - |an|, and R < 1 + max |ak/a0|.
prereqs: [fundamental-theorem-of-algebra]
see_also: [polynomial-root-finding, durand-kerner-method, aberth-ehrlich-method, jenkins-traub-algorithm, companion-matrix-method, gershgorin-circle-theorem, gauss-lucas-theorem, real-root-counting]
sources:
  - book: "Augustin-Louis Cauchy, Exercices de mathématiques, quatrième année, de Bure frères, Paris, 1829"
    locator: the bound on the moduli of the roots by the positive root of the associated polynomial with signs changed
  - book: "Morris Marden, Geometry of Polynomials, second edition, Mathematical Surveys 3, American Mathematical Society, 1966"
    locator: the chapter on bounds for the moduli of the zeros (Cauchy's theorem and its corollaries)
  - book: "Q. I. Rahman and G. Schmeisser, Analytic Theory of Polynomials, London Mathematical Society Monographs 26, Oxford University Press, 2002"
    locator: Chapter 8, Bounds for the zeros (Cauchy's bound, the Fujiwara bound and comparisons)
  - paper: "Matsusaburô Fujiwara, Über die obere Schranke des absoluten Betrages der Wurzeln einer algebraischen Gleichung, Tôhoku Mathematical Journal 10, 167-171, 1916"
    locator: the bound 2 max |ak/a0|^(1/k)
---

The Cauchy root bound gives a disc centred at 0 that contains every root of a polynomial, computed from the moduli of its coefficients alone. For $p(z) = a_0 z^n + a_1 z^{n-1} + \cdots + a_n$ with $a_0 \ne 0$, every root satisfies $|z| \le R$, where $R$ is the unique positive root of $|a_0| x^n - |a_1| x^{n-1} - \cdots - |a_n|$, and $R < 1 + \max_k |a_k/a_0|$. Applied to the reversed polynomial it gives a lower bound for the moduli of the nonzero roots. These bounds set the starting circle of simultaneous methods, the search interval of real root isolation, and the shift radius of the [Jenkins-Traub algorithm](/jenkins-traub-algorithm/).

## Statement

Let $p(z) = a_0 z^n + a_1 z^{n-1} + \cdots + a_n$ with complex coefficients, $n \ge 1$ and $a_0 \ne 0$, and assume that $a_1, \dots, a_n$ are not all zero (otherwise every root is 0). Let
$$q(x) = |a_0| x^n - |a_1| x^{n-1} - \cdots - |a_{n-1}| x - |a_n|$$
be the Cauchy polynomial of $p$, and $M = \max_{1 \le k \le n} |a_k/a_0|$.

**Theorem (Cauchy, 1829).**

1. $q$ has exactly one positive root $R$; $q(x) < 0$ on $(0, R)$ and $q(x) > 0$ on $(R, \infty)$.
2. Every root $z$ of $p$ satisfies $|z| \le R$.
3. $R < 1 + M$. So every root satisfies $|z| < 1 + M$.
4. (Fujiwara, 1916.) $R \le F = 2 \max\left(|a_1/a_0|, |a_2/a_0|^{1/2}, \dots, |a_{n-1}/a_0|^{1/(n-1)}, |a_n/(2a_0)|^{1/n}\right)$.
5. (Lower bound.) If $a_n \ne 0$, every root satisfies $|z| \ge r$, where $r$ is the unique positive root of $|a_0| x^n + |a_1| x^{n-1} + \cdots + |a_{n-1}| x - |a_n|$. Equivalently $r = 1/R'$, with $R'$ the bound of item 1 for the reversed polynomial $z^n p(1/z)$. In particular $|z| > |a_n|/(|a_n| + \max_{0 \le k < n}|a_k|)$.

Item 2 is sharp: if there is an angle $\theta$ with $a_k/a_0 = -|a_k/a_0|\,e^{ik\theta}$ for every $k \ge 1$, then $Re^{i\theta}$ is a root. The simplest case is $a_0 > 0$ and all $a_k \le 0$ real, where $R$ itself is a root.

## In plain words

If $z$ is very large, the leading term $a_0 z^n$ outweighs all the others put together, so $p(z)$ cannot be zero. The bound $R$ is the point beyond which the leading term always wins, even if all the other terms conspire against it with the same phase. Finding $R$ means solving one real equation with a single sign change, which bisection does in a few steps; the cruder bound $1 + M$ needs no solving at all. The same idea applied to $p(1/z)$ shows that the roots also cannot be too close to 0.

## Proof

*Item 1.* Since some $a_k \ne 0$ with $k \ge 1$, the function $\phi(x) = q(x)/x^n = |a_0| - \sum_{k=1}^{n}|a_k| x^{-k}$ is continuous and strictly increasing on $(0, \infty)$, tends to $-\infty$ as $x \to 0^+$ and to $|a_0| > 0$ as $x \to \infty$. So it has exactly one zero $R$, negative before and positive after, and $q = x^n\phi$ has the same signs.

*Item 2.* If $|z| > R$, the reverse triangle inequality gives
$$|p(z)| \ge |a_0||z|^n - \sum_{k=1}^{n}|a_k||z|^{n-k} = q(|z|) > 0,$$
so $z$ is not a root.

*Item 3.* Put $x = 1 + M > 1$. Then $\sum_{k=1}^{n}|a_k| x^{n-k} \le |a_0| M \sum_{k=1}^{n} x^{n-k} = |a_0| M \frac{x^n - 1}{x - 1} = |a_0|(x^n - 1)$, so $q(1 + M) \ge |a_0| > 0$, and $R < 1 + M$ by item 1.

*Item 4.* Put $x = F$. By the definition of $F$, $|a_k/a_0| \le (F/2)^k$ for $1 \le k < n$ and $|a_n/a_0| \le 2(F/2)^n$. Then
$$\sum_{k=1}^{n}\left|\frac{a_k}{a_0}\right| F^{n-k} \le F^n\left(\sum_{k=1}^{n-1} 2^{-k} + 2 \cdot 2^{-n}\right) = F^n\left(1 - 2^{1-n} + 2^{1-n}\right) = F^n,$$
so $q(F) \ge 0$, and $R \le F$ by item 1.

*Item 5.* If $a_n \ne 0$, the roots of $\tilde p(w) = w^n p(1/w) = a_n w^n + a_{n-1} w^{n-1} + \cdots + a_0$ are the reciprocals of the roots of $p$, all nonzero. Item 2 for $\tilde p$ gives $|1/z| \le R'$, so $|z| \ge 1/R'$. Substituting $x = 1/y$ in the Cauchy polynomial of $\tilde p$ and multiplying by $-y^n$ shows that $1/R'$ is the positive root of $|a_0| y^n + \cdots + |a_{n-1}| y - |a_n|$. Item 3 for $\tilde p$ gives $R' < 1 + \max_{k<n}|a_k/a_n|$, which is the last inequality. $\square$

*Sharpness.* If $a_k/a_0 = -|a_k/a_0|e^{ik\theta}$ for all $k \ge 1$, then $p(Re^{i\theta}) = a_0 e^{in\theta}\left(R^n - \sum_k |a_k/a_0| R^{n-k}\right) = e^{in\theta}\,\frac{a_0}{|a_0|}\,q(R) = 0$.

## Consequences

- **Example.** For $p(z) = z^3 - z - 2$, $q = p$, so $R = 1.5213797$ is the real root itself, and the complex roots have modulus $1.1464$. The crude bound is $1 + M = 3$, Fujiwara's is $F = 2$, the lower bound of item 5 is $1$.
- **A looser example.** For $\prod_{k=1}^{5}(z - k) = z^5 - 15z^4 + 85z^3 - 225z^2 + 274z - 120$, the largest root is 5, while $R = 19.88$, $F = 30$ and $1 + M = 275$. The bound ignores the signs of the coefficients, which here cancel strongly. Lagrange's bound $\max(1, \sum_k|a_k/a_0|) = 719$ is worse still.
- **Starting points.** The [Durand-Kerner](/durand-kerner-method/) and [Aberth-Ehrlich](/aberth-ehrlich-method/) pages cap their starting circle by Fujiwara's bound, so every root lies inside it.
- **Jenkins-Traub.** Stage 2 of the [Jenkins-Traub algorithm](/jenkins-traub-algorithm/) takes its shifts on a circle of radius $\beta$, the lower bound $r$ of item 5, so that the roots tend to be found in order of increasing modulus.
- **Real roots.** All real roots lie in $[-R, R]$, which gives the starting interval for [real root counting](/real-root-counting/) by Sturm sequences or Descartes' rule, and a bracket for [bisection](/bisection-method/).
- **Companion matrix.** The roots of $p$ are the eigenvalues of the [companion matrix](/companion-matrix-method/) with first row $-a_1/a_0, \dots, -a_n/a_0$ and ones on the subdiagonal. Its column sums of moduli are $1 + |a_k/a_0|$ for $k < n$ and $|a_n/a_0|$, so $|\lambda| \le \|C\|_1 \le 1 + M$ gives item 3 again (non-strict). Its row sums give $\|C\|_\infty = \max(1, \sum_k|a_k/a_0|)$, Lagrange's bound. The [Gershgorin circle theorem](/gershgorin-circle-theorem/) gives similar discs.
- **Scaling.** Substituting $z = Rw$ maps all roots into the unit disc, which keeps the powers $w^k$ in range during evaluation.

## Tightness

- **Item 2 is attained.** For $a_0 > 0$ and $a_k \le 0$ the root $R$ lies on the circle, as shown above.
- **Item 3 is sharp in the limit.** For $p = z^n - M(z^{n-1} + \cdots + 1)$ with $M = 2$, $R$ is $2.7321$ for $n = 2$, $2.9917$ for $n = 5$ and $3.0000$ to four places for $n = 10$, approaching $1 + M = 3$. So no bound of the form $1 + cM$ with $c < 1$ holds for all degrees.
- **Clustered roots.** For $p = (z - 1)^n$ the Cauchy polynomial is $2x^n - (x + 1)^n$, so $R = 1/(2^{1/n} - 1) \approx n/\ln 2$, while every root has modulus 1. For $n = 10$: $R = 13.93$, $F = 20$ and $1 + M = 253$. The bounds grow with the degree because they cannot see the cancellation between the binomial coefficients.
- **Moduli only.** Any bound that depends only on $|a_k|$ is at least $R$, because $R$ is attained by a polynomial with those moduli. So $R$ is the best bound of this kind; to do better one must use the phases, for example through [Graeffe's method](/graeffe-method/) or a few steps of a root finder.
- **Roots near 0.** Item 2 gives no information about small roots; item 5 does, and fails only when $a_n = 0$, where $z = 0$ is a root.

## History

Cauchy proved the bound by the positive root of the associated polynomial in his Exercices de mathématiques of 1829, as part of his work on the existence and location of roots. The simpler form $1 + \max_k|a_k/a_0|$ follows at once and is often called Cauchy's bound. Many refinements followed: Lagrange's sum bound, Fujiwara's 1916 bound with $k$th roots, and bounds by Kojima, Montel and others collected in Marden's Geometry of Polynomials. In numerical work the bound is used to scale polynomials, to place starting points and, in Jenkins and Traub's 1970 algorithm, to choose the radius of the shifts.

## References
