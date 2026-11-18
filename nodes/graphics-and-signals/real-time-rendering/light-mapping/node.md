---
tag: N0YP0P
kind: technique
slug: light-mapping
name: Light mapping
aliases:
- lightmapping
- baked lightmaps
area: graphics-and-signals/real-time-rendering
level: intro
summary: Precompute the lighting of static surfaces into a second texture with a unique parameterization and modulate the surface texture by it at run time.
prereqs: [texture-mapping, radiosity]
see_also: [irradiance-volume, precomputed-radiance-transfer, mesh-parameterization, rectangle-packing, path-tracing, ambient-occlusion, bilinear-filtering, global-illumination]
sources:
  - book: isbn:9781576101742
    title: Michael Abrash, Michael Abrash's Graphics Programming Black Book, Special Edition, The Coriolis Group, 1997
    locator: Chapter 68, Quake's Lighting Model (light maps sampled on a grid of one value per 16 texels, and surface caching that combines them with the textures)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 11, Global Illumination (the part on precomputed lighting stored in textures)
---

Light mapping stores the lighting of static surfaces in a texture, computed once before the program runs. Every static surface gets a second set of texture coordinates in which no two points of the scene share a texel, and the light map holds, at each texel, the light that arrives at that point of the surface. The light comes from an offline renderer, such as [radiosity](/radiosity/) or [path tracing](/path-tracing/), so it can include soft shadows, bounced light and the color of nearby walls, at no cost at run time. At run time the shader reads the light map with the second coordinates and multiplies it by the surface color from the ordinary texture. The light map can be coarse, because light usually changes slowly over a surface, while the surface texture keeps its fine detail and can repeat. Quake (1996) used light maps for all its static surfaces. Light maps cannot light moving objects, and they are wrong when the lights or the geometry change; [irradiance volumes](/irradiance-volume/) cover the moving objects.

## In plain words

Imagine painting the light and shadow of a room onto its walls, floor and ceiling, once, with great care, using a slow but good method. Every spot of every surface gets its own spot in a big picture of light, so nothing overlaps. While the game runs, it just reads that picture and darkens or brightens the color of each surface by it. The light can be as soft and rich as you like, because it was worked out ahead of time. The pattern of bricks or wood still comes from its own texture, which can be much sharper than the light picture. The cost is memory and a long bake, and nothing that moves can use it.

## When it applies

- The geometry and the main lights are static, or change in a few known ways that can each be baked.
- Global illumination effects such as bounced light, soft shadows from large lights and ambient occlusion are wanted, and computing them at run time is too expensive.
- Memory for one more texture per static surface is available.
- The surfaces can be given a unique parameterization: a set of charts in a second texture space without overlaps, see [mesh parameterization](/mesh-parameterization/).

## The template

1. **Unwrap.** Give each static surface a chart in a second texture coordinate set, with no overlaps and with a texel size in world units that is about the same everywhere.
2. **Pack.** Place the charts in one or a few textures, with gaps between them, a [rectangle packing](/rectangle-packing/) problem.
3. **Bake.** For each texel, find its point and normal on the surface, and compute the light there with a global illumination renderer.
4. **Fix the borders.** Copy texel values into the gaps around each chart, so that filtering near chart borders does not read empty texels, and remove noise.
5. **Shade.** At run time, read the light map with the second coordinates, and multiply by the surface color.

```pseudo id=main
LIGHT-MAP(scene)
L1  offline: for each static surface, a chart in a second UV set, without overlaps, with padding   ▷ hole: unwrapping and packing
L2  offline: for each texel t:  (x_t, n_t) ← the surface point and normal at the texel center
L3  offline:     E[t] ← the irradiance at x_t for the normal n_t   ▷ hole: the renderer, N rays per texel
L4  offline: dilate E into the padding;  denoise
L5  run time: c ← albedo(uv) · E(uv2) / π                          ▷ bilinear filtering of E
L6  run time: add the dynamic lights and the specular terms
```

**The charts (line L1).** The second coordinates must be one to one on the static scene, or two surfaces would share light. The padding between charts must be at least the radius of the texture filter, and more if the light map has mip levels.

**The texel points (line L2).** Each texel center maps back to a point on a triangle of its chart, found by rasterizing the triangles in the space of the light map. Texels that cover a chart border have their center outside the triangle, and need a nearby point inside it.

