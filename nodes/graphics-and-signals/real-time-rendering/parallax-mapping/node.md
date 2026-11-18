---
tag: NCNT13
kind: technique
slug: parallax-mapping
name: Parallax mapping
aliases:
- offset mapping
area: graphics-and-signals/real-time-rendering
level: core
summary: Shift the texture coordinates along the view direction by the height read from a height map, to fake the parallax of surface relief.
prereqs: [normal-mapping, texture-mapping]
see_also: [parallax-occlusion-mapping, normal-mapping, bump-mapping, displacement-mapping, fixed-point-iteration, ray-marching, mipmap, bilinear-filtering]
sources:
  - paper: "Tomomichi Kaneko, Toshiyuki Takahei, Masahiko Inami, Naoki Kawakami, Yasuyuki Yanagida, Taro Maeda and Susumu Tachi, Detailed shape representation with parallax mapping, Proceedings of ICAT 2001, Tokyo, pages 205 to 208"
    title: Kaneko and others, Detailed shape representation with parallax mapping, ICAT 2001
    locator: the whole paper (the shift of the texture coordinate by the height and the view direction)
  - paper: "Terry Welsh, Parallax mapping with offset limiting: a per-pixel approximation of uneven surfaces, technical report, Infiscape Corporation, 2004"
    title: Terry Welsh, Parallax mapping with offset limiting, Infiscape, 2004
    locator: the offset without the division by the normal component of the view vector (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 6.8, Parallax Mapping, from page 214
---

Parallax mapping moves the texture coordinate of each pixel by an offset that depends on the view direction and on the depth stored in a height map. Points of the relief that lie deep then shift away from the viewer, as they would on a real rough surface, and the texture seems to have depth when the camera moves. [Bump mapping](/bump-mapping/) and [normal mapping](/normal-mapping/) change only the normal, so the texture stays fixed on the polygon. Parallax mapping applies one offset, computed from the depth at the starting point. That is cheap, but it is right only where the relief is smooth. [Parallax occlusion mapping](/parallax-occlusion-mapping/) marches the view ray through the height field to find the true intersection, and [displacement mapping](/displacement-mapping/) moves the geometry itself.

## In plain words

Look at a brick wall from the side. The mortar between the bricks lies deeper, so you see it a little behind and to the side of where it would be on a flat picture of the wall.

Parallax mapping fakes this. For each pixel, read how deep the surface is at that spot. Then slide the texture lookup a little along the direction you look in, by an amount that grows with the depth. Deep spots slide more and high spots slide less, so the picture shifts as the camera moves, like a real surface with depth.

It uses one read of the depth per pixel, so it is fast. It is only a guess, and it fails on steep or tall relief.

## When it applies

- The relief is shallow and smooth compared with the size of the texture: bricks with soft edges, cobblestones, bark, worn stone.
- The surface is seen from angles near the normal, not grazing.
- There is a normal map for the lighting, and a height or depth map in the same texture space. Often the depth is in the alpha channel of the normal map.
- The budget allows one more texture read per pixel, but not a loop.
- It does not apply when the relief is steep or tall, when it must hide itself, or at grazing angles. Use parallax occlusion mapping then.

## The template

The work happens in tangent space, as in normal mapping. The inputs are the texture coordinate $uv_0$ of the pixel, the unit vector $v$ from the surface toward the viewer in the tangent frame, with $v_z > 0$, a depth map $m$ with values in $[0, 1]$ (0 at the top, at the polygon), and a scale $s$, the depth of the relief in texture units.

1. Transform the view vector into the tangent frame with the matrix of normal mapping, $v = (v \cdot T, v \cdot B, v \cdot N)$.
2. Read the depth at the start, $d = m(uv_0)$.
3. Compute the offset. Kaneko and others use $uv' = uv_0 - s \, d \, (v_x, v_y)/v_z$, the point where a ray at depth $d$ would be.
4. Or, with Welsh's offset limiting, use $uv' = uv_0 - s \, d \, (v_x, v_y)$, which drops the division by $v_z$.
5. Read every texture of the material, including the normal map, at $uv'$, and shade the pixel as usual.

Step 3 is exact when the depth is the same, $d$, at every point between $uv_0$ and $uv'$, because the view ray then reaches depth $d$ exactly at $uv'$. This is a proved property. Where the depth changes along the ray, the error grows with the slope of the relief and with $1/v_z$. Step 4 keeps the offset at most $s \, d \le s$, because $|(v_x, v_y)| \le 1$. This is also proved, and it hides the worst errors at grazing angles, at the cost of less parallax there. The scale $s$, and an optional bias added to $d$, are tuning.

## Classic examples

**A trace.** Take $uv_0 = (0.5, 0.5)$, $s = 0.1$ and a view with $v_x / v_z = -2$ and $v_y = 0$, so $v = (-2, 0, 1)/\sqrt5$. Let the depth along the ray be $m = 0.3 + 0.6 r^2$ at depth $r$ of the ray, the example of [parallax occlusion mapping](/parallax-occlusion-mapping/). The true intersection is at $r^* \approx 0.392$, so the true point has $u \approx 0.5 + 0.2 \cdot 0.392 = 0.578$.

| method | depth used | $u$ |
|---|---|---|
| step 3, one offset | $d = 0.3$ | $0.5 + 0.2 \cdot 0.3 = 0.560$ |
| step 4, offset limiting | $d = 0.3$ | $0.5 + 0.0894 \cdot 0.3 = 0.527$ |
| iterative, 8 steps | $0.392$ | $0.578$ |
| march of POM | $0.409$ | $0.582$ |

The single offset gets about two thirds of the way to the true point. Offset limiting gets less, which is its purpose at grazing angles.

**Brick and stone walls.** The classic use is a wall with a normal map and a depth map in its alpha channel. The mortar lines shift as the camera moves, which a [normal map](/normal-mapping/) alone cannot do.

**Floors in games.** Cobblestone and tile floors use parallax mapping for distant surfaces, and switch to [parallax occlusion mapping](/parallax-occlusion-mapping/) near the camera, where the errors would show.

**Decals.** Footprints, bullet holes and cracks get depth from a small depth map at the cost of one read.

## Variations

- **Offset limiting.** Step 4, from Welsh (2004). The parallax is weaker at grazing angles, but the texture no longer swims away.
- **Iterative parallax mapping.** Repeat steps 2 and 3 with the depth at the last offset: $r_{k+1} = m(uv_0 + r_k \Delta)$ with $\Delta = -s (v_x, v_y)/v_z$. This is a [fixed-point iteration](/fixed-point-iteration/) for the intersection depth $r^* = m(uv_0 + r^* \Delta)$. It converges when the map $r \mapsto m(uv_0 + r \Delta)$ has a slope of absolute value below 1 near $r^*$, by the contraction argument. In the trace the slope is $1.2 r^* \approx 0.47$, and the iteration goes $0.354$, $0.375$, $0.385$, and so on to $0.392$.
- **Slope-based offset.** Some versions also use the normal from the normal map to tilt the offset, which follows the local slope of the relief.
- **Parallax occlusion mapping.** Replace the single read by a march along the ray. See [parallax occlusion mapping](/parallax-occlusion-mapping/).

## Pitfalls

- **Swimming at grazing angles.** As $v_z \to 0$ the offset of step 3 grows without a bound, and the texture slides across the surface. Use offset limiting, clamp $v_z$, or fade the effect out.
- **Steep edges.** At the edge of a brick the depth jumps, so the offset jumps too, and the texture tears or doubles along the edge.
- **No occlusion.** A high point never hides a deep point behind it. Tall relief looks warped instead of solid.
- **Depth and height mixed up.** If the map stores height (1 at the top), use $1 - h$ as the depth. The wrong sign moves the deep parts toward the viewer.
- **Wrong tangent frame.** The view vector must be in the same frame as the texture axes, as for normal maps. A wrong sign of the bitangent moves the relief the wrong way.
- **Mip level of the shifted read.** The shift happens in the pixel shader, so the derivatives of $uv'$ include the derivatives of the offset. Use the derivatives of $uv_0$ for the reads at $uv'$ to avoid seams.

## Exercises

1. Show that step 3 gives the exact intersection when $m$ is constant along the ray.
2. For a depth map that is a plane, $m = a + b \, r$ along the ray with $0 \le b < 1$, find the true intersection and the error of step 3 as a function of $b$.
3. Show that the offset of step 4 is at most $s$, and compare it with the offset of step 3 for $v_z = 0.1$.
4. Run the iterative version on $m = 0.3 + 0.6 r^2$ and count the steps until the error is below $0.001$. Compare with the bound from the contraction factor $0.47$.
5. Explain why parallax mapping needs the normal map to be read at $uv'$ and not at $uv_0$.

## References
