---
title: The perturbed observation EnKF gives the Kalman mean and, in expectation, the Kalman covariance of the sample prior
proves: [correctness, termination]
status: full
---

**Setting.** There are $N \ge 2$ forecast members $x_1, \ldots, x_N \in \mathbb R^n$ with mean $\bar x$, unscaled perturbations $X$ ($n \times N$, column $i$ is $x_i - \bar x$) and sample covariance $P = XX^\top/(N - 1)$. The observations are $y^o \in \mathbb R^p$ with a linear operator $H$ and a symmetric positive definite error covariance $R$. There is no localization until the remarks. The Kalman values for the sample prior are

$$K = PH^\top(HPH^\top + R)^{-1}, \qquad \bar x^a = \bar x + K(y^o - H\bar x), \qquad P^a = (I - KH)P.$$

The perturbations $\varepsilon_1, \ldots, \varepsilon_N$ of line L4 have the mean $\bar\varepsilon$, the centred values $e_i = \varepsilon_i - \bar\varepsilon$ (columns of $E$) and the sample covariance $C = EE^\top/(N - 1)$.

**Lemma 1 (the gain).** For a linear $H$, line L3 computes $PH^\top$ and $HPH^\top$, so the matrix used in line L7 is the Kalman gain $K$ of the sample prior.

*Proof.* Line L1 gives $y_i = Hx_i$, so $\bar y = H\bar x$ and $Y = HX$. Then $XY^\top/(N - 1) = XX^\top H^\top/(N - 1) = PH^\top$ and $YY^\top/(N - 1) = HPH^\top$. Lines L5 and L7 use $PH^\top S^{-1}$ with $S = HPH^\top + R$. $\square$

**Lemma 2 (members, mean and perturbations).** The analysis members are $x^a_i = x_i + K(y^o + \varepsilon_i - Hx_i)$. Their mean is $\bar x^a + K\bar\varepsilon$ and their perturbations are

$$X^a = (I - KH)X + KE.$$

*Proof.* Lines L6 and L7 give the first formula. Average it over $i$ to get $\bar x + K(y^o + \bar\varepsilon - H\bar x) = \bar x^a + K\bar\varepsilon$. Subtract the mean from each member to get column $i$ of $X^a$: $(x_i - \bar x) - KH(x_i - \bar x) + K e_i$. $\square$

**Theorem 3 (Burgers, van Leeuwen and Evensen 1998).** Let the forecast ensemble be fixed and let $\varepsilon_1, \ldots, \varepsilon_N$ be independent draws of $N(0, R)$. Then the expected analysis mean is $\bar x^a$ and the expected sample covariance of the analysis is $P^a$.

*Proof.* $K$ depends only on the forecast ensemble, so it is fixed. $E[\bar\varepsilon] = 0$ gives the mean by Lemma 2. By Lemma 2 the sample covariance is

$$\frac{X^aX^{a\top}}{N - 1} = (I - KH)P(I - KH)^\top + KCK^\top + \frac{(I - KH)XE^\top K^\top + KEX^\top(I - KH)^\top}{N - 1}.$$

The centred sample covariance of $N$ independent draws is unbiased, so $E[C] = R$. Each entry of $E$ has mean zero and $X$ is fixed, so the last term has mean zero. Hence the expectation is $(I - KH)P(I - KH)^\top + KRK^\top$. Expand it and use $K(HPH^\top + R) = PH^\top$:

$$(I - KH)P - (I - KH)PH^\top K^\top + KRK^\top = (I - KH)P - PH^\top K^\top + K(HPH^\top + R)K^\top = (I - KH)P. \quad\square$$

**Corollary 4 (without perturbations the spread is too small).** If $\varepsilon_i = 0$ for every member, the analysis covariance is $(I - KH)P(I - KH)^\top = P^a - KRK^\top$, which is smaller than $P^a$ by the positive semidefinite matrix $KRK^\top$. This is why the observations must be perturbed (Burgers et al. 1998).

**Corollary 5 (exact perturbations).** If $\bar\varepsilon = 0$, $C = R$ and $XE^\top = 0$, then the analysis has exactly the mean $\bar x^a$ and the covariance $P^a$. This follows from the formula in the proof of Theorem 3 without the expectation.

With $x = (-1, 1)$, $H = 1$, $R = 1$, $y^o = 1$ and $\varepsilon = (-1/2, 1/2)$, $P = 2$ and $K = 2/3$, and the members are $0$ and $4/3$. The mean is $2/3$, which is the Kalman mean because $\bar\varepsilon = 0$, but the variance is $8/9$ instead of $P^a = 2/3$, because $C = 1/2$ and $XE^\top = 1 \ne 0$. With three members $-1, 0, 1$ and $\varepsilon = c(1, -2, 1)$, $c = \sqrt{R/3}$, the conditions of Corollary 5 hold and the result is exact.

**Large ensembles.** For a linear model and Gaussian data, Mandel, Cobb and Beezley (2011) prove that the EnKF members converge in $L^p$ to the Kalman filter as $N \to \infty$. This is cited, not proved here.

**Remark (localization).** If $H$ picks state values at the positions $q_1, \ldots, q_p$, and the weights are $\rho(j, q_k)$ in $\mathrm{loc}_{xy}$ and $\rho(q_k, q_l)$ in $\mathrm{loc}_{yy}$ for a weight matrix $\rho$ on the grid, then line L3 computes $(\rho\circ P)H^\top$ and $H(\rho\circ P)H^\top$, where $\circ$ is the entrywise product. So the gain is the Kalman gain of the localized covariance $\rho\circ P$. For other operators the localized gain is a heuristic.

**A nonlinear $H$.** Line L3 then uses the sample covariances of the state and the predicted observations. Lemma 1 no longer holds, and the update is the usual heuristic of the ensemble filters.

**Termination.** Line L1 makes $N$ calls of $h$. $HPH^\top$ is positive semidefinite and $R$ is positive definite, so $S$ is positive definite and line L7 can solve with it. With localization $S$ stays positive definite if the weight matrix of the observations is positive semidefinite, by the Schur product theorem. The loop of line L7 runs $N$ times, and the algorithm returns at line L8. $\blacksquare$
