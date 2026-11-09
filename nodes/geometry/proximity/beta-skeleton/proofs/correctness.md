---
title: The exact region test and BUILD compute the lune-based beta-skeleton, and the skeletons shrink as beta grows
proves: [correctness, termination]
status: full
---

**Setting.** $P$ is a set of distinct points in the plane and $\beta > 0$ is rational. For distinct $p, q$ put $w = q - p$, $L = \|w\|$, $m = (p + q)/2$, and for a point $r$ put $u = p - r$, $v = q - r$, $u \cdot v$ their dot product and $u \times v = u_x v_y - u_y v_x$ their cross product. The open lune-based region $R_\beta(p, q)$ of Kirkpatrick and Radke is:

- for $\beta \ge 1$, the intersection of the open disks of radius $\beta L / 2$ centered at $c_1 = p + \frac{\beta}{2} w$ and $c_2 = q - \frac{\beta}{2} w$;
- for $0 < \beta < 1$, the intersection of the two open disks of radius $\rho = L / (2\beta)$ whose boundary circles pass through $p$ and $q$.

The closed region uses closed disks. We prove the claims for open regions; the closed case is the same with $<$ replaced by $\le$ throughout.

**Lemma 1 (the case $\beta \ge 1$).** Lines L8 and L9 return true exactly when $r \in R_\beta(p, q)$. Moreover, $r \in R_\beta(p, q)$ if and only if $\|r - p\|^2 < \beta\,(r - p) \cdot w$ and $\|r - q\|^2 < -\beta\,(r - q) \cdot w$.

*Proof.* Line L8 computes $c_1$, $c_2$ and $\rho^2 = (\beta/2)^2 L^2$ in exact rational arithmetic, and line L9 compares $\|r - c_1\|^2$ and $\|r - c_2\|^2$ with $\rho^2$, which is the definition. For the second form, expand $\|r - c_1\|^2 = \|(r - p) - \frac{\beta}{2} w\|^2 = \|r - p\|^2 - \beta (r - p) \cdot w + \frac{\beta^2}{4} L^2$; this is less than $\frac{\beta^2}{4} L^2$ exactly when $\|r - p\|^2 < \beta (r - p) \cdot w$. The disk around $c_2$ is symmetric, with $p$ and $q$ exchanged and $w$ replaced by $-w$. $\square$

**Lemma 2 (the case $\beta < 1$).** Lines L10 and L11 return true exactly when $r \in R_\beta(p, q)$. Moreover, $r \in R_\beta(p, q)$ if and only if $u \cdot v < -\frac{\sqrt{1 - \beta^2}}{\beta} |u \times v|$.

*Proof.* Let $n$ be a unit normal of $pq$. A circle through $p$ and $q$ has its center on the perpendicular bisector, at $c_t = m + t n$ for some real $t$, and its squared radius is $L^2/4 + t^2$. Put $s = n \cdot (r - m)$. Then $\|r - c_t\|^2 = \|r - m\|^2 - 2ts + t^2$, so $r$ is inside the circle exactly when $\|r - m\|^2 - L^2/4 < 2ts$. The identity $u \cdot v = \|r - m\|^2 - L^2/4$ holds (write $u = (m - r) - w/2$ and $v = (m - r) + w/2$). The two circles of radius $\rho$ have $t = \pm h$ with $h = \sqrt{\rho^2 - L^2/4}$, so $r$ is in both disks exactly when $u \cdot v < \min(2hs, -2hs) = -2h|s|$. Now $|s| \cdot L$ is twice the area of the triangle $pqr$, which is $|u \times v|$, and $2h / L = \sqrt{4\rho^2/L^2 - 1} = \sqrt{1/\beta^2 - 1} = \sqrt{1 - \beta^2}/\beta$. This gives the second form.

For the test of line L11: the right side is at most $0$, so the condition implies $u \cdot v < 0$. When $u \cdot v < 0$, both sides of $-u \cdot v > \frac{\sqrt{1 - \beta^2}}{\beta}|u \times v|$ are non-negative, so squaring gives the equivalent $\beta^2 (u \cdot v)^2 > (1 - \beta^2)(u \times v)^2$. Using $(u \times v)^2 = \|u\|^2 \|v\|^2 - (u \cdot v)^2$, this becomes $(u \cdot v)^2 > (1 - \beta^2) \|u\|^2 \|v\|^2$, which is what line L11 tests together with $u \cdot v < 0$. $\square$

**Lemma 3 (BUILD is correct).** After BUILD, $adj$ holds, at both ends, exactly the pairs $\{i, j\}$ whose region $R_\beta(p_i, p_j)$ contains no other point of $P$.

*Proof.* Lines L1 to L6 visit each unordered pair once. Line L5 clears $empty$ exactly when line L4 finds a third point in the region (Lemmas 1 and 2), and $empty$ is never set again, so leaving the loop early is safe. Line L6 adds the pair exactly when no such point exists. Lines L12 and L13 only read $adj$. $\square$

**Termination.** Each of the $\binom{n}{2}$ pairs makes at most $n - 2$ region tests, each a constant number of exact operations.

**Lemma 4 (monotonicity).** If $0 < \beta \le \beta'$, then $R_\beta(p, q) \subseteq R_{\beta'}(p, q)$, so the $\beta'$-skeleton is a subgraph of the $\beta$-skeleton.

*Proof.* For $\beta < 1$ the coefficient $\sqrt{1 - \beta^2}/\beta$ in Lemma 2 decreases as $\beta$ grows, so the condition gets weaker and the region grows. At $\beta = 1$ the condition of Lemma 2 would read $u \cdot v < 0$, the open disk with diameter $pq$, and the region of Lemma 1 for $\beta = 1$ is the same disk, since $c_1 = c_2 = m$ and the radius is $L/2$. So every region for $\beta < 1$ lies in this disk. For $\beta \ge 1$, take $r \in R_\beta$. The point $r$ is not $p$, since $\|p - c_1\| = \beta L / 2$ is not less than the radius, so $\|r - p\|^2 > 0$ and the first condition of Lemma 1 forces $(r - p) \cdot w > 0$; then $\beta (r - p) \cdot w \le \beta' (r - p) \cdot w$, and the first condition holds for $\beta'$. The second condition is symmetric. An empty larger region implies an empty smaller one, which gives the statement about graphs. $\square$

**Special values.** For $\beta = 1$ the closed region is the closed disk with diameter $pq$, so the closed 1-skeleton is the [Gabriel graph](/gabriel-graph/). For $\beta = 2$, $c_1 = q$, $c_2 = p$ and the radius is $L$, so the open region is the open lune, and the open 2-skeleton is the [relative neighborhood graph](/relative-neighborhood-graph/).

**Conclusion.** By Lemmas 1 to 3, BUILD stores exactly the $\beta$-skeleton, and it terminates. By Lemma 4 and the special values, the open $\beta$-skeletons for $1 \le \beta \le 2$ lie between the relative neighborhood graph and the open 1-skeleton, which contains the Gabriel graph. $\blacksquare$
