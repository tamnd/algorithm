---
tag: GZHC8D
kind: theorem
slug: tikhonov-convergence-rates
name: Convergence rates of Tikhonov regularization
aliases:
- order optimality of Tikhonov regularization
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: "If x = (A*A)^nu w with 0 < nu <= 1, Tikhonov with alpha ~ delta^(2/(2nu+1)) has the optimal error O(delta^(2nu/(2nu+1))). No choice of alpha beats delta^(2/3) unless x = 0."
prereqs: [tikhonov-regularization, source-condition, spectral-filter-factors]
see_also: [qualification-of-regularization, morozov-discrepancy-principle, truncated-svd, landweber-iteration, bakushinskii-veto, degree-of-ill-posedness, regularization-parameter-choice, ridge-regression]
sources:
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 4 (rates for filter methods with an a priori choice, the discrepancy principle) and Chapter 5, Tikhonov Regularization (the rate up to nu = 1, saturation at delta^(2/3), the rate delta^(1/2) with the discrepancy principle)
  - book: "C. W. Groetsch, The Theory of Tikhonov Regularization for Fredholm Equations of the First Kind, Pitman Research Notes in Mathematics 105, Pitman, Boston, 1984"
    locator: the chapter on convergence rates and the saturation result (general locator)
  - paper: "A. N. Tikhonov, Solution of incorrectly formulated problems and the regularization method, Soviet Mathematics Doklady 4, 1963, 1035 to 1038"
    locator: the method and the choice of its parameter from the error level (general locator)
  - book: isbn:9780898714036
    title: Per Christian Hansen, Rank-Deficient and Discrete Ill-Posed Problems, Numerical Aspects of Linear Inversion, SIAM, 1998
    locator: the chapters on Tikhonov regularization and on parameter choice (general locator)
---

This theorem gives the accuracy of [Tikhonov regularization](/tikhonov-regularization/) $x_\alpha^\delta = (A^* A + \alpha I)^{-1} A^* y^\delta$ as the noise level $\delta$ goes to 0. If the solution satisfies the [source condition](/source-condition/) $x^\dagger = (A^* A)^\nu w$ with $\|w\| \le \rho$ and $0 < \nu \le 1$, the a priori choice $\alpha = (\delta/\rho)^{2/(2\nu+1)}$ gives an error of at most $\frac32 \rho^{1/(2\nu+1)} \delta^{2\nu/(2\nu+1)}$. This is the best order that any method can reach on that set of solutions. For $\nu > 1$ there is no further gain: the best rate is $\delta^{2/3}$, and Groetsch (1984) proved that no parameter choice, a priori or not, gives an error $o(\delta^{2/3})$ for all noise unless $x^\dagger = 0$. This stop is the saturation of Tikhonov regularization, and $\nu_0 = 1$ is its [qualification](/qualification-of-regularization/) in this convention. (With the source condition written as $(A^* A)^{\mu/2} w$, the limit is $\mu = 2$.) The page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for the parameter $\alpha$.

## Statement

**Setting.** $A: X \to Y$ is a bounded linear operator between Hilbert spaces, $x^\dagger = A^\dagger y$ is the minimum norm solution of $A x = y$, and $y^\delta$ are data with $\|y^\delta - y\| \le \delta$. For $\alpha > 0$, $x_\alpha^\delta = (A^* A + \alpha I)^{-1} A^* y^\delta$ and $x_\alpha = (A^* A + \alpha I)^{-1} A^* y$.

