---
title: The IPW estimates are unbiased with known propensities and equal the stratified estimate with empirical ones
proves: [correctness]
status: full
---

Unit $i$ has treatment $T_i \in \{0, 1\}$, outcome $Y_i$ and propensity $e_i$ with $0 < e_i < 1$. Write $\psi_i = T_iY_i/e_i - (1 - T_i)Y_i/(1 - e_i)$. All arithmetic is exact.

**Lemma 1 (the loops).** IPW-ATE returns $\hat\tau_{\mathrm{HT}} = \frac1n\sum_i \psi_i$ and $\hat\tau_{\mathrm{H}} = a_1/w_1 - a_0/w_0$, with $a_1 = \sum_i T_iY_i/e_i$, $w_1 = \sum_i T_i/e_i$, $a_0 = \sum_i (1 - T_i)Y_i/(1 - e_i)$ and $w_0 = \sum_i (1 - T_i)/(1 - e_i)$.

*Proof.* Line L1 sets the four sums to 0. The loop L2 visits each unit once. Line L3 does not change the sums. For a treated unit, line L4 adds $Y_i/e_i$ to $a_1$ and $1/e_i$ to $w_1$, which are the terms $T_iY_i/e_i$ and $T_i/e_i$; the terms of $a_0$ and $w_0$ are 0 for this unit, and line L5 does not run. For a control the roles swap. So after the loop the four sums have the stated values. Line L6 returns $(a_1 - a_0)/n = \frac1n\sum_i\psi_i$, and line L7 returns $a_1/w_1 - a_0/w_0$. $\square$

## Design-based results

Here the potential outcomes $Y_i(1), Y_i(0)$ of $n$ units are fixed numbers, and only the assignment vector $(T_1, \ldots, T_n)$ is random, with a known distribution (the design). Let $\pi_i = \Pr[T_i = 1]$, and assume $0 < \pi_i < 1$ for all $i$. The observed outcome is $Y_i = T_iY_i(1) + (1 - T_i)Y_i(0)$ (consistency). The sample average treatment effect is $\tau_S = \frac1n\sum_i (Y_i(1) - Y_i(0))$.

**Theorem 2 (unbiased for any design).** With $e_i = \pi_i$, $\mathbb{E}[\hat\tau_{\mathrm{HT}}] = \tau_S$.

*Proof.* Since $T_i(1 - T_i) = 0$, consistency gives $T_iY_i = T_iY_i(1)$ and $(1 - T_i)Y_i = (1 - T_i)Y_i(0)$. So $\psi_i = T_iY_i(1)/\pi_i - (1 - T_i)Y_i(0)/(1 - \pi_i)$, in which only $T_i$ is random. With $\mathbb{E}[T_i] = \pi_i$, $\mathbb{E}[\psi_i] = Y_i(1) - Y_i(0)$. By [linearity of expectation](/linearity-of-expectation/) and Lemma 1, $\mathbb{E}[\hat\tau_{\mathrm{HT}}] = \frac1n\sum_i (Y_i(1) - Y_i(0)) = \tau_S$. The proof uses only the marginal probabilities $\pi_i$, so it holds for every joint distribution of the assignment. $\square$

**Theorem 3 (variance under independent assignment).** If the $T_i$ are independent, then
$$\operatorname{Var}[\hat\tau_{\mathrm{HT}}] = \frac{1}{n^2}\sum_{i=1}^n\left(\frac{1 - \pi_i}{\pi_i}Y_i(1)^2 + \frac{\pi_i}{1 - \pi_i}Y_i(0)^2 + 2Y_i(1)Y_i(0)\right).$$

*Proof.* The $\psi_i$ are independent, so $\operatorname{Var}[\hat\tau_{\mathrm{HT}}] = \frac{1}{n^2}\sum_i\operatorname{Var}[\psi_i]$. Write $a = Y_i(1)$, $b = Y_i(0)$ and $\pi = \pi_i$. The variable $\psi_i$ is $a/\pi$ with probability $\pi$ and $-b/(1 - \pi)$ with probability $1 - \pi$, so $\mathbb{E}[\psi_i^2] = a^2/\pi + b^2/(1 - \pi)$ and $\mathbb{E}[\psi_i] = a - b$. Then
$$\operatorname{Var}[\psi_i] = \frac{a^2}{\pi} + \frac{b^2}{1 - \pi} - a^2 + 2ab - b^2 = \frac{1 - \pi}{\pi}a^2 + \frac{\pi}{1 - \pi}b^2 + 2ab. \qquad\square$$

