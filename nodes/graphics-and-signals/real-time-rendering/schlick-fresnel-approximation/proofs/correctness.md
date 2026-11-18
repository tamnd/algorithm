---
title: Properties of Schlick's Fresnel approximation
proves: [correctness]
status: full
---

**Setting.** Lines L1 to L3 compute $S(c) = F_0 + (F_{90} - F_0)(1 - c)^5$ for $c$ clamped to $[0, 1]$. Lines L4 to L9 compute $F_0 = ((\eta - 1) / (\eta + 1))^2$ and, for $\eta < 1$, replace $c$ by the transmitted cosine or return 1. The reference is the exact unpolarized reflectance of a smooth dielectric interface, $R = (r_s^2 + r_p^2) / 2$ with $r_s = (c_i - \eta c_t) / (c_i + \eta c_t)$ and $r_p = (\eta c_i - c_t) / (\eta c_i + c_t)$, where $c_t = \sqrt{1 - (1 - c_i^2) / \eta^2}$. The claims are about these formulas in exact arithmetic. The size of the error between the two in the middle of the range is a measurement, made on a grid by the tests.

**Claim 1 (end points).** $S(1) = F_0$ and $S(0) = F_{90}$. For $F_{90} = 1$ and $\eta > 1$, these equal the exact values $R(1) = F_0$ and $R(0) = 1$.

*Proof.* At $c = 1$, $(1 - c)^5 = 0$; at $c = 0$ it is 1. For the exact formula at $c_i = 1$, $c_t = 1$, so $r_s = (1 - \eta) / (1 + \eta)$ and $r_p = (\eta - 1) / (\eta + 1)$, and $R = ((\eta - 1) / (\eta + 1))^2 = F_0$. At $c_i = 0$, $r_s = -1$ and $r_p = -1$, so $R = 1$. $\square$

**Claim 2 (monotone and bounded).** If $F_0 \le F_{90}$, $S$ is decreasing in $c$ on $[0, 1]$ and $F_0 \le S(c) \le F_{90}$.

*Proof.* $(1 - c)^5$ decreases from 1 to 0 on $[0, 1]$, and $F_{90} - F_0 \ge 0$. So $S$ is a convex combination of $F_0$ and $F_{90}$ with a weight that decreases in $c$. $\square$

**Claim 3 (the symmetry used by lines L5 to L8).** Let $\eta > 1$, let $\theta_i \in [0, \pi / 2]$ and let $\theta_t$ be given by $\sin\theta_i = \eta \sin\theta_t$. Then $R(\cos\theta_i, \eta) = R(\cos\theta_t, 1 / \eta)$.

*Proof.* From inside, the incident cosine is $\cos\theta_t$ and the index ratio is $1 / \eta$; the transmitted cosine is then $\cos\theta_i$, by Snell's law. So the inside amplitudes are $r_s' = (\cos\theta_t - \cos\theta_i / \eta) / (\cos\theta_t + \cos\theta_i / \eta) = -(\cos\theta_i - \eta \cos\theta_t) / (\cos\theta_i + \eta \cos\theta_t) = -r_s$, after multiplying the numerator and the denominator by $\eta$, and in the same way $r_p' = -r_p$. Squares do not see the sign. $\square$

**Claim 4 (lines L5 to L8 are correct).** For $\eta < 1$ and $c$ the incident cosine inside, line L7 returns 1 exactly when the exact reflectance is 1 (total internal reflection), and otherwise line L9 returns $S(c_t)$ with $F_0 = ((1 / \eta - 1) / (1 / \eta + 1))^2$, which is the outside approximation at the outside angle. So the inside error equals the outside error at the matching angle.

*Proof.* $((\eta - 1) / (\eta + 1))^2 = ((1 - \eta) / (1 + \eta))^2 = ((1 / \eta - 1) / (1 / \eta + 1))^2$, by dividing by $\eta$. The value $s = (1 - c^2) / \eta^2$ is $\sin^2$ of the transmitted angle, and it is at least 1 exactly when there is no transmitted ray, where the exact $R$ is 1. Otherwise $\sqrt{1 - s}$ is the cosine of the outside angle, and Claim 3 says that the exact inside value is the exact outside value at that angle. $\square$

**Claim 5 (the cosine-weighted average).** $2 \int_0^1 S(c)\, c\, dc = F_0 + (F_{90} - F_0) / 21$.

*Proof.* $2 \int_0^1 c\, dc = 1$, and $2 \int_0^1 (1 - c)^5 c\, dc = 2 B(2, 6) = 2 \cdot 1!\, 5! / 7! = 1 / 21$. $\square$

**Conductors.** The test also compares $S$ with the exact reflectance for a complex index $n + ik$. Claim 1 holds there for $F_0 = ((n - 1)^2 + k^2) / ((n + 1)^2 + k^2)$, but Claim 2 does not hold for the exact curve, which falls below $F_0$ before it rises. The size of that dip and of the error is a measurement on a grid.

**What the tests check.** Claims 1 and 2 at random inputs, Claim 3 at 500 random angles and indices, Claim 4 by comparing the largest inside and outside errors, and the page values against the exact formulas.
