---
tag: HVPMNH
kind: technique
slug: deferred-shading
name: Deferred shading
aliases:
- deferred rendering
area: graphics-and-signals/real-time-rendering
level: core
summary: Draw the scene once to store the surface attributes of the visible surface at each pixel, then compute the lighting per pixel from these stored values, so each light is applied once per visible pixel.
prereqs: [g-buffer, z-buffer, graphics-pipeline]
see_also: [g-buffer, tiled-shading, clustered-shading, visibility-buffer, order-independent-transparency, multisample-antialiasing, phong-shading, physically-based-shading]
sources:
  - paper: "Michael Deering, Stephanie Winner, Bic Schediwy, Chris Duffy and Neil Hunt, The triangle processor and normal vector shader: a VLSI system for high performance graphics, SIGGRAPH 1988, 21-30"
    locator: the pipeline that resolves visibility first and then shades each pixel once from the stored normal
  - paper: doi:10.1145/97880.97901
    title: "Takafumi Saito and Tokiichiro Takahashi, Comprehensible rendering of 3-D shapes, SIGGRAPH 1990, Computer Graphics 24(4), 197-206"
    locator: the G-buffer and the image-space passes over it
  - paper: doi:10.1080/2151237X.2011.621761
    title: "Ola Olsson and Ulf Assarsson, Tiled shading, Journal of Graphics, GPU, and Game Tools 15(4), 235-251, 2011"
    locator: the review of deferred shading and its cost, and the tiled variants
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 20, Efficient Shading (deferred shading, its costs and its variants)
---

Deferred shading splits rendering into two passes. The geometry pass draws all opaque triangles with the depth test and writes, for each pixel, the attributes of the nearest surface into a [G-buffer](/g-buffer/): the normal, the base color, the roughness and so on. The lighting pass then visits each pixel once, reads these attributes and adds the light of every light that reaches it. The cost of lighting thus depends on the number of visible pixels and not on how many fragments were drawn on top of each other. Deering and his coauthors built the idea into hardware in 1988, and the name G-buffer is from Saito and Takahashi (1990). This page is the general technique. The G-buffer page covers the stored data, [tiled shading](/tiled-shading/) and [clustered shading](/clustered-shading/) cover the selection of lights per pixel, and the [visibility buffer](/visibility-buffer/) is a variant that stores less.

## In plain words

In plain forward rendering, every triangle is lit while it is drawn. When a later triangle covers it, that lighting work is thrown away. With many lights, most of the time goes into pixels that nobody sees. Deferred shading waits. First it draws everything, but only notes what each pixel shows: which way the surface faces, its color and how shiny it is. Once the picture is complete and only the nearest surface is left at every pixel, it computes the lighting from these notes. Each light is then applied only to pixels that are really on the screen. The price is the memory for the notes, and surfaces that are see-through do not fit, because each pixel has room for one surface only.

## When it applies

The technique fits when these conditions hold:

- **Many lights.** The lighting cost is large compared with the cost of drawing the geometry, so moving it out of the overdraw pays.
- **Opaque surfaces.** Each pixel shows one surface. Transparent surfaces need more than one surface per pixel and are drawn in a separate forward pass after the deferred pass, see [order-independent transparency](/order-independent-transparency/).
- **A shared shading model.** All materials read the same fields of the G-buffer. A scene with many very different shading models needs more fields or a material id per pixel.
- **Enough memory bandwidth.** The G-buffer is written once and read once per lighting pass, at $b$ bytes per pixel.

The cost model uses $p = W H$ pixels, $f$ fragments that pass the depth test during the geometry pass (with overdraw, $f$ can be several times $p$), $l$ lights and $b$ bytes of G-buffer per pixel. Forward shading of every light at every fragment costs $O(f l)$ light evaluations. Deferred shading costs $O(f)$ G-buffer writes of $b$ bytes and $O(p l)$ light evaluations without culling. With light culling per tile or cluster, the lighting cost drops to the number of (pixel, light) pairs that the culling keeps.

## The template

The camera looks along $-z$. The page stores the linear view depth $d > 0$ of each pixel (clip-space depth in OpenGL has the range $[-1, 1]$; the page uses no reversed z). The pixel $(i, j)$ has its center at $(i + 1/2, j + 1/2)$.

```pseudo id=main
DEFERRED-SHADING(triangles, lights)
L1  clear the G-buffer G and the depth buffer D to the background
L2  for each opaque triangle and each of its fragments at pixel q           ▷ geometry pass
L3      if the fragment depth < D[q] then D[q] ← depth;  G[q] ← the surface attributes
L4  for each pixel q with D[q] not the background                           ▷ lighting pass
L5      P ← the view-space position of the pixel center at depth D[q]
L6      c ← 0
L7      for each light j in LIGHTS(q)                                          ▷ all lights, or a culled list
L8          c ← c + SHADE(G[q], P, light j)
L9      out[q] ← c + the ambient and emissive terms of G[q]
L10 draw the transparent triangles in a forward pass, depth tested against D and blended over out
```