**Theorem 4 (complete randomization).** If every assignment with $P[T] > 0$ treats exactly $n_1$ units, with $0 < n_1 < n$, and $e_i = n_1/n$ for all $i$, then $\hat\tau_{\mathrm{HT}} = \hat\tau_{\mathrm{H}} = \bar Y_1 - \bar Y_0$, the difference of the arm means, for every such assignment.

*Proof.* $w_1 = n_1 \cdot n/n_1 = n$ and $w_0 = (n - n_1)\cdot n/(n - n_1) = n$, so the two forms coincide. And $a_1/n = \frac{n}{n_1}\sum_{T_i = 1}Y_i/n = \bar Y_1$, and in the same way $a_0/n = \bar Y_0$. $\square$

Under complete randomization of $n_1$ of $n$ units, $\pi_i = n_1/n$, so Theorem 2 shows that the difference in means is unbiased for $\tau_S$, the result proved on the [randomized experiment](/randomized-experiment/) page.

## Superpopulation results

Here the units $(X_i, T_i, Y_i(0), Y_i(1))$ are independent copies of $(X, T, Y(0), Y(1))$, with $e(x) = \Pr[T = 1 \mid X = x]$, $e_i = e(X_i)$ and $\mathbb{E}|Y(t)| < \infty$ for $t = 0, 1$. Assume consistency $Y = TY(1) + (1 - T)Y(0)$, ignorability $(Y(0), Y(1)) \perp T \mid X$, and positivity $0 < e(X) < 1$ with probability 1.

**Theorem 5 (identification).** $\mathbb{E}[TY/e(X)] = \mathbb{E}[Y(1)]$ and $\mathbb{E}[(1 - T)Y/(1 - e(X))] = \mathbb{E}[Y(0)]$. Hence $\mathbb{E}[\hat\tau_{\mathrm{HT}}] = \tau = \mathbb{E}[Y(1) - Y(0)]$.

*Proof.* By consistency $TY = TY(1)$. Ignorability gives $T \perp Y(1) \mid X$, so $\mathbb{E}[T\,|Y(1)| \mid X] = \mathbb{E}[T \mid X]\,\mathbb{E}[|Y(1)| \mid X] = e(X)\,\mathbb{E}[|Y(1)| \mid X]$. Since $1/e(X)$ is a function of $X$, by the tower property of [conditional expectation](/conditional-expectation/), $\mathbb{E}[T|Y(1)|/e(X)] = \mathbb{E}[\mathbb{E}[|Y(1)| \mid X]] = \mathbb{E}|Y(1)| < \infty$, so $TY/e(X)$ is integrable. The same steps without absolute values give
$$\mathbb{E}\left[\frac{TY(1)}{e(X)}\right] = \mathbb{E}\left[\frac{\mathbb{E}[T \mid X]\,\mathbb{E}[Y(1) \mid X]}{e(X)}\right] = \mathbb{E}\big[\mathbb{E}[Y(1) \mid X]\big] = \mathbb{E}[Y(1)].$$
Positivity makes the division by $e(X)$ valid with probability 1. The control arm is the same with $1 - T$, $Y(0)$ and $1 - e(X)$. So $\mathbb{E}[\psi_i] = \tau$ for each $i$, and $\mathbb{E}[\hat\tau_{\mathrm{HT}}] = \tau$ by linearity. $\square$

**Theorem 6 (unbiased variance estimate).** If also $\mathbb{E}[\psi^2] < \infty$, then $\operatorname{Var}[\hat\tau_{\mathrm{HT}}] = \operatorname{Var}[\psi]/n$, and $v_{\mathrm{HT}} = S_\psi^2/n$, with $S_\psi^2$ the sample variance of $\psi_1, \ldots, \psi_n$ with divisor $n - 1$ ($n \ge 2$), satisfies $\mathbb{E}[v_{\mathrm{HT}}] = \operatorname{Var}[\hat\tau_{\mathrm{HT}}]$.

