---
tag: 2WFPAC
kind: algorithm
slug: slic-superpixels
name: SLIC superpixels
aliases:
- SLIC
- simple linear iterative clustering
area: graphics-and-signals/image-processing
level: advanced
summary: Split an image into about k compact superpixels by k-means on color and position, where each center only looks at pixels in a window of twice the grid spacing around it.
solves: [image-segmentation]
model: real-ram
complexity:
  vars: {N: the number of pixels, I: the number of iterations}
  time: {worst: O(N I), average: O(N I), best: O(N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, local_search_window: true, compactness_parameter: true, connected_superpixels: true, monotone_energy: false}
history:
  year: 2010
  people: [Radhakrishna Achanta, Appu Shaji, Kevin Smith, Aurelien Lucchi, Pascal Fua, Sabine Süsstrunk]
  note: Achanta and colleagues at EPFL described SLIC in a 2010 technical report and published it with a comparison of superpixel methods in IEEE Transactions on Pattern Analysis and Machine Intelligence in 2012.
prereqs: [k-means, image-segmentation]
see_also: [lloyds-algorithm, felzenszwalb-segmentation, watershed-segmentation, mean-shift-segmentation, color-spaces, connected-component-labeling, centroidal-voronoi-tessellation, normalized-cut]
sources:
  - paper: doi:10.1109/TPAMI.2012.120
    title: Radhakrishna Achanta, Appu Shaji, Kevin Smith, Aurelien Lucchi, Pascal Fua and Sabine Süsstrunk, SLIC superpixels compared to state-of-the-art superpixel methods, IEEE Transactions on Pattern Analysis and Machine Intelligence 34(11), 2274 to 2282, 2012
    locator: Section 3 (Algorithm 1, the grid interval S, the distance measure of equation (3) with the compactness m, the postprocessing for connectivity, and the complexity)
  - paper: doi:10.1109/TIT.1982.1056489
    title: Stuart P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 129 to 137, 1982
    locator: the alternation of nearest-center assignment and centroid update that SLIC restricts to local windows
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 10, Image segmentation, the section on region segmentation using clustering and superpixels
---

SLIC, simple linear iterative clustering, splits an image into superpixels: small, compact regions of similar color that follow the edges in the image. Later steps, such as labeling or graph cuts, then work on a few hundred superpixels instead of a million pixels. SLIC is [k-means](/k-means/) on five numbers per pixel, the three CIELAB [color](/color-spaces/) values and the two coordinates, with two changes. The centers start on a regular grid with spacing $S$, and each center compares itself only with the pixels in a $2S \times 2S$ window around it. So each pixel is compared with a few nearby centers instead of all of them, and an iteration costs $O(N)$ whatever the number of superpixels. A compactness parameter $m$ sets how much position counts against color. Achanta and colleagues published it in 2012, with a comparison that showed it to be fast and to follow boundaries as well as or better than the methods of that time.

## In plain words

Lay a square grid over the picture and put a pin in the middle of each square. Each pin will collect a superpixel. Every pixel looks at the pins near it and joins the one that is closest, where "close" mixes how near the pin is on the picture with how similar its color is. Then each pin moves to the average place and color of the pixels it got. Do this a few times. Each pin only looks at pixels within about one square of it, so the work stays small even with many pins. At the end, stray bits that broke off from their superpixel are given to a neighbor.

## The problem

The input is an image with $N$ pixels, each with a color vector $c$ (CIELAB values, or one gray value) and a position $(x, y)$, a wanted number of superpixels $k$, and a compactness $m > 0$. The output is a partition of the pixels into about $k$ connected regions that are compact and have uniform color. For a pixel $i$ and a center $C_j = [c_j, x_j, y_j]$, SLIC uses

$$D = \sqrt{d_c^2 + \left(\frac{d_s}{S}\right)^2 m^2}, \qquad d_c = \lVert c_i - c_j \rVert, \quad d_s = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}, \quad S = \sqrt{N/k}.$$

Dividing $d_s$ by $S$ makes the trade-off independent of the size of the superpixels. The paper gives $m$ in $[1, 40]$ for CIELAB values. It is one way to solve the [image segmentation](/image-segmentation/) problem, aimed at oversegmentation.

## The algorithm

