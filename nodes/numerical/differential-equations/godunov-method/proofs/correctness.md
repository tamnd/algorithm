---
title: Godunov's method for a convex scalar flux is conservative, monotone and TVD under the CFL condition
proves: [correctness, termination]
status: full
---

**Setting.** $f \in C^1(\mathbb{R})$ is convex, so $f'$ is nondecreasing. If $f'$ changes sign, $u_s$ is a point with $f'(u_s) = 0$ (if there are several, $f$ is constant on the set of such points, so the choice does not matter); otherwise $f'$ has one sign and the sonic branch is never used. One step of GODUNOV with step $k$ and $\lambda = k/\Delta x$ computes

$$u_i^{\text{new}} = H(u_{i-1}, u_i, u_{i+1}) := u_i - \lambda\big(F(u_i, u_{i+1}) - F(u_{i-1}, u_i)\big), \qquad F(u_L, u_R) = f\big(u^*(u_L, u_R)\big),$$

with $u^*$ the face state of the main page (lines L3 and L4). $I = [\alpha, \beta]$ is an interval containing all current values, including ghost values, and $L = \max_I|f'|$.

**Termination.** The loop runs $\lceil T/\Delta t\rceil$ times, each with $m + 1$ face evaluations of constant cost and $O(m)$ arithmetic; the final step is shortened so the run ends at $T$.

