---
title: Correctness of primary ray generation
proves: [correctness]
status: full
---

Let the camera be as on the page: an eye $e$, an orthonormal basis $(u, v, w)$, an image of $W \times H$ pixels, the vertical field of view $\theta$ and $\tau = \tan(\theta / 2)$.

**The image plane.** The image plane is the plane at distance 1 in front of the eye, the set of points $e + x\,u + y\,v - w$. The image covers $y \in [-\tau, \tau]$, which is the vertical field of view $\theta$ because $\tan(\theta / 2) = \tau / 1$, and $x \in [-\tfrac{W}{H}\tau, \tfrac{W}{H}\tau]$. The pixel coordinates $(\xi, \eta) \in [0, W] \times [0, H]$, with $\eta = 0$ at the top, map to the image plane by the affine map

$$x = \frac{2 \xi - W}{H}\,\tau, \qquad y = \frac{H - 2 \eta}{H}\,\tau.$$

It maps $\xi = 0$ and $\xi = W$ to $\mp \tfrac{W}{H}\tau$, and $\eta = 0$ and $\eta = H$ to $\pm \tau$. A step of one pixel changes $x$ and $y$ by the same amount $2\tau / H$, so pixels are square. The sample $(s_x, s_y)$ of pixel $(i, j)$ is the point $(\xi, \eta) = (i + s_x, j + s_y)$, and lines L1 and L2 compute exactly its image coordinates.

**Claim 1: the pinhole ray passes through the sample.** By line L3, $d = x\,u + y\,v - w$, so the ray point at $t = 1$ is $e + d = e + x\,u + y\,v - w$, the image point of the sample. Its origin is the eye, which is the center of projection of the pinhole model. So line L4 returns the ray from the center through the sample point, as required.

**Claim 2: the thin-lens ray starts on the lens and passes through the point in focus.** By lines L5 and L6, $o = e + R p_x\,u + R p_y\,v$. Since $u$ and $v$ are orthonormal and $p_x^2 + p_y^2 \le 1$, the point $o$ lies in the plane through $e$ spanned by $u$ and $v$, at distance $R \sqrt{p_x^2 + p_y^2} \le R$ from $e$: on the lens disk. By line L8 the direction is $p_f - o$, so the ray point at $t = 1$ is $p_f$. By line L7, $p_f = e + z_f\,d$; its component along $-w$ is $z_f\,(-w \cdot d) = z_f$, since $-w \cdot d = 1$ by the orthonormality of the basis. So $p_f$ is the point of the pinhole ray at the depth $z_f$, which is the plane of focus.

**Claim 3: the lens rays of a sample focus at $p_f$ and only there.** Every lens point gives a ray through the same $p_f$, by claim 2. Two lens rays with different origins $o_1 \ne o_2$ and the common point $p_f$ meet only at $p_f$, because two distinct lines meet at most once. So the rays of one sample meet at $p_f$ and nowhere else, and a scene point at a depth other than $z_f$ is reached by rays of several samples, which is the blur.

**Claim 4: the pinhole is the limit of the lens.** With $R = 0$, line L4 returns $(e, d)$. If lines L5 to L8 were run anyway, they would give $o = e$ and the direction $p_f - e = z_f\,d$, which is the same ray with a direction scaled by $z_f > 0$. So the two forms agree.

Together, PRIMARY-RAY returns the ray that the camera model defines for the sample. $\blacksquare$
