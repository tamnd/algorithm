---
tag: 4GQPKN
kind: definition
slug: qualification-of-regularization
name: Qualification of a regularization method
aliases:
- saturation of regularization
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: "The largest smoothness order nu for which a filter method's bias falls like alpha^nu. With x = (A*A)^nu w it is 1 for Tikhonov (2 if mu = 2 nu) and infinite for TSVD and Landweber."
prereqs: [spectral-filter-factors, source-condition]
see_also: [tikhonov-convergence-rates, truncated-svd, landweber-iteration, tikhonov-regularization, morozov-discrepancy-principle, regularization-method, convergence-rate, cgls]
sources:
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 4, Continuous Regularization Methods (the definition of the qualification of a filter method, order optimality under a source condition, and Tikhonov regularization with its saturation and with the discrepancy principle); Chapter 6 for Landweber
  - book: "C. W. Groetsch, The Theory of Tikhonov Regularization for Fredholm Equations of the First Kind, Pitman Research Notes in Mathematics 105, Pitman, Boston, 1984"
    locator: the chapter on convergence rates (the rate delta^(2/3) cannot be improved unless the solution is zero) (general locator)
  - paper: "P. Mathé and S. V. Pereverzev, Geometry of linear ill-posed problems in variable Hilbert scales, Inverse Problems 19(3), 2003, 789 to 803"
    locator: the qualification of a method with respect to a general index function (general locator)
  - book: isbn:9780898714036
    title: Per Christian Hansen, Rank-Deficient and Discrete Ill-Posed Problems, Numerical Aspects of Linear Inversion, SIAM, 1998
    locator: Chapter 5 (filter factors of the direct methods) and Chapter 6 (iterative methods) (general locator)
---

The qualification of a linear regularization method measures how much smoothness of the solution the method can use. Under the [source condition](/source-condition/) $x^\dagger = (A^* A)^\nu w$, a method can reach the best possible error order $\delta^{2\nu/(2\nu+1)}$ only if its bias falls like $\alpha^\nu$, where $\alpha$ is the regularization parameter. The qualification $\nu_0$ is the largest $\nu$ for which this holds. Up to $\nu_0$ the method gets more accurate as the solution gets smoother. Above $\nu_0$ it stops gaining: its rate is stuck at the rate for $\nu_0$. This stop is called saturation. In the convention $x^\dagger = (A^* A)^\nu w$, used on this page and in Engl, Hanke and Neubauer (EHN), [Tikhonov regularization](/tikhonov-regularization/) has qualification 1, iterated Tikhonov of order $j$ has qualification $j$, and [truncated SVD](/truncated-svd/) and [Landweber iteration](/landweber-iteration/) have infinite qualification. Authors who write the source condition as $x^\dagger = (A^* A)^{\mu/2} w$, with $\mu = 2\nu$, get numbers twice as large, so Tikhonov has qualification 2 for them.

## Definition

**Setting.** $A: X \to Y$ is a bounded linear operator between Hilbert spaces with singular system $(\sigma_j; v_j, u_j)$, and $y^\delta$ are data with $\|y^\delta - A x^\dagger\| \le \delta$. A filter method (see [spectral filter factors](/spectral-filter-factors/)) computes
$$x_\alpha^\delta = g_\alpha(A^* A) A^* y^\delta = \sum_j g_\alpha(\sigma_j^2)\, \sigma_j \langle u_j, y^\delta \rangle v_j, \qquad \alpha > 0,$$
for functions $g_\alpha$ on $(0, \|A\|^2]$. The filter factor of the component $j$ is $f_\alpha(\sigma_j) = \sigma_j^2 g_\alpha(\sigma_j^2)$, and the residual function is
$$r_\alpha(\lambda) = 1 - \lambda g_\alpha(\lambda), \qquad 0 < \lambda \le \|A\|^2 .$$
The standing assumptions of EHN Chapter 4 are: $|r_\alpha(\lambda)| \le C_r$, $|g_\alpha(\lambda)| \le C_g / \alpha$, and $r_\alpha(\lambda) \to 0$ as $\alpha \to 0$ for every $\lambda > 0$. They make the method a [regularization method](/regularization-method/) with the right parameter choice.

**Definition.** The method has qualification at least $\nu > 0$ if there is a constant $c_\nu$ with
$$\sup_{0 < \lambda \le \|A\|^2} \lambda^\nu |r_\alpha(\lambda)| \le c_\nu\, \alpha^\nu \quad \text{for all } \alpha > 0 .$$
The qualification $\nu_0 \in (0, \infty]$ is the supremum of all such $\nu$ (EHN Chapter 4 calls it $\mu_0$ and asks for the bound for all $\nu$ up to $\nu_0$). If the bound holds for every $\nu > 0$, the qualification is infinite.

