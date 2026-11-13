---
tag: TADBZ8
kind: algorithm
slug: hit-or-miss-transform
name: Hit-or-miss transform
aliases:
- hit-and-miss transform
area: graphics-and-signals/image-processing
level: advanced
summary: Find the pixels where a local pattern matches exactly, with one structuring element that must hit the foreground and a disjoint one that must miss it.
solves: [morphological-filtering]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, k: the number of offsets in the two elements together}
  time: {worst: Θ(W H k)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, recursive: false, in_place: false, exact: true, linear: false}
prereqs: [morphological-erosion, structuring-element]
see_also: [zhang-suen-thinning, image-skeletonization, mathematical-morphology, template-matching, morphological-filtering, connected-component-labeling]
sources:
  - book: isbn:9780126372403
    title: Jean Serra, Image Analysis and Mathematical Morphology, Academic Press, 1982
    locator: Chapter II, The hit or miss transformation, erosion and opening
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: Chapter 5, Hit-or-miss and Skeletons (the binary transform, the gray extensions, thinning and thickening)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 9, Morphological Image Processing (the section on the hit-or-miss transform and the sections on thinning, thickening and pruning)
---

The hit-or-miss transform finds the pixels of a binary image where a small pattern matches exactly. The pattern is a pair of disjoint [structuring elements](/structuring-element/): a hit set $B_1$ of offsets that must be foreground and a miss set $B_2$ of offsets that must be background. The result is the intersection of two [erosions](/morphological-erosion/), $(X \ominus B_1) \cap (X^c \ominus B_2)$. It detects isolated points, corners, line ends and junctions, and it is the step from which thinning, thickening and pruning are built. The direct method costs $\Theta(WHk)$ for a $W \times H$ image and $k$ offsets in the two elements.

## In plain words

Draw a small grid of cells. Mark some cells "must be white", some "must be black", and leave the rest as "do not care". Put the center of the grid on a pixel of a black and white picture. If every "white" cell lies on a white pixel and every "black" cell lies on a black pixel, the pixel is a match. Do this for every pixel.

With a white center and eight black cells around it, the matches are the single white dots. With black above and to the right, and white to the left and below, the matches are the upper right corners of the white shapes. One pattern finds one kind of place. To find all corners, run the pattern in its four turned positions and join the results.

## The problem

The input is a binary image $X \subseteq D = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$, with the pixel centers at the integer points and $y$ growing downward, and two finite sets of offsets $B_1, B_2 \subset \mathbb{Z}^2$ with $B_1 \cap B_2 = \emptyset$. The usual rule counts the pixels outside the image as background. The output is

$$X \circledast (B_1, B_2) = \{p \in D : p + b \in X \text{ for all } b \in B_1, \text{ and } p + b \notin X \text{ for all } b \in B_2\} = (X \ominus B_1) \cap (X^c \ominus B_2).$$

The two elements are often drawn as one template with cells `1` (in $B_1$), `0` (in $B_2$) and `.` (in neither), centered on the origin. If $B_1$ and $B_2$ share an offset, no pixel can match, so the pair must be disjoint. Some books write the transform with one element $B$ and its complement in a window, $B_2 = W \setminus B$; that form has no "do not care" cells.

## The algorithm

```pseudo id=main
HMT(X, W, H, B1, B2)                    ▷ B1 ∩ B2 = ∅; the outside is background
L1  set r[p] ← 1 for every pixel p
L2  for each offset b in B1 do
L3      for each pixel p do if p + b is outside the image or X[p + b] = 0 then r[p] ← 0
L4  for each offset b in B2 do
L5      for each pixel p do if p + b is inside the image and X[p + b] = 1 then r[p] ← 0
L6  return r
```

Lines L2 and L3 are the erosion of $X$ by $B_1$ with the outside as background: a pixel survives only if all its hit cells are foreground. Lines L4 and L5 are the erosion of the complement by $B_2$ with the outside as foreground of the complement: a pixel survives only if all its miss cells are background. The two erosions write into the same result, which is their intersection. Each round is a shift of the whole image and an AND, or an AND with the negation, so packed bits give 64 pixels per word operation.

## Example

Take the 8 by 5 image $X$ of the [erosion](/morphological-erosion/) page: a 4 by 3 block from $(1, 1)$ to $(4, 3)$, a bump at $(5, 2)$ and an isolated pixel at $(7, 2)$. Three templates:

```text
isolated point    upper right corner    right end of a line
0 0 0             . 0 .                 . 0 0
0 1 0             1 1 0                 1 1 0
0 0 0             . 1 .                 . 0 0
```

| template | hit set $B_1$ | miss set $B_2$ | matches in $X$ |
|---|---|---|---|
| isolated point | $(0, 0)$ | the 8 neighbors | $(7, 2)$ |
| upper right corner | $(0, 0), (-1, 0), (0, 1)$ | $(0, -1), (1, 0)$ | $(4, 1)$ |
| right end of a line | $(0, 0), (-1, 0)$ | $(1, -1), (1, 0), (1, 1), (0, -1), (0, 1)$ | $(5, 2)$ |

The isolated pixel has 8 background neighbors. The pixel $(4, 1)$ has background above and to the right, and foreground to the left and below. The pixel $(5, 2)$ is the end of the bump: foreground to the left, background in the other five cells. The block pixel $(4, 2)$ is not a right end, because $(5, 2)$ to its right and $(4, 1)$ above it are foreground. Turning the corner template by a quarter turn three times, with $(u, v) \mapsto (-v, u)$, and joining the four results gives the four corners $(1, 1)$, $(4, 1)$, $(1, 3)$ and $(4, 3)$ of the block.