**The light (line L3).** For a [Lambertian](/lambertian-reflectance/) surface the light map stores irradiance, and the outgoing radiance is $\rho E / \pi$, with the albedo $\rho$ from the surface texture. Storing irradiance instead of the final color lets the albedo keep its own, finer resolution. Any [global illumination](/global-illumination/) method can fill the texels; [final gathering](/final-gathering/) or [irradiance caching](/irradiance-caching/) speed up the bake.

**The borders (line L4).** Dilation copies each border texel into the empty texels around it. Bilinear filtering at line L5 then reads valid values. Denoising is needed when line L3 used few rays.

**Run time (lines L5 and L6).** One more texture read and one multiplication per pixel. Dynamic lights and specular reflections, which depend on the view, are added on top.

## Classic examples

- **Quake.** Abrash describes how Quake stored the light of each surface in a light map with one value on a grid of 16 texels of the surface texture, and how surface caching lit each texel of the tiled texture with bilinear weights of the four nearest light map values, in software. Dynamic lights changed the light map and rebuilt the cached surface. Quake 2 baked its light maps with [radiosity](/radiosity/).
- **Ambient occlusion maps.** Store only the [ambient occlusion](/ambient-occlusion/) of each texel and multiply any lighting by it, a light map of visibility.
- **Relightable maps.** Store [precomputed radiance transfer](/precomputed-radiance-transfer/) vectors per texel instead of light, so that the sky can change after the bake.
- **Probes for moving objects.** Bake an [irradiance volume](/irradiance-volume/) in the same pass, so that moving objects match the light maps of the static scene.

## Variations

- **Directional light maps.** Store, per texel, the light from a few basis directions, or a dominant direction and its color, or a few [spherical harmonic](/spherical-harmonic-lighting/) coefficients. Normal maps can then change the shading within a texel.
- **High range formats.** Store the light in a format with a large range, such as half floats, a shared exponent, or a color times a scale, since the sun and dark corners differ by orders of magnitude.
- **Shadow masks.** Store only the visibility of a few main lights per texel, and compute their light at run time, so that their color and brightness can change.
- **Many light states.** Bake one map per state of a switchable light and add the maps of the lights that are on.
- **GPU baking.** Bake with GPU ray tracing in minutes instead of hours, which makes iteration on lighting practical.

## Pitfalls

- **Seams at line L1.** Two sides of a cut in the unwrap are far apart in the light map, so their texels get slightly different values and the cut shows as a line. Bake both sides with the same samples, or blend them after the bake.
- **Light leaks at line L2.** A texel whose center lies inside a wall or below the floor sees no light, and darkens the texels around it; a texel that reaches past a corner gets light from the other side. Move such sample points to a point of the surface that is not in solid geometry.
- **Too little padding at line L4.** With too few texels between charts, bilinear filtering and mipmapping at line L5 mix the light of unrelated charts. Pad by at least the filter radius at the coarsest mip level used.
- **Noise at line L3.** Few rays per texel give speckles that look like dirt. Use more rays, a denoiser, or irradiance caching, and check the result at the texel size the game uses.
- **Resolution.** A light map texel of half a meter cannot show a sharp shadow of a thin pole. Increase the texel density where shadows matter, or leave those lights dynamic.
- **Mixing static and dynamic lights.** A light baked into the map and also computed at run time at line L6 counts twice. Mark each light as baked, dynamic or mixed, and use the same rule in the bake and at run time.

## Exercises

1. A level has $10000\ \text{m}^2$ of static surface and a light map density of 8 texels per meter. How many texels does the light map need, and how much memory at 4 bytes per texel? *Answer:* $64$ texels per square meter, $640000$ texels in all, about 2.6 MB before padding and mip levels.
2. Why does the light map store irradiance and not the final color? *Answer:* the albedo texture can be sharper and can repeat, while the light map is unique and coarse; their product at line L5 keeps the detail of both. The final color would need the resolution of the albedo in a unique texture.
3. The texture filter at line L5 is bilinear, and the game uses three mip levels below the base level of the light map. How many base texels of padding does each chart need? *Answer:* one texel of the coarsest level is $2^3 = 8$ base texels, so about 8 base texels on each side, or more if charts are placed at arbitrary offsets.

## References
