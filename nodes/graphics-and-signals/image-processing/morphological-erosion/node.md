---
tag: 8EKNQA
kind: algorithm
slug: morphological-erosion
name: Morphological erosion
aliases:
- erosion
area: graphics-and-signals/image-processing
level: intro
summary: Shrink the foreground by keeping the pixels where the structuring element fits inside it. On a gray image, take the minimum over the element.
solves: [morphological-filtering]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, k: the number of offsets in the structuring element}
  time: {worst: Θ(W H k)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, recursive: false, in_place: false, exact: true, linear: false}
prereqs: [structuring-element, digital-image]
see_also: [morphological-dilation, morphological-opening, morphological-closing, hit-or-miss-transform, mathematical-morphology, sliding-window-maximum, minkowski-sum, distance-transform]
sources:
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: Chapter 3, Erosion and Dilation (the binary and gray definitions, the duality, the properties and the fast algorithms for lines and rectangles)
  - book: isbn:9780126372403
    title: Jean Serra, Image Analysis and Mathematical Morphology, Academic Press, 1982
    locator: Chapter II, The hit or miss transformation, erosion and opening
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 9, Morphological Image Processing (the sections on preliminaries and on erosion and dilation)
  - paper: doi:10.1109/TPAMI.1987.4767941
    title: Robert M. Haralick, Stanley R. Sternberg and Xinhua Zhuang, Image analysis using mathematical morphology, IEEE Transactions on Pattern Analysis and Machine Intelligence 9(4), 532 to 550, 1987
    locator: the sections on binary and gray scale erosion, with the umbra and the chain rule
---

Morphological erosion shrinks the foreground of an image with a small shape called the [structuring element](/structuring-element/) $B$: a pixel $p$ stays in the foreground $X$ only if $B$, moved so that its origin is at $p$, lies inside $X$. On a gray image with a flat element it is the moving minimum over $B$. It is one of the two basic operators of [mathematical morphology](/mathematical-morphology/), and it is dual to [dilation](/morphological-dilation/): eroding the foreground is dilating the background with the reflected element. The direct method takes the minimum of the image shifted by each offset of $B$, in $\Theta(WHk)$ time for a $W \times H$ image and $k$ offsets.

## In plain words

Take a small stamp, for example a 3 by 3 square of pixels, with one marked center. Put the center on a pixel of a black and white picture. If the whole stamp lies on white pixels, the pixel stays white. If any part of the stamp touches black, the pixel becomes black. Do this for every pixel.

White regions lose a layer along their edges as thick as the stamp. White parts thinner than the stamp vanish, and small white dots disappear. On a gray picture the rule is "take the darkest value under the stamp", so bright details smaller than the stamp disappear and dark regions grow.

A fast program does not move the stamp. It shifts the whole picture once for each cell of the stamp and keeps, at each pixel, the darkest value it has seen.

## The problem

The input is an image $f$ with $W$ columns and $H$ rows, $f[y][x]$ for $0 \le x < W$ and $0 \le y < H$, with the pixel centers at the integer points and one channel of integer values in $\{0, \dots, \top\}$. A binary image has values 0 (background) and 1 (foreground) and $\top = 1$; an 8-bit gray image has $\top = 255$. The values can be linear or gamma encoded: erosion only compares values, and any increasing map of the values commutes with it. The structuring element is a finite set $B \subset \mathbb{Z}^2$ of offsets $(u, v)$; its origin is the offset $(0, 0)$, which $B$ may or may not contain. A pixel $q$ outside the image takes an outside value $o$; the usual choice $o = \top$ ignores the outside. Write $\tilde f$ for the extended image. The output is

$$(f \ominus B)(p) = \min\bigl(\{\top\} \cup \{\tilde f(p + b) : b \in B\}\bigr), \qquad p \in \{0, \dots, W-1\} \times \{0, \dots, H-1\}.$$

For a binary image with foreground $X$ this is the set definition

$$X \ominus B = \{p : B_p \subseteq X\}, \qquad B_p = \{p + b : b \in B\},$$

with $X$ extended by the outside rule. Equivalently, $X \ominus B = \bigcap_{b \in B} X_{-b}$, the intersection of the copies of $X$ shifted by $-b$. A non-flat element is a function $b : B \to \mathbb{Z}$, and the gray erosion is $\min_{y \in B} \bigl(\tilde f(p + y) - b(y)\bigr)$; this page uses flat elements.

## The algorithm

```pseudo id=main
ERODE(f, W, H, B, o)                 ▷ o is the outside value; o = ⊤ ignores the outside
L1  set g[y][x] ← ⊤ for every pixel
L2  for each offset (u, v) in B do
L3      for y ← 0 to H − 1 do
L4          for x ← 0 to W − 1 do
L5              if 0 ≤ x + u < W and 0 ≤ y + v < H then t ← f[y + v][x + u]
L6              else t ← o
L7              g[y][x] ← min(g[y][x], t)
L8  return g
```

