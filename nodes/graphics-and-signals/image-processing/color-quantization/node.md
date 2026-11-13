---
tag: 5RJJ90
kind: problem
slug: color-quantization
name: Color quantization
aliases:
- palette generation
area: graphics-and-signals/image-processing
level: advanced
summary: Choose a palette of k colors and map each pixel to one of them so that the image changes little, usually by the total squared error, which is the k-means problem on the pixel colors.
model: real-ram
complexity:
  vars: {n: the number of pixels, k: the palette size}
  time: {worst: Ω(n)}
prereqs: [digital-image, k-means-problem]
see_also: [median-cut, octree-color-quantization, k-means, vector-quantization, halftoning, floyd-steinberg-dithering, k-means-np-hardness, self-organizing-map]
sources:
  - paper: doi:10.1145/965145.801294
    title: Paul Heckbert, Color image quantization for frame buffer display, ACM SIGGRAPH Computer Graphics 16(3), 1982, 297 to 307
    locator: the statement of the problem for frame buffers with a color map, the popularity and median cut algorithms, and the mapping of pixels to the nearest color
  - url: https://www.cs.cmu.edu/~ph/ciq_thesis
    title: Paul S. Heckbert, Color image quantization for frame buffer display, bachelor's thesis, Department of Mathematics, Massachusetts Institute of Technology, May 1980
    locator: the sections on optimal quantization (the dynamic program for one dimension and the remark that an efficient optimal algorithm in several dimensions seems unlikely) and Algorithms for 3-D Quantization
  - paper: doi:10.1016/j.tcs.2010.05.034
    title: Meena Mahajan, Prajakta Nimbhorkar and Kasturi Varadarajan, The planar k-means problem is NP-hard, Theoretical Computer Science 442, 2012, 13 to 21
    locator: the main theorem (k-means in the plane, with k part of the input, is NP-hard)
  - paper: doi:10.1145/146443.146475
    title: Xiaolin Wu, Color quantization by dynamic programming and principal analysis, ACM Transactions on Graphics 11(4), 1992, 348 to 372
    locator: the formulation as minimum squared error partition of the color histogram, and the reduction to optimal one-dimensional problems along principal axes
  - paper: doi:10.1109/TIT.1982.1056489
    title: Stuart P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982, 129 to 137
    locator: the two conditions of an optimal quantizer (nearest level and centroid) and the iteration that alternates them
---

Color quantization is the problem of showing an image with a small palette of $k$ colors, often 256 or 16. An algorithm chooses the palette, and maps each pixel to one palette color, so that the result looks like the original. The usual measure is the total squared distance between each pixel color and its palette color. With that measure the problem is the [k-means problem](/k-means-problem/) on the $n$ pixel colors, weighted by how often each color occurs: the best palette color of a group is its mean, and the best group of a color is its nearest palette color. The problem is [NP-hard](/k-means-np-hardness/) for points in the plane when $k$ is part of the input, so practical methods such as [median cut](/median-cut/), [octree quantization](/octree-color-quantization/) and [k-means](/k-means/) iterations are heuristics. Gray images, with one channel, have an exact dynamic program.

## In plain words

An old display or a GIF file can show only a few colors at once, say 256, but a photo may hold a hundred thousand. Color quantization picks the few colors to keep and decides, for each pixel, which kept color to use. A good choice spends many colors where the photo has many similar shades, such as skin or sky, and few where colors are rare. The usual score adds up, over all pixels, how far each pixel moves in color. Finding the best possible choice is very hard when the palette is large, so programs use fast methods that give a good choice, not the best one. Mixing nearby palette colors in small patterns, called dithering, can then hide the steps between them.

## Definition

The input is a list of $n$ colors $c_1, \ldots, c_n$, one per pixel of a [digital image](/digital-image/), each a point of a color space $\mathbb{R}^d$ (usually RGB with $d = 3$ and integer values from 0 to 255), and a palette size $k \ge 1$. The output is a palette $P = \{p_1, \ldots, p_k\} \subset \mathbb{R}^d$ and a map $j : \{1, \ldots, n\} \to \{1, \ldots, k\}$. The *squared error* is

$$
\mathrm{SSE}(P, j) = \sum_{i=1}^{n} |c_i - p_{j(i)}|^2 .
$$

The *minimum squared error* problem asks for $P$ and $j$ with the least SSE. Two facts reduce it to a search over partitions. For a fixed palette, the best map takes each pixel to its nearest palette color. For a fixed partition of the pixels into $k$ groups, the best palette color of a group is its mean. So the optimum is the least, over partitions of the colors into at most $k$ groups, of the sum of the squared distances to the group means, which is the [k-means problem](/k-means-problem/) with the distinct colors as points and their pixel counts as weights.

The palette entries can be any points of the space, which a frame buffer with a color map allows, or must be integers, which changes the optimum only by rounding. A palette that is fixed in advance, such as 6 levels per channel, is a *uniform* quantization; a palette chosen for the image is *adaptive*.

## Variants

