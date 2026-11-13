---
tag: V188PY
kind: algorithm
slug: morphological-closing
name: Morphological closing
aliases:
- closing
area: graphics-and-signals/image-processing
level: intro
summary: Dilation followed by erosion with the same element. It fills the holes and gaps of the foreground where the element does not fit in the background.
solves: [morphological-filtering]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, k: the number of offsets in the structuring element}
  time: {worst: Θ(W H k)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, recursive: false, in_place: false, exact: true, linear: false, idempotent: true}
prereqs: [morphological-dilation, morphological-erosion, structuring-element]
see_also: [morphological-opening, morphological-filtering, mathematical-morphology, image-thresholding, image-segmentation, flood-fill, distance-transform]
sources:
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: Chapter 4, Opening and Closing (the definitions, the duality with the opening, the algebraic properties and the top-hats)
  - book: isbn:9780126372403
    title: Jean Serra, Image Analysis and Mathematical Morphology, Academic Press, 1982
    locator: Chapter II, The hit or miss transformation, erosion and opening (the closing as the dual of the opening)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 9, Morphological Image Processing (the section on opening and closing)
  - paper: doi:10.1109/TPAMI.1987.4767941
    title: Robert M. Haralick, Stanley R. Sternberg and Xinhua Zhuang, Image analysis using mathematical morphology, IEEE Transactions on Pattern Analysis and Machine Intelligence 9(4), 532 to 550, 1987
    locator: the sections on opening and closing
---

Morphological closing is [dilation](/morphological-dilation/) followed by [erosion](/morphological-erosion/) with the same [structuring element](/structuring-element/) $B$: $X \bullet B = (X \oplus B) \ominus B$. It fills the holes, gaps and narrow bays of the foreground that the reflected element cannot fit into, and it leaves the rest of the shape unchanged. It is the dual of the [opening](/morphological-opening/): closing the foreground is opening the background with the reflected element. Closing is increasing, extensive and idempotent. The direct method costs $\Theta(WHk)$ for a $W \times H$ image and $k$ offsets.

## In plain words

Take a stamp, for example a small disk, and slide it everywhere in the black part of a black and white picture, without letting it touch white. Every black pixel that the stamp can cover stays black. Every black pixel that the stamp can never reach turns white.

Small black holes inside white regions fill up, narrow black cracks close, and white pieces that are almost touching join. Large black areas keep their size, and white regions do not grow outward. Doing it a second time changes nothing.

On a gray picture, dark details narrower than the stamp are filled up to the level around them. Bright details stay.

## The problem

The input is an image $f$ with $W$ columns and $H$ rows of integer values in $\{0, \dots, \top\}$, pixel centers at the integer points, binary or gray, and a finite structuring element $B \subset \mathbb{Z}^2$. The output is

$$\varphi_B(f) = (f \oplus B) \ominus B, \qquad (f \oplus B)(z) = \max_{b \in B} f(z - b), \quad (g \ominus B)(p) = \min_{b \in B} g(p + b),$$

with both steps ignoring the pixels outside the image (the maximum over an empty set is 0, the minimum is $\top$). For a binary image with foreground $X$, a pixel $p$ is in the closing unless some translate of the reflected element $\check B = \{-b : b \in B\}$ holds $p$ and misses $X$:

$$X \bullet B = \Bigl(\bigcup \{\check B_z : \check B_z \cap X = \emptyset\}\Bigr)^c = (X^c \circ \check B)^c.$$

On a gray image, $\varphi_B(f)(p)$ is the smallest value $t$ such that some translate of $\check B$ that covers $p$ has $f \le t$ on all of it: push a flat stamp down onto the graph of $f$ from above, and keep the lowest level that the stamp reaches.

## The algorithm

