---
title: Parareal reproduces the fine solution on the first k + 1 slice ends after k iterations, and for linear problems its error is bounded by alpha^k times a binomial coefficient
proves: [correctness, termination, convergence]
status: full
---

**Setting.** Slice ends $T_0 = t_0 < T_1 < \dots < T_N = T$. Propagators $\mathcal{F}_n, \mathcal{G}_n : \mathbb{R}^d \to \mathbb{R}^d$, $\mathcal{F}_n(y) = \mathcal{F}(T_n, T_{n+1}, y)$ and likewise for $\mathcal{G}$, are arbitrary maps (no smoothness is needed for the first two results). The fine solution is $u_0 = y_0$, $u_{n+1} = \mathcal{F}_n(u_n)$. The iterates are $U^0_0 = y_0$, $U^0_{n+1} = \mathcal{G}_n(U^0_n)$, and for $k \ge 0$

$$U^{k+1}_0 = y_0, \qquad U^{k+1}_{n+1} = \mathcal{G}_n(U^{k+1}_n) + \mathcal{F}_n(U^k_n) - \mathcal{G}_n(U^k_n). \tag{P}$$

All arithmetic is exact.

**Lemma 1 (the loop).** Line L1 computes $U^0$ and stores $g_n = \mathcal{G}_n(U^0_n)$. If at the start of iteration $k + 1$ of line L2 the array $U$ holds $U^k$ and $g_n = \mathcal{G}_n(U^k_n)$ for all $n$, then line L3 sets $F_n = \mathcal{F}_n(U^k_n)$; lines L4 to L7 compute $V = U^{k+1}$ by (P) in order $n = 0, 1, \dots$, each $V_{n+1}$ using $V_n$ computed just before; and afterwards $g_n = \mathcal{G}_n(U^{k+1}_n)$. Line L8 sets $U = U^{k+1}$.

*Proof.* Line L6 computes $\mathcal{G}_n(V_n)$ and line L7 uses the old $g_n$, which is $\mathcal{G}_n(U^k_n)$, before overwriting it with the new value. The fine values $F_n$ were all computed from $U^k$ in line L3, before $U$ changes in line L8. Induction on $k$. $\square$

The $N$ fine solves in line L3 read only $U^k$, so they are independent of each other, which is what allows them to run in parallel.

**Termination.** The loop of line L2 runs at most $K$ times, each with $N$ fine and $N$ coarse calls; line L1 makes $N$ coarse calls.

**Theorem 2 (exactness).** For every $k \ge 0$ and every $n \le \min(k, N)$, $U^k_n = u_n$. In particular $U^N = u$, and with $K = N$ (the default) the returned values are the fine solution.

*Proof.* Induction on $k$. For $k = 0$, $U^0_0 = y_0 = u_0$. Suppose $U^k_n = u_n$ for $n \le k$. Then $U^{k+1}_0 = u_0$, and if $U^{k+1}_n = u_n$ for some $n \le k$, (P) gives

$$U^{k+1}_{n+1} = \mathcal{G}_n(u_n) + \mathcal{F}_n(u_n) - \mathcal{G}_n(u_n) = u_{n+1}.$$

So $U^{k+1}_n = u_n$ for $n \le k + 1$ by induction on $n$. $\square$

**Corollary 3 (fixed points).** If $U^{k+1} = U^k = U$, then $U = u$: (P) gives $U_{n+1} = \mathcal{F}_n(U_n)$ and $U_0 = y_0$. So when line L9 stops with $\text{tol} = 0$ the result is the fine solution; with $\text{tol} > 0$ it stops at a nearby iterate, and how near is only bounded for the linear case below.

