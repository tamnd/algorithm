---
tag: C0KDQE
kind: problem
slug: halftoning
name: Halftoning
aliases:
- dithering
- digital halftoning
area: graphics-and-signals/image-processing
level: advanced
summary: Render continuous tones with a small set of output levels by spatial patterns, so that the image blurred by the eye matches the input, as in black and white printing.
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Ω(W H)}
prereqs: [digital-image, image-thresholding]
see_also: [ordered-dithering, floyd-steinberg-dithering, color-quantization, scalar-quantization, gamma-correction, median-cut, octree-color-quantization]
sources:
  - book: isbn:9780262210096
    title: Robert Ulichney, Digital Halftoning, MIT Press, 1987
    locator: the whole book (the statement of the problem, the models of the eye, ordered dither and error diffusion, and their spectra)
  - paper: doi:10.1016/S0146-664X(76)80003-2
    title: J. F. Jarvis, C. N. Judice and W. H. Ninke, A survey of techniques for the display of continuous tone pictures on bilevel displays, Computer Graphics and Image Processing 5(1), 1976, 13 to 40
    locator: the whole survey (fixed thresholds, random and ordered dither, and minimized average error)
  - paper: "Robert W. Floyd and Louis Steinberg, An adaptive algorithm for spatial greyscale, Proceedings of the Society for Information Display 17(2), 1976, 75 to 77"
    locator: the whole paper (error diffusion with four weights)
  - paper: doi:10.1145/35039.35040
    title: Donald E. Knuth, Digital halftones by dot diffusion, ACM Transactions on Graphics 6(4), 1987, 245 to 273
    locator: the statement of the problem for printers, and the comparison of ordered dither, error diffusion and dot diffusion
  - paper: doi:10.1145/383259.383326
    title: Victor Ostromoukhov, A simple and efficient error-diffusion algorithm, Proceedings of SIGGRAPH 2001, 567 to 572
    locator: the error diffusion with weights that depend on the input level
---

Halftoning is the problem of showing an image with many gray levels on a device that has only a few, often only black and white. A printer puts ink or no ink, an e-paper screen shows a pixel dark or light, and a file format may store one binary digit per pixel. The answer is a pattern: in an area of gray $g$, about a fraction $g$ of the output pixels are on, spread so that the eye, which blurs fine detail, sees the gray and not the dots. A halftoning algorithm chooses that pattern for every pixel. Rounding each pixel to the nearest level, which is [image thresholding](/image-thresholding/), loses every gray in between; the two classic answers are [ordered dithering](/ordered-dithering/), which compares each pixel with a threshold from a tiled matrix, and [Floyd-Steinberg dithering](/floyd-steinberg-dithering/), which passes the error of each pixel to its neighbors.

## In plain words

A newspaper photo, seen through a magnifier, is made of black dots on white paper. Dark areas have big or many dots, light areas small or few. From a normal distance the eye merges the dots into shades of gray. Halftoning is the task of making such a dot picture from a gray picture. Each spot can only be black or white, so the method must decide which spots to fill so that every small area has the right share of black. The dots should also be spread so that they do not form lines, clumps or a visible grid. Doing this well, and fast, is the whole problem.

## Definition

**Input.** A [digital image](/digital-image/) $v$ with $H$ rows and $W$ columns of values in $[0, 1]$, linear in light intensity, and a finite set of output levels $\Lambda \subset [0, 1]$ that contains 0 and 1, usually $\Lambda = \{0, 1\}$.

**Output.** An image $q$ of the same size with every $q(x, y) \in \Lambda$.

**Goal.** The image $q$ seen by the eye looks like $v$. A common model writes the eye as a low-pass filter $h$, and asks for a small value of

$$
E(q) = \sum_{x, y} \big( (h * v)(x, y) - (h * q)(x, y) \big)^2,
$$

where $*$ is the convolution. A weaker but simpler measure asks that the mean of $q$ over every small window be close to the mean of $v$. Rounding each pixel alone minimizes $\sum (v - q)^2$, the measure without the filter, and is the wrong answer for halftoning.

## Variants

