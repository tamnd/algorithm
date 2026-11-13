---
tag: GK4YJV
kind: algorithm
slug: morphological-dilation
name: Morphological dilation
aliases:
- dilation
area: graphics-and-signals/image-processing
level: intro
summary: Grow the foreground by adding every pixel that the structuring element reaches from it. On a gray image, take the maximum over the element.
solves: [morphological-filtering]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, k: the number of offsets in the structuring element}
  time: {worst: Θ(W H k)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, recursive: false, in_place: false, exact: true, linear: false}
prereqs: [structuring-element, digital-image]
see_also: [morphological-erosion, morphological-closing, morphological-opening, minkowski-sum, mathematical-morphology, sliding-window-maximum, distance-transform, flood-fill]
sources:
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: Chapter 3, Erosion and Dilation (the definitions for sets and functions, the duality, the properties and the fast algorithms)
  - book: isbn:9780126372403
    title: Jean Serra, Image Analysis and Mathematical Morphology, Academic Press, 1982
    locator: Chapter II, The hit or miss transformation, erosion and opening (dilation as the dual of erosion)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 9, Morphological Image Processing (the section on erosion and dilation)
  - paper: doi:10.1109/TPAMI.1987.4767941
    title: Robert M. Haralick, Stanley R. Sternberg and Xinhua Zhuang, Image analysis using mathematical morphology, IEEE Transactions on Pattern Analysis and Machine Intelligence 9(4), 532 to 550, 1987
    locator: the sections on binary dilation and on gray scale dilation
---

Morphological dilation grows the foreground of an image with a small shape called the [structuring element](/structuring-element/) $B$: the result is every point $x + b$ with $x$ in the foreground $X$ and $b$ in $B$, which is the [Minkowski sum](/minkowski-sum/) $X \oplus B$. On a gray image with a flat element it is the moving maximum over the reflected element. It is the dual of [erosion](/morphological-erosion/): dilating the foreground is eroding the background with the reflected element. The direct method takes the maximum of the image shifted by each offset of $B$, in $\Theta(WHk)$ time for a $W \times H$ image and $k$ offsets.

## In plain words

Take a small stamp, for example a 3 by 3 square with a marked center. For every white pixel of a black and white picture, press the stamp on the picture with its center on that pixel, and paint white everything under it. The white regions grow by a layer as thick as the stamp, small black holes and narrow black gaps fill up, and pieces that are close together join.

On a gray picture the rule is "take the brightest value that the stamp brings to this pixel". Bright regions grow and dark details smaller than the stamp disappear.

A fast program does not press the stamp pixel by pixel. It shifts the whole picture once for each cell of the stamp and keeps, at each pixel, the brightest value it has seen.

## The problem

The input is an image $f$ with $W$ columns and $H$ rows, $f[y][x]$ for $0 \le x < W$ and $0 \le y < H$, with the pixel centers at the integer points and one channel of integer values in $\{0, \dots, \top\}$. A binary image has 0 for background and 1 for foreground. Dilation only compares values, so linear and gamma encoded values give the same result up to the encoding. The structuring element is a finite set $B \subset \mathbb{Z}^2$ of offsets $(u, v)$. A pixel outside the image takes an outside value $o$; the usual choice $o = 0$ ignores the outside. With $\tilde f$ the extended image, the output is

$$(f \oplus B)(p) = \max\bigl(\{0\} \cup \{\tilde f(p - b) : b \in B\}\bigr).$$

For a binary image with foreground $X$ and the outside ignored, this is the Minkowski sum cut to the image,

$$X \oplus B = \{x + b : x \in X,\ b \in B\} = \bigcup_{b \in B} X_b = \{p : \check B_p \cap X \neq \emptyset\},$$

with $\check B = \{-b : b \in B\}$ the reflected element. The last form says that $p$ is in the result when the reflected element, put at $p$, hits $X$. For a symmetric element such as a square, a disk or a cross, $\check B = B$ and the reflection does not matter.

## The algorithm

```pseudo id=main
DILATE(f, W, H, B, o)                ▷ o is the outside value; o = 0 ignores the outside
L1  set g[y][x] ← 0 for every pixel
L2  for each offset (u, v) in B do
L3      for y ← 0 to H − 1 do
L4          for x ← 0 to W − 1 do
L5              if 0 ≤ x − u < W and 0 ≤ y − v < H then t ← f[y − v][x − u]
L6              else t ← o
L7              g[y][x] ← max(g[y][x], t)
L8  return g
```

