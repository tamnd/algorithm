---
title: The observer of linear ADRC estimates the total disturbance with an error of order 1 over its bandwidth, and the loop rejects constant disturbances exactly
proves: [correctness]
status: full
---

The plant is $\ddot y = f(t, y, \dot y) + b u$ with $f$ unknown and $b$ known only as $b_0 \neq 0$. Write it as

$$\ddot y = F + b_0 u, \qquad F = f(t, y, \dot y) + (b - b_0) u,$$

where $F$ is the total disturbance. Lines L1 to L7 compute

$$u = \frac{\omega_c^2 (r - z_1) - 2 \omega_c z_2 - z_3}{b_0}, \qquad \begin{aligned} \dot z_1 &= z_2 + 3 \omega_o (y - z_1), \\ \dot z_2 &= z_3 + 3 \omega_o^2 (y - z_1) + b_0 u, \\ \dot z_3 &= \omega_o^3 (y - z_1), \end{aligned}$$

with $\omega_c, \omega_o > 0$ and a constant reference $r$. Let $x = (y, \dot y, F)$ and $e = x - z$. Here $\|\cdot\|$ is the Euclidean norm.

## Lemma 1: the observer error equation

If $F$ is absolutely continuous in $t$ along the motion, then for almost every $t$

$$\dot e_1 = e_2 - 3 \omega_o e_1, \qquad \dot e_2 = e_3 - 3 \omega_o^2 e_1, \qquad \dot e_3 = \dot F - \omega_o^3 e_1.$$

*Proof.* $\dot x_1 = \dot y = x_2$, $\dot x_2 = \ddot y = F + b_0 u$, $\dot x_3 = \dot F$. Subtract the observer, using $y - z_1 = e_1$: $\dot e_1 = x_2 - z_2 - 3 \omega_o e_1$, $\dot e_2 = F + b_0 u - z_3 - 3 \omega_o^2 e_1 - b_0 u = e_3 - 3 \omega_o^2 e_1$, $\dot e_3 = \dot F - \omega_o^3 e_1$. $\square$

The input $u$ cancels, so the error equation does not depend on the control law. The tests check Lemma 1 exactly in Fraction for 200 random cases.

## Theorem 1: the size of the estimation error

Let $\eta = (\omega_o^2 e_1, \omega_o e_2, e_3)$. Then $\dot \eta = \omega_o A_1 \eta + B \dot F$ with

$$A_1 = \begin{pmatrix} -3 & 1 & 0 \\ -3 & 0 & 1 \\ -1 & 0 & 0 \end{pmatrix}, \qquad B = (0, 0, 1)^T,$$

and $\det(sI - A_1) = (s + 1)^3$. Let $P_1 = P_1^T > 0$ solve $P_1 A_1 + A_1^T P_1 = -I$, let $\lambda_1, \lambda_2$ be its smallest and largest eigenvalues, and $\beta = \|P_1 B\|$; these numbers depend only on $A_1$. If $|\dot F(t)| \le M$ on $[0, t_1)$, then for $t \in [0, t_1)$

$$\|\eta(t)\| \le \sqrt{\frac{\lambda_2}{\lambda_1}} \left( \|\eta(0)\| e^{-\omega_o t / (4 \lambda_2)} + \frac{4 \beta M}{\omega_o} \right).$$

So after a transient of length $O(\ln(\omega_o) / \omega_o)$, $|e_3| = O(M / \omega_o)$, $|e_2| = O(M / \omega_o^2)$ and $|e_1| = O(M / \omega_o^3)$.

*Proof.* From Lemma 1, $\dot \eta_1 = \omega_o^2 (e_2 - 3 \omega_o e_1) = \omega_o (\eta_2 - 3 \eta_1)$, $\dot \eta_2 = \omega_o (e_3 - 3 \omega_o^2 e_1) = \omega_o (\eta_3 - 3 \eta_1)$, $\dot \eta_3 = \dot F - \omega_o \eta_1$. $A_1$ is the companion matrix of $s^3 + 3 s^2 + 3 s + 1 = (s + 1)^3$, so it is Hurwitz. With $\varepsilon = 1/\omega_o$ this is the scaled error equation $\varepsilon \dot \eta = A_1 \eta + \varepsilon B \dot F$ of a [high-gain observer](/high-gain-observer/) of order $3$ with $\delta = \dot F$, and Theorem 1 of that page's proof gives the bound. $\square$