```pseudo id=main
CLOSE(f, W, H, B)                        ▷ both steps ignore the outside
L1  set d[p] ← 0 for every pixel p
L2  for each offset b in B do
L3      for each pixel p with p − b in the image do d[p] ← max(d[p], f[p − b])
L4  set g[p] ← ⊤ for every pixel p
L5  for each offset b in B do
L6      for each pixel p with p + b in the image do g[p] ← min(g[p], d[p + b])
L7  return g
```

Lines L1 to L3 dilate: $d(z)$ is the maximum of $f$ over the translate $\check B_z$. Lines L4 to L6 erode: $g(p)$ is the minimum of $d(z)$ over the translates $\check B_z$ that hold $p$, since $p + b = z$ means $p = z - b$. On a binary image, $g(p) = 0$ exactly when some translate of $\check B$ that holds $p$ lies in the background.

## Example

Take a 12 by 7 image with two blocks: a 3 by 3 ring with a hole at $(3, 3)$, and a 4 by 3 block with a notch at $(7, 4)$. A gap one pixel wide, column 5, separates them. The image has two rows of background on each side so that the border plays no part.

```text
X                         X closed by the square      X closed by the cross
. . . . . . . . . . . .   . . . . . . . . . . . .     . . . . . . . . . . . .
. . . . . . . . . . . .   . . . . . . . . . . . .     . . . . . . . . . . . .
. . # # # . # # # # . .   . . # # # # # # # # . .     . . # # # . # # # # . .
. . # . # . # # # # . .   . . # # # # # # # # . .     . . # # # # # # # # . .
. . # # # . # . # # . .   . . # # # # # # # # . .     . . # # # . # . # # . .
. . . . . . . . . . . .   . . . . . . . . . . . .     . . . . . . . . . . . .
. . . . . . . . . . . .   . . . . . . . . . . . .     . . . . . . . . . . . .
```

The 3 by 3 square cannot fit in the hole, in the gap or in the notch, so the closing fills all three, and the result is one 8 by 3 rectangle. The outer outline does not move. The 5-pixel cross fills only $(3, 3)$ and $(5, 3)$: every cross that holds one of them also holds a foreground pixel, since both have foreground on the left and on the right. At $(5, 2)$ the cross fits upward into the background above, and at $(7, 4)$ it fits downward, so these stay background.

On a gray row with the segment $\{-1, 0, 1\}$:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $f$ | 5 | 3 | 8 | 8 | 2 | 7 | 7 | 6 |
| dilation | 5 | 8 | 8 | 8 | 8 | 7 | 7 | 7 |
| closing | 5 | 5 | 8 | 8 | 7 | 7 | 7 | 7 |

The dark pits 3 and 2, one pixel wide, are filled to the lower of their two neighbors, 5 and 7. The closing is above $f$ at every pixel.

## Correctness

The proof below shows that CLOSE returns, at each pixel $p$, the minimum over the cut translates $S$ of $\check B$ that hold $p$ of the maximum of $f$ on $S$. The complement of that formula is the formula of the opening of the complement by $\check B$, so the closing is the dual of the opening. The three properties follow from the form as for the opening. It is increasing, since each maximum grows with $f$. It is extensive, since a maximum over a set that holds $p$ is at least $f(p)$. It is idempotent, since the set $S$ that gives the value at $p$ is at most that value everywhere after one closing.

## Complexity

- **Time.** Two passes of $k$ offsets over $WH$ pixels: $\Theta(WHk)$ in the word-RAM model, in every case.
- **Space.** The intermediate dilation and the output: $\Theta(WH)$ extra.
- **Fast elements.** For a rectangle, constant time per pixel moving maxima and minima by the method on the page [sliding window maximum](/sliding-window-maximum/) give $\Theta(WH)$ for any size. For a binary disk of radius $r$, the dilation is a threshold of the Euclidean [distance transform](/distance-transform/) of $X$ and the erosion is a threshold of the distance transform of the complement of the dilation: $\Theta(WH)$ for any $r$.
- **Packed bits.** $O(WHk/w)$ word operations on a binary image with $w$ pixels in a word.

