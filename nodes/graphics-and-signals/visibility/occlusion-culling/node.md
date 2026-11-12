---
tag: J4XCZM
kind: algorithm
slug: occlusion-culling
name: Occlusion culling
aliases:
- depth-buffer occlusion culling
area: graphics-and-signals/visibility
level: advanced
summary: Draw objects near to far and skip each object whose bounding box is behind the depth already drawn at every pixel it covers. A visible object is never skipped.
solves: [visibility-culling]
model: real-ram
complexity:
  vars: {n: the number of objects, t: the number of triangles, A: the number of pixels}
  time: {worst: O(n log n + (n + t) A), average: O(n log n + (n + t) A), best: Θ(n log n + A)}
  space: {extra: Θ(n + A)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1993
  people: [Ned Greene, Michael Kass, Gavin Miller]
  note: Greene, Kass and Miller tested the boxes of an octree against a z-buffer pyramid, near to far, and skipped the boxes that the depth already drawn hid. Later systems did the same test with occlusion queries on the GPU.
prereqs: [z-buffer, bounding-volume, axis-aligned-bounding-box, hidden-surface-removal]
see_also: [hierarchical-z-buffer, occlusion-query, frustum-culling, back-face-culling, portal-culling, potentially-visible-set, early-depth-test, visibility-coherence]
sources:
  - paper: doi:10.1145/166117.166147
    title: Ned Greene, Michael Kass and Gavin Miller, Hierarchical Z-buffer visibility, Proceedings of SIGGRAPH 1993, pages 231 to 238
    locator: the whole paper
  - paper: doi:10.1111/j.1467-8659.2004.00793.x
    title: Jiří Bittner, Michael Wimmer, Harald Piringer and Werner Purgathofer, Coherent hierarchical culling, hardware occlusion queries made useful, Computer Graphics Forum 23(3), 2004, pages 615 to 624
    locator: the whole paper
  - paper: doi:10.1109/TVCG.2003.1207447
    title: Daniel Cohen-Or, Yiorgos L. Chrysanthou, Cláudio T. Silva and Frédo Durand, A survey of visibility for walkthrough applications, IEEE Transactions on Visualization and Computer Graphics 9(3), 2003, pages 412 to 431
    locator: the whole paper (the classes conservative, aggressive and approximate, and the from-point methods)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 19, Section 19.7 (Occlusion Culling), page 840
---

Occlusion culling skips the objects that other objects hide. The form on this page draws the objects from near to far into a [z-buffer](/z-buffer/). Before it draws an object, it tests the object's [bounding box](/axis-aligned-bounding-box/) against the depth buffer. If each pixel that the box covers already holds a depth strictly nearer than the nearest point of the box, the object is hidden, and the renderer skips it. The test is *conservative*: it never skips a visible object, but it can draw an object that turns out to be hidden. So the image is the same as with no culling. The [hierarchical z-buffer](/hierarchical-z-buffer/) makes the box test fast, and GPU [occlusion queries](/occlusion-query/) do it in hardware. It is the hardest case of [visibility culling](/visibility-culling/), because whether an object is hidden depends on the other objects.

## In plain words

In a city street you see the near buildings, and they hide most of the city behind them. A renderer that draws each building in the city spends most of its time on buildings that no one sees.

Occlusion culling draws the near things first. After that, for each farther thing, it puts a box around it and asks: at every pixel of this box, is there already something nearer than the box? If yes, the thing is surely hidden, and the renderer skips it.

Because the test uses the box, not the object, it can say "maybe visible" for an object that is in fact hidden. Then the object is drawn and the z-buffer hides it. It never says "hidden" for an object that shows.

## The problem

The view is orthographic along the $z$ axis, and a larger $z$ is nearer to the viewer; a perspective view is first changed to this form by the projection. The image has $W \times H = A$ pixels, and pixel $(i, j)$ is a point sample at its center $(i + \tfrac12, j + \tfrac12)$. The input is $n$ objects, each a set of triangles, $t$ triangles in total, with no triangle seen edge on. The box of an object is the smallest axis-aligned box that contains it, with nearest depth $z_{\max}$.

An object is *visible* when, at some pixel center, one of its triangles covers the center with the largest depth among all triangles that cover it (a tie counts as visible). The output is a set of objects to draw, which must contain each visible object, and the image that a z-buffer makes from them. A smaller set is better. The coordinates are real numbers; the implementation uses exact fractions.

## The algorithm

```pseudo id=main
OCCLUSION-CULL(objects o[1 .. n], W, H)
L1  D[c] ← −∞ and image[c] ← background for each pixel c; drawn ← an empty list
L2  order ← the objects sorted by z_max of their boxes, nearest first
L3  for each object o in order do
L4      R ← the pixels whose centers are in the xy rectangle of box(o)
L5      if each pixel c in R has D[c] > z_max(box(o)) then
L6          skip o and continue at L3                    ▷ hidden by what is drawn
L7      for each triangle of o and each pixel c whose center it covers, let z be its depth at c
L8          if z > D[c] then D[c] ← z; image[c] ← o          ▷ the z-buffer test
L9      append o to drawn
L10 return drawn, image
```

Line L2 puts the likely occluders first, so that the depth buffer fills early. Lines L4 to L6 are the occlusion test: they compare the nearest depth of the box with the depth already in the buffer, pixel by pixel. If $R$ is empty, the box covers no pixel center, and the object cannot be visible. Lines L7 and L8 are the ordinary [z-buffer](/z-buffer/). The implementation stops the test of line L5 at the first pixel that is not hidden.

In a real renderer, the test of line L5 is not done pixel by pixel. A [hierarchical z-buffer](/hierarchical-z-buffer/) keeps the farthest depth of each block of pixels, so a few lookups decide a box; an [occlusion query](/occlusion-query/) draws the box with depth writes off and counts the pixels that pass. The objects are usually the nodes of a hierarchy, so that one test can skip a whole group.

## Example

The image has $8 \times 6$ pixels. There are four objects.

- A, the wall: the rectangle from $(0, 0)$ to $(8, 4)$ at $z = 5$.
- B: the triangle $(1, 1, 1)$, $(4, 1, 2)$, $(1, 3, 2)$, with $z_{\max} = 2$.
- C: the rectangle from $(5, 2)$ to $(7, 6)$ at $z = 3$.
- D: the triangle $(2, 0)$, $(4, 0)$, $(2, 5)$ at $z = 4$.

The order of line L2 is A, D, C, B.

| step | object | pixels in $R$ | test of line L5 | result |
|---|---|---|---|---|
| 1 | A | 32 | buffer empty | drawn, writes 32 pixels |
| 2 | D | 10 | the 2 pixels of row 4 are empty | drawn, writes 0 pixels |
| 3 | C | 8 | the 4 pixels of rows 4 and 5 are empty | drawn, writes 4 pixels |
| 4 | B | 6 | each has $D = 5 > 2$ | skipped |

D is the conservative case. Its box reaches row 4 (centers at $y = 4.5$), where the wall does not reach, but the triangle covers only the centers $(2.5, 0.5)$, $(3.5, 0.5)$, $(2.5, 1.5)$, $(2.5, 2.5)$ and $(2.5, 3.5)$, all behind the wall. So D is drawn but writes nothing. The final image, with row 5 at the top and `.` for the background, is

```
.....CC.
.....CC.
AAAAAAAA
AAAAAAAA
AAAAAAAA
AAAAAAAA
```

which is the image of a full z-buffer.

## Correctness

The depth $D[c]$ only increases. If line L5 skips $o$, then at each pixel center $c$ that $o$ covers, $c \in R$ and $D[c] > z_{\max} \ge$ the depth of $o$ at $c$; later $D[c]$ is still larger. So $o$ is strictly behind another triangle at each pixel it covers, and it is not visible, not even in a tie. A full z-buffer that draws all objects in the same order has, at each step, a buffer at least as near as this one, so it also writes nothing for $o$. Hence the two runs give the same image, and each visible object is drawn. The order of line L2 helps the speed but not the correctness: the proof holds for each order. The full proofs are below. The tests check the depth buffer, the image and the drawn set against an exact per-pixel depth test of all triangles.

## Complexity

The sort takes $O(n \log n)$ time and the initialization $\Theta(A)$. The test of an object reads at most $A$ pixels, and the drawing of a triangle at most $A$ pixels, so the worst case is $O(n \log n + (n + t) A)$. With scan conversion, the drawing costs the number of pixels that the drawn triangles cover. The gain is that skipped objects cost only the test. In a dense scene, such as a city seen from the street, most objects are skipped, and the cost depends on the visible part of the scene, not on its size. The best case, for example when the first object covers the whole image and the boxes of the others are small, is $\Theta(n \log n + A)$. A hierarchy of objects and a z-buffer pyramid reduce both terms. The extra space is the depth buffer and the order, $\Theta(n + A)$.

## Properties

- **Conservative.** A visible object is never skipped. The image is the image of the z-buffer with no culling.
- **Not exact.** An object can pass the test and still be hidden, as D shows, because its box is larger than it.
- **Occluder fusion.** The depth buffer holds the union of all drawn objects, so two walls side by side can hide an object that neither wall hides alone. Methods that test one occluder at a time miss this case.
- **From-point and online.** The test works for the current viewpoint, after the near objects are drawn, with no preprocessing. Compare the [potentially visible set](/potentially-visible-set/), which is computed for a region of viewpoints before the run.
- **Order dependent speed.** A far-to-near order culls nothing. A near-to-far order by box depth is a cheap approximation of the best order.

## Variants and improvements

- **Hierarchical z-buffer.** Greene, Kass and Miller in 1993 kept a pyramid of the farthest depth of square blocks, and tested the boxes of an octree, near to far, against it. See [hierarchical z-buffer](/hierarchical-z-buffer/).
- **Occlusion queries.** The GPU draws the box with color and depth writes off and reports the number of pixels that pass the depth test; zero means hidden. See [occlusion query](/occlusion-query/). The result arrives later than the request, so a renderer that waits for each result stalls.
- **Coherent hierarchical culling.** Bittner, Wimmer, Piringer and Purgathofer in 2004 used the visibility of the last frame to hide the delay of the queries. Nodes that were visible are drawn at once and queried for the next frame, and the queries of the other nodes are interleaved with the drawing. This uses [visibility coherence](/visibility-coherence/) between frames.
- **Occlusion maps.** Keep a coverage map and a depth estimate of a chosen set of large occluders, and test boxes against both. The hierarchical occlusion maps of Zhang, Manocha, Hudson and Hoff in 1997 are of this kind; they also allow an approximate test that drops nearly hidden objects.
- **Software occlusion culling.** Draw a few simple occluders into a small depth buffer on the CPU, and test boxes there before the GPU work starts.
- **Precomputed visibility.** For walls and rooms, use [portal culling](/portal-culling/) at run time, or a [potentially visible set](/potentially-visible-set/) computed before the run.

## When to use it

Use occlusion culling when the scene has much depth complexity and large occluders, such as cities, buildings and terrain, and the cost of drawing is high. Do [frustum culling](/frustum-culling/) first, because it is cheaper. For an open scene with little occlusion, the tests cost more than they save. For indoor scenes with rooms and doors, [portal culling](/portal-culling/) is often simpler and stronger.

## Pitfalls

- **The far depth of the box.** The test must use the nearest point of the box, $z_{\max}$ in this convention. A test with the farthest point drops an object that pokes through the occluder; the tests show a triangle from $z = 2$ to $z = 8$ behind a wall at $z = 5$ that is visible but would be dropped.
- **A test that is not strict.** With $D[c] \ge z_{\max}$ in place of $D[c] > z_{\max}$, an object at the same depth as the occluder is dropped. If the depth test of the renderer keeps ties, this changes the image.
- **Waiting for the GPU.** An occlusion query answers later. A renderer that waits for each answer loses more time than it saves. Use the results of the last frame, as coherent hierarchical culling does.
- **Aggressive tests.** A test with a lower resolution buffer, or with the result of the last frame used as final, can drop a visible object for a frame. Such methods are *approximate*, not conservative; know which one you use.
- **Bad order.** Far-to-near order culls nothing. Draw the large near occluders first.

## Implementations

## History

Early visible surface methods already used the idea that a near object can hide a far one with no further work, for example the list priority methods. Greene, Kass and Miller in 1993 gave the form on this page for large scenes: an octree traversed near to far, each node box tested against a z-buffer pyramid, so that the cost follows the visible part of the scene. Zhang, Manocha, Hudson and Hoff in 1997 gave hierarchical occlusion maps. Graphics hardware later added occlusion queries, and Bittner, Wimmer, Piringer and Purgathofer in 2004 showed how to use them without stalls by temporal coherence. The survey of Cohen-Or, Chrysanthou, Silva and Durand in 2003 sorts these methods into conservative, aggressive and approximate ones, and into from-point and from-region ones.

## References
