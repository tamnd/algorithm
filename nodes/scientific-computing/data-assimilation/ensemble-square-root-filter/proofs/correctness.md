---
title: The serial EnSRF gives exactly the Kalman analysis mean and covariance of the sample prior
proves: [correctness, termination]
status: full
---

**Setting.** There are $N \ge 2$ forecast members $x_1, \ldots, x_N \in \mathbb R^n$ and $p$ observations $y^o_k = h_k x^t + \varepsilon_k$ with a linear operator $H$ (rows $h_k$) and independent errors of variances $r_k > 0$, so $R = \mathrm{diag}(r_k)$. $X$ ($n \times N$) holds the unscaled perturbations and $P = X X^\top/(N - 1)$ is the sample covariance. $Y$ ($p \times N$) holds the perturbations of the predicted observations (line L1). There is no localization in Lemmas 1 to 3.

**Lemma 1 (one scalar observation).** Let $h = h_k$, $Y_k = h X$, $s = h P h^\top$ (line L3), $K = P h^\top/(s + r)$ (lines L4 and L5), $q = \sqrt{r/(s + r)}$ and $\alpha = 1/(1 + q)$ (line L6). Lines L8 and L9 give a new mean $\bar x + K(y^o_k - h\bar x)$ and new perturbations $X' = (I - \alpha K h)X$ with

$$\frac{X' X'^\top}{N - 1} = (I - K h) P.$$

*Proof.* The sample covariance of $Y_k$ and $X$ is $X Y_k^\top/(N - 1) = P h^\top$, so line L5 is the scalar Kalman gain and line L8 the Kalman mean. Line L9 is $X' = X - \alpha K h X$. Then

$$\frac{X'X'^\top}{N - 1} = P - \alpha K h P - \alpha P h^\top K^\top + \alpha^2 K s K^\top = P - \bigl(2\alpha (s + r) - \alpha^2 s\bigr) K K^\top,$$

because $K h P = P h^\top h P/(s + r) = (s + r) K K^\top$ and also $P h^\top K^\top = (s + r)KK^\top$. The Kalman covariance is $(I - Kh)P = P - (s + r) K K^\top$. The two agree if $\alpha^2 s - 2\alpha(s + r) + (s + r) = 0$. Write $s = (s + r)(1 - q^2)$ and divide by $s + r$: the condition is $\alpha^2(1 - q^2) - 2\alpha + 1 = 0$, that is $((1 + q)\alpha - 1)((1 - q)\alpha - 1) = 0$, and $\alpha = 1/(1 + q)$ is a root. If $s = 0$ then $K = 0$ and both sides equal $P$. $\square$

The other root $\alpha = 1/(1 - q)$ also gives the right covariance, but it is larger than $1$ and flips the sign of the observed part of the perturbations. The root of line L6 lies in $[1/2, 1)$.

**Lemma 2 (the observation ensemble stays consistent).** After each pass of the loop of line L2, the predicted observation ensemble equals $H$ applied to the state ensemble: $\bar y = H \bar x$ and $Y = H X$.

*Proof.* It holds after line L1. If it holds before a pass, then the vector of lines L4 and L5 for the observations is $K_y = Y Y_k^\top/((N - 1)(s + r)) = H X Y_k^\top/((N - 1)(s + r)) = H K$. So lines L8 and L9 change $\bar y$ by $H K d$ and $Y$ by $-\alpha H K Y_k$, which is $H$ times the change of $\bar x$ and of $X$. $\square$

**Theorem 3 (serial equals batch).** With a diagonal $R$, a linear $H$ and no localization, the output ensemble has the mean $\bar x + K(y^o - H\bar x)$ and the sample covariance $(I - KH)P$, with the batch gain $K = P H^\top (H P H^\top + R)^{-1}$.

*Proof.* Let $\xi \sim N(\bar x, P)$, a Gaussian vector ($P$ may be singular), and $z_k = h_k \xi + e_k$ with independent $e_k \sim N(0, r_k)$. For a Gaussian prior and a linear observation with positive definite noise covariance, the Kalman formulas give the mean and the covariance of the conditional distribution of $\xi$ given the data. By Lemma 1 and Lemma 2, after the pass for observation $k$ the ensemble mean and covariance are the moments of $\xi$ given $z_1 = y^o_1, \ldots, z_k = y^o_k$: the conditional distribution given the first $k - 1$ values is Gaussian with the moments before the pass, and $z_k$ is a linear observation of it with noise independent of the earlier ones. After the last pass these are the moments of $\xi$ given all of $z$, which are the batch Kalman mean and covariance. These moments do not depend on $\xi$ being Gaussian: they are a function of $\bar x$, $P$, $H$, $R$ and $y^o$ only. $\square$

With $N = 2$, $x = (-1/\sqrt 2, 1/\sqrt 2)$, $h = 1$, $r = 1$ and $y^o = 1$, $s = 1$, $K = 1/2$, and the ensemble has the mean $1/2$ and the variance $1/2$.

**Corollary 4.** The analysis members lie in $\bar x^a + \mathrm{range}(X)$, because every pass multiplies $X$ on the left by $I - \alpha K h$ and $K$ lies in the range of $P$, which is the range of $X$.

**With localization.** If the weights multiply $K$ entry by entry, Lemma 1 becomes a statement about $\rho_k \circ K$ and is no longer exact: the perturbations of the state change by $-\alpha(\rho_k\circ K) Y_k$, which is not the square root update of a localized covariance in general, and Lemma 2 fails because $K_y \ne H(\rho_k \circ K)$. The serial order then matters a little. The use of localization is a heuristic whose value is measured, not proved.

**Termination.** The loop of line L2 makes $p$ passes, and each pass is a finite number of sums over $N$ members. Line L6 divides by $1 + q \ge 1$ and line L5 by $s + r \ge r > 0$, so no step fails. The algorithm returns at line L10. $\blacksquare$
