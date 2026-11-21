---
tag: C2NPR6
kind: concept
slug: semi-convergence
name: Semi-convergence
aliases:
- semiconvergence
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: The behavior of iterative methods on noisy ill-posed problems, where the error first falls and then grows as the iterates start to fit the noise.
prereqs: [regularization-method, spectral-filter-factors]
see_also: [landweber-iteration, cgls, lsqr, morozov-discrepancy-principle, kaczmarz-method, mlem-reconstruction, richardson-lucy-deconvolution, early-stopping]
sources:
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 6 (the split of the Landweber error into an approximation error and a data error, and the divergence of the iteration for noisy data) and Chapter 7 (the same for conjugate gradients)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 6 (iterative regularization methods and their semi-convergence)
  - book: isbn:9780898714937
    title: Frank Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001 (reprint of the Teubner and Wiley edition of 1986)
    locator: Chapter V (iterative reconstruction algorithms such as ART, and their behavior on noisy data)
  - paper: "L. Landweber, An iteration formula for Fredholm integral equations of the first kind, American Journal of Mathematics 73(3), 1951, 615 to 624"
    locator: the iteration whose noisy behavior is the standard example
---

Semi-convergence is the way the error of an iterative method behaves when the method is applied to an ill-posed problem $A x = y$ with noisy data $y^\delta$, $\|y^\delta - y\| \le \delta$. The error $\|x_k^\delta - x^\dagger\|$ to the minimum norm solution $x^\dagger$ first decreases, reaches a minimum, and then increases, often far above its starting value. The iteration "converges" only for a while. It is not a defect of one method: [Landweber iteration](/landweber-iteration/), [CGLS](/cgls/), [LSQR](/lsqr/), ART ([Kaczmarz method](/kaczmarz-method/)), [SIRT](/sirt/), [MLEM](/mlem-reconstruction/) and [Richardson-Lucy](/richardson-lucy-deconvolution/) all show it. The cause is the split of the error into an approximation error that falls with $k$ and a propagated data error that grows with $k$. So the iteration index is a regularization parameter, and an iterative method becomes a [regularization method](/regularization-method/) only together with a stopping rule, such as the [discrepancy principle](/morozov-discrepancy-principle/).

## In plain words

An iterative method improves its answer step by step. The first steps recover the large, smooth features of the answer, which the data determine well. Later steps try to recover fine details. For a blurred or smoothed measurement, those details are weak in the data, and the method has to amplify them a lot to get them back. The noise is amplified in the same way. So at first each step removes more error than it adds, and later each step adds more noise than it removes error. The answer gets better and then worse. The best moment to stop is somewhere in the middle, and the data residual alone does not show where it is, because the residual keeps falling.

## The idea

**Setting.** $A: X \to Y$ is a bounded linear operator between Hilbert spaces with singular system $(\sigma_j; v_j, u_j)$, $A v_j = \sigma_j u_j$, $\sigma_j$ descending (a matrix with its SVD in the discrete setting). The noise is deterministic, $\|y^\delta - y\| \le \delta$ with $y = A x^\dagger$. Many iterative methods started at $x_0 = 0$ produce, for a fixed index $k$, a filtered expansion (see [spectral filter factors](/spectral-filter-factors/)):
$$x_k^\delta = \sum_j f_k(\sigma_j) \frac{\langle u_j, y^\delta\rangle}{\sigma_j} v_j.$$
For Landweber with step $\omega$, $0 < \omega < 2/\|A\|^2$, the filter is $f_k(\sigma) = 1 - (1 - \omega\sigma^2)^k$. Let $x_k$ be the iterate for the exact data $y$.

**The split.** The triangle inequality gives
$$\|x_k^\delta - x^\dagger\| \le \underbrace{\|x_k - x^\dagger\|}_{\text{approximation error}} + \underbrace{\|x_k^\delta - x_k\|}_{\text{data error}}.$$
For Landweber both parts have a closed form:
$$\|x_k - x^\dagger\|^2 = \sum_j (1 - \omega\sigma_j^2)^{2k} |\langle v_j, x^\dagger\rangle|^2, \qquad x_k^\delta - x_k = \sum_j f_k(\sigma_j) \frac{\langle u_j, y^\delta - y\rangle}{\sigma_j} v_j.$$

