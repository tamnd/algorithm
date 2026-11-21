---
tag: 33TH4D
kind: concept
slug: spectral-filter-factors
name: Spectral filter factors
aliases:
- regularizing filter
- filter function
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "Weights f(sigma_i) that a linear regularization method puts on each singular component: x = sum f(sigma_i) (<u_i, y> / sigma_i) v_i. TSVD, Tikhonov and Landweber differ only in f."
model: real-ram
prereqs: [singular-value-expansion, regularization-method]
see_also: [truncated-svd, tikhonov-regularization, landweber-iteration, qualification-of-regularization, resolution-matrix, cgls, semi-convergence, generalized-cross-validation]
sources:
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 4, Continuous Regularization Methods (regularization by filter functions g_alpha, qualification), and Chapter 6, Iterative Regularization Methods
  - book: isbn:9780898714036
    title: Per Christian Hansen, Rank-Deficient and Discrete Ill-Posed Problems, Numerical Aspects of Linear Inversion, SIAM, 1998
    locator: Chapter 4 (filter factors) and Chapter 5 (the filter factors of the direct methods)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 4, Regularization Methods, and Chapter 6, Iterative Regularization
---

Spectral filter factors are the numbers $f_i$ by which a linear regularization method multiplies each term of the singular expansion of the naive solution: $x_{\mathrm{filt}} = \sum_i f_i\, \frac{\langle u_i, y \rangle}{\sigma_i}\, v_i$. A factor near 1 keeps a component, a factor near 0 removes it. When $f_i = f_\alpha(\sigma_i)$ for a function $f_\alpha$, the [truncated SVD](/truncated-svd/), Tikhonov regularization, Landweber iteration and many other methods differ only in this function, so one analysis covers them all. A [regularization method](/regularization-method/) is the general notion (operators plus a parameter rule); filter factors are the standard way to build its operators, and the [qualification](/qualification-of-regularization/) of a method is a property of its filter.

## In plain words

Solving a smoothing inverse problem means dividing each component of the data by a gain, and the small gains blow up the noise. A filter decides, component by component, how much of the division to keep. The truncated method keeps the first few components fully and throws away the rest. Tikhonov's method fades them out smoothly. An iterative method lets more components in with each step. Seen this way, the methods are different dimmer switches on the same set of channels. One knob, the regularization parameter, sets where the dimming starts. Too far one way and the noise comes through; too far the other way and real detail is lost.

## The idea

**The form.** Let $(\sigma_i; v_i, u_i)$ be the singular system of the forward operator $A$ (the [singular value expansion](/singular-value-expansion/), or the SVD $A = \sum_i \sigma_i u_i v_i^T$ of a matrix). The minimum norm solution is $x^\dagger = \sum_i \langle u_i, y \rangle v_i/\sigma_i$. A spectral (filter) method replaces it by
$$x_\alpha = R_\alpha y = \sum_i f_\alpha(\sigma_i)\, \frac{\langle u_i, y \rangle}{\sigma_i}\, v_i.$$
Engl, Hanke and Neubauer write the same method as $x_\alpha = g_\alpha(A^* A) A^* y$; the two forms are related by $f_\alpha(\sigma) = \sigma^2 g_\alpha(\sigma^2)$.

**The common filters.**

| method | $f_\alpha(\sigma)$ | parameter |
|---|---|---|
| truncated SVD | $1$ for $\sigma_i$ with $i \le k$, else $0$ | $k$ |
| Tikhonov | $\sigma^2/(\sigma^2 + \alpha)$ | $\alpha$ |
| iterated Tikhonov, $j$ steps | $1 - (\alpha/(\sigma^2 + \alpha))^j$ | $\alpha$ |
| Landweber, $k$ steps | $1 - (1 - \omega \sigma^2)^k$ | $k$ |
| Showalter (asymptotic) | $1 - \exp(-t \sigma^2)$ | $t$ |

Tikhonov here minimizes $\|A x - y^\delta\|^2 + \alpha \|x\|^2$; the page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for this $\alpha$. Landweber is $x_{k+1} = x_k + \omega A^*(y - A x_k)$ with $x_0 = 0$ and $0 < \omega < 2/\|A\|^2$. Its filter follows from the sum $x_k = \omega \sum_{j < k} (I - \omega A^* A)^j A^* y$: on the component $i$ the sum is the geometric series $\omega \sigma_i \sum_{j<k} (1 - \omega \sigma_i^2)^j = (1 - (1 - \omega\sigma_i^2)^k)/\sigma_i$.

**When a filter regularizes.** Suppose that, for every $\sigma \in (0, \|A\|]$,

1. $f_\alpha(\sigma) \to 1$ as $\alpha \to 0$;
2. $|f_\alpha(\sigma)| \le C$ for a constant $C$ independent of $\alpha$ and $\sigma$;
3. $G(\alpha) = \sup_\sigma |f_\alpha(\sigma)|/\sigma < \infty$ for each $\alpha > 0$.