**The geometry pass (lines L1 to L3).** The fragment shader does no lighting. It evaluates the material (textures, normal maps) and writes the result. The depth test of the [z-buffer](/z-buffer/) keeps the nearest fragment, so after the pass $G[q]$ belongs to the visible surface. A depth-only pre-pass before line L2 can stop the material work for hidden fragments too.

**The position (line L5).** With an aspect ratio $a = W / H$ and a vertical field of view $2\theta$, the view-space position is $P = d\,(u, v, -1)$ with $u = (2(i + 1/2)/W - 1)\, a \tan\theta$ and $v = (2(j + 1/2)/H - 1) \tan\theta$. Storing the depth and computing $P$ saves the 12 bytes of a stored position.

**The light loop (lines L7 and L8).** LIGHTS$(q)$ decides the cost. The early form draws a bounding volume for each light (a sphere or a cone) and shades the pixels that it covers, so a pixel inside $k$ light volumes is read $k$ times from the G-buffer. [Tiled shading](/tiled-shading/) and [clustered shading](/clustered-shading/) build a list of lights per screen tile or per cluster, so each pixel reads the G-buffer once and loops only over its list. SHADE is any local shading model, for example [Phong shading](/phong-shading/) or a [microfacet BRDF](/microfacet-brdf/).

**Transparency (line L10).** The G-buffer has one surface per pixel, so transparent surfaces are drawn forward after the deferred pass, with their own lighting.

## Classic examples

- **Deering and coauthors (1988).** A hardware pipeline with a triangle processor that resolves visibility and a normal vector shader that then shades each pixel from its stored normal. This is the first form of the idea.
- **Saito and Takahashi (1990).** The G-buffer as stored per-pixel geometry, used for edges, contours and hatching rather than for many lights.
- **Light volumes.** Each point light draws a sphere and each spot light a cone. Pixels inside the volume are shaded with that light, and the results are added with additive blending. A stencil test can reject pixels in front of or behind the volume.
- **A worked count.** At 1920 by 1080 pixels, $p \approx 2.07$ million. With an overdraw of 3 ($f \approx 6.2$ million) and 100 lights that all reach every pixel, forward shading does about 622 million light evaluations and deferred shading 207 million. If culling leaves 8 lights per pixel on average, deferred shading does about 17 million. With a 16-byte G-buffer, the price is about 33 MB written and 33 MB read per frame. These numbers are an illustration of the cost model, not a measurement.

## Variations

- **Tiled deferred shading.** One compute pass reads the G-buffer, builds a light list per screen tile and shades each pixel with its list, see [tiled shading](/tiled-shading/).
- **Clustered deferred shading.** The same with clusters in view space, which handles tiles with a large depth range, see [clustered shading](/clustered-shading/).
- **Light pre-pass (deferred lighting).** A thin G-buffer of depth and normal, a pass that accumulates diffuse and specular light into a light buffer, and a second geometry pass that applies the materials. It needs less G-buffer memory and allows more material variety, at the cost of drawing the geometry twice.
- **Tiled forward shading.** The light lists of tiled shading used in a forward pass, which keeps MSAA and transparency simple. Harada, McKee and Yang (2012) published a renderer of this kind.
- **Visibility buffer.** Store only a triangle id and an instance id per pixel, and compute the attributes in the shading pass, see [visibility buffer](/visibility-buffer/).
- **Screen-space effects.** Once a G-buffer exists, passes such as [screen-space ambient occlusion](/screen-space-ambient-occlusion/) and [screen-space reflections](/screen-space-reflections/) read it at little extra cost.

## Pitfalls

- **Transparency.** The G-buffer holds one surface per pixel. Transparent surfaces need a separate forward pass with its own lights, or an order-independent method.
- **MSAA.** [Multisample antialiasing](/multisample-antialiasing/) needs one G-buffer record per sample, which multiplies the memory and bandwidth by the sample count, and the lighting pass must find the edge pixels and shade them per sample. Many engines use a post-process or temporal antialiasing instead.
- **Bandwidth.** At high resolution the G-buffer traffic can cost more than the lighting it saves. Pack the fields tightly, see [G-buffer](/g-buffer/).
- **Material variety.** Every material must fit the fields of the G-buffer and the one shading function. A material id per pixel allows a branch, which can cause [warp divergence](/warp-divergence/).
- **Light volumes that contain the camera.** When the camera is inside a light sphere, the front faces are behind the near plane. Draw the back faces with the depth test reversed in that case.
- **Position precision.** The position computed from a low-precision depth buffer can be off by more than the bias of later passes, which shows as shading noise on distant surfaces.

## Exercises

1. For a G-buffer of $b$ bytes per pixel at $W \times H$ pixels and 60 frames per second, compute the bandwidth of one write and one read per frame. Evaluate it for $b = 16$ at 3840 by 2160 pixels.
2. With light volumes, a pixel inside $k$ volumes reads its G-buffer record $k$ times. Show that tiled shading reads it once, and give the cost of both forms in terms of $p$, $b$ and the average $k$.
3. Explain why the result of lines L4 to L9 is the same as forward shading of the nearest fragment at each pixel, if SHADE uses only the stored attributes and their precision is exact. Then list what is lost when the attributes are quantized.
4. A scene has one transparent window in front of a lit room. Describe the passes needed to draw it with deferred shading for the room and forward shading for the window.

## References
