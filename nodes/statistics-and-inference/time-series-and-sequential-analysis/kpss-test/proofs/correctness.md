---
title: KPSS computes the stated statistic with a nonnegative long-run variance, the statistic is invariant to level, scale and trend, and its numerator has the exact mean of the Brownian bridge limit
proves: [correctness, termination]
status: full
---

We prove that KPSS returns $\eta = \sum_t S_t^2/(n^2\hat\sigma^2(\ell))$ with residual partial sums that start and end at 0 (Lemma 1), that the Bartlett estimate $\hat\sigma^2(\ell)$ is never negative (Lemma 2), that $\eta$ is invariant to the maps of Lemma 3, and that in case "c" with iid errors the numerator has mean $\sigma^2(n^2 - 1)/6$ (Lemma 4), whose scaled limit $1/6$ is the mean of $\int_0^1V(r)^2dr$ for a Brownian bridge $V$. We do not prove the limit law $\eta \Rightarrow \int_0^1V^2$, the consistency of $\hat\sigma^2(\ell)$ for $\ell \to \infty$, $\ell/n \to 0$, or the divergence of $\eta$ under a unit root. These are Theorems in Kwiatkowski, Phillips, Schmidt and Shin (1992), with the partial-sum limit for polynomial regression from MacNeill (1978).

**Lemma 1 (line L1 and the bridge).** In case "c", $e_t = X_t - \bar X$ is the least squares residual on $1$, and $\sum_te_t = 0$. In case "ct", with $\bar t = (n + 1)/2$ and $\hat b = \sum_t(t - \bar t)X_t/\sum_t(t - \bar t)^2$, $e_t = X_t - \bar X - \hat b(t - \bar t)$ is the least squares residual on $1$ and $t$, and $\sum_te_t = \sum_t te_t = 0$. In both cases $S_n = 0$.

*Proof.* The columns $1$ and $t - \bar t$ are orthogonal, since $\sum_t(t - \bar t) = 0$. The least squares fit on an orthogonal basis is the sum of the separate projections, which are $\bar X \cdot 1$ and $\hat b(t - \bar t)$. The span of $1$ and $t - \bar t$ equals the span of $1$ and $t$. A least squares residual is orthogonal to every regressor, so $\sum e_t = 0$, and in case "ct" also $\sum te_t = 0$. Finally $S_n = \sum_te_t = 0$. $\square$

**Lemma 2 (the Bartlett estimate is nonnegative).** Extend $e$ by $e_t = 0$ for $t \le 0$ and $t > n$. For $\ell \ge 0$,
$$\hat\gamma_0 + 2\sum_{j=1}^{\ell}\left(1 - \frac{j}{\ell + 1}\right)\hat\gamma_j = \frac{1}{n(\ell + 1)}\sum_{t=-\ell+1}^{n}\left(\sum_{i=0}^{\ell}e_{t+i}\right)^2 \ \ge 0.$$

