---
title: Holt-Winters has an error correction form, Winters' seasonal update is a reparametrization, Holt's linear method gives the ARIMA(0, 2, 2) forecasts, and noise-free trend-plus-season series are forecast exactly
proves: [correctness, termination]
status: full
---

We prove the error correction form of the recursions (Lemma 1), the equivalence of Winters' seasonal update with the component form (Lemma 2), the equivalence of Holt's linear method with ARIMA(0, 2, 2) for one-step and $h$-step forecasts (Theorem 3), the invertibility region (Corollary 4), and exactness on noise-free series (Lemma 5). We do not prove that the forecasts are optimal (minimum mean squared error) for the ETS state space models of Hyndman, Koehler, Snyder and Grose (2002), the equivalence of the additive seasonal method with a seasonal ARIMA model, or any property of the constants chosen by least squares. Indices: $\hat y_t$ is the forecast of $y_t$ made at $t - 1$ (line L1), and $e_t = y_t - \hat y_t$ (line L2).

**Lemma 1 (error correction form).** Lines L3 to L5 are equivalent to
$$\ell_t = \ell_{t-1} + b_{t-1} + \alpha e_t, \qquad b_t = b_{t-1} + \alpha\beta e_t, \qquad s_t = s_{t-m} + \gamma e_t$$
in the additive seasonal method, and to the first two with $e_t = y_t - \ell_{t-1} - b_{t-1}$ in Holt's method.

*Proof.* Line L3: $\alpha(y_t - s_{t-m}) + (1 - \alpha)(\ell_{t-1} + b_{t-1}) = \ell_{t-1} + b_{t-1} + \alpha(y_t - s_{t-m} - \ell_{t-1} - b_{t-1}) = \ell_{t-1} + b_{t-1} + \alpha e_t$. Line L4: $\beta(\ell_t - \ell_{t-1}) + (1 - \beta)b_{t-1} = b_{t-1} + \beta(\ell_t - \ell_{t-1} - b_{t-1}) = b_{t-1} + \alpha\beta e_t$, by the first identity. Line L5: $\gamma(y_t - \ell_{t-1} - b_{t-1}) + (1 - \gamma)s_{t-m} = s_{t-m} + \gamma(y_t - \ell_{t-1} - b_{t-1} - s_{t-m}) = s_{t-m} + \gamma e_t$. Holt's method is the case $s \equiv 0$. $\square$

