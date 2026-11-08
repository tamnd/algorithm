---
title: Euler's method computes the Euler polygon, and its global error is O(h)
proves: [correctness, termination, convergence]
status: full
---

**Setting.** We use any norm $\|\cdot\|$ on $\mathbb{R}^d$. The function $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is continuous and Lipschitz in $y$: $\|f(t, u) - f(t, v)\| \le L \|u - v\|$ for all $t$, $u$, $v$. By the [Picard-Lindelöf theorem](/picard-lindelof-theorem/) the problem $y' = f(t, y)$, $y(t_0) = y_0$ has a unique solution $y$ on $[t_0, T]$. For the error bound we also assume that $y$ is twice continuously differentiable, and we put $M_2 = \max_{t_0 \le t \le T} \|y''(t)\|$. This holds when $f$ is $C^1$, because then $y'' = f_t + f_y f$ is continuous.

**Lemma 1 (the loop).** Let $N$ be the value of line L1. After the iteration of lines L3 to L6 with index $n$, the variables hold $t = t_{n+1}$ and $y = y_{n+1}$, where $t_m = t_0 + m h$ for $m < N$, $t_N = T$, and $y_{m+1} = y_m + (t_{m+1} - t_m) f(t_m, y_m)$.

*Proof.* Induction on $n$. Before the loop, line L2 sets $t = t_0$ and $y = y_0$. Assume that $t = t_n$ and $y = y_n$ at the start of iteration $n$. Line L4 sets $t_{\text{next}} = t_{n+1}$ by the definition of the grid. Line L5 evaluates $f$ at $(t_n, y_n)$ and sets $y = y_n + (t_{n+1} - t_n) f(t_n, y_n) = y_{n+1}$. Line L6 sets $t = t_{n+1}$. The loop of line L3 runs exactly $N$ times, so the algorithm stops and returns $(t_N, y_N) = (T, y_N)$. If $N = 0$, which happens exactly when $T = t_0$, it returns $(t_0, y_0)$. $\square$

Line L1 chooses $N$ so that each step length $h_n = t_{n+1} - t_n$ is at most $h$, up to a relative rounding slack that is $0$ in exact arithmetic. Below, $h$ denotes $\max_n h_n$.

**Lemma 2 (local error).** For each $n$, the defect $\tau_n = y(t_{n+1}) - y(t_n) - h_n f(t_n, y(t_n))$ satisfies $\|\tau_n\| \le \tfrac12 h_n^2 M_2$.

*Proof.* Since $y' = f(t, y)$, Taylor's formula with integral remainder gives $y(t_{n+1}) = y(t_n) + h_n y'(t_n) + \int_{t_n}^{t_{n+1}} (t_{n+1} - s) y''(s)\, ds$. The norm of the integral is at most $M_2 \int_{t_n}^{t_{n+1}} (t_{n+1} - s)\, ds = \tfrac12 h_n^2 M_2$. $\square$

**Theorem (convergence).** Under the hypotheses above, the global error $e_n = y(t_n) - y_n$ satisfies, for each $n \le N$,

$$\|e_n\| \le \frac{h M_2}{2L}\left(e^{L(t_n - t_0)} - 1\right) \quad (L > 0), \qquad \|e_n\| \le \frac{h M_2}{2}(t_n - t_0) \quad (L = 0).$$

*Proof.* Subtract the step $y_{n+1} = y_n + h_n f(t_n, y_n)$ from the definition of $\tau_n$:

$$e_{n+1} = e_n + h_n\big(f(t_n, y(t_n)) - f(t_n, y_n)\big) + \tau_n.$$

By the Lipschitz condition and Lemma 2, $\|e_{n+1}\| \le (1 + h_n L)\|e_n\| + \tfrac12 h_n h M_2$, where we used $h_n \le h$. Let $L > 0$ and $C = h M_2 / (2L)$. We show $\|e_n\| \le C(e^{L(t_n - t_0)} - 1)$ by induction on $n$. For $n = 0$, $e_0 = 0$. Assume the bound for $n$. Since $1 + x \le e^x$,

$$\|e_{n+1}\| \le e^{h_n L} C\left(e^{L(t_n - t_0)} - 1\right) + C h_n L = C\left(e^{L(t_{n+1} - t_0)} - e^{h_n L} + h_n L\right) \le C\left(e^{L(t_{n+1} - t_0)} - 1\right),$$

where the last step uses $e^{h_n L} \ge 1 + h_n L$ again. For $L = 0$ the recurrence is $\|e_{n+1}\| \le \|e_n\| + \tfrac12 h_n h M_2$, and summing gives $\|e_n\| \le \tfrac12 h M_2 (t_n - t_0)$. $\blacksquare$

**Corollary (with rounding).** Suppose that each computed step has an extra error of norm at most $\varepsilon$ (rounding in $f$ and in the update), so that $\tilde y_{n+1} = \tilde y_n + h_n f(t_n, \tilde y_n) + \delta_n$ with $\|\delta_n\| \le \varepsilon$, and that all steps have length $h$. The same induction with $\tfrac12 h^2 M_2 + \varepsilon$ in place of $\tfrac12 h^2 M_2$ gives

$$\|y(t_n) - \tilde y_n\| \le \left(\frac{h M_2}{2} + \frac{\varepsilon}{h}\right)\frac{e^{L(t_n - t_0)} - 1}{L}.$$

The right side is smallest at $h = \sqrt{2\varepsilon / M_2}$, so with rounding the error cannot be made smaller than about $\sqrt{2 \varepsilon M_2}\,(e^{L(t_n - t_0)} - 1)/L$ by a smaller step. $\blacksquare$
