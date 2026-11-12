---
tag: TZFVTD
kind: technique
slug: ray-differentials
name: Ray differentials
aliases:
- ray footprints
area: graphics-and-signals/ray-tracing
level: advanced
summary: Carry with each ray the derivatives of its origin and direction with respect to the image coordinates, so that every hit knows the size and shape of the pixel's footprint for texture filtering.
prereqs: [primary-ray-generation, mipmap]
see_also: [anisotropic-filtering, texture-mapping, cone-tracing, beam-tracing, whitted-ray-tracing, snells-law, automatic-differentiation, supersampling-antialiasing]
sources:
  - paper: doi:10.1145/311535.311555
    title: Homan Igehy, Tracing ray differentials, SIGGRAPH 99, 1999, pages 179 to 186
    locator: the definition of the ray differential, the formulas for transfer, reflection and refraction, the initialization at the camera, and the use of the footprint for texture filtering
  - paper: doi:10.1145/964967.801126
    title: Lance Williams, Pyramidal parametrics, Computer Graphics 17(3) (SIGGRAPH 83), 1983, pages 1 to 11
    locator: the mipmap pyramid and the choice of its level from the size of the pixel's footprint in the texture
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, 2016
    locator: Section 10.1 (Sampling and Antialiasing, where ray differentials give the texture-space footprint of a camera ray)
  - paper: doi:10.1145/964965.808589
    title: John Amanatides, Ray tracing with cones, Computer Graphics 18(3) (SIGGRAPH 84), 1984, pages 129 to 135
    locator: the earlier footprint model, a cone around each ray whose radius grows with distance
---

A ray differential is the pair of derivatives $(\partial P/\partial x, \partial D/\partial x)$ of a ray's origin $P$ and unit direction $D$ with respect to an image coordinate $x$, and a second pair for $y$. A ray tracer computes them at the camera and updates them at each hit, with the chain rule applied to the formulas for transfer, reflection and refraction. At a hit point, the two vectors $\partial P/\partial x$ and $\partial P/\partial y$ span a small parallelogram on the surface, the first-order image of the pixel. Mapped into texture space, its size picks the level of a [mipmap](/mipmap/) and its shape steers [anisotropic filtering](/anisotropic-filtering/). Without this, a ray tracer that hits a texture far away or after a curved mirror samples one texel per ray and shows aliasing. Homan Igehy introduced ray differentials in 1999. The extra cost per ray is a few dozen multiplications for each of the two image directions.

## In plain words

A ray through the middle of a pixel stands for the whole pixel. Near the camera the pixel covers a small part of the floor, and far away it covers a large part. To choose how blurred a texture should look at the hit, the ray tracer must know how large that part is.

One way is to trace the neighboring rays too and measure how far apart their hits are. Ray differentials get the same answer without tracing them. Each ray carries two small arrows that say how its start point and its direction would move if you moved one pixel to the right or one pixel up. At each bounce, simple rules update the arrows. At the end, the arrows show how big the pixel looks on the surface.

## When it applies

- The renderer traces one ray or a few rays per pixel and needs a texture filter whose width matches the pixel, as in [Whitted ray tracing](/whitted-ray-tracing/).
- The path from the camera to the textured surface is a chain of smooth steps: transfer through space, specular reflection, refraction. Each step has a derivative.
- The surface has a normal that is differentiable along the hit point, so the normal's derivative is known. This holds for planes, spheres and smooth parametric surfaces, and for triangle meshes with interpolated normals.
- A first-order model is good enough: the footprint is a parallelogram, not the exact image of the pixel square.

It does not apply as such to diffuse or glossy bounces, where the outgoing direction is random and not a function of $x$.

## The template

**Conventions.** Directions are unit vectors and normals $N$ are unit vectors that face the incoming ray, $D \cdot N < 0$. We write $\partial$ for $\partial/\partial x$, and every formula is applied twice, once for $x$ and once for $y$. The pinhole camera sends the ray through pixel $(x, y)$ along $d = V + x R + y U$, where $R$ and $U$ are the steps of one pixel on the image plane and $V$ points to the image center.

