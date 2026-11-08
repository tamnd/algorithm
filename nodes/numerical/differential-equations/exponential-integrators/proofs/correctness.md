---
title: ETD2RK computes the φ-functions correctly, is exact for affine forcing, preserves equilibria, and converges with order 2 independently of the stiffness
proves: [correctness, termination, convergence]
status: full
---

**Setting.** $y' = Ay + g(t, y)$ on $[t_0, T]$, $N$ equal steps of length $k = (T - t_0)/N$, $t_n = t_0 + nk$, $Z = kA$. $\|\cdot\|$ is a vector norm and the induced matrix norm. $\varphi_0(z) = e^z$, $\varphi_j(z) = \sum_{i \ge 0}z^i/(i + j)!$, so that for matrices

$$k\varphi_1(kA) = \int_0^ke^{(k - \sigma)A}\,d\sigma, \qquad k\varphi_2(kA) = \int_0^ke^{(k - \sigma)A}\frac{\sigma}{k}\,d\sigma, \tag{1}$$

which follows by expanding $e^{(k-\sigma)A}$ in its power series and integrating term by term ($\int_0^k(k - \sigma)^i\,d\sigma = k^{i+1}/(i+1)$ and $\int_0^k(k - \sigma)^i\sigma\,d\sigma = k^{i+2}/((i+1)(i+2))$).

**Lemma 1 (line L2).** Let $W = \begin{pmatrix}Z & I & 0\\ 0 & 0 & I\\ 0 & 0 & 0\end{pmatrix}$. The first block row of $e^W$ is $[e^Z, \varphi_1(Z), \varphi_2(Z)]$.

*Proof.* The first block row $R_j$ of $W^j$ is $[I, 0, 0]$ for $j = 0$, $[Z, I, 0]$ for $j = 1$, and $[Z^j, Z^{j-1}, Z^{j-2}]$ for $j \ge 2$: by induction, $R_{j+1} = R_jW = [Z^{j+1}, Z^j, Z^{j-1}]$, using the block columns of $W$ (the second block column of $W$ is $(I, 0, 0)^T$ and the third is $(0, I, 0)^T$). Summing $R_j/j!$: the first block is $\sum_jZ^j/j! = e^Z$, the second $\sum_{j \ge 1}Z^{j-1}/j! = \varphi_1(Z)$, the third $\sum_{j \ge 2}Z^{j-2}/j! = \varphi_2(Z)$. $\square$

The implementation evaluates $e^W$ by scaling and squaring: $e^W = (e^{W/2^s})^{2^s}$ exactly, and the Taylor sum of $e^{W/2^s}$ with $\|W/2^s\|_1 \le \tfrac12$ is truncated when a term falls below $10^{-18}$, which leaves a remainder of at most twice that term, since subsequent terms shrink by a factor at least 2. In exact rational arithmetic with nilpotent $W$ the series terminates and the result is exact. The rounding error of the squaring phase is analysed in Higham (2008, Chapter 10); we treat line L2 as exact below.

**Lemma 2 (quadrature form).** Let $G_n = g(t_n, y_n)$ and $a = e^{Z}y_n + k\varphi_1(Z)G_n$. Then ETD2RK is

$$y_{n+1} = e^{kA}y_n + \int_0^ke^{(k - \sigma)A}\Big(G_n + \frac{\sigma}{k}\big(g(t_{n+1}, a) - G_n\big)\Big)\,d\sigma,$$

and exponential Euler is $y_{n+1} = e^{kA}y_n + \int_0^ke^{(k - \sigma)A}G_n\,d\sigma$.

*Proof.* Lines L5 to L7 give $y_{n+1} = e^Zy_n + k\varphi_1(Z)G_n + k\varphi_2(Z)(g(t_{n+1}, a) - G_n)$; substitute (1). $\square$

**Theorem 1 (exactness).** (a) If $g(t, y) = c_0 + c_1t$, ETD2RK gives $y_n = y(t_n)$ for all $n$. (b) If $Ay^* + g(t, y^*) = 0$ for all $t$, then $y_n = y^*$ for all $n$ when $y_0 = y^*$, for both methods and every $k$.

*Proof.* (a) The exact solution satisfies the variation-of-constants formula $y(t_{n+1}) = e^{kA}y(t_n) + \int_0^ke^{(k-\sigma)A}F(t_n + \sigma)\,d\sigma$ with $F(t) = c_0 + c_1t$, and $F(t_n + \sigma) = F(t_n) + \frac{\sigma}{k}(F(t_{n+1}) - F(t_n))$ exactly. Since $g$ does not depend on $y$, $G_n = F(t_n)$ and $g(t_{n+1}, a) = F(t_{n+1})$, so Lemma 2 gives the same formula; induction on $n$.

(b) With $y_n = y^*$ and $G_n = g(t_n, y^*) = -Ay^*$: $a = e^Zy^* - k\varphi_1(Z)Ay^* = e^Zy^* - \varphi_1(Z)Zy^* = e^Zy^* - (e^Z - I)y^* = y^*$, using $\varphi_1(Z)Z = e^Z - I$ (power series). Then $g(t_{n+1}, a) - G_n = -Ay^* + Ay^* = 0$ and $y_{n+1} = a = y^*$. $\square$

**Theorem 2 (stiff convergence).** Assume

- (A) $\|e^{tA}\| \le 1$ for all $t \ge 0$;
- (L) $\|g(t, u) - g(t, v)\| \le L\|u - v\|$;
- (S) $F(t) = g(t, y(t))$ is $C^2$ on $[t_0, T]$ with $\|F'\| \le K_1$, $\|F''\| \le K_2$.

