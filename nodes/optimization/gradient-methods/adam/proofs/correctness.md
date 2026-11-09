---
title: Adam's bias correction and step bound are exact, but its original convergence proof is wrong, and a convex counterexample shows the claimed regret bound fails
proves: [correctness, convergence-rate]
status: full
---

**Setting.** Adam with steps $\alpha_t > 0$, $\beta_1, \beta_2 \in [0, 1)$ and $\epsilon \ge 0$ starts from $x_1$ and $m_0 = v_0 = 0$. In round $t = 1, 2, \dots$ it receives a gradient $g_t$ and sets, for each coordinate (the index is dropped),

$$m_t = \beta_1m_{t-1} + (1 - \beta_1)g_t, \quad v_t = \beta_2v_{t-1} + (1 - \beta_2)g_t^2, \quad \hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t},$$

$$x_{t+1} = \Pi\Big(x_t - \alpha_t\frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}\Big),$$

where $\Pi$ is the clip to an interval in the online setting and the identity otherwise. This is Algorithm 1 of Kingma and Ba (2015), with an optional projection.

**Lemma 1 (bias correction).** $\hat{m}_t = \sum_{s=1}^tw_{t,s}g_s$ and $\hat{v}_t = \sum_{s=1}^tw'_{t,s}g_s^2$ with

$$w_{t,s} = \frac{(1 - \beta_1)\beta_1^{t-s}}{1 - \beta_1^t}, \qquad w'_{t,s} = \frac{(1 - \beta_2)\beta_2^{t-s}}{1 - \beta_2^t},$$

and both sets of weights are nonnegative and add up to $1$. Consequently:

1. $\hat{m}_t$ lies between the smallest and the largest of $g_1, \dots, g_t$, and $\hat{v}_t$ between the smallest and the largest of $g_1^2, \dots, g_t^2$.
2. If $g_t = c \ne 0$ for all $t$ and $\epsilon = 0$, then $\hat{m}_t = c$, $\hat{v}_t = c^2$, and with no projection every step is exactly $\alpha_t\operatorname{sign}(c)$.
3. If $g_1, g_2, \dots$ have a common mean $\mu$ and a common second moment $\nu$, then $\mathbb{E}\hat{m}_t = \mu$ and $\mathbb{E}\hat{v}_t = \nu$ for every $t$.

*Proof.* Unroll the recursions: $m_t = (1 - \beta_1)\sum_{s\le t}\beta_1^{t-s}g_s$, and $(1 - \beta_1)\sum_{s\le t}\beta_1^{t-s} = 1 - \beta_1^t$. The same holds for $v_t$. The three consequences follow because the weights are a probability vector. $\square$

Without the correction, $m_t$ and $v_t$ are biased toward $0$ by the factors $1 - \beta_1^t$ and $1 - \beta_2^t$. For $\beta_2 = 0.999$ the factor $1 - \beta_2^t$ is $0.001$ at $t = 1$, so the uncorrected first step would be about $\sqrt{1000}\,(1 - \beta_1) \approx 3.2$ times $\alpha$ for $\beta_1 = 0.9$.

**Lemma 2 (step bound).** Let $\epsilon = 0$ and $\gamma = \beta_1^2/\beta_2 < 1$. Then, with no projection, for every gradient sequence,

$$|x_{t+1} - x_t| \le \alpha_t\,\frac{1 - \beta_1}{1 - \beta_1^t}\sqrt{\frac{1 - \beta_2^t}{1 - \beta_2}}\sqrt{\frac{1 - \gamma^t}{1 - \gamma}}.$$

The right side is $\alpha_t$ at $t = 1$ and tends to $\alpha_t(1 - \beta_1)/\sqrt{(1 - \beta_2)(1 - \gamma)}$, which is about $7.27\,\alpha_t$ for $\beta_1 = 0.9$, $\beta_2 = 0.999$.

*Proof.* By the Cauchy-Schwarz inequality,

