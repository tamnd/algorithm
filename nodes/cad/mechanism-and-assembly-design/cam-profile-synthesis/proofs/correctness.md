---
title: The computed points lie on the cam profile, and the follower touches the cam without cutting it
proves: [correctness]
status: full
---

We use the notation of the page. The cam turns counterclockwise by $\theta$ about the origin $O$. $R(\alpha)$ is the rotation by $\alpha$, and $J = R(\pi/2)$, so $J(a, b) = (-b, a)$. The program is a list of segments with laws $f_i$, angles $\beta_i > 0$ and lifts $L_i$, with $\sum \beta_i = 2\pi$ and $\sum L_i = 0$. We assume that each $f_i$ is $C^2$ on $[0, 1]$ and that $s$ and $s'$ are continuous across the segment ends, so $s$ is $C^1$ on the cycle and $s''$ is piecewise continuous. All derivatives below are with respect to $\theta$. At a segment end where $s''$ jumps, the statements about $s''$, $\alpha'$ and $\rho$ hold on each side.

**Lemma 1 (the program).** Line L5 returns $s(\theta)$, $s'(\theta)$ and $s''(\theta)$.

*Proof.* Line L1 sets $\theta_i = \sum_{j < i} \beta_j$ and $h_i = \sum_{j < i} L_j$, so segment $i$ covers $[\theta_i, \theta_{i+1})$ and starts at the height $h_i$. Line L4 finds the segment that holds $\theta$ and sets $x = (\theta - \theta_i)/\beta_i$, so $dx/d\theta = 1/\beta_i$. On that segment $s = h_i + L_i f_i(x)$, and the chain rule gives $s' = L_i f_i'(x)/\beta_i$ and $s'' = L_i f_i''(x)/\beta_i^2$. Since $\sum L_i = 0$ and $\sum \beta_i = 2\pi$, the end of the last segment has height $h_1 = 0$ at the angle $2\pi$, so $s$ is $2\pi$-periodic. $\square$

**Lemma 2 (inversion).** In the frame of the cam, the roller center at the angle $\theta$ is $C(\theta) = R(-\theta)(\varepsilon, u)$ with $u = d_0 + s$, which is line L7. Its derivative is $C' = R(-\theta)(u, w)$ with $w = s' - \varepsilon$.

*Proof.* In the fixed frame the follower slides on the line $x = \varepsilon$, and at $s = 0$ the roller center is on the prime circle of radius $R_p = R_b + R_f$, so it is at $(\varepsilon, d_0)$ with $\varepsilon^2 + d_0^2 = R_p^2$. That is line L2. At lift $s$ it is at $p(\theta) = (\varepsilon, d_0 + s)$. A point with cam coordinates $c$ is at $R(\theta) c$ in the fixed frame, so the fixed point $p$ has the cam coordinates $R(-\theta) p$. Since $\frac{d}{d\theta} R(-\theta) = -R(-\theta) J$,
$$C' = R(-\theta)\bigl(-J(\varepsilon, u) + (0, s')\bigr) = R(-\theta)\bigl((u, -\varepsilon) + (0, s')\bigr) = R(-\theta)(u, w). \qquad \square$$

Put $D = \sqrt{u^2 + w^2} = |C'|$, the unit tangent $T = R(-\theta)(u, w)/D$ and the unit normal $n = JT = R(-\theta)(-w, u)/D$. We assume $u > 0$, which holds when $s > -d_0$, for example when $s \ge 0$. Then $D > 0$ and the pitch curve is regular.

**Lemma 3 (the turning of the tangent).** The angle of $T$ is $\alpha(\theta) = \varphi(\theta) - \theta$, where $\varphi = \operatorname{atan2}(w, u)$ is the value of line L9, and the signed curvature of the pitch curve is $\kappa = \alpha'/D$. Line L10 computes $\rho = -1/\kappa = -D/\alpha'$.

*Proof.* The vector $(u, w)$ has the angle $\varphi$, and $R(-\theta)$ subtracts $\theta$. The curvature of a plane curve is the rate of turn of its tangent per unit length, and the length grows at the rate $D$, so $\kappa = \alpha'/D$. With $u' = s'$ and $w' = s''$,
$$\varphi' = \frac{u w' - w u'}{D^2} = \frac{u s'' - w s'}{D^2}, \qquad \alpha' = \varphi' - 1 = -\frac{u^2 + w(w + s') - u s''}{D^2},$$
so $-D/\alpha' = D^3/(u^2 + w(w + s') - u s'')$, which is line L10. $\square$

As $\theta$ grows the pitch curve runs clockwise about $O$, so a convex arc has $\alpha' < 0$ and $\rho > 0$, and $\rho$ is then the ordinary radius of curvature. On a circle of radius $R_p$ about $O$ (a dwell with $\varepsilon = 0$) we get $\rho = R_p$. Since $\varphi$ is periodic, $\alpha$ changes by exactly $-2\pi$ over one cycle. The normal $n = JT$ is to the left of the direction of travel, which is the outer side of a clockwise convex arc.

**Lemma 4 (the contact point).** The roller circles $|p - C(\theta)| = R_f$ have the envelope $C \pm R_f n$. Line L8 computes $K = C - R_f n$, the branch on the side of the cam, and $K' = (D + R_f\alpha')T = D(1 - R_f/\rho)\,T$.

