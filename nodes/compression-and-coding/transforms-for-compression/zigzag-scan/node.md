---
tag: 4K7DEC
kind: technique
slug: zigzag-scan
name: Zigzag scan
aliases:
- zig-zag ordering
- zigzag order of DCT coefficients
area: compression-and-coding/transforms-for-compression
level: intro
summary: "Read an 8 x 8 block of quantized DCT coefficients along its anti-diagonals, from low to high frequency, so that the zeros come last and run-length coding is short."
prereqs: [discrete-cosine-transform, run-length-encoding]
see_also: [jpeg-compression, transform-coding, scalar-quantization, huffman-coding, z-order-curve, energy-compaction]
sources:
  - url: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
    title: ITU-T Recommendation T.81 (09/92), Digital compression and coding of continuous-tone still images, Requirements and guidelines
    locator: Clause A.3.6 and Figure A.6, Zig-zag sequence of quantized DCT coefficients (page 30); Figure 5, Preparation of quantized coefficients for entropy encoding (page 16); Clause F.1.2.2, Huffman encoding of AC coefficients
  - paper: doi:10.1145/103085.103089
    title: Gregory K. Wallace, The JPEG still picture compression standard, Communications of the ACM 34(4), 1991
    locator: pages 30 to 44 (the zig-zag sequence and the entropy coding of the AC coefficients)
  - book: isbn:9780442012724
    title: William B. Pennebaker and Joan L. Mitchell, JPEG Still Image Data Compression Standard, Van Nostrand Reinhold, 1993
    locator: the chapters on the baseline DCT system and its Huffman coding
---

A zigzag scan reads the coefficients of a square block, such as the $8 \times 8$ [DCT](/discrete-cosine-transform/) block of JPEG, along its anti-diagonals from the top left (low frequency) to the bottom right (high frequency), changing direction on each diagonal. After quantization most high-frequency coefficients are zero, so the zigzag order puts them in one long run at the end. [Run-length coding](/run-length-encoding/) of that list then needs only a few (run, value) pairs and one end-of-block code. The order is fixed by ITU-T T.81, Figure A.6.

## In plain words

After the DCT, the number at the top left of a block says how bright the block is on average. Numbers further to the right describe finer detail across the block, and numbers further down describe finer detail from top to bottom. After rounding, the fine detail is almost always zero.

To send the block, you must put the 64 numbers in a line. If you read row by row, the zeros at the end of each row break up the useful numbers. If you read in slanted lines from the top left corner, going down one line and up the next, you meet the coarse detail first and the fine detail last. So all the zeros come together at the end, and you can replace them by one short "end of block" sign.

## When it applies

Use a zigzag scan when a block of quantized transform coefficients must become a one-dimensional list for an entropy coder, and the chance that a coefficient is zero grows with its frequency in both directions. This is the case for the 2D DCT of natural images in [transform coding](/transform-coding/): [energy compaction](/energy-compaction/) puts the large coefficients near the top left, and a [scalar quantizer](/scalar-quantization/) with larger steps at high frequencies sets most others to zero.

**Definition.** Let position $(r, c)$ of an $n \times n$ block hold the coefficient of vertical frequency $r$ and horizontal frequency $c$, with $0 \le r, c < n$. Diagonal $s$ is the set of positions with $r + c = s$, for $s = 0, 1, \ldots, 2n - 2$. The zigzag scan visits the diagonals in order of $s$. Inside diagonal $s$ it visits the positions by increasing $r$ when $s$ is odd, and by decreasing $r$ when $s$ is even. This gives the JPEG order: $(0,0)$, then $(0,1)$, $(1,0)$, then $(2,0)$, $(1,1)$, $(0,2)$, and so on. Each diagonal ends at an edge of the block, and the next one starts at a neighbouring position on that edge, so each step moves to an adjacent cell, either along the diagonal or one step along an edge.

**The run-length step.** T.81 codes the first entry, the DC coefficient, on its own as the difference from the DC of the previous block. The other 63 entries, the AC coefficients in zigzag order, become pairs (RRRR, value): RRRR is the number of zeros before the next nonzero value, from 0 to 15. A run of 16 or more zeros is cut by the code ZRL, which stands for 16 zeros, and the last run of zeros of the block is replaced by EOB (end of block). Each pair is sent as a Huffman code for the byte RRRRSSSS, where SSSS is the size category of the value, followed by SSSS extra bits (T.81, Clause F.1.2.2 and Figure 5). If the last coefficient, position 63, is nonzero, no EOB is sent.

## The template

```pseudo id=main
ZIGZAG-ORDER(n)                         ▷ the positions of an n × n block in scan order
L1  order ← empty list
L2  for s ← 0 to 2n − 2                 ▷ one anti-diagonal r + c = s
L3      lo ← max(0, s − n + 1); hi ← min(s, n − 1)
L4      rows ← lo, lo + 1, …, hi if s is odd, else hi, hi − 1, …, lo   ▷ hole: the direction rule
L5      for r in rows
L6          append (r, s − r) to order
L7  return order
```

The scan costs $\Theta(n^2)$ time, one step per position, and in practice it is a table of 64 entries. The order is a permutation: each position $(r, c)$ lies on exactly one diagonal $s = r + c$, and lines L3 and L4 list each row of that diagonal once. The run-length step is one pass over the 63 AC entries, also linear.

