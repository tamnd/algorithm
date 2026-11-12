---
title: Correctness of ray-plane intersection
proves: [correctness]
status: full
---

**Claim.** RAY-PLANE returns $t$ if and only if $t_{\min} < t < t_{\max}$, $n \cdot (o + t\,d) = h$ and $n \cdot d \ne 0$; it returns MISS when $n \cdot d = 0$ or when the solution is outside the interval.

**Proof.** The dot product is linear in each argument, so for every real $t$

$$n \cdot (o + t\,d) = n \cdot o + t\,(n \cdot d).$$

Hence the ray point with parameter $t$ lies on the plane if and only if

$$n \cdot o + t\,\mathrm{den} = h, \qquad \mathrm{den} = n \cdot d. \tag{1}$$

*Case $\mathrm{den} = 0$.* Equation (1) reads $n \cdot o = h$, which does not depend on $t$. Either it is false, and no point of the ray is on the plane, or it is true, and the whole ray lies in the plane. The problem defines both cases as MISS, and line L2 returns MISS.

*Case $\mathrm{den} \ne 0$.* Equation (1) is a linear equation in $t$ with a nonzero coefficient, so it has exactly one solution, $t^* = (h - n \cdot o) / \mathrm{den}$, which is the value of line L3. Every other $t$ gives a point off the plane. If $t^*$ lies in $(t_{\min}, t_{\max})$, line L4 does not return and line L5 returns $t^*$, which is a valid answer. If it does not, no valid answer exists, because $t^*$ is the only candidate, and line L4 returns MISS.

**The point-normal form.** If $h = n \cdot p_0$, then $h - n \cdot o = n \cdot p_0 - n \cdot o = n \cdot (p_0 - o)$ by linearity, so the two forms of line L3 give the same $t^*$ in exact arithmetic.

**Back-face culling.** With culling, line L2 also returns MISS for $\mathrm{den} > 0$; the claim then holds for the rays with $\mathrm{den} < 0$, by the same argument. $\blacksquare$
