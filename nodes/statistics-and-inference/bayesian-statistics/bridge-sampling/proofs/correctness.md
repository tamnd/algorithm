---
title: The bridge identity, the optimal bridge, and the convergence of the iteration
proves: [correctness, convergence]
status: full
---

**Setting.** For $k = 1, 2$ let $p_k = q_k/c_k$ be a probability density on $\Omega_k \subseteq \mathbb{R}^d$ (with respect to a common measure), where $q_k \ge 0$ can be evaluated and $c_k = \int q_k > 0$ is unknown. The target is $r = c_1/c_2$. A bridge function is a measurable $\alpha \ge 0$ with

$$0 < \int_{\Omega_1 \cap \Omega_2} \alpha\, q_1 q_2 < \infty. \tag{1}$$

$\mathbb{E}_k$ is the expectation under $p_k$. The draws are $\theta_1, \ldots, \theta_{n_1} \sim p_1$ and $\phi_1, \ldots, \phi_{n_2} \sim p_2$. Write $n = n_1 + n_2$, $s_k = n_k/n$, and $l = q_1/q_2$, with $l_{1i} = l(\theta_i)$ and $l_{2j} = l(\phi_j)$.

## Claim 1: the bridge identity

For every bridge function $\alpha$, $\;r = \mathbb{E}_2[q_1 \alpha]/\mathbb{E}_1[q_2 \alpha]$.

*Proof.* $\mathbb{E}_2[q_1\alpha] = \int q_1 \alpha\, q_2/c_2$ and $\mathbb{E}_1[q_2\alpha] = \int q_2 \alpha\, q_1/c_1$. Both integrands are $\alpha q_1 q_2$, which vanishes outside $\Omega_1 \cap \Omega_2$, so the two integrals are $J/c_2$ and $J/c_1$ with $J = \int \alpha q_1 q_2 \in (0, \infty)$ by (1). Their ratio is $c_1/c_2$. $\blacksquare$

**Consistency of a fixed bridge.** If the draws within each sample are independent (or form ergodic Markov chains) then, by the [law of large numbers](/law-of-large-numbers/), $\frac{1}{n_2}\sum_j q_1(\phi_j)\alpha(\phi_j) \to \mathbb{E}_2[q_1\alpha]$ and $\frac{1}{n_1}\sum_i q_2(\theta_i)\alpha(\theta_i) \to \mathbb{E}_1[q_2\alpha] > 0$ almost surely, because both expectations are finite by (1). So $\hat r_\alpha \to r$ almost surely.

## Claim 2: importance sampling and the harmonic mean are bridges

(a) If $\Omega_1 \subseteq \Omega_2$ and $\alpha = 1/q_2$ on $\Omega_2$, then $\mathbb{E}_1[q_2\alpha] = 1$ and the identity reads $r = \mathbb{E}_2[q_1/q_2]$: [importance sampling](/importance-sampling/) of $q_1$ with proposal $p_2$. Condition (1) holds: $\int \alpha q_1 q_2 = c_1$.

(b) If $\Omega_2 \subseteq \Omega_1$ and $\alpha = 1/q_1$ on $\Omega_1$, then $\mathbb{E}_2[q_1\alpha] = 1$ and $\mathbb{E}_1[q_2\alpha] = \mathbb{E}_1[q_2/q_1]$, so $r = 1/\mathbb{E}_1[q_2/q_1]$: reciprocal importance sampling, the estimator of Gelfand and Dey when $q_2$ is a normalized density. Condition (1) holds: $\int \alpha q_1 q_2 = \int_{\Omega_2} q_2 = c_2$. With $q_1 = f(x \mid \theta)\pi(\theta)$ and $q_2 = \pi$, a normalized prior ($c_2 = 1$), this is $Z = 1/\mathbb{E}_{\mathrm{post}}[1/f(x \mid \theta)]$, the harmonic mean identity. The identity is exact, but the variance of the estimate is finite only if $\mathbb{E}_1[(q_2/q_1)^2] < \infty$, which needs $q_2$ to have lighter tails than $p_1$; the prior usually has heavier tails than the posterior. $\blacksquare$

## Claim 3: the optimal bridge under the first-order approximation

**The approximation.** Assume that all $n$ draws are independent, that $\int p_1 p_2 \alpha^2 (p_1 + p_2) < \infty$, and measure the error by the relative mean squared error $\mathrm{RE}^2(\hat r_\alpha) = \mathbb{E}(\hat r_\alpha - r)^2/r^2$. Write $\hat r_\alpha = A/B$ with $A = \frac{1}{n_2}\sum_j q_1(\phi_j)\alpha(\phi_j)$ and $B = \frac{1}{n_1}\sum_i q_2(\theta_i)\alpha(\theta_i)$, and $\mu = \int p_1 p_2 \alpha$. Then $\mathbb{E}A = c_1\mu$, $\mathbb{E}B = c_2\mu$, and $A$ and $B$ are independent with

