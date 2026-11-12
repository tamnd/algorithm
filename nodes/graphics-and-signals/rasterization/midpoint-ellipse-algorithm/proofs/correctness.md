---
title: The midpoint ellipse algorithm applies the midpoint rule exactly and draws a connected quadrant from (0, b) to (a, 0)
proves: [correctness, termination]
status: full
---

Let $a, b \ge 0$ be integers and $F(x, y) = b^2 x^2 + a^2 y^2 - a^2 b^2$, which is negative inside the ellipse and positive outside. For $0 \le x \le a$ let $Y(x) = b(1 - x^2/a^2)^{1/2}$, and for $0 \le y \le b$ let $X(y) = a(1 - y^2/b^2)^{1/2}$. The pixel nearest to the ellipse in column $x$ is $(x, y)$ with $y - \tfrac12 < Y(x) \le y + \tfrac12$, and the pixel nearest in row $y$ is $(x, y)$ with $x - \tfrac12 < X(y) \le x + \tfrac12$. We prove five things about lines L1 to L12: the decision variables are $4F$ at the midpoints, no midpoint is on the ellipse, the program stops at $(a, 0)$ after at most $a + b$ passes, its pixels form an 8-connected chain, and a pixel nearest in its column (or row) stays so while the curve moves by less than one pixel per step.

**Invariants of the decision variables.** At line L3, (D1) $d_1 = 4F(x + 1, y - \tfrac12) = 4b^2(x+1)^2 + a^2(2y - 1)^2 - 4a^2b^2$. At line L8, (D2) $d_2 = 4F(x + \tfrac12, y - 1) = b^2(2x + 1)^2 + 4a^2(y-1)^2 - 4a^2b^2$.

*Proof of (D1).* Line L1 gives $x = 0$, $y = b$ and $d_1 = 4b^2 - 4a^2 b + a^2$, and $4b^2 + a^2(2b - 1)^2 - 4a^2b^2 = 4b^2 - 4a^2b + a^2$. If $d_1 < 0$, line L4 adds $4b^2(2x + 3) = 4b^2\big((x+2)^2 - (x+1)^2\big)$ and line L6 adds 1 to $x$. If $d_1 \ge 0$, line L5 also subtracts 1 from $y$ and adds $-8a^2(y - 1) = a^2\big((2y - 3)^2 - (2y - 1)^2\big)$. In both cases (D1) holds for the new values. *Proof of (D2).* Line L7 sets $d_2$ to the right side of (D2). If $d_2 < 0$, line L9 adds $8b^2(x + 1) = b^2\big((2x + 3)^2 - (2x + 1)^2\big)$ and $4a^2(3 - 2y) = 4a^2\big((y - 2)^2 - (y - 1)^2\big)$, adds 1 to $x$, and line L11 subtracts 1 from $y$. If $d_2 \ge 0$, line L10 adds only the second term. In both cases (D2) holds for the new values.

So in region 1 the program keeps the row of $(x, y)$ for column $x + 1$ exactly when the midpoint $(x + 1, y - \tfrac12)$ is inside, and in region 2 it moves to column $x + 1$ for row $y - 1$ exactly when the midpoint $(x + \tfrac12, y - 1)$ is inside. The test of line L3 is $F_y > F_x$ for the gradient $(F_x, F_y) = (2b^2 X, 2a^2 Y)$ at the midpoint $(X, Y) = (x + 1, y - \tfrac12)$, multiplied by $\tfrac12$.

**No midpoint is on the ellipse.** Let $a, b \ge 1$. A region 1 midpoint is $(u, v/2)$ with $u = x + 1$ an integer and $v = 2y - 1$ odd. Suppose $F(u, v/2) = 0$, that is $(u/a)^2 + (v/(2b))^2 = 1$. Write $v/(2b) = p/q$ in lowest terms with $q \ge 1$, and $u/a = r/q$. Then $r^2 = q^2 - p^2$ is an integer, so $r$ is an integer, and $p^2 + r^2 = q^2$ with $\gcd(p, q) = 1$. In such a triple $q$ is odd: if $q$ were even, $p$ would be odd, so $r$ would be odd, and $p^2 + r^2 \equiv 2 \pmod 4$ could not be a multiple of 4. From $vq = 2bp$ with $q$ odd, $v$ is even, a contradiction. A region 2 midpoint is $(u/2, w)$ with $u = 2x + 1$ odd and $w$ an integer, and the same argument with $a$ and $b$ exchanged applies. So $d_1 \ne 0$ and $d_2 \ne 0$ at each test, and the choice of the tie rule never changes the output. For $a = 0$ or $b = 0$ the ellipse is a segment, and the same holds for each midpoint that the program tests.

