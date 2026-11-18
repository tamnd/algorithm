---
tag: P04D18
kind: data-structure
slug: g-buffer
name: G-buffer
aliases:
- geometry buffer
area: graphics-and-signals/real-time-rendering
level: core
summary: A set of screen-sized images that stores, per pixel, the depth and the surface attributes of the nearest surface, such as the normal, the base color and the roughness, for a later shading pass.
model: real-ram
complexity:
  vars: {p: the number of pixels, b: the number of bytes per pixel, m: the number of samples per pixel}
  time: {write: O(1), read: O(1), clear: Θ(p m b)}
  space: {total: Θ(p m b)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1990
  people: [Takafumi Saito, Tokiichiro Takahashi]
  note: Saito and Takahashi named the G-buffer in 1990 and used it for image-space drawing of edges, contours and hatching. Deering and his coauthors had already shaded from stored normals after visibility in 1988.
prereqs: [z-buffer, pixel]
see_also: [deferred-shading, visibility-buffer, tiled-shading, normal-mapping, bit-packing, scalar-quantization, multisample-antialiasing, screen-space-ambient-occlusion]
sources:
  - paper: doi:10.1145/97880.97901
    title: "Takafumi Saito and Tokiichiro Takahashi, Comprehensible rendering of 3-D shapes, SIGGRAPH 1990, Computer Graphics 24(4), 197-206"
    locator: the geometric buffers (G-buffers) and the image-space operations on them
  - url: http://jcgt.org/published/0003/02/01/
    title: "Zina H. Cigolle, Sam Donow, Daniel Evangelakos, Michael Mara, Morgan McGuire and Quirin Meyer, A survey of efficient representations for independent unit vectors, Journal of Computer Graphics Techniques 3(2), 1-30, 2014"
    locator: the octahedral representation, its encode and decode, and the precise encoding that tests the nearby integer codes
  - paper: "Michael Deering, Stephanie Winner, Bic Schediwy, Chris Duffy and Neil Hunt, The triangle processor and normal vector shader: a VLSI system for high performance graphics, SIGGRAPH 1988, 21-30"
    locator: the shading of each pixel from a stored normal after the visibility stage
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 20, Efficient Shading (the part on deferred shading and G-buffer layouts)
---

A G-buffer is a group of screen-sized images, written in one geometry pass, that keeps for each pixel the depth and the surface attributes of the nearest surface: for example the normal, the base color, the roughness and the metallic value. Later passes read it instead of the triangles. It is the data structure under [deferred shading](/deferred-shading/), which shades each pixel once from these values, and under screen-space effects such as [screen-space ambient occlusion](/screen-space-ambient-occlusion/). A [visibility buffer](/visibility-buffer/) is a smaller relative: it stores only a triangle id per pixel and computes the attributes again. Saito and Takahashi named the G-buffer in 1990. This page gives one layout as an example and the octahedral encoding of the normal, which is the most common way to store a normal in 32 bits.

## In plain words

When the renderer draws the scene, it does not compute the light yet. For each pixel it only writes down facts about the surface that is closest to the camera: how far away it is, which way it faces, what color it is and how rough it is. These notes fill a few images of the same size as the screen. A later pass reads the notes for each pixel and computes the light from them, without going back to the triangles. The notes must be small, because there is one set for every pixel, so each value is packed into few bits. A direction, for example, is stored as two short numbers instead of three long ones.

## The abstract type

A G-buffer of width $W$ and height $H$ holds $p = W H$ records, one per pixel, or $p m$ records with $m$ samples per pixel. Each record has the same fixed fields. The operations are:

- **clear**: set every record to the value of the background (the far depth and no surface).
- **write(pixel, record)**: store the record of a fragment that passes the depth test. The geometry pass calls it, and the [z-buffer](/z-buffer/) test decides which fragment is kept.
- **read(pixel)**: return the record. Lighting and screen-space passes call it.

After the geometry pass, the record of each pixel is the record of the fragment with the smallest depth at that pixel, which is the depth test invariant. The buffer holds one surface per pixel and sample. It cannot hold a second, partly hidden surface, so it has no place for transparent fragments.

## Representation

Each field is a channel of one of a few render targets, and the GPU writes all targets of a pixel in one fragment shader call. The layout below is an example, not a standard. Engines differ in the fields, the formats and the number of targets.

| target | format | content | bytes |
|---|---|---|---|
| depth | 32-bit float | the depth of the nearest surface | 4 |
| RT0 | RGBA, 8 bits unorm each | base color (sRGB) and metallic | 4 |
| RT1 | RG, 16 bits snorm each | normal, octahedral code | 4 |
| RT2 | RGBA, 8 bits unorm each | roughness and 3 spare channels | 4 |

This layout uses $b = 16$ bytes per pixel. The view-space position is not stored: the shading pass computes it from the depth and the pixel position.

**The octahedral normal.** A unit normal $n = (x, y, z)$ has two degrees of freedom, so three floats waste space. The octahedral map of Cigolle, Donow, Evangelakos, Mara, McGuire and Meyer (2014) divides $n$ by $s = |x| + |y| + |z|$, which puts it on the octahedron $|x| + |y| + |z| = 1$. The upper half ($z \ge 0$) projects straight down onto the diamond $|u| + |v| \le 1$. The lower half is folded out over the four corners of the square $[-1, 1]^2$. The square is then stored as two signed normalized integers of $b$ bits. The survey compares this map with many other unit-vector codes and finds it among the best in error for its size, at a low cost of encode and decode. That ranking is a measurement.

## Operations

Lines L1 to L4 encode and lines L5 to L7 decode a normal. $\operatorname{sgn}(x)$ is $+1$ for $x \ge 0$ and $-1$ for $x < 0$. The assignment in L3 and L6 is simultaneous: both new values use the old $u$ and $v$. Lines L8 and L9 store a value of $[-1, 1]$ in $b$ bits with $m = 2^{b-1} - 1$. Lines L10 to L15 write and read one texel of the example layout.

```pseudo id=main
OCT-ENCODE(n)
L1  s ← |n.x| + |n.y| + |n.z|
L2  (u, v) ← (n.x / s, n.y / s)
L3  if n.z < 0 then (u, v) ← ((1 - |v|) sgn(u), (1 - |u|) sgn(v))   ▷ fold the lower half
L4  return (u, v)

OCT-DECODE(u, v)
L5  z ← 1 - |u| - |v|
L6  if z < 0 then (u, v) ← ((1 - |v|) sgn(u), (1 - |u|) sgn(v))     ▷ unfold
L7  return (u, v, z) / ‖(u, v, z)‖

QUANTIZE(x, b) and DEQUANTIZE(q, b)
L8  q ← round(x · m)
L9  x ← max(-1, q / m)

PACK-TEXEL(c, n, r, k)                 ▷ base color c, normal n, roughness r, metallic k
L10 word0 ← unorm8(c.r) | unorm8(c.g) << 8 | unorm8(c.b) << 16 | unorm8(k) << 24
L11 word1 ← the two 16-bit codes QUANTIZE(OCT-ENCODE(n), 16), low half first
L12 word2 ← unorm8(r)
UNPACK-TEXEL(word0, word1, word2)
L13 c ← the low three bytes of word0 / 255;  k ← the high byte / 255
L14 n ← OCT-DECODE(DEQUANTIZE of the two signed halves of word1)
L15 return (c, n, word2 / 255, k)
```

The sign rule $\operatorname{sgn}(0) = +1$ matters. With the usual sign function, which is 0 at 0, a normal in the plane $x = 0$ or $y = 0$ with $z < 0$ folds to a wrong point. The clamp in L9 is there because the integer $-2^{b-1}$ has no partner; it maps to $-1$ like $-m$.

**Precise encoding.** Rounding $u$ and $v$ separately does not always give the code that decodes closest to $n$. The survey also gives an encoder that tries the four integer points around $(u m, v m)$ and keeps the one with the smallest angle error. It costs four decodes and helps when the normal is written once and read many times.

## Example

**Encode and decode.** Take $n = (0.6, 0, -0.8)$. Line L1 gives $s = 1.4$ and line L2 gives $(u, v) = (0.428571, 0)$. Since $z < 0$, line L3 folds: $u \leftarrow (1 - 0) \cdot (+1) = 1$ and $v \leftarrow (1 - 0.428571) \cdot \operatorname{sgn}(0) = 0.571429$. The code is $(1, 0.571429)$, a point on the right edge of the square.

To decode, line L5 gives $z = 1 - 1 - 0.571429 = -0.571429$, which is negative, so line L6 unfolds to $(0.428571, 0)$. Line L7 normalizes $(0.428571, 0, -0.571429)$, whose length is $0.714286$, and returns $(0.6, 0, -0.8)$.

**With 8 bits.** $m = 127$, so the code becomes the integers $(127, 73)$, because $0.571429 \cdot 127 = 72.57$. Decoding gives $73 / 127 = 0.574803$, then $(0.425197, 0, -0.574803)$ after the unfold, and $(0.594701, 0, -0.803947)$ after normalizing. The angle error is $0.379$ degrees. With 16 bits ($m = 32767$) the code is $(32767, 18724)$, and since $18724 / 32767 = 4/7$ exactly, this normal decodes without error.

**One texel.** The base color $(0.5, 0.25, 1)$, metallic 0, the normal above and roughness $0.4$ give the three words `0x00FF4080` (the bytes 128, 64, 255 and 0, low byte first), `0x49247FFF` (the codes 32767 and 18724) and `0x00000066` (102, which is $0.4 \cdot 255$).

**Memory.** At 1920 by 1080 pixels, $p = 2\,073\,600$, and the 16 bytes of the layout take $33\,177\,600$ bytes, about 31.6 MiB. With 4 samples per pixel for [multisample antialiasing](/multisample-antialiasing/), every sample needs its own record, and the size is 126.6 MiB. These numbers are the reason for tight packing.

## Correctness

The proofs are in the proofs folder. With $\operatorname{sgn}(0) = +1$ and exact arithmetic:

- OCT-ENCODE maps every nonzero vector into $[-1, 1]^2$, and OCT-DECODE(OCT-ENCODE$(n)$) $= n / \lVert n \rVert$. The proof splits on the sign of $z$ and shows that the unfold undoes the fold, because the fold keeps the signs of $u$ and $v$.
- On the open square $(-1, 1)^2$ the map is also one to one in the other direction: OCT-ENCODE(OCT-DECODE$(u, v)$) $= (u, v)$. On the border, $(1, t)$ and $(1, -t)$ decode to the same vector, and the four corners all decode to $(0, 0, -1)$.
- Quantization moves each coordinate by at most $1 / (2m)$. The angle error after decoding is not proved here. The values in the tests are measurements on 4000 random directions: below 1 degree with 8 bits and below 0.005 degrees with 16 bits, and the precise encoding is never worse.
- The texel pack and unpack return each 8-bit value to within $1/510$ and give the normal of the 16-bit code.

The depth test invariant of the abstract type is a property of the z-buffer, see its page.

## Complexity

The model is the real RAM with $p$ pixels, $m$ samples per pixel and $b$ bytes per record. A write and a read are $O(1)$. A clear is $\Theta(p m b)$ in bytes, though GPUs often clear with a fast metadata flag. The space is $\Theta(p m b)$. The encode and decode of a normal take $O(1)$ operations and one square root.

On a GPU the cost that matters is memory bandwidth. The geometry pass writes $b$ bytes for every fragment that passes the depth test, including fragments that a nearer fragment later overwrites, and each lighting or screen-space pass reads $b$ bytes per pixel. A layout with fewer bytes per pixel is often faster even when it needs more arithmetic to decode. This is the trade that the octahedral code makes, see [memory coalescing](/memory-coalescing/).

## Variants

- **Thin G-buffer.** Only depth and normal, for a light pre-pass: the lights are accumulated into a light buffer, and a second geometry pass reads it to apply the materials.
- **Visibility buffer.** Only the triangle id and the instance id. The [visibility buffer](/visibility-buffer/) page explains the trade.
- **Other normal codes.** Spherical coordinates, a stored $(x, y)$ with $z$ computed from them (wrong for normals that face away from the camera, which occur with normal maps and perspective), and the sphere map code. The survey of Cigolle and coauthors compares them.
- **Material ids.** Some layouts store a small material or shading model id per pixel, so that the shading pass can branch per pixel. This costs bits and can cause [warp divergence](/warp-divergence/).
- **Multisample G-buffer.** One record per sample, with a resolve that shades edge pixels per sample and inner pixels once.

## When to use it

Use a G-buffer when many lights or screen-space passes need the surface attributes of each pixel, and the cost of reading them back is lower than the cost of drawing the geometry again. Keep it as small as the materials allow. Use a visibility buffer when the G-buffer bandwidth is the limit, for example at high resolution or with many samples per pixel. Do not use it for transparent surfaces: draw them in a forward pass after the deferred pass.

## Pitfalls

- **The sign of zero.** Use a sign function with $\operatorname{sgn}(0) = +1$ in the fold, or normals with $x = 0$ or $y = 0$ in the lower half decode wrong.
- **The $(x, y)$ code with $z \ge 0$ assumed.** View-space normals can point away from the camera, so the sign of $z$ must be stored.
- **Base color in the wrong space.** Store the base color in an sRGB format, which the hardware converts, or in linear values with more bits. 8-bit linear values band in dark areas.
- **Interpolating codes.** Do not filter the encoded normal across pixels: the code is not linear, and the fold edges give wrong values. Decode first.
- **Precision of depth.** If the position is computed from the depth, the depth format sets its precision. A 24-bit depth with a standard projection loses precision far from the camera.
- **Bandwidth of MSAA.** With $m$ samples per pixel the buffer is $m$ times larger.

## Implementations

## History

Deering, Winner, Schediwy, Duffy and Hunt built a hardware pipeline in 1988 that found the visible surface first and then shaded each pixel from its stored normal. Saito and Takahashi (1990) gave the stored per-pixel geometry the name G-buffer, and used it for image-space operations: edges, contours and hatching for illustration. In games, deferred shading with a G-buffer became common in the late 2000s, when GPUs could write several render targets at once. The octahedral normal map was used in graphics before 2014; the survey by Cigolle, Donow, Evangelakos, Mara, McGuire and Meyer compared it with the other codes and made it a standard choice.

## References
