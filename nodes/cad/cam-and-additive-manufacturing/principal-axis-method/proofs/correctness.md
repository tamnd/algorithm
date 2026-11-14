---
title: On a concave cylinder, the PAM tilt is the smallest tilt without a gouge, it gives the least clearance at every point of the cutting edge, and its effective profile has the curvature of the surface
proves: [correctness]
status: full
---

**Model.** The part is a concave circular trough of radius $\rho$. In coordinates $(x, y, z)$ its axis is the line $L = \{y = 0, z = \rho\}$ and its bottom line is $\{y = 0, z = 0\}$. A point $X$ of the tool is in the material (a gouge) when $\mathrm{dist}(X, L) > \rho$. The contact point is $p = 0$, the normal is $n = (0, 0, 1)$, the minimum curvature direction is $e_{\min} = (1, 0, 0)$ (curvature 0), and the maximum curvature is $\kappa_{\max} = 1/\rho$ in the direction $(0, 1, 0)$. The tool feeds along $x$ with a fixed axis.

The tool is a toroidal end mill. Its center circle $C$ has radius $R > 0$ and lies at height $r \ge 0$ above the tip plane, and the corner radius is $r$. With $r = 0$ it is a flat end mill. The solid tool is the set of points at axial height $h \ge 0$ above the tip with a distance from the tool axis of at most $R + \sqrt{r^2 - (r - h)^2}$ for $h \le r$, and at most $R + r$ for $h \ge r$. Only the part of the tool at or below the height $\rho$ of the trough axis counts, as a trough is open above. Write $\rho' = \rho - r$ and assume $2R + 2r < \rho$, so the corner of the tool is below the height of the trough axis.

For a tilt $\lambda \in (0, \pi/2]$, write $s = \sin\lambda$, $c = \cos\lambda$, and place the tool by lines L6 to L8: axis $a = c\,n + s\,e_{\min} = (s, 0, c)$, direction $e = c\,e_{\min} - s\,n = (c, 0, -s)$, tip center $t_0 = p + r n - r a - R e$.

**Claim.** Let $\lambda^* = \arcsin(R/\rho')$, which exists when $R \le \rho'$.

(a) The tool at tilt $\lambda$ makes no gouge if and only if $\sin\lambda \ge R/\rho'$.

(b) At each point of the center circle, given by its angle $t$ from $e$, the clearance $\rho' - \mathrm{dist}(q(t), L)$ grows with $\lambda$. So $\lambda^*$ is the smallest tilt without a gouge, and of all tilts without a gouge it puts every point of the cutting edge nearest to the surface. With a lower bound $\lambda_{\min}$, the best tilt is $\max(\lambda^*, \lambda_{\min})$, which line L5 returns.

(c) At $\lambda^*$ the cross-section of the swept tool has the radius of curvature $\rho$ at the contact point, the same as the trough. The tool touches the trough along the line $\{y = 0, z = 0\}$ only, and the clearance near it is of fourth order in the distance from the contact.

If $R > \rho'$, every tilt makes a gouge, and line L4 reports it.

**Step 1: the gouge test reduces to the center circle.** The distance from $L$ does not depend on $x$, so the feed motion along $x$ does not change it. The function $X \mapsto \mathrm{dist}(X, L)$ is convex and 1-Lipschitz. For $q \in C$ and $|u| \le r$, $\mathrm{dist}(q + u, L) \le \mathrm{dist}(q, L) + r$, with equality when $u$ is $r$ times the unit vector from $L$ to $q$ at right angles to $L$. The ball $q + B_r$ is in the tool, since the solid torus $C \oplus B_r$ is the corner of the tool together with points inside it. The rest of the tool is the convex hull of the bottom circle (radius $R$, height 0) and of $C$, which are in $C \oplus B_r$, and the shank above height $r$. A shank point is $Y + h a$ with $Y$ on the disk of radius $R + r$ at height $r$ and $h \ge 0$. As $a$ points up, $\mathrm{dist}(Y + h a, L)$ decreases in $h$ while the point stays below the axis height. By convexity, the maximum of the distance over the convex hull and over that disk is on their boundary circles, which are in $C \oplus B_r$. So

$$\max_{X \in \text{tool}} \mathrm{dist}(X, L) = \max_{q \in C} \mathrm{dist}(q, L) + r,$$

and the tool makes no gouge if and only if $\mathrm{dist}(q, L) \le \rho'$ for every $q \in C$.

**Step 2: the center circle in coordinates.** The vector $w = a \times e = (0, 1, 0)$ completes the frame of the tool. The center circle is $q(t) = t_0 + r a + R(\cos t\, e + \sin t\, w)$, and $t_0 + r a + R e = p + r n = (0, 0, r)$. So

$$q(t) = (0, 0, r) + R(\cos t - 1)\, e + R \sin t\, w, \qquad q_y = R\sin t, \qquad q_z = r + R s (1 - \cos t).$$

Seen along $x$, the center circle is an ellipse with semi axes $R$ and $b = R s$, with its lowest point at height $r$ above $p$. Put $u = 1 - \cos t \in [0, 2]$, so $\sin^2 t = u(2 - u)$. Then

$$D(t)^2 = q_y^2 + (\rho - q_z)^2 = R^2 u (2 - u) + (\rho' - b u)^2,$$

$$D(t)^2 - \rho'^2 = u\,\big[\,2(R^2 - \rho' b) - u (R^2 - b^2)\,\big]. \qquad (*)$$

