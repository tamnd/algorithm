---
tag: K5KSY9
kind: problem
slug: hidden-surface-removal
name: Hidden surface removal
aliases:
- visible-surface determination
- visibility determination
area: graphics-and-signals/visibility
level: core
summary: Given opaque surfaces and a viewpoint, find which part of each surface is visible, either as exact regions or as the nearest surface at each pixel.
prereqs: [pixel]
see_also: [z-buffer, painters-algorithm, object-space-vs-image-space, hidden-line-removal, warnock-algorithm, watkins-scanline-algorithm, bsp-tree-visibility, visibility-culling]
sources:
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the statement of the problem, the view of hidden surface removal as a sort, and the comparison of the ten algorithms
  - paper: doi:10.1145/27625.27627
    title: Michael McKenna, Worst-case optimal hidden-surface removal, ACM Transactions on Graphics 6(1), 1987, pages 19 to 28
    locator: the O(n^2) algorithm and the matching lower bound on the output size
  - paper: doi:10.1145/102377.112141
    title: Micha Sharir and Mark H. Overmars, A simple output-sensitive algorithm for hidden surface removal, ACM Transactions on Graphics 11(1), 1992, pages 1 to 11
    locator: the main result (triangles with a known depth order) and its extensions
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 15, Visible-Surface Determination (the problem, the two precisions, and the classic algorithms)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 12, Binary Space Partitions (the painter's algorithm and hidden surface removal)
---

Hidden surface removal is the problem of finding, for a scene of opaque surfaces and a viewpoint, which part of each surface the viewer sees. The answer is either exact (the visible region of each polygon, in *object precision*) or sampled (the nearest surface at each [pixel](/pixel/) center, in *image precision*). Each renderer of opaque scenes solves it, and Sutherland, Sproull and Schumacker showed in 1974 that each classic method is a sort of the surfaces by depth, done in a different order and at a different precision.

## In plain words

You stand in a room and look at the things in it. The table hides part of the floor, and the chair hides part of the table. A picture of the room must show, at each place, only the thing that is nearest to you there. Hidden surface removal is the job of finding out, for each place in the picture, which thing that is.

You can ask the question in two ways. In the first way, you want the exact outline of each visible piece, as a drawing with lines. In the second way, you only want to know the nearest thing at each dot of a screen.

The job is hard because a thing can be in front of another thing at one place and behind it at another place. Two planks that cross are an example.

## Definition

**Input.** A scene of $n$ opaque planar polygons in 3D, with $N$ edges in total, and a view: a viewpoint and a projection onto an image plane. After the viewing transform and the perspective divide, the view direction is the $z$ axis, a point $(x, y, z)$ projects to $(x, y)$, and a smaller $z$ is nearer. A projective map takes lines to lines and keeps the order of depths along each viewing ray, so the problem is the same after the transform. The depth of a polygon $p$ at a point $q = (x, y)$ of its projection is $z_p(q)$.

**Visible point.** A point $q$ of the image plane *sees* polygon $p$ if $q$ is in the projection of $p$ and $z_p(q) < z_r(q)$ for each other polygon $r$ whose projection contains $q$. Ties happen only on a set of measure zero, unless two polygons are coplanar and overlap; a method must state its rule for them.

**Object precision.** The output is the *visibility map*: the subdivision of the image plane into maximal connected regions in which one polygon is seen (or none). Each region is a polygon, and the size $k$ of the output is the number of its vertices and edges.

**Image precision.** The image is $W \times H$ pixels, and pixel $(i, j)$ is the point sample at its center $(i + \tfrac12, j + \tfrac12)$. The output is, at each pixel, the polygon that the center sees, or the background. A center on a shared edge goes to one polygon by a fill rule, for example the [top-left fill rule](/top-left-fill-rule/).

**Cost model.** An object-precision method is measured in the [real RAM](/real-ram/) by $n$, $N$ and $k$. An image-precision method is measured by $n$, $W H$ and the number $P$ of covered pixel centers, summed over the polygons.

## Variants

- **The two precisions.** Object precision gives an exact answer that does not depend on the screen; image precision gives one answer per sample and can use the [frame buffer](/frame-buffer/) as its data structure. See [object space and image space](/object-space-vs-image-space/).
- **Hidden line removal.** Draw only the visible parts of the edges, for a line drawing. See [hidden line removal](/hidden-line-removal/).
- **Transparency.** With surfaces that are not opaque, the output needs all the surfaces on a ray, in depth order. [Depth peeling](/depth-peeling/) and the [A-buffer](/a-buffer/) solve this version.
- **Antialiased output.** The output is the visible area of each polygon inside each pixel, not only at the center. The [A-buffer](/a-buffer/) and [Warnock's algorithm](/warnock-algorithm/) with subpixel windows give it.
- **Seen from a light.** A point is lit when it is visible from the light. This is [shadow determination](/shadow-determination/).
- **Conservative visibility.** Find a superset of the visible polygons fast, and leave the exact part to a later step. This is [visibility culling](/visibility-culling/).
- **Curved surfaces and terrains.** The input is a parametric surface, or a height field seen from a point.

## Examples

**Interpenetration.** The triangles $a = ((0,0,0), (8,0,0), (4,6,12))$ and $b = ((0,6,0), (8,6,0), (4,0,12))$ have depths $z = 2y$ and $z = 12 - 2y$ on their planes. Their projections overlap in a diamond. Above the line $y = 3$ the viewer sees $a$, and below it the viewer sees $b$. So no single order of the two triangles is right, and a method that draws whole polygons in an order fails. The [z-buffer](/z-buffer/) page draws this scene pixel by pixel.

**Cyclic overlap.** Three long planks lie so that the first is over the second, the second over the third and the third over the first, each at a different place. No triangle passes through another, but again no order is right. Methods that sort polygons, such as the [Newell-Newell-Sancha algorithm](/newell-newell-sancha-algorithm/) and [BSP tree visibility](/bsp-tree-visibility/), cut a polygon to break the cycle.

**A large output.** Put $m$ long thin horizontal rectangles in front of $m$ long thin vertical rectangles, so that the projections form a grid. Each vertical rectangle shows $m + 1$ visible pieces, between and beyond the horizontal ones. The visibility map has $m(m + 1) + m = m(m + 2)$ visible faces, for $n = 2m$ polygons, which is $n^2/4 + n$. For $m = 4$ this is 24 faces from 8 rectangles.

## Known algorithms

| algorithm | year | precision | idea |
|---|---|---|---|
| [Roberts](/roberts-hidden-line-algorithm/) | 1963 | object | hidden lines of convex bodies |
| [Appel](/appel-hidden-line-algorithm/) | 1967 | object | quantitative invisibility along the edges |
| [Ray casting](/ray-casting/) | 1968 | image | a [closest-hit query](/closest-hit-query/) for the ray through each pixel |
| [Warnock](/warnock-algorithm/) | 1969 | image | subdivide the screen until each window is simple |
| [Watkins](/watkins-scanline-algorithm/) | 1970 | image | scanline order, spans between edge crossings |
| [Newell, Newell and Sancha](/newell-newell-sancha-algorithm/) | 1972 | mixed | sort by depth, test and split, paint far to near |
| [Z-buffer](/z-buffer/) | 1974 | image | one depth per pixel, any order |
| [BSP tree visibility](/bsp-tree-visibility/) | 1980 | object order | a tree of planes gives a back-to-front order from any viewpoint |
| [A-buffer](/a-buffer/) | 1984 | image | fragment lists with coverage masks per pixel |

The [painter's algorithm](/painters-algorithm/) is the plain depth sort that the Newell-Newell-Sancha algorithm repairs. The years are those of the first descriptions on the linked pages.

## Bounds

- **Output size.** The visibility map of $n$ polygons can have $\Theta(n^2)$ faces, by the grid example. It has $O(N^2)$ size in each case, because each vertex of the map is a vertex of the input or a crossing of two projected edges. So $\Omega(n^2)$ time is necessary in the worst case for object precision.
- **Worst-case optimal.** McKenna (1987) gave an $O(n^2)$ time algorithm for object precision, which matches the lower bound.
- **Output sensitive.** When the output is small, the time can depend on $k$. Sharir and Overmars (1992) solve the problem for $n$ triangles with a known depth order in $O(n k^{1/2} \log n)$ time.
- **Image precision.** The [z-buffer](/z-buffer/) takes $\Theta(W H + n + P)$ time, with no sort. $P$ can be as large as $n W H$, when each polygon covers the whole screen.
- **The plane version.** For $n$ segments in the plane seen from $y = -\infty$, the visible part is the lower envelope of the segments. It has $O(n \alpha(n))$ pieces, and it can be computed in $O(n \log n)$ time (see [lower envelope of segments](/lower-envelope-of-segments/)). When the output lists the pieces from left to right, $\Omega(n \log n)$ comparisons are necessary in the algebraic decision tree model, by the reduction from sorting below.

## Reductions

- **From sorting.** Given distinct numbers $x_1, \ldots, x_n$, make the short horizontal segment $[x_r, x_r + \varepsilon]$ at height $r$, with $\varepsilon$ less than the least gap. Each segment is visible, and the visible pieces from left to right list the numbers in sorted order. So the plane version, with the output in order, is at least as hard as the [sorting problem](/sorting-problem/).
- **To ray queries.** Image precision is $W H$ [closest-hit queries](/closest-hit-query/), one for the ray through each pixel center. This is [ray casting](/ray-casting/).
- **To depth sorting.** If the polygons have a valid visibility order, painting in that order solves the problem. Sutherland, Sproull and Schumacker describe each method as a sort in $y$, $x$ and $z$, in some order and with some coherence.
- **Shadows.** The lit points of a scene are the points that the light sees, so [shadow determination](/shadow-determination/) is hidden surface removal from the light. [Shadow mapping](/shadow-mapping/) uses a z-buffer from the light.

## Applications

Hidden surface removal is a step of each 3D renderer: games and other interactive programs (on GPUs, with the [z-buffer](/z-buffer/) and [visibility culling](/visibility-culling/)), film rendering, CAD and technical drawing (in object precision, often as [hidden line removal](/hidden-line-removal/)), flight simulators (where the early scanline and list-priority methods were made for hardware), shadows, and the visibility analysis of terrain.

## References
