---
title: The targeted estimate is the AIPW estimate at the updated outcome model, and its limit is doubly robust
proves: [correctness]
status: full
---

The outcome is scaled to $[0, 1]$. Unit $i$ has treatment $T_i$, outcome $Y_i \in [0, 1]$, propensity value $\tilde e_i \in (0, 1)$ and initial predictions $Q_{1i}, Q_{0i} \in (0, 1)$ of the mean outcome under each treatment. The clever covariate is $H_i = T_i/\tilde e_i - (1 - T_i)/(1 - \tilde e_i)$, and $Q_{T_i i}$ is the prediction for the arm the unit was in. For a number $\varepsilon$ let

$$Q_{1i}(\varepsilon) = \operatorname{expit}\Big(\operatorname{logit} Q_{1i} + \frac{\varepsilon}{\tilde e_i}\Big), \qquad Q_{0i}(\varepsilon) = \operatorname{expit}\Big(\operatorname{logit} Q_{0i} - \frac{\varepsilon}{1 - \tilde e_i}\Big),$$

so that $\operatorname{logit} Q_{T_i i}(\varepsilon) = \operatorname{logit} Q_{T_i i} + \varepsilon H_i$. The log-likelihood of the fluctuation is $L(\varepsilon) = \sum_i \big(Y_i \log Q_{T_i i}(\varepsilon) + (1 - Y_i)\log(1 - Q_{T_i i}(\varepsilon))\big)$.

**Lemma 1 (the fluctuation step).** $L'(\varepsilon) = \sum_i H_i\big(Y_i - Q_{T_i i}(\varepsilon)\big)$ and $L''(\varepsilon) = -\sum_i H_i^2\,Q_{T_i i}(\varepsilon)(1 - Q_{T_i i}(\varepsilon)) < 0$. So $L$ is strictly concave, it has at most one maximizer, and a maximizer $\hat\varepsilon$ exists if and only if $L'$ changes sign; then $L'(\hat\varepsilon) = 0$.

*Proof.* For $q = \operatorname{expit}(z)$, $dq/dz = q(1 - q)$, and $\frac{d}{dz}\big(y\log q + (1 - y)\log(1 - q)\big) = y(1 - q) - (1 - y)q = y - q$. With $z = \operatorname{logit} Q_{T_i i} + \varepsilon H_i$ the chain rule gives the factor $H_i$ in $L'$ and $H_i^2 q(1 - q)$ in $L''$. Every $H_i \neq 0$ and $0 < q < 1$, so $L'' < 0$. A strictly decreasing continuous $L'$ has at most one zero, which is the maximizer, and it has one exactly when it takes both signs. $\square$

$L'$ fails to change sign only when $Y_i = 1$ for all units with $H_i > 0$ and $Y_i = 0$ for all with $H_i < 0$, or the reverse (the outcome is separated by $H$). Then the code raises an error. Lines L3 to L7 are Newton-Raphson for the root of $L'$ with step halving; each accepted step does not lower $L$, and on a strictly concave smooth function this converges to the maximizer. Lines L8 and L9 give $Q^*_{ti} = Q_{ti}(\hat\varepsilon)$ and $\hat\tau = \frac1n\sum_i (Q^*_{1i} - Q^*_{0i})$.

**Theorem 2 (TMLE is AIPW at the targeted predictions).** Let $Q^*_{1i}, Q^*_{0i}$ be any predictions that satisfy the score equation $\sum_i H_i(Y_i - Q^*_{T_i i}) = 0$. Then

$$\frac1n\sum_i (Q^*_{1i} - Q^*_{0i}) = \hat\tau_{\mathrm{AIPW}}(\tilde e, Q^*_1, Q^*_0).$$

*Proof.* For each unit, $T_i(Y_i - Q^*_{1i})/\tilde e_i - (1 - T_i)(Y_i - Q^*_{0i})/(1 - \tilde e_i) = H_i(Y_i - Q^*_{T_i i})$: if $T_i = 1$ both sides are $(Y_i - Q^*_{1i})/\tilde e_i$, and if $T_i = 0$ both are $-(Y_i - Q^*_{0i})/(1 - \tilde e_i)$. So the AIPW estimate at $Q^*$ is $\frac1n\sum_i(Q^*_{1i} - Q^*_{0i}) + \frac1n\sum_i H_i(Y_i - Q^*_{T_i i})$, and the last sum is 0. $\square$

By Lemma 1 the logistic fluctuation gives predictions that satisfy the score equation, so Theorem 2 applies to TMLE.

