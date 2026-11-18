---
tag: BTYHAV
kind: technique
slug: environment-mapping
name: Environment mapping
aliases:
- "reflection mapping"
area: graphics-and-signals/real-time-rendering
level: intro
summary: Approximate reflections by looking up the reflected direction in a texture that stores the distant surroundings as a function of direction.
prereqs: [texture-mapping, cube-map]
see_also: [cube-map, image-based-lighting, irradiance-environment-map, split-sum-approximation, screen-space-reflections, fresnel-equations, snells-law, mipmap]
sources:
  - paper: doi:10.1145/360349.360353
    title: James F. Blinn and Martin E. Newell, Texture and reflection in computer generated images, Communications of the ACM 19(10), 1976, 542 to 547
    locator: the reflection of a surrounding environment stored as a map indexed by the angles of the reflected direction (general locator)
  - paper: doi:10.1109/MCG.1986.276658
    title: Ned Greene, Environment mapping and other applications of world projections, IEEE Computer Graphics and Applications 6(11), 1986, 21 to 29
    locator: the cube projection of the environment and the filtering of environment map lookups (general locator)
  - url: https://www.pauldebevec.com/ReflectionMapping/illumap.pdf
    title: Gene S. Miller and C. Robert Hoffman, Illumination and Reflection Maps, Simulated Objects in Simulated and Real Environments, SIGGRAPH 84 course notes, Advanced Computer Graphics Animation
    locator: reflection maps from photographs of real surroundings, maps convolved for diffuse and glossy reflection, and storage as six cube faces
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 10, Local Illumination (the parts on environment mapping and its projections)
---

Environment mapping draws a reflection without tracing rays. A texture stores what the surroundings look like in every direction, as seen from one point. To shade a shiny surface, the renderer computes the reflected view direction and reads the texture in that direction. The idea rests on one assumption: the surroundings are far away compared to the size of the object, so the reflected color depends only on the direction, not on the point of the surface. When the assumption holds, the cost is one reflection and one texture fetch per pixel. When it fails, reflections slide and are in the wrong place, and the object never reflects itself. Blinn and Newell introduced the idea in 1976. The same lookup with other directions gives refraction and the sky background, and with prefiltered textures it gives diffuse and glossy lighting, which is [image-based lighting](/image-based-lighting/). The usual storage is a [cube map](/cube-map/).

## In plain words

Look at a polished metal ball. You see a small, bent picture of the room in it. Each spot of the ball shows the part of the room in one direction, the direction a light ray bounces to from that spot. If the room is large compared to the ball, it does not matter where exactly on the ball the bounce happens, only in which direction the ray goes. So take one photo of the room in all directions, from the place of the ball. To color a spot of the ball, find the bounce direction and read the photo in that direction. This is fast. It is wrong for things that are close to the ball, and the ball cannot show its own parts in the reflection.

## When it applies

- The surface reflects or refracts its surroundings, and what it reflects is far compared to the size of the object, such as a sky, a distant landscape or a large room seen in a small object.
- An exact reflection is too expensive, or not needed: the error of a lookup by direction is acceptable because curved shiny surfaces distort the reflected picture anyway.
- The object does not need to reflect itself or nearby moving objects, or those can be handled by another method such as [screen-space reflections](/screen-space-reflections/).
- The surroundings change slowly, so the map can be made once, or rendered again only now and then.

## The template

```pseudo id=main
ENVIRONMENT-SHADE(p, n, eye, E)
L1  v ← normalize(eye - p)                        ▷ from the surface to the eye
L2  r ← 2 (n · v) n - v                           ▷ the mirror direction
L3  c ← LOOKUP(E, r)                               ▷ hole: the map and its projection
L4  k ← FRESNEL(n · v)                             ▷ hole: how much is reflected
L5  return k · c + (1 - k) · LOCAL-SHADE(p, n, v)  ▷ hole: the rest of the shading
```

**The view direction (line L1).** The vector $v$ points from the surface to the eye, with unit length.

**The reflection (line L2).** For a unit normal $n$, the mirror direction is $r = 2(n \cdot v)n - v$. It has unit length, makes the same angle with $n$ as $v$, and lies in the plane of $n$ and $v$; these are proved properties of the formula.

**The lookup (line L3).** The map $E$ stores radiance as a function of direction. The projection decides how a direction becomes texture coordinates: a [cube map](/cube-map/) divides by the largest component, a latitude and longitude map uses two angles, and a sphere map uses the image of a mirror ball. Only the direction $r$ is used, not the point $p$; this is where the distant environment assumption enters. The [mipmap](/mipmap/) level of the lookup should match the spread of the reflected rays across the pixel, which grows on curved surfaces.