Then for every $N$, exponential Euler satisfies $\max_n\|y(t_n) - y_n\| \le \frac{K_1}{2L}(e^{L(T - t_0)} - 1)k$, and ETD2RK satisfies $\max_n\|y(t_n) - y_n\| \le C_2k^2$ with $C_2 = \frac{K_2/12 + LK_1/4}{c}(e^{c(T - t_0)} - 1)$ and $c = 2L + L^2(T - t_0)/2$. Neither constant depends on $A$.

*Proof.* From (A) and (1), $\|e^{\sigma A}\| \le 1$, $\|k\varphi_1(kA)\| \le k$ and $\|k\varphi_2(kA)\| \le \int_0^k\frac{\sigma}{k}d\sigma = \frac k2$.

*Local error of ETD2RK.* Start one step from the exact value: $\hat a = e^{kA}y(t_n) + k\varphi_1(kA)F(t_n)$ and $\hat y_{n+1} = \hat a + k\varphi_2(kA)(g(t_{n+1}, \hat a) - F(t_n))$. By variation of constants and (1),

$$y(t_{n+1}) - \hat a = \int_0^ke^{(k - \sigma)A}\big(F(t_n + \sigma) - F(t_n)\big)d\sigma, \qquad \|y(t_{n+1}) - \hat a\| \le \int_0^kK_1\sigma\,d\sigma = \frac{K_1k^2}{2}.$$

Write $\ell(\sigma) = F(t_n) + \frac{\sigma}{k}(F(t_{n+1}) - F(t_n))$, the linear interpolant, with $\|F(t_n + \sigma) - \ell(\sigma)\| \le \frac{\sigma(k - \sigma)}{2}K_2$. Then

$$y(t_{n+1}) - \hat y_{n+1} = \int_0^ke^{(k-\sigma)A}\big(F(t_n + \sigma) - \ell(\sigma)\big)d\sigma + k\varphi_2(kA)\big(F(t_{n+1}) - g(t_{n+1}, \hat a)\big),$$

and since $F(t_{n+1}) = g(t_{n+1}, y(t_{n+1}))$, (L) gives

$$\|d_{n+1}\| := \|y(t_{n+1}) - \hat y_{n+1}\| \le \frac{K_2k^3}{12} + \frac k2L\frac{K_1k^2}{2} = \Big(\frac{K_2}{12} + \frac{LK_1}{4}\Big)k^3.$$

*Stability of one step.* For two starting values $u, v$ with predictors $a_u, a_v$: $\|a_u - a_v\| \le \|u - v\| + kL\|u - v\|$, and

$$\|\Psi(u) - \Psi(v)\| \le \|a_u - a_v\| + \frac k2\big(L\|a_u - a_v\| + L\|u - v\|\big) \le \Big(1 + 2kL + \frac{k^2L^2}{2}\Big)\|u - v\| \le (1 + ck)\|u - v\|,$$

where $\Psi$ is one ETD2RK step and $k \le T - t_0$ was used.

*Global error.* $e_{n+1} = y(t_{n+1}) - y_{n+1} = d_{n+1} + \big(\Psi(y(t_n)) - \Psi(y_n)\big)$, so $\|e_{n+1}\| \le (1 + ck)\|e_n\| + \|d_{n+1}\|$ with $e_0 = 0$. Unrolling and using $1 + ck \le e^{ck}$,

$$\|e_n\| \le \Big(\frac{K_2}{12} + \frac{LK_1}{4}\Big)k^3\sum_{j=0}^{n-1}e^{cjk} \le \Big(\frac{K_2}{12} + \frac{LK_1}{4}\Big)k^2\frac{e^{c(T - t_0)} - 1}{c}.$$

*Exponential Euler.* Its local error is $\int_0^ke^{(k-\sigma)A}(F(t_n + \sigma) - F(t_n))d\sigma$, of norm $\le K_1k^2/2$, and one step satisfies $\|\Psi(u) - \Psi(v)\| \le (1 + kL)\|u - v\|$. The same unrolling gives $\|e_n\| \le \frac{K_1k^2}{2}\sum_je^{Ljk} \le \frac{K_1}{2L}(e^{L(T - t_0)} - 1)k$. $\square$

**Termination.** Line L1 gives a finite $N \ge 1$ (or the algorithm returns at once when $T = t_0$). Line L2 performs at most 40 Taylor terms and $s = \lceil\log_2(2\|W\|_1)\rceil$ squarings (zero if $\|W\|_1 \le \tfrac12$). The loop runs $N$ times with two evaluations of $g$ each. $\blacksquare$

**Remarks.** (i) Hypothesis (A) holds in the 2-norm exactly when $A + A^T$ is negative semidefinite; with $\|e^{tA}\| \le e^{\omega t}$ the same proof works with constants multiplied by $e^{\omega(T - t_0)}$. (ii) Hypothesis (S) asks for a smooth exact solution in the sense that $t \mapsto g(t, y(t))$ has bounded derivatives; this excludes initial layers, which Hochbruck and Ostermann treat with weighted estimates for parabolic problems (2010, Section 2). (iii) The test with $y' = \lambda(y - \sin t) + \cos t$ satisfies (A), (L) with $L = 0$ and (S) with $K_1, K_2$ of size $|\lambda|$; there the bound above grows with $|\lambda|$, yet the observed constant does not, because the leading interpolation error is damped by $e^{(k - \sigma)\lambda}$; that observation is not covered by Theorem 2.
