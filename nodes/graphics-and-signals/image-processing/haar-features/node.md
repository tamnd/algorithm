---
tag: 28YD6A
kind: concept
slug: haar-features
name: Haar-like features
aliases:
- Haar features
- Haar wavelet features
area: graphics-and-signals/image-processing
level: advanced
summary: Differences of the pixel sums of two, three or four adjacent equal rectangles in a window, each computed from an integral image in a constant number of reads at any position and scale.
prereqs: [integral-image]
see_also: [viola-jones-detector, haar-wavelet, haar-wavelet-transform, face-detection, adaboost, decision-stump, box-blur, two-dimensional-prefix-sums]
sources:
  - paper: doi:10.1023/B:VISI.0000013087.49260.fb
    title: Paul Viola and Michael J. Jones, Robust real-time face detection, International Journal of Computer Vision 57(2), 137-154, 2004
    locator: Section 2 and Figure 1 (the two-, three- and four-rectangle features), Section 2.1 (the integral image and the 6, 8 and 9 array references), Section 5.4 (variance normalization)
  - paper: doi:10.1109/ICCV.1998.710772
    title: Constantine P. Papageorgiou, Michael Oren and Tomaso Poggio, A general framework for object detection, Sixth International Conference on Computer Vision, 555-562, 1998
    locator: the whole paper (an overcomplete set of Haar wavelets as features for detection)
  - paper: doi:10.1109/ICIP.2002.1038171
    title: Rainer Lienhart and Jochen Maydt, An extended set of Haar-like features for rapid object detection, IEEE International Conference on Image Processing, vol. 1, I-900 to I-903, 2002
    locator: the whole paper (features turned by 45 degrees, center-surround features, and the rotated integral image)
  - paper: doi:10.1145/964965.808600
    title: Franklin C. Crow, Summed-area tables for texture mapping, ACM SIGGRAPH Computer Graphics 18(3), 207-212, 1984
    locator: the whole paper (the table of sums and the four-corner rule for a rectangle)
  - paper: doi:10.1016/j.cviu.2007.09.014
    title: Herbert Bay, Andreas Ess, Tinne Tuytelaars and Luc Van Gool, Speeded-up robust features (SURF), Computer Vision and Image Understanding 110(3), 346-359, 2008
    locator: the whole paper (Haar wavelet responses on an integral image for the orientation and the descriptor)
---

Haar-like features are simple numbers computed from a rectangular window of a gray image. Each one is the pixel sum of some rectangles minus the pixel sum of other, adjacent rectangles of the same size. A two-rectangle feature responds to an edge between its halves, a three-rectangle feature to a bar, and a four-rectangle feature to a diagonal pattern. With an [integral image](/integral-image/), any such feature costs 6, 8 or 9 table reads, whatever its size and position. They are called Haar-like because the two-rectangle pattern is a box form of the [Haar wavelet](/haar-wavelet/). Papageorgiou, Oren and Poggio used Haar wavelets as features for detection in 1998, and Viola and Jones made the rectangle features and their fast evaluation the base of the [Viola-Jones detector](/viola-jones-detector/).

## In plain words

Look at a small gray picture of a face. The band across the eyes is darker than the band across the cheeks under it. The bridge of the nose is lighter than the eyes on both sides. You can turn such facts into numbers: add up all the pixels in one box, add up the pixels in the box next to it, and subtract. A large result means that one box is much brighter than the other. Each choice of boxes, of their size and of their place in the picture gives one such number. There are a very large number of choices, and each one is a weak clue. A learning method picks the few clues that best tell faces from other things. A prepared table of running sums makes every box sum take only four lookups, so the clues are cheap.

## The idea

**Model.** The window is part of a gray [digital image](/digital-image/) $I$ with one channel of integer values, for example 0 to 255, used as they are stored with no gamma step. Pixel $(x, y)$ has its center at the integer point $(x, y)$, with $x$ to the right and $y$ down. A rectangle $[x_0, x_1) \times [y_0, y_1)$ is the set of pixels with $x_0 \le x < x_1$ and $y_0 \le y < y_1$. Features lie fully inside the window and the window inside the image, so no border rule is needed.

**The five basic kinds.** A feature has a kind, a corner $(x, y)$ in the window and a cell size $w \times h$. All cells of a feature have the same size, and the weights are $+1$ or $-1$:

| Kind | Cells | Value |
|---|---|---|
| two-rectangle, horizontal | $2 \times 1$ | left minus right |
| two-rectangle, vertical | $1 \times 2$ | top minus bottom |
| three-rectangle, horizontal | $3 \times 1$ | center minus the two outer cells |
| three-rectangle, vertical | $1 \times 3$ | center minus the two outer cells |
| four-rectangle | $2 \times 2$ | one diagonal pair minus the other |

In general a feature is $f = \sum_i \omega_i \,\mathrm{sum}(c_i)$ over its cells $c_i$ with weights $\omega_i$. This is the inner product of the window with a kernel that is $\omega_i$ on cell $c_i$ and $0$ elsewhere. For the two-rectangle kinds the kernel is, up to a factor, the Haar wavelet of the [Haar wavelet transform](/haar-wavelet-transform/) on a box, and the four-rectangle kernel is the product of a horizontal and a vertical Haar function. The rectangle features are not a basis: there are far more of them than pixels, and they overlap.

**Fast evaluation.** Let $S(x, y) = \sum_{j < y} \sum_{i < x} I(i, j)$ be the integral image, the table of [two-dimensional prefix sums](/two-dimensional-prefix-sums/). Then

$$\mathrm{sum}([x_0, x_1) \times [y_0, y_1)) = S(x_1, y_1) - S(x_0, y_1) - S(x_1, y_0) + S(x_0, y_0).$$