*Proof.* Write the family as $F(p, \theta) = |p - C(\theta)|^2 - R_f^2 = 0$. A point of the envelope also satisfies $\partial F/\partial\theta = -2(p - C)\cdot C' = 0$, so $p - C$ is a multiple of $n$ of length $R_f$. In the fixed frame, $-R_f n$ is $R_f(w, -u)/D$, so $K = R(-\theta)(\varepsilon + R_f w/D,\ u - R_f u/D)$, which is line L8. For the derivative, $n' = \alpha' J n = -\alpha' T$, so $K' = C' - R_f n' = DT + R_f \alpha' T$. With $\alpha' = -D/\rho$ this is $D(1 - R_f/\rho)T$. $\square$

At $K$ the roller circle and the profile have the common normal $n$. The force between them, without friction, acts along $n$. In the fixed frame $n$ is $(-w, u)/D$ and the follower moves along $(0, 1)$, so the angle between the force and the motion has the tangent $w/u$. This is the pressure angle $\varphi$ of line L9.

**Theorem (no interference).** Assume $\rho(\theta) > R_f$ for every $\theta$. Then the profile $K$ is a closed convex curve with radius of curvature $\rho - R_f$. For every $\theta_0$, every point $q$ of the region $\Omega$ bounded by $K$ satisfies $|q - C(\theta_0)| \ge R_f$, with equality at $q = K(\theta_0)$. So at each angle the roller touches the cam at $K(\theta_0)$ and does not cut into it.

*Proof.* By Lemma 4, $K'$ is a positive multiple of $T$, so $K$ has the same tangent angle $\alpha$ as the pitch curve, and its speed is $D(1 - R_f/\rho)$. Its radius of curvature is $-|K'|/\alpha' = \rho - R_f$. Fix $\theta_0$ and write $n_0 = n(\theta_0)$ and $\alpha_0 = \alpha(\theta_0)$. Let $g(\theta) = (K(\theta) - K(\theta_0))\cdot n_0$ on $[\theta_0, \theta_0 + 2\pi]$. Since $T(\theta) = (\cos\alpha, \sin\alpha)$ and $n_0 = (-\sin\alpha_0, \cos\alpha_0)$,
$$g'(\theta) = K'(\theta)\cdot n_0 = D\Bigl(1 - \frac{R_f}{\rho}\Bigr)\sin(\alpha(\theta) - \alpha_0).$$
The factor in front is positive. Since $\alpha' < 0$ and the total change is $-2\pi$, the difference $\alpha(\theta) - \alpha_0$ falls strictly from $0$ to $-2\pi$. It is in $(-\pi, 0)$ up to an angle $\theta_1$ and in $(-2\pi, -\pi)$ after it, so $g$ falls on $[\theta_0, \theta_1]$ and rises on $[\theta_1, \theta_0 + 2\pi]$. As $g(\theta_0) = 0$ and $g(\theta_0 + 2\pi) = 0$ by periodicity, $g \le 0$ everywhere. So the whole curve $K$ lies in the closed half-plane $H_0 = \{q : (q - K(\theta_0))\cdot n_0 \le 0\}$. A closed curve whose tangent turns once in one direction is a simple convex curve, so $\Omega$ is well defined. It lies in the convex hull of $K$, and so in $H_0$. For $q \in H_0$, since $C(\theta_0) - K(\theta_0) = R_f n_0$,
$$|q - C(\theta_0)| \ge (C(\theta_0) - q)\cdot n_0 = R_f + (K(\theta_0) - q)\cdot n_0 \ge R_f,$$
with equality at $q = K(\theta_0)$. $\blacksquare$

