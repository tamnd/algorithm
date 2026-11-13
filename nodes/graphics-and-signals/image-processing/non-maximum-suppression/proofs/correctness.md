---
title: Non-maximum suppression keeps the maxima along the rounded gradient direction, one per run
proves: [correctness]
status: full
---

Let $m(p) = g_x(p)^2 + g_y(p)^2$, as line L1 computes. Line L2 visits each interior pixel, so the reads $p \pm d$ of line L5 are inside the image for each of the four steps $d_k$. Line L3 skips $m(p) = 0$, where the gradient has no direction. We prove four facts.

**Lemma 1 (the sector test is exact).** Let $(g_x, g_y) \ne (0, 0)$ have the angle $\varphi$, and let $\psi \in [0°, 90°]$ be the angle between the line through $(g_x, g_y)$ and the $x$ axis, so $\tan \psi = |g_y| / |g_x|$. Then $(|g_x| + |g_y|)^2 < 2 g_x^2$ holds exactly when $\psi < 22.5°$, and $(|g_x| + |g_y|)^2 < 2 g_y^2$ holds exactly when $\psi > 67.5°$.

*Proof.* Both sides of $(|g_x| + |g_y|)^2 < 2 g_x^2$ are squares of numbers that are not negative, so the test is the same as $|g_x| + |g_y| < \sqrt{2}\, |g_x|$, that is $|g_y| < (\sqrt{2} - 1) |g_x|$. The half angle formula gives $\tan 22.5° = \sin 45° / (1 + \cos 45°) = 1 / (\sqrt{2} + 1) = \sqrt{2} - 1$. Since $\tan$ increases on $[0°, 90°)$, the test holds exactly when $\psi < 22.5°$, also for $g_x = 0$, where both sides fail. The second test is the first with $x$ and $y$ exchanged, so it holds exactly when the angle to the $y$ axis is below $22.5°$, that is $\psi > 67.5°$. $\square$

So SECTOR returns 0 when the direction is within $22.5°$ of the $x$ axis and 2 when it is within $22.5°$ of the $y$ axis. Otherwise $22.5° \le \psi \le 67.5°$, so $g_x \ne 0$ and $g_y \ne 0$. If $g_x g_y > 0$, the vector points into the first or the third quadrant, and the nearest of the four directions is that of $(1, 1)$, sector 1. If $g_x g_y < 0$, the nearest is that of $(-1, 1)$, sector 3. So SECTOR is the nearest of the four directions modulo $180°$, except at $\psi = 22.5°$ and $\psi = 67.5°$, where two are equally near. For integers these angles never occur: $|g_y| = (\sqrt{2} - 1)|g_x|$ with $g_x \ne 0$ would make $\sqrt{2}$ rational. $\blacksquare$

**Lemma 2 (strict maxima stay).** If $m(p) > m(p - d)$ and $m(p) > m(p + d)$ for the step $d$ that line L4 picks, then $p$ stays.

*Proof.* Then $m(p) > 0$, so line L3 does not skip $p$, and both parts of the test of line L6 hold. $\square$

**Lemma 3 (no two neighbors of one sector both stay).** Let $p$ and $q = p + d_k$ be interior pixels that both have sector $k$. Then $p$ and $q$ do not both stay.

*Proof.* Suppose both stay. Pixel $p$ has the step $d_k$, and its test reads $m(p + d_k) = m(q)$ as the value in front, so $m(p) \ge m(q)$. Pixel $q$ has the same step, and its test reads $m(q - d_k) = m(p)$ as the value behind, so $m(q) > m(p)$. The two inequalities contradict each other. $\square$

Lemma 3 is the single response property along the gradient: on a line of pixels in the direction $d_k$ that all have sector $k$, the pixels that stay are pairwise not adjacent on that line. It says nothing about two pixels that are adjacent in another direction, which is why a 45 degree edge can stay two pixels wide.

**Lemma 4 (a plateau keeps its first pixel).** Let $p_i = p_0 + i\, d_k$ for $i = 0, \ldots, r$ be interior pixels, all of sector $k$, with $m(p_0) = m(p_1) = \cdots = m(p_r) = M > 0$, $m(p_0 - d_k) < M$ and $m(p_r + d_k) \le M$. Then $p_0$ stays and $p_1, \ldots, p_r$ do not.

*Proof.* For $p_0$, the value behind is $m(p_0 - d_k) < M$ and the value in front is $m(p_1) = M$ if $r \ge 1$, or $m(p_0 + d_k) \le M$ if $r = 0$. So both parts of line L6 hold. For $i \ge 1$, the value behind is $m(p_{i-1}) = M$, which is not less than $m(p_i)$, so the strict part of line L6 fails. $\square$

**Theorem.** The output of NON-MAXIMUM-SUPPRESSION holds $m(p)$ exactly at the interior pixels $p$ with $m(p) > 0$, $m(p) > m(p - d)$ and $m(p) \ge m(p + d)$, where $d$ is the step of the nearest of the four directions to the gradient at $p$, and 0 at each other pixel. These pixels include every strict maximum along its direction, include exactly one pixel of each maximal plateau along a direction, and never include two neighbors along $d$ of the same sector.

*Proof.* The output starts as 0 and line L7 is the only write, at the pixels that pass lines L3 and L6, so the first sentence holds with $d$ from line L4. Lemma 1 shows that $d$ is the nearest direction. Lemmas 2, 4 and 3 give the three other claims. $\blacksquare$

All the operations are integer multiplications, additions and comparisons. With integer inputs the output is the same on every machine, and the implementation tests it against a reference that rounds $\operatorname{atan2}(g_y, g_x)$ to the nearest multiple of $45°$.
