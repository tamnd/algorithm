---
tag: E1FYMV
kind: definition
slug: regularization-method
name: Regularization method
aliases:
- regularization operator
- regularization strategy
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "A family of bounded operators R_alpha with a rule alpha(delta, y^delta) such that R_alpha y^delta tends to the minimum norm solution x^dagger as the noise level delta goes to 0."
model: real-ram
prereqs: [well-posed-problem, singular-value-expansion, pseudoinverse]
see_also: [spectral-filter-factors, truncated-svd, tikhonov-regularization, landweber-iteration, regularization-parameter-choice, qualification-of-regularization, semi-convergence, bakushinskii-veto]
sources:
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 3, Regularization Operators (the definition of a regularization and a parameter choice rule, order optimality)
  - paper: "A. N. Tikhonov, Solution of incorrectly formulated problems and the regularization method, Soviet Mathematics Doklady 4, 1963, 1035 to 1038"
    locator: the regularizing operator and the choice of its parameter from the error level (general locator)
  - book: "A. N. Tikhonov and V. Y. Arsenin, Solutions of Ill-Posed Problems, Winston, Washington, 1977"
    locator: the chapters on regularizing operators (general locator)
  - book: isbn:9780898714036
    title: Per Christian Hansen, Rank-Deficient and Discrete Ill-Posed Problems, Numerical Aspects of Linear Inversion, SIAM, 1998
    locator: Chapter 5 (direct regularization methods and their common description by filter factors)
---

A regularization method for a linear [inverse problem](/inverse-problem/) $y = A x + e$ is a family of bounded operators $R_\alpha$ together with a rule that picks the parameter $\alpha$ from the noise level $\delta$ and the data $y^\delta$, such that $R_{\alpha} y^\delta$ converges to the minimum norm solution $x^\dagger = A^\dagger y$ as $\delta \to 0$, uniformly over all data within $\delta$ of $y$. The family alone is not enough: the definition is about the pair of operators and rule. This page gives the definition and the basic test for it. The usual way to build the operators is by [spectral filter factors](/spectral-filter-factors/); [truncated SVD](/truncated-svd/) and [Tikhonov regularization](/tikhonov-regularization/) are instances; how fast the convergence is depends on a [source condition](/source-condition/) and on the [qualification](/qualification-of-regularization/) of the method.

## Definition

Let $A: X \to Y$ be a bounded linear operator between Hilbert spaces, and let $A^\dagger$ be its generalized inverse (see [pseudoinverse](/pseudoinverse/)). Assume $A^\dagger$ is unbounded, so that the problem is not [well posed](/well-posed-problem/). The data are $y^\delta$ with $\|y^\delta - y\| \le \delta$ for some $y \in D(A^\dagger)$.

**Regularization operators.** A family $\{R_\alpha\}_{\alpha > 0}$ of bounded linear operators $R_\alpha: Y \to X$ with $R_\alpha y \to A^\dagger y$ as $\alpha \to 0$ for every $y \in D(A^\dagger)$. The parameter $\alpha$ is the regularization parameter. For a method indexed by an integer $k$, such as an iteration count or a truncation index, read $\alpha = 1/k$.

**Parameter choice rule.** A map $\alpha = \alpha(\delta, y^\delta)$. It is called a priori if it uses only $\delta$, a posteriori if it uses $\delta$ and $y^\delta$, and heuristic if it uses only $y^\delta$.

**Regularization method.** The pair $(R_\alpha, \alpha)$ is a (convergent) regularization method for $A^\dagger$ if, for every $y \in D(A^\dagger)$,
$$\lim_{\delta \to 0}\ \sup\big\{\, \|R_{\alpha(\delta, y^\delta)}\, y^\delta - A^\dagger y\| \ :\ y^\delta \in Y,\ \|y^\delta - y\| \le \delta \,\big\} = 0$$
and
$$\lim_{\delta \to 0}\ \sup\big\{\, \alpha(\delta, y^\delta) \ :\ y^\delta \in Y,\ \|y^\delta - y\| \le \delta \,\big\} = 0.$$
The supremum makes the definition a worst-case statement over all noise of size at most $\delta$.

The aliases differ in use. "Regularization operator" often names one $R_\alpha$, and "regularization strategy" the pair of operators and rule; this page uses "regularization method" for the pair.

**A basic test for a priori rules.** Let $R_\alpha \to A^\dagger$ pointwise on $D(A^\dagger)$, and let $\alpha(\delta) \to 0$ with $\delta \|R_{\alpha(\delta)}\| \to 0$ as $\delta \to 0$. Then $(R_\alpha, \alpha(\delta))$ is a regularization method. The proof is one line:
$$\|R_\alpha y^\delta - A^\dagger y\| \le \|R_\alpha (y^\delta - y)\| + \|R_\alpha y - A^\dagger y\| \le \delta \|R_\alpha\| + \|R_\alpha y - A^\dagger y\|.$$
The first term is the propagated noise and the second the approximation error (the bias). Both tend to zero, and the bound does not depend on which $y^\delta$ was chosen. The parameter must go to zero, but slowly enough that the noise term goes to zero too.

