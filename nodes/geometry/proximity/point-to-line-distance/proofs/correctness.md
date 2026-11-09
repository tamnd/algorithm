---
title: The cross product formula gives the squared distance from a point to a line
proves: [correctness, termination]
status: full
---

**Claim.** Let $a \ne b$ and $p$ be points of the plane, $u = b - a$ and $w = p - a$. Then POINT-LINE-DISTANCE-SQUARED returns $(\delta^2, f)$ where

$$\delta^2 = \min_{t \in \mathbb{R}} \|p - (a + t u)\|^2 = \frac{(u \times w)^2}{u \cdot u},$$

and $f$ is the unique point of the line $\ell = \{a + t u : t \in \mathbb{R}\}$ with $\|p - f\|^2 = \delta^2$. The algorithm has no loop, so it terminates after lines L1 to L7.

**Step 1 (the minimum exists and is unique).** For $t \in \mathbb{R}$ let $g(t) = \|p - (a + t u)\|^2 = \|w - t u\|^2$. Expanding the dot product,

$$g(t) = (w \cdot w) - 2 t\,(w \cdot u) + t^2 (u \cdot u).$$

Since $a \ne b$, $u \ne 0$ and $u \cdot u > 0$. Completing the square,

$$g(t) = (u \cdot u)\left(t - \frac{w \cdot u}{u \cdot u}\right)^2 + (w \cdot w) - \frac{(w \cdot u)^2}{u \cdot u}.$$

The first term is non-negative and is zero exactly at $t^* = (w \cdot u)/(u \cdot u)$. So $g$ has the unique minimizer $t^*$, and the minimum is $g(t^*) = (w \cdot w) - (w \cdot u)^2/(u \cdot u)$. Line L5 computes $t^*$ and line L6 computes $f = a + t^* u$, which is therefore the unique nearest point of $\ell$ to $p$.

**Step 2 (Lagrange's identity in the plane).** For $u = (u_x, u_y)$ and $w = (w_x, w_y)$,

$$(u_x^2 + u_y^2)(w_x^2 + w_y^2) - (u_x w_x + u_y w_y)^2 = u_x^2 w_y^2 + u_y^2 w_x^2 - 2 u_x w_x u_y w_y = (u_x w_y - u_y w_x)^2.$$

The first equality expands both products and cancels $u_x^2 w_x^2$ and $u_y^2 w_y^2$; the second is the square of a difference. So $(u \cdot u)(w \cdot w) - (w \cdot u)^2 = (u \times w)^2$.

**Step 3 (line L7).** Divide the identity of Step 2 by $u \cdot u > 0$:

$$g(t^*) = (w \cdot w) - \frac{(w \cdot u)^2}{u \cdot u} = \frac{(u \times w)^2}{u \cdot u}.$$

Line L4 computes $c = u \times w$, so line L7 returns $c^2/(u \cdot u) = g(t^*) = \delta^2$.

**Step 4 (the foot is perpendicular).** $(p - f) \cdot u = (w - t^* u) \cdot u = (w \cdot u) - t^* (u \cdot u) = 0$. So the segment from $p$ to $f$ is orthogonal to the line, as the name "foot of the perpendicular" says.

**Exactness.** Lines L2 to L7 use only subtraction, multiplication and division by $u \cdot u \ne 0$. The rationals are closed under these operations, so for rational input the returned values are the exact rationals of the claim. $\blacksquare$

**Remark (the line equation form).** With $\alpha = u_y$, $\beta = -u_x$ and $\gamma = u_x a_y - u_y a_x$, the value $\alpha x + \beta y + \gamma$ at $p = (x, y)$ is $u_y (x - a_x) - u_x (y - a_y) = -(u \times w)$, and $\alpha^2 + \beta^2 = u \cdot u$. So the quotient $(\alpha x + \beta y + \gamma)^2/(\alpha^2 + \beta^2)$ is the same number $\delta^2$. A general equation $\lambda(\alpha x + \beta y + \gamma) = 0$ with $\lambda \ne 0$ multiplies the numerator and the denominator by $\lambda^2$, so the formula holds for every equation of the line.
