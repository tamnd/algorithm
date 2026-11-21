---
title: Correctness of the Feldkamp-Davis-Kress algorithm
proves: [correctness]
status: full
---

We use the conventions of the page. $\omega(\beta) = (\cos\beta, \sin\beta, 0)$, $\omega^\perp(\beta) = (-\sin\beta, \cos\beta, 0)$ and $e_3 = (0, 0, 1)$. The source is $S(\beta) = D\,\omega^\perp(\beta)$, and the detector point $(t, z)$ is $P = t\,\omega(\beta) + z\,e_3$. The data is $g(\beta, t, z) = \int_0^\infty f(S + \lambda v)\,d\lambda$ with the unit vector $v = (P - S)/|P - S|$ and $|P - S| = \sqrt{D^2 + t^2 + z^2}$. The FDK formula is
$$f_{\mathrm{FDK}}(x) = \int_0^{2\pi} \frac{1}{U^2}\,q(\beta, t', z')\,d\beta, \qquad q(\beta, t, z) = \int \frac{h(t - u)}{2}\,\frac{D\,g(\beta, u, z)}{\sqrt{D^2 + u^2 + z^2}}\,du,$$
with $U = (D - x\cdot\omega^\perp)/D$, $t' = x\cdot\omega/U$ and $z' = x_3/U$, where $h$ is the ramp filter. The proof shows two exactness results, that the code computes the discrete form of them exactly, and why the formula is not exact in general. It relies on the 2D flat-detector fan-beam formula, which [fan-beam filtered back-projection](/fan-beam-filtered-back-projection/) proves:

**Fact (2D flat-detector fan-beam formula).** Let $f_0$ be smooth with support in the open disk of radius $r < D$, and let $g_0(\beta, t)$ be its integral along the line in the plane from $D\omega^\perp(\beta)$ through $t\,\omega(\beta)$. Then for $|x| < r$,
$$f_0(x) = \int_0^{2\pi} \frac{1}{U^2}\int \frac{h(t' - u)}{2}\,\frac{D\,g_0(\beta, u)}{\sqrt{D^2 + u^2}}\,du\,d\beta.$$

## Part 1. The geometry of the back-projection

**Lemma 1.** The point $x$ lies on the ray from $S(\beta)$ through the detector point $(t', z')$, and $D U$ is the depth of $x$ along the central ray, that is, $(x - S)\cdot(-\omega^\perp) = D U$.

*Proof.* $(x - S)\cdot(-\omega^\perp) = D - x\cdot\omega^\perp = D U$. The detector point is $P' - S = t'\omega + z' e_3 + D(-\omega^\perp)$, and $x - S = (x\cdot\omega)\,\omega + x_3 e_3 + D U(-\omega^\perp)$, because the three vectors $\omega$, $e_3$ and $-\omega^\perp$ are orthonormal. With $t' = x\cdot\omega/U$ and $z' = x_3/U$ we get $x - S = U(P' - S)$, so $x$ is on the ray. $\square$

The code computes $U$, $t'$ and $z'$ in this way (line L7), and the test checks Lemma 1 at random points.

## Part 2. The mid-plane

**Theorem 1.** Let $f$ be smooth with support in a ball of radius $r < D$. For $x = (x_1, x_2, 0)$ with $|x| < r$, $f_{\mathrm{FDK}}(x) = f(x)$.

*Proof.* For $x_3 = 0$, $z' = 0$, so the formula only reads $q(\beta, t', 0)$, which only uses the data row $z = 0$. The rays of this row lie in the plane $x_3 = 0$, so $g(\beta, u, 0) = g_0(\beta, u)$ for $f_0 = f(\cdot, \cdot, 0)$. The weight is $D/\sqrt{D^2 + u^2}$. So $f_{\mathrm{FDK}}(x)$ is the right side of the Fact for $f_0$, which equals $f_0(x_1, x_2) = f(x)$. $\square$

## Part 3. Objects that do not depend on $z$

**Lemma 2.** Let $f(x_1, x_2, x_3) = f_0(x_1, x_2)$ with $f_0$ integrable on lines. Then $g(\beta, t, z) = \dfrac{\sqrt{D^2 + t^2 + z^2}}{\sqrt{D^2 + t^2}}\,g_0(\beta, t)$.

*Proof.* Write $v = (v_{12}, v_3)$. Then $f(S + \lambda v) = f_0(S_{12} + \lambda v_{12})$, and $v_{12} = (t\omega - D\omega^\perp)/\sqrt{D^2 + t^2 + z^2}$ has the length $\sqrt{D^2 + t^2}/\sqrt{D^2 + t^2 + z^2}$. Put $\mu = \lambda|v_{12}|$. Then $S_{12} + \lambda v_{12}$ runs along the planar ray from $D\omega^\perp$ through $t\omega$ with the unit speed in $\mu$, and $d\lambda = d\mu/|v_{12}|$. So $g = g_0/|v_{12}|$. $\square$

