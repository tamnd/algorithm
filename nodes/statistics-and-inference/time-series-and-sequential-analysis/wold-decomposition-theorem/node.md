---
tag: YMGAKW
kind: theorem
slug: wold-decomposition-theorem
name: Wold decomposition theorem
aliases:
- Wold representation
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: Every weakly stationary process is the sum of a deterministic part and an infinite moving average of its one-step prediction errors.
prereqs: [stationary-process, linear-prediction]
see_also: [moving-average-model, arma-model, innovations-algorithm, partial-autocorrelation-function, power-spectral-density, wiener-filter, kalman-filter, levinson-durbin-recursion]
sources:
  - book: "Herman Wold, A Study in the Analysis of Stationary Time Series, Almqvist and Wiksell, Uppsala, 1938"
    title: Wold 1938 (doctoral thesis, Stockholm University; second edition 1954 with an appendix by Peter Whittle)
    locator: the decomposition theorem for discrete stationary processes and its use for the moving average and autoregressive schemes
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 2.3 (the projection theorem, p. 48), Section 5.7 (the Wold decomposition, pp. 187 to 190) and Section 5.8 (Kolmogorov's formula, p. 191)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 2.6 (the Wold decomposition, p. 67), stated without proof
  - paper: doi:10.2307/1907241
    title: Eugen Slutzky, The summation of random causes as the source of cyclic processes, Econometrica 5(2), 1937
    locator: pp. 105 to 146 (moving sums of random shocks give cycles; the English version of the 1927 Russian paper)
---

The Wold decomposition theorem says that every weakly [stationary process](/stationary-process/) with a nonzero one-step prediction error splits into two uncorrelated parts. The first is a moving average of infinite order, $\sum_{j \ge 0} \psi_j \varepsilon_{t-j}$, driven by the process's own one-step prediction errors $\varepsilon_t$. The second is a deterministic process, which the infinitely remote past predicts without error. The theorem is the reason why linear time series models are moving averages and autoregressions: once the deterministic part is removed, a stationary process is a linear filter of white noise. Herman Wold proved it in his 1938 thesis.

## Statement

**Setting.** Let $\{X_t : t \in \mathbb{Z}\}$ be weakly stationary with mean 0 (subtract $\mu$ first). Work in the Hilbert space $L^2$ of random variables with finite variance and the inner product $\langle U, W \rangle = \mathbb{E}[UW]$. Let

- $\mathcal{M}_t = \overline{\operatorname{sp}}\{X_s : s \le t\}$, the closed linear span of the past and present at time $t$,
- $\mathcal{M}_{-\infty} = \bigcap_t \mathcal{M}_t$, the remote past,
- $P_t$ the orthogonal projection onto $\mathcal{M}_t$, so that $P_{t-1} X_t$ is the best linear predictor of $X_t$ from the infinite past,
- $\sigma^2 = \mathbb{E}[(X_t - P_{t-1} X_t)^2]$, the one-step prediction error variance. It does not depend on $t$ (Step 0 below).

The process is **deterministic** when $\sigma^2 = 0$, that is when $X_t \in \mathcal{M}_{t-1}$ for every $t$.

**Theorem (Wold 1938).** If $\sigma^2 > 0$, then

$$X_t = \sum_{j = 0}^{\infty} \psi_j \varepsilon_{t-j} + V_t, \qquad t \in \mathbb{Z},$$

with the sum converging in mean square, where

1. $\varepsilon_t = X_t - P_{t-1} X_t$, and $\{\varepsilon_t\} \sim \mathrm{WN}(0, \sigma^2)$;
2. $\psi_0 = 1$, $\psi_j = \mathbb{E}[X_t \varepsilon_{t-j}]/\sigma^2$ does not depend on $t$, and $\sum_j \psi_j^2 < \infty$;
3. $\varepsilon_t \in \mathcal{M}_t$;
4. $\mathbb{E}[\varepsilon_s V_t] = 0$ for all $s$ and $t$;
5. $V_t \in \mathcal{M}_{-\infty}$;
6. $\{V_t\}$ is a deterministic stationary process.

The sequences $\{\psi_j\}$, $\{\varepsilon_t\}$ and $\{V_t\}$ are the only ones with properties 1 to 5 (with $\varepsilon$ any white noise with $\psi_0 = 1$ in 1). The process is called **purely nondeterministic** (or regular) when $V_t = 0$, which happens exactly when $\mathcal{M}_{-\infty} = \{0\}$.

## In plain words

Stand at some time and try to guess the next value of a stationary series with the best straight-line rule built on everything seen so far. Your mistake is the surprise of that step. The theorem says that the series is just a weighted sum of all its past surprises, with the newest surprise at full weight and older ones fading in a way whose squared weights add up to a finite total. Sometimes a second piece is left over. That piece is so regular, like a perfect sine wave, that the far past alone tells you its value exactly. The surprises are uncorrelated with each other, but they need not be independent, and the rule is only the best straight-line rule.

## Proof

The proof uses only the projection theorem in a Hilbert space (Brockwell and Davis 1991, Section 2.3): for a closed subspace $\mathcal{M}$ and any $Y$, there is a unique $PY \in \mathcal{M}$ with $Y - PY \perp \mathcal{M}$, and $\lVert Y - PY \rVert$ is the smallest distance from $Y$ to $\mathcal{M}$. Let $\mathcal{H} = \overline{\operatorname{sp}}\{X_t : t \in \mathbb{Z}\}$.

**Step 0 (the shift).** Define $U \sum_i a_i X_{t_i} = \sum_i a_i X_{t_i + 1}$ on finite linear combinations. By stationarity, $\lVert \sum_i a_i X_{t_i + 1} \rVert^2 = \sum_{i, k} a_i a_k \gamma(t_i - t_k) = \lVert \sum_i a_i X_{t_i} \rVert^2$, so $U$ is well defined and preserves norms. It extends by continuity to a unitary map of $\mathcal{H}$ onto itself with $U X_t = X_{t+1}$. It maps $\mathcal{M}_t$ onto $\mathcal{M}_{t+1}$, so $U P_t = P_{t+1} U$. Hence $U \varepsilon_t = \varepsilon_{t+1}$, $\lVert \varepsilon_t \rVert^2$ is the same for every $t$, and $\langle X_t, \varepsilon_{t-j} \rangle = \langle U^t X_0, U^t \varepsilon_{-j} \rangle = \langle X_0, \varepsilon_{-j} \rangle$ does not depend on $t$.

**Step 1 (the innovations are white noise).** $\varepsilon_t = X_t - P_{t-1} X_t$ lies in $\mathcal{M}_t$ and is orthogonal to $\mathcal{M}_{t-1}$. For $s < t$, $\varepsilon_s \in \mathcal{M}_s \subseteq \mathcal{M}_{t-1}$, so $\mathbb{E}[\varepsilon_s \varepsilon_t] = 0$. Every element of $\mathcal{H}$ has mean 0, because it is an $L^2$ limit of linear combinations of variables with mean 0. With Step 0, $\{\varepsilon_t\} \sim \mathrm{WN}(0, \sigma^2)$. This proves 1 and 3.

**Step 2 (peeling one innovation off the past).** $X_t = \varepsilon_t + P_{t-1} X_t$ with $P_{t-1} X_t \in \mathcal{M}_{t-1}$, so $\mathcal{M}_t = \operatorname{sp}\{\varepsilon_t\} \oplus \mathcal{M}_{t-1}$, an orthogonal sum. Repeating $k$ times gives

$$\mathcal{M}_t = \operatorname{sp}\{\varepsilon_t, \varepsilon_{t-1}, \ldots, \varepsilon_{t-k+1}\} \oplus \mathcal{M}_{t-k}.$$

**Step 3 (the moving average part).** The variables $\varepsilon_{t-j}/\sigma$, $j \ge 0$, are orthonormal. Let $\mathcal{E}_t = \overline{\operatorname{sp}}\{\varepsilon_s : s \le t\}$. The projection of $X_t$ onto $\mathcal{E}_t$ is $\sum_{j \ge 0} \psi_j \varepsilon_{t-j}$ with $\psi_j = \langle X_t, \varepsilon_{t-j} \rangle/\sigma^2$, and Bessel's inequality gives $\sigma^2 \sum_j \psi_j^2 \le \mathbb{E}[X_t^2] = \gamma(0)$. So the series converges in mean square. By Step 0, $\psi_j$ does not depend on $t$, and $\psi_0 = \langle \varepsilon_t + P_{t-1} X_t, \varepsilon_t \rangle/\sigma^2 = 1$ because $P_{t-1} X_t \perp \varepsilon_t$. This proves 2.

**Step 4 (the remainder is orthogonal to all innovations).** Let $V_t = X_t - \sum_{j \ge 0} \psi_j \varepsilon_{t-j}$. As the error of a projection onto $\mathcal{E}_t$, $V_t \perp \varepsilon_s$ for $s \le t$. Also $V_t \in \mathcal{M}_t$, since $X_t$ and every $\varepsilon_{t-j}$ lie there. For $s > t$, $\varepsilon_s \perp \mathcal{M}_{s-1} \supseteq \mathcal{M}_t$, so $V_t \perp \varepsilon_s$. This proves 4.

**Step 5 (the remainder lies in the remote past).** $V_t \in \mathcal{M}_t$ and $V_t \perp \varepsilon_t, \ldots, \varepsilon_{t-k+1}$. By Step 2, $V_t \in \mathcal{M}_{t-k}$ for every $k \ge 1$, so $V_t \in \mathcal{M}_{-\infty}$. This proves 5.

**Step 6 (the remainder is deterministic).** Let $\mathcal{M}^V_s = \overline{\operatorname{sp}}\{V_r : r \le s\}$. For $r \le s$, $X_r = \sum_j \psi_j \varepsilon_{r-j} + V_r$ with the first term in $\mathcal{E}_s$, and $\mathcal{E}_s \perp \mathcal{M}^V_s$ by Step 4. Both $\mathcal{E}_s$ and $\mathcal{M}^V_s$ lie in $\mathcal{M}_s$, so $\mathcal{M}_s = \mathcal{E}_s \oplus \mathcal{M}^V_s$. Now $\mathcal{M}_{-\infty} \subseteq \mathcal{M}_s$, and $\mathcal{M}_{-\infty} \perp \mathcal{E}_s$, because each $\varepsilon_q$ is orthogonal to $\mathcal{M}_{q-1} \supseteq \mathcal{M}_{-\infty}$. So $\mathcal{M}_{-\infty} \subseteq \mathcal{M}^V_s$ for every $s$. With Step 5, $V_t \in \mathcal{M}_{-\infty} \subseteq \mathcal{M}^V_{t-1}$: the past of $V$ predicts $V_t$ with no error. Finally $U V_t = V_{t+1}$ by Step 0, so $\{V_t\}$ is stationary. This proves 6.

**Step 7 (uniqueness).** Suppose $X_t = \sum_j c_j e_{t-j} + W_t$ with $\{e_t\}$ white noise, $c_0 = 1$, $e_t \in \mathcal{M}_t$, $W_t \in \mathcal{M}_{-\infty}$ and $e_s \perp W_t$ for all $s, t$. Every $X_s$ with $s \le t - 1$ is then in the closed span of $\{e_r : r \le t - 1\}$ and $\{W_r\}$, and $e_t$ is orthogonal to all of these, so $e_t \perp \mathcal{M}_{t-1}$. The terms $\sum_{j \ge 1} c_j e_{t-j}$ and $W_t$ lie in $\mathcal{M}_{t-1}$. So $\sum_{j \ge 1} c_j e_{t-j} + W_t$ is the projection $P_{t-1} X_t$, and $e_t = X_t - P_{t-1} X_t = \varepsilon_t$. Then $c_j = \langle X_t, \varepsilon_{t-j} \rangle/\sigma^2 = \psi_j$ and $W_t = V_t$. $\square$

## Consequences

- **Prediction.** With the decomposition, $P_t X_{t+h} = \sum_{j \ge h} \psi_j \varepsilon_{t+h-j} + V_{t+h}$, because $\varepsilon_{t+1}, \ldots, \varepsilon_{t+h}$ are orthogonal to $\mathcal{M}_t$ and the other terms lie in it. The $h$-step mean squared error is $\sigma^2 \sum_{j = 0}^{h-1} \psi_j^2$. It grows to $\operatorname{Var}(X_t) - \operatorname{Var}(V_t)$ as $h \to \infty$. This is the theory behind [linear prediction](/linear-prediction/) and the [Wiener filter](/wiener-filter/).
- **Moving averages and ARMA models.** A purely nondeterministic process is an MA($\infty$) process. A finite [moving-average model](/moving-average-model/) truncates the $\psi_j$, and an [ARMA model](/arma-model/) approximates the generating function $\psi(z) = \sum_j \psi_j z^j$ by a ratio $\theta(z)/\phi(z)$ of polynomials. For a causal and invertible ARMA process, the Wold innovations are the ARMA noise and the $\psi_j$ are the ARMA weights.
- **Spectrum.** For a purely nondeterministic process, $\gamma(h) = \sigma^2 \sum_j \psi_j \psi_{j + |h|}$ and the spectral density is $f(\lambda) = \frac{\sigma^2}{2\pi} |\psi(e^{-i\lambda})|^2$. Kolmogorov's formula expresses the prediction error in terms of the spectrum: $\sigma^2 = 2\pi \exp\{\frac{1}{2\pi} \int_{-\pi}^{\pi} \log f(\lambda)\, d\lambda\}$, where $f$ is the density of the absolutely continuous part of the spectral distribution (Brockwell and Davis 1991, Section 5.8). So $\sigma^2 > 0$ exactly when $\int \log f > -\infty$. The [Whittle likelihood](/whittle-likelihood/) uses this formula.
- **Finite samples.** With $n$ observations instead of the infinite past, the [innovations algorithm](/innovations-algorithm/) computes the one-step errors $X_{m+1} - \hat X_{m+1}$, and the [Levinson-Durbin recursion](/levinson-durbin-recursion/) computes the finite-past predictors. Their error variances decrease to $\sigma^2$ as the past grows. The [Kalman filter](/kalman-filter/) gives the same innovations for a process in state space form.
- **Partial autocorrelations.** The [partial autocorrelation function](/partial-autocorrelation-function/) measures how much each further past value reduces the prediction error. The errors satisfy $v_k = \gamma(0) \prod_{j=1}^{k} (1 - \phi_{jj}^2)$, which decreases to $\sigma^2$.

## Tightness

- **Uncorrelated, not independent.** The innovations are white noise and need not be independent, even when the process is a linear filter of IID noise. Take the noncausal AR(1) process $X_t = \phi X_{t-1} + Z_t$ with $|\phi| > 1$ and $Z_t \sim \mathrm{IID}(0, \sigma^2)$. Its stationary solution is $X_t = -\sum_{j \ge 1} \phi^{-j} Z_{t+j}$, and it has the same autocovariance as the causal AR(1) with coefficient $1/\phi$ and noise variance $\sigma^2/\phi^2$. Its Wold form is $X_t = \phi^{-1} X_{t-1} + \varepsilon_t$ with $\varepsilon_t \sim \mathrm{WN}(0, \sigma^2/\phi^2)$. When $Z_t$ is not Gaussian, the $\varepsilon_t$ are uncorrelated but not independent (Brockwell and Davis 1991, Section 3.1).
- **Linear, not best.** The decomposition concerns linear prediction only. Let $Z_t$ be IID $N(0, 1)$ and $X_t = Z_t Z_{t-1}$. Then $\mathbb{E}[X_t X_{t+h}] = 0$ for $h \ne 0$, so $X$ is white noise, its Wold form is $X_t = \varepsilon_t$, and no linear rule predicts it. But $\operatorname{Cov}(X_t^2, X_{t-1}^2) = \mathbb{E}[Z_{t-1}^4] - 1 = 2$, so the squares are predictable. Volatility models such as the [GARCH model](/garch-model/) use this kind of dependence.
- **Square summable, not absolutely summable.** The theorem gives only $\sum_j \psi_j^2 < \infty$. This cannot be improved: fractionally integrated (long-memory) processes with memory parameter $d \in (0, 1/2)$ have $\psi_j$ of order $j^{d-1}$, which is square summable but not summable, and their autocovariances are not summable either.
- **Infinitely many weights.** Nothing forces $\psi$ to be rational or to have finitely many nonzero terms, so an ARMA model is an approximation in general.
- **The deterministic part can be large.** The random sinusoid $X_t = A \cos(\omega t) + B \sin(\omega t)$ of the [stationary process](/stationary-process/) page satisfies $X_t = 2\cos(\omega) X_{t-1} - X_{t-2}$, so $\sigma^2 = 0$ and $X = V$. If a white noise $Z_t$, uncorrelated with $A$ and $B$, is added, then the sinusoid can be recovered from the infinite past (for example, $\frac{2}{k}\sum_{s = t-k}^{t-1} \cos(\omega s) X_s \to A$ in mean square as $k \to \infty$), so $V_t$ is the sinusoid, $\varepsilon_t = Z_t$ and $\psi = (1, 0, 0, \ldots)$.
- **Stationarity is needed.** A random walk has no decomposition of this form with a stationary $V$, since its variance grows without bound.

## History

Yule (1927) fitted an autoregression to sunspot numbers, and Slutsky (1927 in Russian, 1937 in English) showed that moving sums of random shocks produce cycles that look regular. Herman Wold, a student of Harald Cramér, put the two schemes into one theory in his 1938 Stockholm thesis. He proved that every stationary process is the sum of a deterministic part and a moving average of uncorrelated shocks. Kolmogorov (1941) gave the Hilbert space treatment of stationary sequences and the formula for the prediction error in terms of the spectrum, and Wiener developed the continuous-time prediction theory in the same years. The second edition of Wold's book (1954) has an appendix by Peter Whittle on later work.

## References
