---
title: The length rho_t, its bounds, and the rectification term of RAdam
proves: [correctness]
status: full
---

**Setting.** Fix $0 < \beta < 1$ (this is $\beta_2$). After $t$ steps Adam's bias-corrected second moment is $\hat{v}_t = \sum_{i=1}^t w_i g_i^2$ with weights $w_i = (1 - \beta)\beta^{t-i}/(1 - \beta^t)$, which are positive and add to $1$. A simple moving average of the last $f$ values $g_{t-f+1}^2, \ldots, g_t^2$ has its center of mass at $t - (f-1)/2$. RAdam defines $\rho_t$ as the $f$ for which the two centers of mass agree, $\rho_\infty = 2/(1 - \beta) - 1$, and, for $\rho_t > 4$, $r_t = \sqrt{\phi(\rho_t)/\phi(\rho_\infty)}$ with $\phi(\rho) = (\rho - 4)(\rho - 2)/\rho$.

**Claim 1 (closed form).** $\rho_t = \rho_\infty - 2t\beta^t/(1 - \beta^t)$.

*Proof.* The center of mass is $\mu_t = \sum_i i\,w_i$. With $k = t - i$,
$$(1 - \beta^t)\,\mu_t = \sum_{k=0}^{t-1}(t - k)(1 - \beta)\beta^k = t(1 - \beta^t) - (1 - \beta)\sum_{k=0}^{t-1}k\beta^k.$$
The standard sum $\sum_{k=0}^{t-1}k\beta^k = \beta\bigl(1 - t\beta^{t-1} + (t-1)\beta^t\bigr)/(1 - \beta)^2$ gives
$$t - \mu_t = \frac{\beta - t\beta^t + (t-1)\beta^{t+1}}{(1 - \beta)(1 - \beta^t)}.$$
Setting $t - (f-1)/2 = \mu_t$ gives $f = 1 + 2(t - \mu_t)$. On the other side,
$$\rho_\infty - 1 - \frac{2t\beta^t}{1 - \beta^t} = \frac{2\beta}{1 - \beta} - \frac{2t\beta^t}{1 - \beta^t} = \frac{2\bigl(\beta(1 - \beta^t) - t\beta^t(1 - \beta)\bigr)}{(1 - \beta)(1 - \beta^t)} = \frac{2\bigl(\beta - t\beta^t + (t-1)\beta^{t+1}\bigr)}{(1 - \beta)(1 - \beta^t)},$$
which is $2(t - \mu_t)$. So $f = \rho_\infty - 2t\beta^t/(1 - \beta^t)$. $\square$

**Claim 2 (bounds and monotonicity).** $\rho_1 = 1$; $\rho_t$ is strictly increasing in $t$ with limit $\rho_\infty$; and $\rho_t \le t$, with equality only for $t = 1$.

*Proof.* For $t = 1$, $\rho_1 = 2/(1 - \beta) - 1 - 2\beta/(1 - \beta) = 1$. Write $u = 1/\beta > 1$, so $t\beta^t/(1 - \beta^t) = t/(u^t - 1)$ and $(u^t - 1)/t = (u - 1)\cdot\frac{1}{t}\sum_{j=0}^{t-1}u^j$. The mean of $1, u, \ldots, u^{t-1}$ strictly increases with $t$, because each new term is larger than all earlier ones, and it tends to infinity. So $t\beta^t/(1 - \beta^t)$ strictly decreases to $0$, and $\rho_t$ strictly increases to $\rho_\infty$. For the upper bound, the weights $w_i$ increase with $i$, so their center of mass is at least that of the uniform weights: $\mu_t \ge (t + 1)/2$, with equality only when all weights are equal, which for $\beta < 1$ happens only for $t = 1$. Then $\rho_t = 1 + 2(t - \mu_t) \le t$. $\square$

**Consequences for the algorithm.** With the paper's test $\rho_t > 4$, the steps $t = 1, 2, 3, 4$ always take the momentum branch, for every $\beta_2$, because $\rho_t \le t$. Since $\rho_t < \rho_\infty$, if $\rho_\infty \le 4$, that is $\beta_2 \le 3/5$, every step takes the momentum branch and RAdam is SGD with bias-corrected momentum. If $\rho_\infty > 4$, Claim 2 gives a first step $t_0$ with $\rho_{t_0} > 4$, and all later steps are rectified. For $\beta_2 = 0.999$, $\rho_4 = 3.9975$ and $\rho_5 = 4.996$, so $t_0 = 5$; with the threshold $5$ of the official code, $t_0 = 6$.

**Claim 3 (the rectification term).** For $4 < \rho_t < \rho_\infty$, $0 < r_t < 1$; $r_t$ is strictly increasing in $t$ and tends to $1$.

*Proof.* $\phi(\rho) = \rho - 6 + 8/\rho$ has $\phi'(\rho) = 1 - 8/\rho^2 > 0$ for $\rho > 2\sqrt2$, so $\phi$ is strictly increasing on $[4, \infty)$ with $\phi(4) = 0$. Hence $0 < \phi(\rho_t) < \phi(\rho_\infty)$, which gives $0 < r_t < 1$. By Claim 2, $\rho_t$ increases to $\rho_\infty$, so $r_t$ increases to $\sqrt{\phi(\rho_\infty)/\phi(\rho_\infty)} = 1$ by continuity. $\square$

**What $r_t$ corrects.** The paper models $\psi_t^2 = 1/\hat{v}_t$ as scaled inverse chi squared with $\rho_t$ degrees of freedom and scale $1/\sigma^2$, and derives the first order approximation $\operatorname{Var}[\psi_t] \approx \rho_t/(2(\rho_t - 2)(\rho_t - 4)\sigma^2) = 1/(2\sigma^2\phi(\rho_t))$ (Eq. 5 of the paper), which is finite only for $\rho_t > 4$. Under this approximation, $\operatorname{Var}[r_t\psi_t] = r_t^2/(2\sigma^2\phi(\rho_t)) = 1/(2\sigma^2\phi(\rho_\infty))$, the variance of the limit. So by construction the rectified adaptive learning rate has the same approximate variance at every step. The approximation itself is the model of the paper and is not proved here; the tests check it by simulation for Gaussian gradients.