$$\frac{\mathrm{Var}(A)}{(\mathbb{E}A)^2} = \frac{1}{n_2}\Big(\frac{\int p_1^2 p_2 \alpha^2}{\mu^2} - 1\Big), \qquad \frac{\mathrm{Var}(B)}{(\mathbb{E}B)^2} = \frac{1}{n_1}\Big(\frac{\int p_1 p_2^2 \alpha^2}{\mu^2} - 1\Big).$$

The first-order [delta method](/delta-method/) for the ratio $A/B$ of independent averages gives $\mathrm{RE}^2 \approx \mathrm{Var}(A)/(\mathbb{E}A)^2 + \mathrm{Var}(B)/(\mathbb{E}B)^2$. With $\frac{p_1}{n_2} + \frac{p_2}{n_1} = \frac{s_1 p_1 + s_2 p_2}{n s_1 s_2}$ and $\frac1{n_1} + \frac1{n_2} = \frac{1}{n s_1 s_2}$ this is

$$\mathrm{RE}^2(\hat r_\alpha) \approx \frac{1}{n s_1 s_2}\left(\frac{\int p_1 p_2 (s_1 p_1 + s_2 p_2)\, \alpha^2}{\big(\int p_1 p_2 \alpha\big)^2} - 1\right). \tag{2}$$

This is equation (3.2) of Meng and Wong (1996). It is an approximation, exact only to the first order in $1/n$. The claim below is about the right side of (2).

**Claim.** Over all bridge functions, the right side of (2) is minimized by $\alpha_{\mathrm{opt}} \propto 1/(s_1 p_1 + s_2 p_2)$ on $\{p_1 p_2 > 0\}$, and the minimum is

$$\frac{1}{n s_1 s_2}\left(\Big(\int \frac{p_1 p_2}{s_1 p_1 + s_2 p_2}\Big)^{-1} - 1\right).$$

*Proof.* Let $w = s_1 p_1 + s_2 p_2 > 0$ on $\{p_1 p_2 > 0\}$. By the Cauchy-Schwarz inequality,

$$\Big(\int p_1 p_2 \alpha\Big)^2 = \Big(\int \big(\alpha\sqrt{p_1 p_2 w}\big)\Big(\sqrt{p_1 p_2/w}\Big)\Big)^2 \le \int p_1 p_2 w\, \alpha^2 \cdot \int \frac{p_1 p_2}{w}.$$

So the ratio in (2) is at least $\big(\int p_1 p_2/w\big)^{-1}$. Equality in Cauchy-Schwarz holds exactly when the two factors are proportional, that is $\alpha\sqrt{p_1 p_2 w} = \kappa \sqrt{p_1 p_2/w}$, or $\alpha = \kappa/w$ where $p_1 p_2 > 0$. The value of $\alpha$ where $p_1 p_2 = 0$ does not enter (2). $\blacksquare$

Two consequences. First, $\int p_1 p_2/w \le \int p_2/s_1 = 1/s_1$ is always finite, and it is positive when the supports overlap, so the optimal bridge has a finite first-order error even when the importance sampling and harmonic mean bridges have infinite variance. Second, $\alpha_{\mathrm{opt}} \propto 1/(s_1 q_1/c_1 + s_2 q_2/c_2) \propto 1/(s_1 q_1 + s_2 r q_2)$ depends on the unknown $r$.

## Claim 4: the iteration has one fixed point, and it converges to it

Plug $\alpha = 1/(s_1 q_1 + s_2 \rho q_2)$, with a trial value $\rho$ in place of $r$, into $\hat r = A/B$. Divide the numerator and the denominator inside each sum by $q_2$:

$$T(\rho) = \frac{\frac{1}{n_2}\sum_j \frac{l_{2j}}{s_1 l_{2j} + s_2 \rho}}{\frac{1}{n_1}\sum_i \frac{1}{s_1 l_{1i} + s_2 \rho}} = \frac{N(\rho)}{D(\rho)}.$$

The algorithm iterates $\rho_{t+1} = T(\rho_t)$ (lines L5 to L9). Assume all $l_{1i}, l_{2j}$ are positive and finite, and let $l_- $ and $l_+$ be the smallest and the largest of them.

**(a) The fixed points are the roots of one increasing function.** Since $D(\rho) > 0$, $T(\rho) = \rho$ if and only if $\Psi(\rho) = 0$, where

$$\Psi(\rho) = \rho D(\rho) - N(\rho) = \frac{1}{n_1}\sum_i \frac{\rho}{s_1 l_{1i} + s_2\rho} - \frac{1}{n_2}\sum_j \frac{l_{2j}}{s_1 l_{2j} + s_2\rho}.$$

