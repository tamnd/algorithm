---
title: The midpoint circle algorithm plots the nearest pixel in each column of the octant
proves: [correctness, termination]
status: full
---

Let $r \ge 0$ be an integer, $F(x, y) = x^2 + y^2 - r^2$, and $Y(x) = (r^2 - x^2)^{1/2}$ for $0 \le x \le r$. The octant is the arc of the circle with $0 \le x \le y$. We prove three things about the loop of lines L2 to L6: it stops, the value $d$ is $F$ at the midpoint minus $\tfrac14$, and each plotted pixel $(x, y)$ has $y$ equal to the integer nearest to $Y(x)$, with no tie possible. PLOT-8 then gives the other seven octants by the symmetries $(x, y) \mapsto (\pm x, \pm y), (\pm y, \pm x)$ of the circle, which map pixels to pixels.

**No ties.** For integers $x$ and $y$, the equation $(y + \tfrac12)^2 = r^2 - x^2$ means $(2y + 1)^2 = 4(r^2 - x^2)$. The left side is odd and the right side is even, so this is impossible. So $Y(x)$ is never half way between two integers, and the nearest integer to $Y(x)$ is unique. In the same way, $F(x, y - \tfrac12) = x^2 + y^2 - y + \tfrac14 - r^2$ is an integer plus $\tfrac14$, so it is never zero.

**Termination.** Each pass adds 1 to $x$ (line L6) and does not increase $y$. So $y - x$ drops by at least 1 per pass. It starts at $r$, and the loop stops when it is negative, so there are at most $r + 1$ passes.

**Invariant.** Write $(x, y, d)$ for the values at line L2 at the start of a pass. Then:

> **(C1)** $d = F(x + 1, y - \tfrac12) - \tfrac14 = (x + 1)^2 + y^2 - y - r^2$.
>
> **(C2)** If $x \le y$, then $|y - Y(x)| < \tfrac12$, so $y$ is the integer nearest to $Y(x)$.

*Initialization.* Line L1 sets $x = 0$, $y = r$, $d = 1 - r$. Then $(0 + 1)^2 + r^2 - r - r^2 = 1 - r$, so (C1) holds. And $Y(0) = r = y$, so (C2) holds.

*Maintenance of (C1).* If $d < 0$, line L4 adds $2x + 3$ and line L6 adds 1 to $x$. The new value of the right side of (C1) is $(x + 2)^2 + y^2 - y - r^2 = d + 2x + 3$. If $d \ge 0$, line L5 adds $2(x - y) + 5$ and subtracts 1 from $y$. The new right side is

$$(x + 2)^2 + (y - 1)^2 - (y - 1) - r^2 = d + (2x + 3) + (-2y + 1) + 1 = d + 2(x - y) + 5.$$

So (C1) holds at the start of the next pass.

*The test.* By (C1), $F(x + 1, y - \tfrac12) = d + \tfrac14$ with $d$ an integer. So $d < 0$ if and only if $F(x + 1, y - \tfrac12) < 0$. For $t \ge 0$ the function $t \mapsto F(x+1, t)$ is increasing, and it is zero at $t = Y(x + 1)$ when $x + 1 \le r$. If $x + 1 > r$, then $F(x+1, t) > 0$ for each $t$, and the program steps $y$ down. So:

- if $d < 0$, then $Y(x + 1) > y - \tfrac12$, and the new pixel is $(x + 1, y)$;
- if $d \ge 0$, then $Y(x + 1) < y - \tfrac12$ (or $x + 1 > r$), and the new pixel is $(x + 1, y - 1)$.

*Maintenance of (C2).* Assume (C2) for the pass at $(x, y)$, and let $(x', y')$ be the new values, with $x' = x + 1$. We must show $|y' - Y(x')| < \tfrac12$ when $x' \le y'$.

Case $d < 0$. Then $y' = y$ and $Y(x') > y - \tfrac12$. Also $Y(x') < Y(x) < y + \tfrac12$, because $Y$ is decreasing and by (C2). So $|y' - Y(x')| < \tfrac12$.

Case $d \ge 0$. Then $y' = y - 1$ and $Y(x') < y - \tfrac12 = y' + \tfrac12$ (if $x' > r$ then $x' > y'$ and there is nothing to prove). We must show $Y(x') > y' - \tfrac12 = y - \tfrac32$ when $x' \le y'$, that is when $y \ge x + 2$. Suppose instead that $Y(x + 1) \le y - \tfrac32$. By (C2), $Y(x) > y - \tfrac12$, so $Y(x) - Y(x + 1) > 1$. Also

$$Y(x)^2 - Y(x+1)^2 = (x + 1)^2 - x^2 = 2x + 1,$$

so $Y(x) + Y(x + 1) = (2x + 1)/(Y(x) - Y(x+1)) < 2x + 1$. On the other side, $y \ge x + 2$ gives $Y(x) > y - \tfrac12 \ge x + \tfrac32$, and

$$Y(x + 1)^2 = Y(x)^2 - 2x - 1 > \left(x + \tfrac32\right)^2 - 2x - 1 = x^2 + x + \tfrac54 > \left(x + \tfrac12\right)^2,$$

so $Y(x+1) > x + \tfrac12$. Then $Y(x) + Y(x + 1) > 2x + 2$, a contradiction. So $|y' - Y(x')| < \tfrac12$.

**Conclusion.** Each pass plots $(x, y)$ at line L3 with $x \le y$, and by (C2) $y$ is the unique nearest integer to $Y(x)$. The values of $x$ are $0, 1, 2, \ldots$ with no gap, so the octant gets one pixel in each column from $x = 0$ to the last column with $x \le y$. When the loop stops, the last pixel $(x, y)$ has $y - x \in \{0, 1\}$: if the last pass kept $y$, then $x + 1 > y$, and if it stepped, then $x + 1 > y - 1$. So the last pixel is at the diagonal, and the eight images of the octant cover the whole circle.

**Range of $d$.** At line L4, (C1) gives $d = 2x + 1 - y - (r^2 - x^2 - y^2)$. By (C2), $(y - \tfrac12)^2 < r^2 - x^2 < (y + \tfrac12)^2$, so $-y + \tfrac14 < r^2 - x^2 - y^2 < y + \tfrac14$. With $0 \le x \le y \le r$, this gives $2x - 2y + \tfrac34 < d < 2x + \tfrac54$, so $-2r < d < 2r + 2$ at each test. The update after the last test adds at most $2x + 3 \le 2r + 3$ or $2(x - y) + 5 \le 5$. So each value of $d$ has absolute value at most $4r + 5$. $\blacksquare$