**The set of good $\nu$ is an interval.** If the bound holds for $\nu$ and $0 < \nu' < \nu$, then with $\theta = \nu'/\nu$,
$$\lambda^{\nu'} |r_\alpha(\lambda)| = \left(\lambda^\nu |r_\alpha(\lambda)|\right)^\theta |r_\alpha(\lambda)|^{1 - \theta} \le c_\nu^\theta C_r^{1 - \theta} \alpha^{\nu'} .$$
So "qualification $\nu_0$" means the bound holds for all $\nu < \nu_0$ and fails for all $\nu > \nu_0$.

**Why it matters (theorem).** The error splits into a bias and a data error. Under $x^\dagger = (A^* A)^\nu w$ with $\|w\| \le \rho$ and $\nu \le \nu_0$,
$$\|x_\alpha - x^\dagger\| = \|r_\alpha(A^* A)(A^* A)^\nu w\| \le c_\nu \alpha^\nu \rho, \qquad \|x_\alpha^\delta - x_\alpha\| \le \sup_\lambda \sqrt{\lambda}\,|g_\alpha(\lambda)|\, \delta \le \sqrt{(1 + C_r) C_g}\, \frac{\delta}{\sqrt\alpha},$$
because $\lambda g_\alpha(\lambda)^2 = |1 - r_\alpha(\lambda)|\, |g_\alpha(\lambda)| \le (1 + C_r) C_g / \alpha$. The choice $\alpha \sim (\delta/\rho)^{2/(2\nu+1)}$ balances the two terms and gives
$$\|x_\alpha^\delta - x^\dagger\| = O\!\left(\rho^{1/(2\nu+1)} \delta^{2\nu/(2\nu+1)}\right),$$
which is the best order any method can reach on this class (EHN Chapter 4). For $\nu > \nu_0$ the same argument only gives the order for $\nu_0$. For Tikhonov this is not a weakness of the proof: the [Tikhonov convergence rates](/tikhonov-convergence-rates/) page proves that no parameter choice beats $\delta^{2/3}$ unless $x^\dagger = 0$.

**Qualification of a method with a rule.** The definition is about the a priori choice above. An a posteriori rule can lower it. Tikhonov regularization with the [discrepancy principle](/morozov-discrepancy-principle/) is order optimal only for $\nu \le 1/2$, so its best rate is $\delta^{1/2}$ (EHN Chapter 4). Landweber with the discrepancy principle is order optimal for all $\nu > 0$ (EHN Chapter 6). [CGLS](/cgls/) is not a filter method in this sense, because its filter depends on the data, but with the discrepancy principle it is order optimal for all $\nu > 0$ (EHN Chapter 7).

## Examples and non-examples

Write $\lambda = \sigma^2$ and $L = \|A\|^2$.

**Tikhonov: qualification 1.** $x_\alpha^\delta = (A^* A + \alpha I)^{-1} A^* y^\delta$, so $g_\alpha(\lambda) = 1/(\lambda + \alpha)$ and $r_\alpha(\lambda) = \alpha/(\lambda + \alpha)$. (The page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for the parameter; here $\lambda$ is a squared singular value and $\alpha$ is the parameter.)

- For $0 < \nu \le 1$, Young's inequality gives $\lambda^\nu \alpha^{1 - \nu} \le \nu \lambda + (1 - \nu)\alpha \le \lambda + \alpha$. So $\lambda^\nu r_\alpha(\lambda) = \alpha^\nu \cdot \lambda^\nu \alpha^{1-\nu}/(\lambda + \alpha) \le \alpha^\nu$, with $c_\nu = 1$.
- For $\nu > 1$ and $\alpha \le L$, take $\lambda = L$: $L^\nu \alpha/(L + \alpha) \ge L^{\nu - 1} \alpha / 2$. The ratio to $\alpha^\nu$ is at least $L^{\nu-1}\alpha^{1-\nu}/2$, which tends to infinity as $\alpha \to 0$. So the bound fails, and the bias is of order $\alpha$, not $\alpha^\nu$.

**Iterated Tikhonov of order $j$: qualification $j$.** Apply Tikhonov $j$ times, each time to the residual of the previous step. Then $r_\alpha(\lambda) = (\alpha/(\lambda + \alpha))^j$, and the same two arguments, applied to each factor, give qualification exactly $j$.