Line L1 starts every pixel at the top value, the neutral value of a minimum. Each round of line L2 compares the whole image, shifted by one offset, with the result so far. Lines L5 and L6 read the shifted pixel, or the outside value when the shift leaves the image. On a binary image line L7 is a logical AND, and the round is an AND of the image with a shifted copy, which a program can do on 64 pixels at a time with packed bits. The loop order, offsets outside and pixels inside, reads $f$ along rows for each offset; the opposite order, pixels outside and offsets inside, is the set definition and gives the same result.

## Example

Take $W = 8$, $H = 5$, the outside ignored, and the 3 by 3 square $B = \{-1, 0, 1\}^2$. The image $X$ has 14 foreground pixels (`#`):

```text
X                   X eroded by the square     X eroded by the cross
. . . . . . . .     . . . . . . . .            . . . . . . . .
. # # # # . . .     . . . . . . . .            . . . . . . . .
. # # # # # . #     . . # # . . . .            . . # # # . . .
. # # # # . . .     . . . . . . . .            . . . . . . . .
. . . . . . . .     . . . . . . . .            . . . . . . . .
```

Only the pixels $(2, 2)$ and $(3, 2)$ have all 9 square neighbors in $X$. The bump $(5, 2)$ and the isolated pixel $(7, 2)$ vanish. With the 5-pixel cross $\{(0,0), (\pm 1, 0), (0, \pm 1)\}$ the pixel $(4, 2)$ also stays, because its diagonal neighbors are not tested.

The border rule matters. For the 3 by 4 image whose first three columns are foreground and whose last column is background, the square erosion keeps the first two columns when the outside is ignored. When the outside is background ($o = 0$), only the pixel $(1, 1)$ stays: every pixel of the first column and of the top and bottom rows has a neighbor outside the image.

On a gray row with the horizontal segment $\{-1, 0, 1\}$, the erosion is the moving minimum of three values:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $f$ | 5 | 3 | 8 | 8 | 2 | 7 | 7 | 6 |
| $f \ominus B$ | 3 | 3 | 3 | 2 | 2 | 2 | 6 | 6 |

The two bright plateaus 8, 8 and 7, 7 are removed, and the dark pixel 2 spreads to its two neighbors.

## Correctness

The loop of line L2 keeps the invariant that after the offsets $b_1, \dots, b_j$, each $g(p)$ is the minimum of $\top$ and of $\tilde f(p + b_i)$ for $i \le j$. A round writes $g$ only at the pixel it visits and reads only $f$, so the rounds do not disturb each other. After the last offset the invariant is the definition. On a binary image the minimum is 1 exactly when every $p + b$ is in the extended foreground, which is the set definition. The full proof below also proves the duality with dilation and the chain rule for rectangles.

## Complexity

- **Time.** Lines L5 to L7 run once for each pair of a pixel and an offset, so the time is $\Theta(WHk)$ in the word-RAM model, in every case. The set definition, which scans the element at each pixel, has the same count.
- **Space.** The output $g$ takes $WH$ values. The method cannot write into $f$, because later rounds read pixels that an earlier round would have changed.
- **Packed bits.** On a binary image stored with $w$ pixels in a machine word, each round is a shift and an AND of whole words, so the time is $O(WHk/w)$ word operations, plus the cost of the shifts that cross word boundaries.
- **Rectangles and lines.** By the chain rule below, a $a \times b$ rectangle costs a horizontal pass with a segment of $a$ pixels and a vertical pass with a segment of $b$ pixels, $\Theta(WH(a + b))$ by the direct method. The van Herk and Gil-Werman method computes the moving minimum over a segment in a constant number of comparisons per pixel, for any length; it is on the page [sliding window maximum](/sliding-window-maximum/). A rectangle then costs $\Theta(WH)$.

## Properties

- **Duality.** With $\bar f = \top - f$ and the reflected element $\check B = \{-b : b \in B\}$, $\overline{f \ominus B} = \bar f \oplus \check B$, where $\oplus$ is the [dilation](/morphological-dilation/). In sets, $(X \ominus B)^c = X^c \oplus \check B$. On a finite image this holds when the outside value $o$ on one side is $\top - o$ on the other; ignoring the outside on both sides satisfies this.
- **Increasing.** If $f_1 \le f_2$ at every pixel, then $f_1 \ominus B \le f_2 \ominus B$.
- **Anti-extensive when $B$ holds the origin.** Then $f \ominus B \le f$, because the term $b = (0, 0)$ is in the minimum. If $B$ does not hold the origin, a pixel can go from background to foreground: $B = \{(1, 0)\}$ shifts the image one pixel to the left.
- **Decreasing in the element.** If $B_1 \subseteq B_2$, then $f \ominus B_2 \le f \ominus B_1$.
- **Translation.** Away from the border, eroding a shifted image is shifting the eroded image.
- **Chain rule.** On the whole plane, $X \ominus (A \oplus C) = (X \ominus A) \ominus C$. On a finite image with any outside value it holds exactly for a rectangle split into its horizontal and vertical segments, because the image and the rectangle are both products of intervals.
- **Adjunction.** On the whole plane, $X \oplus B \subseteq Y$ if and only if $X \subseteq Y \ominus B$. This is the property from which the idempotence of [opening](/morphological-opening/) and [closing](/morphological-closing/) follows.