Line L1 starts every pixel at 0, the neutral value of a maximum. Each round of line L2 is the image shifted by one offset $(u, v)$: the pixel at $(x, y)$ reads the input at $(x - u, y - v)$, so the input pixel at $q$ arrives at $q + (u, v)$. Line L7 combines the shifted copy with the result so far; on a binary image it is a logical OR. This "gather" form reads the input and writes each output pixel once per offset. The "scatter" form, which visits each foreground pixel and paints $B$ around it, gives the same set but writes the same pixel many times and does not extend to gray images as simply.

## Example

Take $W = 8$, $H = 5$, the outside ignored, and the image $X$ of 14 foreground pixels (`#`) from the page on [erosion](/morphological-erosion/): a 4 by 3 block with a bump at $(5, 2)$ and an isolated pixel at $(7, 2)$.

```text
X                   X dilated by the square    X dilated by the cross
. . . . . . . .     # # # # # # . .            . # # # # . . .
. # # # # . . .     # # # # # # # #            # # # # # # . #
. # # # # # . #     # # # # # # # #            # # # # # # # #
. # # # # . . .     # # # # # # # #            # # # # # # . #
. . . . . . . .     # # # # # # . .            . # # # # . . .
```

The 3 by 3 square gives 36 pixels: the block grows by one pixel on every side, and the gap at column 6 between the bump and the isolated pixel fills, so the three parts become one. The 5-pixel cross gives 30 pixels: it does not reach the diagonal corners, so the corners of the block stay rounded off.

An element that is not symmetric shows the direction of the shift. With $B = \{(0, 0), (1, 0)\}$ each foreground pixel also paints the pixel to its right:

```text
. . . . . . . .
. # # # # # . .
. # # # # # # #
. # # # # # . .
. . . . . . . .
```

Erosion by the same element looks to the right instead, which is the reflection in the duality.

On a gray row with the horizontal segment $\{-1, 0, 1\}$, the dilation is the moving maximum of three values:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $f$ | 5 | 3 | 8 | 8 | 2 | 7 | 7 | 6 |
| $f \oplus B$ | 5 | 8 | 8 | 8 | 8 | 7 | 7 | 7 |

The dark pixels 3 and 2 are filled, and the plateau of 8 grows by one pixel on each side.

## Correctness

The loop of line L2 keeps the invariant that after the offsets $b_1, \dots, b_j$, each $g(p)$ is the maximum of 0 and of $\tilde f(p - b_i)$ for $i \le j$; a round reads only $f$ and writes $g$ only at the pixel it visits. After the last offset the invariant is the definition. On a binary image a maximum is 1 exactly when some $p - b$ is foreground, that is when $p = x + b$ for some foreground $x$, which is the Minkowski sum. The full proof below also proves the duality with erosion and the distributivity over unions.

## Complexity

- **Time.** Lines L5 to L7 run once for each pair of a pixel and an offset: $\Theta(WHk)$ in the word-RAM model, in every case. The scatter form costs $\Theta(WH + |X| k)$ and is faster only when the foreground is sparse.
- **Space.** The output takes $WH$ values; the method cannot write into $f$.
- **Packed bits.** On a binary image with $w$ pixels in a word, each round is a shift and an OR of whole words: $O(WHk/w)$ word operations.
- **Rectangles and disks.** A rectangle is the sum of a horizontal and a vertical segment, and the moving maximum over a segment costs a constant number of comparisons per pixel by the method of van Herk and of Gil and Werman on the page [sliding window maximum](/sliding-window-maximum/). A dilation by a rectangle then costs $\Theta(WH)$. A binary dilation by a digital disk of radius $r$ is the set of pixels whose squared Euclidean [distance](/distance-transform/) to $X$ is at most $r^2$, which also costs $\Theta(WH)$ for any $r$.

## Properties

