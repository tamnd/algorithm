---
title: A z-map cut sets each column to the lowest point of the swept ball-end tool
proves: [correctness, termination]
status: full
---

**Setting.** The tool is a ball-end mill of radius $r > 0$ with its axis parallel to $z$. With the ball center at $c$, the tool is the set $T(c)$ = the closed ball of radius $r$ about $c$, together with the half-infinite cylinder $\{p : (p_x - c_x)^2 + (p_y - c_y)^2 \le r^2,\ p_z \ge c_z\}$. A linear move takes the center along $c(t) = c_0 + t(c_1 - c_0)$ for $t \in [0, 1]$, and the swept volume is $S = \bigcup_{t \in [0,1]} T(c(t))$. Fix a column point $q = (q_x, q_y)$ and write $d(t)$ for the horizontal distance from $q$ to $(c_x(t), c_y(t))$.

**Claim.** Let $\Theta = \{t \in [0, 1] : d(t) \le r\}$ and $f(t) = c_z(t) - \sqrt{r^2 - d(t)^2}$ on $\Theta$. Then:

1. $S \cap (\{q\} \times \mathbb{R})$ is empty if $\Theta$ is empty, and otherwise it is $\{q\} \times [z_{lo}, \infty)$ with $z_{lo} = \min_\Theta f$;
2. LOWEST of lines L6 to L17 returns None exactly when $\Theta$ is empty, and otherwise returns $z_{lo}$;
3. after CUT, each column height is $\min(H_{\text{old}}, z_{lo})$, clamped at the stock bottom, and a column outside the box of line L1 has $\Theta$ empty.

All real numbers are exact in the proof. The code computes the same formulas in floating point.

**Step 1 (one position).** Fix $t$. If $d(t) > r$, neither the ball nor the cylinder meets the vertical line at $q$. If $d(t) \le r$, let $w = \sqrt{r^2 - d(t)^2}$. The ball meets the line in $[c_z - w, c_z + w]$ and the cylinder meets it in $[c_z, \infty)$. Their union is $[c_z - w, \infty) = [f(t), \infty)$, since $w \ge 0$.

**Step 2 (all positions).** So the line meets $S$ in $\bigcup_{t \in \Theta} [f(t), \infty)$. The function $d(t)^2$ is a convex quadratic in $t$, so $\Theta$ is a closed interval or empty. On $\Theta$, $f$ is continuous, so it has a minimum $z_{lo}$, and the union is $[z_{lo}, \infty)$. This proves part 1.

**Step 3 (convexity).** Write $a = (c_{0x} - q_x, c_{0y} - q_y)$, $b = (c_{1x} - c_{0x}, c_{1y} - c_{0y})$, $s = c_{1z} - c_{0z}$, $A = a \cdot a$, $k = a \cdot b$, $B = b \cdot b$, and $R = r^2 - A$, as in lines L6 and L7. Then $d(t)^2 = g(t) = A + 2kt + Bt^2$. The map $\varphi(u) = -\sqrt{r^2 - u}$ is convex and nondecreasing on $(-\infty, r^2]$, and $g$ is convex, so $\varphi \circ g$ is [convex](/convex-function/). Adding the linear term $c_{0z} + ts$ keeps it convex. So $f$ is convex on $\Theta$.

**Step 4 (no horizontal motion).** If $B = 0$ (line L8), then $g(t) = A$ for all $t$. If $A > r^2$, $\Theta$ is empty, and line L9 returns None. Otherwise $\Theta = [0, 1]$ and $f(t) = c_{0z} + ts - \sqrt{R}$ is linear with slope $s$, so its minimum is at $t = 0$ when $s \ge 0$ and at $t = 1$ when $s < 0$, as in line L10.

**Step 5 (the closed form).** Let $B > 0$ and put $u = k + tB$. Then $g(t) = A + (u^2 - k^2)/B$, so
$$r^2 - g(t) = \frac{D - u^2}{B}, \qquad D = k^2 + BR.$$
Hence $g(t) \le r^2$ if and only if $u^2 \le D$. If $D < 0$, no real $t$ has $g(t) \le r^2$, and line L12 returns None. If $D \ge 0$, the real $t$ with $g(t) \le r^2$ form $[t_a, t_b]$ with $t_{a,b} = (-k \mp \sqrt D)/B$, and $\Theta = [t_a, t_b] \cap [0, 1] = [lo, hi]$ of line L13. If $lo > hi$, $\Theta$ is empty and line L14 returns None. This proves the None cases of part 2.

Now let $\Theta = [lo, hi]$ be non-empty. Put $t^* = (-k - s\sqrt{D/(B + s^2)})/B$, as in line L15, so $u^* = k + t^*B = -s\sqrt{D/(B + s^2)}$. If $D = 0$ then $t_a = t_b = t^* = -k/B$, and $\Theta$ is the single point $t^*$, so the clamp of line L16 returns it. Let $D > 0$. Then $u^{*2} = s^2 D/(B + s^2) < D$, because $B > 0$, so $t^*$ lies in the open interval $(t_a, t_b)$, where $f$ is differentiable with
$$f'(t) = s + \frac{g'(t)}{2\sqrt{r^2 - g(t)}} = s + \frac{u\sqrt B}{\sqrt{D - u^2}}.$$
At $t^*$, $D - u^{*2} = DB/(B + s^2)$, so $\sqrt B/\sqrt{D - u^{*2}} = \sqrt{B + s^2}/\sqrt D$, and the second term is $-s\sqrt{D/(B + s^2)} \cdot \sqrt{B + s^2}/\sqrt D = -s$. So $f'(t^*) = 0$. A convex function with zero derivative at an interior point has its minimum over $[t_a, t_b]$ there, and it is nonincreasing to the left of $t^*$ and nondecreasing to the right. So its minimum over the subinterval $[lo, hi]$ is at the point of $[lo, hi]$ nearest to $t^*$, which is the clamp of line L16. Line L17 evaluates $f$ there. This proves part 2.

**Step 6 (the cut).** If $\Theta$ is not empty, there is a $t$ with $d(t) \le r$, so $|q_x - c_x(t)| \le r$ and $|q_y - c_y(t)| \le r$. Since $c_x(t)$ lies between $c_{0x}$ and $c_{1x}$, $q_x$ lies in $[\min(c_{0x}, c_{1x}) - r, \max(c_{0x}, c_{1x}) + r]$, and the same holds for $y$. So the columns that line L1 skips have $\Theta$ empty, and the tool does not touch them. For each other column, by part 1 the stock that remains on the line is the old interval $[z_{\text{bottom}}, H_{\text{old}}]$ minus $[z_{lo}, \infty)$, whose top is $\min(H_{\text{old}}, z_{lo})$, or nothing if $z_{lo}$ is below the bottom. Lines L4 and L5 store exactly this, with the empty column stored as height $z_{\text{bottom}}$. This proves part 3.

**Termination.** CUT visits a finite box of columns and does a constant amount of work per column. $\blacksquare$

**Remark (what the z-map does not represent).** Part 1 holds because the tool has a shank that goes up forever. For a tool without a shank, or a tool that is not parallel to $z$, the line can meet the swept volume in a bounded interval, and the stock left on the line is two intervals. A z-map cannot store that. The [dexel representation](/dexel-representation/) can.
