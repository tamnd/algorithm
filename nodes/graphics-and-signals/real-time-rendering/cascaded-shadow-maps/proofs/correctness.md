---
title: The practical split scheme is monotone, each cascade map contains its view slice, the lookup is the shadow map test of one map, and the stable fit keeps a fixed texel grid
proves: [correctness]
status: full
---

We use the notation of the page. The camera has its near plane at view depth $n > 0$ and its far plane at $f > n$; here $n$ and $f$ are planes, not counts. There are $m$ cascades. The light is directional, with the orthonormal frame $R$ whose rows are $l_x, l_y, l_z$; a point $p$ has the light coordinates $q = R p$, and $-q_z$ is its light depth. The arithmetic is exact real arithmetic, except where a claim says floating point.

## The splits

Line L1 computes $C_i = \lambda\, n (f/n)^{i/m} + (1 - \lambda)(n + (f - n)\, i / m)$ for $i = 0, \ldots, m$ and a blend $\lambda \in [0, 1]$.

**Lemma 1.** $C_0 = n$, $C_m = f$, and $C_0 < C_1 < \cdots < C_m$. So the slices $[C_i, C_{i+1})$ partition $[n, f)$, and each view depth in $[n, f)$ has exactly one cascade (line L6).

*Proof.* At $i = 0$ both terms equal $n$, and at $i = m$ both equal $f$, so the convex combination does too. For $f > n$, both $n (f/n)^{i/m}$ and $n + (f - n) i / m$ increase strictly in $i$, and a convex combination of two strictly increasing sequences increases strictly. $\square$

With $\lambda = 1$ the ratio $C_{i+1} / C_i = (f/n)^{1/m}$ is the same for all slices (the logarithmic split). With $\lambda = 0$ the differences $C_{i+1} - C_i = (f - n)/m$ are equal (the uniform split). The blend $\lambda$ is a tuning; GPU Gems 3, chapter 10, suggests 0.5.

**Lemma 2 (why the logarithmic split).** Take the model in which the shadow texel size in cascade $i$ is proportional to the slice length $C_{i+1} - C_i$ and the pixel footprint at depth $d$ is proportional to $d$. Then the largest ratio of texel size to pixel footprint at the near end of a slice, $\max_i (C_{i+1} - C_i)/C_i$, over all splits with $C_0 = n$ and $C_m = f$, is smallest for the logarithmic split.

*Proof.* Let $r_i = C_{i+1} / C_i$. The product of the $r_i$ is $f / n$, so the largest $r_i$ is at least the geometric mean $(f/n)^{1/m}$, with equality only when all $r_i$ are equal. The quantity is $\max_i r_i - 1$. $\square$

This is a model, not a property of real scenes: a tight crop also depends on the width of the slice and on the light direction. Zhang, Sun and Nyman (GPU Gems 3, chapter 10) give the logarithmic split as the split that distributes the perspective aliasing evenly; the lemma is a simple form of that argument. The uniform part of the blend is there because the pure logarithmic split makes the first slices very thin when $n$ is small.

## Containment

The slice $S_i$ is the set of points with view depth in $[C_i, C_{i+1}]$ whose image lies on the screen. In the camera frame it is $\{(a d\, t s, b d\, t, d) : d \in [C_i, C_{i+1}], (a, b) \in [-1, 1]^2\}$, written as right, up and forward components, where $t = \tan(\theta/2)$ for the vertical field of view $\theta$ and $s$ is the aspect ratio.

**Lemma 3.** $S_i$ is a convex polytope with the 8 corners that `slice_corners` returns. The rectangle that lines L3 and L4 compute from the corners holds the light $(x, y)$ of every point of $S_i$. The stable fit holds them too.

*Proof.* $S_i$ is the intersection of six half-spaces: the two depth planes and the four planes $|r| \le t s\, d$, $|u| \le t\, d$ through the camera center. So it is convex, and it is bounded, so it is the convex hull of its vertices. Its vertices are the points with $d \in \{C_i, C_{i+1}\}$ and $a, b \in \{-1, 1\}$. The map $p \mapsto (q_x, q_y)$ is linear, so the image of $S_i$ is the convex hull of the images of the corners, and it lies in the box of their least and greatest coordinates.

For the stable fit, every corner lies within the radius $r$ of the corner mean $c$, so $S_i$, the hull of the corners, lies in the ball of radius $r$ around $c$, and its light $(x, y)$ lies in the square of side $2r$ around the light $(x, y)$ of $c$, since $R$ is orthonormal. The fit takes $\mathrm{lo} \le q(c) - r$ per axis, with the texel $\tau = 2r/(N - 1)$ for a map of $N$ texels. The map covers up to $\mathrm{lo} + N \tau > (q(c) - r - \tau) + 2r + \tau = q(c) + r$. $\square$

## The lookup

**Theorem 4.** Let $p$ be a visible point with view depth $d \in [n, f)$. Lines L6 to L8 return the binary [shadow map](/shadow-mapping/) test of $p$ against the map of the unique cascade $i$ with $C_i \le d < C_{i+1}$, at the texel that holds the light $(x, y)$ of $p$. If $p$ is at a texel center of that map and the bias is 0, the result is shadowed exactly when a sphere of the scene meets the ray from $p$ toward the light strictly nearer to the light.

*Proof.* By Lemma 1 there is exactly one such $i$. By Lemma 3 the light $(x, y)$ of $p$ lies in the rectangle of map $i$, so the lookup does not fall outside the map (a point on the upper edge of the rectangle is the one exception, and the code calls it lit). Line L5 rendered map $i$ as the nearest light depth of the spheres at each texel center, and line L8 compares the light depth of $p$ with it. This is the test of shadow mapping, and its exactness at texel centers is the correctness result of that page: the stored value is the least light depth of the spheres along the light ray through the center, and the ray from $p$ toward the light is that ray when $p$ projects to the center. $\square$

Away from texel centers the test is exact when $p$ is farther than half a texel diagonal from every shadow edge, measured in the light $(x, y)$ plane; the test of the code checks the lookup against ray casting at such points.

## The stable fit

**Proposition 5.** In the stable fit, (a) the texel size of each cascade does not change when the camera moves or turns, and (b) the texel centers lie on the fixed grid $\{((k + \tfrac12) \tau, (k' + \tfrac12) \tau)\}$ of the light plane in every frame. So a static occluder gives the same map values at the same light positions in every frame, and its shadow edge does not move from frame to frame.

*Proof.* (a) The corners of $S_i$ in the camera frame depend only on $C_i$, $C_{i+1}$, $t$ and $s$. A motion of the camera is a rotation and a translation, which keep the distances from the corners to their mean. So $r$ is the same in every frame, and so is the rounded radius and $\tau = 2r/(N - 1)$. (b) The fit sets each coordinate of lo to $\lfloor (q - r)/\tau \rfloor\, \tau$, a whole multiple of $\tau$, so the centers $\mathrm{lo} + (k + \tfrac12)\tau$ lie on the stated grid. $\square$

In floating point the radius can change in its last bits when the camera turns. The rounding up of $r$ to a multiple of a quantum makes these changes disappear unless the radius is within one rounding error of a multiple of the quantum. The quantum $1/64$ is a tuning. The cost of the stable fit is that the square of side $2r$ is larger than the tight rectangle, so the texels are larger (by a factor of 1.21 to 1.34 in the example of the page).
