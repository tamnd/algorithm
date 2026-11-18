---
title: The neo-Hookean stress is the gradient of its energy for J > 0, is objective and isotropic, has the Lamé parameters as its linear limit, and has a barrier at J = 0
proves: [correctness]
status: full
---

The code works in $\mathbb R^d$ with $d = 2$ or 3.
For a matrix $F$ with $J = \det F > 0$ it computes $I_1 = \operatorname{tr}(F^TF) = \lvert F\rvert_F^2$,
$$\Psi(F) = \frac\mu2(I_1 - d) - \mu\log J + \frac\lambda2(\log J)^2, \qquad P = \mu(F - F^{-T}) + \lambda\log(J)F^{-T},$$
and it raises an error for $J \le 0$.
$A : B = \operatorname{tr}(A^TB)$ is the Frobenius inner product, and all claims are about exact arithmetic.

## Step 1: $P = \partial\Psi/\partial F$ for $J > 0$

$dI_1 = 2F : dF$.
By Jacobi's formula, $dJ = J\operatorname{tr}(F^{-1}dF) = JF^{-T} : dF$, so $d\log J = F^{-T} : dF$.
So $d\Psi = \mu F : dF - \mu F^{-T} : dF + \lambda\log(J)F^{-T} : dF = P : dF$. $\square$

## Step 2: the element forces

As for every energy density of $F$, with $F = D_sD_m^{-1}$ and $W = V_0\Psi(F)$, $dW = V_0PD_m^{-T} : dD_s$.
So the gradient for vertex $k = 1, \dots, d$ is column $k$ of $V_0PD_m^{-T}$, the gradient for vertex 0 is minus their sum, and the code returns minus these vectors. $\square$

## Step 3: objectivity, isotropy and no torque

For a rotation $Q$, $\lvert QF\rvert_F = \lvert FQ\rvert_F = \lvert F\rvert_F$ and $\det(QF) = \det(FQ) = \det F$, so $\Psi(QF) = \Psi(FQ) = \Psi(F)$.
$(QF)^{-T} = Q^{-T}F^{-T} = QF^{-T}$, so $P(QF) = QP(F)$.
$PF^T = \mu(FF^T - I) + \lambda\log(J)I$ is symmetric, so the element forces have no net torque. $\square$

## Step 4: the rest state and rotations

For a rotation $Q$, $I_1 = d$, $J = 1$ and $Q^{-T} = Q$, so $\Psi(Q) = 0$ and $P(Q) = \mu(Q - Q) = 0$.
This includes $F = I$.
Without the term $-\mu\log J$, the energy $\frac\mu2(I_1 - 3) + \frac\lambda2(J - 1)^2$ in 3D has the stress $\mu F + \lambda(J - 1)\operatorname{cof}F$, which is $\mu I \ne 0$ at $F = I$: the rest shape is not in equilibrium.
The term $-\mu\log J$ has the gradient $-\mu F^{-T}$, which is $-\mu I$ at rest and cancels it. $\square$

## Step 5: the linear limit

Let $F = I + \varepsilon H$.
Then $F^{-T} = I - \varepsilon H^T + O(\varepsilon^2)$ and $\log J = \varepsilon\operatorname{tr}H + O(\varepsilon^2)$, so
$$P = \mu\bigl(\varepsilon H + \varepsilon H^T\bigr) + \lambda\varepsilon\operatorname{tr}(H)I + O(\varepsilon^2) = \varepsilon\bigl(2\mu\operatorname{sym}H + \lambda\operatorname{tr}(H)I\bigr) + O(\varepsilon^2).$$
So $\mu$ and $\lambda$ are the Lamé parameters of the linear limit, with no remap. $\square$

## Step 6: the bar and the barrier

Let $F = \operatorname{diag}(s, 1, 1)$ with $s > 0$, so $I_1 = s^2 + 2$ and $J = s$.
Then $\Psi = \frac\mu2(s^2 - 1) - \mu\log s + \frac\lambda2(\log s)^2$, $P_{xx} = \mu(s - 1/s) + \lambda\log(s)/s$ and $P_{yy} = P_{zz} = \lambda\log s$.

- For $0 < s < 1$, both terms of $P_{xx}$ are negative, so the stress always pushes back toward $s = 1$, and $\Psi$ falls as $s$ grows to 1.
- $dP_{xx}/ds = \mu(1 + 1/s^2) + \lambda(1 - \log s)/s^2 > 0$ for $0 < s < 1$, so the size of the compressive stress grows as $s$ falls; it has no largest value, unlike the St. Venant-Kirchhoff model.
- $\Psi \ge -\frac\mu2 - \mu\log s \to \infty$ and $P_{xx} \le \mu - \mu/s \to -\infty$ as $s \to 0^+$.

For a general $F$, $\Psi \ge -\frac\mu2 d - \mu\log J$, which tends to $\infty$ as $J \to 0^+$, so no finite value at $J = 0$ continues $\Psi$, and $\log J$ has no real value for $J < 0$. This is why the code rejects $J \le 0$. $\square$

## Step 7: where the volume term is convex

$\frac{d^2}{dJ^2}(\log J)^2 = \frac{2(1 - \log J)}{J^2}$, which is positive for $0 < J < e$ and negative for $J > e$.
So the term $\frac\lambda2(\log J)^2$ is convex in $J$ only up to $J = e$, and a Newton solver can meet an indefinite stiffness under strong expansion as well as under compression. $\blacksquare$
