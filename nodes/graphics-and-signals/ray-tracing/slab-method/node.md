---
tag: 2SZ2M7
kind: algorithm
slug: slab-method
name: Slab method (ray-box intersection)
aliases:
- ray-AABB test
- ray-box intersection
area: graphics-and-signals/ray-tracing
level: intro
summary: Intersect a ray with an axis-aligned box by intersecting three parameter intervals, one for each slab between two parallel planes of the box.
solves: [ray-object-intersection]
model: real-ram
complexity:
  vars: {k: the number of axes (3 in space)}
  time: {worst: Θ(k)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1986
  people: [Timothy L. Kay, James T. Kajiya]
  note: Kay and Kajiya bounded objects by sets of slabs and intersected a ray with each set by intersecting the parameter intervals of its slabs.
prereqs: [axis-aligned-bounding-box, ieee-754]
see_also: [bvh-traversal, kd-tree-traversal, ray-sphere-intersection, moller-trumbore, interval-arithmetic, separating-axis-theorem, amanatides-woo-traversal, slab-method-point-location]
sources:
  - paper: doi:10.1145/15886.15916
    title: Timothy L. Kay and James T. Kajiya, Ray tracing complex scenes, SIGGRAPH 1986, Computer Graphics 20(4), 269 to 278
    locator: the slab bounding volumes (pairs of parallel planes with a fixed set of normals) and the ray test that intersects the intervals of the slabs
  - paper: doi:10.1080/2151237X.2005.10129188
    title: Amy Williams, Steve Barrus, R. Keith Morley and Peter Shirley, An efficient and robust ray-box intersection algorithm, Journal of Graphics Tools 10(1), 2005, 49 to 54
    locator: the test with the reciprocal direction and its signs computed once per ray, and the handling of zero direction components with IEEE infinities
  - url: http://jcgt.org/published/0002/02/02/
    title: Thiago Ize, Robust BVH ray traversal, Journal of Computer Graphics Techniques 2(2), 2013, 12 to 27
    locator: Section 2 (min and max that drop a NaN argument) and Section 3 (the rounding error of the slab values and the padding of the far value)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 3.1.2 Ray-Bounds Intersections, and Section 3.9.2 Conservative Ray-Bounds Intersections (the factor 1 + 2γ3 on the far value)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 22, Intersection Test Methods, Section 22.7 Ray/Box Intersection
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 5, Basic Primitive Tests, the section on the intersection of a ray or segment with a box
---

The slab method tests a ray against an [axis-aligned box](/axis-aligned-bounding-box/). It sees the box as the intersection of three slabs, where each slab is the region between two parallel planes, and it computes the interval of the ray parameter $t$ in which the ray is inside each slab. The ray meets the box exactly when the three intervals and the ray's own interval have a common part, and that common part is the piece of the ray inside the box. The test costs a constant number of operations, and it is the inner step of each [BVH traversal](/bvh-traversal/) and [kd-tree traversal](/kd-tree-traversal/).

## In plain words

A box has three pairs of opposite walls: left and right, front and back, floor and ceiling. The space between one pair of walls is a thick layer, a slab. A point is in the box when it is in all three slabs.

Walk along the ray and note the time when you go into each slab and the time when you come out. That gives three time windows. You are in the box while all three windows are open, which is from the last entry to the first exit. If the last entry comes after the first exit, the ray misses the box.

If the ray runs parallel to a pair of walls, it never crosses them. It is between them for all of time, or never. The trick of the method is to let the computer's infinity values handle this case without a special branch.

## The problem

The box is $B = [lo, hi] = \{p \in \mathbb{R}^3 : lo_a \le p_a \le hi_a$ for $a = 0, 1, 2\}$, closed, with finite bounds and $lo_a \le hi_a$. A flat box with $lo_a = hi_a$ is allowed: it is the bound of a triangle that lies in an axis plane. The ray is $r(t) = o + t\,d$ with $d \ne 0$, restricted to a parameter interval $[t_0, t_1]$ with $t_0$ finite and $t_1 \le +\infty$. A primary ray uses $[0, +\infty)$, and a ray in a [closest-hit query](/closest-hit-query/) uses $[0, t_{best}]$.

The output is the set $I = \{t \in [t_0, t_1] : r(t) \in B\}$. Because $B$ is convex and closed, $I$ is a closed interval $[t_{in}, t_{out}]$ or empty. This is the box case of [ray-object intersection](/ray-object-intersection/). It is not the slab decomposition of the plane used for [planar point location](/slab-method-point-location/), which is a different method with the same name.

## The algorithm

For each axis $a$, the slab is $S_a = \{t : lo_a \le o_a + t\,d_a \le hi_a\}$. If $d_a \ne 0$, it is the interval between $(lo_a - o_a)/d_a$ and $(hi_a - o_a)/d_a$. The reciprocal $inv_a = 1/d_a$ is computed once per ray, because a ray is tested against many boxes. In [IEEE 754](/ieee-754/) arithmetic, $1/(+0) = +\infty$ and $1/(-0) = -\infty$, so the same code handles a ray that is parallel to a slab.

```pseudo id=main
SLAB-TEST(lo, hi, o, inv, t0, t1, ρ)   ▷ inv[a] = 1/d[a]; ρ = 1, or 1 + 2γ3 for the conservative test
L1  for a ← 0 to 2 do
L2      if inv[a] ≥ 0 then (n, f) ← (lo[a], hi[a]) else (n, f) ← (hi[a], lo[a])
L3      tn ← (n − o[a]) · inv[a]                    ▷ entry into slab a
L4      tf ← (f − o[a]) · inv[a] · ρ                ▷ exit from slab a
L5      t0 ← MAX(tn, t0)                            ▷ MAX(x, y) = x if x > y, else y
L6      t1 ← MIN(tf, t1)                            ▷ MIN(x, y) = x if x < y, else y
L7      if t0 > t1 then return MISS
L8  return (t0, t1)
```

Line L2 picks the near plane and the far plane from the sign of $inv_a$, so that $tn \le tf$ without a swap (Williams et al. 2005). Lines L5 and L6 shrink the running interval. The two helpers are written with one comparison each, and the new value is the first argument. Each comparison with NaN is false, so a NaN in $tn$ or $tf$ leaves the running value unchanged.

A NaN comes from $0 \cdot \infty$. It appears only when $d_a = 0$ and the origin lies on a plane of slab $a$. Then the ray lies in the plane of a face of the box, and the NaN means "no bound from this plane". With the first argument rule, the test treats the box as closed. The six cases of a zero component are in the [proof](proofs/correctness.md).

Line L7 exits early. A version for SIMD hardware runs all three axes and tests once at the end, and it gets the same answer.

## Example

Take the box $lo = (1, 1, 0)$, $hi = (3, 2, 2)$ and the ray $o = (0, 0, 1)$, $d = (2, 1, 0)$ on $[0, +\infty)$, with $\rho = 1$. Then $inv = (0.5, 1, +\infty)$. The z component of $d$ is zero, so the ray is parallel to the floor and the ceiling of the box.

| axis | $n$ | $f$ | $tn$ (L3) | $tf$ (L4) | $t_0$ (L5) | $t_1$ (L6) |
|---|---|---|---|---|---|---|
| start | | | | | 0 | $+\infty$ |
| x | 1 | 3 | $(1 - 0) \cdot 0.5 = 0.5$ | $(3 - 0) \cdot 0.5 = 1.5$ | 0.5 | 1.5 |
| y | 1 | 2 | $(1 - 0) \cdot 1 = 1$ | $(2 - 0) \cdot 1 = 2$ | 1 | 1.5 |
| z | 0 | 2 | $(0 - 1) \cdot \infty = -\infty$ | $(2 - 1) \cdot \infty = +\infty$ | 1 | 1.5 |

The result is $[1, 1.5]$. The ray goes in at $r(1) = (2, 1, 1)$ on the face $y = 1$ and comes out at $r(1.5) = (3, 1.5, 1)$ on the face $x = 3$.

Move the origin to $o = (0, 0, 2)$, in the plane of the ceiling. In the z row, $tn = (0 - 2) \cdot \infty = -\infty$ and $tf = (2 - 2) \cdot \infty = $ NaN. Line L6 computes MIN(NaN, 1.5): the comparison NaN $<$ 1.5 is false, so $t_1$ stays 1.5 and the result is again $[1, 1.5]$. The ray runs along the ceiling, and the closed box contains it. With the origin at $z = 0$ the NaN is in $tn$ instead, and MAX(NaN, 1) keeps 1. With the origin at $z = 2.5$, $tf = (2 - 2.5) \cdot \infty = -\infty$, so $t_1 = -\infty$ and line L7 returns MISS.

## Correctness

Claim: in exact arithmetic with the IEEE rules for infinities and NaN, and with $\rho = 1$, SLAB-TEST returns MISS if $I$ is empty and returns $I = [t_0, t_1]$ otherwise.

The key invariant holds after each pass of the loop that does not return. Let $A$ be the set of axes done so far. Then the set of real $t$ with $t_0 \le t \le t_1$ is $[t_0^{in}, t_1^{in}] \cap \bigcap_{a \in A} S_a$, where $t_0^{in}$ and $t_1^{in}$ are the input values. One pass keeps it because, in each of the cases $d_a > 0$, $d_a < 0$ and the six cases of $d_a = \pm 0$, the set $\{t : tn \le t \le tf\}$ equals $S_a$ when a NaN is read as "no bound". Line L7 returns MISS only when that set is empty, and after the last axis it is $I$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

In floating point the claim is false in general. Each value $tn$ and $tf$ has a relative error of at most $\gamma_3 = 3u/(1 - 3u)$, where $u = 2^{-53}$ is the unit roundoff of binary64 (Pharr, Jakob and Humphreys, Section 3.9.2). A ray that touches an edge or a corner of the box has $t_{in} = t_{out}$ in exact arithmetic, and rounding can make $t_0 > t_1$ by a few [ulps](/ulp/). With $\rho = 1 + 2\gamma_3$ in line L4 the test is conservative: it does not miss a box that the exact ray meets, and it can report a hit for a ray that misses by a few ulps. A false hit in a bounding volume test only costs time. A false miss drops geometry.

## Complexity

The model is the [real RAM](/real-ram/) with $\pm\infty$; in practice it is IEEE 754 arithmetic. The loop runs once per axis. Each pass makes two subtractions, two multiplications (three with $\rho \ne 1$), one sign test and three comparisons, so the cost is $\Theta(k)$ for $k$ axes, which is $\Theta(1)$ for a box in space. The extra space is the two running values, $O(1)$. The three divisions of $inv$ are made once per ray and are shared by all the boxes that the ray meets in a traversal. The early exit at line L7 makes a miss cheaper on average, but not in the worst case.

## Properties

- **Closed box.** Points on the faces count as inside, also for a ray that lies in the plane of a face.
- **Exact in exact arithmetic.** With rational inputs, a version with exact fractions gives the true interval. The floating-point version is exact when each subtraction and product is exact, for example for integer coordinates and directions whose components are powers of two.
- **Conservative with padding.** With $\rho = 1 + 2\gamma_3$, no false misses; without it, rare false misses at edges and corners.
- **No division in the inner loop.** All divisions are moved to the setup of the ray.
- **Few branches.** Only the sign test and the early exit branch, and both can be removed: the sign is fixed per ray, and the exit can be one test at the end.

## Variants and improvements

- **Kay and Kajiya slabs.** The original method uses slabs with arbitrary normals $n_i$, not only the three axes. A bounding volume is the intersection of $k$ slabs $\{p : d_i^{lo} \le n_i \cdot p \le d_i^{hi}\}$ with a fixed set of normals for the whole scene, so that $n_i \cdot o$ and $1/(n_i \cdot d)$ are computed once per ray. The axis-aligned box is the case of the three coordinate normals, and more normals give a tighter volume.
- **Precomputed signs.** Williams et al. (2005) store the sign of each $inv_a$ in the ray and index the box bounds with it, as line L2 does, and they note that this form handles $d_a = \pm 0$ through IEEE infinities.
- **Robust traversal.** Ize (2013) bounds the rounding error of $tn$ and $tf$ and widens the far value by a few ulps, so that a traversal never misses a box that the ray meets. PBRT multiplies the far value by $1 + 2\gamma_3$, as in line L4.
- **Wide and packet tests.** A node of a wide BVH tests one ray against 4 or 8 boxes, one per SIMD lane, with the same lines L3 to L7 in vector registers. [Ray packets](/ray-packet-tracing/) test many rays against one box. The SSE instructions for min and max return the second operand when either operand is NaN, which matches the argument order of lines L5 and L6.
- **Entry face.** If the origin is outside the box, the axis that sets the final $t_0$ at line L5 is the axis of the entry face. A box primitive needs it for its normal.
- **Oriented boxes.** For a box with its own frame, move the ray into the frame of the box and use the same test.

## When to use it

Use it for every ray against box test in a hierarchy: [BVH traversal](/bvh-traversal/), the root clip of a [kd-tree traversal](/kd-tree-traversal/), and the entry into a grid before [Amanatides-Woo traversal](/amanatides-woo-traversal/). For a segment against a box in collision code, a test of separating axes ([separating axis theorem](/separating-axis-theorem/)) is an alternative that does not need $t$. For a sphere, use [ray-sphere intersection](/ray-sphere-intersection/), and for a triangle use [Möller-Trumbore](/moller-trumbore/) or a [watertight test](/watertight-ray-triangle-intersection/). If the answer must be exact, as for a sign decision in a geometric algorithm, use fractions or [interval arithmetic](/interval-arithmetic/), not floats.

## Pitfalls

- **A min or max that keeps the NaN.** Line L5 must read $t_0 \leftarrow$ MAX$(tn, t_0)$, with the slab value first. If it reads MAX$(t_0, tn)$ with the same helper, then a NaN $tn$ becomes the new $t_0$, each later comparison with it is false, line L7 never fires, and the test reports a hit for a ray that runs in the plane of a face but passes beside the box. Library functions differ: C `fmax` and `fmin` drop a NaN, while C++ `std::max` and `std::min` and Python `max` and `min` return their first argument when a NaN is involved, which is the opposite order of the helpers here. The same holds for line L6.
- **The sign of zero.** Line L2 must test the sign of $inv_a$, not the test $d_a < 0$. For $d_a = -0$, the test $d_a < 0$ is false but $inv_a = -\infty$. Then $n = lo_a$, and for an origin inside the slab, $tn = (lo_a - o_a) \cdot (-\infty) = +\infty$, so the ray misses a box that it goes through.
- **A division that traps.** In languages that raise an error on $1/0$, for example Python, compute $inv_a$ as an infinity with the sign of $d_a$. Do not replace $d_a = 0$ by a tiny number: the result then depends on that number.
- **False misses at edges.** Line L4 with $\rho = 1$ can drop a ray that grazes an edge. In a BVH this drops a whole subtree, and the image shows single missing pixels along the edges of boxes. Use $\rho = 1 + 2\gamma_3$, or Ize's padding, when the traversal must be complete.
- **The wrong start interval.** Starting with $t_0 = -\infty$ instead of the ray's $t_{min}$ accepts boxes behind the origin. In a closest-hit traversal, pass the current best hit as $t_1$, so that farther boxes are rejected.
- **Rejecting flat boxes.** A box with $lo_a = hi_a$ is valid. Code that adds a test such as $tf - tn > \epsilon$ drops triangles that lie in axis planes, which are common in architectural scenes.

## Implementations

## History

Rubin and Whitted (1980) ray traced scenes through a hierarchy of bounding volumes. Kay and Kajiya (1986) defined bounding volumes as intersections of slabs with a fixed set of normals, tested a ray against such a volume by intersecting the parameter intervals of its slabs, and visited the hierarchy in the order of the entry distance with a heap. Williams, Barrus, Morley and Shirley (2005) gave the form with the precomputed reciprocal and signs, which handles zero components with IEEE infinities. Ize (2013) bounded its rounding error and made BVH traversal robust by padding the far value. The form in line L4 is the one in the third edition of PBRT.

## References
