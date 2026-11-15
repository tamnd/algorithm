---
title: The MIT rule is a gradient step on the squared error, and its stability depends on the gain and the command amplitude
proves: [correctness]
status: full
---

Notation is that of the page. The error is $e = y - y_m$, the adaptation gain is $\gamma > 0$, and $p = d/dt$.

**Claim 1 (gradient).** Fix $\theta$ and let $y(t, \theta)$ be the plant output for this constant $\theta$. Then $\partial (e^2/2)/\partial\theta = e\,\partial y/\partial\theta$, because $y_m$ does not depend on $\theta$. So the law $\dot\theta = -\gamma\,(\partial e/\partial\theta)\, e$ (line L7 with the exact sensitivity in line L5) is $\dot\theta = -\gamma \nabla_\theta (e^2/2)$, the continuous-time gradient flow of the instantaneous cost. If $\psi = c\,\partial e/\partial\theta$ with a known constant $c > 0$, then $-\gamma\psi e = -(\gamma c)\nabla_\theta(e^2/2)$, which is the same flow with the gain $\gamma c$.

For the feedforward gain, a constant $\theta$ gives $y = k G(p)(\theta u_c) = \theta\, k G u_c$, so $\partial e/\partial\theta = k G u_c = (k/k_0) y_m$ with $c = k/k_0 > 0$. The law $\dot\theta = -\gamma y_m e$ is therefore the gradient flow with gain $\gamma k / k_0$. For the first order plant, a constant $\theta$ gives $y = \frac{b\theta_1}{p + a + b\theta_2} u_c$. Differentiation gives $\partial y/\partial\theta_1 = \frac{b}{p + a + b\theta_2} u_c$ and $\partial y/\partial\theta_2 = -\frac{b^2\theta_1}{(p + a + b\theta_2)^2} u_c = -\frac{b}{p + a + b\theta_2} y$. At $\theta = \theta^*$ the denominator is $p + a_m$, and $\frac{b}{p + a_m} = \frac{b}{a_m}\cdot\frac{a_m}{p + a_m}$ with $b/a_m > 0$. So the filters of the page are the exact sensitivities at $\theta^*$, up to the positive constant $b/a_m$.

The claim needs $\theta$ constant. When $\theta$ changes, $G(p)(\theta u_c) \ne \theta\,G(p)u_c$, and the flow is only an approximation of the gradient flow. That is why Claim 1 gives no stability.

**Claim 2 (equilibrium).** At $\theta = \theta^*$ the closed loop transfer function from $u_c$ to $y$ equals that of the model: $k G \theta^* = k_0 G$ for the feedforward gain, and $\frac{b\theta_1^*}{p + a + b\theta_2^*} = \frac{b_m}{p + a_m}$ for the first order plant. So $e$ is the difference of the free responses of two systems with the same poles in the open left half plane, and $e(t) \to 0$ exponentially. Then $\psi e \to 0$ for every bounded command, because $\psi$ is the output of a BIBO stable filter of bounded signals. So $\theta^*$ with $e = 0$ is an equilibrium of the adaptive loop when the plant and the model start from matching states.

**Claim 3 (exact stability limit).** Let $G(s) = 1/(s^2 + a_1 s + a_2)$ with $a_1, a_2 > 0$, let $k, k_0 > 0$, let the command be the constant $u_0 \ne 0$, and let the model be at rest, $y_m(t) = y_{m0} = k_0 u_0 / a_2$ for all $t \ge 0$. Then $\theta(t) \to k_0/k$ for all initial states if and only if $\gamma k k_0 u_0^2 < a_1 a_2^2$.

*Proof.* The plant equation is $\ddot y + a_1 \dot y + a_2 y = k u_0\, \theta(t)$, and the law is $\dot\theta = -\gamma y_{m0}(y - y_{m0})$. Differentiate the law twice: $\ddot\theta = -\gamma y_{m0} \dot y$ and $\dddot\theta = -\gamma y_{m0} \ddot y$. Then
$$\dddot\theta + a_1\ddot\theta + a_2\dot\theta = -\gamma y_{m0}(\ddot y + a_1 \dot y + a_2 y - a_2 y_{m0}) = -\gamma y_{m0}(k u_0\theta - a_2 y_{m0}).$$
With $y_{m0} = k_0 u_0/a_2$ this is
$$\dddot\theta + a_1\ddot\theta + a_2\dot\theta + \frac{\gamma k k_0 u_0^2}{a_2}\,\theta = \frac{\gamma k_0^2 u_0^2}{a_2}.$$
This is a linear equation with constant coefficients. Its constant solution is $\theta = k_0/k$. The map from the state $(y, \dot y, \theta)$ to $(\theta, \dot\theta, \ddot\theta)$ is linear and invertible (its determinant is $\gamma^2 y_{m0}^2 \ne 0$), so every solution of the adaptive loop goes to the constant solution if and only if the polynomial $s^3 + a_1 s^2 + a_2 s + c$ with $c = \gamma k k_0 u_0^2 / a_2 > 0$ is Hurwitz. By the Routh-Hurwitz criterion for a cubic with positive coefficients, this holds if and only if $a_1 a_2 > c$, that is, $\gamma k k_0 u_0^2 < a_1 a_2^2$. If $a_1 a_2 < c$, the first column of the Routh array has two sign changes, so two roots are in the open right half plane and $\theta$ grows without bound for almost every initial state. $\square$

For the example of the page, $a_1 = a_2 = k = 1$ and $k_0 = 2$, so the condition is $\gamma u_0^2 < 1/2$. The test file checks the formula against the Routh verdict on random data, and checks the simulated $\theta$ against a separate integration of the third order equation.

**Consequence.** For every $\gamma > 0$ there is a command amplitude $u_0$ with $\gamma k k_0 u_0^2 > a_1 a_2^2$, so no fixed gain makes the adaptive loop of the MIT rule converge for all constant commands. This is the reason for the Lyapunov design of model reference adaptive control.
