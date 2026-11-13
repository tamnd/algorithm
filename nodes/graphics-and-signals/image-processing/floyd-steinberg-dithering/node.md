---
tag: DDE4HS
kind: algorithm
slug: floyd-steinberg-dithering
name: Floyd-Steinberg dithering
aliases:
- Floyd-Steinberg dithering
- error diffusion dithering
area: graphics-and-signals/image-processing
level: advanced
summary: Scan the image, set each pixel to the nearest output level, and pass its error to the four neighbors not yet done with weights 7/16, 3/16, 5/16 and 1/16, so the local mean is kept.
solves: [halftoning]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H), average: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(W)}
properties: {deterministic: true, exact: false, sequential: true, mean_preserving: true, in_place: true}
history:
  year: 1976
  people: [Robert W. Floyd, Louis Steinberg]
  note: Floyd and Steinberg published the four weights 7/16, 3/16, 5/16 and 1/16 in their paper on an adaptive algorithm for spatial grayscale, for display on two-level screens.
prereqs: [halftoning, image-thresholding]
see_also: [ordered-dithering, color-quantization, median-cut, octree-color-quantization, gamma-correction, digital-image, scalar-quantization]
sources:
  - paper: "Robert W. Floyd and Louis Steinberg, An adaptive algorithm for spatial greyscale, Proceedings of the Society for Information Display 17(2), 1976, 75 to 77"
    locator: the whole paper (the scan order, the four weights and the two-level output)
  - book: isbn:9780262210096
    title: Robert Ulichney, Digital Halftoning, MIT Press, 1987
    locator: the chapters on error diffusion (the Floyd-Steinberg weights, the serpentine raster, the artifacts of the plain raster and the spectral analysis of the patterns)
  - paper: doi:10.1016/S0146-664X(76)80003-2
    title: J. F. Jarvis, C. N. Judice and W. H. Ninke, A survey of techniques for the display of continuous tone pictures on bilevel displays, Computer Graphics and Image Processing 5(1), 1976, 13 to 40
    locator: the section on minimized average error, with the larger diffusion filter over twelve neighbors
  - paper: doi:10.1145/35039.35040
    title: Donald E. Knuth, Digital halftones by dot diffusion, ACM Transactions on Graphics 6(4), 1987, 245 to 273
    locator: the comparison of dot diffusion with error diffusion, and the parallel order of the class matrix
---

Floyd-Steinberg dithering turns an image with many gray levels into one with a few, often only black and white, so that the local mean brightness stays the same. It visits the pixels in raster order. Each pixel is set to the nearest output level, and the error, the value minus the chosen level, is not thrown away: it is added to the four neighbors that come later, with the weights $7/16$ to the next pixel in the row and $3/16$, $5/16$ and $1/16$ to the three pixels below. The method is the classic *error diffusion* algorithm for the [halftoning](/halftoning/) problem. Every unit of error ends up in a later pixel or off the image, so the sum of the output differs from the sum of the input only by the error pushed off the border.

## In plain words

Suppose a printer can put only black or white dots, and the image has a medium gray. Look at the first pixel and choose black or white, whichever is closer. You made a mistake: the pixel is too dark or too light by some amount. Do not forget that amount. Give most of it to the next pixel in the row and the rest to the three pixels below, so that they lean the other way when their turn comes. Then go on to the next pixel and do the same. Over a small area, the too-dark and too-light choices cancel, and from a distance the eye sees the right gray. The pattern of dots is fine and irregular, which looks better than a fixed grid.

## The problem

The input is a gray [digital image](/digital-image/) $v$ with $H$ rows and $W$ columns of values in $[0, 1]$, linear in light intensity, and a set of output levels, usually $\{0, 1\}$. The output is an image $q$ with each pixel at one of the levels, such that $q$ blurred by the eye looks like $v$. The local mean of $q$ should match the local mean of $v$; the [halftoning](/halftoning/) page gives the measures.

## The algorithm

```pseudo id=main
FLOYD-STEINBERG(v, levels)
L1  v′ ← a copy of v                                    ▷ the values with the errors added so far
L2  for y ← 0 to H − 1 do
L3      for x ← 0 to W − 1 do                           ▷ right to left on odd rows, in the serpentine order
L4          q(x, y) ← the level nearest to v′(x, y)     ▷ a tie goes to the higher level
L5          e ← v′(x, y) − q(x, y)
L6          for (dx, dy, w) in (1, 0, 7/16), (−1, 1, 3/16), (0, 1, 5/16), (1, 1, 1/16) do
L7              if (x + dx, y + dy) is inside the image then v′(x + dx, y + dy) ← v′(x + dx, y + dy) + w e
L8              else lost ← lost + w e                  ▷ the error pushed off the image
L9  return q
```

In the serpentine order, line L3 runs right to left on odd rows and each $dx$ in line L6 changes its sign, so the error always goes ahead in the direction of the scan. The variable `lost` is not needed for the output; it is kept here because it makes the exact balance of Claim 1 below visible. An implementation needs only the current row and the next row of $v'$, which is the $\Theta(W)$ extra space.

The weights, as a picture, with $\ast$ the current pixel and the scan from left to right:

$$
\frac{1}{16}
\begin{pmatrix}
\cdot & \ast & 7 \\
3 & 5 & 1
\end{pmatrix}
$$

## Example

**A 3 by 2 image of gray 1/2, output levels 0 and 1.**

- **Pixel (0, 0).** $v' = 1/2$, a tie, so $q = 1$ and $e = -1/2$. It sends $-7/32$ to the right, $-5/32$ and $-1/32$ to the pixels below and below right, and $-3/32$ off the left border.
- **Pixel (1, 0).** $v' = 1/2 - 7/32 = 9/32$, so $q = 0$ and $e = 9/32$.
- **Pixel (2, 0).** $v' = 1/2 + \frac{7}{16} \cdot \frac{9}{32} = 319/512$, so $q = 1$ and $e = -193/512$.
- **Pixel (0, 1).** $v' = 1/2 - 5/32 + \frac{3}{16} \cdot \frac{9}{32} = 203/512$, so $q = 0$.