**The holes.** The direction rule of line L4 (which diagonal goes down first), the block shape (square, or a rectangle with a different scan), and the scan table itself, which a coder may replace for interlaced video or for a known direction of the content.

### Worked example

Take an $8 \times 8$ block of quantized coefficients that is zero except for $12$ at $(0,0)$, $5$ at $(0,1)$, $-3$ at $(1,0)$, $1$ at $(2,2)$ and $2$ at $(3,5)$. Figure A.6 of T.81 gives the zigzag index of each position:

| $r \backslash c$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 5 | 6 | 14 | 15 | 27 | 28 |
| 1 | 2 | 4 | 7 | 13 | 16 | 26 | 29 | 42 |
| 2 | 3 | 8 | 12 | 17 | 25 | 30 | 41 | 43 |
| 3 | 9 | 11 | 18 | 24 | 31 | 40 | 44 | 53 |
| 4 | 10 | 19 | 23 | 32 | 39 | 45 | 52 | 54 |
| 5 | 20 | 22 | 33 | 38 | 46 | 51 | 55 | 60 |
| 6 | 21 | 34 | 37 | 47 | 50 | 56 | 59 | 61 |
| 7 | 35 | 36 | 48 | 49 | 57 | 58 | 62 | 63 |

So the list is $12, 5, -3$, then nine zeros (indices 3 to 11), then $1$ at index 12, then 27 zeros (13 to 39), then $2$ at index 40, then 23 zeros. The DC value 12 is coded apart. The AC pairs are

$$(0, 5),\ (0, -3),\ (9, 1),\ \text{ZRL},\ (11, 2),\ \text{EOB}.$$

The run of 27 zeros becomes ZRL (16 zeros) and a run of 11. The zigzag order does not win on every block. A row-by-row scan of this block gives $(0, 5), (6, -3), (9, 1), (10, 2)$, EOB, which is one symbol fewer, because the value at $(3, 5)$ is far from the corner. The zigzag order wins on typical blocks, where the nonzero values fill a triangle near the top left corner.

## Classic examples

- [JPEG](/jpeg-compression/) baseline and progressive modes (T.81): the $8 \times 8$ zigzag order of Figure A.6, before the run-length and [Huffman](/huffman-coding/) coding of the AC coefficients. The progressive mode cuts the same order into spectral bands.
- MPEG-1, MPEG-2 and H.261: the same $8 \times 8$ zigzag order for intra and inter blocks. MPEG-2 adds an alternate scan for interlaced pictures, which goes down the columns faster.
- H.264: a $4 \times 4$ zigzag scan for frame blocks and a field scan for field blocks, before CAVLC or [CABAC](/cabac/).
- [Transform coding](/transform-coding/) of other 2D data, such as the DCT blocks of some audio and video codecs, uses the same idea: sort the coefficients by expected magnitude.

## Variations

- **Adaptive and alternate scans.** A coder picks one of several fixed scans per block, or reorders the scan by the measured frequency of nonzero values. HEVC uses diagonal, horizontal and vertical scans of $4 \times 4$ groups.
- **Rectangular blocks.** The same rule works on an $m \times n$ block: visit the diagonals $r + c = s$ in order and alternate the direction; only the bounds of line L3 change to $\max(0, s - n + 1)$ and $\min(s, m - 1)$.
- **Significance maps instead of runs.** [CABAC](/cabac/) codes, in scan order, one flag per coefficient saying whether it is nonzero and one flag saying whether it is the last nonzero one. The scan order still matters, because it makes the flags predictable for [context modeling](/context-modeling/).
- **Not the Z-order curve.** The [Z-order curve](/z-order-curve/) (Morton order) also maps a 2D grid to a line, but it interleaves the binary digits of the two coordinates to keep nearby cells close. It does not sort by frequency, and coders do not use it for this purpose.

## Pitfalls

- **Row and column.** T.81 writes the block with the horizontal frequency across. Swapping $r$ and $c$ gives the transposed scan, $(0,0), (1,0), (0,1), \ldots$, which decodes to a transposed image if the decoder uses the standard order.
- **Natural order in DQT.** The quantization tables in a JPEG file are also stored in zigzag order, not in row order. Writing them in row order gives a valid file that decodes with the wrong steps.
- **A trailing EOB.** No EOB follows when coefficient 63 is nonzero; a decoder that always reads an EOB loses its place.
- **ZRL before EOB.** A run of zeros that reaches the end of the block is one EOB, not a series of ZRL codes. An encoder that writes ZRL first produces a longer but still valid stream; a decoder must accept it.
- **The scan does not compress.** It only reorders. All the gain comes from the run-length and entropy coding that follow, and it depends on the quantizer having made the high frequencies zero.

## Exercises

1. Show that the zigzag order of an $n \times n$ block visits position $(r, c)$ at index $s(s+1)/2 + k$ for $s = r + c < n$, where $k = r$ for odd $s$ and $k = c$ for even $s$.
2. Write the inverse of the run-length step and show that it rebuilds the 63 AC values from any list made by the encoder, including the list with ZRL codes and no EOB.
3. For a block whose nonzero values fill the triangle $r + c \le t$, how many zeros come before the last nonzero value in zigzag order, and how many in row order?

## References
