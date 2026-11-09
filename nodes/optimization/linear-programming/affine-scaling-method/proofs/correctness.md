---
title: Each step of affine scaling stays feasible and lowers the cost, and its answers are correct
proves: [correctness]
status: full
---

**Statement.** Let $x > 0$ with $Ax = b$, let $A$ have full row rank, and let $y$, $r$, $d$ be the vectors of lines L3, L4 and L6. Then:

1. $Ad = 0$ and $c^\top d = -\|Xr\|^2$.
2. If the method reaches line L8, then $\max_j x_j r_j > 0$, and the new point $x'$ satisfies $Ax' = b$, $x' \ge (1 - \gamma) x > 0$, and $c^\top x' = c^\top x - t\|Xr\|^2 < c^\top x$ with $t = \gamma / \max_j x_j r_j$.
3. If the method returns OPTIMAL$(x, y)$, then $y$ is dual feasible and $c^\top x - \text{OPT} \le c^\top x - b^\top y = x^\top r \le \varepsilon$.
4. If the method returns UNBOUNDED$(d)$, then $d \ge 0$, $Ad = 0$ and $c^\top d < 0$, so the program is unbounded.

**Step 1 (claim 1).** Since $A$ has full row rank and $X$ is nonsingular, $AX^2A^\top = (AX)(AX)^\top$ is positive definite, so $y$ is well defined, and $AX^2 A^\top y = AX^2 c$. Then

$$Ad = -AX^2 r = -AX^2 c + AX^2 A^\top y = 0.$$

Since $c = r + A^\top y$, $c^\top d = r^\top d + y^\top A d = -r^\top X^2 r = -\|Xr\|^2$.

**Step 2 (claim 2).** Line L7 returns if $d \ge 0$. Since $d_j = -x_j (x_j r_j)$ with $x_j > 0$, $d \ge 0$ holds exactly when $x_j r_j \le 0$ for all $j$. So at line L8 some $x_j r_j > 0$, and $t > 0$ is defined. For each $j$,

$$x'_j = x_j + t d_j = x_j (1 - t x_j r_j) \ge x_j \left(1 - \gamma \frac{x_j r_j}{\max_k x_k r_k}\right) \ge (1 - \gamma) x_j,$$

since $x_j r_j / \max_k x_k r_k \le 1$ (and if $x_j r_j \le 0$, then $x'_j \ge x_j$). With $\gamma < 1$ this gives $x' > 0$. By Step 1, $Ax' = Ax + tAd = b$ and $c^\top x' = c^\top x - t\|Xr\|^2$. Here $\|Xr\| > 0$, since some $x_j r_j > 0$, so the cost falls strictly.

**Step 3 (claim 3).** Line L5 returns only if $r = c - A^\top y \ge 0$, which says that $y$ is feasible for the dual program $\max\{b^\top y : A^\top y \le c\}$. By weak duality, $b^\top y \le \text{OPT} \le c^\top x$. And $c^\top x - b^\top y = c^\top x - y^\top A x = (c - A^\top y)^\top x = x^\top r$, which line L5 bounds by $\varepsilon$.

**Step 4 (claim 4).** Line L7 returns only if $d \ge 0$. By Step 1, $Ad = 0$. If $d = 0$, then $Xr = 0$ since $X$ is nonsingular, so $r = 0$ and $x^\top r = 0$, and line L5 would have returned first. So $d \ne 0$, $\|Xr\| > 0$, and $c^\top d = -\|Xr\|^2 < 0$. For every $t \ge 0$, $x + td \ge 0$ and $A(x + td) = b$, while $c^\top(x + td) \to -\infty$. $\blacksquare$

**Remark.** The proof shows that every answer is correct and that the cost falls at every step. It does not show that the method reaches the stop test of line L5. For that, see Bertsimas and Tsitsiklis (Section 9.2) for the nondegenerate case, and Tsuchiya and Muramatsu (1995) for the general case with $\gamma \le 2/3$. The implementation also uses a relative tolerance in the tests of lines L5 and L7.
