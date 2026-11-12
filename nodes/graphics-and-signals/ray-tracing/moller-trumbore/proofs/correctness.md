---
title: Correctness of the Möller-Trumbore test
proves: [correctness]
status: full
---

**Claim.** In exact arithmetic, MOLLER-TRUMBORE returns $(t, u, v)$ if and only if $o + t\,d = (1 - u - v)\,v_0 + u\,v_1 + v\,v_2$ with $u \ge 0$, $v \ge 0$, $u + v \le 1$ and $t_{\min} < t < t_{\max}$, for a triangle with non-collinear vertices and a ray that is not parallel to its plane. It returns MISS otherwise.

**The linear system.** With $e_1 = v_1 - v_0$, $e_2 = v_2 - v_0$ and $s = o - v_0$, the equation of the claim is equivalent to

$$-t\,d + u\,e_1 + v\,e_2 = s,$$

a $3 \times 3$ linear system $M x = s$ with the columns $M = [-d, e_1, e_2]$ and the unknown $x = (t, u, v)$.

**Determinants as triple products.** For three vectors, $\det[a, b, c] = a \cdot (b \times c)$, and the scalar triple product is invariant under cyclic shifts and changes sign under a swap. Then

- $\det M = \det[-d, e_1, e_2] = -d \cdot (e_1 \times e_2) = e_1 \cdot (e_2 \times (-d)) = e_1 \cdot (d \times e_2) = e_1 \cdot p$, which is line L3;
- $\det[-d, s, e_2] = s \cdot (d \times e_2) = s \cdot p$ by the same steps with $s$ in place of $e_1$;
- $\det[-d, e_1, s] = -d \cdot (e_1 \times s) = d \cdot (s \times e_1) = d \cdot q$;
- $\det[s, e_1, e_2] = s \cdot (e_1 \times e_2) = e_2 \cdot (s \times e_1) = e_2 \cdot q$.

**The singular case.** $\det M = 0$ if and only if the columns are linearly dependent. If $e_1$ and $e_2$ are independent, this happens exactly when $d$ lies in their span, that is when the ray is parallel to the plane of the triangle. If $e_1$ and $e_2$ are dependent, the vertices are collinear. In both cases the problem defines the answer as MISS, and line L4 returns MISS.

**The regular case.** If $\det M \ne 0$, the system has exactly one solution, and by Cramer's rule it is

$$t = \frac{\det[s, e_1, e_2]}{\det M}, \qquad u = \frac{\det[-d, s, e_2]}{\det M}, \qquad v = \frac{\det[-d, e_1, s]}{\det M}.$$

By the identities above, lines L7, L9 and L10 compute exactly these values. Since the solution is unique, a valid triple exists if and only if this solution meets the constraints.

**The early returns.** Line L7 returns MISS if $u < 0$, which breaks $u \ge 0$, or if $u > 1$. In the second case either $v < 0$ or $u + v > 1$, so a constraint is broken. Line L9 returns MISS if $v < 0$ or $u + v > 1$. Line L10 returns MISS if $t$ is outside $(t_{\min}, t_{\max})$. So every MISS of lines L7 to L10 is correct. If none of them returns, then $0 \le u \le 1$, $v \ge 0$, $u + v \le 1$ and $t_{\min} < t < t_{\max}$, and line L11 returns the solution, which meets all constraints.

Together, the algorithm returns the unique solution when it is valid and MISS otherwise. $\blacksquare$
