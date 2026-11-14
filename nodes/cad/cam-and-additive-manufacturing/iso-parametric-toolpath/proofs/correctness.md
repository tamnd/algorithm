---
title: On a bilinear patch, the iso-parametric passes chosen from the end gaps keep every surface point within half the path interval of the path
proves: [correctness, termination]
status: full
---

**Setting.** $S(u, v) = (1-u)(1-v)P_{00} + u(1-v)P_{10} + (1-u)vP_{01} + uvP_{11}$ on $[0, 1]^2$, with corners in $\mathbb{Q}^3$, and $w > 0$ is rational. Let $a = P_{01} - P_{00}$, $b = P_{11} - P_{10}$ and $B(u) = (1-u)a + ub$. Let $N$ be the value of line L2 and $v_j = j/N$. Pass $j$ is the segment from $S(0, v_j)$ to $S(1, v_j)$, and $\Gamma$ is the union of the passes and the links.

**Claim.** (a) Line L2 stops, and $N$ is the smallest positive integer with $|B(u)|/N \le w$ for all $u \in [0, 1]$. (b) Pass $j$ is the iso-parametric curve $\{S(u, v_j) : 0 \le u \le 1\}$, and the links lie on the patch. (c) Every point of the patch lies within distance $w/2$ of $\Gamma$, along a straight segment that lies on the patch.

**Step 1 (the patch is linear in each parameter).** Expanding the formula gives $S(u, v) = A(u) + vB(u)$ with $A(u) = (1-u)P_{00} + uP_{10}$, and in the same way $S(u, v) = A'(v) + u B'(v)$ with $A'(v) = (1-v)P_{00} + vP_{01}$ and $B'(v) = (1-v)(P_{10} - P_{00}) + v(P_{11} - P_{01})$. So for fixed $v$, $u \mapsto S(u, v)$ is the affine map from $S(0, v)$ to $S(1, v)$, and for fixed $u$, $v \mapsto S(u, v)$ is affine with derivative $B(u)$. This proves the first part of (b). The link from pass $j$ to pass $j + 1$ joins $S(e, v_j)$ to $S(e, v_{j+1})$ for $e \in \{0, 1\}$, and by the same fact it is the curve $v \mapsto S(e, v)$ on $[v_j, v_{j+1}]$, which lies on the patch.

**Step 2 (the largest gap is at an end).** The function $g(u) = |B(u)|^2$ is the square of the norm of an affine map, so it is convex: for $u = (1 - \lambda)u_0 + \lambda u_1$, $B(u) = (1 - \lambda)B(u_0) + \lambda B(u_1)$, and the convexity of $x \mapsto |x|^2$ gives $g(u) \le (1-\lambda) g(u_0) + \lambda g(u_1)$. With $u_0 = 0$ and $u_1 = 1$, $g(u) \le \max(g(0), g(1)) = M$, the value of line L1.

**Step 3 (proof of (a)).** The test of line L2 is $M > n^2 w^2$, and $n^2 w^2$ grows without bound as $n$ grows, so the loop stops at the smallest $n \ge 1$ with $M \le n^2 w^2$. By Step 2, $\max_u |B(u)|/n \le w$ holds if and only if $M \le n^2 w^2$. So $N$ is the smallest positive integer with that property.

**Step 4 (proof of (c)).** Let $(u, v) \in [0, 1]^2$ and choose $j$ with $v_j \le v \le v_{j+1}$. By Step 1 the points $S(u, v')$ for $v' \in [v_j, v_{j+1}]$ form a straight segment on the patch from $q_0 = S(u, v_j)$ to $q_1 = S(u, v_{j+1})$, of length $|B(u)|(v_{j+1} - v_j) = |B(u)|/N \le w$ by (a). The point $S(u, v)$ lies on this segment, so it is within $w/2$ of $q_0$ or of $q_1$, along the segment. By (b), $q_0$ lies on pass $j$ and $q_1$ lies on pass $j + 1$. $\blacksquare$

**Remark.** The bound of (c) holds for every $u$, but the gap $|B(u)|/N$ is $w$ only where $|B(u)|$ is largest. Where $|B(u)|$ is small, the passes are closer than needed, which is the unevenness of iso-parametric paths. On a curved surface the gap between two iso-curves is only $\Delta v\,|S_v|$ to first order, and this proof does not apply.