## Variants and improvements

- **Decomposition.** Write a large element as a Minkowski sum of small ones and erode by each in turn. A $(2r+1) \times (2r+1)$ square is a horizontal segment plus a vertical one. A diamond of radius $r$ is the sum of $r$ copies of the 5-pixel cross, at $5r$ comparisons per pixel against $2r^2 + 2r + 1$.
- **Moving minimum in constant time.** For segments, use the van Herk and Gil-Werman blocks or a monotone [deque](/deque/), as on the page [sliding window maximum](/sliding-window-maximum/). Lines in other directions and octagons are built from these.
- **Disks through the distance transform.** With the Euclidean [distance transform](/distance-transform/) of the background, the erosion by the digital disk $\{b : |b|^2 \le r^2\}$ keeps exactly the pixels whose squared distance to the nearest background pixel is more than $r^2$. With the [Felzenszwalb-Huttenlocher algorithm](/felzenszwalb-distance-transform/) this costs $\Theta(WH)$ for any radius.
- **Non-flat elements.** Subtract the height $b(y)$ before the minimum. The [Felzenszwalb-Huttenlocher algorithm](/felzenszwalb-distance-transform/) is a fast non-flat erosion: its min-convolution with a parabola is $-\bigl((-f) \oplus (-b)\bigr)$ for the paraboloid height $b(y) = -|y|^2$.
- **Geodesic erosion and reconstruction.** Erode, then take the maximum with a mask image, and repeat until nothing changes. This is the base of the reconstruction filters on the page [morphological filtering](/morphological-filtering/).

## When to use it

Use erosion to remove foreground specks and thin bridges smaller than the element, to separate objects that touch, and as a step of [opening](/morphological-opening/), [closing](/morphological-closing/), the [hit-or-miss transform](/hit-or-miss-transform/) and the morphological gradient $f \oplus B - f \ominus B$. Erosion alone also shrinks every object that survives; when the size of the objects must stay, use the opening. For a large disk, use the distance transform; for a rectangle, use two passes of a constant-time moving minimum; for a small or irregular element, the direct method is simple and fast. A [median filter](/median-filter/) also removes small specks but is not increasing in the element and does not shrink objects; it is a rank filter between the erosion (rank 1) and the dilation (rank $k$).

## Pitfalls

- **The wrong outside value.** Setting $o = 0$ at line L6 counts the outside as background, and every object that touches the border loses a layer there. This is right only when the image is known to end with background. Use $o = \top$ to ignore the outside.
- **Writing into the input.** Writing $g$ into $f$ at line L7 lets later offsets read pixels that are already eroded, and the foreground shrinks too far. Keep $g$ separate, or use a buffer of one row per offset in a streaming version.
- **The reflected element.** Line L5 reads $f$ at $p + b$. A program that reads $p - b$ computes the erosion by $\check B$. For a symmetric element both agree; for an element such as $\{(0, 0), (1, 0)\}$ they do not. Books differ here: the Minkowski subtraction of Hadwiger is $\bigcap_{b} X_{b}$, which is the erosion by $\check B$ in the notation of this page.
- **An element without the origin.** Erosion is anti-extensive only when $B$ holds $(0, 0)$. An element such as $\{(-1, 0), (1, 0)\}$ can turn a background pixel between two foreground pixels into foreground.
- **Duality with the wrong outside rule.** The identity $(X \ominus B)^c = X^c \oplus \check B$ fails at the border when both sides use $o = 0$. Use complementary outside values.

## Implementations

## History

Erosion, under the name of Minkowski subtraction, comes from the geometry of convex sets. Matheron and Serra made it, with dilation, the base of mathematical morphology at the École des Mines de Paris in the 1960s; Serra (1982) gives the theory for sets and for gray functions. Haralick, Sternberg and Zhuang (1987) gave the account that made the gray scale erosion and the umbra common in computer vision. The constant time per pixel moving minimum for lines and rectangles is due to van Herk (1992) and, independently, Gil and Werman (1993).

## References
