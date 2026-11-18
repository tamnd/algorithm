---
tag: XB2HVD
kind: algorithm
slug: adaptive-scalable-texture-compression
name: Adaptive scalable texture compression
aliases:
- ASTC
area: graphics-and-signals/real-time-rendering
level: advanced
summary: A block texture format with 128 bits per block for footprints from 4x4 to 12x12 texels, whose color endpoints and weights are packed with trits, quints and bits by integer sequence coding.
model: word-ram
complexity:
  vars: {N: the number of texels decoded}
  time: {worst: Θ(N)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, in_place: false}
history:
  year: 2012
  people: [Jørn Nystad, Anders Lassen, Andy Pomianowski, Sean Ellis, Tom Olson]
  note: Nystad and others presented the format at High Performance Graphics 2012, and Khronos adopted it for OpenGL and OpenGL ES.
prereqs: [s3-texture-compression, texture-mapping]
see_also: [s3-texture-compression, texture-mapping, mipmap, vector-quantization, arithmetic-coding, bilinear-interpolation, hash-function, lossy-compression]
sources:
  - paper: doi:10.2312/EGGH/HPG12/105-114
    title: Jørn Nystad, Anders Lassen, Andy Pomianowski, Sean Ellis and Tom Olson, Adaptive scalable texture compression, High Performance Graphics 2012
    locator: pages 105 to 114 (the block layout, bounded integer sequence encoding, the color endpoint modes and partitions, and the quality measurements)
  - url: https://registry.khronos.org/OpenGL/extensions/KHR/KHR_texture_compression_astc_hdr.txt
    title: Khronos Group, KHR_texture_compression_astc_hdr and KHR_texture_compression_astc_ldr, OpenGL extension specification
    locator: the appendix on the ASTC format (block mode table, weight ranges, integer sequence encoding, unquantization tables, color endpoint modes and weight infill)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 6.2, Image Texturing, the part on texture compression (general locator)
---

Adaptive scalable texture compression, ASTC, is a fixed-rate block format like [S3 texture compression](/s3-texture-compression/), but every block has 128 bits, whatever its footprint. A 2D footprint goes from $4 \times 4$ to $12 \times 12$ texels, so one format gives rates from 8 down to $8/9$ bits per texel. In S3TC each texel has its own 2-bit index and the endpoints are always RGB565. In ASTC the block stores a smaller grid of weights that the decoder interpolates up to the texels, the color endpoints can have many precisions and channel layouts, and both are packed in ranges that are not powers of two. This page describes the decoding of a block and the bounded integer sequence encoding (BISE) that packs the numbers. The code covers a stated subset: BISE in both directions, and the decoding of a 2D LDR block with one partition, one weight plane and the RGB or RGBA direct endpoint modes.

## In plain words

Each block of the texture gets the same 16 bytes, but the encoder decides how to spend them. It stores two end colors and a small grid of mixing weights. To color a texel, the decoder looks up the weight at that place in the grid, smoothly between grid points, and mixes the two end colors by that weight.

The trick is how numbers are stored. A number from 0 to 2 needs more than one bit but less than two. So ASTC packs five such numbers into 8 bits, and three numbers from 0 to 4 into 7 bits. That way no bit goes to waste, and the encoder can pick almost any precision for the colors and the weights.

## The problem

The decoder gets one block of 128 bits and the footprint $B_s \times B_t$ of the texture, which is fixed for the whole image. It must return the color of every texel of the block, as a fixed function of these bits, so that the texture unit can fetch a texel at a known address and decode it alone. The encoder gets the texels and must choose the block mode, the endpoints and the weights that give the smallest error. That is a search, and its quality is measured, not proved.

The rate follows from the footprint:

| footprint | bits per texel |
|---|---|
| $4 \times 4$ | 8 |
| $6 \times 6$ | $32/9 \approx 3.56$ |
| $8 \times 8$ | 2 |
| $12 \times 12$ | $8/9 \approx 0.89$ |

A block of one partition has this layout:

| bits | field |
|---|---|
| 0 to 10 | block mode: the weight grid $N \times M$, the weight range $0..w_{max}$, and dual plane |
| 11 to 12 | the number of partitions minus 1 |
| 13 to 16 | the color endpoint mode, CEM |
| 17 upward | the color values, one BISE stream |
| 127 downward | the weights, one BISE stream, with bit $k$ of the stream at bit $127 - k$ |

The bits between the two streams are not used. A range $0..M$ in BISE has $M + 1 = 2^n$, $3 \cdot 2^n$ or $5 \cdot 2^n$. A value is $h \cdot 2^n + m$, with $m$ its $n$ low bits and $h$ a trit or a quint. Five trits pack into 8 bits and three quints into 7, which costs $n + 8/5$ or $n + 7/3$ bits per value.

