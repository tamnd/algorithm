---
tag: PWY9S0
kind: algorithm
slug: simplex-noise
name: Simplex noise
aliases:
- Perlin simplex noise
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Gradient noise summed over the n + 1 corners of the simplex that holds the point, which costs O(n^2) instead of O(n 2^n) in n dimensions.
model: real-ram
complexity:
  vars: {n: the dimension of the domain, q: the number of points at which the noise is evaluated}
  time: {worst: Θ(q n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true, in_place: false}
history:
  year: 2001
  people: [Ken Perlin]
  note: Perlin presented simplex noise in his SIGGRAPH course notes of 2001 and 2002 as a replacement for his lattice noise. Stefan Gustavson explained it with code for two to four dimensions in 2005.
prereqs: [perlin-noise, hash-function]
see_also: [perlin-noise, worley-noise, fractal-noise, bump-mapping, triangulation, random-permutation, delaunay-triangulation, hash-function]
sources:
  - paper: "Ken Perlin, Noise hardware, in Real-Time Shading, SIGGRAPH 2001 course notes"
    title: Ken Perlin, Noise hardware, SIGGRAPH 2001 course notes
    locator: the simplex grid, the skew of the input, and the radial kernel per corner (general locator)
  - url: https://itn-web.it.liu.se/~stegu76/simplexnoise/simplexnoise.pdf
    title: Stefan Gustavson, Simplex noise demystified, Linköping University, 2005
    locator: the 2D code (skew factor F2, unskew factor G2, the radius 0.5 and the scale 70) and the 3D code, with the note that its radius 0.6 should be 0.5 for continuity
  - paper: doi:10.1145/325165.325247
    title: Ken Perlin, An image synthesizer, Computer Graphics 19(3), SIGGRAPH 1985, pages 287 to 296
    locator: the lattice gradient noise that simplex noise replaces (general locator)
---

Simplex noise is a gradient noise on $\mathbb{R}^n$, like [Perlin noise](/perlin-noise/), but it uses a different grid. Perlin noise blends the $2^n$ corners of a cube cell. Simplex noise splits space into simplices (triangles in 2D, tetrahedra in 3D) and adds one radial kernel for each of the $n + 1$ corners of the simplex that holds the point. So it costs $O(n^2)$ per point in place of $\Theta(n 2^n)$, it has less axis bias, and its gradient is continuous. Like Perlin noise it is a base noise for [fractal noise](/fractal-noise/). [Worley noise](/worley-noise/) is a different kind of base noise, made of distances to random points.

## In plain words

Cover the plane with equal triangles. At each corner of each triangle, put a small tilted plane with a random slope, and fade it out in a round bump around the corner. The noise at a point is the sum of the bumps that reach it.

The trick is that the bumps are small enough that only the three corners of the triangle that holds the point can reach it. So you find that triangle, add three terms, and you are done. In 3D there are four corners, in 4D five. A square grid would need four, eight and sixteen corners.

To find the triangle quickly, the method stretches the plane along its diagonal, so that the triangles become halves of unit squares.

## The problem

The input is a point $x \in \mathbb{R}^n$ and a permutation $P$ of $0, \dots, 255$, stored twice as in Perlin noise. The output is a real number $N(x)$. Let $F = (\sqrt{n+1} - 1)/n$ and $G = (1 - 1/\sqrt{n+1})/n$, and let $S(x)$ be the sum of the coordinates. The skew $\sigma(x) = x + F S(x) \mathbf{1}$ maps the simplex grid onto the integer lattice $\mathbb{Z}^n$, and the unskew $\tau(y) = y - G S(y) \mathbf{1}$ is its inverse. In 2D, $F = (\sqrt3 - 1)/2$ and $G = (3 - \sqrt3)/6$.

Each lattice point $k$ has a gradient $g_k$, chosen by a nested [hash](/hash-function/) of its coordinates through $P$. Its kernel at $x$ is $T_k(x) = \max(0, r^2 - |d|^2)^4 \, (g_k \cdot d)$ with $d = x - \tau(k)$ and $r^2 = \tfrac12$. The noise is $N(x) = \sum_{k \in \mathbb{Z}^n} T_k(x)$. The task is to compute this sum without a search over the lattice.

## The algorithm

```pseudo id=main
SIMPLEX-NOISE(x, P)                            ▷ x in R^n
L1  s ← F · (x_1 + ... + x_n)                  ▷ the skew
L2  k ← (⌊x_1 + s⌋, ..., ⌊x_n + s⌋)            ▷ the cell in skewed space
L3  π ← the axes sorted by decreasing x_i + s - k_i
L4  c_0 ← k; c_m ← c_{m-1} + e_{π(m)} for m = 1..n
L5  for m ← 0 to n do
L6      d ← x - (c_m - G · (sum of c_m) · 1)   ▷ the unskewed offset
L7      if r^2 - |d|^2 ≤ 0 then skip this corner
L8      total ← total + (r^2 - |d|^2)^4 · (g[HASH(c_m, P)] · d)
L9  return scale · total
```

The table $g$ in the code is the table of Gustavson's code in 2D and 3D: the 12 edge directions of a cube, with the hash modulo 12, and in 2D their first two components. In four or more dimensions it holds the vectors with entries in $\{-1, 0, 1\}$ and exactly one zero. The scale is 70 in 2D, as in Gustavson's code, and 1 otherwise. It only sets the range.

## Example

Take $x = (\tfrac14, \tfrac12)$ in 2D and the permutation of seed 0 in the code. Line L1 gives $s = 0.75 F \approx 0.2745$, so the skewed point is about $(0.5245, 0.7745)$ and $k = (0, 0)$. The $y$ part is larger, so line L4 steps along $y$ first, and the corners are $(0, 0)$, $(0, 1)$ and $(1, 1)$.

| corner | unskewed corner | $d$ | $\tfrac12 - \lvert d \rvert^2$ | $g$ | $g \cdot d$ | term |
|---|---|---|---|---|---|---|
| $(0, 0)$ | $(0, 0)$ | $(0.2500, 0.5000)$ | $0.1875$ | $(1, 0)$ | $0.2500$ | $0.000309$ |
| $(0, 1)$ | $(-0.2113, 0.7887)$ | $(0.4613, -0.2887)$ | $0.2038$ | $(0, -1)$ | $0.2887$ | $0.000498$ |
| $(1, 1)$ | $(0.5774, 0.5774)$ | $(-0.3274, -0.0774)$ | $0.3869$ | $(1, 0)$ | $-0.3274$ | $-0.007332$ |

The sum is $-0.006524$, and with the scale 70 the noise is $N(x) \approx -0.4567$. The nearest corner, $(1, 1)$, has the largest weight, as expected.

## Correctness

The proof file shows that the sum over the $n + 1$ corners equals the sum over the whole lattice when $r^2 \le \tfrac12$. The key step is a formula for the distance. If $e$ is an offset in skewed space, then $|\tau(e)|^2 = |e|^2 - S(e)^2/(n+1)$, which is the spread of the $n + 1$ numbers $(e_1, \dots, e_n, 0)$ about their mean. For a lattice point that is not one of the chosen corners, two of these numbers differ by at least 1, so the squared distance is at least $\tfrac12$, and its kernel is zero.

Three facts follow. The value does not depend on how line L3 breaks ties, so the noise is continuous across the faces of the simplices. The noise is $C^3$, because $\max(0, t)^4$ is $C^3$. And the noise is zero at every lattice point. The bound $\tfrac12$ is reached, so a larger radius makes the corner sum drop terms that are not zero.

## Complexity

Lines L1 and L2 take $O(n)$ time. The sort of line L3 takes $O(n \log n)$. Each of the $n + 1$ corners takes $O(n)$ for the unskew, the distance, the dot product and the $n$ lookups of the hash. So one point costs $\Theta(n^2)$, and $q$ points cost $\Theta(q n^2)$, in the real-RAM model. Perlin noise costs $\Theta(n 2^n)$: in 3D that is 4 corners against 8, and in 4D 5 corners against 16. The extra space is $\Theta(n)$ for the corner, plus the table of 512 entries.

## Properties

- **Continuous with a continuous gradient.** This is a proved property for $r^2 \le \tfrac12$. The noise is $C^3$.
- **Zero at the lattice points.** $N(\tau(k)) = 0$ for every $k \in \mathbb{Z}^n$. This is proved.
- **Less axis bias.** The kernels are radial, so the pattern has fewer features along the axes than Perlin noise. This is an observation, not a theorem.
- **Range.** With the scale 70 in 2D, the largest absolute value on 200000 random points with seed 0 is $0.998$. This is a measurement. Other dimensions need their own scale.
- **Period.** The hash reduces each coordinate modulo 256, so the noise repeats every 256 units of the skewed lattice.

## Variants and improvements

- **Gustavson's code.** It unrolls the sort of line L3 into comparisons, two in 2D and a decision tree in 3D, and hard-codes the corner offsets.
- **Radius 0.6.** Gustavson's 3D and 4D code first used $r^2 = 0.6$, which gives wider and smoother bumps. The PDF now marks it as an error: with 0.6 the noise jumps on the faces of the simplices. See the pitfall below.
- **Analytic derivatives.** The kernel is a polynomial in $d$, so its gradient costs little more than its value. This is useful for [bump mapping](/bump-mapping/) and flow noise.
- **OpenSimplex and similar.** Other lattices and kernels avoid some of the artifacts of the plain simplex grid. They follow the same plan of a few corners and a radial kernel.
- **Tiling.** A tiling version needs a lattice whose period matches the simplex grid, which is harder than for Perlin noise.

## When to use it

Use simplex noise in three or more dimensions, for example 3D noise animated in time as 4D noise, where the corner count of Perlin noise grows fast. Use it when the axis bias of Perlin noise shows, or when the shading needs a continuous gradient. In 2D at small scale the gain over [Perlin noise](/perlin-noise/) is small, and Perlin noise tiles more easily. Use [Worley noise](/worley-noise/) for cell patterns, and [fractal noise](/fractal-noise/) to sum several octaves of either base noise.

## Pitfalls

- **A radius above $\tfrac12$.** The sum then misses terms of lattice points outside the simplex. The noise jumps on the faces. In 3D the code test measures the jump with $r^2 = 0.6$.
- **A wrong unskew factor.** $F$ and $G$ must satisfy $(1 + nF)(1 - nG) = 1$. A copy of the 2D constants in 3D, or a rounded constant, puts the point in the wrong simplex.
- **Truncation in place of floor.** As for Perlin noise, a cast to an integer gives the wrong cell for negative coordinates.
- **Assuming a range.** The scale depends on the dimension, the radius and the gradient set. Measure the range or bound it before you clamp.
- **Hash collisions in high dimensions.** With a table of 256 entries, the nested hash repeats with the period 256, and in many dimensions this can show as repeats in the pattern.

## Implementations

## History

Ken Perlin presented simplex noise in his SIGGRAPH course notes of 2001 and 2002, with a compact reference code in Java. His aims were a lower cost in high dimensions, a design that suits hardware, and the removal of the axis artifacts of his 1985 noise. Few people used it at first, because the reference code was hard to read. In 2005 Stefan Gustavson wrote Simplex noise demystified, which explains the skew and the choice of the simplex and gives readable code for two, three and four dimensions. Most later implementations follow his code.

## References