Each term $\rho/(s_1 l + s_2\rho)$ has derivative $s_1 l/(s_1 l + s_2\rho)^2 > 0$, and each term $l/(s_1 l + s_2\rho)$ has derivative $-s_2 l/(s_1 l + s_2 \rho)^2 < 0$. So $\Psi$ is strictly increasing on $(0, \infty)$, with limit $-1/s_1$ as $\rho \to 0$ and $1/s_2$ as $\rho \to \infty$. By the intermediate value theorem it has exactly one root $\hat r$, and $T$ has exactly one fixed point.

**(b) $T$ maps $(0, \infty)$ into a compact interval.** For $a \le b$ and $\rho > 0$, $(s_1 a + s_2\rho)/(s_1 b + s_2\rho) \ge a/b$. Every denominator $s_1 l + s_2\rho$ lies between $s_1 l_- + s_2\rho$ and $s_1 l_+ + s_2\rho$, so

$$T(\rho) \ge \frac{l_-/(s_1 l_+ + s_2\rho)}{1/(s_1 l_- + s_2\rho)} \ge l_-\frac{l_-}{l_+}, \qquad T(\rho) \le l_+ \frac{l_+}{l_-}.$$

So $T$ maps $(0, \infty)$ into $J = [l_-^2/l_+,\ l_+^2/l_-]$.

**(c) $T$ is a contraction in the log scale on $J$.** Let $u = \log \rho$ and $\tau(u) = \log T(e^u)$. Then

$$\tau'(u) = \frac{d\log N}{du} - \frac{d\log D}{du} = -\sum_j \omega_j \frac{s_2\rho}{s_1 l_{2j} + s_2\rho} + \sum_i \nu_i \frac{s_2\rho}{s_1 l_{1i} + s_2\rho},$$

where $\omega_j \propto l_{2j}/(s_1 l_{2j} + s_2\rho)$ and $\nu_i \propto 1/(s_1 l_{1i} + s_2\rho)$ are positive weights that sum to $1$. Each fraction $s_2\rho/(s_1 l + s_2\rho)$ lies in $(0, 1)$, so each weighted mean lies in $(0, 1)$, and $\tau'(u) \in (-1, 1)$. $\tau'$ is continuous, so on the compact interval $\log J$ it satisfies $\lvert \tau' \rvert \le \kappa$ for some $\kappa < 1$. By the mean value theorem, $\lvert \tau(u) - \tau(v) \rvert \le \kappa \lvert u - v \rvert$ for $u, v \in \log J$.

**(d) Convergence.** After one step $\rho_1 \in J$ by (b), and $\tau$ maps $\log J$ into itself. By the Banach fixed point theorem on the complete set $\log J$, $\log\rho_t \to \log\hat r$ with $\lvert \log\rho_t - \log\hat r \rvert \le \kappa^{t-1}\lvert \log\rho_1 - \log\hat r \rvert$. So the iteration converges geometrically from any start $\rho_0 > 0$, and the stopping test of line L9 is reached after $O(\log(1/\mathrm{tol}))$ steps. $\blacksquare$

Meng and Wong (1996, Theorem 2) state the convergence and uniqueness; the argument above is a self-contained proof of the same fact.

## Claim 5: the root is a consistent estimate of $r$

Let the two samples be independent and identically distributed within each sample, with $n_1, n_2 \to \infty$ and $s_1, s_2$ fixed, and let the supports overlap, $\int p_1 p_2 > 0$. For fixed $\rho$, the law of large numbers gives $\Psi_n(\rho) \to \psi(\rho)$ almost surely, where

$$\psi(\rho) = \mathbb{E}_1\Big[\frac{\rho}{s_1 l + s_2\rho}\Big] - \mathbb{E}_2\Big[\frac{l}{s_1 l + s_2\rho}\Big] = \Big(\frac{\rho}{c_1} - \frac{1}{c_2}\Big)\int \frac{q_1 q_2}{s_1 q_1 + s_2\rho q_2}.$$

Both expectations are finite because each integrand is bounded by $1/s_2$ and $1/s_1$. The integral is positive, so $\psi(\rho) < 0$ for $\rho < r$ and $\psi(\rho) > 0$ for $\rho > r$. Fix $\varepsilon \in (0, 1)$. Almost surely, for all large $n$, $\Psi_n(r(1 - \varepsilon)) < 0 < \Psi_n(r(1 + \varepsilon))$, and since $\Psi_n$ is increasing its root $\hat r$ lies in $(r(1 - \varepsilon), r(1 + \varepsilon))$. So $\hat r \to r$ almost surely. $\blacksquare$