*Proof.* Expand the square: $\sum_t\left(\sum_{i=0}^{\ell}e_{t+i}\right)^2 = \sum_{i=0}^{\ell}\sum_{i'=0}^{\ell}\sum_te_{t+i}e_{t+i'}$. For fixed $i, i'$ with $|i - i'| = j$, the inner sum runs over all $t$ for which both indices lie in $1..n$, so it equals $\sum_{s=j+1}^{n}e_se_{s-j} = n\hat\gamma_j$. The number of pairs $(i, i')$ in $\{0, \dots, \ell\}^2$ with $i - i' = j$ is $\ell + 1 - |j|$. So the sum is $n\sum_{j=-\ell}^{\ell}(\ell + 1 - |j|)\hat\gamma_{|j|} = n(\ell + 1)\left(\hat\gamma_0 + 2\sum_{j=1}^{\ell}(1 - j/(\ell + 1))\hat\gamma_j\right)$. Divide by $n(\ell + 1)$. $\square$

The estimate is 0 only if every window sum $\sum_{i=0}^{\ell}e_{t+i}$ is 0. The window that starts at $t = -\ell + 1$ contains only $e_1$, so then $e_1 = 0$, and by induction along the windows all $e_t = 0$. The implementation reports this case as an error. Without the Bartlett weights the estimate can be negative: for $e = (1, -1, 1, -1)$ and $\ell = 1$, $\hat\gamma_0 + 2\hat\gamma_1 = 1 - 3/2 < 0$, while the Bartlett value is $1 - 3/4 = 1/4$.

With Lemmas 1 and 2, lines L2 to L5 compute $N = \sum S_t^2$, the autocovariances, $\hat\sigma^2(\ell) > 0$ and $\eta = N/(n^2\hat\sigma^2(\ell))$, which is the statistic defined on the page.

**Lemma 3 (invariance).** Let $c \ne 0$. In case "c", the map $X_t \mapsto a + cX_t$ leaves $\eta$ unchanged. In case "ct", so does $X_t \mapsto a + bt + cX_t$.

*Proof.* The residual map $X \mapsto e$ is the linear projection $M$ onto the orthogonal complement of the regressors, so $M(a\mathbf 1 + b\mathbf t + cX) = cMX$ whenever $a\mathbf 1 + b\mathbf t$ lies in the regressor span (with $b = 0$ in case "c"). So $e$ becomes $ce$, every $S_t$ becomes $cS_t$, every $\hat\gamma_j$ becomes $c^2\hat\gamma_j$, and $N$ and $\hat\sigma^2(\ell)$ are both multiplied by $c^2$. Their ratio is unchanged. $\square$

**Lemma 4 (the mean of the numerator).** In case "c", let $X_t = \mu + \varepsilon_t$ with $\varepsilon_t$ uncorrelated, mean 0 and variance $\sigma^2$. Then $\operatorname{Var}(S_t) = \sigma^2t(n - t)/n$ and
$$E\sum_{t=1}^{n}S_t^2 = \sigma^2\frac{n^2 - 1}{6}, \qquad \text{so} \qquad \frac{1}{n^2\sigma^2}E\sum_tS_t^2 \to \frac16 = E\int_0^1V(r)^2\,dr.$$

*Proof.* $S_t = \sum_{s \le t}(\varepsilon_s - \bar\varepsilon) = A_t - (t/n)A_n$ with $A_t = \sum_{s \le t}\varepsilon_s$. Since $\operatorname{Var}(A_t) = t\sigma^2$ and $\operatorname{Cov}(A_t, A_n) = t\sigma^2$,
$\operatorname{Var}(S_t) = \sigma^2\left(t - 2t^2/n + t^2/n\right) = \sigma^2t(n - t)/n$, and $ES_t = 0$. Summing, $\sum_{t=1}^{n}t(n - t)/n = \left(n\cdot\frac{n(n+1)}{2} - \frac{n(n+1)(2n+1)}{6}\right)/n = \frac{(n+1)(n-1)}{6}$. For the limit, $E V(r)^2 = r(1 - r)$ and $\int_0^1r(1 - r)dr = 1/6$. $\square$

The same computation in case "ct" gives the limit mean $\int_0^1K(r, r)dr = \int_0^1(r - 4r^2 + 6r^3 - 3r^4)dr = 1/15$, which is the trace of the covariance kernel $K$ stated on the page, and the sum of its eigenvalues.

**Cited: the limit law and consistency.** Under $H_0$, with $\varepsilon_t$ satisfying a functional central limit theorem with long-run variance $\sigma^2 > 0$, $n^{-1/2}S_{\lfloor nr\rfloor} \Rightarrow \sigma V(r)$ (MacNeill 1978 for polynomial regression residuals), and $\hat\sigma^2(\ell) \to \sigma^2$ in probability when $\ell \to \infty$, $\ell/n \to 0$. The continuous mapping theorem then gives $\eta \Rightarrow \int_0^1V^2$. Under $H_1$, $\eta$ is of exact order $n/\ell$ in probability, so $P(\eta > c) \to 1$ for every fixed $c$ (KPSS 1992). The quantiles in the table of the page were computed numerically from the eigenvalue expansion of the limit and are not part of the proof.

**Termination.** Every line is a finite loop over $t = 1..n$ or $j = 0..\ell$. $\square$