**Proof of (a).** Note $R^2 - b^2 = R^2 (1 - s^2) \ge 0$ and $u \ge 0$. If $\rho' b \ge R^2$, both terms in the bracket of $(*)$ are at most 0, so $D(t) \le \rho'$ for every $t$ and there is no gouge by Step 1. If $\rho' b < R^2$, then for $0 < u < 2(R^2 - \rho' b)/(R^2 - b^2)$, or for every $u \in (0, 2]$ when $b = R$, the bracket is positive and $D(t) > \rho'$, which is a gouge. The condition $\rho' b \ge R^2$ is $\rho' R s \ge R^2$, that is $s \ge R/\rho'$. If $R > \rho'$ this needs $s > 1$, so no tilt works.

**Proof of (b).** Fix $t$, so $u$ is fixed. As $\lambda$ grows in $(0, \pi/2]$, $b = R\sin\lambda$ grows, and
$$\frac{\partial}{\partial b} D(t)^2 = -2u(\rho' - b u) \le 0,$$
since $b u \le 2R < \rho'$. So $D(t)$ does not grow, and the clearance $\rho' - D(t)$ does not shrink, as $\lambda$ grows. By (a), the tilts without a gouge are exactly $\lambda \ge \lambda^*$, so the smallest of them, $\lambda^*$, gives the least clearance at every $t$. With the bound $\lambda \ge \lambda_{\min}$, the feasible set is $\lambda \ge \max(\lambda^*, \lambda_{\min})$, and the same argument picks its smallest element.

**Proof of (c).** The swept cross-section is the projection of the tool along $x$. By Step 1, near the contact its lower boundary is the lower arc of the ellipse grown by a disk of radius $r$, that is, the offset of the ellipse at distance $r$. An ellipse with semi axes $R \ge b$ has the radius of curvature $R^2/b$ at the ends of its short axis, and the offset at distance $r$ outward adds $r$ to the radius of curvature. So the cut profile has radius $R^2/b + r = R/s + r$ at the contact. At $s = R/\rho'$ this is $\rho' + r = \rho$. At $s = R/\rho'$, $(*)$ becomes $D(t)^2 - \rho'^2 = -u^2(R^2 - b^2)$, which is 0 only at $u = 0$ when $s < 1$, so the tool touches along $t = 0$ only. As $u = t^2/2 + O(t^4)$, the clearance is $\rho' - D(t) = u^2(R^2 - b^2)/(2\rho') + O(u^3) = t^4 (R^2 - b^2)/(8\rho') + O(t^6)$, which is of fourth order. For $s > R/\rho'$ the first term of $(*)$ is $2u(R^2 - \rho' b) < 0$, and the clearance is of second order in $t$. $\blacksquare$

**Remarks.** (1) The claims hold for the trough, where the feed direction has zero curvature and the axis of the tool is fixed along the feed. On a general surface, PAM uses the same formula with $\rho = 1/\kappa_{\max}$ at each contact point. This matches the second-order shape of the surface in the plane of maximum curvature, but it does not prove the absence of a gouge away from the contact point, and a global gouge check is still needed. (2) The tests check (a) and (b) by a grid search over tilts with a direct 3D test of the tool in the trough, and they check (a) and the single touch point of (c) with exact rational arithmetic at the tilt $\sin\lambda = 7/25$.
