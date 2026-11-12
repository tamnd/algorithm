---
title: Bresenham's line algorithm plots the nearest pixel in each step of the major axis
proves: [correctness, termination]
status: full
---

We prove the claim for the case $x_1 \ge x_0$, $y_1 \ge y_0$ and $d_y \le d_x$, where $d_x = x_1 - x_0$ and $d_y = y_1 - y_0$. In the other seven octants, the program of the page is the same program after a change of signs ($s_x$, $s_y$) and, when $d_y > d_x$, an exchange of the roles of the two axes (line L3). These maps send pixels to pixels and distances along an axis to equal distances, so the claim carries over with "column" read as "step of the major axis" and "nearer to the start" kept as it is. We write $m = d_x$ and $n = d_y$, so $0 \le n \le m$.

**Claim.** If $m = 0$, the program plots the one pixel $(x_0, y_0)$. If $m \ge 1$, the program plots exactly the $m + 1$ pixels $(x_0 + i, y_0 + k_i)$ for $i = 0, 1, \ldots, m$, with

$$k_i = \left\lceil \frac{i n}{m} - \frac12 \right\rceil .$$

The value $y_0 + k_i$ is the integer nearest to the exact height $y(x_0 + i) = y_0 + i n / m$ of the segment, and when two integers are equally near, it is the lower one, which is the one nearer to the start. The program uses only integers, and each value of $e$ satisfies $-2m < e \le 2m$.

**Termination.** The loop of line L5 runs exactly $m + 1$ times. If $m = 0$, then $n = 0$, the loop runs one time and plots $(x_0, y_0)$. From now on, $m \ge 1$.

**Notation.** Let $v_i = i n / m$. Write $x^{(i)}, y^{(i)}, e^{(i)}$ for the values of $x, y, e$ at line L6 of pass $i$, for $i = 0, \ldots, m$.

**Invariant.** At line L6 of pass $i$:

> **(B)** $x^{(i)} = x_0 + i$, $y^{(i)} = y_0 + k_i$, and $e^{(i)} = 2n(i + 1) - m(2k_i + 1)$.

*Initialization.* Line L4 sets $x = x_0$, $y = y_0$ and $e = 2n - m$. Since $-\tfrac12 < 0 \le \tfrac12$, we have $k_0 = \lceil -\tfrac12 \rceil = 0$. So $e^{(0)} = 2n - m = 2n(0 + 1) - m(2 \cdot 0 + 1)$, and (B) holds for $i = 0$.

*Maintenance.* Assume (B) holds for pass $i < m$. By the definition of the ceiling, $k_i - \tfrac12 < v_i \le k_i + \tfrac12$. Since $0 \le n/m \le 1$,

$$k_i - \tfrac12 < v_i \le v_{i+1} = v_i + \tfrac{n}{m} \le k_i + \tfrac32 .$$

So $v_{i+1} - \tfrac12$ lies in $(k_i - 1, k_i + 1]$, and $k_{i+1} = \lceil v_{i+1} - \tfrac12 \rceil$ is $k_i$ or $k_i + 1$. It is $k_i + 1$ exactly when $v_{i+1} - \tfrac12 > k_i$. Multiply this by $2m > 0$:

$$k_{i+1} = k_i + 1 \iff 2n(i+1) - m(2k_i + 1) > 0 \iff e^{(i)} > 0 .$$

This is the test of line L7. If $e^{(i)} > 0$, lines L8 to L10 add 1 to $y$ and change $e$ by $-2m + 2n$. Then $y = y_0 + k_i + 1 = y_0 + k_{i+1}$ and

$$e = 2n(i+1) - m(2k_i + 1) - 2m + 2n = 2n(i + 2) - m(2k_{i+1} + 1).$$

If $e^{(i)} \le 0$, then $k_{i+1} = k_i$, $y$ does not change, and line L10 adds $2n$, which gives $e = 2n(i + 2) - m(2k_{i+1} + 1)$. In both cases line L11 adds 1 to $x$, so $x = x_0 + i + 1$. So (B) holds for pass $i + 1$.

*Termination of the loop.* By (B), pass $i$ plots $(x_0 + i, y_0 + k_i)$, for $i = 0, \ldots, m$. The last pixel is $(x_0 + m, y_0 + k_m) = (x_1, y_0 + \lceil n - \tfrac12 \rceil) = (x_1, y_1)$.

**Nearest pixel.** For a real $v$, the integer $k = \lceil v - \tfrac12 \rceil$ satisfies $v - \tfrac12 \le k < v + \tfrac12$, so $|k - v| \le \tfrac12$. Each other integer $k'$ has $|k' - v| \ge 1 - |k - v| \ge \tfrac12$, with equality only when $|k - v| = \tfrac12$. So $k$ is a nearest integer to $v$. When two integers are equally near, $v - \tfrac12$ is an integer, $k = v - \tfrac12$, and $k$ is the lower one of the two. Apply this to $v = v_i$: the pixel $y_0 + k_i$ is the nearest to $y(x_0 + i)$, and a tie goes to the lower pixel. Since $y_1 \ge y_0$, the lower pixel is the one nearer to the start.

**Range of $e$.** By (B), $e^{(i)} = 2m(v_{i+1} - k_i - \tfrac12)$. The bounds above give $-1 < v_{i+1} - k_i - \tfrac12 \le 1$, so $-2m < e^{(i)} \le 2m$. The maintenance step does not use $i < m$, so the value of $e$ after the last pass is also in $(-2m, 2m]$. The only other value is $e - 2m$ after line L9, and line L9 runs only when $e > 0$, so this value is in $(-2m, 0]$. So if $2m$ fits in a machine integer, no value of $e$ overflows. $\blacksquare$
