---
tag: QWP9HR
kind: algorithm
slug: perlin-noise
name: Perlin noise
aliases:
- gradient noise
- improved Perlin noise
area: graphics-and-signals/real-time-rendering
level: core
summary: A smooth pseudorandom function made by interpolating random gradients at the points of an integer lattice with a quintic fade curve.
model: real-ram
complexity:
  vars: {n: the dimension of the domain, q: the number of points at which the noise is evaluated}
  time: {worst: Θ(q n 2^n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, in_place: false}
history:
  year: 1985
  people: [Ken Perlin]
  note: Perlin described noise in his SIGGRAPH 1985 paper An image synthesizer. In 2002 he replaced the cubic interpolant by a quintic fade and the random gradients by 12 fixed directions.
prereqs: [texture-mapping, hash-function]
see_also: [simplex-noise, worley-noise, fractal-noise, bump-mapping, random-permutation, fisher-yates-shuffle, bilinear-interpolation, texture-mapping]
sources:
  - paper: doi:10.1145/325165.325247
    title: Ken Perlin, An image synthesizer, Computer Graphics 19(3), SIGGRAPH 1985, pages 287 to 296
    locator: the noise function (pseudorandom gradients at the integer lattice, interpolated with a cubic) and its use in procedural textures (general locator)
  - paper: doi:10.1145/566654.566636
    title: Ken Perlin, Improving noise, ACM Transactions on Graphics 21(3), SIGGRAPH 2002, pages 681 to 682
    locator: the whole paper (the fade 6t^5 - 15t^4 + 10t^3 and the 12 gradient directions, with the reference code)
  - book: isbn:9781558608481
    title: David S. Ebert, F. Kenton Musgrave, Darwyn Peachey, Ken Perlin and Steven Worley, Texturing and Modeling, A Procedural Approach, third edition, Morgan Kaufmann, 2003
    locator: the chapters by Peachey on building procedural textures and by Perlin on noise (general locator)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 10.6.1, Perlin Noise
---

Perlin noise is a pseudorandom function on $\mathbb{R}^n$ that is smooth, has no visible structure at a large scale, and has most of its variation at the scale of one lattice cell. At each point of the integer lattice it fixes a random gradient vector. At any other point it blends the linear functions of the $2^n$ corners of the cell, with a fade curve as the weight. The function is zero at every lattice point and repeats with a period of 256 in each axis. It is the base of most procedural textures, and of [fractal noise](/fractal-noise/), which sums it at many scales. This page gives the improved version of Perlin (2002) in three dimensions. [Simplex noise](/simplex-noise/) is a later noise of Perlin that sums over the $n + 1$ corners of a simplex, and [Worley noise](/worley-noise/) is a different basis made of distances to random points.

## In plain words

You want a random pattern for marble, clouds or rough stone, but white noise looks like television static, and a texture image repeats and costs memory. Perlin noise is a formula that you can evaluate at any point.

Think of a grid of posts. On top of each post sits a small tilted plane, and the tilt is random. To get the value at a point, find the cell of the grid that holds it. Each corner of the cell gives the height of its tilted plane at that point. Then blend the corner heights, with a smooth curve that gives more weight to the nearer corners. The result is a gentle surface of hills and valleys, about one cell wide, that passes through zero at each post. The same point always gives the same value, so the pattern stays fixed on the object.

## The problem

The input is a point $p = (x, y, z) \in \mathbb{R}^3$ and a permutation $P$ of $0, \dots, 255$. In the code, $P$ comes from a seeded [Fisher-Yates shuffle](/fisher-yates-shuffle/), and it is stored twice, as $P[0 \ldots 511]$ with $P[i + 256] = P[i]$, so that sums of indices need no reduction. The output is a real number $N(p)$. The required properties are: $N$ is deterministic for a fixed $P$, it is $C^2$, it is 0 at the lattice points, its gradient at a lattice point is the gradient that the [hash](/hash-function/) gives that point, and its values in different cells are not correlated beyond the neighbors.

The gradient set $G$ holds the 12 vectors from the center of a cube to the midpoints of its edges, $(\pm 1, \pm 1, 0)$, $(\pm 1, 0, \pm 1)$ and $(0, \pm 1, \pm 1)$, and four of them again, $(1, 1, 0)$, $(0, -1, 1)$, $(-1, 1, 0)$ and $(0, -1, -1)$, for 16 entries. With 16 entries the index is $h \bmod 16$, a bit mask.

## The algorithm

```pseudo id=main
PERLIN-NOISE(x, y, z, P)                       ▷ P: a permutation of 0..255, stored twice
L1  (X, Y, Z) ← (⌊x⌋ mod 256, ⌊y⌋ mod 256, ⌊z⌋ mod 256)
L2  (x, y, z) ← (x - ⌊x⌋, y - ⌊y⌋, z - ⌊z⌋)     ▷ the position in the unit cell
L3  (u, v, w) ← (FADE(x), FADE(y), FADE(z))
L4  for each corner (a, b, c) in {0, 1}^3 do
L5      h ← P[P[P[X + a] + Y + b] + Z + c]     ▷ the hash of the corner
L6      n[a, b, c] ← GRAD(h, x - a, y - b, z - c)
L7  blend the 8 values n with lerp in x by u, then in y by v, then in z by w
L8  return the blended value

FADE(t)
L9  return 6t^5 - 15t^4 + 10t^3

GRAD(h, x, y, z)
L10 return G[h mod 16] · (x, y, z)
```

Here $\mathrm{lerp}(t, A, B) = A + t (B - A)$. In the code the hashes of line L5 share their inner lookups, as in Perlin's reference code: $A = P[X] + Y$, $AA = P[A] + Z$, and so on. GRAD in the code uses bit tests in place of the table, which give the same 16 vectors with no multiplication.

The fade $f$ has $f(0) = 0$, $f(1) = 1$ and zero first and second derivatives at 0 and 1. So a corner has the full weight at its own lattice point, no weight on the far side of the cell, and the weight changes with no jump in its first two derivatives across a cell face.

## Example

Take the point $p = (\tfrac14, \tfrac12, 0)$ in the cell of the origin, and the permutation of seed 0 in the code. Its hash gives the corner gradients $g_{000} = (0, -1, -1)$, $g_{100} = (0, -1, 1)$, $g_{010} = (1, 1, 0)$ and $g_{110} = (0, 1, 1)$. Since $z = 0$, the weight $w = f(0) = 0$, and the four corners with $c = 1$ do not count.

| corner | offset $p - $ corner | $g \cdot$ offset |
|---|---|---|
| $(0, 0, 0)$ | $(\tfrac14, \tfrac12, 0)$ | $-\tfrac12$ |
| $(1, 0, 0)$ | $(-\tfrac34, \tfrac12, 0)$ | $-\tfrac12$ |
| $(0, 1, 0)$ | $(\tfrac14, -\tfrac12, 0)$ | $-\tfrac14$ |
| $(1, 1, 0)$ | $(-\tfrac34, -\tfrac12, 0)$ | $-\tfrac12$ |

The fades are $u = f(\tfrac14) = \tfrac{53}{512}$ and $v = f(\tfrac12) = \tfrac12$. The lerp in $x$ gives $-\tfrac12$ on the edge $y = 0$, and $-\tfrac14 + \tfrac{53}{512}(-\tfrac12 + \tfrac14) = -\tfrac{565}{2048}$ on the edge $y = 1$. The lerp in $y$ gives $N(p) = \tfrac12 (-\tfrac{1024}{2048} - \tfrac{565}{2048}) = -\tfrac{1589}{4096} \approx -0.3879$. At the corner $(0, 0, 0)$ itself, every offset either is zero or has a component of absolute value 1, where the weight is 0, so $N = 0$.

## Correctness

The proof file shows four facts in exact arithmetic. First, the nested lerps of line L7 equal the sum, over the 8 corners, of the corner value times a product of fades, one per axis. Second, this is the same as a sum over all lattice points $q$ of a kernel $K(p - q) = \prod_i s(p_i - q_i)$ times $g_q \cdot (p - q)$, where $s(r) = 1 - f(|r|)$ on $[-1, 1]$ and 0 outside. The kernel is $C^2$ because $f'$ and $f''$ vanish at 0 and 1, so $N$ is $C^2$, its value at a lattice point is 0, and its gradient there is $g_q$. Third, $|N| \le 2$ in three dimensions, because each corner value is at most 2 and the weights are convex. Fourth, $N$ has the period 256 in each axis, because line L1 reduces the cell index modulo 256.

## Complexity

In $n$ dimensions one evaluation visits the $2^n$ corners of the cell, and each corner costs $n$ table lookups and a dot product of length $n$. The blend is $2^n - 1$ lerps. So one point costs $\Theta(n 2^n)$ operations, and $q$ points cost $\Theta(q n 2^n)$, in the real-RAM model. In three dimensions this is 8 corners and 7 lerps, a constant. The table takes 512 entries. On a GPU the table is a small texture or a hash function in the shader. [Simplex noise](/simplex-noise/) costs $O(n^2)$ per point, which is less for $n \ge 4$.

## Properties

- **Band limited in practice.** Most of the energy lies near the frequency of one cell, so the noise can be scaled to a chosen feature size and summed at several scales without much overlap. It is not strictly band limited: the fade and the lattice add higher frequencies.
- **Zero at the lattice.** $N(q) = 0$ for $q \in \mathbb{Z}^3$. A sample on the integers gives a constant image.
- **Range.** The proved bound is $|N| \le 2$. It is not tight: on 200000 random points with seed 0, the largest absolute value is $0.921$. Do not assume the range $[-1, 1]$ without a scale and a clamp.
- **Period.** The pattern repeats every 256 units in each axis.
- **Axis bias.** The cells are cubes, and the 12 gradients lie in the coordinate planes, so the noise has slight directional features along the axes. Simplex noise has less of this.

## Variants and improvements

- **Original noise (1985).** A table of random unit gradient vectors and the cubic fade $3t^2 - 2t^3$. Its second derivative jumps on the cell faces, which shows as artifacts in [bump mapping](/bump-mapping/), where the shading uses the derivative of the noise.
- **Value noise.** Random values, not gradients, at the lattice points, interpolated in the same way. It is cheaper but looks more blocky, and it is not zero at the lattice.
- **Analytic derivatives.** Differentiate the sum of Lemma 2 in the proof file to get $\nabla N$ with the value, which bump mapping and terrain need.
- **Tiling noise.** Reduce the cell index modulo a period $T$ before the hash, so that the noise tiles on a texture of $T$ cells.
- **Hash in place of a table.** GPU code often replaces $P$ by an integer hash of the cell coordinates.
- **Higher dimensions.** Four-dimensional noise animates a three-dimensional pattern in time. Its cost is 16 corners, which is one reason for [simplex noise](/simplex-noise/).

## When to use it

Use Perlin noise for procedural textures, terrain heights, cloud density, and to perturb other textures or animation curves. Use it as the base octave of [fractal noise](/fractal-noise/) and turbulence. Use [simplex noise](/simplex-noise/) in four or more dimensions, or when the axis bias is visible, and [Worley noise](/worley-noise/) for cell-like patterns such as stone, scales or foam. When the texture is fixed and the memory is free, a stored [texture](/texture-mapping/) with [mipmaps](/mipmap/) is cheaper to sample.

## Pitfalls

- **Truncation in place of floor.** A cast to an integer rounds toward zero in C and many shader languages. For negative coordinates this gives the wrong cell and a seam at 0. Use floor, as in lines L1 and L2.
- **Integer sample points.** Sampling at integer coordinates, or at a scale that maps the pixels to integers, gives zeros.
- **Precision far from the origin.** With 32-bit floats, $x - \lfloor x \rfloor$ loses bits when $|x|$ is large, and the noise becomes blocky. Keep the coordinates small, or wrap them by the period first.
- **Assuming a range.** The range depends on the dimension and the gradient set. Scale and clamp by a measured or proved bound.
- **Aliasing.** Noise at a frequency above half the pixel rate aliases. In a fractal sum, drop the octaves that are finer than a pixel. See [aliasing](/aliasing/).
- **A different table on each machine.** The pattern depends on $P$. To get the same texture on every run and platform, fix the seed or the table.

## Implementations

## History

Perlin described noise in 1985, in the paper An image synthesizer, as one primitive of a language for procedural shading of images. There the gradients were pseudorandom vectors from a table, and the interpolant was the cubic $3t^2 - 2t^3$. In the 2002 note Improving noise, Perlin replaced the cubic by the quintic fade, to make the second derivative continuous, and replaced the random gradients by 12 fixed edge directions of a cube, to remove clumps where random gradients happen to align. In 2001 he had described [simplex noise](/simplex-noise/), which uses a simplex grid in place of the cubic lattice.

## References