- **Uniform palette.** A fixed grid, such as 8, 8 and 4 levels of red, green and blue, or the 216 colors of 6 levels per channel. Only the map is chosen, by a [scalar quantization](/scalar-quantization/) of each channel.
- **Adaptive palette.** The palette is chosen for the image, which is the main problem of this page.
- **Gray images.** With $d = 1$, the optimal groups are intervals of the sorted values, and a dynamic program finds the exact optimum; see the [k-means problem](/k-means-problem/).
- **Perceptual error.** The squared distance in a space such as CIELAB, where equal distances are closer to equal perceived differences.
- **Spatial error.** The error after a blur that models the eye, which favors maps that mix palette colors in fine patterns. This joins the problem with [halftoning](/halftoning/).
- **Shared palettes.** One palette for several images or for all frames of a video.
- **Weighted importance.** Larger weights for regions such as faces or for colors that must stay exact, such as the colors of a logo.

## Examples

- **Fewer colors than the palette.** An image with at most $k$ distinct colors has an optimum of 0: the palette is the set of its colors.
- **Gray outlier.** The gray values $0, 1, 2, 3, 100$ with $k = 2$ have the optimum $\{3/2, 100\}$ with an error of $\frac{9}{4} + \frac{1}{4} + \frac{1}{4} + \frac{9}{4} = 5$. [Median cut](/median-cut/) splits at the median 2 and gets an error of 4234; [octree quantization](/octree-color-quantization/) finds the optimum here.
- **Popularity.** Taking the $k$ most frequent colors fails on the same data: all five values occur once, and with the palette $\{0, 1\}$, the pixel 100 alone has an error of $99^2 = 9801$.
- **Uniform grid.** With 6 levels per channel, the colors $0, 51, 102, 153, 204, 255$ in each channel, the largest error of one channel is $25.5$, whatever the image, while an adaptive palette can fit an image with few hues much better.

## Known algorithms

| Algorithm | Idea | Palette size | Time |
|---|---|---|---|
| Uniform grid | fixed levels per channel | fixed | $\Theta(n)$ |
| Popularity (Boyle and Lippman) | the $k$ most frequent colors after a reduction to 5 binary digits per channel | $k$ | $\Theta(n)$ plus a selection |
| [Median cut](/median-cut/) | split the box with the longest side at the median | $\min(k, D)$ | $O(n k)$ |
| [Octree quantization](/octree-color-quantization/) | merge the deepest nodes of an octree | at most $k$ | $O(n b k)$, $\Theta(k b)$ memory |
| [k-means](/k-means/) (Lloyd iterations) | alternate nearest colors and means | $k$ | $\Theta(n k)$ per iteration |
| Variance split (Wu) | split along principal axes to reduce the error most | $k$ | $\Theta(n)$ for a histogram, then work on the histogram |
| [Self-organizing map](/self-organizing-map/) | train a one-dimensional map of $k$ units on the colors | $k$ | $\Theta(n k)$ per pass |

Here $D$ is the number of distinct colors and $b$ the depth of the octree. Each method is often followed by a few [k-means](/k-means/) iterations, which can only lower the error, and by a map with [Floyd-Steinberg dithering](/floyd-steinberg-dithering/) or [ordered dithering](/ordered-dithering/) instead of the nearest color.

## Bounds

- **Reading the input.** Every pixel must be read, because one changed pixel can change the best palette, so any algorithm needs $\Omega(n)$ time.
- **NP-hard in general.** Minimum squared error clustering is NP-hard in the plane when $k$ is part of the input (Mahajan, Nimbhorkar and Varadarajan) and in general dimension for $k = 2$ (Aloise and others), as on the [hardness page](/k-means-np-hardness/). The planar case embeds in RGB by setting one channel to a constant. Heckbert had noted in 1980 that an efficient optimal algorithm seemed unlikely. For integer colors in $[0, 256)^3$ the space is finite, so the hardness is a statement about the general problem with real points and growing $k$.
- **Exact cases.** For $d = 1$ the dynamic program on the sorted values is exact and polynomial. For fixed $d$ and $k$, the optimal partition is a Voronoi partition, and the number of such partitions of $n$ points is polynomial in $n$, so the problem can be solved exactly in polynomial time, with a degree that grows with $k d$.
- **Approximation.** No approximation ratio holds for median cut or octree quantization in general: their errors can be any multiple of the optimum, as the examples on their pages show. [k-means++](/k-means-plus-plus/) seeding gives an expected $O(\log k)$ factor.

## Reductions

- **To the k-means problem.** As stated in the definition, with the distinct colors as weighted points. Every method for the [k-means problem](/k-means-problem/) applies.
- **To vector quantization.** A palette is a codebook of [vector quantization](/vector-quantization/) in three dimensions, and the Lloyd conditions of nearest neighbor and centroid (Lloyd 1982) are the same.
- **To nearest-neighbor search.** The map step asks, for each color, for the [nearest](/nearest-neighbor-search/) palette color, which a [k-d tree](/kd-tree/) or a grid of buckets speeds up.
- **From one dimension.** Wu reduces the three-dimensional problem to a sequence of optimal one-dimensional problems along principal axes.
- **To halftoning.** With a fixed palette, the choice of a map that looks good after the eye blurs it is the [halftoning](/halftoning/) problem with several output levels.

## Applications

- Images in formats with a palette, such as GIF and PNG with a palette, and icons.
- Displays and frame buffers with a color map, as in the systems that Heckbert studied.
- Reduction of the colors of an image for printing with few inks, for embroidery and for posters.
- Compression: an index per pixel and a small palette instead of three values per pixel.
- Segmentation by color, where each palette color stands for one class of pixels.

## References
