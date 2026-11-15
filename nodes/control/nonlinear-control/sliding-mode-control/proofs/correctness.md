---
title: Sliding mode control reaches the surface s = 0 within |s(0)| / eta, stays on it, and the reduced motion is exponentially stable for every matched uncertainty within the bound
proves: [correctness]
status: full
---

The system is

$$\dot x_i = x_{i+1} \quad (1 \le i \le n - 1), \qquad \dot x_n = \hat f(x) + \delta(t, x) + b(x)\, u,$$

where $\hat f$ and $b$ are known and continuous, $b(x) \neq 0$, and the unknown term $\delta$ is measurable in $t$, continuous in $x$, and satisfies $|\delta(t, x)| \le D$ for all $t$ and $x$. The coefficients $c_1, \dots, c_{n-1}$ make $p(\lambda) = \lambda^{n-1} + c_{n-1} \lambda^{n-2} + \dots + c_1$ Hurwitz, and $k \ge D + \eta$ with $\eta > 0$. For $n = 1$ there are no coefficients and $s = x_1$.

Lines L1 to L5 give

$$s = \sum_{i=1}^{n-1} c_i x_i + x_n, \qquad v = -\hat f(x) - \sum_{i=1}^{n-1} c_i x_{i+1}, \qquad u = \frac{v - k \sigma(s)}{b(x)},$$

with $\sigma = \operatorname{sgn}$ (line L4) or $\sigma(s) = \operatorname{sat}(s / \phi)$ for $\phi > 0$ (line L3). Here $|\cdot|$ is the absolute value of a real number, and $\|\cdot\|$ is the Euclidean norm of a vector.

## Lemma 1: the sliding variable obeys s' = delta - k sigma(s)

Along a solution, wherever the derivative exists,

$$\dot s = \sum_{i=1}^{n-1} c_i \dot x_i + \dot x_n = \sum_{i=1}^{n-1} c_i x_{i+1} + \hat f + \delta + b u.$$

By line L5, $b u = v - k \sigma(s) = -\hat f - \sum_{i<n} c_i x_{i+1} - k \sigma(s)$. Substitution gives $\dot s = \delta - k \sigma(s)$. $\square$

The identity is algebraic, so it holds exactly for exact data. The tests check it in Fraction.

## Solutions

With $\sigma = \operatorname{sgn}$ the right side is discontinuous on $s = 0$, so solutions are taken in the sense of Filippov (Filippov 1988): an absolutely continuous $x(t)$ whose derivative lies, for almost every $t$, in the closed convex hull of the limits of the right side at nearby points. Off the surface this is the ordinary equation. On the surface, $\sigma(0)$ is replaced by any value in $[-1, 1]$. In both cases Lemma 1 holds in the form $\dot s(t) = \delta - k \sigma(t)$ with $\sigma(t) = \operatorname{sgn} s(t)$ when $s(t) \neq 0$ and $\sigma(t) \in [-1, 1]$ when $s(t) = 0$, for almost every $t$. The function $s(t)$ is absolutely continuous, because $x(t)$ is.

## Theorem 1: reaching in finite time

Let $\sigma = \operatorname{sgn}$. On every interval where $s(t) \neq 0$,

$$\frac{d}{dt} |s| = \operatorname{sgn}(s)\, \dot s = \operatorname{sgn}(s)\, \delta - k \le D - k \le -\eta$$

for almost every $t$. Equivalently, $s \dot s \le -\eta |s|$ (the reaching condition). Integrating, $|s(t)| \le |s(0)| - \eta t$ for as long as $s$ has not reached $0$. Since $|s| \ge 0$, $s$ reaches $0$ at some time $t_r \le |s(0)| / \eta$. $\square$

## Theorem 2: the surface is invariant

Let $t_r$ be a time with $s(t_r) = 0$, and suppose $s(t_1) \neq 0$ for some $t_1 > t_r$. Let $t_0 = \sup \{ t \in [t_r, t_1] : s(t) = 0 \}$. By continuity, $s(t_0) = 0$ and $s(t) \neq 0$ on $(t_0, t_1]$. By Theorem 1, $|s|$ is non-increasing on $(t_0, t_1]$, and by absolute continuity $|s(t_1)| = |s(t_0)| + \int_{t_0}^{t_1} \frac{d}{dt}|s|\, dt \le 0 - \eta (t_1 - t_0) < 0$. This is impossible. So $s(t) = 0$ for all $t \ge t_r$. $\square$