- **The approximation error falls (theorem).** It decreases monotonically in $k$ and tends to $0$ for every $x^\dagger$, because $|1 - \omega\sigma_j^2| < 1$ for each $j$ (EHN Chapter 6). How fast it falls depends on the smoothness of $x^\dagger$: under the [source condition](/source-condition/) $x^\dagger = (A^* A)^\nu w$, $\|w\| \le \rho$, and with $\omega\|A\|^2 \le 1$, it is at most $(\nu/(\omega k))^\nu \rho$.
- **The data error grows (theorem).** With $\omega\|A\|^2 \le 1$, $\|x_k^\delta - x_k\| \le \sqrt{\omega k}\,\delta$. The worst case over all noise with $\|y^\delta - y\| \le \delta$ is $\delta \max_j f_k(\sigma_j)/\sigma_j$. If the range of $A$ is not closed (a compact $A$ with infinitely many nonzero singular values), the singular values tend to $0$, and this worst case tends to infinity as $k \to \infty$. For data $y^\delta$ that are not in the domain of $A^\dagger$ (the [Picard condition](/picard-condition/) fails, which is the usual case for noisy data), $\|x_k^\delta\| \to \infty$ (EHN Chapter 6).

The sum of a falling and a rising term has a minimum, and the bound $(\nu/(\omega k))^\nu\rho + \sqrt{\omega k}\,\delta$ is smallest for $\omega k \sim (\rho/\delta)^{2/(2\nu+1)}$, where it is of the order $\rho^{1/(2\nu+1)}\delta^{2\nu/(2\nu+1)}$. So the best index grows as $\delta$ falls, and the best error goes to $0$ with $\delta$. This is the sense in which an iteration with a good stopping index is a convergent regularization method.

**What is proved and what is not.** The split and the two bounds above are theorems. The name "semi-convergence" describes the typical shape of the true error curve, and that shape is not a theorem: the error need not have a single minimum, and for some noise it can even decrease all the way (see the second example). For a matrix, the limit $k \to \infty$ is the least squares solution $A^\dagger y^\delta$, whose error $\|A^\dagger (y^\delta - y)\|$ is finite but can be as large as $\delta/\sigma_r$, where $\sigma_r$ is the smallest nonzero singular value. For [CGLS](/cgls/) and [LSQR](/lsqr/) the filter $f_k$ depends on $y^\delta$, so the split above does not hold in the same simple form, but the same two effects are proved in EHN Chapter 7 and in Hanke (1995).

**The residual does not show it.** For Landweber, CGLS and LSQR the residual $\|y^\delta - A x_k^\delta\|$ decreases at every step (a theorem for each of them). The error has turned around long before the residual stops falling. A stopping rule must use extra information: the noise level $\delta$ (the discrepancy principle, the [Lepskii principle](/lepskii-balancing-principle/)) or a heuristic assumption about the noise (the [quasi-optimality criterion](/quasi-optimality-criterion/), the [L-curve](/l-curve-method/), [GCV](/generalized-cross-validation/)). By the [Bakushinskii veto](/bakushinskii-veto/), a rule that uses only $y^\delta$ cannot work in the worst case.

## Examples

**Two components, by hand.** Take $A = \mathrm{diag}(1, 0.1)$, $x^\dagger = (1, 0)$, so $y = (1, 0)$, and the noise $e = (0, 0.01)$, so $y^\delta = (1, 0.01)$ and $\delta = 0.01$. Run Landweber with $\omega = 0.5$. The first component is pure signal and the second is pure noise. The iterate is $x_k^\delta = (1 - 0.5^k,\ 0.1\,(1 - 0.995^k))$, because $1 - \omega\sigma^2$ is $0.5$ for $\sigma = 1$ and $0.995$ for $\sigma = 0.1$, and the noise $0.01$ is divided by $\sigma = 0.1$. So the approximation error is $0.5^k$ and the data error is $0.1(1 - 0.995^k)$.

| $k$ | $x_k^\delta$ | approximation error | data error | $\|x_k^\delta - x^\dagger\|$ | $\|y^\delta - A x_k^\delta\|$ |
|---|---|---|---|---|---|
| 0 | $(0, 0)$ | 1 | 0 | 1 | 1.00005 |
| 2 | $(0.75, 0.00100)$ | 0.25 | 0.00100 | 0.25000 | 0.25020 |
| 6 | $(0.98438, 0.00296)$ | 0.01563 | 0.00296 | 0.01590 | 0.01839 |
| 9 | $(0.99805, 0.00441)$ | 0.00195 | 0.00441 | 0.00482 | 0.00976 |
| 20 | $(1.00000, 0.00954)$ | 0.00000 | 0.00954 | 0.00954 | 0.00905 |
| 100 | $(1.00000, 0.03942)$ | 0.00000 | 0.03942 | 0.03942 | 0.00606 |
| 1000 | $(1.00000, 0.09933)$ | 0.00000 | 0.09933 | 0.09933 | 0.00007 |
| $\infty$ | $(1, 0.1)$ | 0 | 0.1 | 0.1 | 0 |

