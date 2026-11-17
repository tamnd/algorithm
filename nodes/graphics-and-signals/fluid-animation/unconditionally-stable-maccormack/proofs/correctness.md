---
title: The MacCormack step is second order and stable under constant velocity, and the limiter gives a maximum principle
proves: [correctness]
status: full
---

We use the line numbers of the page. $A$ is one semi-Lagrangian step with time step $\Delta t$ (the helper's RK2 backtrace and bilinear sample), and $A^R$ is the same step with $-\Delta t$. The step is

$$\hat q = A q, \qquad \check q = A^R \hat q, \qquad q^{\text{new}} = \hat q + \tfrac12 (q - \check q),$$

followed by the limiter. All statements are in exact arithmetic.

**Lemma 1 (constants).** A constant field stays the same, with or without the limiter.

*Proof.* $A$ and $A^R$ take convex combinations, so $\hat q = \check q = q = \kappa$ and $q^{\text{new}} = \kappa + \frac12 (\kappa - \kappa) = \kappa$. The stencil range is $[\kappa, \kappa]$, so the limiter does nothing. $\square$

**Lemma 2 (an ordinary differential equation).** Apply the same steps to $y' = \lambda y$, with forward Euler $A y = (1 + \lambda h) y$ and its reverse $A^R y = (1 - \lambda h) y$. Then the step is $y \mapsto (1 + \lambda h + \frac12 \lambda^2 h^2)\, y$, which is the second order Taylor step, the same as the two-stage Runge-Kutta methods on this equation.

*Proof.* $\check y = (1 - \lambda h)(1 + \lambda h) y = (1 - \lambda^2 h^2) y$, so $y^{\text{new}} = (1 + \lambda h) y + \frac12 \lambda^2 h^2 y$. $\square$

This is the simplest view of the method: a first order step plus half of its round trip error.

**Setting for the next results.** A periodic grid of spacing $\Delta x$ in 1D, a constant velocity $u > 0$, and $c = u \Delta t / \Delta x = m + \varphi$ with an integer $m \ge 0$ and $\varphi \in [0, 1)$. The RK2 backtrace is exact for a constant velocity, so $A$ multiplies the mode $e^{\mathrm i \theta a}$ by $A(\theta) = e^{-\mathrm i m \theta}(1 - \varphi + \varphi e^{-\mathrm i \theta})$, and $A^R$ multiplies it by $\overline{A(\theta)}$, as on the [BFECC](/bfecc/) proof page. The test file checks the symbol below against the code to $10^{-13}$ in the interior of a 1D grid of 40 cells.

**Lemma 3 (the symbol).** One MacCormack step without the limiter multiplies the mode by

$$G(\theta) = A + \tfrac12 (1 - |A|^2), \qquad 1 - |A|^2 = 2 \varphi (1 - \varphi)(1 - \cos \theta).$$

*Proof.* $\check q = \bar A A q = |A|^2 q$, so $q^{\text{new}} = A q + \frac12 (1 - |A|^2) q$. The modulus is computed on the BFECC page. $\square$

**Theorem 1 (stability for any $\Delta t$, without the limiter).** For every $c \ge 0$ and every $\theta$, $|G(\theta)| \le 1$. So on the periodic grid the step does not increase the $\ell^2$ norm, at any CFL number.

*Proof.* Let $s = |A| \in [0, 1]$. By the triangle inequality, $|G| \le s + \frac12 (1 - s^2)$, and $1 - s - \frac12 (1 - s^2) = \frac12 (1 - s)^2 \ge 0$. Parseval's identity gives the norm bound. $\square$

Unlike BFECC, the MacCormack step can damp a mode more than the plain step does, because $\frac12 (1 - |A|^2)$ is added to $A$ as a real number. For $c = 1.5$ and $\theta = 1.3$, $|A| = 0.796$ and $|G| = 0.748$. The test file checks that such modes exist.

**Theorem 2 (second order).** Let $\alpha = \frac12 \varphi (1 - \varphi)$ and $\beta = \frac16 \varphi(1 - \varphi)(1 - 2 \varphi)$. Then

$$G(\theta) = e^{-\mathrm i c \theta}\left(1 + \mathrm i (\beta + \alpha c)\, \theta^3 + O(\theta^4)\right).$$

For a periodic trigonometric polynomial $q = \sum_k \hat q_k e^{\mathrm i k x}$, with $\Delta x$ small enough that $|k \Delta x| \le \pi$ for each of its modes, the error after the time $T$ at a fixed CFL number is $O(\Delta x^2)$, with the leading term at most

$$T u \left(\alpha + \frac{\beta}{c}\right) \Delta x^2 \sum_k |k|^3 |\hat q_k|$$

up to higher order terms.

*Proof.* The BFECC page shows $A e^{\mathrm i c \theta} = \exp(-\alpha \theta^2 + \mathrm i \beta \theta^3 + O(\theta^4)) = 1 - \alpha \theta^2 + \mathrm i \beta \theta^3 + O(\theta^4)$. By Lemma 3, $\frac12 (1 - |A|^2) = \varphi (1 - \varphi)(1 - \cos \theta) = \alpha \theta^2 + O(\theta^4)$. So

$$G e^{\mathrm i c \theta} = 1 - \alpha \theta^2 + \mathrm i \beta \theta^3 + \alpha \theta^2 (1 + \mathrm i c \theta + O(\theta^2)) + O(\theta^4) = 1 + \mathrm i (\beta + \alpha c) \theta^3 + O(\theta^4).$$

Since $|G| \le 1$, the telescoping bound $|G^N - e^{-\mathrm i N c \theta}| \le N |G - e^{-\mathrm i c \theta}|$ holds. With $\theta = k \Delta x$ and $N = T u / (c \Delta x)$ steps, the error of mode $k$ is at most $\frac{T u}{c \Delta x} \left( |\beta + \alpha c|\, |k \Delta x|^3 + O(|k \Delta x|^4) \right)$, which gives the bound. $\square$

The error constant shows a difference from BFECC. The BFECC constant is $\beta / c$, which shrinks as the CFL number grows. The MacCormack constant has the extra term $\alpha$, which depends only on the fractional part $\varphi$. So at a fixed grid, a larger step does not make MacCormack more accurate. The test file moves a smooth bump for 0.25 s on a 32 by 32 grid and finds the error $0.0486$ at $c = 2/3$ and $0.0492$ at $c = 4/3$. At $c = 4$, a whole number of cells, both $\alpha$ and $\beta$ vanish, and the step is exact. In 2D with a constant velocity, $A = A_x A_y$ and $A^R = \bar A$. Theorem 1 holds with the same proof, and in Theorem 2 the term $\frac12(1 - |A|^2)$ cancels the real second order part of $\log A$ in the same way, so the step is second order in 2D too. The test file measures the order 1.68 between 16 and 32 cells, against 0.89 for the plain step.

**Theorem 3 (the limiter, line L5).** Let $[\ell_a, h_a]$ be the range of the four values of $q$ that the plain step $A$ mixes at sample $a$ (line L4). With the "revert" or the "clamp" limiter, every new value lies in $[\ell_a, h_a]$. So $\min q \le q^{\text{new}} \le \max q$, for any velocity field and any $\Delta t$.

*Proof.* With "revert", a value outside the range is replaced by $\hat q_a = (A q)_a$, a convex combination of the four values, which lies in the range. With "clamp", it is replaced by the nearest end of the range. A value inside the range stays. $\square$

This bound is what keeps the method stable at any step size: with the limiter, every value is bounded by the old extremes for any velocity, as for the plain semi-Lagrangian step. The linear Theorems 1 and 2 hold only where the limiter does not act. Without the limiter, a square of height 1 reaches $1.31$ and $-0.25$ after five steps in the test file, and with either limiter it stays in $[0, 1]$.