Then $R_\alpha$ is bounded with $\|R_\alpha\| = G(\alpha)$ (taken over the singular values), and $R_\alpha y \to A^\dagger y$ for every $y \in D(A^\dagger)$. Proof of the limit: with $c_i = \langle u_i, y \rangle/\sigma_i$,
$$\|R_\alpha y - A^\dagger y\|^2 = \sum_i (1 - f_\alpha(\sigma_i))^2 |c_i|^2.$$
Each term tends to zero by condition 1 and is at most $(1 + C)^2 |c_i|^2$ by condition 2, and $\sum_i |c_i|^2 < \infty$ by the [Picard condition](/picard-condition/). Dominated convergence gives the limit. With a parameter rule such that $\alpha(\delta) \to 0$ and $\delta\, G(\alpha(\delta)) \to 0$, the method is a regularization method.

**The noise bounds $G(\alpha)$.**

- TSVD: $G = 1/\sigma_k$.
- Tikhonov: $\sigma/(\sigma^2 + \alpha) \le 1/(2\sqrt{\alpha})$, since $\sigma^2 + \alpha \ge 2\sigma\sqrt{\alpha}$.
- Landweber with $0 < \omega \le 1/\|A\|^2$: $x = \omega \sigma^2 \in (0, 1]$, and $1 - (1 - x)^k \le \min(1, k x) \le \sqrt{k x}$, so $f/\sigma \le \sqrt{\omega k}$.

So $1/\sqrt{\alpha}$ for Tikhonov and $\sqrt{\omega k}$ for Landweber play the same role: Landweber after $k$ steps behaves roughly like Tikhonov with $\alpha \approx 1/(\omega k)$.

**Bias and qualification.** The approximation error on the component $i$ is $(1 - f_\alpha(\sigma_i)) c_i$. Under a [source condition](/source-condition/) $c_i = \sigma_i^{2\nu} w_i$, the bias is bounded by $\sup_\sigma \sigma^{2\nu} |1 - f_\alpha(\sigma)| \cdot \|w\|$. For Tikhonov, $\sigma^{2\nu} \alpha/(\sigma^2 + \alpha) \le \alpha^\nu$ only for $\nu \le 1$; for larger $\nu$ the bound stays of order $\alpha$. This saturation at $\nu = 1$ is the qualification of Tikhonov. TSVD and Landweber have no such limit; their qualification is infinite.

**Filters that depend on the data.** Conjugate gradient methods ([CGLS](/cgls/), LSQR) also give $x_k = \sum_i f_i^{(k)} \langle u_i, y \rangle v_i/\sigma_i$, but their factors depend on $y$ through the Ritz values of the Krylov space. So CGLS is not a linear method, and the theory above does not apply to it directly.

## Examples

**Check values.** Tikhonov with $\sigma = \alpha = 1$ gives $f = 1/2$. Landweber with $\omega\sigma^2 = 0.01$ after $100$ steps gives $f = 1 - 0.99^{100} = 0.63397$.

**Tikhonov against Landweber.** Tikhonov with $\alpha = 0.01$ and Landweber with $\omega = 1$ and $k = 100$ steps, so that $1/(\omega k) = \alpha$:

| $\sigma$ | Tikhonov $\sigma^2/(\sigma^2 + 0.01)$ | Landweber $1 - (1 - \sigma^2)^{100}$ |
|---|---|---|
| 1 | 0.990 | 1.000 |
| 0.1 | 0.500 | 0.634 |
| 0.01 | 0.00990 | 0.00995 |

Both pass the components with $\sigma \gg 0.1 = \sqrt{\alpha}$ and remove those with $\sigma \ll 0.1$. Landweber cuts off a little more sharply.

**A discretized operator.** For the rectangle-rule matrix of the integration operator with $n = 24$ (singular values $0.650$, $0.217$, $0.131$, and so on down to $0.0209$) and Tikhonov with $\alpha = 10^{-3}$, the first ten filter factors are $0.998$, $0.979$, $0.945$, $0.898$, $0.843$, $0.784$, $0.726$, $0.670$, $0.618$ and $0.570$. Their sum over all 24 components is $13.33$. This sum is the trace of the [resolution matrix](/resolution-matrix/), often read as the effective number of parameters that the data determine. For TSVD with $k = 6$ the same sum is exactly $6$.

## Where it is used

- To compare methods and to choose one: a sharp cutoff (TSVD) against a smooth one (Tikhonov), and direct methods against iterative ones.
- In parameter choice rules: [generalized cross-validation](/generalized-cross-validation/) and UPRE use $\sum_i f_i$ and $\sum_i (1 - f_i)^2 \langle u_i, y \rangle^2$, which are cheap once the SVD is known.
- In the [resolution matrix](/resolution-matrix/) $V \operatorname{diag}(f_i) V^T$ and in bias and variance estimates.
- In the analysis of iterative methods: SIRT and SART are Landweber iterations in weighted norms, so their filters have the Landweber form, and [semi-convergence](/semi-convergence/) is the growth of the filter on the noise components with $k$.
- In deconvolution, where the singular vectors are Fourier modes and a filter is a frequency response; the Wiener filter is a Tikhonov filter with a weight per frequency.

## References