**Lemma 1 (Osher's formula).** For all $u_L, u_R$,

$$F(u_L, u_R) = \begin{cases} \min_{u_L \le u \le u_R} f(u) & \text{if } u_L \le u_R, \\ \max_{u_R \le u \le u_L} f(u) & \text{if } u_L > u_R. \end{cases}$$

*Proof.* Let $u_L \le u_R$. If $f'(u_L) \ge 0$, then $f' \ge 0$ on $[u_L, u_R]$, $f$ is nondecreasing there, and the minimum is $f(u_L)$, which is the value used. If $f'(u_R) \le 0$, $f$ is nonincreasing on the interval and the minimum is $f(u_R)$. Otherwise $f'(u_L) < 0 < f'(u_R)$, so $u_L < u_s < u_R$; $f$ is nonincreasing on $[u_L, u_s]$ and nondecreasing on $[u_s, u_R]$, and the minimum is $f(u_s)$. Now let $u_L > u_R$. A convex function on an interval attains its maximum at an endpoint, so the maximum is $\max(f(u_L), f(u_R))$. The shock speed $\sigma = (f(u_L) - f(u_R))/(u_L - u_R)$ has the sign of $f(u_L) - f(u_R)$, and the algorithm takes $u_L$ exactly when $\sigma \ge 0$, that is when $f(u_L) \ge f(u_R)$. $\square$

The face states are the values at $x/t = 0$ of the entropy solutions of the Riemann problems (a shock for $u_L > u_R$, a rarefaction fan otherwise; LeVeque 2002, Chapter 11), so $F$ is Godunov's flux. Lemma 1 gives a description that does not mention waves, and it is what the proofs below use.

**Lemma 2 (monotone flux).** $F$ is consistent, $F(v, v) = f(v)$, nondecreasing in $u_L$ and nonincreasing in $u_R$.

*Proof.* Consistency is immediate. Fix $u_R = b$ and let $a < a'$. If both are $\le b$, $[a', b] \subseteq [a, b]$, so the minimum over the smaller interval is at least the minimum over the larger one: $F(a, b) \le F(a', b)$. If both are $> b$, $[b, a] \subseteq [b, a']$ and the maximum grows. If $a \le b < a'$, then $F(a, b) = \min_{[a,b]}f \le f(b) \le \max_{[b,a']}f = F(a', b)$. The statement for $u_R$ follows the same way with the inclusions reversed. $\square$

**Lemma 3 (one-sided derivatives).** Fix $c$ and $d$ in $I$, and let $\varphi(v) = F(v, c)$ and $\psi(v) = F(d, v)$ for $v \in I$. Both are Lipschitz, and at almost every $v \in I$

$$0 \le \varphi'(v) \le \max(f'(v), 0), \qquad \min(f'(v), 0) \le \psi'(v) \le 0.$$

*Proof.* By Lemma 1, for $v \le c$, $\varphi(v) = f(\pi(v))$ with $\pi(v)$ the point of $[v, c]$ closest to $u_s$ (with $u_s = \pm\infty$ if there is no sonic point). So $\varphi(v) = f(v)$ when $v \ge u_s$, where $f'(v) \ge 0$, and $\varphi$ is constant when $v < u_s$. For $v > c$, $\varphi(v) = \max(f(v), f(c))$. The sublevel set $\{f < f(c)\}$ is an interval, so $\{v > c : f(v) \ge f(c)\}$ is a ray $[v_0, \infty)$; on it $\varphi = f$ and, by convexity, $f'(v) \ge (f(v) - f(c))/(v - c) \ge 0$, while on $(c, v_0)$ $\varphi$ is constant. These pieces are $C^1$ with the stated derivatives, and $\varphi$ is continuous and piecewise $C^1$ with finitely many breakpoints, hence Lipschitz on $I$ with constant $L$. The claim for $\psi$ is symmetric: for $v \ge d$, $\psi(v) = f(v)$ when $v \le u_s$ (where $f' \le 0$) and constant otherwise; for $v < d$, $\psi(v) = \max(f(d), f(v))$, which equals $f(v)$ on a ray $(-\infty, v_1]$ where $f(v) \ge f(d)$ forces $f'(v) \le (f(d) - f(v))/(d - v) \le 0$, and is constant on $(v_1, d)$. $\square$

**Theorem.** Suppose $\lambda L \le 1$.

1. (Monotone.) $H$ is nondecreasing in each of its three arguments on $I^3$.
2. (Maximum principle.) $\min(u_{i-1}, u_i, u_{i+1}) \le u_i^{\text{new}} \le \max(u_{i-1}, u_i, u_{i+1})$.
3. (Conservation.) With periodic boundaries $\sum_iu_i^{\text{new}} = \sum_iu_i$; in general $\Delta x\sum_i(u_i^{\text{new}} - u_i) = k(F_{1/2} - F_{m+1/2})$.
4. (TVD.) With periodic boundaries $\sum_i|u_{i+1}^{\text{new}} - u_i^{\text{new}}| \le \sum_i|u_{i+1} - u_i|$, indices modulo $m$.

*Proof.* (1) In $u_{i-1}$, $H$ is $\lambda F(u_{i-1}, u_i)$ plus a constant, nondecreasing by Lemma 2. In $u_{i+1}$, $H$ is $-\lambda F(u_i, u_{i+1})$ plus a constant, nondecreasing by Lemma 2. In $u_i = v$, with $c = u_{i+1}$ and $d = u_{i-1}$, $g(v) = v - \lambda\varphi(v) + \lambda\psi(v)$ is Lipschitz, and by Lemma 3 at almost every $v \in I$

$$g'(v) \ge 1 - \lambda\max(f'(v), 0) + \lambda\min(f'(v), 0) = 1 - \lambda|f'(v)| \ge 1 - \lambda L \ge 0.$$

A Lipschitz function is absolutely continuous, so $g(w) - g(v) = \int_v^wg' \ge 0$ for $v < w$.

(2) Let $M = \max(u_{i-1}, u_i, u_{i+1})$. Raising the arguments one at a time to $M$ and using (1), $H(u_{i-1}, u_i, u_{i+1}) \le H(M, M, M) = M - \lambda(f(M) - f(M)) = M$. The lower bound is the same with the minimum.

(3) Multiplying the update by $\Delta x$ and summing, the inner fluxes cancel in pairs; with periodic ghost cells $F_{m+1/2} = F(u_m, u_1) = F_{1/2}$.

(4) Write $\Delta_{i+1/2} = u_{i+1} - u_i$ and define, when $\Delta_{i+1/2} \ne 0$,

$$D_{i+1/2} = \lambda\frac{f(u_i) - F_{i+1/2}}{\Delta_{i+1/2}}, \qquad C_{i+1/2} = \lambda\frac{f(u_{i+1}) - F_{i+1/2}}{\Delta_{i+1/2}},$$

and $C_{i+1/2} = D_{i+1/2} = 0$ when $\Delta_{i+1/2} = 0$ (then $F_{i+1/2} = f(u_i) = f(u_{i+1})$). Then $u_i^{\text{new}} = u_i - \lambda(F_{i+1/2} - f(u_i)) - \lambda(f(u_i) - F_{i-1/2}) = u_i + D_{i+1/2}\Delta_{i+1/2} - C_{i-1/2}\Delta_{i-1/2}$. By Lemma 1, if $u_i < u_{i+1}$ then $F_{i+1/2}$ is the minimum of $f$ on $[u_i, u_{i+1}]$, so both numerators are $\ge 0$ and so are $C$ and $D$; if $u_i > u_{i+1}$ it is the maximum, both numerators are $\le 0$, and again $C, D \ge 0$. For the sum: if $u_i < u_{i+1}$ and the minimum is at $\xi$, then $f(u_i) - f(\xi) \le L(\xi - u_i)$ and $f(u_{i+1}) - f(\xi) \le L(u_{i+1} - \xi)$, so $C + D \le \lambda L \le 1$. If $u_i > u_{i+1}$ and the maximum is $f(u_i)$, then $C + D = \lambda(f(u_{i+1}) - f(u_i))/(u_{i+1} - u_i) \le \lambda L$, and likewise if it is $f(u_{i+1})$. Now

$$\Delta^{\text{new}}_{i+1/2} = (1 - C_{i+1/2} - D_{i+1/2})\Delta_{i+1/2} + D_{i+3/2}\Delta_{i+3/2} + C_{i-1/2}\Delta_{i-1/2}$$

has nonnegative coefficients, and summing absolute values over $i$ modulo $m$ and shifting indices gives the claim (Harten 1983). $\blacksquare$

**Remarks.** (i) The CFL hypothesis is on the current values; by (2) the values stay in the initial range, so $\lambda\max|f'|$ over the initial range $\le 1$ suffices for every step. (ii) Under the same condition Godunov's method equals exact evolution of the piecewise constant data for time $k$ followed by cell averaging, because waves from neighbouring faces cannot reach a face within one step (finite speed of propagation; LeVeque 2002, Chapters 4 and 12); this is not used above. (iii) Convergence to the entropy solution is cited, not proved here: conservative monotone schemes converge to the Kruzhkov entropy solution as $\Delta x \to 0$ at fixed $\lambda$ (Crandall and Majda 1980).
