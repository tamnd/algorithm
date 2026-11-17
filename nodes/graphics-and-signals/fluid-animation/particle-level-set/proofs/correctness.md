---
title: Seeded particles do not escape, the escape test, and what the correction changes
proves: [correctness]
status: full
---

We use the line numbers of the page. $\varphi$ is sampled at the nodes of a square grid of spacing $\Delta x$, and $\varphi(\mathbf x)$ off the nodes is the bilinear interpolation. A particle $p$ has a position $\mathbf x_p$, a sign $s_p \in \{+1, -1\}$ and a radius $r_p \in [r_{min}, r_{max}]$, with $r_{min} = 0.1 \Delta x$ and $r_{max} = 0.5 \Delta x$. The band is $[b_{min}, b_{max}]$ with $b_{min} = r_{min}$ and $b_{max} = 3 \Delta x$. The particle's own level set is $\varphi_p(\mathbf x) = s_p (r_p - |\mathbf x - \mathbf x_p|)$: it has the sign $s_p$ inside the circle of radius $r_p$ about $\mathbf x_p$, and the other sign outside it. A particle has escaped (line L2) when $s_p \varphi(\mathbf x_p) < 0$ and $|\varphi(\mathbf x_p)| > r_p$, that is, when $s_p \varphi(\mathbf x_p) < -r_p$.

**Lemma 1 (seeded particles have not escaped).** After seeding, no particle has escaped, so lines L2 to L4 change nothing. After line L7, a particle has escaped exactly when $s_p \varphi(\mathbf x_p) < -r_{min}$.

*Proof.* Seeding keeps a particle only if $b_{min} \le s_p \varphi(\mathbf x_p) \le b_{max}$, and sets $r_p = \min(\max(s_p \varphi(\mathbf x_p), r_{min}), r_{max})$. Line L7 uses the same formula. Let $a = s_p \varphi(\mathbf x_p)$. If $a \ge 0$, then $a > -r_p$, so $p$ has not escaped. If $a < 0$, which is possible only after line L7, then $r_p = r_{min}$, and the particle has escaped exactly when $a < -r_{min}$. After seeding, $a \ge b_{min} > 0$. With no escaped particle, $\varphi^+ = \varphi^- = \varphi$ in line L3, and line L4 gives $\varphi$ back. $\square$

So after line L7, a particle that was out by more than $r_{min}$ is still marked as escaped. Line L7 makes it as small as allowed, so that it repairs only a small region the next time. The test file checks that 400 seeded particles around Zalesak's disk are all in the band with $r_p \le s_p \varphi(\mathbf x_p)$, and that line L2 finds none of them.

**Lemma 2 (what the escape test means).** If $\varphi$ is the signed distance to the interface near $\mathbf x_p$, then $p$ has escaped exactly when the whole open disk of radius $r_p$ about $\mathbf x_p$ is on the side of sign $-s_p$.

*Proof.* For a signed distance, $|\varphi(\mathbf x_p)|$ is the distance from $\mathbf x_p$ to the interface. The disk misses the interface exactly when this distance is at least $r_p$, and then the whole disk has the sign of $\varphi(\mathbf x_p)$. So the disk lies on the side $-s_p$ with no point on the interface exactly when $s_p \varphi(\mathbf x_p) < 0$ and $|\varphi(\mathbf x_p)| > r_p$, up to the case of equality, which the strict test leaves out. $\square$

A particle that only touches the interface, or that is out by less than its radius, has not escaped. The paper chooses this test so that the small errors of a well resolved level set do not trigger a repair (its section 2.3.3). The test file checks a particle out by $0.2 \Delta x$ with radius $0.3 \Delta x$: it has not escaped.

**Theorem 1 (the correction is local and one-sided).** Lines L3 and L4 change $\varphi$ only at the four nodes around each escaped particle, that is, the corners of the grid cell that contains $\mathbf x_p$. At every node, the new value is $\varphi^+$ or $\varphi^-$, with $\varphi^- \le \varphi \le \varphi^+$. If only escaped particles of one sign $s$ reach a node, the new value there is either the old value or $\max_p \varphi_p$ (for $s = +1$) or $\min_p \varphi_p$ (for $s = -1$) over those particles, and in the second case it is closer to zero than the old value or equal in magnitude.

*Proof.* Line L3 sets $\varphi^+$ to the maximum of $\varphi$ and the values $\varphi_p$ of the positive escaped particles at the corners of their cells, and $\varphi^-$ to the minimum of $\varphi$ and the values of the negative ones. At any other node, $\varphi^+ = \varphi^- = \varphi$, so line L4 gives $\varphi$. Taking a maximum cannot lower a value, and taking a minimum cannot raise it, so $\varphi^- \le \varphi \le \varphi^+$. Let only positive particles reach a node. Then $\varphi^- = \varphi$, and $\varphi^+$ is either $\varphi$ or $\max_p \varphi_p > \varphi$. Line L4 takes $\varphi^+$ if $|\varphi^+| \le |\varphi|$, else $\varphi$. The negative case is the mirror image. $\square$

