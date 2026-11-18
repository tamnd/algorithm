---
tag: PZ1RGX
kind: technique
slug: toon-shading
name: Toon shading
aliases:
- cel shading
area: graphics-and-signals/real-time-rendering
level: intro
summary: "Quantize the diffuse term to a few flat bands through a one-dimensional ramp texture and draw dark silhouettes, to look like hand-drawn cartoons."
prereqs: [lambertian-reflectance, silhouette-edge]
see_also: [gooch-shading, blinn-phong-reflection-model, edge-detection, sobel-operator, color-quantization, texture-mapping, gouraud-shading, phong-shading]
sources:
  - paper: doi:10.1145/340916.340918
    title: Adam Lake, Carl Marshall, Mark Harris and Marc Blackstein, Stylized rendering techniques for scalable real-time 3D animation, Proceedings of the 1st International Symposium on Non-Photorealistic Animation and Rendering (NPAR 2000), 2000, 13 to 20
    locator: the hard shading of cartoons with a one-dimensional texture indexed by the diffuse cosine, and the drawing of silhouette and crease edges (general locator)
  - paper: "Philippe Decaudin, Cartoon-looking rendering of 3D-scenes, INRIA research report 2919, 1996"
    locator: the cartoon look from flat shading bands and dark outlines (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: the chapter on non-photorealistic rendering, toon shading and outline methods (general locator)
---

Toon shading, also called cel shading, makes a 3D model look like a frame of a hand-drawn cartoon. Cartoon painters fill each region with a few flat colors, one for the lit part and one or two darker ones for the parts in shadow, and outline the figure with a dark line. Toon shading does the same in a renderer. It computes the [Lambertian](/lambertian-reflectance/) cosine $x = \max(0, n \cdot l)$ at each point, replaces it by the color of the band that $x$ falls in, and draws the [silhouette edges](/silhouette-edge/) in black. The band lookup is usually a one-dimensional texture with nearest filtering, the "ramp", so an artist can paint the bands, and the cost is one texture fetch per pixel. Decaudin (1996) and Lake, Marshall, Harris and Blackstein (2000) are early descriptions of the method.

## In plain words

A cartoon does not show smooth shading. A face is one color where the light hits it and a darker color where it does not, with a sharp line between the two, and a black line around the outside. Toon shading copies this. For each point the renderer first works out how much the surface faces the light, as ordinary shading does. Then, instead of using that amount directly, it rounds it to one of a few steps, for example "lit" or "in shadow", and paints the color of that step. A small strip of colors, painted by an artist, says which color goes with each step. Last, the renderer finds the outline of the object, where the surface turns away from the viewer, and draws it in black. The result is flat areas with crisp edges.

## When it applies

- A stylized look is the goal: cartoons, comics, games with a hand-drawn style, technical or children's illustrations.
- The mesh has smooth vertex normals, so the band edges are smooth curves. On flat-shaded meshes each face gets one band and the edges follow the polygons.
- One main light, or a main light that decides the bands while other lights add little. Many lights with their own bands give cluttered patterns.
- It is not a [physically based](/physically-based-shading/) model and makes no energy claim. Use a smooth model where the brightness must match a real material.

## The template

The inputs are the unit normal $n$, the unit vector $l$ toward the light, the unit vector $v$ toward the viewer, $k$ band colors $C[0..k-1]$ from dark to light, the band edges $0 < T[1] < \dots < T[k-1] \le 1$, and an optional highlight with exponent $p$ and threshold $\tau$.

```pseudo id=main
TOON-SHADE(n, l, v, C, T, p, τ)
L1  x ← max(0, n·l)                         ▷ the Lambertian cosine
L2  i ← 0
L3  for j ← 1 to k - 1 do                   ▷ T is increasing
L4      if x ≥ T[j] then i ← j
L5  c ← C[i]                                ▷ one flat color per band
L6  h ← normalize(l + v)
L7  if (n·h)^p ≥ τ then c ← white           ▷ optional hard highlight
L8  return c

OUTLINE(mesh, eye)
L9  for each edge e with adjacent faces f1, f2 do
L10     v ← eye - (a point of e)
L11     if (n1·v)(n2·v) ≤ 0 then draw e in black   ▷ a silhouette edge
```

Lines L2 to L5 find the largest $j$ with $x \ge T[j]$, or 0 if there is none, so the color is constant on each interval $[T[j], T[j+1])$ of $x$. With equal bands, $T[j] = j / k$, this is $i = \min(k - 1, \lfloor k x \rfloor)$, which is the texel that a ramp texture of width $k$ returns with nearest filtering and clamped addressing at the coordinate $x$. In a shader, L1 to L5 is one dot product and one texture fetch, so the cost per pixel is $O(1)$; with explicit thresholds it is $O(k)$, or $O(\log k)$ by binary search. Line L7 is the same idea for the specular term: the Blinn lobe of the [Blinn-Phong model](/blinn-phong-reflection-model/) is cut to a flat white spot.

Lines L9 to L11 mark an edge as a silhouette when one adjacent face faces the viewer and the other faces away, which is the test of the [silhouette edge](/silhouette-edge/) page. Done by brute force, it costs $O(E)$ per frame for $E$ edges.

## Classic examples

**Two tones.** $k = 2$, $C = (\text{shadow color}, \text{lit color})$, $T[1] = 0.5$. The band edge is where $n \cdot l = 0.5$, the curve where the normal is 60° from the light. On a sphere lit from the viewer the lit band is the central disk of the image with radius $\sin 60° \approx 0.866$ times the radius of the sphere, so it covers $1 - 0.5^2 = 75$ percent of the image of the sphere.

**Three equal bands.** $k = 3$, $T = (1/3, 2/3)$. On the same sphere the band edges are circles of radius $\sqrt{1 - T^2}$, that is $0.943$ and $0.745$. The image of the sphere is then 11 percent darkest band, 33 percent middle band and 56 percent lightest band. All of the darkest band is in a thin ring at the rim, because $x$ changes fastest near the silhouette.

**A trace.** With $C = (0.2, 0.5, 0.9)$ in gray, $T = (1/3, 2/3)$ and no highlight:

| $n \cdot l$ | $x$ | band $i$ | color |
|---|---|---|---|
| -0.4 | 0 | 0 | 0.2 |
| 0.30 | 0.30 | 0 | 0.2 |
| 0.34 | 0.34 | 1 | 0.5 |
| 0.66 | 0.66 | 1 | 0.5 |
| 0.70 | 0.70 | 2 | 0.9 |
| 1 | 1 | 2 | 0.9 |

Points with very different cosines, 0.34 and 0.66, get the same color, and points with almost the same cosine, 0.30 and 0.34, get colors far apart. That is the intended cartoon look, and it is also the cause of the aliasing in the pitfalls below.

**The ramp of Lake et al.** Lake et al. (2000) compute the cosine per vertex, use it as the coordinate of a one-dimensional texture with a few flat colors, and let the texture unit do the lookup.

## Variations

- **Painted ramps.** A ramp texture of more than $k$ texels with soft or colored steps lets the artist paint the transition, for example a warm lit color and a cool shadow color, as in [Gooch shading](/gooch-shading/) but with hard steps.
- **Smoothed edges.** Replacing the step at $T[j]$ by a short linear or smooth ramp over a width of about one pixel in $x$ (measured with screen-space derivatives) removes the stair steps at band edges. This is a heuristic.
- **Shadows as a band.** Points in a cast shadow are given the darkest band, so shadows and shading share the same flat colors.
- **Outline methods.** Edge tests as in L9 to L11 on the mesh; drawing the back faces of a slightly enlarged copy of the mesh in black behind the model; or [edge detection](/edge-detection/), for example with the [Sobel operator](/sobel-operator/), on the depth and normal images after rendering. Crease edges, where the angle between two faces is above a threshold, are often drawn too.
- **Rim bands.** A band on $1 - n \cdot v$ instead of $n \cdot l$ draws a bright or dark rim along the outline.

## Pitfalls

- **Linear filtering of the ramp.** With linear filtering the texture unit blends neighboring texels, so a ramp of $k$ texels gives smooth gradients between band centers instead of flat bands. Use nearest filtering and no mipmaps for the ramp.
- **Wrap addressing.** At $x = 1$ a ramp with repeat addressing samples coordinate 1, which wraps to texel 0, the darkest color, so the points that face the light directly turn dark. Clamp the address to the edge.
- **Aliasing at band edges.** A step function of $x$ has an infinite frequency at the edge, so the edge shows stair steps and crawls in animation. Multisampling or the smoothed edges above reduce it.
- **Interpolated normals.** The band edges follow the normals, not the geometry. Normals that are too smooth across a sharp corner move the edge away from the corner, and normals that are not normalized after interpolation give a wrong $x$.
- **Unwanted bands from noise.** A normal map or noisy normals make small islands of the next band. Toon shading magnifies small changes of $x$ near a threshold.
- **Thresholds are tuning.** The number of bands, the thresholds and the colors are chosen by eye for each style; there is no correct value.

## Exercises

1. Show that for a sphere lit from the viewer and a threshold $T$, the band $x \ge T$ covers a fraction $1 - T^2$ of the image of the sphere, and use it to choose two thresholds that give three bands of equal image area.
2. Write the ramp lookup $i = \min(k - 1, \lfloor k x \rfloor)$ as the texel index of a nearest-filtered texture with clamped addressing, and find the coordinate at which repeat addressing gives a wrong band.
3. Replace the step at $T[1] = 0.5$ by a linear ramp over $[0.5 - w, 0.5 + w]$. For a sphere of radius 100 pixels lit from the viewer, find $w$ so that the transition is about one pixel wide in the image.
4. For an orthographic view (one $v$ for all edges) and a closed manifold mesh with no face exactly edge-on, show that every vertex lies on an even number of the edges that L11 marks. Give a mesh where L11 marks an edge that is hidden by another part of the mesh.
5. Combine the bands with a Blinn-Phong highlight cut at $\tau$. For a sphere lit from the viewer, find $\tau$ as a function of $p$ so that the white spot has a radius of 0.1 times the radius of the sphere, and explain why only $\tau^{1/p}$ matters.

## References