$$\Big|\sum_{s\le t}\beta_1^{t-s}g_s\Big| = \Big|\sum_{s\le t}\frac{\beta_1^{t-s}}{\beta_2^{(t-s)/2}}\cdot\beta_2^{(t-s)/2}g_s\Big| \le \Big(\sum_{j=0}^{t-1}\gamma^j\Big)^{1/2}\Big(\sum_{s\le t}\beta_2^{t-s}g_s^2\Big)^{1/2} = \sqrt{\frac{1 - \gamma^t}{1 - \gamma}}\sqrt{\frac{v_t}{1 - \beta_2}}.$$

So $|m_t|/\sqrt{v_t} \le (1 - \beta_1)\sqrt{(1 - \gamma^t)/((1 - \gamma)(1 - \beta_2))}$, and the step is $\alpha_t|m_t|\sqrt{1 - \beta_2^t}/((1 - \beta_1^t)\sqrt{v_t})$. A projection does not increase the distance moved. $\square$

Kingma and Ba (2015, Section 2.1) state the informal bound $|\Delta_t| \lesssim \alpha$ in common cases; Lemma 2 is a bound that holds for all sequences.

**Proposition 3 (the convex counterexample, with bias correction).** Fix $C \ge 2$, $\alpha > 0$, $\beta_1 = 0$, $\beta_2 = 1/(1 + C^2)$, $\alpha_t = \alpha/\sqrt{t}$ and $\epsilon = 0$, on $X = [-1, 1]$, with losses $f_t(x) = Cx$ for $t \equiv 1 \pmod 3$ and $f_t(x) = -x$ otherwise. The best fixed point is $u = -1$. If $x_t = 1$ for some $t \equiv 1 \pmod 3$ with $t \ge 4$, then $x_{t+3} = 1$. If $x_1 = x_4 = 1$, then $R_{3m}(-1) \ge 2(C - 2)m$ for every $m$, so the average regret stays at least $2(C - 2)/3$.

*Proof.* This follows the proof for RMSProp (Proposition 4 on that page), with the factor $1 - \beta_2^t$ added. As there, $v_s \le C^2$ for all $s$, $v_t \ge (1 - \beta_2)C^2$ in a round with $g_t = C$, and $v_{t+1}, v_{t+2} \le 2$ in the next two rounds.

The correction only enlarges $\hat{v}_t \ge v_t$, so the downward step in round $t$ is at most $\alpha_t\sqrt{1 + C^2}/C$. In rounds $t + 1$ and $t + 2$, $\hat{v} \le 2/(1 - \beta_2^{t+1})$, so each upward step, before the clip, is at least $\alpha_{t+2}\sqrt{1 - \beta_2^{t+1}}/\sqrt{2}$. As in the RMSProp proof, $x_{t+3} = 1$ when

$$\sqrt{2}\sqrt{\frac{t}{t + 2}}\sqrt{1 - \beta_2^{t+1}} \ge \sqrt{1 + 1/C^2}.$$

For $t \ge 4$ and $C \ge 2$, $\beta_2 \le 1/5$ and $t + 1 \ge 5$, so the left side is at least $1.1547 \cdot \sqrt{1 - 5^{-5}} > 1.154$, and the right side is at most $1.1180$. The regret count is the same as for RMSProp: each period that starts at $1$ adds at least $2(C - 2)$. $\square$

For $C = 3$ and $\alpha \in \{0.1, 0.5, 2\}$ the condition $x_4 = 1$ holds, and the test checks it. Reddi, Kale and Kumar (2018, Theorem 1) prove non-convergence for this construction without the condition, for Adam with $\beta_1 = 0$.