**Moves.** Each pass of region 1 moves the pixel by $(1, 0)$ or $(1, -1)$, each pass of region 2 by $(0, -1)$ or $(1, -1)$, and each pass of line L12 by $(1, 0)$. So consecutive pixels are 8-neighbors, $x$ never decreases and $y$ never increases.

**Lemma 1. No pass of region 1 starts at a pixel with $x \ge a$.** Since $x$ grows by one per pass, it is enough to show that no pass starts at $(a, y)$. Suppose one does. Its test gives $a^2(2y - 1) > 2b^2(a + 1)$, so $a, b \ge 1$ and $y \ge 1$. Call a pixel $(x, y)$ of region 1 *certified* if $F(x, y - \tfrac12) < 0$. The first pixel is certified, because $F(0, b - \tfrac12) = a^2\big((b - \tfrac12)^2 - b^2\big) < 0$, and by (D1) each pass with $d_1 < 0$ makes a certified pixel. The pixel $(a, y)$ is not certified, because $F(a, y - \tfrac12) = a^2(y - \tfrac12)^2 \ge 0$. Let $(x_k, y_k)$ be the last certified pixel before it, and $t = a - x_k \ge 1$. All the passes after it moved by $(1, -1)$, so $y_k = y + t$. The certificate gives $a^2(y_k - \tfrac12)^2 < b^2(a^2 - x_k^2) = b^2 t(2a - t)$, so

$$a\left(y - \tfrac12\right) = a\left(y_k - \tfrac12\right) - at < b\,(t(2a - t))^{1/2} - at.$$

The test at $(a, y)$ gives $a(y - \tfrac12) > b^2(a + 1)/a$. Together, and by the inequality of the arithmetic and geometric means,

$$b\,(t(2a - t))^{1/2} > at + \frac{b^2(a + 1)}{a} \ge 2\,(t\, b^2 (a + 1))^{1/2} = 2b\,(t(a + 1))^{1/2}.$$

Divide by $b\,t^{1/2}$ and square: $2a - t > 4a + 4$, which is false. $\square$

**Lemma 2. Region 2 never passes column $a$.** Line L9 moves to $x + 1$ only if $F(x + \tfrac12, y - 1) < 0$, so $b^2(x + \tfrac12)^2 < a^2 b^2$, so $x + 1 \le a$.

**Termination and the end point.** By Lemma 1 each pixel of region 1 has $x \le a$, so region 1 makes at most $a$ passes. Its test needs $y \ge 1$ at the start of each pass, so $y \ge 0$ after it. Region 2 makes exactly $y$ passes and stops at $y = 0$, with $x \le a$ by Lemma 2. Line L12 then moves along row 0 to $x = a$. So the last pixel is $(a, 0)$. Each pass adds 1 to $x$ or subtracts 1 from $y$ or both, $x$ goes from 0 to $a$ and $y$ from $b$ to 0, so there are at most $a + b$ passes and at most $a + b + 1$ pixels.

**Lemma 3. The midpoint rule keeps the nearest pixel while the curve moves by less than one pixel per step.** In region 1, let the pixel $(x, y)$ be the nearest in column $x$, with $x + 1 \le a$ and $Y(x) - Y(x + 1) < 1$. If $d_1 < 0$, the new pixel is $(x + 1, y)$, and $y - \tfrac12 < Y(x + 1) \le Y(x) \le y + \tfrac12$. If $d_1 > 0$, the new pixel is $(x + 1, y - 1)$, and $Y(x + 1) < y - \tfrac12$, while $Y(x + 1) > Y(x) - 1 > y - \tfrac32$. In both cases the new pixel is the nearest in column $x + 1$. In region 2 the same argument with the roles of $x$ and $y$ exchanged shows: if $(x, y)$ is the nearest in row $y$ and $X(y - 1) - X(y) < 1$, the new pixel is the nearest in row $y - 1$. $\square$

**Consequences.** The first pixel $(0, b)$ is the nearest in column 0. The function $Y$ is concave, so the drops $Y(x) - Y(x + 1)$ grow with $x$. So by Lemma 3, each pixel of region 1 is the nearest in its column up to the first column where the drop of the curve reaches one pixel. In the same way, the drops $X(y - 1) - X(y)$ shrink as $y$ goes down, so once a pixel of region 2 is the nearest in its row at a row where the drop is below one, all the later pixels of region 2 are the nearest in their rows. If region 1 reaches row 0 at a column $x < a$, its last pass had $F(x, \tfrac12) > 0$, so $Y(x') < \tfrac12$ for each $x' > x$, and the pixels $(x', 0)$ of line L12 are the nearest in their columns. The pixel $(a, 0)$ is always the nearest in column $a$.

**Symmetry.** The ellipse is symmetric under $(x, y) \mapsto (\pm x, \pm y)$, and so are the nearest pixels. So PLOT-4 maps the quadrant to the other three quadrants, and the four chains meet at $(0, \pm b)$ and $(\pm a, 0)$. $\blacksquare$
