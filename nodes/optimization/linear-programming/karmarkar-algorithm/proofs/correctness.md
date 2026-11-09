---
title: The potential drops by at least 1/8 at each step of Karmarkar's algorithm
proves: [correctness, termination]
status: full
---

**Statement.** Let $n \ge 3$, let $A e = 0$, and let the program $\min\{c^\top x : Ax = 0, e^\top x = 1, x \ge 0\}$ have the optimal value $0$. Let $x > 0$ be feasible with $c^\top x > 0$, and let $x'$ be the point of line L7 with $\alpha = 1/4$, in the case $p \ne 0$. Then $x' > 0$ is feasible, and $f(x') \le f(x) - 1/8$ for $f(z) = n \ln(c^\top z) - \sum_j \ln z_j$. As a result, KARMARKAR returns a feasible $x > 0$ with $c^\top x \le \varepsilon \, c^\top(e/n)$ after at most $8 n \ln(1/\varepsilon)$ steps.

**Step 1 (the projective map).** Let $X = \operatorname{diag}(x)$ and $\Delta = \{y \ge 0 : e^\top y = 1\}$. For $y \in \Delta$ with $y > 0$ let $z = Xy / (e^\top X y)$. Then $z > 0$, $e^\top z = 1$, and $Az = AXy / (e^\top Xy)$, so $z$ is feasible if and only if $AXy = 0$. Let $s = e^\top X y$ and $\bar c = Xc$. Then $c^\top z = \bar c^\top y / s$ and $z_j = x_j y_j / s$, so

$$f(z) = n \ln(\bar c^\top y) - n \ln s - \sum_j \ln x_j - \sum_j \ln y_j + n \ln s = g(y) - \sum_j \ln x_j,$$

with $g(y) = n \ln(\bar c^\top y) - \sum_j \ln y_j$. The point $y = e/n$ maps to $z = x$. Hence $f(x') - f(x) = g(y) - g(e/n)$ for the point $y$ of line L6. Also, if $x^*$ is an optimal point, then $y^* = X^{-1}x^* / (e^\top X^{-1} x^*)$ is in $\Delta$, has $AXy^* = 0$, and has $\bar c^\top y^* = 0$.

**Step 2 (feasibility of $y$).** Let $S = \{y : AXy = 0, e^\top y = 1\}$ and let $B$ be the matrix with rows $AX$ and $e^\top$. The vector $p$ is in the null space of $B$, so $y = e/n - \alpha r p/\|p\|$ is in $S$. Let $t = ny - e$. Then $\|t\| = n \alpha r = \alpha \sqrt{n/(n-1)} \le \alpha \sqrt{3/2} =: \beta$, using $n \ge 3$. With $\alpha = 1/4$, $\beta < 0.31$. Each $|t_j| \le \|t\| < 1$, so $y_j = (1 + t_j)/n > 0$, and $x' > 0$ is feasible by Step 1.

**Step 3 (the linear term).** Every $w \in \Delta$ has $\|w - e/n\|^2 = \sum_j w_j^2 - 1/n \le 1 - 1/n$, so $\Delta$ lies in the ball of radius $R = \sqrt{(n-1)/n}$ about $e/n$. For $w \in S$, the vector $w - e/n$ is in the null space of $B$, so $\bar c^\top (w - e/n) = p^\top (w - e/n) \ge -\|p\| \, \|w - e/n\|$, since $\bar c - p$ is orthogonal to that null space. With $w = y^*$ from Step 1:

$$0 = \bar c^\top y^* \ge \bar c^\top(e/n) - \|p\| R, \quad \text{so} \quad \|p\| \ge \bar c^\top(e/n)/R.$$

The step gives $\bar c^\top y = \bar c^\top(e/n) - \alpha r \|p\| \le \bar c^\top(e/n)\,(1 - \alpha r/R)$, and $r/R = 1/(n-1)$. Since $\ln(1 - u) \le -u$,

$$n \ln \frac{\bar c^\top y}{\bar c^\top(e/n)} \le -\frac{n \alpha}{n-1} \le -\alpha.$$

The logarithm is defined: $\bar c^\top y = s \, c^\top x' \ge 0$, because $x'$ is feasible and the optimal value is $0$. If $\bar c^\top y = 0$, then $x'$ is optimal, $f(x') = -\infty$, the claim holds, and the test of line L2 stops the method at once. So assume $\bar c^\top y > 0$.

**Step 4 (the barrier term).** For $|u| \le \beta < 1$,

$$\ln(1 + u) = u - \sum_{k \ge 2} \frac{(-u)^k}{k} \ge u - \frac{1}{2} \sum_{k \ge 2} |u|^k = u - \frac{u^2}{2(1 - |u|)} \ge u - \frac{u^2}{2(1-\beta)}.$$

With $u = t_j$, and since $\sum_j t_j = n e^\top y - n = 0$ and $\sum_j t_j^2 \le \beta^2$:

$$-\sum_j \ln(n y_j) = -\sum_j \ln(1 + t_j) \le -\sum_j t_j + \frac{\sum_j t_j^2}{2(1-\beta)} \le \frac{\beta^2}{2(1-\beta)}.$$

**Step 5 (the drop).** By Steps 3 and 4,

$$g(y) - g(e/n) = n \ln \frac{\bar c^\top y}{\bar c^\top(e/n)} - \sum_j \ln(n y_j) \le -\alpha + \frac{\beta^2}{2(1-\beta)}.$$

For $\alpha = 1/4$, $\beta^2 = 3/32$ and $1 - \beta > 0.69$, so the right side is at most $-0.25 + 0.068 < -1/8$. By Step 1, $f(x') \le f(x) - 1/8$.

**Step 6 (the bound on the steps).** Let $x_0 = e/n$ and $x_k$ the point after $k$ steps. Since $e^\top x_k = 1$, the inequality of arithmetic and geometric means gives $\sum_j \ln x_{k,j} \le n \ln(1/n)$, so $f(x_k) \ge n \ln(c^\top x_k) + n \ln n$, with equality for $k = 0$. By Step 5, $f(x_k) \le f(x_0) - k/8$. Together,

$$n \ln(c^\top x_k) \le n \ln(c^\top x_0) - k/8, \quad \text{so} \quad c^\top x_k \le e^{-k/(8n)} c^\top x_0.$$

For $k \ge 8n \ln(1/\varepsilon)$ this is at most $\varepsilon\, c^\top x_0$, and the test of line L2 stops the loop. Line L5 stops it earlier only if $p = 0$; then $\bar c$ is in the row space of $B$, so $\bar c^\top y$ is constant on $S$, and $c^\top z$ is constant on the feasible set. With the optimal value $0$, this constant is $0 = c^\top x$, which the test of line L2 catches first. So with valid input the method returns at line L8 a feasible point with $c^\top x \le \varepsilon \, c^\top (e/n)$. $\blacksquare$

**Remark.** Karmarkar's paper proves a drop of $1/8$ with $\alpha = 1/4$ by a similar argument. The bound of Step 2 uses $n \ge 3$; with the cruder $\sqrt{n/(n-1)} \le \sqrt 2$, the barrier term is at most $0.097$ and the drop is still more than $1/8$.
