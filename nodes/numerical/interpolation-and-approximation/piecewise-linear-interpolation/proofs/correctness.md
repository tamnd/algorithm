---
title: Piecewise linear interpolation returns the broken line through the data, with its error bound
proves: [correctness, termination, error]
status: full
---

**Setting.** The nodes satisfy $x_0 < x_1 < \cdots < x_n$, the data are $y_0, \ldots, y_n$, and $s$ is the continuous function that is linear on each $[x_j, x_{j+1}]$ with $s(x_j) = y_j$. On $[x_j, x_{j+1}]$, $s(t) = (1 - \lambda) y_j + \lambda y_{j+1}$ with $\lambda = (t - x_j)/(x_{j+1} - x_j)$; the two formulas of neighboring intervals agree at the common node, so $s$ is well defined and continuous.

**Theorem 1.** For $x_0 \le t \le x_n$, PL-INTERPOLATE$(x, y, t)$ terminates and returns $s(t)$.

*Proof.* If $n = 0$, then $t = x_0$ and line L1 returns $y_0 = s(t)$. Let $n \ge 1$. We show that this invariant holds at each test of line L3:

> **(B)** $0 \le lo < hi \le n$ and $x_{lo} \le t \le x_{hi}$.

*Initialization.* Line L2 sets $lo = 0$ and $hi = n \ge 1$, and $x_0 \le t \le x_n$ by the precondition.

*Maintenance.* If $hi - lo > 1$, line L4 gives $lo < mid < hi$, because $1 \le \lfloor (hi - lo)/2 \rfloor < hi - lo$. If $x_{mid} \le t$, line L5 sets $lo = mid$, and $x_{lo} \le t \le x_{hi}$ with $lo < hi$. Otherwise $t < x_{mid}$ and line L5 sets $hi = mid$, with the same conclusion.

*Termination.* Let $g = hi - lo$. A pass replaces $g$ by $mid - lo = \lfloor g/2 \rfloor$ or by $hi - mid = g - \lfloor g/2 \rfloor = \lceil g/2 \rceil$. For $g \ge 2$ both are at most $g - 1$, so $g$ drops by at least 1 in each pass, and the loop stops after at most $n - 1$ passes, in fact after at most $\lceil \log_2 n \rceil$ since $\lceil g/2 \rceil \le g/2 + 1/2$. At the exit, (B) holds and $hi - lo \le 1$, so $hi = lo + 1$ and $x_{lo} \le t \le x_{lo+1}$.

*Result.* Line L6 computes $\lambda = (t - x_{lo})/(x_{lo+1} - x_{lo})$, which lies in $[0, 1]$, and line L7 returns $(1 - \lambda) y_{lo} + \lambda y_{lo+1}$, which is $s(t)$ by the formula of the interval $[x_{lo}, x_{lo+1}]$. $\square$

**Theorem 2 (error).** If $f \in C^2[x_0, x_n]$ and $y_j = f(x_j)$, then $|f(t) - s(t)| \le \tfrac{1}{8} h^2 \max |f''|$ for all $t \in [x_0, x_n]$, where $h = \max_j (x_{j+1} - x_j)$.

*Proof.* Fix $t$ in $[x_j, x_{j+1}]$. If $t$ is a node the error is 0. Otherwise, let $e(u) = f(u) - s(u) - K (u - x_j)(u - x_{j+1})$ on $[x_j, x_{j+1}]$, with $K$ chosen so that $e(t) = 0$. Then $e$ has the three zeros $x_j < t < x_{j+1}$, so by Rolle's theorem $e'$ has two zeros and $e''$ has one zero $\xi$. Since $s'' = 0$ on the open interval, $e''(\xi) = f''(\xi) - 2K = 0$, so $f(t) - s(t) = \tfrac{1}{2} f''(\xi)(t - x_j)(t - x_{j+1})$. The quadratic $|(t - x_j)(t - x_{j+1})|$ is largest at the midpoint, where it equals $(x_{j+1} - x_j)^2/4 \le h^2/4$. $\square$

**Theorem 3 (stability and shape).** For all $t \in [x_0, x_n]$, $\min_j y_j \le s(t) \le \max_j y_j$. If $y_0 \le y_1 \le \cdots \le y_n$, then $s$ is nondecreasing. If the slopes $\delta_j = (y_{j+1} - y_j)/(x_{j+1} - x_j)$ are nondecreasing in $j$, then $s$ is convex.

*Proof.* $s(t)$ is a convex combination of two data values, which gives the first claim. On each interval $s$ has slope $\delta_j$; monotone data give $\delta_j \ge 0$ for all $j$, and a continuous function with nonnegative slope on each piece is nondecreasing. Let $\ell_k$ be the line through the piece $k$, extended to all of $[x_0, x_n]$. For $t$ in the piece $j$ and $k < j$, $s$ and $\ell_k$ agree at $x_{k+1}$, and from $x_{k+1}$ to $t$ the slope of $s$ is $\delta_{k+1}, \ldots, \delta_j \ge \delta_k$, so $s(t) \ge \ell_k(t)$. For $k > j$ the same argument runs from $x_k$ to the left, with slopes at most $\delta_k$. So $s = \max_k \ell_k$, and a maximum of linear functions is convex. $\blacksquare$