The error is smallest at $k = 9$, where it is $0.00482$, and then grows by a factor of $20$ to its limit $0.1 = \delta/\sigma_2$. The residual falls at every step. The discrepancy principle with $\tau = 1.5$ stops at the first $k$ with residual at most $0.015$, which is $k = 7$ (residual $0.01242$), with error $0.00854$, within a factor of $2$ of the best.

**No turn-around.** In the same problem, put the signal and the noise on the same component: $x^\dagger = (0, 1)$ and $e = (0, -0.01)$, so $y^\delta = (0, 0.09)$. Then $x_k^\delta = (0, 0.9(1 - 0.995^k))$ and the error $0.1 + 0.9 \cdot 0.995^k$ decreases at every step to $0.1$. There is no minimum at a finite $k$. Semi-convergence needs components where the noise dominates the signal; these are the components with small $\sigma_j$ in a typical ill-posed problem, but not in every example.

**An integral operator (a measurement).** For $(A x)(s) = \int_0^s x(t)\,dt$ on $L^2(0, 1)$, $\sigma_j = 2/((2j - 1)\pi)$, and $x^\dagger(t) = 1 - t$ has the coefficients $\langle v_j, x^\dagger\rangle = \sqrt2/((j - \frac12)\pi)^2$. With the first 200 components, Gaussian noise drawn with `random.Random(3)` and scaled to norm $\delta$, and Landweber with $\omega = 1/\sigma_1^2$:

| $\delta$ | $k$ | error | approximation error | data error |
|---|---|---|---|---|
| $10^{-2}$ | 1 | 0.0623 | 0.0626 | 0.0006 |
| $10^{-2}$ | 39 (best) | 0.0142 | | |
| $10^{-2}$ | 1000 | 0.1335 | 0.0009 | 0.1332 |
| $10^{-2}$ | 100000 | 2.4045 | 0.0000 | 2.4045 |
| $10^{-3}$ | 157 (best) | 0.0044 | | |
| $10^{-3}$ | 1000 | 0.0137 | 0.0009 | 0.0133 |
| $10^{-3}$ | 100000 | 0.2405 | 0.0000 | 0.2404 |

The approximation error does not depend on $\delta$. The data error at a fixed $k$ is ten times smaller for the ten times smaller $\delta$. So the best index moves from $39$ to $157$. At $k = 100000$ the error is four times the norm $\|x^\dagger\| = 0.577$ for $\delta = 10^{-2}$: running too long is worse than not starting. The discrepancy principle with $\tau = 1.5$ stopped at $k = 3$ (error $0.050$) and $k = 32$ (error $0.0117$). It stops early, as is typical, and its error is within a factor of about $3.5$ of the best here.

## Where it is used

- **Iterative regularization.** Landweber, CGLS, LSQR, the $\nu$-methods and nonlinear Landweber are regularization methods only because of semi-convergence and a stopping rule; the theory is in EHN Chapters 6, 7 and 11. The [iteratively regularized Gauss-Newton method](/iteratively-regularized-gauss-newton/) also needs a stopping index.
- **Tomography.** ART, SIRT and SART on noisy projection data improve the image for a number of sweeps and then fill it with streaks and noise. Natterer (1986, Chapter V) treats ART and its relaxation parameter. The number of sweeps and the relaxation parameter are chosen to stop near the minimum.
- **Emission tomography and deconvolution.** [MLEM](/mlem-reconstruction/), [OSEM](/osem/) and [Richardson-Lucy](/richardson-lucy-deconvolution/) increase the likelihood at every step but produce noisy, "checkerboard" images after many steps. Practitioners stop early or add a penalty; stopping rules without a known noise level are heuristics.
- **Hybrid methods.** [Hybrid Krylov regularization](/hybrid-krylov-regularization/) adds a Tikhonov penalty inside the Krylov method, so that the error curve flattens after its minimum and the exact stopping index matters much less.
- **Machine learning.** [Early stopping](/early-stopping/) of gradient descent on a least squares loss is the same effect: the step count acts like the parameter of ridge regression.

## References