## The algorithm

```pseudo id=main
ASTC-DECODE(block, Bs, Bt)
L1  (N, M, wmax, dual) ← BLOCK-MODE(bits 0..10); error if reserved, N > Bs or M > Bt
L2  partitions ← bits 11..12 + 1; CEM ← bits 13..16          ▷ here 1 partition, no dual plane
L3  wbits ← ISE-BITS(N M, wmax); error unless N M ≤ 64 and 24 ≤ wbits ≤ 96
L4  cmax ← the largest color range with ISE-BITS(2 (CEM div 4 + 1), cmax) ≤ 111 - wbits
L5  v ← UNQUANT-COLOR(ISE-DECODE(bits from 17 upward, cmax))     ▷ to 0..255
L6  (E0, E1) ← ENDPOINTS(CEM, v)              ▷ swap and blue contraction if the sums fall
L7  w ← UNQUANT-WEIGHT(ISE-DECODE(bits from 127 downward, wmax)) ▷ to 0..64
L8  for each texel (s, t): i ← INFILL(w, s, t)               ▷ fixed-point bilinear
L9      C ← floor((257 E0 (64 - i) + 257 E1 i + 32) / 64)    ▷ per channel, 16 bits
L10 return the texels

ISE-DECODE(stream, count, max)           ▷ max + 1 = 2^n, 3 2^n or 5 2^n
L11 set the bits at and past ISE-BITS(count, max) to 0
L12 for each group of 5 values (trits) or 3 (quints), read m_j and the code bits between them
L13     (h_0, h_1, ...) ← TABLE[code]
L14     value_j ← h_j 2^n + m_j
```

Line L4 is why the format needs no field for the color precision: the decoder gives the colors all the bits that the weights leave, at the largest range that fits. Line L6, for the modes 8 (RGB) and 12 (RGBA), compares the sums $v_0 + v_2 + v_4$ and $v_1 + v_3 + v_5$. If the second is smaller, it swaps the endpoints and moves red and green halfway toward blue, which gives more precision to colors near gray. This costs no bits, in the same way as the order of the endpoints in S3TC. Line L8 maps the texel to the weight grid with the step $\lfloor (1024 + \lfloor B_s/2 \rfloor)/(B_s - 1) \rfloor$ and mixes four weights with factors in sixteenths.

The trit and quint tables of line L13 come from short bit formulas in the format specification. Their values are not in order: in the weight range $0..11$, the stored values $0, 1, 2, 3$ unquantize to $0, 64, 17, 47$.

## Example

**BISE.** Store the five values $7, 0, 11, 4, 9$ in the range $0..11 = 3 \cdot 2^2 - 1$, so $n = 2$.

| value | 7 | 0 | 11 | 4 | 9 |
|---|---|---|---|---|---|
| trit $h$ | 1 | 0 | 2 | 1 | 2 |
| low bits $m$ | 3 | 0 | 3 | 0 | 1 |

The trits $(1, 0, 2, 1, 2)$ pack into the code $T = 231$. The stream is $m_0$, $T_{1..0}$, $m_1$, $T_{3..2}$, $m_2$, $T_4$, $m_3$, $T_{6..5}$, $m_4$, $T_7$, which is $5 \cdot 2 + 8 = 18$ bits. Fixed 4-bit fields would take 20 bits, and the information content is $\log_2 12^5 \approx 17.9$ bits.

**A block.** Take a $4 \times 4$ footprint with a $4 \times 4$ weight grid in the range $0..11$ and CEM 8. The weights take $16 \cdot 2 + \lceil 128/5 \rceil = 58$ bits. That leaves $128 - 17 - 58 = 53$ bits for 6 color values, and the largest range that fits is $0..255$, at 48 bits. Let the colors be $v = (40, 200, 100, 220, 50, 60)$. The sums are $190$ and $480$, so there is no swap: $E_0 = (40, 100, 50, 255)$ and $E_1 = (200, 220, 60, 255)$. Let each row of weights store $0, 2, 5, 11$, which unquantize to $0, 17, 59, 36$. The grid has the size of the block, so the infill is the identity. The second texel of a row has $i = 17$, and its red channel is $\lfloor (10280 \cdot 47 + 51400 \cdot 17 + 32)/64 \rfloor = 21203$, about 82.5 on a scale of 255. The code writes this block as the 16 bytes `51 02 51 90 c9 b8 65 78 40 97 d0 2a 38 1e ba 04`.

## Correctness

