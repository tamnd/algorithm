---
title: The acceptance ratio identity, the Bennett equation, its unique root and the optimal weight
proves: [correctness]
status: full
---

Let $U_0$ and $U_1$ be potentials on the same space with $Z_k = \int e^{-\beta U_k(x)}\,dx$ finite and positive, $A_k = -\beta^{-1} \ln Z_k$ and $\Delta A = A_1 - A_0$. Write $\langle g \rangle_k = Z_k^{-1} \int g\, e^{-\beta U_k}\,dx$, $w_F = \beta(U_1 - U_0)$ on state-0 samples, $w_R = \beta(U_0 - U_1)$ on state-1 samples, and $f(t) = 1/(1 + e^t)$.

**Claim 1 (the acceptance ratio identity).** For every measurable $W > 0$ with $\int W e^{-\beta U_0} e^{-\beta U_1}\,dx$ finite and positive,
$$\frac{Z_1}{Z_0} = \frac{\langle W e^{-\beta U_1} \rangle_0}{\langle W e^{-\beta U_0} \rangle_1}.$$

*Proof.* Both averages are integrals of the same function $W e^{-\beta U_0} e^{-\beta U_1}$, divided by $Z_0$ in the numerator and by $Z_1$ in the denominator. Let $I$ be that integral. Then the ratio is $(I / Z_0) / (I / Z_1) = Z_1 / Z_0$. $\square$

**Claim 2 (the Bennett equation).** Let $n_0, n_1 > 0$ and $C^* = \beta \Delta A + \ln(n_1 / n_0)$. Then
$$n_1 \langle f(w_R + C^*) \rangle_1 = n_0 \langle f(w_F - C^*) \rangle_0.$$

*Proof.* Take $W = 1 / (n_0 e^{-\beta U_0} + n_1 (Z_0 / Z_1) e^{-\beta U_1})$, which satisfies the condition of Claim 1 because $W e^{-\beta U_0} e^{-\beta U_1} \le e^{-\beta U_0} / (n_1 Z_0 / Z_1)$ is integrable and positive. Note $Z_0 / Z_1 = e^{\beta \Delta A}$. Then
$$W e^{-\beta U_1} = \frac{1}{n_0 e^{\beta (U_1 - U_0)} + n_1 e^{\beta \Delta A}} = \frac{1}{n_1 e^{\beta \Delta A}}\, f(w_F - C^*),$$
because $n_0 e^{w_F} / (n_1 e^{\beta \Delta A}) = e^{w_F - C^*}$. In the same way
$$W e^{-\beta U_0} = \frac{1}{n_0 + n_1 e^{\beta \Delta A} e^{\beta(U_0 - U_1)}} = \frac{1}{n_0}\, f(w_R + C^*).$$
Claim 1 gives $e^{-\beta \Delta A} = \langle W e^{-\beta U_1} \rangle_0 / \langle W e^{-\beta U_0} \rangle_1 = n_0 \langle f(w_F - C^*) \rangle_0 / (n_1 e^{\beta \Delta A} \langle f(w_R + C^*) \rangle_1)$. Multiply both sides by $e^{\beta \Delta A}$ and rearrange. $\square$

The algorithm replaces the two averages by sample means. By the law of large numbers the sample equation tends to the equation of Claim 2, and Claim 3 shows that both have one root, so the estimate is consistent when the right side of the limit equation is strictly monotone, which it is by the same argument.

**Claim 3 (one root and a valid bracket).** Let $R(C) = \sum_{j=1}^{n_1} f(w_{R,j} + C) - \sum_{i=1}^{n_0} f(w_{F,i} - C)$ for finite samples. Then $R$ is continuous and strictly decreasing, $R(C) \to n_1$ as $C \to -\infty$ and $R(C) \to -n_0$ as $C \to +\infty$, so $R$ has exactly one root $C$. If $\max(n_0, n_1) / \min(n_0, n_1) < e^{40} - 1$, the root lies in $[lo, hi]$ with $lo = \min(\min_i w_{F,i}, \min_j (-w_{R,j})) - 40$ and $hi = \max(\max_i w_{F,i}, \max_j (-w_{R,j})) + 40$, and the bisection of lines L3 to L6 returns a point within tol of it.

*Proof.* $f$ is continuous and strictly decreasing, so each $f(w_R + C)$ decreases and each $f(w_F - C)$ increases in $C$, and $R$ is strictly decreasing. The limits follow from $f(t) \to 1$ as $t \to -\infty$ and $f(t) \to 0$ as $t \to +\infty$. So $R$ has exactly one zero.

At $C = lo$, every $w_{R,j} + lo \le w_{R,j} - w_{R,j} - 40 = -40$, so each $f(w_{R,j} + lo) \ge 1 / (1 + e^{-40})$, and every $w_{F,i} - lo \ge 40$, so each $f(w_{F,i} - lo) \le e^{-40}$. Hence $R(lo) \ge n_1 / (1 + e^{-40}) - n_0 e^{-40} > 0$ when $n_0 / n_1 < e^{40} / (1 + e^{-40})$, which holds under the assumption. In the same way $R(hi) \le n_1 e^{-40} - n_0 / (1 + e^{-40}) < 0$ when $n_1 / n_0 < e^{40} / (1 + e^{-40})$. By the intermediate value theorem the root lies in $(lo, hi)$. Lines L5 and L6 keep $R(lo) > 0 \ge R(hi)$, so the root stays in $[lo, hi]$, and the width halves at each step until it is below tol. $\square$

