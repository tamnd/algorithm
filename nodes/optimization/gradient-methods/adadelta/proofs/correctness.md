---
title: Adadelta needs ε to move, has bounded steps, is invariant to diagonal rescaling when its two ε terms carry the right units, and on a constant slope its step tends to the gradient
proves: [correctness, convergence-rate]
status: full
---

**Setting.** Adadelta with decay $\rho \in (0, 1)$, constants $\epsilon_x > 0$ and $\epsilon_g \ge 0$ and a factor $\lambda > 0$ starts from $x_1$ and $a_0 = b_0 = 0$. In round $t = 1, 2, \dots$ it receives a gradient $g_t$ and sets, for each coordinate $i$ (the index is dropped),

$$b_t = \rho b_{t-1} + (1 - \rho)g_t^2, \quad \Delta_t = -\lambda\frac{\sqrt{a_{t-1} + \epsilon_x}}{\sqrt{b_t + \epsilon_g}}g_t, \quad a_t = \rho a_{t-1} + (1 - \rho)\Delta_t^2, \quad x_{t+1} = x_t + \Delta_t,$$

with $\Delta_t = 0$ when $b_t + \epsilon_g = 0$. Zeiler's method is $\lambda = 1$ and $\epsilon_x = \epsilon_g = \epsilon$; $b_t$ is $E[g^2]_t$ and $a_t$ is $E[\Delta x^2]_t$ in his notation. Two separate constants are used here because $\epsilon_x$ has the units of $x^2$ and $\epsilon_g$ the units of $g^2$, and Proposition 4 needs this.

Zeiler (2012) gives no convergence proof, and the sources of this page give no convergence theorem for Adadelta with assumptions like those for AdaGrad or AMSGrad. This file proves the structural facts that the method's design rests on.

**Proposition 1 (ε is needed).** If $\epsilon_x = 0$, then $\Delta_t = 0$ and $x_t = x_1$ for all $t$.

*Proof.* By induction, $a_{t-1} = 0$, so the numerator $\sqrt{a_{t-1} + 0}$ is $0$ and $\Delta_t = 0$, so $a_t = \rho\cdot0 + 0 = 0$. $\square$

So $\epsilon_x$ is not a safeguard against division by zero. It sets the size of the first steps.

**Proposition 2 (first step).** $\Delta_1 = -\lambda\sqrt{\epsilon_x}\,g_1/\sqrt{(1 - \rho)g_1^2 + \epsilon_g}$. If $g_1^2 \gg \epsilon_g/(1 - \rho)$, then $|\Delta_1| \approx \lambda\sqrt{\epsilon_x/(1 - \rho)}$.

*Proof.* Put $a_0 = b_0 = 0$ in the update. $\square$

For $\epsilon = 10^{-6}$ and $\rho = 0.95$, the first step is about $0.0045$, whatever the gradient. So in its first steps Adadelta behaves like RMSProp with the step $\sqrt{\epsilon_x}$.

**Proposition 3 (bounded steps).** For every gradient sequence, $|\Delta_t| \le \lambda\sqrt{(a_{t-1} + \epsilon_x)/(1 - \rho)}$.

*Proof.* $b_t \ge (1 - \rho)g_t^2$, so $|g_t|/\sqrt{b_t + \epsilon_g} \le 1/\sqrt{1 - \rho}$. $\square$

So each step is bounded by a multiple of the root mean square of the recent steps, and the step can grow by at most a factor of about $1/\sqrt{1 - \rho}$ relative to the recent ones.

**Proposition 4 (units).** Let $c > 0$ and $s_1, \dots, s_d > 0$, put $S = \operatorname{diag}(s)$, and let $h(y) = c\,f(Sy)$. Run Adadelta on $f$ from $x_1$ with constants $\epsilon_{x,i}, \epsilon_{g,i}$, and on $h$ from $y_1 = S^{-1}x_1$ with constants $\epsilon_{x,i}/s_i^2$ and $c^2s_i^2\epsilon_{g,i}$, both with the same $\rho$ and $\lambda$. If the oracle for $h$ returns $cSg$ whenever the oracle for $f$ at $Sy$ returns $g$ (true for exact gradients, and for stochastic gradients with shared samples), then $y_t = S^{-1}x_t$ for all $t$.

*Proof.* By induction, suppose $y_t = S^{-1}x_t$, $a^h_{t-1,i} = a_{t-1,i}/s_i^2$ and $b^h_{t-1,i} = c^2s_i^2b_{t-1,i}$. The gradient of $h$ is $cs_ig_{t,i}$ in coordinate $i$, so $b^h_{t,i} = c^2s_i^2b_{t,i}$ and

