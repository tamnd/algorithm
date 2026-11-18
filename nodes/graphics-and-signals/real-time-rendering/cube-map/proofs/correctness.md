---
title: Correctness of the cube map operations
proves: [correctness]
status: full
---

**Setting.** The cube is $[-1, 1]^3$ and the faces are the six squares where one coordinate is $\pm 1$. A cube map of size $N$ stores one value per texel $(f, i, j)$ with $f \in \{0, \dots, 5\}$ (the OpenGL order $+x, -x, +y, -y, +z, -z$) and $0 \le i, j < N$. The invariant of the representation is: there are six arrays of $N \times N$ values, and texel $(f, i, j)$ is the part of face $f$ with $s \in [i/N, (i+1)/N]$ and $t \in [j/N, (j+1)/N]$, where $(s, t)$ are the face coordinates of the OpenGL table. No operation except `store` changes the arrays, and `store` changes one entry, so the invariant always holds. The claims are in exact arithmetic, for a direction $d \ne 0$.

**Claim 1 (the face).** Let $a$ be the axis of the largest $|d_a|$ (line L1) and $\sigma$ the sign of $d_a$. The ray $\{\lambda d : \lambda > 0\}$ leaves the cube through face $(a, \sigma)$, at the point $p = d / |d_a|$.

*Proof.* The ray is inside the cube while $\lambda \max_k |d_k| \le 1$, so it leaves at $\lambda = 1 / |d_a|$. At that point $p_a = \sigma$ and $|p_k| = |d_k| / |d_a| \le 1$ for the other axes, so $p$ is on face $(a, \sigma)$. If two components tie, $p$ is on the common edge of two faces, and both faces contain it; the fixed tie order picks one of them. $\square$

**Claim 2 (the face coordinates).** Lines L2 and L3 give $s, t \in [0, 1]$, and they are the coordinates of $p$ in the square of the face, an affine map of its two other components.

*Proof.* In each row of the table, $sc$ and $tc$ are the two components of $d$ other than $d_a$, each with a fixed sign, and $ma = d_a$. So $sc / |ma|$ and $tc / |ma|$ are $\pm p_k$ for the two other axes $k$, and they are in $[-1, 1]$ by Claim 1. Then $s = (sc / |ma| + 1)/2$ and $t = (tc / |ma| + 1)/2$ are in $[0, 1]$. $\square$

**Claim 3 (round trip).** `face_direction(f, s, t)` returns $d / |d|$ for $(f, s, t) =$ `face_coords(d)`.

*Proof.* `face_direction` sets $sc' = 2s - 1 = sc / |ma|$ and $tc' = 2t - 1 = tc / |ma|$. For each face it builds the vector with $\sigma$ in coordinate $a$ and the other two coordinates from $sc'$ and $tc'$ with the inverse signs of the table. For example on $+x$, the table gives $sc = -z$, $tc = -y$, and the inverse is $(1, -tc', -sc') = (1, y/|x|, z/|x|) = d / |x|$. The other five rows are checked the same way. So the vector is $p = d / |d_a|$, and its normalization is $d / |d|$. $\square$

**Claim 4 (the texel).** Line L4 returns the texel that contains $(s, t)$: $i = \min(\lfloor sN \rfloor, N - 1)$ satisfies $i/N \le s \le (i+1)/N$, and the same for $j$. The center of texel $(f, i, j)$ maps back to $(f, i, j)$.

*Proof.* For $s < 1$, $\lfloor sN \rfloor \le sN < \lfloor sN \rfloor + 1$; for $s = 1$, the minimum gives $i = N - 1$ and $s = (i+1)/N$. For the center, $s = (i + 1/2)/N$, so $sc' = 2s - 1$ has $|sc'| < 1$, and the same for $tc'$. The direction of the center then has $|p_a| = 1 > |p_k|$, so line L1 selects $f$ with no tie, Claim 3 returns the same $s$ and $t$, and $\lfloor (i + 1/2) \rfloor = i$. $\square$

**Claim 5 (store and lookup).** After any sequence of `store` operations, `lookup(d)` returns the value of the last `store` to the texel of $d$ given by Claims 1 to 4, or the initial value 0 if there was none.

*Proof.* `store(f, i, j, v)` writes `faces[f][j][i]`, and line L5 reads `faces[f][j][i]` for the $(f, i, j)$ of line L4. Each entry holds the last value written to it. $\square$

**Claim 6 (solid angle).** The solid angle of the rectangle $[x_0, x_1] \times [y_0, y_1]$ of a face is $F(x_1, y_1) - F(x_0, y_1) - F(x_1, y_0) + F(x_0, y_0)$ with $F(x, y) = \arctan\big(xy / \sqrt{1 + x^2 + y^2}\big)$, and the $6 N^2$ texels have a total solid angle of $4\pi$.

*Proof.* A point $(x, y)$ of the face plane at distance 1 from the center is at distance $r = \sqrt{1 + x^2 + y^2}$, and the plane makes the angle with $\cos = 1/r$ with the ray. So $d\omega = \cos / r^2\, dA = dA / r^3$. With $r^2 + x^2 y^2 = (1 + x^2)(1 + y^2)$, the derivative is $\partial F / \partial x = y / ((1 + x^2) r)$, and then $\partial^2 F / \partial x \partial y = \frac{1}{1 + x^2} \cdot \frac{r^2 - y^2}{r^3} = 1 / r^3$. The double integral of $1/r^3$ over the rectangle is the alternating sum of $F$ at the corners. A whole face has $4 F(1, 1) = 4 \arctan(1/\sqrt 3) = 4\pi/6$, and the texels of a face partition it, so the total over six faces is $4\pi$. $\square$

**Cost.** Lines L1 to L5 do a constant number of comparisons, one division per coordinate and two array reads, so `lookup`, `store` and `texel_direction` cost $O(1)$. `fill` evaluates the function once per texel, $\Theta(N^2)$ per face. The memory is $6 N^2$ values. $\blacksquare$
