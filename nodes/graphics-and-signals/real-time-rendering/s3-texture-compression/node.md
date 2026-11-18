---
tag: EBSNSC
kind: algorithm
slug: s3-texture-compression
name: S3 texture compression
aliases:
- S3TC
- DXT1
- BC1 compression
area: graphics-and-signals/real-time-rendering
level: core
summary: Code each 4x4 block of texels in 64 bits, as two 16-bit endpoint colors and a 2-bit index per texel into the line between them, for 4 bits per texel and random access on the GPU.
model: word-ram
complexity:
  vars: {N: the number of texels of the image}
  time: {worst: Θ(N)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, in_place: false}
history:
  year: 1997
  people: [Konstantine Iourcha, Krishna Nayak, Zhou Hong]
  note: The S3 patent for fixed-rate block compression with inferred pixel values was filed in 1997 and granted in 1999. Microsoft adopted the formats in DirectX as DXTC.
prereqs: [texture-mapping]
see_also: [adaptive-scalable-texture-compression, texture-mapping, mipmap, vector-quantization, principal-component-analysis, power-iteration, color-quantization, lossy-compression]
sources:
  - paper: "Konstantine I. Iourcha, Krishna S. Nayak and Zhou Hong, System and method for fixed-rate block-based image compression with inferred pixel values, US patent 5,956,431, S3 Incorporated, filed 2 October 1997, granted 21 September 1999"
    title: Iourcha, Nayak and Hong, US patent 5,956,431, 1999
    locator: the whole patent (two stored colors per block, inferred colors between them, and an index per pixel)
  - url: https://registry.khronos.org/OpenGL/extensions/EXT/EXT_texture_compression_s3tc.txt
    title: Khronos Group, EXT_texture_compression_s3tc, OpenGL extension specification, version 1.6, 2013
    locator: the appendix on the S3TC formats (the 8 bytes of a block, code(x, y) from bits 2(4y + x) and 2(4y + x) + 1, and the palettes for color0 > color1 and color0 <= color1)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 6.2, Image Texturing, the part on texture compression (general locator)
---

S3 texture compression stores a color texture in fixed-size blocks that the GPU decodes as it samples. Each block of $4 \times 4$ texels takes 64 bits: two endpoint colors of 16 bits, and a 2-bit index per texel that picks one of four colors on the line between the endpoints. So every texel costs 4 bits, and the GPU finds any texel at a fixed address. S3TC is a family of formats. This page covers its basic RGB format, which Direct3D names BC1, and mentions the formats with alpha as variants. [Adaptive scalable texture compression](/adaptive-scalable-texture-compression/) is a later fixed-rate format with 128-bit blocks of many sizes, many color modes and a choice of bit rate. Both differ from general image codecs such as JPEG, which have a variable rate and cannot decode one texel without its neighbors.

## In plain words

A small patch of a photo seldom holds many different colors. Most of the time the colors of a $4 \times 4$ patch lie close to one straight line between a darker and a lighter color.

So, for each patch, store only the two end colors, in a short form of 16 bits each. Between them the decoder makes two more colors, one third and two thirds of the way along. Then for each of the 16 texels, store a number from 0 to 3 that says which of the four colors to use.

Every patch takes the same 8 bytes. The graphics card can jump straight to the patch it needs, read 8 bytes, and get the color of any texel in it.

## The problem

The input is an image of $W \times H$ RGB texels, with $W$ and $H$ multiples of 4. The output is $W H / 16$ blocks of 64 bits. The decoder must be a fixed and cheap function of one block, so that the texture unit can sample a compressed texture at random places, with [mipmaps](/mipmap/) and filtering. The encoder may be slow, because it runs once, offline. Its goal is a small error between the image and the decoded image.

A color word is RGB565: red in bits 15 to 11, green in bits 10 to 5 and blue in bits 4 to 0. The word $w$ stands for the color $E(w) = (R/31, G/63, B/31)$. Green gets one more bit because the eye is most sensitive to it.

