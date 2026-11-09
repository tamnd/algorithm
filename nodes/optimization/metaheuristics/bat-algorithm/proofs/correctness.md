---
title: The bat algorithm keeps its points in the box, its points only improve, its loudness and pulse rate follow closed forms, it returns the best point it evaluated, and its velocity term has no damping
proves: [correctness]
status: full
---

We use the pseudocode of the page for minimizing $f$ on the box $B = \prod_{k=1}^D [\ell_k, u_k]$ with $\ell_k < u_k$, $n \ge 1$ and $0 < \alpha \le 1$. Let $x_i$, $v_i$, $A_i$ and $r_i$ be the point, velocity, loudness and pulse rate of bat $i$, and $x^*$ the stored best point. The frequency drawn in line L3 is $q$.

**Claim 1 (feasibility).** Every point and every evaluated proposal lies in $B$.

*Proof.* Line L1 draws the points in $B$, and line L5 clips every proposal before it is evaluated. A point is only ever set to a start point or to an evaluated proposal. $\square$

**Claim 2 (monotone bats).** For each $i$, $f(x_i)$ never increases, and every change of $x_i$ lowers it strictly.

*Proof.* Only line L6 changes $x_i$, and only when $f(y) < f(x_i)$. $\square$

**Claim 3 (loudness and pulse rate).** If bat $i$ has accepted $k_i$ proposals, the last one in iteration $t_i$, then $A_i = \alpha^{k_i} A_0$ and $r_i = r_0 (1 - e^{-\gamma t_i})$, with $r_i = 0$ when $k_i = 0$. So an improving proposal of bat $i$ is accepted with probability $\alpha^{k_i} A_0$, which does not increase with $k_i$.

*Proof.* Line L1 sets $A_i = A_0$ and $r_i = 0$. Line L6 multiplies $A_i$ by $\alpha$ and sets $r_i$ to $r_0 (1 - e^{-\gamma t})$ at each acceptance, and no other line changes them. The acceptance test draws a uniform number independent of the rest, and it is below $A_i$ with probability $\min(A_i, 1)$. $\square$

**Claim 4 (the best point).** After line L1 and after each proposal, $f(x^*) = \min\{f(z) : z \text{ evaluated so far}\}$, and $x^*$ is one of these points.

*Proof.* After line L1, $x^*$ is the best start point. Each proposal is evaluated once in line L5, and line L7 replaces $x^*$ by it when it is better. This holds whether line L6 accepts the proposal or not. $\square$

**Claim 5 (the velocity grows while a bat waits).** Suppose $x_i$ and $x^*$ do not change from iteration $s$ to iteration $t > s$. Then
$$v_i^{(t)} = v_i^{(s)} + Q\,(x_i - x^*), \qquad Q = \sum_{\tau = s+1}^{t} q_\tau .$$
If $q_{\min} > 0$, then $Q \ge (t - s) q_{\min}$, so in every coordinate $k$ with $x_{ik} \ne x^*_k$ the unclipped velocity proposal $x_{ik} + v_{ik}$ leaves the interval $[\ell_k, u_k]$ within $\lfloor (w_k + |v^{(s)}_{ik}|) / (q_{\min} |x_{ik} - x^*_k|) \rfloor + 1$ iterations, where $w_k = u_k - \ell_k$, and is then clipped to its border.

*Proof.* Line L3 adds $q_\tau (x_i - x^*)$ to $v_i$ in each iteration, whether the proposal is accepted or not, and $x_i - x^*$ is fixed by assumption. Summing gives the formula. In coordinate $k$, $|v_{ik}| \ge Q |x_{ik} - x^*_k| - |v^{(s)}_{ik}| \ge (t - s) q_{\min} |x_{ik} - x^*_k| - |v^{(s)}_{ik}|$. Since $x_{ik} \in [\ell_k, u_k]$, the proposal leaves the interval once $|v_{ik}| > w_k$, which holds as soon as $t - s$ exceeds $(w_k + |v^{(s)}_{ik}|) / (q_{\min} |x_{ik} - x^*_k|)$. $\square$

With $q_{\min} = 0$ the same holds in expectation, since $E[Q] = (t - s)(q_{\min} + q_{\max})/2$. The proposals of a bat that does not move therefore end on the border of the box. A negative $q$ gives the same growth with the opposite sign: the proposal overshoots $x^*$ to the far border.

**Claim 6 (the velocity part is PSO with inertia 1, and it has no damping).** Fix $x^*$, take $r_i = 1$ so that line L4 never acts, and suppose every proposal is accepted and stays in the box. Then lines L3 and L6 are the PSO update $v \leftarrow w v + c_2 \rho (x^* - x)$, $x \leftarrow x + v$, with $w = 1$, no personal-best term, and $c_2 \rho = -q$. For a fixed $q$, the error $e_t = x_{ik}^{(t)} - x^*_k$ in each coordinate satisfies
$$e_{t+1} = (2 + q)\, e_t - e_{t-1}.$$
If $-4 < q < 0$, the form $P_t = e_t^2 - (2 + q) e_t e_{t-1} + e_{t-1}^2$ is positive definite and constant, so $e_t$ stays bounded and does not tend to 0 unless $e_0 = e_1 = 0$. If $q > 0$, which is the case for the frequency range $[q_{\min}, q_{\max}]$ with $q_{\min} \ge 0$ of the paper, then $e_t$ grows like $\lambda^t$ with $\lambda = \big(2 + q + \sqrt{q^2 + 4q}\big)/2 > 1$ for almost every start.

*Proof.* Write $\tau = 2 + q$. The update is $v_{t+1} = v_t + q e_t$ and $e_{t+1} = e_t + v_{t+1}$, which is the PSO form with $w = 1$ and $c_2 \rho = -q$. Then $e_{t+1} - e_t = v_{t+1} = v_t + q e_t = (e_t - e_{t-1}) + q e_t$, which is the recurrence. For the invariant, $P_{t+1} = e_{t+1}^2 - \tau e_{t+1} e_t + e_t^2 = e_{t+1}(e_{t+1} - \tau e_t) + e_t^2 = e_t^2 - e_{t+1} e_{t-1}$, and $P_t = e_t^2 - e_{t-1}(\tau e_t - e_{t-1}) = e_t^2 - e_{t-1} e_{t+1}$, so $P_{t+1} = P_t$. The form $a^2 - \tau a b + b^2$ is positive definite exactly when $|\tau| < 2$, that is $-4 < q < 0$, and then $P_t = P_1 > 0$ unless $e_0 = e_1 = 0$, so $e_t$ cannot tend to 0. If $q > 0$, then $\tau > 2$, and the characteristic roots $\lambda$ and $1/\lambda$ of $z^2 - \tau z + 1$ are real with $\lambda > 1$. The solution is $a \lambda^t + b \lambda^{-t}$, which grows unless $a = 0$, and $a = 0$ holds only on a line of starts. $\square$

This matches the stability analysis of PSO by Clerc and Kennedy (2002) and Poli (2009), in which convergence of the deterministic and order-1 dynamics needs $|w| < 1$. With $w = 1$ the velocity term alone never converges.

**Remark.** No claim here says that $x^*$ approaches a global minimizer. By Claims 5 and 6 the velocity proposals do not settle near $x^*$, and the local walk of line L4 has step size equal to the mean loudness, which falls only when proposals are accepted, while by Claim 3 acceptance itself becomes rarer as the loudness falls. $\blacksquare$
