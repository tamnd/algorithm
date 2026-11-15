---
title: The high-gain observer error decays on the time scale eps to a size that is a power of eps, with a peak of order eps to the power 1 - n
proves: [correctness]
status: full
---

The plant is

$$\dot x_i = x_{i+1} \quad (i = 1, \dots, n - 1), \qquad \dot x_n = \phi(x, u), \qquad y = x_1,$$

and lines L1 to L5 compute the right side of

$$\dot{\hat x}_i = \hat x_{i+1} + \frac{\alpha_i}{\varepsilon^i} (y - \hat x_1) \quad (i = 1, \dots, n - 1), \qquad \dot{\hat x}_n = \phi_0(\hat x, u) + \frac{\alpha_n}{\varepsilon^n} (y - \hat x_1),$$

with $\varepsilon > 0$ and $p(s) = s^n + \alpha_1 s^{n-1} + \dots + \alpha_n$ Hurwitz. Let $e_i = x_i - \hat x_i$ and $\delta = \phi(x, u) - \phi_0(\hat x, u)$. Here $\|\cdot\|$ is the Euclidean norm of a vector and the norm it induces on matrices.

## Lemma 1: the scaled error equation

Let $\eta_i = e_i / \varepsilon^{n-i}$ for $i = 1, \dots, n$, and let

$$A_0 = \begin{pmatrix} -\alpha_1 & 1 & & \\ -\alpha_2 & & \ddots & \\ \vdots & & & 1 \\ -\alpha_n & 0 & \cdots & 0 \end{pmatrix}, \qquad B = (0, \dots, 0, 1)^T.$$

Then $\varepsilon \dot \eta = A_0 \eta + \varepsilon B \delta$.

*Proof.* Since $y = x_1$, the output error is $e_1$. For $i < n$, $\dot e_i = e_{i+1} - (\alpha_i / \varepsilon^i) e_1$. Divide by $\varepsilon^{n-i}$ and multiply by $\varepsilon$:

$$\varepsilon \dot \eta_i = \frac{e_{i+1}}{\varepsilon^{n-i-1}} - \alpha_i \frac{e_1}{\varepsilon^{n-1}} = \eta_{i+1} - \alpha_i \eta_1.$$

For $i = n$, $\dot e_n = \delta - (\alpha_n / \varepsilon^n) e_1$, so $\varepsilon \dot \eta_n = \varepsilon \delta - \alpha_n \eta_1$. These are the rows of $A_0 \eta + \varepsilon B \delta$. $\square$

The characteristic polynomial of $A_0$ is $p(s)$, since $A_0$ is a companion matrix (expand the determinant of $sI - A_0$ along the first column). So $A_0$ is Hurwitz. In the time $\tau = t / \varepsilon$ the equation reads $d\eta / d\tau = A_0 \eta + \varepsilon B \delta$: the observer error is a fixed Hurwitz system driven by a term of size $\varepsilon$.

## Theorem 1: exponential decay and ultimate bound

Let $P_0 = P_0^T > 0$ solve $P_0 A_0 + A_0^T P_0 = -I$; it exists because $A_0$ is Hurwitz (theorem of the [Lyapunov equation](/lyapunov-equation/)). Let $\lambda_1 = \lambda_{\min}(P_0)$, $\lambda_2 = \lambda_{\max}(P_0)$, $\beta = \|P_0 B\|$, and assume $|\delta(t)| \le M$ on an interval $[0, t_1)$. Then for $t \in [0, t_1)$

$$\|\eta(t)\| \le \sqrt{\frac{\lambda_2}{\lambda_1}}\, \|\eta(0)\|\, e^{-t/(4 \lambda_2 \varepsilon)} + 4 \beta \sqrt{\frac{\lambda_2}{\lambda_1}}\, \varepsilon M.$$

*Proof.* Let $W = \eta^T P_0 \eta$. By Lemma 1,

$$\varepsilon \dot W = \eta^T (P_0 A_0 + A_0^T P_0) \eta + 2 \varepsilon \eta^T P_0 B \delta \le -\|\eta\|^2 + 2 \varepsilon \beta M \|\eta\|.$$

When $\|\eta\| \ge 4 \varepsilon \beta M$, the last term is at most $\|\eta\|^2 / 2$, so $\varepsilon \dot W \le -\|\eta\|^2 / 2 \le -W / (2 \lambda_2)$. Let $w = \sqrt W$. Where $W > 0$, $\dot w = \dot W / (2 w)$, so $\dot w \le -w / (4 \lambda_2 \varepsilon)$ whenever $\|\eta\| \ge 4 \varepsilon \beta M$. The set $\{W \le \lambda_2 (4 \varepsilon \beta M)^2\}$ contains the ball $\|\eta\| \le 4 \varepsilon \beta M$, and on its boundary $\|\eta\| \ge 4 \varepsilon \beta M$, so $\dot W \le 0$ there and the set is positively invariant. Outside it, $w$ decays at least like $w(0) e^{-t / (4 \lambda_2 \varepsilon)}$. So $w(t) \le \max(w(0) e^{-t/(4 \lambda_2 \varepsilon)}, \sqrt{\lambda_2}\, 4 \varepsilon \beta M)$, and with $\sqrt{\lambda_1} \|\eta\| \le w \le \sqrt{\lambda_2} \|\eta\|$ the bound follows. $\square$