| part of the block | bits |
|---|---|
| `color0`, a little-endian RGB565 word | 16 |
| `color1`, a little-endian RGB565 word | 16 |
| 16 indices of 2 bits, texel $i = 4y + x$ in bits $2i$ and $2i + 1$ of a little-endian 32-bit word | 32 |
| total for 16 texels | 64, so 4 bits per texel |

Against 24-bit RGB this is a ratio of 6 to 1.

## The algorithm

```pseudo id=main
BC1-DECODE(block)
L1  c0, c1 ← the first two 16-bit words; bits ← the last 32 bits
L2  C0, C1 ← E(c0), E(c1)                        ▷ expand RGB565
L3  if c0 > c1 then P ← (C0, C1, (2 C0 + C1)/3, (C0 + 2 C1)/3)
L4  else P ← (C0, C1, (C0 + C1)/2, transparent black)
L5  return texel i = P[(bits >> 2i) & 3] for i = 0..15

BC1-ENCODE(16 colors)
L6  axis ← the principal axis of the colors      ▷ power iteration on the covariance
L7  lo, hi ← the colors with the least and the greatest projection on the axis
L8  c0, c1 ← RGB565 of hi and lo, swapped so that c0 > c1   ▷ equal words: all indices 0
L9  for each texel pick the index of the nearest color of P
L10 return c0, c1 and the 16 indices packed
```

Decoding is lines L1 to L5, a fixed function of the block. The comparison of the two words in lines L3 and L4 is the trick of the format: the order of the endpoints, which costs no bits, picks one of two palettes. The four-color palette suits smooth blocks. The three-color palette has a transparent texel for cut-out textures such as leaves.

Encoding is a search over endpoints and indices, and lines L6 to L10 are one simple strategy, a range fit. It takes the axis of largest spread of the colors, as in [principal component analysis](/principal-component-analysis/) computed by [power iteration](/power-iteration/), and uses the two extreme colors along it. For fixed endpoints, line L9 picks the best index for every texel.

## Example

Take a block in which every row holds the colors $(0.8, 0.4, 0.1)$, $(0.7, 0.4, 0.2)$, $(0.6, 0.4, 0.3)$ and $(0.5, 0.4, 0.4)$. They lie on a line, so the principal axis is the direction $(1, 0, -1)$. The extremes are $(0.8, 0.4, 0.1)$ and $(0.5, 0.4, 0.4)$.

Rounding gives $R = 25$, $G = 25$, $B = 3$ for the first, the word `0xCB23`, and $R = 16$, $G = 25$, $B = 12$ for the second, the word `0x832C`. Since `0xCB23 > 0x832C`, the palette has four colors:

| index | $(R/31, G/63, B/31)$ | about |
|---|---|---|
| 0 | $(25/31, 25/63, 3/31)$ | $(0.806, 0.397, 0.097)$ |
| 1 | $(16/31, 25/63, 12/31)$ | $(0.516, 0.397, 0.387)$ |
| 2 | $(22/31, 25/63, 6/31)$ | $(0.710, 0.397, 0.194)$ |
| 3 | $(19/31, 25/63, 9/31)$ | $(0.613, 0.397, 0.290)$ |

The four texels of a row get the indices 0, 2, 3 and 1. As 2-bit fields from the low bits up, this is the byte $0 + 2 \cdot 4 + 3 \cdot 16 + 1 \cdot 64 = 120$, or `0x78`. The whole block is the 8 bytes `23 CB 2C 83 78 78 78 78`. The largest error of a channel is $0.016$, about 4 levels of 255, which comes from the rounding to RGB565.

## Correctness

The proof file shows three facts. First, the 64 bits split into fields that do not overlap, and every 64-bit string decodes, so decoding is a fixed function of the block with random access. Second, for fixed endpoints the index of line L9 gives the least total squared error, because each texel adds its own term. Third, if all colors of a block lie on the palette of two RGB565 words $c_0 > c_1$, and both endpoints occur, the encoder finds exactly those words and the decoded block equals the input. The covariance of such a block has rank one, so the power iteration finds the line in one step.

## Complexity

