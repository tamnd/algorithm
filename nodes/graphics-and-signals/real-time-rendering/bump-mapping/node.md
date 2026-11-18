---
tag: 2SWA67
kind: technique
slug: bump-mapping
name: Bump mapping
aliases:
- Blinn bump mapping
area: graphics-and-signals/real-time-rendering
level: intro
summary: Perturb the shading normal by the gradient of a height texture, so that a flat surface looks wrinkled without changing its geometry.
prereqs: [texture-mapping]
see_also: [normal-mapping, parallax-mapping, displacement-mapping, perlin-noise, fractal-noise, blinn-phong-reflection-model, finite-differences, cross-product]
sources:
  - paper: doi:10.1145/965139.507101
    title: James F. Blinn, Simulation of wrinkled surfaces, SIGGRAPH 1978
    locator: the perturbed normal from the partial derivatives of a bump function along the two surface tangents (general locator)
  - paper: doi:10.1145/258734.258873
    title: Mark Peercy, John Airey and Brian Cabral, Efficient bump mapping hardware, SIGGRAPH 1997
    locator: the perturbation in a tangent frame per vertex, interpolated over the triangle (general locator)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 9.3, Bump Mapping
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 6.7, Bump Mapping, from page 208
---

Bump mapping makes a smooth surface look rough by changing only the normal that the lighting uses. A scalar height texture $h(u, v)$ describes small bumps, and the method tilts the normal by the slope of $h$ at each point, as if the surface had moved by $h$ along its normal. The geometry and the texture coordinates do not change. [Normal mapping](/normal-mapping/) stores the tilted normal itself in a texture in place of computing it from a height. [Parallax mapping](/parallax-mapping/) and [parallax occlusion mapping](/parallax-occlusion-mapping/) also move the texture coordinate by the view, so the bumps seem to shift. [Displacement mapping](/displacement-mapping/) moves the geometry, which also changes the silhouette and the shadows.

## In plain words

Light makes a bump visible mainly through shading: the side of the bump that faces the light is bright and the other side is dark. The eye reads this pattern of light and dark as shape.

So keep the surface flat, but at each point tell the lighting that the surface is tilted. The tilt comes from a gray image of heights: where the heights rise to the right, tilt the surface to the left, and so on. Steeper slopes give stronger tilts.

The result looks bumpy from the front. It still looks flat at the edges of the object, because the outline does not change, and the bumps never hide each other.

## When it applies

- The detail is small compared with the object: pores, scratches, orange peel, cloth weave, ripples, hammered metal.
- The view is not at a grazing angle, and the outline of the object does not need to show the detail.
- A height texture is at hand, or a procedural height such as [Perlin noise](/perlin-noise/) or [fractal noise](/fractal-noise/) whose derivative can be computed.
- The lighting uses the normal, as in [Blinn-Phong](/blinn-phong-reflection-model/) or a physically based model.
- It does not apply when the relief must hide parts of itself, cast shadows on itself or change the outline. Use the parallax methods or displacement mapping then.

## The template

The inputs are a surface point $P(u, v)$ with the tangents $P_u = \partial P/\partial u$ and $P_v = \partial P/\partial v$, the normal $N = P_u \times P_v$, the unit normal $n = N/|N|$, and a height $h(u, v)$ with a scale $s$.

1. Read the slopes of the height, $h_u$ and $h_v$. For a texture, use central [finite differences](/finite-differences/) one texel apart, $h_u \approx (h(u + \Delta, v) - h(u - \Delta, v))/(2 \Delta)$, or the derivatives of a filtered lookup. For a procedural height, use its analytic gradient.
2. Think of the displaced surface $P' = P + s h n$. Its tangents are $P'_u = P_u + s h_u n + s h n_u$ and the same for $v$.
3. Drop the terms $s h n_u$ and $s h n_v$, which are small when $s h$ is small compared with the radius of curvature of the surface.
4. Take the [cross product](/cross-product/) of the two tangents. This gives Blinn's perturbed normal $N' = N + s \big(h_u (n \times P_v) - h_v (n \times P_u)\big)$, since $n \times n = 0$ and the term in $h_u h_v$ vanishes.
5. Normalize $N'$ and use it in place of $n$ in the lighting of the pixel.
6. In a tangent frame with unit tangents $T = P_u$ and $B = P_v$ that are orthogonal, step 4 becomes $N' = n - s h_u T - s h_v B$, the vector $(-s h_u, -s h_v, 1)$ in the coordinates $(T, B, n)$.