```pseudo id=main
SLIC(I, k, m)
L1  S ← √(N/k);  place the centers C_j = [c_j, x_j, y_j] on a grid with spacing S
L2  move each center to the pixel of least gradient in its 3 × 3 neighborhood
L3  repeat
L4      d(i) ← ∞ for each pixel i
L5      for each center C_j, for each pixel i with |x_i − x_j| ≤ S and |y_i − y_j| ≤ S do
L6          D ← √(d_c² + (d_s / S)² m²);  if D < d(i) then d(i) ← D;  l(i) ← j
L7      C_j ← the mean [c, x, y] of the pixels with l(i) = j;  E ← how far the centers moved
L8  until E = 0 or after the iteration limit (10 in the paper)
L9  enforce connectivity: keep the largest connected piece of each label, give the other pixels to the nearest adjacent center
```

Line L2 keeps a seed off an edge and off a noisy pixel. The implementation takes the gradient as the sum of squared central differences of the color in $x$ and in $y$, and breaks ties by the first pixel in raster order. Lines L5 and L6 are the assignment step of k-means restricted to windows: a pixel only competes for the centers whose window covers it, and among those it takes the nearest, the first one on a tie. Line L7 is the update step. Line L9 is needed because nothing in the clustering keeps a label connected.

The pseudocode in the paper sets $d(i) \gets \infty$ once, before the loop. When the centers move, a pixel would then keep the distance to an old center position and could miss a closer new center, so the implementation resets it at line L4 in each pass. A pixel that no window covers keeps its old label. The paper's postprocessing says only that orphaned pixels go to the nearest cluster center through a connected components pass. Here, each label keeps its largest 4-connected piece, and the other pixels are taken in breadth-first order from the kept pieces, each one joining the label of an already labeled neighbor whose center is nearest in $D$. The implementation compares $D^2$ in exact fractions, with $S^2 = N/K$ for the $K$ centers actually placed.

## Example

Take the $8 \times 6$ gray image whose pixel $(x, y)$ is 20 if $x + y < 6$ and 200 otherwise, so a diagonal step edge runs from the top right to the bottom left. Ask for $k = 4$ with $m = 10$. Then $S^2 = 48/4 = 12$ and $S \approx 3.46$. The grid seeds are $(2, 1)$, $(6, 1)$, $(2, 4)$ and $(6, 4)$. Every pixel near them has gradient 0, and line L2 moves them to the first such pixel in raster order: $(1, 0)$, $(7, 0)$, $(1, 3)$ and $(5, 3)$, with values 20, 200, 20 and 200.

In the first assignment, the pixel $(5, 0)$ has value 20, but it is 4 columns from center 0, which is more than $S$, so it is not in that center's window. The only window that covers it is that of center 1, so it joins center 1, and center 1 gets the mean color 170. This is the window at work: the result depends on which centers are near, not only on which is best. The superpixels settle step by step. The tenth step gives the labels below, and the eleventh changes nothing ($E = 0$).

| row | labels |
|---|---|
| 0 | 0 0 0 0 0 0 1 1 |
| 1 | 0 0 0 0 0 1 1 1 |
| 2 | 2 2 0 0 3 1 1 1 |
| 3 | 2 2 2 3 3 3 1 1 |
| 4 | 2 2 3 3 3 3 3 1 |
| 5 | 2 3 3 3 3 3 3 3 |

Each superpixel now has one gray value: 13 pixels of 20 with center $(30/13, 9/13)$, 11 pixels of 200 with center $(69/11, 19/11)$, 8 pixels of 20 with center $(5/8, 13/4)$ and 16 pixels of 200 with center $(4, 33/8)$. All four are connected, so line L9 changes nothing. With $m = 200$, position counts much more, and the pixel $(1, 5)$, of value 200, is put into superpixel 2 with the dark pixels.

## Correctness

