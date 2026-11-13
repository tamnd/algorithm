---
tag: CMASJZ
kind: technique
slug: mathematical-morphology
name: Mathematical morphology
aliases:
- morphological image processing
area: graphics-and-signals/image-processing
level: advanced
summary: Build image operators from erosion and dilation with a structuring element, which compare the image with a small probe shape by minima and maxima instead of weighted sums.
prereqs: [structuring-element, morphological-erosion, morphological-dilation]
see_also: [morphological-filtering, morphological-opening, morphological-closing, hit-or-miss-transform, image-skeletonization, distance-transform, watershed-segmentation, sliding-window-maximum]
sources:
  - book: isbn:9780126372403
    title: Jean Serra, Image Analysis and Mathematical Morphology, Academic Press, 1982
    locator: Chapter II, The hit or miss transformation, erosion and opening; the later chapters on the morphological operators for sets and functions (general locator)
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: Chapter 3 (Erosion and Dilation), Chapter 4 (Opening and Closing), Chapter 5 (Hit-or-miss and Skeletons), Chapter 6 (Geodesic Transformations), Chapter 8 (Filtering), Chapter 9 (Segmentation)
  - paper: doi:10.1109/TPAMI.1987.4767941
    title: Robert M. Haralick, Stanley R. Sternberg and Xinhua Zhuang, Image analysis using mathematical morphology, IEEE Transactions on Pattern Analysis and Machine Intelligence 9(4), 532 to 550, 1987
    locator: the binary and gray scale erosion, dilation, opening and closing, the umbra, and their properties (general locator)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 9, Morphological Image Processing (general locator)
---

Mathematical morphology is a way to build image operators from two primitives, [erosion](/morphological-erosion/) and [dilation](/morphological-dilation/), each defined by a small probe shape, the [structuring element](/structuring-element/). Erosion takes at each pixel the minimum of the image over the probe placed there, and dilation the maximum. Where linear filtering asks what the weighted average near a pixel is, morphology asks whether the probe fits inside a shape, or how high it can be pushed under the gray landscape. From these two operators come the [opening](/morphological-opening/) and the [closing](/morphological-closing/), the [hit-or-miss transform](/hit-or-miss-transform/), skeletons, reconstructions, top-hats, gradients, size distributions and the [watershed](/watershed-segmentation/). The theory rests on order, not on addition: images form a lattice under the pointwise order, and erosion and dilation form an adjunction on it, which gives the properties that make the operators predictable. Matheron and Serra founded the field at the École des Mines de Paris from the 1960s.

## In plain words

Take a small stamp, such as a 3 by 3 square or a short line. Slide it over a black and white picture. Erosion keeps a pixel only if the whole stamp, placed there, lies inside the black shape, so shapes shrink and thin bits vanish. Dilation marks a pixel if the stamp placed there touches the shape, so shapes grow and small gaps close.

Combine them and you get useful tools. Shrink, then grow back, and you remove everything too small for the stamp while the big shapes come back unchanged. Grow, then shrink, and you fill small holes and cracks. For gray pictures, the same idea works with the darkest and brightest value under the stamp. The choice of stamp says what counts as small, and in which direction.

## When it applies

- **The information is in shape and size.** Objects, defects or noise differ from the rest by their width, length, orientation or by whether a probe shape fits them, rather than by their frequency content.
- **Edges must stay sharp.** Morphological operators move edges only where structures are removed, and openings and closings never blur. This suits documents, masks, industrial parts, cells, grains and maps.
- **The values are ordered but not additive.** Binary masks, labels thresholded to masks, and gray images where only the order of the values matters. Many operators commute with thresholding, so the gray result is the stack of the binary results.
- **Speed matters.** For lines, rectangles, polygons and disks, the primitives run in a constant number of comparisons per pixel, independent of the size of the probe.
- **It does not apply well** when the noise is additive and Gaussian and the goal is to average it out, which is the job of [smoothing filters](/image-smoothing/), or when the decision depends on a learned model rather than a shape rule.

## The template

The two primitives for a flat structuring element $B$, a finite set of offsets, on an image $f$ over a rectangle $D$, ignoring offsets that leave $D$:

$$\varepsilon_B(f)(p) = \min_{b \in B} f(p + b), \qquad \delta_B(f)(p) = \max_{b \in B} f(p - b).$$

```pseudo id=main
MORPHOLOGY(f, task)
L1   choose B: a shape that fits the structures to keep and does not fit those to remove
L2   e ← ERODE(f, B)                ▷ e(p) = min of f(p + b), b in B; a moving minimum for segments
L3   d ← DILATE(f, B)               ▷ d(p) = max of f(p − b), b in B; a moving maximum for segments
L4   γ ← DILATE(e, B)               ▷ opening: removes the bright parts that B does not fit
L5   φ ← ERODE(d, B)                ▷ closing: fills the dark parts that B does not fit
L6   combine for the task: γ, φ, γ(φ) or φ(γ) to filter; f − γ or φ − f for small details; d − e for edges
L7   measure or segment the result: threshold, label the components, count, or flood with a watershed
```

**Why it works: the adjunction.** For every pair of images $f$ and $g$,

$$\delta_B(f) \le g \iff f \le \varepsilon_B(g),$$