The bound needs $|\dot F| \le M$ along the motion. $\dot F$ contains $(b - b_0) \dot u$, and $\dot u$ contains $\dot z_3 = \omega_o^3 e_1$, so for $b \neq b_0$ the bound is not given in advance; it must come from an analysis of the closed loop, such as Theorem 3 for linear plants, or the nonlinear analysis of Guo and Zhao (2011), which this page cites and does not reprove.

## Theorem 2: the closed loop as a perturbed PD loop

Let $\tilde y = y - r$. Then

$$\ddot{\tilde y} + 2 \omega_c \dot{\tilde y} + \omega_c^2 \tilde y = e_3 + 2 \omega_c e_2 + \omega_c^2 e_1.$$

*Proof.* $b_0 u = \omega_c^2 (r - z_1) - 2 \omega_c z_2 - z_3$, and $z_i = x_i - e_i$. So $\ddot y = F + b_0 u = F + \omega_c^2 (r - y + e_1) - 2 \omega_c (\dot y - e_2) - (F - e_3)$. The $F$ terms cancel. $\square$

The left side has the double pole $-\omega_c$. With $\omega_c^2 e_1$ and $2 \omega_c e_2$ small next to $e_3$ (they carry the extra factors $\omega_c^2 / \omega_o^2$ and $\omega_c / \omega_o$), the deviation of $\tilde y$ from the response of the PD loop is the forced response of $1 / (s + \omega_c)^2$ to the right side. Its impulse response $t e^{-\omega_c t}$ is positive with integral $1/\omega_c^2$, so an input bounded by $m$ gives a deviation bounded by $m / \omega_c^2$ (a theorem, by the convolution bound). So the deviation is of order $M / (\omega_c^2 \omega_o)$. The page example measures the maximum deviation from the ideal response $1 - (1 + 2t) e^{-2t}$ as $0.0514$, $0.0241$, $0.0113$ for $\omega_o = 10, 20, 40$: each doubling of $\omega_o$ divides it by about $2.13$.

## Theorem 3: separation and exact rejection for linear plants

Let $f = -a_0 y - a_1 \dot y + d$ with constants $a_0, a_1$ and a constant $d$.

(a) If $f = 0$ and $b = b_0$, the closed loop is linear with characteristic polynomial $(s + \omega_c)^2 (s + \omega_o)^3$.

(b) In general the closed loop is linear and time invariant in $(y, \dot y, z_1, z_2, z_3)$, with the constant input $(r, d)$. If its matrix is Hurwitz, then $y(t) \to r$ for every constant $d$.

*Proof.* (a) Here $F = 0$ and $e$ obeys Lemma 1 with $\dot F = 0$, a system with the polynomial $(s + \omega_o)^3$ (Theorem 1 scaled back). Theorem 2 gives $\tilde y$ driven by $e$, with the polynomial $(s + \omega_c)^2$. In the coordinates $(\tilde y, \dot{\tilde y}, e)$ the matrix is block triangular, so its characteristic polynomial is the product. The tests check this exactly in Fraction for 20 random choices of $\omega_c$, $\omega_o$, $b_0$, with the matrix written in the original coordinates.

(b) If the matrix is Hurwitz, the state converges to the unique equilibrium. At the equilibrium, $\dot z_3 = \omega_o^3 (y - z_1) = 0$ gives $z_1 = y$; $\dot z_1 = z_2 = 0$; $\dot z_2 = z_3 + b_0 u = 0$, and with L2, $b_0 u = \omega_c^2 (r - z_1) - z_3$, so $\omega_c^2 (r - y) = 0$ and $y = r$. This holds for every $d$, $a_0$, $a_1$ and $b$: the state $z_3$ acts as an integrator. $\square$

For the page example ($a_0 = 1$, $a_1 = 1/2$, $b = 2$, $b_0 = 3/2$, $\omega_c = 2$, $\omega_o = 10$) the characteristic polynomial is

$$s^5 + \tfrac{69}{2} s^4 + 442 s^3 + \tfrac{10018}{3} s^2 + \tfrac{22072}{3} s + \tfrac{16000}{3},$$

and the first column of its Routh array is positive (computed exactly in the tests), so the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/) says the matrix is Hurwitz. By (b), $y \to 1$ before and after the step in $d$. With the same gains, the loop is Hurwitz for $b = 1/100$ and $b = 8$ and not for $b = 17/2$: a gain error $b / b_0$ up to about $5.3$ is tolerated here, and the bound is not symmetric. For a plant that is not linear, convergence of the estimates and of the output is a theorem of Guo and Zhao (2011) under bounds on $f$ and its derivatives and on $b - b_0$; this page cites it.