1. **Error split.** For every $\alpha > 0$, $\|x_\alpha^\delta - x_\alpha\| \le \delta / (2\sqrt\alpha)$, and $\|x_\alpha - x^\dagger\| \to 0$ as $\alpha \to 0$. So any choice with $\alpha \to 0$ and $\delta^2/\alpha \to 0$ gives $x_\alpha^\delta \to x^\dagger$.
2. **Rate.** If $x^\dagger = (A^* A)^\nu w$ with $\|w\| \le \rho$ and $0 < \nu \le 1$, then
$$\|x_\alpha^\delta - x^\dagger\| \le \alpha^\nu \rho + \frac{\delta}{2\sqrt\alpha},$$
and with $\alpha = (\delta/\rho)^{2/(2\nu+1)}$,
$$\|x_\alpha^\delta - x^\dagger\| \le \tfrac32\, \rho^{1/(2\nu+1)}\, \delta^{2\nu/(2\nu+1)} .$$
This order is optimal on the source set: no method has a better order of worst-case error there.
3. **Saturation (Groetsch).** Let $A$ be compact with infinitely many nonzero singular values. Let $\alpha = \alpha(\delta, y^\delta)$ be any parameter choice, and let
$$e(\delta) = \sup \{ \|x_{\alpha(\delta, y^\delta)}^\delta - x^\dagger\| : \|y^\delta - y\| \le \delta \}.$$
If $e(\delta) = o(\delta^{2/3})$ as $\delta \to 0$, then $x^\dagger = 0$.

## In plain words

Tikhonov regularization makes two errors. It damps the solution on purpose, which costs accuracy, more for larger $\alpha$. It also passes on part of the noise, more for smaller $\alpha$. If the true solution is smooth in the sense of the source condition, the first error is small, and one can take a small $\alpha$. The best balance gives an error that falls like a power of the noise level, and a smoother solution gives a larger power.

There is a ceiling. The damping of Tikhonov is too gentle on the large singular values: it changes even well-measured components by a relative amount of about $\alpha$. So past a smoothness of $\nu = 1$, a smoother solution no longer helps, and the error cannot fall faster than $\delta^{2/3}$, whatever $\alpha$ one picks.

## Proof

Let $(\sigma_j; v_j, u_j)$ be the singular system and $L = \|A\|^2$. All operators below are functions of $A^* A$, so their norms are suprema over the spectrum in $[0, L]$.

**Part 1.** $x_\alpha^\delta - x_\alpha = (A^* A + \alpha I)^{-1} A^* (y^\delta - y)$, whose norm is at most $\sup_\sigma \sigma/(\sigma^2 + \alpha) \cdot \delta$. Since $\sigma^2 + \alpha \ge 2\sigma\sqrt\alpha$, this is at most $\delta/(2\sqrt\alpha)$. For the other term, $x_\alpha - x^\dagger = -\alpha (A^* A + \alpha I)^{-1} x^\dagger$, so
$$\|x_\alpha - x^\dagger\|^2 = \sum_j \left(\frac{\alpha}{\sigma_j^2 + \alpha}\right)^2 |\langle v_j, x^\dagger\rangle|^2 ,$$
using that $x^\dagger$ is orthogonal to the null space of $A$ (in the compact case; in general the same holds with the spectral measure of $A^* A$). Each term is at most $|\langle v_j, x^\dagger\rangle|^2$ and tends to 0 as $\alpha \to 0$, so the sum tends to 0 by dominated convergence. If $\alpha \to 0$ and $\delta/\sqrt\alpha \to 0$, both terms tend to 0.

**Part 2.** Now $x_\alpha - x^\dagger = -\alpha (A^* A + \alpha I)^{-1} (A^* A)^\nu w$, so $\|x_\alpha - x^\dagger\| \le \sup_{\lambda \ge 0} \frac{\alpha \lambda^\nu}{\lambda + \alpha}\, \rho$. For $0 < \nu \le 1$, Young's inequality gives $\lambda^\nu \alpha^{1-\nu} \le \nu\lambda + (1-\nu)\alpha \le \lambda + \alpha$, hence $\alpha\lambda^\nu/(\lambda + \alpha) \le \alpha^\nu$. With part 1, $\|x_\alpha^\delta - x^\dagger\| \le \alpha^\nu\rho + \delta/(2\sqrt\alpha)$. Put $\alpha = (\delta/\rho)^{2/(2\nu+1)}$. Then $\alpha^\nu\rho = \delta^{2\nu/(2\nu+1)}\rho^{1/(2\nu+1)}$ and $\delta/(2\sqrt\alpha) = \frac12 \delta \cdot (\rho/\delta)^{1/(2\nu+1)} = \frac12 \delta^{2\nu/(2\nu+1)}\rho^{1/(2\nu+1)}$. The sum is the stated bound. Optimality: the [source condition](/source-condition/) page proves that the worst-case error of the best method on $\{(A^*A)^\nu w : \|w\| \le \rho\}$ is of the order $\delta^{2\nu/(2\nu+1)}\rho^{1/(2\nu+1)}$ and no smaller (EHN Chapter 3).

