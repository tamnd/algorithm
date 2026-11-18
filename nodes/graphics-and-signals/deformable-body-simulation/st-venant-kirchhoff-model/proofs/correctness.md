---
title: The St. Venant-Kirchhoff stress is the gradient of its energy, is objective and isotropic, has the linear limit, and weakens and reverses under strong compression
proves: [correctness]
status: full
---

The code works in $\mathbb R^d$ with $d = 2$ or 3.
For a matrix $F$ it computes $E = \frac12(F^TF - I)$, $\Psi(F) = \mu\lvert E\rvert_F^2 + \frac\lambda2(\operatorname{tr}E)^2$, $S = 2\mu E + \lambda\operatorname{tr}(E)I$ and $P = FS$.
$A : B = \operatorname{tr}(A^TB)$ is the Frobenius inner product.
All claims are about exact arithmetic.

## Step 1: $P = \partial\Psi/\partial F$

For a change $dF$, $dE = \frac12(dF^TF + F^TdF)$, the symmetric part of $F^TdF$.
Then $d\Psi = 2\mu E : dE + \lambda\operatorname{tr}(E)\operatorname{tr}(dE) = S : dE$.
$S$ is symmetric, and a symmetric matrix has a zero inner product with every antisymmetric one, so $S : dE = S : F^TdF = FS : dF$.
So $d\Psi = P : dF$ with $P = FS$.
No step uses $\det F > 0$, so this holds for every $F$, also for flat and inverted ones. $\square$

## Step 2: the element forces are minus the gradient of the element energy

For a linear element with the rest edge matrix $D_m$, the rest measure $V_0 = \det D_m/d!$ and the current edge matrix $D_s$, the code uses $F = D_sD_m^{-1}$ and $W = V_0\Psi(F)$.
By Step 1, $dW = V_0P : dD_sD_m^{-1} = V_0PD_m^{-T} : dD_s$.
Column $k$ of $D_s$ is $x_k - x_0$, so $\partial W/\partial x_k$ is column $k$ of $V_0PD_m^{-T}$ for $k = 1, \dots, d$, and $\partial W/\partial x_0$ is minus their sum.
The code returns minus these vectors, so the forces are $-\partial W/\partial x$ and they sum to zero. $\square$

## Step 3: objectivity, isotropy and no torque

For a rotation $Q$, $(QF)^T(QF) = F^TF$, so $E(QF) = E(F)$ and $\Psi(QF) = \Psi(F)$; also $S(QF) = S(F)$ and $P(QF) = QFS = QP(F)$.
For the rest side, $(FQ)^T(FQ) = Q^TF^TFQ$, so $E(FQ) = Q^TE(F)Q$, which has the same Frobenius norm and the same trace; so $\Psi(FQ) = \Psi(F)$.
$PF^T = FSF^T$ is symmetric because $S$ is, so the forces of an element have no net torque. $\square$

## Step 4: the rest state, rigid motions and mirror images

If $F^TF = I$, then $E = 0$, $S = 0$, $P = 0$ and $\Psi = 0$.
This includes $F = I$, every rotation, and every reflection such as $\operatorname{diag}(-1, 1, 1)$.
So a mirror image of the rest shape has zero energy and zero stress: it is a second rest state. $\square$

## Step 5: the linear limit

Let $F = I + \varepsilon H$.
Then $E = \varepsilon\operatorname{sym}H + \frac{\varepsilon^2}2H^TH$ with $\operatorname{sym}H = \frac12(H + H^T)$, so $S = \varepsilon(2\mu\operatorname{sym}H + \lambda\operatorname{tr}(H)I) + O(\varepsilon^2)$ and
$$P = (I + \varepsilon H)S = \varepsilon\bigl(2\mu\operatorname{sym}H + \lambda\operatorname{tr}(H)I\bigr) + O(\varepsilon^2).$$
So $P(I + \varepsilon H)/\varepsilon$ differs from the linear stress by $O(\varepsilon)$, and $\mu$ and $\lambda$ are the Lamé parameters of the linear limit. $\square$

## Step 6: the bar under compression

Let $F = \operatorname{diag}(s, 1, 1)$.
Then $E = \operatorname{diag}(\frac{s^2 - 1}2, 0, 0)$, so $\lvert E\rvert_F^2 = (\operatorname{tr}E)^2 = \frac{(s^2 - 1)^2}4$ and
$$\Psi = \Bigl(\mu + \frac\lambda2\Bigr)\frac{(s^2 - 1)^2}4.$$
$S_{xx} = (2\mu + \lambda)\frac{s^2 - 1}2$ and $S_{yy} = S_{zz} = \lambda\frac{s^2 - 1}2$, so $P_{xx} = sS_{xx} = c(s^3 - s)$ with $c = \mu + \frac\lambda2 > 0$, and $P_{yy} = P_{zz} = S_{yy}$.
This $P_{xx}$ is also $d\Psi/ds$.

- For $0 < s < 1$, $s^3 - s < 0$, so $P_{xx} < 0$: the stress pushes the bar back toward $s = 1$.
- $dP_{xx}/ds = c(3s^2 - 1)$ is zero on $(0, 1)$ only at $s = 1/\sqrt3$, negative before it and positive after it. So the size of the compressive stress grows as $s$ falls from 1 to $1/\sqrt3$, has its largest value $2c/(3\sqrt3)$ there, and then falls to zero at $s = 0$.
- For $-1 < s < 0$, $s^3 - s = s(s^2 - 1) > 0$, so $P_{xx} > 0$. The force $-dW/ds$ is negative, so it pushes $s$ toward $-1$, the mirror image of Step 4, and not back toward $s = 1$.
- $d^2\Psi/ds^2 = c(3s^2 - 1) < 0$ for $\lvert s\rvert < 1/\sqrt3$, so $\Psi$ is not convex along this line, and so not convex in $F$. $\blacksquare$