**Where the original proof fails.** Kingma and Ba (2015, Theorem 4.1 and Corollary 4.2) claim that, for bounded gradients, bounded iterates, $\beta_1^2/\sqrt{\beta_2} < 1$, $\alpha_t = \alpha/\sqrt{t}$ and $\beta_{1,t} = \beta_1\lambda^{t-1}$, the regret is $O(\sqrt{T})$, so $R_T/T \to 0$. The example above has bounded gradients ($|g_t| \le C$), bounded iterates, $\beta_1 = 0$ (so $\beta_{1,t} = 0$ for every $\lambda$) and $\alpha_t = \alpha/\sqrt{t}$, yet $R_T/T$ stays at least $2(C - 2)/3$. Reddi, Kale and Kumar (2018, Section 3) locate the error. Regret proofs for methods with per-coordinate steps $\eta_{t,i}$ telescope the terms $\big(\frac{1}{\eta_{t,i}} - \frac{1}{\eta_{t-1,i}}\big)(x_{t,i} - u_i)^2$ and bound their sum by $D^2/\eta_{T,i}$. This needs $1/\eta_{t,i} = \sqrt{\hat{v}_{t,i}}/\alpha_t$ to be nondecreasing in $t$. For SGD with decreasing steps and for AdaGrad it is; for Adam and RMSProp it is not. In the example with $C = 3$, $\hat{v}$ is about $8.21$ after each large gradient and about $1.07$ two rounds later, so $1/\eta$ falls by a factor of about $2.8$ in every period.

**What is known now.** All statements below are theorems in the cited papers, under the assumptions given.

- **Fixes with a proof for online convex problems.** AMSGrad uses $\hat{v}_t = \max(\hat{v}_{t-1}, v_t)$ in the denominator, which makes $1/\eta_{t,i}$ nondecreasing, and has $O(\sqrt{T})$ regret on bounded convex domains (Reddi, Kale and Kumar 2018, Theorem 4, with a decreasing $\beta_{1,t}$). AdaGrad (and RMSProp with $\beta_{2,t} = 1 - 1/t$) also satisfies the condition.
- **Counterexamples for every constant pair.** For any constant $\beta_1 < \sqrt{\beta_2}$ there is a stochastic convex problem on which Adam does not converge to the optimum (Reddi, Kale and Kumar 2018, Theorem 3). So no theorem can give convergence for all convex problems with $\beta_1, \beta_2$ fixed in advance.
- **Nonconvex rates with problem-dependent settings.** Défossez, Bottou, Bach and Usunier (2022) prove, for an $L$-smooth $F$ bounded below with stochastic gradients bounded by $R$ in each coordinate, a bound on $\mathbb{E}\lVert\nabla F(x_\tau)\rVert^2$ for a random iterate $x_\tau$. With $\beta_2 = 1 - 1/N$ and $\alpha \propto 1/\sqrt{N}$ for a run of $N$ steps, it is $O(d\ln N/\sqrt{N})$; with a constant $\beta_2$ and $\alpha$, the bound has a term that does not shrink, so it only shows convergence to a neighbourhood.
- **Constant $\beta_2$ close to $1$.** Zhang, Chen, Shi, Sun and Luo (2022) show, for finite sums with random shuffling and a growth condition on the gradients, that Adam with $\beta_1 < \sqrt{\beta_2}$ and $\beta_2$ above a threshold that depends on the number of terms $n$ converges to a neighbourhood of stationary points, and to stationary points when the gradient noise vanishes at the optimum. They also show divergence for small $\beta_2$. This matches practice, where $\beta_2 = 0.999$ is close to $1$, and it is consistent with the counterexamples, because there $\beta_2$ is fixed before the problem.
- **Other conditions.** Chen, Liu, Sun and Hong (2019) give sufficient conditions for a class of Adam-type methods, including AMSGrad, with rate $O(\ln T/\sqrt{T})$ on smooth nonconvex problems. Zou, Shen, Jie, Zhang and Liu (2019) give a sufficient condition with $\beta_{2,t} \to 1$. Li, Rakhlin and Jadbabaie (2023) prove convergence under a relaxed smoothness condition without a bound on the gradients.

**What is only practice.** The default settings $\alpha = 10^{-3}$, $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$ with a constant or hand-made step schedule are not covered by a convergence theorem for general convex or nonconvex problems. Their success in training neural networks, and the claim that the defaults need little tuning, rest on experiments.