Decoding a texel reads one block and does a few integer operations, $O(1)$ in the word-RAM model. Encoding a block with the range fit takes $O(1)$ time, for a fixed number of iterations on a $3 \times 3$ matrix and 16 comparisons with 4 colors. So an image of $N$ texels takes $\Theta(N)$ time to encode and $N / 2$ bytes to store. Better encoders search more endpoints per block and cost more, but the decoder stays the same.

## Properties

- **Fixed rate.** Every block has 64 bits. This is a property of the format.
- **Random access.** The address of a texel is known, and its block decodes alone. This is proved.
- **Lossless on palette colors.** Proved for the encoder of this page, as above.
- **Measured error.** On 300 random blocks of diagonal color gradients with a little noise, the encoder of the code has a root mean square error of about 3.4 levels of 255 when the colors in a block span at most 0.15, and about 11.5 levels when they span the full range. These are measurements. Four colors cannot follow a gradient of seven steps exactly.
- **Not exact across GPUs.** The format specification gives the palette formulas but no rounding rule for the thirds and the halves, and GPUs differ in the last bit. The decoder of the code gives exact fractions.

## Variants and improvements

- **Formats with alpha.** Direct3D names them BC2 and BC3. BC2 adds 4 bits of alpha per texel. BC3 adds an alpha block of two 8-bit endpoints and 3-bit indices. Both use 128 bits per block, 8 bits per texel.
- **One and two channels.** BC4 and BC5 use the alpha block of BC3 for one or two channels, which suits height maps and [normal maps](/normal-mapping/).
- **Later block formats.** BC6H codes HDR color and BC7 codes high-quality RGBA, both in 128-bit blocks with several modes and partitions. [ASTC](/adaptive-scalable-texture-compression/) has many block sizes.
- **Better encoders.** Refine the endpoints by least squares for the chosen indices and repeat, or try many endpoint pairs around the range fit. Cluster fit tries every split of the sorted colors into the four palette slots.
- **Hardware rounding.** Some decoders round the expansion to 8 bits and the thirds in integer arithmetic. A test that must match one GPU bit for bit needs its rounding rule.

## When to use it

Use it for color textures on GPUs that support it, which includes nearly all desktop GPUs, when 4 bits per texel are worth a small loss. Use the alpha variants for textures with smooth alpha, and the three-color mode only for cut-out alpha. Use [ASTC](/adaptive-scalable-texture-compression/) or BC7 where a better quality or another bit rate is needed. Do not use it for data that needs exact values, such as lookup tables or masks with many levels.

## Pitfalls

- **Endpoints in the wrong order.** If an encoder writes `color0 <= color1` by accident, the block switches to the three-color palette, and index 3 becomes black or transparent. When the two rounded words are equal, the four-color mode is impossible, so write all indices 0.
- **Opaque black or transparent black.** In the RGB variant of the OpenGL extension, index 3 of the three-color palette is opaque black. In the RGBA variant it is transparent. The code returns transparent black.
- **Gradients and banding.** Smooth gradients over large areas show steps, because a block has only four colors and the endpoints have only 5 or 6 bits.
- **Normal maps.** Storing $x$, $y$ and $z$ in the three channels of this format gives poor normals. Use two channels in BC5 and rebuild $z$.
- **Image size.** The sides must be multiples of 4. Small mip levels still use whole blocks.
- **sRGB.** For an sRGB texture, the decoder interpolates the stored values, and the sampler converts to linear after decoding. An encoder that measures the error in linear space and then stores sRGB values chooses worse endpoints.

## Implementations

## History

S3 Incorporated filed the patent for fixed-rate block compression with inferred pixel values in October 1997, with Konstantine Iourcha, Krishna Nayak and Zhou Hong as inventors, and it was granted in September 1999. The method builds on block truncation coding, which also codes a block by two colors and a bit per pixel. Microsoft licensed the formats for DirectX, where they were called DXTC, and later versions of Direct3D renamed them BC1 to BC3. OpenGL supports them through the EXT_texture_compression_s3tc extension. For many years they were the standard compressed texture formats on desktop GPUs.

## References
