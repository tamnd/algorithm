---
title: The relative trigger makes the linear loop exponentially stable and keeps the inter-event times above tau*
proves: [correctness, termination]
status: full
---

**Setting.** The plant is $x' = Ax + Bu$ with $x \in \mathbb{R}^n$, and the controller applies $u(t) = -K x(t_k)$ for $t \in [t_k, t_{k+1})$. The closed-loop matrix $A_{cl} = A - BK$ is Hurwitz. The error is $e(t) = x(t_k) - x(t)$, and the next event is

$$t_{k+1} = \inf\{t > t_k : \|e(t)\| \ge \sigma \|x(t)\|\},$$

with $\|\cdot\|$ the Euclidean norm and the induced matrix 2-norm. $Q \succ 0$, and $P \succ 0$ solves $A_{cl}^T P + P A_{cl} = -Q$. Let $\alpha = \|A_{cl}\|$ and $\beta = \|BK\|$. The template lines L1 to L7 implement this trigger. If $x(t_k) = 0$, then $u = 0$ and $x$ stays at $0$, so no more events are needed; the statements below concern $x(t_k) \ne 0$.

**Lemma 1 (the closed loop with the error).** On $[t_k, t_{k+1})$, $x' = A_{cl} x - BK e$ and $e' = -x'$.

*Proof.* $x' = Ax - BK x(t_k) = Ax - BK(x + e)$, and $x(t_k)$ is constant on the interval. $\blacksquare$

**Lemma 2 (Lyapunov equation).** For a Hurwitz $A_{cl}$ and $Q \succ 0$, the equation $A_{cl}^T P + P A_{cl} = -Q$ has one solution, and it is positive definite. The function `lyapunov` solves its Kronecker form $(I \otimes A_{cl}^T + A_{cl}^T \otimes I)\operatorname{vec}(P) = -\operatorname{vec}(Q)$.

*Proof.* The eigenvalues of the Kronecker matrix are $\lambda_i + \lambda_j$ for eigenvalues $\lambda_i, \lambda_j$ of $A_{cl}$; their real parts are negative, so the matrix is invertible and the solution is unique. The integral $P = \int_0^\infty e^{A_{cl}^T t} Q e^{A_{cl} t}\, dt$ converges, solves the equation, and has $x^T P x > 0$ for $x \ne 0$. The Kronecker form follows from $\operatorname{vec}(MXN) = (N^T \otimes M)\operatorname{vec}(X)$. $\blacksquare$

**Theorem 1 (exponential stability).** If $\sigma < \bar\sigma = \lambda_{\min}(Q) / (2\|PBK\|)$, then with $c = \lambda_{\min}(Q) - 2\sigma\|PBK\| > 0$,

$$\|x(t)\| \le \sqrt{\lambda_{\max}(P) / \lambda_{\min}(P)}\; e^{-c t / (2\lambda_{\max}(P))} \|x(0)\| \quad \text{for all } t \ge 0,$$

so the origin is globally exponentially stable.

*Proof.* By the definition of $t_{k+1}$, $\|e(t)\| \le \sigma \|x(t)\|$ on $[t_k, t_{k+1}]$. With $V = x^T P x$ and Lemma 1,

$$V' = x^T (A_{cl}^T P + P A_{cl}) x - 2 x^T P B K e \le -\lambda_{\min}(Q)\|x\|^2 + 2\|PBK\|\,\|x\|\,\|e\| \le -c\|x\|^2 \le -\frac{c}{\lambda_{\max}(P)} V.$$

$V$ is continuous across events, because $x$ is. So $V(t) \le e^{-ct/\lambda_{\max}(P)} V(0)$ on every interval that the event times cover, and $\lambda_{\min}(P)\|x\|^2 \le V \le \lambda_{\max}(P)\|x\|^2$ gives the bound. Theorem 2 shows that the event times do not accumulate, so they cover $[0, \infty)$. $\blacksquare$

**Theorem 2 (inter-event times).** For every $k$, $t_{k+1} - t_k \ge \tau^*$, where

$$\tau^* = \frac{1}{\alpha - \beta} \ln\frac{\alpha(1 + \sigma)}{\alpha + \beta\sigma} \quad (\alpha \ne \beta), \qquad \tau^* = \frac{\sigma}{\alpha(1 + \sigma)} \quad (\alpha = \beta).$$

*Proof.* Let $y = \|e\| / \|x\|$ on $[t_k, t_{k+1})$. Here $x \ne 0$: $y$ is continuous where $x \ne 0$, $y(t_k) = 0$, and $y$ would tend to infinity as $x \to 0$, so the event comes first. Wherever $e \ne 0$, $\|e\|' \le \|e'\| = \|x'\|$ and $\|x\|' \ge -\|x'\|$, so

$$y' \le \frac{\|x'\|}{\|x\|}(1 + y) \le \frac{\alpha\|x\| + \beta\|e\|}{\|x\|}(1 + y) = (\alpha + \beta y)(1 + y),$$

and the same bound holds for the upper right Dini derivative where $e = 0$. Let $z$ solve $z' = (\alpha + \beta z)(1 + z)$, $z(0) = 0$. By the comparison lemma, $y(t_k + s) \le z(s)$. Separating the variables, with $\frac{1}{(\alpha + \beta z)(1 + z)} = \frac{1}{\alpha - \beta}\left(\frac{1}{1 + z} - \frac{\beta}{\alpha + \beta z}\right)$, gives the time for $z$ to go from $0$ to $\sigma$:

$$s(\sigma) = \frac{1}{\alpha - \beta}\Big[\ln(1 + z) - \ln(\alpha + \beta z)\Big]_0^\sigma = \frac{1}{\alpha - \beta}\ln\frac{\alpha(1 + \sigma)}{\alpha + \beta\sigma}.$$

For $\alpha = \beta$, $z' = \alpha(1 + z)^2$ gives $s = \frac{1}{\alpha}\left(1 - \frac{1}{1 + \sigma}\right) = \frac{\sigma}{\alpha(1 + \sigma)}$. The event needs $y = \sigma$, so it cannot come before $z$ reaches $\sigma$, that is before $t_k + \tau^*$. $\blacksquare$

**Termination.** By Theorem 2, a time interval of length $T$ has at most $\lceil T / \tau^* \rceil + 1$ events, so there is no Zeno behavior and the loop runs for all time. The simulation of lines L3 to L7 takes $T / \Delta t$ steps of the Runge-Kutta method.

**What the simulation checks.** The simulation tests the trigger only at the end of each step of length $\Delta t$, so an event can be up to $\Delta t$ late, and the error can exceed $\sigma\|x\|$ by a term of order $\Delta t$ just before an event. The theorems are about the exact trigger. The tests check that the simulated gaps are at least $\tau^* - \Delta t$, that the error stays below $\sigma\|x\|$ at the steps between events, and that the state goes to zero on random stable loops with $\sigma = 0.8\bar\sigma$.
