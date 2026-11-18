---
title: The stable neo-Hookean stress is the gradient of its energy for every F, the rest state needs the stated alpha, and the remap gives the target Lamé parameters
proves: [correctness]
status: full
---

The code works in $\mathbb R^3$.
For every $3 \times 3$ matrix $F$ it computes $I_C = \lvert F\rvert_F^2$, $J = \det F$,
$$\Psi(F) = \frac\mu2(I_C - 3) + \frac\lambda2(J - \alpha)^2 - \frac\mu2\log(I_C + 1), \qquad P = \mu\Bigl(1 - \frac1{I_C + 1}\Bigr)F + \lambda(J - \alpha)\operatorname{cof}F,$$
with $\alpha = 1 + \frac{3\mu}{4\lambda}$ unless the caller gives another $\alpha$, and the cofactor matrix $\operatorname{cof}F$, whose column $k$ is the cross product of the other two columns of $F$ in cyclic order.
$A : B = \operatorname{tr}(A^TB)$, and all claims are about exact arithmetic with $\mu > 0$ and $\lambda > 0$.

## Step 1: $P = \partial\Psi/\partial F$ for every $F$

$J$ is a polynomial in the entries of $F$, and its expansion along row $i$ gives $\partial J/\partial F_{ij} = (\operatorname{cof}F)_{ij}$, for every $F$, singular or not.
When $J \ne 0$, $\operatorname{cof}F = JF^{-T}$.
$dI_C = 2F : dF$ and $I_C + 1 \ge 1$, so the log term is smooth for all $F$.
So $d\Psi = \mu F : dF + \lambda(J - \alpha)\operatorname{cof}F : dF - \frac{\mu}{I_C + 1}F : dF = P : dF$.
$\Psi$ and $P$ are finite and smooth on all of $\mathbb R^{3\times3}$, including $J = 0$ and $J < 0$. $\square$

## Step 2: the element forces

With $F = D_sD_m^{-1}$ and $W = V_0\Psi(F)$, $dW = V_0PD_m^{-T} : dD_s$, as for every energy density of $F$.
So the code, which returns minus column $k$ of $V_0PD_m^{-T}$ for vertex $k = 1, 2, 3$ and minus their negated sum for vertex 0, returns $-\partial W/\partial x$.
Only $D_m$ is inverted, so this holds when the current tetrahedron is flat or inverted. $\square$

## Step 3: objectivity, isotropy and no torque

For a rotation $Q$, $I_C$ and $J$ do not change when $F$ becomes $QF$ or $FQ$, so neither does $\Psi$.
$\operatorname{cof}(QF) = Q\operatorname{cof}F$, because $\operatorname{cof}(AB) = \operatorname{cof}A\operatorname{cof}B$ and $\operatorname{cof}Q = Q$, so $P(QF) = QP(F)$.
$PF^T = a FF^T + \lambda(J - \alpha)\operatorname{cof}(F)F^T$ with $a = \mu(1 - 1/(I_C + 1))$, and $\operatorname{cof}(F)F^T = JI$, so $PF^T$ is symmetric. $\square$

## Step 4: the rest state needs the right $\alpha$

At $F = I$, $I_C = 3$, $J = 1$ and $\operatorname{cof}I = I$, so $P(I) = \bigl(\frac34\mu + \lambda(1 - \alpha)\bigr)I$.
This is zero exactly when $\alpha = 1 + \frac{3\mu}{4\lambda}$, which is the same number as $1 + \frac\mu\lambda - \frac\mu{4\lambda}$.
With $\alpha = 1$, $P(I) = \frac34\mu I$; with $\alpha = 1 + \mu/\lambda$, the value without the log term, $P(I) = -\frac14\mu I$.
For a rotation $Q$, $P(Q) = QP(I)$ by Step 3, so every rotation is at rest too.
$\Psi(I) = \frac\lambda2(1 - \alpha)^2 - \frac\mu2\log4$ is not zero; only differences of $\Psi$ matter. $\square$

## Step 5: the linear limit and the remap

Let $F = I + \varepsilon H$ and $t = \operatorname{tr}H$.
Then $I_C = 3 + 2\varepsilon t + O(\varepsilon^2)$, so $1 - 1/(I_C + 1) = \frac34 + \frac{\varepsilon t}8 + O(\varepsilon^2)$; $J - \alpha = (1 - \alpha) + \varepsilon t + O(\varepsilon^2)$ with $\lambda(1 - \alpha) = -\frac34\mu$; and $\operatorname{cof}F = I + \varepsilon(tI - H^T) + O(\varepsilon^2)$.
Collecting the terms of order $\varepsilon$:
$$P = \varepsilon\Bigl(\tfrac34\mu(H + H^T) + \bigl(\tfrac18\mu - \tfrac34\mu + \lambda\bigr)tI\Bigr) + O(\varepsilon^2) = \varepsilon\bigl(2\mu_0\operatorname{sym}H + \lambda_0 tI\bigr) + O(\varepsilon^2)$$
with $\mu_0 = \frac34\mu$ and $\lambda_0 = \lambda - \frac58\mu$.
So the model parameters $\mu = \frac43\mu_0$ and $\lambda = \lambda_0 + \frac56\mu_0$ give the target Lamé parameters $\mu_0$ and $\lambda_0$.
The Poisson's ratio of the limit is $\lambda_0/(2(\lambda_0 + \mu_0)) = (\lambda - \frac58\mu)/(2(\lambda + \frac18\mu))$. $\square$

## Step 6: the bar, flat and inverted states

Let $F = \operatorname{diag}(s, 1, 1)$ for any real $s$.
Then $I_C = s^2 + 2$, $J = s$, and $P_{xx} = d\Psi/ds = g(s) + \lambda(s - \alpha)$ with $g(s) = \mu s(s^2 + 2)/(s^2 + 3)$.
$g'(s) = \mu(s^4 + 7s^2 + 6)/(s^2 + 3)^2 > 0$, so $P_{xx}$ is strictly increasing in $s$, and by Step 4 it is zero at $s = 1$.
So $P_{xx} < 0$ for every $s < 1$ and $P_{xx} > 0$ for every $s > 1$: for a compressed, flat or inverted bar the force $-d\Psi/ds$ pushes toward $s = 1$, and $s = 1$ is the only rest state on this line.
At $s = 0$ the energy is finite, and $P_{xx} = -\lambda\alpha$. $\square$

## Step 7: the collapsed state

At $F = 0$, $\operatorname{cof}F = 0$ and the first term of $P$ is zero, so $P(0) = 0$: a tetrahedron collapsed to a point feels no elastic force.
For $F = \varepsilon G$, $I_C = \varepsilon^2\lvert G\rvert_F^2$ and $-\frac\mu2\log(1 + I_C) = -\frac\mu2I_C + O(\varepsilon^4)$, so the terms of order $\varepsilon^2$ cancel and
$$\Psi(\varepsilon G) - \Psi(0) = -\lambda\alpha\varepsilon^3\det G + O(\varepsilon^4).$$
So $F = 0$ is a saddle: the energy falls for $\det G > 0$ and rises for $\det G < 0$.
On the line $F = \varepsilon G$ the force $-d\Psi/d\varepsilon = 3\lambda\alpha\varepsilon^2\det G + O(\varepsilon^3)$ moves $\varepsilon$ toward the sign of $\det G$, which is the side where $\det(\varepsilon G) = \varepsilon^3\det G > 0$. $\blacksquare$