**Theorem 4 (linear error bound).** Let $\mathcal{F}_n(y) = \varphi y$ and $\mathcal{G}_n(y) = \gamma y$ with scalars $\varphi, \gamma$ (for instance $y' = \lambda y$ with equal slices, or one mode of a diagonalisable linear system with a fixed eigenbasis). Put $\alpha = |\varphi - \gamma|$, $\beta = |\gamma|$, $e^k_n = U^k_n - u_n$ and $M = \max_n|e^0_n|$. If $\beta \le 1$, then for $n \ge 1$

$$|e^k_n| \le M\alpha^k\binom{n-1}{k}, \qquad \text{hence} \qquad \max_n|e^k_n| \le M\frac{(\alpha(N - 1))^k}{k!}.$$

*Proof.* Since $u_{n+1} = \varphi u_n = \gamma u_n + (\varphi - \gamma)u_n$, subtracting from (P) gives

$$e^{k+1}_{n+1} = \gamma e^{k+1}_n + (\varphi - \gamma)e^k_n, \qquad e^{k+1}_0 = 0,$$

and unrolling, $e^{k+1}_n = (\varphi - \gamma)\sum_{j=0}^{n-1}\gamma^{n-1-j}e^k_j$. With $E^k_n = |e^k_n|$ and $\beta \le 1$, $E^{k+1}_n \le \alpha\sum_{j=1}^{n-1}E^k_j$, the term $j = 0$ vanishing because $e^k_0 = 0$. For $k = 0$ the claim is $E^0_n \le M$. If it holds for $k$, then

$$E^{k+1}_n \le \alpha\sum_{j=1}^{n-1}M\alpha^k\binom{j-1}{k} = M\alpha^{k+1}\sum_{i=0}^{n-2}\binom{i}{k} = M\alpha^{k+1}\binom{n-1}{k+1},$$

by the hockey-stick identity. Finally $\binom{n-1}{k} \le (n-1)^k/k! \le (N-1)^k/k!$. $\square$

For $n \le k$ the binomial coefficient vanishes, which recovers Theorem 2 in this case. If $\beta > 1$ the same argument gives the extra factor $\beta^{n-1-k}$, which is the instability of the coarse sweep.

**Corollary 5 (order increase, asymptotic).** Suppose the problem is $y' = \lambda y$ on $[t_0, T]$ with $\operatorname{Re}\lambda \le 0$, $\Delta T = (T - t_0)/N$, the coarse propagator has $|\gamma| \le 1$ and local error $|e^{\lambda\Delta T} - \gamma| \le C_G\Delta T^{p+1}$, and the fine propagator has $|e^{\lambda\Delta T} - \varphi| \le C_F\Delta T^{p+1}$ as well. Then $\alpha \le (C_G + C_F)\Delta T^{p+1}$ and $M \le (C_G + C_F)(T - t_0)\Delta T^p|y_0|\max(1, |\varphi|^N)$, which is $O(\Delta T^p)$ when $|\varphi| \le 1$. Theorem 4 gives

$$\max_n|e^k_n| \le M\frac{((C_G + C_F)(T - t_0)\Delta T^p)^k}{k!} = O(\Delta T^{p(k+1)}).$$

*Proof of the bound on $M$.* $e^0_n = (\gamma^n - \varphi^n)y_0$ and $\gamma^n - \varphi^n = (\gamma - \varphi)\sum_{j<n}\gamma^{n-1-j}\varphi^j$, each term at most $\max(1, |\varphi|^N)$ in modulus, and $|\gamma - \varphi| \le (C_G + C_F)\Delta T^{p+1}$; so $M \le N(C_G + C_F)\Delta T^{p+1}|y_0|\max(1,|\varphi|^N)$, and $N\Delta T = T - t_0$. $\square$

**What is proved, cited and observed.** Lemma 1, Theorem 2, Corollary 3, Theorem 4 and Corollary 5 are proved above. The linear bound on unbounded intervals, $\max_n|e^k_n| \le (\alpha/(1 - \beta))^kM$ for $\beta < 1$, is Gander and Vandewalle (2007), Section 4, and follows from the same recursion by summing the geometric series instead of bounding $\beta$ by 1. Nonlinear convergence bounds (Gander and Hairer, 2008) are cited, not proved. The convergence factors in the example tables and the speedup estimate are observations or cost-model estimates.
