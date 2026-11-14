---
title: CUPED with a fixed coefficient is unbiased, the best coefficient cuts the variance by 1 - rho^2, and the within-arm coefficient gives the ANCOVA estimate
proves: [correctness]
status: full
---

There are $n$ units. Unit $i$ has a covariate $X_i$ measured before the experiment and an outcome $Y_i$; the treated arm $\mathcal T$ has $n_t \ge 2$ units and the control arm $\mathcal C$ has $n_c \ge 2$ units. Write $\bar y_t, \bar x_t$ for the means over $\mathcal T$, $\bar y_c, \bar x_c$ for the means over $\mathcal C$, and $\bar x$ for the mean of $X$ over all $n$ units. CUPED returns

$$\hat\delta(\theta) = \frac{1}{n_t}\sum_{i \in \mathcal T}\big(Y_i - \theta(X_i - \bar x)\big) - \frac{1}{n_c}\sum_{i \in \mathcal C}\big(Y_i - \theta(X_i - \bar x)\big).$$

**Lemma 1 (the form of the estimate).** $\hat\delta(\theta) = (\bar y_t - \bar y_c) - \theta(\bar x_t - \bar x_c)$.

*Proof.* The mean of $Y_i - \theta(X_i - \bar x)$ over $\mathcal T$ is $\bar y_t - \theta\bar x_t + \theta\bar x$, and over $\mathcal C$ it is $\bar y_c - \theta\bar x_c + \theta\bar x$. The $\theta\bar x$ terms cancel in the difference. $\square$

So centring by $\bar x$ does not change $\hat\delta$; it only keeps the adjusted values on the scale of $Y$, which makes the per-arm means readable.

## Unbiased under randomization

**Theorem 2 (fixed theta).** Take the finite population view: each unit has fixed potential outcomes $Y_i(1), Y_i(0)$ and a fixed $X_i$, and the treated set is a uniformly random subset of size $n_t$ (complete randomization). Let $\tau = \frac1n\sum_i(Y_i(1) - Y_i(0))$. If $\theta$ does not depend on the assignment, then $\mathbb{E}[\hat\delta(\theta)] = \tau$.

*Proof.* Each unit is treated with probability $n_t/n$, so $\mathbb{E}[\bar y_t] = \frac{1}{n_t}\sum_i \frac{n_t}{n}Y_i(1) = \frac1n\sum_i Y_i(1)$, and in the same way $\mathbb{E}[\bar y_c] = \frac1n\sum_i Y_i(0)$ and $\mathbb{E}[\bar x_t] = \mathbb{E}[\bar x_c] = \bar x$. By Lemma 1 and linearity, $\mathbb{E}[\hat\delta(\theta)] = \tau - \theta\cdot 0$. $\square$

The covariate must be measured before the treatment starts. If the treatment can change $X$, then $X_i$ is not fixed in the sense of the theorem, and $\mathbb{E}[\bar x_t - \bar x_c]$ is the effect of the treatment on $X$, which leaks into $\hat\delta$.

**Theorem 3 (pooled theta under the sharp null).** If $Y_i(1) = Y_i(0)$ for every unit, the pooled coefficient $\hat\theta = \sum_i(X_i - \bar x)(Y_i - \bar y)/\sum_i(X_i - \bar x)^2$ does not depend on the assignment, and $\mathbb{E}[\hat\delta(\hat\theta)] = 0$.

*Proof.* Under the sharp null the observed $Y_i$ equals $Y_i(0)$ whatever the assignment, and $\hat\theta$ uses all units without their arm labels. So $\hat\theta$ is a constant, and Theorem 2 applies with $\tau = 0$. $\square$

With a real effect, the pooled $\hat\theta$ and the within-arm $\hat\theta$ both depend on the assignment, and $\mathbb{E}[\hat\delta(\hat\theta)] = \tau - \mathbb{E}[\hat\theta(\bar x_t - \bar x_c)]$, which is not 0 in general. The tests find a population of 6 units where the mean over all 20 assignments differs from $\tau$. Freedman (2008) shows the bias is of order $1/n$; it is not proved here.

## The variance

**Theorem 4 (the best coefficient).** Let $X$ and $Y$ be random variables with finite variances, $\operatorname{Var}(X) > 0$, and correlation $\rho$. Then $\operatorname{Var}(Y - \theta X)$ is smallest at $\theta^* = \operatorname{Cov}(X, Y)/\operatorname{Var}(X)$, and

$$\operatorname{Var}(Y - \theta^* X) = \operatorname{Var}(Y)(1 - \rho^2).$$

The same identity holds for sample moments: with $s_{xx}, s_{yy}, s_{xy}$ the sums of squares and cross products about the means, and $\hat\theta = s_{xy}/s_{xx}$, the sum of squares of $Y_i - \hat\theta X_i$ about its mean is $s_{yy}(1 - s_{xy}^2/(s_{xx}s_{yy}))$.

*Proof.* $\operatorname{Var}(Y - \theta X) = \operatorname{Var}(Y) - 2\theta\operatorname{Cov}(X, Y) + \theta^2\operatorname{Var}(X)$, a quadratic in $\theta$ with positive leading coefficient, smallest where its derivative $-2\operatorname{Cov}(X, Y) + 2\theta\operatorname{Var}(X)$ is 0. Putting $\theta^*$ in gives $\operatorname{Var}(Y) - \operatorname{Cov}(X, Y)^2/\operatorname{Var}(X) = \operatorname{Var}(Y)(1 - \rho^2)$, since $\rho^2 = \operatorname{Cov}(X, Y)^2/(\operatorname{Var}(X)\operatorname{Var}(Y))$. The sample version is the same algebra with $s_{xx}, s_{yy}, s_{xy}$ in place of the moments. $\square$