**Proposition (the undercut flag).** If $0 < \rho(\theta_0) < R_f$ and $s''$ is continuous at $\theta_0$, then the roller at angles close to $\theta_0$ covers the point $K(\theta_0)$. So the cam cannot have $K(\theta_0)$ on its boundary, and the follower does not follow the program near $\theta_0$. This is the case that line L11 marks.

*Proof.* Let $f(\theta) = |K(\theta_0) - C(\theta)|^2$. Then $f(\theta_0) = R_f^2$ and $f'(\theta) = -2(K(\theta_0) - C(\theta))\cdot C'(\theta)$, which is $0$ at $\theta_0$ because $K(\theta_0) - C(\theta_0) = -R_f n_0$ is normal to $C'$. Next, $C'' = D'T + D\alpha' n$, so
$$f''(\theta_0) = 2|C'|^2 - 2(K(\theta_0) - C(\theta_0))\cdot C'' = 2D^2 + 2R_f D\alpha' = 2D^2\Bigl(1 - \frac{R_f}{\rho}\Bigr) < 0.$$
So $f$ has a strict local maximum $R_f^2$ at $\theta_0$, and $|K(\theta_0) - C(\theta)| < R_f$ for $\theta \ne \theta_0$ close to $\theta_0$. $\square$

**Theorem (flat-faced follower).** Let $e(\theta) = R(-\theta)(0, 1)$ and $h = R_b + s$. In the frame of the cam the face is the line $q\cdot e = h$. Line L14 computes $Q = h e + s' e'$, the envelope of these lines, and line L15 computes its radius of curvature $\rho = R_b + s + s''$. If $\rho > 0$ for every $\theta$, then the whole profile lies in the half-plane $q\cdot e(\theta_0) \le h(\theta_0)$ for every $\theta_0$, and touches the face at $Q(\theta_0)$, at the distance $s'(\theta_0)$ from the follower axis.

*Proof.* In the fixed frame the face is the line $y = R_b + s$. A cam point $q$ is at $R(\theta) q$ in the fixed frame, and its height is $R(\theta) q \cdot (0, 1) = q \cdot e$. This gives the line. Here $e' = R(-\theta)(1, 0)$ and $e'' = -e$. The envelope of the lines $q\cdot e = h$ satisfies also $q\cdot e' = h'$, and since $e$ and $e'$ are orthonormal, $q = he + h'e' = R(-\theta)(s', R_b + s)$, which is line L14. The fixed-frame point $(s', R_b + s)$ is on the face at the distance $s'$ from the axis. Then $Q' = h'e + he' + h''e' + h'e'' = (h + h'')e' = \rho e'$, and the tangent $e'$ turns at the unit rate, so $\rho$ is the radius of curvature. For the half-plane, let $g(\theta) = (Q(\theta) - Q(\theta_0))\cdot e(\theta_0)$. Then
$$g'(\theta) = \rho(\theta)\, e'(\theta)\cdot e(\theta_0) = -\rho(\theta)\sin(\theta - \theta_0),$$
which is negative on $(\theta_0, \theta_0 + \pi)$ and positive on $(\theta_0 + \pi, \theta_0 + 2\pi)$. As $g(\theta_0) = g(\theta_0 + 2\pi) = 0$, $g \le 0$, so $Q(\theta)\cdot e(\theta_0) \le Q(\theta_0)\cdot e(\theta_0) = h(\theta_0)$. $\blacksquare$

**The algorithm.** Lines L3 to L11 apply Lemmas 1 to 4 at each angle $2\pi k/N$, and lines L12 to L16 apply the last theorem. So every output point is a point of the true profile, with no error from the sampling at the sample angles. When the check of line L11 finds no sample with $0 < \rho \le R_f$ and every $\rho$ is positive, the conditions of the no-interference theorem hold at the samples. Between samples, the check is only as fine as the step $2\pi/N$.