SLIC is a heuristic: it has no optimality claim and its loop need not settle. The full proof in [proofs/correctness.md](proofs/correctness.md) shows what does hold. After lines L4 to L6, every pixel covered by at least one window has the label of the nearest covering center, the first one on a tie, because each covering center is tested once against $d(i)$ with a strict comparison. Line L7 sets each center to the mean of its pixels, which minimizes the sum of $D^2$ over those pixels for fixed labels. After line L9, every label is connected, because each pixel it gains has a neighbor that already has that label. Unlike k-means, the assignment step can raise the total of $D^2$, since a pixel can leave the window of its own center when the center moves. The tests show such a step on a $2 \times 3$ image, and they check the other claims against an assignment that tests every pixel against every center, against exact means, and on random gray and color images.

## Complexity

- Lines L1 and L2 take $O(N)$ time.
- In each assignment, a center visits at most $(2S + 1)^2 \approx 4 N / k$ pixels, so the $k$ centers visit $O(N)$ pixels together. Each pixel is in only a few windows.
- The update and the postprocessing take $O(N)$ time.

The total is $O(N I)$ for $I$ iterations. With the fixed $I = 10$ of the paper, SLIC is linear in $N$ and independent of $k$, against $O(k N I)$ for plain k-means. The extra space is $\Theta(N)$ for the labels and the distances. The implementation uses exact fractions, so its constant is much larger than that of a floating-point version.

## Properties

- **About $k$ superpixels of about equal size.** The grid fixes the starting number, and the windows keep each superpixel near its starting square.
- **Compactness control.** A large $m$ gives near-square superpixels. A small $m$ follows color edges more closely, with less regular shapes.
- **Linear time.** The window makes the cost per iteration independent of $k$.
- **Not a descent method.** The windowed assignment can raise the energy of k-means, so the usual argument that k-means stops does not apply. The iteration limit stops it.
- **Connected only after postprocessing.** The clustering itself can leave pieces of a label apart from the rest.
- **Deterministic.** With the grid start and fixed tie rules, the output depends only on the image and the parameters.

## Variants and improvements

- **Plain k-means.** Without the window, each pixel compares with every center; see [Lloyd's algorithm](/lloyds-algorithm/). It is slower and gives less regular superpixels.
- **SLICO.** The authors' zero-parameter version adapts the color normalization for each superpixel from the largest color distance seen in the last iteration, so $m$ need not be set.
- **Supervoxels.** Add the frame number to the spatial distance to cluster video or 3D data.
- **Gray images.** Use one gray value as the color.
- **Other superpixels.** [Felzenszwalb segmentation](/felzenszwalb-segmentation/) gives irregular regions with no size control, the [watershed](/watershed-segmentation/) gives regions from a gradient, and [mean shift](/mean-shift-segmentation/) finds the number of regions from the data. Compact watershed and SEEDS are later methods with a compactness trade-off.
- **Lower-cost updates.** Faster versions avoid the full distance array or run the assignment in parallel on a GPU.

## When to use it

Use SLIC when a later step needs a few hundred to a few thousand regions that respect edges, are about the same size and are compact: features for classification, the nodes of a conditional random field, a faster [graph cut](/image-segmentation-graph-cuts/) or [GrabCut](/grabcut/), or a mosaic effect. It is simple, fast, and has one parameter besides $k$. Do not use it when the final objects are wanted directly, since it does not merge regions, or when the regions must be irregular, thin or very different in size.

## Pitfalls

- **Wrong color space.** The value range of $m$ is for CIELAB. In RGB or with values in $[0, 1]$, the same $m$ gives a very different trade-off.
- **Stale distances.** If $d(i)$ is not reset in each iteration, pixels keep distances to old center positions.
- **Uncovered pixels.** After the centers move, some pixels can lie outside every window. They must keep a label or be handled by the postprocessing.
- **Too few or too many superpixels.** The grid gives about $k$, and the postprocessing can remove some. Do not rely on an exact count.
- **No connectivity guarantee before L9.** Code that skips the postprocessing gets labels with several pieces.
- **Texture.** In strongly textured areas, the mean color is a poor model and the superpixels become irregular.

## Implementations

## History

Superpixels as a preprocessing step go back to Ren and Malik in 2003, who used normalized cuts to build them. Radhakrishna Achanta and colleagues at EPFL proposed SLIC in a 2010 technical report and published it in IEEE Transactions on Pattern Analysis and Machine Intelligence in 2012, with a comparison against graph-based and gradient-based superpixel methods on the Berkeley data set. Its speed and its single parameter made it the default superpixel method in many libraries.

## References
