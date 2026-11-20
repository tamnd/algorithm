---
title: The EAKF gives exactly the Kalman analysis mean and covariance of the sample prior
proves: [correctness, termination]
status: full
---

**Setting.** There are $N \ge 2$ forecast members $x_1, \ldots, x_N \in \mathbb R^n$ with mean $\bar x$, unscaled perturbations $X$ ($n \times N$, column $i$ is $x_i - \bar x$) and sample covariance $P = XX^\top/(N - 1)$. The observations are $y^o \in \mathbb R^p$ with a linear operator $H$ (rows $h_k$) and an error covariance $R$. The serial form needs $R = \mathrm{diag}(r_k)$ with $r_k > 0$; the joint form needs $R$ symmetric positive definite. There is no localization until the last remark. The Kalman values are $K = PH^\top(HPH^\top + R)^{-1}$, $\bar x^a = \bar x + K(y^o - H\bar x)$ and $P^a = (I - KH)P$.

**Lemma 1 (the step in observation space).** Fix one observation $k$ with $r = r_k$, and let $v_i$ be the predicted values of line L1 with mean $\bar y$ and sample variance $s > 0$ (line L3). Lines L4 and L5 give new values $v_i + \Delta y_i$ with mean $y^a = \bar y + \frac{s}{s + r}(y^o_k - \bar y)$ and sample variance $s^a = \frac{sr}{s + r}$.

*Proof.* Line L4 sets $s^a = (1/s + 1/r)^{-1} = sr/(s + r)$ and $y^a = s^a(\bar y/s + y^o_k/r)$. Since $s^a/s + s^a/r = 1$, this is $y^a = \bar y + (s^a/r)(y^o_k - \bar y)$ with $s^a/r = s/(s + r)$. Line L5 sets $v_i + \Delta y_i = y^a + f(v_i - \bar y)$ with $f = \sqrt{s^a/s}$. The deviations from $y^a$ are $f$ times the old deviations, which sum to zero, so the mean is $y^a$ and the variance is $f^2 s = s^a$. $\square$

These are the mean and the variance of the posterior of a scalar Gaussian prior $N(\bar y, s)$ after one observation with error variance $r$. Note that $f = \sqrt{r/(s + r)}$, which is the number $q$ of the [EnSRF](/ensemble-square-root-filter/) proof.

**Lemma 2 (the serial EAKF step is the serial EnSRF step).** Let $Y_k = h_k X$ be the perturbations of observation $k$ and suppose the predicted observations are $H$ applied to the members. With $K = Ph_k^\top/(s + r)$, $d = y^o_k - h_k\bar x$, $q = \sqrt{r/(s + r)}$ and $\alpha = 1/(1 + q)$, lines L6 and L7 change member $i$ to

$$x_i + K d - \alpha K\, (Y_k)_i,$$

and change the predicted observations by $H$ times the same increments.

*Proof.* Line L6 sets $b_x = X Y_k^\top/((N - 1)s) = Ph_k^\top/s$, the regression coefficients of the state on observation $k$. By Lemma 1, $\Delta y_i = (y^a - \bar y) + (q - 1)(Y_k)_i = \frac{s}{s + r} d + (q - 1)(Y_k)_i$. So $b_x \Delta y_i = K d + \frac{q - 1}{s} P h_k^\top (Y_k)_i$. Now $s = (s + r)(1 - q^2)$, so

$$\frac{q - 1}{s} = -\frac{1 - q}{(s + r)(1 - q)(1 + q)} = -\frac{1}{(s + r)(1 + q)},$$

and the second term is $-\alpha K (Y_k)_i$. Line L7 uses $b_y = YY_k^\top/((N - 1)s)$ with $Y = HX$, which is $H b_x$, so the predicted observations change by $H b_x \Delta y_i$. Both coefficients use the values before the update, as the lines of the code do. $\square$

**Theorem 3 (serial form).** With a linear $H$, a diagonal $R$ and no localization, the serial EAKF returns the same members as the serial EnSRF, so its output has the mean $\bar x^a$ and the sample covariance $P^a$. If $s = 0$ for an observation, the code skips it, which is the Kalman update with $K = 0$.

*Proof.* By Lemma 2 each pass of the loop of line L2 makes the EnSRF update of lines L8 and L9 of the EnSRF, and keeps the predicted observations equal to $H$ applied to the members. Theorem 3 of the [EnSRF proof](/ensemble-square-root-filter/) says that the serial EnSRF ends with the Kalman mean and covariance. If $s = 0$, then $Y_k = 0$, so $h_k P h_k^\top = 0$, $Ph_k^\top = 0$ ($P$ is positive semidefinite) and $K = 0$. $\square$

