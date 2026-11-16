---
title: For the 3R position problem, the real roots of the quartic left after the dialytic elimination give exactly the solutions
proves: [correctness]
status: full
---

This page proves the correctness of the 3R version that the implementation runs.
The 6R method of Raghavan and Roth follows the same steps on a larger system, and its proof is in their paper; the page only describes it.

## Setting

The arm has Denavit-Hartenberg parameters $(a_i, \alpha_i, d_i)$, with $T_i = R_z(\theta_i)\,T_z(d_i)\,T_x(a_i)\,R_x(\alpha_i)$, and the task is to put the origin of frame 3 at the point $p$.
Write $c_i = \cos\theta_i$, $s_i = \sin\theta_i$, and $ca_i$, $sa_i$ for the cosine and sine of $\alpha_i$.
We call the arm and the target **general** if $a_1 \ne 0$, $sa_1 \ne 0$, $h_1^2 + h_2^2 > 0$ for every $\theta_3$ (with $h$ below), $(p_x, p_y) \ne (0, 0)$, and the quartic below is not the zero polynomial.

## Step 1: two equations free of $\theta_1$

Multiplying out the transforms gives $p = R_z(\theta_1)\,g$, with
$$g = (a_1, 0, d_1) + R_x(\alpha_1)\,R_z(\theta_2)\,h, \qquad h = (a_2, 0, d_2) + R_x(\alpha_2)(a_3c_3, a_3s_3, d_3).$$
So $h = (a_2 + a_3c_3,\ ca_2a_3s_3 - sa_2d_3,\ d_2 + sa_2a_3s_3 + ca_2d_3)$ depends on $\theta_3$ only.
A rotation about $z$ keeps the length and the $z$ coordinate, so $|p|^2 = |g|^2$ and $p_z = g_z$.
With $f = R_z(\theta_2)h = (c_2h_1 - s_2h_2,\ s_2h_1 + c_2h_2,\ h_3)$, these two equations become
$$E_1:\ 2a_1h_1\,c_2 - 2a_1h_2\,s_2 + K = 0, \qquad E_2:\ sa_1h_2\,c_2 + sa_1h_1\,s_2 + L = 0,$$
with $K = |h|^2 + a_1^2 - d_1^2 - |p|^2 + 2d_1p_z$ and $L = d_1 + ca_1h_3 - p_z$.
For $E_1$ we used $g_z = p_z$ to replace the term $2d_1(sa_1f_2 + ca_1h_3)$ by $2d_1(p_z - d_1)$.
Conversely, if $\theta_2, \theta_3$ satisfy $E_1$ and $E_2$, then $|g| = |p|$ and $g_z = p_z$, so $(g_x, g_y)$ and $(p_x, p_y)$ have the same length.
If that length is not 0, exactly one $\theta_1$ modulo $2\pi$ rotates the one onto the other, $\theta_1 = \operatorname{atan2}(p_y, p_x) - \operatorname{atan2}(g_y, g_x)$, and then $R_z(\theta_1)g = p$.
So the solutions are in one to one correspondence with the pairs $(\theta_2, \theta_3)$ that satisfy $E_1$ and $E_2$.

## Step 2: the condition on $\theta_3$

Write $E_j$ as $P_jc_2 + Q_js_2 + K_j = 0$, with $(P_1, Q_1, K_1) = (2a_1h_1, -2a_1h_2, K)$ and $(P_2, Q_2, K_2) = (sa_1h_2, sa_1h_1, L)$.
Let $D = P_1Q_2 - P_2Q_1 = 2a_1sa_1(h_1^2 + h_2^2)$, $X = Q_1K_2 - Q_2K_1$ and $Y = K_1P_2 - K_2P_1$.
For a general arm $D \ne 0$, so the linear system has the unique solution $(c_2, s_2) = (X/D, Y/D)$ by Cramer's rule, and a $\theta_2$ exists if and only if $X^2 + Y^2 = D^2$.
Expanding, the cross terms of $X^2 + Y^2$ cancel, and
$$X^2 + Y^2 - D^2 = (h_1^2 + h_2^2)\,q, \qquad q = 4a_1^2L^2 + sa_1^2K^2 - 4a_1^2sa_1^2(h_1^2 + h_2^2).$$
Since $h_1^2 + h_2^2 > 0$, a $\theta_3$ gives a solution if and only if $q = 0$ at $\theta_3$, and then $\theta_2$ is unique.
So the number of solutions equals the number of zeros of $q$ in $\theta_3$ modulo $2\pi$.

