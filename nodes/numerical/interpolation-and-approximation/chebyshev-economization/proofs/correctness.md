---
title: Correctness of Chebyshev economization
proves: [correctness, error-bound, one-term-minimax, near-minimax]
status: full
---

Let $p(x) = \sum_{k=0}^N b_kx^k$, and let $T_k(x) = \cos(k\arccos x)$ on $[-1, 1]$, with $T_0 = 1$, $T_1 = x$ and $T_{k+1} = 2xT_k - T_{k-1}$.

**Claim 1 (multiplication by $x$).** If $r = \sum_{j=0}^{L}d_jT_j$, then $xr = \sum_{j=0}^{L+1}d'_jT_j$, where $d'$ is obtained by adding $d_0$ to $d'_1$ and, for each $j \ge 1$, adding $d_j/2$ to both $d'_{j+1}$ and $d'_{j-1}$.

*Proof.* $xT_0 = T_1$, and the recurrence gives $xT_j = \frac12(T_{j+1} + T_{j-1})$ for $j \ge 1$. Multiply by $d_j$ and add. $\square$

**Claim 2 (lines L1 and L2 convert to the Chebyshev basis).** After line L2, $\sum_{k=0}^Nc_kT_k = p$.

*Proof.* Let $r_N = b_N$ and $r_k = xr_{k+1} + b_k$ for $k = N-1, \ldots, 0$; by Horner's rule $r_0 = p$. Invariant: when the loop of L2 has processed index $k$, the list $c$ holds the Chebyshev coefficients of $r_k$. This holds at the start ($r_N = b_NT_0$, line L1). Each step applies Claim 1 to get $xr_{k+1}$ and adds $b_k = b_kT_0$ to the coefficient of $T_0$, which gives $r_k$. The list length grows by one per step, ending at $N + 1$. $\square$

**Claim 3 (error bound, lines L3 and L4).** Let $m$ and $e$ be the values returned. Then $e = \sum_{k=m+1}^N|c_k| \le \tau$, and for every $x \in [-1, 1]$,
$$\Big|p(x) - \sum_{k=0}^mc_kT_k(x)\Big| \le e.$$
The bound is attained at $x = 1$ if the dropped $c_k$ have one sign, and at $x = -1$ if $(-1)^kc_k$ has one sign.

*Proof.* Line L3 maintains $e = \sum_{k=m+1}^N|c_k|$ and only decreases $m$ when the new sum stays at most $\tau$; the loop stops after at most $N$ steps. By Claim 2 the difference is $\sum_{k>m}c_kT_k(x)$, and $|T_k(x)| \le 1$ gives the bound. Since $T_k(1) = 1$ and $T_k(-1) = (-1)^k$, the sum equals $\pm e$ at the stated endpoint in the two sign cases. $\square$

**Claim 4 (one dropped term is optimal).** If $N \ge 1$, $b_N \ne 0$ and only $c_NT_N$ is dropped, then $q = \sum_{k<N}c_kT_k$ is the best approximation of $p$ of degree at most $N - 1$ in the maximum norm on $[-1, 1]$, and $E_{N-1}(p) = |c_N| = |b_N|2^{1-N}$.

*Proof.* The leading coefficient of $T_k$ is $2^{k-1}$ for $k \ge 1$, and only $T_N$ has degree $N$ among $T_0, \ldots, T_N$, so $c_N2^{N-1} = b_N$. The error $p - q = c_NT_N$ takes the values $c_N(-1)^j$ at the $N + 1$ points $x_j = \cos(j\pi/N)$, alternating in sign with absolute value equal to its maximum norm. By the Chebyshev equioscillation theorem (sufficiency direction: an error that equioscillates at $N + 1$ points is optimal for degree $N - 1$), $q$ is the best approximation. Directly: if some $\tilde q$ of degree at most $N - 1$ had $\|p - \tilde q\|_\infty < |c_N|$, then $\tilde q - q = (p - q) - (p - \tilde q)$ would have the sign of $c_N(-1)^j$ at each $x_j$, hence $N$ sign changes and $N$ zeros, so $\tilde q = q$, a contradiction. $\square$

**Claim 5 (near-optimality).** Let $q^*$ be a best approximation of $p$ of degree at most $m$ and $E_m = \|p - q^*\|_\infty$. Then $|c_k| \le 2E_m$ for every $k > m$. If moreover $|c_{k+1}| \le r|c_k|$ for all $k > m$ with $0 \le r < 1$, then the economized error satisfies $e \le \frac{2}{1 - r}E_m$.

*Proof.* With the weight $w(x) = (1 - x^2)^{-1/2}$ the Chebyshev polynomials are orthogonal, $\int_{-1}^1T_jT_kw\,dx = 0$ for $j \ne k$ and $\frac\pi2$ for $j = k \ge 1$. So $c_k = \frac2\pi\int_{-1}^1pT_kw\,dx$ for $k \ge 1$, and since $q^*$ has degree at most $m < k$, also $c_k = \frac2\pi\int_{-1}^1(p - q^*)T_kw\,dx$. Hence $|c_k| \le \frac2\pi E_m\int_{-1}^1w\,dx = 2E_m$. Under the decay hypothesis, $e = \sum_{k>m}|c_k| \le |c_{m+1}|\sum_{i \ge 0}r^i \le \frac{2E_m}{1 - r}$. $\square$

**Claim 6 (lines L5 and L6).** TO-MONOMIAL returns the monomial coefficients of $\sum_{k \le m}c_kT_k$.

*Proof.* Line L5 builds the monomial coefficients of $T_0 = 1$, $T_1 = x$ and $T_k = 2xT_{k-1} - T_{k-2}$ by the recurrence (multiplying by $2x$ shifts the coefficient list by one place and doubles it). Line L6 adds $c_k$ times them, so after the loop the list holds $\sum_k c_kT_k$ by linearity. $\square$

**Termination.** Line L2 runs $N$ steps, L3 at most $N$, and L5 and L6 $m + 1$ steps, each of bounded length. Claims 2 and 3 show that ECONOMIZE returns a polynomial within the reported bound $e \le \tau$ of $p$ on $[-1, 1]$.