**Lemma 2 (Winters' form).** Winters (1960) updates the season by $s_t = \gamma^*(y_t - \ell_t) + (1 - \gamma^*)s_{t-m}$, with $\ell_t$ from line L3. This is line L5 with $\gamma = \gamma^*(1 - \alpha)$.

*Proof.* From line L3, $y_t - \ell_t = y_t - \alpha y_t + \alpha s_{t-m} - (1 - \alpha)(\ell_{t-1} + b_{t-1}) = (1 - \alpha)(y_t - \ell_{t-1} - b_{t-1}) + \alpha s_{t-m}$. Substituting, $s_t = \gamma^*(1 - \alpha)(y_t - \ell_{t-1} - b_{t-1}) + (\gamma^*\alpha + 1 - \gamma^*)s_{t-m} = \gamma(y_t - \ell_{t-1} - b_{t-1}) + (1 - \gamma)s_{t-m}$, since $\gamma^*\alpha + 1 - \gamma^* = 1 - \gamma^*(1 - \alpha) = 1 - \gamma$. $\square$

**Theorem 3 (Holt's method is ARIMA(0, 2, 2)).** In Holt's method put $f_t = \ell_t + b_t$, the forecast of $y_{t+1}$ made at $t$, and $\theta_1 = \alpha(1 + \beta) - 2$, $\theta_2 = 1 - \alpha$. Then for every $t \ge 3$,
$$\nabla^2y_t = e_t + \theta_1e_{t-1} + \theta_2e_{t-2}, \qquad f_t = 2y_t - y_{t-1} + \theta_1e_t + \theta_2e_{t-1}. \tag{1}$$
The second equation is the one-step forecast of ARIMA(0, 2, 2) with moving average polynomial $\theta(z) = 1 + \theta_1z + \theta_2z^2$, computed from its innovations. So, started from the same $f_2$ and $e_1$, the two methods produce the same one-step forecasts and the same errors for all later $t$. The $h$-step forecasts agree as well: Holt's $\ell_n + hb_n$ equals the ARIMA forecast for every $h \ge 1$.

*Proof.* By Lemma 1, $f_t - f_{t-1} = (\ell_t - \ell_{t-1}) + (b_t - b_{t-1}) = b_{t-1} + \alpha e_t + \alpha\beta e_t$. Taking one more difference and using $b_{t-1} - b_{t-2} = \alpha\beta e_{t-1}$,
$$\nabla^2f_t = \alpha\beta e_{t-1} + \alpha(1 + \beta)(e_t - e_{t-1}) = \alpha(1 + \beta)e_t - \alpha e_{t-1}.$$
Since $y_t = f_{t-1} + e_t$ for all $t$, $\nabla^2y_t = \nabla^2f_{t-1} + \nabla^2e_t = \alpha(1 + \beta)e_{t-1} - \alpha e_{t-2} + e_t - 2e_{t-1} + e_{t-2}$, which is $e_t + (\alpha(1 + \beta) - 2)e_{t-1} + (1 - \alpha)e_{t-2}$. That is the first equation of (1). Apply it at $t + 1$ with $y_{t+1} = f_t + e_{t+1}$: $f_t + e_{t+1} - 2y_t + y_{t-1} = e_{t+1} + \theta_1e_t + \theta_2e_{t-1}$, which gives the second equation. The ARIMA(0, 2, 2) model $\nabla^2y_t = \varepsilon_t + \theta_1\varepsilon_{t-1} + \theta_2\varepsilon_{t-2}$ has the one-step forecast $2y_t - y_{t-1} + \theta_1\varepsilon_t + \theta_2\varepsilon_{t-1}$, with $\varepsilon_t = y_t - (\text{its forecast})$. Both recursions map $(f_{t-1}, e_{t-1}, y_t, y_{t-1})$ to $f_t$ by the same formula, so by induction on $t$ they agree from a common start.

For $h$ steps, the ARIMA forecasts set future innovations to 0: $\hat y_{n+1} = f_n$, $\hat y_{n+2} = 2f_n - y_n + \theta_2e_n$, and $\hat y_{n+k} = 2\hat y_{n+k-1} - \hat y_{n+k-2}$ for $k \ge 3$. Holt gives $\ell_n + kb_n$. For $k = 1$ both are $f_n$. For $k = 2$, Holt gives $f_n + b_n$, and $2f_n - y_n + (1 - \alpha)e_n - (f_n + b_n) = \ell_n - y_n + (1 - \alpha)e_n$. By Lemma 1, $\ell_n = f_{n-1} + \alpha e_n = y_n - e_n + \alpha e_n$, so this difference is 0. For $k \ge 3$ both sequences satisfy $x_k = 2x_{k-1} - x_{k-2}$, which determines a sequence from its first two terms, so they agree for all $k$. $\square$

**Corollary 4 (invertibility).** The polynomial $\theta(z) = 1 + (\alpha(1 + \beta) - 2)z + (1 - \alpha)z^2$ has both roots outside the unit circle if and only if $0 < \alpha < 2$ and $0 < \alpha\beta < 4 - 2\alpha$.

*Proof.* For $1 + \theta_1z + \theta_2z^2$ the roots lie outside the unit circle if and only if $|\theta_2| < 1$, $\theta_1 + \theta_2 > -1$ and $\theta_2 - \theta_1 > -1$ (the stationarity triangle of an AR(2) polynomial $1 - \phi_1z - \phi_2z^2$ with $\phi_i = -\theta_i$). Here $|1 - \alpha| < 1$ is $0 < \alpha < 2$; $\theta_1 + \theta_2 = \alpha\beta - 1 > -1$ is $\alpha\beta > 0$; and $\theta_2 - \theta_1 = 3 - 2\alpha - \alpha\beta > -1$ is $\alpha\beta < 4 - 2\alpha$. $\square$

Inside this region the errors $e_t$ are a convergent linear filter of the data, and the effect of the start values on the forecasts dies out geometrically. All constants in $(0, 1)$ lie inside it.

**Lemma 5 (exactness on noise-free series).** Let $y_t = a + ct + \sigma_t$ with $\sigma_{t+m} = \sigma_t$, and start the additive method at $\ell_0 = a$, $b_0 = c$, $s_{i-m} = \sigma_i$ for $i = 1..m$. Then $e_t = 0$ for all $t$ and any $\alpha, \beta, \gamma$, and $\hat y_{n+k} = y_{n+k}$ for all $k \ge 1$. The same holds for $y_t = (a + ct)\sigma_t$ with the multiplicative method and $\sigma_t \ne 0$, $a + ct \ne 0$.

*Proof.* By induction on $t$, with the claim $\ell_{t-1} = a + c(t - 1)$, $b_{t-1} = c$, and the seasonal state for position $t$ equal to $\sigma_t$. It holds for $t = 1$ by the start. Then $\hat y_t = a + ct + \sigma_t = y_t$, so $e_t = 0$, and by Lemma 1 $\ell_t = \ell_{t-1} + b_{t-1} = a + ct$, $b_t = c$ and $s_t = s_{t-m} = \sigma_t = \sigma_{t+m}$. The forecasts of line L6 are $a + c(n + k) + \sigma_{n+k} = y_{n+k}$. In the multiplicative case, line L1 gives $(a + ct)\sigma_t = y_t$; line L3 gives $\alpha(a + ct) + (1 - \alpha)(a + ct) = a + ct$; line L4 gives $c$; and line L5 gives $\gamma y_t/(a + ct) + (1 - \gamma)\sigma_t = \sigma_t$. $\square$

**Exact arithmetic.** Every line uses only additions, subtractions, multiplications and, in the multiplicative case, divisions of the inputs. With rational data and constants the outputs are rational, and the implementation computes them exactly when given Fractions. The tests check the worked examples, Theorem 3 and Lemmas 2 and 5 in rationals.

**Termination.** The loop runs $n$ times and line L6 runs $h$ times, each with $O(1)$ work, so the method stops after $\Theta(n + h)$ operations. The grid search for the constants evaluates the method a fixed number of times.