**Theorem 5 (the variance of the estimate).** Take the sampling view: the units of each arm are independent, the treated units are draws of $(X, Y(1))$ and the control units are draws of $(X, Y(0))$ from one population, so $X$ has the same law in both arms. Let $\sigma_a^2 = \operatorname{Var}(Y(a))$, $c_a = \operatorname{Cov}(X, Y(a))$ and $v = \operatorname{Var}(X) > 0$. For a fixed $\theta$,

$$\operatorname{Var}(\hat\delta(\theta)) = \frac{\sigma_1^2 - 2\theta c_1 + \theta^2 v}{n_t} + \frac{\sigma_0^2 - 2\theta c_0 + \theta^2 v}{n_c}.$$

It is smallest at $\theta^* = (c_1/n_t + c_0/n_c)/(v(1/n_t + 1/n_c))$. If $c_1 = c_0$ and $\sigma_1 = \sigma_0$, which holds for example when the effect is the same for every unit, the smallest value is $(1 - \rho^2)$ times the variance of $\bar y_t - \bar y_c$, where $\rho$ is the correlation of $X$ and $Y(0)$.

*Proof.* By Lemma 1, $\hat\delta(\theta)$ is the difference of the arm means of $Y_i - \theta X_i$; the two arms are independent and each mean averages independent terms, so the variance is the sum of $\operatorname{Var}(Y(a) - \theta X)/n_a$, and each of these expands as in Theorem 4. The sum is a quadratic in $\theta$ with leading coefficient $v(1/n_t + 1/n_c) > 0$, smallest at $\theta^*$. If $c_1 = c_0 = c$ and $\sigma_1 = \sigma_0 = \sigma$, then $\theta^* = c/v$, and each arm term is $\sigma^2(1 - \rho^2)/n_a$ by Theorem 4, while the unadjusted variance is $\sigma^2(1/n_t + 1/n_c)$. $\square$

When $c_1 \ne c_0$, the pooled coefficient estimates a weighted slope that need not be $\theta^*$, and the variance can even rise when the arm sizes differ. This is the case that Freedman (2008) studied; Lin (2013) shows that fitting a separate slope in each arm removes the problem in large samples. The plug-in variance that CUPED reports (line L5) treats $\hat\theta$ as fixed; its validity in large samples is cited from Deng et al. (2013) and Lin (2013).

## The within-arm coefficient is ANCOVA

**Theorem 6.** Let $\hat\theta_w = \big(\sum_{\mathcal T}(X_i - \bar x_t)(Y_i - \bar y_t) + \sum_{\mathcal C}(X_i - \bar x_c)(Y_i - \bar y_c)\big)/\big(\sum_{\mathcal T}(X_i - \bar x_t)^2 + \sum_{\mathcal C}(X_i - \bar x_c)^2\big)$, with a positive denominator. In the least squares fit of $Y$ on $(1, T, X)$, the coefficient of $X$ is $\hat\theta_w$ and the coefficient of $T$ is $\hat\delta(\hat\theta_w)$.

*Proof.* Let $(a, b, g)$ be the coefficients of $(1, T, X)$ and $r_i = Y_i - a - bT_i - gX_i$ the residuals. The normal equations for the columns $1$ and $T$ say $\sum_i r_i = 0$ and $\sum_{\mathcal T} r_i = 0$, so the residuals sum to 0 in each arm:

$$\bar y_t = a + b + g\bar x_t, \qquad \bar y_c = a + g\bar x_c.$$

Subtracting, $b = (\bar y_t - \bar y_c) - g(\bar x_t - \bar x_c) = \hat\delta(g)$ by Lemma 1. Substituting $a + bT_i = \bar y_{(i)} - g\bar x_{(i)}$, where $(i)$ is the arm of unit $i$, gives $r_i = (Y_i - \bar y_{(i)}) - g(X_i - \bar x_{(i)})$. The normal equation for the column $X$, $\sum_i X_ir_i = 0$, becomes $\sum_i (X_i - \bar x_{(i)})r_i = 0$ because $\sum_{\text{arm}} r_i = 0$ in each arm. That is $\sum_i (X_i - \bar x_{(i)})(Y_i - \bar y_{(i)}) = g\sum_i (X_i - \bar x_{(i)})^2$, so $g = \hat\theta_w$. The denominator is positive, so the design has full rank and the solution is unique. $\square$

## What is proved and what is measured

Proved here: the form of the estimate (Lemma 1), exact unbiasedness over the randomization for any coefficient fixed in advance (Theorem 2) and for the pooled coefficient under the sharp null (Theorem 3), the factor $1 - \rho^2$ for the best coefficient (Theorems 4 and 5), and the equality with the ANCOVA coefficient (Theorem 6). The tests check Lemma 1 and Theorems 2, 3, 4 and 6 exactly with fractions. Not proved: that the estimated coefficient changes the large-sample distribution by a negligible amount and that the interval has its nominal level; these come from Deng et al. (2013) and Lin (2013). The variance ratio 0.360 and the coverage on the page are measured in a simulation.