This is the ultimate bound argument with comparison functions in Khalil 2002 (Section 4.8), written out for a quadratic $W$.

**Consequence in the original errors.** Since $e_i = \varepsilon^{n-i} \eta_i$, after the transient

$$|e_i(t)| \le \varepsilon^{n-i} \|\eta(t)\| \le c\, \varepsilon^{n+1-i} M, \qquad c = 8 \beta \sqrt{\lambda_2 / \lambda_1},$$

once the exponential term is below the constant term. With $\|\eta(0)\| \le \|e(0)\| / \varepsilon^{n-1}$ (for $\varepsilon \le 1$), this takes a time of at most $4 \lambda_2 \varepsilon \ln(\|e(0)\| / (4 \beta \varepsilon^n M))$, which is $O(\varepsilon \ln(1/\varepsilon))$. In the page example, $n = 2$: $e_1 = O(\varepsilon^2)$ and $e_2 = O(\varepsilon)$, and the tests measure $e_1 / \varepsilon^2$ between $4.5$ and $4.8$ and $e_2 / \varepsilon$ between $9.2$ and $9.6$ for $\varepsilon = 0.04, 0.02, 0.01$.

The bound $|\delta| \le M$ must hold along the motion. If $\phi$ and $\phi_0$ are continuous and $x$ stays in a compact set, it holds as long as $\hat x$ stays bounded; if $\phi_0$ is evaluated at clipped estimates, as in the second example of the page, it holds for all $t$ with a constant $M$ that does not depend on $\varepsilon$.

## Theorem 2: peaking

For $n \ge 2$ and $e_1(0) \neq 0$, $\|\eta(0)\| \ge |e_1(0)| / \varepsilon^{n-1}$, so the bound of Theorem 1 allows transients of size $1/\varepsilon^{n-1}$, and they occur. For $n = 2$, $\alpha = (2, 1)$, $\delta = 0$ and $e_2(0) = 0$:

$$e_2(t) = -\frac{t}{\varepsilon} e^{-t/\varepsilon} \frac{e_1(0)}{\varepsilon}, \qquad \max_{t \ge 0} |e_2(t)| = \frac{|e_1(0)|}{e\, \varepsilon} \text{ at } t = \varepsilon.$$

*Proof.* With $\delta = 0$ the errors obey $\dot e_1 = e_2 - (2/\varepsilon) e_1$, $\dot e_2 = -(1/\varepsilon^2) e_1$. The matrix has the double eigenvalue $-1/\varepsilon$. Try $e_1 = (a + b t) e^{-t/\varepsilon}$ with $a = e_1(0)$. From $\dot e_1 = e_2 - (2/\varepsilon) e_1$ and $e_2(0) = 0$: $\dot e_1(0) = -2a/\varepsilon$, and $\dot e_1(0) = b - a/\varepsilon$, so $b = -a/\varepsilon$ and $e_1 = a (1 - t/\varepsilon) e^{-t/\varepsilon}$. Then $e_2 = \dot e_1 + (2/\varepsilon) e_1 = a e^{-t/\varepsilon} (-1/\varepsilon - (1/\varepsilon)(1 - t/\varepsilon) + (2/\varepsilon)(1 - t/\varepsilon)) = -a (t/\varepsilon^2) e^{-t/\varepsilon}$. Check the second equation: $\dot e_2 = -a e^{-t/\varepsilon} (1/\varepsilon^2 - t/\varepsilon^3) = -(1/\varepsilon^2) e_1$. The function $\tau e^{-\tau}$ has its largest value $1/e$ at $\tau = 1$. $\square$

The tests check this formula along an RK4 solution with tolerance $10^{-5}$, and the peak of the Van der Pol example (where $\delta \neq 0$) agrees with it within $0.4$ percent.

## Effect of peaking on a feedback loop

The peak of Theorem 2 is the reason a high-gain observer can destabilize a plant whose state feedback is globally asymptotically stable. In the second example of the page, the plant $\dot x_2 = x_2^3 + u$ receives an input of size about $1/\varepsilon^2$ times a cubic in the peak during a time of order $\varepsilon$, which can drive it to a finite escape time; the tests measure an escape before $t = 0.02$ for $\varepsilon = 0.0025$. If $u$ is clipped to $[-M_u, M_u]$, the plant moves at most $O(\varepsilon \ln(1/\varepsilon))$ during the transient of Theorem 1, which tends to $0$ with $\varepsilon$. After the transient the estimates are close to the state, and the loop behaves like the state feedback loop with a small perturbation. The full statement, that the region of attraction and the trajectories of state feedback are recovered as $\varepsilon \to 0$, is the separation principle of Atassi and Khalil (1999); this page cites it and does not reprove it. The tests measure the recovery for $\varepsilon = 0.0025$.
