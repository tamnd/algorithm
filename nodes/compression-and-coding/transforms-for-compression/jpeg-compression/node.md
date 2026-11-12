---
tag: 2JBQT3
kind: algorithm
slug: jpeg-compression
name: JPEG compression
aliases:
- JPEG
- JPEG baseline
- baseline sequential DCT JPEG
- ITU-T T.81 baseline process
area: compression-and-coding/transforms-for-compression
level: core
summary: "The baseline JPEG coder: 8 x 8 DCT, uniform quantization by a table, zigzag scan, DC differences and run/size Huffman codes, in a file of marker segments."
solves: [lossy-image-compression]
model: real-ram
complexity:
  vars: {n: the number of pixels}
  time: {worst: Θ(n), average: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 1992
  people: [Joint Photographic Experts Group (ISO and CCITT)]
  note: The baseline process and the rest of the JPEG standard were approved as CCITT Recommendation T.81 in September 1992 and published as ISO/IEC 10918-1. JFIF, the usual file format, appeared the same year.
prereqs: [discrete-cosine-transform, scalar-quantization, zigzag-scan, huffman-coding]
see_also: [lossy-image-compression, transform-coding, canonical-huffman-code, fast-dct, jpeg-2000, run-length-encoding, color-spaces, psnr]
sources:
  - url: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
    title: ITU-T Recommendation T.81 (09/92), Digital compression and coding of continuous-tone still images, Requirements and guidelines
    locator: "A.3.3 (FDCT and IDCT), A.3.4 (quantization), A.3.5 (DC differences), A.3.6 and Figure A.6 (zigzag); B.1.1.5 and Table B.1 (entropy-coded segments, padding, marker codes); B.2.2 to B.2.4.2 (frame header, scan header, DQT and DHT syntax, pages 35 to 40); Annex C, Figures C.1 to C.3 (code generation from BITS and HUFFVAL, pages 51 to 53); F.1.2.1 to F.1.2.3 and Table F.1 (Huffman coding of DC and AC coefficients, byte stuffing, pages 88 to 91); F.2.2.3 and Figures F.15 and F.16 (DECODE, pages 107 to 109); Annex K, Tables K.1, K.3 and K.5 and K.3.3 (pages 143, 149, 150 and 158)"
  - url: https://www.w3.org/Graphics/JPEG/jfif3.pdf
    title: Eric Hamilton, JPEG File Interchange Format, Version 1.02, C-Cube Microsystems, 1992
    locator: the APP0 marker segment and the conversion between RGB and YCbCr
  - paper: doi:10.1145/103085.103089
    title: Gregory K. Wallace, The JPEG still picture compression standard, Communications of the ACM 34(4), 1991
    locator: pages 30 to 44 (the history of the JPEG committee, the baseline system, and the modes of operation)
  - book: isbn:9780442012724
    title: William B. Pennebaker and Joan L. Mitchell, JPEG Still Image Data Compression Standard, Van Nostrand Reinhold, 1993
    locator: the chapters on the history of JPEG, the DCT, quantization and the baseline Huffman coding
  - paper: doi:10.1109/T-C.1974.223784
    title: Nasir Ahmed, T. Natarajan and K. R. Rao, Discrete cosine transform, IEEE Transactions on Computers C-23(1), 1974
    locator: pages 90 to 93
---

JPEG compression, in its baseline form, codes an image by cutting it into $8 \times 8$ blocks, taking the 2D [discrete cosine transform](/discrete-cosine-transform/) of each block, dividing each coefficient by the matching entry of a quantization table and rounding, reading the results in [zigzag order](/zigzag-scan/), and coding them with [Huffman codes](/huffman-coding/): the DC coefficient as a difference from the previous block, and the AC coefficients as (run of zeros, size) symbols with ZRL and EOB. The result is a file of marker segments (SOI, DQT, SOF0, DHT, SOS, EOI). The standard is ITU-T T.81 (1992). This page gives a complete baseline coder for greyscale images.

## In plain words

Split the picture into small squares of 8 by 8 pixels. In each square, replace the 64 pixel values by 64 numbers that say how much of each pattern, from flat to finely striped, the square contains. Most squares in a photo are smooth, so the striped patterns get small numbers.

Divide each number by a step taken from a table, with small steps for the smooth patterns and large steps for the fine ones, and round. Many numbers become zero. Read the 64 rounded numbers from the smooth patterns to the fine ones, so that the zeros come together at the end.

Write the first number as the change from the previous square. Write the rest as "so many zeros, then this value", and stop with an "end of block" sign when only zeros are left. Short codes stand for common cases. Decoding undoes each step except the rounding.

## The problem

Given an image with $H$ rows and $W$ columns of 8-bit samples and a quantization table $Q$ of 64 steps from 1 to 255, produce a byte string that a baseline decoder turns into an image $\hat x$ of the same size, with an error that the table controls. This page codes one component, a greyscale image; colour JPEG codes three components the same way, usually after the YCbCr transform and 4:2:0 chroma subsampling of [lossy image compression](/lossy-image-compression/).

**The subset on this page.** Baseline sequential process (SOF0), 8-bit samples, one component, one scan, Huffman tables of Annex K (K.3.3) and quantization table K.1 or a scaled form of it, no restart intervals, a JFIF APP0 segment. The decoder reads any one-component baseline file with 8-bit quantization tables and no restart markers, and skips APPn and COM segments. It does not implement colour, interleaved scans, restart markers, the progressive, lossless and hierarchical processes, or arithmetic coding.

## The algorithm

**Level shift and FDCT (A.3.1, A.3.3).** Subtract 128 from each sample, so $-128 \le s(y, x) \le 127$, and compute

$$F(v, u) = \tfrac14 C_u C_v \sum_{x=0}^{7} \sum_{y=0}^{7} s(y, x) \cos\frac{(2x+1) u \pi}{16} \cos\frac{(2y+1) v \pi}{16},$$

with $C_0 = 1/\sqrt 2$ and $C_u = 1$ otherwise. Here $u$ is the horizontal frequency and $v$ the vertical one. With this scale the transform is orthonormal, and $F(0, 0)$ is 8 times the block mean.

**Quantization (A.3.4).** $S(v, u) = \mathrm{round}(F(v, u) / Q(v, u))$. The decoder uses $R(v, u) = S(v, u) \cdot Q(v, u)$. T.81 gives Table K.1 for luminance as an example, with steps from 10 to 121; it says the tables are "based on psychovisual thresholding" and are examples only.

**DC differences (A.3.5, F.1.2.1).** The DC value $S(0,0)$ is coded as $\mathrm{DIFF} = S(0,0) - \mathrm{PRED}$, where PRED is the DC value of the previous block, 0 at the start. The *category* (SSSS) of a value $v$ is the number of bits of $|v|$ (Table F.1). The encoder writes the Huffman code of SSSS and then SSSS extra bits: the low bits of $v$, or of $v - 1$ when $v < 0$. So a negative value starts with a 0 bit and a positive one with a 1 bit, and the decoder's EXTEND (Figure F.12) undoes it.

**AC run/size symbols (F.1.2.2).** The 63 AC values in zigzag order become symbols RRRRSSSS: RRRR zeros (0 to 15) and then a value of category SSSS (1 to 10), followed by its SSSS extra bits. ZRL (0xF0) stands for 16 zeros and is written only before a later nonzero value. EOB (0x00) ends the block when the rest is zero; it is omitted when position 63 is nonzero.

**Huffman tables (Annex C).** A table is sent as BITS, the number of codes of each length from 1 to 16, and HUFFVAL, the symbols in order of code length. Figures C.1 and C.2 give the codes: the codes of each length are consecutive integers, and the first code of the next length is the last one plus one, shifted left. This is a [canonical Huffman code](/canonical-huffman-code/). The decoder's DECODE (F.2.2.3) keeps MINCODE, MAXCODE and VALPTR per length and reads bits until the value is at most MAXCODE for the current length.

**Byte stuffing and markers.** A marker is 0xFF followed by a code (Table B.1). Inside entropy-coded data the encoder writes 0x00 after each 0xFF byte so that the decoder never sees a false marker (F.1.2.3), and pads the last byte with 1-bits (B.1.1.5). The file is SOI (FFD8), APP0 (FFE0, JFIF), DQT (FFDB, the table in zigzag order), SOF0 (FFC0, precision 8, height, width, components), DHT (FFC4, once for DC and once for AC), SOS (FFDA, then the entropy-coded data), and EOI (FFD9).

```pseudo id=main
JPEG-ENCODE(x, Q)                   ▷ x: H × W samples 0..255, Q: 64 steps
L1  write SOI, APP0, DQT(Q in zigzag order), SOF0(H, W), DHT(DC), DHT(AC), SOS
L2  PRED ← 0
L3  for each 8 × 8 block b in raster order   ▷ edge samples repeated to fill
L4      F ← FDCT(b − 128)
L5      S[k] ← round(F[k] / Q[k]) for k = 0 … 63
L6      z ← S read in zigzag order
L7      DIFF ← z[0] − PRED; PRED ← z[0]; write code(SSSS(DIFF)) and the SSSS extra bits
L8      write the AC run/size codes of z[1 … 63] with ZRL and EOB, each followed by its extra bits
L9  pad the last byte with 1-bits          ▷ 0x00 after each 0xFF, all along
L10 write EOI

JPEG-DECODE(bytes)
L11 read the marker segments up to SOS: Q from DQT, H and W from SOF0, the code tables from DHT
L12 for each block: s ← DECODE(DC table); PRED ← PRED + EXTEND(next s bits); z[0] ← PRED
L13     read (r, s) symbols: EOB ends, ZRL skips 16, else skip r zeros and place EXTEND(next s bits)
L14     R ← z in natural order times Q; b ← round(IDCT(R) + 128) clamped to 0 … 255
L15 crop the blocks to H × W and return the image
```

## Example

Take one block with $x(y, x) = 100 + 6x + 3y$, plus 20 in the right half ($x \ge 4$); its first row is 100, 106, 112, 118, 144, 150, 156, 162. After the level shift the nonzero DCT coefficients are $F(0,0) = 108$, $F(0,1) = -181.82$, $F(0,3) = 14.03$, $F(0,5) = -20.42$, $F(0,7) = 13.56$, $F(1,0) = -54.66$, $F(3,0) = -5.71$, $F(5,0) = -1.70$ and $F(7,0) = -0.43$, because the block is a sum of a function of $x$ and a function of $y$. Dividing by Table K.1 and rounding leaves five nonzero values:

$$S(0,0) = 7,\quad S(0,1) = -17,\quad S(1,0) = -5,\quad S(0,3) = 1,\quad S(0,5) = -1,$$

at zigzag positions 0, 1, 2, 6 and 15. The bits, with the tables of K.3.3:

| item | symbol | Huffman code | extra bits |
|---|---|---|---|
| DC, DIFF = 7 | SSSS = 3 | 100 | 111 |
| $-17$ at 1 | 0/5 | 11010 | 01110 |
| $-5$ at 2 | 0/3 | 100 | 010 |
| $1$ at 6 | 3/1 | 111010 | 1 |
| $-1$ at 15 | 8/1 | 111111000 | 0 |
| end | EOB | 1010 | |

That is 43 bits, padded with five 1-bits to the six bytes 9F 4E 8B AF E1 5F, instead of 64 bytes. The decoded first row is 98, 110, 109, 118, 145, 154, 153, 166: the step is smoothed into a ringing edge. The largest error is 6 and the MSE is 10.625, a PSNR of 37.87 dB.

## Correctness

The entropy-coded layer is lossless. Byte stuffing is undone exactly, the Huffman codes of Annex C form a prefix code that DECODE reads correctly, EXTEND inverts the extra bits, and the decoder keeps the same DC predictor and the same position in the block as the encoder. So the decoder obtains exactly the quantized values $S$.

The only loss is the rounding of line L5 and the final rounding to integers. Since the FDCT is orthonormal, each coefficient error $|F - SQ|$ is at most $Q/2$, and the samples of a block are off by at most $B + 4$ in Euclidean norm, with $B = \frac12 \sqrt{\sum Q^2}$. When the sides are multiples of 8 this gives MSE at most $(B + 4)^2 / 64$: PSNR at least 17.49 dB for Table K.1 and at least 48.13 dB when all steps are 1. The bound is loose. The proof also shows that the DC differences fit in category 11 and the AC values in category 10, as the baseline tables need.

## Complexity

Each block costs a constant amount of work: the separable DCT with the $8 \times 8$ matrix takes 1024 multiplications, and a [fast DCT](/fast-dct/) far fewer; quantization, the zigzag scan and the entropy coding take $O(64)$ steps plus one step per output bit. The number of blocks is $\lceil H/8 \rceil \lceil W/8 \rceil$, so encoding and decoding take $\Theta(n)$ time for $n = HW$ pixels. The coder on this page keeps the whole image, $\Theta(n)$ space; a streaming coder needs only 8 rows at a time.

## Properties

- **Lossy, with a lossless back end.** All loss is in the quantization; the Huffman layer is exact.
- **Fixed blocks, no overlap.** Errors are independent in each block, which gives blocking artifacts at large steps.
- **Not embedded.** A prefix of a baseline file decodes only the blocks it contains, at full quality. Progressive JPEG and [JPEG 2000](/jpeg-2000/) give rising quality instead.
- **Decoder not bit-exact.** The standard does not fix one exact integer IDCT; it allows any IDCT that meets an accuracy requirement, so two conforming decoders can differ slightly on some samples.
- **The quality factor is not in the standard.** The common scale from 1 to 100 comes from the Independent JPEG Group software: steps are multiplied by $5000/q$ percent for $q < 50$ and by $200 - 2q$ percent otherwise, and clamped to 1 to 255. The code here offers it as `scaled_table`.

## Variants and improvements

- **Colour.** Three components, usually Y, Cb and Cr with chroma subsampled 2:1 in one or both directions; one scan interleaves the blocks in minimum coded units (MCUs). Annex K gives Table K.2 for chrominance.
- **Optimized Huffman tables.** A first pass counts the symbols and builds tables limited to 16 bits (Annex K.2), which saves bits over the example tables.
- **Arithmetic coding.** T.81 also defines the QM coder, an adaptive binary [arithmetic coder](/arithmetic-coding/), in place of Huffman coding. It was little used.
- **Progressive mode.** Spectral selection sends bands of zigzag positions in separate scans; successive approximation sends the coefficients one bit plane at a time.
- **Extended and lossless modes.** 12-bit samples with the DCT, and a lossless mode with a [predictive coder](/predictive-coding/) instead of the DCT.
- **Restart markers.** RSTn markers every few MCUs reset the DC predictor, so that an error stops at the next marker.
- **Encoder-side gains.** Trellis quantization chooses the values $S$ to minimize rate plus distortion, and deblocking filters help at the decoder; both keep the baseline syntax.

## When to use it

Use baseline JPEG for photographs and other natural images when every decoder must read the file: it is supported almost everywhere, fast, and needs little memory. Do not use it for text, line art or screenshots, where the sharp edges ring and a lossless format does better, for images that need an exact copy, or for images with more than 8 bits per sample. For better quality at low rates, scalable streams or lossless and lossy coding in one format, see [JPEG 2000](/jpeg-2000/).

## Pitfalls

- **DQT in zigzag order.** The 64 steps in a DQT segment are in zigzag order, not row order.
- **Negative extra bits.** The extra bits of a negative value are those of $v - 1$, and EXTEND must test the first bit; a sign-magnitude reading decodes garbage.
- **Stuffing and fill bytes.** Each 0xFF in the entropy-coded data is followed by 0x00, which the decoder must drop. Before a marker, any number of 0xFF fill bytes may appear.
- **No EOB after position 63.** If the last coefficient is nonzero, the block ends without EOB.
- **ZRL only before a nonzero value.** Sixteen trailing zeros are coded by EOB, not by ZRL.
- **Partial blocks.** The encoder fills partial blocks; repeating the edge samples, as here, avoids a false edge that costs bits. The decoder crops to the size in SOF0.
- **Clamping.** The IDCT plus 128 can leave $[0, 255]$, so round and clamp.
- **No oracle in the standard library.** Python has no JPEG codec, so the tests check the generated Huffman codes against codewords copied from Annex K, the marker layout, the stuffing, a block coded by hand and the error bound, but no independent decoder. The tests use no official conformance data (ITU-T T.83).

## Implementations

## History

The Joint Photographic Experts Group, a joint committee of ISO and CCITT, began work on a standard for continuous-tone still images in the late 1980s and compared several proposals before it chose a method based on the $8 \times 8$ DCT (Wallace 1991). The DCT itself goes back to Ahmed, Natarajan and Rao (1974). The standard was approved as CCITT Recommendation T.81 in September 1992 and published by ISO as ISO/IEC 10918-1. It defines the baseline process, the extended, progressive, lossless and hierarchical processes, and both Huffman and arithmetic coding, but no file format; Eric Hamilton's JFIF (1992) filled that gap with an APP0 segment and a fixed YCbCr colour space. Pennebaker and Mitchell (1993) give the full account of the standard.

## References