```pseudo id=main
L1  at the camera: P ← eye, ∂P ← 0, D ← d/|d|,  ∂D ← ((d·d) R − (d·R) d) / (d·d)^(3/2)
L2  for each bounce: t ← INTERSECT(P, D); P' ← P + t D; N ← normal at P'   ▷ hole: the scene
L3      ∂t ← −((∂P + t ∂D) · N) / (D · N)
L4      ∂P' ← ∂P + t ∂D + ∂t D
L5      ∂N ← derivative of the normal along ∂P'      ▷ hole: the surface; ∂P'/r on a sphere of radius r
L6      reflection: D' ← D − 2(D·N) N,  ∂D' ← ∂D − 2[(D·N) ∂N + (∂D·N + D·∂N) N]
L7      refraction with ratio η: D' ← ηD − μN, μ ← η(D·N) − (D'·N), (D'·N) = −√(1 − η²(1 − (D·N)²)),
            ∂μ ← (η − η²(D·N)/(D'·N)) (∂D·N + D·∂N),  ∂D' ← η∂D − (μ ∂N + ∂μ N)
L8  at the textured hit: ∂(u,v) ← (texture Jacobian) · ∂P'; level ← log2(max(|∂(u,v)/∂x|, |∂(u,v)/∂y|) · texels)
```