**Theorem 2.** Let $f(x_1, x_2, x_3) = f_0(x_1, x_2)$ with $f_0$ smooth and supported in the disk of radius $r < D$. Then $f_{\mathrm{FDK}}(x) = f(x)$ for every $x$ with $|(x_1, x_2)| < r$ and every height $x_3$.

*Proof.* By Lemma 2 the weighted data is $D g/\sqrt{D^2 + u^2 + z^2} = D g_0(\beta, u)/\sqrt{D^2 + u^2}$, which does not depend on $z$. So $q(\beta, t, z) = q(\beta, t, 0)$ for every $z$, and $f_{\mathrm{FDK}}(x)$ equals $f_{\mathrm{FDK}}$ at $(x_1, x_2, 0)$, because $U$ and $t'$ do not depend on $x_3$. By the Fact (or Theorem 1) this is $f_0(x_1, x_2)$. $\square$

The detector must be tall enough: the proof needs the data at the height $z' = x_3/U$.

## Part 4. The discrete algorithm

The code samples $t_j = (j - (d-1)/2)\tau$ and $z_r = (r - (m-1)/2)\zeta$ and $\beta_k = 2\pi k/a$. Lines L2 to L5 replace the convolution by $\tau\sum_l \frac{1}{2}h_B((j - l)\tau)\,p_l$, with $h_B$ the band-limited ramp (Ram-Lak) kernel. Line L8 reads $q$ at $(t', z')$ by bilinear interpolation, with 0 outside the detector, and line L9 replaces $\int_0^{2\pi} d\beta$ by $(2\pi/a)\sum_k$. In each row this is the discrete 2D flat-detector fan-beam algorithm, whose errors (band limit, sums over the bins and the angles, interpolation) are discussed on the fan-beam page. Two facts are exact in the discrete case too.

**Proposition 1 (discrete mid-plane).** If $m$ is odd, the output in the slice $x_3 = 0$ depends only on the row $r = (m-1)/2$ of the data.

*Proof.* For $x_3 = 0$, $z' = 0$, so the fractional row index is $0/\zeta + (m-1)/2$, an integer $r_0$. Bilinear interpolation then gives the weight 1 to row $r_0$ and 0 to the row $r_0 + 1$, which the code skips. The filter of line L5 works on each row alone, so row $r_0$ of $q$ depends only on row $r_0$ of the data. $\square$

**Proposition 2 (discrete z-invariance).** If $g(\beta_k, t_j, z_r) = \frac{\sqrt{D^2 + t_j^2 + z_r^2}}{\sqrt{D^2 + t_j^2}}\,c_{kj}$ for numbers $c_{kj}$, as Lemma 2 gives for a $z$-invariant object, then in exact arithmetic the output is the same in every slice $x_3$ at every pixel where the fractional row index $z'/\zeta + (m-1)/2$ lies in $[0, m-1]$.

*Proof.* After line L4 every row of projection $k$ is the same vector $D c_{kj}/\sqrt{D^2 + t_j^2}$, so after line L5 every row of $q_k$ is the same vector $Q_k$. Bilinear interpolation between two equal rows, with weights $1 - w$ and $w$, gives $Q_k$ interpolated in $t$ alone, provided both rows exist. If the index is exactly $m - 1$ the second weight is 0 and only one row is read. This value does not depend on $x_3$. The factor $1/U^2$ and $t'$ do not depend on $x_3$ either. $\square$

The test checks Proposition 1 by changing all other rows at random, and Proposition 2 on an infinite cylinder at three heights. In floating point the two weights of Proposition 2 are computed with rounding, so the test allows $10^{-9}$.

## Part 5. Why FDK is not exact in general

For a point with $x_3 \ne 0$, the rays that FDK uses for one source position lie in the tilted plane through $S(\beta)$ and the detector row $z = z'$. Each source position uses a different tilted plane, and these planes do not form a single plane through $x$. The 2D argument of Theorem 1 needs all the rays in one plane, so it does not apply. This is a heuristic, not a proof that the formula fails. The page gives a measurement: a blob that is thin in $z$ and lies at the height $0.5$ comes out about 7 percent too low, and the error changes little when the sampling is made finer (the peak goes from 0.909 to 0.926), while the same blob in the mid-plane is reconstructed within 0.2 percent. A deeper reason is Tuy's condition: a plane $x_3 = c$ with $c \ne 0$ that cuts the object does not meet the source circle, so the circular orbit does not give the data that exact inversion needs (see the [Tuy condition](/tuy-condition/) and [Grangeat's formula](/grangeat-formula/)).
