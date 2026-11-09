---
title: The clamped projection gives the squared distance from a point to a segment
proves: [correctness, termination]
status: full
---

**Claim.** Let $a$, $b$ and $p$ be points of $\mathbb{R}^2$, $u = b - a$, $w = p - a$, and $S = \{a + t u : 0 \le t \le 1\}$. POINT-SEGMENT-DISTANCE-SQUARED returns $(\delta^2, c)$ with $c \in S$ and

$$\|p - c\|^2 = \delta^2 = \min_{x \in S} \|p - x\|^2 .$$

The algorithm has no loop and stops after at most eight lines.

**Notation.** For $t \in \mathbb{R}$ let $g(t) = \|p - (a + t u)\|^2 = \|w - t u\|^2 = (w \cdot w) - 2 t s + t^2 D$, where $s = w \cdot u$ (line L3) and $D = u \cdot u$ (line L5). Then $\delta^2 = \min_{0 \le t \le 1} g(t)$; the minimum exists because $g$ is continuous on a closed interval.

**Case 0: $a = b$.** Then $u = 0$, $s = 0$, and line L4 returns $(w \cdot w, a)$. The segment is the single point $a$ and $\|p - a\|^2 = w \cdot w$, so the claim holds.

From now on $u \ne 0$, so $D > 0$. Completing the square gives

$$g(t) = D\,(t - t^*)^2 + g(t^*), \qquad t^* = s / D .$$

So for $t_1, t_2$ on the same side of $t^*$, $g(t_1) < g(t_2)$ exactly when $|t_1 - t^*| < |t_2 - t^*|$. In particular $g$ is strictly increasing on $[t^*, \infty)$ and strictly decreasing on $(-\infty, t^*]$.

**Case 1: $s \le 0$ (line L4).** Then $t^* \le 0$ because $D > 0$. Every $t \in [0, 1]$ satisfies $t \ge 0 \ge t^*$, and $g$ is increasing on $[t^*, \infty)$, so $g(t) \ge g(0)$. Hence $\delta^2 = g(0) = w \cdot w$ and $c = a$, which is what line L4 returns.

**Case 2: $s > 0$ and $s \ge D$ (line L6).** Then $t^* = s / D \ge 1$. Every $t \in [0, 1]$ satisfies $t \le 1 \le t^*$, and $g$ is decreasing on $(-\infty, t^*]$, so $g(t) \ge g(1)$. Hence $\delta^2 = g(1) = \|p - b\|^2$ and $c = b$, which is what line L6 returns.

**Case 3: $0 < s < D$ (lines L7 and L8).** Then $0 < t^* < 1$, so $t^* \in [0, 1]$ and $g(t) \ge g(t^*)$ for all $t$. Hence $\delta^2 = g(t^*)$ and $c = a + t^* u$. By the completed square, $g(t^*) = (w \cdot w) - s^2 / D$. Lagrange's identity in the plane, $(u \cdot u)(w \cdot w) - (u \cdot w)^2 = (u \times w)^2$ (expanded in the correctness proof of the [point-line distance](/point-to-line-distance/)), gives $g(t^*) = (u \times w)^2 / D$. Line L7 computes $u \times w$ and line L8 returns $((u \times w)^2 / D, a + (s/D) u)$.

**The cases are exhaustive.** If $u \ne 0$, either $s \le 0$, or $s > 0$ and $s \ge D$, or $0 < s < D$. Line L4 tests the first, line L6 the second, and the rest reach line L8. When line L5 runs, $s > 0$, which is impossible if $u = 0$; so no division by zero happens.

**Exactness.** All operations are additions, multiplications, and one division by $D \ne 0$, so for rational input the returned values are the exact rationals of the claim. $\blacksquare$

**Remark (dimension $d$).** Cases 0 to 2 do not use the dimension. In Case 3, $g(t^*) = (w \cdot w) - s^2/D$ holds in every dimension, so returning this value instead of $(u \times w)^2/D$ gives the algorithm for $\mathbb{R}^d$.
