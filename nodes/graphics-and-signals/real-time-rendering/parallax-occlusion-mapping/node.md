---
tag: 2N7VM7
kind: algorithm
slug: parallax-occlusion-mapping
name: Parallax occlusion mapping
aliases:
- POM
- steep parallax mapping
area: graphics-and-signals/real-time-rendering
level: advanced
summary: March the view ray through a height field in texture space to find the first intersection, giving parallax and self-occlusion per pixel.
model: real-ram
complexity:
  vars: {k: the number of steps of the march, P: the number of shaded pixels}
  time: {worst: Θ(P k), best: Θ(P)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, in_place: false}
history:
  year: 2004
  people: [Zoe Brawley, Natalya Tatarchuk]
  note: Brawley and Tatarchuk described the per-pixel march in ShaderX3 in 2004. Tatarchuk presented the dynamic version with approximate soft shadows at I3D 2006.
prereqs: [parallax-mapping, texture-mapping]
see_also: [parallax-mapping, bump-mapping, normal-mapping, displacement-mapping, ray-marching, secant-method, sphere-tracing, bilinear-filtering]
sources:
  - paper: doi:10.1145/1111411.1111423
    title: Natalya Tatarchuk, Dynamic parallax occlusion mapping with approximate soft shadows, Proceedings of the 2006 Symposium on Interactive 3D Graphics and Games (I3D 2006)
    locator: the linear march of the height field in tangent space, the intersection between the last two samples, and the soft shadow march toward the light (general locator)
  - paper: doi:10.1145/1185657.1185830
    title: Natalya Tatarchuk, Practical parallax occlusion mapping with approximate soft shadows for detailed surface rendering, SIGGRAPH 2006 course notes
    locator: the course version of the same method, with the choice of the sample count (general locator)
  - paper: "Zoe Brawley and Natalya Tatarchuk, Parallax occlusion mapping, self-shadowing, perspective-correct bump mapping using reverse height map tracing, in Wolfgang Engel (editor), ShaderX3, Charles River Media, 2004, pages 135 to 154"
    title: Zoe Brawley and Natalya Tatarchuk, Parallax occlusion mapping, ShaderX3, 2004
    locator: the whole chapter (the per-pixel march of the height map)
  - paper: "Fabio Policarpo, Manuel M. Oliveira and João L. D. Comba, Real-time relief mapping on arbitrary polygonal surfaces, Symposium on Interactive 3D Graphics and Games (I3D 2005), pages 155 to 162"
    title: Fabio Policarpo, Manuel M. Oliveira and João L. D. Comba, Real-time relief mapping on arbitrary polygonal surfaces, I3D 2005
    locator: the linear search followed by a binary search (general locator)
  - paper: "Morgan McGuire and Max McGuire, Steep parallax mapping, poster at the 2005 Symposium on Interactive 3D Graphics and Games"
    title: Morgan McGuire and Max McGuire, Steep parallax mapping, I3D 2005 poster
    locator: the linear march without a refinement step (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 6.8, Parallax Mapping, from page 214
---

Parallax occlusion mapping makes a flat polygon look like a surface with real depth. For each pixel it walks along the view ray inside a depth map, in texture space, until the ray goes under the stored surface. Then it shades the pixel with the texture at that point. [Bump mapping](/bump-mapping/) and [normal mapping](/normal-mapping/) only change the normal, so the texture does not move with the view. [Parallax mapping](/parallax-mapping/) moves the texture coordinate by one offset from the depth at the start, which works for gentle relief only. This method searches for the first intersection of the ray with the height field, so steep relief shifts and hides itself correctly. [Displacement mapping](/displacement-mapping/) moves the geometry, which also fixes the silhouette, at the cost of many more triangles.

## In plain words

Imagine the polygon is a glass window, and behind the glass lies a bumpy landscape stored as a depth image. To color one pixel, follow your line of sight through the glass and into the landscape. Take small steps down along the line. At each step, look at the depth image right below you. As long as you are above the ground, keep going. At the first step that is under the ground, you have passed the surface, so step back a little to where the line crossed the ground, and use the color stored there.

Bumps near the front can then hide what is behind them, just as on a real rough wall.

## The problem

The work happens in tangent space, where the polygon is the plane $z = 0$ and the texture axes are $x$ and $y$. The inputs are the texture coordinate $uv_0$ of the pixel, the unit vector $v = (v_x, v_y, v_z)$ from the surface toward the viewer with $v_z > 0$, a depth map $m$ with values in $[0, 1]$ (0 is the top of the relief, at the polygon, and 1 is the bottom), a scale $s$ (the depth of the relief in texture units), and the number of steps $k$.

Going one unit of depth down along the ray moves the texture coordinate by $\Delta = -s (v_x, v_y)/v_z$, so at depth $r$ the ray is at $uv_0 + r \Delta$. The ray is under the surface when $f(r) = r - m(uv_0 + r \Delta) \ge 0$. The output is the texture coordinate of the first root $r^*$ of $f$ in $[0, 1]$. It exists because $f(0) \le 0 \le f(1)$.

## The algorithm

```pseudo id=main
POM(m, uv0, v, s, k)
L1  Δ ← -s (v_x, v_y) / v_z                 ▷ the shift per unit of depth
L2  r_prev ← 0; f_prev ← 0 - m(uv0)
L3  if f_prev ≥ 0 then return uv0           ▷ the top of the relief
L4  for i ← 1 to k do
L5      r ← i / k; f ← r - m(uv0 + r Δ)
L6      if f ≥ 0 then                       ▷ the first sample under the surface
L7          t ← f_prev / (f_prev - f)
L8          r̂ ← r_prev + t (r - r_prev); return uv0 + r̂ Δ
L9      (r_prev, f_prev) ← (r, f)
```

Lines L4 to L6 are a [ray march](/ray-marching/) with a fixed step. Lines L7 and L8 are one step of the [secant method](/secant-method/) between the last sample above the surface and the first sample below it. The pixel is then shaded with all its textures at the returned coordinate, usually with a normal map for the lighting.

## Example

Take $k = 4$, $uv_0 = (0.5, 0.5)$, $s = 0.1$ and a view with $v_x / v_z = -2$ and $v_y = 0$, so $\Delta = (0.2, 0)$. Let the depth map along this ray be $m = 0.3 + 0.6 r^2$, which holds for $m(u, v) = 0.3 + 15 (u - 0.5)^2$.

| step | $r$ | $m$ | $f = r - m$ | under the surface |
|---|---|---|---|---|
| L2 | 0 | 0.3 | $-0.3$ | no |
| 1 | 0.25 | 0.3375 | $-0.0875$ | no |
| 2 | 0.5 | 0.45 | $0.05$ | yes |

Line L7 gives $t = 0.0875 / 0.1375 = 7/11$, and line L8 gives $\hat r = 0.25 + 0.25 \cdot 7/11 = 9/22 \approx 0.4091$. The texture coordinate is $u = 0.5 + 0.2 \cdot 9/22 \approx 0.5818$. The true first hit solves $0.6 r^2 - r + 0.3 = 0$, which gives $r^* \approx 0.3924$, so the error is $0.017$, well inside one step of $0.25$. Plain parallax mapping uses the depth at the start, $r = 0.3$, which is off by $0.092$.

## Correctness

The proof file shows four facts. First, the loop always returns, with $f < 0$ at the previous sample and $f \ge 0$ at the current one, because $f(1) \ge 0$. Second, the secant step lands in that interval. Third, if the ray, once it enters the relief, stays inside for at least one step, then the first sample under the surface is the one just after $r^*$, so the result is within $1/k$ of the first hit. Fourth, if the depth map is planar along the ray, $f$ is affine and the secant step is exact. Without the condition of the third fact, the result is still within one step of some intersection, but maybe not of the first one.

## Complexity

One pixel takes at most $k + 1$ samples of the depth map and $O(k)$ time. If the ray meets the surface at the first sample, it takes $O(1)$. The memory is $O(1)$ per pixel. So $P$ pixels take $\Theta(P k)$ in the worst case. On a GPU the loop runs in the pixel shader, and the pixels of one group wait for the slowest one, so the worst case sets the cost.

## Properties

- **Within one step of the first hit, when the relief is not too thin.** This is proved. It needs the ray to stay under the surface for at least one step after it enters.
- **Exact for planar relief.** This is proved. The secant step solves an affine $f$.
- **Self-occlusion.** A high point in front hides a low point behind it, because the march stops at the first hit.
- **No silhouette.** The geometry does not change, so the edge of the polygon stays straight. Only [displacement mapping](/displacement-mapping/) or a clip of the pixels that leave the texture fixes this.
- **Depends on the depth convention.** Some engines store height (1 at the top), others depth. Flip $m$ to $1 - m$ when the map is a height map.

## Variants and improvements

- **No refinement.** McGuire and McGuire (2005) return the first sample under the surface without the secant step. The error is up to one step, and the result shows layers.
- **Binary search.** Relief mapping (Policarpo, Oliveira and Comba, 2005) refines the bracket with several steps of bisection in place of one secant step.
- **A step count from the angle.** The ray crosses more texels at a grazing angle. Engines often set $k$ between a minimum and a maximum by the angle between $v$ and the normal. The values are tuning.
- **Self-shadowing.** From the hit, march toward the light the same way. If any sample is above the ray, the point is in shadow. Tatarchuk (2006) derives an approximate soft shadow from the same samples.
- **Cone step mapping and distance fields.** A precomputed cone or distance per texel gives a safe step size, as in [sphere tracing](/sphere-tracing/), so the march can take large steps without missing thin features.
- **Mip level selection.** Use the gradients of $uv_0$ for all samples, so that the texture lookups in the loop pick the same mip level as the pixel.

## When to use it

Use it for walls, floors and rocks that the camera sees from close by, where normal mapping looks flat and real geometry costs too much. It suits relief that is shallow compared with the size of the polygon. Use [normal mapping](/normal-mapping/) for distant or very fine detail, [parallax mapping](/parallax-mapping/) when only one sample is affordable, and [displacement mapping](/displacement-mapping/) when the silhouette matters.

## Pitfalls

- **Thin features.** A wall thinner than one step can fall between two samples, and the ray passes through it. The code test shows a wall one texel wide that a march of 8 steps misses and a march of 512 steps finds. Raise $k$ at grazing angles.
- **Stair steps.** Without the secant step, or with too few steps, the result shows layers at grazing angles.
- **Grazing angles.** As $v_z \to 0$, $\Delta$ grows without a bound, and the march crosses many texels per step. Clamp $v_z$ or fade the effect out at grazing angles.
- **Gradient instructions in a loop.** Texture lookups with an implicit mip level inside a loop with a varying count can give wrong derivatives on a GPU. Use explicit gradients or an explicit level.
- **Wrong tangent frame.** The view vector must be in the same tangent frame as the texture axes. A mirrored or wrongly signed bitangent moves the relief the wrong way.
- **Depth and height mixed up.** If the map is a height map, the relief appears inverted.

## Implementations

## History

Kaneko and others introduced parallax mapping in 2001, with one offset per pixel, and Welsh added offset limiting in 2004. In 2004 Brawley and Tatarchuk described a march of the height map per pixel, which they traced in reverse from the eye, in ShaderX3. McGuire and McGuire showed the march without a refinement step in a 2005 poster, and Policarpo, Oliveira and Comba refined it with a binary search in relief mapping in the same year. Tatarchuk presented the dynamic version with approximate soft shadows at I3D 2006 and in a SIGGRAPH course that year, and the method became standard in game engines.

## References