**The weight (line L4).** A real surface reflects more at grazing angles, by the [Fresnel equations](/fresnel-equations/). Shaders use the [Schlick approximation](/schlick-fresnel-approximation/) $F_0 + (1 - F_0)(1 - n \cdot v)^5$.

**The mix (line L5).** The reflection is added to the diffuse or other local terms. For a metal, the local diffuse term is near zero and the reflection carries the color.

## Classic examples

- **Mirror reflection.** A chrome object in a cube map of its surroundings, the original use of Blinn and Newell. Lines L1 to L3 with $k$ close to 1.
- **Refraction.** Replace line L2 by the refracted direction from [Snell's law](/snells-law/), $\eta$ the ratio of the indices; glass and water use both, mixed by the Fresnel weight of line L4.
- **Sky background.** Look up the map with the view direction itself instead of $r$, to draw the background behind all geometry. This is the skybox.
- **Diffuse lighting.** Look up a map convolved with the clamped cosine, with the normal $n$ instead of $r$. The [irradiance environment map](/irradiance-environment-map/) does the same with nine numbers.
- **Glossy reflection.** Look up a map blurred by the lobe of a rough [microfacet BRDF](/microfacet-brdf/), with a mip level per roughness; the [split sum approximation](/split-sum-approximation/) is the standard form.

## Variations

- **Projections.** Latitude and longitude maps are easy to capture and paint but waste texels near the poles. Sphere maps store the image of a mirror ball and are valid only for one view direction. Cube maps are view independent and native to the hardware. Dual paraboloid and octahedral maps use one or two square textures.
- **Dynamic maps.** Render the six faces of a cube map from the center of the object each frame, or one face per frame, so that moving objects appear in the reflection.
- **Local corrections.** Intersect the reflected ray with a simple proxy of the room, such as a box, and look up the direction from the map center to that hit point. This fixes much of the parallax for interiors, at the cost of a ray and box intersection per pixel (a heuristic: correct only for walls that match the proxy).
- **Many probes.** Place several maps in a level and blend the nearest ones per pixel, as the reflection part of a probe system; the diffuse part is an [irradiance volume](/irradiance-volume/).
- **Prefiltered maps.** Store the map already blurred for each roughness, since a blur at run time would need many lookups per pixel.

## Pitfalls

- **Parallax.** Line L3 ignores $p$. For a reflected object at distance $D$ from the map center, seen from a point at distance $d$ from that center, the direction to it is off by up to about $d / D$ radians (a geometric bound for $d \ll D$). Floors and walls of a room reflect close geometry and show the error clearly. Use a local correction or [screen-space reflections](/screen-space-reflections/) for near content.
- **Wrong vector at line L2.** Using $v$ from the eye to the surface instead of from the surface to the eye gives exactly $-r$, a direction into the surface, so the lookup returns the wrong side of the world. GLSL `reflect(I, N)` expects the incident vector toward the surface and returns $I - 2(N \cdot I)N$, which equals $r$ for $I = -v$.
- **Unnormalized normal.** Line L2 needs a unit $n$. After interpolation the normal is shorter than 1, and $r$ bends toward $-v$.
- **Aliasing.** On bumpy or highly curved surfaces, neighboring pixels reflect very different directions. A lookup at the finest mip level at line L3 then flickers. Pick the level from the derivatives of $r$, or prefilter by roughness.
- **Gamma and range.** Store linear radiance with a high range. An 8-bit sRGB map clamps the sun and bright windows, so reflections of light sources look gray. Decode before filtering, see [gamma correction](/gamma-correction/).
- **Missing occlusion.** A map does not know that a part of the object hides the environment. Crevices reflect the sky. Multiply by a specular occlusion term, or accept the error.

## Exercises

1. For $n = (0, 0, 1)$ and $v = (1, 0, 1)/\sqrt 2$, compute $r$ and the cube map face it selects with the tie rule of the [cube map](/cube-map/) page. *Answer:* $n \cdot v = 1/\sqrt 2$, so $r = (0, 0, \sqrt 2) - v = (-1, 0, 1)/\sqrt 2$. The $x$ and $z$ components tie in absolute value, the tie rule picks $x$, and the sign gives face $-x$.
2. Show that $r = 2(n \cdot v)n - v$ has unit length when $n$ and $v$ do. *Answer:* $|r|^2 = 4(n \cdot v)^2 - 4(n \cdot v)^2 + |v|^2 = 1$.
3. A mirror ball of radius 0.1 m sits in a room whose walls are 3 m from it. What is the largest angular error of the reflection by the bound in the pitfalls, and how does it compare to a car body of 2 m in the same room? *Answer:* about $0.1/3 \approx 0.033$ rad, or 1.9 degrees, for the ball; for the car, points up to 1 m from the center give up to about $1/3$ rad, which is far too large, and the small angle bound itself no longer holds.

## References
