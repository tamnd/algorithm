---
title: On the three-step counterexample, Adam goes to the worst point and AMSGrad to the best
proves: [correctness]
status: full
---

**Setting.** The domain is $F = [-1, 1]$ and the losses are $f_t(x) = Cx$ when $t \bmod 3 = 1$ and $f_t(x) = -x$ otherwise, with $C > 2$. The sum of the three losses of a period is $(C - 2)x$, so the best fixed point is $x^* = -1$. Both methods use $\beta_1 = 0$ (so $m_t = g_t$), $\beta_2 = 1/(1 + C^2)$, $\epsilon = 0$, $v_0 = 0$, no bias correction, $\alpha_t = \alpha/\sqrt{t}$ with $\alpha > 0$, and the projection $\Pi(y) = \min(1, \max(-1, y))$. Adam steps by $\alpha_t g_t/\sqrt{v_t}$ and AMSGrad by $\alpha_t g_t/\sqrt{\hat{v}_t}$ with $\hat{v}_t = \max(\hat{v}_{t-1}, v_t)$, $\hat{v}_0 = 0$. Period $k \ge 0$ is the steps $3k+1, 3k+2, 3k+3$.

**Lemma 1.** $0 \le v_t \le C^2$ for all $t$, and $v_t \ge (1 - \beta_2)C^2$ when $t \bmod 3 = 1$.

*Proof.* $v_t = \beta_2 v_{t-1} + (1 - \beta_2)g_t^2$ is a convex combination of $v_{t-1}$ and $g_t^2 \le C^2$, and $v_0 = 0$, so $0 \le v_t \le C^2$ by induction. When $t \bmod 3 = 1$, $g_t^2 = C^2$ and $\beta_2 v_{t-1} \ge 0$. $\square$

**Claim 1 (Adam).** There is a period $k_1$ such that $x_{3k+1} = 1$ for all $k \ge k_1$. The average regret tends to $2(C - 2)/3 > 0$.

*Proof.* Write $s = \sqrt{1 + C^2}/C$, so $1 - \beta_2 = C^2/(1 + C^2) = 1/s^2$ and $\beta_2 = 1/(1 + C^2)$.

*Step sizes.* At $t = 3k+1$ the step is downward with size $D_k = \alpha_t C/\sqrt{v_t} \le \alpha_t C/\sqrt{(1 - \beta_2)C^2} = s\,\alpha_{3k+1}$ by Lemma 1. At $t = 3k+2$, $v_t = (1 - \beta_2) + \beta_2 v_{t-1} \le (1 - \beta_2) + \beta_2 C^2 = 2C^2/(1 + C^2)$, so the upward step is $U_k = \alpha_t/\sqrt{v_t} \ge \alpha_{3k+2}\,s/\sqrt2$. At $t = 3k+3$, $v_t = (1 - \beta_2) + \beta_2 v_{t-1} \le (C^2 + 2)/(1 + C^2)$, using $v_{t-1} < 2$, so the upward step is $U'_k \ge \alpha_{3k+3}\sqrt{(1 + C^2)/(C^2 + 2)} = \alpha_{3k+3}\, s\, C/\sqrt{C^2 + 2}$.

*Net drift.* Let $r_k = \alpha_{3k+3}/\alpha_{3k+1} = \sqrt{(3k+1)/(3k+3)}$, which is at least $\sqrt{2/3} > 0.816$ for $k \ge 1$. Since $\alpha_{3k+2} \ge \alpha_{3k+3}$ and $C/\sqrt{C^2 + 2} > 2/\sqrt6 > 0.816$ for $C > 2$,
$$U_k + U'_k - D_k \ge s\,\alpha_{3k+1}\Bigl(r_k\bigl(\tfrac{1}{\sqrt2} + \tfrac{C}{\sqrt{C^2+2}}\bigr) - 1\Bigr) \ge s\,\alpha_{3k+1}\bigl(0.816 \cdot 1.523 - 1\bigr) > 0.24\, s\,\alpha_{3k+1} =: \delta_k$$
for $k \ge 1$.

*Projection.* In period $k$, let $y_1 = \Pi(x_{3k+1} - D_k) \ge x_{3k+1} - D_k$. The next two steps go up, and the projection can only cut them at $1$. If no cut happens, $x_{3k+4} = y_1 + U_k + U'_k \ge x_{3k+1} + \delta_k$; if a cut happens, $x_{3k+4} = 1$. So $x_{3k+4} \ge \min(1, x_{3k+1} + \delta_k)$ for $k \ge 1$.

