---
title: RK4 with a cubic Hermite history and breakpoint grid is explicit, terminates, and converges with order 4
proves: [correctness, termination, convergence]
status: full
---

**Setting.** $f(t, y, z_1, \ldots, z_m)$ with constant delays $0 < \tau_{\min} = \min_j\tau_j$, $\tau = \max_j\tau_j$; history $\varphi$ on $[t_0 - \tau, t_0]$. $\|\cdot\|$ is a norm on $\mathbb{R}^d$. The grid is $t_0 < t_1 < \cdots < t_N = T$ with step lengths $k_n = t_{n+1} - t_n \le H = \min(h, \tau_{\min})$. $Y$ is the numerical history of line L11, $y$ the exact solution, $e_n = y(t_n) - y_n$. For $k = 0, 1, 2, \ldots$ let $S_k = \{t_0 + \sum_jn_j\tau_j : n_j \ge 0, \sum_jn_j \le k\}$; line L1 puts $S_4 \cap [t_0, T]$ and $T$ into the grid (we argue in exact arithmetic, so no breakpoints are merged).

**Lemma 1 (explicitness).** In the step from $t_n$ to $t_{n+1}$, every delayed time $s - \tau_j$ with $s \in \{t_n + k_n/2, t_{n+1}\}$ satisfies $s - \tau_j \le t_n$. Hence $Z(s)$ at lines L7, L8 and L10 only uses $\varphi$ and the stored triples $(t_l, y_l, F_l)$ with $l \le n$, all of which exist.

*Proof.* $s - \tau_j \le t_n + k_n - \tau_j \le t_n + H - \tau_{\min} \le t_n$. If $s - \tau_j \le t_0$, $Y = \varphi$; otherwise $t_l < s - \tau_j \le t_{l+1}$ for some $l + 1 \le n$, and the triples for $l$ and $l + 1$ were stored at line L3 or at line L10 of an earlier step. $\square$

**Lemma 2 (termination).** The algorithm performs $N = \sum_{i=1}^{K}n_i$ steps, a finite number.

*Proof.* $B$ is finite: there are at most $\binom{m+4}{4} - 1$ tuples $(n_j)$ with $1 \le \sum n_j \le 4$. For each interval, $n_i = \max(1, \lceil(b_i - b_{i-1})/H - \delta\rceil)$ is a finite integer, and each inner iteration does a bounded amount of work (four evaluations of $f$ and $2m$ lookups, each a binary search over finitely many stored times). $\square$

**Lemma 3 (piecewise smoothness).** Let $f \in C^4$ and $\varphi \in C^4[t_0 - \tau, t_0]$, and let the solution $y$ exist on $[t_0, T]$. For $k = 0, \ldots, 4$, on every closed interval $J$ whose endpoints are consecutive points of $(S_k \cap [t_0, T]) \cup \{T\}$, the restriction $y|_J$ is $C^{k+1}$ (with one-sided derivatives at the ends of $J$). In particular $y$ is $C^5$ on every grid interval $[t_n, t_{n+1}]$.

*Proof.* Induction on $k$. For $k = 0$: $y$ is continuous on $[t_0 - \tau, T]$ (the solution starts at $\varphi(t_0)$), so $t \mapsto f(t, y(t), y(t - \tau_1), \ldots)$ is continuous on $[t_0, T]$ and $y \in C^1[t_0, T]$, with $y'(t_0)$ the right derivative.

Step $k \to k + 1$ ($k + 1 \le 4$). Let $J = [\alpha, \beta]$ have consecutive endpoints in $S_{k+1} \cup \{T\}$. Since $S_k \subseteq S_{k+1}$, $J$ lies in an interval of the $S_k$ partition, so $y|_J \in C^{k+1}$ by the induction hypothesis. Fix $j$ and consider $J - \tau_j = [\alpha - \tau_j, \beta - \tau_j]$. If a point $p \in S_k$ were in its interior, then $p + \tau_j \in S_{k+1}$ would be in the interior of $J$, which is impossible. Since $t_0 \in S_k$, either $J - \tau_j \subseteq [t_0 - \tau, t_0]$, where $\varphi \in C^4 \subseteq C^{k+1}$, or $J - \tau_j \subseteq [t_0, T]$ lies in one interval of the $S_k$ partition, where $y \in C^{k+1}$ by the hypothesis. Either way $t \mapsto y(t - \tau_j)$ is $C^{k+1}$ on $J$. Then $y' = f(t, y(t), y(t - \tau_1), \ldots)$ is a composition of $C^{k+1}$ maps on $J$ ($f \in C^4$, $k + 1 \le 4$), so $y|_J \in C^{k+2}$.