Steps 2 to 4 are exact except for the dropped terms, so on a flat base, where $n_u = n_v = 0$, the normal of step 4 is the exact normal of the displaced surface. This is a proved property. On a curved base it is an approximation. The scale $s$ and the texel step $\Delta$ are tuning.

## Classic examples

**A trace.** On the plane $z = 0$ with $T = (1, 0, 0)$, $B = (0, 1, 0)$ and $n = (0, 0, 1)$, let the height be $h = 0.1 \sin(2 \pi u)$, with $s = 1$, and let the light come from the unit direction $l = (0.6, 0, 0.8)$. Then $h_u = 0.2 \pi \cos(2 \pi u)$ and $h_v = 0$.

| $u$ | $h_u$ | normal after step 5 | $n' \cdot l$ |
|---|---|---|---|
| any, flat surface | | $(0, 0, 1)$ | $0.800$ |
| 0 | $0.628$ | $(-0.532, 0, 0.847)$ | $0.358$ |
| 0.25 | 0 | $(0, 0, 1)$ | $0.800$ |
| 0.5 | $-0.628$ | $(0.532, 0, 0.847)$ | $0.997$ |

The slope that faces away from the light is dark, the slope that faces it is bright, and the tops and the bottoms keep the flat shading. These are the stripes of light and shade that read as ridges.

**Procedural surfaces.** Perlin added the gradient of [Perlin noise](/perlin-noise/) to the normal in 1985, for bumpy surfaces and water waves. A sum of octaves of [fractal noise](/fractal-noise/) gives rough stone, and $F_2 - F_1$ of [Worley noise](/worley-noise/) gives cracked tiles, both with analytic or numeric slopes.

**Normal map baking.** The normal of step 6 can be computed once per texel and stored. This is how a height map becomes a [normal map](/normal-mapping/), and it is a common step in texture tools.

**Ripples on water.** An animated sum of a few sine waves in $h$ gives moving highlights on a flat water plane with no extra geometry.

## Variations

- **Tangent space bump mapping.** Peercy, Airey and Cabral (1997) moved the computation into a tangent frame per vertex, interpolated over the triangle, which made it practical in hardware.
- **Bump mapping without a tangent frame.** A pixel shader can take screen-space derivatives of the position and of the height, and build the perturbation from them. This needs no stored tangents, but the derivatives are coarse, per block of 2 by 2 pixels.
- **Normal mapping.** Store the result of step 6 in place of the height. This trades memory for fewer texture reads and avoids the finite differences.
- **Parallax mapping.** Also shift the texture coordinate by the view direction and the height. See [parallax mapping](/parallax-mapping/).
- **Bump to displacement.** For close views, move the vertices with the same height, as in [displacement mapping](/displacement-mapping/), and keep the bump for the detail finer than the mesh.

## Pitfalls

- **Flat at the outline.** The silhouette stays smooth, and at grazing angles the shading shows bumps that the outline denies.
- **No self-occlusion and no self-shadowing.** Bumps never hide or shadow each other, so deep relief looks painted.
- **Sign and handedness.** If the texture's $v$ axis runs the other way from $B$, or the mesh is mirrored, the bumps look inverted. Check with a light from one side.
- **Scale of the slopes.** The slopes depend on the texture scale: the same height map on a smaller area has steeper slopes. Make $s$ depend on the world size of a texel, or the strength changes with the tiling.
- **Aliasing.** Fine bumps far away alias into sparkles, because the normal varies faster than the pixel grid. Mipmapping the height smooths the slopes, but it also removes the roughness. See [aliasing](/aliasing/).
- **Shading normal facing away.** A strong perturbation can tilt the normal away from the viewer or below the surface, which gives black spots or light leaks. Clamp the tilt or the scale.

## Exercises

1. Derive the formula of step 4 from steps 2 and 3, and show that it reduces to the formula of step 6 on a plane with an orthonormal tangent frame.
2. For $h = a \sin(2 \pi u / L)$ on a plane, find the largest tilt angle of the normal as a function of $a / L$.
3. Show that scaling $u$ by a factor $c$ (the texture repeats $c$ times more often) scales $h_u$ by $c$. What must happen to $s$ to keep the look?
4. Compute the normal from a central difference on a height texture with values $0.2$, $0.5$ and $0.9$ at $u - \Delta$, $u$ and $u + \Delta$, with $\Delta = 1/256$ and $s = 0.01$.
5. Explain why the dropped term $s h n_u$ matters on a sphere of radius $R$ when $s h$ is close to $R$, and what shape the true displaced surface has then.

## References