## Theorem 3: the motion on the surface

For $t \ge t_r$, $x_n = -\sum_{i<n} c_i x_i$. Let $\xi = (x_1, \dots, x_{n-1})$. Then $\dot \xi_i = \xi_{i+1}$ for $i < n - 1$, and $\dot \xi_{n-1} = x_n = -c_1 \xi_1 - \dots - c_{n-1} \xi_{n-1}$. So $\dot \xi = A_c \xi$, where $A_c$ is the companion matrix of $p(\lambda)$. Its eigenvalues are the roots of $p$, which have negative real parts. So there are constants $M \ge 1$ and $\alpha > 0$ with $\|\xi(t)\| \le M e^{-\alpha (t - t_r)} \|\xi(t_r)\|$, and $x_n = -\sum c_i \xi_i$ decays at the same rate. The term $\delta$ does not appear in this equation. For $n = 1$, $s = x_1 = 0$ already. $\square$

Together, Theorems 1 to 3 show that every solution reaches the surface within $|s(0)| / \eta$, stays on it, and then converges to $0$ exponentially, for every $\delta$ with $|\delta| \le D$. In the reduced coordinates the origin is globally asymptotically stable.

## Theorem 4: the boundary layer

Let $\sigma(s) = \operatorname{sat}(s / \phi)$ with $\phi > 0$. Now the closed loop has a continuous right side. Where $|s| \ge \phi$, $\sigma = \operatorname{sgn} s$ and Theorem 1 applies, so $s$ enters the layer $|s| \le \phi$ within time $\max(0, |s(0)| - \phi) / \eta$; by the argument of Theorem 2 it does not leave it. Inside the layer, $\dot s = \delta - (k / \phi) s$, so where $s \neq 0$,

$$\frac{d}{dt} |s| \le D - \frac{k}{\phi} |s|.$$

By the comparison lemma (Khalil 2002, Section 3.4), $|s(t)| \le \frac{\phi D}{k} + \left(|s(t_1)| - \frac{\phi D}{k}\right) e^{-k (t - t_1) / \phi}$ after the entry time $t_1$. So $\limsup |s(t)| \le \phi D / k$. Since $\phi D / k < \phi$, this band lies in the layer. With $|s| \le \varepsilon$ from some time $t_2$ on, the state $\xi = (x_1, \dots, x_{n-1})$ obeys $\dot \xi = A_c \xi + e_{n-1} s$, with $e_{n-1}$ the last unit vector, and the variation of constants formula gives $\|\xi(t)\| \le M e^{-\alpha (t - t_2)} \|\xi(t_2)\| + M \varepsilon / \alpha$. So $\xi$ is ultimately bounded by any number larger than $M \varepsilon / \alpha$. $\square$

The boundary layer gives up exact sliding and exact rejection of $\delta$; it keeps a bound that is proportional to $\phi$.

## Theorem 5: sampled switching

Suppose the switching term is computed at the instants $t_j = j h$ and held, so that $\dot s = \delta(t) - k \operatorname{sgn}(s(t_j))$ on $[t_j, t_{j+1})$, while the rest of the control acts continuously. Let $B = (k + D) h$.

If $s(t_j) > 0$, then on the step $\dot s \in [-(k + D), -(k - D)]$, so $s$ decreases, and $s(t) \ge s(t_j) - B$ on the step. If $0 < s(t_j) \le B$, every value on the step lies in $[s(t_j) - B, s(t_j)] \subset [-B, B]$. The case $s(t_j) < 0$ is symmetric, and if $s(t_j) = 0$, then $|\dot s| \le D$ and $|s(t)| \le D h \le B$ on the step. So once $|s(t_j)| \le B$ at a sample, $|s(t)| \le B$ for all later $t$. If $|s(t_j)| > B$, then $|s|$ decreases by at least $(k - D) h \ge \eta h$ over the step, so the band is reached after at most $|s(0)| / (\eta h)$ steps. $\square$

In an implementation where the whole control, including $v$, is held, $\dot s$ has the extra term $\sum c_i (x_{i+1}(t) - x_{i+1}(t_j)) + \hat f(x(t)) - \hat f(x(t_j))$, which is of order $h$ on a bounded set. It adds a term of order $h^2$ to the band. The tests measure $|s| \le 0.00399$ for $h = 0.002$ and $0.00200$ for $h = 0.001$ in the page example, where $B = 2h$.