The proof file shows four things for the subset. First, a BISE stream of $V$ values has $V n + \lceil 8V/5 \rceil$ or $V n + \lceil 7V/3 \rceil$ bits, and decoding returns what the encoder wrote, also for a short last group, whatever the bits past the end hold. The proof uses the fact that the smallest code of a tuple padded with zeros has its high bits zero, which is checked on every short tuple. Second, the color unquantization of a trit or quint range is one to one onto values from 0 to 255, and flipping the lowest bit mirrors the value. Third, the infill factors are nonnegative and sum to 16, a neighbor past the grid always has the factor 0, and the corners get the corner weights. Fourth, the whole decode reads only the 128 bits and the footprint, and the color and weight streams never overlap.

## Complexity

A block has at most 64 weights and at most 18 color values, so the work before the texel loop is $O(1)$. Each texel then takes $O(1)$ operations on small integers, in the word-RAM model. So decoding $N$ texels takes $\Theta(N)$ time and $O(1)$ extra space per block. A texture of $W \times H$ texels takes $128 \lceil W/B_s \rceil \lceil H/B_t \rceil$ bits. Encoding is far more costly: a good encoder tries many block modes, partitions and endpoint fits per block.

## Properties

- **Fixed rate and random access.** Every block has 128 bits and decodes alone. This is proved for the subset and is a property of the whole format.
- **Near-optimal packing.** BISE costs less than 0.016 bits per value above the information content for trits and less than 0.012 for quints. This follows from $8/5 - \log_2 3$ and $7/3 - \log_2 5$.
- **One decoder for many rates.** The footprint sets the rate, and the block mode sets how the bits split between the weights and the colors.
- **Bit-exact decoding.** The specification gives every step in integer arithmetic, so all conforming decoders agree on every bit, unlike S3TC.
- **Measured quality.** Nystad and others compare ASTC with other formats at equal bit rates on test images. Such results are measurements of a given encoder on given images.

## Variants and improvements

- **Partitions.** A block can split its texels into 2, 3 or 4 partitions, each with its own endpoints. A 10-bit seed and a hash function of the texel position choose the partition of each texel, so the format needs no table of shapes.
- **Dual plane.** A second weight grid for one channel, for example alpha or one channel of a normal map, lets that channel vary on its own.
- **Other color endpoint modes.** There are 16 modes: luminance, luminance with alpha, RGB with a scale, base and offset forms, and HDR modes.
- **3D blocks.** Footprints from $3 \times 3 \times 3$ to $6 \times 6 \times 6$ texels code volume textures.
- **Void extent.** A special block mode stores one constant color for the block, with the extent of the area that has this color.
- **Profiles.** The LDR profile is the most common in hardware. The HDR profile adds the HDR endpoint modes.
- **Encoders.** Encoders search the block modes and partitions with heuristics and give presets from fast to thorough. The search time is tuning, and the quality is measured.

## When to use it

Use it on GPUs that support it, which includes most mobile GPUs, when you need one format for many kinds of textures and rates, or a rate below 2 bits per texel for large, smooth textures. It handles color, alpha, normal maps and HDR with the same decoder. On desktop GPUs without ASTC, use [S3TC](/s3-texture-compression/) or the later BC formats. For textures that need exact values, do not use any lossy format.

## Pitfalls

- **The footprint is not in the block.** The decoder must get the footprint from the texture format. The same 16 bytes decode to a different image with another footprint.
- **Quantized values are not in order.** In trit and quint ranges, the stored integer and the unquantized value have different orders. An encoder that rounds to the nearest stored integer gives wrong colors. Map through the tables.
- **The weight stream is reversed.** The weights start at bit 127 and run down, bit by bit. Reading them from bit 0 upward gives garbage.
- **Illegal blocks.** A weight grid larger than the block, more than 64 weights, or too many bits all give the error color. The decoder must check every condition, because the block mode field has many values that are reserved or illegal.
- **sRGB and output formats.** The 16-bit result of line L9 converts to the output format by rules of the profile, and sRGB textures use other rules for the expansion of the endpoints. The code of this page returns the 16-bit values only.
- **Low rates on detailed textures.** A large footprint has few weights per texel, which blurs fine detail. Choose the footprint per texture.

## Implementations

## History

Jørn Nystad, Anders Lassen, Andy Pomianowski, Sean Ellis and Tom Olson designed ASTC and presented it at High Performance Graphics in 2012. Their goal was one format for all kinds of content and many bit rates, in place of several formats with fixed rates. Khronos adopted it as an extension for OpenGL and OpenGL ES, with an LDR and an HDR profile, and later Vulkan supported it too. It became the main compressed texture format on mobile GPUs.

## References
