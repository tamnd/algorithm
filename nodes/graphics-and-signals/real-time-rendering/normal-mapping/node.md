---
tag: AJKGDG
kind: technique
slug: normal-mapping
name: Normal mapping
aliases:
- normal maps
area: graphics-and-signals/real-time-rendering
level: intro
summary: Store surface normals in a texture, usually in tangent space, and use them in place of the interpolated normal when shading.
prereqs: [bump-mapping, texture-mapping]
see_also: [bump-mapping, parallax-mapping, displacement-mapping, mesh-simplification, gram-schmidt-process, s3-texture-compression, mipmap, blinn-phong-reflection-model]
sources:
  - paper: doi:10.1145/280814.280832
    title: Jonathan Cohen, Marc Olano and Dinesh Manocha, Appearance-preserving simplification, SIGGRAPH 1998
    locator: storing the normals of the detailed surface in a texture over the simplified mesh (general locator)
  - paper: doi:10.1145/258734.258873
    title: Mark Peercy, John Airey and Brian Cabral, Efficient bump mapping hardware, SIGGRAPH 1997
    locator: the tangent frame per vertex and the perturbed normal in that frame (general locator)
  - paper: doi:10.1080/2151237x.2005.10129203
    title: Michael Toksvig, Mipmapping normal maps, Journal of Graphics Tools, 2005
    locator: the length of the averaged normal as a measure of the spread of normals, and the reduced specular exponent (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 6.7, Bump Mapping, from page 208 (the tangent frame and normal maps)
---

Normal mapping stores a unit normal per texel in an RGB texture and uses it as the shading normal of the pixel. Most normal maps store the normal in tangent space, relative to the frame of the surface, so the same map works on any part of any mesh and can tile. [Bump mapping](/bump-mapping/) computes the tilted normal from the slopes of a height texture at run time. Normal mapping stores the result, which costs one texture read and no differences, and can store normals that come from no single height field, such as those baked from a detailed mesh. Like bump mapping, it changes only the lighting. [Parallax mapping](/parallax-mapping/) also shifts the texture by the view, and [displacement mapping](/displacement-mapping/) moves the geometry.

## In plain words

A normal is the direction a surface faces, and light uses it to decide how bright a point is. A normal map is an image where each pixel holds such a direction, written as a color: red for left and right, green for up and down, blue for straight out of the surface.

At render time the shader reads the color, turns it back into a direction, and turns that direction from the frame of the surface into the frame of the world. Then it lights the pixel with it. A low-detail model with a good normal map looks almost as detailed as the high-detail model it came from, as long as you do not look at its outline.

## When it applies

- The surface detail is smaller than the triangles, and the outline does not need to show it.
- There is a detailed version of the model, or a height or sculpt, from which to bake the normals.
- The renderer has a tangent frame per vertex, or can build one, that matches the frame of the baking tool.
- The memory for a second texture is acceptable. Compressed two-channel formats reduce it to 8 bits per texel or less.
- It does not apply when the relief must hide parts of itself or change the outline. Use the parallax methods or displacement mapping then.

## The template

The inputs are a normal map with texels $c \in [0, 1]^3$, and at each vertex a normal $N$, a tangent $T$ along the $u$ axis of the texture, and a sign $\sigma = \pm 1$ for the handedness.

1. Bake or author the map. For each texel, find the normal $n = (n_T, n_B, n_N)$ of the detailed surface in the tangent frame of the low-detail surface, and store $c = (n + 1)/2$, quantized to 8 or more bits per channel.
2. Per vertex, make $T$ orthogonal to $N$ by one step of the [Gram-Schmidt process](/gram-schmidt-process/), $T \leftarrow \mathrm{normalize}(T - (N \cdot T) N)$, and set the bitangent $B = \sigma (N \times T)$.
3. Interpolate $N$, $T$ and $B$ over the triangle, and normalize them again per pixel.
4. Read the texel and decode it: $n = 2c - 1$, then normalize $n$. For a two-channel map, rebuild $n_N = \sqrt{\max(0, 1 - n_T^2 - n_B^2)}$.
5. Transform to the world: $n_w = n_T T + n_B B + n_N N$.
6. Use $n_w$ in the lighting in place of the interpolated normal.

Step 5 is exact only if $T$, $B$ and $N$ are the same frame that step 1 used. Two tools that build tangents in different ways give visible seams and wrong shading, so the baker and the renderer must agree on the convention. This is the main practical rule of the method, and it is a convention, not a law.

## Classic examples

**A trace.** A floor has $N = (0, 1, 0)$, $T = (1, 0, 0)$ and $B = (0, 0, -1)$, and the light comes from the unit direction $l = (0.6, 0.8, 0)$. The flat floor gives $N \cdot l = 0.8$. A texel stores $c = (204, 128, 230)/255$, which decodes in step 4 to $(0.600, 0.004, 0.804)$, of length $1.003$, and normalizes to $(0.598, 0.004, 0.801)$. Step 5 gives $n_w = (0.598, 0.801, -0.004)$, tilted by about 37 degrees toward the light, and $n_w \cdot l = 1.000$. The pixel is lit as if it faced the light. The value 128 does not decode to exactly 0, because $2 \cdot 128/255 - 1 = 1/255$.

**Detail from a high-poly model.** Cohen, Olano and Manocha (1998) stored the normals of a detailed mesh in a texture over a [simplified mesh](/mesh-simplification/), so that the simplified model kept its appearance. Game art is made the same way today: a sculpt with millions of triangles, a game mesh with thousands, and a baked normal map.

**Tiled materials.** Bricks, wood, cloth and stone use tiling tangent-space maps, often made from a height map as in [bump mapping](/bump-mapping/), and stored with [block compression](/s3-texture-compression/) in two channels.

**Detail maps.** A second, small normal map that repeats many times adds fine detail, such as pores on skin, over a large base map.

## Variations

- **Object-space normal maps.** Store the normal in the frame of the object. This needs no tangents and has no tangent seams, but the map cannot tile or be shared between parts, and it breaks with skinning unless the normal is transformed with the bones.
- **Two-channel storage.** Store only $n_T$ and $n_B$, and rebuild $n_N$ in step 4. Block formats for two channels keep more precision than three-channel color formats.
- **Mipmapping with Toksvig's factor.** The average of different unit normals is shorter than 1. Toksvig (2005) uses its length $|\bar n|$ to lower the specular exponent $p$ to $p' = p |\bar n| / (|\bar n| + p (1 - |\bar n|))$, so that distant bumpy surfaces get a wider highlight in place of sparkles. This is a heuristic. For the two normals $(\pm 0.6, 0, 0.8)$ the average is $(0, 0, 0.8)$, and $p = 32$ becomes about $3.6$.
- **Blending two maps.** Adding the tangent components of two maps and normalizing again is a common heuristic. Methods that rotate the detail normal into the frame of the base normal keep more of the detail.
- **Parallax and relief.** The normal map gives the lighting, and [parallax mapping](/parallax-mapping/) or [parallax occlusion mapping](/parallax-occlusion-mapping/) shifts the texture coordinate where the normal is read.

## Pitfalls

- **Tangent frame mismatch.** If the renderer builds $T$ and $B$ in another way than the baker, the lighting is wrong near seams and on curved parts. Use one shared convention.
- **The green channel.** Some tools store $+B$ and others $-B$ in green. A map in the other convention lights bumps from the wrong side.
- **Mirrored UVs.** Mirrored parts of a mesh need $\sigma = -1$. Without it, the mirrored side has inverted bumps.
- **Forgetting to decode or normalize.** Using $c$ in place of $2c - 1$, or skipping the normalization after filtering and interpolation, gives a dim and wrong result.
- **Wrong color space.** A normal map holds vectors, not colors. Loading it as sRGB applies a gamma curve and bends all normals. Mark it as linear data.
- **Specular aliasing.** At a distance, a mipmapped normal map gives an average normal, but the true surface has many normals, so the highlight should widen. Without a correction such as Toksvig's, highlights sparkle or vanish.
- **Flat outlines and no self-shadowing.** As with bump mapping, the silhouette stays smooth and the bumps cast no shadows.

## Exercises

1. Show that $n = 2c - 1$ inverts $c = (n + 1)/2$, and find the largest angle error that 8-bit quantization of each channel can cause for a unit normal near $(0, 0, 1)$.
2. Show that $T$, $B$ and $N$ from step 2 form an orthonormal frame when $N$ is a unit vector and $T$ is not parallel to $N$.
3. Explain why the interpolated $T$ and $N$ of step 3 are in general not orthogonal, and what error this gives in step 5.
4. Compute Toksvig's exponent for $p = 64$ when the average of the normals in a texel has length 0.95.
5. A height map $h$ is converted to a normal map by the formula of step 6 of bump mapping. What happens to the result when the texture is tiled twice as often, and how must the conversion change?

## References
