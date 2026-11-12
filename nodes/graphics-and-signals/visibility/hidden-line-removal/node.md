---
tag: 8DKCAP
kind: problem
slug: hidden-line-removal
name: Hidden-line removal
aliases:
- hidden edge removal
area: graphics-and-signals/visibility
level: core
summary: Given opaque polyhedra and a viewpoint, find the visible parts of their edges, so that a line drawing shows only the lines that the viewer can see.
prereqs: [hidden-surface-removal, polygon-mesh]
see_also: [roberts-hidden-line-algorithm, appel-hidden-line-algorithm, silhouette-edge, hidden-surface-removal, object-space-vs-image-space, back-face-culling, z-buffer, visibility-coherence]
sources:
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the object space algorithms for lines (Roberts, Appel and their followers) and the comparison with the surface algorithms
  - url: https://dspace.mit.edu/handle/1721.1/11589
    title: Lawrence G. Roberts, Machine Perception of Three-Dimensional Solids, PhD thesis, Massachusetts Institute of Technology, 1963
    locator: the part on drawing the solids from a new viewpoint with the hidden lines removed
  - paper: doi:10.1145/800196.806007
    title: Arthur Appel, The notion of quantitative invisibility and the machine rendering of solids, Proceedings of the 1967 22nd National Conference of the ACM, pages 387 to 393
    locator: the whole paper (quantitative invisibility and contour lines)
  - paper: doi:10.1145/10515.10544
    title: Ferenc Dévai, Quadratic bounds for hidden line elimination, Proceedings of the Second Annual Symposium on Computational Geometry, 1986, pages 269 to 275
    locator: the whole paper (the worst-case optimal bound for the problem)
---

Hidden-line removal is the problem of finding which parts of the edges of a scene the viewer can see, when the faces of the scene are opaque. The input is a set of polyhedra, or of opaque polygons, and a viewpoint. The output is a set of line segments: the visible part of each edge. It was one of the first visibility problems of computer graphics, because the first displays and plotters drew lines, not filled areas. It differs from [hidden-surface removal](/hidden-surface-removal/), which asks for the visible part of each face or the nearest face at each pixel. The two problems are close, and the visible faces give the visible edges, but a line drawing needs exact segments and does not need the colors of the faces. The classic algorithms are [Roberts'](/roberts-hidden-line-algorithm/) for convex solids and [Appel's](/appel-hidden-line-algorithm/), which counts the faces in front of each point. The plane problem of finding the parts of segments seen from below is the [lower envelope of segments](/lower-envelope-of-segments/) in geometry, a different question with its own methods.

## In plain words

Think of a drawing of a box made of wire. You can see all twelve edges, also the ones at the back, and it is hard to tell which way the box faces. If the box is solid, some edges are behind it, and a good drawing leaves them out. With many objects, one object can also hide part of an edge of another object, so an edge can be partly seen and partly hidden. Hidden-line removal is the job of finding, for each edge, the exact pieces that a person at the viewpoint would see, so that a pen or a screen draws only those pieces.

## Definition

**Input.** A scene of opaque faces in space: the boundary polygons of $s$ polyhedral solids, or a set of polygons, with $n$ edges in total. A viewpoint: an eye point $e$ for a perspective view, or a direction for a parallel view.

**Visibility.** A point $p$ of an edge is *visible* if the open segment from $e$ to $p$ meets no face at an interior point of the face. In a parallel view, the segment is replaced by the ray from $p$ toward the viewer. Points where the segment only touches the boundary of a face need a fixed convention, and the scenes below are in general position, so that such points are isolated.

**Output.** For each edge, the set of its visible points, as a list of segments, or the projection of these segments onto the picture plane. Let $k$ be the number of segments in the output.

**Quantitative form.** Appel's *quantitative invisibility* of a point is the number of faces that the segment from the eye to the point crosses. A point is visible exactly when this number is $0$. Some programs output the number, for example to draw hidden lines dashed.

## Variants