since both sides say that $f(p - b) \le g(p)$ for all $p$ and $b$. From this one fact follow the properties every pipeline relies on. Erosion and dilation are increasing and commute with infima and suprema respectively. The opening $\gamma_B = \delta_B\varepsilon_B$ is anti-extensive, and the closing $\varphi_B = \varepsilon_B\delta_B$ is extensive. And $\varepsilon_B\delta_B\varepsilon_B = \varepsilon_B$ and $\delta_B\varepsilon_B\delta_B = \delta_B$, so the opening and the closing are idempotent: $\gamma_B\gamma_B = \delta_B(\varepsilon_B\delta_B\varepsilon_B) = \delta_B\varepsilon_B = \gamma_B$.

**Duality.** With the complement $f^c = \top - f$ and the reflected element $\check B = \{-b : b \in B\}$, $\varepsilon_B(f)^c = \delta_{\check B}(f^c)$. So every statement about bright structures has a twin about dark structures, and the code for one primitive gives the other.

**Example.** On the gray row $(2, 2, 7, 2, 2, 2, 0, 2, 2, 5, 5, 5, 2, 2)$ with the segment of 3 pixels centered at the origin, line L4 removes the narrow peak 7, line L5 fills the narrow pit 0, and both keep the plateau of three 5s exactly; the white top-hat $f - \gamma$ is 5 at the peak and 0 elsewhere. The [morphological filtering](/morphological-filtering/) page works this example in full.

## Classic examples

- [Morphological opening](/morphological-opening/) and [closing](/morphological-closing/): the template with L4 or L5 as the result.
- [Morphological filtering](/morphological-filtering/): alternating sequential filters, reconstructions, top-hats, gradients and granulometries, all compositions of L2 and L3.
- [Hit-or-miss transform](/hit-or-miss-transform/): two erosions, of the image and of its complement, with a pair of disjoint elements, intersected to find a local pattern.
- [Image skeletonization](/image-skeletonization/) and [Zhang-Suen thinning](/zhang-suen-thinning/): the morphological skeleton is a union of differences of erosions and openings, and thinning removes the hits of hit-or-miss templates.
- [Distance transform](/distance-transform/): thresholds of the distance transform are erosions and dilations by disks of every radius at once.
- [Watershed segmentation](/watershed-segmentation/): the flooding of a morphological gradient $\delta - \varepsilon$.
- [Sliding window maximum](/sliding-window-maximum/): the moving maximum that computes flat dilation by a segment in constant time per pixel.

## Variations

- **Binary, flat gray and non-flat.** For sets, min and max become intersection and union. For gray images with a flat element, the template is unchanged. A non-flat element adds a height $b(x)$: $\varepsilon(f)(p) = \min_x (f(p + x) - b(x))$, which models rolling a ball or a paraboloid under the landscape.
- **Geodesic operators.** Dilate under a mask, $\min(\delta(f), g)$, and repeat until stable: this is reconstruction, which keeps or removes whole connected structures without changing their outlines.
- **Connected and attribute operators.** Area openings and max-tree filters work on the connected components of the threshold sets, with no structuring element at all.
- **Other lattices.** Color images, label images, graphs and meshes carry morphology once an order and an adjunction are defined on them, though color has no single natural order.
- **Morphology on point sets and polygons.** In geometry, dilation is the [Minkowski sum](/minkowski-sum/), used for configuration space obstacles.

## Pitfalls

- **The reflection.** Some books define dilation as $\max_b f(p + b)$, without the minus sign. Then the duality and the adjunction hold with $\check B$ in a different place, and the results differ for elements that are not symmetric. Fix one convention and test it on an asymmetric element.
- **The origin.** An element that does not contain the origin shifts the image; erosion then need not be below $f$, and dilation need not be above it. Openings and closings are still anti-extensive and extensive.
- **The border.** Pixels outside the image must be given a value or ignored. Ignoring them in a closing can grow the foreground along the border; padding with background, filtering and cropping avoids it. State the choice, because the duality holds only if the border is treated in a dual way.
- **The size of the element.** A direct scan costs $|B|$ comparisons per pixel. Large disks and squares need a decomposition into segments or a distance transform, or the pipeline becomes slow.
- **Order matters.** $\gamma\varphi$ and $\varphi\gamma$ differ, and so do sequences with growing elements in different orders.
- **Discrete disks are not round.** A 3 by 3 square repeated $n$ times gives a square, and a cross gives a diamond. For isotropic results, use a digital disk, an octagon from alternating square and cross, or a Euclidean distance transform.

## Exercises

1. Prove the adjunction $\delta_B(f) \le g \iff f \le \varepsilon_B(g)$ for the conventions of the template, and derive from it that $\varepsilon_B$ commutes with pointwise minima.
2. Prove $\varepsilon_B\delta_B\varepsilon_B = \varepsilon_B$ using only the adjunction, and conclude that the opening is idempotent.
3. Prove the duality $\varepsilon_B(f)^c = \delta_{\check B}(f^c)$, and give a 1D example with $B = \{0, 1\}$ where it fails if the reflection is left out.
4. Compute the opening and the closing of the binary row `##.###.#.####` by the segment $\{-1, 0, 1\}$, ignoring the outside, and check that applying each one again changes nothing.
5. Show that the flat erosion of a row of $n$ pixels by a segment of $k$ pixels can be computed with at most 3 comparisons per pixel for every $k$, by splitting the row into blocks of length $k$ and using prefix and suffix minima.

## References
