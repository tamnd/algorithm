---
tag: 7GMTX1
kind: definition
slug: structuring-element
name: Structuring element
aliases:
- kernel for morphology
area: graphics-and-signals/image-processing
level: intro
summary: A small set of pixel offsets with a marked origin, the probe shape that morphological operators place at each pixel of an image.
prereqs: [digital-image, pixel]
see_also: [morphological-erosion, morphological-dilation, morphological-opening, morphological-closing, hit-or-miss-transform, mathematical-morphology, minkowski-sum, distance-transform]
sources:
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: the definition of structuring elements, their origin, reflection and size, and their decomposition for fast erosion and dilation (general locator)
  - book: isbn:9780126372403
    title: Jean Serra, Image Analysis and Mathematical Morphology, Academic Press, 1982
    locator: Chapter II, The hit or miss transformation, erosion and opening (general locator)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 9, the introduction of structuring elements for binary morphology (general locator)
---

A structuring element is the small shape that a morphological operator uses to probe an image. It is a finite set of offsets on the pixel grid, with one point marked as its origin, and the operator places a copy of it at every pixel. [Erosion](/morphological-erosion/) asks whether the copy fits inside the shape, [dilation](/morphological-dilation/) whether it touches the shape, and the [opening](/morphological-opening/) keeps the parts of a shape that are unions of copies. The size, shape and orientation of the element decide what an operator counts as a small or a thin structure. Unlike the kernel of a linear filter, a flat structuring element has no weights: it is only a set.

## Definition

A **flat structuring element** is a finite set $B \subset \mathbb{Z}^2$ of offsets. The offset $(0, 0)$ is its **origin**; $B$ usually contains it, but it does not have to. The copy of $B$ **placed at** a pixel $p$ is the translate

$$B_p = \{p + b : b \in B\}.$$

The **reflection** of $B$ is $\check B = \{-b : b \in B\}$, and $B$ is **symmetric** if $\check B = B$. The reflection appears in the duality of erosion and dilation and in the relation of dilation to the [Minkowski sum](/minkowski-sum/).

The element of **size** $n$ is the Minkowski sum of $n$ copies,

$$nB = \underbrace{B \oplus B \oplus \cdots \oplus B}_{n}, \qquad 0B = \{(0, 0)\},$$

with $X \oplus Y = \{x + y : x \in X, y \in Y\}$. Families $nB$ give the sizes of openings in a granulometry. An element **decomposes** if $B = B_1 \oplus B_2$ for smaller elements; then erosion by $B$ is erosion by $B_1$ followed by erosion by $B_2$, and the same for dilation, which is faster.

A **non-flat** structuring element adds a height $h : B \to \mathbb{Z}$, and the gray erosion becomes $\min_{b \in B} (f(p + b) - h(b))$. For the [hit-or-miss transform](/hit-or-miss-transform/), a **composite** structuring element is a pair $(B_1, B_2)$ of disjoint flat elements, one to fit the foreground and one to fit the background.

## Examples and non-examples

| element | offsets | pixels | notes |
|---|---|---|---|
| 3 by 3 square | $\{-1, 0, 1\}^2$ | 9 | symmetric; $H \oplus V$ for the horizontal and vertical 3 pixel segments; $nB$ is the $(2n+1)$ by $(2n+1)$ square |
| cross | $(0, 0)$ and its 4 edge neighbors | 5 | symmetric; $nB$ is the diamond $\lvert x\rvert + \lvert y\rvert \le n$ |
| horizontal segment of $k$ pixels | $\{0, \dots, k-1\} \times \{0\}$ | $k$ | not symmetric unless centered; flat erosion by it is a moving minimum |
| digital disk of radius $r$ | $\{b : b_x^2 + b_y^2 \le r^2\}$ | 13 for $r = 2$, 29 for $r = 3$ | the nearest to a round probe; from a distance transform for large $r$ |
| corner pair $\{(0, 0), (1, 1)\}$ | two diagonal pixels | 2 | not symmetric; useful to test the reflection convention |
| hit-or-miss pair for an isolated point | $B_1 = \{(0, 0)\}$, $B_2$ the 8 neighbors | 1 and 8 | disjoint, so a valid composite element |

- **The cross and the disk.** The diamond $2B$ of the cross has 13 pixels and equals the digital disk of radius 2. The diamond $3B$ has 25 pixels and differs from the disk of radius 3, which has 29: it lacks $(\pm 2, \pm 2)$. Repeating a small element does not give round disks.
- **The origin outside the element.** $B = \{(1, 0)\}$ is a valid element. Erosion and dilation by it shift the image by one pixel, so erosion need not shrink a shape. The opening by it gives back the image everywhere except in the first column, which no copy placed inside the image covers.
- **Non-example: a convolution kernel.** The 3 by 3 averaging kernel with weights $1/9$ is not a structuring element: its weights are summed, while a structuring element only selects which pixels the minimum or maximum runs over. The square of the same size is the structuring element.
- **Non-example: an overlapping pair.** $B_1 = \{(0, 0), (1, 0)\}$ and $B_2 = \{(1, 0)\}$ share $(1, 0)$, so no pixel can be in the foreground and in the background at that offset, and the hit-or-miss transform with this pair is empty for every image. It is not a valid composite element.
- **Non-example: an infinite set.** A half plane is a structuring element in the continuous theory but not on a finite image; in practice it is replaced by a large rectangle.

## Related definitions

- [Erosion](/morphological-erosion/) and [dilation](/morphological-dilation/): the minimum and the maximum of the image over the placed element.
- [Opening](/morphological-opening/) and [closing](/morphological-closing/): the compositions that remove the structures the element does not fit.
- [Hit-or-miss transform](/hit-or-miss-transform/): the operator with a composite element.
- [Minkowski sum](/minkowski-sum/): the set operation behind dilation and behind the size $nB$.
- [Mathematical morphology](/mathematical-morphology/): the technique built on structuring elements.
- [Distance transform](/distance-transform/): thresholds of it give erosion and dilation by disks, the element that repeated small elements do not give.
- [Digital image](/digital-image/) and [pixel](/pixel/): the grid on which the offsets live.

## References