At $k = 4$, every grid interval lies inside one interval of the $S_4$ partition, because line L1 puts all of $S_4 \cap (t_0, T)$ into the grid and line L5 does not step across a breakpoint. $\square$

**Lemma 4 (Hermite interpolation).** On $[a, b]$ with $k = b - a$ and $\theta \in [0, 1]$, the basis functions $h_{00} = 2\theta^3 - 3\theta^2 + 1$, $h_{01} = 3\theta^2 - 2\theta^3$, $h_{10} = \theta(1 - \theta)^2$, $h_{11} = -\theta^2(1 - \theta)$ satisfy $h_{00}, h_{01} \in [0, 1]$, $h_{00} + h_{01} = 1$, $|h_{10}|, |h_{11}| \le \tfrac4{27}$. If $g \in C^4[a, b]$ and $p$ is its Hermite cubic, $\|g(u) - p(u)\| \le \tfrac{k^4}{384}\max_{[a,b]}\|g^{(4)}\|$ (componentwise in the maximum norm; up to a norm-equivalence constant in other norms).

*Proof.* $h_{00} + h_{01} = 1$ by expansion; $h_{01}' = 6\theta(1 - \theta) \ge 0$ with $h_{01}(0) = 0$, $h_{01}(1) = 1$. $\theta(1 - \theta)^2$ has its maximum $\tfrac4{27}$ at $\theta = \tfrac13$, and $\theta^2(1 - \theta)$ has its maximum $\tfrac4{27}$ at $\theta = \tfrac23$. The remainder of Hermite interpolation with double nodes $a, b$ is $g^{(4)}(\xi)(u - a)^2(u - b)^2/4!$ per component, and $\max(u - a)^2(u - b)^2 = (k/2)^4 = k^4/16$; $\tfrac1{16 \cdot 24} = \tfrac1{384}$. $\square$

**Theorem (order 4).** Assume, in addition to the hypotheses of Lemma 3, that $f$ is Lipschitz: $\|f(t, y, z) - f(t, \tilde y, \tilde z)\| \le L\|y - \tilde y\| + M\max_j\|z_j - \tilde z_j\|$. Then there are $H_0 > 0$ and $C$ independent of the grid such that, for $H \le H_0$,

$$\max_n\|y(t_n) - y_n\| \le CH^4, \qquad \sup_{t_0 - \tau \le s \le T}\|y(s) - Y(s)\| \le CH^4.$$

*Proof.* Write $E_n = \max_{l \le n}\|e_l\|$ and $D_n = \sup_{s \le t_n}\|y(s) - Y(s)\|$, where $Y$ uses the triples stored up to $t_n$. Let $F_l^* = y'(t_l)$ (the right derivative at $t_0$; $y'$ is continuous on $(t_0, T]$ by Lemma 3). Constants $c_1, c_2, \ldots$ depend only on $f$, $\varphi$, $T - t_0$ and bounds of $y^{(4)}, y^{(5)}$ on the pieces of Lemma 3.

*Slopes.* By Lemma 1, $F_l = f(t_l, y_l, Z(t_l))$ uses delayed values at times $\le t_{l-1}$, so for $l \le n$, $\|F_l - F_l^*\| \le L\|e_l\| + MD_n \le LE_n + MD_n$. (For $l = 0$ the delayed values come from $\varphi$ and $F_0 = F_0^*$.)

*History.* For $s \le t_0$ the error is 0. For $s \in [t_l, t_{l+1}]$ with $l + 1 \le n$, write $Y(s) - y(s) = (Y(s) - p(s)) + (p(s) - y(s))$, where $p$ is the Hermite cubic of the exact data. By Lemma 4 and Lemma 3 ($y$ is $C^5$, hence $C^4$, on the step),