**Part 3.** Suppose $x^\dagger \ne 0$ and $e(\delta) = o(\delta^{2/3})$. We find noisy data for which the error is too large.

*Step 1 (an identity).* From $(A^* A + \alpha I) x_\alpha^\delta = A^* y^\delta$ and $(A^* A + \alpha I) x^\dagger = A^* y + \alpha x^\dagger$,
$$(A^* A + \alpha I)(x_\alpha^\delta - x^\dagger) = A^*(y^\delta - y) - \alpha x^\dagger .$$

*Step 2 (the test data).* Let $c_n = \langle v_n, x^\dagger\rangle$ and $\delta_n = \sigma_n^3$, which tends to 0 because $\sigma_n \to 0$. Take $y_n = y - s_n \delta_n u_n$, with $s_n = 1$ if $c_n \ge 0$ and $s_n = -1$ otherwise, so $\|y_n - y\| = \delta_n$. Let $\alpha_n = \alpha(\delta_n, y_n)$ and $x_n = x_{\alpha_n}^{\delta_n}$ be the result for these data. Then $e(\delta_n) \ge \|x_n - x^\dagger\|$.

*Step 3 ($\alpha_n$ is small).* Let $P_n$ be the orthogonal projection onto the complement of $v_n$. It commutes with $A^* A$, and $P_n A^* u_n = \sigma_n P_n v_n = 0$, so $P_n A^*(y_n - y) = 0$. Apply $P_n$ to the identity of step 1: $\alpha_n P_n x^\dagger = -(A^* A + \alpha_n I) P_n (x_n - x^\dagger)$. Hence
$$\alpha_n \|P_n x^\dagger\| \le (L + \alpha_n)\, \|x_n - x^\dagger\| \le (L + \alpha_n)\, e(\delta_n).$$
Since $c_n \to 0$, $\|P_n x^\dagger\| \to \|x^\dagger\| > 0$, so $\|P_n x^\dagger\| \ge \|x^\dagger\|/2$ for large $n$. If $\alpha_n \ge 1$, the inequality gives $\|x^\dagger\|/2 \le (L + 1)\, e(\delta_n)$, which fails for large $n$ because $e(\delta_n) \to 0$. So for large $n$, $\alpha_n < 1$ and
$$\alpha_n \le \frac{2(L + 1)}{\|x^\dagger\|}\, e(\delta_n) = o(\delta_n^{2/3}) = o(\sigma_n^2).$$

*Step 4 (the error on $v_n$ is large).* The coefficient of $x_n - x^\dagger$ on $v_n$ is
$$\langle v_n, x_n - x^\dagger\rangle = \frac{\sigma_n(\sigma_n c_n - s_n \delta_n)}{\sigma_n^2 + \alpha_n} - c_n = -\frac{s_n \sigma_n \delta_n + \alpha_n c_n}{\sigma_n^2 + \alpha_n} .$$
By the choice of $s_n$, the two terms in the numerator have the same sign, so $|\langle v_n, x_n - x^\dagger\rangle| \ge \sigma_n\delta_n/(\sigma_n^2 + \alpha_n)$. By step 3, $\alpha_n \le \sigma_n^2$ for large $n$, so this is at least $\sigma_n \delta_n/(2\sigma_n^2) = \sigma_n^2/2 = \delta_n^{2/3}/2$.

So $e(\delta_n) \ge \delta_n^{2/3}/2$ for all large $n$, which contradicts $e(\delta) = o(\delta^{2/3})$. Hence $x^\dagger = 0$. $\square$

## Consequences