## Step 3: the dialytic matrix gives the same polynomial

With $x_i = \tan(\theta_i/2)$, $c_i = (1 - x_i^2)/(1 + x_i^2)$ and $s_i = 2x_i/(1 + x_i^2)$.
Every coefficient $P_j, Q_j, K_j$ has the form $u + vc_3 + ws_3$, so its product with $1 + x_3^2$ is the polynomial $(u + v) + 2wx_3 + (u - v)x_3^2$; we mark such products with a tilde.
Multiplying $E_j$ by $(1 + x_2^2)(1 + x_3^2)$ gives the quadratic $A_jx_2^2 + B_jx_2 + C_j$ with $A_j = \tilde K_j - \tilde P_j$, $B_j = 2\tilde Q_j$ and $C_j = \tilde K_j + \tilde P_j$.
Multiplying each quadratic by $1$ and by $x_2$ gives four equations, linear in $(x_2^3, x_2^2, x_2, 1)$, with the $4 \times 4$ matrix $M(x_3)$ of line L3; this is the Sylvester matrix of the two quadratics, and its determinant is their resultant.
For two quadratics the resultant is $(A_1C_2 - A_2C_1)^2 - (A_1B_2 - A_2B_1)(B_1C_2 - B_2C_1)$, and substituting $A_j, B_j, C_j$ gives
$$\det M(x_3) = 4\big[(\tilde K_1\tilde P_2 - \tilde K_2\tilde P_1)^2 + \tilde X^2 - \tilde D^2\big] = 4\,\big(\tilde h_1^2 + \tilde h_2^2\big)\,\tilde q,$$
where every tilde quantity is the polynomial in $x_3$ of the same quantity times the right power of $1 + x_3^2$.
Here $\tilde h_1^2 + \tilde h_2^2 = (1 + x_3^2)^2(h_1^2 + h_2^2)$ is the extraneous factor of line L5: it has no real root for a general arm, so it gives no solution.
The quotient $\tilde q = (1 + x_3^2)^2q$ is a polynomial of degree at most 4 in $x_3$, and for real $x_3$ it is zero exactly when $q$ is zero.
The tests check the identity $\det M = 4(\tilde h_1^2 + \tilde h_2^2)\tilde q$ coefficient by coefficient.

## Step 4: back substitution

Take a real root $x_3$ of $\tilde q$ and $\theta_3 = 2\arctan x_3$.
The vector $(c_2, s_2, 1)$ is a null vector of the $2 \times 3$ matrix with rows $(P_j, Q_j, K_j)$.
Since $D \ne 0$, that matrix has rank 2, its null space is one dimensional, and the cross product of the rows, $(X, Y, D)$, spans it.
So $(c_2, s_2) = (X/D, Y/D)$, as line L7 computes, and by Step 2 it lies on the unit circle.
Line L8 then gives $\theta_1$ by Step 1.
$\square$

## Conclusion

For a general arm and target, the algorithm returns every solution, and each real root of $\tilde q$ gives exactly one solution.
The angle $\theta_3 = \pi$ is the root $x_3 = \infty$; it shows up as a drop of the degree of $\tilde q$, and the implementation then tests it as a candidate.
Since $\tilde q$ has degree at most 4, a general 3R arm has at most 4 solutions for a position.
The implementation checks every candidate by forward kinematics, which guards against roots that rounding has moved off the real axis or onto it.