**Truncated SVD: infinite.** $f_\alpha(\sigma) = 1$ for $\sigma^2 \ge \alpha$ and $0$ otherwise, so $r_\alpha(\lambda) = 1$ for $\lambda < \alpha$ and $0$ otherwise. Then $\lambda^\nu r_\alpha(\lambda) \le \alpha^\nu$ for every $\nu$.

**Landweber: infinite.** With $\alpha = 1/k$ and a step $\omega$ with $0 < \omega \le 1/L$, $r_k(\lambda) = (1 - \omega\lambda)^k$. With $t = \omega\lambda \in (0, 1]$, $\lambda^\nu (1 - \omega\lambda)^k \le \omega^{-\nu} t^\nu e^{-k t} \le \omega^{-\nu} (\nu/(e k))^\nu$, the maximum being at $t = \nu/k$. So the bound holds for every $\nu$ with $c_\nu = (\nu/(e\omega))^\nu$. Showalter's method, with $r_\alpha(\lambda) = e^{-\lambda/\alpha}$, is infinite for the same reason.

**A measurement of saturation.** Take the diagonal model $\sigma_j = 1/j$, $j = 1, \dots, 1000$, and $x^\dagger_j = j^{-p}$. Then $x^\dagger = (A^* A)^\nu w$ with $\|w\|$ finite exactly when $\sum_j j^{4\nu - 2p} < \infty$, that is, for $\nu < (2p - 1)/4$ (in the infinite model). For each $\delta$ let $E(\delta)$ be the smallest value, over the parameter, of bias plus $\delta \|R_\alpha\|$. For a linear method this is within a factor $\sqrt 2$ of the worst-case error over all noise with norm $\delta$. The table gives the observed slope of $\log E$ against $\log\delta$ between $\delta = 10^{-5}$ and $10^{-7}$, and the predicted order $2\nu/(2\nu + 1)$ with $\nu = \min((2p-1)/4, \nu_0)$.

| $p$ | smoothness $\nu$ | Tikhonov, predicted | Tikhonov, observed | TSVD, predicted | TSVD, observed |
|---|---|---|---|---|---|
| 2 | $< 3/4$ | $0.600$ | $0.607$ | $0.600$ | $0.610$ |
| 3 | $< 5/4$ | $0.667$ (saturated) | $0.666$ | $0.714$ | $0.712$ |
| 5 | $< 9/4$ | $0.667$ (saturated) | $0.667$ | $0.818$ | $0.811$ |

For $p = 5$ the errors are $1.19 \cdot 10^{-2}$, $5.54 \cdot 10^{-4}$ and $2.57 \cdot 10^{-5}$ for Tikhonov and $4.04 \cdot 10^{-3}$, $1.01 \cdot 10^{-4}$ and $2.42 \cdot 10^{-6}$ for TSVD at $\delta = 10^{-3}, 10^{-5}, 10^{-7}$. The smooth solution lets TSVD gain a factor of about $40$ per two decades of $\delta$, but Tikhonov gains only a factor of about $21$, the same as for $p = 3$. The cause is visible in the bias alone: for $p = 5$ the Tikhonov bias divided by $\alpha$ is $0.998$, $1.009$ and $1.009$ at $\alpha = 10^{-2}, 10^{-4}, 10^{-6}$, so the bias falls like $\alpha$, not like a higher power.

**Non-example: a rate is not a qualification.** A method can reach a good rate for one particular $x^\dagger$ and one noise vector, for example by luck in the noise. The qualification is about the bound for the whole class $\{(A^*A)^\nu w : \|w\| \le \rho\}$ and all noise with norm at most $\delta$.

## Related definitions

- [Source condition](/source-condition/): the smoothness classes $x^\dagger = (A^* A)^\nu w$ that the qualification is measured against. General index functions $\varphi(A^* A) w$ lead to a qualification with respect to $\varphi$ (Mathé and Pereverzev 2003).
- [Spectral filter factors](/spectral-filter-factors/): $r_\alpha(\sigma^2) = 1 - f_\alpha(\sigma)$ is one minus the filter factor, so the qualification is a property of how fast the filter factors approach 1 for large $\sigma$.
- [Tikhonov convergence rates](/tikhonov-convergence-rates/): the rate $\delta^{2\nu/(2\nu+1)}$ for $\nu \le 1$, and the saturation theorem that makes qualification 1 sharp.
- [Convergence rate](/convergence-rate/): the general notion; here the rate is in the noise level $\delta$, not in an iteration count.
- [Regularization method](/regularization-method/): convergence without a rate, which needs no source condition and no qualification.

## References
