---
tag: TJT6MZ
kind: concept
slug: object-space-vs-image-space
name: Object space versus image space
aliases:
- object precision
- image precision
area: graphics-and-signals/visibility
level: core
summary: A visibility method works in object space when it decides with the exact geometry, and in image space when it decides once per pixel sample.
prereqs: [hidden-surface-removal]
see_also: [z-buffer, painters-algorithm, warnock-algorithm, watkins-scanline-algorithm, hidden-line-removal, roberts-hidden-line-algorithm, newell-newell-sancha-algorithm, ray-casting]
sources:
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the classification of the ten algorithms into object-space, list-priority and image-space methods, and the comparison of their costs
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 15, the introduction (object-precision and image-precision algorithms, and their costs)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 23.7 (the depth buffer as the image-space method of GPUs)
---

A [hidden surface removal](/hidden-surface-removal/) method works in *object space* (at object precision) when it compares the surfaces with their exact geometry and outputs exact visible regions. It works in *image space* (at image precision) when it decides visibility once for each [pixel](/pixel/) sample. Sutherland, Sproull and Schumacker used this split in 1974 to classify ten hidden surface algorithms, with the list-priority methods between the two. The split tells what a method costs, what its output is, and what happens when the resolution changes.

## In plain words

There are two ways to find out what is in front in a picture.

In the first way, you work with the shapes themselves. You take two shapes, find where one covers the other, and cut away the hidden part. At the end you have the exact outline of each visible piece. You can print it at any size, and it stays sharp. But you may have to compare each shape with each other shape.

In the second way, you work with the dots of the screen. For each dot, you ask which shape is nearest there. The answer is only as good as the dots: if you make the picture bigger, you must ask again for the new dots. But the work is the same simple step at each dot, and machines can do it very fast.

## The idea

Fix a scene of $n$ opaque polygons and an image of $W \times H$ pixels, where pixel $(i, j)$ is the point sample at $(i + \tfrac12, j + \tfrac12)$.

**Object space.** The method works with the polygons in the coordinates of the scene, at the precision of the arithmetic (exact rationals in theory, floating point in practice). Its basic step compares two polygons, or a polygon and an edge, and its output is the visibility map: the visible region of each polygon, as polygons. A direct method compares each pair, so it needs $\Theta(n^2)$ pair tests, and the output itself can have $\Theta(n^2)$ size. The result does not depend on the screen: it can be scaled, plotted or rasterized later at any resolution.

**Image space.** The method works with the samples of the screen. Its basic step decides, for one sample, which polygon is nearest there. The direct method tests each polygon at each sample, for $\Theta(n W H)$ tests. The [z-buffer](/z-buffer/) does it in $\Theta(W H + n + P)$ time, where $P$ is the number of covered samples, by visiting for each polygon only the samples it covers. The output is correct only at the samples. Between the samples it says nothing, so a narrow polygon can fall between two centers, and edges show [aliasing](/aliasing/).

**List priority.** Some methods find an order of the polygons in object space, and then let the frame buffer resolve the overlaps in image space by drawing in that order. The [painter's algorithm](/painters-algorithm/), the [Newell-Newell-Sancha algorithm](/newell-newell-sancha-algorithm/) and [BSP tree visibility](/bsp-tree-visibility/) work this way. Sutherland, Sproull and Schumacker treat them as a third class between the two.

**Coherence.** Both kinds save work by coherence: nearby pixels, nearby scanlines and the next frame usually see the same surfaces. Image-space methods use it most, for example the span coherence of [Watkins' algorithm](/watkins-scanline-algorithm/) and the area coherence of [Warnock's algorithm](/warnock-algorithm/). See [visibility coherence](/visibility-coherence/).

| | object space | image space |
|---|---|---|
| basic step | compare two polygons | find the nearest polygon at one sample |
| direct cost | $\Theta(n^2)$ pair tests | $\Theta(n W H)$ tests |
| output | exact visible regions | one answer per sample |
| change of resolution | the output stays valid | run again |
| robustness | geometric predicates must be exact or careful | each decision is local to one sample |
| typical methods | Roberts, Appel, McKenna | z-buffer, Warnock, Watkins, ray casting |

## Examples

**Cost at a common size.** For $n = 1000$ polygons and a $1920 \times 1080$ image, the direct object-space method does $n(n-1)/2 = 499{,}500$ pair tests. The direct image-space method does $n W H = 2{,}073{,}600{,}000$ point tests. The z-buffer does about $W H + P$ steps, and $P$ is $W H$ times the average number of surfaces on a pixel ray. These are counts of basic steps, not times: a pair test is much more work than a point test.

**A thin polygon.** A triangle of width $0.3$ pixels that lies between two columns of pixel centers is part of the object-space output, but an image-space method with one sample per pixel does not draw it at all. With 4 samples per pixel it may cover some of them. The object-space answer does not change.

**Hidden lines.** A line drawing for a plotter or a vector file needs the visible parts of the edges as segments. Object-space methods, such as the [Roberts](/roberts-hidden-line-algorithm/) and [Appel](/appel-hidden-line-algorithm/) hidden line algorithms, give them directly. An image-space method gives pixels, which must be traced back into segments. See [hidden line removal](/hidden-line-removal/).

**Ray casting.** [Ray casting](/ray-casting/) is image space: it does one [closest-hit query](/closest-hit-query/) per sample. With a [bounding volume hierarchy](/bounding-volume-hierarchy/) the cost of a query on typical scenes grows slowly with $n$, which makes image-space cost almost independent of the scene size in practice; this is an observed behavior, not a worst-case bound.

## Where it is used

Real-time rendering is image space: GPUs use the [z-buffer](/z-buffer/) with one or more samples per pixel, and add object-space [visibility culling](/visibility-culling/) to skip whole objects early. Film renderers are image space, with many samples per pixel, by ray tracing or by a z-buffer with fragment lists such as the [A-buffer](/a-buffer/). Object space is used where the output must be exact or independent of resolution: hidden line drawings in CAD, vector output, and the computational geometry of [hidden surface removal](/hidden-surface-removal/), where worst-case bounds are proved in terms of $n$ and the output size.

## References