$$\Delta^h_{t,i} = -\lambda\frac{\sqrt{(a_{t-1,i} + \epsilon_{x,i})/s_i^2}}{\sqrt{c^2s_i^2(b_{t,i} + \epsilon_{g,i})}}\,cs_ig_{t,i} = \frac{1}{s_i}\Delta_{t,i}.$$

Then $a^h_{t,i} = a_{t,i}/s_i^2$ and $y_{t+1} = S^{-1}x_{t+1}$. $\square$

This is the exact form of Zeiler's claim that the update has the units of $x$. The other methods on this site do not have it. For SGD with step $\eta$, the step in $y_i$ is $-\eta cs_ig_i$, but the step that matches $x$ is $-\eta g_i/s_i$, so the path depends on $c$ and $s$. For RMSProp and Adam with $\epsilon = 0$, the step in $y$ equals the step in $x$, which is invariant to $c$ but wrong by the factor $s_i$. Newton's method is invariant to all invertible linear maps, which is the property Adadelta imitates on the diagonal. With Zeiler's single $\epsilon$ the invariance holds only approximately, when both $\epsilon$ terms are small compared with $a_t$ and $b_t$.

**Proposition 5 (constant slope).** Let $g_t = c \ne 0$ for all $t$ and $\lambda = 1$.

1. If $\epsilon_g = 0$, then $|\Delta_t| \ge \sqrt{\epsilon_x(1 + (1 - \rho)(t - 1))}$ for all $t \ge 1$, so the step grows without bound.
2. If $\epsilon_x = \epsilon_g = \epsilon > 0$, then $|\Delta_t| \to |c|$.

*Proof.* Here $b_t = (1 - \rho^t)c^2 \le c^2$ (Lemma 2 of the RMSProp page) and $\Delta_t^2 = (a_{t-1} + \epsilon_x)q_t$ with $q_t = c^2/(b_t + \epsilon_g)$.

Part 1. $q_t \ge 1$, so $\Delta_t^2 \ge a_{t-1} + \epsilon_x$ and $a_t \ge \rho a_{t-1} + (1 - \rho)(a_{t-1} + \epsilon_x) = a_{t-1} + (1 - \rho)\epsilon_x$. Hence $a_{t-1} \ge (t - 1)(1 - \rho)\epsilon_x$ and $\Delta_t^2 \ge \epsilon_x(1 + (1 - \rho)(t - 1))$.

Part 2. $q_t$ decreases to $q = c^2/(c^2 + \epsilon) < 1$, and $a_t = \lambda_ta_{t-1} + \mu_t$ with $\lambda_t = \rho + (1 - \rho)q_t \to \ell = \rho + (1 - \rho)q < 1$ and $\mu_t = (1 - \rho)q_t\epsilon \to \mu = (1 - \rho)q\epsilon$. The fixed point is $a^* = \mu/(1 - \ell) = q\epsilon/(1 - q) = c^2$. Put $e_t = a_t - a^*$. Then $e_t = \lambda_te_{t-1} + \delta_t$ with $\delta_t = (\lambda_t - 1)a^* + \mu_t \to (\ell - 1)a^* + \mu = 0$. Take $t_0$ with $\lambda_t \le \ell' < 1$ for $t \ge t_0$; then $|e_t| \le \ell'|e_{t-1}| + |\delta_t|$, and since $\delta_t \to 0$, $e_t \to 0$. So $\Delta_t^2 = (a_{t-1} + \epsilon)q_t \to (c^2 + \epsilon)q = c^2$. $\square$

Part 2 shows what the single $\epsilon$ does to the units: on a long constant slope, Adadelta becomes gradient descent with step $1$, because $a_t$ (units of $x^2$) settles at $c^2$ (units of $g^2$). The rate of approach is $1 - \ell = (1 - \rho)\epsilon/(c^2 + \epsilon)$ per step, so this takes about $c^2/((1 - \rho)\epsilon)$ steps, which is long for small $\epsilon$. Part 1 shows that with $\epsilon_g = 0$ the step grows on a slope like $\sqrt{t}$. Both say that Adadelta has no fixed step scale: its effective learning rate is set by its own history and by $\epsilon$.

**What is not proved.** There is no convergence rate for Adadelta in the convex, strongly convex or nonconvex stochastic settings in Zeiler's paper, and Propositions 3 and 5 show that its steps are not bounded by a fixed schedule, so the analyses of AdaGrad and AMSGrad do not apply. Its use rests on experiments: Zeiler reports good results on MNIST and on a large speech recognition task with $\rho = 0.95$ and $\epsilon = 10^{-6}$, with little sensitivity to these values.
