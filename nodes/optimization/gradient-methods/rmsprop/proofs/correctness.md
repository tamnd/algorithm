---
title: RMSProp has bounded steps and reduces to AdaGrad for one schedule, but with a constant decay it can fail to converge on a convex problem
proves: [correctness, convergence-rate]
status: full
---

**Setting.** RMSProp with steps $\eta_t > 0$, decay factors $\beta_t \in [0, 1)$ and $\epsilon \ge 0$ starts from $x_1$ and $v_0 = 0$. In round $t = 1, 2, \dots$ it receives a gradient $g_t$ and sets, for each coordinate $i$,

$$v_{t,i} = \beta_tv_{t-1,i} + (1 - \beta_t)g_{t,i}^2, \qquad x_{t+1,i} = \Pi_i\Big(x_{t,i} - \eta_t\frac{g_{t,i}}{\sqrt{v_{t,i}} + \epsilon}\Big),$$

where $\Pi_i$ is the clip to an interval $[l_i, h_i]$ (or the identity when there is no box), and $x_{t+1,i} = x_{t,i}$ when $v_{t,i} = 0$. The usual method has constant $\beta_t = \beta$ and constant $\eta_t = \eta$. The results below cover what is proved for the method itself. Results from the literature are listed at the end, with their assumptions.

**Lemma 1 (bounded steps).** For every gradient sequence and every $t$, $|x_{t+1,i} - x_{t,i}| \le \eta_t/\sqrt{1 - \beta_t}$.

*Proof.* $v_{t-1,i} \ge 0$, so $v_{t,i} \ge (1 - \beta_t)g_{t,i}^2$. Hence $|g_{t,i}|/(\sqrt{v_{t,i}} + \epsilon) \le |g_{t,i}|/\sqrt{v_{t,i}} \le 1/\sqrt{1 - \beta_t}$ when $v_{t,i} > 0$. The clip to an interval that contains $x_{t,i}$ does not increase the distance moved. $\square$

So the step in each coordinate does not depend on the scale of the gradient: multiplying all gradients in coordinate $i$ by $c > 0$ multiplies $v_{\cdot,i}$ by $c^2$ and, for $\epsilon = 0$, leaves the iterates unchanged.

**Lemma 2 (constant gradient and the start-up bias).** Let $\beta_t = \beta$, $\eta_t = \eta$, $\epsilon = 0$ and $g_{t,i} = c \ne 0$ for all $t$. Then $v_{t,i} = (1 - \beta^t)c^2$ and, with no box, $x_{t,i} - x_{t+1,i} = \operatorname{sign}(c)\,\eta/\sqrt{1 - \beta^t}$.

*Proof.* By induction, $v_{t,i} = (1 - \beta)c^2\sum_{s=0}^{t-1}\beta^s = (1 - \beta^t)c^2$. Put this in the update. $\square$

The first step is $\eta/\sqrt{1 - \beta}$, which is $3.16\eta$ for $\beta = 0.9$ and $10\eta$ for $\beta = 0.99$; the step falls to $\eta$ only as $\beta^t \to 0$. Adam removes this factor by dividing $v_t$ by $1 - \beta^t$.

**Proposition 3 (AdaGrad is a special case).** Let $\beta_t = 1 - 1/t$, $\eta_t = \eta/\sqrt{t}$ and $\epsilon = 0$. Then the iterates of RMSProp are the iterates of diagonal AdaGrad with step $\eta$. Hence, on a box with sides at most $D_\infty$ and convex losses, RMSProp with this schedule has regret at most $(D_\infty^2/(2\eta) + \eta)\sum_i\lVert g_{1:T,i}\rVert_2$.

*Proof.* With $\beta_t = 1 - 1/t$, $tv_{t,i} = (t - 1)v_{t-1,i} + g_{t,i}^2$, so $tv_{t,i} = s_{t,i} = \sum_{s\le t}g_{s,i}^2$. Then $\eta_t/\sqrt{v_{t,i}} = (\eta/\sqrt{t})/\sqrt{s_{t,i}/t} = \eta/\sqrt{s_{t,i}}$, which is the AdaGrad step, and $v_{t,i} = 0$ exactly when $s_{t,i} = 0$. The regret bound is the theorem on the AdaGrad page. $\square$

So RMSProp has a proved regret bound when $\beta_t \to 1$ fast enough that $v_t$ remembers all past gradients. The next result shows that a constant $\beta$ can break convergence, even on a one-dimensional linear problem.

**Proposition 4 (non-convergence with a constant decay).** Fix $C \ge 2$, $\alpha > 0$, $\beta = 1/(1 + C^2)$, $\eta_t = \alpha/\sqrt{t}$ and $\epsilon = 0$ on $X = [-1, 1]$. Let the losses be $f_t(x) = Cx$ for $t \equiv 1 \pmod 3$ and $f_t(x) = -x$ otherwise. Over each period of three rounds the losses add up to $(C - 2)x$, so the best fixed point is $u = -1$. If $x_t = 1$ for some $t \equiv 1 \pmod 3$ with $t \ge 4$, then $x_{t+3} = 1$. Consequently, if $x_1 = x_4 = 1$, then $x_t = 1$ at the start of every period and $R_T(-1) \ge 2(C - 2)\lfloor T/3\rfloor$, so the average regret does not go to $0$.