So positive particles can only push the interface toward the $\varphi < 0$ side, which gives more room to $\varphi > 0$, and negative particles do the opposite. A node changes sign only if a particle circle covers it more firmly than the old value says it is on the other side. Where escaped particles of both signs meet, line L4 keeps the value that is closer to the interface. The paper argues that this value is the more reliable one (its section 2.3.3).

**Theorem 2 (a single escaped particle).** Let $p$ be the only escaped particle, let it be negative, and let $\mathbf y$ be a corner of its cell, at the distance $d = |\mathbf y - \mathbf x_p|$. Then $\mathbf y$ changes from positive to negative exactly when $\varphi(\mathbf y) > 0$, $d < r_p$ and $r_p - d \le \varphi(\mathbf y)$, and its new value is then $\varphi_p(\mathbf y) = -(r_p - d)$. A corner with $\varphi(\mathbf y) \le 0$ does not change. A positive corner stays positive in all other cases.

*Proof.* Only $p$ reaches $\mathbf y$, and it is negative, so $\varphi^+ = \varphi$ and $\varphi^- = \min(\varphi, \varphi_p)$ at $\mathbf y$. There are four cases.

1. $\varphi(\mathbf y) \le 0$. Then $\varphi^- = \min(\varphi, \varphi_p) \le \varphi(\mathbf y) \le 0$ and $\varphi^+ = \varphi$. If $\varphi_p(\mathbf y) < \varphi(\mathbf y)$, then $|\varphi^-| > |\varphi^+|$ and line L4 takes $\varphi^+ = \varphi$. Otherwise $\varphi^- = \varphi$. Either way the value does not change.
2. $\varphi(\mathbf y) > 0$ and $\varphi_p(\mathbf y) \ge \varphi(\mathbf y)$. Then $\varphi^- = \varphi$ and nothing changes.
3. $\varphi(\mathbf y) > 0$ and $0 \le \varphi_p(\mathbf y) < \varphi(\mathbf y)$. Then $|\varphi^-| < |\varphi^+|$, and the new value is $\varphi_p(\mathbf y) \ge 0$. The node stays on the positive side, closer to zero.
4. $\varphi(\mathbf y) > 0$ and $\varphi_p(\mathbf y) < 0$, which means $d < r_p$. Then $\varphi^- = \varphi_p(\mathbf y)$, and the new value is $\varphi_p(\mathbf y) < 0$ if $r_p - d \le \varphi(\mathbf y)$, and $\varphi(\mathbf y) > 0$ otherwise.

So $\mathbf y$ becomes negative exactly in case 4 with $r_p - d \le \varphi(\mathbf y)$. $\square$

The test file uses $\varphi = y - 1/2$ on a $32 \times 32$ grid, a negative particle at $(1/2 + \Delta x / 2,\ 1/2 + 0.4 \Delta x)$ with $r_p = 0.3 \Delta x$. The node $(16, 16)$ at height $1/2 + 0.5 \Delta x$ is at distance $0.1 \Delta x$ from the particle, so case 4 applies: $\varphi_p = -0.2 \Delta x$ and $0.2 \Delta x \le 0.5 \Delta x$. The node becomes $-0.2 \Delta x$, and the liquid gains the region near the particle. The two corners below the surface are in case 1. The corner $(17, 16)$ is at distance $1.005 \Delta x$, so $\varphi_p = 0.705 \Delta x \ge 0.5 \Delta x = \varphi$, which is case 2. These three do not change, and the test checks that $(16, 16)$ is the only node that changes.

**Lemma 3 (the motion of the particles).** For a rigid rotation, the code moves each particle by the exact rotation, so after one full turn every particle is back at its start up to rounding.

*Proof.* `rotation` returns the map $\mathbf x \mapsto \mathbf c + R(\omega\, \Delta t)(\mathbf x - \mathbf c)$, which is the exact flow of the field $\mathbf u = \omega (-(y - c_y), x - c_x)$ over the time $\Delta t$. The composition of these maps over steps that add up to $2\pi / \omega$ is the rotation by $2\pi$, the identity. $\square$

The particles thus carry the shape without error in this test, while the level set is resampled on the grid each step and smooths the corners. Lines L2 to L4 repair $\varphi$ where the two disagree by more than a particle radius. This is why, in the test file, a turn of Zalesak's disk in 64 steps on a $32 \times 32$ grid keeps 92 percent of the area with particles and 47 percent without them. These are measurements, not consequences of the lemmas: the particles do not conserve area exactly, and they cannot restore detail where no particle remains.