**Why the formulas are right.** Line L1 is the derivative of $d/\lVert d\rVert$ with $\partial d = R$. Line L4 differentiates $P' = P + tD$, and line L3 comes from the plane of the hit: $(P' - Q) \cdot N = 0$ for a point $Q$ of the tangent plane, so to first order $\partial P' \cdot N = 0$, and solving for $\partial t$ gives line L3. Line L6 differentiates the mirror formula with the product rule, and line L7 differentiates Snell's law in the vector form of [Snell's law](/snells-law/). These are Igehy's formulas. They need only $D$, $N$, $t$ and $\partial N$, which a ray tracer has at each hit anyway.

**Cost.** Each of lines L3 to L7 is a constant number of dot products and vector sums, done twice. So a ray with differentials costs a constant factor more arithmetic per bounce, and it stores 12 more numbers: four 3-vectors. No extra rays are traced.

**Example.** The camera is at the origin, looking along $+z$, with a $90°$ field of view over 512 pixels, so $R = (1/256, 0, 0)$ and $U = (0, 1/256, 0)$. The floor is the plane $y = -1$ with texture coordinates $(u, v) = (x, z)$ and 64 texels per unit. Take the pixel column $x = 0$ and the row $k$ pixels below the center. The ray hits the floor at $z = 256/k$, and lines L1 to L4 give $\partial P/\partial x = (z/256, 0, 0)$ and $\partial P/\partial y = (0, 0, z^2/256)$.

| rows below center | hit $z$ | footprint in texels ($x$, $y$) | mipmap level |
|---|---|---|---|
| 256 | 1 | 0.25, 0.25 | 0 |
| 64 | 4 | 1, 4 | 2 |
| 16 | 16 | 4, 64 | 6 |
| 4 | 64 | 16, 1024 | 10 |

The footprint grows linearly with distance across the view and with the square of the distance along it, because the floor is seen at a grazing angle. The isotropic rule of line L8 takes the longer side. At 64 units it blurs the texture to 1024 texels in both directions, although the footprint is only 16 texels wide; this is the case for [anisotropic filtering](/anisotropic-filtering/).

Curvature matters after a bounce. A mirror sphere of radius 2 at $(0, 0, 6)$ reflects the ray of pixel $(0, -40)$ onto the floor $y = -3$. There the footprint is $(0.075, 0.120)$ units. A flat mirror in the tangent plane of the same hit point gives $(0.029, 0.039)$, smaller by factors of 2.6 and 3.1. A renderer that used the distance traveled alone, as for a flat mirror, would pick a texture level more than one step too sharp. The tests compare every differential with central differences of rays traced at $x \pm h$ and $y \pm h$, through planes, a mirror sphere and a glass sphere, and they agree to the accuracy of the difference quotient.

## Classic examples

- **Texture filtering on primary rays.** The footprint selects the mipmap level and, with the two vectors, the axis of an anisotropic filter. PBRT computes its texture lookups this way.
- **Textures seen in mirrors and through glass.** Reflection and refraction change the footprint. Curved mirrors spread it and lenses can shrink or grow it, which a footprint based on distance alone gets wrong.
- **Level of detail for geometry.** The footprint size picks a tessellation rate or a displacement level at the hit, so that far or blurred geometry gets coarse triangles.
- **Offsets for secondary rays.** The footprint gives a scale for the offset that moves a new ray off the surface.

## Variations

- **Cone tracing.** [Cone tracing](/cone-tracing/) keeps one number per ray, the spread angle, and grows a circular footprint with distance. It is cheaper but cannot show the stretching of a grazing view or the effect of curvature in two directions.
- **Beam tracing.** [Beam tracing](/beam-tracing/) carries exact polygonal beams instead of a first-order model, for polygonal scenes and mirror reflections.
- **Finite differences.** Trace a few extra rays per pixel and difference their hits. This needs no derivative of the normal but costs two or more rays per pixel and fails when neighbor rays hit different objects.
- **Automatic differentiation.** Run the tracer with dual numbers, as in [automatic differentiation](/automatic-differentiation/), to get the same derivatives without writing lines L3 to L7 by hand.
- **Path differentials.** For glossy and diffuse bounces, extend the model with derivatives with respect to the random numbers of the sampled directions, and treat the footprint as a spread rather than a function of $x$ alone.
- **Ray cones on GPUs.** Real-time ray tracers often keep a single cone width per ray and add a spread angle from the surface curvature at each hit, a cheaper form of the differential.

## Pitfalls

- **Mixed normalization.** Line L1 gives the derivative of the normalized direction. Pairing the unit $D$ with the derivative $R$ of the unnormalized $d$ gives a wrong $\partial D$. Transfer and reflection also work with an unnormalized direction if $D$ and $\partial D$ both come from $d$, but line L7 needs unit vectors.
- **Forgetting the normal's derivative.** With $\partial N = 0$ every surface acts like a flat mirror, and the footprint after a curved mirror is too small, by a factor of about three in the example.
- **Interpolated normals on triangles.** The derivative of a shading normal comes from the barycentric derivatives of the hit point; the geometric normal of a triangle has $\partial N = 0$ and gives a different footprint.
- **Silhouettes and grazing angles.** At $D \cdot N \to 0$, line L3 divides by a small number and the footprint becomes huge. Clamp the filter width. Near a silhouette the first-order model also breaks down, because neighbor rays miss the surface.
- **Total internal reflection.** In line L7 the square root is not real when $1 - \eta^2(1 - (D \cdot N)^2) < 0$. Follow the reflection formula then.
- **Isotropic filters on stretched footprints.** Taking the longer side, as in line L8, blurs the short side too much. Use both vectors with an anisotropic filter.
- **Trusting it after diffuse bounces.** The outgoing direction of a sampled diffuse bounce does not depend smoothly on the pixel, so the differential is meaningless there. Restart with a heuristic width.

## Exercises

1. Prove line L1: show that $\partial (d/\lVert d\rVert) = \bigl((d \cdot d) R - (d \cdot R) d\bigr)/(d \cdot d)^{3/2}$ for $\partial d = R$, and that it is perpendicular to $d$.
2. For the camera of the example and the plane $z = 10$ facing the camera, show that $\partial P/\partial x = (10/256, 0, 0)$ for every pixel, not only at the center.
3. Derive the floor footprint $\partial P/\partial y = (0, 0, z^2/256)$ of the example from $z = 256/k$.
4. Show that line L6 gives $\partial D' \cdot D' = 0$ when $\partial D \cdot D = 0$, so the reflected direction stays a unit vector to first order.
5. A sphere of radius $r$ is seen head-on, and the ray hits its center point. Show that the reflected spread angle is the incoming spread plus $2\lVert\partial P\rVert/r$ per pixel, to first order. Explain why a convex mirror always increases the footprint.

## References