*Proof.* All $g_s^2$ lie in $\{1, C^2\}$ and $v_s$ is a convex combination of $0$ and past $g^2$ values, so $v_s \le C^2$ for every $s$.

The first round of the period has $g_t = C$. As in Lemma 1, $v_t \ge (1 - \beta)C^2$, so the downward step is at most $\eta_t/\sqrt{1 - \beta} = \eta_t\sqrt{1 + C^2}/C$, and $x_{t+1} \ge 1 - \eta_t\sqrt{1 + C^2}/C$.

The next two rounds have $g = -1$. Here $v_{t+1} = \beta v_t + (1 - \beta) \le \beta C^2 + 1 - \beta = 2C^2/(1 + C^2) \le 2$, and $v_{t+2} = \beta v_{t+1} + 1 - \beta \le 2$. So each upward step, before the clip, is at least $\eta_{t+1}/\sqrt{2}$ and $\eta_{t+2}/\sqrt{2}$. If the clip at $1$ is active after round $t + 1$, then $x_{t+2} = 1$ and $x_{t+3} = 1$. Otherwise

$$x_{t+3} \ge \min\Big(1,\ 1 - \frac{\alpha}{\sqrt{t}}\frac{\sqrt{1 + C^2}}{C} + \frac{2}{\sqrt{2}}\frac{\alpha}{\sqrt{t + 2}}\Big),$$

and the right side is $1$ when $\sqrt{2}\sqrt{t/(t + 2)} \ge \sqrt{1 + 1/C^2}$. For $t \ge 4$ the left side is at least $\sqrt{2}\sqrt{2/3} = 1.1547$, and for $C \ge 2$ the right side is at most $\sqrt{1.25} = 1.1180$. So $x_{t+3} = 1$.

For the regret, a period that starts at $x_t = 1$ has loss $C - x_{t+1} - x_{t+2} \ge C - 2$, and the comparator $u = -1$ has loss $-C + 2$ in that period. So each such period adds at least $2(C - 2)$ to the regret against $-1$, and after $m$ full periods $R_{3m}(-1) \ge 2(C - 2)m$. Hence $R_{3m}(-1)/(3m) \ge 2(C - 2)/3 > 0$ for every $m$ when $C > 2$. $\square$

The condition $x_4 = 1$ holds for $C = 3$ and $\alpha = 0.5$; the test checks it and then checks that every period starts at $1$. Reddi, Kale and Kumar (2018, Theorem 1) prove non-convergence for this construction without the condition, for Adam with $\beta_1 = 0$, which is RMSProp with $\eta_t = \alpha/\sqrt{t}$. Their Theorems 2 and 3 extend it to any constant $\beta_1 < \sqrt{\beta_2}$ and to a stochastic problem. The fix they propose, AMSGrad, uses $\max(\hat{v}_{t-1}, v_t)$ so that the effective step never increases.

**What else is proved, and under which assumptions.**

- Mukkamala and Hein (2017) prove $O(\log T)$ regret for strongly convex losses for a variant with $\beta_t = 1 - \gamma/t$ and $\eta_t = \alpha/t$, which is again close to AdaGrad.
- Zou, Shen, Jie, Zhang and Liu (2019) give a sufficient condition for stochastic nonconvex convergence of RMSProp and Adam: $\beta_t \to 1$ and $\eta_t = \alpha/\sqrt{t}$ with a growth condition that includes $\beta_t = 1 - 1/t$. The rate is $O(\log T/\sqrt{T})$ for the minimum expected gradient norm.
- De, Mukherjee and Ullah (2018) prove convergence of deterministic RMSProp to a point with a small gradient on smooth functions with bounded gradients, under conditions on $\eta$ and $\beta$.
- Shi, Li, Hong and Sun (2021) and Zhang, Chen, Shi, Sun and Luo (2022) consider finite sums with random shuffling. When $\beta$ is close enough to $1$, depending on the number of terms $n$, RMSProp and Adam with constant $\beta$ converge to a neighbourhood of stationary points, and to stationary points under a strong growth condition. Their results do not contradict Proposition 4, because the order of choice is different. In Proposition 4 the problem is built after $\beta$ is fixed. In those results the problem is fixed first and then $\beta$ is taken close enough to $1$.

So for every constant $\beta$ there is a convex problem on which RMSProp fails (Reddi, Kale and Kumar 2018, Theorem 3, with $\beta_1 = 0$), and the guarantees above need either $\beta_t \to 1$ or a $\beta$ tuned to the problem. With a constant $\beta$ such as $0.9$ or $0.99$ and a constant or hand-made step schedule, as in common use, the good results in training neural networks are an empirical fact, not a theorem.