**Theorem 3 (the linear fluctuation).** With $Q_{1i}(\varepsilon) = Q_{1i} + \varepsilon/\tilde e_i$ and $Q_{0i}(\varepsilon) = Q_{0i} - \varepsilon/(1 - \tilde e_i)$, the least squares choice $\hat\varepsilon = \sum_i H_i r_i/\sum_i H_i^2$ with $r_i = Y_i - Q_{T_i i}$ satisfies the score equation exactly, so Theorem 2 holds in exact arithmetic.

*Proof.* $Q_{T_i i}(\varepsilon) = Q_{T_i i} + \varepsilon H_i$, so $\sum_i H_i(Y_i - Q_{T_i i}(\hat\varepsilon)) = \sum_i H_i r_i - \hat\varepsilon\sum_i H_i^2 = 0$. $\square$

**Theorem 4 (range).** With the logistic fluctuation, every $Q^*_{ti}$ is in $(0, 1)$, so $\hat\mu_1, \hat\mu_0 \in (0, 1)$ and $\hat\tau \in (-1, 1)$. On the original scale $[a, b]$, $\hat\mu_t \in (a, b)$.

*Proof.* $\operatorname{expit}$ maps the real line into $(0, 1)$, and an average of numbers in $(0, 1)$ is in $(0, 1)$. The scale map $u \mapsto a + (b - a)u$ is increasing. $\square$

**Theorem 5 (no update needed).** If $\tilde e$ is constant within each arm, and $Q_1$ and $Q_0$ come from logistic regressions with an intercept, fitted within each arm, then $\hat\varepsilon = 0$ and the TMLE equals the plug-in estimate $\frac1n\sum_i(Q_{1i} - Q_{0i})$.

*Proof.* The intercept's score equation of the logistic fit in arm $t$ is $\sum_{i:\,T_i = t}(Y_i - Q_{ti}) = 0$. With $H_i = 1/\tilde e$ for every treated unit and $-1/(1 - \tilde e)$ for every control, $L'(0) = \frac{1}{\tilde e}\sum_{T_i = 1}(Y_i - Q_{1i}) - \frac{1}{1 - \tilde e}\sum_{T_i = 0}(Y_i - Q_{0i}) = 0$. By Lemma 1, $\hat\varepsilon = 0$. $\square$

## The limit is doubly robust

Use the setting and assumptions of the [AIPW proof](/augmented-inverse-probability-weighting/): independent units, consistency, ignorability, positivity, true propensity $e$ and true regressions $\mu_t(x) = \mathbb{E}[Y \mid T = t, X = x]$. Fix working functions $\tilde e(x) \in [c, 1 - c]$ and $Q_t(x) \in (0, 1)$, let $Q_t(x; \varepsilon)$ be their fluctuations, $H = T/\tilde e(X) - (1 - T)/(1 - \tilde e(X))$, and suppose the population score $S(\varepsilon) = \mathbb{E}[H(Y - Q_T(X; \varepsilon))]$ has a root $\bar\varepsilon$. Let $\bar\tau = \mathbb{E}[Q_1(X; \bar\varepsilon) - Q_0(X; \bar\varepsilon)]$.

**Theorem 6.** If $\tilde e = e$, or if $Q_1 = \mu_1$ and $Q_0 = \mu_0$, then $\bar\tau = \tau$.

*Proof.* The argument of Theorem 2 in expectation gives $\bar\tau = \mathbb{E}[\psi(\tilde e, \bar Q)] - S(\bar\varepsilon) = \mathbb{E}[\psi(\tilde e, \bar Q)]$, where $\bar Q_t = Q_t(\cdot\,; \bar\varepsilon)$ and $\psi$ is the AIPW score. If $\tilde e = e$, the bias identity of the AIPW page gives $\mathbb{E}[\psi(e, m)] = \tau$ for every outcome function $m$, in particular for $\bar Q$. If $Q_t = \mu_t$, then $S(0) = \mathbb{E}[H\,\mathbb{E}[Y - \mu_T(X) \mid T, X]] = 0$, and $S$ is strictly decreasing (the derivative is $-\mathbb{E}[H^2 Q_T(1 - Q_T)] < 0$), so $\bar\varepsilon = 0$, $\bar Q = \mu$ and $\bar\tau = \mathbb{E}[\mu_1(X) - \mu_0(X)] = \tau$. $\square$

## What is not proved here

That $\hat\varepsilon \to \bar\varepsilon$ and $\hat\tau \to \bar\tau$, that $\hat\tau$ is asymptotically linear with influence function $H(Y - \bar Q_T) + \bar Q_1 - \bar Q_0 - \tau$ when the nuisance estimates converge fast enough, that it is efficient when both are right, and that the influence-function variance gives intervals of the right coverage are cited from van der Laan and Rubin (2006) and van der Laan and Rose (2011, Chapters 4 and 5). The simulation figures on the page are measured.
