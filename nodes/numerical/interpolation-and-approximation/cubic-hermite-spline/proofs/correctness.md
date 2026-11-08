---
title: The cubic Hermite spline interpolates values and slopes, is C^1, and has error at most h^4 max|f''''|/384 with exact slopes
proves: [correctness, termination, error-bound]
status: full
---

We use the notation of the page: increasing knots $x_0 < \cdots < x_n$ with $n \ge 1$, values $y_k$, slopes $d_k$, $h_k = x_{k+1} - x_k$, and the basis $h_{00}, h_{10}, h_{01}, h_{11}$ on $[0, 1]$.

## Claim 1: termination and the interval

Line L1 is a binary search over a sorted array of $n + 1$ entries, which ends after at most $\lceil \log_2(n + 1) \rceil + 1$ comparisons, and the clamp puts $k$ in $\{0, \ldots, n - 1\}$. For $t \in [x_0, x_n)$, $k$ is the unique index with $x_k \le t < x_{k+1}$; for $t = x_n$ the clamp gives $k = n - 1$. Lines L2 to L6 are straight-line code; $h > 0$ because the knots are distinct.

## Claim 2: the basis

Direct computation gives $h_{00}(0) = 1$, $h_{00}(1) = 0$, $h_{00}'(\sigma) = 6\sigma^2 - 6\sigma$, so $h_{00}'(0) = h_{00}'(1) = 0$. Similarly $h_{01} = 1 - h_{00}$ has values $0, 1$ and zero end slopes. $h_{10} = \sigma(1 - \sigma)^2$ has values $0, 0$ and $h_{10}' = (1 - \sigma)(1 - 3\sigma)$, so $h_{10}'(0) = 1$, $h_{10}'(1) = 0$. $h_{11} = \sigma^2(\sigma - 1)$ has values $0, 0$ and $h_{11}' = 3\sigma^2 - 2\sigma$, so $h_{11}'(0) = 0$, $h_{11}'(1) = 1$.

## Claim 3: interpolation and continuity

Let $P_k(t)$ be the expression of line L6 with $\sigma = (t - x_k)/h_k$, a cubic in $t$. Since $d\sigma/dt = 1/h_k$, Claim 2 gives $P_k(x_k) = y_k$, $P_k(x_{k+1}) = y_{k+1}$, $P_k'(x_k) = h_k \cdot d_k / h_k = d_k$ and $P_k'(x_{k+1}) = d_{k+1}$. So $s = P_k$ on $[x_k, x_{k+1}]$ satisfies $s(x_k) = y_k$ and $s'(x_k) = d_k$ for every $k$, the one-sided values and slopes of neighboring pieces agree at each interior knot, and $s \in C^1[x_0, x_n]$. By the uniqueness of [Hermite interpolation](/hermite-interpolation/) with the nodes $x_k, x_k, x_{k+1}, x_{k+1}$, $P_k$ is the only cubic with these four conditions; in particular, if $y_k = q(x_k)$ and $d_k = q'(x_k)$ for a cubic polynomial $q$, then every $P_k = q$.

## Claim 4: the error bound

Assume $f \in C^4[x_0, x_n]$, $y_k = f(x_k)$ and $d_k = f'(x_k)$. Fix $t \in (x_k, x_{k+1})$ and let $\psi(\tau) = (\tau - x_k)^2(\tau - x_{k+1})^2$. Define
$$g(\tau) = f(\tau) - P_k(\tau) - c\, \psi(\tau), \qquad c = \frac{f(t) - P_k(t)}{\psi(t)},$$
so that $g(t) = 0$. Also $g(x_k) = g'(x_k) = g(x_{k+1}) = g'(x_{k+1}) = 0$ by Claim 3 and since $\psi$ has double roots at both ends. Rolle's theorem on $[x_k, t]$ and $[t, x_{k+1}]$ gives zeros $\eta_1 < \eta_2$ of $g'$ strictly inside these intervals; together with $x_k$ and $x_{k+1}$, $g'$ has four distinct zeros $x_k < \eta_1 < \eta_2 < x_{k+1}$. Applying Rolle three more times, $g^{(4)}$ has a zero $\xi \in (x_k, x_{k+1})$. Since $P_k^{(4)} = 0$ and $\psi^{(4)} = 24$, this gives $f^{(4)}(\xi) = 24c$, that is
$$f(t) - s(t) = \frac{f^{(4)}(\xi)}{24} (t - x_k)^2 (t - x_{k+1})^2.$$
The factor $(t - x_k)^2(t - x_{k+1})^2$ is largest at the midpoint, where it equals $h_k^4/16$, so $|f(t) - s(t)| \le h_k^4 \|f^{(4)}\|_\infty / 384$. At the knots the error is zero. $\square$

## Claim 5: slope errors

If the slopes are $d_k = f'(x_k) + e_k$, the value of line L6 changes by $h_k(h_{10}(\sigma) e_k + h_{11}(\sigma) e_{k+1})$, because the expression is linear in the slopes. On $[0, 1]$, $|h_{10}|$ is largest where $h_{10}' = 0$, at $\sigma = 1/3$, with value $4/27$, and likewise $|h_{11}| \le 4/27$ (at $\sigma = 2/3$). So the change is at most $\tfrac{8}{27} h_k \max(|e_k|, |e_{k+1}|)$.
