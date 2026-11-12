---
title: Correctness of ray-sphere intersection
proves: [correctness]
status: full
---

**Claim.** In exact arithmetic, RAY-SPHERE returns the smallest $t \in (t_{\min}, t_{\max})$ with $|o + t\,d - c| = r$, or MISS if there is none.

**The quadratic.** Put $f = o - c$. For every real $t$,

$$|f + t\,d|^2 - r^2 = (d \cdot d)\,t^2 + 2\,(f \cdot d)\,t + (f \cdot f - r^2) = a t^2 + 2 b t + k,$$

so the hit parameters are exactly the real roots of $g(t) = a t^2 + 2 b t + k$, with $a = |d|^2 > 0$. Since $a > 0$, $g$ has real roots if and only if $\Delta = b^2 - a k \ge 0$, and then they are $(-b \pm \sqrt{\Delta}) / a$.

**Line L3 computes $\Delta$.** With $s = b / a$ and $l = f - s\,d$,

$$l \cdot l = f \cdot f - 2 s\,(f \cdot d) + s^2\,(d \cdot d) = f \cdot f - 2 \frac{b^2}{a} + \frac{b^2}{a} = f \cdot f - \frac{b^2}{a}.$$

Hence $a\,(r^2 - l \cdot l) = a r^2 - a\,f \cdot f + b^2 = b^2 - a\,(f \cdot f - r^2) = b^2 - a k = \Delta$. So line L4 returns MISS exactly when there is no real root, which is exactly when no point of the ray line is on the sphere.

**Lines L5 and L6 compute the roots.** Let $\sigma = \mathrm{sign}(b) \in \{1, -1\}$, with $\sigma = 1$ for $b = 0$, and $q = -(b + \sigma \sqrt{\Delta})$. Then $q / a = (-b - \sigma \sqrt{\Delta}) / a$ is one of the two roots, call it $t_1'$. The other root $t_0'$ satisfies $t_0' t_1' = k / a$ by Vieta's formula (the product of the roots of $a t^2 + 2 b t + k$). If $q \ne 0$, then $t_1' \ne 0$ and $t_0' = (k / a) / (q / a) = k / q$. So line L6 gives the two roots, and line L7 orders them, $t_0 \le t_1$.

If $q = 0$, then $b + \sigma \sqrt{\Delta} = 0$. Both terms have the sign $\sigma$ or are zero, so $b = 0$ and $\Delta = 0$, hence $a k = b^2 - \Delta = 0$ and $k = 0$. Then $g(t) = a t^2$ and the double root is 0, which is what the implementation returns in this case.

**Line L8.** The set of hit parameters on the line is $\{t_0, t_1\}$. Line L8 tests $t_0$ first and then $t_1$, and returns the first that lies in the interval. Since $t_0 \le t_1$, the value returned is the smallest hit parameter in the interval, and MISS is returned exactly when neither root is in it. $\blacksquare$

**Remark on stability.** In floating point, line L5 adds $b$ and $\sigma \sqrt{\mathrm{disc}}$, which have the same sign, so the relative error of $q$ is a few units of the rounding error plus the relative error of $\mathrm{disc}$. Line L3 computes $r^2 - l \cdot l$, a difference that is small only when the ray is close to tangent, where the problem itself is ill conditioned; it avoids the difference of the two large numbers $b^2$ and $a k$. The remaining source of error is $k$, as the page explains.