$$\|Y(s) - y(s)\| \le h_{00}\|e_l\| + h_{01}\|e_{l+1}\| + \tfrac4{27}k_l\big(\|F_l - F_l^*\| + \|F_{l+1} - F_{l+1}^*\|\big) + c_1H^4 \le E_n + \tfrac8{27}H(LE_n + MD_n) + c_1H^4.$$

Taking the supremum, $D_n \le E_n + \tfrac8{27}H(LE_n + MD_n) + c_1H^4$. For $H \le H_0$ with $\tfrac8{27}H_0M \le \tfrac12$ this gives

$$D_n \le c_2E_n + c_3H^4. \tag{1}$$

*One step.* Let $g(t, v) = f(t, v, y(t - \tau_1), \ldots, y(t - \tau_m))$ on $[t_n, t_{n+1}]$. By Lemma 3 and the argument in its proof, $t \mapsto y(t - \tau_j)$ is $C^4$ on the step, so $g$ is $C^4$ there and $y$ is the solution of $v' = g(t, v)$ through $y(t_n)$, which is $C^5$ on the step. Let $\Phi(t_n, v; z)$ be the RK4 increment computed at lines L7 to L9 from $v$ with delayed values $z$. Then

$$y(t_{n+1}) = y(t_n) + k_n\Phi(t_n, y(t_n); z^*) + \lambda_{n+1},$$

where $z^*$ are the exact delayed values and $\lambda_{n+1}$ is the local error of classical RK4 on the ODE $v' = g(t, v)$, which satisfies $\|\lambda_{n+1}\| \le c_4k_n^5$ because the method has order 4 and the solution and $g$ are smooth on the closed step (HNW I, Sections II.2 and II.3). Subtracting $y_{n+1} = y_n + k_n\Phi(t_n, y_n; z)$ with the numerical delayed values $z$ (errors at most $D_n$ by Lemma 1):

*Lipschitz bound for $\Phi$.* Write $\Delta K_i$ for the difference of the stages computed from $(y_n, z)$ and from $(y(t_n), z^*)$. Then $\|\Delta K_1\| \le LE_n + MD_n$ by the slope bound, and each later stage satisfies $\|\Delta K_{i+1}\| \le L(\|e_n\| + k_n\|\Delta K_i\|) + MD_n$, so all $\|\Delta K_i\| \le (LE_n + MD_n)(1 + HL + (HL)^2 + (HL)^3) \le e^{HL}(LE_n + MD_n)$, and the same bound holds for $\Delta\Phi = \tfrac16(\Delta K_1 + 2\Delta K_2 + 2\Delta K_3 + \Delta K_4)$.

Hence, using (1),

$$\|e_{n+1}\| \le \|e_n\| + k_ne^{HL}(LE_n + M(c_2E_n + c_3H^4)) + c_4k_nH^4 \le (1 + c_5k_n)E_n + c_6k_nH^4,$$

and therefore $E_{n+1} \le (1 + c_5k_n)E_n + c_6k_nH^4$. With $E_0 = 0$ (since $y_0 = \varphi(t_0)$) and $1 + x \le e^x$,

$$E_N \le c_6H^4\sum_nk_n\prod_{l > n}(1 + c_5k_l) \le \frac{c_6}{c_5}\big(e^{c_5(T - t_0)} - 1\big)H^4,$$

the discrete Gronwall inequality. The dense output bound follows from (1) with $n = N$. Since $H \le h$, both errors are also $O(h^4)$. $\blacksquare$

**Remarks.** (i) The hypotheses are needed: if a point of $S_1$ or $S_2$ lies inside a step, $y$ has a jump in $y''$ or $y'''$ there, the local error of that step is only $O(k^2)$ or $O(k^3)$, and the global order drops accordingly; the tests observe order 2 when $t_0 + \tau$ lies in the middle of a step. (ii) The proof is the case $p = 4$, $q = 3$ of the bound $\min(p, q + 1)$ for Runge-Kutta methods with continuous extensions of uniform order $q$ (Bellen and Zennaro 2003, Chapters 4 to 6). (iii) In floating point, line L1 merges breakpoints closer than $10^{-9}(T - t_0)$; a merged pair perturbs the solution by an amount of order of that distance times a bounded derivative jump, which is below the error of any practical step size.
