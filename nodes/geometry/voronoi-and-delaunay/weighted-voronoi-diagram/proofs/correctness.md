---
title: The exact weighted Voronoi queries are correct
proves: [correctness]
status: full
---

**Claim.** Let $P$ be a set of distinct integer sites with integer weights, all $\ge 0$ in the additive mode and all $> 0$ in the multiplicative mode, and let $q$ have rational coordinates. Then $\mathrm{compare}$ returns the exact sign of the difference of the two weighted distances, $\mathrm{nearest}(q)$ returns exactly the sites at the smallest weighted distance from $q$, $\mathrm{hasCell}(p)$ is true exactly when the cell of $p$ has nonempty interior, and $\mathrm{bisector}$ returns the set of points at equal distance, with the shapes stated on the page. Also, a nonempty additive cell holds its site and is star-shaped around it.

No general position is assumed. Write $\delta_p(x) = |x - p| - w_p$ and $\mu_p(x) = |x - p| / w_p$.

**Lemma 1 (one root).** For rationals $x$, $y$ and $b \ge 0$, the routine for the sign of $x - y \sqrt{b}$ is right.

*Proof.* Let $s_1$ be the sign of $x$ and $s_2$ the sign of $y \sqrt{b}$, which is the sign of $y$ when $b > 0$ and $0$ when $b = 0$. If $s_2 = 0$, the value is $x$. If $s_1 \ne s_2$, the two terms $x$ and $-y \sqrt{b}$ do not have opposite signs, so the sign is $s_1$ when $s_1 \ne 0$ and $-s_2$ when $x = 0$. If $s_1 = s_2 \ne 0$, then $x - y\sqrt{b} = s_1 (|x| - |y| \sqrt{b})$, and $|x| - |y| \sqrt{b}$ has the sign of $x^2 - y^2 b$, because $t \mapsto t^2$ is increasing on $t \ge 0$. $\square$

**Lemma 2 (two roots).** For rationals $a, b \ge 0$ and $c$, the routine returns the sign of $\sqrt{a} - \sqrt{b} - c$.

*Proof.* Let $r$ be the sign of $\sqrt{b} + c$. If $c > 0$, or $c = 0$ and $b > 0$, then $r = 1$; if $c = 0$ and $b = 0$, then $r = 0$; if $c < 0$, then $\sqrt{b} + c > 0$ exactly when $b > c^2$, so $r$ is the sign of $b - c^2$. This is what the code computes. If $r \le 0$, then $\sqrt{a} - (\sqrt{b} + c) \ge \sqrt{a} \ge 0$, with equality exactly when $a = 0$ and $r = 0$. If $r > 0$, both $\sqrt{a}$ and $\sqrt{b} + c$ are $\ge 0$, so the sign of their difference is the sign of $a - (\sqrt{b} + c)^2 = (a - b - c^2) - 2 c \sqrt{b}$, which Lemma 1 computes. $\square$

**compare.** In the additive mode, $\delta_{p_i}(q) - \delta_{p_j}(q) = \sqrt{a} - \sqrt{b} - (w_i - w_j)$ with $a = |q - p_i|^2$ and $b = |q - p_j|^2$, rational, so Lemma 2 applies. In the multiplicative mode, $\mu_{p_i}(q) - \mu_{p_j}(q)$ has the sign of $|q - p_i| w_j - |q - p_j| w_i$, a difference of two numbers $\ge 0$, which has the sign of $|q - p_i|^2 w_j^2 - |q - p_j|^2 w_i^2$.

**nearest.** The loop keeps the invariant that $\mathrm{best}$ is the list of the sites with the smallest distance among those seen, in order. A site with a smaller distance replaces the list (line L3), a site with the same distance joins it (line L4), and a site with a larger distance is skipped. All comparisons are exact by the above. After the last site, line L5 returns the sites with the smallest distance.

**Additive hasCell.** Fix the site $p$ with weight $w_p$.