- **Two levels or several.** The two-level case is the classic one. For $m + 1$ levels, the same methods dither between the two levels next to each value.
- **Color.** Each channel can be halftoned on its own, as for the inks of a printer, or the output can be a palette from [color quantization](/color-quantization/), with the pattern chosen among the palette colors.
- **Dispersed or clustered dots.** On screens, single pixels show well, and the best patterns spread the on pixels as evenly as possible. On paper, single dots of ink do not print reliably, so the on pixels are grouped into round dots whose size grows with the gray.
- **Amplitude or frequency modulation.** Clustered dots on a regular grid vary the dot size (amplitude modulation). Dispersed patterns vary the number of dots in an area (frequency modulation).
- **Video.** The patterns of successive frames should not change where the image does not change, or the dots flicker.
- **Model-based halftoning.** Search directly for the $q$ that minimizes a measure such as $E(q)$, with a model of the eye and of the printer.

## Examples

**A gray of 1/3 on a 64 by 64 image.** The input sum is $4096/3 = 1365\tfrac{1}{3}$, so an ideal pattern has 1365 ones.

- **Thresholding** at $1/2$ sets every pixel to 0: no ones at all, and the image is black.
- **[Ordered dithering](/ordered-dithering/)** with a matrix of side $n$ turns on $\lceil n^2/3 - 1/2 \rceil$ pixels per tile: 1280 ones for $n = 4$, 1344 for $n = 8$ and 1360 for $n = 16$. Each tile is within half a pixel of $n^2/3$, but the error repeats in every tile.
- **[Floyd-Steinberg dithering](/floyd-steinberg-dithering/)** in raster order gives 1359 ones. The difference from $4096/3$ is exactly $19/3$, the error pushed off the border of the image.

**A gray of 1/2.** Both ordered dithering and Floyd-Steinberg dithering give a checkerboard, which is the finest pattern with half the pixels on.

## Known algorithms

| Method | Idea | Parallel | Pattern |
|---|---|---|---|
| [Image thresholding](/image-thresholding/) | round each pixel to the nearest level | yes | no gray between the levels |
| Random dither | add noise, then threshold | yes | grainy, with clumps |
| [Ordered dithering](/ordered-dithering/) | compare with a tiled threshold matrix, such as the Bayer matrix | yes | regular texture, exact count per tile |
| [Floyd-Steinberg dithering](/floyd-steinberg-dithering/) | scan and pass the error to four later neighbors | no | fine and irregular, worms on light and dark grays |
| Larger error filters | Jarvis, Judice and Ninke, and others, spread the error to twelve neighbors | no | smoother, slower |
| Variable error diffusion | Ostromoukhov chooses the weights per input level | no | fewer visible patterns |
| Dot diffusion | Knuth spreads the error by a class matrix instead of a scan | yes, in classes | between ordered and error diffusion |
| Blue noise masks | a large threshold array with no regular period | yes | close to error diffusion |
| Model-based search | change pixels while $E(q)$ goes down | no | the best quality, the slowest |

## Bounds

- **Time.** Every output pixel must be written, so any algorithm takes $\Omega(W H)$ time. Ordered dithering and error diffusion meet this bound, with $\Theta(W H)$ time.
- **Mean of a constant gray.** For a constant gray $g$, ordered dithering with a Bayer matrix of side $n$ is within $1/2$ of $g n^2$ in every aligned tile. Floyd-Steinberg dithering is within $(W + 2H)/2$ of $g W H$ over the whole image, by the conservation of the error proved on its page.
- **Levels of a tile.** A fixed $n \times n$ threshold matrix can show only $n^2 + 1$ distinct means on a tile, so a smooth ramp shows steps unless $n$ is large.

## Reductions

- **From [scalar quantization](/scalar-quantization/).** Halftoning is scalar quantization of each pixel to the levels $\Lambda$, with the extra goal that the errors of nearby pixels cancel. Error diffusion is a quantizer with feedback of the error.
- **With [color quantization](/color-quantization/).** A palette from [median cut](/median-cut/) or [octree quantization](/octree-color-quantization/) gives the output levels, and halftoning in color then dithers between the palette colors.
- **To image thresholding.** With a constant threshold matrix, ordered dithering is thresholding; with zero weights, error diffusion is rounding to the nearest level.

## Applications

- Printing with ink on paper, in newspapers, books and office printers.
- Two-level and few-level screens, such as e-paper and some small displays.
- Image formats and devices with a palette or few levels, such as GIF images, fax and old computer screens.
- Reducing the bit depth of an image without visible bands in smooth areas.

## References