The output is $\begin{pmatrix} 1 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}$, three ones for an input sum of 3, and the error pushed off the image adds up to exactly 0.

**Larger gray fields.** An $8 \times 8$ field of $1/2$ gives a perfect checkerboard with 32 ones. A $64 \times 64$ field of $1/3$ gives 1359 ones, against $4096/3 = 1365\tfrac{1}{3}$; the difference, $19/3$, is exactly the error pushed off the border, as Claim 1 says.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows two facts, for the raster and the serpentine orders. **Claim 1 (conservation).** $\sum v - \sum q = \text{lost}$ exactly: the input sum minus the output sum is the error that lines L8 push off the image. **Claim 2 (bounded error).** For the levels $\{0, 1\}$ and an input in $[0, 1]$, every error $e$ of line L5 lies in $[-1/2, 1/2]$ and every $v'$ in $[-1/2, 3/2]$; for $m + 1$ equally spaced levels from 0 to 1, $|e| \le 1/(2m)$. As a consequence, only the pixels of the last row and of the first and last columns push error off, each at most $1/2$, so the count of ones on a constant gray $g$ differs from $g W H$ by at most $(W + 2H)/2$. The tests check both claims in exact fractions on random images with seed 8.

## Complexity

- **Time.** Each pixel does one decision and four additions, so the time is $\Theta(W H)$ in the [real RAM](/real-ram/). With integer values from 0 to 255, the weights are a multiplication and a shift by 4.
- **Space.** Two rows of $v'$, $\Theta(W)$, or in place in the image.
- **Order.** Each pixel depends on the one before it in the row, so the loop is sequential. A wavefront order that runs each row two pixels behind the one above allows about $\min(H, W/2)$ pixels at a time.

## Properties

- **Mean preserving.** By Claim 1, the total brightness is kept except at the border, and the same holds for any window, up to the error that crosses the boundary of the window.
- **Bounded error.** By Claim 2, the error carried by a pixel never exceeds half a step.
- **Blue noise.** On mid grays the dots form an irregular pattern with little energy at low spatial frequencies, which the eye does not see as a texture.
- **Sharpening.** The diffusion also enhances edges, because the error of a bright side flows into the dark side.
- **Not shift invariant.** The result depends on the scan order and on the position of the image on the grid.

## Variants and improvements

- **Serpentine scan.** Alternate the direction of the rows, which breaks up the diagonal artifacts of the plain raster. Ulichney recommended it.
- **Larger filters.** Jarvis, Judice and Ninke spread the error over twelve neighbors in the current row and the two rows below, with weights that add up to 48, which gives smoother but slower results; Stucki and others proposed other filters of that size.
- **Partial diffusion.** Atkinson's method, used on early Macintosh computers, passes only part of the error, which gives more contrast and loses detail in dark and bright areas.
- **Variable weights.** Ostromoukhov chose the weights per input level to reduce the visible patterns.
- **Threshold modulation.** Add a small noise or a pattern to the threshold, which breaks up the regular patterns near 0, 1/2 and 1.
- **Color.** Diffuse a vector error in RGB and choose the nearest color of a palette from [median cut](/median-cut/) or an [octree](/octree-color-quantization/), which is error diffusion for [color quantization](/color-quantization/).
- **Dot diffusion.** Knuth's method spreads the error by a class matrix instead of a scan, so the pixels can be done in parallel, with a pattern closer to [ordered dithering](/ordered-dithering/).

## When to use it

Use Floyd-Steinberg dithering to show an image on a device or in a format with few levels or few colors, such as a two-level screen, an e-paper display, a fax or a GIF with a palette, when the image is still and the pixels are small. Use [ordered dithering](/ordered-dithering/) when each pixel must be decided on its own, for parallel hardware, for video where error diffusion makes patterns that flicker from frame to frame, or for printers that need clustered dots.

## Pitfalls

- **Gamma.** The values must be linear in light. Dithering values that are coded with [gamma correction](/gamma-correction/) makes midtones too dark or too light.
- **Clipping $v'$.** Clamping $v'$ to $[0, 1]$ before the decision breaks the balance of Claim 1 and makes dark and bright areas lose detail; it is a choice, not a fix.
- **Rounding the shares.** With integers, the four shares of $e$ computed as $\lfloor 7e/16 \rfloor$ and so on do not add up to $e$. Give the remainder to the last share, or keep the errors at a higher precision.
- **Worms and patterns.** On light and dark grays, the dots can line up in worm-like chains, and near simple fractions such as $1/2$ and $1/3$ they form regular patterns. The serpentine scan and threshold modulation help.
- **Video.** A small change in one pixel can change the dots of the whole rest of the image, which flickers in animation.
- **Palette search.** In color, the nearest palette color must be found for $v'$, which may lie outside the cube; a map built for the original colors may not cover it.

## Implementations

## History

Floyd and Steinberg presented error diffusion in 1975 and published it in 1976 in the Proceedings of the Society for Information Display, with the four weights 7/16, 3/16, 5/16 and 1/16. In the same year Jarvis, Judice and Ninke surveyed the techniques for showing continuous tones on two-level displays and gave a larger filter. Ulichney's book of 1987 analyzed the patterns in the frequency domain and recommended the serpentine raster, and his later work named the good patterns blue noise. Knuth proposed dot diffusion in 1987 as a parallel alternative, and Ostromoukhov in 2001 made the weights depend on the input level.

## References