**Order optimality.** On the set of $x^\dagger = (A^* A)^\nu w$ with $\|w\| \le \rho$, no method can have a worst-case error better than order $\delta^{2\nu/(2\nu+1)} \rho^{1/(2\nu+1)}$. A method that attains this order is called order optimal for that $\nu$.

## Examples and non-examples

**Truncated SVD with an a priori rule.** $R_k y = \sum_{i \le k} \langle u_i, y \rangle v_i/\sigma_i$ has $\|R_k\| = 1/\sigma_k$, and $R_k y \to A^\dagger y$ as $k \to \infty$ by the [Picard condition](/picard-condition/). Any rule $k(\delta) \to \infty$ with $\delta/\sigma_{k(\delta)} \to 0$ gives a regularization method. For the integration operator, $\sigma_k \approx 1/(\pi k)$, so $k(\delta) = \lceil \delta^{-1/2} \rceil$ works.

**Tikhonov with $\alpha \to 0$ and $\delta^2/\alpha \to 0$.** $R_\alpha = (A^* A + \alpha I)^{-1} A^*$ has $\|R_\alpha\| \le 1/(2\sqrt{\alpha})$. Any $\alpha(\delta) \to 0$ with $\delta/\sqrt{\alpha(\delta)} \to 0$ passes the test, for example $\alpha = \delta$. ([Tikhonov regularization](/tikhonov-regularization/) writes the same parameter as $\lambda$.)

**Landweber iteration stopped in time.** After $k$ steps with step size $0 < \omega < 2/\|A\|^2$, $\|R_k\| \le \sqrt{\omega k}$. Any stopping index with $k(\delta) \to \infty$ and $\delta^2 k(\delta) \to 0$ works (see [Landweber iteration](/landweber-iteration/)).

**The discrepancy principle.** Choose the smallest $k$ (or the $\alpha$) with $\|A x - y^\delta\| \le \tau \delta$ for a fixed $\tau > 1$. This a posteriori rule makes TSVD, Tikhonov and Landweber regularization methods (see [Morozov discrepancy principle](/morozov-discrepancy-principle/)).

**A numerical picture.** Take the rectangle-rule matrix of the integration operator with $n = 24$, $x_j = \sin(\pi t_j)$ at the midpoints (so $\|x\| = 3.464$) and Gaussian noise (seed 15) scaled to $\|e\| = 10^{-2}$. The TSVD error is $3.464$ for $k = 0$, $0.245$ for $k = 3$, $0.108$ for $k = 6$, the smallest value $0.063$ for $k = 9$, and $0.416$ for $k = 24$, where TSVD is the plain inverse. The discrepancy principle with $\tau = 1.1$ picks $k = 6$. The matrix is invertible, so here the plain inverse is still finite; for the operator itself it is not.

**Non-example: $A^\dagger$ itself.** $A^\dagger$ is not bounded, so it is not a family of bounded operators, and $A^\dagger y^\delta$ may not exist (noisy data usually fail the Picard condition).

**Non-example: a fixed parameter.** With $\alpha$ fixed, $R_\alpha y^\delta \to R_\alpha y \ne A^\dagger y$ as $\delta \to 0$. The error does not go to zero, and the first limit of the definition fails.

**Non-example: a parameter that goes to zero too fast.** Tikhonov with $\alpha = \delta^4$. Take $y^\delta = y + \delta u_k$ with $\sigma_k$ near $\sqrt{\alpha} = \delta^2$. The noise term is $\delta \sigma_k/(\sigma_k^2 + \alpha) \approx \delta/(2\delta^2) = 1/(2\delta)$, which grows without bound.

**Non-example: a heuristic rule.** A rule $\alpha(y^\delta)$ that does not use $\delta$ cannot give a regularization method when $A^\dagger$ is unbounded ([Bakushinskii veto](/bakushinskii-veto/)). Rules such as GCV and the L-curve are still used, but their good behavior needs assumptions on the noise beyond $\|e\| \le \delta$.

## Related definitions

- [Spectral filter factors](/spectral-filter-factors/): the functions $f_\alpha(\sigma)$ that define $R_\alpha$ through the singular system, and the conditions on $f_\alpha$ that make $R_\alpha \to A^\dagger$.
- [Regularization parameter choice](/regularization-parameter-choice/): the a priori, a posteriori and heuristic rules in detail.
- [Source condition](/source-condition/) and [Tikhonov convergence rates](/tikhonov-convergence-rates/): the extra assumptions that turn convergence into a rate.
- [Qualification of regularization](/qualification-of-regularization/): the largest $\nu$ for which a method can be order optimal.
- [Semi-convergence](/semi-convergence/): the error of an iterative method first falls and then rises as $k$ grows, so the stopping index is the regularization parameter.

## References