- *If $|p - r| > w_r - w_p$ for every other site $r$.* At $x = p$, $\delta_p(p) = -w_p$ and $\delta_r(p) = |p - r| - w_r > -w_p$. The functions are continuous, and there are finitely many sites, so a disc around $p$ has $\delta_p < \delta_r$ for all $r$, and it lies in the cell.
- *If $|p - r| \le w_r - w_p$ for some $r$.* For every $x$, $|x - r| \le |x - p| + |p - r| \le |x - p| + w_r - w_p$, so $\delta_r(x) \le \delta_p(x)$. Equality needs $|x - r| = |x - p| + |p - r|$, so $p$ is on the segment from $x$ to $r$, and $x$ is on the ray from $p$ away from $r$. So the cell of $p$ is inside this ray and has empty interior.

The code tests $\sqrt{|p - r|^2} - \sqrt{0} - (w_r - w_p) > 0$ with Lemma 2, which is the first condition.

**Multiplicative hasCell.** $\mu_p(p) = 0 < \mu_r(p)$ for every other $r$, so by continuity a disc around $p$ is in the cell.

**Additive bisector.** Let $k = w_p - w_r$. The bisector is $\{x : |x - p| - |x - r| = k\}$. By the triangle inequality $\left| |x - p| - |x - r| \right| \le |p - r|$.

- *$k = 0$.* The set $|x - p| = |x - r|$ is the perpendicular bisector line $2 (r - p) \cdot x = |r|^2 - |p|^2$, which is the triple the code returns.
- *$|k| > |p - r|$.* The set is empty.
- *$|k| = |p - r|$, say $k > 0$.* Then $|x - p| = |x - r| + |r - p|$, so $r$ is on the segment from $x$ to $p$, and $x$ is on the ray from $r$ away from $p$; every such point satisfies the equation. So the bisector is the ray that starts at the lighter site $r$ and points away from $p$. The case $k < 0$ is the same with the roles exchanged. The code tests $k^2 = |p - r|^2$ exactly.
- *$0 < |k| < |p - r|$.* The points with $\left| |x - p| - |x - r| \right| = |k|$ form the hyperbola with foci $p$ and $r$, and the sign of $|x - p| - |x - r|$ is constant on each of its two branches and different between them. So the bisector is one branch; for $k > 0$ its points are nearer to $r$, the lighter site.

**Multiplicative bisector.** If $w_p = w_r$, it is the line above. Otherwise let $D = w_r^2 - w_p^2 \ne 0$. The set $\mu_p(x) \le \mu_r(x)$ is $w_r^2 |x - p|^2 - w_p^2 |x - r|^2 \le 0$. Expanding, the left side is $D |x|^2 - 2 x \cdot (w_r^2 p - w_p^2 r) + w_r^2 |p|^2 - w_p^2 |r|^2 = D \left( |x - c|^2 - \rho^2 \right)$ with $c = (w_r^2 p - w_p^2 r)/D$ and

$$\rho^2 = |c|^2 - \frac{w_r^2 |p|^2 - w_p^2 |r|^2}{D} = \frac{w_p^2 w_r^2 |p - r|^2}{D^2},$$

where the last step expands $D^2 |c|^2 - D (w_r^2 |p|^2 - w_p^2 |r|^2)$ to $w_p^2 w_r^2 (|p|^2 - 2 p \cdot r + |r|^2)$. So the bisector is the circle of center $c$ and squared radius $\rho^2$, as the code returns. If $w_p < w_r$, then $D > 0$, and the region where $p$ is at least as near is the closed disc $|x - c| \le \rho$; it holds $p$, since the left side is $-w_p^2 |p - r|^2 < 0$ at $x = p$.

**Star-shaped additive cells.** Let $x$ be in the cell of $p$, and let $y$ be on the segment from $p$ to $x$. Then $|y - p| = |x - p| - |x - y|$, and for every other site $r$, $|y - r| \ge |x - r| - |x - y|$. So $\delta_r(y) \ge \delta_r(x) - |x - y| \ge \delta_p(x) - |x - y| = \delta_p(y)$, and $y$ is in the cell. Taking $y = p$ shows that a nonempty cell holds $p$, and the segments show that it is connected. $\blacksquare$
