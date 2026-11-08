---
title: An explicit Runge-Kutta method of order p converges with global error O(h^p)
proves: [correctness, termination, convergence]
status: full
---

**Setting.** We use a norm $\|\cdot\|$ on $\mathbb{R}^d$. The function $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is continuous and Lipschitz in $y$ with constant $L$: $\|f(t, u) - f(t, v)\| \le L\|u - v\|$. By the [Picard-Lindelöf theorem](/picard-lindelof-theorem/), $y' = f(t, y)$, $y(t_0) = y_0$ has a unique solution $y$ on $[t_0, T]$. The tableau $(A, b, c)$ is explicit ($a_{ij} = 0$ for $j \ge i$) and satisfies $c_i = \sum_j a_{ij}$. Put $\alpha = \max_i \sum_j |a_{ij}|$ and $\beta = \sum_i |b_i|$. The step sizes are $h_n = t_{n+1} - t_n \le h$.

**Termination and what the loop computes.** Line L5 gives a finite $N \ge 0$, and the loop of line L7 runs $N$ times. By induction on $n$, after iteration $n$ the variables hold $t = t_{n+1}$ and $y = y_{n+1} = y_n + h_n \Phi(t_n, y_n, h_n)$, where the increment function is $\Phi(t, u, h) = \sum_{i=1}^s b_i k_i(t, u, h)$ and $k_i = f(t + c_i h, u + h\sum_{j<i} a_{ij} k_j)$. Lines L1 to L3 compute $k_1, \ldots, k_s$ in this order: each $k_i$ uses only $k_j$ with $j < i$, which exist. The last grid point is $t_N = T$ by line L8.

**Lemma 1 (the increment is Lipschitz).** For all $t$, $u$, $v$ and $0 < h' \le h$,
$$\|\Phi(t, u, h') - \Phi(t, v, h')\| \le \Lambda \|u - v\|, \qquad \Lambda = L\beta(1 + hL\alpha)^{s-1}.$$

*Proof.* Let $\delta_i = \|k_i(t, u, h') - k_i(t, v, h')\|$ and $\varepsilon = \|u - v\|$. We show $\delta_i \le L(1 + hL\alpha)^{i-1}\varepsilon$ by induction on $i$. For $i = 1$, $\delta_1 = \|f(t, u) - f(t, v)\| \le L\varepsilon$. For $i > 1$, the Lipschitz condition gives $\delta_i \le L(\varepsilon + h\sum_{j<i}|a_{ij}|\delta_j) \le L(\varepsilon + h\alpha\max_{j<i}\delta_j) \le L(\varepsilon + h\alpha L(1 + hL\alpha)^{i-2}\varepsilon) \le L(1 + hL\alpha)^{i-1}\varepsilon$, since $1 + x(1 + x)^{i-2} \le (1 + x)^{i-1}$ for $x \ge 0$. Then $\|\Phi(u) - \Phi(v)\| \le \sum_i |b_i| \delta_i \le \Lambda\varepsilon$. $\square$

**Lemma 2 (order 1 and 2).** Let $f \in C^2$. The local error $\ell(t, h) = y(t + h) - y(t) - h\Phi(t, y(t), h)$ is $O(h^2)$ if and only if $\sum_i b_i = 1$, and $O(h^3)$ if and only if moreover $\sum_i b_i c_i = \frac12$.

*Proof.* Write $y = y(t)$ and $f, f_t, f_y$ for the values at $(t, y)$. By Taylor's theorem, $y(t + h) = y + h f + \frac{h^2}{2}(f_t + f_y f) + O(h^3)$. For the stages, $k_i = f + h c_i f_t + h f_y \sum_j a_{ij} k_j + O(h^2)$, and $k_j = f + O(h)$, so $k_i = f + h c_i (f_t + f_y f) + O(h^2)$, by $\sum_j a_{ij} = c_i$. Hence $h\Phi = h(\sum_i b_i) f + h^2(\sum_i b_i c_i)(f_t + f_y f) + O(h^3)$. Compare the coefficients of $h$ and $h^2$. Both directions hold because $f$ and $f_t + f_y f$ are not zero for a general problem. $\square$

For a general order $p$, the local error is $O(h^{p+1})$ when $f \in C^p$ and the tableau satisfies the order conditions $\Phi(\tau) = 1/\gamma(\tau)$ for all rooted trees $\tau$ with at most $p$ vertices (Butcher's theorem; HNW I, Section II.2; Butcher 2016, Chapter 3). We use this as a known result. The conditions up to $p = 4$ are listed on the page.

**Theorem (convergence).** Assume that the local error satisfies $\|\ell(t_n, h_n)\| \le C h_n^{p+1}$ for each step. Then, with $e_n = y(t_n) - y_n$,
$$\|e_n\| \le \frac{C h^p}{\Lambda}\left(e^{\Lambda(t_n - t_0)} - 1\right) \qquad \text{for } 0 \le n \le N.$$

*Proof.* Split the error of step $n$:
$$e_{n+1} = \ell(t_n, h_n) + e_n + h_n\left(\Phi(t_n, y(t_n), h_n) - \Phi(t_n, y_n, h_n)\right).$$
By Lemma 1, $\|e_{n+1}\| \le (1 + h_n\Lambda)\|e_n\| + C h^p h_n$. We show the claim by induction on $n$. For $n = 0$, $e_0 = 0$. Write $E_n = e^{\Lambda(t_n - t_0)}$. If $\|e_n\| \le \frac{Ch^p}{\Lambda}(E_n - 1)$, then
$$\|e_{n+1}\| \le \frac{Ch^p}{\Lambda}\left((1 + h_n\Lambda)E_n - 1 - h_n\Lambda + h_n\Lambda\right) = \frac{Ch^p}{\Lambda}\left((1 + h_n\Lambda)E_n - 1\right) \le \frac{Ch^p}{\Lambda}(E_{n+1} - 1),$$
because $1 + x \le e^x$ gives $(1 + h_n\Lambda)E_n \le E_{n+1}$. $\blacksquare$

**Remarks.** The bound is non-asymptotic. It needs only the global Lipschitz condition, the local error bound, and $e_0 = 0$. When $f$ is Lipschitz only near the solution, the same proof works in a tube around the solution for $h$ small enough. A rounding error $\eta$ per step adds $\eta/h$ times the same factor to the bound.
