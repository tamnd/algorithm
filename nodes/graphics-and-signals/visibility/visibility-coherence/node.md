---
tag: 5SA4T0
kind: concept
slug: visibility-coherence
name: Visibility coherence
aliases:
- object coherence
- scanline coherence
- area coherence
- depth coherence
- frame coherence
area: graphics-and-signals/visibility
level: core
summary: Exploit the fact that visibility changes little between nearby points, lines, or frames.
prereqs: [hidden-surface-removal, triangle-rasterization]
see_also: [watkins-scanline-algorithm, warnock-algorithm, z-buffer, occlusion-culling, hierarchical-z-buffer, occlusion-query, painters-algorithm, object-space-vs-image-space]
sources:
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the discussion of coherence and of how each of the ten algorithms uses it
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, 1990
    locator: Chapter 15, Section 15.2 (techniques for efficient visible-surface algorithms, coherence)
  - paper: doi:10.1145/166117.166147
    title: Ned Greene, Michael Kass and Gavin Miller, Hierarchical Z-buffer visibility, Proceedings of SIGGRAPH 1993
    locator: the use of the visible set of the previous frame (temporal coherence)
  - paper: doi:10.1111/j.1467-8659.2004.00793.x
    title: Jiří Bittner, Michael Wimmer, Harald Piringer and Werner Purgathofer, Coherent hierarchical culling, hardware occlusion queries made useful, Computer Graphics Forum 23(3), 2004 (Eurographics 2004)
    locator: the use of the visibility of the previous frame to schedule occlusion queries
---

*Coherence* is the tendency of the visible scene to change little between points that are near each other: neighboring pixels, neighboring scan lines, neighboring regions of the screen and consecutive frames. A visibility algorithm *exploits coherence* when it computes a result once and then updates it in small, cheap steps, in place of computing it again from the start for each sample. Sutherland, Sproull and Schumacker in 1974 named coherence as the main tool of efficient [hidden surface removal](/hidden-surface-removal/). They showed that the ten algorithms of their survey differ mostly in which kind of coherence they use. The kinds have names: object, face, edge, scan-line, area, depth and frame coherence.

## In plain words

When you look across a room, the wall you see at one point is almost always the same wall you see at the point next to it. When you blink, the picture after the blink is almost the same as before it. A program that draws pictures can use this. It does not need to ask "what is in front here?" from the start at each pixel. It can remember the answer from the pixel next door, or from the last frame, and only fix the small part that changed.

Coherence is not a guarantee. At the edge of an object the answer does change. The good algorithms find those few places quickly and do the cheap update everywhere else.

## The idea

The kinds of coherence below are the ones that Sutherland, Sproull and Schumacker, and later Foley and others, list. Each one is a statement about a scene. It says that some quantity is constant, or changes in a simple way, over a set of nearby samples.

- **Object coherence.** If two objects are wholly separate, for example their [bounding boxes](/axis-aligned-bounding-box/) do not overlap on the screen, then no part of one can hide a part of the other. One test on the objects replaces many tests on their faces.
- **Face coherence.** The properties of a face, such as its depth and its color, change smoothly across it. A plane's depth is a linear function of the screen position.
- **Edge coherence.** An edge that is visible on one side of a point usually stays visible, or invisible, along its length. It changes only where it crosses behind another face.
- **Scan-line coherence.** The set of visible spans on one scan line is usually almost the same as on the line before. The [Watkins scan-line algorithm](/watkins-scanline-algorithm/) keeps an *active edge table*, sorted by $x$, and updates it from line to line in place of finding all edges again.
- **Area coherence.** A region of the screen is often covered by one face only. The [Warnock algorithm](/warnock-algorithm/) tests a whole square at a time and subdivides only where the square is not simple.
- **Depth coherence.** Neighboring samples of one face have nearby depths, which can be found by adding a constant. Once two faces are ordered at one sample, they usually keep that order nearby.
- **Frame coherence.** Consecutive images are nearly the same, because the eye and the objects move only a little in a frame. The visible set, or the depth order, of the last frame is a good first guess for the next one. This is also called *temporal coherence*.

Coherence makes the *expected* cost small, not the worst-case cost. A scene of thin, interleaved strips, such as grass or a picket fence seen from far away, has little coherence. An algorithm that relies on coherence then does more work than a simple method like the [z-buffer](/z-buffer/), which uses only face coherence and pays a fixed cost for each sample.

## Examples

**Depth along a scan line.** A face on the plane $2x + 3y + 6z = 60$ has the depth $z = (60 - 2x - 3y)/6$. At the pixel $(0, 0)$ the depth is $10$. One step to the right changes $z$ by $-\tfrac{2}{6} = -\tfrac13$, and one step down changes it by $-\tfrac{3}{6} = -\tfrac12$. So a rasterizer computes $z$ with one addition for each pixel: $10, \tfrac{29}{3}, \tfrac{28}{3}, 9, \dots$. This is face and depth coherence, and it is how [triangle rasterization](/triangle-rasterization/) interpolates depth.

**Edges between scan lines.** An edge from $(0, 0)$ to $(10, 4)$ meets the scan line $y$ at $x = 2.5\,y$. The scan-line algorithm keeps the value $x$ for the current line and adds $2.5$ for each new line, in place of solving for the intersection again. The order of the active edges by $x$ changes only where two edges cross. So a sort of the active edges at each new line starts from a list that is almost sorted.

**An almost sorted depth order.** A [painter's algorithm](/painters-algorithm/) sorts $n$ objects by depth for each frame. If the eye moves a little, only a few pairs of objects change their order. Insertion sort on the order of the last frame then costs $O(n + k)$ for $k$ pairs that changed, in place of $\Theta(n \log n)$ for a new sort. With $n = 10\,000$ objects and $k = 50$ changes, that is about $10^4$ steps against about $1.3 \times 10^5$ comparisons.

**Last frame's visible set.** [Occlusion culling](/occlusion-culling/) with [occlusion queries](/occlusion-query/) first draws the objects that were visible in the last frame. They are probably visible again, and they fill the depth buffer with good occluders before the other objects are tested. Greene, Kass and Miller used this order for the [hierarchical z-buffer](/hierarchical-z-buffer/) in 1993. The coherent hierarchical culling method of Bittner and others in 2004 also uses the last result of each node to decide which queries to issue and when to wait for their answers.

**When coherence fails.** Seen from far away, a fence of 200 thin posts gives a scan line that crosses 400 edges. The active edge table on each line changes in many places, and the Warnock algorithm subdivides down to single pixels along the fence. There the coherence methods give little gain.

## Where it is used

- **Scan-line and area methods.** The classic image-space methods of about 1970, such as the [Watkins](/watkins-scanline-algorithm/) and [Warnock](/warnock-algorithm/) algorithms, are mostly ways of using scan-line, edge and area coherence.
- **Rasterization.** Each GPU interpolates depth and the other attributes by incremental or plane-equation steps across a triangle, which is face coherence. Tiled hardware also uses area coherence. For example, a block of pixels where the triangle is behind all the stored depths is skipped as a whole.
- **Culling across frames.** Occlusion culling, [portal culling](/portal-culling/) with cached portal results, and the update of [potentially visible sets](/potentially-visible-set/) while streaming use frame coherence.
- **Ray tracing.** Neighboring rays tend to hit the same nodes of an acceleration structure and the same triangles. This is [ray coherence](/ray-coherence/), and [ray packet tracing](/ray-packet-tracing/) traces such rays together.

## References