- **Qualification 1.** Parts 2 and 3 together say that the qualification of Tikhonov regularization is exactly 1 in the convention $x^\dagger = (A^*A)^\nu w$. Methods with a larger qualification, such as iterated Tikhonov of order $j$ (up to $\nu = j$), [truncated SVD](/truncated-svd/) and [Landweber iteration](/landweber-iteration/) (all $\nu$), do not saturate at $\delta^{2/3}$. See [qualification of regularization](/qualification-of-regularization/).
- **The a priori choice needs $\nu$ and $\rho$.** The optimal $\alpha$ depends on the smoothness, which is rarely known. A posteriori rules choose $\alpha$ from the data and $\delta$ instead.
- **Discrepancy principle.** With $\alpha$ chosen so that $\|A x_\alpha^\delta - y^\delta\| = \tau\delta$, $\tau > 1$, Tikhonov regularization converges, and it is order optimal for $0 < \nu \le 1/2$. Its rate is never better than $\delta^{1/2}$ unless $x^\dagger = 0$ (EHN Chapters 4 and 5). Modified rules, such as the one of Raus and Gfrerer, recover the optimal order up to $\nu = 1$ (EHN Chapters 4 and 5). See [Morozov discrepancy principle](/morozov-discrepancy-principle/).
- **Rules without $\delta$.** A rule $\alpha(y^\delta)$ that does not use $\delta$ cannot give convergence for all noise when $A^\dagger$ is unbounded, by the [Bakushinskii veto](/bakushinskii-veto/). So parts 1 and 2 need $\delta$ or extra assumptions on the noise.
- **Ridge regression.** The same estimator in statistics is [ridge regression](/ridge-regression/); there the noise is random, and the rates are stated for the expected error, but the bias and variance split is the same as in parts 1 and 2.

## Tightness

- **$\nu \le 1$ is needed.** Part 3 shows that no choice of $\alpha$ improves on $\delta^{2/3}$, so the condition $\nu \le 1$ in part 2 cannot be dropped. The [qualification](/qualification-of-regularization/) page shows this in a diagonal model with $\sigma_j = 1/j$: for coefficients $x_j^\dagger = j^{-3}$ and $j^{-5}$ (smoothness just below $\nu = 5/4$ and $\nu = 9/4$) the best Tikhonov error falls with slope $0.666$ and $0.667$ in $\log\delta$, while truncated SVD reaches $0.712$ and $0.811$.
- **The bias bound is sharp.** For $\nu \le 1$ the supremum of $\alpha\lambda^\nu/(\lambda + \alpha)$ over $\lambda \ge 0$ is attained at $\lambda = \nu\alpha/(1-\nu)$ for $\nu < 1$ and approached as $\lambda \to \infty$ for $\nu = 1$, with a value of the order $\alpha^\nu$. If the spectrum of $A^* A$ has points there, a $w$ concentrated on them gives a bias of the order $\alpha^\nu\rho$.
- **The noise bound is sharp.** If $\sigma_j = \sqrt\alpha$ for some $j$, noise $\delta u_j$ gives a data error of exactly $\delta/(2\sqrt\alpha)$.
- **The source condition is needed.** Without it the convergence in part 1 can be arbitrarily slow (see [source condition](/source-condition/)).
- **Compactness in part 3.** If $R(A)$ is closed, $A^\dagger$ is bounded and the error can be of the order $\delta$, so the condition that $A$ has infinitely many nonzero singular values cannot be dropped.

## History

A. N. Tikhonov introduced the method in 1963 and chose the parameter from the error level. Rates under range conditions of the form $x^\dagger = A^* z$ and $x^\dagger = A^* A w$ followed in the 1970s and early 1980s. C. W. Groetsch's monograph of 1984 collected the theory for Fredholm equations of the first kind and contains the saturation result that the rate $\delta^{2/3}$ cannot be improved. The monograph of Engl, Hanke and Neubauer (1996) states the result for general filter methods through the qualification, and proves the rate $\delta^{1/2}$ limit for the discrepancy principle. We could not confirm the first source of the general fractional rate $\delta^{2\nu/(2\nu+1)}$, so we do not name one.

## References