## Correctness

A pixel starts as a match at line L1 and loses the match at line L3 if a hit cell falls on background or outside the image, and at line L5 if a miss cell falls on foreground. A lost match never comes back, and every pair of a pixel and a cell is tested once, so the result is exactly the set of pixels whose hit cells are all foreground and whose miss cells are all background. The proof below also shows that this is the intersection of the two erosions, and that the transform of $X$ by $(B_1, B_2)$ equals the transform of the complement by $(B_2, B_1)$ when the outside rule is also swapped.

## Complexity

- **Time.** One test for each pair of a pixel and a cell of $B_1 \cup B_2$: $\Theta(WHk)$ in the word-RAM model, with $k = |B_1| + |B_2|$, in every case. The cells marked "do not care" cost nothing.
- **Space.** The result image, $\Theta(WH)$.
- **Lookup table for 3 by 3 templates.** Read the 9 bits of the neighborhood of each pixel as an index into a table of $2^9 = 512$ entries that holds the answer for every template at once. One pass of $\Theta(WH)$ then applies any number of 3 by 3 templates, or their union.
- **Packed bits.** $O(WHk/w)$ word operations with $w$ pixels in a word.

## Properties

- **Not increasing.** Adding foreground can destroy a match (a miss cell becomes foreground) or create one. The transform is neither increasing nor decreasing, unlike erosion, dilation, opening and closing.
- **Erosion as a special case.** With $B_2 = \emptyset$ it is the erosion of $X$ by $B_1$ with the outside as background.
- **Swap.** $X \circledast (B_1, B_2) = X^c \circledast (B_2, B_1)$, with the outside rule swapped from background to foreground.
- **Inside or outside the foreground.** If the origin is in $B_1$, every match is a foreground pixel; if it is in $B_2$, every match is a background pixel. Templates for thinning hold the origin in $B_1$, templates for thickening hold it in $B_2$.
- **Translation invariant.** Away from the border, shifting $X$ shifts the matches.
- **Exact match.** A single noise pixel inside the template breaks a match. The transform finds configurations, not similar shapes.

## Variants and improvements

- **Thinning and thickening.** Thinning removes the matches from $X$: $X \setminus (X \circledast (B_1, B_2))$, with the origin in $B_1$. Thickening adds them: $X \cup (X \circledast (B_1, B_2))$, with the origin in $B_2$. Repeating a thinning with a sequence of 8 templates, the 4 turns of an edge template and the 4 turns of a corner template, until nothing changes gives a one pixel wide skeleton; see [image skeletonization](/image-skeletonization/).
- **Parallel thinning by a lookup table.** The [Zhang-Suen algorithm](/zhang-suen-thinning/) is a thinning whose deletion rule depends only on the 3 by 3 neighborhood, so it is a union of hit-or-miss templates evaluated by one table lookup per pixel.
- **Pruning.** Thinning with the line end templates, repeated a fixed number of times, removes the short spurs of a skeleton.
- **Gray scale versions.** For a gray image, the value at $p$ can be the gap between the minimum of $f$ over $B_1$ and the maximum over $B_2$, when it is positive. Soille gives this and related definitions.
- **Rank and fuzzy versions.** To tolerate noise, require only a given number of the hit cells and of the miss cells, instead of all of them. This is a rank filter on each set.
- **Template matching.** To find a pattern that is similar rather than exact in a gray image, use [template matching](/template-matching/) by correlation instead.

## When to use it

Use the hit-or-miss transform to find small exact configurations in a binary image: isolated pixels to delete, line ends and branch points of a skeleton, corners of a shape on a grid, or a fixed glyph in a clean scan. Use it as the step of a thinning or thickening loop. For a set of 3 by 3 templates, use a lookup table instead of one transform per template. For noisy images, or patterns that change in size or angle, use a rank version or [template matching](/template-matching/).

## Pitfalls

- **Overlapping elements.** If $B_1$ and $B_2$ share a cell, the result is empty for every image, which is easy to miss in a test with few matches.
- **The border rule.** Counting the outside as foreground for $B_1$ finds false corners and line ends along the image border. Count it as background for $X$, which makes it foreground for the complement in line L5.
- **Forgetting the turned copies.** One corner template finds one kind of corner. For all corners, apply its four turns and take the union.
- **Coordinates.** With $y$ growing downward, "above" is $v = -1$. A template drawn with $y$ growing upward finds the mirror image of the pattern.
- **Thinning in parallel.** Deleting all the matches of a thinning template at once is safe for one template from a well chosen set. Deleting the matches of several templates in the same pass can disconnect a shape, as the 2 by 2 square shows for [Zhang-Suen thinning](/zhang-suen-thinning/).

## Implementations

## History

The hit or miss transformation is one of the first operations of mathematical morphology, from the work of Serra and Matheron at the École des Mines de Paris in the 1960s. Serra (1982) opens the theory of erosion and opening with it in Chapter II. Thinning and thickening by sequences of hit-or-miss templates came from the same school and from the work on hexagonal grids in the late 1960s, and are standard in the textbooks of Serra, Soille, and Gonzalez and Woods.

## References