*Proof.* The $\psi_i$ are independent and identically distributed, since each is the same function of one unit's data. The variance of their mean is $\operatorname{Var}[\psi]/n$, and the sample variance with divisor $n - 1$ is unbiased for $\operatorname{Var}[\psi]$. $\square$

**Theorem 7 (the Hájek form is consistent).** $\hat\tau_{\mathrm{H}} \to \tau$ with probability 1 as $n \to \infty$.

*Proof.* By Theorem 5 with $Y$ replaced by the constant 1, $\mathbb{E}[T/e(X)] = 1$. By the strong [law of large numbers](/law-of-large-numbers/), $a_1/n \to \mathbb{E}[Y(1)]$ and $w_1/n \to 1$ with probability 1, so $a_1/w_1 = (a_1/n)/(w_1/n) \to \mathbb{E}[Y(1)]$. In the same way $a_0/w_0 \to \mathbb{E}[Y(0)]$. For all large $n$, $w_1 > 0$ and $w_0 > 0$, so line L7 is defined. $\square$

Theorem 7 is a limit statement. It gives no bound on the bias of $\hat\tau_{\mathrm{H}}$ at a fixed $n$, and the coverage of the normal intervals is not proved here.

## Empirical propensities with a discrete covariate

**Theorem 8 (equal to the stratified estimate).** Let $X$ take finitely many values. For each value $x$, let $n_x$ be the number of units with $X_i = x$, $n_{1x}$ the number of those treated, $n_{0x} = n_x - n_{1x}$, and $\bar Y_{1x}$ and $\bar Y_{0x}$ the mean outcomes of the treated and the controls with $X_i = x$. Assume $0 < n_{1x} < n_x$ for every $x$ that occurs. With $\hat e_i = n_{1x}/n_x$ for each unit with $X_i = x$,
$$\hat\tau_{\mathrm{HT}} = \hat\tau_{\mathrm{H}} = \sum_x \frac{n_x}{n}\left(\bar Y_{1x} - \bar Y_{0x}\right).$$
The ATT form $\bar Y_{\text{treated}} - \sum_{T_i = 0}\frac{\hat e_i}{1 - \hat e_i}Y_i \big/ \sum_{T_i = 0}\frac{\hat e_i}{1 - \hat e_i}$ equals $\sum_x \frac{n_{1x}}{n_1}(\bar Y_{1x} - \bar Y_{0x})$, where $n_1 = \sum_x n_{1x}$.

*Proof.* The assumption gives $0 < \hat e_i < 1$. Group the sums by the value of $X$. The treated units with $X_i = x$ contribute $\frac{n_x}{n_{1x}}\sum Y_i = n_x\bar Y_{1x}$ to $a_1$ and $n_{1x}\cdot\frac{n_x}{n_{1x}} = n_x$ to $w_1$. So $a_1 = \sum_x n_x\bar Y_{1x}$ and $w_1 = \sum_x n_x = n$. In the same way, $1/(1 - \hat e_i) = n_x/n_{0x}$ gives $a_0 = \sum_x n_x\bar Y_{0x}$ and $w_0 = n$. Since $w_1 = w_0 = n$, the two forms agree, and both equal $\frac1n\sum_x n_x(\bar Y_{1x} - \bar Y_{0x})$.

For the ATT, a control with $X_i = x$ has weight $\hat e_i/(1 - \hat e_i) = n_{1x}/n_{0x}$. The controls with $X_i = x$ contribute $n_{1x}\bar Y_{0x}$ to the weighted sum and $n_{1x}$ to the sum of weights, so the control term is $\sum_x n_{1x}\bar Y_{0x}/n_1$. The treated mean is $\sum_x n_{1x}\bar Y_{1x}/n_1$. Their difference is the stated sum. $\square$

**Cost.** The loop L2 to L5 runs $n$ times and does a constant number of comparisons, divisions and additions per pass; lines L6 to L8 take constant time. So the time is $\Theta(n)$ in every case, and the extra space is the four sums, $\Theta(1)$. The loop is over a finite range, so the procedure terminates. $\blacksquare$