- **Convex solids.** Each solid is convex. An edge between two faces that turn away from the viewer is hidden by its own solid, and each solid can be tested on its own as a possible blocker ([Roberts' algorithm](/roberts-hidden-line-algorithm/)).
- **Which lines to draw.** A drawing can show all edges of the faces, or only the [silhouette edges](/silhouette-edge/) and the sharp creases. For smooth surfaces it shows the contour curves where the view ray is tangent to the surface.
- **Dashed hidden lines.** Technical drawings draw hidden lines dashed instead of leaving them out, which needs the full split of each edge into visible and hidden parts.
- **Object precision or image precision.** The exact problem gives segments in the coordinates of the scene. An image-precision version draws on a pixel grid: fill the faces with the background color into a [z-buffer](/z-buffer/), then draw the edges with the depth test, so only edges in front of all faces show. It is fast on graphics hardware, but the result is a picture, not a list of segments (see [object space and image space](/object-space-vs-image-space/)).
- **Terrains and surfaces given by a grid.** A height field drawn as a mesh of lines can use the order of the grid rows, front to back, and a running horizon (see [terrain visibility](/terrain-visibility/)).

## Examples

**One cube.** Take the cube $[0, 1]^3$ and the eye at $(3, 2, 5)$. The three faces $x = 1$, $y = 1$ and $z = 1$ turn toward the eye. For a single convex solid, an edge is visible exactly when one of its two faces turns toward the eye, so 9 of the 12 edges are visible. The 3 hidden edges are the ones at the corner $(0, 0, 0)$, where three faces that turn away meet. The outline of the picture is a hexagon of [silhouette edges](/silhouette-edge/).

**An edge partly hidden.** The worked example on the page of [Appel's algorithm](/appel-hidden-line-algorithm/) has a slab and a block above it, in a sheared parallel view. There the top back edge of the slab is visible on the first $5/6$ of its length and hidden behind the block on the rest. So the output must split edges, not only keep or drop them.

**Many pieces.** Put $m$ long thin horizontal bars in a row near the viewer, with gaps between them, and $m$ long thin vertical bars behind them. Each edge of a vertical bar is seen through each gap, so it shows as about $m$ visible pieces. The scene has $n = \Theta(m)$ edges, and the output has $k = \Theta(m^2) = \Theta(n^2)$ segments.

## Known algorithms

| algorithm | scene | time | idea |
|---|---|---|---|
| [Roberts](/roberts-hidden-line-algorithm/) (1963) | convex solids | $O(n s)$ edge-against-solid tests, each $O$ of the size of the solid | clip each edge against each solid by linear inequalities |
| [Appel](/appel-hidden-line-algorithm/) (1967) | closed polyhedra | $O(n (c \log c + s))$ for $c$ [silhouette edges](/silhouette-edge/) | quantitative invisibility, which changes only where an edge passes behind a silhouette edge |
| visibility map, then read the edges | polygons | $O(n^2)$ | solve [hidden-surface removal](/hidden-surface-removal/) in object precision and keep the edges of the visible regions |
| Dévai (1986) | polygons | $O(n^2)$ | worst-case optimal by the bound below |
| z-buffer line drawing | polygons | $O(n + W H)$ plus the pixels drawn, for a $W \times H$ image | image precision, in hardware |

[Back-face culling](/back-face-culling/) is a step of most object-space methods: for a closed solid, an edge between two faces that turn away is always hidden, so it can be dropped before any other test.

## Bounds

- **Output size.** The example of many bars has $k = \Theta(n^2)$, and $k = O(n^2)$ always holds, since each end of a visible segment is an end of an edge or a crossing of two edges in the projection. So $\Omega(n^2)$ time is needed in the worst case when the output is listed.
- **Worst-case optimal.** Dévai (1986) gave an $O(n^2)$ time algorithm, which matches this bound.
- **Output sensitive.** When $k$ is small, the time can depend on $k$. The edges of the visibility map are the visible pieces of the scene edges, so the output-sensitive methods on the [hidden-surface removal](/hidden-surface-removal/) page also give the visible lines.
- **Sorting.** The plane case, segments seen from far below, already needs $\Omega(n \log n)$ comparisons in the algebraic decision tree model when the visible pieces are listed from left to right, by the reduction from sorting on the hidden-surface page.

## Reductions

- **To hidden-surface removal.** The visible part of an edge is the part of it on the boundary of the visible regions of its faces. So a solution of hidden-surface removal in object precision gives the visible lines in time linear in its size.
- **To silhouette crossings.** For closed solids, the number of faces in front of a point of an edge changes only where the edge passes behind a silhouette edge in the projection, or at a vertex. So the problem reduces to the crossings in the picture plane between the edges and the silhouette edges, plus one exact count per connected part of the scene. This is the reduction that [Appel's algorithm](/appel-hidden-line-algorithm/) uses.
- **To segment-polygon clipping.** Each edge can be clipped against each face, or against each convex solid, as a set of linear inequalities in the edge parameter. This is the reduction that [Roberts' algorithm](/roberts-hidden-line-algorithm/) uses, and it costs a product of the two sizes.

## Applications

- **Technical and engineering drawings.** CAD systems draw solid models as line drawings, with hidden lines removed or dashed.
- **Pen plotters and vector output.** A device that draws lines, such as a plotter, a laser cutter or a file in a vector format, needs exact segments, not pixels.
- **Illustration.** Stylized rendering draws the visible silhouette edges and creases of a model with strokes, often in real time with coherence between frames ([silhouette edge](/silhouette-edge/)).
- **Scene understanding.** Roberts' thesis of 1963 built models of solids from a photograph and drew them from new viewpoints with the hidden lines removed.

## References