**Claim 4 (least variance).** Let $\hat Z$ be the ratio of the two sample means of Claim 1 with $n_0$ independent samples of state 0 and $n_1$ of state 1, and let $\phi = e^{-\beta U_0} e^{-\beta U_1}$. To first order in $1 / n_0$ and $1 / n_1$ (the delta method), the relative variance of $\hat Z$ is
$$\frac{\mathrm{var}\,\hat Z}{(Z_1 / Z_0)^2} = \frac{\int W^2 \phi\, D\,dx}{\bigl(\int W \phi\,dx\bigr)^2} - \frac{1}{n_0} - \frac{1}{n_1}, \qquad D = \frac{Z_0 e^{-\beta U_1}}{n_0} + \frac{Z_1 e^{-\beta U_0}}{n_1}.$$
Among all $W$ for which these integrals are finite, this is smallest when $W \propto 1 / D$, which is the weight of Claim 2.

*Proof.* Write $a = \langle W e^{-\beta U_1} \rangle_0 = I / Z_0$ and $b = \langle W e^{-\beta U_0} \rangle_1 = I / Z_1$ with $I = \int W \phi$. The sample means $\hat a$ and $\hat b$ are independent with variances $\sigma_a^2 / n_0$ and $\sigma_b^2 / n_1$, where $\sigma_a^2 + a^2 = \langle W^2 e^{-2\beta U_1} \rangle_0 = Z_0^{-1} \int W^2 \phi\, e^{-\beta U_1}$ and $\sigma_b^2 + b^2 = Z_1^{-1} \int W^2 \phi\, e^{-\beta U_0}$. The delta method gives
$$\frac{\mathrm{var}(\hat a / \hat b)}{(a / b)^2} \approx \frac{\sigma_a^2}{n_0 a^2} + \frac{\sigma_b^2}{n_1 b^2} = \frac{Z_0 \int W^2 \phi\, e^{-\beta U_1}}{n_0 I^2} + \frac{Z_1 \int W^2 \phi\, e^{-\beta U_0}}{n_1 I^2} - \frac{1}{n_0} - \frac{1}{n_1}.$$
So the relative variance is $\int W^2 \phi\, D / (\int W \phi)^2 - 1/n_0 - 1/n_1$ with $D > 0$ as in the statement. By the Cauchy-Schwarz inequality, $(\int W \phi)^2 = (\int (W \sqrt{\phi D}) \sqrt{\phi / D})^2 \le \int W^2 \phi D \cdot \int \phi / D$, so the first term is at least $1 / \int (\phi / D)$, which does not depend on $W$, with equality exactly when $W \sqrt{\phi D}$ is proportional to $\sqrt{\phi / D}$, that is $W \propto 1 / D$ where $\phi > 0$. Multiplying $D$ by the constant $n_0 n_1 / Z_1$ shows $1 / D \propto 1 / (n_0 e^{-\beta U_0} + n_1 (Z_0 / Z_1) e^{-\beta U_1})$, the weight of Claim 2. $\square$

The optimal weight contains the unknown $Z_0 / Z_1$, so the algorithm solves for it self-consistently: the root of Claim 3 is the value at which the estimate of Claim 1 with that weight returns the same ratio that was put in. To first order in $1/n$ the self-consistent estimator has the same variance as the estimator with the exact optimal weight (Bennett 1976); this note does not prove that step. Substituting the weight of Claim 2 into the variance formula gives the error bar of the page, which uses the sample variances of $f(w_F - C)$ and $f(w_R + C)$.

**Claim 5 (symmetry and exact cases).** (a) Exchanging the states, which maps $(w_F, w_R, n_0, n_1)$ to $(w_R, w_F, n_1, n_0)$, maps the estimate $\widehat{\Delta A}$ to $-\widehat{\Delta A}$. (b) If $U_1 - U_0 = c$ everywhere, the estimate is $c$. (c) With $n_0 = n_1 = 1$, the estimate is $(w_F - w_R) / (2\beta)$.

*Proof.* (a) Let $C$ be the root for the original data, so $\sum_j f(w_{R,j} + C) = \sum_i f(w_{F,i} - C)$. For the exchanged data the equation is $\sum_i f(w_{F,i} + C') = \sum_j f(w_{R,j} - C')$, which $C' = -C$ satisfies; by Claim 3 it is the root. The new estimate is $(C' - \ln(n_0 / n_1)) / \beta = -(C - \ln(n_1 / n_0)) / \beta$. (b) Then $w_F = \beta c$ and $w_R = -\beta c$, and the equation $n_1 f(C - \beta c) = n_0 f(\beta c - C)$ with $t = C - \beta c$ reads $n_1 / (1 + e^t) = n_0 / (1 + e^{-t}) = n_0 e^t / (1 + e^t)$, so $e^t = n_1 / n_0$ and $C = \beta c + \ln(n_1 / n_0)$, which gives the estimate $c$. (c) The equation $f(w_R + C) = f(w_F - C)$ holds if and only if $w_R + C = w_F - C$ because $f$ is injective, so $C = (w_F - w_R)/2$ and $M = 0$. $\square$

The example on the page with $w_F = 1.0$ and $w_R = -0.2$ is case (c): the estimate is $0.6$.