**Lemma 4 (the adjustment matrix).** Let $P = F D F^\top$ where $F$ ($n \times m$) has orthonormal columns and $D = \mathrm{diag}(d_1, \ldots, d_m)$ holds the positive eigenvalues (line J2). Put $G = D^{1/2}$, $Z = FG$, $B = HZ$ and $M = B^\top R^{-1} B = U\Lambda U^\top$ (line J3), and

$$A = Z\, U (I + \Lambda)^{-1/2} U^\top\, G^{-1} F^\top \quad\text{(line J4)}.$$

Then $A P A^\top = P^a$.

*Proof.* $P = ZZ^\top$ and $F^\top F = I$, so $G^{-1}F^\top P F G^{-1} = G^{-1} D G^{-1} = I$. With $C = U(I + \Lambda)^{-1/2}U^\top$, which is symmetric, $APA^\top = Z C C Z^\top = Z U (I + \Lambda)^{-1} U^\top Z^\top = Z (I + M)^{-1} Z^\top$. On the other side,

$$P^a = ZZ^\top - Z B^\top (BB^\top + R)^{-1} B Z^\top = Z\bigl(I - B^\top (BB^\top + R)^{-1} B\bigr) Z^\top,$$

and the Woodbury identity gives $I - B^\top(BB^\top + R)^{-1}B = (I + B^\top R^{-1} B)^{-1} = (I + M)^{-1}$. $\square$

$G$ is invertible because only positive eigenvalues are kept. Anderson (2001, Appendix A) gives this matrix with singular value decompositions, and Grooms (2020) discusses the case where $P$ is singular, which is the usual case with $N \le n$.

**Theorem 5 (joint form).** For a linear $H$ and a symmetric positive definite $R$, the members $x^a_i = \bar x^a + A(x_i - \bar x)$ of line J6 have the mean $\bar x^a$ and the sample covariance $P^a$.

*Proof.* Line J5 computes $\bar x^a = \bar x + PH^\top z$ with $(HPH^\top + R) z = y^o - H\bar x$, which is the Kalman mean. The new perturbations are $AX$. Their columns sum to $A$ times the sum of the columns of $X$, which is zero, so the mean is $\bar x^a$. Their sample covariance is $AXX^\top A^\top/(N - 1) = APA^\top = P^a$ by Lemma 4. $\square$

**Corollary 6 (one scalar observation).** If $p = 1$, the joint form gives the same members as the serial form.

*Proof.* With $H = h$ (one row) and $R = r$, $B = hZ$ is one row, and $M = B^\top B/r$ has the single positive eigenvalue $BB^\top/r = hPh^\top/r = s/r$ with the unit eigenvector $u = B^\top/\|B\|$ (if $s = 0$, then $M = 0$, $A = FF^\top$ and $AX = X$, which is the skipped update). So $C = I + (q - 1)uu^\top$ with $q = (1 + s/r)^{-1/2} = \sqrt{r/(s + r)}$, and

$$A = ZG^{-1}F^\top + (q - 1)\frac{Z B^\top B G^{-1}F^\top}{s} = FF^\top + \frac{q - 1}{s} P h^\top h FF^\top,$$

because $ZB^\top = ZZ^\top h^\top = Ph^\top$ and $BG^{-1}F^\top = hFF^\top$. The columns of $X$ lie in the range of $P$, which is the range of $F$, so $FF^\top X = X$ and $AX = X + \frac{q - 1}{s} Ph^\top hX = X - \alpha K hX$ by the identity in the proof of Lemma 2. The mean is the Kalman mean in both forms, so the members agree. $\square$

For more than one observation the joint and the serial members differ in general. The covariance of the analysis fixes the perturbations only up to an orthogonal transform in ensemble space (Tippett et al. 2003), and the two forms make different choices.

With $N = 2$, $x = (-1/\sqrt 2, 1/\sqrt 2)$, $h = 1$, $r = 1$ and $y^o = 1$, $s = 1$, $s^a = 1/2$ and $y^a = 1/2$, so both forms return the mean $1/2$ and the variance $1/2$.

**With localization.** If the weights multiply $b_x$ and $b_y$ entry by entry, the proof of Lemma 2 still shows that the serial EAKF makes the same step as the serial EnSRF with the same weights on its gain. The step is then no longer an exact Kalman update, as the EnSRF proof explains, and its use is a heuristic.

**A nonlinear $H$.** The serial form evaluates $h$ only at line L1 and then updates the predicted observations by regression. The theorems above do not cover this case. Anderson (2003) describes it as a least squares fit of each state value on each observed value.

**Termination.** The serial form makes $p$ passes of a finite number of sums over $N$ members. It skips an observation with $s = 0$, so line L4 divides only by $s > 0$ and $r > 0$, and line L6 by $(N - 1)s > 0$. The joint form calls the Jacobi method twice with a fixed upper limit on the number of sweeps, and solves two linear systems with $R$ and $HPH^\top + R$, which are positive definite. Both forms return. $\blacksquare$