*Conclusion.* $\sum_k \delta_k = 0.24\,s\,\alpha\sum_k (3k+1)^{-1/2} = \infty$ and $x \ge -1$, so the iterates cannot stay below $1$ at all period starts: some $k_1$ has $x_{3k_1+1} = 1$. Then $x_{3k+4} \ge \min(1, 1 + \delta_k) = 1$ for every $k \ge k_1$. Inside such a period, $x_{3k+2} \ge 1 - s\alpha_{3k+1}$ and $x_{3k+3} \ge x_{3k+2}$, so the regret of the period is
$$C(x_{3k+1} + 1) - (x_{3k+2} + 1) - (x_{3k+3} + 1) \ge 2C - 4 = 2(C - 2),$$
since $x_{3k+2}, x_{3k+3} \le 1$. The regret of each later period is at least $2(C-2)$, and at most $2(C - 2) + O(\alpha_{3k+1})$ since $x_{3k+2}, x_{3k+3} \ge 1 - s\alpha_{3k+1}$. So $R_T/T \to 2(C - 2)/3$. $\square$

**Claim 2 (AMSGrad).** $x_t \to -1$, and the average regret tends to $0$.

*Proof.* By Lemma 1, $\hat{v}_t \le C^2$, and $\hat{v}_t \ge v_1 = (1 - \beta_2)C^2 > 0$ for $t \ge 1$. In period $k$ the downward step is $D_k = \alpha_{3k+1}C/\sqrt{\hat{v}_{3k+1}}$. The upward steps are $\alpha_{3k+2}/\sqrt{\hat{v}_{3k+2}}$ and $\alpha_{3k+3}/\sqrt{\hat{v}_{3k+3}}$; since $\alpha_t$ decreases and $\hat{v}_t$ does not, each is at most $\alpha_{3k+1}/\sqrt{\hat{v}_{3k+1}}$. So without projection the period moves $x$ down by at least
$$\delta'_k = \frac{(C - 2)\,\alpha_{3k+1}}{\sqrt{\hat{v}_{3k+1}}} \ge \frac{(C - 2)\,\alpha_{3k+1}}{C}.$$

*Projection.* Let $y_1 = \Pi(x_{3k+1} - D_k)$. The two upward steps can only be cut at $1$, which makes $x$ smaller, so $x_{3k+4} \le y_1 + 2\alpha_{3k+1}/\sqrt{\hat{v}_{3k+1}}$. If $y_1 = x_{3k+1} - D_k$, this gives $x_{3k+4} \le x_{3k+1} - \delta'_k$. If $y_1 = -1$, it gives $x_{3k+4} \le -1 + e_k$ with $e_k = 2\alpha_{3k+1}/\sqrt{(1 - \beta_2)C^2} \to 0$. So $x_{3k+4} \le \max(x_{3k+1} - \delta'_k,\ -1 + e_k)$.

*Conclusion.* Fix $\varepsilon > 0$ and $K$ with $e_k < \varepsilon$ for $k \ge K$. If $x_{3k+1} > -1 + \varepsilon$ for all $k \ge K$, the bound forces $x_{3k+4} \le x_{3k+1} - \delta'_k$ for all these $k$, and since $\sum_k \delta'_k = \infty$, $x$ would go below $-1$, which is impossible. So $x_{3k+1} \le -1 + \varepsilon$ for some $k \ge K$, and then for all later $k$, because $\max(-1 + \varepsilon - \delta'_k, -1 + e_k) \le -1 + \varepsilon$. Inside a period $x$ moves by at most $(C + 2)\alpha_{3k+1}/\sqrt{(1 - \beta_2)C^2} \to 0$. Hence $x_t \to -1$. The regret of step $t$ is at most $C\lvert x_t + 1\rvert$, which tends to $0$, so $R_T/T \to 0$ by the Cesàro mean. $\square$

**Claim 3 (the effective step).** For any losses, if $\alpha_t$ is nonincreasing then $\alpha_t/\sqrt{\hat{v}_{t,i}}$ is nonincreasing in $t$ for each coordinate $i$ with $\hat{v}_{t,i} > 0$.

*Proof.* $\hat{v}_{t,i} = \max(\hat{v}_{t-1,i}, v_{t,i}) \ge \hat{v}_{t-1,i}$, so the denominator does not decrease and the numerator does not increase. $\square$

Claim 3 is the property that the regret proof of Adam needed and that Adam lacks: in the counterexample, Adam's effective step after the two small gradients is larger than after the large one. The general $O(\sqrt{T})$ type regret bound of AMSGrad is Theorem 4 of Reddi, Kale and Kumar (2018); its proof uses Claim 3 to make the sum of the terms $\sqrt{\hat{v}_{t,i}}/\alpha_t - \sqrt{\hat{v}_{t-1,i}}/\alpha_{t-1} \ge 0$ telescope. Tran and Phong (2019) found a gap in how that proof handles a varying $\beta_{1,t}$ and gave a corrected proof.
