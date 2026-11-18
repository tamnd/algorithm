---
title: The deformation gradient of a linear element is the gradient of its affine map, with the stated properties of J, the Green strain and the polar factor
proves: [correctness]
status: full
---

Let a simplex in $\mathbb R^d$ ($d = 2$ or 3) have the rest vertices $X_0, \dots, X_d$ with $\det D_m \ne 0$, where $D_m = [X_1 - X_0, \dots, X_d - X_0]$, and the current vertices $x_0, \dots, x_d$ with $D_s = [x_1 - x_0, \dots, x_d - x_0]$.
The code computes $F = D_sD_m^{-1}$.

## Step 1: $F$ is the gradient of the unique affine map

An affine map $\varphi(X) = AX + t$ with $\varphi(X_k) = x_k$ for all $k$ must satisfy $A(X_k - X_0) = x_k - x_0$ for $k = 1, \dots, d$, that is $AD_m = D_s$.
Since $D_m$ is invertible, $A = D_sD_m^{-1} = F$ is the only solution, and $t = x_0 - FX_0$.
So $F$ is the gradient of the linear interpolant of the vertex positions, and if $x = AX + t$ for some affine map, then $F = A$ exactly.
The interpolant does not depend on how the vertices are numbered, so neither does $F$. $\square$

## Step 2: $J = \det F$ is the ratio of the signed measures

The signed measure of a simplex is $\det D/d!$.
By Step 1, $\det D_s = \det(FD_m) = \det F\det D_m$, so $J = \det D_s/\det D_m$, the ratio of the current to the rest measure with sign.
$J < 0$ exactly when the orientation of the simplex is reversed, which is an inverted element, and $J = 0$ exactly when it is flat. $\square$

## Step 3: composition

Let $\varphi_1$ map the rest simplex to a middle simplex $y$ and $\varphi_2$ map $y$ to $x$, both affine with the gradients $F_1$ and $F_2$.
Then $\varphi_2 \circ \varphi_1$ is affine with the gradient $F_2F_1$ and maps $X_k$ to $x_k$, so by Step 1 the deformation gradient from $X$ to $x$ is $F_2F_1$. $\square$

## Step 4: the Green strain

$E = (F^TF - I)/2$.
For a rotation $Q$, $(QF)^T(QF) = F^TQ^TQF = F^TF$, so $E(QF) = E(F)$: a rotation after the deformation does not change the strain.
$E = 0$ exactly when $F^TF = I$, that is when $F$ is orthogonal.
An orthogonal $F$ is a rotation if $\det F = 1$ and a reflection if $\det F = -1$, so $E$ is zero for every rigid motion, and also for a mirror image, which $E$ cannot tell apart from the rest shape.
With $F = I + H$, $F^TF = I + H + H^T + H^TH$, so

$$E = \tfrac12(H + H^T) + \tfrac12H^TH,$$

and for $H$ replaced by $\varepsilon H$ the difference between $E$ and the linear strain $\frac12\varepsilon(H + H^T)$ is $\frac12\varepsilon^2H^TH$, which falls by a factor of 4 when $\varepsilon$ is halved. $\square$

## Step 5: small elements of a smooth map

Let $\varphi$ be twice continuously differentiable, and let the rest simplex have the vertices $X_0$ and $X_k = X_0 + hu_k$ with fixed $u_k$ and $\det[u_1, \dots, u_d] \ne 0$.
By Taylor's theorem, $\varphi(X_k) - \varphi(X_0) = h\nabla\varphi(X_0)u_k + \frac{h^2}{2}r_k$ with $r_k$ bounded independently of $h$.
So $D_s = h\nabla\varphi(X_0)U + \frac{h^2}{2}[r_1, \dots, r_d]$ with $U = [u_1, \dots, u_d]$, $D_m = hU$, and

$$F - \nabla\varphi(X_0) = \tfrac h2[r_1, \dots, r_d]U^{-1}.$$

The error is $O(h)$, and $[r_1, \dots, r_d] \to \nabla^2\varphi(X_0)[u_k, u_k]$ column by column as $h \to 0$, so the error divided by $h$ has a limit and the error halves when $h$ halves, unless that limit is zero. $\square$

## Step 6: the polar factor in 2D

For a rotation $R(\theta)$ with $c = \cos\theta$ and $s = \sin\theta$, $\operatorname{tr}(R^TF) = c(F_{00} + F_{11}) + s(F_{10} - F_{01})$.
With $\rho = \sqrt{(F_{00} + F_{11})^2 + (F_{10} - F_{01})^2}$ this is $\rho\cos(\theta - \theta^*)$ with $\theta^* = \operatorname{atan2}(F_{10} - F_{01}, F_{00} + F_{11})$, which is largest at $\theta = \theta^*$, the angle of the code.
For this angle, the off-diagonal entries of $S = R^TF$ are $cF_{01} + sF_{11}$ and $-sF_{00} + cF_{10}$, and their difference $c(F_{01} - F_{10}) + s(F_{00} + F_{11})$ is $\rho(-\sin\theta^*\cos\theta^* + \cos\theta^*\sin\theta^*) = 0$, so $S$ is symmetric and $F = RS$.
$\operatorname{tr}S = \rho \ge 0$ and $\det S = \det F$, so if $\det F > 0$ both eigenvalues of $S$ are positive and $S$ is the positive definite polar factor.
Then $F^TF = S^TR^TRS = S^2$, so $E(F) = E(S)$, which is also true in 3D for the factors of anim.polar. $\blacksquare$