## Properties

- **Idempotent.** $\varphi_B(\varphi_B(f)) = \varphi_B(f)$.
- **Extensive.** $f \le \varphi_B(f)$, for every $B$.
- **Increasing.** $f_1 \le f_2$ implies $\varphi_B(f_1) \le \varphi_B(f_2)$. An operator with these three properties is an algebraic closing.
- **Duality.** $\overline{\varphi_B(f)} = \gamma_{\check B}(\bar f)$, with $\bar f = \top - f$ and $\gamma$ the opening; in sets $(X \bullet B)^c = X^c \circ \check B$. Every statement about openings has a dual statement about closings.
- **Order with the opening.** $X \circ B \subseteq X \subseteq X \bullet B$ for every $B$, with or without the origin.
- **Sieving.** On the whole plane, if $B = A \oplus C$ then $X \bullet A \subseteq X \bullet B$ and $(X \bullet A) \bullet B = X \bullet B$: larger elements fill more.
- **Fixed points.** A set is kept by the closing exactly when its complement is a union of translates of $\check B$.

## Variants and improvements

- **Black top-hat.** The difference $\varphi_B(f) - f$ keeps the dark details narrower than $B$, such as dark text or cracks on an uneven bright background, and removes the background. It is a usual step before [thresholding](/image-thresholding/).
- **Closing by reconstruction.** Dilate, then erode repeatedly by a small element and take the maximum with $f$ after each step, until nothing changes. The dark components that do not hold a translate of $B$ are filled, and the others come back with their exact outline. It is on the page [morphological filtering](/morphological-filtering/).
- **Hole filling.** To fill every hole of a binary mask, whatever its size, fill the background from the image border with a [flood fill](/flood-fill/) and take the complement of what the fill reaches. No closing with a fixed element does that.
- **Intersection of closings.** The minimum of closings by line segments in several directions is an algebraic closing that fills gaps in any of the directions, but keeps elongated dark structures in the other directions.
- **Alternating filters.** A closing and an opening in sequence remove both dark and bright noise. They are on the page [morphological filtering](/morphological-filtering/).

## When to use it

Use closing to fill small holes and cracks in a binary mask after [thresholding](/image-thresholding/) or [segmentation](/image-segmentation/), to join pieces of a character or of a line that the scan broke, and to smooth the bays of an outline without moving its outer edge. Use it when the objects must keep their size; dilation alone grows them. Use the [opening](/morphological-opening/) to remove small specks instead. If the holes to fill can be of any size, use hole filling by a flood fill instead of a large closing, which would also join objects that are far apart.

## Pitfalls

- **Foreground grows at the border.** With the outside ignored in both steps, a translate of $\check B$ cut by the border is small and can miss the background, so the closing adds foreground there. In a 4 by 3 image with the two pixels $(1, 1)$ and $(2, 1)$, the closing by the horizontal segment $\{-1, 0, 1\}$ gives the whole row 1, because the gaps to the border are one pixel wide. To get the closing of the plane, pad the image with background by the reach of $B$ on each side, close, and crop.
- **The wrong order.** Erosion followed by dilation is the opening, which removes specks instead of filling holes.
- **A large element joins objects.** Two objects closer than the width of $B$ become one. If the count of objects matters, use a closing by reconstruction or fill holes by a flood fill.
- **The reflection.** For an element that is not symmetric, the dual of the closing by $B$ is the opening by $\check B$, not by $B$.
- **Gray closing does not remove bright noise.** A flat closing never lowers a value. Use an opening for bright specks.

## Implementations

## History

The closing is the dual of the opening in the work of Matheron and Serra on mathematical morphology at the École des Mines de Paris from the 1960s, and Serra (1982) develops the two together. Haralick, Sternberg and Zhuang (1987) made the gray scale closing common in computer vision.

## References