Adjacent cells share corners, so after the coefficients of equal corners are added, a two-rectangle feature needs 6 reads, a three-rectangle feature 8 and a four-rectangle feature 9. The cost does not depend on $w$ and $h$. So a detector can scale its features, not the image: a feature at scale $s$ has its corner and cell size multiplied by $s$ and costs the same number of reads.

**How many there are.** For a pattern of $a \times b$ cells in an $n \times n$ window, the cell width $w$ runs from 1 to $\lfloor n/a \rfloor$ with $n - aw + 1$ positions, and the same along $y$, so the number of features is

$$N_{a,b}(n) = \Big(\sum_{w=1}^{\lfloor n/a \rfloor} (n - aw + 1)\Big) \Big(\sum_{h=1}^{\lfloor n/b \rfloor} (n - bh + 1)\Big).$$

For $n = 24$ this gives $43{,}200$ for each two-rectangle kind, $27{,}600$ for each three-rectangle kind and $20{,}736$ for the four-rectangle kind, $162{,}336$ in all. Viola and Jones give "160,000" for this window in 2004 and "over 180,000" in 2001; the counts differ with the rules for which shapes and sizes are allowed.

**Brightness and contrast.** A feature is linear in the pixels. Multiplying the window by $c$ multiplies every feature by $c$, so detectors divide each feature by the standard deviation $\sigma$ of the window, which an integral image of $I^2$ gives in $O(1)$; this removes the gain for $c > 0$. Adding $b$ to every pixel changes a feature by $b \sum_i \omega_i |c_i|$, where $|c_i|$ is the area of a cell. The weights of the two- and four-rectangle features sum to zero, so these do not change. The three-rectangle feature with weights $-1, +1, -1$ on equal cells does not: it changes by $-b\,wh$. Lienhart and Maydt write each feature as a weighted sum of two rectangles with weights that make the areas cancel; for the three-rectangle feature this is the same as weight $+2$ on the center and $-1$ on the outer cells.

**Extensions.** Lienhart and Maydt add features turned by $45°$, whose cells are evaluated with a second, rotated table of sums, and center-surround features. All of them keep the constant cost.

## Examples

**The integral image of a ramp.** Take the $4 \times 4$ patch with values $1$ to $16$ row by row, so $I(x, y) = 1 + x + 4y$. Its integral image, with rows $y = 0$ to $4$ and columns $x = 0$ to $4$, is

$$S = \begin{pmatrix} 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 3 & 6 & 10 \\ 0 & 6 & 14 & 24 & 36 \\ 0 & 15 & 33 & 54 & 78 \\ 0 & 28 & 60 & 96 & 136 \end{pmatrix}.$$

**A two-rectangle feature in 6 reads.** Let the horizontal two-rectangle feature have corner $(0, 1)$ and cells of $2 \times 2$. The left cell holds $5, 6, 9, 10$ with sum $30$, and the right cell holds $7, 8, 11, 12$ with sum $38$, so the value is $-8$. From the table, the left cell is $S(2, 3) - S(0, 3) - S(2, 1) + S(0, 1) = 33 - 0 - 3 + 0$ and the right cell is $S(4, 3) - S(2, 3) - S(4, 1) + S(2, 1) = 78 - 33 - 10 + 3$. In the difference, the shared corners $(2, 1)$ and $(2, 3)$ get the coefficients $-2$ and $+2$:

$$f = S(0, 1) - 2S(2, 1) + S(4, 1) - S(0, 3) + 2S(2, 3) - S(4, 3) = 0 - 6 + 10 - 0 + 66 - 78 = -8.$$

**What the features see on a ramp.** On this ramp each pixel of the right cell is $w$ larger than its partner in the left cell, so the horizontal two-rectangle feature is $-w \cdot wh = -w^2 h$ at every position, here $-8$: it measures the slope along $x$. The four-rectangle feature is $0$ at every position, because a linear ramp has no diagonal change. With cells of $1 \times 1$ at the corner $(0, 0)$ the five kinds give $1 - 2 = -1$, $1 - 5 = -4$, $-1 + 2 - 3 = -2$, $-1 + 5 - 9 = -5$ and $1 - 2 - 5 + 6 = 0$.

**The offset of the three-rectangle feature.** The vertical three-rectangle feature with corner $(1, 0)$ and cells of $2 \times 1$ has the cells $\{2, 3\}$, $\{6, 7\}$ and $\{10, 11\}$, so it is $-5 + 13 - 21 = -13$. On a ramp the two outer cells add up to twice the center, so the value is minus the center sum and changes with the brightness: adding $b$ to every pixel changes it by $-2b$. With the weights $-1, +2, -1$ the value is $-5 + 26 - 21 = 0$, as it should be for a pattern with no bar in it.

## Where it is used

- **Cascade detectors.** The [Viola-Jones detector](/viola-jones-detector/) uses [AdaBoost](/adaboost/) to choose a few features from all of them, each with a threshold, as a [decision stump](/decision-stump/), for [face detection](/face-detection/) and for other rigid object classes.
- **Detection with Haar wavelets.** Papageorgiou, Oren and Poggio used an overcomplete set of Haar wavelets as the input of a support vector machine that detects faces and people.
- **Descriptors.** SURF computes the responses of horizontal and vertical Haar wavelets on an integral image to find the orientation of a feature point and to build its descriptor.
- **Fast filters.** Box sums are the base of the [box blur](/box-blur/) and of other filters that use an integral image, and two-rectangle differences are a cheap gradient at a large scale.
- **Limits.** The features are aligned with the axes and respond to coarse patterns of light and dark. They do not describe texture or fine shape well, and learned detectors based on convolutional neural networks have replaced them in most new systems.

## References
