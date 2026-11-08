---
title: Correctness of Fritsch-Carlson monotone interpolation
proves: [correctness, shape-preservation]
status: full
---

Let $x_0 < \cdots < x_n$, $n \ge 1$, with $h_k = x_{k+1} - x_k$ and $\delta_k = (y_{k+1} - y_k)/h_k$. On $[x_k, x_{k+1}]$ write $u = (t - x_k)/h_k$ and $v = 1 - u$.

**Claim 1 (interpolation and $C^1$).** The function $s$ of line L6 satisfies $s(x_k) = y_k$ and $s'(x_k) = d_k$ from both sides, so $s \in C^1[x_0, x_n]$.

*Proof.* $P(u) = y_kv^2(1 + 2u) + y_{k+1}u^2(1 + 2v) + h_k(d_kuv^2 - d_{k+1}u^2v)$. At $u = 0$: $P = y_k$; at $u = 1$: $P = y_{k+1}$. Differentiating, $\frac{dP}{du} = 6uv(y_{k+1} - y_k) + h_k\big(d_k(v^2 - 2uv) - d_{k+1}(2uv - u^2)\big)$, which is $h_kd_k$ at $u = 0$ and $h_kd_{k+1}$ at $u = 1$. Since $\frac{ds}{dt} = \frac1{h_k}\frac{dP}{du}$, the one-sided derivatives at $x_k$ are $d_k$ from both neighbouring pieces. $\square$

**Claim 2 (the derivative of a piece).** If $\delta_k \ne 0$, then $s'(t) = \delta_k\,g(u)$ with $\alpha = d_k/\delta_k$, $\beta = d_{k+1}/\delta_k$ and
$$g(u) = 6u(1 - u) + \alpha(1 - 4u + 3u^2) + \beta(3u^2 - 2u).$$

*Proof.* From the derivative in Claim 1, divide by $h_k$: $s' = 6uv\delta_k + d_k(v^2 - 2uv) + d_{k+1}(u^2 - 2uv)$. Now $v^2 - 2uv = (1 - u)(1 - 3u) = 1 - 4u + 3u^2$ and $u^2 - 2uv = u^2 - 2u + 2u^2 = 3u^2 - 2u$. Factor out $\delta_k$. $\square$

**Claim 3 (the square condition).** If $0 \le \alpha \le 3$ and $0 \le \beta \le 3$, then $g(u) \ge 0$ for $u \in [0, 1]$.

*Proof.* For fixed $u$, $g$ is affine in $(\alpha, \beta)$, so its minimum over the square is at a corner:
$g(0, 0) = 6u(1 - u)$, $g(3, 0) = 6u - 6u^2 + 3 - 12u + 9u^2 = 3(1 - u)^2$, $g(0, 3) = 6u - 6u^2 + 9u^2 - 6u = 3u^2$, $g(3, 3) = 12u^2 - 12u + 3 = 3(2u - 1)^2$. All are nonnegative on $[0, 1]$. $\square$

The quarter disk $\{\alpha, \beta \ge 0,\ \alpha^2 + \beta^2 \le 9\}$ lies in the square, so the same conclusion holds on it.

**Claim 4 (signs after line L2).** After L2, for every $k$ with $\delta_k \ne 0$, $d_k\delta_k \ge 0$ and $d_{k+1}\delta_k \ge 0$.

*Proof.* For an interior node $j$, L2 sets $d_j = 0$ unless $\delta_{j-1}\delta_j > 0$, and then $d_j$ is a convex combination of $\delta_{j-1}$ and $\delta_j$ (weights $h_j/(h_{j-1} + h_j)$ and $h_{j-1}/(h_{j-1} + h_j)$), so it has their common sign. An end slope is set to $0$ when its sign differs from the adjacent secant, and otherwise has that sign (also after the replacement by $3\delta$). For $n = 1$, $d_0 = d_1 = \delta_0$. So each slope is zero or has the sign of every adjacent nonzero secant. $\square$

**Claim 5 (invariant of lines L3 and L4).** After the pass, for every $k$: if $\delta_k = 0$ then $d_k = d_{k+1} = 0$; otherwise $\alpha_k, \beta_k \ge 0$ and $\alpha_k^2 + \beta_k^2 \le 9$.

*Proof.* The pass only multiplies slopes by factors in $[0, 1]$ (setting to $0$ in L3, or by $\tau < 1$ in L4), so the signs of Claim 4 are kept, and $|d_j|$ never increases. When the pass treats interval $k$ it ensures the condition for interval $k$: if $\delta_k = 0$ both slopes become 0; otherwise either $\sqrt{d_k^2 + d_{k+1}^2} \le 3|\delta_k|$ already, or after scaling $\sqrt{d_k^2 + d_{k+1}^2} = 3|\delta_k|$. Later steps change only $d_{k+1}$ (when treating interval $k + 1$), and only by shrinking it toward 0, which keeps $(\alpha_k, \beta_k)$ in the quarter disk, and keeps $d_k = d_{k+1} = 0$ if they were zero. $\square$

**Theorem (shape preservation).** On each $[x_k, x_{k+1}]$: if $y_{k+1} > y_k$, $s$ is nondecreasing; if $y_{k+1} < y_k$, nonincreasing; if $y_{k+1} = y_k$, constant equal to $y_k$. Consequently $\min(y_k, y_{k+1}) \le s \le \max(y_k, y_{k+1})$ on the interval, and every local extremum of $s$ in the interior of $[x_0, x_n]$ is attained at a node.

*Proof.* If $\delta_k \ne 0$, Claims 2, 3 and 5 give $s' = \delta_kg(u)$ with $g \ge 0$, so $s'$ has the sign of $\delta_k$ or is $0$. If $\delta_k = 0$, then $y_{k+1} = y_k$ and $d_k = d_{k+1} = 0$ by Claim 5, so $P(u) = y_k\big(v^2(1 + 2u) + u^2(1 + 2v)\big)$. With $1 = u + v$, $v^2(1 + 2u) = v^3 + 3uv^2$ and $u^2(1 + 2v) = u^3 + 3u^2v$, which add up to $(u + v)^3 = 1$, so $P(u) = y_k$. A monotone function on an interval lies between its endpoint values. A strict local extremum inside an interval would contradict monotonicity there, so local extrema of $s$ occur at nodes. $\square$

**Termination and cost.** Every loop runs a fixed number of times ($n$ or $n + 1$), and evaluation uses one binary search, so the algorithm terminates in $O(n)$ operations for setup and $O(\log n)$ per point.