- **Duality.** With $\bar f = \top - f$, $\overline{f \oplus B} = \bar f \ominus \check B$; in sets, $(X \oplus B)^c = X^c \ominus \check B$. On a finite image, the outside value $o$ on one side must be $\top - o$ on the other.
- **Extensive when $B$ holds the origin.** Then $f \le f \oplus B$. Without the origin the input can be lost: $B = \{(1, 0)\}$ only shifts the image.
- **Increasing.** $f_1 \le f_2$ implies $f_1 \oplus B \le f_2 \oplus B$.
- **Commutes with the maximum.** $\max(f_1, f_2) \oplus B = \max(f_1 \oplus B, f_2 \oplus B)$, and $f \oplus (B \cup C) = \max(f \oplus B, f \oplus C)$. Erosion has the dual rules with the minimum: $\min(f_1, f_2) \ominus B = \min(f_1 \ominus B, f_2 \ominus B)$ and $f \ominus (B \cup C) = \min(f \ominus B, f \ominus C)$.
- **Commutative and associative.** On the whole plane $X \oplus B = B \oplus X$ and $(X \oplus A) \oplus C = X \oplus (A \oplus C)$. The second identity is the base of all decompositions. On a finite image with the outside ignored it holds exactly for a rectangle split into its two segments.
- **Adjunction with erosion.** On the whole plane $X \oplus B \subseteq Y$ if and only if $X \subseteq Y \ominus B$. From this, erosion followed by dilation is the [opening](/morphological-opening/) and dilation followed by erosion is the [closing](/morphological-closing/), and both are idempotent.

## Variants and improvements

- **Decomposition.** A $(2r+1) \times (2r+1)$ square is a horizontal segment plus a vertical one; a diamond of radius $r$ is $r$ copies of the 5-pixel cross; an octagon alternates the square and the cross. Each costs far fewer comparisons than the direct method.
- **Constant time per pixel for segments.** The van Herk and Gil-Werman blocks or a monotone [deque](/deque/) give the moving maximum in $O(1)$ amortized time per pixel, as on the page [sliding window maximum](/sliding-window-maximum/).
- **Disks by the distance transform.** Compute the Euclidean distance transform of the foreground, for example by the [Felzenszwalb-Huttenlocher algorithm](/felzenszwalb-distance-transform/), and threshold it at $r^2$. A [chamfer distance transform](/chamfer-distance/) gives an octagon instead of a disk.
- **Non-flat elements.** Add the height $b(y)$ before the maximum: $\max_y \bigl(\tilde f(p - y) + b(y)\bigr)$. This is the max-plus convolution.
- **Conditional dilation.** Dilate and take the minimum with a mask, and repeat until nothing changes. This is the reconstruction by dilation, which rebuilds the objects of the mask that touch a marker; for a binary image with the cross it is a [flood fill](/flood-fill/) from the marker.

## When to use it

Use dilation to close small gaps and holes in a binary mask, to join pieces that are near each other, to grow a region by a safety margin, and as the second step of the [opening](/morphological-opening/) and the first step of the [closing](/morphological-closing/). The difference $(X \oplus B) \setminus X$ is an outer boundary of one pixel width when $B$ is the cross or the square. Dilation alone enlarges every object; when the size of the objects must stay, use the closing. For a gray image, dilation by a flat element is a moving maximum and removes dark specks, but it also widens bright features.

## Pitfalls

- **The reflection at line L5.** The pixel at $p$ reads the input at $p - b$, not $p + b$. A program that reads $p + b$ dilates by $\check B$, which is wrong for an element that is not symmetric, and the error does not show on a square or a disk. Gonzalez and Woods write the dilation as the set of $p$ where the reflected element hits $X$, which is the same set.
- **The wrong outside value.** Setting $o = \top$ at line L6 makes the border grow foreground. Use $o = 0$ unless the image is known to continue with foreground.
- **Painting in place.** The scatter form must write into a separate output. If it writes into the input, each painted pixel paints again later in the same scan, and the foreground grows across the whole image in the scan direction.
- **Erosion is not the inverse.** Dilating and then eroding with the same element does not give back the input; it gives the closing, which can only add pixels. Small holes and gaps that the dilation filled stay filled.
- **Empty element.** With $B = \emptyset$ the result is empty, not the input. The identity element is $\{(0, 0)\}$.

## Implementations

## History

Dilation is the Minkowski sum of the geometry of convex sets, named after Hermann Minkowski; Hadwiger studied it with the Minkowski subtraction in integral geometry. Matheron and Serra made dilation and erosion the base of mathematical morphology at the École des Mines de Paris in the 1960s, and Serra (1982) is the standard account. Sternberg introduced the umbra and the gray scale dilation for image processing, and Haralick, Sternberg and Zhuang (1987) gave the survey that made it common in computer vision.

## References
